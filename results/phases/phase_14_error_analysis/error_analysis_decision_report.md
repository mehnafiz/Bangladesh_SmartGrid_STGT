# Error Analysis Decision Report — Phase 14

Generated: 2026-06-24

## Design rationale

### Why six error categories?

PF-STGT is a multi-task spatio-temporal graph model (Phase 09). Failures can arise
in spatial coupling (E2/E6), temporal seasonality (E5), stress regime (E3), or operational
extremes (E4). E1 provides the global baseline; root-cause triangulation explains *why*.

### Regional analysis (E2)

Phase 10 mandates Dhaka separate reporting. Phase 08 hybrid graph gives heterogeneous
node degrees (Dhaka=8, periphery=4). Regional framework links to E6 connectivity tiers.

### Stress analysis (E3)

Continuous OSI (Phase 08.5) with train-frozen tertiles avoids validation leakage.
Test-period shift to 60% High stress requires regime-stratified metrics, not pooled MAE alone.

### Extreme events (E4)

Phase 02: shedding sparse in train (~18%) but dense in test (~63%). Extreme-event
framework uses train-fitted thresholds applied to t+1 labels — critical for operator relevance.

### Temporal analysis (E5)

Phase 02 identified month-9 peak and multi-year trend. Weekly/holiday bins use Phase 01
calendar fields. Low-confidence flag for bins with n<15.

### Root-cause analysis

Phase 12 hybrid XAI stack is post-hoc by design. Phase 14 consumes SHAP, attention,
and stress decomposition outputs — no new XAI methods introduced.
Triangulation prevents over-interpreting any single attribution method (Jain & Wallace 2019).

## Category registry

| error_id   | category         | name                              | priority   |
|:-----------|:-----------------|:----------------------------------|:-----------|
| E1         | overall_forecast | Overall Forecast Error            | Required   |
| E2         | regional         | Regional Error Analysis           | Required   |
| E3         | stress           | Operational Stress Error Analysis | Required   |
| E4         | extreme_event    | Extreme Event Analysis            | Required   |
| E5         | temporal         | Temporal Error Analysis           | Required   |
| E6         | graph            | Graph Error Analysis              | Required   |

## Graph connectivity groups (E6)

- **High:** Dhaka, Cumilla, Mymensingh (degree ≥ 6)
- **Low:** Barishal, Rangpur, Sylhet (degree ≤ 4)

## Expected findings (hypotheses — to validate post-training)

| Category | Hypothesis |
| --- | --- |
| E2 | Dhaka largest MW error; periphery highest MAPE |
| E3 | Largest OSI error in High-stress regime |
| E4 | Shedding-day demand MAE > non-shedding |
| E5 | Month-9 MAE > annual mean |
| E6 | Low-connectivity regions benefit most from graph module |
| RC | RC-L1 and RC-G1 dominate on test (shedding + reserve stress) |

## Dependencies

| Prerequisite phase | Required artefact |
| --- | --- |
| Phase 10 | Trained PF-STGT + test predictions |
| Phase 12 | SHAP/attention export pipeline |
| Phase 13 | A2/A3 ablation predictions for RC-S1/RC-T1 validation |
