# Phase 06 — Feature Validation Report

Validated **65** engineered features across train / validation / test.

## Checklist

| # | check | result |
| --- | --- | --- |
| 1 | Constant features | **0** found |
| 2 | Near-zero variance features | **0** found |
| 3 | Exact duplicate engineered pairs | **0** found |
| 4 | Unexpected missing values | **0** found |
| 5 | Infinite values | **0** found |
| 6 | Features passing validation | **65 / 65** |

## Expected warm-up missing values (train only)

- Lag-1 / load_lag_1: 1 missing row at series start (9 regions × 1 = 9 feature-series).
- Lag-7 / rolling_mean_7: 7 missing rows at series start (9 regions × 1 = 9 feature-series).
- All validation/test engineered features: 0 missing (history available from prior splits).

## Graph-related features

- No graph candidate features were implemented in Phase 05B (Batch 3 deferred).
- No graph-related features were removed in this phase (selection prohibited).

## Verdict

**Feature quality: PASS**
