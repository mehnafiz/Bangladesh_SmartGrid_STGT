# Phase 07A — Systematic Literature Collection

## Objective

Systematically collect high-quality literature relevant to the proposed research.

The purpose is to establish a reproducible and well-organized literature database before conducting critical analysis.

---

## Target Sources

Priority 1

- IEEE Xplore
- ScienceDirect (Elsevier)
- SpringerLink
- ACM Digital Library

Priority 2

- MDPI
- Wiley
- Nature
- arXiv (only if highly relevant)

---

## Publication Years

Priority

2023–2026

Acceptable

2021–2022

Older papers only if foundational.

---

## Research Topics

Collect papers related to

- Electrical Load Forecasting
- Load Shedding Prediction
- Smart Grid Analytics
- Graph Neural Networks
- Graph Transformers
- Spatio-Temporal Forecasting
- Explainable AI
- SHAP
- Multi-task Learning
- Operational Stress Assessment
- Power System Reliability

---

## Required Metadata

For every paper collect

- Title

- Authors

- Year

- Journal

- Publisher

- DOI

- Link

- Abstract

- Keywords

- Citation Count (optional)

---

## Folder Structure

references/

papers/

bib/

metadata/

---

## Deliverables

references/

metadata/

literature_catalog.csv

topic_distribution.csv

publisher_distribution.csv

publication_year_distribution.csv

collection_summary.md

---

## Definition of Done

✔ Papers collected

✔ Metadata complete

✔ Sources verified

✔ Organized by topic

✔ Ready for critical review

---

## Execution Record

### Completion Date

2026-06-16

### Collection Summary

* **55 papers** collected (target: 40–60).
* **100%** published 2023–2026 (priority window).
* **Priority publishers:** IEEE (33), Elsevier (20), Springer (2).
* Metadata sourced via CrossRef API with curated seed DOIs and topic-driven queries.
* Metadata only — no summaries, no research-gap analysis, no model design.

### Topic Coverage (11 research areas)

| research_topic | count |
| --- | --- |
| Electrical Load Forecasting | 20 |
| Load Shedding Prediction | 15 |
| Smart Grid Analytics | 7 |
| Graph Neural Networks | 4 |
| Explainable AI | 2 |
| Operational Stress Assessment | 2 |
| SHAP | 1 |
| Graph Transformers | 1 |
| Multi-task Learning | 1 |
| Power System Reliability | 1 |
| Spatio-Temporal Forecasting | 1 |

### Metadata Fields (per paper)

Title, Authors, Year, Journal, Publisher, DOI, Link, Abstract, Keywords, Citation Count (when available), Research Topic, Source Priority.

### Deliverables Generated

`references/metadata/`:

* `literature_catalog.csv` (55 entries)
* `topic_distribution.csv`
* `publisher_distribution.csv`
* `publication_year_distribution.csv`
* `collection_summary.md`

Folder structure:

* `references/papers/` (reserved for PDF storage)
* `references/bib/` (reserved for BibTeX)

Script: `scripts/phase_07A_literature_collection.py`

### Scope Compliance

* Systematic metadata collection only.
* Locked phase outputs (Phases 01–06) not modified.
* No paper summarization, gap identification, or model design performed.

### Recommendations for Phase 07B

* Conduct critical review and research-gap synthesis using `literature_catalog.csv`.
* Prioritize deep reading of Graph Neural Networks, Graph Transformers, Spatio-Temporal Forecasting, Load Shedding Prediction, and Multi-task Learning clusters.
* Map each literature cluster to the STGT framework components (spatial graph, temporal transformer, multi-task heads, SHAP explainability).

### Status

Ready for critical review (Phase 07B).