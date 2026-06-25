# Architecture Recommendation — Experiment 03B

Generated: 2026-06-25

## Q1 — Does correlation-only outperform PF-STGT?

**Yes.** S2 demand MAE **88.65** vs S1 **93.31** MW (Δ = -4.66; median daily Δ -5.43, p_better = 0.0000).

## Q2 — Does removing transformer hurt performance?

**No meaningful harm on demand.** S3 MAE **92.64** vs S1 **93.31** (Δ = -0.66; p = 0.3836).
Temporal attention in S1 is near-uniform (Exp 03A); graph branch already encodes 7-day windows.

## Q3 — Can a simpler model achieve similar performance?

**Partially — depends on which simplification.**

- **S3 (no transformer):** **92.64** MW vs S1 **93.31** (Δ = -0.66; within noise) with 451,202 active parameters (−40% compute path).
- **S2 (correlation graph):** **88.65** MW — **better** than S1, not merely similar.
- **S4 (both removals):** **114.63** MW — **worse** than S1 (+21.32 MW; negative interaction).

## Recommended deployment profiles

| Goal | Variant | Rationale |
| --- | --- | --- |
| Best demand + stress (multi-task W20) | **S2** | Lowest MAE (88.65 MW) and highest stress R² (0.745) |
| Minimum compute, similar demand | **S3** | −40% active params; ΔMAE -0.66 MW vs S1 |
| Paper reference (full PF-STGT) | **S1** | Original hybrid + parallel fusion design |
| Avoid | **S4** | Stacking graph + transformer removal hurts demand (+21.32 MW) |
