"""PF-STGT training loop."""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn
from torch.utils.data import DataLoader

from training.config import TrainingConfig
from training.losses import LossBreakdown, MultiTaskLoss
from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class TrainEpochResult:
    loss_total: float
    loss_demand: float
    loss_stress: float
    num_batches: int


class Trainer:
    """Execute forward pass, loss computation, backpropagation, and optimizer step."""

    def __init__(
        self,
        model: nn.Module,
        config: TrainingConfig,
        loss_fn: MultiTaskLoss | None = None,
    ) -> None:
        self.model = model
        self.config = config
        self.device = torch.device(config.device)
        self.model.to(self.device)
        self.loss_fn = loss_fn or MultiTaskLoss(
            lambda_demand=config.lambda_demand,
            lambda_stress=config.lambda_stress,
            huber_delta=config.huber_delta,
        )
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay,
        )
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode="min",
            factor=config.scheduler_factor,
            patience=config.scheduler_patience,
        )

    def _move_batch(self, batch: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
        return {key: value.to(self.device) if torch.is_tensor(value) else value for key, value in batch.items()}

    def train_batch(self, batch: dict[str, torch.Tensor]) -> LossBreakdown:
        self.model.train()
        batch = self._move_batch(batch)

        self.optimizer.zero_grad(set_to_none=True)
        output = self.model(
            batch["node_features"],
            batch["global_features"],
            batch["adjacency"],
            attention_bias=batch["attention_bias"],
        )
        loss, breakdown = self.loss_fn(
            output.demand_pred,
            output.osi_pred,
            batch["demand_target"],
            batch["osi_target"],
        )
        loss.backward()
        if self.config.grad_clip_norm > 0:
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config.grad_clip_norm)
        self.optimizer.step()
        return breakdown

    def train_epoch(self, dataloader: DataLoader) -> TrainEpochResult:
        total = demand = stress = 0.0
        num_batches = 0
        for batch in dataloader:
            breakdown = self.train_batch(batch)
            total += breakdown.total
            demand += breakdown.demand
            stress += breakdown.stress
            num_batches += 1

        if num_batches == 0:
            raise RuntimeError("Training dataloader produced zero batches")

        result = TrainEpochResult(
            loss_total=total / num_batches,
            loss_demand=demand / num_batches,
            loss_stress=stress / num_batches,
            num_batches=num_batches,
        )
        logger.info(
            "Train epoch: loss=%.4f demand=%.4f stress=%.4f batches=%s",
            result.loss_total,
            result.loss_demand,
            result.loss_stress,
            result.num_batches,
        )
        return result

    def step_scheduler(self, validation_score: float) -> None:
        self.scheduler.step(validation_score)
