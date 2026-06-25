# Metric Verification — Experiment 02A

Generated: 2026-06-25

## Objective

Recompute demand metrics from materialized test-set predictions and compare
against Experiment 02 `benchmark_results.csv`.

## Prediction sources

| Model | Source |
| --- | --- |
| B07 PF-STGT | W20 checkpoint inference only (`predict_pf_stgt.py`) |
| B02 Random Forest | Deterministic Exp02 protocol replay (`predict_classical.py`) |
| B03 XGBoost | Deterministic Exp02 protocol replay (`predict_classical.py`) |

## Verification table

| model_id   | model_name    |   reported_mae |   recomputed_macro_mae |   mae_delta |   reported_r2 |   recomputed_macro_r2 |   recomputed_pooled_r2 |   r2_macro_delta |   r2_pooled_delta |   reported_rmse |   recomputed_macro_rmse |   reported_mape |   recomputed_mape |
|:-----------|:--------------|---------------:|-----------------------:|------------:|--------------:|----------------------:|-----------------------:|-----------------:|------------------:|----------------:|------------------------:|----------------:|------------------:|
| B07        | PF-STGT (W20) |        93.3084 |                93.3084 |     0       |      0.674277 |              0.674277 |               0.981253 |         0        |          0.306976 |         128.809 |                 128.809 |         6.75991 |           6.75991 |
| B02        | Random Forest |        97.0264 |                97.0265 |     1.9e-05 |      0.984076 |              0.687791 |               0.984076 |        -0.296285 |         -0        |         156.99  |                 124.35  |         7.0374  |           7.0374  |
| B03        | XGBoost       |       109.727  |               109.727  |     2.3e-05 |      0.979407 |              0.590229 |               0.979407 |        -0.389178 |          0        |         178.527 |                 141.074 |         7.99462 |           7.99463 |

## Findings

- **MAE match:** All models recomputed macro MAE matches reported values within floating-point tolerance (max |Δ| = 2.29e-05 MW).
- **R² mismatch (classical):** B02/B03 reported R² equals **pooled** R², not macro R² (B02 Δ = -3.12e-10; macro Δ = -0.296).
- **R² match (PF-STGT):** B07 reported R² matches **macro** R² (Δ = 0.00e+00).

## Rankings under unified macro metrics (recomputed)

### By MAE (lower is better)

|   rank | model_id   | model_name    |   macro_mae |
|-------:|:-----------|:--------------|------------:|
|      1 | B07        | PF-STGT (W20) |       93.31 |
|      2 | B02        | Random Forest |       97.03 |
|      3 | B03        | XGBoost       |      109.73 |

### By macro R² (higher is better)

|   rank | model_id   | model_name    |   macro_r2 |
|-------:|:-----------|:--------------|-----------:|
|      1 | B02        | Random Forest |     0.6878 |
|      2 | B07        | PF-STGT (W20) |     0.6743 |
|      3 | B03        | XGBoost       |     0.5902 |
