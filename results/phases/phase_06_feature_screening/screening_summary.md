# Phase 06 — Screening Summary

- Completion date: 2026-06-17
- Input: `data/features/` (train / validation / test)
- Engineered features validated: **65**

## Dataset health

- Total rows: **1850** (1,295 + 277 + 278)
- Columns: **146** (consistent across splits)
- Temporal integrity: **PASS**
- Input files unchanged: **True**

## Feature health

- Constant: **0** | Near-zero variance: **0** | Infinite: **0**
- Unexpected missing: **0** | Exact duplicates: **0**
- Passing validation: **65/65**
- Distribution shift flags (val/test): **0/0** (informational)

## Leakage assessment

- **No temporal leakage detected**
- Distribution shifts reflect real temporal drift (demand growth 2019→2024), not preprocessing leakage.

## Scope compliance

- Screening and validation only. No feature selection performed.
- No features removed (including any graph-related). No models trained. No graphs built.
- Locked phase outputs (Phases 01–05B) not modified.

## Recommendations for graph construction

1. Use 9 regional nodes (Dhaka, Chattogram, Rajshahi, Mymensingh, Sylhet, Barishal, Rangpur, Cumilla, Khulna).
2. Node features: regional demand/supply/load + engineered lags, shares, load intensity from validated set.
3. Implement Batch 3 graph candidates from blueprint: rolling_demand_corr_90d, geographic adjacency, pairwise_demand_gradient.
4. Handle first 7 train rows (warm-up NaNs) via masking or drop before sequence windowing.
5. Preserve chronological split boundaries when constructing dynamic edge weights.

## Deliverables

- `feature_validation_report.md`
- `feature_quality_summary.csv`
- `constant_feature_report.csv`
- `duplicate_feature_report.csv`
- `missing_feature_report.csv`
- `leakage_validation_report.md`
- `dataset_validation_report.md`
- `screening_summary.md`
