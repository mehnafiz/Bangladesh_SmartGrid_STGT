# Proposed Research Positioning

Generated: 2026-06-23

## Working title alignment

*An Explainable Spatio-Temporal Graph Transformer for Multi-Task Load Shedding Forecasting and Operational Stress Assessment in Bangladesh Smart Power Networks*

## Positioning statement

This research occupies the intersection of four under-served areas in the reviewed literature (n=55, 2023–2026): **(1)** Bangladesh division-level smart-grid analytics, **(2)** multi-task coupling of demand and sparse load shedding, **(3)** graph-temporal modelling with explainability, and **(4)** daily operational-stress assessment derived from limitation-aware covariates. Existing work clusters into single-task forecasting (20 papers), shedding control/optimisation (15), and isolated graph or transformer methods (5 graph-based, 7 transformer-based) evaluated mainly on US/EU residential or microgrid data.

## Literature cluster map

| Cluster | Papers | Project differentiation |
| --- | --- | --- |
| Electrical Load Forecasting | 14 | Adds graph coupling, shedding head, OSI task, Bangladesh data |
| Load Shedding Prediction | 15 | Shifts from UFLS/control to daily forecast formulation |
| Graph / Spatio-temporal | 5 graph, 7 transformer | Targets 9-division national grid, not AMI/EV micro-networks |
| Explainability (SHAP/XAI) | 3 with XAI | Integrates XAI with multi-task graph-temporal outputs (planned) |
| Operational stress / reliability | 3 | Daily OSI from demand–limitation stacks vs asset reliability |

## Gap-to-contribution alignment

- **GAP-01** (Critical): No peer-reviewed spatio-temporal load or load-shedding forecasting study uses Bangladesh division-level smart-grid daily data.
- **GAP-02** (Critical): Literature rarely couples continuous regional demand forecasting with sparse load-shedding prediction in a unified multi-task learning framework.
- **GAP-03** (Critical): Most load-shedding literature optimises control actions or frequency response rather than forecasting sparse daily shedding intensity for operational planning.
- **GAP-04** (High): Few recent papers combine graph-based spatial coupling with transformer-style temporal modelling for multi-node load forecasting; none target Bangladesh shedding.
- **GAP-05** (High): Explainable AI is rarely integrated with graph-temporal load or shedding models; SHAP/XAI appears in only a small fraction of the reviewed corpus.
- **GAP-06** (High): Operational stress and reliability studies focus on transmission/microgrid assets rather than daily regional stress indices derived from demand–supply–limitation dynamics.
- **GAP-07** (Medium): Published graph/load models seldom co-design exogenous limitation covariates (fuel, water, maintenance, temperature anomalies) with spatio-temporal architectures.
- **GAP-08** (Medium): Many conference and metadata-sparse papers lack documented splits, baselines, and ablations needed to benchmark spatio-temporal multi-task methods fairly.

## Competitive positioning (conceptual — no architecture specified)

**Versus univariate forecasters:** Project adds spatial graph coupling, shedding sparsity, and stress assessment beyond scalar load prediction.

**Versus shedding control papers:** Project targets ex-ante daily forecasting for planning, not real-time UFLS or optimisation.

**Versus GNN/GT papers:** Project combines Bangladesh national-grid context, multi-task objectives, and explainability mandate absent in high-relevance comparators.

**Versus XAI papers:** Project embeds explainability in a multi-node, multi-task forecasting setting rather than microgrid control with distillation-only interpretability.

## Phase readiness

- Data & features: Phases 01–06 complete (1,850 rows, 146 validated columns).
- Literature: Phases 07A–07B complete (55 papers, 161 limitations, 110 opportunities).
- Next allowed phase: **Graph Construction** (topology design explicitly deferred).

## Positioning risks (see reviewer_risk_matrix.md)

Primary risks: single-region case study, sparse shedding degeneracy, and architecture incrementalism. Defenses are evidence-linked in gap and novelty matrices.
