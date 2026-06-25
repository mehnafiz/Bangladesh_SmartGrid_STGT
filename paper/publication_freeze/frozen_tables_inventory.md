# Frozen Tables Inventory — Publication Asset Freeze

**Freeze date:** 2026-06-25  
**Git commit:** `dda83f1d9201d55ad8daf6b4cc0456569a84b6aa`  
**Version tag (designated):** `publication-freeze-2026-06-25`

All tables below are **read-only** for manuscript preparation. Source CSV/MD paths are authoritative;
manuscript copies should reference these paths or export to `manuscript/overleaf/tables/` without
altering underlying experiment files.

---

## Manuscript table numbering (assigned)

| Table ID | Title | Primary source | Format |
| --- | --- | --- | --- |
| **Table 1** | Benchmark model comparison (test set) | Exp02 | CSV + MD |
| **Table 2** | PF-STGT ablation study (A1–A6) | Exp03 | CSV + MD |
| **Table 3** | Architecture simplification (S1–S4) | Exp03B | CSV + MD |
| **Table 4** | Statistical significance (benchmarks) | Exp02 | MD |
| **Table 5** | Statistical significance (ablations) | Exp03 | MD |
| **Table S1** | Classical benchmark metric verification | Exp02A | MD |
| **Table S2** | Global grouped SHAP (stress + demand) | Exp04 | CSV |
| **Table S3** | Permutation feature importance | Exp04 | CSV |
| **Table S4** | Case-study stress attribution summary | Exp04 | MD + CSV |

---

## Table 1 — Benchmark comparison

| Property | Value |
| --- | --- |
| Experiment | 02 |
| Frozen file | `experiments/experiment_02_benchmark_models/benchmark_results.csv` |
| Supporting docs | `benchmark_summary.md`, `benchmark_rankings.md`, `performance_tables.md` |
| Models | B01–B07 (B07 = S1 / historical PF-STGT W20) |
| Split | Test |
| Key result | B07 MAE 93.31 MW; B02 RF 97.03 MW |

---

## Table 2 — Ablation results

| Property | Value |
| --- | --- |
| Experiment | 03 |
| Frozen file | `experiments/experiment_03_ablation_studies/ablation_results.csv` |
| Raw JSON | `ablation_raw.json` |
| Supporting docs | `ablation_summary.md`, `ablation_rankings.md`, `component_contribution.md` |
| Reference | A1 (S1); **A6 = S2 final architecture** |
| Key result | A6 demand MAE 88.65 MW; A4 single-task 86.89 MW |

---

## Table 3 — Simplification / final model selection

| Property | Value |
| --- | --- |
| Experiment | 03B |
| Frozen file | `experiments/experiment_03B_architecture_simplification/simplification_results.csv` |
| Supporting docs | `complexity_analysis.md`, `performance_vs_complexity.md`, `final_architecture_decision.md` |
| Final row | **S2** — Correlation-Only PF-STGT |

---

## Table 4 — Benchmark statistical significance

| Property | Value |
| --- | --- |
| Experiment | 02 |
| Frozen file | `experiments/experiment_02_benchmark_models/statistical_significance.md` |
| Method | Wilcoxon signed-rank vs B07 |

---

## Table 5 — Ablation statistical significance

| Property | Value |
| --- | --- |
| Experiment | 03 |
| Frozen file | `experiments/experiment_03_ablation_studies/statistical_significance.md` |
| Method | Wilcoxon vs A1; Bonferroni α = 0.01 |

---

## Table S1 — Benchmark verification (Exp02A)

| Property | Value |
| --- | --- |
| Experiment | 02A |
| Frozen reports | |
| | `metric_verification.md` |
| | `aggregation_audit.md` |
| | `variance_explanation.md` |
| | `residual_analysis.md` |
| | `prediction_distribution_analysis.md` |
| | `benchmark_verification_report.md` |
| Finding | Pooled vs macro R² inconsistency resolved for B02/B03 vs B07 |

---

## Table S2 — Global SHAP coalitions (Exp04)

| Property | Value |
| --- | --- |
| Experiment | 04 |
| Frozen files | |
| | `results/explainability/shap/global_stress.csv` |
| | `results/explainability/shap/global_demand_dhaka.csv` |
| Summary | `experiments/experiment_04_explainability_analysis/shap_summary.md` |

---

## Table S3 — Permutation importance (Exp04)

| Property | Value |
| --- | --- |
| Experiment | 04 |
| Frozen files | |
| | `results/explainability/permutation/demand_importance.csv` |
| | `results/explainability/permutation/stress_importance.csv` |
| Summary | `experiments/experiment_04_explainability_analysis/feature_importance.md` |

---

## Table S4 — Case-study attribution (Exp04)

| Property | Value |
| --- | --- |
| Experiment | 04 |
| Frozen file | `experiments/experiment_04_explainability_analysis/case_studies.md` |
| Per-date CSVs | `results/explainability/case_studies/<date>/` |
| Machine-readable | `experiments/experiment_04_explainability_analysis/xai_metrics.json` |

---

## Supporting tables (investigation; supplementary)

| Label | Source | File |
| --- | --- | --- |
| Exp01 metrics | Exp01 | `experiments/experiment_01_pf_stgt/metrics.json` |
| Exp01B repair | Exp01B | `experiments/experiment_01B_multitask_optimization_repair/results.json` |
| Exp03A metrics | Exp03A | `experiments/experiment_03A_ablation_failure_investigation/investigation_metrics.json` |
| Final model spec | Freeze | `experiments/architecture_freeze_revision/final_model_specification.md` |

---

## Overleaf export target

Copy frozen tables to `manuscript/overleaf/tables/` during LaTeX integration. Do not edit
source experiment CSVs when building LaTeX tables.
