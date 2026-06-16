# Phase 01 — Data Audit & Research Readiness

## Objective

Perform a complete **read-only audit** of the original dataset.

The goal is to understand the dataset scientifically before any preprocessing, cleaning, feature engineering, or modelling.

This phase establishes whether the dataset is suitable for a Spatio-Temporal Graph Transformer based multi-task learning framework.

---

## Input

data/raw/bangladesh_smartgrid_raw.csv

---

## Scope

Allowed

* Read dataset
* Inspect structure
* Identify feature names
* Identify data types
* Count rows and columns
* Detect missing values
* Detect duplicate rows
* Produce descriptive statistics
* Detect target variable(s)
* Inspect temporal information
* Document observations

Not Allowed

* Remove rows
* Remove columns
* Modify values
* Encode variables
* Normalize data
* Impute missing values
* Create models
* Perform feature engineering
* Build graphs

---

## Deliverables

results/phase_01_data_audit/

* dataset_summary.csv
* feature_dictionary.csv
* data_types_report.csv
* missing_value_report.csv
* duplicate_report.csv
* target_analysis.csv
* basic_statistics.csv
* temporal_structure_report.md
* data_audit_report.md

---

## Phase Report

Update

docs/phases/Phase_01_Data_Audit.md

after execution with

* Completion Date
* Deliverables Generated
* Initial Findings
* Research Risks
* Recommendations for Phase 02

---

## Definition of Done

* Dataset inspected
* Dataset not modified
* Reports generated
* Deliverables saved
* Phase documentation updated
* Ready for review

---

## Execution Record

### Completion Date

2026-06-16

### Integrity

* Read-only audit confirmed.
* Source file MD5 unchanged before/after: `28d8594de1b60ba37892e56ae64a8262`
* No rows/columns removed, no values modified, no encoding/normalization/imputation/feature-engineering/graph-building/modelling performed.

### Deliverables Generated

All written to `results/phase_01_data_audit/`:

* `dataset_summary.csv`
* `feature_dictionary.csv`
* `data_types_report.csv`
* `missing_value_report.csv`
* `duplicate_report.csv`
* `target_analysis.csv`
* `basic_statistics.csv`
* `temporal_structure_report.md`
* `data_audit_report.md`

Audit script (read-only): `scripts/phase_01_data_audit.py`

### Initial Findings

* **Shape:** 1,850 rows × 45 columns (42 numeric, 3 non-numeric: `Date`, `Day of the week`, `Holiday name`).
* **Missing values:** 0 missing cells across the entire dataset (0.0%).
* **Duplicates:** 0 full duplicate rows; 0 duplicate `Date` values.
* **Temporal coverage:** Daily series from 2019-11-21 to 2024-12-30 (1,866-day calendar span, 1,850 unique daily records). Dominant sampling interval = 1 day; 11 calendar gaps (9 × 2-day, 1 × 3-day, 1 × 7-day), so ~17 expected days are absent vs. a perfectly continuous daily series.
* **Spatial structure:** 9 regional divisions (Dhaka, Chattogram, Rajshahi, Mymensingh, Sylhet, Barishal, Rangpur, Cumilla, Khulna), each with `_demand`, `_supply`, and `_load` triplets — a natural node set for a spatio-temporal graph.
* **National signals:** Generation/demand columns at generation and sub-station ends (peak, highest, minimum, day-peak, evening-peak, forecast).
* **Exogenous drivers present:** `Maximum Temperature in Dhaka`, `Gas/LF limitation`, `Coal supply Limitation`, `Low water level in Kaptai lake`, `Plants under shut down/maintenance`, plus calendar fields (`Year`, `Month`, `Day of the week`) and holiday flags (`Holiday name`, `Holiday_cat`).
* **Candidate targets:** 35 demand/supply/load/generation columns detected (see `target_analysis.csv`). Note: `Coal supply Limitation` matched on the substring "supply" but is an exogenous limitation feature, not a forecasting target.

### Research Risks

* **Sparse load-shedding targets:** Every regional `_load` column is overwhelmingly zero (e.g., `Dhaka_load` 1,497/1,850 zeros; `Barishal_load` 1,822/1,850 zeros). Load (unmet demand / shedding) is a rare, highly imbalanced signal — direct regression on it will be dominated by zeros and may need a separate task formulation (e.g., zero-inflated / classification of shedding events).
* **Temporal gaps:** 11 non-contiguous date steps mean the daily series is not perfectly regular; downstream windowing must account for missing calendar days rather than assuming strict day-to-day continuity.
* **Mixed dtypes in equivalent fields:** Some generation/demand fields are stored as `int64` and others as `float64` for conceptually similar quantities — consistency should be reviewed (without modifying raw data) in later phases.
* **Demand ≈ supply in most rows:** Regional demand and supply track each other closely, consistent with load being near-zero; this collinearity should be considered when defining independent prediction targets.
* **Categorical target leakage potential:** `Holiday name` / `Holiday_cat` and limitation flags are strong exogenous drivers; care is needed in later phases to avoid leakage when constructing features.

### Recommendations for Phase 02

* Treat the 9 regions as graph nodes; define `_demand`, `_supply`, `_load` as candidate node-level targets, with the national generation/peak metrics as graph-level (global) signals.
* Decide an explicit target strategy for the sparse `_load` signal (separate task head, event classification, or de-prioritize) before any preprocessing.
* Establish a complete daily calendar index and explicitly mark the ~17 absent days as gaps (handling deferred to the preprocessing phase — no imputation in Phase 01).
* Normalize dtype representation of equivalent generation/demand quantities during preprocessing (Phase 02+), keeping raw data untouched.
* Catalogue exogenous covariates (temperature, fuel/water/maintenance limitations, calendar, holidays) for use as conditioning inputs, with a leakage-safe split plan.

### Status

Ready for review.
