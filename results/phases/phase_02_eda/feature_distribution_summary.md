# Phase 02 — Feature Distribution Summary

Per-feature distributional shape for all numeric features. Normality assessed with the D'Agostino-Pearson test (no modification of data).

| feature | mean | std | skewness | kurtosis | n_zeros | shape |
| --- | --- | --- | --- | --- | --- | --- |
| Year | 2021.92 | 1.46 | -0.044 | -1.191 | 0 | approx. symmetric |
| Month | 6.65 | 3.50 | -0.037 | -1.236 | 0 | approx. symmetric |
| Max. Demand at eve. peak (Generation end) | 11670.27 | 2083.71 | 0.185 | -0.833 | 0 | approx. symmetric |
| Max. Demand at eve. peak (Sub-station end) | 11167.44 | 2028.45 | 0.115 | -0.840 | 0 | approx. symmetric |
| Highest Generation (Generation end) | 11580.17 | 1946.64 | 0.037 | -0.937 | 0 | approx. symmetric |
| Minimum Generation (Generation end) | 8363.69 | 2056.23 | 0.195 | -0.972 | 0 | approx. symmetric |
| Day-peak Generation (Generation end) | 9870.29 | 1858.05 | 0.038 | -0.677 | 0 | approx. symmetric |
| Evening-peak Generation (Generation end) | 11545.22 | 1937.59 | 0.056 | -0.921 | 0 | approx. symmetric |
| Minimum Generation Forecast up to 8:00 hrs. | 8359.95 | 2093.45 | 0.173 | -0.920 | 0 | approx. symmetric |
| Maximum Temperature in Dhaka was | 31.53 | 4.05 | -0.863 | 0.678 | 0 | left-skewed |
| Gas/LF limitation | 2408.51 | 1114.59 | 0.507 | -0.587 | 0 | right-skewed |
| Coal supply Limitation | 110.12 | 93.65 | 0.266 | -0.943 | 500 | approx. symmetric |
| Low water level in Kaptai lake | 114.76 | 82.55 | -0.445 | -1.500 | 547 | approx. symmetric |
| Plants under shut down/ maintenance | 2189.55 | 869.76 | 1.180 | 3.483 | 0 | right-skewed |
| Dhaka_demand | 3995.09 | 771.11 | -0.015 | -0.787 | 0 | approx. symmetric |
| Dhaka_supply | 3969.45 | 742.98 | -0.084 | -0.801 | 0 | approx. symmetric |
| Dhaka_load | 25.96 | 90.83 | 8.620 | 136.178 | 1497 | right-skewed |
| Chattogram_demand | 1147.42 | 176.26 | -0.117 | -0.760 | 0 | approx. symmetric |
| Chattogram_supply | 1141.90 | 171.32 | -0.159 | -0.778 | 0 | approx. symmetric |
| Chattogram_load | 5.49 | 30.05 | 7.435 | 72.070 | 1761 | right-skewed |
| Rajshahi_demand | 1189.54 | 228.06 | 0.357 | -0.628 | 0 | approx. symmetric |
| Rajshahi_supply | 1178.42 | 218.94 | 0.360 | -0.530 | 0 | approx. symmetric |
| Rajshahi_load | 11.21 | 40.47 | 4.122 | 18.244 | 1675 | right-skewed |
| Mymensingh_demand | 937.28 | 171.99 | 0.178 | -0.608 | 0 | approx. symmetric |
| Mymensingh_supply | 901.86 | 138.32 | -0.148 | -0.826 | 0 | approx. symmetric |
| Mymensingh_load | 35.08 | 69.93 | 2.316 | 6.545 | 1330 | right-skewed |
| Sylhet_demand | 446.42 | 98.72 | 0.316 | -0.992 | 0 | approx. symmetric |
| Sylhet_supply | 439.52 | 91.69 | 0.256 | -1.007 | 0 | approx. symmetric |
| Sylhet_load | 6.99 | 24.30 | 4.832 | 34.004 | 1630 | right-skewed |
| Barishal_demand | 331.52 | 79.99 | 0.369 | -0.796 | 0 | approx. symmetric |
| Barishal_supply | 330.87 | 79.04 | 0.346 | -0.821 | 0 | approx. symmetric |
| Barishal_load | 0.75 | 6.70 | 10.008 | 109.036 | 1822 | right-skewed |
| Rangpur_demand | 724.16 | 178.04 | -0.907 | 1.673 | 0 | left-skewed |
| Rangpur_supply | 710.57 | 165.02 | -1.229 | 2.235 | 0 | left-skewed |
| Rangpur_load | 13.62 | 37.70 | 3.068 | 9.500 | 1574 | right-skewed |
| Cumilla_demand | 1055.34 | 233.14 | 0.026 | -1.153 | 0 | approx. symmetric |
| Cumilla_supply | 1038.37 | 216.01 | -0.039 | -1.133 | 0 | approx. symmetric |
| Cumilla_load | 16.68 | 49.45 | 3.660 | 14.864 | 1531 | right-skewed |
| Khulna_demand | 1379.16 | 269.89 | 0.223 | -1.020 | 0 | approx. symmetric |
| Khulna_supply | 1367.92 | 260.61 | 0.231 | -0.942 | 0 | approx. symmetric |
| Khulna_load | 11.19 | 45.34 | 4.619 | 22.610 | 1690 | right-skewed |
| Holiday_cat | 0.32 | 0.84 | 2.530 | 4.866 | 1586 | right-skewed |
