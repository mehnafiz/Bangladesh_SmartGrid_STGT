# Prediction Distribution Analysis — Experiment 02A

Generated: 2026-06-25

| model_id   | model_name    |   actual_mean_mw |   actual_std_mw |   pred_mean_mw |   pred_std_mw |   pred_actual_corr |   mean_per_region_r2 |   pooled_r2 |
|:-----------|:--------------|-----------------:|----------------:|---------------:|--------------:|-------------------:|---------------------:|------------:|
| B07        | PF-STGT (W20) |          1457.74 |         1244.07 |        1438.16 |       1223.03 |             0.9907 |               0.6743 |      0.9813 |
| B02        | Random Forest |          1457.74 |         1244.07 |        1424.66 |       1198.15 |             0.9928 |               0.6878 |      0.9841 |
| B03        | XGBoost       |          1457.74 |         1244.07 |        1405.36 |       1180.1  |             0.9915 |               0.5902 |      0.9794 |

## Key observations

| Model | Pred/Actual std ratio | Interpretation |
| --- | --- | --- |
| B07 PF-STGT | 0.983 | Attenuated dynamic range — damped variance |
| B02 RF | 0.963 | Tracks actual spread more closely |
| B03 XGB | 0.949 | Intermediate variance tracking |

PF-STGT achieves lower macro MAE partly by staying closer to typical load levels,
but under-predicts peak swings (especially Dhaka), lowering per-region R².

## Visualizations

Per-region actual-vs-predicted scatter plots:

- `plots/actual_vs_pred_Barishal.png`
- `plots/actual_vs_pred_Chattogram.png`
- `plots/actual_vs_pred_Cumilla.png`
- `plots/actual_vs_pred_Dhaka.png`
- `plots/actual_vs_pred_Khulna.png`
- `plots/actual_vs_pred_Mymensingh.png`
- `plots/actual_vs_pred_Rajshahi.png`
- `plots/actual_vs_pred_Rangpur.png`
- `plots/actual_vs_pred_Sylhet.png`
