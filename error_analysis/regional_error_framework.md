# Regional Error Framework — Phase 14

Generated: 2026-06-24
Status: **FROZEN**

## Scope (E2)

Per-region demand forecast error analysis for all 9 division nodes on the test split.

## Regions under study

Barishal, Chattogram, Cumilla, Dhaka, Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet.

**Dhaka** reported separately (Phase 10 rule): ~35.65% mean national demand share (Phase 02).

## Graph connectivity context (Phase 08)

| region     |   graph_degree | connectivity_tier   |
|:-----------|---------------:|:--------------------|
| Barishal   |              4 | Low                 |
| Chattogram |              5 | Mid                 |
| Cumilla    |              7 | High                |
| Dhaka      |              8 | High                |
| Khulna     |              5 | Mid                 |
| Mymensingh |              6 | High                |
| Rajshahi   |              5 | Mid                 |
| Rangpur    |              4 | Low                 |
| Sylhet     |              4 | Low                 |

## Residual definitions

```
e_r(d) = D_r(d) − D̂_r(d)          signed residual (MW)
|e_r(d)|                         absolute error
APE_r(d) = |e_r(d)| / |D_r(d)| × 100%   (exclude D_r=0)
```

## Primary metrics (per region, test split)

| Metric | Formula | Report |
| --- | --- | --- |
| MAE_r | mean(|e_r|) | MW + rank |
| RMSE_r | sqrt(mean(e_r²)) | MW |
| MAPE_r | mean(APE_r) | % |
| R²_r | 1 − SS_res/SS_tot | unitless |
| Bias_r | mean(e_r) | MW (systematic over/under) |
| p95_|e|_r | 95th percentile | MW tail risk |

## Segmentation dimensions

| Dimension | Purpose |
| --- | --- |
| All test days | Baseline regional leaderboard |
| High-error days | Top 10% macro MAE days — which regions drive spike? |
| Connectivity tier | High vs mid vs low graph degree |
| Demand share quartile | Large vs small regions (regional_demand_share) |

## Regional failure hypotheses

| Region | Expected failure mode | Evidence |
| --- | --- | --- |
| Dhaka | Trend extrapolation; national peak driver | Phase 02 dominance |
| Chattogram | Port/industrial volatility | High demand variance |
| Mymensingh | Sparse shedding in OSI c1 (Phase 12) | Stress attribution design |
| Barishal / Rangpur / Sylhet | Higher MAPE (low degree, smaller MW) | Graph E6 |
| Cumilla | Benefit from hybrid non-geo edges | ρ≈0.93 Barishal–Cumilla |

## Comparison protocol

1. PF-STGT vs **T-GCN** per-region ΔMAE (graph baseline).
2. PF-STGT vs **LSTM** — quantify graph gain on low-connectivity subset.
3. Phase 13 **A2 (−Graph)** regional ΔMAE — confirm spatial module helps periphery most.

## Visualisation spec

| Figure | Content |
| --- | --- |
| `regional_mae_bar.png` | 9-region MAE ranked |
| `regional_error_boxplot.png` | Residual distribution per region |
| `dhaka_vs_macro.png` | Dhaka MAE vs macro MAE time series |
| `regional_mae_by_month_heatmap.png` | E2 × E5 interaction |

## Output artefacts

```
results/error_analysis/regional/per_region_metrics_test.csv
results/error_analysis/regional/regional_error_ranking.csv
results/error_analysis/regional/regional_bias_report.csv
results/error_analysis/regional/connectivity_tier_mae.csv
```

## Acceptance criteria

- All 9 regions reported with n=278 test days each.
- Dhaka MAE and macro MAE both reported in summary table.
- At least one region where PF-STGT beats T-GCN on MAE (validates graph value).
