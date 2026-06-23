# Phase 03 — Scientific Data Cleaning

## Objective

Create a scientifically valid cleaned dataset while preserving all meaningful operational events.

This phase is NOT responsible for model preparation.

The objective is only to remove or correct invalid records while preserving genuine rare events.

---

## Input

data/raw/bangladesh_smartgrid_raw.csv

---

## Output

data/interim/

bangladesh_smartgrid_clean.parquet

---

## Allowed

✔ Remove duplicate rows (if any)

✔ Handle missing values (if present)

✔ Validate timestamps

✔ Validate data types

✔ Detect impossible values

✔ Detect physically inconsistent records

✔ Preserve operational anomalies

✔ Create cleaning report

---

## Not Allowed

❌ Encoding

❌ Scaling

❌ Normalization

❌ Feature Engineering

❌ Train/Test Split

❌ Feature Selection

❌ Graph Construction

❌ Model Development

---

## Scientific Cleaning Rules

Never remove an observation simply because it is statistically rare.

Only remove or correct data that is

* impossible
* corrupted
* duplicated
* invalid

Rare operational events must be preserved.

---

## Deliverables

data/interim/

bangladesh_smartgrid_clean.parquet

results/phases/phase_03_cleaning/

* cleaning_summary.md

* duplicate_handling_report.csv

* missing_value_handling_report.csv

* outlier_decision_report.md

* data_integrity_report.md

* timestamp_validation_report.md

* cleaning_log.csv

---

## Update

Update this phase document with

* Cleaning Summary

* Records Modified

* Records Removed

* Integrity Checks

* Recommendations for Phase 04

---

## Definition of Done

✔ Dataset cleaned

✔ Integrity validated

✔ No preprocessing applied

✔ Dataset saved

✔ Reports generated

✔ Ready for preprocessing

---

## Execution Record

### Completion Date

2026-06-16

### Cleaning Summary

* Input: `data/raw/bangladesh_smartgrid_raw.csv` (1,850 rows × 45 columns).
* Output: `data/interim/bangladesh_smartgrid_clean.parquet` (1,850 rows × 45 columns).
* The dataset was already complete (0 missing) and free of duplicates, so cleaning was deliberately minimal and conservative — only invalid metadata was corrected and no measurement values were altered.
* Cleaning script (read-only on raw): `scripts/phase_03_cleaning.py`.

### Records Modified

* **`Date` dtype validated and corrected:** `object` (string) → `datetime64[ns]`. Values unchanged.
* **6 invalid `Day of the week` labels corrected** to match the authoritative `Date` (which agrees with `Year` and `Month` in 100% of rows):
  * 2020-02-27 Friday → Thursday
  * 2020-02-28 Saturday → Friday
  * 2021-12-05 Saturday → Sunday
  * 2022-05-31 Wednesday → Tuesday
  * 2023-03-14 Wednesday → Tuesday
  * 2023-12-29 Wednesday → Friday
* No numeric/measurement values were modified (verified byte-identical to raw).

### Records Removed

* **0 rows removed.** No duplicates, no missing values, no impossible values, and no negative measurements were found. Statistically rare but genuine operational events were preserved per the scientific cleaning rule.

### Integrity Checks

* Raw file unchanged (MD5 `28d8594de1b60ba37892e56ae64a8262`, verified before/after).
* Row count preserved: 1,850 → 1,850. Column count preserved: 45 → 45.
* Negatives: 0; implausible temperatures (<5 °C or >50 °C): 0.
* Timestamps: all parseable, unique, strictly monotonic increasing; range 2019-11-21 → 2024-12-30.
* Calendar gaps: 17 missing daily timestamps **documented but NOT filled** (gap filling is preprocessing, out of scope for Phase 03).
* **Physical-consistency anomalies detected and PRESERVED** (not impossible — reporting/metering/grid-transfer differences):
  * Regional `demand` ≠ `supply` + `load`: 74 region-rows
  * Regional `supply` > `demand`: 11 region-rows
  * Evening-peak generation > highest generation: 17 rows; day-peak > highest: 5 rows; minimum > day/eve-peak: 1 each
  * Sub-station-end max demand > generation-end max demand: 16 rows
  * Full details and samples in `results/phases/phase_03_cleaning/data_integrity_report.md`.

### Deliverables Generated

* `data/interim/bangladesh_smartgrid_clean.parquet`
* `results/phases/phase_03_cleaning/cleaning_summary.md`
* `results/phases/phase_03_cleaning/duplicate_handling_report.csv`
* `results/phases/phase_03_cleaning/missing_value_handling_report.csv`
* `results/phases/phase_03_cleaning/outlier_decision_report.md`
* `results/phases/phase_03_cleaning/data_integrity_report.md`
* `results/phases/phase_03_cleaning/timestamp_validation_report.md`
* `results/phases/phase_03_cleaning/cleaning_log.csv`

### Recommendations for Phase 04

* Build a continuous daily calendar index and decide an explicit strategy for the 17 missing days (e.g., reindex + mask) during preprocessing — no imputation was performed here.
* Treat the preserved physical-consistency anomalies as informative signals; consider deriving consistency/diagnostic flags during feature engineering rather than discarding the rows.
* Harmonize numeric dtypes (int64/float64) and apply scaling/normalization in the preprocessing phase (intentionally not done here to keep raw measurements untouched).
* Use the cleaned parquet (`bangladesh_smartgrid_clean.parquet`) as the single source of truth for Phase 04 onward.
* Define the multi-task target formulation (continuous demand regression + sparse load-shedding event handling) before splitting, with a leakage-safe temporal split.

### Status

Ready for preprocessing.
