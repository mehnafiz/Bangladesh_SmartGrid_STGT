# Extreme Event Framework — Phase 14

Generated: 2026-06-24
Status: **FROZEN**

## Scope (E4)

Evaluate PF-STGT under operational extremes: demand spikes, supply drops, and load shedding.
Aligned with Phase 07B resilience literature and Phase 02 sparse `_load` signal.

## Event taxonomy

### Event Type 1 — Demand spikes

| Tier | Rule (train-fitted thresholds) |
| --- | --- |
| Regional spike | `{Region}_demand(t+1) > μ_r,train + 2σ_r,train` |
| National spike | `total_regional_demand(t+1) > μ_nat,train + 2σ_nat,train` |
| Severe | > μ + 3σ or top 5% of train demand |

### Event Type 2 — Supply drops

| Tier | Rule |
| --- | --- |
| Reserve stress | `generation_reserve(t+1) < Q10_train` |
| Generation drop | `Highest Generation(t+1) < Q10_train` |
| Compound | reserve stress AND demand spike |

### Event Type 3 — Load shedding periods

| Tier | Rule |
| --- | --- |
| Any shedding | `any_regional_shedding(t+1) = 1` (test: ~63% days) |
| Regional shed | `{Region}_load(t+1) > 0` |
| Multi-region | `shedding_region_count(t+1) ≥ 2` |

All thresholds computed on **train split only**; applied to test labels at t+1.

## Evaluation metrics per event type

### Demand task

| Metric | Definition |
| --- | --- |
| Event MAE | mean(|e_r|) on event days only |
| Event MAPE | mean(APE_r) on event days |
| Spike recall | fraction of spike days with |e_r| < 1.5 × median |e| |
| Peak under-prediction rate | P(D̂ < D | spike day) |

### Stress task

| Metric | Definition |
| --- | --- |
| High-OSI event MAE | MAE on OSI > train Q90 |
| Shedding-day OSI MAE | MAE when any_regional_shedding=1 |
| Missed stress alert | OSI > Q2 but OSI_hat < Q2 |

## Severity stratification

```
severity_score = rank(normalize(|Δdemand|) + normalize(OSI) + shedding_flag)
Report metrics for severity terciles: Mild / Moderate / Severe
```

## Benchmark comparison

| Comparison | Purpose |
| --- | --- |
| PF-STGT vs T-GCN | Graph model on shedding days |
| PF-STGT vs LSTM | Temporal-only on demand spikes |
| PF-STGT vs persistence | Stress on high-OSI events |

## Case study protocol (top-K events)

Select **K=10** worst macro-error days on test; for each document:

1. Event type(s) triggered
2. Per-region error contribution
3. OSI residual
4. Phase 12 XAI summary (SHAP + attention)
5. Root-cause label (see `root_cause_analysis_protocol.md`)

## Visualisation spec

| Figure | Content |
| --- | --- |
| `extreme_event_mae_comparison.png` | MAE: normal vs event days |
| `demand_spike_scatter.png` | Actual vs predicted on spike days |
| `shedding_timeline.png` | Shedding flag vs |OSI − OSI_hat| |

## Output artefacts

```
results/error_analysis/extreme/event_definitions.csv
results/error_analysis/extreme/event_metrics_by_type.csv
results/error_analysis/extreme/top10_worst_days.csv
results/error_analysis/extreme/extreme_event_case_studies.md
```

## Acceptance criteria

- All three event types evaluated with train-frozen thresholds.
- Shedding-period analysis mandatory (operational relevance for Bangladesh grid).
- Top-10 worst-day case studies linked to root-cause protocol.
