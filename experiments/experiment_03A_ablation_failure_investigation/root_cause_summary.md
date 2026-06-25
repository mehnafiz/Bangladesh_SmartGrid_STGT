# Root Cause Summary — Experiment 03A

Generated: 2026-06-25

## F1 — Why A4 beats A1

| Cause | Evidence |
| --- | --- |
| **Objective mismatch** | A1 uses balanced ES (demand + stress); A4 uses demand-only ES |
| **Task interference** | λ₂=20 stress term; stress-head gradients active on shared trunk |
| **Protocol confound** | A1 = Exp01B W20 checkpoint; A4 = fresh Exp03 demand-only training |
| **Regional effect** | Dhaka ΔMAE −14.7 MW (largest single-region gain) |

## F2 — Why A3 ≈ A1

| Cause | Evidence |
| --- | --- |
| **Redundant temporal path** | Graph branch already encodes 7-day windows |
| **Near-uniform temporal attention** | Entropy ratio 0.998 on A1 |
| **Moderate representation overlap** | A1 vs A3 h_shared cosine ≈ 0.70 |
| **Non-significant ΔMAE** | −0.66 MW, p = 0.38 |

## F3 — Why correlation-only beats hybrid (A6 vs A1)

| Cause | Evidence |
| --- | --- |
| **Denser informative edges** | Corr graph higher edge density than hybrid (see graph_contribution_report) |
| **Geo noise in hybrid** | A5 (geo-only) +4.67 MW vs A1; geo-only edges misconnect weakly correlated pairs |
| **Different training runs** | A6 retrained; may find better demand minima with corr adjacency |

## F4 — Is hybrid graph beneficial?

**Partially.** Hybrid significantly **beats geographical-only** (A5 vs A1, p_adj < 0.01).
It does **not** beat correlation-only on demand. Hybrid adds correlation weights but retains
geographical edges that hurt relative to a pure correlation topology.

## Multi-task interference verdict

**Confirmed** for demand vs stress: removing stress (A4) yields ~6.4 MW lower demand MAE while
eliminating OSI capability. Interference is **by design** in W20, not a implementation bug.
