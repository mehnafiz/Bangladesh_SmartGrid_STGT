# Phase 13 — Ablation Studies Design

## Objective

Design a comprehensive ablation framework for PF-STGT.

The goal is to isolate and quantify the contribution of each major component.

---

## Inputs

Phase 08 Graph Construction

Phase 08.5 Task Definition

Phase 09 Architecture

Phase 10 Training Strategy

Phase 11 Hyperparameter Strategy

Phase 12 Explainability Design

---

## Required Ablations

### A1

PF-STGT Full Model

Reference Model

---

### A2

Without Graph Module

Purpose:

Measure spatial contribution.

---

### A3

Without Transformer Module

Purpose:

Measure temporal contribution.

---

### A4

Without Multi-Task Learning

Single-task Demand Forecasting

Purpose:

Measure multitask benefit.

---

### A5

Without Hybrid Graph

Use Geographical Graph Only

Purpose:

Measure hybrid graph value.

---

### A6

Without Explainability Components

Purpose:

Measure interpretability tradeoffs.

---

## Evaluation

Compare:

- MAE
- RMSE
- MAPE
- R²

for all variants.

---

## Deliverables

ablation/

- ablation_plan.md

- ablation_matrix.csv

- component_contribution_framework.md

- statistical_significance_plan.md

results/phases/

phase_13_ablation/

- ablation_summary.md

- ablation_decision_report.md

---

## Definition of Done

✔ Ablation variants defined

✔ Evaluation protocol defined

✔ Component contribution framework defined

✔ Ready for implementation

---

## Execution Record

### Completion Date

2025-06-25

### Ablation Framework Summary

| Category | Variants | Purpose |
| --- | --- | --- |
| Reference | **A1** PF-STGT Full | Baseline for all comparisons |
| Component removal | **A2** −Graph, **A3** −Transformer | Spatial vs temporal contribution |
| Multi-task | **A4** demand-only vs A1 | Multi-task benefit (GAP-02) |
| Hybrid graph | **A5-GEO**, **A5-CORR** vs A1 hybrid | Graph topology value (Phase 08) |
| Explainability | **A6** black-box trunk, **A6-XAI** analysis on A1 | Performance–interpretability tradeoff |

**9 variants** in registry; **9 planned training runs** (A1×3 seeds + 5 ablations×1 seed + 1 supplementary).

### Evaluation Metrics (frozen)

**Demand (all variants):** MAE, RMSE, MAPE, R² — macro over 9 regions + Dhaka separate.

**Stress (A1, A2, A3, A5*, A6):** MAE, RMSE, R² — A4 N/A (no stress head).

### Statistical Testing (frozen)

- Primary: **Wilcoxon signed-rank** on daily macro MAE (~278 test days)
- Correction: **Bonferroni** α_adj = 0.01 for 5 comparisons vs A1
- Effect size: Cohen's d; bootstrap 95% CI for R²
- A6 non-inferiority: ≤5% relative MAE degradation

### Training Protocol (all variants)

Phase 11 best hyperparameters; Phase 10 loss/splits; seed 42 for ablations; seeds 42/123/456 for A1 only.

### Deliverables Generated

`ablation/`:

* `ablation_plan.md`
* `ablation_matrix.csv`
* `component_contribution_framework.md`
* `statistical_significance_plan.md`

`results/phases/phase_13_ablation/`:

* `ablation_summary.md`
* `ablation_decision_report.md`

Script: `scripts/phase_13_ablation_design.py`

### Scope Compliance

* Ablation framework design only.
* **No model implementation, training, or results generated.**
* Locked phase outputs not modified.

### Status

Ready for ablation implementation and training (next phase).