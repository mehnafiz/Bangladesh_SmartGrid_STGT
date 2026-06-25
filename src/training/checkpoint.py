"""Checkpoint save/load with metadata (Phase 10)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch
import yaml
from torch import nn
from torch.optim import Optimizer

from constants import LOCKED_MD5
from training.config import TrainingConfig
from utils.logging import get_logger
from utils.md5 import verify_locked_artifacts

logger = get_logger(__name__)


class CheckpointManager:
    """Save and load best validation checkpoints."""

    def __init__(self, config: TrainingConfig) -> None:
        self.config = config
        self.checkpoint_dir = config.checkpoint_dir()
        self.best_path = config.best_checkpoint_path()
        self.metrics_path = config.metrics_val_path()
        self.config_path = config.config_path()

    def save_best(
        self,
        model: nn.Module,
        optimizer: Optimizer,
        epoch: int,
        metrics: dict[str, Any],
    ) -> Path:
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        payload = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "metrics": metrics,
            "config": {
                "benchmark_id": self.config.benchmark_id,
                "seed": self.config.seed,
                "batch_size": self.config.batch_size,
                "learning_rate": self.config.learning_rate,
                "weight_decay": self.config.weight_decay,
                "lambda_demand": self.config.lambda_demand,
                "lambda_stress": self.config.lambda_stress,
            },
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "locked_md5": verify_locked_artifacts(strict=False),
        }
        torch.save(payload, self.best_path)

        self.metrics_path.write_text(json.dumps(metrics, indent=2))
        self.config_path.write_text(
            yaml.safe_dump(
                {
                    "benchmark_id": self.config.benchmark_id,
                    "seed": self.config.seed,
                    "batch_size": self.config.batch_size,
                    "learning_rate": self.config.learning_rate,
                    "weight_decay": self.config.weight_decay,
                    "lambda_demand": self.config.lambda_demand,
                    "lambda_stress": self.config.lambda_stress,
                    "locked_md5": LOCKED_MD5,
                }
            )
        )
        logger.info("Saved best checkpoint -> %s", self.best_path)
        return self.best_path

    def load(self, model: nn.Module, optimizer: Optimizer | None = None) -> dict[str, Any]:
        if not self.best_path.exists():
            raise FileNotFoundError(f"Checkpoint not found: {self.best_path}")
        payload = torch.load(self.best_path, map_location="cpu", weights_only=False)
        model.load_state_dict(payload["model_state_dict"])
        if optimizer is not None and "optimizer_state_dict" in payload:
            optimizer.load_state_dict(payload["optimizer_state_dict"])
        logger.info("Loaded checkpoint from %s (epoch=%s)", self.best_path, payload.get("epoch"))
        return payload

    def has_checkpoint(self) -> bool:
        return self.best_path.exists()
