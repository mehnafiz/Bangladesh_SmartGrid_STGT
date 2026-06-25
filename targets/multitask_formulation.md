# Multi-Task Formulation — Phase 08.5

Generated: 2026-06-24
Status: **FROZEN**

## Overview

Shared spatio-temporal graph representation (Phase 08 hybrid adjacency) with **two task heads**:

| Task | Name | Type | Target at t+h | Output |
| --- | --- | --- | --- | --- |
| **Task 1** | Regional Load Forecasting | Regression | \(D_r(t+1)\) per node | Vector \(\hat{D} \in \mathbb{R}^9\) (MW) |
| **Task 2** | Operational Stress Assessment | Regression | OSI\(t+1)\) | Scalar \(\widehat{OSI} \in [0,1]\) |

## Task 1 — Regional Load Forecasting

- **Objective:** Minimise regional demand forecast error across 9 divisions.
- **Loss (conceptual):** \(L_1 = \frac{1}{9} \sum_r \ell(\hat{D}_r, D_r)\) with \( \ell \) = MAE or Huber on MW scale.
- **Output format:** 9 continuous values (one per graph node); optional per-node standardisation at training time.
- **Evidence:** Phase 02 strong seasonality/trend; Phase 08 graph coupling; Phase 07C GAP-04.

## Task 2 — Operational Stress Assessment

- **Objective:** Predict composite operational stress score integrating shedding, reserve, and limitations.
- **Loss (conceptual):** \(L_2 = \ell_{MSE}(\widehat{OSI}, OSI)\) on [0,1] bounded target.
- **Output format:** Single continuous score per forecast day (graph-level head).
- **Evidence:** Phase 05B OSI; Phase 07C GAP-06; selected SF-04 in stress analysis.

## Joint training objective (conceptual — weights deferred to training phase)

```
L_total = λ1 · L1 + λ2 · L2
```

Task weighting \(\lambda_i\) and uncertainty balancing **not fixed here** (no training in this phase).

## Task complementarity (Phase 02 / 07C)

- Demand (Task 1) and stress (Task 2) are **non-collinear**: demand≈supply but OSI adds reserve/limitation/shedding composite.
- Shedding events partially encoded in OSI \(c_1\); dedicated sparse shedding head remains optional in architecture phase.

## Input–target alignment

- Forecast horizon: **h = 1** day for both tasks.
- Features at time \(t\): node lags, calendar, exogenous limitations, graph structure — **no same-day target leakage**.

## Scope

- Task/target definition only; **STGT architecture not designed** in this phase.
