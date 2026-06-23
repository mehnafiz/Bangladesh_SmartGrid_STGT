"""Phase 07A — Systematic Literature Collection (metadata only).

Collects high-quality literature metadata for the Bangladesh Smart Grid STGT
research project. Does NOT summarize papers, identify research gaps, or design
models.

Outputs:
    references/metadata/literature_catalog.csv
    references/metadata/topic_distribution.csv
    references/metadata/publisher_distribution.csv
    references/metadata/publication_year_distribution.csv
    references/metadata/collection_summary.md
    references/papers/.gitkeep, references/bib/.gitkeep
"""

from __future__ import annotations

import html
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REF_DIR = ROOT / "references"
META_DIR = REF_DIR / "metadata"
PAPERS_DIR = REF_DIR / "papers"
BIB_DIR = REF_DIR / "bib"

TOPICS = [
    "Electrical Load Forecasting",
    "Load Shedding Prediction",
    "Smart Grid Analytics",
    "Graph Neural Networks",
    "Graph Transformers",
    "Spatio-Temporal Forecasting",
    "Explainable AI",
    "SHAP",
    "Multi-task Learning",
    "Operational Stress Assessment",
    "Power System Reliability",
]

PRIORITY_PUBLISHERS = ("ieee", "elsevier", "springer", "association for computing", "acm")

RELEVANCE_KEYWORDS = (
    "load", "power", "grid", "energy", "electric", "shedding", "forecast",
    "graph", "transformer", "gnn", "spatio", "spatial", "temporal", "smart",
    "reliability", "resilience", "stress", "explain", "shap", "multi-task",
    "multi task", "operational", "demand", "generation", "distribution",
)

EXCLUDE_TITLE = (
    "withdrawn", "financial volatility", "text spotting", "language model",
    "jiuzhang", "streamflow", "epidemic", "traffic flow", "road traffic",
    "highway load", "campus electric", "data center load forecasting: a liquid",
)

# Curated high-quality entries (DOI verified via CrossRef where possible).
CURATED: list[tuple[str, str]] = [
    ("10.1109/TSG.2023.3315750", "Graph Neural Networks"),
    ("10.1109/TSG.2023.3321116", "Electrical Load Forecasting"),
    ("10.1016/j.ijepes.2024.110074", "Graph Transformers"),
    ("10.1016/j.egyai.2024.100358", "Explainable AI"),
    ("10.1016/j.apenergy.2024.123788", "Multi-task Learning"),
    ("10.1007/s41019-023-00233-8", "Graph Neural Networks"),
    ("10.1016/j.ijepes.2023.109310", "Power System Reliability"),
    ("10.1016/j.ress.2023.109212", "Smart Grid Analytics"),
    ("10.1007/s40747-024-01578-x", "Graph Transformers"),
    ("10.1007/s10586-024-04462-y", "Graph Transformers"),
    ("10.1109/TPWRS.2024.3357748", "Operational Stress Assessment"),
    ("10.1109/icpst61417.2024.10602123", "Operational Stress Assessment"),
    ("10.1016/j.apenergy.2022.120565", "Spatio-Temporal Forecasting"),
    ("10.1109/TSG.2022.3208211", "Electrical Load Forecasting"),
    ("10.1109/ei259745.2023.10512367", "Load Shedding Prediction"),
    ("10.1109/pesgm51994.2024.10688439", "Load Shedding Prediction"),
    ("10.1109/psgec58411.2023.10256003", "Load Shedding Prediction"),
    ("10.1109/epsic63429.2024.00025", "Load Shedding Prediction"),
    ("10.1016/b978-0-443-18426-0.00002-9", "Load Shedding Prediction"),
    ("10.1109/segre58867.2023.00041", "Smart Grid Analytics"),
    ("10.1109/icsgsc59580.2023.10319230", "Spatio-Temporal Forecasting"),
    ("10.1109/TPWRS.2023.10384705", "Graph Neural Networks"),
    ("10.1109/ACCESS.2023.3334561", "Graph Neural Networks"),
    ("10.1109/TSTE.2023.3334561", "Spatio-Temporal Forecasting"),
]

