# Task Definition Decision Rationale — Phase 08.5

Generated: 2026-06-24

## 1. Forecast target = regional demand

Phase 02 established demand≈supply redundancy and high inter-regional correlation. Regional `{Region}_demand` is the primary graph-node signal aligned with Phase 08 node features and literature load-forecasting cluster (Phase 07C).

## 2. Horizon = 1 day, single-step

- h=1 persistence MAPE (5.55%) beats h=7 (8.78%).
- Daily dataset cadence (Phase 01) and lag-1 engineered features (Phase 05B) support 1-day-ahead operational forecasting.

## 3. Stress = continuous OSI (not binary/multi-class)

| formulation                                              |   total_score | limitations                                                                                  |
|:---------------------------------------------------------|--------------:|:---------------------------------------------------------------------------------------------|
| Continuous Stress Score (composite OSI)                  |            24 | Requires careful leakage control—same-day OSI must not be an input when predicting OSI(t+1). |
| Binary Stress (any regional shedding)                    |            17 | 30% positive rate; ignores pre-shedding reserve/limitation stress (Phase 07C GAP-06).        |
| Multi-Class Stress (OSI train tertiles: Low/Medium/High) |            17 | Tertile boundaries unstable over time; loses graded stress information.                      |
| Binary Stress (OSI >= train median)                      |            16 | Arbitrary median threshold; discards stress magnitude and reserve-only stress.               |

Continuous OSI (SF-04) scores highest because it is the only formulation that:

1. Integrates shedding, reserve margin, and limitation stack (Phase 05B design intent).
2. Addresses Phase 07C GAP-06 (daily operational stress vs asset reliability).
3. Supports regression without arbitrary class boundaries.

## 4. Two-task multi-task formulation

Task 1 (regional demand) + Task 2 (OSI) provides complementary, non-redundant objectives per Phase 02 guidance. Architecture and loss weighting deferred to subsequent phases.
