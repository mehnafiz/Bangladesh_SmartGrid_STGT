# Submission Review Report — Final Internal Pre-Submission Review

**Document:** `paper/conference/main.pdf`  
**Review date:** 5 July 2026  
**Reviewer role:** IEEE Associate Editor (internal acceptance-quality review)  
**Compile status:** `pdflatex` × 2 + `bibtex` — **6 pages, 0 errors, 0 overfull boxes**

---

## Executive Summary

The conference manuscript was reviewed from the **rendered PDF** (all six pages), cross-checked against `paper/template/`, `paper/publication_freeze/`, and frozen experiment inventories. Scientific content is internally consistent with the publication freeze. Three objective presentation fixes were applied during this review. No blocking defects remain.

---

## Category Verdicts

| Category | Verdict | Notes |
|---|---|---|
| **Scientific quality** | **PASS** | Logical chain intact; limitations honest; frozen numbers consistent |
| **Writing** | **PASS** | Dense but clear; one Wilcoxon paragraph reordered for clarity |
| **Figures** | **PASS** | Figs. 1–2 vector TikZ; Figs. 3–4 PDF vector; Fig. 5 raster (acceptable) |
| **Tables** | **PASS** | Ablation table completed to match Fig. 4 and text |
| **Layout** | **PASS** | 6 pages; no overfull; minor float separation on Fig. 5 |
| **IEEE compliance** | **PASS** | IEEEtran conference class; correct numbering and reference style |
| **Camera-ready quality** | **PASS** | Template-derived author block; unified figure palette |
| **Reviewer readiness** | **PASS** | Anticipated Reviewer #2 concerns documented below |

---

## Category 1 — Scientific Logic

### Strengths
- **Research question** is explicit and answered: one spatio-temporal framework can jointly forecast regional demand and OSI on Bangladesh data.
- **Contribution enumeration** (five items) maps cleanly to results: correlation graph, multi-task loss, benchmarks, ablations, explainability.
- **Methodology** is complete for a 6-page conference paper: problem formulation, OSI definition with leakage guard, graph construction, architecture, loss repair.
- **Experimental design** is justified: chronological split, frozen feature store, shared windowing, Wilcoxon with Bonferroni, bootstrap CIs.
- **Discussion** goes beyond restating numbers — explains *why* correlation beats geography, *why* multi-task trade-off exists, Bangladesh-specific implications, deployment caveats, and limitations.
- **Conclusion** matches results without overclaiming; deployment qualified as offline evaluation.

### Weaknesses identified (not blocking)
| Issue | Severity | Status |
|---|---|---|
| OSI lacks inferential tests | Medium | Explicitly stated in Results and Limitations |
| A3 (no transformer) not distinguishable from A1 | Low | Correctly reported; supports correlation-graph focus over component removal |
| Benchmark Table II omits B01, B04, B05 | Low | Intentional conference compression; values cited in prose |
| Novelty is incremental (graph transformer + multi-task on one national dataset) | Low | Framed as case study + empirical graph-prior lesson |
| Explainability discordance (ρ = −0.564) weakens XAI claims | Low | Honestly reported; not oversold |

**Verdict: PASS**

---

## Category 2 — Writing

### Page-by-page assessment

| Section | Assessment |
|---|---|
| **Abstract** | Complete, quantitative, scoped to offline evaluation. No math in abstract (IEEE compliant). |
| **Introduction** | Strong motivation; gap articulation clear; contributions enumerated. |
| **Methodology** | Technical but readable; OSI components explained operationally. |
| **Experimental Setup** | Concise; metrics and testing protocol clear. |
| **Results** | Numbers match frozen inventory; Wilcoxon paragraph improved during review. |
| **Discussion** | Substantive; subsection titles aid navigation; limitations thorough. |
| **Conclusion** | Mirrors abstract without new claims. |

### Style notes (not changed — subjective or low priority)
- Mixed British/American spelling (`synchronised`, `favours`, `behaviour`, `Optimiser`) — common in South Asian English academic writing; not erroneous.
- Opening discussion sentence (“These results demonstrate…”) is conventional, not defective.
- “Correlation-Aware Multi-Task Forecasting Framework” vs title “Correlation-Aware Graph Transformer” — naming slightly redundant but consistent with journal lineage.

