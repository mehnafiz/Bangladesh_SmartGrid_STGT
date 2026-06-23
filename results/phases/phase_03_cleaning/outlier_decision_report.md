# Phase 03 — Outlier Decision Report

## Principle

Per the scientific cleaning rule, **no observation is removed merely because it is statistically rare**. Only impossible / corrupted / duplicated / invalid records are removed or corrected. Genuine rare operational events are preserved.

## Decisions

| category | example | decision | rationale |
| --- | --- | --- | --- |
| Sparse load-shedding (`_load` > 0) | rare non-zero load days | **PRESERVE** | genuine operational events (unmet demand) |
| Record-high demand / generation | upper-tail peak days | **PRESERVE** | real extreme-demand observations |
| Regional `demand` ≠ `supply`+`load` | accounting gaps | **PRESERVE** | not impossible; reporting/metering differences |
| Regional `supply` > `demand` | net import days | **PRESERVE** | plausible in an interconnected grid |
| Generation-ordering anomalies | eve/day-peak > highest | **PRESERVE** | not impossible; reporting differences |
| Negative measurements | none found | n/a | would be impossible → would be flagged |
| Implausible temperatures | none found | n/a | physically impossible range would be flagged |

## Outcome

- Impossible values found: **0** → 0 rows removed on outlier grounds.
- All statistical/operational outliers retained for scientific fidelity.
