# Design Decision Rationale — Phase 09

Generated: 2026-06-24

## Selected: PF-STGT (Parallel-Fusion Graph Transformer) (ARCH-C, score 27)

## Why PF-STGT over alternatives

### vs ARCH-A (GCN-LSTM)
- LSTM temporal encoding lacks transformer attention maps (GAP-05).
- GCN cannot leverage Phase 08 correlation-weighted hybrid edges as flexibly as graph attention.

### vs ARCH-B (GAT + Temporal Attention, ST-first)
- Sequential fusion underuses parallel national-seasonality and spatial-coupling drivers (Phase 02).
- Shallow temporal attention insufficient for T=7 weekly patterns.

## Research gap alignment

| Gap | PF-STGT response |
| --- | --- |
| GAP-04 | Graph Transformer + Transformer Encoder |
| GAP-05 | Dual attention export + SHAP feature groups |
| GAP-02 | Shared H_shared with dual task heads |
| GAP-06 | StressHead on graph readout + limitation-aware inputs |
| GAP-07 | F_g includes limitation stack and grid covariates |

## Implementation deferral

This phase produces design artefacts only. PyTorch modules, training loops, and SHAP pipelines
are deferred to the implementation/training phases.