TOPIC_QUERIES: dict[str, list[str]] = {
    "Electrical Load Forecasting": [
        "short-term load forecasting smart grid IEEE",
        "electric load forecasting deep learning Elsevier 2024",
        "residential load forecasting transformer",
    ],
    "Load Shedding Prediction": [
        "load shedding power system optimization IEEE",
        "under frequency load shedding smart grid",
        "optimal load shedding neural network",
    ],
    "Smart Grid Analytics": [
        "smart grid analytics machine learning IEEE",
        "demand response smart grid deep learning",
        "smart grid operational analytics",
    ],
    "Graph Neural Networks": [
        "graph neural network power system IEEE",
        "graph convolutional network load forecasting",
        "GNN power grid state estimation",
    ],
    "Graph Transformers": [
        "graph transformer spatio-temporal forecasting",
        "spatio-temporal graph attention transformer energy",
        "graph transformer time series forecasting Springer",
    ],
    "Spatio-Temporal Forecasting": [
        "spatio-temporal forecasting power load IEEE",
        "spatial temporal graph convolution energy forecasting",
        "multivariate spatio-temporal load forecasting",
    ],
    "Explainable AI": [
        "explainable artificial intelligence load forecasting",
        "interpretable machine learning smart grid",
        "XAI energy forecasting review",
    ],
    "SHAP": [
        "SHAP Shapley load forecasting explainable",
        "Shapley additive explanations energy prediction",
    ],
    "Multi-task Learning": [
        "multi-task learning load forecasting energy",
        "multi-task deep learning electricity demand",
        "hierarchical multi-task energy forecasting",
    ],
    "Operational Stress Assessment": [
        "operational reliability power system assessment",
        "grid operational resilience stress metrics",
        "power system operational risk assessment",
    ],
    "Power System Reliability": [
        "power system reliability assessment smart grid",
        "distribution network resilience reliability Elsevier",
        "cyber physical power system reliability",
    ],
}


def crossref_search(query: str, rows: int = 12) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "query": query,
            "rows": rows,
            "filter": "from-pub-date:2023,until-pub-date:2026",
            "select": "DOI,title,author,published-print,published-online,created,"
            "publisher,container-title,abstract,subject,link,is-referenced-by-count",
        }
    )
    url = f"https://api.crossref.org/works?{params}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read())["message"]["items"]


def crossref_work(doi: str) -> dict | None:
    try:
        url = f"https://api.crossref.org/works/{urllib.parse.quote(doi.lower())}"
        with urllib.request.urlopen(url, timeout=20) as resp:
            return json.loads(resp.read())["message"]
    except Exception:
        return None


def extract_year(item: dict) -> int | None:
    for key in ("published-print", "published-online", "created"):
        dp = item.get(key, {})
        parts = dp.get("date-parts", [[None]])
        if parts and parts[0][0]:
            return int(parts[0][0])
    return None


def extract_authors(item: dict) -> str:
    authors = item.get("author", [])
    names = []
    for a in authors[:8]:
        given = a.get("given", "")
        family = a.get("family", "")
        names.append(f"{given} {family}".strip())
    if len(authors) > 8:
        names.append("et al.")
    return "; ".join(names)


def extract_abstract(item: dict) -> str:
    ab = item.get("abstract", "")
    if not ab:
        return ""
    return re.sub(r"<[^>]+>", "", ab).strip()


def extract_link(item: dict, doi: str) -> str:
    for link in item.get("link", []):
        if link.get("intended-application") == "text-mining":
            return link.get("URL", "")
    return f"https://doi.org/{doi}"


def is_priority_publisher(publisher: str) -> bool:
    p = publisher.lower()
    return any(k in p for k in PRIORITY_PUBLISHERS)


def is_relevant(title: str, abstract: str = "") -> bool:
    text = f"{title} {abstract}".lower()
    if any(x in text for x in EXCLUDE_TITLE):
        return False
    return any(k in text for k in RELEVANCE_KEYWORDS)


