# Experiment 01A — OSI Failure Investigation

## Objective

Investigate why PF-STGT fails to accurately predict OSI despite successfully forecasting demand.

---

## Inputs

Experiment 01 Results

PF-STGT Predictions

Ground Truth Targets

Training Logs

---

## Investigation Areas

### I1

OSI Distribution Analysis

Evaluate:

- Mean
- Standard Deviation
- Min
- Max
- Skewness

for:

- Train
- Validation
- Test

---

### I2

Prediction Distribution Analysis

Compare:

Actual OSI

vs

Predicted OSI

---

### I3

Variance Collapse Analysis

Evaluate:

std(actual)

vs

std(predicted)

---

### I4

Demand–OSI Relationship

Evaluate:

- Pearson Correlation
- Spearman Correlation

between:

Demand

and

OSI

---

### I5

Loss Weight Investigation

Current:

Demand = 1.0

Stress = 0.5

Evaluate:

Stress = 1.0

Stress = 2.0

without changing architecture.

---

### I6

Feature Sufficiency Analysis

Evaluate:

Can current inputs explain OSI?

Identify missing predictive signals.

---

## Required Outputs

osi_distribution_report.md

prediction_distribution_report.md

variance_analysis.md

correlation_analysis.md

loss_weight_analysis.md

root_cause_report.md

---

## Definition of Done

✔ Root cause identified

✔ Distribution analyzed

✔ Variance analyzed

✔ Loss weighting analyzed

✔ Recommendation produced
---
---
---
---
---

## Execution Record

**Date:** 2026-06-24
**Script:** `experiments/experiment_01A_osi_failure_investigation/run_investigation.py`
**Status:** COMPLETE

### Root cause (primary)

Loss-scale imbalance + demand-only early stopping → stress head variance collapse.

### Reports generated

| Report | Status |
| --- | --- |
| osi_distribution_report.md | ✓ |
| prediction_distribution_report.md | ✓ |
| variance_analysis.md | ✓ |
| correlation_analysis.md | ✓ |
| loss_weight_analysis.md | ✓ |
| root_cause_report.md | ✓ |

### Key finding

- Val std(predicted)/std(actual): see variance_analysis.md
- Val stress R² (Exp 01): -20.5387

### Scope compliance

- No retraining, baselines, ablations, or architecture changes.
