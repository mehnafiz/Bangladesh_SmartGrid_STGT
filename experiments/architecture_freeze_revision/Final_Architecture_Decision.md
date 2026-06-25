# Final Architecture Decision

## Purpose

This document records the final architecture decision following Experiments 03, 03A, and 03B.

**Status:** Architecture Freeze **APPROVED** (2026-06-25)

---

## Original Architecture (S1)

**PF-STGT (Parallel-Fusion Spatio-Temporal Graph Transformer)**

| Role | Label |
| --- | --- |
| Architecture ID | **S1** |
| Benchmark ID (Exp02) | B07 |
| Ablation ID (Exp03) | A1 |

Components:

* Hybrid Graph (geographical + correlation)
* Graph Transformer (spatial branch)
* Temporal Transformer (temporal branch)
* Parallel Fusion
* Multi-Task Learning (W20)
* Demand Forecasting Head
* Operational Stress Forecasting Head

**Reference checkpoint:**

`experiments/experiment_01B_multitask_optimization_repair/checkpoints/W20/B07/seed_42/best.pt`

S1 remains the **original Phase 09 design** and historical benchmark. It is **not** the
production model for remaining experiments.

---

## Experimental Findings

### Experiment 03

Ablation studies revealed:

* Single-task forecasting (A4) outperformed full PF-STGT for demand-only accuracy.
* Correlation-only graph (A6) outperformed the hybrid graph on demand.
* Removing the transformer (A3) produced nearly identical demand performance on hybrid graph.

### Experiment 03A

Investigation revealed:

* Multi-task learning enables simultaneous demand and stress forecasting but introduces task interference.
* Transformer attention on S1 was nearly uniform (entropy ratio 0.998).
* Correlation relationships carried most predictive graph signal.
* Geographical edges contributed noise on several regions (especially Dhaka).

### Experiment 03B

Architecture simplification study showed:

* **S2 (correlation-only PF-STGT) achieved the best demand + stress trade-off** (88.65 MW, stress R² 0.745).
* Hybrid graph underperformed correlation-only graph (−4.66 MW vs S1).
* Transformer removal on hybrid graph caused negligible degradation (S3); **stacking both removals hurt badly (S4, +21 MW)**.
* Full S1 complexity is not justified for accuracy; selective graph simplification is.

---

## Final Architecture (S2)

**Correlation-Aware Multi-Task Forecasting Framework**

| Role | Label |
| --- | --- |
| Architecture ID | **S2** |
| Ablation ID (Exp03) | A6 |
| Implementation | `PFSTGT` + `GraphVariant.CORR` |

Components (retained):

* **Correlation Graph** (τ = 0.65; 33 undirected edges)
* Graph Transformer (spatial branch)
* Temporal Transformer (temporal branch)
* Parallel Fusion
* Multi-Task Learning (W20)
* Demand Forecasting Head
* Operational Stress Forecasting Head

Removed vs S1:

* **Geographical graph edges** (hybrid → correlation-only adjacency)

Evaluated but **not** removed in S2:

* Temporal transformer — required for correlation graph performance (Exp03B S4 failure when removed)

**Reference checkpoint:**

`experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt`

Full specification: `final_model_specification.md`

---

## Rationale

The final architecture is selected based on empirical evidence rather than original design assumptions.

Evidence supports:

* Correlation graph contribution (S2 beats S1, p < 0.001)
* Multi-task forecasting capability (stress R² 0.745 vs S1 0.585)
* Retention of spatio-temporal trunk for correlation topology

Evidence does not support:

* Hybrid graph superiority over correlation-only
* Full S1 as the accuracy-optimal proposed model

---

## Final Decision

**S2 is adopted as the final architecture** for Experiment 04, explainability analysis,
manuscript tables/figures, and all remaining evaluation.

| Architecture | Status |
| --- | --- |
| **S1** | Original design / historical benchmark (B07, A1) |
| **S2** | **Final frozen model** (A6) |

---

## Related documents

| Document | Purpose |
| --- | --- |
| `architecture_transition_summary.md` | S1→S2 transition and experiment mapping |
| `final_model_specification.md` | I/O, training, evaluation contract |
| `../experiment_03B_architecture_simplification/final_architecture_decision.md` | Exp03B simplification evidence |
| `../experiment_04_explainability/Experiment_04_Explainability.md` | Next experiment scaffold |

---

## Status

Architecture Freeze: **APPROVED**

Final Model: **S2**

Ready for **Experiment 04 — Explainability Analysis** and manuscript development.
