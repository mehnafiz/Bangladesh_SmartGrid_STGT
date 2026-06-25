"""Experiment 01 — PF-STGT training (Phase 09/10/11 defaults)."""

from __future__ import annotations

import json
import logging
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import torch

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from constants import LOCKED_MD5, PROJECT_ROOT
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
from utils.logging import setup_logging
from utils.md5 import verify_locked_artifacts

OUTPUT_DIR = PROJECT_ROOT / "experiments" / "experiment_01_pf_stgt"
EXPERIMENT_DOC = OUTPUT_DIR / "Experiment_01_PF_STGT_Training.md"


@dataclass
class EpochRecord:
    epoch: int
    train_loss: float
    train_demand_loss: float
    train_stress_loss: float
    val_loss: float
    val_demand_loss: float
    val_stress_loss: float
    val_demand_mae: float
    val_stress_mae: float
    learning_rate: float


def _select_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def _metrics_payload(metrics, *, split: str) -> dict[str, Any]:
    return {
        "split": split,
        "loss_total": metrics.loss_total,
        "loss_demand": metrics.loss_demand,
        "loss_stress": metrics.loss_stress,
        "demand": {
            "mae": metrics.demand.mae,
            "rmse": metrics.demand.rmse,
            "mape": metrics.demand.mape,
            "r2": metrics.demand.r2,
            "mae_dhaka": metrics.demand.mae_dhaka,
        },
        "stress": {
            "mae": metrics.stress.mae,
            "rmse": metrics.stress.rmse,
            "r2": metrics.stress.r2,
            "pearson_r": metrics.stress.pearson_r,
        },
    }


