# Experiment 01B — Multi-Task Optimization Repair

## Objective

Repair the OSI learning collapse identified in Experiment 01A.

Root Cause:

Demand loss dominates optimization.

Stress task receives negligible gradients.

---

## Inputs

Experiment 01 Results

Experiment 01A Analysis

---

## Hypothesis

The architecture is valid.

The optimization strategy is suppressing OSI learning.

---

## Intervention A

Loss Weight Study

Evaluate:

Stress Weight = 5

Stress Weight = 10

Stress Weight = 20

---

## Intervention B

Demand Loss Scaling

Evaluate:

Normalized Demand Loss

vs

Original Demand Loss

---

## Intervention C

Balanced Early Stopping

Current:

Demand-focused

Evaluate:

Combined validation objective

---

## Metrics

Demand:

- MAE
- RMSE
- MAPE
- R²

Stress:

- MAE
- RMSE
- R²
- Pearson r

---

## Success Criteria

OSI:

R² > 0

Predicted variance > 0

Stress gradients active

Demand performance not significantly degraded

---

## Required Outputs

repair_summary.md

loss_weight_study.md

gradient_analysis.md

validation_comparison.md

best_configuration.md

root_cause_confirmation.md

---

## Definition of Done

✔ Weight study completed

✔ Gradient study completed

✔ Best configuration identified

✔ OSI learning validated
---

## Execution Record

**Date:** 2026-06-25
**Script:** `experiments/experiment_01B_multitask_optimization_repair/run_repair_study.py`
**Status:** COMPLETE

**Best config:** W20 (λ₂=20.0)
**Val stress R²:** 0.6373
**Val demand R²:** 0.8630
