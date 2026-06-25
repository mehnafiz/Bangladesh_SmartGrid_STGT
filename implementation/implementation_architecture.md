# Implementation Architecture — Phase 16A

Generated: 2026-06-24
Status: **FROZEN BLUEPRINT** (no code in this phase)

## Purpose

End-to-end engineering architecture translating Phases 01–15 into implementable
Python modules under `src/`. This document defines **system layers**, **data flow**,
and **artefact boundaries** — not executable code.

## System context

```
┌─────────────────────────────────────────────────────────────────┐
│                     OFFLINE DATA (LOCKED)                       │
│  clean.parquet │ *_features.parquet │ adjacency.csv │ targets/  │
└────────────────────────────┬────────────────────────────────────┘
                             │
    ┌────────────────────────┼────────────────────────┐
    ▼                        ▼                        ▼
 P1 Data              P2 Feature              P3 Graph
    │                        │                        │
    └────────────┬───────────┴───────────┬────────────┘
                 ▼                       │
            P4 Target                    │
                 │                       │
                 └───────────┬───────────┘
                             ▼
                      P5 Model (PF-STGT)
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         P6 Training   P7 Evaluation  P8 Explainability
              │              │              │
              ▼              ▼              ▼
         checkpoints/  results/evaluation/  results/explainability/
```

## Pipeline registry

| pipeline_id   | name                     | src_package                           | phase_sources   | locked_inputs                    | outputs                                          |
|:--------------|:-------------------------|:--------------------------------------|:----------------|:---------------------------------|:-------------------------------------------------|
| P1            | Data Pipeline            | src.data, src.datasets                | 01–04, 06       | data/interim/, data/features/    | SmartGridDataset, split manifests                |
| P2            | Feature Pipeline         | src.features, src.preprocessing       | 05A, 05B, 06    | data/features/*_features.parquet | node_tensor (B,T,N,F_n), global_tensor (B,T,F_g) |
| P3            | Graph Pipeline           | src.graph                             | 08              | graphs/adjacency_matrix.csv      | adjacency (N,N), edge_index, adjacency_bias      |
| P4            | Target Pipeline          | src.datasets (targets module)         | 08.5, 05B       | targets/, clean parquet columns  | demand_target (B,N), osi_target (B,1)            |
| P5            | Model Pipeline (PF-STGT) | src.models, src.losses                | 09, 10, 13      | architecture/                    | demand_pred, osi_pred, attn maps                 |
| P6            | Training Pipeline        | src.training                          | 10, 11          | experiments/, optimization/      | checkpoints/, metrics_val.json                   |
| P7            | Evaluation Pipeline      | src.evaluation, src.metrics           | 14, 15          | evaluation/, error_analysis/     | tables/, leaderboards, significance              |
| P8            | Explainability Pipeline  | src.explainability, src.visualization | 12              | explainability/                  | SHAP, attention, permutation artefacts           |

## Layer responsibilities

### Layer 1 — Data ingestion (P1)

- Load locked parquet artefacts; verify MD5 before any run.
- Enforce chronological splits (Phase 04); expose `SmartGridDataset`.
- Warm-up: skip first 7 rows per split (Phase 06).

### Layer 2 — Feature & graph preparation (P2, P3)

- Materialise `(B, T=7, N=9, F_n=9)` and `(B, T, F_g=17)` tensors.
- Load hybrid adjacency; support A5-GEO / A5-CORR variants via registry.
- **Leakage guard:** exclude `operational_stress_index` from model inputs.

### Layer 3 — Target assembly (P4)

- `demand_target`: 9 × `{Region}_demand` at horizon t+1.
- `osi_target`: composite OSI at t+1 (Phase 05B formula, train-fitted bounds).

### Layer 4 — Model forward (P5)

PF-STGT module graph (Phase 09):

```
InputEmbedding → [GraphTransformer ∥ TemporalTransformer] → ParallelFusion
    → MultiTaskHeads → demand_pred (B,9), osi_pred (B,1)
```

Ablation switches (Phase 13): disable spatial/temporal branch, swap adjacency,
remove stress head (A4), replace trunk (A6).

### Layer 5 — Training orchestration (P6)

- AdamW lr=5e-4, ReduceLROnPlateau, early stopping patience=15.
- Multi-seed {42, 123, 456} for B04–B07 and A1.
- Checkpoints: `checkpoints/{model_id}/seed_{s}/best.pt`.

### Layer 6 — Evaluation & reporting (P7)

- Populate Tables 1–4 (Phase 15); run Phase 14 error taxonomy E1–E6.
- Wilcoxon + Bonferroni on daily macro MAE (~278 test days).

### Layer 7 — Explainability (P8)

- Post-training only: SHAP, attention export, permutation, stress decomposition.
- 20 stratified case studies (Phase 12); Figures 3–5.

## Configuration hierarchy

```
configs/
  default.yaml          # global paths, seeds, T, N, h
  model/pf_stgt.yaml    # d_model=128, L_s=2, L_t=2, heads=4
  training/deep.yaml    # Phase 10/11 hyperparameters
  evaluation/test.yaml  # Phase 15 table/figure targets
  ablation/A2_no_graph.yaml  # per-variant overrides
```

## CLI entry points (implementation phase — not built here)

| Command | Pipeline | Purpose |
| --- | --- | --- |
| `python -m scripts.train --model B07 --seed 42` | P6 | Train single run |
| `python -m scripts.evaluate --benchmark all` | P7 | Table 1 generation |
| `python -m scripts.ablate --variant A2` | P6,P7 | Ablation train+eval |
| `python -m scripts.explain --checkpoint ...` | P8 | XAI export |
| `python -m scripts.error_analysis` | P7 | Phase 14 segments |

## Non-goals (this phase)

- No PyTorch module implementations.
- No training runs or result files.
- No modification of locked parquet/CSV artefacts.
