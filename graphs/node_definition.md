# Graph Node Definition — Phase 08

Generated: 2026-06-24

## Node set

Each node represents one **regional division entity** in the Bangladesh smart-grid dataset.
Nodes align with validated feature tensors from Phase 05B/06 (`{Region}_demand`, `{Region}_supply`, `{Region}_load`, and per-region engineered features).

**Count:** 9 nodes

| Node ID | Region | Role | Primary node features (from Phase 05B) |
| --- | --- | --- | --- |
| 0 | Barishal | Regional division | Barishal_demand, Barishal_supply, Barishal_load, demand_lag_1/7, load_lag_1, demand_rolling_mean_7, regional_demand_share, regional_load_intensity |
| 1 | Chattogram | Regional division | Chattogram_demand, Chattogram_supply, Chattogram_load, demand_lag_1/7, load_lag_1, demand_rolling_mean_7, regional_demand_share, regional_load_intensity |
| 2 | Cumilla | Regional division | Cumilla_demand, Cumilla_supply, Cumilla_load, demand_lag_1/7, load_lag_1, demand_rolling_mean_7, regional_demand_share, regional_load_intensity |
| 3 | Dhaka | Regional division | Dhaka_demand, Dhaka_supply, Dhaka_load, demand_lag_1/7, load_lag_1, demand_rolling_mean_7, regional_demand_share, regional_load_intensity |
| 4 | Khulna | Regional division | Khulna_demand, Khulna_supply, Khulna_load, demand_lag_1/7, load_lag_1, demand_rolling_mean_7, regional_demand_share, regional_load_intensity |
| 5 | Mymensingh | Regional division | Mymensingh_demand, Mymensingh_supply, Mymensingh_load, demand_lag_1/7, load_lag_1, demand_rolling_mean_7, regional_demand_share, regional_load_intensity |
| 6 | Rajshahi | Regional division | Rajshahi_demand, Rajshahi_supply, Rajshahi_load, demand_lag_1/7, load_lag_1, demand_rolling_mean_7, regional_demand_share, regional_load_intensity |
| 7 | Rangpur | Regional division | Rangpur_demand, Rangpur_supply, Rangpur_load, demand_lag_1/7, load_lag_1, demand_rolling_mean_7, regional_demand_share, regional_load_intensity |
| 8 | Sylhet | Regional division | Sylhet_demand, Sylhet_supply, Sylhet_load, demand_lag_1/7, load_lag_1, demand_rolling_mean_7, regional_demand_share, regional_load_intensity |

## Global (graph-level) context

Not encoded as nodes; attached as graph-level conditioning per Phase 06 recommendation:

- `total_regional_demand`, `generation_reserve`, `operational_stress_index`
- Exogenous limitation stacks (gas, coal, water, maintenance)
- Calendar / trend features (`day_of_year_sin/cos`, `trend_index`, `Holiday_cat`)

## Node ordering

Fixed alphabetical order for reproducible adjacency indexing:

```
Barishal, Chattogram, Cumilla, Dhaka, Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet
```

## Evidence

- Phase 01: 9 regional entities confirmed in raw dataset.
- Phase 02: high inter-regional demand correlation; Dhaka ~35.7% national share.
- Phase 06: 9-division node set validated for graph construction.
