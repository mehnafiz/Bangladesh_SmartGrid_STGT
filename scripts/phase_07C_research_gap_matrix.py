"""Phase 07C — Research Gap Matrix.

Transforms Phase 07B limitations and opportunities into evidence-based research
gaps, novelty statements, contribution statements, reviewer risk assessment,
and research positioning.

Does NOT design graph topology, model architecture, training, or evaluation.

Inputs:
    references/analysis/*.csv  (Phase 07B deliverables)

Outputs:
    references/gap_analysis/  (6 deliverables)
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = ROOT / "references" / "analysis"
GAP_DIR = ROOT / "references" / "gap_analysis"


def _count_contains(series: pd.Series, needle: str) -> int:
    return int(series.str.contains(needle, case=False, na=False).sum())


def load_inputs() -> dict[str, pd.DataFrame]:
    return {
        "paper_analysis": pd.read_csv(ANALYSIS_DIR / "paper_analysis_catalog.csv"),
        "model_matrix": pd.read_csv(ANALYSIS_DIR / "model_comparison_matrix.csv"),
        "dataset_matrix": pd.read_csv(ANALYSIS_DIR / "dataset_comparison_matrix.csv"),
        "explain_matrix": pd.read_csv(ANALYSIS_DIR / "explainability_comparison_matrix.csv"),
        "limitations": pd.read_csv(ANALYSIS_DIR / "limitation_catalog.csv"),
        "opportunities": pd.read_csv(ANALYSIS_DIR / "opportunity_catalog.csv"),
    }


def build_research_gap_matrix(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    lim = data["limitations"]
    opp = data["opportunities"]
    papers = data["paper_analysis"]
    model = data["model_matrix"]
    dataset = data["dataset_matrix"]
    explain = data["explain_matrix"]
    n_papers = len(papers)

    rel = papers["relevance_to_stgt_paper"].str.split(" — ").str[0]
    high_rel = int((rel == "High").sum())
    graph_n = int(model["graph_based"].sum())
    transformer_n = int(model["transformer_based"].sum())
    xai_n = int((~explain["none_reported"]).sum())
    bd_case_n = _count_contains(dataset["geographic_scope"], "Bangladesh")
    shedding_papers = int((papers["research_topic"] == "Load Shedding Prediction").sum())
    multitask_lit = int(model["multi_task"].sum())
    gen_lim = int((lim["limitation_category"] == "Generalisation").sum())
    task_lim = int((lim["limitation_category"] == "Task formulation").sum())
    bd_opp = int((opp["opportunity_category"] == "Bangladesh validation").sum())
    stgt_opp = int((opp["opportunity_category"] == "STGT architecture").sum())
    shed_opp = int((opp["opportunity_category"] == "Shedding formulation").sum())
    sparse_lim = _count_contains(lim["limitation"], "sparse")
    joint_lim = _count_contains(lim["limitation"], "jointly with demand")
    xai_weak = _count_contains(papers["weaknesses"], "No explainability")

    gaps = [
        {
            "gap_id": "GAP-01",
            "gap_category": "Geographic & contextual validity",
            "research_gap": (
                "No peer-reviewed spatio-temporal load or load-shedding forecasting study "
                "uses Bangladesh division-level smart-grid daily data."
            ),
            "evidence_type": "limitation;opportunity;dataset_matrix",
            "evidence_summary": (
                f"{gen_lim} generalisation limitations cite absent Bangladesh/South-Asia validation; "
                f"{bd_opp}/{n_papers} opportunity entries call for Bangladesh benchmarking; "
                f"{bd_case_n}/{n_papers} collected papers use Bangladesh geography."
            ),
            "supporting_limitation_count": gen_lim,
            "supporting_opportunity_count": bd_opp,
            "related_topics": "All topics",
            "project_phase_evidence": (
                "Phase 01–02: 1,850 daily rows, 9 divisions (2019–2024); "
                "Phase 06: validated 146-column feature splits ready for modelling."
            ),
            "priority": "Critical",
            "literature_coverage": "Absent",
        },
        {
            "gap_id": "GAP-02",
            "gap_category": "Multi-task formulation",
            "research_gap": (
                "Literature rarely couples continuous regional demand forecasting with "
                "sparse load-shedding prediction in a unified multi-task learning framework."
            ),
            "evidence_type": "limitation;opportunity;model_matrix",
            "evidence_summary": (
                f"{joint_lim} limitations note task isolation (demand vs shedding); "
                f"{task_lim} task-formulation limitations; "
                f"only {multitask_lit}/{n_papers} papers flagged multi-task in model matrix; "
                f"1 multi-task extension opportunity in catalog."
            ),
            "supporting_limitation_count": joint_lim + task_lim,
            "supporting_opportunity_count": int((opp["opportunity_category"] == "Multi-task extension").sum()),
            "related_topics": "Electrical Load Forecasting; Load Shedding Prediction; Multi-task Learning",
            "project_phase_evidence": (
                "Phase 02: demand≈supply collinearity → complementary targets advised; "
                "Phase 05A/05B: operational stress index + shedding-aware engineered features."
            ),
            "priority": "Critical",
            "literature_coverage": "Fragmented",
        },
        {
            "gap_id": "GAP-03",
            "gap_category": "Shedding target formulation",
            "research_gap": (
                "Most load-shedding literature optimises control actions or frequency response "
                "rather than forecasting sparse daily shedding intensity for operational planning."
            ),
            "evidence_type": "limitation;opportunity",
            "evidence_summary": (
                f"{shedding_papers} shedding-topic papers collected; "
                f"{shed_opp} opportunity entries propose zero-inflated/event-aware forecasting; "
                f"{sparse_lim} limitations reference sparse shedding labels."
            ),
            "supporting_limitation_count": sparse_lim + _count_contains(lim["limitation"], "control"),
            "supporting_opportunity_count": shed_opp,
            "related_topics": "Load Shedding Prediction",
            "project_phase_evidence": (
                "Phase 02: regional _load non-zero on minority of days (zero-inflated); "
                "Phase 06 recommends separate event/zero-inflated head (not implemented here)."
            ),
            "priority": "Critical",
            "literature_coverage": "Misaligned objective",
        },
        {
            "gap_id": "GAP-04",
            "gap_category": "Spatio-temporal graph modelling",
            "research_gap": (
                "Few recent papers combine graph-based spatial coupling with transformer-style "
                "temporal modelling for multi-node load forecasting; none target Bangladesh shedding."
            ),
            "evidence_type": "model_matrix;opportunity",
            "evidence_summary": (
                f"Graph-based: {graph_n}/{n_papers}; Transformer-based: {transformer_n}/{n_papers}; "
                f"High STGT relevance: {high_rel}/{n_papers}; "
                f"{stgt_opp} STGT-architecture transfer opportunities."
            ),
            "supporting_limitation_count": _count_contains(lim["limitation"], "US/EU"),
            "supporting_opportunity_count": stgt_opp,
            "related_topics": "Graph Neural Networks; Graph Transformers; Spatio-Temporal Forecasting",
            "project_phase_evidence": (
                "Phase 02: inter-regional demand correlation >0.65 (most >0.9); "
                "Phase 05A Batch 3: dynamic edge candidates (rolling_demand_corr_90d)."
            ),
            "priority": "High",
            "literature_coverage": "Partial (US/EU-centric)",
        },
        {
            "gap_id": "GAP-05",
            "gap_category": "Explainability integration",
            "research_gap": (
                "Explainable AI is rarely integrated with graph-temporal load or shedding models; "
                "SHAP/XAI appears in only a small fraction of the reviewed corpus."
            ),
            "evidence_type": "explainability_matrix;limitation",
            "evidence_summary": (
                f"Explainability reported: {xai_n}/{n_papers}; "
                f"{xai_weak} papers flagged for absent explainability in weaknesses; "
                f"Phase 07B: insufficient for explainable STGT claims without new integration."
            ),
            "supporting_limitation_count": xai_weak,
            "supporting_opportunity_count": _count_contains(opp["opportunity"], "SHAP"),
            "related_topics": "SHAP; Explainable AI; Graph Neural Networks",
            "project_phase_evidence": (
                "Project title mandates explainable STGT; Phase 05B engineered interpretable "
                "stress/demand features as attribution-ready covariates."
            ),
            "priority": "High",
            "literature_coverage": "Sparse",
        },
        {
            "gap_id": "GAP-06",
            "gap_category": "Operational stress assessment",
            "research_gap": (
                "Operational stress and reliability studies focus on transmission/microgrid assets "
                "rather than daily regional stress indices derived from demand–supply–limitation dynamics."
            ),
            "evidence_type": "limitation;opportunity",
            "evidence_summary": (
                f"{int((papers['research_topic'] == 'Operational Stress Assessment').sum())} "
                f"operational-stress papers; "
                f"{int((papers['research_topic'] == 'Power System Reliability').sum())} reliability papers; "
                f"limitations cite HV/transmission focus vs daily regional stress."
            ),
            "supporting_limitation_count": _count_contains(lim["limitation"], "transmission"),
            "supporting_opportunity_count": _count_contains(opp["opportunity"], "stress"),
            "related_topics": "Operational Stress Assessment; Power System Reliability; Smart Grid Analytics",
            "project_phase_evidence": (
                "Phase 05B: operational_stress_index and limitation-stack features validated (Phase 06)."
            ),
            "priority": "High",
            "literature_coverage": "Adjacent (not dataset-matched)",
        },
        {
            "gap_id": "GAP-07",
            "gap_category": "Feature–method co-design",
            "research_gap": (
                "Published graph/load models seldom co-design exogenous limitation covariates "
                "(fuel, water, maintenance, temperature anomalies) with spatio-temporal architectures."
            ),
            "evidence_type": "opportunity;phase_finding",
            "evidence_summary": (
                f"{int((opp['opportunity_category'] == 'Feature/method transfer').sum())} "
                f"feature/method transfer opportunities; "
                f"Phase 05B: 65 validated engineered features including calendar, lag, stress groups."
            ),
            "supporting_limitation_count": _count_contains(lim["limitation"], "covariate"),
            "supporting_opportunity_count": int((opp["opportunity_category"] == "Feature/method transfer").sum()),
            "related_topics": "Smart Grid Analytics; Electrical Load Forecasting",
            "project_phase_evidence": (
                "Phase 05A blueprint + Phase 05B implementation: limitation-stack, calendar, "
                "regional share, and stress features passed Phase 06 screening."
            ),
            "priority": "Medium",
            "literature_coverage": "Under-specified",
        },
        {
            "gap_id": "GAP-08",
            "gap_category": "Evaluation & reproducibility",
            "research_gap": (
                "Many conference and metadata-sparse papers lack documented splits, baselines, and "
                "ablations needed to benchmark spatio-temporal multi-task methods fairly."
            ),
            "evidence_type": "limitation;dataset_matrix",
            "evidence_summary": (
                f"{int((lim['limitation_category'] == 'Metadata constraint').sum())} metadata constraints; "
                f"{int((dataset['metadata_confidence'] == 'Low (title/metadata inference)').sum())}/"
                f"{n_papers} dataset inferences low-confidence."
            ),
            "supporting_limitation_count": int((lim["limitation_category"] == "Metadata constraint").sum()),
            "supporting_opportunity_count": 0,
            "related_topics": "All topics",
            "project_phase_evidence": (
                "Phase 04: chronological 70/15/15 split with train-only fitting; "
                "Phase 06: leakage-safe validation passed."
            ),
            "priority": "Medium",
            "literature_coverage": "Weak reporting",
        },
    ]
    return pd.DataFrame(gaps)


def build_novelty_matrix(gap_df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "novelty_id": "NOV-01",
            "research_gap_id": "GAP-01",
            "novelty_statement": (
                "First explainable spatio-temporal graph-transformer study anchored on "
                "Bangladesh division-level daily smart-grid records (2019–2024)."
            ),
            "contrast_with_literature": (
                "Reviewed corpus has 0 Bangladesh case studies despite 62 Bangladesh-validation opportunities."
            ),
            "evidence_basis": "limitation_catalog Generalisation (63); opportunity_catalog Bangladesh validation (62)",
            "defensibility": "Strong",
        },
        {
            "novelty_id": "NOV-02",
            "research_gap_id": "GAP-02",
            "novelty_statement": (
                "Joint multi-task formulation linking continuous regional demand dynamics with "
                "sparse load-shedding outcomes under shared spatio-temporal representation."
            ),
            "contrast_with_literature": (
                "16+ task-formulation limitations; literature predominantly single-task forecasting or control."
            ),
            "evidence_basis": "limitation_catalog Task formulation; joint demand/shedding limitations",
            "defensibility": "Strong",
        },
        {
            "novelty_id": "NOV-03",
            "research_gap_id": "GAP-03",
            "novelty_statement": (
                "Forecast-oriented treatment of daily load shedding as a zero-inflated operational "
                "signal rather than a real-time frequency-control optimisation problem."
            ),
            "contrast_with_literature": (
                "15 shedding-formulation opportunities; shedding cluster skewed to UFLS/control papers."
            ),
            "evidence_basis": "opportunity_catalog Shedding formulation; Phase 02 zero-inflated _load finding",
            "defensibility": "Strong",
        },
        {
            "novelty_id": "NOV-04",
            "research_gap_id": "GAP-04",
            "novelty_statement": (
                "Integration of graph-structured regional coupling with transformer-style temporal "
                "encoding for nine-division Bangladesh networks."
            ),
            "contrast_with_literature": (
                "Only 5/55 graph-based and 7/55 transformer-based papers; high-relevance cluster is US/EU residential/EV."
            ),
            "evidence_basis": "model_comparison_matrix; 8 High STGT-relevance papers",
            "defensibility": "Moderate",
        },
        {
            "novelty_id": "NOV-05",
            "research_gap_id": "GAP-05",
            "novelty_statement": (
                "Explainability layer (SHAP-oriented) co-designed with graph-temporal multi-task "
                "forecasts for operator-facing regional attribution."
            ),
            "contrast_with_literature": (
                "Explainability reported in 3/55 papers; graph-temporal SHAP integration largely absent."
            ),
            "evidence_basis": "explainability_comparison_matrix; SHAP-topic paper isolated to microgrid control",
            "defensibility": "Moderate",
        },
        {
            "novelty_id": "NOV-06",
            "research_gap_id": "GAP-06",
            "novelty_statement": (
                "Daily operational-stress assessment derived from demand–supply margins and "
                "exogenous limitation stacks at regional and national scale."
            ),
            "contrast_with_literature": (
                "Operational stress literature targets asset reliability/microgrids, not daily OSI-style indices."
            ),
            "evidence_basis": "Phase 05B operational_stress_index; limitation HV/transmission scope mismatch",
            "defensibility": "Moderate",
        },
        {
            "novelty_id": "NOV-07",
            "research_gap_id": "GAP-07",
            "novelty_statement": (
                "Systematic co-design of limitation-aware engineered covariates with "
                "spatio-temporal graph learning (65 validated features, Phase 06)."
            ),
            "contrast_with_literature": (
                "14 feature/method transfer opportunities; papers rarely document limitation-stack features."
            ),
            "evidence_basis": "opportunity_catalog Feature/method transfer; Phase 05A/05B/06",
            "defensibility": "Moderate",
        },
        {
            "novelty_id": "NOV-08",
            "research_gap_id": "GAP-08",
            "novelty_statement": (
                "Reproducible chronological evaluation protocol with leakage-validated splits "
                "for multi-task graph-temporal benchmarking."
            ),
            "contrast_with_literature": (
                "52/55 papers metadata-limited; weak split/baseline reporting in conference subset."
            ),
            "evidence_basis": "limitation_catalog Metadata constraint; Phase 04/06 leakage validation",
            "defensibility": "Strong",
        },
    ]
    return pd.DataFrame(rows)


def build_contribution_matrix(gap_df: pd.DataFrame, novelty_df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "contribution_id": "CON-01",
            "research_gap_id": "GAP-01",
            "novelty_id": "NOV-01",
            "contribution_statement": (
                "Empirical anchoring of spatio-temporal multi-task load analytics on a "
                "curated Bangladesh smart-grid dataset with documented division-level coverage."
            ),
            "contribution_type": "Dataset & regional case study",
            "manuscript_section_hint": "Data description; Experimental setup",
        },
        {
            "contribution_id": "CON-02",
            "research_gap_id": "GAP-02",
            "novelty_id": "NOV-02",
            "contribution_statement": (
                "Multi-task learning framework unifying demand forecasting and sparse "
                "load-shedding prediction under shared regional representations."
            ),
            "contribution_type": "Methodological",
            "manuscript_section_hint": "Problem formulation; Multi-task objective",
        },
        {
            "contribution_id": "CON-03",
            "research_gap_id": "GAP-03",
            "novelty_id": "NOV-03",
            "contribution_statement": (
                "Forecast-centric shedding formulation addressing zero-inflated daily _load "
                "signals identified in exploratory analysis."
            ),
            "contribution_type": "Task formulation",
            "manuscript_section_hint": "Target definition; Loss design (conceptual)",
        },
        {
            "contribution_id": "CON-04",
            "research_gap_id": "GAP-04",
            "novelty_id": "NOV-04",
            "contribution_statement": (
                "Spatio-temporal graph-transformer approach capturing inter-division demand "
                "coupling validated in Phase 02 correlation structure."
            ),
            "contribution_type": "Architectural (conceptual positioning only)",
            "manuscript_section_hint": "Related work contrast; Proposed approach overview",
        },
        {
            "contribution_id": "CON-05",
            "research_gap_id": "GAP-05",
            "novelty_id": "NOV-05",
            "contribution_statement": (
                "Explainability pathway linking SHAP-style attribution to regional graph "
                "features and multi-task outputs for operator interpretability."
            ),
            "contribution_type": "Explainability",
            "manuscript_section_hint": "Explainability methodology; Results discussion",
        },
        {
            "contribution_id": "CON-06",
            "research_gap_id": "GAP-06",
            "novelty_id": "NOV-06",
            "contribution_statement": (
                "Operational stress assessment task complementing demand and shedding heads "
                "using engineered stress indices from validated feature pipeline."
            ),
            "contribution_type": "Empirical & operational",
            "manuscript_section_hint": "Multi-task heads; Stress assessment results",
        },
        {
            "contribution_id": "CON-07",
            "research_gap_id": "GAP-07",
            "novelty_id": "NOV-07",
            "contribution_statement": (
                "Feature-engineering blueprint and validated covariate set (calendar, lags, "
                "limitation stacks, regional shares) supporting graph-temporal learning."
            ),
            "contribution_type": "Feature engineering",
            "manuscript_section_hint": "Features; Ablation rationale",
        },
        {
            "contribution_id": "CON-08",
            "research_gap_id": "GAP-08",
            "novelty_id": "NOV-08",
            "contribution_statement": (
                "Transparent chronological train/validation/test protocol with leakage "
                "validation supporting fair comparison to literature baselines."
            ),
            "contribution_type": "Reproducibility",
            "manuscript_section_hint": "Experimental protocol; Limitations",
        },
    ]
    return pd.DataFrame(rows)


def write_reviewer_risk_matrix(
    gap_df: pd.DataFrame,
    novelty_df: pd.DataFrame,
    data: dict[str, pd.DataFrame],
) -> None:
    papers = data["paper_analysis"]
    n = len(papers)
    lines = [
        "# Reviewer Risk Assessment — Phase 07C",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "Evidence base: 55 papers (Phase 07A), critical analysis (Phase 07B).",
        "This document anticipates reviewer challenges to novelty and contributions.",
        "It does **not** specify graph topology or model architecture.",
        "",
        "## Risk matrix",
        "",
        "| Risk ID | Challenge | Likely reviewer concern | Mitigation strategy | Residual risk |",
        "| --- | --- | --- | --- | --- |",
        "| R-01 | Geographic generalisation | \"Single-country case; findings may not transfer.\" | Frame as first rigorous Bangladesh division-level benchmark; compare methods against US/EU graph papers on same metrics internally. | Medium |",
        "| R-02 | Incremental architecture | \"Graph + transformer is incremental vs GNN/GT literature.\" | Emphasise multi-task shedding + OSI formulation and Bangladesh context as differentiators, not backbone alone (8 High-relevance papers are method-centric). | Medium |",
        "| R-03 | Shedding vs control | \"Shedding literature is control-oriented; forecasting claim is misaligned.\" | Explicit task contrast in introduction; cite 15 shedding-formulation opportunities and Phase 02 zero-inflated evidence. | Low |",
        "| R-04 | Sparse target degeneracy | \"Model may predict all-zero shedding.\" | Acknowledge Phase 02 imbalance; commit to event-aware metrics and separate shedding head (Phase 06 recommendation). | Medium |",
        "| R-05 | Explainability cost | \"SHAP on graph-temporal models is expensive/misleading.\" | Cite isolated SHAP paper in corpus; plan node-level vs global attribution and correlation-aware interpretation (Phase 07B weakness flagged). | Medium |",
        "| R-06 | Data collinearity | \"Demand≈supply redundancy inflates importance.\" | Reference Phase 02 collinearity finding; use complementary targets and ablation on engineered features (Phase 05B groups). | Low |",
        "| R-07 | Temporal gaps | \"17 missing calendar days break windowing.\" | Document gap handling from Phase 01/03; use continuous index with explicit gap flags in methodology. | Low |",
        "| R-08 | Metadata-thin related work | \"Literature review depth limited by missing abstracts (52/55).\" | Deep-read 8 High-relevance + 3 abstract-rich papers; supplement with full-text retrieval before submission. | Medium |",
        "| R-09 | Multi-task negative transfer | \"Joint training hurts sparse shedding head.\" | Cite Phase 07B multi-task weakness theme; plan uncertainty/task-weighting analysis in future evaluation phase. | Medium |",
        "| R-10 | Novelty overclaim | \"Explainable STGT is buzzword stacking.\" | Tie each claim to gap ID and counted evidence (novelty_matrix); avoid architecture details not yet implemented. | Low |",
        "",
        "## Severity summary",
        "",
        "| Residual risk | Count |",
        "| --- | --- |",
        "| Low | 3 |",
        "| Medium | 6 |",
        "| High | 0 |",
        "",
        "## Highest-priority reviewer defenses",
        "",
        "1. **Bangladesh gap (GAP-01):** 0/" + str(n) + " papers in corpus use Bangladesh data — regional contribution is evidence-backed.",
        "2. **Task integration (GAP-02/GAP-03):** Joint demand + sparse shedding forecasting is under-represented vs control/optimisation cluster.",
        "3. **Reproducibility (GAP-08):** Project phases 04/06 provide stronger evaluation discipline than metadata-sparse conference comparators.",
        "",
    ]
    (GAP_DIR / "reviewer_risk_matrix.md").write_text("\n".join(lines))


def write_research_positioning(gap_df: pd.DataFrame, data: dict[str, pd.DataFrame]) -> None:
    model = data["model_matrix"]
    papers = data["paper_analysis"]
    lines = [
        "# Proposed Research Positioning",
        "",
        f"Generated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "## Working title alignment",
        "",
        "*An Explainable Spatio-Temporal Graph Transformer for Multi-Task Load Shedding "
        "Forecasting and Operational Stress Assessment in Bangladesh Smart Power Networks*",
        "",
        "## Positioning statement",
        "",
        "This research occupies the intersection of four under-served areas in the reviewed "
        "literature (n=55, 2023–2026): **(1)** Bangladesh division-level smart-grid analytics, "
        "**(2)** multi-task coupling of demand and sparse load shedding, **(3)** graph-temporal "
        "modelling with explainability, and **(4)** daily operational-stress assessment derived "
        "from limitation-aware covariates. Existing work clusters into single-task forecasting "
        "(20 papers), shedding control/optimisation (15), and isolated graph or transformer "
        "methods (5 graph-based, 7 transformer-based) evaluated mainly on US/EU residential or "
        "microgrid data.",
        "",
        "## Literature cluster map",
        "",
        "| Cluster | Papers | Project differentiation |",
        "| --- | --- | --- |",
        f"| Electrical Load Forecasting | {int((papers['research_topic']=='Electrical Load Forecasting').sum())} | Adds graph coupling, shedding head, OSI task, Bangladesh data |",
        f"| Load Shedding Prediction | {int((papers['research_topic']=='Load Shedding Prediction').sum())} | Shifts from UFLS/control to daily forecast formulation |",
        f"| Graph / Spatio-temporal | {int(model['graph_based'].sum())} graph, {int(model['transformer_based'].sum())} transformer | Targets 9-division national grid, not AMI/EV micro-networks |",
        f"| Explainability (SHAP/XAI) | {int((~data['explain_matrix']['none_reported']).sum())} with XAI | Integrates XAI with multi-task graph-temporal outputs (planned) |",
        f"| Operational stress / reliability | {int((papers['research_topic'].isin(['Operational Stress Assessment','Power System Reliability']).sum()))} | Daily OSI from demand–limitation stacks vs asset reliability |",
        "",
        "## Gap-to-contribution alignment",
        "",
    ]
    for _, g in gap_df.iterrows():
        lines.append(f"- **{g['gap_id']}** ({g['priority']}): {g['research_gap']}")
    lines += [
        "",
        "## Competitive positioning (conceptual — no architecture specified)",
        "",
        "**Versus univariate forecasters:** Project adds spatial graph coupling, shedding sparsity, "
        "and stress assessment beyond scalar load prediction.",
        "",
        "**Versus shedding control papers:** Project targets ex-ante daily forecasting for planning, "
        "not real-time UFLS or optimisation.",
        "",
        "**Versus GNN/GT papers:** Project combines Bangladesh national-grid context, multi-task "
        "objectives, and explainability mandate absent in high-relevance comparators.",
        "",
        "**Versus XAI papers:** Project embeds explainability in a multi-node, multi-task forecasting "
        "setting rather than microgrid control with distillation-only interpretability.",
        "",
        "## Phase readiness",
        "",
        "- Data & features: Phases 01–06 complete (1,850 rows, 146 validated columns).",
        "- Literature: Phases 07A–07B complete (55 papers, 161 limitations, 110 opportunities).",
        "- Next allowed phase: **Graph Construction** (topology design explicitly deferred).",
        "",
        "## Positioning risks (see reviewer_risk_matrix.md)",
        "",
        "Primary risks: single-region case study, sparse shedding degeneracy, and architecture "
        "incrementalism. Defenses are evidence-linked in gap and novelty matrices.",
        "",
    ]
    (GAP_DIR / "proposed_research_positioning.md").write_text("\n".join(lines))


def write_gap_summary(
    gap_df: pd.DataFrame,
    novelty_df: pd.DataFrame,
    contribution_df: pd.DataFrame,
    data: dict[str, pd.DataFrame],
) -> None:
    lim = data["limitations"]
    opp = data["opportunities"]
    lines = [
        "# Phase 07C — Research Gap Matrix Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        f"- Input: `references/analysis/` (Phase 07B, 6 files)",
        f"- Research gaps identified: **{len(gap_df)}**",
        f"- Novelty statements: **{len(novelty_df)}**",
        f"- Contribution statements: **{len(contribution_df)}**",
        "",
        "## Scope compliance",
        "",
        "- Evidence-based gap synthesis from limitation and opportunity catalogs.",
        "- Novelty, contribution, reviewer risk, and positioning documented.",
        "- **No graph topology design** performed.",
        "- **No model architecture design** performed.",
        "- **No training or evaluation** performed.",
        "- Locked phase outputs (Phases 01–07B) not modified.",
        "",
        "## Gap priority distribution",
        "",
    ]
    for pri, cnt in gap_df["priority"].value_counts().items():
        lines.append(f"- {pri}: **{cnt}**")
    lines += [
        "",
        "## Evidence traceability",
        "",
        f"- Limitation entries consumed: **{len(lim)}**",
        f"- Opportunity entries consumed: **{len(opp)}**",
        f"- Papers in corpus: **{len(data['paper_analysis'])}**",
        "",
        "## Critical gaps (priority = Critical)",
        "",
    ]
    for _, g in gap_df[gap_df["priority"] == "Critical"].iterrows():
        lines.append(f"1. **{g['gap_id']}** — {g['research_gap']}")
    lines += [
        "",
        "## Deliverables",
        "",
        "- `research_gap_matrix.csv`",
        "- `novelty_matrix.csv`",
        "- `contribution_matrix.csv`",
        "- `reviewer_risk_matrix.md`",
        "- `proposed_research_positioning.md`",
        "- `gap_summary.md`",
        "",
        "## Next phase",
        "",
        "Ready for Graph Construction (Phase 08 or equivalent per project plan).",
    ]
    (GAP_DIR / "gap_summary.md").write_text("\n".join(lines))


def main() -> None:
    GAP_DIR.mkdir(parents=True, exist_ok=True)
    data = load_inputs()
    gap_df = build_research_gap_matrix(data)
    novelty_df = build_novelty_matrix(gap_df)
    contribution_df = build_contribution_matrix(gap_df, novelty_df)

    gap_df.to_csv(GAP_DIR / "research_gap_matrix.csv", index=False)
    novelty_df.to_csv(GAP_DIR / "novelty_matrix.csv", index=False)
    contribution_df.to_csv(GAP_DIR / "contribution_matrix.csv", index=False)
    write_reviewer_risk_matrix(gap_df, novelty_df, data)
    write_research_positioning(gap_df, data)
    write_gap_summary(gap_df, novelty_df, contribution_df, data)

    print("Phase 07C research gap matrix complete.")
    print(f"Gaps: {len(gap_df)} | Novelty: {len(novelty_df)} | Contributions: {len(contribution_df)}")
    print(f"Critical gaps: {(gap_df['priority']=='Critical').sum()}")
    print(f"Reports -> {GAP_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
