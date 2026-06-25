# Sprint 03 — Training System Report

Generated: 2026-06-24
Status: **COMPLETE**

## Scope

Implemented PF-STGT training infrastructure. No full experiments, HPO, or explainability executed.

## Components delivered

### src/training/

| Module | Responsibility |
| --- | --- |
| `config.py` | Phase 10/11 frozen hyperparameters |
| `losses.py` | Huber (demand) + MSE (stress) + multi-task |
| `dataset.py` | PyTorch dataset over Sprint 01 foundation |
| `dataloader.py` | Train/val/test DataLoader factory |
| `trainer.py` | Forward, loss, backward, optimizer |
| `validator.py` | Validation loss + metrics |
| `checkpoint.py` | Best checkpoint save/load + metadata |
| `early_stopping.py` | Val macro MAE monitor (patience=15) |
| `experiment_runner.py` | End-to-end orchestration |
| `seed.py` | Reproducibility |

### src/evaluation/

| Module | Metrics |
| --- | --- |
| `metrics.py` | Demand: MAE, RMSE, MAPE, R²; Stress: MAE, RMSE, R², Pearson r |

## Loss function (Phase 10 — frozen)

```
L_total = 1.0 × Huber_δ(demand) + 0.5 × MSE(OSI)
δ = 1.0 MW, macro-averaged over 9 regions
```

## Training defaults (Phase 10/11)

| Parameter | Value |
| --- | --- |
| Optimizer | AdamW |
| Learning rate | 0.0005 |
| Weight decay | 0.0001 |
| Batch size | 32 |
| Max epochs | 200 |
| Grad clip | 1.0 |
| Early stop patience | 15 |
| Early stop min delta | 0.01 MW |
| Scheduler | ReduceLROnPlateau (factor=0.5, patience=5) |

## Checkpoint layout

```
checkpoints/B07/seed_{seed}/best.pt
checkpoints/B07/seed_{seed}/config.yaml
checkpoints/B07/seed_{seed}/metrics_val.json
```

## Tests

```
pytest tests/test_training_losses.py tests/test_evaluation_metrics.py \
       tests/test_early_stopping.py tests/test_checkpoint.py \
       tests/test_trainer_validator.py tests/test_experiment_runner.py -v
```

Includes 1-batch smoke loop in `test_experiment_runner_smoke_loop` (not a full experiment).

## Locked artefact integrity

- `data/features/train_features.parquet` MD5 unchanged: True
- `data/interim/bangladesh_smartgrid_clean.parquet` MD5 unchanged: True
- `graphs/adjacency_matrix.csv` MD5 unchanged: True

## Sprint 01/02 integrity

Foundation and model modules not modified.

## Next step

Execute benchmark experiments (B07 PF-STGT, seeds 42/123/456) in experiment phase.
