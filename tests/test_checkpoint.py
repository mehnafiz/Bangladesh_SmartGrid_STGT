"""Tests for checkpoint manager."""

from __future__ import annotations

from pathlib import Path

import torch

from models.pf_stgt import PFSTGT
from training.checkpoint import CheckpointManager
from training.config import TrainingConfig
from training.trainer import Trainer


def test_checkpoint_save_and_load(tmp_path: Path) -> None:
    config = TrainingConfig(checkpoint_root=tmp_path, seed=42)
    model = PFSTGT()
    trainer = Trainer(model, config)
    manager = CheckpointManager(config)

    metrics = {"demand_mae": 123.4, "stress_mae": 0.05}
    path = manager.save_best(model, trainer.optimizer, epoch=1, metrics=metrics)
    assert path.exists()
    assert config.metrics_val_path().exists()
    assert config.config_path().exists()

    model2 = PFSTGT()
    trainer2 = Trainer(model2, config)
    payload = manager.load(model2, trainer2.optimizer)
    assert payload["epoch"] == 1
    assert payload["metrics"]["demand_mae"] == 123.4

    for p1, p2 in zip(model.parameters(), model2.parameters(), strict=True):
        assert torch.allclose(p1, p2)
