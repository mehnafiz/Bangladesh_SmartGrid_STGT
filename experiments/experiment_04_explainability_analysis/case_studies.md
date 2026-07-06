# Case Studies — Experiment 04

Generated: 2026-07-06

**24** cases (20 stratified validation + 4 representative test).

| date       | split      | stratum        |      osi |   demand_total | top_stress_group   | osi_driver    | driver_agreement   |
|:-----------|:-----------|:---------------|---------:|---------------:|:-------------------|:--------------|:-------------------|
| 2023-11-16 | validation | high_osi       | 0.559225 |          10362 | G8                 | c2_reserve    | False              |
| 2024-01-19 | validation | high_osi       | 0.550514 |           9782 | G8                 | c3_limitation | True               |
| 2024-01-06 | validation | high_osi       | 0.493495 |           8225 | G8                 | c3_limitation | True               |
| 2024-01-18 | validation | high_osi       | 0.482827 |           9061 | G8                 | c3_limitation | True               |
| 2023-12-31 | validation | high_osi       | 0.434268 |           9415 | G8                 | c3_limitation | True               |
| 2023-07-25 | validation | low_osi        | 0.184196 |          14651 | G8                 | c2_reserve    | False              |
| 2023-07-28 | validation | low_osi        | 0.187087 |          14463 | G8                 | c2_reserve    | False              |
| 2023-07-29 | validation | low_osi        | 0.187087 |          14463 | G8                 | c2_reserve    | False              |
| 2023-09-28 | validation | low_osi        | 0.199575 |          12861 | G8                 | c2_reserve    | False              |
| 2023-07-27 | validation | low_osi        | 0.201144 |          13676 | G8                 | c2_reserve    | False              |
| 2023-07-24 | validation | peak_demand    | 0.225893 |          14906 | G8                 | c2_reserve    | False              |
| 2023-07-18 | validation | peak_demand    | 0.34251  |          14905 | G7                 | c2_reserve    | True               |
| 2023-07-23 | validation | peak_demand    | 0.249378 |          14893 | G7                 | c2_reserve    | True               |
| 2023-09-16 | validation | peak_demand    | 0.286176 |          14728 | G7                 | c2_reserve    | True               |
| 2023-07-19 | validation | peak_demand    | 0.243343 |          14712 | G7                 | c2_reserve    | True               |
| 2023-07-04 | validation | shedding       | 0.233991 |          12586 | G8                 | c2_reserve    | False              |
| 2023-10-25 | validation | shedding       | 0.2555   |          12116 | G6                 | c2_reserve    | False              |
| 2024-02-08 | validation | shedding       | 0.300647 |           9774 | G8                 | c3_limitation | True               |
| 2024-02-07 | validation | shedding       | 0.310805 |          10263 | G8                 | c2_reserve    | False              |
| 2024-02-05 | validation | shedding       | 0.371622 |          10308 | G8                 | c3_limitation | True               |
| 2024-10-27 | test       | typical_demand | 0.425537 |          13357 | G8                 | c3_limitation | True               |
| 2024-04-28 | test       | high_demand    | 0.343876 |          16418 | G7                 | c2_reserve    | True               |
| 2024-12-19 | test       | low_demand     | 0.486816 |           8866 | G8                 | c3_limitation | True               |
| 2024-09-08 | test       | high_stress    | 0.564551 |          15354 | G8                 | c2_reserve    | False              |

### Representative test days

- **typical_demand** (2024-10-27): OSI=0.426, demand=13357 MW, top stress SHAP=G8, component driver=c3_limitation
- **high_demand** (2024-04-28): OSI=0.344, demand=16418 MW, top stress SHAP=G7, component driver=c2_reserve
- **low_demand** (2024-12-19): OSI=0.487, demand=8866 MW, top stress SHAP=G8, component driver=c3_limitation
- **high_stress** (2024-09-08): OSI=0.565, demand=15354 MW, top stress SHAP=G8, component driver=c2_reserve
