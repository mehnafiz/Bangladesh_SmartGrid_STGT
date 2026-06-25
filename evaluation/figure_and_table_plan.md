# Figure and Table Plan — Phase 15

Generated: 2026-06-24
Status: **FROZEN**

## Publication evidence map

Maps every required manuscript table and figure to data source,
format spec, and implementation output path.

---

## Required tables (main text)

### Table 1 — Main Benchmark Results

| Property | Specification |
| --- | --- |
| **Caption** | Test-set demand forecasting performance across seven benchmark models |
| **Rows** | B01–B07 (7 rows) |
| **Columns** | Model, MAE↓, RMSE↓, MAPE↓, R²↑, Dhaka MAE↓, Seeds |
| **Highlight** | Bold best macro MAE; underline B07 |
| **Source** | `results/evaluation/tables/table1_benchmark_demand_test.csv` |
| **Format** | LaTeX `booktabs`; 2 decimal MW, 1 decimal % |

### Table 2 — Ablation Results

| Property | Specification |
| --- | --- |
| **Caption** | Component ablation study vs PF-STGT full model (A1) on test split |
| **Rows** | A1, A2, A3, A4, A5-GEO, A6 (6 core; A5-CORR appendix) |
| **Columns** | Variant, ΔMAE, ΔR², ΔMAE_OSI, Relative deg.%, Significant |
| **Source** | `results/evaluation/tables/table2_ablation_results.csv` |
| **Notes** | A4: stress columns N/A; Δ positive = worse than A1 |

### Table 3 — Stress Forecast Results

| Property | Specification |
| --- | --- |
| **Caption** | Operational stress index (OSI) forecasting on test split |
| **Rows** | PF-STGT (A1), Persistence, Train median, A4 (N/A) |
| **Columns** | Model, MAE↓, RMSE↓, R²↑, Pearson r, High-regime MAE |
| **Source** | `results/evaluation/tables/table3_stress_forecast_test.csv` |
| **Notes** | Only A1/A variants with stress head report OSI metrics |

### Table 4 — Statistical Significance Results

| Property | Specification |
| --- | --- |
| **Caption** | Wilcoxon signed-rank tests on daily macro MAE (test split, Bonferroni corrected) |
| **Rows** | 6 benchmark + 5 ablation + 2 stress + 3 robustness = 16 |
| **Columns** | Comparison, ΔMAE, 95% CI, p, p_adj, Cohen's d, Sig., Verdict |
| **Source** | `results/evaluation/tables/table4_statistical_significance.csv` |

---

## Supplementary tables

| ID | Title | Rows × Cols | Source |
| --- | --- | --- | --- |
| **Table S1** | Per-region demand metrics (B07) | 9 × (MAE, RMSE, MAPE, R²) | per_region_metrics_test.csv |
| **Table S2** | Explainability quality metrics | 5 checks × (metric, threshold, result) | xai_quality_metrics.csv |
| **Table S3** | Robustness segment summary | ~15 segments × metrics | robustness_summary.csv |
| **Table S4** | Hyperparameter configuration | Phase 11 best config | optimization/ |
| **Table S5** | Dataset and split summary | Phase 04 stats | data/ |

---

## Required figures (main text)

### Figure 1 — Prediction vs Actual

| Property | Specification |
| --- | --- |
| **Type** | Dual-panel time series |
| **Panel A** | National aggregate demand: actual vs B07 vs B06 (test period) |
| **Panel B** | OSI: actual vs B07 prediction |
| **X-axis** | Date (2024-03-20 → 2024-12-30) |
| **Y-axis** | MW (demand) / OSI unitless [0,1] |
| **Annotations** | Shade shedding days (any_regional_shedding=1) |
| **Size** | 2 × 6 in (double column) |
| **Output** | `results/evaluation/figures/figure1_prediction_vs_actual.png` |

### Figure 2 — Regional Performance

