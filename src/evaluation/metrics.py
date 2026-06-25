"""Evaluation metrics for demand and stress tasks (Phase 15)."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import torch
from torch import Tensor


def _to_numpy(x: Tensor | np.ndarray) -> np.ndarray:
    if isinstance(x, Tensor):
        return x.detach().cpu().numpy()
    return np.asarray(x)


@dataclass(frozen=True)
class DemandMetricsResult:
    mae: float
    rmse: float
    mape: float
    r2: float
    mae_dhaka: float | None = None
    per_region_mae: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class StressMetricsResult:
    mae: float
    rmse: float
    r2: float
    pearson_r: float | None = None


@dataclass(frozen=True)
class ValidationMetrics:
    """Aggregated validation metrics for model selection."""

    loss_total: float
    loss_demand: float
    loss_stress: float
    demand: DemandMetricsResult
    stress: StressMetricsResult


def _r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return 0.0
    return float(1.0 - ss_res / ss_tot)


def compute_demand_metrics(
    y_true: Tensor | np.ndarray,
    y_pred: Tensor | np.ndarray,
    *,
    region_names: tuple[str, ...] | None = None,
    dhaka_index: int = 3,
) -> DemandMetricsResult:
    """
    Compute macro demand metrics over regions.

    y_true, y_pred: shape (N_samples, N_regions) or (N_regions,)
    """
    yt = _to_numpy(y_true)
    yp = _to_numpy(y_pred)
    if yt.ndim == 1:
        yt = yt.reshape(1, -1)
        yp = yp.reshape(1, -1)

    abs_err = np.abs(yt - yp)
    sq_err = (yt - yp) ** 2

    mae_per_region = abs_err.mean(axis=0)
    rmse_per_region = np.sqrt(sq_err.mean(axis=0))

    mask = np.abs(yt) > 1e-8
    mape_vals = abs_err[mask] / np.abs(yt[mask]) * 100.0
    mape = float(mape_vals.mean()) if mape_vals.size else 0.0

    r2_per_region = [_r2_score(yt[:, r], yp[:, r]) for r in range(yt.shape[1])]

    per_region: dict[str, float] = {}
    if region_names:
        for i, name in enumerate(region_names):
            if i < len(mae_per_region):
                per_region[name] = float(mae_per_region[i])

    return DemandMetricsResult(
        mae=float(mae_per_region.mean()),
        rmse=float(rmse_per_region.mean()),
        mape=mape,
        r2=float(np.mean(r2_per_region)),
        mae_dhaka=float(mae_per_region[dhaka_index]) if mae_per_region.size > dhaka_index else None,
        per_region_mae=per_region,
    )


def compute_stress_metrics(
    y_true: Tensor | np.ndarray,
    y_pred: Tensor | np.ndarray,
) -> StressMetricsResult:
    """Compute OSI metrics. Inputs shape (N,) or (N, 1)."""
    yt = _to_numpy(y_true).reshape(-1)
    yp = _to_numpy(y_pred).reshape(-1)

    mae = float(np.mean(np.abs(yt - yp)))
    rmse = float(np.sqrt(np.mean((yt - yp) ** 2)))
    r2 = _r2_score(yt, yp)

    pearson_r: float | None = None
    if yt.size > 1 and np.std(yt) > 0 and np.std(yp) > 0:
        pearson_r = float(np.corrcoef(yt, yp)[0, 1])

    return StressMetricsResult(mae=mae, rmse=rmse, r2=r2, pearson_r=pearson_r)
