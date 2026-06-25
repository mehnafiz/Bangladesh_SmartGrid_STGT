# Engineering Blueprint — Phase 16A

Generated: 2026-06-24
Status: **FROZEN BLUEPRINT**

## Implementation roadmap

Recommended coding order respecting dependency flow:

### Sprint 1 — Foundations (P1, P2, P3, P4)

| Step | Task | Acceptance test |
| --- | --- | --- |
| 1.1 | `MD5Guard` + data loaders | Locked hashes pass |
| 1.2 | `SplitManager` + validators | Row counts = Phase 04 |
| 1.3 | Feature builders + scaler | Tensor shapes match Phase 09 |
| 1.4 | Graph loader + bias | (9,9) matches CSV |
| 1.5 | Target builders | OSI formula matches Phase 05B |
| 1.6 | `SmartGridDataset` + DataLoader | Single batch loads without NaN |

### Sprint 2 — Model core (P5)

| Step | Task | Acceptance test |
| --- | --- | --- |
| 2.1 | InputEmbedding | Output (B,T,N,d) |
| 2.2 | GraphTransformer + TemporalEncoder | Attention export works |
| 2.3 | ParallelFusion + Heads | demand (B,9), osi (B,1) |
| 2.4 | MultiTaskLoss | Scalar backward pass |
| 2.5 | PFSTGT forward + ablation switches | A2/A3/A4 config toggles |
| 2.6 | Baseline stubs B04–B06 | Same batch interface |

### Sprint 3 — Training (P6)

| Step | Task | Acceptance test |
| --- | --- | --- |
| 3.1 | Trainer + callbacks | 1 epoch runs on CPU |
| 3.2 | Checkpoint + seed | Reproducible loss curve |
| 3.3 | HPO integration (Phase 11) | Random search hook |
| 3.4 | Multi-seed launcher | 3 checkpoints B07 |

### Sprint 4 — Evaluation (P7)

| Step | Task | Acceptance test |
| --- | --- | --- |
| 4.1 | DemandMetrics + StressMetrics | Unit tests on synthetic |
| 4.2 | BenchmarkRunner | Populates table schema |
| 4.3 | AblationRunner + statistics | Wilcoxon pipeline |
| 4.4 | ErrorAnalysisRunner | E1–E6 CSV schemas |

### Sprint 5 — Explainability (P8)

| Step | Task | Acceptance test |
| --- | --- | --- |
| 5.1 | Attention export | Non-null attn tensors |
| 5.2 | SHAP + permutation | Quality gate metrics |
| 5.3 | Manuscript figures | Fig 1–5 file paths |

## Directory layout (target state)

```
Bangladesh_SmartGrid_STGT/
├── configs/                    # NEW — YAML configs
├── scripts/
│   ├── train.py                # NEW
│   ├── evaluate.py             # NEW
│   ├── ablate.py               # NEW
│   └── explain.py              # NEW
├── src/
│   ├── data/                   # P1
│   ├── datasets/               # P1, P4
│   ├── features/               # P2
│   ├── preprocessing/          # P2
│   ├── graph/                  # P3
│   ├── models/                 # P5
│   ├── losses/                 # P5
│   ├── training/               # P6
│   ├── evaluation/             # P7
│   ├── metrics/                # P7
│   ├── explainability/         # P8
│   ├── visualization/          # P8
│   └── utils/                  # shared
├── checkpoints/                # NEW — runtime output
├── results/
│   ├── experiments/            # leaderboards
│   ├── evaluation/             # tables, figures
│   ├── explainability/         # XAI artefacts
│   └── error_analysis/         # Phase 14 outputs
└── [locked] data/, graphs/, architecture/, ...
```

## Pipeline data flow (single training step)

```
SmartGridDataset.__getitem__(idx)
  → WindowBuilder: node (T,N,F_n), global (T,F_g)
  → TargetBuilder: demand (N,), osi (1,)
  → collate_fn → batch dict

PFSTGT.forward(batch)
  → AdjacencyLoader → bias
  → encoders → fusion → heads
  → ModelOutput

MultiTaskLoss(output, batch)
  → scalar loss → backward
```

## Benchmark / ablation execution matrix

| Run ID | Model | Seeds | Pipeline | Est. hours |
| --- | --- | --- | --- | --- |
| B01–B03 | Classical | 1 | P1→P2→P5→P7 | ~0.5 |
| B04–B06 | Deep baselines | 3 | P1→P2→P3→P5→P6→P7 | ~6 |
| B07 / A1 | PF-STGT full | 3 | All P1–P8 | ~6 |
| A2–A6 | Ablations | 1 | P1–P7 (+P8 for A6-XAI on A1) | ~12–18 total |

## Testing strategy

| Level | Scope |
| --- | --- |
| Unit | Metrics, OSI formula, adjacency bias, leakage guard |
| Integration | Dataset → model forward → loss (1 batch) |
| Regression | Locked MD5 unchanged after any pipeline run |
| Smoke | 2-epoch train on CPU subset |

## Risk register

| Risk | Mitigation |
| --- | --- |
| OSI leakage | `LeakageGuard` unit test; exclude OSI from F_g |
| Node order mismatch | Single `REGIONS` constant imported everywhere |
| Small train set (1295) | Early stopping; Phase 11 HPO; report seed std |
| Test stress shift | Robustness segments (Phase 14/15) |
| XAI cost | 20 case studies only; cache SHAP backgrounds |

## Definition of ready for coding

['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8']
- P1 through P8 fully specified with module paths and acceptance tests.
All eight pipelines specified with module paths, I/O contracts, and sprint plan.
