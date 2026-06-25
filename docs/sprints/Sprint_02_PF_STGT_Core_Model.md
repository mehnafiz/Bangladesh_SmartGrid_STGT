# Sprint 02 — PF-STGT Core Model

## Objective

Implement the PF-STGT architecture.

This sprint implements:

- Graph Transformer
- Temporal Transformer
- Parallel Fusion
- Demand Head
- Stress Head

No training.

No explainability.

No evaluation.

---

## Input Contract

X_temporal_node

Shape:

(7, 9, 9)

---

X_temporal_global

Shape:

(7, 17)

---

X_graph

Shape:

(9, 9)

---

## Architecture

Graph Transformer Branch

↓

Temporal Transformer Branch

↓

Parallel Fusion

↓

Shared Representation

↓

Demand Head

↓

Stress Head

---

## Output Contract

Demand Output

Shape:

(9,)

---

OSI Output

Shape:

(1,)

---

## Required Modules

models/

graph_transformer.py

temporal_transformer.py

fusion.py

heads.py

pf_stgt.py

---

## Testing Requirements

Forward Pass Test

Shape Validation Test

Parameter Count Report

Dummy Batch Test

---

## Definition of Done

✔ PF-STGT implemented

✔ Forward pass works

✔ Output shapes validated

✔ Unit tests pass

✔ Ready for training

---

## Execution Record

### Completion Date

2025-06-25

### Modules Implemented

| Module | File |
| --- | --- |
| Graph Transformer | `src/models/graph_transformer.py` |
| Temporal Transformer | `src/models/temporal_transformer.py` |
| Parallel Fusion | `src/models/fusion.py` |
| Demand + Stress Heads | `src/models/heads.py` |
| PF-STGT Wrapper | `src/models/pf_stgt.py` |

Supporting: `config.py`, `types.py`, `torch_utils.py`

### Architecture (Phase 09)

```
InputEmbedding → [GraphTransformer ∥ TemporalTransformer] → ParallelFusion
    → H_shared → DemandHead (B,9) + StressHead (B,1)
```

Defaults: d_model=128, L_s=2, L_t=2, heads=4, ffn=256, dropout=0.1

### I/O Contract Validation

| Tensor | Expected | Verified |
| --- | --- | --- |
| node_features | (B, 7, 9, 9) | Pass |
| global_features | (B, 7, 17) | Pass |
| adjacency | (9, 9) | Pass |
| demand_pred | (B, 9) | Pass |
| osi_pred | (B, 1) ∈ [0,1] | Pass |

**Parameters:** 749,058 trainable

### Tests

- **26/26** total tests passing (8 new PF-STGT tests + Sprint 01 regression)
- Script: `scripts/sprint_02_pf_stgt.py`
- Report: `results/phases/sprint_02_pf_stgt/sprint_02_report.md`

### Scope Compliance

- PF-STGT core model only — no training, evaluation, or explainability
- Sprint 01 modules not modified; locked MD5s unchanged

### Status

Ready for Sprint 3 — Training pipeline.