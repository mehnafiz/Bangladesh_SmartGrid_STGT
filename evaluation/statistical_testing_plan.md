# Statistical Testing Plan — Phase 15

Generated: 2026-06-24
Status: **FROZEN**

## Objective (D6)

Unified statistical protocol for benchmark and ablation comparisons,
extending Phase 13 ablation significance plan to full evaluation.

## Primary comparison unit

**Daily macro MAE** on test split (~278 paired observations):

```
macro_MAE_d = (1/9) Σ_r |D_r(d) − D̂_r(d)|
```

## Test battery

### Set 1 — Benchmark comparisons (B07 vs B01–B06)

| Comparison | Test | H0 | Correction |
| --- | --- | --- | --- |
| B07 vs B_v | Wilcoxon signed-rank (paired) | median(ΔMAE_d)=0 | Bonferroni, α_adj = 0.0083 |

One-sided alternative for primary claim: B07 MAE < B_v MAE.
Report two-sided p-values in Table 4; apply correction for claims.

### Set 2 — Ablation comparisons (A1 vs A2, A3, A4, A5-GEO, A6)

| Comparison | Test | Correction |
| --- | --- | --- |
| A1 vs A_v | Wilcoxon signed-rank | Bonferroni, α_adj = 0.0100 |

Per Phase 13: ablation seed 42 vs A1 seed 42 for paired tests.

### Set 3 — Stress comparisons (A1 only)

| Comparison | Test | Unit |
| --- | --- | --- |
| A1 vs persistence | Wilcoxon | daily |OSI − OSI_hat| |
| A1 vs train median | Wilcoxon | daily |OSI − OSI_hat| |
| High vs Low regime | Mann-Whitney | daily OSI error |

### Set 4 — Robustness segments

| Segment | Test | Notes |
| --- | --- | --- |
| Event vs normal days | Wilcoxon on daily MAE | Paired by model |
| High vs normal stress | Mann-Whitney | Unpaired OSI error |

## Confidence intervals

| Quantity | Method | Resamples |
| --- | --- | --- |
| MAE difference (B07 − B_v) | Bootstrap percentile CI | 1,000 |
| R² difference | Bootstrap CI | 1,000 |
| A1 MAE multi-seed | Report mean ± std (not CI) | 3 seeds |
| A6 non-inferiority | One-sided bootstrap upper 95% CI | 1,000 |

Non-inferiority (A6): upper 95% CI on (MAE_A6 − MAE_A1)/MAE_A1 < 5%.

## Effect size

```
Cohen's d = mean(ΔMAE_d) / std(ΔMAE_d)
|d| ≥ 0.2 small, ≥ 0.5 medium, ≥ 0.8 large
```

## Table 4 — Statistical Significance Results

### Columns

| Column | Description |
| --- | --- |
| comparison_id | e.g. B07_vs_B06, A1_vs_A2 |
| comparison_type | benchmark / ablation / stress / robustness |
| metric | macro_MAE / osi_MAE / etc. |
| delta_mean | Mean difference (test days) |
| ci_95_low, ci_95_high | Bootstrap CI |
| p_value | Two-sided Wilcoxon |
| p_adj | Bonferroni-adjusted |
| cohens_d | Effect size |
| significant | p_adj < α |
| verdict | Supports / Does not support claim |

### Row ordering

1. Benchmark set (6 rows)
2. Ablation set (5 rows)
3. Stress baselines (2 rows)
4. Key robustness (3 rows: extreme, high-stress, shedding)

## Reporting rules

- Always report **MAE + p_adj + Cohen's d** together.
- Non-significant benchmark win: report as trend, not claim.
- Multi-seed std reported separately from inferential tests.
- All tests on test split only; no peeking at test during model selection.

## Output artefacts

```
results/evaluation/tables/table4_statistical_significance.csv
results/evaluation/statistics/significance_tests.csv
results/evaluation/statistics/bootstrap_ci_mae.csv
results/evaluation/statistics/effect_sizes.csv
results/evaluation/statistics/stress_significance.csv
```
