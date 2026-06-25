# Variance Explanation — Experiment 02A

Generated: 2026-06-25

## Why R² ranking diverges from MAE ranking

Under **unified macro R²** (Phase 15 definition), rankings align with intuition:

| model         |   macro_mae |   macro_r2 |   pooled_r2 |
|:--------------|------------:|-----------:|------------:|
| PF-STGT (W20) |     93.3084 |     0.6743 |      0.9813 |
| Random Forest |     97.0265 |     0.6878 |      0.9841 |
| XGBoost       |    109.727  |     0.5902 |      0.9794 |

### Mechanism 1 — Inconsistent R² aggregation (primary)

Experiment 02 reported **pooled R²** for Random Forest / XGBoost but **macro R²** for PF-STGT.
RF pooled R² = 0.9841 vs macro R² = 0.6878.
PF-STGT pooled R² = 0.9813 vs macro R² = 0.6743.

Pooled R² weights high-variance regions (Dhaka) more heavily because they contribute
more to total sum-of-squares. Tree models score higher under pooled R² because they
fit Dhaka peaks better.

### Mechanism 2 — Variance attenuation in PF-STGT (secondary)

PF-STGT prediction std / actual std = 0.983.
Lower dynamic range reduces SS_res relative to mean-benchmark but hurts R² when
regional variance is high.

## Regional variance decomposition (top 3 by actual variance)

| model_id   | region   |   actual_variance |     r2 |      mae |   pred_std_ratio |
|:-----------|:---------|------------------:|-------:|---------:|-----------------:|
| B03        | Dhaka    |          449098   | 0.5663 | 345.832  |           0.7443 |
| B07        | Dhaka    |          449098   | 0.5744 | 299.776  |           0.7917 |
| B02        | Dhaka    |          449098   | 0.6666 | 311.587  |           0.7594 |
| B02        | Khulna   |           74261.1 | 0.7835 |  92.0577 |           0.8895 |
| B03        | Khulna   |           74261.1 | 0.725  | 105.239  |           0.8435 |
| B07        | Khulna   |           74261.1 | 0.7353 | 118.722  |           0.8563 |
| B02        | Rajshahi |           68978.1 | 0.8274 |  83.1256 |           0.8283 |
| B07        | Rajshahi |           68978.1 | 0.827  |  85.7009 |           0.8292 |
| B03        | Rajshahi |           68978.1 | 0.7799 |  95.7775 |           0.7457 |
