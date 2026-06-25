# Transformer Utilization Report — Experiment 03A

Generated: 2026-06-25

## Question

Why does A3 (no transformer) perform similarly to A1 (ΔMAE = −0.66 MW, p = 0.38)?

## Performance

| Model | Demand MAE | Demand R² | Stress R² |
| --- | --- | --- | --- |
| A1 | 93.31 | 0.6743 | 0.5849 |
| A3 | 92.64 | 0.6706 | 0.7005 |

Difference is **not statistically significant**.

## Temporal attention diagnostics (A1, test set)

|   mean_temporal_attn_entropy |   max_entropy_log_T |   normalized_entropy_ratio |   mean_mass_on_last_timestep |   n_windows |
|-----------------------------:|--------------------:|---------------------------:|-----------------------------:|------------:|
|                       1.9421 |              1.9459 |                      0.998 |                       0.1435 |        1056 |

- Normalized entropy ratio **0.998** (≈1.0 = nearly uniform / low selectivity).
- Mean mass on last timestep: **0.144**.

Attention is **near-uniform** (entropy ratio 0.998); the graph branch already
processes all **T=7** timesteps via GraphTransformer, partially substituting for temporal encoding.

## Representation overlap (h_shared, test)

| pair     |   mean_cosine_per_sample |   std_cosine_per_sample |
|:---------|-------------------------:|------------------------:|
| A1 vs A3 |                   0.6956 |                  0.2173 |
| A1 vs A4 |                   0.3045 |                  0.2357 |

A1 and A3 produce **moderately aligned** latent codes (mean cosine ≈ **0.70**), while A1 vs A4 diverge strongly (cosine ≈ **0.30**), consistent with different training objectives.

## Conclusion

The transformer is **weakly utilized for demand** in this dataset: graph-temporal message passing
on the 7-day window captures most usable temporal context. Removing it (A3) does not materially
harm demand MAE, though it slightly **improves stress R²** in this run (0.701 vs 0.585).
