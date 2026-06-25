"""Tests for evaluation metrics."""

from __future__ import annotations

import numpy as np
import torch

from constants import REGIONS
from evaluation.metrics import compute_demand_metrics, compute_stress_metrics


def test_perfect_demand_metrics() -> None:
    y = torch.randn(10, 9)
    metrics = compute_demand_metrics(y, y, region_names=REGIONS)
    assert metrics.mae == 0.0
    assert metrics.rmse == 0.0
    assert metrics.r2 == 1.0


def test_demand_metrics_mape_excludes_zero() -> None:
    y_true = np.array([[0.0, 100.0], [0.0, 200.0]])
    y_pred = np.array([[1.0, 110.0], [2.0, 190.0]])
    metrics = compute_demand_metrics(y_true, y_pred)
    assert metrics.mape > 0.0


def test_stress_metrics() -> None:
    y_true = torch.linspace(0.1, 0.9, 20).unsqueeze(-1)
    y_pred = y_true + 0.05
    metrics = compute_stress_metrics(y_true, y_pred)
    assert metrics.mae > 0.0
    assert metrics.rmse > 0.0
    assert metrics.pearson_r is not None
