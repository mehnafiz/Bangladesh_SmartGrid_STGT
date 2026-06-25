# Explainability Design — Phase 09

Generated: 2026-06-24

## Design goal (GAP-05 / NOV-05)

Provide operator-facing attribution for regional demand forecasts and national stress scores
without post-hoc approximations alone.

## 1. SHAP compatibility

| Component | SHAP approach |
| --- | --- |
| Demand head | TreeSHAP on extracted features OR DeepSHAP on MLP head |
| Stress head | KernelSHAP / DeepSHAP on graph readout + global vector |
| Full model | GradientSHAP with grouped feature coalitions |

**Feature groups for coalition SHAP (Phase 05B/07):**

- Regional demand/supply/load blocks (9 nodes)
- Calendar / trend (`day_of_year_*`, `trend_index`, `Holiday_cat`)
- Limitation stack (gas, coal, water, maintenance)
- Grid aggregates (`generation_reserve`, `total_regional_demand`)

**Caution (Phase 07B reviewer risk R-05):** SHAP on correlated regional features may misattribute;
report node-level and global attributions separately.

## 2. Attention visualisation

| Map | Source | Interpretation |
| --- | --- | --- |
| Spatial attention | Graph Transformer heads | Which divisions influence each other |
| Temporal attention | Transformer Encoder heads | Which past days drive forecast |

Export `attn_spatial` (N×N) and `attn_temporal` (T×T) per forecast for case-study days with shedding.

## 3. Feature attribution compatibility

- Architecture uses explicit node/global input partitions → direct mapping to Phase 05A feature groups.
- Hybrid adjacency edge weights (Phase 08) can be overlaid on spatial attention heatmaps.
- Ablation hooks: remove limitation stack, remove spatial branch, remove temporal branch.

## Explainability readiness checklist

- [x] Attention weights exposed from spatial and temporal modules
- [x] Input feature groups documented for SHAP coalitions
- [x] Separate node-level (Task 1) and graph-level (Task 2) attribution paths
- [x] Leakage-safe inputs ensure attributions reference legitimate predictors only
