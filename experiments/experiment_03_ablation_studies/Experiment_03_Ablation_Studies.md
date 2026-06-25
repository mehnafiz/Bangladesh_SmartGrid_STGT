# Experiment 03 — Ablation Studies

## Objective

Quantify the contribution of each PF-STGT component.

---

## Reference Model

A1

PF-STGT (Final W20 Configuration)

---

## Ablation A2

No Graph Module

Purpose:

Measure graph contribution.

---

## Ablation A3

No Transformer Module

Purpose:

Measure temporal transformer contribution.

---

## Ablation A4

Single-Task Demand Forecasting

Purpose:

Measure multi-task benefit.

---

## Ablation A5

Geographical Graph Only

Purpose:

Measure hybrid graph benefit.

---

## Ablation A6

Correlation Graph Only

Purpose:

Measure graph construction contribution.

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

---

## Statistical Testing

Wilcoxon Signed-Rank

Confidence Intervals

---

## Required Outputs

ablation_results.csv

component_contribution.md

ablation_rankings.md

statistical_significance.md

ablation_summary.md

---

## Definition of Done

✔ All ablations trained

✔ Metrics generated

✔ Contributions quantified

✔ Statistical testing completed

---

## Execution Record

**Date:** 2026-06-25
**Reference:** A1 W20 demand MAE 93.31 MW
**Script:** `experiments/experiment_03_ablation_studies/run_ablation.py`
