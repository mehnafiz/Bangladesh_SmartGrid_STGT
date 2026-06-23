# Phase 05B — Feature Validation Report

## Leakage prevention

- Features computed on full chronological timeline; lags/rolling use **past rows only** (`shift` + `rolling`).
- Train-only fitted transforms: monthly temperature means, OSI component bounds, StandardScaler on engineered features.
- Train max date < validation min: **True** (2023-06-15 < 2023-06-16)
- Validation max < test min: **True**
- Row counts preserved after merge: **True**

## Output schema

- Baseline processed columns: **81**
- New engineered columns: **65**
- Total columns per split: **146**

## Missing values (train split)

| feature | n_missing | missing_pct |
| --- | --- | --- |
| demand_lag_1_Dhaka | 1 | 0.0772% |
| demand_lag_1_Chattogram | 1 | 0.0772% |
| demand_lag_1_Rajshahi | 1 | 0.0772% |
| demand_lag_1_Mymensingh | 1 | 0.0772% |
| demand_lag_1_Sylhet | 1 | 0.0772% |
| demand_lag_1_Barishal | 1 | 0.0772% |
| demand_lag_1_Rangpur | 1 | 0.0772% |
| demand_lag_1_Cumilla | 1 | 0.0772% |
| demand_lag_1_Khulna | 1 | 0.0772% |
| demand_lag_7_Dhaka | 7 | 0.5405% |
| demand_lag_7_Chattogram | 7 | 0.5405% |
| demand_lag_7_Rajshahi | 7 | 0.5405% |
| demand_lag_7_Mymensingh | 7 | 0.5405% |
| demand_lag_7_Sylhet | 7 | 0.5405% |
| demand_lag_7_Barishal | 7 | 0.5405% |
| demand_lag_7_Rangpur | 7 | 0.5405% |
| demand_lag_7_Cumilla | 7 | 0.5405% |
| demand_lag_7_Khulna | 7 | 0.5405% |
| load_lag_1_Dhaka | 1 | 0.0772% |
| load_lag_1_Chattogram | 1 | 0.0772% |
| load_lag_1_Rajshahi | 1 | 0.0772% |
| load_lag_1_Mymensingh | 1 | 0.0772% |
| load_lag_1_Sylhet | 1 | 0.0772% |
| load_lag_1_Barishal | 1 | 0.0772% |
| load_lag_1_Rangpur | 1 | 0.0772% |
| load_lag_1_Cumilla | 1 | 0.0772% |
| load_lag_1_Khulna | 1 | 0.0772% |
| demand_rolling_mean_7_Dhaka | 7 | 0.5405% |
| demand_rolling_mean_7_Chattogram | 7 | 0.5405% |
| demand_rolling_mean_7_Rajshahi | 7 | 0.5405% |
| demand_rolling_mean_7_Mymensingh | 7 | 0.5405% |
| demand_rolling_mean_7_Sylhet | 7 | 0.5405% |
| demand_rolling_mean_7_Barishal | 7 | 0.5405% |
| demand_rolling_mean_7_Rangpur | 7 | 0.5405% |
| demand_rolling_mean_7_Cumilla | 7 | 0.5405% |
| demand_rolling_mean_7_Khulna | 7 | 0.5405% |

- Expected warm-up NaNs at series start for lag-7 and rolling-7 features (first 7 rows of full timeline; fewer in train split start).

## Integrity

- Interim input unchanged: **True**
- Processed train unchanged: **True**

## Chronological ordering

- Train dates monotonic: **True**
- Validation dates monotonic: **True**
- Test dates monotonic: **True**
