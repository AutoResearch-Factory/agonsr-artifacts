"""Perovskite ABX3 stability classification problem.

This is the single source of truth for the problem definition:
  1. Data loading and feature extraction
  2. Fitness function (BFGS param fitting + decision tree)
  3. Prompt variant loading

Usage:
    from problems.perovskite_abx3.problem import load_data, build_fitness_fn, load_prompt

    variant = load_prompt()
    X_train, y_train, X_test, y_test, df = load_data()
    fitness_fn = build_fitness_fn(fitness="fisher", depth=1)
"""

import builtins
from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

_PROBLEM_DIR = Path(__file__).resolve().parent
_TABLE_S1 = _PROBLEM_DIR / "data" / "TableS1.csv"
_PROMPT_YAML = _PROBLEM_DIR / "prompt.yaml"
_FEATURE_COLS = ("rA (Ang)", "rB (Ang)", "rX (Ang)", "nA", "nB", "nX")


def load_prompt(path: Path | str | None = None) -> dict:
    """Load prompt.yaml and return as a dict."""
    return yaml.safe_load(Path(path or _PROMPT_YAML).read_text())


def load_train_data() -> tuple[np.ndarray, np.ndarray]:
    """Load TableS1.csv and return only (X_train, y_train)."""
    df = pd.read_csv(_TABLE_S1).copy()
    df["nX"] = df["nX"].abs()
    train_df = df[df["is_train"] == 1].reset_index(drop=True)
    X_train = train_df[list(_FEATURE_COLS)].to_numpy(dtype=float)
    y_train = train_df["exp_label"].to_numpy(dtype=int)
    return X_train, y_train


def load_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, pd.DataFrame]:
    """Load TableS1.csv and return (X_train, y_train, X_test, y_test, df).

    The original CSV uses nX as negative integers; we take abs() so the
    LLM-generated formulas receive positive values for all oxidation states.
    """
    df = pd.read_csv(_TABLE_S1).copy()
    df["nX"] = df["nX"].abs()

    train_df = df[df["is_train"] == 1].reset_index(drop=True)
    test_df = df[df["is_train"] == -1].reset_index(drop=True)

    X_train = train_df[list(_FEATURE_COLS)].to_numpy(dtype=float)
    y_train = train_df["exp_label"].to_numpy(dtype=int)
    X_test = test_df[list(_FEATURE_COLS)].to_numpy(dtype=float)
    y_test = test_df["exp_label"].to_numpy(dtype=int)
    return X_train, y_train, X_test, y_test, df


def _compile_equation(code: str):
    ns = {"np": np, "__builtins__": builtins.__dict__}
    try:
        builtins.exec(builtins.compile(code, "<equation>", "exec"), ns)  # noqa: S102
    except Exception:
        return None
    return ns.get("equation") or ns.get("descriptor")


def build_fitness_fn(
    X_train: np.ndarray,
    y_train: np.ndarray,
    max_nparams: int = 4,
    fitness: str = "fisher",
    depth: int = 1,
) -> Callable[[str], float | None]:
    """Return a fitness function: (code_string) -> float | None.

    All problem-specific data is closed over at construction time.
    """
    from scipy.optimize import minimize
    from sklearn.tree import DecisionTreeClassifier

    X, y = X_train, y_train

    def fitness_fn(code: str) -> float | None:
        fn = _compile_equation(code)
        if fn is None:
            return None

        def _vals(p):
            try:
                v = fn(X[:, 0], X[:, 1], X[:, 2], X[:, 3], X[:, 4], X[:, 5], p)
            except Exception:
                return None
            v = np.asarray(v, dtype=float).ravel()
            if v.shape != y.shape or not np.isfinite(v).all():
                return None
            return v

        def _loss(p):
            v = _vals(p)
            if v is None:
                return 1e6
            if fitness == "mse":
                return float(np.mean((v - y) ** 2))
            if fitness == "fisher":
                pos, neg = v[y > 0], v[y < 0]
                if len(pos) < 2 or len(neg) < 2:
                    return 1e6
                return -float((pos.mean() - neg.mean()) ** 2 / (pos.var() + neg.var() + 1e-12))
            if fitness == "logistic":
                margins = np.clip(y * v, -500, 500)
                return float(np.mean(np.log1p(np.exp(-margins))))
            raise ValueError(f"unknown fitness {fitness}")

        best = None
        for init in (np.ones(max_nparams), 0.5 * np.ones(max_nparams), 2.0 * np.ones(max_nparams)):
            try:
                r = minimize(_loss, init, method="BFGS", options={"maxiter": 100})
            except Exception:
                continue
            if np.isfinite(r.fun) and (best is None or r.fun < best.fun):
                best = r
        if best is None:
            return None
        v_star = _vals(best.x)
        if v_star is None:
            return None
        clf = DecisionTreeClassifier(max_depth=depth, random_state=0)
        clf.fit(v_star.reshape(-1, 1), y)
        return float(clf.score(v_star.reshape(-1, 1), y))

    return fitness_fn


