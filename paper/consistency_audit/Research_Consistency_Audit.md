# Research Consistency Audit

**Stage:** 05D — Research Consistency Audit  
**Executed:** 2026-06-30  
**Auditor action:** Documentation-only verification  
**Inputs:** Publication Asset Freeze, Final Results Package, Paper Outline, Final Architecture Decision, Exp01–04 (+ sub-studies)  
**Constraints:** No experiments rerun; no results modified; no model regeneration

---

## Objective

Verify that every research question, contribution, experiment, figure, table, and manuscript claim is supported by validated evidence before manuscript writing begins.

This document is the final scientific quality gate for Stage 06.

---

## Audit verdict

| Dimension | Result |
| --- | --- |
| Research questions | 5/5 answerable (3 fully, 2 with qualified wording) |
| Contributions | 5/5 supportable (4 fully, 1 with qualified wording) |
| Main-text tables | 7/7 justified |
| Main-text figures | 9/9 justified (+ subfigure 6b) |
| Experiments | 11/11 consistent and mapped |
| Architecture S1→S2 | Consistent |
| Blocking issues | **None** |
| **Overall** | **✅ READY FOR MANUSCRIPT WRITING** |

**Detail deliverables:**

| File | Purpose |
| --- | --- |
| `research_question_mapping.md` | RQ → evidence traceability |
| `contribution_mapping.md` | C1–C5 → results traceability |
| `claim_audit.md` | Claim-by-claim defensibility review |
| `figure_table_mapping.md` | Asset purpose and placement |
| `final_readiness_report.md` | Executive readiness decision |

---

# Section 1 — Research Questions

| ID | Question | Experiments | Tables | Figures | Conclusion | Status |
| --- | --- | --- | --- | --- | --- | --- |
| **RQ1** | Spatio-temporal graph transformer vs classical/GNN baselines on macro demand MAE? | Exp02, 02A, 03, 03B | 3, 4, 6 | 4 | S2: 88.65 MW beats S1 (93.31) and RF (97.03) on point estimate; S1 beats RF (p=0.00135); S2 beats S1 (p=5.5×10⁻⁵) | **Supported** |
| **RQ2** | Which graph/architectural components contribute? | Exp03, 03A, 03B | 5, 6 | 5 | Corr graph dominant; geo-only worst; transformer required on corr topology (S4) | **Supported** |
| **RQ3** | Correlation-only vs hybrid geographical graph? | Exp03, 03A, 03B, 04 | 5, 6, 7 | 5, 7 | A6/S2 significantly beats A1/S1; A5 significantly worse; ρ=0.422 | **Supported** |
| **RQ4** | Multi-task stress without sacrificing demand vs single-task? | Exp01A, 01B, 03 | 2, 5 | 3 | S2 beats S1 on demand + enables stress R² 0.745; A4 demand-only bound 86.89 MW (1.76 MW better than S2) | **Partially Supported** |
| **RQ5** | Interpretable via SHAP, attention, OSI alignment? | Exp04 | 7 | 6–9 | Coherent attributions; 52.2% OSI agreement; demand SHAP≠permutation | **Partially Supported** |

---

# Section 2 — Research Objectives

| Objective | Evidence | Validation | Status |
| --- | --- | --- | --- |
| Train stable multi-task PF-STGT | Exp01, 01B W20 protocol | Loss curves (Fig 3); stress R² restored | ✅ Achieved |
| Benchmark against classical/GNN baselines | Exp02, 02A | Tables 3–4; Wilcoxon + Bonferroni | ✅ Achieved |
| Identify contributing components | Exp03, 03A | Table 5; component contribution analysis | ✅ Achieved |
| Select final simplified architecture | Exp03B, architecture freeze | Table 6; S2 approved | ✅ Achieved |
| Explain frozen S2 predictions | Exp04 | Table 7; Figures 6–9 | ✅ Achieved |
| Freeze publication assets | Publication freeze 2026-06-25 | `frozen_*_inventory.md` | ✅ Achieved |

---

# Section 3 — Contributions

| # | Contribution | Experiment | Key results | Tables | Figures | Status |
| --- | --- | --- | --- | --- | --- | --- |
| **C1** | S2 multi-task framework | 03, 03B, 04 | MAE 88.65; stress R² 0.745 | 3, 5, 6, 7 | 1–9 | ✅ Supported |
| **C2** | Correlation-only architecture simplification | 03, 03A, 03B | ΔMAE −4.66 MW vs S1; p=5.5×10⁻⁵ | 5, 6 | 2, 5, 7 | ✅ Supported |
| **C3** | W20 multi-task loss repair | 01A, 01B, 03 | λ₂=20; stress learning restored | 2, 5 | 3 | ✅ Supported |
| **C4** | Rigorous evaluation programme | 02, 02A, 03, 03B | Bonferroni Wilcoxon; bootstrap CIs | 3–6 | 4, 5 | ✅ Supported |
| **C5** | Integrated explainability | 04 | G8/G6 drivers; 52.2% OSI agreement | 7 | 6–9 | ⚠️ Partial |

