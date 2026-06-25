# Experiment 02A — Classical Benchmark Verification

## Objective

Investigate the discrepancy observed between MAE and R² rankings for PF-STGT, Random Forest, and XGBoost.

---

## Inputs

Experiment 02 Results

benchmark_results.csv

performance_tables.md

statistical_significance.md

---

## Models

PF-STGT

Random Forest

XGBoost

---

## Investigation Areas

### V1

Metric Recalculation

Recompute:

- MAE
- RMSE
- MAPE
- R²

from saved predictions.

---

### V2

Prediction Distribution Analysis

Compare:

Actual

vs

Predicted

for all models.

---

### V3

Residual Analysis

Evaluate:

- Mean residual
- Residual variance
- Residual distribution

---

### V4

Error Aggregation Audit

Verify:

- Macro averaging
- Micro averaging
- Regional averaging

Consistency.

---

### V5

Variance Explanation Audit

Investigate why:

R² differs from MAE ranking.

---

### V6

Prediction Visualization

Generate:

Actual vs Predicted plots

for:

PF-STGT

Random Forest

XGBoost

---

## Required Outputs

metric_verification.md

prediction_distribution_analysis.md

residual_analysis.md

aggregation_audit.md

variance_explanation.md

benchmark_verification_report.md

---

## Definition of Done

✔ Metrics verified

✔ Aggregation verified

✔ R² discrepancy explained

✔ Benchmark ranking validated

---

## Execution Record

**Date:** 2026-06-25
**Root cause:** Inconsistent R² aggregation (pooled vs macro) between classical and PF-STGT paths
**Script:** `experiments/experiment_02A_classical_benchmark_verification/run_verification.py`
