# Phase 09 — STGT Architecture Design

## Objective

Design the complete architecture of the proposed Explainable Multi-Task Spatio-Temporal Graph Transformer (STGT).

The architecture must be supported by:

* Literature evidence
* Research gap analysis
* Graph construction outputs
* Task definitions

---

## Inputs

Graph Construction Outputs

Task & Target Definition Outputs

Research Gap Outputs

---

## Architecture Components

### Input Layer

Define:

* Node features
* Input window
* Feature dimensions

---

### Spatial Module

Evaluate:

* GCN
* GAT
* Graph Transformer

Select the most appropriate spatial encoder.

Provide justification.

---

### Temporal Module

Evaluate:

* Temporal Attention
* Transformer Encoder
* Temporal Transformer

Select the most appropriate temporal encoder.

Provide justification.

---

### Fusion Strategy

Evaluate:

1. Spatial → Temporal

2. Temporal → Spatial

3. Parallel Fusion

Select the strongest design.

Provide justification.

---

### Shared Representation

Define latent representation.

---

### Multi-Task Heads

Task 1

Regional Load Forecasting

Output:

9 regional demand predictions

---

Task 2

Operational Stress Assessment

Output:

Continuous OSI prediction

---

### Explainability Readiness

Specify:

* SHAP compatibility
* Attention visualization
* Feature attribution compatibility

---

## Deliverables

architecture/

* architecture_overview.md

* architecture_components.md

* architecture_diagram.md

* input_output_specification.md

* module_rationale.md

* loss_function_design.md

* explainability_design.md

results/phases/

phase_09_architecture/

* architecture_summary.md

* architecture_validation_report.md

* design_decision_rationale.md

---

## Definition of Done

✔ Architecture defined

✔ Modules justified

✔ Inputs defined

✔ Outputs defined

✔ Explainability integrated

✔ Ready for implementation

---

## Execution Record

### Completion Date

2026-06-24

### Selected Architecture

**PF-STGT** — Parallel-Fusion Spatio-Temporal Graph Transformer (score 27/27 vs ARCH-A 14, ARCH-B 18)

| Module | Selection | Score |
| --- | --- | --- |
| Spatial | **Graph Transformer** (adjacency-biased attention) | 25/25 |
| Temporal | **Transformer Encoder** (multi-layer, shared across nodes) | 25/25 |
| Fusion | **Parallel Fusion** (gated spatial ∥ temporal) | 23/25 |

### I/O Specification

| Item | Value |
| --- | --- |
| Input window T | 7 days |
| Nodes N | 9 |
| Node features F_n | 9 per node (demand/supply/load + 6 engineered) |
| Global features F_g | 17 (calendar, grid, limitations, national gen) |
| Horizon h | 1 day (Phase 08.5) |
| Task 1 output | 9 × regional demand (MW) |
| Task 2 output | 1 × OSI ∈ [0,1] |
| d_model | 128, heads=4, L_s=2, L_t=2 |

### Multi-Task Loss (design)

```
L_total = λ1 · Huber(D_hat, D) + λ2 · MSE(OSI_hat, OSI)     (λ1=1.0, λ2=0.5 default)
```

### Explainability Hooks

- Spatial + temporal attention map export
- SHAP feature-group coalitions (regional, calendar, limitation stack, grid)
- Separate node-level (Task 1) and graph-level (Task 2) attribution paths

### Research Gap Alignment

| Gap | PF-STGT response |
| --- | --- |
| GAP-04 | Graph Transformer + Transformer Encoder |
| GAP-05 | Attention export + SHAP compatibility |
| GAP-02 | Shared H_shared, dual task heads |
| GAP-06 | StressHead + limitation-aware global inputs |
| GAP-07 | F_g co-design with Phase 05B covariates |

### Deliverables Generated

`architecture/`:

* `architecture_overview.md`
* `architecture_components.md`
* `architecture_diagram.md`
* `input_output_specification.md`
* `module_rationale.md`
* `loss_function_design.md`
* `explainability_design.md`

`results/phases/phase_09_architecture/`:

* `architecture_summary.md`
* `architecture_validation_report.md`
* `design_decision_rationale.md`

Script: `scripts/phase_09_stgt_architecture_design.py`

### Scope Compliance

* Architecture design only — **no implementation or training**.
* Locked phase outputs unchanged (`train_features.parquet` MD5: `b8b3bda95d0fd6cc65f4910d85a98e16`; `adjacency_matrix.csv` MD5: `dacb7ac3a827d00a4b61ea9400e75686`).

### Status

Ready for implementation phase.
