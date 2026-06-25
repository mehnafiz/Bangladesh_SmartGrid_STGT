# Manuscript Assets Inventory — Stage 05B Final Results Package

**Generated:** 2026-06-16  
**Freeze reference:** `paper/publication_freeze/` (2026-06-25)  
**Package root:** `paper/final_results_package/`

Master index linking publication tables, figures, frozen sources, and recommended Overleaf targets. All assets are read-only derivatives of frozen experiment outputs.

---

## Package contents

| File | Description |
| --- | --- |
| `Final_Results_Package.md` | Stage 05B specification and execution record |
| `publication_tables.md` | Tables 1–7 (publication-ready markdown) |
| `publication_figures.md` | Figures 1–9 with captions and provenance |
| `statistical_summary.md` | Consolidated p-values, CIs, effect sizes |
| `manuscript_assets_inventory.md` | This file |
| `build_publication_assets.py` | Figure assembly script (Figures 1–5 only) |
| `figures/` | Publication figure copies and generated charts |

---

## Tables inventory

| Manuscript ID | Title | Package doc | Frozen primary source | Overleaf target |
| --- | --- | --- | --- | --- |
| **Table 1** | Dataset Summary | `publication_tables.md` §1 | `src/constants.py`, `paper/publication_freeze/frozen_results_inventory.md` | `manuscript/overleaf/tables/table_01_dataset.tex` |
| **Table 2** | Training Configuration | `publication_tables.md` §2 | `experiments/architecture_freeze_revision/final_model_specification.md` | `manuscript/overleaf/tables/table_02_training.tex` |
| **Table 3** | Benchmark Comparison | `publication_tables.md` §3 | `experiments/experiment_02_benchmark_models/benchmark_results.csv` + A6 row | `manuscript/overleaf/tables/table_03_benchmarks.tex` |
| **Table 4** | Benchmark Statistical Significance | `publication_tables.md` §4 | `experiments/experiment_02_benchmark_models/statistical_significance.md` | `manuscript/overleaf/tables/table_04_benchmark_stats.tex` |
| **Table 5** | Ablation Study Results | `publication_tables.md` §5 | `experiments/experiment_03_ablation_studies/ablation_results.csv` | `manuscript/overleaf/tables/table_05_ablations.tex` |
| **Table 6** | Architecture Comparison (S1–S4) | `publication_tables.md` §6 | `experiments/experiment_03B_architecture_simplification/simplification_results.csv` | `manuscript/overleaf/tables/table_06_architecture.tex` |
| **Table 7** | Explainability Summary | `publication_tables.md` §7 | `experiments/experiment_04_explainability_analysis/xai_metrics.json` | `manuscript/overleaf/tables/table_07_explainability.tex` |

### Supplementary tables (frozen; optional manuscript)

| ID | Title | Frozen source |
| --- | --- | --- |
| Table S1 | Classical benchmark verification | `experiments/experiment_02A_classical_benchmark_verification/` |
| Table S2 | Global grouped SHAP (full) | `experiments/experiment_04_explainability_analysis/` SHAP CSVs |
| Table S3 | Permutation feature importance | Exp04 permutation exports |
| Table S4 | Case-study attribution summary | `experiments/experiment_04_explainability_analysis/case_studies.md` |

---

## Figures inventory

