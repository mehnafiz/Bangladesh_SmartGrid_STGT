"""Phase 12 — Explainability Design Framework.

Designs the complete XAI framework for PF-STGT covering feature, node, temporal,
graph-attention, and stress attribution. Evaluates SHAP, attention visualization,
and permutation importance; selects the final toolkit.

Does NOT implement models, train models, or modify locked phase outputs.

Inputs (read-only):
    architecture/explainability_design.md
    references/gap_analysis/
    graphs/
    targets/
    experiments/

Outputs:
    explainability/  (6 deliverables)
    results/phases/phase_12_explainability/  (2 reports + method comparison CSV)
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
XAI_DIR = ROOT / "explainability"
REPORT_DIR = ROOT / "results" / "phases" / "phase_12_explainability"
ARCH_DIR = ROOT / "architecture"
GRAPHS_DIR = ROOT / "graphs"
TARGETS_DIR = ROOT / "targets"
GAP_DIR = ROOT / "references" / "gap_analysis"

REGIONS = [
    "Barishal", "Chattogram", "Cumilla", "Dhaka", "Khulna",
    "Mymensingh", "Rajshahi", "Rangpur", "Sylhet",
]

SELECTED_TOOLKIT = "Hybrid XAI Stack (SHAP-primary + Attention-native + Permutation-validation)"
INPUT_WINDOW = 7
N_NODES = 9


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def xai_method_comparison() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "method": "SHAP",
            "interpretability": 5,
            "computational_cost": 2,
            "literature_support": 5,
            "pf_stgt_suitability": 5,
            "multi_task_coverage": 5,
            "total_score": 22,
            "role": "Primary — feature & stress attribution",
            "selected": True,
        },
        {
            "method": "Attention Visualization",
            "interpretability": 4,
            "computational_cost": 5,
            "literature_support": 4,
            "pf_stgt_suitability": 5,
            "multi_task_coverage": 3,
            "total_score": 21,
            "role": "Primary — node, temporal, graph analysis",
            "selected": True,
        },
        {
            "method": "Permutation Importance",
            "interpretability": 4,
            "computational_cost": 3,
            "literature_support": 4,
            "pf_stgt_suitability": 3,
            "multi_task_coverage": 4,
            "total_score": 18,
            "role": "Validation — global sanity check",
            "selected": True,
        },
        {
            "method": "SHAP only (standalone)",
            "interpretability": 5,
            "computational_cost": 2,
            "literature_support": 5,
            "pf_stgt_suitability": 3,
            "multi_task_coverage": 4,
            "total_score": 19,
            "role": "Rejected as sole toolkit — misses native graph/temporal structure",
            "selected": False,
        },
        {
            "method": "Attention only (standalone)",
            "interpretability": 3,
            "computational_cost": 5,
            "literature_support": 3,
            "pf_stgt_suitability": 3,
            "multi_task_coverage": 2,
            "total_score": 16,
            "role": "Rejected as sole toolkit — not faithful attributions (Jain & Wallace 2019)",
            "selected": False,
        },
    ])


def feature_groups_df() -> pd.DataFrame:
    rows = [
        {"group_id": "G1", "group_name": "regional_demand_block", "scope": "node",
         "features": "9 × {Region}_demand", "tasks": "demand;stress", "shap_coalition": True},
        {"group_id": "G2", "group_name": "regional_supply_block", "scope": "node",
         "features": "9 × {Region}_supply", "tasks": "demand", "shap_coalition": True},
        {"group_id": "G3", "group_name": "regional_load_block", "scope": "node",
         "features": "9 × {Region}_load", "tasks": "demand;stress", "shap_coalition": True},
        {"group_id": "G4", "group_name": "engineered_lags_rolling", "scope": "node",
         "features": "demand_lag_1/7, load_lag_1, rolling_mean_7 × 9", "tasks": "demand", "shap_coalition": True},
        {"group_id": "G5", "group_name": "regional_share_intensity", "scope": "node",
         "features": "regional_demand_share, regional_load_intensity × 9", "tasks": "demand;stress", "shap_coalition": True},
        {"group_id": "G6", "group_name": "calendar_trend", "scope": "global",
         "features": "day_of_year_sin/cos, trend_index, gap_days, Holiday_cat", "tasks": "demand;stress", "shap_coalition": True},
        {"group_id": "G7", "group_name": "grid_aggregates", "scope": "global",
         "features": "total_regional_demand, total_regional_load, generation_reserve", "tasks": "demand;stress", "shap_coalition": True},
        {"group_id": "G8", "group_name": "limitation_stack", "scope": "global",
         "features": "gas, coal, water, maintenance limitations, total_operational_limitation", "tasks": "stress;demand", "shap_coalition": True},
        {"group_id": "G9", "group_name": "weather_anomaly", "scope": "global",
         "features": "temperature_anomaly_month", "tasks": "demand", "shap_coalition": True},
        {"group_id": "G10", "group_name": "national_generation_scalars", "scope": "global",
         "features": "Max eve peak gen-end, Highest Generation", "tasks": "demand;stress", "shap_coalition": True},
        {"group_id": "G11", "group_name": "shedding_indicator", "scope": "global",
         "features": "any_regional_shedding", "tasks": "stress", "shap_coalition": True},
    ]
    return pd.DataFrame(rows)


def write_xai_strategy(methods: pd.DataFrame) -> None:
    lines = [
        "# XAI Strategy — Phase 12",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Objective (GAP-05 / NOV-05)",
        "",
        "Provide operator-facing, scientifically defensible explanations for:",
        "",
        "1. **Task 1:** 9-node regional demand forecasts \\( \\hat{D}_r(t+1) \\)",
        "2. **Task 2:** National operational stress \\( \\widehat{OSI}(t+1) \\)",
        "",
        "Only **3/55** papers in Phase 07B corpus report integrated XAI for graph-temporal load models.",
        "",
        "## Selected toolkit",
        "",
        f"**{SELECTED_TOOLKIT}**",
        "",
        "| Layer | Method | Purpose |",
        "| --- | --- | --- |",
        "| Primary A | **SHAP** (GradientSHAP + grouped coalitions) | Feature & stress attribution |",
        "| Primary B | **Attention export** (Graph Transformer + Temporal Encoder) | Node, temporal, graph influence |",
        "| Validation | **Permutation importance** (validation split) | Global feature ranking sanity check |",
        "",
        "## Method evaluation summary",
        "",
        methods.to_markdown(index=False),
        "",
        "**Decision:** No single method covers all five attribution levels. Hybrid stack maximises ",
        "interpretability while keeping computational cost feasible for N=9, T=7.",
        "",
        "## Five-level explainability framework",
        "",
        "| Level | Name | Primary method | Deliverable |",
        "| --- | --- | --- | --- |",
        "| L1 | Feature Attribution | SHAP + Permutation | `shap_design.md` |",
        "| L2 | Node Attribution | SHAP coalitions + spatial attention | `node_importance_design.md` |",
        "| L3 | Temporal Attribution | Temporal attention + SHAP time groups | `attention_analysis_design.md` |",
        "| L4 | Graph Attention Analysis | Spatial attention + hybrid adjacency overlay | `attention_analysis_design.md` |",
        "| L5 | Stress Attribution | SHAP on stress head + OSI component decomposition | `stress_attribution_design.md` |",
        "",
        "## Scope boundaries",
        "",
        "- Explanations computed **post-training** on validation/test case studies.",
        "- **Excluded input:** same-day OSI when explaining OSI(t+1) (Phase 08.5 leakage rule).",
        "- No model implementation in this phase.",
        "",
    ]
    (XAI_DIR / "xai_strategy.md").write_text("\n".join(lines))


def write_shap_design(groups: pd.DataFrame) -> None:
    lines = [
        "# SHAP Design — Phase 12 (Feature Attribution)",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Level 1 — Global & local feature attribution",
        "",
        "### SHAP variant selection",
        "",
        "| Target | SHAP method | Background dataset |",
        "| --- | --- | --- |",
        "| Task 1 demand (per region) | **GradientSHAP** on demand head | 100 train windows (stratified by season) |",
        "| Task 2 OSI | **GradientSHAP** on stress head | 100 train windows (include high/low OSI) |",
        "| Global ranking | **Grouped SHAP** (11 coalitions) | Same background |",
        "",
        "### Feature coalitions (leakage-safe groups)",
        "",
        groups.to_markdown(index=False),
        "",
        "### Output artefacts (implementation phase)",
        "",
        "```",
        "results/explainability/shap/demand_shap_values_{region}.csv",
        "results/explainability/shap/stress_shap_values.csv",
        "results/explainability/shap/global_shap_summary.png",
        "results/explainability/shap/shap_beeswarm_demand_dhaka.png",
        "```",
        "",
        "### Correlation caution (Phase 07B R-05)",
        "",
        "- Report **group-level SHAP** first; then drill to features within top groups.",
        "- Demand≈supply collinearity (Phase 02): interpret G1/G2 jointly, not competitively.",
        "- Use `shap_interaction_values` optionally for Dhaka–national aggregate pairs only.",
        "",
        "### Computational budget",
        "",
        "| Item | Estimate |",
        "| --- | --- |",
        "| Background samples | 100 |",
        "| GradientSHAP steps | 50 per explanation |",
        "| Full val split (~270 windows) | ~2–4 GPU-hours (batched) |",
        "| Case-study subset (20 days) | ~15 min |",
        "",
        "**Publication default:** report SHAP on **20 stratified case-study days** (5 high OSI, 5 low, 5 peak demand, 5 shedding).",
        "",
    ]
    (XAI_DIR / "shap_design.md").write_text("\n".join(lines))


def write_attention_analysis_design() -> None:
    lines = [
        "# Attention Analysis Design — Phase 12",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Level 3 — Temporal attribution",
        "",
        "### Source",
        "",
        "Transformer Encoder self-attention: `attn_temporal` shape `(heads, T, T)` per node (shared weights).",
        "",
        "### Aggregation",
        "",
        "```",
        "α_t = mean_{heads, nodes}( attn_temporal[:, :, t] )   # contribution of day t to forecast",
        "Report top-k days (k=3) for each case study",
        "```",
        "",
        "### Interpretation",
        "",
        "- High weight on t (lag-1 day) expected given autocorr 0.924 (Phase 08.5).",
        "- Weight on t−6…t−7 supports rolling-7 / weekly seasonality (Phase 02).",
        "",
        "## Level 4 — Graph attention analysis",
        "",
        "### Source",
        "",
        "Graph Transformer attention: `attn_spatial` shape `(heads, N, N)` per timestep, averaged over T.",
        "",
        "### Inter-regional influence matrix",
        "",
        "```",
        "I_ij = mean_{heads, t}( attn_spatial[head, i, j, t] )",
        "Overlay on Phase 08 hybrid adjacency A_ij (edge exists if A_ij > 0)",
        "```",
        "",
        "### Validation against graph prior",
        "",
        "- Compute Spearman ρ between I_ij and hybrid edge weights A_ij on existing edges.",
        "- High ρ supports that learned attention aligns with correlation-geographic structure.",
        "",
        "### Visual outputs",
        "",
        "```",
        "results/explainability/attention/spatial_heatmap_{date}.png",
        "results/explainability/attention/temporal_bar_{date}.png",
        "results/explainability/attention/adjacency_attention_overlay.png",
        "results/explainability/attention/influence_matrix.csv",
        "```",
        "",
        "### Limitations (document in paper)",
        "",
        "Attention weights are **explanatory hints**, not guaranteed faithful attributions ",
        "(Jain & Wallace, 2019). Cross-check with SHAP for top features on same case studies.",
        "",
    ]
    (XAI_DIR / "attention_analysis_design.md").write_text("\n".join(lines))


def write_node_importance_design(groups: pd.DataFrame) -> None:
    lines = [
        "# Node Importance Design — Phase 12",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Level 2 — Node-level attribution",
        "",
        "### Regional contribution analysis (Task 1)",
        "",
        "For each forecast day and target region r*, compute:",
        "",
        "1. **SHAP node coalition score:** sum |φ| for groups G1,G3,G4,G5 restricted to node r.",
        "2. **Spatial attention inflow:** Σ_i attn_spatial[i, r*, t] (who influences r*).",
        "3. **Spatial attention outflow:** Σ_j attn_spatial[r*, j, t] (r* influences whom).",
        "",
        "### Node ranking table (per case study)",
        "",
        "| Column | Definition |",
        "| --- | --- |",
        "| `node` | Division name |",
        "| `shap_mass` | Σ\\|φ\\| over node-local features |",
        "| `attention_inflow` | Mean incoming attention |",
        "| `attention_outflow` | Mean outgoing attention |",
        "| `demand_share` | regional_demand_share (context) |",
        "",
        "### Dhaka emphasis",
        "",
        "Always report Dhaka separately (Phase 02: ~35.7% national share); macro rankings can hide hub influence.",
        "",
        "### Regional contribution to national forecast",
        "",
        "```",
        "Contribution_r = shap_mass_r / sum_r shap_mass_r",
        "Compare to demand_share_r for consistency check",
        "```",
        "",
        "### Output",
        "",
        "```",
        "results/explainability/nodes/node_importance_{date}.csv",
        "results/explainability/nodes/regional_contribution_ranking.png",
        "```",
        "",
    ]
    (XAI_DIR / "node_importance_design.md").write_text("\n".join(lines))


def write_stress_attribution_design() -> None:
    lines = [
        "# Stress Attribution Design — Phase 12",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Level 5 — Operational stress attribution",
        "",
        "### Goal (GAP-06)",
        "",
        "Identify drivers of high OSI(t+1) forecasts: shedding intensity, reserve margin, limitation stack.",
        "",
        "### OSI component reference (Phase 05B — for post-hoc decomposition, not model input)",
        "",
        "```",
        "c1 = L_total / D_total           shedding intensity",
        "c2 = 1 - GR / Highest_Gen        reserve margin stress",
        "c3 = TOL / Highest_Gen           limitation stack stress",
        "OSI = mean(minmax(c1), minmax(c2), minmax(c3))",
        "```",
        "",
        "### Dual attribution pathway",
        "",
        "#### Path A — Model-based (SHAP on stress head)",
        "",
        "- Target: OSI_hat(t+1)",
        "- Top SHAP groups expected: G7 (grid), G8 (limitations), G3 (regional load), G11 (shedding flag)",
        "- Report grouped bar chart for high-OSI case studies (top 10% OSI days on validation)",
        "",
        "#### Path B — Component-based (ground-truth decomposition)",
        "",
        "For same case studies, report actual c1,c2,c3 at t+1 to validate model attributions:",
        "",
        "| Component | Physical driver | Expected high-stress signal |",
        "| --- | --- | --- |",
        "| c1 | Load shedding | Mymensingh / sparse _load events (Phase 02) |",
        "| c2 | Low generation reserve | Peak demand days, low GR |",
        "| c3 | Operational limitations | Gas/water/maintenance spikes |",
        "",
        "### Stress driver classification (case study labels)",
        "",
        "```",
        "driver = argmax( minmax(c1), minmax(c2), minmax(c3) ) at t+1",
        "Compare driver to top SHAP group for consistency",
        "```",
        "",
        "### Multi-task link",
        "",
        "- Compare stress SHAP (G7,G8) with demand SHAP on same days.",
        "- Joint high OSI + high demand days → operator alert scenario (Phase 07C positioning).",
        "",
        "### Outputs",
        "",
        "```",
        "results/explainability/stress/stress_shap_grouped_{date}.csv",
        "results/explainability/stress/osi_component_decomposition_{date}.csv",
        "results/explainability/stress/stress_driver_confusion.csv",
        "results/explainability/stress/high_stress_case_study.md",
        "```",
        "",
    ]
    (XAI_DIR / "stress_attribution_design.md").write_text("\n".join(lines))


def write_explainability_protocol(groups: pd.DataFrame) -> None:
    lines = [
        "# Explainability Protocol — Phase 12",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Execution workflow (implementation phase)",
        "",
        "```",
        "1. Train PF-STGT (Phase 10/11) → load best checkpoint",
        "2. Select 20 case-study dates (stratified from validation + test)",
        "3. Export attention maps (spatial + temporal) for each date",
        "4. Compute GradientSHAP for demand (9 regions) and stress (global)",
        "5. Compute permutation importance on validation (global ranking)",
        "6. Cross-validate: SHAP top groups vs permutation top groups (Spearman ρ)",
        "7. Stress: compare SHAP drivers vs OSI c1/c2/c3 decomposition",
        "8. Generate manuscript figures from results/explainability/",
        "```",
        "",
        "## Case-study selection (frozen)",
        "",
        "| Stratum | Count | Selection rule |",
        "| --- | --- | --- |",
        "| High OSI | 5 | Top decile OSI(t+1) on validation |",
        "| Low OSI | 5 | Bottom decile |",
        "| Peak demand | 5 | Top decile total_regional_demand |",
        "| Shedding event | 5 | any_regional_shedding=1 |",
        "",
        "## Attribution levels → methods mapping",
        "",
        "| Level | Method(s) | Metric output |",
        "| --- | --- | --- |",
        "| L1 Feature | SHAP + Permutation | φ values, importance rank |",
        "| L2 Node | SHAP coalitions + spatial attention | node_importance.csv |",
        "| L3 Temporal | Temporal attention | α_t per lag day |",
        "| L4 Graph | Spatial attention + A_ij overlay | influence_matrix.csv |",
        "| L5 Stress | SHAP + c1/c2/c3 decomposition | stress_driver labels |",
        "",
        "## Quality checks",
        "",
        "1. **Leakage audit:** no OSI(t) in SHAP input tensor for OSI(t+1) explanation.",
        "2. **Stability:** bootstrap 10 backgrounds → report SHAP rank correlation > 0.7.",
        "3. **Attention–SHAP agreement:** same top-2 feature groups on ≥60% case studies.",
        "4. **Graph prior alignment:** Spearman(attention, A) > 0.3 on hybrid edges.",
        "",
        "## Manuscript integration (Phase 16 placeholder)",
        "",
        "- Figure: spatial attention heatmap on Bangladesh 9-node layout.",
        "- Figure: SHAP beeswarm for stress (grouped G1–G11).",
        "- Table: stress driver classification vs SHAP top group agreement rate.",
        "",
    ]
    (XAI_DIR / "explainability_protocol.md").write_text("\n".join(lines))


def write_summary(methods: pd.DataFrame, locked_md5: dict[str, str]) -> None:
    lines = [
        "# Phase 12 — Explainability Design Framework Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        f"- Selected toolkit: **{SELECTED_TOOLKIT}**",
        "",
        "## Five attribution levels defined",
        "",
        "| Level | Coverage |",
        "| --- | --- |",
        "| L1 Feature Attribution | SHAP + Permutation |",
        "| L2 Node Attribution | SHAP node coalitions + spatial attention |",
        "| L3 Temporal Attribution | Temporal attention over T=7 |",
        "| L4 Graph Attention | Spatial attention + hybrid adjacency overlay |",
        "| L5 Stress Attribution | SHAP + OSI c1/c2/c3 decomposition |",
        "",
        "## Deliverables",
        "",
        "### explainability/",
        "- xai_strategy.md",
        "- shap_design.md",
        "- attention_analysis_design.md",
        "- node_importance_design.md",
        "- stress_attribution_design.md",
        "- explainability_protocol.md",
        "",
        "### results/phases/phase_12_explainability/",
        "- explainability_summary.md",
        "- explainability_decision_report.md",
        "- xai_method_comparison.csv",
        "",
        "## Scope compliance",
        "",
        "- Explainability framework design only.",
        "- **No model implementation or training.**",
        "- Locked phase outputs not modified.",
        "",
        "## Locked input integrity",
        "",
    ]
    for path, md5 in locked_md5.items():
        lines.append(f"- `{path}` MD5: `{md5}`")
    lines += [
        "",
        "## Status",
        "",
        "Ready for PF-STGT implementation with integrated XAI pipeline (next phase).",
        "",
    ]
    (REPORT_DIR / "explainability_summary.md").write_text("\n".join(lines))


def write_decision_report(methods: pd.DataFrame) -> None:
    selected = methods[methods["selected"] & ~methods["method"].str.contains("only")]
    lines = [
        "# Explainability Decision Report — Phase 12",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Selected toolkit",
        "",
        f"**{SELECTED_TOOLKIT}**",
        "",
        selected[["method", "total_score", "role"]].to_markdown(index=False),
        "",
        "## Why hybrid over single-method?",
        "",
        "### SHAP alone (rejected as sole toolkit)",
        "- Strong feature attribution and literature support (NOV-05, 1/55 dedicated SHAP paper).",
        "- Misses native graph/temporal structure exposed by PF-STGT architecture (Phase 09).",
        "- Expensive for full graph-temporal DeepSHAP on entire model.",
        "",
        "### Attention alone (rejected as sole toolkit)",
        "- Zero marginal cost at inference; ideal for node/temporal/graph levels.",
        "- Attention ≠ explanation (Jain & Wallace 2019); insufficient for operator-grade stress claims.",
        "",
        "### Permutation alone (rejected as sole toolkit)",
        "- Good global validation; ignores temporal window structure and graph dependencies.",
        "- Model-agnostic but expensive and high-variance on small validation set (277 rows).",
        "",
        "## Gap alignment",
        "",
        "| Gap | Framework response |",
        "| --- | --- |",
        "| GAP-05 | SHAP + attention integrated across both tasks |",
        "| GAP-06 | Stress attribution via SHAP + c1/c2/c3 decomposition |",
        "| GAP-07 | 11 feature coalitions map to Phase 05B groups |",
        "| GAP-02 | Separate demand vs stress explanation paths |",
        "",
    ]
    (REPORT_DIR / "explainability_decision_report.md").write_text("\n".join(lines))


def main() -> None:
    XAI_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    locked_paths = {
        "architecture/explainability_design.md": ARCH_DIR / "explainability_design.md",
        "graphs/adjacency_matrix.csv": GRAPHS_DIR / "adjacency_matrix.csv",
        "targets/multitask_formulation.md": TARGETS_DIR / "multitask_formulation.md",
        "references/gap_analysis/research_gap_matrix.csv": GAP_DIR / "research_gap_matrix.csv",
    }
    locked_md5 = {k: file_md5(v) for k, v in locked_paths.items()}

    methods = xai_method_comparison()
    groups = feature_groups_df()

    methods.to_csv(REPORT_DIR / "xai_method_comparison.csv", index=False)
    groups.to_csv(REPORT_DIR / "feature_coalition_registry.csv", index=False)

    write_xai_strategy(methods)
    write_shap_design(groups)
    write_attention_analysis_design()
    write_node_importance_design(groups)
    write_stress_attribution_design()
    write_explainability_protocol(groups)
    write_summary(methods, locked_md5)
    write_decision_report(methods)

    print("Phase 12 explainability design framework complete.")
    print(f"Toolkit: {SELECTED_TOOLKIT}")
    print(f"Reports -> {XAI_DIR.relative_to(ROOT)} , {REPORT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
