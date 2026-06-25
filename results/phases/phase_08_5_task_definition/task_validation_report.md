# Task Validation Report — Phase 08.5

Generated: 2026-06-24

## Frozen decisions checklist

| Decision | Status | Value |
| --- | --- | --- |
| Forecast target | FROZEN | 9 × `{Region}_demand` |
| Forecast horizon | FROZEN | h=1 day, single-step |
| Stress target | FROZEN | Continuous OSI (SF-04) |
| Multi-task formulation | FROZEN | Task 1 demand + Task 2 OSI regression |

## Data validation

| Check | Result |
| --- | --- |
| Train rows | 1295 |
| All 9 demand columns present | PASS |
| OSI in [0,1] on train | PASS (min=0.061, max=0.711) |
| h=1 horizon feasible on daily series | PASS |
| Stress formulation selected | PASS (SF-04, score 24/25) |

## Locked input integrity

- `data/features/train_features.parquet` MD5: `b8b3bda95d0fd6cc65f4910d85a98e16` (unchanged)
- `data/interim/bangladesh_smartgrid_clean.parquet` MD5: `4255024d735a91a4b53b2edee203d0ca` (unchanged)
- `graphs/adjacency_matrix.csv` MD5: `dacb7ac3a827d00a4b61ea9400e75686` (unchanged)

## Horizon sanity (h=1 vs h=7)

|   horizon_days |   mean_regional_mape_pct |   mean_regional_autocorr_lag_h |
|---------------:|-------------------------:|-------------------------------:|
|              1 |                    5.546 |                         0.9237 |
|              7 |                    8.776 |                         0.8    |

## Status

**PASS** — targets frozen; ready for STGT architecture phase.
