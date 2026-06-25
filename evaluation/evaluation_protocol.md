# Final Evaluation Protocol — Phase 15

Generated: 2026-06-24
Status: **FROZEN**

## Purpose

Consolidate Phases 10–14 into a single publication-ready evaluation framework
for PF-STGT. Defines **what** to measure, **how** to compare, and **when** to report
— without executing training or generating numeric results in this phase.

## Evaluation dimensions (D1–D6)

| Dim | Name | Primary source | Output |
| --- | --- | --- | --- |
| **D1** | Predictive performance | Phase 10 metrics | Tables 1, 3 |
| **D2** | Benchmark comparison | Phase 10 benchmark_design | Table 1, Fig 1–2 |
| **D3** | Ablation evaluation | Phase 13 ablation_plan | Table 2 |
| **D4** | Explainability evaluation | Phase 12 explainability_protocol | Fig 3–5, Table S2 |
| **D5** | Robustness evaluation | Phase 14 error_analysis | Table S3, Fig S1–S3 |
| **D6** | Statistical significance | Phase 13 + this phase | Table 4 |

## Scope and split policy (frozen)

| Rule | Specification |
| --- | --- |
| Final metrics | **Test split only** (278 days, 2024-03-20 → 2024-12-30) |
| Model selection | Validation split only; no test tuning |
| Warm-up | Exclude first T=7 rows per split (Phase 06) |
| Graph (historical) | Phase 08 hybrid adjacency for B06, B07 (Exp02), ablation A1 |
| Graph (final model S2) | **Correlation-only** adjacency (`GraphVariant.CORR`, τ=0.65) — Exp03 A6 |
| Leakage | No same-day OSI as input for OSI(t+1) (Phase 08.5) |

### Frozen final model (S2)

| Property | Value |
| --- | --- |
| Architecture ID | S2 |
| Implementation | `PFSTGT` + `GraphVariant.CORR` |
| Checkpoint | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| Original (S1) | Exp01B W20 / Exp03 A1 / Exp02 B07 — historical reference only |

Specification: `experiments/architecture_freeze_revision/final_model_specification.md`

---

## D1 — Predictive Performance

### Task 1: Regional demand forecasting

| Metric | Formula | Primary aggregation |
| --- | --- | --- |
| MAE | mean(|y − ŷ|) MW | Macro over 9 regions |
| RMSE | sqrt(mean((y − ŷ)²)) MW | Macro over 9 regions |
| MAPE | mean(|y − ŷ|/|y|) × 100% | Macro; exclude y=0 |
| R² | 1 − SS_res/SS_tot | Macro over 9 regions |

**Dhaka reported separately** (~35.7% national share, Phase 02).

### Task 2: Operational stress forecasting (B07 / A1 only)

| Metric | Formula |
| --- | --- |
| MAE | mean(|OSI − OSI_hat|) |
| RMSE | sqrt(mean((OSI − OSI_hat)²)) |
| R² | 1 − SS_res/SS_tot |
| Pearson r | corr(OSI, OSI_hat) | Supplementary |

Non-model baselines (context): persistence OSI(t), train median.

---

## D2 — Benchmark Comparison

See `benchmark_comparison_plan.md`.

| benchmark_id   | model_name        | family              | uses_graph   | tasks         |
|:---------------|:------------------|:--------------------|:-------------|:--------------|
| B01            | Linear Regression | Classical ML        | False        | demand        |
| B02            | Random Forest     | Classical ML        | False        | demand        |
| B03            | XGBoost           | Classical ML        | False        | demand        |
| B04            | LSTM              | Deep Learning       | False        | demand        |
| B05            | GRU               | Deep Learning       | False        | demand        |
| B06            | T-GCN             | Spatio-Temporal GNN | True         | demand        |
| B07            | PF-STGT (S1 / original) | Proposed (historical) | True         | demand;stress |
| **S2**         | Correlation-Only PF-STGT | **Final model**       | True         | demand;stress |

