# Experiment 02 — Benchmark Model Comparison

## Objective

Compare PF-STGT against all benchmark models using identical datasets, targets, splits, and evaluation metrics.

---

## Models

### B01

Linear Regression

---

### B02

Random Forest

---

### B03

XGBoost

---

### B04

LSTM

---

### B05

GRU

---

### B06

T-GCN

---

### B07

PF-STGT (Final W20 Configuration)

---

## Dataset

Processed Bangladesh Smart Grid Dataset

Nodes: 9

Lookback Window: 7

Forecast Horizon: 1

---

## Split Protocol

Chronological split.

Use the exact same:

- Train
- Validation
- Test

for every model.

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

## Statistical Evaluation

Wilcoxon Signed-Rank Test

Confidence Intervals

---

## Required Outputs

benchmark_results.csv

benchmark_summary.md

benchmark_rankings.md

statistical_significance.md

performance_tables.md

---

## Definition of Done

✔ All benchmark models trained

✔ Metrics generated

✔ Rankings generated

✔ Statistical testing completed

✔ PF-STGT comparison completed

---

---

## Execution Record

**Date:** 2026-06-25
**Best model:** PF-STGT (W20) (B07)
**Script:** `experiments/experiment_02_benchmark_models/run_benchmark.py`
