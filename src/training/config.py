"""Training configuration (Phase 10 / Phase 11 defaults)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from constants import PROJECT_ROOT


@dataclass(frozen=True)
class TrainingConfig:
    """Frozen default training hyperparameters for PF-STGT (B07)."""

    benchmark_id: str = "B07"
    seed: int = 42
    batch_size: int = 32
    learning_rate: float = 5e-4
    weight_decay: float = 1e-4
    max_epochs: int = 200
    grad_clip_norm: float = 1.0
    lambda_demand: float = 1.0
    lambda_stress: float = 0.5
    huber_delta: float = 1.0
    early_stop_patience: int = 15
    early_stop_min_delta: float = 0.01
    scheduler_patience: int = 5
    scheduler_factor: float = 0.5
    num_workers: int = 0
    device: str = "cpu"
    checkpoint_root: Path = field(default_factory=lambda: PROJECT_ROOT / "checkpoints")

    def checkpoint_dir(self) -> Path:
        return self.checkpoint_root / self.benchmark_id / f"seed_{self.seed}"

    def best_checkpoint_path(self) -> Path:
        return self.checkpoint_dir() / "best.pt"

    def metrics_val_path(self) -> Path:
        return self.checkpoint_dir() / "metrics_val.json"

    def config_path(self) -> Path:
        return self.checkpoint_dir() / "config.yaml"
