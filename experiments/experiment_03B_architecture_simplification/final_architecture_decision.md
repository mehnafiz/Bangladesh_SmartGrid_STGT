# Final Architecture Decision — Experiment 03B

Generated: 2026-06-25

## Q4 — Is PF-STGT complexity justified?

**No — the full S1 architecture is not justified for demand accuracy; selective simplification is.**

### Evidence

1. **Hybrid graph + fusion is not demand-optimal:** S2 beats S1 by **4.66 MW** (p < 0.001). Correlation-only graph is simpler *and* stronger.
2. **Temporal transformer is redundant on hybrid graph:** S3 matches S1 within **0.66 MW** (p = 0.384; Exp 03A entropy 0.998).
3. **Simplifications do not compose:** S4 (+21.32 MW vs S1) shows correlation graph needs the temporal branch; removing both geo noise *and* transformer oversimplifies.
4. **Complexity cost without benefit:** S1 uses 749k active parameters, parallel fusion, and hybrid edges; none of these improve demand vs S2 or S3.

### Decision

| Role | Selected architecture |
| --- | --- |
| **Primary (demand + stress)** | **S2** — Correlation-only PF-STGT (88.65 MW) |
| **Compute-efficient alternative** | **S3** — No-transformer PF-STGT (92.64 MW, 451k active params) |
| **Paper baseline / design reference** | **S1** — Full PF-STGT W20 (disclose not demand-optimal) |
| **Not recommended** | **S4** — Both removals together |

### Caveats

- S1 checkpoint comes from Exp01B; S2/S3 from Exp03; S4 trained here — protocol alignment is good for S4 but S1 provenance differs.
- Multi-task interference (Exp 03A) still affects all W20 variants; demand-only A4 remains strongest for pure demand.
- Full PF-STGT complexity **is justified** only if the research claim requires hybrid graph + parallel fusion **as the stated architecture**, not if the goal is minimum error.
