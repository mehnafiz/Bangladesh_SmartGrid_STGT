# Phase 11 — Hyperparameter Optimization Strategy

## Objective

Design a scientifically justified hyperparameter optimization protocol for PF-STGT.

The protocol must be reproducible, computationally feasible, and publication-ready.

---

## Inputs

Phase 09 Architecture Design

Phase 10 Training Strategy

---

## Fixed Parameters

Lookback Window (T) = 7

Forecast Horizon (H) = 1

Nodes = 9

Tasks = 2

Graph Strategy = Hybrid

---

## Search Parameters

### Graph Module

- Number of Graph Layers
- Graph Hidden Dimension
- Graph Dropout

### Transformer Module

- Number of Transformer Layers
- Number of Attention Heads
- Transformer Dropout

### Training Parameters

- Learning Rate
- Weight Decay
- Batch Size

---

## Candidate Ranges

Must be justified.

Avoid excessively large search spaces.

---

## Optimization Strategy

Evaluate:

1. Grid Search
2. Random Search
3. Bayesian Optimization

Select the most appropriate strategy.

Provide justification.

---

## Computational Budget

Estimate:

- Number of trials
- Expected runtime
- Resource requirements

---

## Model Selection

Define:

- Primary metric
- Secondary metrics
- Tie-breaking strategy

---

## Deliverables

optimization/

- search_space.md

- parameter_ranges.csv

- optimization_strategy.md

- computational_budget.md

- model_selection_protocol.md

results/phases/

phase_11_hyperparameter_optimization/

- optimization_summary.md

- optimization_decision_report.md

---

## Definition of Done

✔ Search space frozen

✔ Optimization strategy frozen

✔ Computational budget defined

✔ Model selection protocol defined

✔ Ready for implementation

---

## Execution Record

### Completion Date

2026-06-24

### Frozen HPO Protocol

| Component | Decision |
| --- | --- |
| **Optimization method** | Random Search (seed 42, validation-only) |
| **Search dimensions** | 9 (graph ×3, transformer ×3, training ×3) |
| **Stage 1 trials** | 20 |
| **Stage 2 confirmation** | Top-3 configs × 3 seeds (42, 123, 456) |
| **Total training runs** | 29 (20 + 9 + 1 test) |
| **Est. GPU budget** | ~5–9 hours |
| **Primary metric** | validation_macro_demand_MAE |
| **Secondary metric** | validation_stress_MAE |

### Parameter Ranges (searchable)

| Parameter | Candidates |
| --- | --- |
| num_graph_layers (L_s) | 1, 2, 3 |
| graph_hidden_dim (d_model) | 64, 128, 192 |
| graph_dropout | 0.1, 0.2, 0.3 |
| num_transformer_layers (L_t) | 1, 2, 3 |
| num_attention_heads | 2, 4, 8 (must divide d_model) |
| transformer_dropout | 0.1, 0.2, 0.3 |
| learning_rate | 1e-4, 5e-4, 1e-3 |
| weight_decay | 1e-5, 1e-4, 1e-3 |
| batch_size | 16, 32, 64 |

### Fixed (not searched)

T=7, H=1, N=9, hybrid adjacency, AdamW, λ1=1.0, λ2=0.5, early stopping patience=15.

### Method Selection

| Method | Score | Selected |
| --- | --- | --- |
| Random Search | 21/25 | **Yes** |
| Bayesian Optimization | 17/25 | No |
| Grid Search | 10/25 | No |

Grid rejected (19,683 combos); Bayesian rejected (small val set, reproducibility).

### Deliverables Generated

`optimization/`:

* `search_space.md`
* `parameter_ranges.csv`
* `optimization_strategy.md`
* `computational_budget.md`
* `model_selection_protocol.md`

`results/phases/phase_11_hyperparameter_optimization/`:

* `optimization_summary.md`
* `optimization_decision_report.md`
* `trial_0_baseline_config.csv` (Phase 09 default reference)

Script: `scripts/phase_11_hyperparameter_optimization.py`

### Scope Compliance

* HPO strategy design only; **no implementation or training**.
* Locked phase outputs unchanged (`train_features.parquet` MD5: `b8b3bda95d0fd6cc65f4910d85a98e16`).

### Status

Ready for PF-STGT implementation and HPO execution (next phase).