def _plot_curve(
    epochs: list[int],
    values: list[float],
    *,
    title: str,
    ylabel: str,
    path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(epochs, values, marker="o", markersize=3, linewidth=1.5)
    ax.set_xlabel("Epoch")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def _write_training_log(path: Path, records: list[EpochRecord], header_lines: list[str]) -> None:
    lines = header_lines + ["", "epoch,train_loss,val_loss,val_demand_mae,val_stress_mae,lr"]
    for record in records:
        lines.append(
            f"{record.epoch},{record.train_loss:.6f},{record.val_loss:.6f},"
            f"{record.val_demand_mae:.6f},{record.val_stress_mae:.6f},{record.learning_rate:.8f}"
        )
    path.write_text("\n".join(lines))


def _write_summary(
    path: Path,
    *,
    result: dict[str, Any],
) -> None:
    val = result["validation"]
    test = result["test"]
    lines = [
        "# Experiment 01 — Training Summary",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Run metadata",
        "",
        f"- Seed: {result['seed']}",
        f"- Device: {result['device']}",
        f"- Parameters: {result['parameter_count']:,}",
        f"- Training time: {result['training_time_seconds']:.1f}s",
        f"- Epochs run: {result['epochs_run']}",
        f"- Best epoch: {result['best_epoch']}",
        f"- Early stopping epoch: {result['early_stopping_epoch']}",
        f"- Stopped early: {result['stopped_early']}",
        "",
        "## Validation metrics (best checkpoint)",
        "",
        f"| Metric | Demand | Stress |",
        f"| --- | --- | --- |",
        f"| MAE | {val['demand']['mae']:.4f} | {val['stress']['mae']:.4f} |",
        f"| RMSE | {val['demand']['rmse']:.4f} | {val['stress']['rmse']:.4f} |",
        f"| MAPE | {val['demand']['mape']:.4f} | — |",
        f"| R² | {val['demand']['r2']:.4f} | {val['stress']['r2']:.4f} |",
        "",
        "## Test metrics (best checkpoint)",
        "",
        f"| Metric | Demand | Stress |",
        f"| --- | --- | --- |",
        f"| MAE | {test['demand']['mae']:.4f} | {test['stress']['mae']:.4f} |",
        f"| RMSE | {test['demand']['rmse']:.4f} | {test['stress']['rmse']:.4f} |",
        f"| MAPE | {test['demand']['mape']:.4f} | — |",
        f"| R² | {test['demand']['r2']:.4f} | {test['stress']['r2']:.4f} |",
        "",
        "## Outputs",
        "",
        "- `best_model.pt`",
        "- `metrics.json`",
        "- `train_loss.png`",
        "- `val_loss.png`",
        "- `training_log.txt`",
        "",
    ]
    path.write_text("\n".join(lines))


def _update_experiment_doc(result: dict[str, Any]) -> None:
    val = result["validation"]
    test = result["test"]
    execution = [
        "",
        "---",
        "",
        "## Execution Record",
        "",
        f"**Date:** {datetime.now(timezone.utc).date().isoformat()}",
        f"**Script:** `experiments/experiment_01_pf_stgt/run_experiment.py`",
        f"**Status:** COMPLETE",
        "",
        "### Run Summary",
        "",
        f"| Item | Value |",
        f"| --- | --- |",
        f"| Seed | {result['seed']} |",
        f"| Device | {result['device']} |",
        f"| Parameters | {result['parameter_count']:,} |",
        f"| Training time | {result['training_time_seconds']:.1f}s |",
        f"| Epochs run | {result['epochs_run']} |",
        f"| Best epoch | {result['best_epoch']} |",
        f"| Early stopping epoch | {result['early_stopping_epoch']} |",
        f"| Stopped early | {result['stopped_early']} |",
        "",
        "### Validation metrics (best checkpoint)",
        "",
        f"| Task | MAE | RMSE | MAPE / R² |",
        f"| --- | --- | --- | --- |",
        f"| Demand | {val['demand']['mae']:.4f} | {val['demand']['rmse']:.4f} | MAPE {val['demand']['mape']:.4f}, R² {val['demand']['r2']:.4f} |",
        f"| Stress | {val['stress']['mae']:.4f} | {val['stress']['rmse']:.4f} | R² {val['stress']['r2']:.4f} |",
        "",
        "### Test metrics (best checkpoint)",
        "",
        f"| Task | MAE | RMSE | MAPE / R² |",
        f"| --- | --- | --- | --- |",
        f"| Demand | {test['demand']['mae']:.4f} | {test['demand']['rmse']:.4f} | MAPE {test['demand']['mape']:.4f}, R² {test['demand']['r2']:.4f} |",
        f"| Stress | {test['stress']['mae']:.4f} | {test['stress']['rmse']:.4f} | R² {test['stress']['r2']:.4f} |",
        "",
        "### Deliverables",
        "",
        "| File | Status |",
        "| --- | --- |",
        "| train_loss.png | Generated |",
        "| val_loss.png | Generated |",
        "| metrics.json | Generated |",
        "| best_model.pt | Generated |",
        "| training_log.txt | Generated |",
        "| training_summary.md | Generated |",
        "",
        "### Locked artefact integrity",
        "",
    ]
    for path, expected in LOCKED_MD5.items():
        actual = result["locked_md5"].get(path, "")
        execution.append(f"- `{path}` unchanged: {actual == expected}")

    base = EXPERIMENT_DOC.read_text(encoding="utf-8")
    marker = "## Execution Record"
    if marker in base:
        base = base.split(marker)[0].rstrip()
    EXPERIMENT_DOC.write_text(base + "\n".join(execution), encoding="utf-8")


def run_experiment() -> dict[str, Any]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    device = _select_device()
    config = TrainingConfig(
        seed=42,
        device=device,
        checkpoint_root=OUTPUT_DIR,
    )

    log_path = OUTPUT_DIR / "training_log.txt"
    setup_logging()
    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    )
    logging.getLogger().addHandler(file_handler)

    locked_md5 = verify_locked_artifacts(PROJECT_ROOT, strict=True)
    set_seed(config.seed)

    coordinator = FoundationCoordinator(verify_md5=True)
    model = PFSTGT()
    param_count = model.count_parameters()
    loss_fn = MultiTaskLoss(
        lambda_demand=config.lambda_demand,
        lambda_stress=config.lambda_stress,
        huber_delta=config.huber_delta,
    )
    trainer = Trainer(model, config, loss_fn)
    validator = Validator(model, config, loss_fn)
    early_stopping = EarlyStopping(
        patience=config.early_stop_patience,
        min_delta=config.early_stop_min_delta,
    )
    checkpoint_manager = CheckpointManager(config)
    loaders = build_dataloaders(coordinator, config)

    records: list[EpochRecord] = []
    best_epoch = 0
    best_val_metrics = None
    stopped_early = False
    start = time.perf_counter()

    for epoch in range(1, config.max_epochs + 1):
        train_result = trainer.train_epoch(loaders["train"])
        val_metrics = validator.validate(loaders["validation"])
        trainer.step_scheduler(val_metrics.demand.mae)
        lr = trainer.optimizer.param_groups[0]["lr"]

        records.append(
            EpochRecord(
                epoch=epoch,
                train_loss=train_result.loss_total,
                train_demand_loss=train_result.loss_demand,
                train_stress_loss=train_result.loss_stress,
                val_loss=val_metrics.loss_total,
                val_demand_loss=val_metrics.loss_demand,
                val_stress_loss=val_metrics.loss_stress,
                val_demand_mae=val_metrics.demand.mae,
                val_stress_mae=val_metrics.stress.mae,
                learning_rate=lr,
            )
        )

        stop_state = early_stopping.step(val_metrics.demand.mae)
        if stop_state.improved:
            best_epoch = epoch
            best_val_metrics = val_metrics
            checkpoint_manager.save_best(
                model,
                trainer.optimizer,
                epoch,
                {
                    "loss_total": val_metrics.loss_total,
                    "demand_mae": val_metrics.demand.mae,
                    "stress_mae": val_metrics.stress.mae,
                },
            )

        if stop_state.should_stop:
            stopped_early = True
            break

    elapsed = time.perf_counter() - start

    best_model_path = OUTPUT_DIR / "best_model.pt"
    if checkpoint_manager.has_checkpoint():
        payload = checkpoint_manager.load(model, trainer.optimizer)
        torch.save(payload, best_model_path)
    else:
        torch.save(
            {
                "epoch": best_epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": trainer.optimizer.state_dict(),
            },
            best_model_path,
        )

    test_metrics = validator.validate(loaders["test"])
    if best_val_metrics is None:
        best_val_metrics = validator.validate(loaders["validation"])

    epochs = [r.epoch for r in records]
    _plot_curve(
        epochs,
        [r.train_loss for r in records],
        title="PF-STGT Training Loss",
        ylabel="Train loss (L_total)",
        path=OUTPUT_DIR / "train_loss.png",
    )
    _plot_curve(
        epochs,
        [r.val_loss for r in records],
        title="PF-STGT Validation Loss",
        ylabel="Validation loss (L_total)",
        path=OUTPUT_DIR / "val_loss.png",
    )

    result: dict[str, Any] = {
        "experiment": "experiment_01_pf_stgt",
        "benchmark_id": config.benchmark_id,
        "seed": config.seed,
        "device": device,
        "parameter_count": param_count,
        "epochs_run": records[-1].epoch if records else 0,
        "best_epoch": best_epoch,
        "early_stopping_epoch": records[-1].epoch if records else 0,
        "stopped_early": stopped_early,
        "training_time_seconds": elapsed,
        "hyperparameters": {
            "batch_size": config.batch_size,
            "learning_rate": config.learning_rate,
            "weight_decay": config.weight_decay,
            "lambda_demand": config.lambda_demand,
            "lambda_stress": config.lambda_stress,
            "huber_delta": config.huber_delta,
            "early_stop_patience": config.early_stop_patience,
            "max_epochs": config.max_epochs,
        },
        "validation": _metrics_payload(best_val_metrics, split="validation"),
        "test": _metrics_payload(test_metrics, split="test"),
        "history": [asdict(r) for r in records],
        "locked_md5": locked_md5,
    }

    metrics_path = OUTPUT_DIR / "metrics.json"
    metrics_path.write_text(json.dumps(result, indent=2))

    _write_training_log(
        log_path,
        records,
        header_lines=[
            "Experiment 01 — PF-STGT Training Log",
            f"Started: {datetime.now(timezone.utc).isoformat()}",
            f"Device: {device}",
            f"Seed: {config.seed}",
        ],
    )
    _write_summary(OUTPUT_DIR / "training_summary.md", result=result)
    _update_experiment_doc(result)

    file_handler.close()
    logging.getLogger().removeHandler(file_handler)

    print(f"Experiment 01 complete. Outputs -> {OUTPUT_DIR.relative_to(PROJECT_ROOT)}")
    print(f"Best epoch: {best_epoch} | Test demand MAE: {test_metrics.demand.mae:.4f}")
    return result


if __name__ == "__main__":
    run_experiment()
