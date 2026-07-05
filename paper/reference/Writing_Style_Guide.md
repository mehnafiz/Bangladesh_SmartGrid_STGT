# Writing Style Guide

**Generated:** 2026-06-30  
**Purpose:** Conventions for prose, tone, and evidence discipline across all manuscript sections  
**Companion documents:** `Terminology_Guide.md`, `Notation_Guide.md`, `Claim_Guide.md`

---

## Academic tone

Write in formal third-person or passive constructions typical of IEEE and Elsevier engineering journals. Prefer precise, measured statements over promotional language. Each paragraph should advance one coherent idea: context, method, or finding. Avoid sentence fragments, colloquialisms, and unsupported superlatives.

Distinguish **observations** (what the data show) from **interpretations** (what they may imply). Use interpretive verbs only when the reference repository supports them.

---

## Preferred and discouraged wording

### Use when evidence supports

| Term | When appropriate |
| --- | --- |
| **demonstrates** | Supported by frozen results or audit |
| **indicates** | Descriptive or correlational finding |
| **suggests** | Interpretation with stated limitations |
| **achieves** | Reported metric on held-out test set |
| **is consistent with** | Alignment between methods or hypotheses |
| **outperforms** | Point estimate or validated significance (see `Claim_Guide.md`) |
| **statistically significant** | Only with reported p-value and Bonferroni context |

### Avoid unless explicitly justified

| Term | Reason |
| --- | --- |
| **proves** | Empirical studies rarely prove; use *demonstrates* |
| **guarantees** | No operational guarantee from offline evaluation |
| **revolutionary** | Promotional; not evidence-based |
| **perfect** | Overstates model or data quality |
| **always / never** | Absolute claims invite refutation |
| **impossible** | Unless formally established |
| **state-of-the-art** | No external SOTA benchmark in frozen programme |
| **novel** | Use only for contributions explicitly supported (C1–C5) |
| **validates** (interpretability) | Use *demonstrates attribution*; OSI agreement is 52.2% |
| **best model** (unqualified) | A4 beats S2 on demand; use *best multi-task configuration* |

---

## Evidence-first writing

1. State the claim.
2. Cite the frozen source (table, figure, experiment).
3. Report uncertainty (p-value, CI) when making comparative claims.
4. Note limitations where the consistency audit flags partial support (RQ4, RQ5, C5).

Never introduce a number not present in `MASTER_REFERENCE.md` or `publication_tables.md`. Copy values exactly; do not round beyond manuscript convention without checking the source.

---

## Terminology consistency

- First mention: **Operational Stress Index (OSI)**.
- Proposed model: **S2**; historical reference: **S1** / **B07**.
- Primary metric: **macro demand MAE** (MW).
- File `06_Methodology.md` ↔ manuscript **Section 6**; section numbers in outline match file prefixes (`08_Results.md` = Section 8).

Consult `Terminology_Guide.md` before introducing any model ID, graph variant, or task label.

---

## Paragraph flow

- **Opening sentence:** States the subsection topic.
- **Body:** Definitions, notation, or evidence in logical order.
- **Closing sentence:** Links to the next subsection or summarises the takeaway.

Avoid one-sentence paragraphs except for formal definitions. Limit consecutive sentences that begin with the same structure.

---

## Figure references

Format: `Fig. 4` or `Figure 4` (pick one style per section and keep consistent).

- Introduce the figure before it appears: *"Figure 4 compares test-set macro demand MAE across baselines."*
- Subfigures: `Fig. 6(a)` stress, `Fig. 6(b)` demand — or *Figure 6a/6b* per journal style.
- Do not restate every bar value; highlight the message and refer to the table for full metrics.
- Apply caption guardrails from `Figure_Index.md`.

---

## Table references

Format: `Table 3`.

- Introduce tables with their purpose: *"Table 3 summarises benchmark performance on the held-out test set."*
- Repeat only headline values in prose; full grids stay in the table.
- When citing significance, include Bonferroni α (0.0083 for benchmarks; 0.01 for ablations).

---

## Equation references

- Number displayed equations sequentially within each section (e.g., Eq. (1) in §6.1).
- Define every symbol on first use; match `Notation_Guide.md`.
- Reference as *Eq. (3)* or *Equation (3)* consistently.
- Inline math: \(N=9\), \(T=7\), \(\hat{\mathbf{y}}^{\mathrm{demand}}\).

---

## Transition writing

Between subsections, use brief bridges:

- *"Having defined the forecasting problem, the following subsection describes the dataset."*
- *"The benchmark results are examined next for statistical significance."*

Within Results, follow the frozen narrative order: benchmarks → significance → ablations → architecture selection → explainability.

---

## Reviewer-friendly writing

- Define **B07/S1 lineage** before presenting S2 as the proposed model.
- Disclose **A4 demand-only bound** (86.89 MW) when discussing multi-task performance.
- State **S2-vs-RF** as point estimate plus transitive significance where direct test is absent.
- Report **partial OSI agreement** (52.2%) and SHAP–permutation disagreement on demand.
- Document **Adam** optimizer per frozen configs (not AdamW unless footnoted as design intent).

See `Reviewer_Risk_Register.md` for anticipated challenges.

---

## Section-specific notes

| Section | File | Emphasis |
| --- | --- | --- |
| 6 Methodology | `06_Methodology.md` | Problem, data, model, training — no results |
| 7 Experimental Setup | `07_Experimental_Setup.md` | Protocol, metrics, baselines — no outcome claims |
| 8 Results | `08_Results.md` | Observations only; minimal interpretation |
| 9 Discussion | `09_Discussion.md` | Interpretation, limitations, contributions |
| 4 Introduction | `04_Introduction.md` | Motivation and gaps; cite contributions without full numbers overload |
| 2 Abstract | `02_Abstract.md` | Draft last; cross-check `Claim_Guide.md` |

---

## Citations

- Do not invent references; add entries to `paper/sections/12_References.bib` using `Citation_Map.md`. Do not create a Markdown references section.
- Cite baseline methods at first mention (RF, XGBoost, T-GCN, etc.).
- Distinguish this work (S2) from prior literature clearly.

---

## Pre-submission prose checklist

- [ ] All numbers match `MASTER_REFERENCE.md`
- [ ] Terminology matches `Terminology_Guide.md`
- [ ] Claims checked against `Claim_Guide.md`
- [ ] S2 vs S1 vs B07 roles clear
- [ ] No architecture/results content in Methods where inappropriate
- [ ] Figure and table references match `Figure_Index.md` / `Table_Index.md`
