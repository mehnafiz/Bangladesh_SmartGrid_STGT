"""PF-STGT validation loop and metric computation."""

from __future__ import annotations

import torch
from torch import nn
from torch.utils.data import DataLoader

from constants import REGIONS
from evaluation.metrics import (
    ValidationMetrics,
    compute_demand_metrics,
    compute_stress_metrics,
)
from training.config import TrainingConfig
from training.losses import MultiTaskLoss
from utils.logging import get_logger

logger = get_logger(__name__)


class Validator:
    """Compute validation loss and Phase 15 metrics."""

    def __init__(
        self,
        model: nn.Module,
        config: TrainingConfig,
        loss_fn: MultiTaskLoss | None = None,
    ) -> None:
        self.model = model
        self.config = config
        self.device = torch.device(config.device)
        self.loss_fn = loss_fn or MultiTaskLoss(
            lambda_demand=config.lambda_demand,
            lambda_stress=config.lambda_stress,
            huber_delta=config.huber_delta,
        )

    def validate(self, dataloader: DataLoader) -> ValidationMetrics:
        self.model.eval()
        demand_preds: list[torch.Tensor] = []
        demand_targets: list[torch.Tensor] = []
        osi_preds: list[torch.Tensor] = []
        osi_targets: list[torch.Tensor] = []
        loss_total = loss_demand = loss_stress = 0.0
        num_batches = 0

        with torch.no_grad():
            for batch in dataloader:
                batch = {
                    key: value.to(self.device) if torch.is_tensor(value) else value
                    for key, value in batch.items()
                }
                output = self.model(
                    batch["node_features"],
                    batch["global_features"],
                    batch["adjacency"],
                    attention_bias=batch["attention_bias"],
                )
                _, breakdown = self.loss_fn(
                    output.demand_pred,
                    output.osi_pred,
                    batch["demand_target"],
                    batch["osi_target"],
                )
                loss_total += breakdown.total
                loss_demand += breakdown.demand
                loss_stress += breakdown.stress
                num_batches += 1

                demand_preds.append(output.demand_pred.cpu())
                demand_targets.append(batch["demand_target"].cpu())
                osi_preds.append(output.osi_pred.cpu())
                osi_targets.append(batch["osi_target"].cpu())

        if num_batches == 0:
            raise RuntimeError("Validation dataloader produced zero batches")

        demand_pred = torch.cat(demand_preds, dim=0)
        demand_true = torch.cat(demand_targets, dim=0)
        osi_pred = torch.cat(osi_preds, dim=0)
        osi_true = torch.cat(osi_targets, dim=0)

        demand_metrics = compute_demand_metrics(
            demand_true,
            demand_pred,
            region_names=REGIONS,
        )
        stress_metrics = compute_stress_metrics(osi_true, osi_pred)

        metrics = ValidationMetrics(
            loss_total=loss_total / num_batches,
            loss_demand=loss_demand / num_batches,
            loss_stress=loss_stress / num_batches,
            demand=demand_metrics,
            stress=stress_metrics,
        )
        logger.info(
            "Validation: loss=%.4f demand_mae=%.4f stress_mae=%.4f stress_r2=%.4f",
            metrics.loss_total,
            metrics.demand.mae,
            metrics.stress.mae,
            metrics.stress.r2,
        )
        return metrics
