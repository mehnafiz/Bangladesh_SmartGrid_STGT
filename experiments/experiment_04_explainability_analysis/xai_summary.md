# XAI Summary — Experiment 04

Generated: 2026-06-25

## Scope

Full explainability pass on frozen **S2** model. No retraining; no modification to Exp01–03 results.

## Key findings

1. **Stress** is driven primarily by **G8** (limitation_stack) and grid/limitation coalitions G7/G8.
2. **Demand (Dhaka)** top coalitions: **G6**, **G4** — regional demand block and engineered lags dominate.
3. **Nodes:** Dhaka highest SHAP mass; correlation-graph attention aligns with adjacency (ρ=0.422).
4. **Temporal:** weights near-uniform (max lag t-6).
5. **Stress dual-path agreement:** 52.2% across case studies.

## Manuscript figures

| Figure | File |
| --- | --- |
| SHAP summary (stress) | `figures/figure_shap_summary_stress.png` |
| SHAP summary (demand) | `figures/figure_shap_summary_demand.png` |
| Feature importance | `figures/figure_feature_importance_ranking.png` |
| Node heatmap | `figures/figure_node_importance_heatmap.png` |
| Temporal α_t | `figures/figure_temporal_importance.png` |
| Stress attribution | `figures/figure_stress_attribution.png` |
| Regional contribution | `figures/figure_regional_contribution.png` |

Copies synced to `manuscript/overleaf/figures/`.

## Artefacts

- `xai_metrics.json` — machine-readable metrics
- `results/explainability/` — CSVs and case-study exports