def classify_topic(title: str, abstract: str, default: str) -> str:
    text = f"{title} {abstract}".lower()
    # Order matters: specific topics before generic load forecasting.
    rules = [
        ("SHAP", ("shap", "shapley additive", "shapley values", "shapley value")),
        ("Explainable AI", ("explainability and interpretability", "explainable artificial intelligence", "explainable electrical", "xai", "interpretable machine learning", "interpretable deep learning")),
        ("Load Shedding Prediction", ("load shed", "under-frequency", "under frequency", "ufls")),
        ("Multi-task Learning", ("multi-task", "multi task", "multitask", "hierarchical multi-task")),
        ("Graph Transformers", ("graph transformer", "graph-based transformer", "graph attention transformer", "graph attention-enabled transformer", "stgt", "graphdeformer")),
        ("Graph Neural Networks", ("graph neural", "gnn", "graph convolution", "graph convolutional")),
        ("Spatio-Temporal Forecasting", ("spatio-temporal", "spatiotemporal", "spatial-temporal", "spatial temporal")),
        ("Operational Stress Assessment", ("operational stress", "operational reliability", "operational risk", "operational resilience")),
        ("Power System Reliability", ("reliability assessment", "resilience assessment", "risk quantification", "cyber-physical", "cyber physical")),
        ("Smart Grid Analytics", ("smart grid", "demand response", "demand-side", "microgrid analytics")),
        ("Electrical Load Forecasting", ("load forecast", "demand forecast", "power forecast", "energy forecast", "load forecasting")),
    ]
    for topic, kws in rules:
        if any(k in text for k in kws):
            return topic
    return default


def normalize_publisher(name: str) -> str:
    n = name.lower()
    if "ieee" in n:
        return "IEEE"
    if "elsevier" in n:
        return "Elsevier"
    if "springer" in n:
        return "Springer"
    if "acm" in n or "association for computing" in n:
        return "ACM"
    return name


def row_from_item(item: dict, topic: str) -> dict | None:
    doi = item.get("DOI", "")
    if not doi:
        return None
    title = html.unescape(item.get("title", [""])[0])
    publisher = item.get("publisher", "")
    year = extract_year(item)
    if year is None or year < 2021:
        return None
    if year > 2026:
        return None
    if not is_priority_publisher(publisher):
        return None
    abstract = extract_abstract(item)
    if not is_relevant(title, abstract):
        return None
    journal = ""
    if item.get("container-title"):
        journal = html.unescape(item["container-title"][0])
    assigned = classify_topic(title, abstract, topic)
    return {
        "paper_id": doi.replace("/", "_").lower(),
        "title": title,
        "authors": extract_authors(item),
        "year": year,
        "journal": journal,
        "publisher": normalize_publisher(publisher),
        "doi": doi,
        "link": extract_link(item, doi),
        "abstract": abstract,
        "keywords": "; ".join(item.get("subject", [])[:10]) if item.get("subject") else "",
        "citation_count": item.get("is-referenced-by-count", ""),
        "research_topic": assigned,
        "source_priority": "Priority 1" if any(
            x in publisher.lower() for x in ("ieee", "elsevier", "springer", "acm")
        ) else "Priority 2",
        "collection_method": "CrossRef",
    }


def collect_literature(target_min: int = 45, target_max: int = 55) -> pd.DataFrame:
    catalog: dict[str, dict] = {}

    # 1) Curated entries (fetch metadata from CrossRef).
    for doi, topic in CURATED:
        item = crossref_work(doi)
        if item is None:
            continue
        row = row_from_item(item, topic)
        if row:
            catalog[row["doi"].lower()] = row
        time.sleep(0.15)

    # 2) Topic-driven CrossRef discovery.
    for topic, queries in TOPIC_QUERIES.items():
        for query in queries:
            try:
                items = crossref_search(query, rows=10)
            except Exception:
                continue
            for item in items:
                row = row_from_item(item, topic)
                if row:
                    catalog[row["doi"].lower()] = row
            time.sleep(0.35)
            if len(catalog) >= target_max + 10:
                break
        if len(catalog) >= target_max + 10:
            break

    df = pd.DataFrame(list(catalog.values()))
    if df.empty:
        return df

    # Prefer 2023-2026, then sort by year desc and trim to target range.
    df["year_priority"] = df["year"].apply(lambda y: 0 if 2023 <= y <= 2026 else 1)
    df = df.sort_values(["year_priority", "year"], ascending=[True, False])
    if len(df) > target_max:
        df = df.head(target_max)
    elif len(df) < target_min:
        pass  # keep all found
    df = df.drop(columns=["year_priority"]).reset_index(drop=True)
    df.insert(0, "catalog_index", range(1, len(df) + 1))
    return df


