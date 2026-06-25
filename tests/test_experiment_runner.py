"""Smoke test for ExperimentRunner (limited batches — not a full experiment)."""

from __future__ import annotations

from pathlib import Path

from training.config import TrainingConfig
from training.experiment_runner import ExperimentRunner


def test_experiment_runner_smoke_loop(tmp_path: Path) -> None:
    config = TrainingConfig(
        batch_size=8,
        max_epochs=200,
        seed=42,
        device="cpu",
        checkpoint_root=tmp_path,
    )
    runner = ExperimentRunner(config, verify_md5=True)
    result = runner.run(max_epochs=1, max_train_batches=1, max_val_batches=1)
    assert result.epochs_run == 1
    assert result.best_val_demand_mae < float("inf")
    assert result.checkpoint_path is not None