| Manuscript ID | Title | Package file | Frozen / generated source | Overleaf target |
| --- | --- | --- | --- | --- |
| **Figure 1** | Overall Framework | `figures/figure_01_framework.png` | Generated from `architecture/architecture_diagram.md` | `manuscript/overleaf/figures/figure_01_framework.png` |
| **Figure 2** | Final S2 Architecture | `figures/figure_02_s2_architecture.png` | Generated from architecture freeze docs | `manuscript/overleaf/figures/figure_02_s2_architecture.png` |
| **Figure 3** | Training Curves | `figures/figure_03_training_curves.png` | `experiments/experiment_01_pf_stgt/train_loss.png`, `val_loss.png` | `manuscript/overleaf/figures/figure_03_training_curves.png` |
| **Figure 4** | Benchmark Comparison | `figures/figure_04_benchmark_comparison.png` | Generated from Exp02 CSV + A6 | `manuscript/overleaf/figures/figure_04_benchmark_comparison.png` |
| **Figure 5** | Ablation Comparison | `figures/figure_05_ablation_comparison.png` | Generated from Exp03 CSV | `manuscript/overleaf/figures/figure_05_ablation_comparison.png` |
| **Figure 6** | SHAP Summary | `figures/figure_06_shap_summary_stress.png`, `figure_06_shap_summary_demand.png` | Exp04 frozen figures | `manuscript/overleaf/figures/figure_shap_summary_*.png` |
| **Figure 7** | Node Importance | `figures/figure_07_node_importance.png` | Exp04 `figure_node_importance_heatmap.png` | `manuscript/overleaf/figures/figure_node_importance_heatmap.png` |
| **Figure 8** | Temporal Attribution | `figures/figure_08_temporal_attribution.png` | Exp04 `figure_temporal_importance.png` | `manuscript/overleaf/figures/figure_temporal_importance.png` |
| **Figure 9** | Stress Attribution | `figures/figure_09_stress_attribution.png` | Exp04 `figure_stress_attribution.png` | `manuscript/overleaf/figures/figure_stress_attribution.png` |

---

## Model and checkpoint reference

| Symbol | Name | Checkpoint path | Role in manuscript |
| --- | --- | --- | --- |
| **S2 ★** | Correlation-Only PF-STGT (A6) | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` | **Proposed final model** |
| S1 | PF-STGT W20 hybrid (A1/B07) | `experiments/experiment_01B_multitask_optimization_repair/checkpoints/W20/B07/seed_42/best.pt` | Historical reference |
| A4 | Single-task hybrid | Exp03 checkpoint A4 | Demand-only upper bound |

---

## Key numeric claims (frozen; for abstract/Results cross-check)

| Claim | Value | Source experiment |
| --- | --- | --- |
| S2 test demand MAE | 88.65 MW | Exp03 A6 / Exp03B S2 |
| S2 test demand R² | 0.684 | same |
| S2 test stress R² | 0.745 | same |
| S2 vs S1 ΔMAE | −4.66 MW (−5.0%) | Exp03B |
| S2 vs S1 p-value | 5.5×10⁻⁵ | Exp03 / Exp03B Wilcoxon |
| Best classical baseline MAE | 97.03 MW (RF) | Exp02 B02 |
| Top stress SHAP group | G8 limitation_stack | Exp04 |
| Top demand SHAP groups (Dhaka) | G6, G4 | Exp04 |
| Attention–adjacency ρ | 0.422 | Exp04 |

---

## Experiment traceability matrix

| Experiment | Reports used | Tables | Figures |
| --- | --- | --- | --- |
| 01 / 01B | `training_summary.md`, loss PNGs | — | Fig 3 |
| 02 | `benchmark_results.csv`, `statistical_significance.md` | 3, 4 | Fig 4 |
| 02A | verification plots | S1 (opt.) | Supp. Fig S2–S3 |
| 03 | `ablation_results.csv`, `statistical_significance.md` | 5 | Fig 5 |
| 03A | investigation reports | (discussion only) | — |
| 03B | `simplification_results.csv`, `performance_vs_complexity.md` | 6 | — |
| 04 | `xai_metrics.json`, 8 figure PNGs | 7 | Fig 6–9 |
| Arch freeze | `Final_Architecture_Decision.md`, `final_model_specification.md` | 2 | Fig 1–2 |

---

## Files that must NOT be modified

Per publication freeze policy, do not edit during manuscript writing:

```
experiments/experiment_02_benchmark_models/benchmark_results.csv
experiments/experiment_03_ablation_studies/ablation_results.csv
experiments/experiment_03B_architecture_simplification/simplification_results.csv
experiments/experiment_04_explainability_analysis/xai_metrics.json
experiments/experiment_04_explainability_analysis/figures/*
experiments/*/checkpoints/**
data/**
```

---

## Next steps (manuscript writing)

1. Export markdown tables to LaTeX under `manuscript/overleaf/tables/`.
2. Copy `paper/final_results_package/figures/*` to `manuscript/overleaf/figures/` (merge with existing Exp04 copies).
3. Draft Results section using `statistical_summary.md` for significance language.
4. Cross-reference `paper/publication_freeze/freeze_record.md` for version control tag.

**Status:** Ready for manuscript outlining.
