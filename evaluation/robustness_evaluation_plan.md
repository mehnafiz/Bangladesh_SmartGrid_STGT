# Robustness Evaluation Plan — Phase 15

Generated: 2026-06-24
Status: **FROZEN**

## Objective (D5)

Evaluate PF-STGT (B07 / A1) under operational stress, regional heterogeneity,
and extreme events — segments defined in Phase 14 error analysis.

## Reference model

**B07 PF-STGT (A1, seed 42)** on test split (278 days).

## Robustness segments

### R1 — Extreme events (Phase 14 E4)

| Event type | Threshold (train-fitted) | Metric |
| --- | --- | --- |
| Demand spike | demand > μ_train + 2σ | Event MAE, spike recall |
| Supply drop | generation_reserve < Q10_train | Event MAE |
| Load shedding | any_regional_shedding=1 | Event MAE, OSI MAE |

**Comparison:** Event MAE / Normal MAE ratio; B07 vs B06 on shedding days.

### R2 — High stress days (Phase 14 E3)

| Regime | Definition | Metric |
| --- | --- | --- |
| High stress | OSI > train tertile Q2 | OSI MAE, bias, calibration |
| Medium | Q1 < OSI ≤ Q2 | OSI MAE |
| Low | OSI ≤ Q1 | OSI MAE |

Test split: ~60% High stress days — primary robustness focus.

### R3 — Regional variability (Phase 14 E2)

| Analysis | Metric | Pass criterion |
| --- | --- | --- |
| Per-region MAPE range | max(MAPE_r) − min(MAPE_r) | Report; no single region > 2× macro MAPE |
| Dhaka vs periphery | MAPE_Dhaka vs mean(MAPE_periphery) | Dhaka MAPE ≤ periphery mean |
| Low-connectivity subset | MAPE on Barishal, Rangpur, Sylhet | B07 < B06 on subset |

### R4 — Temporal robustness (Phase 14 E5)

| Segment | Expected challenge | Metric |
| --- | --- | --- |
| Month 9 (Apr–Oct peak) | Cooling load | seasonality_ratio = MAE_m9 / MAE_all |
| Holidays | Calendar shift | MAE_holiday / MAE_nonholiday |
| Post-trend test period | Upward demand drift | Bias on last test quartile |

### R5 — Seed robustness (deep models)

B07 test MAE: mean ± std over seeds {42, 123, 456}.
Coefficient of variation CV = std/mean < 0.05 → stable.

## Table S3 — Robustness Summary (supplementary)

| Column | Description |
| --- | --- |
| segment_id | R1–R5 sub-segment |
| segment_name | Display label |
| n_days | Sample count |
| mae_demand_mw | Demand MAE on segment |
| mae_osi | OSI MAE (if applicable) |
| ratio_vs_normal | Segment MAE / baseline MAE |
| b07_vs_b06_delta | ΔMAE vs T-GCN on segment |

## Supplementary figures

| ID | Title | Content |
| --- | --- | --- |
| **Fig S1** | Extreme event performance | Grouped bar: normal vs event MAE by type |
| **Fig S2** | Stress regime error | Violin: |OSI − OSI_hat| by Low/Med/High |
| **Fig S3** | Regional MAPE heatmap | 9 regions × months |

## Robustness claim gates

| Claim | Criterion |
| --- | --- |
| Extreme resilience | Event MAE ratio < 1.5× normal MAE |
| High-stress accuracy | High-regime OSI MAE < persistence |
| Regional fairness | No region MAPE > 2× macro MAPE |
| Temporal stability | seasonality_ratio < 1.3 |

## Output artefacts

```
results/evaluation/robustness/robustness_summary.csv
results/evaluation/robustness/extreme_event_metrics.csv
results/evaluation/robustness/stress_regime_metrics.csv
results/evaluation/robustness/regional_variability.csv
results/evaluation/robustness/temporal_segments.csv
results/evaluation/figures/figureS1_extreme_events.png
results/evaluation/figures/figureS2_stress_regimes.png
results/evaluation/figures/figureS3_regional_heatmap.png
```