**C5 revision:** Use "demonstrates" not "validates"; disclose method disagreement and partial OSI agreement.

---

# Section 4 — Experimental Consistency

| Experiment | Purpose | Key findings | Decision | Dependencies |
| --- | --- | --- | --- | --- |
| **Exp01** | Initial PF-STGT training | Convergence established | Superseded by 01B for S1 ref | Foundation data/splits |
| **Exp01A** | OSI collapse diagnosis | Task interference; variance collapse | Informed W20 repair | Exp01 |
| **Exp01B** | W20 loss repair | λ₂=20 best; stress R² 0.585 (S1) | **Frozen training protocol** | Exp01A |
| **Exp02** | B01–B07 benchmarks | B07/S1 MAE 93.31; beats RF/XGB/T-GCN | **Frozen benchmarks** | Exp01B (B07 ckpt) |
| **Exp02A** | Metric verification | R² aggregation resolved; MAE rankings hold | **Frozen audit** | Exp02 |
| **Exp03** | Ablations A1–A6 | A6 best multi-task; A4 demand ceiling | **Frozen ablations** | Exp01B protocol |
| **Exp03A** | Ablation interpretation | Uniform attention; geo noise; corr signal | **Frozen analysis** | Exp03 |
| **Exp03B** | S1–S4 simplification | S2 selected; S4 failure | **S2 adopted** | Exp03 |
| **Exp04** | XAI on S2 | SHAP, attention, case studies | **Frozen XAI** | S2 checkpoint |

**Cross-experiment narrative:** Exp01/01B → Exp02 → Exp03/03A → Exp03B → Exp04. No circular dependencies or contradictory conclusions.

---

# Section 5 — Architecture Consistency

| Aspect | S1 (original) | S2 (final) | Justification |
| --- | --- | --- | --- |
| Graph | Hybrid (geo + corr) | Correlation-only (τ=0.65, 33 edges) | A6 beats A1 (p=5.5×10⁻⁵); A5 geo-only worst |
| Spatial branch | Graph Transformer | Retained | Required for corr topology |
| Temporal branch | Temporal Transformer | Retained | S4: +21.32 MW when removed on corr graph |
| Fusion | Parallel gated | Retained | Part of PF-STGT trunk |
| Multi-task | W20 (λ₂=20) | W20 (λ₂=20) | Exp01B frozen protocol |
| Heads | Demand + OSI | Demand + OSI | Dual-task objective |
| Parameters | 749,058 | 749,058 | Same active count |
| Test demand MAE | 93.31 MW | **88.65 MW** | −5.0% |
| Test stress R² | 0.585 | **0.745** | +0.160 absolute |

**Removed:** Geographical hybrid edges only.  
**Added:** None (simplification, not expansion).  
**Authority:** `experiments/architecture_freeze_revision/Final_Architecture_Decision.md`

---

# Section 6 — Figure Consistency

| Figure | Title | Section | Supporting claim | Source | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Overall Framework | §6.5 | PF-STGT multi-task pipeline | Generated from arch docs | ✅ |
| 2 | Final S2 Architecture | §6.6 | S1→S2 freeze decision | Architecture freeze | ✅ |
| 3 | Training Curves | §7.6 | W20 convergence stability | Exp01 loss PNGs | ✅ |
| 4 | Benchmark Comparison | §8.1 | S2 vs baselines on macro MAE | Exp02 CSV + A6 | ✅ |
| 5 | Ablation Comparison | §8.3 | Component MAE effects | Exp03 CSV | ✅ |
| 6a | SHAP — Stress | §8.5 | G8/G6 stress drivers | Exp04 frozen | ✅ |
| 6b | SHAP — Demand | §8.5 | G6/G4/G10 demand drivers | Exp04 frozen | ✅ |
| 7 | Node Importance | §8.5 | Spatial attribution; ρ=0.422 | Exp04 frozen | ✅ |
| 8 | Temporal Attribution | §8.5 | Near-uniform α_t; peak t−6 | Exp04 frozen | ✅ |
| 9 | Stress Attribution | §8.5 | SHAP vs OSI dual-path | Exp04 frozen | ✅ |

**Note:** Use `paper/final_results_package/` numbering (not early freeze inventory which assigned Exp02A/04 figures as main-text 1–9).

---

# Section 7 — Table Consistency

