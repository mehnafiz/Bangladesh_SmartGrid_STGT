# Phase 01 — Data Audit Report

## 1. Provenance & Integrity

- Source file: `data/raw/bangladesh_smartgrid_raw.csv`
- File size: 388,569 bytes
- MD5 (before audit): `28d8594de1b60ba37892e56ae64a8262`
- MD5 (after audit): `28d8594de1b60ba37892e56ae64a8262`
- Integrity: **UNCHANGED — dataset not modified**

## 2. Shape

- Rows: **1,850**
- Columns: **45**
- Numeric columns: 42
- Non-numeric columns: 3

## 3. Missing Values

- Total missing cells: 0 (0.0% of all cells)
- Columns with any missing values: 0

- No missing values detected in any column.

## 4. Duplicates

- Full duplicate rows: 0
- Duplicate `Date` values: 0

## 5. Spatial Structure (Regions)

- Regional divisions detected: 9
- Regions: Barishal, Chattogram, Cumilla, Dhaka, Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet
- Each region carries `_demand`, `_supply`, and `_load` columns (node-level signals suitable for a spatio-temporal graph).

## 6. Candidate Targets

- 35 candidate target columns detected (demand / supply / load / generation).
- See `target_analysis.csv` for per-target statistics.

## 7. Generated Deliverables

- `dataset_summary.csv`
- `feature_dictionary.csv`
- `data_types_report.csv`
- `missing_value_report.csv`
- `duplicate_report.csv`
- `target_analysis.csv`
- `basic_statistics.csv`
- `temporal_structure_report.md`
- `data_audit_report.md`

## 8. Scope Compliance

- Read-only audit. No rows/columns removed, no values modified, no encoding, normalization, imputation, feature engineering, graph building, or modelling performed.

