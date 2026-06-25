# Benchmark Comparison Plan — Phase 15

Generated: 2026-06-24
Status: **FROZEN**

## Objective (D2)

Fair comparison of PF-STGT (B07) against six baselines on Task 1 demand forecasting,
with B07 additionally evaluated on Task 2 stress forecasting.

## Benchmark registry

| benchmark_id   | model_name        | family              | uses_graph   | tasks         |   input_window_T |   horizon_h | seeds        | primary_task   |
|:---------------|:------------------|:--------------------|:-------------|:--------------|-----------------:|------------:|:-------------|:---------------|
| B01            | Linear Regression | Classical ML        | False        | demand        |                7 |           1 | 42           | demand         |
| B02            | Random Forest     | Classical ML        | False        | demand        |                7 |           1 | 42           | demand         |
| B03            | XGBoost           | Classical ML        | False        | demand        |                7 |           1 | 42           | demand         |
| B04            | LSTM              | Deep Learning       | False        | demand        |                7 |           1 | 42, 123, 456 | demand         |
| B05            | GRU               | Deep Learning       | False        | demand        |                7 |           1 | 42, 123, 456 | demand         |
| B06            | T-GCN             | Spatio-Temporal GNN | True         | demand        |                7 |           1 | 42, 123, 456 | demand         |
| B07            | PF-STGT           | Proposed            | True         | demand;stress |                7 |           1 | 42, 123, 456 | demand;stress  |

## Fair comparison constraints (Phase 10 — frozen)

| Constraint | Value |
| --- | --- |
| Input window T | 7 days |
| Horizon h | 1 day |
| Features | Phase 05B/06 parquet splits |
| Graph (B06, B07) | Phase 08 hybrid adjacency |
| Warm-up | Skip first 7 rows per split |
| Hyperparameters | Phase 11 best (B04–B07); defaults (B01–B03) |

## Seed policy

| Model class | Seeds | Reporting |
| --- | --- | --- |
| B01–B03 Classical | 42 (deterministic) | Point estimate |
| B04–B07 Deep | 42, 123, 456 | mean ± std |

## Primary comparison hierarchy

```
Tier 1 (graph value):     B07 vs B06 T-GCN
Tier 2 (temporal DL):     B07 vs B04 LSTM, B05 GRU
Tier 3 (classical ML):    B07 vs B01–B03
Tier 4 (stress, B07 only): B07 vs persistence, train median
```

## Metrics for Table 1 (Main Benchmark Results)

### Columns (demand — all 7 models)

| Column | Description |
| --- | --- |
| benchmark_id | B01–B07 |
| model_name | Display name |
| mae_macro_mw | Macro MAE (primary rank) |
| rmse_macro_mw | Macro RMSE |
| mape_macro_pct | Macro MAPE |
| r2_macro | Macro R² |
| mae_dhaka_mw | Dhaka-only MAE |
| seed_std_mae | std over seeds (deep models) |

### Row ordering

Sort by **mae_macro_mw** ascending; bold B07 if rank 1.

## Statistical comparison (feeds Table 4)

For each baseline B_v (v=01..06):

```
H0: median(macro_MAE_B07(d) − macro_MAE_Bv(d)) = 0   on test days d
Test: Wilcoxon signed-rank (paired, one-sided: B07 better)
Correction: Bonferroni over 6 comparisons → α_adj = 0.0083
```

Report Cohen's d and bootstrap 95% CI on MAE difference.

## Success criteria (scientific claims)

| Claim | Criterion | Gap |
| --- | --- | --- |
| Graph-temporal superiority | B07 MAE < B06 MAE (significant) | GAP-04 |
| Beats temporal DL | B07 MAE < B04, B05 | GAP-04 |
| Beats classical ML | B07 MAE < B01–B03 | GAP-08 |
| Multi-task stress | B07 stress MAE < persistence | GAP-02, GAP-06 |
| Dhaka accuracy | B07 mae_dhaka best or within 1 MW of best | Phase 02 |

## Implementation outputs

```
results/evaluation/tables/table1_benchmark_demand_test.csv
results/experiments/leaderboard_demand_test.csv
results/experiments/per_region_metrics_test.csv
results/evaluation/benchmark/paired_mae_daily_test.parquet
```
