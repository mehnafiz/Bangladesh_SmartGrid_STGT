# Phase 08 — Graph Construction

## Objective

Design and construct the graph representation for the proposed STGT framework.

The graph must be supported by both domain knowledge and literature evidence.

---

## Input

Validated feature datasets

Research Gap Outputs

Literature Analysis

---

## Candidate Nodes

Regional Entities

* Barishal
* Chattogram
* Cumilla
* Dhaka
* Khulna
* Mymensingh
* Rajshahi
* Rangpur
* Sylhet

---

## Candidate Graph Strategies

1. Geographical Graph

2. Correlation Graph

3. Hybrid Graph

---

## Required Analysis

For each graph strategy evaluate:

* Scientific validity
* Literature support
* Interpretability
* Complexity
* Suitability for STGT

---

## Deliverables

graphs/

* node_definition.md

* graph_strategy_comparison.md

* adjacency_matrix.csv

* graph_construction_report.md

* graph_statistics.csv

results/phases/

phase_08_graph_construction/

* graph_summary.md

* graph_validation_report.md

* graph_decision_rationale.md

---

## Definition of Done

✔ Nodes defined

✔ Graph strategy selected

✔ Adjacency matrix created

✔ Graph validated

✔ Ready for STGT architecture

---

## Execution Record

### Completion Date

2026-06-24

### Graph Construction Summary

* **9 nodes** — regional divisions (Barishal, Chattogram, Cumilla, Dhaka, Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet).
* **3 strategies compared:** Geographical, Correlation (τ=0.65), Hybrid (geo + ρ weights, ρ≥0.85 augmentation).
* **Selected strategy:** **Hybrid Graph** (score 23/25).
* **Adjacency:** 24 undirected edges, 66.7% density, row-normalised Pearson demand-correlation weights (train-only, n=1,295).

### Strategy Comparison

| Strategy | Edges | Density | Total score ( /25) |
| --- | --- | --- | --- |
| Hybrid Graph | 24 | 66.7% | **23** |
| Geographical Graph | 21 | 58.3% | 19 |
| Correlation Graph | 33 | 91.7% | 15 |

| Dimension | Geographical | Correlation | Hybrid |
| --- | --- | --- | --- |
| Scientific validity | 4 | 4 | **5** |
| Literature support | 3 | 4 | **5** |
| Interpretability | **5** | 2 | 4 |
| Complexity (higher=simpler) | 4 | 2 | 4 |
| STGT suitability | 3 | 3 | **5** |

### Hybrid Construction Rule

```
w_ij = ρ_ij  if geo_ij = 1 OR ρ_ij ≥ 0.85
w_ij = 0     otherwise
A = row_normalize(W)
```

Train-only demand correlation: min=0.622, mean=0.779, max=0.934 (Phase 02 aligned).

### Deliverables Generated

`graphs/`:

* `node_definition.md`
* `graph_strategy_comparison.md`
* `adjacency_matrix.csv`
* `graph_construction_report.md`
* `graph_statistics.csv`

`data/graph/`:

* `adjacency_matrix.csv` (selected strategy copy)

`results/phases/phase_08_graph_construction/`:

* `graph_summary.md`
* `graph_validation_report.md`
* `graph_decision_rationale.md`

Script: `scripts/phase_08_graph_construction.py`

### Validation Results

* Symmetry: **PASS**
* Self-loops: **PASS** (zero)
* Connected: **PASS**
* Non-negative weights: **PASS**
* Train-only correlation: **PASS**
* Mean ρ on edges (0.790) > off edges (0.603): **PASS**

### Scope Compliance

* Graph construction and strategy selection only.
* **No STGT architecture design** performed.
* Locked phase outputs unchanged (`train_features.parquet` MD5: `b8b3bda95d0fd6cc65f4910d85a98e16`).

### Recommendations for STGT Architecture Phase

1. Use `graphs/adjacency_matrix.csv` as fixed spatial prior; consider time-varying edge refresh via `rolling_demand_corr_90d` in later phases.
2. Attach graph-level features (OSI, limitation stacks, national demand) per Phase 06 node/global split.
3. Preserve multi-task heads for demand, sparse shedding, and operational stress (Phase 07C gaps GAP-02/03/06).

### Status

Ready for STGT architecture phase.
