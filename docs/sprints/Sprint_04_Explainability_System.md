# Sprint 04 — Explainability System

## Objective

Implement the explainability framework for PF-STGT.

This sprint must support:

- Feature Attribution
- Node Attribution
- Temporal Attribution
- Stress Attribution

---

## Components

### SHAP Engine

Responsibilities:

- Global feature importance
- Local explanations
- Summary plots

---

### Attention Extractor

Responsibilities:

- Spatial attention extraction
- Temporal attention extraction

---

### Permutation Importance

Responsibilities:

- Global importance validation
- Stability analysis

---

### Node Attribution

Responsibilities:

- Regional contribution analysis
- Node importance ranking

---

### Temporal Attribution

Responsibilities:

- Time-step contribution analysis
- Lookback influence analysis

---

### Stress Attribution

Responsibilities:

- OSI driver analysis
- High-stress event explanation

---

## Deliverables

src/explainability/

tests/

Sprint report

---

## Definition of Done

✔ SHAP integration implemented

✔ Attention extraction implemented

✔ Permutation importance implemented

✔ Attribution modules implemented

✔ Tests pass

✔ Ready for experiments

---

## Execution Record

**Date:** 2026-06-24  
**Script:** `scripts/sprint_04_explainability.py`  
**Report:** `results/phases/sprint_04_explainability/sprint_04_report.md`

### Packages Implemented

| Module | Responsibility |
| --- | --- |
| `config.py` | Phase 12 frozen XAI defaults |
| `types.py` | Typed attribution result containers |
| `coalitions.py` | G1–G11 leakage-safe feature groups |
| `shap_engine.py` | GradientSHAP-style grouped φ values |
| `attention_extractor.py` | Spatial/temporal attention aggregation |
| `permutation.py` | Coalition permutation importance |
| `node_attribution.py` | Regional SHAP + attention ranking |
| `temporal_attribution.py` | Lookback α_t and top-k lags |
| `stress_attribution.py` | SHAP + OSI c1/c2/c3 dual pathway |

### Attribution Mapping (Phase 12)

| Level | Methods |
| --- | --- |
| L1 Feature | SHAP + Permutation |
| L2 Node | SHAP coalitions + spatial attention |
| L3 Temporal | Temporal attention α_t |
| L4 Graph | Spatial attention + adjacency overlay |
| L5 Stress | SHAP + component decomposition |

### Tests

- **54/54** total tests passing (16 new Sprint 04 tests + Sprint 01–03 regression)
- No training or full XAI experiments executed

### Scope Compliance

- Explainability infrastructure only — no model training or benchmark runs
- Sprint 01–03 modules not modified; locked MD5s unchanged

### Status

Ready for post-training XAI experiments (20 case-study dates per Phase 12 protocol).