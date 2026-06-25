# Stress Error Framework — Phase 14

Generated: 2026-06-24
Status: **FROZEN**

## Scope (E3)

Operational Stress Index (OSI) forecast error analysis for Task 2 (Phase 08.5 SF-04).

## Target definition (frozen)

```
c1 = L_total / D_total              shedding intensity
c2 = 1 − GR / Highest_Gen           reserve margin
c3 = TOL / Highest_Gen              limitation stack
OSI = mean(minmax_train(c1), minmax_train(c2), minmax_train(c3))  ∈ [0, 1]
```

**Leakage rule:** same-day OSI never an input when predicting OSI(t+1) (Phase 08.5/12).

## Stress regime segmentation

Use **train-frozen tertile boundaries** on OSI (Phase 08.5 `stress_3class`):

| Regime | Definition | Train % | Test % (approx) |
| --- | --- | --- | --- |
| **Low Stress** | OSI ≤ train tertile Q1 | 33.4% | 16.2% |
| **Medium Stress** | Q1 < OSI ≤ Q2 | 33.3% | 24.1% |
| **High Stress** | OSI > Q2 | 33.4% | 59.7% |

Test-period shift toward high stress (63% any shedding days) — report regime sample counts.

## Primary metrics by regime

| Metric | Formula | Interpretation |
| --- | --- | --- |
| MAE_regime | mean(|OSI − OSI_hat|) | Overall stress accuracy |
| RMSE_regime | sqrt(mean((OSI − OSI_hat)²)) | Penalises large misses |
| R²_regime | 1 − SS_res/SS_tot | Explained variance |
| Bias_regime | mean(OSI_hat − OSI) | Over/under-prediction of stress |
| Calibration slope | linreg(OSI, OSI_hat) slope | 1.0 = well calibrated |

## Secondary diagnostics

| Diagnostic | Method |
| --- | --- |
| Component attribution error | Compare argmax(c1,c2,c3) to SHAP driver (Phase 12) |
| Shedding alignment | OSI error when `any_regional_shedding=1` vs 0 |
| Persistence gap | MAE vs OSI(t) persistence baseline (Phase 10) |
| High-stress recall | Fraction of High regime with OSI_hat > train Q2 |

## Expected failure modes

| Regime | Expected error pattern | Root-cause link |
| --- | --- | --- |
| Low | Over-prediction (bias > 0) | Model trained on fewer low-stress test days |
| Medium | Highest calibration uncertainty | Boundary instability (Phase 08.5 limitation) |
| High | Under-prediction of peak OSI | Sparse extreme c1/c3 combinations |

## Multi-task cross-check (Phase 13 A4)

Compare stress metrics on A1 vs demand-only A4 (stress head absent on A4).
Demand error on high-stress days: does multi-task A1 reduce |e_r| when OSI is High?

## Visualisation spec

| Figure | Content |
| --- | --- |
| `osi_scatter_by_regime.png` | OSI vs OSI_hat coloured by regime |
| `osi_error_violin.png` | |OSI − OSI_hat| by Low/Med/High |
| `osi_component_error_bars.png` | MAE on days dominated by c1 vs c2 vs c3 |

## Output artefacts

```
results/error_analysis/stress/stress_metrics_by_regime.csv
results/error_analysis/stress/stress_calibration_report.csv
results/error_analysis/stress/stress_error_on_shedding_days.csv
results/error_analysis/stress/stress_component_driver_errors.csv
```

## Acceptance criteria

- All three regimes reported with sample counts.
- PF-STGT stress MAE < persistence baseline on test (Phase 10 gate).
- High-stress regime analysed separately (majority of test days).
