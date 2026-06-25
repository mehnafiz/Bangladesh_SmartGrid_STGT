"""Multi-task loss functions (Phase 10)."""

from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn.functional as F
from torch import Tensor


@dataclass(frozen=True)
class LossBreakdown:
    """Component losses for logging."""

    total: float
    demand: float
    stress: float


class DemandHuberLoss(torch.nn.Module):
    """Macro-averaged Huber loss over N regional demand outputs."""

    def __init__(self, delta: float = 1.0) -> None:
        super().__init__()
        self.delta = delta

    def forward(self, demand_pred: Tensor, demand_target: Tensor) -> Tensor:
        if demand_pred.shape != demand_target.shape:
            raise ValueError(
                f"Shape mismatch: pred {demand_pred.shape} vs target {demand_target.shape}"
            )
        per_element = F.huber_loss(
            demand_pred,
            demand_target,
            delta=self.delta,
            reduction="none",
        )
        return per_element.mean()


class StressMSELoss(torch.nn.Module):
    """MSE loss for scalar OSI prediction."""

    def forward(self, osi_pred: Tensor, osi_target: Tensor) -> Tensor:
        if osi_pred.shape != osi_target.shape:
            if osi_target.dim() == 1:
                osi_target = osi_target.unsqueeze(-1)
            if osi_pred.dim() == 1:
                osi_pred = osi_pred.unsqueeze(-1)
        return F.mse_loss(osi_pred, osi_target)


class MultiTaskLoss(torch.nn.Module):
    """
    Combined PF-STGT loss (Phase 10):

    L_total = λ1 · L_demand + λ2 · L_stress
    """

    def __init__(
        self,
        lambda_demand: float = 1.0,
        lambda_stress: float = 0.5,
        huber_delta: float = 1.0,
    ) -> None:
        super().__init__()
        self.lambda_demand = lambda_demand
        self.lambda_stress = lambda_stress
        self.demand_loss_fn = DemandHuberLoss(delta=huber_delta)
        self.stress_loss_fn = StressMSELoss()

    def forward(
        self,
        demand_pred: Tensor,
        osi_pred: Tensor,
        demand_target: Tensor,
        osi_target: Tensor,
    ) -> tuple[Tensor, LossBreakdown]:
        demand_loss = self.demand_loss_fn(demand_pred, demand_target)
        stress_loss = self.stress_loss_fn(osi_pred, osi_target)
        total = self.lambda_demand * demand_loss + self.lambda_stress * stress_loss
        breakdown = LossBreakdown(
            total=float(total.detach().cpu()),
            demand=float(demand_loss.detach().cpu()),
            stress=float(stress_loss.detach().cpu()),
        )
        return total, breakdown
