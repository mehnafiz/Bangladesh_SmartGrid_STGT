"""Phase 13 — Ablation Studies Design.

Designs the complete ablation framework for PF-STGT: component removal,
hybrid graph, multi-task, and explainability studies with evaluation and
statistical significance protocols.

Does NOT implement models, train models, or modify locked phase outputs.

Inputs (read-only):
    architecture/, graphs/, targets/, experiments/, optimization/, explainability/

Outputs:
    ablation/  (4 deliverables)
    results/phases/phase_13_ablation/  (2 reports)
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ABL_DIR = ROOT / "ablation"
REPORT_DIR = ROOT / "results" / "phases" / "phase_13_ablation"

PRIMARY_SEED = 42
CONFIRMATION_SEEDS = [42, 123, 456]
ALPHA = 0.05
N_COMPARISONS = 5  # Bonferroni vs A1 for core A2–A6


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ablation_matrix() -> pd.DataFrame:
    rows = [
        # ── Reference ──
        {
            "ablation_id": "A1",
            "study_category": "reference",
            "variant_name": "PF-STGT Full Model",
            "graph_adjacency": "Hybrid (Phase 08)",
            "spatial_branch": True,
            "temporal_branch": True,
            "fusion": "Parallel gated",
            "multi_task": True,
            "attention_export": True,
            "structural_change": "None — reference model",
            "hypothesis": "Best overall demand + stress performance",
            "seeds": "42, 123, 456",
            "priority": "Required",
        },
        # ── Component removal (A2–A3) ──
        {
            "ablation_id": "A2",
            "study_category": "component_removal",
            "variant_name": "Without Graph Module",
            "graph_adjacency": "None (identity / no message passing)",
            "spatial_branch": False,
            "temporal_branch": True,
            "fusion": "Temporal-only passthrough",
            "multi_task": True,
            "attention_export": "Temporal only",
            "structural_change": "Remove Graph Transformer; disable spatial branch",
            "hypothesis": "Spatial graph coupling improves demand MAE vs temporal-only",
            "seeds": str(PRIMARY_SEED),
            "priority": "Required",
        },
        {
            "ablation_id": "A3",
            "study_category": "component_removal",
            "variant_name": "Without Transformer Module",
            "graph_adjacency": "Hybrid (Phase 08)",
            "spatial_branch": True,
            "temporal_branch": False,
            "fusion": "Spatial-only passthrough",
            "multi_task": True,
            "attention_export": "Spatial only",
            "structural_change": "Remove Transformer Encoder; mean-pool T dim before graph block",
            "hypothesis": "Temporal encoding improves demand MAE vs spatial-only snapshot",
            "seeds": str(PRIMARY_SEED),
            "priority": "Required",
        },
        # ── Multi-task (A4) ──
        {
            "ablation_id": "A4",
            "study_category": "multi_task",
            "variant_name": "Without Multi-Task Learning",
            "graph_adjacency": "Hybrid (Phase 08)",
            "spatial_branch": True,
            "temporal_branch": True,
            "fusion": "Parallel gated",
            "multi_task": False,
            "attention_export": True,
            "structural_change": "Remove stress head; λ2=0; train demand-only",
            "hypothesis": "Joint training improves demand and enables stress forecasting",
            "seeds": str(PRIMARY_SEED),
            "priority": "Required",
        },
        # ── Hybrid graph (A5 family) ──
        {
            "ablation_id": "A5",
            "study_category": "hybrid_graph",
            "variant_name": "Hybrid Graph (same as A1)",
            "graph_adjacency": "Hybrid (Phase 08)",
            "spatial_branch": True,
            "temporal_branch": True,
            "fusion": "Parallel gated",
            "multi_task": True,
            "attention_export": True,
            "structural_change": "Reference adjacency — duplicate row for graph study grouping",
            "hypothesis": "Hybrid beats geo-only and corr-only graphs",
            "seeds": "See A1",
            "priority": "Required",
        },
        {
            "ablation_id": "A5-GEO",
            "study_category": "hybrid_graph",
            "variant_name": "Without Hybrid Graph — Geographical Only",
            "graph_adjacency": "Geographical (21 edges, Phase 08)",
            "spatial_branch": True,
            "temporal_branch": True,
            "fusion": "Parallel gated",
            "multi_task": True,
            "attention_export": True,
            "structural_change": "Replace A with row-normalised geographic adjacency",
            "hypothesis": "Hybrid correlation weighting adds value over borders-only",
            "seeds": str(PRIMARY_SEED),
            "priority": "Required",
        },
        {
            "ablation_id": "A5-CORR",
            "study_category": "hybrid_graph",
            "variant_name": "Correlation Graph Only",
            "graph_adjacency": "Correlation τ=0.65 (33 edges, Phase 08)",
            "spatial_branch": True,
            "temporal_branch": True,
            "fusion": "Parallel gated",
            "multi_task": True,
            "attention_export": True,
            "structural_change": "Replace A with correlation-threshold adjacency",
            "hypothesis": "Hybrid moderates dense correlation graph over-smoothing",
            "seeds": str(PRIMARY_SEED),
            "priority": "Supplementary",
        },
        # ── Explainability (A6) ──
        {
            "ablation_id": "A6",
            "study_category": "explainability",
            "variant_name": "Without Explainability Pathways",
            "graph_adjacency": "Hybrid (Phase 08)",
            "spatial_branch": "Black-box",
            "temporal_branch": "Black-box",
            "fusion": "Concat + MLP",
            "multi_task": True,
            "attention_export": False,
            "structural_change": "Replace GT+TE with param-matched BiLSTM trunk; no attention maps",
            "hypothesis": "Attention-based trunk trades ≤ε performance for native XAI (GAP-05)",
            "seeds": str(PRIMARY_SEED),
            "priority": "Required",
        },
        {
            "ablation_id": "A6-XAI",
            "study_category": "explainability",
            "variant_name": "Full Model XAI Analysis (A1)",
            "graph_adjacency": "Hybrid (Phase 08)",
            "spatial_branch": True,
            "temporal_branch": True,
            "fusion": "Parallel gated",
            "multi_task": True,
            "attention_export": True,
            "structural_change": "Analysis-only: Phase 12 SHAP + attention on trained A1",
            "hypothesis": "Hybrid XAI stack yields stable attributions without retraining",
            "seeds": "See A1",
            "priority": "Required",
        },
    ]
    return pd.DataFrame(rows)


def write_ablation_plan(matrix: pd.DataFrame) -> None:
    core = matrix[matrix["priority"] == "Required"]
    lines = [
        "# Ablation Plan — Phase 13",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Objective",
        "",
        "Isolate and quantify contributions of graph module, transformer module, multi-task learning,",
        "hybrid graph topology, and explainability-enabled architecture for PF-STGT.",
        "",
        "## Reference model",
        "",
        "**A1 — PF-STGT Full Model** (Phase 09 architecture, Phase 08 hybrid graph, Phase 08.5 dual-task).",
        "",
        "## Study categories",
        "",
        "### 1. Component removal studies (A2–A3)",
        "",
        "| ID | Variant | Isolates |",
        "| --- | --- | --- |",
        "| A2 | Without Graph Module | Spatial / graph contribution |",
        "| A3 | Without Transformer Module | Temporal contribution |",
        "",
        "### 2. Hybrid graph studies (A5 family)",
        "",
        "| ID | Adjacency | Edges | Density |",
        "| --- | --- | --- | --- |",
        "| A5 / A1 | Hybrid | 24 | 66.7% |",
        "| A5-GEO | Geographical only | 21 | 58.3% |",
        "| A5-CORR | Correlation τ=0.65 | 33 | 91.7% |",
        "",
        "### 3. Multi-task studies (A4)",
        "",
        "| ID | Variant | Training |",
        "| --- | --- | --- |",
        "| A4 | Demand-only | λ2=0, stress head removed |",
        "| A1 | Full multi-task | λ1=1.0, λ2=0.5 (Phase 10) |",
        "",
        "### 4. Explainability studies (A6)",
        "",
        "| ID | Variant | Type |",
        "| --- | --- | --- |",
        "| A6 | BiLSTM black-box trunk | Trained ablation (no attention maps) |",
        "| A6-XAI / A1 | Phase 12 XAI stack | Post-hoc analysis on full model |",
        "",
        "## Required ablations (Phase 13 spec)",
        "",
        core[core["ablation_id"].isin(["A1", "A2", "A3", "A4", "A5-GEO", "A6"])][
            ["ablation_id", "variant_name", "structural_change", "hypothesis"]
        ].to_markdown(index=False),
        "",
        "## Training protocol (all variants)",
        "",
        "| Rule | Specification |",
        "| --- | --- |",
        "| Hyperparameters | Phase 11 best config (or trial-0 baseline if HPO not yet run) |",
        "| Loss | Phase 10 frozen (Huber + MSE for multi-task) |",
        "| Split | Phase 04 chronological 70/15/15 |",
        "| Early stopping | Val macro demand MAE, patience 15 |",
        "| A1 seeds | 42, 123, 456 |",
        "| Ablation seeds | 42 (single seed for fair budget) |",
        "",
        "## Execution order",
        "",
        "1. Train A1 (full) → confirm test metrics.",
        "2. Train A2–A4, A5-GEO, A6 (parallelizable).",
        "3. Optional A5-CORR supplementary.",
        "4. Run Phase 12 XAI on A1 (A6-XAI analysis track).",
        "5. Statistical tests vs A1 on test split.",
        "",
        "## Total training runs (budget)",
        "",
        "| Category | Runs |",
        "| --- | --- |",
        "| A1 full (3 seeds) | 3 |",
        "| Core ablations (5 × 1 seed) | 5 |",
        "| Supplementary A5-CORR | 1 |",
        "| **Total** | **9** |",
        "",
        "Est. **~12–18 GPU-hours** (Phase 11 scale × 9 runs).",
        "",
    ]
    (ABL_DIR / "ablation_plan.md").write_text("\n".join(lines))


def write_component_contribution_framework(matrix: pd.DataFrame) -> None:
    lines = [
        "# Component Contribution Framework — Phase 13",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Contribution metrics",
        "",
        "For each ablation variant v vs reference A1 on **test split**:",
        "",
        "```",
        "ΔMAE_v   = MAE_v − MAE_A1          (positive = variant worse)",
        "ΔRMSE_v  = RMSE_v − RMSE_A1",
        "ΔMAPE_v  = MAPE_v − MAPE_A1",
        "ΔR²_v    = R²_A1 − R²_v            (positive = variant worse)",
        "",
        "Relative demand degradation:",
        "  RD_v = ΔMAE_v / MAE_A1 × 100%",
        "```",
        "",
        "### Stress task (multi-task variants only)",
        "",
        "```",
        "ΔMAE_OSI_v = MAE_OSI_v − MAE_OSI_A1     (A4: stress undefined → report N/A)",
        "ΔR²_OSI_v  = R²_OSI_A1 − R²_OSI_v",
        "```",
        "",
        "## Component attribution interpretation",
        "",
        "| Component | Comparison | Expected signal if component matters |",
        "| --- | --- | --- |",
        "| Graph module | A1 vs A2 | ΔMAE_A2 > 0 significant |",
        "| Transformer | A1 vs A3 | ΔMAE_A3 > 0 significant |",
        "| Multi-task | A1 vs A4 | ΔMAE_A4 > 0 OR ΔR²_OSI_A4 = N/A |",
        "| Hybrid graph | A1 vs A5-GEO | ΔMAE_GEO > 0 |",
        "| Hybrid vs corr | A1 vs A5-CORR | Compare MAE and graph density tradeoff |",
        "| Explainability trunk | A1 vs A6 | ΔMAE_A6 small if XAI is low-cost |",
        "",
        "## Contribution decomposition table (implementation output)",
        "",
        "```",
        "results/ablation/component_contributions.csv",
        "```",
        "",
        "| Column | Description |",
        "| --- | --- |",
        "| ablation_id | Variant ID |",
        "| delta_mae_mw | Test MAE change vs A1 |",
        "| relative_degradation_pct | ΔMAE / MAE_A1 |",
        "| significant | Wilcoxon p < α_adj |",
        "| component_verdict | Supports / Does not support hypothesis |",
        "",
        "## Graph study summary metrics",
        "",
        "Report alongside demand metrics:",
        "",
        "- Edge density vs MAE scatter (A5-GEO, A5-CORR, A1)",
        "- Spearman(attention, A_ij) per graph variant",
        "",
        "## Multi-task benefit criteria",
        "",
        "Multi-task learning **supported** if ALL hold:",
        "",
        "1. A1 demand MAE ≤ A4 demand MAE (within 0.05 MW or significant).",
        "2. A1 stress MAE < persistence baseline (Phase 10).",
        "3. No collapse: A1 stress R² > 0 on test.",
        "",
        "## Explainability tradeoff criteria",
        "",
        "Explainability pathway **justified** if:",
        "",
        "1. |ΔMAE_A6| / MAE_A1 < 5% (performance cost acceptable), OR",
        "2. A6-XAI attention–SHAP agreement ≥ 60% (Phase 12 protocol) AND A6 lacks native maps.",
        "",
    ]
    (ABL_DIR / "component_contribution_framework.md").write_text("\n".join(lines))


def write_statistical_significance_plan() -> None:
    alpha_adj = ALPHA / N_COMPARISONS
    lines = [
        "# Statistical Significance Plan — Phase 13",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        f"Status: **FROZEN**",
        "",
        "## Primary comparison unit",
        "",
        "**Daily macro MAE** on test split: for each day d,",
        "",
        "```",
        "macro_MAE_d = (1/9) Σ_r |D_r(d) − D̂_r(d)|",
        "```",
        "",
        "Yields ~278 paired observations (test windows) for A1 vs each ablation.",
        "",
        "## Primary test",
        "",
        "| Setting | Test | Null hypothesis |",
        "| --- | --- | --- |",
        "| A1 vs A_v | **Wilcoxon signed-rank** (paired) | median(ΔMAE_d) = 0 |",
        "| Significance | α = 0.05 with **Bonferroni** correction | α_adj = {:.4f} for {} comparisons vs A1 |".format(alpha_adj, N_COMPARISONS),
        "",
        "Comparisons corrected: A2, A3, A4, A5-GEO, A6.",
        "",
        "## Secondary tests",
        "",
        "| Metric | Test | Notes |",
        "| --- | --- | --- |",
        "| RMSE | Wilcoxon on daily macro RMSE | Supplementary |",
        "| MAPE | Wilcoxon on daily macro MAPE | Scale-sensitive; report with MAE |",
        "| R² | Bootstrap 95% CI on R² difference | 1,000 resamples, test days |",
        "| Stress MAE | Wilcoxon on daily |OSI − OSI_hat| | A4 excluded |",
        "",
        "## Effect size",
        "",
        "```",
        "Cohen's d = mean(MAE_v − MAE_A1) / std(MAE_v − MAE_A1)  across test days",
        "|d| ≥ 0.5 → medium effect (report in paper)",
        "```",
        "",
        "## Multi-seed uncertainty (A1 only)",
        "",
        "- Report A1 test MAE as mean ± std over seeds {42, 123, 456}.",
        "- Ablation point estimates use seed 42; compare to A1 seed-42 for paired tests.",
        "",
        "## Non-inferiority check (A6 explainability)",
        "",
        "One-sided test: A6 not worse than A1 by more than **5% relative MAE**.",
        "",
        "```",
        "H0: MAE_A6 ≥ 1.05 × MAE_A1",
        "Use bootstrap upper 95% CI on (MAE_A6 − MAE_A1) / MAE_A1",
        "```",
        "",
        "## Output artefacts",
        "",
        "```",
        "results/ablation/significance_tests.csv",
        "results/ablation/bootstrap_ci_mae.csv",
        "results/ablation/effect_sizes.csv",
        "```",
        "",
        "## Reporting template",
        "",
        "| Comparison | ΔMAE (MW) | p-value | p_adj | Cohen's d | Verdict |",
        "| --- | --- | --- | --- | --- | --- |",
        "| A1 vs A2 | — | — | — | — | — |",
        "| ... | | | | | |",
        "",
    ]
    (ABL_DIR / "statistical_significance_plan.md").write_text("\n".join(lines))


def write_summary(matrix: pd.DataFrame, locked_md5: dict[str, str]) -> None:
    lines = [
        "# Phase 13 — Ablation Studies Design Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        f"- Reference model: **A1 PF-STGT Full**",
        f"- Core ablation variants: **{len(matrix[matrix['priority']=='Required'])}**",
        f"- Total planned training runs: **9** (no runs executed in this phase)",
        "",
        "## Study categories",
        "",
        "| Category | Variants |",
        "| --- | --- |",
        "| Component removal | A2, A3 |",
        "| Hybrid graph | A5, A5-GEO, A5-CORR |",
        "| Multi-task | A4 vs A1 |",
        "| Explainability | A6 (trained), A6-XAI (analysis) |",
        "",
        "## Evaluation metrics (frozen)",
        "",
        "Demand: MAE, RMSE, MAPE, R² (macro + Dhaka). Stress: MAE, RMSE, R².",
        "",
        "## Deliverables",
        "",
        "### ablation/",
        "- ablation_plan.md",
        "- ablation_matrix.csv",
        "- component_contribution_framework.md",
        "- statistical_significance_plan.md",
        "",
        "### results/phases/phase_13_ablation/",
        "- ablation_summary.md",
        "- ablation_decision_report.md",
        "",
        "## Scope compliance",
        "",
        "- Ablation framework design only.",
        "- **No model implementation or training.**",
        "- **No experimental results generated.**",
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
        "Ready for ablation implementation and training (next phase).",
        "",
    ]
    (REPORT_DIR / "ablation_summary.md").write_text("\n".join(lines))


def write_decision_report(matrix: pd.DataFrame) -> None:
    lines = [
        "# Ablation Decision Report — Phase 13",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Design rationale",
        "",
        "### Component removals (A2–A3)",
        "",
        "Parallel fusion PF-STGT (Phase 09) enables clean branch ablation without retuning depth.",
        "A2/A3 directly test GAP-04 graph-temporal coupling claims.",
        "",
        "### Hybrid graph (A5-GEO, A5-CORR)",
        "",
        "Phase 08 selected hybrid over geo-only (23 vs 19) and correlation-only (23 vs 15).",
        "Ablation quantifies whether selection holds on **test forecast metrics**, not graph statistics alone.",
        "",
        "### Multi-task (A4)",
        "",
        "Phase 08.5 frozen dual-task formulation; A4 isolates GAP-02 multi-task benefit on demand **and** enables stress-only evaluation on A1.",
        "",
        "### Explainability (A6)",
        "",
        "Phase 12 XAI is post-hoc on A1; A6 trains param-matched BiLSTM trunk without attention ",
        "to measure performance–interpretability tradeoff (GAP-05).",
        "",
        "## Variant registry",
        "",
        matrix[["ablation_id", "study_category", "variant_name", "priority"]].to_markdown(index=False),
        "",
        "## Expected outcomes (hypotheses)",
        "",
        "| ID | Expected if design is correct |",
        "| --- | --- |",
        "| A2 | Demand MAE increases (graph helps spatial coupling) |",
        "| A3 | Demand MAE increases (transformer helps T=7 seasonality) |",
        "| A4 | Demand MAE equal or worse; no stress output |",
        "| A5-GEO | Demand MAE ≥ A1 (hybrid adds correlation weights) |",
        "| A5-CORR | MAPE may degrade (dense graph over-smoothing) |",
        "| A6 | MAE within 5% of A1; loses attention/SHAP fidelity |",
        "",
    ]
    (REPORT_DIR / "ablation_decision_report.md").write_text("\n".join(lines))


def main() -> None:
    ABL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    locked_paths = {
        "graphs/adjacency_matrix.csv": ROOT / "graphs" / "adjacency_matrix.csv",
        "architecture/architecture_overview.md": ROOT / "architecture" / "architecture_overview.md",
        "experiments/evaluation_protocol.md": ROOT / "experiments" / "evaluation_protocol.md",
        "explainability/xai_strategy.md": ROOT / "explainability" / "xai_strategy.md",
    }
    locked_md5 = {k: file_md5(v) for k, v in locked_paths.items() if v.exists()}

    matrix = ablation_matrix()
    matrix.to_csv(ABL_DIR / "ablation_matrix.csv", index=False)

    write_ablation_plan(matrix)
    write_component_contribution_framework(matrix)
    write_statistical_significance_plan()
    write_summary(matrix, locked_md5)
    write_decision_report(matrix)

    print("Phase 13 ablation studies design complete.")
    print(f"Variants: {len(matrix)} | Core required: {(matrix['priority']=='Required').sum()}")
    print(f"Reports -> {ABL_DIR.relative_to(ROOT)} , {REPORT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
