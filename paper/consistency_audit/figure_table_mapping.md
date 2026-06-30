# Figure and Table Mapping — Consistency Audit

**Stage:** 05D — Research Consistency Audit  
**Executed:** 2026-06-30  
**Authoritative numbering:** `paper/final_results_package/` + `paper/paper_outline/Paper_Outline.md`  
**Note:** `paper/publication_freeze/frozen_figures_inventory.md` and `frozen_tables_inventory.md` use an earlier numbering scheme (Exp02A/Exp04-first). Manuscript writing must follow the **Final Results Package** numbering below.

---

## Summary

| Asset class | Count (main text) | All justified | Orphan assets |
| --- | ---: | --- | --- |
| Tables | 7 | ✅ Yes | 0 |
| Figures | 9 (+1 subfigure) | ✅ Yes | 0 |
| Supplementary tables | 4 | Optional | — |
| Supplementary figures | 5 | Optional | — |

**Verdict:** Every main-text figure and table maps to a manuscript section, supporting claim, and frozen source. No orphan or purposeless assets.

---

## Main-text tables

| Table | Title | Section | Purpose / supporting claim | Frozen source | Status |
| --- | --- | --- | --- | --- | --- |
| **1** | Dataset Summary | §6.2 | Documents N=9 regions, T=7, splits, MD5 reproducibility | `src/constants.py`, `frozen_results_inventory.md` | ✅ Justified |
| **2** | Training Configuration | §6.8, §7.2 | Defines frozen S2/A6 W20 protocol (λ₂=20, Adam, ES criterion) | A6 `config.yaml`, Exp01B `best_configuration.md` | ✅ Justified |
| **3** | Benchmark Comparison | §8.1 | Positions S2 vs B01–B07 on test demand + stress metrics | Exp02 `benchmark_results.csv` + A6 row | ✅ Justified |
| **4** | Benchmark Statistical Significance | §8.2 | Wilcoxon evidence that S1/B07 beats classical/GNN baselines on macro MAE | Exp02 `statistical_significance.md` | ✅ Justified |
| **5** | Ablation Study Results | §8.3 | Component effects A1–A6; A4 upper bound; A6=S2 | Exp03 `ablation_results.csv` | ✅ Justified |
| **6** | Architecture Comparison (S1–S4) | §8.4 | Documents S2 selection; S4 failure case | Exp03B `simplification_results.csv` | ✅ Justified |
| **7** | Explainability Summary | §8.5 | XAI headline metrics: SHAP, ρ, OSI agreement | Exp04 `xai_metrics.json` | ✅ Justified |

### Table-to-RQ / contribution map

| Table | RQs | Contributions |
| --- | --- | --- |
| 1 | — | C1 (context) |
| 2 | RQ4 | C3 |
| 3 | RQ1 | C1, C4 |
| 4 | RQ1 | C4 |
| 5 | RQ2, RQ3, RQ4 | C1, C2, C3 |
| 6 | RQ2, RQ3 | C1, C2 |
| 7 | RQ5 | C5 |

---

## Main-text figures

| Figure | Title | Section | Purpose / supporting claim | Asset path | Frozen source | Status |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | Overall Framework | §6.5 | End-to-end PF-STGT multi-task pipeline schematic | `figures/figure_01_framework.png` | Architecture docs (generated) | ✅ Justified |
| **2** | Final S2 Architecture | §6.6 | S1→S2 freeze decision; corr-only adjacency | `figures/figure_02_s2_architecture.png` | `Final_Architecture_Decision.md` | ✅ Justified |
| **3** | Training Curves | §7.6 | W20 convergence diagnostic; training stability context | `figures/figure_03_training_curves.png` | Exp01 `train_loss.png`, `val_loss.png` | ✅ Justified |
| **4** | Benchmark Comparison | §8.1 | Visual MAE ranking: S2 vs ML baselines vs S1 | `figures/figure_04_benchmark_comparison.png` | Exp02 CSV + A6 (generated) | ✅ Justified |
| **5** | Ablation Comparison | §8.3 | Visual ablation MAE ordering; A4 vs A6 trade-off | `figures/figure_05_ablation_comparison.png` | Exp03 CSV (generated) | ✅ Justified |
| **6a** | SHAP Summary — Stress | §8.5 | Global stress driver coalitions (G8, G6) | `figures/figure_06_shap_summary_stress.png` | Exp04 frozen | ✅ Justified |
| **6b** | SHAP Summary — Demand (Dhaka) | §8.5 | Global demand driver coalitions (G6, G4, G10) | `figures/figure_06_shap_summary_demand.png` | Exp04 frozen | ✅ Justified |
| **7** | Node Importance | §8.5 | Spatial attribution; Dhaka dominance; ρ=0.422 | `figures/figure_07_node_importance.png` | Exp04 `figure_node_importance_heatmap.png` | ✅ Justified |
| **8** | Temporal Attribution | §8.5 | Temporal α_t weights; near-uniform pattern | `figures/figure_08_temporal_attribution.png` | Exp04 `figure_temporal_importance.png` | ✅ Justified |
| **9** | Stress Attribution | §8.5 | SHAP vs OSI component dual-path comparison | `figures/figure_09_stress_attribution.png` | Exp04 frozen | ✅ Justified |

