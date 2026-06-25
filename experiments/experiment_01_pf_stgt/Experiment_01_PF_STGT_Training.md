# Experiment 01 — PF-STGT Training

## Objective

Train the proposed PF-STGT model using the finalized architecture and default hyperparameters.

This experiment validates:

- Training stability
- Convergence behavior
- Generalization performance

No baseline models.

No ablation studies.

No explainability analysis.

---

## Model

PF-STGT

Components:

- Graph Transformer
- Temporal Transformer
- Parallel Fusion
- Demand Head
- Stress Head

---

## Dataset

Processed Bangladesh Smart Grid Dataset

Nodes: 9

Lookback Window (T): 7

Forecast Horizon (H): 1

Tasks:

1. Regional Demand Forecasting

2. Operational Stress Forecasting

---

## Training Configuration

Optimizer:

AdamW

Loss:

Demand:
Huber Loss

Stress:
MSE Loss

Combined:

L_total =
1.0 × Demand Loss
+
0.5 × Stress Loss

EarlyStopping:

Patience = 15

---

## Required Outputs

Training Curves

- train_loss.png
- val_loss.png

Metrics

- metrics.json

Model

- best_model.pt

Logs

- training_log.txt

Summary

- training_summary.md

---

## Evaluation Metrics

Demand

- MAE
- RMSE
- MAPE
- R²

Stress

- MAE
- RMSE
- R²

---

## Definition of Done

✔ Training completed

✔ Best checkpoint saved

✔ Curves generated

✔ Metrics generated

✔ Report generated
---

## Execution Record

**Date:** 2026-06-24
**Script:** `experiments/experiment_01_pf_stgt/run_experiment.py`
**Status:** COMPLETE

### Run Summary

| Item | Value |
| --- | --- |
| Seed | 42 |
| Device | mps |
| Parameters | 749,058 |
| Training time | 281.2s |
| Epochs run | 50 |
| Best epoch | 35 |
| Early stopping epoch | 50 |
| Stopped early | True |

### Validation metrics (best checkpoint)

| Task | MAE | RMSE | MAPE / R² |
| --- | --- | --- | --- |
| Demand | 56.6708 | 76.8344 | MAPE 4.5926, R² 0.8780 |
| Stress | 0.2966 | 0.3038 | R² -20.5387 |

### Test metrics (best checkpoint)

| Task | MAE | RMSE | MAPE / R² |
| --- | --- | --- | --- |
| Demand | 86.8181 | 118.3754 | MAPE 6.5199, R² 0.7299 |
| Stress | 0.3375 | 0.3502 | R² -12.9918 |

### Deliverables

| File | Status |
| --- | --- |
| train_loss.png | Generated |
| val_loss.png | Generated |
| metrics.json | Generated |
| best_model.pt | Generated |
| training_log.txt | Generated |
| training_summary.md | Generated |

### Locked artefact integrity

- `data/features/train_features.parquet` unchanged: True
- `data/interim/bangladesh_smartgrid_clean.parquet` unchanged: True
- `graphs/adjacency_matrix.csv` unchanged: True