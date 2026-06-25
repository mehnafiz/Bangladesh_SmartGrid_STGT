# Statistical Significance — Experiment 02

Wilcoxon signed-rank test on per-sample macro demand MAE (test set).
Bonferroni-adjusted α = 0.0083 for 6 comparisons (Phase 15).

| comparison   |   median_mae_diff_mw |   wilcoxon_stat |   p_value_two_sided |   p_value_b07_better_one_sided |   cohens_d | bonferroni_significant_0.0083   | bootstrap_95ci_mae_diff   |
|:-------------|---------------------:|----------------:|--------------------:|-------------------------------:|-----------:|:--------------------------------|:--------------------------|
| B07 vs B01   |            -58.9777  |            2993 |         1.7247e-31  |                    8.62351e-32 | -0.490951  | True                            | [-193.11, -120.58]        |
| B07 vs B02   |             -4.92395 |           13511 |         0.00135413  |                    0.000677067 | -0.0774399 | True                            | [-8.87, 2.62]             |
| B07 vs B03   |            -14.1347  |            8966 |         6.68176e-12 |                    3.34088e-12 | -0.297711  | True                            | [-22.76, -9.55]           |
| B07 vs B04   |           -134.415   |            1190 |         2.32925e-39 |                    1.16462e-39 | -1.22379   | True                            | [-158.49, -129.48]        |
| B07 vs B05   |           -128.935   |            1172 |         1.92337e-39 |                    9.61686e-40 | -1.21916   | True                            | [-154.54, -126.62]        |
| B07 vs B06   |           -160.656   |             933 |         1.48385e-40 |                    7.41924e-41 | -1.29617   | True                            | [-179.85, -148.85]        |
