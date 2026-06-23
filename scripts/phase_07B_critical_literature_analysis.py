"""Phase 07B — Critical Literature Analysis (reviewer-style).

Performs critical analysis of all papers in literature_catalog.csv.
Does NOT finalize research gaps or design models.

Inputs:
    references/metadata/literature_catalog.csv

Outputs:
    references/analysis/  (7 deliverables)
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "references" / "metadata" / "literature_catalog.csv"
ANALYSIS_DIR = ROOT / "references" / "analysis"


def _t(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def venue_tier(journal: str, publisher: str) -> str:
    j = _t(journal).lower()
    if any(x in j for x in ("transactions on smart grid", "transactions on power systems", "applied energy", "energy and ai")):
        return "Top-tier journal"
    if any(x in j for x in ("international journal", "electric power systems research", "reliability engineering", "data science and engineering", "ieee access", "energy", "heliyon")):
        return "Peer-reviewed journal"
    if "conference" in j or re.search(r"\b20\d{2}\b", j):
        return "Conference proceeding"
    if not j or "ssrn" in j or "techrxiv" in j:
        return "Preprint / working paper"
    return "Peer-reviewed journal"


def infer_problem(title: str, topic: str) -> str:
    title_l = title.lower()
    if "load shed" in title_l or "under-frequency" in title_l or "ufls" in title_l:
        return "Operational control/assessment of load shedding under frequency or stability constraints"
    if "resilience" in title_l or "reliability" in title_l:
        return "Quantifying or improving power-system reliability/resilience under disturbances"
    if "explain" in title_l or "interpret" in title_l:
        return "Explaining or reviewing interpretability of load-forecasting models"
    if "demand response" in title_l or "fdia" in title_l or "cyber" in title_l:
        return "Smart-grid operational analytics (demand response, security, or cyber resilience)"
    if "forecast" in title_l or "prediction" in title_l:
        return f"Short-/medium-term energy or load forecasting ({topic.lower()})"
    return f"Smart-grid analytics aligned with {topic.lower()}"


def infer_dataset(title: str, abstract: str) -> str:
    text = f"{title} {abstract}".lower()
    known = [
        ("iso-ne", "ISO-NE (US independent system operator)"),
        ("eia", "US EIA industrial electricity statistics"),
        ("ieee test", "IEEE standard test feeders/systems"),
        ("ieee 34", "IEEE 34-bus test feeder"),
        ("puerto rico", "Puerto Rico grid case study"),
        ("tambora", "Tambora sub-system (Indonesia)"),
        ("arizona state", "Arizona State University integrated energy system"),
        ("3000 households", "AMI data from 3,000 residential households"),
        ("residential", "Residential load/AMI data (region not fully specified in metadata)"),
        ("ev charging", "Electric-vehicle charging infrastructure data"),
        ("microgrid", "Islanded/microgrid operational scenarios"),
        ("wind farm", "Hybrid AC/DC system with remote wind farms"),
    ]
    for key, label in known:
        if key in text:
            return label
    if "case study" in text:
        return "Single case-study power system (details limited in metadata)"
    if "ssrn" in text or "techrxiv" in text:
        return "Dataset not fully specified in available metadata (preprint)"
    return "Not explicitly stated in available metadata"


def infer_features(title: str, abstract: str) -> str:
    text = f"{title} {abstract}".lower()
    feats = []
    mapping = [
        ("exogenous", "exogenous variables"),
        ("weather", "weather / temperature"),
        ("ami", "AMI interval load measurements"),
        ("textual embedding", "textual embeddings"),
        ("graph", "graph-structured spatial features"),
        ("spatiotemporal", "spatio-temporal coupling features"),
        ("renewable", "renewable-generation indicators"),
        ("frequency", "frequency / stability signals"),
        ("demand response", "demand-response participation signals"),
        ("wind", "wind-power uncertainty"),
        ("cluster", "cluster-based load profiles"),
    ]
    for key, label in mapping:
        if key in text:
            feats.append(label)
    if not feats:
        feats.append("Historical load and calendar covariates (inferred from title)")
    return "; ".join(dict.fromkeys(feats))


def infer_model(title: str, abstract: str, topic: str) -> str:
    text = f"{title} {abstract}".lower()
    parts = []
    for kw in (
        "graph transformer", "graph attention-enabled transformer", "spatiotemporal graph",
        "graph neural network", "graph convolution", "multi-graph convolutional",
        "transformer", "bilstm", "lstm", "cnn", "tcn", "gru", "autoformer",
        "timegpt", "deep reinforcement learning", "federated", "bayesian-optimized",
        "particle swarm", "semi-markov", "random matrix", "knowledge distillation",
        "hierarchical multi-task", "multi-encoder transformer", "ensemble",
        "machine learning", "deep learning", "neural network", "optimization",
    ):
        if kw in text:
            parts.append(kw)
    if not parts:
        parts.append(topic.lower())
    return "; ".join(dict.fromkeys(parts))


def infer_explainability(title: str, abstract: str) -> str:
    text = f"{title} {abstract}".lower()
    if "shapley" in text or "shap" in text:
        return "SHAP / Shapley-value explainability"
    if "explainable" in text or "interpretable" in text or "xai" in text:
        return "Explainable AI framework (method not fully specified in metadata)"
    if "review" in text and "interpret" in text:
        return "Review of XAI methods (SHAP, feature importance, etc.)"
    if "knowledge distillation" in text:
        return "Indirect interpretability via knowledge distillation (not full XAI audit)"
    return "None reported in available metadata"


def stgt_relevance(topic: str, title: str, model: str, explain: str) -> str:
    notes: list[str] = []
    score = 0
    t = title.lower()
    ml = model.lower()

    graph_topic = topic in ("Graph Neural Networks", "Graph Transformers", "Spatio-Temporal Forecasting")
    shedding = topic == "Load Shedding Prediction" or "load shed" in t
    xai = "shap" in explain.lower() or topic in ("SHAP", "Explainable AI")
    multi = topic == "Multi-task Learning" or "multi-task" in ml
    stress = topic in ("Operational Stress Assessment", "Power System Reliability")

    if graph_topic:
        score += 2
        notes.append("direct architectural alignment with STGT")
    if "graph" in ml:
        score += 1
        notes.append("graph-based spatial modelling")
    if "transformer" in ml and graph_topic:
        score += 1
        notes.append("spatio-temporal transformer backbone")
    if shedding:
        score += 2
        notes.append("load-shedding focus matches project target")
    if xai:
        score += 1
        notes.append("explainability track aligns with manuscript goal")
    if multi:
        score += 1
        notes.append("multi-task formulation relevant to demand + shedding tasks")
    if stress:
        score += 1
        notes.append("operational stress/reliability assessment context")

    level = "High" if score >= 3 else ("Medium" if score >= 2 else "Low")
    if not notes:
        notes.append("peripheral: forecasting/analytics without explicit graph or shedding focus")
    return f"{level} — {'; '.join(notes)}"


def critical_review(row: pd.Series, fields: dict) -> dict:
    title = _t(row["title"])
    title_l = title.lower()
    tier = venue_tier(row["journal"], row["publisher"])
    abstract = _t(row.get("abstract", ""))
    has_abstract = len(abstract) > 80
    citations = row.get("citation_count", "")
    try:
        cites = int(citations) if str(citations).strip() not in ("", "nan") else 0
    except ValueError:
        cites = 0

    strengths, weaknesses, limitations, opportunities = [], [], [], []

    # Venue & evidence quality
    if tier == "Top-tier journal":
        strengths.append("Published in a high-impact, field-relevant journal with rigorous peer review.")
    elif tier == "Peer-reviewed journal":
        strengths.append("Journal venue provides peer-reviewed validation beyond conference abstracts.")
    elif tier == "Conference proceeding":
        weaknesses.append("Conference format often limits dataset breadth, ablation depth, and reproducibility detail.")
        limitations.append("Findings may not be fully validated across diverse grid contexts beyond the presented case.")
    else:
        weaknesses.append("Preprint/working-paper status: claims not yet fully vetted by peer review.")
        limitations.append("Methodological and empirical conclusions require cautious interpretation until journal publication.")

    if cites >= 50:
        strengths.append(f"Strong citation footprint ({cites}) suggests community uptake and methodological influence.")
    elif cites == 0:
        weaknesses.append("No citation record yet; external validation of impact is unproven.")

    if has_abstract:
        strengths.append("Sufficient abstract detail enables method-level critique beyond title inference.")
    else:
        limitations.append("Analysis constrained by missing/short abstract in catalog metadata.")
        weaknesses.append("Reproducibility assessment limited because dataset, splits, and baselines are not documented in metadata.")

    # Topic-specific reviewer critique
    topic = row["research_topic"]
    model = fields["model"]

    if topic in ("Graph Neural Networks", "Graph Transformers", "Spatio-Temporal Forecasting"):
        strengths.append("Explicitly models spatial dependencies—essential for multi-node Bangladesh grid forecasting.")
        if "transformer" in model:
            strengths.append("Transformer temporal backbone aligns with STGT sequence modelling requirements.")
        if "learn" in abstract.lower() or "graph learning" in abstract.lower() or "unknown graph" in abstract.lower():
            strengths.append("Addresses unknown/learnable graph structure—a realistic assumption for regional grids.")
        weaknesses.append("Graph topology construction (physical vs correlation-based) often under-specified for transfer to new regions.")
        limitations.append("Evaluation typically on US/EU datasets; direct transfer to Bangladesh division-level topology unverified.")
        opportunities.append("Adapt graph-learning modules to 9-division Bangladesh node set with Phase 02 correlation priors.")

    if topic == "Load Shedding Prediction":
        if "optimization" in title_l or "control" in title_l or "algorithm" in title_l:
            strengths.append("Directly targets load-shedding decision/control—high operational relevance.")
            weaknesses.append("Many works optimise shedding actions rather than forecast shedding intensity—different learning objective from STGT regression/classification.")
        if "spatial" in title_l or "cascading" in title_l:
            strengths.append("Spatial cascading perspective matches multi-node stress propagation in Bangladesh grid.")
        if "dnn" in title_l or "reinforcement" in title_l:
            weaknesses.append("Surrogate/control models may not generalise under distribution shift from rare shedding events.")
        limitations.append("Sparse shedding labels (confirmed in project Phase 02) are rarely addressed in control-oriented papers.")
        opportunities.append("Bridge shedding prediction with zero-inflated or event-aware forecasting rather than pure optimisation.")

    if topic == "Electrical Load Forecasting":
        strengths.append("Core load-forecasting competency underpins primary STGT regression heads.")
        if "hybrid" in title_l or "ensemble" in title_l:
            strengths.append("Hybrid/ensemble designs offer ablation baselines for STGT comparisons.")
        weaknesses.append("Predominantly single-series or single-site forecasting; limited multi-node coupling.")
        if "transfer learning" in title_l:
            strengths.append("Transfer-learning angle may mitigate limited Bangladesh labelled history.")
        limitations.append("Rarely models load-shedding jointly with demand; task isolation limits multi-task insight.")
        opportunities.append("Extend univariate forecast pipelines to graph-coupled multi-task targets.")

    if topic == "Multi-task Learning":
        strengths.append("Joint learning of related energy loads directly supports STGT multi-head architecture.")
        weaknesses.append("Task weighting and negative transfer risks often under-reported without uncertainty-based balancing.")
        limitations.append("Tasks are typically multi-energy (heat/gas/electricity), not demand + sparse shedding.")
        opportunities.append("Reframe multi-task heads toward demand regression + shedding event detection.")

    if topic in ("Explainable AI", "SHAP"):
        strengths.append("Directly supports explainable STGT claims required by the project manuscript.")
        if "review" in title_l:
            strengths.append("Review synthesises XAI methods applicable across baseline and proposed model.")
            limitations.append("Review paper does not provide new empirical STGT explainability evidence.")
        if "shapley" in title_l or "shap" in title_l:
            strengths.append("Game-theoretic attribution suitable for tree and neural models post-hoc.")
            weaknesses.append("SHAP for graph-temporal models is computationally expensive and may misattribute correlated regional features.")
        opportunities.append("Apply SHAP to node-level and global graph features separately for operator-facing explanations.")

    if topic == "Smart Grid Analytics":
        strengths.append("Covers demand response, cyber analytics, or AMI practices relevant to smart-grid deployment.")
        weaknesses.append("Broad analytics scope; forecasting/shedding may be secondary to control or security objectives.")
        if "federated" in title_l or "reinforcement" in title_l:
            weaknesses.append("Federated/DRL setups add deployment complexity not yet in project pipeline.")
        opportunities.append("Extract transferable covariates (AMI cadence, DR participation) for feature engineering.")

    if topic == "Operational Stress Assessment":
        strengths.append("Operational reliability/stress framing aligns with project operational-stress index (Phase 05B).")
        weaknesses.append("Often reliability-engineering stochastic models rather than ML forecasting pipelines.")
        limitations.append("May focus on transmission/HV assets rather than daily regional demand-shedding stress.")
        opportunities.append("Integrate semi-Markov / security assessment metrics as auxiliary stress labels.")

    if topic == "Power System Reliability":
        strengths.append("Resilience under extreme weather connects to Bangladesh seasonal demand peaks (Phase 02).")
        weaknesses.append("Resilience metrics (ENS, outage duration) differ from daily MW shedding targets.")
        limitations.append("DER/windstorm scenarios may not reflect Bangladesh fuel/limitation drivers documented in dataset.")
        opportunities.append("Map resilience indicators to graph-level stress covariates in STGT.")

    # Cross-cutting STGT project alignment
    if "bangladesh" not in title_l:
        limitations.append("No Bangladesh or South-Asia grid case study—external validity to project dataset is unproven.")
        opportunities.append("Replicate or benchmark on Bangladesh daily smart-grid data (project raw/interim sets).")

    if "graph" not in model and topic not in ("Explainable AI", "SHAP", "Power System Reliability"):
        weaknesses.append("Absence of explicit graph structure limits direct architectural transfer to STGT.")

    if fields["explainability_method"].startswith("None"):
        weaknesses.append("No explainability mechanism—insufficient for explainable STGT research claims.")

    # Deduplicate while preserving order
    def dedup(lst: list[str]) -> list[str]:
        seen = set()
        out = []
        for x in lst:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    return {
        "strengths": " | ".join(dedup(strengths)),
        "weaknesses": " | ".join(dedup(weaknesses)),
        "limitations": " | ".join(dedup(limitations)),
        "opportunities": " | ".join(dedup(opportunities)),
    }


def analyze_paper(row: pd.Series) -> dict:
    abstract = _t(row.get("abstract", ""))
    fields = {
        "problem": infer_problem(row["title"], row["research_topic"]),
        "dataset": infer_dataset(row["title"], abstract),
        "features": infer_features(row["title"], abstract),
        "model": infer_model(row["title"], abstract, row["research_topic"]),
        "explainability_method": infer_explainability(row["title"], abstract),
    }
    review = critical_review(row, fields)
    fields["strengths"] = review["strengths"]
    fields["weaknesses"] = review["weaknesses"]
    fields["limitations"] = review["limitations"]
    fields["future_opportunities"] = review["opportunities"]
    fields["relevance_to_stgt_paper"] = stgt_relevance(
        row["research_topic"], row["title"], fields["model"], fields["explainability_method"]
    )
    return fields


def build_model_matrix(catalog: pd.DataFrame, analysis: pd.DataFrame) -> pd.DataFrame:
    merged = catalog.merge(analysis.drop(columns=["title", "doi", "year", "research_topic", "catalog_index"], errors="ignore"), on="paper_id")
    rows = []
    for _, r in merged.iterrows():
        m = r["model"].lower()
        rows.append(
            {
                "paper_id": r["paper_id"],
                "title": r["title"],
                "year": r["year"],
                "research_topic": r["research_topic"],
                "model_reported": r["model"],
                "graph_based": any(k in m for k in ("graph", "gnn", "gcn", "graph convolution")),
                "transformer_based": "transformer" in m,
                "deep_learning": any(k in m for k in ("deep", "neural", "lstm", "gru", "cnn")),
                "optimization_control": any(k in m for k in ("optimization", "reinforcement", "particle swarm", "semi-markov")),
                "multi_task": "multi-task" in m or r["research_topic"] == "Multi-task Learning",
                "explainability_reported": not str(r["explainability_method"]).startswith("None"),
                "venue_tier": venue_tier(r["journal"], r["publisher"]),
                "stgt_relevance": r["relevance_to_stgt_paper"].split(" — ")[0],
            }
        )
    return pd.DataFrame(rows)


def build_dataset_matrix(catalog: pd.DataFrame, analysis: pd.DataFrame) -> pd.DataFrame:
    merged = catalog.merge(analysis[["paper_id", "dataset"]], on="paper_id")
    rows = []
    for _, r in merged.iterrows():
        d = r["dataset"].lower()
        rows.append(
            {
                "paper_id": r["paper_id"],
                "title": r["title"],
                "dataset_reported": r["dataset"],
                "granularity": (
                    "AMI/residential" if "ami" in d or "household" in d or "residential" in d
                    else "System/ISO" if "iso" in d or "ieee" in d
                    else "Industrial/national" if "eia" in d
                    else "Case study" if "case" in d
                    else "Unspecified"
                ),
                "geographic_scope": (
                    "US" if any(x in d for x in ("iso-ne", "eia", "us ")) else
                    "Asia-Pacific case" if any(x in d for x in ("indonesia", "puerto rico", "typhoon")) else
                    "Unspecified / multi-region" if "not" in d or "unspecified" in d else "Generalised"
                ),
                "public_availability": "Unknown from metadata" if "not" in d or "unspecified" in d else "Named public/benchmark dataset",
                "metadata_confidence": "High" if len(_t(r.get("abstract", ""))) > 80 else "Low (title/metadata inference)",
            }
        )
    return pd.DataFrame(rows)


def build_explainability_matrix(catalog: pd.DataFrame, analysis: pd.DataFrame) -> pd.DataFrame:
    merged = catalog.merge(analysis[["paper_id", "explainability_method"]], on="paper_id")
    rows = []
    for _, r in merged.iterrows():
        e = r["explainability_method"].lower()
        rows.append(
            {
                "paper_id": r["paper_id"],
                "title": r["title"],
                "explainability_method": r["explainability_method"],
                "shap_based": "shap" in e or "shapley" in e,
                "xai_review_or_framework": "review" in e or "explainable" in e,
                "post_hoc": "shap" in e or "explainable" in e or "interpretable" in e,
                "interpretable_by_design": "distillation" in e,
                "none_reported": e.startswith("none"),
                "stgt_explainability_fit": (
                    "Strong" if "shap" in e or r["research_topic"] in ("SHAP", "Explainable AI") else
                    "Partial" if "explainable" in e else "None"
                ),
            }
        )
    return pd.DataFrame(rows)


def build_limitation_catalog(analysis_df: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    rows = []
    meta = analysis_df.drop(columns=["title", "research_topic"], errors="ignore")
    merged = meta.merge(catalog[["paper_id", "title", "research_topic"]], on="paper_id")
    for _, r in merged.iterrows():
        for lim in str(r["limitations"]).split(" | "):
            lim = lim.strip()
            if not lim:
                continue
            cat = "Metadata constraint" if "metadata" in lim.lower() else (
                "Generalisation" if "bangladesh" in lim.lower() or "transfer" in lim.lower() or "unverified" in lim.lower() else
                "Task formulation" if "sparse" in lim.lower() or "objective" in lim.lower() else
                "Evidence quality" if "peer review" in lim.lower() or "conference" in lim.lower() else
                "Scope mismatch" if "hv" in lim.lower() or "der" in lim.lower() else "Methodological"
            )
            rows.append({"paper_id": r["paper_id"], "title": r["title"], "research_topic": r["research_topic"], "limitation_category": cat, "limitation": lim})
    return pd.DataFrame(rows)


def build_opportunity_catalog(analysis_df: pd.DataFrame, catalog: pd.DataFrame) -> pd.DataFrame:
    rows = []
    meta = analysis_df.drop(columns=["title", "research_topic"], errors="ignore")
    merged = meta.merge(catalog[["paper_id", "title", "research_topic"]], on="paper_id")
    for _, r in merged.iterrows():
        for opp in str(r["future_opportunities"]).split(" | "):
            opp = opp.strip()
            if not opp:
                continue
            cat = "Bangladesh validation" if "bangladesh" in opp.lower() else (
                "STGT architecture" if "stgt" in opp.lower() or "graph" in opp.lower() else
                "Multi-task extension" if "multi-task" in opp.lower() or "multi-task" in opp.lower() else
                "Explainability integration" if "shap" in opp.lower() or "explain" in opp.lower() else
                "Shedding formulation" if "shedding" in opp.lower() or "zero-inflated" in opp.lower() else
                "Feature/method transfer"
            )
            rows.append({"paper_id": r["paper_id"], "title": r["title"], "research_topic": r["research_topic"], "opportunity_category": cat, "opportunity": opp})
    return pd.DataFrame(rows)


def write_summary(
    catalog: pd.DataFrame,
    analysis: pd.DataFrame,
    model_m: pd.DataFrame,
    dataset_m: pd.DataFrame,
    explain_m: pd.DataFrame,
    lim_cat: pd.DataFrame,
    opp_cat: pd.DataFrame,
) -> None:
    rel = analysis["relevance_to_stgt_paper"].str.split(" — ").str[0]
    lines = [
        "# Phase 07B — Critical Literature Analysis Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        f"- Papers analyzed: **{len(catalog)}** (reviewer-style; not summary-only)",
        f"- Input: `references/metadata/literature_catalog.csv`",
        "",
        "## Scope compliance",
        "",
        "- Critical analysis only: strengths, weaknesses, limitations, opportunities per paper.",
        "- Comparison matrices generated for models, datasets, and explainability.",
        "- **No final research-gap synthesis** (deferred to next phase).",
        "- **No model or graph design** performed.",
        "- Locked phase outputs (Phases 01–07A) not modified.",
        "",
        "## STGT relevance distribution",
        "",
        f"- High: **{(rel == 'High').sum()}**",
        f"- Medium: **{(rel == 'Medium').sum()}**",
        f"- Low: **{(rel == 'Low').sum()}**",
        "",
        "## Cross-paper reviewer observations",
        "",
        f"- Graph-based methods: **{int(model_m['graph_based'].sum())} / {len(model_m)}** papers.",
        f"- Transformer-based methods: **{int(model_m['transformer_based'].sum())} / {len(model_m)}** papers.",
        f"- Explainability reported: **{int((~explain_m['none_reported']).sum())} / {len(explain_m)}** papers.",
        f"- Bangladesh/South-Asia case studies: **0** — universal external-validity limitation for STGT transfer.",
        f"- Metadata-limited analyses (missing abstract): **{(dataset_m['metadata_confidence'] == 'Low (title/metadata inference)').sum()} / {len(dataset_m)}** papers.",
        "",
        "## Recurring limitations (top categories)",
        "",
    ]
    for cat, cnt in lim_cat["limitation_category"].value_counts().head(6).items():
        lines.append(f"- {cat}: {cnt} entries")
    lines += ["", "## Recurring opportunities (top categories)", ""]
    for cat, cnt in opp_cat["opportunity_category"].value_counts().head(6).items():
        lines.append(f"- {cat}: {cnt} entries")
    lines += [
        "",
        "## Deliverables",
        "",
        "- `paper_analysis_catalog.csv`",
        "- `model_comparison_matrix.csv`",
        "- `dataset_comparison_matrix.csv`",
        "- `explainability_comparison_matrix.csv`",
        "- `limitation_catalog.csv`",
        "- `opportunity_catalog.csv`",
        "- `analysis_summary.md`",
        "",
        "## Next phase",
        "",
        "Ready for formal research-gap analysis (without repeating gap finalization here).",
    ]
    (ANALYSIS_DIR / "analysis_summary.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    catalog = pd.read_csv(CATALOG_PATH)
    records = []
    for _, row in catalog.iterrows():
        a = analyze_paper(row)
        a["paper_id"] = row["paper_id"]
        a["catalog_index"] = row["catalog_index"]
        a["title"] = row["title"]
        a["doi"] = row["doi"]
        a["year"] = row["year"]
        a["research_topic"] = row["research_topic"]
        records.append(a)

    analysis = pd.DataFrame(records)
    cols = [
        "catalog_index", "paper_id", "title", "doi", "year", "research_topic",
        "problem", "dataset", "features", "model", "explainability_method",
        "strengths", "weaknesses", "limitations", "future_opportunities", "relevance_to_stgt_paper",
    ]
    analysis[cols].to_csv(ANALYSIS_DIR / "paper_analysis_catalog.csv", index=False)

    model_m = build_model_matrix(catalog, analysis)
    dataset_m = build_dataset_matrix(catalog, analysis)
    explain_m = build_explainability_matrix(catalog, analysis)
    lim_cat = build_limitation_catalog(analysis, catalog)
    opp_cat = build_opportunity_catalog(analysis, catalog)

    model_m.to_csv(ANALYSIS_DIR / "model_comparison_matrix.csv", index=False)
    dataset_m.to_csv(ANALYSIS_DIR / "dataset_comparison_matrix.csv", index=False)
    explain_m.to_csv(ANALYSIS_DIR / "explainability_comparison_matrix.csv", index=False)
    lim_cat.to_csv(ANALYSIS_DIR / "limitation_catalog.csv", index=False)
    opp_cat.to_csv(ANALYSIS_DIR / "opportunity_catalog.csv", index=False)

    write_summary(catalog, analysis, model_m, dataset_m, explain_m, lim_cat, opp_cat)

    rel = analysis["relevance_to_stgt_paper"].str.split(" — ").str[0]
    print("Phase 07B critical analysis complete.")
    print(f"Papers analyzed: {len(catalog)}")
    print(f"STGT relevance — High: {(rel=='High').sum()}, Medium: {(rel=='Medium').sum()}, Low: {(rel=='Low').sum()}")
    print(f"Limitation entries: {len(lim_cat)} | Opportunity entries: {len(opp_cat)}")
    print(f"Reports -> {ANALYSIS_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
