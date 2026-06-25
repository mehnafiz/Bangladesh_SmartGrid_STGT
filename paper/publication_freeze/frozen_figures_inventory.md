# Frozen Figures Inventory — Publication Asset Freeze

**Freeze date:** 2026-06-25  
**Git commit:** `dda83f1d9201d55ad8daf6b4cc0456569a84b6aa`  
**Version tag (designated):** `publication-freeze-2026-06-25`

All figures listed are **read-only** for manuscript preparation. Primary copies for Overleaf
live under `manuscript/overleaf/figures/`. Experiment-local copies are under each experiment's
`figures/` or `plots/` directory.

---

## Manuscript figure numbering (assigned)

| Figure ID | Title | Source experiment | Frozen path (Overleaf) |
| --- | --- | --- | --- |
| **Figure 1** | Actual vs predicted — Dhaka (B07/S1) | 02A | `plots/actual_vs_pred_Dhaka.png` * |
| **Figure 2** | Residual distribution — PF-STGT (B07) | 02A | `plots/residuals_B07.png` * |
| **Figure 3** | SHAP summary — stress (grouped \|φ\|) | 04 | `figure_shap_summary_stress.png` |
| **Figure 4** | SHAP summary — demand Dhaka (grouped \|φ\|) | 04 | `figure_shap_summary_demand.png` |
| **Figure 5** | Feature importance — permutation ΔMAE | 04 | `figure_feature_importance_ranking.png` |
| **Figure 6** | Spatial attention / node importance heatmap | 04 | `figure_node_importance_heatmap.png` |
| **Figure 7** | Temporal attention α_t (T=7) | 04 | `figure_temporal_importance.png` |
| **Figure 8** | Stress attribution — SHAP vs OSI components | 04 | `figure_stress_attribution.png` |
| **Figure 9** | Regional SHAP contribution | 04 | `figure_regional_contribution.png` |
| **Figure S1** | SHAP bar — stress (signed φ) | 04 | `figure_shap_bar_stress.png` |
| **Figure S2** | Actual vs predicted — multi-region panel | 02A | `plots/actual_vs_pred_*.png` * |

\* Exp02A plots: `experiments/experiment_02A_classical_benchmark_verification/plots/`

---

## Figure 3–9 and S1 — Explainability (Exp04) — **FINALIZED**

| File | Experiment copy | Overleaf copy | Status |
| --- | --- | --- | --- |
| `figure_shap_summary_stress.png` | `experiments/experiment_04_explainability_analysis/figures/` | `manuscript/overleaf/figures/` | Frozen |
| `figure_shap_summary_demand.png` | same | same | Frozen |
| `figure_shap_bar_stress.png` | same | same | Frozen |
| `figure_feature_importance_ranking.png` | same | same | Frozen |
| `figure_node_importance_heatmap.png` | same | same | Frozen |
| `figure_temporal_importance.png` | same | same | Frozen |
| `figure_stress_attribution.png` | same | same | Frozen |
| `figure_regional_contribution.png` | same | same | Frozen |

Additional runtime artefact: `results/explainability/shap/global_stress_bar.png`

---

## Figure 1–2, S2 — Verification plots (Exp02A) — **FINALIZED**

| File | Path | Status |
| --- | --- | --- |
| `actual_vs_pred_Dhaka.png` | `experiments/experiment_02A_classical_benchmark_verification/plots/` | Frozen |
| `actual_vs_pred_Barishal.png` | same | Frozen |
| `actual_vs_pred_Chattogram.png` | same | Frozen |
| `actual_vs_pred_Cumilla.png` | same | Frozen |
| `actual_vs_pred_Khulna.png` | same | Frozen |
| `actual_vs_pred_Mymensingh.png` | same | Frozen |
| `residuals_B07.png` | same | Frozen |
| `residuals_B03.png` | same | Frozen |

---

## Training / diagnostic figures (supplementary; frozen)

| File | Source | Path | Notes |
| --- | --- | --- | --- |
| Train loss curve | Exp01 | `experiments/experiment_01_pf_stgt/train_loss.png` | Historical |
| Val loss curve | Exp01 | `experiments/experiment_01_pf_stgt/val_loss.png` | Historical |

---

## Architecture diagram (design reference)

| Asset | Path | Notes |
| --- | --- | --- |
| PF-STGT block diagram | `architecture/architecture_diagram.md` | Mermaid source; S2 corr-graph note included |
| S2 vs S1 diagram addendum | same | Documentation only |

---

## Verification

| Check | Count expected | Status |
| --- | --- | --- |
| Exp04 manuscript figures in Overleaf | 8 | Verified |
| Exp02A verification plots | 8 | Verified |
| All figures referenced in `xai_summary.md` | 7 core + 1 bar | Verified |

**No figure regeneration required before manuscript writing.**
