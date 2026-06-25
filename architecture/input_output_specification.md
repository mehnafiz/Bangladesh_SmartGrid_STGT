# Input / Output Specification — Phase 09

Generated: 2026-06-24

## Model I/O contract

### Inputs

| Input | Shape | Dtype | Source |
| --- | --- | --- | --- |
| `node_features` | (B, T=7, N=9, F_n=9) | float32 | `data/features/*_features.parquet` |
| `global_features` | (B, T, F_g=17) | float32 | same |
| `adjacency` | (N, N) | float32 | Row-normalised graph — **S1:** hybrid; **S2 (final):** correlation-only (`GraphVariant.CORR`) |
| `region_index` | (N,) | int | fixed alphabetical order |

### Targets (supervision at training — not inputs)

| Target | Shape | Horizon | Source |
| --- | --- | --- | --- |
| `demand_target` | (B, N) | t+1 | `{Region}_demand` from clean/features |
| `osi_target` | (B, 1) | t+1 | OSI computed per Phase 05B formula |

### Outputs

| Output | Shape | Range | Task |
| --- | --- | --- | --- |
| `demand_pred` | (B, N) | MW (post inverse-scaling) | Task 1 |
| `osi_pred` | (B, 1) | [0, 1] | Task 2 |
| `attn_spatial` | (B, heads, N, N) | [0, 1] optional export | Explainability |
| `attn_temporal` | (B, heads, T, T) | [0, 1] optional export | Explainability |

## Leakage-safe input policy (Phase 08.5)

At forecast origin time t (last window timestep):

- **Allowed:** all node/global features observed at or before t
- **Forbidden as input:** `operational_stress_index` at t when predicting OSI(t+1)
- **Allowed target:** OSI(t+1), D_r(t+1)

## Window construction

- T=7 consecutive observed days ending at t
- Skip first 7 train timesteps (Phase 06 warm-up for lag-7 / rolling-7)
- Respect 17 calendar gaps via gap-aware lags (Phase 05B)

## Node ordering (must match adjacency)

```
Barishal, Chattogram, Cumilla, Dhaka, Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet
```
