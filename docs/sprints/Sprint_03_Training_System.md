# Sprint 03 — Training System

## Objective

Implement the complete PF-STGT training infrastructure.

This sprint makes PF-STGT trainable.

No benchmark execution.

No experiment execution.

No explainability.

---

## Components

### Trainer

Responsibilities:

- Forward pass
- Loss computation
- Backpropagation
- Optimizer step

---

### Validator

Responsibilities:

- Validation loss
- Metric computation
- Model selection metrics

---

### Checkpoint Manager

Responsibilities:

- Save checkpoints
- Load checkpoints
- Best model tracking

---

### Early Stopping

Responsibilities:

- Monitor validation metric
- Stop training when needed

---

### Metrics

Demand:

- MAE
- RMSE
- MAPE
- R²

Stress:

- MAE
- RMSE
- R²

---

### Loss Functions

Demand Loss:

Huber Loss

Stress Loss:

MSE Loss

Combined Loss:

L_total =
1.0 × Demand Loss
+
0.5 × Stress Loss

---

### Experiment Runner

Responsibilities:

- Config loading
- Training execution
- Logging
- Reproducibility

---

## Deliverables

src/training/

src/evaluation/

tests/

Sprint report

---

## Definition of Done

✔ Trainer implemented

✔ Validator implemented

✔ Metrics implemented

✔ Checkpointing implemented

✔ Early stopping implemented

✔ Training loop works

✔ Ready for experiments

---

## Execution Record

**Date:** 2026-06-24  
**Script:** `scripts/sprint_03_training.py`  
**Report:** `results/phases/sprint_03_training/sprint_03_report.md`

### Packages Implemented

| Package | Modules |
| --- | --- |
| `src/training/` | config, losses, dataset, dataloader, trainer, validator, checkpoint, early_stopping, experiment_runner, seed |
| `src/evaluation/` | metrics |

### Loss & Optimizer (Phase 10 — frozen)

```
L_total = 1.0 × Huber_δ(demand) + 0.5 × MSE(OSI)
AdamW lr=5e-4, wd=1e-4; ReduceLROnPlateau factor=0.5, patience=5
Early stop: val macro demand MAE, patience=15, min_delta=0.01 MW
```

### Tests

- **38/38** total tests passing (12 new Sprint 03 tests + Sprint 01/02 regression)
- Smoke: `test_experiment_runner_smoke_loop` — 1 epoch, 1 train/val batch only (not a full experiment)

### Scope Compliance

- Training infrastructure only — no benchmark runs, HPO, or explainability
- Sprint 01 and Sprint 02 modules not modified; locked MD5s unchanged

### Status

Ready for benchmark experiment execution (B07 PF-STGT, seeds 42/123/456).