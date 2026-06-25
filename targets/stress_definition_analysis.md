# Stress Definition Analysis — Phase 08.5

Generated: 2026-06-24

## Variables investigated

| Signal | Description | Role |
| --- | --- | --- |
| `total_regional_load` | Σ regional shedding MW | Direct shedding severity |
| `generation_reserve` | Highest Gen − Eve Peak demand | Supply margin / headroom |
| `total_operational_limitation` | Sum of fuel/coal/water/maintenance limits | Exogenous constraint stack |
| `any_regional_shedding` | Binary shedding event flag | Sparse event indicator |

## Composite OSI formula (Phase 05B — frozen as stress target)

```
c1 = L_total / D_total
c2 = 1 - GR / Highest_Generation
c3 = TOL / Highest_Generation
OSI = mean(minmax_train(c1), minmax_train(c2), minmax_train(c3))  ∈ [0, 1]
```

Train-only min-max bounds applied to each component (Phase 05B leakage-safe fit).

## Candidate formulation comparison

| formulation_id   | formulation                                              | type                          |   total_score |   corr_with_any_shedding | limitations                                                                                  |
|:-----------------|:---------------------------------------------------------|:------------------------------|--------------:|-------------------------:|:---------------------------------------------------------------------------------------------|
| SF-01            | Binary Stress (OSI >= train median)                      | Classification (binary)       |            16 |                   0.2458 | Arbitrary median threshold; discards stress magnitude and reserve-only stress.               |
| SF-02            | Binary Stress (any regional shedding)                    | Classification (binary)       |            17 |                   1      | 30% positive rate; ignores pre-shedding reserve/limitation stress (Phase 07C GAP-06).        |
| SF-03            | Multi-Class Stress (OSI train tertiles: Low/Medium/High) | Classification (3-class)      |            17 |                 nan      | Tertile boundaries unstable over time; loses graded stress information.                      |
| SF-04            | Continuous Stress Score (composite OSI)                  | Regression (continuous [0,1]) |            24 |                   0.213  | Requires careful leakage control—same-day OSI must not be an input when predicting OSI(t+1). |

## Selected formulation

**Continuous Stress Score (regression on composite OSI)** (score **24/25**).

### Rationale

- **Phase 05A/05B:** `operational_stress_index` designed as novel multi-constraint composite for multi-task STGT.
- **Phase 07C GAP-06:** Daily regional stress from demand–supply–limitation dynamics is under-studied vs transmission reliability literature.
- Unifies shedding intensity (c1), reserve margin (c2), and operational limitations (c3) — broader than binary shedding alone.
- Train OSI correlation with `any_regional_shedding`: **0.213**; with `-generation_reserve`: **0.535**.

### Why not binary or multi-class?

- Binary shedding (SF-02): high interpretability but **30%** positive rate and misses reserve/limitation-only stress.
- Binary OSI median (SF-01): arbitrary cut; moderate shedding correlation (**0.25**).
- Multi-class tertiles (SF-03): balanced classes but loses graded stress needed for operational assessment.

## Stress target at forecast horizon

Predict **OSI(t+1)** (continuous regression) aligned with demand target horizon.

## Leakage note

Same-day `operational_stress_index` in feature tensors must **not** be used as input when predicting OSI(t+1); use lagged observables and exogenous covariates only (Phase 06 leakage discipline).