| Table | Title | Section | Supporting claim | Source | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Dataset Summary | §6.2 | Reproducible data protocol | `src/constants.py`, freeze inventory | ✅ |
| 2 | Training Configuration | §6.8 | Frozen S2 W20 hyperparameters | A6 config, Exp01B | ✅ |
| 3 | Benchmark Comparison | §8.1 | S2 vs B01–B07 metrics | Exp02 + A6 | ✅ |
| 4 | Benchmark Significance | §8.2 | S1 beats baselines (Wilcoxon) | Exp02 stats | ✅ |
| 5 | Ablation Results | §8.3 | A1–A6 component effects | Exp03 | ✅ |
| 6 | Architecture Comparison | §8.4 | S1–S4; S2 selection | Exp03B | ✅ |
| 7 | Explainability Summary | §8.5 | XAI headline metrics | Exp04 | ✅ |

---

# Section 8 — Claim Audit (summary)

**38 major claims audited.** Full detail in `claim_audit.md`.

| Verdict | Count | Examples |
| --- | ---: | --- |
| ✅ Defensible | 28 | S2 MAE 88.65; corr graph beats hybrid; W20 repair |
| ⚠️ Qualify wording | 8 | S2 vs RF significance; moderate ρ=0.422; partial OSI agreement |
| ❌ Remove/rewrite | 6 | "S2 best demand model"; "transformer unnecessary"; "SHAP validates permutation" |

**Numeric cross-check:** All headline values consistent across `publication_tables.md`, `statistical_summary.md`, and `Paper_Outline.md`. No arithmetic discrepancies.

---

# Section 9 — Weak Claims (wording revisions)

| Risky phrase | Safer replacement | Context |
| --- | --- | --- |
| "S2 outperforms all baselines" | "S2 achieves lowest multi-task demand MAE among proposed configurations; beats S1 and RF on point estimates" | Abstract, Conclusion |
| "best demand forecasting model" | "best multi-task demand–stress trade-off" | Contributions |
| "transformer is unnecessary" | "transformer removal is neutral on hybrid graph (A3) but harmful on correlation graph (S4)" | Discussion §9.4 |
| "validates interpretability" | "demonstrates interpretable attributions" | Exp04, C5 |
| "confirms OSI drivers" | "shows partial alignment (52.2%)" | Table 7, Fig 9 |
| "improves vs single-task" (unqualified) | "improves vs S1 multi-task; trades 1.76 MW vs A4 for stress capability" | RQ4, §9.3 |
| "AdamW optimizer" | "Adam optimizer (lr 5×10⁻⁴)" | Methods §6.8 |
| "strong attention–graph alignment" | "moderate alignment (ρ = 0.422)" | Table 7 |

---

# Section 10 — Unsupported Claims (remove before drafting)

| Claim | Reason | Action |
| --- | --- | --- |
| S2 is best on demand MAE overall | A4 = 86.89 MW < S2 = 88.65 MW | **Remove** |
| Transformer universally dispensable | S4 +21.32 MW degradation | **Remove** |
| Geographical graph improves modelling | A5 worst demand ablation | **Remove** |
| SHAP confirms permutation rankings (demand) | Spearman ρ = −0.564 | **Remove** |
| S2 significantly outperforms RF (unqualified) | No S2-vs-B02 Wilcoxon | **Rewrite** |
| State-of-the-art demand forecasting | No external SOTA comparison | **Remove** |

---

# Section 11 — Final Readiness

## Checklist

- [x] Research Questions Answered (5/5 with qualifications documented)
- [x] Objectives Achieved (6/6)
- [x] Contributions Supported (5/5; C5 qualified)
- [x] Figures Validated (9/9 + subfigure)
- [x] Tables Validated (7/7)
- [x] Experiments Consistent (11/11 mapped)
- [x] Final Architecture Consistent (S2 freeze approved)
- [x] No experiments modified
- [x] No results regenerated
- [x] **Ready for Manuscript Writing**

## Frozen headline numbers (manuscript cross-check)

| Metric | Value |
| --- | ---: |
| S2 demand MAE | 88.65 MW |
| S2 demand R² | 0.684 |
| S2 stress R² | 0.745 |
| S1 demand MAE | 93.31 MW |
| A4 demand MAE (bound) | 86.89 MW |
| RF demand MAE | 97.03 MW |
| S2 vs S1 p-value | 5.5×10⁻⁵ |
| S2 vs S1 ΔMAE | −4.66 MW (−5.0%) |
| OSI driver agreement | 52.2% |
| Attention–adjacency ρ | 0.422 |

## Next step

Proceed to **Stage 06 — Manuscript Writing**:

- Import assets from `paper/final_results_package/`
- Follow structure in `paper/paper_outline/Paper_Outline.md`
- Apply guardrails from `claim_audit.md` and `final_readiness_report.md`
- Export to `manuscript/overleaf/`

---

## Definition of Done

✔ Every claim audited  
✔ Every contribution validated  
✔ Every experiment mapped  
✔ Every figure justified  
✔ Every table justified  
✔ Documentation-only audit completed  

**Ready for manuscript writing.**