### Figure-to-RQ / contribution map

| Figure | RQs | Contributions |
| --- | --- | --- |
| 1 | — | C1 |
| 2 | RQ3 | C2 |
| 3 | RQ4 | C3 |
| 4 | RQ1 | C1, C4 |
| 5 | RQ2, RQ3, RQ4 | C2, C4 |
| 6a, 6b | RQ5 | C5 |
| 7 | RQ3, RQ5 | C2, C5 |
| 8 | RQ2, RQ5 | C4, C5 |
| 9 | RQ5 | C5 |

---

## Figure–table pairing consistency

| Results subsection | Table | Figure | Pairing rationale |
| --- | --- | --- | --- |
| §8.1 Benchmarks | 3 | 4 | Table = full metrics; Figure = MAE visual summary |
| §8.2 Significance | 4 | — | Statistical detail; no figure required |
| §8.3 Ablations | 5 | 5 | Table = all variants + Wilcoxon; Figure = MAE bars |
| §8.4 Architecture | 6 | — | Table sufficient; Figure 2 in Methods covers S1→S2 |
| §8.5 Explainability | 7 | 6–9 | Table = headline metrics; Figures = method outputs |

**No redundant figure–table pairs identified.** Each pairing serves complementary roles (numeric detail vs visual communication).

---

## Supplementary assets (optional)

### Supplementary tables

| ID | Title | Source | Purpose | Required? |
| --- | --- | --- | --- | --- |
| S1 | Classical benchmark verification | Exp02A | R² aggregation audit; MAE ranking confirmation | Recommended |
| S2 | Full grouped SHAP values | Exp04 CSVs | Complete attribution rankings | Optional |
| S3 | Permutation feature importance | Exp04 | Cross-method comparison (demand disagreement) | Recommended |
| S4 | Case-study attribution detail | Exp04 `case_studies.md` | Per-date OSI driver analysis | Recommended for RQ5 |

### Supplementary figures

| ID | Title | Source | Purpose | Required? |
| --- | --- | --- | --- | --- |
| S1 | Signed stress SHAP bar | Exp04 | Alternative SHAP visualization | Optional |
| S2 | Actual vs predicted — Dhaka | Exp02A | Classical model fit diagnostic | Recommended |
| S3 | Residual distribution — S1 | Exp02A | Error distribution for B07 | Optional |
| S4 | Permutation ΔMAE ranking | Exp04 | Supports claim X6 (method disagreement) | Recommended |
| S5 | Regional SHAP contribution | Exp04 | Extended spatial attribution | Optional |

---

## Numbering reconciliation (freeze vs package)

| Domain | Publication freeze inventory | Final Results Package (manuscript) | Resolution |
| --- | --- | --- | --- |
| **Tables** | Table 1 = benchmarks (Exp02) | Table 1 = dataset | **Use package numbering** for manuscript |
| **Figures** | Figure 1–2 = Exp02A verification | Figure 1–2 = framework + S2 arch | **Use package numbering**; move 02A plots to supplementary |

This discrepancy is documentation-only. Frozen experiment files are unchanged. Manuscript authors must import from `paper/final_results_package/`.

---

## Asset existence verification

| Asset | File present | Matches frozen data |
| --- | --- | --- |
| figure_01_framework.png | ✅ | Generated schematic |
| figure_02_s2_architecture.png | ✅ | Generated schematic |
| figure_03_training_curves.png | ✅ | Exp01 loss panels |
| figure_04_benchmark_comparison.png | ✅ | Matches Table 3 MAE values |
| figure_05_ablation_comparison.png | ✅ | Matches Table 5 MAE values |
| figure_06_shap_summary_stress.png | ✅ | Exp04 copy |
| figure_06_shap_summary_demand.png | ✅ | Exp04 copy |
| figure_07_node_importance.png | ✅ | Exp04 copy |
| figure_08_temporal_attribution.png | ✅ | Exp04 copy |
| figure_09_stress_attribution.png | ✅ | Exp04 copy |

---

## Caption consistency notes

| Figure | Caption risk | Audit recommendation |
| --- | --- | --- |
| 4 | “outperforms all baselines” | Caption should say “outperforms shown baselines on macro MAE; S2 row is final proposed model” |
| 5 | “best ablation” | Caption must note A4 is demand-only best; A6 is multi-task best |
| 8 | “temporal branch adds limited signal” | Consistent with A3/S4 nuance — qualify “on hybrid graph, marginal; required on corr graph” |
| 9 | “validates OSI drivers” | Caption should say “partial agreement (52.2%)” |

---

## Audit conclusion

- ✅ All 7 tables have defined manuscript purpose
- ✅ All 9 figures (+6b subfigure) have defined manuscript purpose
- ✅ Every Results subsection (§8.1–8.5) has at least one table or figure
- ✅ No duplicate numbering conflicts within the Final Results Package
- ⚠️ Authors must use package numbering, not early freeze inventory numbering

**Ready for Overleaf export** per `manuscript_assets_inventory.md`.
