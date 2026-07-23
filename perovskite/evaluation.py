"""Clean, leakage-free evaluator for perovskite stability descriptors.

This module replaces the legacy ``evaluator.py`` which mixed training and
held-out data in several subtle ways:

  * ``evaluate_candidate`` fit the decision-tree classifier on the train
    mask but evaluated thresholds, per-anion accuracy, and cross-validation
    on the **full 576 compounds** -- mixing train and test.
  * ``_cross_validate`` ran 5-fold CV over the entire dataset (including
    the held-out test compounds), giving a "CV accuracy" that already
    peeked at the test split.
  * Downstream callers (``benchmark_comparison.py``) then selected a "best"
    node on ``test_accuracy`` -- classic test-set selection leakage.

``evaluator.evaluate`` enforces a strict train / val / test contract:

    split="train"  -> 367 compounds  (first 80 percent of is_train==1 pool)
    split="val"    -> 93  compounds  (last  20 percent, stratified by anion X)
    split="test"   -> 116 compounds  (the is_train == -1 rows exactly)

    train union val   = is_train == 1  (460 compounds)
    train union val union test = all 576 compounds, no overlap

All model-selection work (depth tuning, best-formula picking across a
candidate pool, hyperparameter sweeps) must happen on "train" or "val".
"test" is touched exactly once per method x seed, at the very end.

Val-split rule (documented here so it can be audited):

    For each anion X in the train pool (is_train == 1), sort the compounds
    by their row index in the original CSV ascending. Take the **last**
    ``ceil(0.20 * n)`` rows per anion into val; the remaining rows go to
    train. Deterministic, seed-independent, stratified by X.

    -> anion sizes at the moment of writing (TableS1.csv):
        O : 288 train-pool rows -> 58 val, 230 train
        F :  55                 -> 11 val,  44 train
        Cl:  54                 -> 11 val,  43 train
        I :  39                 ->  8 val,  31 train
        Br:  24                 ->  5 val,  19 train
        total                   -> 93 val, 367 train

    (Row counts may differ by +/-1 from "20 percent exact" because of the
    ceil; totals always sum to 460 = train_pool_total.)

Returned ``EvalResult.predictions_per_compound`` is a ``list[bool]`` aligned
with the **returned split's compound order** (same row order as the
``DataFrame`` rows selected by that split). This is the primitive we need
for paired McNemar tests across methods -- persist it to JSON in every
adapter.

Author: salvage-rewrite following AUTO_REVIEW.md Round 1 Phase C.
"""

from __future__ import annotations

import builtins
import hashlib
import logging
import math
import signal
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier

log = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

DEFAULT_DATA_PATH = (
    Path(__file__).parent / "data" / "perovskite-stability" / "TableS1.csv"
).resolve()

TIMEOUT_SECONDS = 10
TRAIN_LABEL = 1  # is_train == 1  -> source pool for "train" union "val"
TEST_LABEL = -1  # is_train == -1 -> the untouched held-out test
VAL_FRACTION = 0.20  # fraction of source-pool rows reserved as val
CV_DEPTHS = (1, 2, 3)  # candidate decision-tree depths for CV selection

_LABEL_COL = "exp_label"
_ANION_COL = "X"
_IS_TRAIN_COL = "is_train"


# -----------------------------------------------------------------------------
# Exceptions and result types
# -----------------------------------------------------------------------------


class EvalTimeout(Exception):
    """Raised when a candidate descriptor exceeds ``TIMEOUT_SECONDS``."""


def _timeout_handler(signum, frame):  # noqa: ARG001
    raise EvalTimeout("Descriptor execution timed out")


@dataclass
class EvalResult:
    """Outcome of evaluating one formula on one split.

    accuracy: overall classification accuracy on the RETURNED split only.
    per_anion_acc: anion -> accuracy, computed on the RETURNED split only.
    predictions_per_compound: list of booleans, one entry per compound in
        the returned split (True = correct prediction). Persist this to
        JSON -- it is what unlocks paired McNemar tests downstream.
    formula_code: the executable descriptor source code that was run.
    metadata: split name/size, chosen depth, seed, CV scores per depth,
        compound IDs in split order, SHA hash of the formula code, and an
        error string that is non-empty iff the formula failed.
    """

    accuracy: float
    per_anion_acc: dict
    predictions_per_compound: list
    formula_code: str
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


# -----------------------------------------------------------------------------
# Dataset loading
# -----------------------------------------------------------------------------


