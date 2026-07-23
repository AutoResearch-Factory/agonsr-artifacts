"""Evaluation helpers for the ZB-vs-RS descriptor problem."""

from __future__ import annotations

import inspect
import re
from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd

PROBLEM_DIR = Path(__file__).resolve().parent
DATASET = PROBLEM_DIR / "data" / "ZB-RS_dataset.csv"

FEATURE_COLS = [
    "Z_A",
    "r_s_A",
    "r_p_A",
    "r_d_A",
    "period_A",
    "EA_A",
    "IP_A",
    "E_HOMO_A",
    "E_LUMO_A",
    "Z_B",
    "r_s_B",
    "r_p_B",
    "r_d_B",
    "period_B",
    "EA_B",
    "IP_B",
    "E_HOMO_B",
    "E_LUMO_B",
]

def load_data(path: str | Path = DATASET) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    df = pd.read_csv(path, index_col=0)
    X = df[FEATURE_COLS].to_numpy(dtype=float)
    y = df["energy_diff"].to_numpy(dtype=float)
    return X, y, df


def get_feature_arrays(df: pd.DataFrame) -> dict[str, np.ndarray]:
    return {col: df[col].to_numpy(dtype=float) for col in FEATURE_COLS}


def count_params(code: str) -> int:
    indices = re.findall(r"params\[(\d+)\]", code)
    return max((int(i) for i in indices), default=-1) + 1


def compute_descriptor(code: str, df: pd.DataFrame, params: np.ndarray | None = None) -> np.ndarray | None:
    """Evaluate candidate code and return an (N, D) descriptor matrix, or None."""
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
            result = fn(**call_args)
        else:
            ctx = {"np": np, "sqrt": np.sqrt, "log": np.log, "abs": np.abs, "exp": np.exp}
            ctx.update(feature_arrays)
            if params is not None:
                ctx["params"] = params
            lines = [line.strip() for line in stripped.splitlines() if line.strip()]
            if len(lines) <= 2:
                vals = [eval(line, {"__builtins__": None}, ctx) for line in lines]
                result = tuple(vals) if len(vals) > 1 else vals[0]
            else:
                ns = dict(ctx)
                exec(code, {"__builtins__": None, "np": np}, ns)
                if "d1" in ns and "d2" in ns:
                    result = (ns["d1"], ns["d2"])
                elif "d1" in ns:
                    result = ns["d1"]
                else:
                    return None

        n = len(df)
        if isinstance(result, tuple):
            arrays = [np.asarray(a, dtype=float).ravel() for a in result]
            if not arrays or not all(len(a) == n and np.all(np.isfinite(a)) for a in arrays):
                return None
            return np.column_stack(arrays)

        arr = np.asarray(result, dtype=float)
        if arr.ndim == 1:
            arr = arr.reshape(-1, 1)
        if arr.ndim == 2 and arr.shape[0] < arr.shape[1]:
            arr = arr.T
        if arr.ndim != 2 or arr.shape[0] != n or not np.all(np.isfinite(arr)):
            return None
        return arr
    except Exception:
        return None


def evaluate_descriptor(D: np.ndarray, y: np.ndarray) -> dict:
    """Evaluate descriptor matrix with linear regression and LOOCV."""
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import LeaveOneOut, cross_val_predict

    if D.ndim == 1:
        D = D.reshape(-1, 1)

    reg = LinearRegression()
    reg.fit(D, y)
    pred_full = reg.predict(D)
    rmse_full = float(np.sqrt(np.mean((pred_full - y) ** 2)))
    mae_full = float(np.mean(np.abs(pred_full - y)))
    r2_full = float(reg.score(D, y))

    loo_pred = cross_val_predict(reg, D, y, cv=LeaveOneOut())
    loocv_rmse = float(np.sqrt(np.mean((loo_pred - y) ** 2)))
    loocv_mae = float(np.mean(np.abs(loo_pred - y)))
    ss_res = np.sum((loo_pred - y) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    loocv_r2 = float(1 - ss_res / ss_tot)

    return {
        "rmse_full": rmse_full,
        "mae_full": mae_full,
        "r2_full": r2_full,
        "loocv_rmse": loocv_rmse,
        "loocv_mae": loocv_mae,
        "loocv_r2": loocv_r2,
    }


def fit_params(code: str, df: pd.DataFrame, y: np.ndarray) -> np.ndarray | None:
    """Reference helper for fitting params[] by minimizing full-fit RMSE."""
    from scipy.optimize import minimize

    n_params = count_params(code)
    if n_params == 0:
        return None

    def objective(p: np.ndarray) -> float:
        D = compute_descriptor(code, df, params=p)
        if D is None:
            return 1e9
        return evaluate_descriptor(D, y)["rmse_full"]

    best_params = None
    best_value = float("inf")
    for init in (np.ones(n_params), 0.5 * np.ones(n_params), 2.0 * np.ones(n_params)):
        try:
            result = minimize(objective, init, method="Nelder-Mead", options={"maxiter": 300})
        except Exception:
            continue
        value = objective(result.x)
        if value < best_value:
            best_value = value
            best_params = result.x
    return best_params


def build_fitness_fn(df: pd.DataFrame, y: np.ndarray) -> Callable[[str], float | None]:
    def fitness_fn(code: str) -> float | None:
        params = fit_params(code, df, y)
        D = compute_descriptor(code, df, params=params)
        if D is None:
            return None
        return -evaluate_descriptor(D, y)["loocv_rmse"]

    return fitness_fn


def save_descriptor_plot(D: np.ndarray, y: np.ndarray, out_path: str | Path) -> None:
    import matplotlib.pyplot as plt

    out_path = Path(out_path)
    if D.ndim == 1:
        D = D.reshape(-1, 1)
    plt.figure(figsize=(5, 4))
    if D.shape[1] >= 2:
        sc = plt.scatter(D[:, 0], D[:, 1], c=y, cmap="coolwarm", alpha=0.85)
        plt.xlabel("d1")
        plt.ylabel("d2")
    else:
        sc = plt.scatter(D[:, 0], y, c=y, cmap="coolwarm", alpha=0.85)
        plt.xlabel("d1")
        plt.ylabel("energy_diff")
    plt.colorbar(sc, label="E[RS] - E[ZB] (eV)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
