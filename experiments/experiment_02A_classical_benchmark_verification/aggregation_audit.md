# Aggregation Audit — Experiment 02A

Generated: 2026-06-25

## Definitions audited

| Scheme | MAE | RMSE | R² | Used in Exp02 for |
| --- | --- | --- | --- | --- |
| **Macro (Phase 15)** | Mean of 9 regional MAEs | Mean of 9 regional RMSEs | Mean of 9 regional R² | B04–B07 (via `compute_demand_metrics`) |
| **Pooled (train_classical)** | Mean over all N×9 values | √mean squared error over all values | Single R² on flattened pooled series | B01–B03 (via `train_classical._demand_metrics`) |

## Side-by-side metrics

| model_id   | model_name    | scheme                   |      mae |    rmse |   mape |     r2 |
|:-----------|:--------------|:-------------------------|---------:|--------:|-------:|-------:|
| B07        | PF-STGT (W20) | macro (Phase 15)         |  93.3084 | 128.809 | 6.7599 | 0.6743 |
| B07        | PF-STGT (W20) | pooled (train_classical) |  93.3084 | 170.34  | 6.7599 | 0.9813 |
| B02        | Random Forest | macro (Phase 15)         |  97.0265 | 124.35  | 7.0374 | 0.6878 |
| B02        | Random Forest | pooled (train_classical) |  97.0264 | 156.99  | 7.0374 | 0.9841 |
| B03        | XGBoost       | macro (Phase 15)         | 109.727  | 141.073 | 7.9946 | 0.5902 |
| B03        | XGBoost       | pooled (train_classical) | 109.727  | 178.527 | 7.9946 | 0.9794 |

## Consistency verdict

| Model | Reported R² matches | Correct unified macro R² |
| --- | --- | --- |
| B02 RF | pooled (0.9841) | 0.6878 |
| B03 XGB | pooled (0.9794) | 0.5902 |
| B07 PF-STGT | macro (0.6743) | 0.6743 |

**Root aggregation issue:** Experiment 02 applied **two different R² definitions** across model families.
MAE/RMSE are numerically identical under macro and pooled schemes when each region
has the same sample count (264 test days), so MAE rankings are consistent.

## Per-region MAE (macro components)

### PF-STGT (B07)

| region     |      mae |     r2 |   actual_std |   pred_std |
|:-----------|---------:|-------:|-------------:|-----------:|
| Barishal   |  30.8464 | 0.4808 |      81.0697 |    82.4807 |
| Chattogram |  75.0388 | 0.6362 |     156.192  |   140.819  |
| Cumilla    |  71.8266 | 0.793  |     210.326  |   185.877  |
| Dhaka      | 299.776  | 0.5744 |     670.147  |   530.556  |
| Khulna     | 118.722  | 0.7353 |     272.509  |   233.359  |
| Mymensingh |  58.7399 | 0.7584 |     168.673  |   154.994  |
| Rajshahi   |  85.7009 | 0.827  |     262.637  |   217.788  |
| Rangpur    |  59.7748 | 0.6928 |     139.3    |   124.518  |
| Sylhet     |  39.3502 | 0.5707 |      97.9822 |    95.6377 |

### Random Forest (B02)

| region     |      mae |     r2 |   actual_std |   pred_std |
|:-----------|---------:|-------:|-------------:|-----------:|
| Barishal   |  32.0709 | 0.6936 |      81.0697 |    68.502  |
| Chattogram |  79.9652 | 0.5941 |     156.192  |    98.9667 |
| Cumilla    |  73.6319 | 0.7688 |     210.326  |   199.537  |
| Dhaka      | 311.587  | 0.6666 |     670.147  |   508.911  |
| Khulna     |  92.0577 | 0.7835 |     272.509  |   242.4    |
| Mymensingh |  85.8478 | 0.6126 |     168.673  |   108.866  |
| Rajshahi   |  83.1256 | 0.8274 |     262.637  |   217.551  |
| Rangpur    |  68.4094 | 0.6264 |     139.3    |   100.935  |
| Sylhet     |  46.5422 | 0.6171 |      97.9822 |    66.6072 |
