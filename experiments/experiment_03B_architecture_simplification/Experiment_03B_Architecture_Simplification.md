# Experiment 03B — Architecture Simplification Study

## Objective

Evaluate whether PF-STGT complexity is justified.

---

## Reference

S1

PF-STGT (Final W20)

---

## Simplified Model S2

Correlation-Only PF-STGT

Remove:

Geographical Graph

Keep:

Correlation Graph

---

## Simplified Model S3

No-Transformer PF-STGT

Remove:

Temporal Transformer

Keep:

Graph Branch

---

## Simplified Model S4

Correlation-Only + No-Transformer

Keep:

Correlation Graph

Remove:

Geographical Graph

Remove:

Transformer

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

## Evaluation Questions

Q1

Does correlation-only outperform PF-STGT?

---

Q2

Does removing transformer hurt performance?

---

Q3

Can a simpler model achieve similar performance?

---

Q4

Is PF-STGT complexity justified?

---

## Required Outputs

simplification_results.csv

complexity_analysis.md

performance_vs_complexity.md

architecture_recommendation.md

final_architecture_decision.md

---

## Definition of Done

✔ Simplified models evaluated

✔ Complexity analyzed

✔ Architecture recommendation produced

✔ Final architecture decision produced

---

---

## Execution Record

**Date:** 2026-06-25
**Best demand:** Correlation-Only PF-STGT (S2) — 88.65 MW
**Script:** `experiments/experiment_03B_architecture_simplification/run_simplification.py`