def train_only_evaluate(
    code: str,
    X_train: np.ndarray,
    y_train: np.ndarray,
    *,
    fitness: str = "fisher",
    depth: int = 1,
    max_nparams: int = 4,
    n_splits: int = 5,
    random_state: int = 42,
) -> dict:
    """Evaluate a formula using stratified K-fold CV on training data only.

    Returns dict with val_accuracy (mean across folds) and train_accuracy.
    No test data is seen or returned.
    """
    from scipy.optimize import minimize
    from sklearn.model_selection import StratifiedKFold
    from sklearn.tree import DecisionTreeClassifier

    fn = _compile_equation(code)
    if fn is None:
        return {"val_accuracy": float("nan"), "train_accuracy": float("nan")}

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    val_accs = []
    train_accs = []

    for train_idx, val_idx in skf.split(X_train, y_train):
        X_tr, X_val = X_train[train_idx], X_train[val_idx]
        y_tr, y_val = y_train[train_idx], y_train[val_idx]

        def _vals(X, p):
            try:
                v = fn(X[:, 0], X[:, 1], X[:, 2], X[:, 3], X[:, 4], X[:, 5], p)
            except Exception:
                return None
            v = np.asarray(v, dtype=float).ravel()
            if v.shape[0] != X.shape[0] or not np.isfinite(v).all():
                return None
            return v

        def _loss(p):
            v = _vals(X_tr, p)
            if v is None:
                return 1e6
            if fitness == "fisher":
                pos, neg = v[y_tr > 0], v[y_tr < 0]
                if len(pos) < 2 or len(neg) < 2:
                    return 1e6
                return -float(
                    (pos.mean() - neg.mean()) ** 2 / (pos.var() + neg.var() + 1e-12)
                )
            if fitness == "mse":
                return float(np.mean((v - y_tr) ** 2))
            if fitness == "logistic":
                margins = np.clip(y_tr * v, -500, 500)
                return float(np.mean(np.log1p(np.exp(-margins))))
            raise ValueError(f"unknown fitness {fitness}")

        best = None
        for init in (
            np.ones(max_nparams),
            0.5 * np.ones(max_nparams),
            2.0 * np.ones(max_nparams),
        ):
            try:
                r = minimize(_loss, init, method="BFGS", options={"maxiter": 100})
            except Exception:
                continue
            if np.isfinite(r.fun) and (best is None or r.fun < best.fun):
                best = r

        if best is None:
            continue
        v_tr = _vals(X_tr, best.x)
        v_val = _vals(X_val, best.x)
        if v_tr is None or v_val is None:
            continue

        clf = DecisionTreeClassifier(max_depth=depth, random_state=0)
        clf.fit(v_tr.reshape(-1, 1), y_tr)
        train_accs.append(float(clf.score(v_tr.reshape(-1, 1), y_tr)))
        val_accs.append(float(clf.score(v_val.reshape(-1, 1), y_val)))

    if not val_accs:
        return {"val_accuracy": float("nan"), "train_accuracy": float("nan")}

    return {
        "val_accuracy": float(np.mean(val_accs)),
        "train_accuracy": float(np.mean(train_accs)),
    }


