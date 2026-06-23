# Phase 05A — Novelty Analysis

## Summary

- Total inventory entries: **114**
- Existing (Phase 04 baseline groups): **10**
- Proposed engineered features: **104**
- Novel research features: **25**
- Generic / literature-standard features: **79**

## Novel Features (research contribution candidates)

These features are specifically motivated by Bangladesh grid characteristics and the multi-task STGT framework:

| feature | category | priority | motivation |
| --- | --- | --- | --- |
| gap_days_since_previous_observation | Temporal | High | 17 calendar gaps exist (Phase 03); lag windows must respect irregular spacing. |
| demand_lag_7_Dhaka | Temporal | High | Weekly periodicity in daily load profiles. |
| demand_lag_7_Chattogram | Temporal | High | Weekly periodicity in daily load profiles. |
| demand_lag_7_Rajshahi | Temporal | High | Weekly periodicity in daily load profiles. |
| demand_lag_7_Mymensingh | Temporal | High | Weekly periodicity in daily load profiles. |
| demand_lag_7_Sylhet | Temporal | High | Weekly periodicity in daily load profiles. |
| demand_lag_7_Barishal | Temporal | High | Weekly periodicity in daily load profiles. |
| demand_lag_7_Rangpur | Temporal | High | Weekly periodicity in daily load profiles. |
| demand_lag_7_Cumilla | Temporal | High | Weekly periodicity in daily load profiles. |
| demand_lag_7_Khulna | Temporal | High | Weekly periodicity in daily load profiles. |
| regional_accounting_residual_Dhaka | Regional | Medium | Phase 03 preserved 74 region-rows with identity mismatch — metering/reporting si… |
| regional_accounting_residual_Chattogram | Regional | Medium | Phase 03 preserved 74 region-rows with identity mismatch — metering/reporting si… |
| regional_accounting_residual_Rajshahi | Regional | Medium | Phase 03 preserved 74 region-rows with identity mismatch — metering/reporting si… |
| regional_accounting_residual_Mymensingh | Regional | Medium | Phase 03 preserved 74 region-rows with identity mismatch — metering/reporting si… |
| regional_accounting_residual_Sylhet | Regional | Medium | Phase 03 preserved 74 region-rows with identity mismatch — metering/reporting si… |
| regional_accounting_residual_Barishal | Regional | Medium | Phase 03 preserved 74 region-rows with identity mismatch — metering/reporting si… |
| regional_accounting_residual_Rangpur | Regional | Medium | Phase 03 preserved 74 region-rows with identity mismatch — metering/reporting si… |
| regional_accounting_residual_Cumilla | Regional | Medium | Phase 03 preserved 74 region-rows with identity mismatch — metering/reporting si… |
| regional_accounting_residual_Khulna | Regional | Medium | Phase 03 preserved 74 region-rows with identity mismatch — metering/reporting si… |
| substation_generation_spread | Grid | Medium | Transmission/distribution losses and metering differences (16 anomalous rows in … |
| forecast_min_generation_error | Grid | Medium | Dispatch forecast accuracy; under-forecast may precede stress. |
| operational_stress_index | Operational | High | Composite stress aligned with multi-task objective (shedding + operational asses… |
| shedding_region_count | Operational | Medium | Spatial extent of load-shedding events. |
| spatial_demand_dispersion | Graph Candidate | Medium | Heterogeneity of load across divisions; high when spatially uneven stress. |
| pairwise_demand_gradient | Graph Candidate | Low | Instantaneous spatial load imbalance between neighbours. |

## Generic Features (baseline comparability)

Standard temporal, statistical, and grid features ensure comparability with prior load-forecasting literature and ablation against the novel components.

## Recommended ablation in later phases

- Remove `operational_stress_index` to test composite vs decomposed constraints.
- Remove gap-aware lags (`gap_days_since_previous_observation`, `demand_lag_7`) to quantify calendar-gap handling benefit.
- Remove `regional_accounting_residual` to test Phase 03 anomaly preservation value.
