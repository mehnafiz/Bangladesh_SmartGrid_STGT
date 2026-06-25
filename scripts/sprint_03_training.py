"""Sprint 03 — training system report generation."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from constants import LOCKED_MD5, PROJECT_ROOT
from training.config import TrainingConfig
from utils.logging import setup_logging
from utils.md5 import verify_locked_artifacts

REPORT_DIR = PROJECT_ROOT / "results" / "phases" / "sprint_03_training"


def main() -> None:
    setup_logging()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    md5_after = verify_locked_artifacts(PROJECT_ROOT, strict=True)
    config = TrainingConfig()

    lines = [
        "# Sprint 03 — Training System Report",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "Status: **COMPLETE**",
        "",
        "## Scope",
        "",
        "Implemented PF-STGT training infrastructure. No full experiments, HPO, or explainability executed.",
        "",
        "## Components delivered",
        "",
        "### src/training/",
        "",
        "| Module | Responsibility |",
        "| --- | --- |",
        "| `config.py` | Phase 10/11 frozen hyperparameters |",
        "| `losses.py` | Huber (demand) + MSE (stress) + multi-task |",
        "| `dataset.py` | PyTorch dataset over Sprint 01 foundation |",
        "| `dataloader.py` | Train/val/test DataLoader factory |",
        "| `trainer.py` | Forward, loss, backward, optimizer |",
        "| `validator.py` | Validation loss + metrics |",
        "| `checkpoint.py` | Best checkpoint save/load + metadata |",
        "| `early_stopping.py` | Val macro MAE monitor (patience=15) |",
        "| `experiment_runner.py` | End-to-end orchestration |",
        "| `seed.py` | Reproducibility |",
        "",
        "### src/evaluation/",
        "",
        "| Module | Metrics |",
        "| --- | --- |",
        "| `metrics.py` | Demand: MAE, RMSE, MAPE, R²; Stress: MAE, RMSE, R², Pearson r |",
        "",
        "## Loss function (Phase 10 — frozen)",
        "",
        "```",
        "L_total = 1.0 × Huber_δ(demand) + 0.5 × MSE(OSI)",
        "δ = 1.0 MW, macro-averaged over 9 regions",
        "```",
        "",
        "## Training defaults (Phase 10/11)",
        "",
        f"| Parameter | Value |",
        f"| --- | --- |",
        f"| Optimizer | AdamW |",
        f"| Learning rate | {config.learning_rate} |",
        f"| Weight decay | {config.weight_decay} |",
        f"| Batch size | {config.batch_size} |",
        f"| Max epochs | {config.max_epochs} |",
        f"| Grad clip | {config.grad_clip_norm} |",
        f"| Early stop patience | {config.early_stop_patience} |",
        f"| Early stop min delta | {config.early_stop_min_delta} MW |",
        f"| Scheduler | ReduceLROnPlateau (factor={config.scheduler_factor}, patience={config.scheduler_patience}) |",
        "",
        "## Checkpoint layout",
        "",
        "```",
        "checkpoints/B07/seed_{seed}/best.pt",
        "checkpoints/B07/seed_{seed}/config.yaml",
        "checkpoints/B07/seed_{seed}/metrics_val.json",
        "```",
        "",
        "## Tests",
        "",
        "```",
        "pytest tests/test_training_losses.py tests/test_evaluation_metrics.py \\",
        "       tests/test_early_stopping.py tests/test_checkpoint.py \\",
        "       tests/test_trainer_validator.py tests/test_experiment_runner.py -v",
        "```",
        "",
        "Includes 1-batch smoke loop in `test_experiment_runner_smoke_loop` (not a full experiment).",
        "",
        "## Locked artefact integrity",
        "",
    ]
    for path, expected in LOCKED_MD5.items():
        actual = md5_after[path]
        lines.append(f"- `{path}` MD5 unchanged: {actual == expected}")

    lines += [
        "",
        "## Sprint 01/02 integrity",
        "",
        "Foundation and model modules not modified.",
        "",
        "## Next step",
        "",
        "Execute benchmark experiments (B07 PF-STGT, seeds 42/123/456) in experiment phase.",
        "",
    ]

    report_path = REPORT_DIR / "sprint_03_report.md"
    report_path.write_text("\n".join(lines))
    print(f"Sprint 03 complete. Report -> {report_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