| Property | Specification |
| --- | --- |
| **Type** | Grouped bar chart (or dot plot) |
| **X-axis** | 9 regions (Dhaka highlighted) |
| **Y-axis** | Test MAE (MW) |
| **Series** | B07, B06, B04 (3 bars per region) |
| **Inset** | Macro MAE ranking table |
| **Output** | `results/evaluation/figures/figure2_regional_performance.png` |

### Figure 3 — SHAP Summary

| Property | Specification |
| --- | --- |
| **Type** | SHAP beeswarm (grouped features G1–G11) |
| **Target** | Demand head — macro aggregate over 20 case studies |
| **Colour** | Feature value (red=high, blue=low) |
| **Top groups** | G1–G2 lags, G7 grid, G5 calendar expected top |
| **Output** | `results/evaluation/figures/figure3_shap_summary.png` |

### Figure 4 — Attention Visualization

| Property | Specification |
| --- | --- |
| **Type** | 2-panel: spatial + temporal |
| **Panel A** | 9×9 spatial attention heatmap on Bangladesh node layout |
| **Panel B** | Temporal attention α_t over T=7 lag days |
| **Overlay** | Hybrid adjacency edges on Panel A (Phase 08) |
| **Case** | Representative high-error day from Phase 14 top-10 |
| **Output** | `results/evaluation/figures/figure4_attention_visualization.png` |

### Figure 5 — Stress Attribution Case Study

| Property | Specification |
| --- | --- |
| **Type** | 3-panel case study |
| **Panel A** | OSI actual vs predicted on high-stress day |
| **Panel B** | SHAP grouped bar for stress head (G7, G8, G3, G11) |
| **Panel C** | Ground-truth c1/c2/c3 decomposition bars |
| **Annotation** | Driver label (shedding / reserve / limitation) |
| **Selection** | Top decile OSI day from Phase 12 case-study strata |
| **Output** | `results/evaluation/figures/figure5_stress_attribution_case_study.png` |

---

## Supplementary figures

| ID | Title | Type | Output |
| --- | --- | --- | --- |
| **Fig S1** | Extreme event MAE comparison | Grouped bar | figureS1_extreme_events.png |
| **Fig S2** | Stress regime error distribution | Violin plot | figureS2_stress_regimes.png |
| **Fig S3** | Regional MAPE by month | Heatmap 9×12 | figureS3_regional_heatmap.png |
| **Fig S4** | Ablation ΔMAE waterfall | Waterfall chart | figureS4_ablation_waterfall.png |
| **Fig S5** | Training convergence | Loss curves (val MAE) | figureS5_training_curves.png |

---

## Figure–table cross-reference

| Evidence claim | Table | Figure |
| --- | --- | --- |
| Overall superiority | Table 1, 4 | Fig 1 |
| Regional accuracy | Table S1 | Fig 2, S3 |
| Component value | Table 2, 4 | Fig S4 |
| Stress forecasting | Table 3 | Fig 1B, 5 |
| Interpretability | Table S2 | Fig 3, 4, 5 |
| Robustness | Table S3 | Fig S1, S2 |

## Style guide (publication-ready)

| Element | Specification |
| --- | --- |
| Font | Times New Roman or serif, 10 pt |
| Colour palette | Colorblind-safe (Okabe-Ito) |
| Resolution | 300 DPI PNG + vector PDF |
| Region order | Fixed: Barishal → Sylhet (alphabetical) |
| Dhaka highlight | Distinct colour / bold label |

## Generation checklist (implementation phase)

- [ ] Table 1 populated from B01–B07 test runs
- [ ] Table 2 populated from A1–A6 ablation runs
- [ ] Table 3 populated from stress predictions
- [ ] Table 4 populated from Wilcoxon + bootstrap pipeline
- [ ] Figures 1–5 rendered from results/evaluation/
- [ ] Supplementary tables S1–S3 generated
- [ ] All artefacts referenced in evaluation_decision_report
