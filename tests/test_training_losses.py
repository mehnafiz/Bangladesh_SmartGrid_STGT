"""Tests for multi-task loss functions."""

from __future__ import annotations

import torch

from training.losses import DemandHuberLoss, MultiTaskLoss, StressMSELoss


def test_demand_huber_loss_shape() -> None:
    pred = torch.tensor([[100.0, 200.0, 300.0]])
    target = torch.tensor([[110.0, 190.0, 310.0]])
    loss = DemandHuberLoss(delta=1.0)(pred, target)
    assert loss.ndim == 0
    assert torch.isfinite(loss)


def test_stress_mse_loss() -> None:
    pred = torch.tensor([[0.3], [0.5]])
    target = torch.tensor([[0.4], [0.45]])
    loss = StressMSELoss()(pred, target)
    assert loss.item() >= 0.0


def test_multitask_loss_weights() -> None:
    loss_fn = MultiTaskLoss(lambda_demand=1.0, lambda_stress=0.5, huber_delta=1.0)
    demand_pred = torch.randn(4, 9)
    demand_target = torch.randn(4, 9)
    osi_pred = torch.rand(4, 1)
    osi_target = torch.rand(4, 1)
    total, breakdown = loss_fn(demand_pred, osi_pred, demand_target, osi_target)
    expected = 1.0 * breakdown.demand + 0.5 * breakdown.stress
    assert abs(total.item() - expected) < 1e-5