**Primary claim gate (Exp02, historical):** B07 beats B06 on macro MAE **and** reports stress R² > 0.

**Forward policy (post-freeze):** manuscript primary model is **S2** (Exp03 A6 checkpoint).
B07 results remain frozen; report S2 as the adopted architecture.

---

## D3 — Ablation Evaluation

See Phase 13 `ablation/ablation_plan.md`. Reference: **A1**.

| ablation_id   | variant_name                | study_category    | multi_task   | stress_output   |
|:--------------|:----------------------------|:------------------|:-------------|:----------------|
| A1            | PF-STGT Full Model          | reference         | True         | True            |
| A2            | Without Graph Module        | component_removal | True         | True            |
| A3            | Without Transformer Module  | component_removal | True         | True            |
| A4            | Without Multi-Task Learning | multi_task        | False        | False           |
| A5-GEO        | Geographical Graph Only     | hybrid_graph      | True         | True            |
| A6            | BiLSTM Black-Box Trunk      | explainability    | True         | False           |

Report ΔMAE, ΔR² vs A1; stress metrics N/A for A4.

---

## D4 — Explainability Evaluation

See Phase 12 `explainability/explainability_protocol.md`.

| Method | Evaluation criterion | Pass threshold |
| --- | --- | --- |
| SHAP | Bootstrap rank stability | Spearman ρ > 0.7 |
| Attention | Hybrid-edge alignment | Spearman(attention, A) > 0.3 |
| Permutation | Global rank vs SHAP | Spearman ρ > 0.5 on validation |
| Cross-method | Top-2 group agreement | ≥ 60% case studies |
| Stress driver | SHAP vs c1/c2/c3 driver | Agreement rate reported |

---

## D5 — Robustness Evaluation

See `robustness_evaluation_plan.md` (Phase 14 error taxonomy E2–E6).

| Segment | Source | Key metric |
| --- | --- | --- |
| Extreme events | E4 | Event MAE vs normal days |
| High stress days | E3 High regime | OSI MAE |
| Regional variability | E2 | Per-region MAPE range |
| Temporal | E5 | Month-9 MAE / overall |
| Graph connectivity | E6 | Low vs high degree MAPE |

---

## D6 — Statistical Significance

See `statistical_testing_plan.md`.

| Comparison set | Test | Correction |
| --- | --- | --- |
| B07 vs B01–B06 | Wilcoxon signed-rank (daily macro MAE) | Bonferroni α_adj = 0.0083 |
| A1 vs A2–A6 core | Wilcoxon signed-rank | Bonferroni α_adj = 0.0100 |
| R² / effect size | Bootstrap 95% CI; Cohen's d | — |

---

## Execution pipeline (post-training)

```
1. Train B01–B07 (Phase 10/11) → collect test predictions  [COMPLETE — Exp02]
2. Train ablations A1–A6 (Phase 13) → collect test predictions  [COMPLETE — Exp03]
3. Architecture freeze → adopt S2 (A6 checkpoint)  [COMPLETE — 2026-06-25]
4. Run Phase 12 XAI on S2 checkpoint → export attributions  [Exp04 — NEXT]
5. Run Phase 14 error analysis → segment residuals
6. Compute D1–D6 metrics → populate Tables 1–4
7. Generate Figures 1–5 (+ supplements) → results/evaluation/
8. Write evaluation_decision_report with claim verification
```

## Output artefact tree (implementation phase)

```
results/evaluation/
  tables/
    table1_benchmark_demand_test.csv
    table2_ablation_results.csv
    table3_stress_forecast_test.csv
    table4_statistical_significance.csv
  figures/
    figure1_prediction_vs_actual.png
    figure2_regional_performance.png
    figure3_shap_summary.png
    figure4_attention_visualization.png
    figure5_stress_attribution_case_study.png
  robustness/
    robustness_summary.csv
  explainability/
    xai_quality_metrics.csv
```
