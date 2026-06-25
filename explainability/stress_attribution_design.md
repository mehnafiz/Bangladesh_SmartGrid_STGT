# Stress Attribution Design — Phase 12

Generated: 2026-06-24
Status: **FROZEN**

## Level 5 — Operational stress attribution

### Goal (GAP-06)

Identify drivers of high OSI(t+1) forecasts: shedding intensity, reserve margin, limitation stack.

### OSI component reference (Phase 05B — for post-hoc decomposition, not model input)

```
c1 = L_total / D_total           shedding intensity
c2 = 1 - GR / Highest_Gen        reserve margin stress
c3 = TOL / Highest_Gen           limitation stack stress
OSI = mean(minmax(c1), minmax(c2), minmax(c3))
```

### Dual attribution pathway

#### Path A — Model-based (SHAP on stress head)

- Target: OSI_hat(t+1)
- Top SHAP groups expected: G7 (grid), G8 (limitations), G3 (regional load), G11 (shedding flag)
- Report grouped bar chart for high-OSI case studies (top 10% OSI days on validation)

#### Path B — Component-based (ground-truth decomposition)

For same case studies, report actual c1,c2,c3 at t+1 to validate model attributions:

| Component | Physical driver | Expected high-stress signal |
| --- | --- | --- |
| c1 | Load shedding | Mymensingh / sparse _load events (Phase 02) |
| c2 | Low generation reserve | Peak demand days, low GR |
| c3 | Operational limitations | Gas/water/maintenance spikes |

### Stress driver classification (case study labels)

```
driver = argmax( minmax(c1), minmax(c2), minmax(c3) ) at t+1
Compare driver to top SHAP group for consistency
```

### Multi-task link

- Compare stress SHAP (G7,G8) with demand SHAP on same days.
- Joint high OSI + high demand days → operator alert scenario (Phase 07C positioning).

### Outputs

```
results/explainability/stress/stress_shap_grouped_{date}.csv
results/explainability/stress/osi_component_decomposition_{date}.csv
results/explainability/stress/stress_driver_confusion.csv
results/explainability/stress/high_stress_case_study.md
```
