"""Materialize B02/B03 test predictions (no PyTorch)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
EXP02 = ROOT / "experiments/experiment_02_benchmark_models"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
sys.path.insert(0, str(EXP02))

from foundation import FoundationCoordinator
from train_classical import XGBMultiOutput, XGB_KWARGS, _build_split

OUT = Path(__file__).resolve().parent / "predictions"
SEED = 42


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    coordinator = FoundationCoordinator(verify_md5=True)
    X_train, y_train, _ = _build_split(coordinator, "train")
    X_test, y_test, _ = _build_split(coordinator, "test")
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    rf = MultiOutputRegressor(
        RandomForestRegressor(n_estimators=300, random_state=SEED, n_jobs=1)
    )
    rf.fit(X_train_s, y_train)
    rf_pred = rf.predict(X_test_s)

    xgb = XGBMultiOutput(**XGB_KWARGS)
    xgb.fit(X_train_s, y_train)
    xgb_pred = xgb.predict(X_test_s)

    np.save(OUT / "y_true.npy", y_test)
    np.save(OUT / "B02_random_forest_demand.npy", rf_pred.astype(np.float32))
    np.save(OUT / "B03_xgboost_demand.npy", xgb_pred.astype(np.float32))
    print(f"Saved classical predictions to {OUT}", flush=True)


if __name__ == "__main__":
    main()
