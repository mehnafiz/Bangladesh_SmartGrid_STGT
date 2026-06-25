# Performance vs Complexity — Experiment 03B

Generated: 2026-06-25

## Test-set demand performance

| variant_id   | model_name                        |   demand_mae |   demand_r2 |   stress_r2 |   active_parameters |   training_seconds |
|:-------------|:----------------------------------|-------------:|------------:|------------:|--------------------:|-------------------:|
| S2           | Correlation-Only PF-STGT          |      88.6487 |      0.6838 |      0.7451 |              749058 |            393.078 |
| S3           | No-Transformer PF-STGT            |      92.6436 |      0.6706 |      0.7005 |              451202 |            366.959 |
| S1           | PF-STGT (W20)                     |      93.3084 |      0.6743 |      0.5849 |              749058 |            413.464 |
| S4           | Correlation-Only + No-Transformer |     114.631  |      0.3617 |      0.7468 |              451202 |            308.835 |

## ΔMAE vs S1 (reference PF-STGT)

| Variant | ΔMAE (MW) | % change | Active params | Training (s) |
| --- | --- | --- | --- | --- |
| S2 | -4.66 | -5.0% | 749,058 | 393 |
| S3 | -0.66 | -0.7% | 451,202 | 367 |
| S4 | +21.32 | +22.9% | 451,202 | 309 |

## Statistical tests vs S1 (Wilcoxon, per-sample MAE)

| comparison   | variant_name                      |   median_mae_diff_mw |   mean_mae_diff_mw |   wilcoxon_stat |   p_value_two_sided |   p_value_variant_better | bonferroni_significant_better_0.01   | bootstrap_95ci_mae_diff   |
|:-------------|:----------------------------------|---------------------:|-------------------:|----------------:|--------------------:|-------------------------:|:-------------------------------------|:--------------------------|
| S1 vs S2     | Correlation-Only PF-STGT          |             -5.43241 |           -4.65967 |           12483 |            5.5e-05  |                 2.8e-05  | True                                 | [-7.17, -2.16]            |
| S1 vs S3     | No-Transformer PF-STGT            |             -1.12954 |           -0.66478 |           16408 |            0.383577 |                 0.191788 | False                                | [-2.36, 1.10]             |
| S1 vs S4     | Correlation-Only + No-Transformer |             14.4684  |           21.3223  |            8086 |            0        |                 1        | False                                | [16.47, 26.40]            |

## Efficiency summary

- **Best demand MAE:** Correlation-Only PF-STGT (S2) — 88.65 MW
- **S2 beats S1** on demand (−4.66 MW); correlation graph adds signal hybrid dilutes.
- **S3 ≈ S1** (-0.66 MW); transformer adds little marginal demand value.
- **S4 stacks both removals and degrades:** demand MAE 114.63 MW (+21.32 vs S1; p < 0.001). Correlation graph appears to benefit from the temporal branch that S4 removes.

Removing inactive modules (S3/S4 forward path) reduces **compute** (~40% fewer active parameters) but not stored model size.
