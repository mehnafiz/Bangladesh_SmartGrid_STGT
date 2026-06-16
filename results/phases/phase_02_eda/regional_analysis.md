# Phase 02 — Regional Analysis

Per-region demand/supply/load behaviour across the 9 divisions (graph node candidates).

| region | demand_mean | demand_max | supply_mean | load_mean | load_max | load_nonzero_days | load_nonzero_% | demand_share_% |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dhaka | 3995.1 | 5944 | 3969.4 | 25.96 | 2002 | 353 | 19.08 | 35.65 |
| Khulna | 1379.2 | 2108 | 1367.9 | 11.19 | 400 | 160 | 8.65 | 12.31 |
| Rajshahi | 1189.5 | 1881 | 1178.4 | 11.21 | 356 | 175 | 9.46 | 10.62 |
| Chattogram | 1147.4 | 1633 | 1141.9 | 5.49 | 500 | 89 | 4.81 | 10.24 |
| Cumilla | 1055.3 | 1619 | 1038.4 | 16.68 | 440 | 319 | 17.24 | 9.42 |
| Mymensingh | 937.3 | 1463 | 901.9 | 35.08 | 665 | 520 | 28.11 | 8.36 |
| Rangpur | 724.2 | 1134 | 710.6 | 13.62 | 272 | 276 | 14.92 | 6.46 |
| Sylhet | 446.4 | 722 | 439.5 | 6.99 | 350 | 220 | 11.89 | 3.98 |
| Barishal | 331.5 | 567 | 330.9 | 0.75 | 110 | 28 | 1.51 | 2.96 |

- **Dhaka** dominates national demand (~35.65% of mean total regional demand).
- Load-shedding (`_load`) is non-zero on only a small fraction of days in every region, confirming the Phase 01 sparsity finding.
- Region with most frequent load-shedding: **Mymensingh**.