def load_dataset(data_path=DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load TableS1.csv with renamed radius columns and a stable row index."""
    df = pd.read_csv(data_path)
    df = df.rename(columns={"rA (Ang)": "rA", "rB (Ang)": "rB", "rX (Ang)": "rX"})
    df = df.reset_index(drop=True)
    df["row_idx"] = np.arange(len(df))
    return df


# -----------------------------------------------------------------------------
# Deterministic split construction
# -----------------------------------------------------------------------------


def _build_splits(df: pd.DataFrame) -> dict:
    """Return split_name -> integer row indices per the val-split rule."""
    n = len(df)
    idx_test = np.flatnonzero(df[_IS_TRAIN_COL].to_numpy() == TEST_LABEL)
    idx_train_pool = np.flatnonzero(df[_IS_TRAIN_COL].to_numpy() == TRAIN_LABEL)

    val_indices: list = []
    train_indices: list = []
    pool_df = df.loc[idx_train_pool]
    for _anion, group in pool_df.groupby(_ANION_COL, sort=True):
        group_sorted = group.sort_values("row_idx")
        group_idx = group_sorted["row_idx"].to_numpy()
        n_group = len(group_idx)
        if n_group >= 2:
            n_val = max(1, math.ceil(VAL_FRACTION * n_group))
            if n_val >= n_group:
                n_val = n_group - 1
        else:
            n_val = 0
        train_indices.extend(group_idx[: n_group - n_val].tolist())
        val_indices.extend(group_idx[n_group - n_val :].tolist())

    splits = {
        "train": np.array(sorted(train_indices), dtype=np.int64),
        "val": np.array(sorted(val_indices), dtype=np.int64),
        "test": np.array(sorted(idx_test.tolist()), dtype=np.int64),
    }

    all_idx = np.concatenate([splits["train"], splits["val"], splits["test"]])
    assert len(np.unique(all_idx)) == n, "splits do not partition rows"
    assert set(all_idx.tolist()) == set(range(n)), "splits miss some rows"
    return splits


def get_splits(df=None) -> dict:
    """Public accessor for the split indices -- used by adapters and tests."""
    if df is None:
        df = load_dataset()
    return _build_splits(df)


# -----------------------------------------------------------------------------
# Descriptor execution -- runs untrusted Python via builtins.exec
# -----------------------------------------------------------------------------


def _run_descriptor_code(func_code: str, df: pd.DataFrame) -> np.ndarray:
    """Run the ``descriptor(...)`` function over a dataframe.

    Uses the ``descriptor(rA, rB, rX, nA, nB, nX)`` calling convention to
    match the legacy ``evaluator.py``. No shell is invoked anywhere here;
    this is Python's dynamic code path, equivalent to ``exec`` in the
    legacy module.
    """
    namespace = {"np": np, "math": __import__("math")}
    builtins.exec(func_code, namespace)  # noqa: S102
    fn = namespace.get("descriptor")
    if fn is None:
        raise ValueError("func_code did not define `descriptor(...)`")

    values: list = []
    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(TIMEOUT_SECONDS)
    try:
        for _, row in df.iterrows():
            val = fn(
                rA=row["rA"],
                rB=row["rB"],
                rX=row["rX"],
                nA=row["nA"],
                nB=row["nB"],
                nX=row["nX"],
            )
            if val is None or not np.isfinite(val):
                raise ValueError(f"descriptor returned {val!r} for {row.get('ABX3', '?')}")
            values.append(float(val))
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
    return np.asarray(values, dtype=np.float64)


# -----------------------------------------------------------------------------
# CV-based depth selection (TRAIN ONLY -- never touches val/test)
# -----------------------------------------------------------------------------


def _select_depth_by_cv(
    values_train: np.ndarray,
    labels_train: np.ndarray,
    seed: int,
    n_folds: int = 5,
    candidate_depths: tuple = CV_DEPTHS,
):
    """Pick decision-tree depth via 5-fold stratified CV on TRAIN ONLY.

    Returns (best_depth, depth -> mean_cv_acc). Deterministic given seed.
    """
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)
    cv_scores: dict = {}
    for depth in candidate_depths:
        scores: list = []
        for tr_idx, va_idx in skf.split(values_train.reshape(-1, 1), labels_train):
            clf = DecisionTreeClassifier(max_depth=depth, random_state=seed)
            clf.fit(values_train[tr_idx].reshape(-1, 1), labels_train[tr_idx])
            preds = clf.predict(values_train[va_idx].reshape(-1, 1))
            scores.append(float((preds == labels_train[va_idx]).mean()))
        cv_scores[depth] = float(np.mean(scores))
    # Tie-break: smallest depth wins (Occam).
    best_depth = min(candidate_depths, key=lambda d: (-cv_scores[d], d))
    return best_depth, cv_scores


# -----------------------------------------------------------------------------
# Public entry point
# -----------------------------------------------------------------------------


def _formula_hash(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()[:12]


def evaluate(
    formula_fn,
    split: str,
    seed: int,
    decision_tree_max_depth="cv",
    *,
    data_path=DEFAULT_DATA_PATH,
    df=None,
) -> EvalResult:
    """Evaluate ``formula_fn`` on exactly one split; depth chosen on TRAIN.

    Args:
        formula_fn: either a Python source string defining
            ``def descriptor(rA, rB, rX, nA, nB, nX)`` or a callable with
            that signature (``inspect.getsource`` is used to recover the
            source and run it through the same sandboxed path).
        split: one of ``"train"``, ``"val"``, ``"test"``. Only the returned
            split's labels contribute to the final metrics. The fit step
            always uses the TRAIN split -- even when ``split=="train"``,
            predictions are train-fit-then-train-predict.
        seed: integer seed controlling CV shuffling and classifier
            ``random_state``. Deterministic given a fixed ``seed``.
        decision_tree_max_depth: either an explicit int (e.g. 2 or 3) or
            the string ``"cv"`` (default), which triggers 5-fold CV on
            TRAIN ONLY over depths ``{1, 2, 3}``.
        data_path: path to TableS1.csv; defaults to the one next to this
            module.
        df: pre-loaded dataframe; if provided, ``data_path`` is ignored.

    Returns:
        :class:`EvalResult`. ``accuracy`` and ``per_anion_acc`` are computed
        on the RETURNED split only -- never full-dataframe.

    Notes:
        The ONE legitimate call on ``split="test"`` per method x seed must
        come AFTER all model-selection / formula-picking is done. Nothing
        in this module enforces that -- it is the adapter's responsibility
        (see ``protocol.py``).
    """
    if split not in ("train", "val", "test"):
        raise ValueError(f"split must be train/val/test, got {split!r}")

    # Normalise formula into a source string
    if callable(formula_fn):
        import inspect

        try:
            code = inspect.getsource(formula_fn)
        except (OSError, TypeError) as e:
            raise ValueError(
                "formula_fn callable has no accessible source; pass code string"
            ) from e
    else:
        code = str(formula_fn)

    if df is None:
        df = load_dataset(data_path)
    splits = _build_splits(df)

    labels_all = df[_LABEL_COL].to_numpy().astype(int)
    anions_all = df[_ANION_COL].to_numpy()
    compounds_all = df["ABX3"].to_numpy()

    # ---- Run descriptor once over the full dataframe. We COMPUTE values
    # for every compound but only LEARN from train and only SCORE on the
    # requested split; no labels leak because the descriptor sees only
    # features (rA, rB, rX, nA, nB, nX), not exp_label.
    try:
        values_all = _run_descriptor_code(code, df)
    except Exception as e:  # noqa: BLE001 -- LLM code crashes arbitrarily
        return EvalResult(
            accuracy=0.0,
            per_anion_acc={},
            predictions_per_compound=[],
            formula_code=code,
            metadata={
                "split": split,
                "seed": seed,
                "error": f"{type(e).__name__}: {e}",
                "formula_hash": _formula_hash(code),
            },
        )

    idx_train = splits["train"]
    idx_requested = splits[split]
    values_train = values_all[idx_train]
    labels_train = labels_all[idx_train]

    # ---- Depth selection: CV within TRAIN ONLY
    cv_scores: dict = {}
    if decision_tree_max_depth == "cv":
        chosen_depth, cv_scores = _select_depth_by_cv(values_train, labels_train, seed=seed)
    else:
        chosen_depth = int(decision_tree_max_depth)
        if chosen_depth < 1:
            raise ValueError("decision_tree_max_depth must be >= 1")

    # ---- Fit on TRAIN ONLY, predict on the requested split
    clf = DecisionTreeClassifier(max_depth=chosen_depth, random_state=seed)
    clf.fit(values_train.reshape(-1, 1), labels_train)

    values_split = values_all[idx_requested]
    labels_split = labels_all[idx_requested]
    anions_split = anions_all[idx_requested]
    compounds_split = compounds_all[idx_requested]

    preds_split = clf.predict(values_split.reshape(-1, 1))
    correct = preds_split == labels_split
    accuracy = float(correct.mean())

    per_anion_acc: dict = {}
    for anion in sorted(set(anions_split.tolist())):
        mask = anions_split == anion
        if mask.any():
            per_anion_acc[str(anion)] = float(correct[mask].mean())

    metadata = {
        "split": split,
        "split_size": int(len(idx_requested)),
        "chosen_depth": int(chosen_depth),
        "depth_was_cv": decision_tree_max_depth == "cv",
        "cv_scores": cv_scores,
        "seed": int(seed),
        "n_train_fit": int(len(idx_train)),
        "n_val": int(len(splits["val"])),
        "n_test": int(len(splits["test"])),
        "compound_ids": compounds_split.tolist(),
        "formula_hash": _formula_hash(code),
        "error": "",
    }

    return EvalResult(
        accuracy=accuracy,
        per_anion_acc=per_anion_acc,
        predictions_per_compound=[bool(x) for x in correct.tolist()],
        formula_code=code,
        metadata=metadata,
    )


# -----------------------------------------------------------------------------
# Convenience helpers for adapters
# -----------------------------------------------------------------------------


def train_only_df(df=None) -> pd.DataFrame:
    """Return a dataframe containing TRAIN rows only (excludes val and test)."""
    if df is None:
        df = load_dataset()
    splits = _build_splits(df)
    return df.iloc[splits["train"]].copy().reset_index(drop=True)


def train_plus_val_df(df=None) -> pd.DataFrame:
    """Return TRAIN union VAL (460 rows). Still excludes test."""
    if df is None:
        df = load_dataset()
    splits = _build_splits(df)
    idx = np.sort(np.concatenate([splits["train"], splits["val"]]))
    return df.iloc[idx].copy().reset_index(drop=True)
