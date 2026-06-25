# Phase 15 — Final Evaluation Framework Summary

- Completion date: 2026-06-24
- Benchmark models: **7** (B01–B07)
- Ablation variants: **7** (A1–A6 + A5-CORR)
- Evaluation dimensions: **6** (D1–D6)
- Required main tables: **4** | Required main figures: **5**
- No training or results generated in this phase

## Evaluation dimensions

| Dim | Component | Deliverable |
| --- | --- | --- |
| D1 | Predictive performance | evaluation_protocol.md |
| D2 | Benchmark comparison | benchmark_comparison_plan.md |
| D3 | Ablation evaluation | evaluation_protocol.md + Table 2 |
| D4 | Explainability evaluation | figure_and_table_plan.md (Fig 3–5) |
| D5 | Robustness evaluation | robustness_evaluation_plan.md |
| D6 | Statistical significance | statistical_testing_plan.md + Table 4 |

## Required tables (main text)

| Table | Title |
| --- | --- |
| **Table 1** | Main Benchmark Results |
| **Table 2** | Ablation Results |
| **Table 3** | Stress Forecast Results |
| **Table 4** | Statistical Significance Results |

## Required figures (main text)

| Figure | Title |
| --- | --- |
| **Figure 1** | Prediction vs Actual |
| **Figure 2** | Regional Performance |
| **Figure 3** | SHAP Summary |
| **Figure 4** | Attention Visualization |
| **Figure 5** | Stress Attribution Case Study |

## Deliverables

### evaluation/
- evaluation_protocol.md
- benchmark_comparison_plan.md
- robustness_evaluation_plan.md
- statistical_testing_plan.md
- figure_and_table_plan.md
- benchmark_registry.csv
- ablation_evaluation_registry.csv

### results/phases/phase_15_evaluation_framework/
- evaluation_summary.md
- evaluation_decision_report.md

## Scope compliance

- Final evaluation framework design only.
- **No model implementation, training, or numeric results generated.**
- Locked phase outputs not modified.

## Locked input integrity

- `data/features/train_features.parquet` MD5: `b8b3bda95d0fd6cc65f4910d85a98e16`
- `data/interim/bangladesh_smartgrid_clean.parquet` MD5: `4255024d735a91a4b53b2edee203d0ca`
- `graphs/adjacency_matrix.csv` MD5: `dacb7ac3a827d00a4b61ea9400e75686`
- `experiments/evaluation_protocol.md` MD5: `829faaed417189e0e154cb8b91ed97ff`
- `ablation/ablation_plan.md` MD5: `826896a1f2f0267b445e9a0c55678e9a`
- `error_analysis/error_taxonomy.md` MD5: `9597cbbdae3e0c9d50f7ab15036d3915`

## Status

Ready for full training, evaluation execution, and manuscript assembly.
