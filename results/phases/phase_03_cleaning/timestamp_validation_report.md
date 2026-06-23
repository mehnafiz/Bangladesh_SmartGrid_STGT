# Phase 03 — Timestamp Validation Report

- Rows: 1850
- Unparseable dates: 0
- Duplicate dates: 0
- Monotonic increasing: True
- Date range: 2019-11-21 → 2024-12-30
- Calendar span: 1867 days; records present: 1850
- Missing calendar days (gaps): 17 (documented only — gap filling is deferred to preprocessing, NOT done here)
- Year vs Date mismatches: 0
- Month vs Date mismatches: 0
- Weekday-label vs Date mismatches (before cleaning): 6

## Dtype correction

- `Date` converted from `object` (string) to `datetime64[ns]`. Values unchanged.

## Corrected weekday labels

| row | date | old_label | corrected_label |
| --- | --- | --- | --- |
| 97 | 2020-02-27 | Friday | Thursday |
| 98 | 2020-02-28 | Saturday | Friday |
| 742 | 2021-12-05 | Saturday | Sunday |
| 919 | 2022-05-31 | Wednesday | Tuesday |
| 1205 | 2023-03-14 | Wednesday | Tuesday |
| 1490 | 2023-12-29 | Wednesday | Friday |

## Missing calendar days (preserved as gaps)

2020-01-02, 2020-03-27, 2020-03-28, 2023-01-23, 2023-03-15, 2023-04-01, 2023-05-08, 2023-05-16, 2023-07-05, 2024-06-03, 2024-07-01, 2024-07-18, 2024-07-19, 2024-07-20, 2024-07-21, 2024-07-22, 2024-07-23
