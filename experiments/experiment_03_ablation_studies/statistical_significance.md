# Statistical Significance — Experiment 03

Generated: 2026-06-25

Wilcoxon signed-rank on per-sample macro demand MAE (test set).
Bonferroni-adjusted α = 0.01 for 5 comparisons vs A1 (Phase 13).

| comparison   | ablation_name           |   median_mae_diff_mw |   mean_mae_diff_mw |   wilcoxon_stat |   p_value_two_sided |   p_value_ablation_worse | bonferroni_significant_0.01   | bootstrap_95ci_mae_diff   |
|:-------------|:------------------------|---------------------:|-------------------:|----------------:|--------------------:|-------------------------:|:------------------------------|:--------------------------|
| A1 vs A2     | No Graph                |              2.81165 |           0.617371 |           16206 |            0.301139 |                 0.15057  | False                         | [-3.69, 4.93]             |
| A1 vs A3     | No Transformer          |             -1.12954 |          -0.66478  |           16408 |            0.383577 |                 0.808212 | False                         | [-2.35, 1.08]             |
| A1 vs A4     | Single-Task             |             -5.247   |          -6.42265  |           13784 |            0.002841 |                 0.998579 | False                         | [-10.63, -2.40]           |
| A1 vs A5     | Geographical Graph Only |              3.84653 |           4.66795  |           12779 |            0.000148 |                 7.4e-05  | True                          | [2.19, 6.90]              |
| A1 vs A6     | Correlation Graph Only  |             -5.43241 |          -4.65967  |           12483 |            5.5e-05  |                 0.999972 | False                         | [-7.17, -2.16]            |