### Modification made
- **Results §IV-A:** Reordered Wilcoxon paragraph to lead with S2 vs B07 (primary result), then note B07 vs other baselines — removes reader confusion when B07 was mentioned before S2.

**Verdict: PASS**

---

## Category 3 — Figures

| Fig. | Content | Format | Quality | Placement |
|---|---|---|---|---|
| **1** | PF-STGT framework | TikZ vector | Professional; clear hierarchy | Page 2, after first citation ✓ |
| **2** | S2 architecture | TikZ vector | Consistent with Fig. 1 | Page 2, after Eq. (3) ✓ |
| **3** | Benchmark MAE bars | PDF vector | Clean; palette matches schematics | Page 3 with Table II ✓ |
| **4** | Ablation MAE bars | PDF vector | All A1–A6 shown | Page 3–4 with Table III ✓ |
| **5** | Node attribution heatmap | PNG raster | Acceptable at column width; only non-vector figure | Floats to page 5 top (minor) |

### Figure inspection
- **Resolution:** No blurry text on Figs. 1–4; Fig. 5 adequate at 0.92× column width.
- **Fonts:** TikZ uses LaTeX Type 1 fonts; bar charts use publication asset pipeline fonts.
- **Colours:** Unified palette (`#2c5282`, `#276749`, `#3182ce`) across all figures.
- **Labels/captions:** All captions end with period (IEEE figure style); informative without redundancy.
- **Citation order:** Fig. 1 → 2 → 3 → 4 → 5 in text; sequential numbering correct.

### Modification made
- **Fig. 5:** Scaled to `0.92\linewidth` to improve column-fit probability.

**Verdict: PASS** (Fig. 5 raster noted as manual optional upgrade)

---

## Category 4 — Tables

| Table | Content | Assessment |
|---|---|---|
| **I** | Dataset + training config | Merged layout efficient; `\resizebox` clean; no overflow |
| **II** | Benchmark comparison | Subset of models; Wilcoxon row in footer; readable |
| **III** | Ablation A1–A6 | **Completed during review** — now matches Fig. 4 |

### Modification made
- **Table III:** Added A3 (No Transformer, 92.64 MW) and A2 (No Graph, 93.93 MW) rows in MAE-sorted order aligned with Fig. 4. Resolves table–figure inconsistency that Reviewer #2 would flag.

**Verdict: PASS**

---

## Category 5 — Author Block

Compared against `paper/template/IEEE-conference-template-062824/IEEE-conference-template-062824.tex`:

| Template element | Implementation |
|---|---|
| `\IEEEauthorblockN{}` / `\IEEEauthorblockA{}` | ✓ `authors.tex` |
| Four-line affiliation block (dept / org / city / email) | ✓ All six authors |
| `\and` separators | ✓ |
| Italic department and organisation | ✓ |
| No custom spacing hacks | ✓ |

**Visual check (Page 1):** Six-author two-column block fills first page naturally; abstract follows immediately. Matches accepted IEEE conference first-page aesthetics. Ordinals (`1st`, `2nd`) correctly omitted for real author names.

**Verdict: PASS**

---

## Category 6 — Page Layout

| Page | Balance | Issues |
|---|---|---|
| **1** | Title + 6 authors + abstract + keywords + intro start | None |
| **2** | Methodology + Figs. 1–2 + Table I | Dense but balanced |
| **3** | Results + Table II + Fig. 3 + Wilcoxon text | Good |
| **4** | Regional analysis + ablation + Table III + Fig. 4 + explainability | Full column |
| **5** | Fig. 5 float + Discussion (5 subsections) | Fig. 5 separates from explainability text (minor) |
| **6** | Conclusion + Acknowledgment + References (22) | Reference column slightly short (typical) |

- **Overfull hboxes:** 0  
- **Widows/orphans:** Controlled via penalties; no visible defects in PDF  
- **Equation spacing:** OSI align block and loss equation clean  
- **Caption spacing:** 4 pt above (configured in preamble)

