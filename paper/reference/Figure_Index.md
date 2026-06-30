# Figure Index

**Revised:** 2026-06-30  
**Numbering authority:** `paper/paper_outline/Paper_Outline.md` Part II, `publication_figures.md`  
**Asset root:** `paper/final_results_package/figures/`  
**Manuscript mapping:** Figure *n* placement per outline; §6 = `06_Methodology.md`, §8 = `08_Results.md`

---

## Main-text figures

| ID | Title | Section | File | Frozen source | Supporting claim |
| --- | --- | --- | --- | --- | --- |
| **1** | Overall Framework | §6.5 Methodology | `figure_01_framework.png` | Generated from `architecture/architecture_diagram.md` | PF-STGT multi-task pipeline with dual heads |
| **2** | Final S2 Architecture | §6.6 Methodology | `figure_02_s2_architecture.png` | `Final_Architecture_Decision.md` | S1→S2 freeze; corr-only graph; ΔMAE −4.66 MW vs S1 |
| **3** | Training Curves | §7.6 Exp. Setup | `figure_03_training_curves.png` | Exp01 `train_loss.png`, `val_loss.png` | W20 protocol convergence (historical reference) |
| **4** | Benchmark Comparison | §8.1 Results | `figure_04_benchmark_comparison.png` | Exp02 CSV + A6 row (generated) | S2 88.65 MW vs RF 97.03 vs S1 93.31 MW |
| **5** | Ablation Comparison | §8.3 Results | `figure_05_ablation_comparison.png` | Exp03 `ablation_results.csv` (generated) | A6 best multi-task; A4 demand-only bound 86.89 MW |
| **6a** | SHAP Summary — Stress | §8.5 Results | `figure_06_shap_summary_stress.png` | Exp04 frozen | G8 limitation_stack, G6 calendar_trend dominate stress |
| **6b** | SHAP Summary — Demand (Dhaka) | §8.5 Results | `figure_06_shap_summary_demand.png` | Exp04 frozen | G6, G4, G10 top Dhaka demand coalitions |
| **7** | Node Importance | §8.5 Results | `figure_07_node_importance.png` | Exp04 `figure_node_importance_heatmap.png` | Dhaka highest mass; ρ(attention, adjacency)=0.422 |
| **8** | Temporal Attribution | §8.5 Results | `figure_08_temporal_attribution.png` | Exp04 `figure_temporal_importance.png` | Near-uniform α_t; peak lag t−6 |
| **9** | Stress Attribution | §8.5 Results | `figure_09_stress_attribution.png` | Exp04 frozen | SHAP vs OSI components; 52.2% case agreement |

---

## Figure placement by section

| Section | Figures | Count |
| --- | --- | ---: |
| §6 Methodology | 1, 2 | 2 |
| §7 Experimental Setup | 3 | 1 |
| §8 Results | 4, 5, 6a, 6b, 7, 8, 9 | 7 (+1 subfigure) |
| **Total** | | **9 (+6b)** |

---

## Caption sources

Draft captions: `paper/final_results_package/publication_figures.md`  
Regeneration policy: Figures 1–5 via `build_publication_assets.py`; Figures 6–9 frozen Exp04 copies only.

---

## Overleaf export paths

| Package file | Overleaf target |
| --- | --- |
| `figure_01_framework.png` | `manuscript/overleaf/figures/figure_01_framework.png` |
| `figure_02_s2_architecture.png` | `manuscript/overleaf/figures/figure_02_s2_architecture.png` |
| `figure_03_training_curves.png` | `manuscript/overleaf/figures/figure_03_training_curves.png` |
| `figure_04_benchmark_comparison.png` | `manuscript/overleaf/figures/figure_04_benchmark_comparison.png` |
| `figure_05_ablation_comparison.png` | `manuscript/overleaf/figures/figure_05_ablation_comparison.png` |
| `figure_06_shap_summary_stress.png` | `manuscript/overleaf/figures/figure_shap_summary_stress.png` |
| `figure_06_shap_summary_demand.png` | `manuscript/overleaf/figures/figure_shap_summary_demand.png` |
| `figure_07_node_importance.png` | `manuscript/overleaf/figures/figure_node_importance_heatmap.png` |
| `figure_08_temporal_attribution.png` | `manuscript/overleaf/figures/figure_temporal_importance.png` |
| `figure_09_stress_attribution.png` | `manuscript/overleaf/figures/figure_stress_attribution.png` |

---

## Supplementary figures (optional)

| ID | Title | Source path | Suggested use |
| --- | --- | --- | --- |
| S1 | Signed stress SHAP bar | Exp04 `figure_shap_bar_stress.png` | Supplementary attribution |
| S2 | Actual vs predicted — Dhaka | Exp02A `plots/actual_vs_pred_Dhaka.png` | Classical fit diagnostic |
| S3 | Residual distribution — S1 | Exp02A `plots/residuals_B07.png` | Error distribution |
| S4 | Permutation ΔMAE ranking | Exp04 `figure_feature_importance_ranking.png` | Cross-method comparison |
| S5 | Regional SHAP contribution | Exp04 `figure_regional_contribution.png` | Extended spatial attribution |

---

## Caption guardrails (from consistency audit)

| Figure | Avoid in caption | Prefer |
| --- | --- | --- |
| 4 | "Outperforms all baselines" | "Macro demand MAE on test set; S2 is proposed final model" |
| 5 | "Best ablation overall" | "A6 best multi-task; A4 demand-only upper bound" |
| 8 | "Strong temporal selectivity" | "Near-uniform weights; marginal peak at t−6" |
| 9 | "Validates OSI drivers" | "Partial dual-path agreement (52.2%)" |

---

## Existence verification

All 10 main-text asset files verified present at `paper/final_results_package/figures/` (2026-06-30).
