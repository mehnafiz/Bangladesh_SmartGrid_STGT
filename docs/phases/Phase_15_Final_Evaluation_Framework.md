# Phase 15 — Final Evaluation Framework

## Objective

Design the final evaluation framework for PF-STGT.

This framework defines how performance, robustness, explainability, and scientific validity will be evaluated.

---

## Inputs

Phase 10 Training Strategy

Phase 12 Explainability Design

Phase 13 Ablation Studies

Phase 14 Error Analysis

---

## Evaluation Dimensions

### D1

Predictive Performance

Demand Forecasting

Operational Stress Forecasting

---

### D2

Benchmark Comparison

Compare:

- Linear Regression
- Random Forest
- XGBoost
- LSTM
- GRU
- T-GCN
- PF-STGT

---

### D3

Ablation Evaluation

Evaluate all Phase 13 variants.

---

### D4

Explainability Evaluation

Evaluate:

- SHAP
- Attention Analysis
- Permutation Importance

---

### D5

Robustness Evaluation

Evaluate:

- Extreme Events
- High Stress Days
- Regional Variability

---

### D6

Statistical Evaluation

Evaluate:

- Wilcoxon Signed-Rank Test
- Confidence Intervals

---

## Required Tables

Table 1

Main Benchmark Results

---

Table 2

Ablation Results

---

Table 3

Stress Forecast Results

---

Table 4

Statistical Significance Results

---

## Required Figures

Figure 1

Prediction vs Actual

---

Figure 2

Regional Performance

---

Figure 3

SHAP Summary

---

Figure 4

Attention Visualization

---

Figure 5

Stress Attribution Case Study

---

## Deliverables

evaluation/

- evaluation_protocol.md

- benchmark_comparison_plan.md

- robustness_evaluation_plan.md

- statistical_testing_plan.md

- figure_and_table_plan.md

results/phases/

phase_15_evaluation_framework/

- evaluation_summary.md

- evaluation_decision_report.md

---

## Definition of Done

✔ Evaluation framework defined

✔ Benchmark comparison defined

✔ Robustness evaluation defined

✔ Statistical testing defined

✔ Publication-ready evidence plan defined

---

## Execution Record

### Completion Date

2025-06-25

### Evaluation Framework Summary

| Dimension | Focus | Primary deliverable |
| --- | --- | --- |
| **D1** | Predictive performance | evaluation_protocol.md |
| **D2** | Benchmark comparison (B01–B07) | benchmark_comparison_plan.md |
| **D3** | Ablation evaluation (A1–A6) | Table 2 spec |
| **D4** | Explainability (SHAP, Attention, Permutation) | figure_and_table_plan.md |
| **D5** | Robustness (extremes, stress, regional) | robustness_evaluation_plan.md |
| **D6** | Statistical significance | statistical_testing_plan.md |

### Required Tables (main text)

| Table | Title |
| --- | --- |
| **Table 1** | Main Benchmark Results (7 models × MAE, RMSE, MAPE, R²) |
| **Table 2** | Ablation Results (ΔMAE, ΔR² vs A1) |
| **Table 3** | Stress Forecast Results (OSI + baselines) |
| **Table 4** | Statistical Significance Results (Wilcoxon + Bonferroni) |

### Required Figures (main text)

| Figure | Title |
| --- | --- |
| **Figure 1** | Prediction vs Actual (demand + OSI time series) |
| **Figure 2** | Regional Performance (9-region MAE comparison) |
| **Figure 3** | SHAP Summary (grouped feature beeswarm) |
| **Figure 4** | Attention Visualization (spatial + temporal) |
| **Figure 5** | Stress Attribution Case Study (SHAP + c1/c2/c3) |

### Statistical Protocol (frozen)

- Primary unit: daily macro MAE (~278 test days)
- Benchmark: Wilcoxon B07 vs B01–B06, Bonferroni α_adj = 0.0083
- Ablation: Wilcoxon A1 vs A2/A3/A4/A5-GEO/A6, Bonferroni α_adj = 0.0100
- Effect size: Cohen's d; bootstrap 95% CI on MAE differences

### Deliverables Generated

`evaluation/`:

* `evaluation_protocol.md`
* `benchmark_comparison_plan.md`
* `robustness_evaluation_plan.md`
* `statistical_testing_plan.md`
* `figure_and_table_plan.md`
* `benchmark_registry.csv`
* `ablation_evaluation_registry.csv`

`results/phases/phase_15_evaluation_framework/`:

* `evaluation_summary.md`
* `evaluation_decision_report.md`

Script: `scripts/phase_15_evaluation_framework_design.py`

### Scope Compliance

* Final evaluation framework design only.
* **No model implementation, training, or numeric results generated.**
* Locked phase outputs not modified.

### Status

Ready for full training, evaluation execution, and manuscript assembly.