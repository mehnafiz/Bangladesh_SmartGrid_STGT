# Architecture Transition Summary

Generated: 2026-06-25  
Status: **ARCHITECTURE FREEZE — APPROVED**

## Purpose

Record the transition from the **original PF-STGT design (S1)** to the **frozen final
model (S2)** following Experiments 03, 03A, and 03B. This document is documentation
only; no results, checkpoints, or datasets were modified.

---

## Architecture lineage

| Label | Name | Role | Experiment mapping | Canonical checkpoint |
| --- | --- | --- | --- | --- |
| **S1** | PF-STGT (W20) | **Original architecture** — hybrid graph, parallel fusion | Exp03 **A1**; Exp03B **S1**; Exp02 **B07** | `experiments/experiment_01B_multitask_optimization_repair/checkpoints/W20/B07/seed_42/best.pt` |
| **S2** | Correlation-Only PF-STGT | **Final architecture** — correlation graph, multi-task W20 | Exp03 **A6**; Exp03B **S2** | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |

Publication name for S2: **Correlation-Aware Multi-Task Forecasting Framework**.

---

## What changed (S1 → S2)

| Component | S1 (original) | S2 (final) | Evidence |
| --- | --- | --- | --- |
| Graph topology | Hybrid (geo + correlation, 24 edges) | Correlation-only (τ=0.65, 33 edges) | Exp03 A6 beats A1 (−4.66 MW); Exp03A geo-noise analysis |
| Graph transformer | Yes | Yes | Retained — spatial encoding still required |
| Temporal transformer | Yes | Yes | Retained — Exp03B S4 shows corr graph needs temporal branch |
| Parallel fusion | Yes | Yes | Unchanged module structure |
| Multi-task (demand + OSI) | Yes (W20) | Yes (W20) | Exp03A confirms joint forecasting value |
| Geographical edges | Included | **Removed** | Exp03 A5 (+4.67 MW vs A1) |

### Evaluated but not adopted

| Variant | Mapping | Outcome | Decision |
| --- | --- | --- | --- |
| No-transformer (hybrid) | Exp03 **A3**; Exp03B **S3** | ΔMAE −0.66 MW vs S1 (not significant) | Optional compute shortcut; **not** frozen |
| Corr + no-transformer | Exp03B **S4** | ΔMAE +21.32 MW vs S1 | **Rejected** — simplifications do not compose |
| Single-task demand-only | Exp03 **A4** | Best demand MAE (86.89 MW) | Retained as analysis baseline; **not** final (no OSI output) |

---

## Performance at freeze (test set, seed 42)

| Model | Demand MAE (MW) | Demand R² | Stress R² | Source |
| --- | --- | --- | --- | --- |
| **S2 (final)** | **88.65** | **0.684** | **0.745** | Exp03B / Exp03 A6 |
| S1 (original) | 93.31 | 0.674 | 0.585 | Exp03B / Exp01B W20 |
| S3 (alt.) | 92.64 | 0.671 | 0.701 | Exp03B |
| S4 (rejected) | 114.63 | 0.362 | 0.747 | Exp03B |

Wilcoxon (S2 vs S1): median daily Δ = −5.43 MW, p < 0.001 (Exp03B).

---

## Experiment timeline

```
Exp01 / Exp01B  →  Train original PF-STGT (S1 / B07 W20)
Exp02           →  Benchmark S1 vs B01–B06 (results frozen)
Exp03           →  Ablation A1–A6; A6 = correlation-only winner
Exp03A          →  Root-cause investigation (task interference, graph, attention)
Exp03B          →  Simplification S1–S4; S2 selected as final
Architecture Freeze → S2 adopted; repository docs updated for Exp04
Exp04 (next)    →  Explainability on S2 checkpoint (no retraining)
```

---

## Repository impact (documentation only)

| Area | Update |
| --- | --- |
| `Final_Architecture_Decision.md` | S2 approved; S1 marked original |
| `final_model_specification.md` | Frozen I/O, training, evaluation contract |
| `architecture/` | S2 graph variant and freeze addendum |
| `evaluation/evaluation_protocol.md` | Proposed model references S2 graph + checkpoint |
| `explainability/explainability_protocol.md` | XAI target checkpoint → S2 |
| `experiments/experiment_04_explainability/` | Experiment 04 scaffold prepared |

**Not modified:** datasets, benchmark CSVs, ablation raw JSON, training code, checkpoints.

---

## Forward policy

All remaining work — **Experiment 04 (explainability)**, manuscript tables/figures, and
robustness analysis — uses **S2** as the reference architecture.

S1 remains cited as the **original Phase 09 design** and historical benchmark (**B07** in
Experiment 02). Ablation comparisons (A1–A6) remain valid as-is; interpret A6 as the
prototype of the frozen final model.
