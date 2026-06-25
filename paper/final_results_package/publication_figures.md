# Publication Figures — Stage 05B Final Results Package

**Generated:** 2026-06-16  
**Package directory:** `paper/final_results_package/figures/`  
**Build script:** `paper/final_results_package/build_publication_assets.py`

Figures 1–5 are assembled from frozen data and architecture documentation. Figures 6–9 are copied from Experiment 04 frozen outputs. No model inference or retraining was performed.

---

## Figure 1 — Overall Framework

| Property | Value |
| --- | --- |
| **File** | `figures/figure_01_framework.png` |
| **Type** | Schematic (generated from frozen architecture spec) |
| **Source** | `architecture/architecture_diagram.md`, `final_model_specification.md` |
| **Caption (draft)** | End-to-end PF-STGT multi-task forecasting framework: regional node tensor, global context, and graph adjacency feed parallel graph and temporal transformers, fused for dual demand and operational stress index (OSI) heads. Final model S2 uses correlation graph only (τ=0.65). |

---

## Figure 2 — Final S2 Architecture

| Property | Value |
| --- | --- |
| **File** | `figures/figure_02_s2_architecture.png` |
| **Type** | Architecture decision diagram (generated) |
| **Source** | `experiments/architecture_freeze_revision/Final_Architecture_Decision.md` |
| **Caption (draft)** | Architecture freeze: S2 retains the full PFSTGT trunk with correlation-only adjacency, improving test demand MAE by 4.66 MW (−5.0%) over superseded S1 hybrid graph while raising stress R² from 0.585 to 0.745. |

---

## Figure 3 — Training Curves

| Property | Value |
| --- | --- |
| **File** | `figures/figure_03_training_curves.png` |
| **Type** | Combined panel (historical reference) |
| **Source** | `experiments/experiment_01_pf_stgt/train_loss.png`, `val_loss.png` |
| **Caption (draft)** | Training and validation loss curves for the W20 multi-task repair protocol (Experiment 01/01B reference run). S2 uses identical training configuration; curves shown as frozen historical diagnostic. |

---

## Figure 4 — Benchmark Comparison

| Property | Value |
| --- | --- |
| **File** | `figures/figure_04_benchmark_comparison.png` |
| **Type** | Horizontal bar chart (generated from frozen CSV) |
| **Source** | `experiments/experiment_02_benchmark_models/benchmark_results.csv` + A6 (S2) |
| **Models shown** | Random Forest, XGBoost, PF-STGT S1 (B07), **PF-STGT S2 ★**, T-GCN |
| **Caption (draft)** | Test-set macro demand MAE comparison. S2 (88.65 MW) outperforms classical ML baselines and the original hybrid-graph S1 reference (93.31 MW). |

---

## Figure 5 — Ablation Comparison

| Property | Value |
| --- | --- |
| **File** | `figures/figure_05_ablation_comparison.png` |
| **Type** | Horizontal bar chart (generated from frozen CSV) |
| **Source** | `experiments/experiment_03_ablation_studies/ablation_results.csv` |
| **Caption (draft)** | Ablation study demand MAE on the test set. A6 (S2, correlation graph) achieves the best multi-task demand performance; A4 (single-task) achieves lowest demand MAE but forfeits stress forecasting. |

---

## Figure 6 — SHAP Summary

| Property | Value |
| --- | --- |
| **Files** | `figures/figure_06_shap_summary_stress.png`, `figures/figure_06_shap_summary_demand.png` |
| **Type** | Grouped SHAP beeswarm (frozen Exp04) |
| **Source** | `experiments/experiment_04_explainability_analysis/figures/` |
| **Overleaf copies** | `manuscript/overleaf/figures/figure_shap_summary_stress.png`, `figure_shap_summary_demand.png` |
| **Caption (draft)** | Global grouped SHAP attributions for stress (left) and Dhaka demand (right). Limitation stack (G8) and calendar/trend features (G6) dominate stress; demand is driven by calendar trend, engineered lags (G4), and national generation scalars (G10). |

---

## Figure 7 — Node Importance

| Property | Value |
| --- | --- |
| **File** | `figures/figure_07_node_importance.png` |
| **Type** | Spatial attention / node importance heatmap |
| **Source** | `experiments/experiment_04_explainability_analysis/figures/figure_node_importance_heatmap.png` |
| **Overleaf copy** | `manuscript/overleaf/figures/figure_node_importance_heatmap.png` |
| **Caption (draft)** | Node-level attribution heatmap on the correlation graph. Dhaka receives the highest SHAP mass; attention aligns with adjacency structure (ρ=0.422). |

---

## Figure 8 — Temporal Attribution

| Property | Value |
| --- | --- |
| **File** | `figures/figure_08_temporal_attribution.png` |
| **Type** | Temporal attention weights α_t (T=7) |
| **Source** | `experiments/experiment_04_explainability_analysis/figures/figure_temporal_importance.png` |
| **Overleaf copy** | `manuscript/overleaf/figures/figure_temporal_importance.png` |
| **Caption (draft)** | Mean temporal attention weights across validation windows. Weights are near-uniform; lag t−6 shows the highest mean α (0.162), consistent with ablation finding that the temporal branch adds limited marginal demand signal. |

---

## Figure 9 — Stress Attribution

| Property | Value |
| --- | --- |
| **File** | `figures/figure_09_stress_attribution.png` |
| **Type** | SHAP vs OSI component attribution |
| **Source** | `experiments/experiment_04_explainability_analysis/figures/figure_stress_attribution.png` |
| **Overleaf copy** | `manuscript/overleaf/figures/figure_stress_attribution.png` |
| **Caption (draft)** | Operational stress attribution comparing grouped SHAP to OSI component drivers (reserve margin vs limitation stack). Dual-path agreement occurs in 52.2% of case studies. |

---

## Supplementary figures (frozen; not in main numbering)

| ID | File | Source |
| --- | --- | --- |
| Fig S1 | `manuscript/overleaf/figures/figure_shap_bar_stress.png` | Exp04 — signed stress SHAP bar |
| Fig S2 | `experiments/experiment_02A_classical_benchmark_verification/plots/actual_vs_pred_Dhaka.png` | Exp02A — actual vs predicted |
| Fig S3 | `experiments/experiment_02A_classical_benchmark_verification/plots/residuals_B07.png` | Exp02A — S1 residuals |
| Fig S4 | `manuscript/overleaf/figures/figure_feature_importance_ranking.png` | Exp04 — permutation ΔMAE |
| Fig S5 | `manuscript/overleaf/figures/figure_regional_contribution.png` | Exp04 — regional SHAP |

---

## Regeneration policy

Figures 1–5 may be regenerated by running:

```bash
python paper/final_results_package/build_publication_assets.py
```

Figures 6–9 must not be regenerated without rerunning Experiment 04 (prohibited). Use frozen copies only.