def posthoc_evaluate(
    code: str,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    df_all: pd.DataFrame,
    *,
    fitness: str = "fisher",
    depth: int = 1,
    max_nparams: int = 4,
) -> dict:
    """Evaluate a formula on train/test/overall + per-anion breakdown.

    Returns a dict with test_accuracy, overall_accuracy, per_anion_accuracy.
    """
    from scipy.optimize import minimize
    from sklearn.tree import DecisionTreeClassifier

    fn = _compile_equation(code)
    if fn is None:
        return {
            "test_accuracy": float("nan"),
            "overall_accuracy": float("nan"),
            "per_anion_accuracy": {},
        }

    def _vals(X, p):
        try:
            v = fn(X[:, 0], X[:, 1], X[:, 2], X[:, 3], X[:, 4], X[:, 5], p)
        except Exception:
            return None
        v = np.asarray(v, dtype=float).ravel()
        if v.shape[0] != X.shape[0] or not np.isfinite(v).all():
            return None
        return v

    def _loss(p):
        v = _vals(X_train, p)
        if v is None:
            return 1e6
        if fitness == "fisher":
            pos, neg = v[y_train > 0], v[y_train < 0]
            if len(pos) < 2 or len(neg) < 2:
                return 1e6
            return -float((pos.mean() - neg.mean()) ** 2 / (pos.var() + neg.var() + 1e-12))
        if fitness == "mse":
            return float(np.mean((v - y_train) ** 2))
        if fitness == "logistic":
            margins = np.clip(y_train * v, -500, 500)
            return float(np.mean(np.log1p(np.exp(-margins))))
        raise ValueError(f"unknown fitness {fitness}")

    best = None
    for init in (np.ones(max_nparams), 0.5 * np.ones(max_nparams), 2.0 * np.ones(max_nparams)):
        try:
            r = minimize(_loss, init, method="BFGS", options={"maxiter": 100})
        except Exception:
            continue
        if np.isfinite(r.fun) and (best is None or r.fun < best.fun):
            best = r
    if best is None:
        return {
            "test_accuracy": float("nan"),
            "overall_accuracy": float("nan"),
            "per_anion_accuracy": {},
        }

    p_star = best.x
    v_train = _vals(X_train, p_star)
    if v_train is None:
        return {
            "test_accuracy": float("nan"),
            "overall_accuracy": float("nan"),
            "per_anion_accuracy": {},
        }

    clf = DecisionTreeClassifier(max_depth=depth, random_state=0)
    clf.fit(v_train.reshape(-1, 1), y_train)

    v_test = _vals(X_test, p_star)
    if v_test is None:
        return {
            "test_accuracy": float("nan"),
            "overall_accuracy": float("nan"),
            "per_anion_accuracy": {},
        }
    test_acc = float((clf.predict(v_test.reshape(-1, 1)) == y_test).mean())

    df_all_copy = df_all.copy()
    df_all_copy["nX"] = df_all_copy["nX"].abs()
    X_all = df_all_copy[list(_FEATURE_COLS)].to_numpy(dtype=float)
    y_all = df_all_copy["exp_label"].to_numpy(dtype=int)
    v_all = _vals(X_all, p_star)
    overall_acc = (
        float((clf.predict(v_all.reshape(-1, 1)) == y_all).mean())
        if v_all is not None
        else float("nan")
    )

    test_df = df_all[df_all["is_train"] == -1].reset_index(drop=True)
    per_anion = {}
    for a in ("O", "F", "Cl", "Br", "I"):
        mask = test_df["X"].to_numpy() == a
        if mask.any():
            per_anion[a] = float((clf.predict(v_test[mask].reshape(-1, 1)) == y_test[mask]).mean())

    return {
        "test_accuracy": test_acc,
        "overall_accuracy": overall_acc,
        "per_anion_accuracy": per_anion,
    }
