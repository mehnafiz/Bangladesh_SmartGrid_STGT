# Phase 16A — Implementation Blueprint

## Objective

Translate the finalized methodology into an implementation-ready engineering blueprint.

No model training.

No experiments.

No results generation.

Only implementation planning.

---

## Inputs

All approved phases.

---

## Required Modules

### Data Pipeline

Responsible for:

- Loading datasets
- Split management
- Data validation

---

### Feature Pipeline

Responsible for:

- Engineered feature generation
- Feature validation
- Feature tensor preparation

---

### Graph Pipeline

Responsible for:

- Hybrid graph loading
- Adjacency matrix management
- Graph tensor construction

---

### Target Pipeline

Responsible for:

- Demand targets
- OSI targets
- Multi-task target generation

---

### Model Pipeline

PF-STGT implementation.

Modules:

- Spatial Encoder
- Temporal Encoder
- Parallel Fusion
- Multi-Task Heads

---

### Training Pipeline

Responsible for:

- Training loop
- Validation loop
- Checkpointing
- Early stopping

---

### Evaluation Pipeline

Responsible for:

- Metrics
- Benchmark comparison
- Statistical testing

---

### Explainability Pipeline

Responsible for:

- SHAP
- Attention visualization
- Permutation importance

---

## Deliverables

implementation/

- implementation_architecture.md

- module_specification.md

- engineering_blueprint.md

- dependency_map.md

results/phases/

phase_16A_implementation_blueprint/

- implementation_summary.md

- implementation_readiness_report.md

---

## Definition of Done

✔ Engineering architecture defined

✔ Module responsibilities defined

✔ Dependency flow defined

✔ Ready for coding

---

## Execution Record

### Completion Date

2025-06-25

### Implementation Blueprint Summary

| Pipeline | ID | Package | Responsibility |
| --- | --- | --- | --- |
| Data | **P1** | `src.data`, `src.datasets` | Load, split, validate, windowed dataset |
| Feature | **P2** | `src.features`, `src.preprocessing` | F_n=9, F_g=17 tensors, leakage guard |
| Graph | **P3** | `src.graph` | Hybrid adjacency, bias, ablation variants |
| Target | **P4** | `src.datasets.targets` | Demand (B,N) + OSI (B,1) at h=1 |
| Model | **P5** | `src.models`, `src.losses` | PF-STGT + baselines + ablation switches |
| Training | **P6** | `src.training` | Loop, early stop, checkpoints, seeds |
| Evaluation | **P7** | `src.evaluation`, `src.metrics` | Tables 1–4, error taxonomy, statistics |
| Explainability | **P8** | `src.explainability`, `src.visualization` | SHAP, attention, permutation, figures |

**45 modules** specified across 8 pipelines.

### PF-STGT Module Structure

```
InputEmbedding → [GraphTransformer ∥ TemporalTransformer] → ParallelFusion
    → DemandHead (9) + StressHead (1)
```

Ablation config switches: A2 (−spatial), A3 (−temporal), A4 (−multi-task), A5 (graph swap), A6 (BiLSTM trunk).

### Sprint Roadmap

1. **Sprint 1** — P1–P4 foundations (dataset + tensors)
2. **Sprint 2** — P5 model core
3. **Sprint 3** — P6 training
4. **Sprint 4** — P7 evaluation
5. **Sprint 5** — P8 explainability

### Deliverables Generated

`implementation/`:

* `implementation_architecture.md`
* `module_specification.md`
* `engineering_blueprint.md`
* `dependency_map.md`
* `pipeline_dependency_edges.csv`
* `module_registry.csv`

`results/phases/phase_16A_implementation_blueprint/`:

* `implementation_summary.md`
* `implementation_readiness_report.md`

Script: `scripts/phase_16A_implementation_blueprint.py`

### Scope Compliance

* Implementation blueprint only.
* **No model code written, no training, no results generated.**
* Locked phase outputs not modified.

### Status

**BLUEPRINT COMPLETE — READY FOR CODING** (Sprint 1: P1–P4 foundations).