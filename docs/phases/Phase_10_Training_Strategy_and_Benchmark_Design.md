# Phase 10 — Training Strategy & Benchmark Design

## Objective

Define the complete experimental and training protocol for the proposed PF-STGT framework.

This phase establishes benchmark models, evaluation metrics, loss functions, and validation methodology.

---

## Inputs

Phase 08 Graph Construction

Phase 08.5 Task & Target Definition

Phase 09 Architecture Design

---

## Benchmark Models

Required

1. Linear Regression

2. Random Forest

3. XGBoost

4. LSTM

5. GRU

6. T-GCN

7. PF-STGT (Proposed)

---

## Evaluation Metrics

### Demand Forecasting

- MAE
- RMSE
- MAPE
- R²

### Operational Stress Forecasting

- MAE
- RMSE
- R²

---

## Training Strategy

Define:

- Batch size candidates
- Learning rate candidates
- Optimizer candidates
- Early stopping strategy
- Checkpoint strategy

---

## Multi-Task Learning

Define:

Task 1 Loss

Task 2 Loss

Combined Loss Strategy

---

## Validation Strategy

Define:

- Chronological split
- Validation procedure
- Test protocol
- Reproducibility protocol

---

## Deliverables

experiments/

- benchmark_design.md

- evaluation_protocol.md

- training_strategy.md

- loss_function_design.md

- reproducibility_protocol.md

results/phases/

phase_10_training_strategy/

- experiment_summary.md

- benchmark_rationale.md

- training_decision_report.md

---

## Definition of Done

✔ Benchmark models frozen

✔ Metrics frozen

✔ Loss functions defined

✔ Training strategy defined

✔ Validation strategy defined

✔ Ready for implementation

---

## Execution Record

### Completion Date

2026-06-24

### Frozen Experimental Protocol

| Component | Frozen specification |
| --- | --- |
| **Benchmark models (7)** | Linear Regression, Random Forest, XGBoost, LSTM, GRU, T-GCN, PF-STGT |
| **Demand metrics** | MAE, RMSE, MAPE, R² (macro over 9 regions + Dhaka separate) |
| **Stress metrics** | MAE, RMSE, R² (+ Pearson r supplementary) |
| **Input window** | T=7, h=1 (Phases 08.5/09) |
| **Training defaults** | batch=32, lr=5e-4, AdamW, weight_decay=1e-4 |
| **Early stopping** | patience=15 on val macro demand MAE |
| **Seeds** | [42, 123, 456] for deep models |
| **Loss (PF-STGT)** | λ1=1.0 Huber(δ=1 MW) + λ2=0.5 MSE + λ_reg=1e-4 |

### Benchmark Coverage

| ID | Model | Graph | Tasks |
| --- | --- | --- | --- |
| B01 | Linear Regression | No | Demand |
| B02 | Random Forest | No | Demand |
| B03 | XGBoost | No | Demand |
| B04 | LSTM | No | Demand |
| B05 | GRU | No | Demand |
| B06 | T-GCN | Yes (Phase 08 hybrid A) | Demand |
| B07 | PF-STGT | Yes | Demand + OSI |

### Validation Protocol

* Chronological 70/15/15 split (Phase 04): train 1,295 / val 277 / test 278 rows.
* Hyperparameter selection on **validation** macro demand MAE only.
* **Single** final test evaluation; train-only fit with best-val checkpoint.
* Warm-up: skip first 7 timesteps per split (Phase 06).

### Deliverables Generated

`experiments/`:

* `benchmark_design.md`
* `evaluation_protocol.md`
* `training_strategy.md`
* `loss_function_design.md`
* `reproducibility_protocol.md`

`results/phases/phase_10_training_strategy/`:

* `experiment_summary.md`
* `benchmark_rationale.md`
* `training_decision_report.md`
* `benchmark_registry.csv`

Script: `scripts/phase_10_training_strategy.py`

### Scope Compliance

* Experimental protocol definition only.
* **No model implementation, training, or results generated.**
* Locked phase outputs unchanged (`train_features.parquet` MD5: `b8b3bda95d0fd6cc65f4910d85a98e16`; `adjacency_matrix.csv` MD5: `dacb7ac3a827d00a4b61ea9400e75686`).

### Status

Ready for implementation and training (next phase).