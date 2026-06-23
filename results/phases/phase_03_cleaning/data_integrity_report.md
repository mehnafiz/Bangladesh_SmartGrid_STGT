# Phase 03 — Data Integrity Report

## Provenance

- Raw source: `data/raw/bangladesh_smartgrid_raw.csv`
- Raw MD5 (before): `28d8594de1b60ba37892e56ae64a8262`
- Raw MD5 (after):  `28d8594de1b60ba37892e56ae64a8262`  → **unchanged**
- Cleaned output: `data/interim/bangladesh_smartgrid_clean.parquet`
- Cleaned MD5: `4255024d735a91a4b53b2edee203d0ca`

## Row / Column accounting

- Rows in: 1850 → Rows out: 1850 (removed: 0)
- Columns in: 45 → Columns out: 45

## Validity checks

- Negative values across numeric columns: 0
- Implausible temperatures (<5°C or >50°C): 0

## Physical-consistency anomalies (PRESERVED — not impossible)

These reflect reporting differences / genuine grid behaviour (e.g., inter-regional transfer, separate metering points) and are NOT statistically-rare events to be removed. They are documented here and retained in the cleaned dataset.

| check | rows affected |
| --- | --- |
| Regional `demand` ≠ `supply` + `load` | 74 |
| Regional `supply` > `demand` | 11 |
| Day-peak generation > highest generation | 5 |
| Evening-peak generation > highest generation | 17 |
| Minimum generation > day-peak generation | 1 |
| Minimum generation > evening-peak generation | 1 |
| Minimum generation > highest generation | 0 |
| Sub-station-end max demand > generation-end max demand | 16 |

## Dtype validation (before → after)

| column | before | after |
| --- | --- | --- |
| Date | object | datetime64[ns] |

All other column dtypes preserved exactly. No measurement values were altered.

## Sample: regional accounting mismatches (first 15 of 74)

| date | region | demand | supply | load | demand-(supply+load) |
| --- | --- | --- | --- | --- | --- |
| 2022-07-26 | Dhaka | 4676 | 4399 | 276 | 1 |
| 2022-10-04 | Dhaka | 4501 | 4167 | 2002 | -1668 |
| 2023-06-16 | Dhaka | 4832 | 4802 | 0 | 30 |
| 2024-05-27 | Dhaka | 5175 | 5157 | 0 | 18 |
| 2024-10-18 | Dhaka | 5016 | 3984 | 0 | 1032 |
| 2022-10-04 | Chattogram | 1331 | 1253 | 500 | -422 |
| 2022-10-24 | Chattogram | 1133 | 1110 | 0 | 23 |
| 2023-05-14 | Chattogram | 1119 | 981 | 0 | 138 |
| 2023-06-06 | Chattogram | 1377 | 1072 | 0 | 305 |
| 2022-10-24 | Rajshahi | 1145 | 1141 | 0 | 4 |
| 2024-05-16 | Rajshahi | 1596 | 1596 | 90 | -90 |
| 2024-07-11 | Rajshahi | 1564 | 1462 | 0 | 102 |
| 2024-09-21 | Rajshahi | 1620 | 1544 | 0 | 76 |
| 2024-11-15 | Rajshahi | 1042 | 1124 | 164 | -246 |
| 2020-06-10 | Mymensingh | 932 | 920 | 350 | -338 |
