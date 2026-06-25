# Statistical Significance Plan — Phase 13

Generated: 2026-06-24
Status: **FROZEN**

## Primary comparison unit

**Daily macro MAE** on test split: for each day d,

```
macro_MAE_d = (1/9) Σ_r |D_r(d) − D̂_r(d)|
```

Yields ~278 paired observations (test windows) for A1 vs each ablation.

## Primary test

| Setting | Test | Null hypothesis |
| --- | --- | --- |
| A1 vs A_v | **Wilcoxon signed-rank** (paired) | median(ΔMAE_d) = 0 |
| Significance | α = 0.05 with **Bonferroni** correction | α_adj = 0.0100 for 5 comparisons vs A1 |

Comparisons corrected: A2, A3, A4, A5-GEO, A6.

## Secondary tests

| Metric | Test | Notes |
| --- | --- | --- |
| RMSE | Wilcoxon on daily macro RMSE | Supplementary |
| MAPE | Wilcoxon on daily macro MAPE | Scale-sensitive; report with MAE |
| R² | Bootstrap 95% CI on R² difference | 1,000 resamples, test days |
| Stress MAE | Wilcoxon on daily |OSI − OSI_hat| | A4 excluded |

## Effect size

```
Cohen's d = mean(MAE_v − MAE_A1) / std(MAE_v − MAE_A1)  across test days
|d| ≥ 0.5 → medium effect (report in paper)
```

## Multi-seed uncertainty (A1 only)

- Report A1 test MAE as mean ± std over seeds {42, 123, 456}.
- Ablation point estimates use seed 42; compare to A1 seed-42 for paired tests.

## Non-inferiority check (A6 explainability)

One-sided test: A6 not worse than A1 by more than **5% relative MAE**.

```
H0: MAE_A6 ≥ 1.05 × MAE_A1
Use bootstrap upper 95% CI on (MAE_A6 − MAE_A1) / MAE_A1
```

## Output artefacts

```
results/ablation/significance_tests.csv
results/ablation/bootstrap_ci_mae.csv
results/ablation/effect_sizes.csv
```

## Reporting template

| Comparison | ΔMAE (MW) | p-value | p_adj | Cohen's d | Verdict |
| --- | --- | --- | --- | --- | --- |
| A1 vs A2 | — | — | — | — | — |
| ... | | | | | |
