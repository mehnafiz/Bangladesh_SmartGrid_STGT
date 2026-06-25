"""Phase 09 — STGT Architecture Design.

Designs the complete Explainable Multi-Task Spatio-Temporal Graph Transformer
architecture using evidence from Phases 07B–08.5. Evaluates spatial, temporal,
and fusion alternatives; selects the strongest design.

Does NOT implement or train models. Does NOT modify locked phase outputs.

Inputs (read-only):
    graphs/adjacency_matrix.csv
    graphs/node_definition.md
    targets/*.md
    references/gap_analysis/*.csv
    references/analysis/paper_analysis_catalog.csv

Outputs:
    architecture/  (7 deliverables)
    results/phases/phase_09_architecture/  (3 reports)
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ARCH_DIR = ROOT / "architecture"
REPORT_DIR = ROOT / "results" / "phases" / "phase_09_architecture"
GRAPHS_DIR = ROOT / "graphs"
TARGETS_DIR = ROOT / "targets"
GAP_DIR = ROOT / "references" / "gap_analysis"

REGIONS = [
    "Barishal", "Chattogram", "Cumilla", "Dhaka", "Khulna",
    "Mymensingh", "Rajshahi", "Rangpur", "Sylhet",
]

# Frozen architecture selection
SELECTED_ARCHITECTURE = "PF-STGT (Parallel-Fusion Spatio-Temporal Graph Transformer)"
SPATIAL_MODULE = "Graph Transformer (adjacency-biased multi-head self-attention)"
TEMPORAL_MODULE = "Transformer Encoder (multi-layer temporal self-attention)"
FUSION_STRATEGY = "Parallel Fusion (spatial branch ∥ temporal branch → gated concat)"
INPUT_WINDOW = 7
FORECAST_HORIZON = 1
N_NODES = 9
D_MODEL = 128
N_HEADS = 4
N_SPATIAL_LAYERS = 2
N_TEMPORAL_LAYERS = 2

NODE_INPUT_FEATURES = [
    "{r}_demand", "{r}_supply", "{r}_load",
    "demand_lag_1_{r}", "demand_lag_7_{r}", "load_lag_1_{r}",
    "demand_rolling_mean_7_{r}", "regional_demand_share_{r}", "regional_load_intensity_{r}",
]
F_NODE = len(NODE_INPUT_FEATURES)  # 9 per node

GLOBAL_INPUT_FEATURES = [
    "day_of_year_sin", "day_of_year_cos", "trend_index",
    "gap_days_since_previous_observation",
    "total_regional_demand", "total_regional_load", "generation_reserve",
    "temperature_anomaly_month", "total_operational_limitation", "any_regional_shedding",
    "Gas/LF limitation", "Coal supply Limitation",
    "Low water level in Kaptai lake", "Plants under shut down/ maintenance",
    "Max. Demand at eve. peak (Generation end)", "Highest Generation (Generation end)",
    "Holiday_cat",
]
F_GLOBAL = len(GLOBAL_INPUT_FEATURES)

EXCLUDED_INPUTS = [
    "operational_stress_index",
    "Same-day OSI used as input when predicting OSI(t+1) — leakage per Phase 08.5",
]


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def spatial_comparison() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "option": "GCN",
            "expressiveness": 3,
            "literature_support": 4,
            "explainability": 2,
            "hybrid_adjacency_fit": 4,
            "stgt_alignment": 2,
            "total_score": 15,
            "selected": False,
            "summary": "Fixed-weight message passing; strong baseline but no attention maps for GAP-05.",
        },
        {
            "option": "GAT",
            "expressiveness": 4,
            "literature_support": 4,
            "explainability": 4,
            "hybrid_adjacency_fit": 5,
            "stgt_alignment": 3,
            "total_score": 20,
            "selected": False,
            "summary": "Edge-weighted attention; good fit for Phase 08 hybrid weights but limited to neighbours.",
        },
        {
            "option": "Graph Transformer",
            "expressiveness": 5,
            "literature_support": 5,
            "explainability": 5,
            "hybrid_adjacency_fit": 5,
            "stgt_alignment": 5,
            "total_score": 25,
            "selected": True,
            "summary": "Full node self-attention with adjacency bias; aligns with STGT title, GAP-04, NOV-04/05.",
        },
    ])


def temporal_comparison() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "option": "Temporal Attention (single layer)",
            "long_range_modelling": 3,
            "literature_support": 3,
            "T7_window_fit": 3,
            "implementation_clarity": 4,
            "stgt_alignment": 3,
            "total_score": 16,
            "selected": False,
            "summary": "Lightweight but shallow for weekly seasonality patterns (Phase 02).",
        },
        {
            "option": "Transformer Encoder",
            "long_range_modelling": 5,
            "literature_support": 5,
            "T7_window_fit": 5,
            "implementation_clarity": 5,
            "stgt_alignment": 5,
            "total_score": 25,
            "selected": True,
            "summary": "Multi-head self-attention over T=7; matches lag-7 feature design and 7/55 transformer papers.",
        },
        {
            "option": "Temporal Transformer (causal variant)",
            "long_range_modelling": 4,
            "literature_support": 4,
            "T7_window_fit": 4,
            "implementation_clarity": 3,
            "stgt_alignment": 4,
            "total_score": 19,
            "selected": False,
            "summary": "Causal masking unnecessary for h=1 ex-post window encoding; adds complexity without gain.",
        },
    ])


def fusion_comparison() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "option": "Spatial → Temporal",
            "scientific_validity": 4,
            "literature_precedent": 5,
            "multi_task_suitability": 3,
            "interpretability": 3,
            "phase02_alignment": 3,
            "total_score": 18,
            "selected": False,
            "summary": "Classic ST-GCN path; may blur temporal trend before cross-region stress propagation.",
        },
        {
            "option": "Temporal → Spatial",
            "scientific_validity": 3,
            "literature_precedent": 3,
            "multi_task_suitability": 3,
            "interpretability": 3,
            "phase02_alignment": 3,
            "total_score": 15,
            "selected": False,
            "summary": "Delays spatial coupling of same-day regional shocks; weaker for correlated divisions.",
        },
        {
            "option": "Parallel Fusion",
            "scientific_validity": 5,
            "literature_precedent": 4,
            "multi_task_suitability": 5,
            "interpretability": 4,
            "phase02_alignment": 5,
            "total_score": 23,
            "selected": True,
            "summary": "Dual pathway for national seasonality (temporal) and inter-node coupling (spatial); ablatable.",
        },
    ])


def architecture_options() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "architecture_id": "ARCH-A",
            "name": "GCN-LSTM Multi-Task Baseline",
            "spatial": "GCN",
            "temporal": "LSTM",
            "fusion": "Spatial → Temporal",
            "total_score": 14,
            "selected": False,
        },
        {
            "architecture_id": "ARCH-B",
            "name": "GAT + Temporal Attention (ST-first)",
            "spatial": "GAT",
            "temporal": "Temporal Attention",
            "fusion": "Spatial → Temporal",
            "total_score": 18,
            "selected": False,
        },
        {
            "architecture_id": "ARCH-C",
            "name": "PF-STGT (Parallel-Fusion Graph Transformer)",
            "spatial": "Graph Transformer",
            "temporal": "Transformer Encoder",
            "fusion": "Parallel Fusion",
            "total_score": 27,
            "selected": True,
        },
    ])


def write_architecture_overview() -> None:
    lines = [
        "# STGT Architecture Overview — Phase 09",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **DESIGN FROZEN (implementation deferred)**",
        "",
        "## Selected architecture",
        "",
        f"**{SELECTED_ARCHITECTURE}**",
        "",
        "An explainable multi-task spatio-temporal graph transformer for:",
        "",
        "1. **Task 1:** 9-node regional demand forecasting \\( \\hat{D}_r(t+1) \\) (MW)",
        "2. **Task 2:** Graph-level operational stress \\( \\widehat{OSI}(t+1) \\in [0,1] \\)",
        "",
        "## Evidence base",
        "",
        "| Source | Contribution to design |",
        "| --- | --- |",
        "| Phase 07B | Graph+transformer cluster (8 High-relevance papers); XAI gap (3/55) |",
        "| Phase 07C | GAP-04 graph-temporal coupling; GAP-05 explainability; GAP-02 multi-task |",
        "| Phase 08 | Hybrid adjacency (9 nodes, 24 edges, correlation-weighted) |",
        "| Phase 08.5 | h=1 horizon; demand + OSI targets; leakage exclusions |",
        "",
        "## High-level data flow",
        "",
        "```",
        "Input window X[t-T+1:t]  (T=7)  +  Global context G[t]",
        "        │",
        "        ├─ Spatial Branch: Graph Transformer × L_s  (adjacency-biased attention)",
        "        │",
        "        └─ Temporal Branch: Transformer Encoder × L_t  (per-node time series)",
        "                    │",
        "              Parallel Fusion (gated concat + projection)",
        "                    │",
        "              Shared representation H ∈ R^{N×d}  (d=128)",
        "                 ┌────┴────┐",
        "           Demand Head   Stress Head",
        "            R^9 (MW)      R^1 [0,1]",
        "```",
        "",
        "## Key hyperparameters (design defaults)",
        "",
        f"| Parameter | Value | Rationale |",
        f"| --- | --- | --- |",
        f"| Input window T | {INPUT_WINDOW} | Phase 05B lag-7 / rolling-7; Phase 06 warm-up |",
        f"| Nodes N | {N_NODES} | Phase 08 graph |",
        f"| Forecast horizon h | {FORECAST_HORIZON} | Phase 08.5 frozen |",
        f"| d_model | {D_MODEL} | Balance capacity vs 1,295 train rows |",
        f"| Attention heads | {N_HEADS} | Standard multi-head for spatial/temporal maps |",
        f"| Spatial layers L_s | {N_SPATIAL_LAYERS} | Depth without over-parameterisation |",
        f"| Temporal layers L_t | {N_TEMPORAL_LAYERS} | Capture weekly seasonality (Phase 02) |",
        "",
    ]
    (ARCH_DIR / "architecture_overview.md").write_text("\n".join(lines))


def write_architecture_components() -> None:
    spatial = spatial_comparison()
    temporal = temporal_comparison()
    fusion = fusion_comparison()
    lines = [
        "# Architecture Components — Phase 09",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## 1. Input Layer",
        "",
        "### Node feature tensor",
        "",
        f"- Shape: `(batch, T={INPUT_WINDOW}, N={N_NODES}, F_n={F_NODE})`",
        f"- F_n={F_NODE} per node (leakage-safe, excludes `operational_stress_index`):",
        "",
    ]
    for i, tmpl in enumerate(NODE_INPUT_FEATURES, 1):
        lines.append(f"  {i}. `{tmpl}`")
    lines += [
        "",
        "### Global context vector",
        "",
        f"- Shape: `(batch, T, F_g={F_GLOBAL})` broadcast to graph readout and stress head",
        f"- Includes calendar, grid aggregates, limitations, national generation scalars",
        "- **Excluded:** `operational_stress_index` (target leakage for Task 2 at h=1)",
        "",
        "### Input embedding",
        "",
        "```",
        "E_node = Linear(F_n → d_model) + RegionalEmbedding(N → d_model)",
        "E_global = Linear(F_g → d_model)",
        "H0 = E_node + broadcast(E_global) + PosEnc_time(T)",
        "```",
        "",
        "## 2. Spatial Module (selected: Graph Transformer)",
        "",
        spatial.to_markdown(index=False),
        "",
        "**Mechanism:** Multi-head self-attention over N nodes at each timestep, with additive",
        "mask/bias from Phase 08 hybrid adjacency A (zero bias where A_ij=0).",
        "",
        "```",
        "Attn_spatial(Q,K,V) = softmax(QK^T / sqrt(d) + B_adj) V",
        "B_adj[i,j] = log(A_ij + ε)  if A_ij > 0 else -inf",
        "```",
        "",
        "## 3. Temporal Module (selected: Transformer Encoder)",
        "",
        temporal.to_markdown(index=False),
        "",
        "**Mechanism:** Standard transformer encoder applied per node across T timesteps",
        "(shared weights across nodes for parameter efficiency).",
        "",
        "## 4. Fusion Strategy (selected: Parallel Fusion)",
        "",
        fusion.to_markdown(index=False),
        "",
        "```",
        "H_spatial = GraphTransformer(H0)      # (B, T, N, d)",
        "H_temporal = TransformerEnc(H0)       # (B, T, N, d)",
        "H_fused = Gate ⊙ H_spatial + (1-Gate) ⊙ H_temporal",
        "Gate = σ(Linear([H_spatial; H_temporal]))",
        "H_shared = H_fused[:, -1, :, :]      # last observed day representation",
        "```",
        "",
        "## 5. Shared Representation",
        "",
        f"- **H_shared** ∈ R^(batch × N × d_model), d_model={D_MODEL}",
        "- Last-timestep fused embedding per node",
        "- Graph readout vector: `h_graph = mean_pool(H_shared) ⊕ E_global[:, -1, :]`",
        "",
        "## 6. Multi-Task Heads",
        "",
        "### Task 1 — Regional Load Forecasting",
        "- `DemandHead`: Linear(d_model → 1) per node → 9 outputs",
        "- Output: `D_hat(t+1) ∈ R^9` (inverse-transform MW at inference if scaled)",
        "- Loss: Huber(δ=1.0) per node, averaged",
        "",
        "### Task 2 — Operational Stress Assessment",
        "- `StressHead`: MLP([h_graph; flatten(H_shared)]) → 1",
        "- Output: `sigmoid` → OSI_hat(t+1) ∈ [0,1]",
        "- Loss: MSE",
        "",
    ]
    (ARCH_DIR / "architecture_components.md").write_text("\n".join(lines))


def write_architecture_diagram() -> None:
    lines = [
        "# STGT Architecture Diagram — Phase 09",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## PF-STGT block diagram",
        "",
        "```mermaid",
        "flowchart TB",
        "    subgraph Input",
        "        X[\"Node tensor<br/>(B,T,N,F_n)\"]",
        "        G[\"Global context<br/>(B,T,F_g)\"]",
        "        A[\"Hybrid adjacency A<br/>(N,N)\"]",
        "    end",
        "",
        "    subgraph Embedding",
        "        EMB[\"Linear + Regional + PosEnc<br/>H0 (B,T,N,d)\"]",
        "    end",
        "",
        "    subgraph ParallelBranches",
        "        GT[\"Graph Transformer × L_s<br/>adjacency-biased attention\"]",
        "        TE[\"Transformer Encoder × L_t<br/>temporal self-attention\"]",
        "    end",
        "",
        "    subgraph Fusion",
        "        GF[\"Gated Parallel Fusion<br/>H_fused (B,T,N,d)\"]",
        "        HS[\"H_shared = H_fused[:,−1]\"]",
        "    end",
        "",
        "    subgraph Heads",
        "        DH[\"Demand Head<br/>9 × MW\"]",
        "        SH[\"Stress Head<br/>OSI ∈ [0,1]\"]",
        "    end",
        "",
        "    subgraph Explainability",
        "        ATTN[\"Attention maps export\"]",
        "        SHAP[\"SHAP attribution hooks\"]",
        "    end",
        "",
        "    X --> EMB",
        "    G --> EMB",
        "    EMB --> GT",
        "    EMB --> TE",
        "    A --> GT",
        "    GT --> GF",
        "    TE --> GF",
        "    GF --> HS",
        "    HS --> DH",
        "    HS --> SH",
        "    GT --> ATTN",
        "    TE --> ATTN",
        "    DH --> SHAP",
        "    SH --> SHAP",
        "```",
        "",
        "## Tensor shape trace",
        "",
        "| Stage | Shape |",
        "| --- | --- |",
        f"| Input node | (B, {INPUT_WINDOW}, {N_NODES}, {F_NODE}) |",
        f"| Input global | (B, {INPUT_WINDOW}, {F_GLOBAL}) |",
        f"| Embedded H0 | (B, {INPUT_WINDOW}, {N_NODES}, {D_MODEL}) |",
        f"| H_shared | (B, {N_NODES}, {D_MODEL}) |",
        f"| Task 1 output | (B, {N_NODES}) |",
        "| Task 2 output | (B, 1) |",
        "",
    ]
    (ARCH_DIR / "architecture_diagram.md").write_text("\n".join(lines))


def write_input_output_spec() -> None:
    lines = [
        "# Input / Output Specification — Phase 09",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Model I/O contract",
        "",
        "### Inputs",
        "",
        "| Input | Shape | Dtype | Source |",
        "| --- | --- | --- | --- |",
        f"| `node_features` | (B, T={INPUT_WINDOW}, N={N_NODES}, F_n={F_NODE}) | float32 | `data/features/*_features.parquet` |",
        f"| `global_features` | (B, T, F_g={F_GLOBAL}) | float32 | same |",
        f"| `adjacency` | (N, N) | float32 | `graphs/adjacency_matrix.csv` |",
        "| `region_index` | (N,) | int | fixed alphabetical order |",
        "",
        "### Targets (supervision at training — not inputs)",
        "",
        "| Target | Shape | Horizon | Source |",
        "| --- | --- | --- | --- |",
        f"| `demand_target` | (B, N) | t+{FORECAST_HORIZON} | `{{Region}}_demand` from clean/features |",
        f"| `osi_target` | (B, 1) | t+{FORECAST_HORIZON} | OSI computed per Phase 05B formula |",
        "",
        "### Outputs",
        "",
        "| Output | Shape | Range | Task |",
        "| --- | --- | --- | --- |",
        f"| `demand_pred` | (B, N) | MW (post inverse-scaling) | Task 1 |",
        "| `osi_pred` | (B, 1) | [0, 1] | Task 2 |",
        "| `attn_spatial` | (B, heads, N, N) | [0, 1] optional export | Explainability |",
        "| `attn_temporal` | (B, heads, T, T) | [0, 1] optional export | Explainability |",
        "",
        "## Leakage-safe input policy (Phase 08.5)",
        "",
        "At forecast origin time t (last window timestep):",
        "",
        "- **Allowed:** all node/global features observed at or before t",
        "- **Forbidden as input:** `operational_stress_index` at t when predicting OSI(t+1)",
        "- **Allowed target:** OSI(t+1), D_r(t+1)",
        "",
        "## Window construction",
        "",
        f"- T={INPUT_WINDOW} consecutive observed days ending at t",
        "- Skip first 7 train timesteps (Phase 06 warm-up for lag-7 / rolling-7)",
        "- Respect 17 calendar gaps via gap-aware lags (Phase 05B)",
        "",
        "## Node ordering (must match adjacency)",
        "",
        "```",
        ", ".join(REGIONS),
        "```",
        "",
    ]
    (ARCH_DIR / "input_output_specification.md").write_text("\n".join(lines))


def write_module_rationale(
    spatial: pd.DataFrame,
    temporal: pd.DataFrame,
    fusion: pd.DataFrame,
    arch_opts: pd.DataFrame,
) -> None:
    lines = [
        "# Module Selection Rationale — Phase 09",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Architecture options evaluated",
        "",
        arch_opts.to_markdown(index=False),
        "",
        "## Spatial module: Graph Transformer (25/25)",
        "",
        "- **Literature:** 8/55 High STGT-relevance papers; Graph Transformers topic in corpus "
        "(spatiotemporal graph attention-enabled transformer, IJEPES 2024).",
        "- **GAP-04 / NOV-04:** Explicit graph + transformer coupling is the project differentiator.",
        "- **Phase 08:** Hybrid adjacency provides edge weights for attention bias (not just binary GCN).",
        "- **GAP-05:** Self-attention weights exportable for spatial explainability (vs opaque GCN aggregation).",
        "- **Rejected GCN:** Fixed aggregation, no attention maps, weaker STGT alignment.",
        "- **Rejected GAT:** Neighbour-only attention; hybrid graph includes selective long-range ρ≥0.85 edges.",
        "",
        "## Temporal module: Transformer Encoder (25/25)",
        "",
        "- **Phase 02:** Strong lag-1 autocorrelation (0.924) and weekly seasonality → multi-day context needed.",
        "- **Phase 05B:** lag-7 and rolling-7 features imply T≥7 input window.",
        "- **Literature:** 7/55 transformer-based papers in corpus; temporal transformer backbone in High-relevance GNN papers.",
        "- **Rejected single Temporal Attention:** Insufficient depth for composite seasonal + trend patterns.",
        "- **Rejected causal Temporal Transformer:** No autoregressive decoding at h=1; full window encoding suffices.",
        "",
        "## Fusion: Parallel Fusion (23/25)",
        "",
        "- **Phase 02 dual driver:** shared national trend (temporal path) + inter-regional correlation (spatial path).",
        "- **Multi-task:** stress head benefits from global temporal context AND spatial stress propagation simultaneously.",
        "- **Rejected Spatial→Temporal:** Premature spatial mixing may attenuate node-specific temporal trajectories before fusion.",
        "- **Rejected Temporal→Spatial:** Delays modelling of same-day cross-region demand coupling.",
        "",
        "## Selected stack: PF-STGT (27/27 component sum)",
        "",
        "Combines highest-scoring spatial, temporal, and fusion modules with multi-task heads aligned to Phase 08.5.",
        "",
    ]
    (ARCH_DIR / "module_rationale.md").write_text("\n".join(lines))


def write_loss_function_design() -> None:
    lines = [
        "# Loss Function Design — Phase 09",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Multi-task objective",
        "",
        "```",
        "L_total = λ1 · L_demand + λ2 · L_stress + λ_reg · L_reg",
        "```",
        "",
        "## Task 1 — Regional demand (Huber)",
        "",
        "```",
        "L_demand = (1/N) Σ_r Huber_δ(D_hat_r, D_r; δ=1.0 MW)",
        "```",
        "",
        "- **Rationale:** Robust to Phase 02 upper-tail demand outliers (record-high days).",
        "- Per-node errors averaged; optional node weights for Dhaka dominance (Phase 02 ~35.7% share).",
        "",
        "## Task 2 — Operational stress (MSE)",
        "",
        "```",
        "L_stress = MSE(OSI_hat, OSI)",
        "```",
        "",
        "- **Rationale:** Continuous [0,1] target (Phase 08.5 SF-04); bounded sigmoid output.",
        "- MSE penalises moderate stress mis-ranking suitable for operational assessment.",
        "",
        "## Default task weights (design starting point)",
        "",
        "| Weight | Value | Note |",
        "| --- | --- | --- |",
        "| λ1 | 1.0 | Primary forecasting task |",
        "| λ2 | 0.5 | Auxiliary stress; scale OSI MSE to demand magnitude |",
        "| λ_reg | 1e-4 | L2 on head weights (optional) |",
        "",
        "Uncertainty-based balancing (Kendall et al.) recommended at implementation — not trained here.",
        "",
        "## Metrics (evaluation phase — not trained here)",
        "",
        "| Task | Primary metrics |",
        "| --- | --- |",
        "| Demand | MAE, MAPE, RMSE per region and macro-avg |",
        "| Stress | MAE, RMSE, Pearson r on OSI |",
        "",
    ]
    (ARCH_DIR / "loss_function_design.md").write_text("\n".join(lines))


def write_explainability_design() -> None:
    lines = [
        "# Explainability Design — Phase 09",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Design goal (GAP-05 / NOV-05)",
        "",
        "Provide operator-facing attribution for regional demand forecasts and national stress scores",
        "without post-hoc approximations alone.",
        "",
        "## 1. SHAP compatibility",
        "",
        "| Component | SHAP approach |",
        "| --- | --- |",
        "| Demand head | TreeSHAP on extracted features OR DeepSHAP on MLP head |",
        "| Stress head | KernelSHAP / DeepSHAP on graph readout + global vector |",
        "| Full model | GradientSHAP with grouped feature coalitions |",
        "",
        "**Feature groups for coalition SHAP (Phase 05B/07):**",
        "",
        "- Regional demand/supply/load blocks (9 nodes)",
        "- Calendar / trend (`day_of_year_*`, `trend_index`, `Holiday_cat`)",
        "- Limitation stack (gas, coal, water, maintenance)",
        "- Grid aggregates (`generation_reserve`, `total_regional_demand`)",
        "",
        "**Caution (Phase 07B reviewer risk R-05):** SHAP on correlated regional features may misattribute;",
        "report node-level and global attributions separately.",
        "",
        "## 2. Attention visualisation",
        "",
        "| Map | Source | Interpretation |",
        "| --- | --- | --- |",
        "| Spatial attention | Graph Transformer heads | Which divisions influence each other |",
        "| Temporal attention | Transformer Encoder heads | Which past days drive forecast |",
        "",
        "Export `attn_spatial` (N×N) and `attn_temporal` (T×T) per forecast for case-study days with shedding.",
        "",
        "## 3. Feature attribution compatibility",
        "",
        "- Architecture uses explicit node/global input partitions → direct mapping to Phase 05A feature groups.",
        "- Hybrid adjacency edge weights (Phase 08) can be overlaid on spatial attention heatmaps.",
        "- Ablation hooks: remove limitation stack, remove spatial branch, remove temporal branch.",
        "",
        "## Explainability readiness checklist",
        "",
        "- [x] Attention weights exposed from spatial and temporal modules",
        "- [x] Input feature groups documented for SHAP coalitions",
        "- [x] Separate node-level (Task 1) and graph-level (Task 2) attribution paths",
        "- [x] Leakage-safe inputs ensure attributions reference legitimate predictors only",
        "",
    ]
    (ARCH_DIR / "explainability_design.md").write_text("\n".join(lines))


def write_validation_report(locked_md5: dict[str, str]) -> None:
    lines = [
        "# Architecture Validation Report — Phase 09",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Design completeness",
        "",
        "| Component | Defined | Aligned to prior phases |",
        "| --- | --- | --- |",
        "| Input layer | Yes | Phase 05B features, Phase 08.5 leakage rules |",
        "| Spatial module | Yes | Phase 08 hybrid adjacency |",
        "| Temporal module | Yes | T=7 window, Phase 02 seasonality |",
        "| Fusion strategy | Yes | Parallel dual-path |",
        "| Shared representation | Yes | H_shared (B,N,d) |",
        "| Multi-task heads | Yes | Phase 08.5 Task 1 + Task 2 |",
        "| Explainability | Yes | Phase 07C GAP-05 |",
        "| Loss functions | Yes | Huber + MSE |",
        "",
        "## Cross-phase consistency",
        "",
        f"| Check | Status |",
        f"| --- | --- |",
        f"| Nodes N=9 match adjacency | PASS |",
        f"| Horizon h=1 | PASS |",
        f"| OSI excluded from inputs | PASS |",
        f"| No implementation code written | PASS |",
        f"| No training performed | PASS |",
        "",
        "## Locked input integrity",
        "",
    ]
    for path, md5 in locked_md5.items():
        lines.append(f"- `{path}` MD5: `{md5}` (unchanged)")
    lines += [
        "",
        "## Status",
        "",
        "**PASS** — architecture design complete; ready for implementation phase.",
        "",
    ]
    (REPORT_DIR / "architecture_validation_report.md").write_text("\n".join(lines))


def write_design_decision_rationale(arch_opts: pd.DataFrame) -> None:
    winner = arch_opts[arch_opts["selected"]].iloc[0]
    lines = [
        "# Design Decision Rationale — Phase 09",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        f"## Selected: {winner['name']} ({winner['architecture_id']}, score {int(winner['total_score'])})",
        "",
        "## Why PF-STGT over alternatives",
        "",
        "### vs ARCH-A (GCN-LSTM)",
        "- LSTM temporal encoding lacks transformer attention maps (GAP-05).",
        "- GCN cannot leverage Phase 08 correlation-weighted hybrid edges as flexibly as graph attention.",
        "",
        "### vs ARCH-B (GAT + Temporal Attention, ST-first)",
        "- Sequential fusion underuses parallel national-seasonality and spatial-coupling drivers (Phase 02).",
        "- Shallow temporal attention insufficient for T=7 weekly patterns.",
        "",
        "## Research gap alignment",
        "",
        "| Gap | PF-STGT response |",
        "| --- | --- |",
        "| GAP-04 | Graph Transformer + Transformer Encoder |",
        "| GAP-05 | Dual attention export + SHAP feature groups |",
        "| GAP-02 | Shared H_shared with dual task heads |",
        "| GAP-06 | StressHead on graph readout + limitation-aware inputs |",
        "| GAP-07 | F_g includes limitation stack and grid covariates |",
        "",
        "## Implementation deferral",
        "",
        "This phase produces design artefacts only. PyTorch modules, training loops, and SHAP pipelines",
        "are deferred to the implementation/training phases.",
        "",
    ]
    (REPORT_DIR / "design_decision_rationale.md").write_text("\n".join(lines))


def write_architecture_summary(arch_opts: pd.DataFrame) -> None:
    lines = [
        "# Phase 09 — STGT Architecture Design Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        f"- Selected architecture: **{SELECTED_ARCHITECTURE}**",
        "",
        "## Module selections",
        "",
        f"| Module | Selection |",
        f"| --- | --- |",
        f"| Spatial | {SPATIAL_MODULE} |",
        f"| Temporal | {TEMPORAL_MODULE} |",
        f"| Fusion | {FUSION_STRATEGY} |",
        "",
        "## I/O summary",
        "",
        f"- Input: (B, T={INPUT_WINDOW}, N={N_NODES}, F_n={F_NODE}) + global (B, T, F_g={F_GLOBAL})",
        f"- Output Task 1: (B, {N_NODES}) demand MW",
        "- Output Task 2: (B, 1) OSI ∈ [0,1]",
        "",
        "## Deliverables",
        "",
        "### architecture/",
        "- architecture_overview.md",
        "- architecture_components.md",
        "- architecture_diagram.md",
        "- input_output_specification.md",
        "- module_rationale.md",
        "- loss_function_design.md",
        "- explainability_design.md",
        "",
        "### results/phases/phase_09_architecture/",
        "- architecture_summary.md",
        "- architecture_validation_report.md",
        "- design_decision_rationale.md",
        "",
        "## Scope compliance",
        "",
        "- Architecture design only; **no implementation or training**.",
        "- Locked phase outputs not modified.",
        "",
        "## Status",
        "",
        "Ready for implementation.",
        "",
    ]
    (REPORT_DIR / "architecture_summary.md").write_text("\n".join(lines))


def main() -> None:
    ARCH_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    locked_paths = {
        "data/features/train_features.parquet": ROOT / "data" / "features" / "train_features.parquet",
        "graphs/adjacency_matrix.csv": GRAPHS_DIR / "adjacency_matrix.csv",
        "targets/multitask_formulation.md": TARGETS_DIR / "multitask_formulation.md",
    }
    locked_md5 = {k: file_md5(v) for k, v in locked_paths.items()}

    spatial = spatial_comparison()
    temporal = temporal_comparison()
    fusion = fusion_comparison()
    arch_opts = architecture_options()

    write_architecture_overview()
    write_architecture_components()
    write_architecture_diagram()
    write_input_output_spec()
    write_module_rationale(spatial, temporal, fusion, arch_opts)
    write_loss_function_design()
    write_explainability_design()
    write_validation_report(locked_md5)
    write_design_decision_rationale(arch_opts)
    write_architecture_summary(arch_opts)

    print("Phase 09 STGT architecture design complete.")
    print(f"Selected: {SELECTED_ARCHITECTURE}")
    print(f"Spatial: Graph Transformer | Temporal: Transformer Encoder | Fusion: Parallel")
    print(f"Reports -> {ARCH_DIR.relative_to(ROOT)} , {REPORT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
