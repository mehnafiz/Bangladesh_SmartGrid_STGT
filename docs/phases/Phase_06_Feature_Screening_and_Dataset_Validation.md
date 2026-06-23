# Phase 06 — Feature Screening & Dataset Validation

## Objective

Validate the engineered feature datasets and perform scientific feature screening before graph construction.

This phase is intended to verify feature quality, dataset integrity, temporal consistency, and leakage prevention.

This is NOT the final feature selection stage.

---

## Input

data/features/

* train_features.parquet
* validation_features.parquet
* test_features.parquet

---

## Scope

### Allowed

✔ Dataset validation

✔ Feature validation

✔ Constant feature detection

✔ Near-zero variance detection

✔ Duplicate feature detection

✔ Missing value validation

✔ Infinite value detection

✔ Data leakage verification

✔ Feature distribution comparison

✔ Train/Validation/Test consistency checking

---

### Not Allowed

❌ Remove graph-related features

❌ Boruta

❌ Recursive Feature Elimination

❌ SHAP selection

❌ Model-based feature selection

❌ Model training

❌ Graph construction

---

## Validation Checklist

Verify

1. No constant features

2. No duplicate engineered features

3. No unexpected missing values

4. No infinite values

5. No leakage between train/validation/test

6. Feature distributions are reasonable

7. Data types are correct

8. Temporal ordering preserved

---

## Deliverables

results/phases/

phase_06_feature_screening/

* feature_validation_report.md

* feature_quality_summary.csv

* constant_feature_report.csv

* duplicate_feature_report.csv

* missing_feature_report.csv

* leakage_validation_report.md

* dataset_validation_report.md

* screening_summary.md

---

## Update

Update this phase document with

* Validation Results

* Dataset Health

* Feature Health

* Leakage Assessment

* Recommendations for Graph Construction

---

## Definition of Done

✔ Dataset validated

✔ Feature quality verified

✔ No leakage detected

✔ Reports completed

✔ Ready for Graph Construction

---

## Execution Record

### Completion Date

2026-06-16

### Validation Results

* **65/65 engineered features** validated across train, validation, and test splits.
* **Dataset integrity: PASS** — 1,850 total rows (1,295 + 277 + 278), 146 columns, identical schema across splits.
* **Feature quality: PASS** — 0 constant, 0 near-zero variance, 0 infinite, 0 unexpected missing, 0 exact duplicate pairs.
* **Temporal integrity: PASS** — dates monotonic in all splits; non-overlapping chronological boundaries preserved.
* **Leakage assessment: PASS** — train max (2023-06-15) < val min (2023-06-16) < test min (2024-03-20); no date overlap between splits.

### Dataset Health

| split | rows | date range | monotonic |
| --- | --- | --- | --- |
| train | 1,295 | 2019-11-21 → 2023-06-15 | True |
| validation | 277 | 2023-06-16 → 2024-03-19 | True |
| test | 278 | 2024-03-20 → 2024-12-30 | True |

* Column schema consistent (146 cols = 81 baseline + 65 engineered).
* Input feature files unchanged (MD5 verified before/after screening).
* Expected warm-up missing values in train only: 1 row (lag-1/load_lag-1) and 7 rows (lag-7/rolling-7) at series start.

### Feature Health

| check | count |
| --- | --- |
| Engineered features validated | 65 |
| Passing validation | 65 |
| Constant features | 0 |
| Near-zero variance | 0 |
| Infinite values | 0 |
| Unexpected missing | 0 |
| Exact duplicate pairs | 0 |
| Val/test missing values | 0 (all engineered features) |

All 65 High-Priority features from Phase 05B present in all splits with correct dtypes (`float32`).

### Leakage Assessment

* **No temporal leakage detected** between train / validation / test.
* Lag and rolling features correctly use history from prior periods (including train history for val/test rows — valid for forecasting).
* Train-only fitted transforms from Phase 05B (temperature anomaly, OSI, StandardScaler) confirmed by design audit.
* Distribution shifts after scaling are within expected bounds; no split overlap.

### Scope Compliance

* Screening and validation only — **no feature selection** performed.
* **No features removed** (graph-related or otherwise).
* No Boruta, RFE, SHAP selection, model training, or graph construction.
* Locked phase outputs (Phases 01–05B) not modified.

### Deliverables Generated

`results/phases/phase_06_feature_screening/`:

* `feature_validation_report.md`
* `feature_quality_summary.csv` (195 rows: 65 features × 3 splits)
* `constant_feature_report.csv`
* `duplicate_feature_report.csv`
* `missing_feature_report.csv`
* `leakage_validation_report.md`
* `dataset_validation_report.md`
* `screening_summary.md`

Script: `scripts/phase_06_feature_screening.py`

### Recommendations for Graph Construction

1. **Node set:** 9 regional divisions with validated node features (demand, supply, load, lags, shares, load intensity).
2. **Global context:** Attach grid-level features (`total_regional_demand`, `generation_reserve`, `operational_stress_index`, exogenous limitations) as graph-level conditioning.
3. **Dynamic edges:** Implement blueprint Batch 3 candidates — `rolling_demand_corr_90d`, `pairwise_demand_gradient` — using train-only trailing windows per split boundary.
4. **Static prior:** Add `static_geographic_adjacency_prior` from Bangladesh admin borders as structural inductive bias.
5. **Warm-up handling:** Mask or exclude first 7 train timesteps when building sequence windows (lag-7 / rolling-7 NaNs).
6. **Multi-task heads:** Demand regression on continuous targets; zero-inflated / event head for sparse `_load` (per Phase 02/05A findings).

### Status

Ready for Graph Construction.
