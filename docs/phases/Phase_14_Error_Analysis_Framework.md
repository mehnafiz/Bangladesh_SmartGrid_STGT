# Phase 14 — Error Analysis Framework

## Objective

Design a comprehensive framework for analyzing PF-STGT prediction errors.

The framework must identify:

- Temporal failures
- Regional failures
- Operational stress failures
- Extreme event failures

---

## Inputs

Phase 08 Graph Construction

Phase 08.5 Task Definition

Phase 09 Architecture

Phase 10 Training Strategy

Phase 12 Explainability Design

Phase 13 Ablation Design

---

## Error Categories

### E1

Overall Forecast Error

---

### E2

Regional Error Analysis

Evaluate:

- Dhaka
- Chattogram
- Cumilla
- Khulna
- Rajshahi
- Rangpur
- Sylhet
- Barishal
- Mymensingh

---

### E3

Operational Stress Error Analysis

Evaluate:

- Low Stress
- Medium Stress
- High Stress

---

### E4

Extreme Event Analysis

Evaluate:

- Demand spikes
- Supply drops
- Load shedding periods

---

### E5

Temporal Error Analysis

Evaluate:

- Weekly patterns
- Seasonal patterns
- Holiday periods

---

### E6

Graph Error Analysis

Evaluate:

- High-connectivity regions
- Low-connectivity regions

---

## Root Cause Analysis

Define methodology for:

- Feature attribution review
- Attention review
- Stress attribution review

---

## Deliverables

error_analysis/

- error_taxonomy.md

- regional_error_framework.md

- stress_error_framework.md

- extreme_event_framework.md

- root_cause_analysis_protocol.md

results/phases/

phase_14_error_analysis/

- error_analysis_summary.md

- error_analysis_decision_report.md

---

## Definition of Done

✔ Error taxonomy defined

✔ Regional analysis defined

✔ Stress analysis defined

✔ Extreme-event analysis defined

✔ Root-cause analysis defined

---

## Execution Record

### Completion Date

2025-06-25

### Error Analysis Framework Summary

| Category | ID | Focus |
| --- | --- | --- |
| Overall | **E1** | Macro demand + OSI baseline on test split |
| Regional | **E2** | 9-division per-node MAE/MAPE; Dhaka separate |
| Stress | **E3** | Low / Medium / High OSI regimes (train-frozen tertiles) |
| Extreme events | **E4** | Demand spikes, supply drops, shedding periods |
| Temporal | **E5** | Weekly, seasonal (month 9 peak), holiday patterns |
| Graph | **E6** | High vs low connectivity (Dhaka/Cumilla vs Barishal/Rangpur/Sylhet) |

**Primary model for analysis:** PF-STGT (A1 seed 42) on 278 test days.

### Root-Cause Pathways (Phase 12 integration)

1. **Feature attribution review** — SHAP grouped coalitions + Permutation (L1)
2. **Attention review** — spatial + temporal attention export (L3–L4)
3. **Stress attribution review** — OSI c1/c2/c3 decomposition vs SHAP (L5)

**Triangulation rule:** ≥2 of 3 pathways agree → assign RC label (RC-T1 through RC-U1).

### Deliverables Generated

`error_analysis/`:

* `error_taxonomy.md`
* `error_taxonomy_index.csv`
* `regional_error_framework.md`
* `stress_error_framework.md`
* `extreme_event_framework.md`
* `root_cause_analysis_protocol.md`

`results/phases/phase_14_error_analysis/`:

* `error_analysis_summary.md`
* `error_analysis_decision_report.md`

Script: `scripts/phase_14_error_analysis_design.py`

### Scope Compliance

* Error analysis framework design only.
* **No model implementation, training, or residual files generated.**
* Locked phase outputs not modified.

### Status

Ready for post-training error analysis execution (after model training phase).