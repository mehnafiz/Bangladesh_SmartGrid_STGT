# Regional Analysis — Experiment 04

Generated: 2026-07-06

Per-region demand SHAP (10 validation samples) and case-study node mass.

| region     | top_group   | top_group_name              |   top_phi |   mean_case_mass |
|:-----------|:------------|:----------------------------|----------:|-----------------:|
| Dhaka      | G6          | calendar_trend              |  172.228  |        340.356   |
| Rajshahi   | G2          | regional_supply_block       |   64.7868 |        110.317   |
| Khulna     | G10         | national_generation_scalars |   52.5174 |        108.914   |
| Mymensingh | G2          | regional_supply_block       |   43.9618 |         93.8388  |
| Cumilla    | G2          | regional_supply_block       |   58.6517 |         18.0399  |
| Sylhet     | G2          | regional_supply_block       |   39.1368 |          9.18429 |
| Barishal   | G2          | regional_supply_block       |   29.0695 |          6.99067 |
| Chattogram | G2          | regional_supply_block       |   43.163  |          6.20665 |
| Rangpur    | G2          | regional_supply_block       |   44.3778 |          1.9884  |

**Dhaka** dominates attribution mass (340.36) consistent with national demand share (~36%).

Figure: `figures/figure_regional_contribution.png`
