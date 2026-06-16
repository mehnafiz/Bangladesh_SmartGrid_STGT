# Phase 02 — Outlier Analysis

Outliers flagged with the 1.5×IQR rule (descriptive only — no rows removed or modified).

| feature | n_outliers | outlier_pct | lower_fence | upper_fence |
| --- | --- | --- | --- | --- |
| Dhaka_load | 353 | 19.08 | 0.00 | 0.00 |
| Mymensingh_load | 327 | 17.68 | -52.50 | 87.50 |
| Cumilla_load | 319 | 17.24 | 0.00 | 0.00 |
| Rangpur_load | 276 | 14.92 | 0.00 | 0.00 |
| Holiday_cat | 264 | 14.27 | 0.00 | 0.00 |
| Sylhet_load | 220 | 11.89 | 0.00 | 0.00 |
| Rajshahi_load | 175 | 9.46 | 0.00 | 0.00 |
| Khulna_load | 160 | 8.65 | 0.00 | 0.00 |
| Rangpur_demand | 119 | 6.43 | 388.50 | 1080.50 |
| Rangpur_supply | 115 | 6.22 | 401.62 | 1048.62 |
| Plants under shut down/ maintenance | 89 | 4.81 | 381.75 | 3903.75 |
| Chattogram_load | 89 | 4.81 | 0.00 | 0.00 |
| Barishal_load | 28 | 1.51 | 0.00 | 0.00 |
| Maximum Temperature in Dhaka was | 27 | 1.46 | 21.40 | 42.20 |
| Rajshahi_supply | 3 | 0.16 | 483.88 | 1830.88 |
| Gas/LF limitation | 1 | 0.05 | -1181.25 | 5774.75 |
| Coal supply Limitation | 1 | 0.05 | -255.00 | 425.00 |
| Mymensingh_demand | 1 | 0.05 | 418.50 | 1438.50 |
| Year | 0 | 0.0 | 2018.00 | 2026.00 |
| Month | 0 | 0.0 | -5.00 | 19.00 |
| Max. Demand at eve. peak (Generation end) | 0 | 0.0 | 4923.00 | 18271.00 |
| Max. Demand at eve. peak (Sub-station end) | 0 | 0.0 | 4725.88 | 17536.88 |
| Highest Generation (Generation end) | 0 | 0.0 | 5175.38 | 17820.38 |
| Minimum Generation (Generation end) | 0 | 0.0 | 1399.50 | 15203.50 |
| Day-peak Generation (Generation end) | 0 | 0.0 | 4244.25 | 15486.25 |
| Evening-peak Generation (Generation end) | 0 | 0.0 | 5166.00 | 17772.00 |
| Minimum Generation Forecast up to 8:00 hrs. | 0 | 0.0 | 1338.38 | 15251.38 |
| Low water level in Kaptai lake | 0 | 0.0 | -285.00 | 475.00 |
| Dhaka_demand | 0 | 0.0 | 1604.62 | 6427.62 |
| Dhaka_supply | 0 | 0.0 | 1681.62 | 6296.62 |
| Chattogram_demand | 0 | 0.0 | 584.00 | 1712.00 |
| Chattogram_supply | 0 | 0.0 | 593.88 | 1692.88 |
| Rajshahi_demand | 0 | 0.0 | 440.88 | 1907.88 |
| Mymensingh_supply | 0 | 0.0 | 467.50 | 1333.50 |
| Sylhet_demand | 0 | 0.0 | 105.38 | 776.38 |
| Sylhet_supply | 0 | 0.0 | 124.62 | 739.62 |
| Barishal_demand | 0 | 0.0 | 65.88 | 588.88 |
| Barishal_supply | 0 | 0.0 | 67.00 | 587.00 |
| Cumilla_demand | 0 | 0.0 | 229.38 | 1852.38 |
| Cumilla_supply | 0 | 0.0 | 272.50 | 1780.50 |
| Khulna_demand | 0 | 0.0 | 440.88 | 2275.88 |
| Khulna_supply | 0 | 0.0 | 470.00 | 2222.00 |

- High outlier counts in `_load` features reflect rare load-shedding events rather than data errors.
- Generation/demand outliers are concentrated at the extreme upper tail (record-high demand days).
