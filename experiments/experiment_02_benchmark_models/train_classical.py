"""Classical benchmark models B01–B03 (no PyTorch import)."""

from __future__ import annotations

import pickle
import sys
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from foundation import FoundationCoordinator

EXP_DIR = Path(__file__).resolve().parent
SEED = 42


def _demand_metrics(y_true, y_pred):
    yt, yp = y_true, y_pred
    mae = float(np.mean(np.abs(yt - yp)))
    rmse = float(np.sqrt(np.mean((yt - yp) ** 2)))
    mask = np.abs(yt) > 1e-8
    mape = float(np.mean(np.abs(yt[mask] - yp[mask]) / np.abs(yt[mask])) * 100) if mask.any() else 0.0
    ss_res = np.sum((yt - yp) ** 2)
    ss_tot = np.sum((yt - np.mean(yt)) ** 2)
    r2 = float(1 - ss_res / ss_tot) if ss_tot else 0.0
    return mae, rmse, mape, r2


def _stress_metrics(y_true, y_pred):
    yt, yp = y_true.reshape(-1), y_pred.reshape(-1)
    mae = float(np.mean(np.abs(yt - yp)))
    rmse = float(np.sqrt(np.mean((yt - yp) ** 2)))
    ss_res = np.sum((yt - yp) ** 2)
    ss_tot = np.sum((yt - np.mean(yt)) ** 2)
    r2 = float(1 - ss_res / ss_tot) if ss_tot else 0.0
    return mae, rmse, r2
XGB_KWARGS = dict(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    random_state=SEED,
    n_jobs=1,
    tree_method="hist",
)


class XGBMultiOutput:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.models: list[XGBRegressor] = []

    def fit(self, X, y):
        self.models = []
        for col in range(y.shape[1]):
            model = XGBRegressor(**self.kwargs)
            model.fit(X, y[:, col])
            self.models.append(model)
        return self

    def predict(self, X):
        return np.column_stack([m.predict(X) for m in self.models])


def _flatten(node, global_):
    return np.concatenate([node.reshape(-1), global_.reshape(-1)])


def _build_split(coordinator, split):
    indices = coordinator.data_result.sample_indices[split]
    flat, demands, osis = [], [], []
    for sample_idx in indices:
        sample = coordinator.build_sample(split, sample_idx.end_idx)
        node = sample.x_temporal.node_features.astype(np.float32)
        glob = sample.x_temporal.global_features.astype(np.float32)
        flat.append(_flatten(node, glob))
        demands.append(sample.targets.y_demand.values.astype(np.float32))
        osis.append(float(sample.targets.y_osi.value))
    return np.stack(flat), np.stack(demands), np.asarray(osis, dtype=np.float32).reshape(-1, 1)


def _eval(bid, name, y_d, d_pred, y_s, s_pred):
    mae, rmse, mape, r2 = _demand_metrics(y_d, d_pred)
    smae, srmse, sr2 = _stress_metrics(y_s, s_pred)
    per_sample = np.abs(y_d - d_pred).mean(axis=1)
    return {
        "benchmark_id": bid,
        "model_name": name,
        "split": "test",
        "demand_mae": mae,
        "demand_rmse": rmse,
        "demand_mape": mape,
        "demand_r2": r2,
        "stress_mae": smae,
        "stress_rmse": srmse,
        "stress_r2": sr2,
        "per_sample_demand_mae": per_sample,
    }


def _train(bid, name, demand_model, stress_model, X_train, X_test, y_d_train, y_d_test, y_s_train, y_s_test):
    demand_model.fit(X_train, y_d_train)
    stress_model.fit(X_train, y_s_train.ravel())
    d_pred = demand_model.predict(X_test)
    s_pred = np.clip(stress_model.predict(X_test).reshape(-1, 1), 0, 1)
    return _eval(bid, name, y_d_test, d_pred, y_s_test, s_pred)


def main() -> None:
    coordinator = FoundationCoordinator(verify_md5=True)
    X_train, y_d_train, y_s_train = _build_split(coordinator, "train")
    X_test, y_d_test, y_s_test = _build_split(coordinator, "test")
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    results = []
    print("B01", flush=True)
    results.append(
        _train(
            "B01",
            "Linear Regression",
            MultiOutputRegressor(LinearRegression()),
            LinearRegression(),
            X_train_s,
            X_test_s,
            y_d_train,
            y_d_test,
            y_s_train,
            y_s_test,
        )
    )
    print("B02", flush=True)
    results.append(
        _train(
            "B02",
            "Random Forest",
            MultiOutputRegressor(RandomForestRegressor(n_estimators=300, random_state=SEED, n_jobs=1)),
            RandomForestRegressor(n_estimators=300, random_state=SEED, n_jobs=1),
            X_train_s,
            X_test_s,
            y_d_train,
            y_d_test,
            y_s_train,
            y_s_test,
        )
    )
    print("B03", flush=True)
    results.append(
        _train(
            "B03",
            "XGBoost",
            XGBMultiOutput(**XGB_KWARGS),
            XGBRegressor(**XGB_KWARGS),
            X_train_s,
            X_test_s,
            y_d_train,
            y_d_test,
            y_s_train,
            y_s_test,
        )
    )

    per_sample = {r["benchmark_id"]: r.pop("per_sample_demand_mae") for r in results}
    out = EXP_DIR / "classical_cache.pkl"
    with out.open("wb") as f:
        pickle.dump({"results": results, "per_sample": per_sample}, f)
    print(f"Saved {out}", flush=True)


if __name__ == "__main__":
    main()
