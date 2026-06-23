# Phase 04 — Data Preprocessing

## Objective

Prepare the cleaned dataset for machine learning while preventing data leakage.

The purpose of this phase is to transform the cleaned dataset into a model-ready format without creating any new predictive features.

---

## Input

data/interim/bangladesh_smartgrid_clean.parquet

---

## Output

data/processed/

* train.parquet
* validation.parquet
* test.parquet

configs/

preprocessing_config.yaml

models/

preprocessing_pipeline.pkl

---

## Allowed

* Datetime conversion
* Chronological sorting
* Time-based train/validation/test split
* Data type optimization
* Encoding categorical variables
* Fit preprocessing pipeline on training data only
* Transform validation and test using fitted pipeline
* Save preprocessing pipeline

---

## Not Allowed

* Feature engineering
* Rolling statistics
* Lag features
* Graph construction
* Model training
* Hyperparameter tuning
* Target balancing

---

## Scientific Rules

1. Never fit preprocessing on the entire dataset.

2. Perform chronological split before fitting transformers.

3. Validation and test data must never influence preprocessing parameters.

4. Preserve temporal ordering.

5. Ensure reproducibility.

---

## Deliverables

data/processed/

* train.parquet
* validation.parquet
* test.parquet

results/phases/phase_04_preprocessing/

* preprocessing_summary.md
* encoding_report.csv
* scaling_report.csv
* split_report.md
* preprocessing_log.csv

---

## Update

Update this phase document with

* Split strategy
* Encoding strategy
* Scaling strategy
* Data leakage prevention
* Recommendations for Phase 05

---

## Definition of Done

* Dataset split chronologically
* No leakage detected
* Pipeline saved
* Processed datasets generated
* Reports completed
* Ready for Feature Engineering

---

## Execution Record

### Completion Date

2026-06-16

### Split Strategy

* **Method:** Chronological split on `Date` after sorting ascending.
* **Ratios:** 70% train / 15% validation / 15% test.
* **Sizes & date ranges:**

| split | rows | date start | date end |
| --- | --- | --- | --- |
| train | 1,295 | 2019-11-21 | 2023-06-15 |
| validation | 277 | 2023-06-16 | 2024-03-19 |
| test | 278 | 2024-03-20 | 2024-12-30 |

* All 1,850 cleaned rows assigned to exactly one split; temporal ordering preserved.
* The 17 missing calendar days from Phase 03 were **not imputed or filled** — only observed daily records are retained.

### Encoding Strategy

* **Categorical columns one-hot encoded** (fitted on train only, `handle_unknown=ignore`):
  * `Day of the week` (7 categories)
  * `Holiday name` (31 categories in train)
  * `Holiday_cat` (4 categories: 0–3)
* Produces 38 encoded binary features from 3 source columns.
* Unseen categories in validation/test are safely ignored (zero vector).

### Scaling Strategy

* **`StandardScaler`** applied to 42 numeric columns (all measurements + `Year` + `Month`).
* Scaler parameters (mean, std) learned from **train split only**; validation and test transformed with frozen parameters.
* Processed feature values stored as `float32` for memory efficiency.
* `Date` preserved as `datetime64[ns]` in each output split (not scaled).

### Data Leakage Prevention

* Chronological split performed **before** any transformer fitting.
* Pipeline fitted exclusively on train (1,295 rows).
* Validation and test receive `transform()` only — no refitting.
* Verified: train max date (2023-06-15) < validation min (2023-06-16) < test min (2024-03-20).
* Interim input (`bangladesh_smartgrid_clean.parquet`) unchanged (MD5 verified before/after).

### Deliverables Generated

Processed data — `data/processed/`:

* `train.parquet` (1,295 × 81)
* `validation.parquet` (277 × 81)
* `test.parquet` (278 × 81)

Pipeline & config:

* `models/preprocessing_pipeline.pkl`
* `configs/preprocessing_config.yaml`

Reports — `results/phases/phase_04_preprocessing/`:

* `preprocessing_summary.md`
* `encoding_report.csv`
* `scaling_report.csv`
* `split_report.md`
* `preprocessing_log.csv`

Script: `scripts/phase_04_preprocessing.py`

### Recommendations for Phase 05

* Use processed splits as the base for feature engineering (lags, rolling statistics, calendar features) — keeping train-only fitting discipline for any new transformers.
* Define explicit target columns before engineering: continuous regional/national demand (regression) and sparse `_load` (zero-inflated / event task).
* Consider inverse-transforming scaled targets at evaluation time if models are trained on scaled outputs.
* Build graph adjacency from regional correlation structure (Phase 02) in the graph-construction phase, not during preprocessing.
* Preserve `Date` as the temporal index when constructing windowed sequences for the STGT model.

### Status

Ready for Feature Engineering.
