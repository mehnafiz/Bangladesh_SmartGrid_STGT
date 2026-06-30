# Reviewer Risk Register

**Revised:** 2026-06-30  
**Source:** Consistency audit, claim audit, experiment design, documentation discrepancies  
**Purpose:** Anticipate reviewer challenges and document evidence-based responses  
**Primary mitigation sections:** `08_Results.md`, `09_Discussion.md`  
**Format:** Risk → Likelihood → Evidence → Recommended response

---

## Risk severity legend

| Level | Meaning |
| --- | --- |
| **High** | Could trigger major revision or rejection if unaddressed |
| **Medium** | Likely reviewer comment; address in text or rebuttal |
| **Low** | Minor clarification; footnote sufficient |

---

## R1 — Single dataset / single country generalisation

| Field | Detail |
| --- | --- |
| **Risk** | Results may not generalise beyond Bangladesh grid |
| **Likelihood** | High |
| **Evidence** | One chronological dataset; no external validation |
| **Response** | State explicitly in Limitations (§9.8). Frame as case study with reproducible MD5 pipeline. Propose external validation in Future Work (§10.3). |
| **Severity** | Medium (expected for domain paper) |

---

## R2 — S2 does not beat single-task demand (A4)

| Field | Detail |
| --- | --- |
| **Risk** | "Why multi-task if A4 has lower MAE?" |
| **Likelihood** | High |
| **Evidence** | A4: 86.89 MW vs S2: 88.65 MW (−1.76 MW); A4 has no stress head |
| **Response** | Report A4 as demand-only upper bound. Frame S2 as best **joint** demand + stress model (stress R² 0.745). Discuss Pareto trade-off in §9.3. |
| **Severity** | High if unreported; Low if A4 disclosed upfront |

---

## R3 — No formal S2 vs Random Forest significance test

| Field | Detail |
| --- | --- |
| **Risk** | "Is S2 significantly better than RF?" |
| **Likelihood** | Medium |
| **Evidence** | S2 vs B02 Wilcoxon not computed; S1 vs RF p=0.00135; S2 vs S1 p=5.5×10⁻⁵ |
| **Response** | Report point estimate (−8.38 MW). State significance chain: S2 < S1 (sig.) and S1 < RF (sig.). Do not claim direct S2-vs-RF significance. |
| **Severity** | Medium |

---

## R4 — RF higher R² but worse MAE

| Field | Detail |
| --- | --- |
| **Risk** | "Why is macro MAE primary if RF has R²=0.984?" |
| **Likelihood** | High |
| **Evidence** | Exp02A aggregation audit; macro vs pooled R² discrepancy |
| **Response** | Define macro MAE as primary ranking metric in §7.3. Footnote Exp02A finding. Supplementary Table S1 optional. |
| **Severity** | Medium |

---

## R5 — Transformer necessity inconsistency (A3 vs S4)

| Field | Detail |
| --- | --- |
| **Risk** | "You removed transformer in A3 with no effect but claim it's required" |
| **Likelihood** | High |
| **Evidence** | A3 vs A1: p=0.384 (hybrid); S4 vs S1: +21.32 MW (corr graph) |
| **Response** | Always qualify A3 finding as **hybrid-graph only**. Cite S4 as proof transformer is required on correlation topology. |
| **Severity** | High if conflated; Low with clear topology-specific wording |

---

## R6 — Geographical graph motivation vs evidence

| Field | Detail |
| --- | --- |
| **Risk** | "Why assume geographic adjacency initially?" |
| **Likelihood** | Medium |
| **Evidence** | A5 geo-only worst demand (97.98 MW); Exp03A geo noise on Dhaka |
| **Response** | Present S1 as design hypothesis tested empirically. Contribution C2 is evidence-driven simplification. |
| **Severity** | Low (strengthens contribution narrative) |

---

## R7 — OSI driver agreement only 52.2%

| Field | Detail |
| --- | --- |
| **Risk** | "Explainability validation is weak" |
| **Likelihood** | High |
| **Evidence** | 13/24 case studies agree; 47.8% disagree |
| **Response** | Report as partial agreement. Disclose in Limitations. Do not claim full OSI validation. Position XAI as exploratory operator-facing analysis. |
| **Severity** | Medium |

---

## R8 — SHAP vs permutation disagreement on demand

