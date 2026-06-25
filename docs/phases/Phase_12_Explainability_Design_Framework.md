# Phase 12 — Explainability Design Framework

## Objective

Design a complete explainability framework for PF-STGT.

The framework must support both:

1. Regional Load Forecasting
2. Operational Stress Assessment

---

## Inputs

Phase 07C Research Gap Matrix

Phase 08 Graph Construction

Phase 08.5 Task Definition

Phase 09 STGT Architecture

Phase 10 Training Strategy

---

## Explainability Levels

### Level 1

Global Feature Importance

---

### Level 2

Node-Level Importance

Regional Contribution Analysis

---

### Level 3

Temporal Importance

Time-Step Contribution Analysis

---

### Level 4

Graph Attention Analysis

Inter-Regional Influence Analysis

---

### Level 5

Operational Stress Attribution

Identify drivers of high stress conditions.

---

## Candidate Methods

### SHAP

Feature Attribution

---

### Attention Visualization

Graph Attention

Temporal Attention

---

### Permutation Importance

Global Validation

---

## Required Analysis

Evaluate:

- Interpretability
- Computational Cost
- Literature Support
- Suitability for PF-STGT

Select final explainability toolkit.

---

## Deliverables

explainability/

- xai_strategy.md

- shap_design.md

- attention_analysis_design.md

- node_importance_design.md

- stress_attribution_design.md

- explainability_protocol.md

results/phases/

phase_12_explainability/

- explainability_summary.md

- explainability_decision_report.md

---

## Definition of Done

✔ Explainability framework defined

✔ XAI methods selected

✔ Attention analysis defined

✔ Stress attribution defined

✔ Ready for implementation

---

## Execution Record

### Completion Date

2026-06-24

### Selected Explainability Toolkit

**Hybrid XAI Stack (SHAP-primary + Attention-native + Permutation-validation)**

| Method | Score (/25) | Role |
| --- | --- | --- |
| SHAP (GradientSHAP + grouped coalitions) | 22 | Primary — feature & stress attribution |
| Attention Visualization | 21 | Primary — node, temporal, graph analysis |
| Permutation Importance | 18 | Validation — global sanity check |

Standalone SHAP-only or attention-only toolkits rejected (miss graph/temporal structure or faithful attribution).

### Five Attribution Levels

| Level | Name | Primary method |
| --- | --- | --- |
| L1 | Feature Attribution | SHAP + Permutation |
| L2 | Node Attribution | SHAP node coalitions + spatial attention inflow/outflow |
| L3 | Temporal Attribution | Transformer temporal attention (T=7) |
| L4 | Graph Attention Analysis | Spatial attention + Phase 08 hybrid adjacency overlay |
| L5 | Stress Attribution | SHAP on stress head + OSI c1/c2/c3 decomposition |

### Feature Coalitions (11 groups)

G1–G5 node blocks (demand, supply, load, lags, shares); G6–G11 global (calendar, grid, limitations, weather, generation, shedding indicator). Same-day OSI excluded from inputs (Phase 08.5).

### Case-Study Protocol

20 stratified dates: 5 high OSI, 5 low OSI, 5 peak demand, 5 shedding events.

### Deliverables Generated

`explainability/`:

* `xai_strategy.md`
* `shap_design.md`
* `attention_analysis_design.md`
* `node_importance_design.md`
* `stress_attribution_design.md`
* `explainability_protocol.md`

`results/phases/phase_12_explainability/`:

* `explainability_summary.md`
* `explainability_decision_report.md`
* `xai_method_comparison.csv`
* `feature_coalition_registry.csv`

Script: `scripts/phase_12_explainability_design.py`

### Scope Compliance

* Explainability framework design only.
* **No model implementation or training.**
* Locked phase outputs unchanged.

### Status

Ready for PF-STGT implementation with integrated XAI pipeline (next phase).