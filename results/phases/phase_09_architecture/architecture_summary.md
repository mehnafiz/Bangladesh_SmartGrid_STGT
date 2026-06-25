# Phase 09 — STGT Architecture Design Summary

- Completion date: 2026-06-24
- Selected architecture: **PF-STGT (Parallel-Fusion Spatio-Temporal Graph Transformer)**

## Module selections

| Module | Selection |
| --- | --- |
| Spatial | Graph Transformer (adjacency-biased multi-head self-attention) |
| Temporal | Transformer Encoder (multi-layer temporal self-attention) |
| Fusion | Parallel Fusion (spatial branch ∥ temporal branch → gated concat) |

## I/O summary

- Input: (B, T=7, N=9, F_n=9) + global (B, T, F_g=17)
- Output Task 1: (B, 9) demand MW
- Output Task 2: (B, 1) OSI ∈ [0,1]

## Deliverables

### architecture/
- architecture_overview.md
- architecture_components.md
- architecture_diagram.md
- input_output_specification.md
- module_rationale.md
- loss_function_design.md
- explainability_design.md

### results/phases/phase_09_architecture/
- architecture_summary.md
- architecture_validation_report.md
- design_decision_rationale.md

## Scope compliance

- Architecture design only; **no implementation or training**.
- Locked phase outputs not modified.

## Status

Phase 09 design complete. **Post-freeze (2026-06-25):** final production model is **S2**
(correlation graph PF-STGT); see `experiments/architecture_freeze_revision/`.

Ready for Experiment 04 explainability on S2 checkpoint.