| Field | Detail |
| --- | --- |
| **Risk** | "Which attribution method should operators trust?" |
| **Likelihood** | Medium |
| **Evidence** | Demand Spearman ρ = −0.564 |
| **Response** | Report both methods; note disagreement. Stress methods agree moderately (ρ = 0.366). Recommend ensemble interpretation. |
| **Severity** | Medium |

---

## R9 — Near-uniform temporal attention

| Field | Detail |
| --- | --- |
| **Risk** | "Temporal transformer adds complexity without interpretable benefit" |
| **Likelihood** | Medium |
| **Evidence** | Near-uniform α_t; peak t−6 only marginally higher; S4 shows functional necessity on corr graph |
| **Response** | Distinguish interpretability (uniform weights) from functional requirement (S4 degradation). Do not claim strong temporal selectivity. |
| **Severity** | Medium |

---

## R10 — S1/B07 vs S2 lineage in benchmarks

| Field | Detail |
| --- | --- |
| **Risk** | "Table 3 shows B07 but you propose S2 — inconsistent?" |
| **Likelihood** | Medium |
| **Evidence** | B07 = Exp02 S1 checkpoint; S2 = Exp03 A6; different graph variant |
| **Response** | Clarify lineage in Methods and Results opening. Label B07 as historical S1 reference; S2 as proposed final model. |
| **Severity** | High if unexplained; Low with clear labelling |

---

## R11 — Adam vs AdamW documentation mismatch

| Field | Detail |
| --- | --- |
| **Risk** | "Methods says AdamW but configs say Adam" |
| **Likelihood** | Low |
| **Evidence** | `Publication_Asset_Freeze.md` mentions AdamW; checkpoint configs use Adam |
| **Response** | Report **Adam** in Methods per frozen `config.yaml`. Optional footnote on design intent. |
| **Severity** | Low |

---

## R12 — Chronological split / no cross-year validation

| Field | Detail |
| --- | --- |
| **Risk** | "Temporal leakage or overfitting to era?" |
| **Likelihood** | Medium |
| **Evidence** | Strict chronological train/val/test; test 2024-03-20 → 2024-12-30 |
| **Response** | Document split policy Table 1. Note limitation: no multi-year external holdout. |
| **Severity** | Medium |

---

## R13 — Correlation graph threshold τ = 0.65 not ablated

| Field | Detail |
| --- | --- |
| **Risk** | "Sensitivity to τ not shown" |
| **Likelihood** | Medium |
| **Evidence** | τ fixed at 0.65 in frozen spec; no τ sweep in completed experiments |
| **Response** | Report τ as frozen design choice. List τ sensitivity as Future Work. Do not claim τ optimality. |
| **Severity** | Medium |

---

## R14 — Single seed (42)

| Field | Detail |
| --- | --- |
| **Risk** | "Results may be seed-dependent" |
| **Likelihood** | Medium |
| **Evidence** | All reference runs use seed 42 |
| **Response** | Document seed in Table 2. Note as limitation. Multi-seed study as future work. |
| **Severity** | Medium |

---

## R15 — Novelty claim inflation

| Field | Detail |
| --- | --- |
| **Risk** | "Incremental combination of known components" |
| **Likelihood** | High |
| **Evidence** | PF-STGT combines known GNN/transformer/multi-task elements |
| **Response** | Emphasise evidence-driven **simplification** (C2) and dual-task Bangladesh case study. Avoid "state-of-the-art" language. |
| **Severity** | High if overclaimed; Low with measured framing |

---

## Pre-emptive mitigation checklist

| Risk | Mitigation in manuscript |
| --- | --- |
| R2 | Introduce A4 in §8.3 before multi-task claims |
| R3 | Transparent S2-vs-RF wording in Abstract |
| R4 | Macro MAE primary metric in §7.3 |
| R5 | Topology-specific transformer discussion §9.4 |
| R7–R8 | Limitations §9.8; moderated C5 language |
| R10 | Lineage paragraph at start of §8.1 |
| R15 | Contribution framing §4.5, §10.2 |

---

## Reviewer response template (for post-submission)

```
Comment: [reviewer concern]
Response: We thank the reviewer. [Acknowledge].
Evidence: [cite Table/Figure/Experiment from this register]
Manuscript change: [section + specific addition]
```

Use frozen numbers only — cross-check `MASTER_REFERENCE.md` before any rebuttal statistic.
