# Final Model Specification — S2 (Frozen)

Generated: 2026-06-25  
Status: **FROZEN** — Architecture Freeze Revision  
Architecture ID: **S2**  
Publication name: **Correlation-Aware Multi-Task Forecasting Framework**

---

## 1. Architecture summary

S2 is implemented as **`PFSTGT`** (`src/models/pf_stgt.py`) with the **correlation graph**
selected at the data layer (`GraphVariant.CORR`). It retains the parallel-fusion
spatio-temporal trunk (graph transformer + temporal transformer + fusion) and dual
forecasting heads. Only the **geographical component of the hybrid adjacency** is removed.

| Property | Value |
| --- | --- |
| Structural class | `PFSTGT` (full parallel-fusion trunk) |
| Graph variant | `GraphVariant.CORR` |
| Correlation threshold | τ = 0.65 (`CORRELATION_THRESHOLD`) |
| Undirected edges | 33 (91.7% of 36 possible pairs) |
| Parameters | 749,058 (all active in forward pass) |
| Tasks | Multi-task: regional demand + graph-level OSI |
| Original architecture | **S1** — hybrid graph PF-STGT W20 (superseded for production) |

---

## 2. Inputs

Identical windowing and leakage policy to Phase 08.5 / Phase 09. Graph adjacency is the
**only** input difference vs S1.

| Input | Shape | Dtype | Description |
| --- | --- | --- | --- |
| `node_features` | (B, T=7, N=9, F_n=9) | float32 | Per-region lag/rolling features |
| `global_features` | (B, T=7, F_g=17) | float32 | National / system context |
| `adjacency` | (N, N) | float32 | Row-normalised **correlation** graph (not hybrid) |
| `attention_bias` | (N, N) | float32 | Optional; derived from adjacency if omitted |

**Node order (fixed):** Barishal, Chattogram, Cumilla, Dhaka, Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet.

**Leakage policy:** OSI(t) excluded from inputs when predicting OSI(t+1). See
`architecture/input_output_specification.md`.

**Data artefacts (MD5-locked):**

| Artefact | Role |
| --- | --- |
| `data/interim/bangladesh_smartgrid_clean.parquet` | Timeline source |
| `data/features/*_features.parquet` | Model features |
| `graphs/adjacency_matrix.csv` | Geographic prior (used to build corr graph) |

---

## 3. Outputs

| Output | Shape | Range | Task |
| --- | --- | --- | --- |
| `demand_pred` | (B, 9) | MW | Task 1 — next-day regional demand |
| `osi_pred` | (B, 1) | [0, 1] | Task 2 — next-day operational stress index |
| `attn_spatial` | optional | [0, 1] | Explainability export (Exp04) |
| `attn_temporal` | optional | [0, 1] | Explainability export (Exp04) |
| `h_shared` | (B, 9, 128) | — | Shared representation (diagnostics) |

---

## 4. Training configuration (frozen)

Matches Experiment 03 **A6** / W20 repair protocol. **Do not retrain** unless explicitly
starting a new study.

| Setting | Value |
| --- | --- |
| Loss | `L = Huber(demand)/100 + λ₂ · MSE(OSI)` |
| λ₂ (stress weight) | **20.0** |
| Demand normalisation | Divide raw Huber by 100 in total loss |
| Optimiser | Adam, lr = **5×10⁻⁴**, weight decay = **10⁻⁴** |
| Batch size | 32 |
| Max epochs | 200 |
| Early stopping | Patience 15; score = **0.7·(val_demand_MAE/100) + 0.3·val_stress_MAE** |
| Scheduler | ReduceLROnPlateau on val demand MAE |
| Seed | **42** (frozen reference run) |
| Device | As available (cuda > mps > cpu) |

**Coordinator:** `FoundationCoordinator(graph_variant=GraphVariant.CORR, verify_md5=True)`

**Canonical checkpoint (frozen):**

```
experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt
```

Training time (reference): ~393 s (Experiment 03, seed 42).

---

## 5. Evaluation configuration (frozen)

| Rule | Specification |
| --- | --- |
| Primary split | **Test** — 264 samples (278 days minus T=7 warm-up) |
| Date range | 2024-03-20 → 2024-12-30 |
| Model selection | Validation only; no test tuning |
| Warm-up | Exclude first T=7 rows per split |

### Task 1 — Demand metrics (macro over 9 regions)

| Metric | Primary? |
| --- | --- |
| MAE (MW) | **Yes** — primary ranking metric |
| RMSE (MW) | Yes |
| MAPE (%) | Yes (exclude y=0) |
| R² | Yes — **macro** (mean of per-region R²) |

### Task 2 — Stress metrics

| Metric | Primary? |
| --- | --- |
| MAE | Yes |
| RMSE | Yes |
| R² | Yes |
| Pearson r | Supplementary |

### Reference test performance (frozen checkpoint, seed 42)

| Metric | Value | Source |
| --- | --- | --- |
| Demand MAE | **88.65 MW** | Exp03B S2 / Exp03 A6 |
| Demand R² | 0.684 | same |
| Stress MAE | 0.0371 | same |
| Stress R² | 0.745 | same |

### Statistical testing

- Wilcoxon signed-rank on per-sample macro demand MAE (test set)
- Bonferroni α = 0.01 for multi-comparison sets (Phase 13 / Exp03 protocol)
- Bootstrap 95% CI on mean MAE differences (2000 resamples, seed 42)

---

## 6. Implementation loading (inference / Exp04)

```python
from foundation import FoundationCoordinator
from graph.registry import GraphVariant
from models.pf_stgt import PFSTGT
import torch

CKPT = "experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt"
coordinator = FoundationCoordinator(verify_md5=True, graph_variant=GraphVariant.CORR)
model = PFSTGT()
payload = torch.load(CKPT, map_location="cpu", weights_only=False)
model.load_state_dict(payload["model_state_dict"])
model.eval()
```

---

## 7. Relationship to benchmarks and ablations

| ID | Relationship to S2 |
| --- | --- |
| B07 (Exp02) | Historical **proposed** benchmark = S1, not S2 |
| A1 (Exp03) | Original full-model ablation reference = S1 |
| A6 (Exp03) | **Identical architecture and checkpoint to S2** |
| S1 (Exp03B) | Original architecture baseline |
| S2 (Exp03B) | **Final frozen model** |

---

## 8. Next experiment

**Experiment 04 — Explainability** will load the S2 checkpoint above and run Phase 12 /
Sprint 04 attribution pipelines. No retraining required.

See `experiments/experiment_04_explainability/Experiment_04_Explainability.md`.
