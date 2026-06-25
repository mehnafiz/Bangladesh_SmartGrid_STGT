"""Experiment orchestration for PF-STGT training (Phase 10 / 11)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import torch
from torch.utils.data import DataLoader

from foundation import FoundationCoordinator
from models.pf_stgt import PFSTGT
from training.checkpoint import CheckpointManager
from training.config import TrainingConfig
from training.dataloader import build_dataloaders
from training.early_stopping import EarlyStopping
from training.losses import MultiTaskLoss
from training.seed import set_seed
from training.trainer import Trainer
from training.validator import Validator
from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class ExperimentResult:
    """Summary returned after a training run."""

    epochs_run: int
    best_val_demand_mae: float
    stopped_early: bool
    checkpoint_path: str | None


class ExperimentRunner:
    """
    Configuration-driven PF-STGT training orchestrator.

    Wires foundation data, model, trainer, validator, checkpointing, and early stopping.
    """

    def __init__(
        self,
        config: TrainingConfig | None = None,
        *,
        coordinator: FoundationCoordinator | None = None,
        verify_md5: bool = True,
    ) -> None:
        self.config = config or TrainingConfig()
        set_seed(self.config.seed)
        self.coordinator = coordinator or FoundationCoordinator(verify_md5=verify_md5)
        self.model = PFSTGT()
        self.loss_fn = MultiTaskLoss(
            lambda_demand=self.config.lambda_demand,
            lambda_stress=self.config.lambda_stress,
            huber_delta=self.config.huber_delta,
        )
        self.trainer = Trainer(self.model, self.config, self.loss_fn)
        self.validator = Validator(self.model, self.config, self.loss_fn)
        self.early_stopping = EarlyStopping(
            patience=self.config.early_stop_patience,
            min_delta=self.config.early_stop_min_delta,
        )
        self.checkpoint_manager = CheckpointManager(self.config)
        self.loaders = build_dataloaders(self.coordinator, self.config)

    @property
    def train_loader(self) -> DataLoader:
        return self.loaders["train"]

    @property
    def val_loader(self) -> DataLoader:
        return self.loaders["validation"]

    def run(
        self,
        *,
        max_epochs: int | None = None,
        max_train_batches: int | None = None,
        max_val_batches: int | None = None,
    ) -> ExperimentResult:
        """
        Execute the training loop.

        Optional batch limits support smoke testing without full experiments.
        """
        epochs = max_epochs or self.config.max_epochs
        best_val_mae = float("inf")
        checkpoint_path: str | None = None
        stopped_early = False

        for epoch in range(1, epochs + 1):
            self._train_limited(self.train_loader, max_train_batches)
            val_metrics = self._validate_limited(self.val_loader, max_val_batches)
            self.trainer.step_scheduler(val_metrics.demand.mae)

            stop_state = self.early_stopping.step(val_metrics.demand.mae)
            if stop_state.improved:
                best_val_mae = val_metrics.demand.mae
                path = self.checkpoint_manager.save_best(
                    self.model,
                    self.trainer.optimizer,
                    epoch,
                    self._metrics_to_dict(val_metrics),
                )
                checkpoint_path = str(path)

            if stop_state.should_stop:
                stopped_early = True
                break

        if checkpoint_path and self.checkpoint_manager.has_checkpoint():
            self.checkpoint_manager.load(self.model, self.trainer.optimizer)

        return ExperimentResult(
            epochs_run=epoch,
            best_val_demand_mae=best_val_mae,
            stopped_early=stopped_early,
            checkpoint_path=checkpoint_path,
        )

    def _train_limited(
        self,
        loader: DataLoader,
        max_batches: int | None,
    ) -> None:
        if max_batches is None:
            self.trainer.train_epoch(loader)
            return
        self.model.train()
        for batch_idx, batch in enumerate(loader):
            if batch_idx >= max_batches:
                break
            self.trainer.train_batch(batch)

    def _validate_limited(
        self,
        loader: DataLoader,
        max_batches: int | None,
    ):
        if max_batches is None:
            return self.validator.validate(loader)

        self.model.eval()
        demand_preds: list[torch.Tensor] = []
        demand_targets: list[torch.Tensor] = []
        osi_preds: list[torch.Tensor] = []
        osi_targets: list[torch.Tensor] = []
        loss_total = loss_demand = loss_stress = 0.0
        num_batches = 0

        with torch.no_grad():
            for batch_idx, batch in enumerate(loader):
                if batch_idx >= max_batches:
                    break
                batch = {
                    key: value.to(self.trainer.device) if torch.is_tensor(value) else value
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

        from constants import REGIONS
        from evaluation.metrics import ValidationMetrics, compute_demand_metrics, compute_stress_metrics

        demand_pred = torch.cat(demand_preds, dim=0)
        demand_true = torch.cat(demand_targets, dim=0)
        osi_pred = torch.cat(osi_preds, dim=0)
        osi_true = torch.cat(osi_targets, dim=0)
        return ValidationMetrics(
            loss_total=loss_total / max(num_batches, 1),
            loss_demand=loss_demand / max(num_batches, 1),
            loss_stress=loss_stress / max(num_batches, 1),
            demand=compute_demand_metrics(demand_true, demand_pred, region_names=REGIONS),
            stress=compute_stress_metrics(osi_true, osi_pred),
        )

    @staticmethod
    def _metrics_to_dict(metrics) -> dict[str, Any]:
        return {
            "loss_total": metrics.loss_total,
            "loss_demand": metrics.loss_demand,
            "loss_stress": metrics.loss_stress,
            "demand_mae": metrics.demand.mae,
            "demand_rmse": metrics.demand.rmse,
            "demand_mape": metrics.demand.mape,
            "demand_r2": metrics.demand.r2,
            "stress_mae": metrics.stress.mae,
            "stress_rmse": metrics.stress.rmse,
            "stress_r2": metrics.stress.r2,
        }
