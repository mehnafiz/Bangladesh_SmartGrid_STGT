# Phase 04 — Split Report

## Strategy

- Method: **chronological** (sorted by `Date`)
- Ratios: train 70% / validation 15% / test 15%

## Split sizes

| split | rows | date start | date end |
| --- | --- | --- | --- |
| train | 1295 | 2019-11-21 | 2023-06-15 |
| validation | 277 | 2023-06-16 | 2024-03-19 |
| test | 278 | 2024-03-20 | 2024-12-30 |
| **total** | **1850** | | |

## Data leakage checks

- Train max date < validation min date: **True** (2023-06-15 < 2023-06-16)
- Validation max date < test min date: **True** (2024-03-19 < 2024-03-20)
- All input rows assigned to exactly one split: **True**
- Preprocessing fitted on train only: **True**
- Interim input unchanged (MD5 `4255024d735a91a4b53b2edee203d0ca`): **True**

## Calendar gaps

- The 17 missing calendar days documented in Phase 03 are **not imputed** and **not filled** in this phase. Rows remain at observed daily timestamps only.
