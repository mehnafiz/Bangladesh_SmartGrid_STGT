# Phase 06 — Dataset Validation Report

## Split summary

| split | rows | date start | date end | monotonic |
| --- | --- | --- | --- | --- |
| train | 1295 | 2019-11-21 | 2023-06-15 | True |
| validation | 277 | 2023-06-16 | 2024-03-19 | True |
| test | 278 | 2024-03-20 | 2024-12-30 | True |
| **total** | **1850** | | | |

## Schema consistency

- Columns per split: **146**
- Column names identical across splits: **True**
- Date dtype: `datetime64[ns]`
- Baseline + engineered: 81 processed + 65 engineered = 146

## Checklist

| # | check | pass |
| --- | --- | --- |
| 1 | Row counts sum to 1,850 | **True** |
| 2 | Temporal ordering preserved | **True** |
| 3 | Non-overlapping chronological splits | **True** |
| 4 | Schema consistent across splits | **True** |
| 5 | Input feature files unmodified | **True** |

## Verdict

**Dataset integrity: PASS**