**Verdict: PASS**

---

## Category 7 — IEEE Compliance

| Requirement | Status |
|---|---|
| `IEEEtran` conference class | ✓ |
| Abstract + Index Terms | ✓ |
| Section numbering I–VI | ✓ |
| Figure/table numbering sequential | ✓ (internal labels `fig:4`, `fig:5`, `fig:7` render as Figs. 3–5) |
| Equation numbering | ✓ (1)–(3) |
| IEEE bibliography style | ✓ 22 references, chronological citation order |
| No math in title/abstract | ✓ |
| Table captions without trailing period | ✓ |
| Figure captions with period | ✓ |
| Cross-references (`Section~\ref`, `Table~\ref`, `Fig.~\ref`, `Eq.~\eqref`) | ✓ |

**Verdict: PASS**

---

## Category 8 — Reviewer #2 Perspective

### Likely criticisms
1. **“Single-country case study — generalisation?”**  
   → Mitigated by explicit limitations and South Asian replication proposal.

2. **“Why correlation graph when A3 shows transformer removal doesn't matter?”**  
   → A3 tests hybrid-graph trunk without transformer; S2 vs A1 still shows 4.66 MW gain from correlation graph + full architecture. Could be clearer but not contradictory.

3. **“OSI is engineered — not a standard metric.”**  
   → OSI components defined in Eq. (1) with operational semantics; acknowledged as composite index.

4. **“B02 has R² 0.984 but worse MAE — confusing.”**  
   → Addressed in Results with explicit MAE vs R² ranking discussion.

5. **“Explainability adds little (52% agreement, negative ρ).”**  
   → Discordance reported; framed as transparency not causal proof.

6. **“Six student authors + one supervisor — contribution clarity?”**  
   → Author block is standard; not a manuscript defect.

**None of these warrant rejection; all are addressable in rebuttal if raised.**

**Verdict: PASS**

---

## Modifications Made During This Review

| # | File | Change | Rationale |
|---|---|---|---|
| 1 | `tables/table_03_ablation.tex` | Added A2, A3 rows (full A1–A6) | Table–figure–text consistency |
| 2 | `sections/04_results.tex` | Reordered Wilcoxon paragraph (S2 vs B07 first) | Removes logical confusion |
| 3 | `figures/figure_07.tex` | `width=0.92\linewidth` | Improve column fit for heatmap |

**No scientific numbers, claims, or conclusions were altered.**

---

## Remaining Weaknesses (Non-Blocking)

| # | Weakness | Recommendation |
|---|---|---|
| 1 | Fig. 5 remains raster PNG | Optional: regenerate as PDF from frozen Exp04 script |
| 2 | Table II omits B01/B04/B05 | Acceptable for page limit; full table in journal version |
| 3 | Fig. 5 floats to page 5 while cited on page 4 | Acceptable IEEE float behaviour; no fix without `[H]` |
| 4 | British/American spelling mix | Optional harmonisation to US English if venue requires |
| 5 | Internal `\label{fig:4}` vs rendered “Fig. 3” | Maintenance-only; does not affect PDF |
| 6 | `publication_freeze/` at `paper/publication_freeze/` not repo root | Documentation path only |

---

## Manual Recommendations Before Upload

1. **Verify PDF visually** in a PDF viewer (not only LaTeX log) after final compile — confirm Table III shows six ablation rows.
2. **Check conference page limit** — current 6 pages is within typical IEEE 6–8 page caps; confirm venue-specific limit.
3. **Confirm author emails** and supervisor affiliation with all co-authors.
4. **IEEE PDF eXpress** (if required by venue): run after upload; expect pass on Type 1 fonts (TikZ + Times).
5. **Copyright / funding footnote:** Template `\thanks{}` for funding is absent — add only if agency requires it.

---

## Compile Verification

```
pdflatex → bibtex → pdflatex × 2
Output: main.pdf (6 pages)
Errors: 0 | Overfull: 0 | Undefined references: 0
```

---

## Final Determination

All eight review categories: **PASS**

---

# READY FOR IEEE SUBMISSION
