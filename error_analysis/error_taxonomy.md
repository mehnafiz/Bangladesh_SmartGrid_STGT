# Error Taxonomy — Phase 14

Generated: 2026-06-24
Status: **FROZEN**

## Objective

Classify PF-STGT prediction failures into six orthogonal error categories (E1–E6)
for systematic post-training analysis on the **test split only** (278 days).

## Reference model and inputs

- **Primary model:** B07 PF-STGT (A1 seed 42) (Phase 09/10/11)
- **Residual store:** `results/error_analysis/residuals_test.parquet` (implementation phase)
- **Splits:** Phase 04 chronological 70/15/15 — analysis locked to test rows
- **Tasks:** Task 1 `{Region}_demand` h=1; Task 2 continuous OSI (Phase 08.5)

## Error category registry

| error_id   | name                              | scope                                         | primary_metrics                                    | segmentation                                                                                             | priority   |
|:-----------|:----------------------------------|:----------------------------------------------|:---------------------------------------------------|:---------------------------------------------------------------------------------------------------------|:-----------|
| E1         | Overall Forecast Error            | Macro demand + national OSI on test split     | MAE, RMSE, MAPE, R² (Phase 10)                     | None — global baseline                                                                                   | Required   |
| E2         | Regional Error Analysis           | Per-node demand residuals for 9 divisions     | MAE, RMSE, MAPE, R² per region; Dhaka separate     | 9 regions + macro aggregate                                                                              | Required   |
| E3         | Operational Stress Error Analysis | OSI(t+1) residuals by stress regime           | MAE, RMSE, R²; bias; calibration                   | Low / Medium / High (train tertiles frozen)                                                              | Required   |
| E4         | Extreme Event Analysis            | Demand spikes, supply drops, shedding periods | Event recall, peak MAE, false-alarm rate           | 3 event types × severity tiers                                                                           | Required   |
| E5         | Temporal Error Analysis           | Weekly, seasonal, holiday error patterns      | MAE by DOW, month, holiday flag; seasonality ratio | Weekday/weekend; month 1–12; holiday vs non-holiday                                                      | Required   |
| E6         | Graph Error Analysis              | Error vs hybrid-graph node connectivity       | MAE vs degree; attention–error correlation         | High-connectivity ['Dhaka', 'Cumilla', 'Mymensingh']; Low-connectivity ['Barishal', 'Rangpur', 'Sylhet'] | Required   |

---

## E1 — Overall Forecast Error

Baseline error profile before segmentation.

```
residual_demand_r(d) = D_r(d) − D̂_r(d)     ∀ r ∈ {9 regions}, d ∈ test
residual_osi(d)      = OSI(d) − OSI_hat(d)
```

Report Phase 10 metrics + residual distribution (mean, std, skew, p95 |error|).
Compare PF-STGT vs T-GCN and persistence on same test windows.

---

## E2 — Regional Error Analysis

See `regional_error_framework.md`.

Key hypothesis: Dhaka (~35.7% national share, Phase 02) drives macro error;
peripheral low-degree nodes may show higher MAPE despite lower MW error.

---

## E3 — Operational Stress Error Analysis

See `stress_error_framework.md`.

Stratify by **train-frozen OSI tertiles** (Low/Medium/High) applied to test labels.
Test split stress shift: ~16% Low / 24% Medium / 60% High (Phase 08.5 distribution).

---

## E4 — Extreme Event Analysis

See `extreme_event_framework.md`.

Three event classes aligned with Bangladesh grid operations:

1. **Demand spikes** — national or regional demand > train μ + 2σ
2. **Supply drops** — `generation_reserve` or `Highest Generation` drop > train p10
3. **Load shedding** — `any_regional_shedding=1` or regional `_load > 0`

---

## E5 — Temporal Error Analysis

### Segmentation axes

| Axis | Field | Bins | Rationale |
| --- | --- | --- | --- |
| Weekly | `Day of the week` / Date | Mon–Sun | Phase 02 weekday load shape |
| Seasonal | `Month` / Date | 1–12 | Month-9 summer peak (Phase 02) |
| Holiday | `Holiday_cat` / `Holiday name` | holiday vs non-holiday | Calendar exogenous (Phase 01) |

### Metrics per bin

```
MAE_bin   = mean(|residual|) over days in bin
n_bin     = sample count (flag bins with n < 15 as low-confidence)
seasonality_ratio = MAE_month9 / MAE_month_overall
```

### Expected failure modes

- **Month 9 (Apr–Oct peak):** cooling-driven demand; temperature_anomaly_month sensitivity
- **Fridays / pre-holiday:** calendar shift not fully captured by T=7 window
- **Post-2023 test period:** upward demand trend extrapolation error

### Outputs

```
results/error_analysis/temporal/mae_by_dow.csv
results/error_analysis/temporal/mae_by_month.csv
results/error_analysis/temporal/mae_holiday_vs_nonholiday.csv
results/error_analysis/temporal/temporal_error_heatmap.png
```

---

## E6 — Graph Error Analysis

### Connectivity groups (Phase 08 hybrid graph)

| Group | Regions | Mean degree |
| --- | --- | --- |
| High-connectivity | Dhaka, Cumilla, Mymensingh | ≥ 6 |
| Mid-connectivity | Chattogram, Khulna, Rajshahi | 5 |
| Low-connectivity | Barishal, Rangpur, Sylhet | ≤ 4 |

### Analysis protocol

1. Compute per-region test MAE; correlate with node degree (Spearman ρ).
2. Compare macro MAE on high- vs low-connectivity subsets.
3. Overlay spatial attention mass on hybrid edges for high-error days.
4. Cross-reference Phase 13 A2 (−Graph) degradation by connectivity group.

### Hypotheses

- Hub node **Dhaka** (degree 8): lower MAPE via rich neighbor signal; errors from national trend.
- **Low-connectivity** nodes (Barishal, Rangpur, Sylhet): higher MAPE; graph ablation hurts more.
- Non-geographic hybrid edges (Cumilla–Khulna, Cumilla–Sylhet): attention should activate on coupled errors.

### Outputs

```
results/error_analysis/graph/mae_vs_degree.csv
results/error_analysis/graph/high_vs_low_connectivity_summary.csv
results/error_analysis/graph/attention_error_cases.csv
```

## Cross-category interaction matrix

| Interaction | Analysis |
| --- | --- |
| E2 × E5 | Regional MAE heatmap by month |
| E3 × E4 | OSI error on shedding days |
| E4 × E5 | Extreme demand spikes by season |
| E6 × E2 | Degree vs regional MAPE |
| E3 × E6 | Stress error on high- vs low-connectivity aggregate load |

## Implementation artefact index

```
results/error_analysis/error_taxonomy_index.csv
results/error_analysis/residuals_test.parquet
results/error_analysis/error_segment_summary.csv
```