def write_distribution(df: pd.DataFrame, col: str, out_name: str) -> pd.DataFrame:
    dist = df[col].value_counts().reset_index()
    dist.columns = [col, "count"]
    dist["percentage"] = (dist["count"] / len(df) * 100).round(2)
    dist.to_csv(META_DIR / out_name, index=False)
    return dist


def main() -> None:
    for d in (REF_DIR, META_DIR, PAPERS_DIR, BIB_DIR):
        d.mkdir(parents=True, exist_ok=True)
    (PAPERS_DIR / ".gitkeep").touch()
    (BIB_DIR / ".gitkeep").touch()

    catalog = collect_literature(target_min=45, target_max=55)
    if len(catalog) < 40:
        raise RuntimeError(f"Only collected {len(catalog)} papers; target is 40-60.")

    catalog.to_csv(META_DIR / "literature_catalog.csv", index=False)
    topic_dist = write_distribution(catalog, "research_topic", "topic_distribution.csv")
    pub_dist = write_distribution(catalog, "publisher", "publisher_distribution.csv")
    year_dist = write_distribution(catalog, "year", "publication_year_distribution.csv")

    y2326 = int(((catalog["year"] >= 2023) & (catalog["year"] <= 2026)).sum())
    summary = [
        "# Phase 07A — Literature Collection Summary",
        "",
        f"- Completion date: {datetime.now(timezone.utc).date().isoformat()}",
        f"- Total papers collected: **{len(catalog)}**",
        f"- Publications 2023–2026: **{y2326}** ({round(y2326/len(catalog)*100,1)}%)",
        f"- Priority publishers (IEEE/Elsevier/Springer/ACM): **{len(catalog)}**",
        "",
        "## Scope compliance",
        "",
        "- Metadata-only collection. No paper summaries, no research-gap analysis, no model design.",
        "- Locked phase outputs (Phases 01–06) not modified.",
        "",
        "## Topic coverage",
        "",
        "| research_topic | count |",
        "| --- | --- |",
    ]
    for _, r in topic_dist.iterrows():
        summary.append(f"| {r['research_topic']} | {int(r['count'])} |")
    summary += [
        "",
        "## Publisher coverage",
        "",
        "| publisher | count |",
        "| --- | --- |",
    ]
    for _, r in pub_dist.head(10).iterrows():
        summary.append(f"| {r['publisher']} | {int(r['count'])} |")
    summary += [
        "",
        "## Deliverables",
        "",
        "- `references/metadata/literature_catalog.csv`",
        "- `references/metadata/topic_distribution.csv`",
        "- `references/metadata/publisher_distribution.csv`",
        "- `references/metadata/publication_year_distribution.csv`",
        "- `references/metadata/collection_summary.md`",
        "- `references/papers/` (reserved for PDF storage)",
        "- `references/bib/` (reserved for BibTeX)",
        "",
        "## Next phase",
        "",
        "Ready for Phase 07B critical literature review and gap analysis.",
    ]
    (META_DIR / "collection_summary.md").write_text("\n".join(summary) + "\n")

    print("Phase 07A literature collection complete.")
    print(f"Papers collected: {len(catalog)}")
    print(f"2023-2026: {y2326}")
    print(f"Topics: {catalog['research_topic'].nunique()}")
    print(f"Catalog -> {META_DIR / 'literature_catalog.csv'}")


if __name__ == "__main__":
    main()
