"""Evaluation helpers for the metal/nonmetal descriptor problem."""

import inspect
import re
from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd

PROBLEM_DIR = Path(__file__).resolve().parent
TRAIN_DAT = PROBLEM_DIR / "data" / "train.dat"
FEATURE_COLS = ["IE_A", "IE_B", "X_A", "X_B", "xA", "xB", "Vcell_over_Vatom"]
N_METALS = 188
N_NONMETALS = 111


def load_data(path: str | Path = TRAIN_DAT) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    df = pd.read_csv(path, sep=r"\s+")
    if len(df) != N_METALS + N_NONMETALS:
        raise ValueError(f"expected {N_METALS + N_NONMETALS} rows, got {len(df)}")
    X = df[FEATURE_COLS].to_numpy(dtype=float)
    y = np.array([1] * N_METALS + [-1] * N_NONMETALS)
    return X, y, df


def get_feature_arrays(df: pd.DataFrame) -> dict[str, np.ndarray]:
    arrays = {col: df[col].to_numpy(dtype=float) for col in FEATURE_COLS}
    arrays["packing"] = 1.0 / arrays["Vcell_over_Vatom"]
    return arrays


def compute_descriptor(code: str, df: pd.DataFrame, params: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray] | None:
    """Evaluate candidate code and return descriptor arrays (d1, d2), or None."""
    feature_arrays = get_feature_arrays(df)
    try:
        stripped = code.strip()
        if stripped.startswith("def descriptor"):
            ns = {"np": np, "__builtins__": __builtins__}
            exec(code, ns)
            fn = ns["descriptor"]
            sig_params = list(inspect.signature(fn).parameters.keys())
            call_args = {k: feature_arrays[k] for k in sig_params if k in feature_arrays}
            if "params" in sig_params:
                call_args["params"] = params if params is not None else np.ones(4)
            d1, d2 = fn(**call_args)
        else:
            lines = stripped.splitlines()
            ctx = {"np": np, "sqrt": np.sqrt, "log": np.log, "abs": np.abs, "exp": np.exp}
            ctx.update(feature_arrays)
            if params is not None:
                ctx["params"] = params
            if len(lines) == 2:
                d1 = eval(lines[0].strip(), {"__builtins__": None}, ctx)
                d2 = eval(lines[1].strip(), {"__builtins__": None}, ctx)
            else:
                ns = dict(ctx)
                exec(code, {"__builtins__": None, "np": np}, ns)
                d1, d2 = ns["d1"], ns["d2"]
        d1 = np.asarray(d1, dtype=float)
        d2 = np.asarray(d2, dtype=float)
        if d1.shape != (len(df),) or d2.shape != (len(df),):
            return None
        if not (np.all(np.isfinite(d1)) and np.all(np.isfinite(d2))):
            return None
        return d1, d2
    except Exception:
        return None


def evaluate_pair(d1: np.ndarray, d2: np.ndarray, y: np.ndarray) -> dict:
    """Evaluate a descriptor pair with LinearSVC train accuracy and LOOCV."""
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import LinearSVC

    X_feat = np.column_stack([d1, d2])
    sc = StandardScaler()
    Xs = sc.fit_transform(X_feat)
    clf = LinearSVC(C=1.0, max_iter=10000, dual="auto")
    clf.fit(Xs, y)
    preds = clf.predict(Xs)
    train_acc = float((preds == y).mean())

    loo_correct = 0
    for i in range(len(y)):
        mask = np.ones(len(y), dtype=bool)
        mask[i] = False
        sc_i = StandardScaler()
        Xtr = sc_i.fit_transform(X_feat[mask])
        Xte = sc_i.transform(X_feat[i : i + 1])
        clf_i = LinearSVC(C=1.0, max_iter=10000, dual="auto")
        clf_i.fit(Xtr, y[mask])
        loo_correct += int(clf_i.predict(Xte)[0] == y[i])

    misclassified = np.where(preds != y)[0].tolist()
    return {
        "train_accuracy": train_acc,
        "loocv_accuracy": loo_correct / len(y),
        "n_misclassified": len(misclassified),
        "misclassified_indices": misclassified,
    }


def count_params(code: str) -> int:
    indices = re.findall(r"params\[(\d+)\]", code)
    return max((int(i) for i in indices), default=-1) + 1


def fit_params(code: str, df: pd.DataFrame, y: np.ndarray) -> np.ndarray | None:
    """Fit params[] by maximizing LinearSVC training accuracy."""
    from scipy.optimize import minimize
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import LinearSVC

    n_params = count_params(code)
    if n_params == 0:
        return None

    def score(p: np.ndarray) -> float:
        result = compute_descriptor(code, df, params=p)
        if result is None:
            return 0.0
        d1, d2 = result
        X_feat = np.column_stack([d1, d2])
        Xs = StandardScaler().fit_transform(X_feat)
        clf = LinearSVC(C=1.0, max_iter=10000, dual="auto")
        clf.fit(Xs, y)
        return float((clf.predict(Xs) == y).mean())

    best_params = None
    best_score = -1.0
    for init in (np.ones(n_params), 0.5 * np.ones(n_params), 2.0 * np.ones(n_params)):
        try:
            result = minimize(lambda p: -score(p), init, method="Nelder-Mead", options={"maxiter": 200})
        except Exception:
            continue
        s = score(result.x)
        if s > best_score:
            best_score = s
            best_params = result.x
    return best_params


def build_fitness_fn(df: pd.DataFrame, y: np.ndarray) -> Callable[[str], float | None]:
    def fitness_fn(code: str) -> float | None:
        params = fit_params(code, df, y)
        result = compute_descriptor(code, df, params=params)
        if result is None:
            return None
        d1, d2 = result
        return evaluate_pair(d1, d2, y)["loocv_accuracy"]
    return fitness_fn


def save_descriptor_plot(d1: np.ndarray, d2: np.ndarray, y: np.ndarray, out_path: str | Path) -> None:
    import matplotlib.pyplot as plt

    out_path = Path(out_path)
    plt.figure(figsize=(5, 4))
    plt.scatter(d1[y == 1], d2[y == 1], label="metal", alpha=0.75)
    plt.scatter(d1[y == -1], d2[y == -1], label="nonmetal", alpha=0.75)
    plt.xlabel("d1")
    plt.ylabel("d2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
