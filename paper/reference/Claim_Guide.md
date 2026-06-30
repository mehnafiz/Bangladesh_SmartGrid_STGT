# Claim Guide

**Revised:** 2026-06-30  
**Source:** `paper/consistency_audit/claim_audit.md`, `statistical_summary.md`  
**Purpose:** Quick reference for defensible, qualified, and forbidden claims during drafting  
**Apply before:** `02_Abstract.md`, `08_Results.md`, `09_Discussion.md`, `10_Conclusion.md`  
**Legend:** ✅ Use as stated | ⚠️ Qualify wording | ❌ Remove or rewrite

---

## Headline performance

| Claim | Verdict | Approved wording |
| --- | --- | --- |
| S2 test demand MAE = 88.65 MW | ✅ | State with test set n=264 |
| S2 test stress R² = 0.745 | ✅ | Pair with stress MAE 0.0371 if reporting both |
| S2 beats S1 by 4.66 MW (−5.0%) | ✅ | Add p = 5.5×10⁻⁵, CI [−7.17, −2.16] |
| S2 beats RF (97.03 MW) | ⚠️ | Point estimate Δ = −8.38 MW; cite S1 vs RF p=0.00135 for significance chain |
| S2 is best model overall | ❌ | "S2 is the best **multi-task** configuration" |
| S2 best demand MAE among ablations | ❌ | "A6/S2 best multi-task; A4 demand-only bound 86.89 MW" |

---

## Architecture and ablation

| Claim | Verdict | Approved wording |
| --- | --- | --- |
| Correlation graph beats hybrid | ✅ | A6 vs A1: p = 5.5×10⁻⁵ |
| Geo-only graph hurts demand | ✅ | A5 vs A1: +3.85 MW, p = 1.48×10⁻⁴, Bonferroni sig. |
| Transformer removal has no effect | ⚠️ | "**On hybrid graph**, A3 ≈ A1 (p = 0.384)" |
| Transformer is unnecessary | ❌ | "Required on correlation topology — S4 +21.32 MW" |
| Graph module essential | ⚠️ | "No significant isolated benefit on hybrid (A2 ≈ A1)" |
| Full S1 complexity justified | ❌ | "Hybrid S1 not accuracy-optimal; selective simplification wins" |
| S4 stacked simplification fails | ✅ | +21.32 MW, p < 10⁻⁶ |

---

## Multi-task and training

| Claim | Verdict | Approved wording |
| --- | --- | --- |
| W20 repairs OSI collapse | ✅ | Cite Exp01A → Exp01B chain |
| Multi-task does not hurt vs S1 | ✅ | 88.65 vs 93.31 MW |
| Multi-task matches single-task demand | ❌ | "~1.76 MW trade-off vs A4 for stress capability" |
| Stress R² improved S1→S2 | ✅ | 0.585 → 0.745 |
| Optimiser is AdamW | ⚠️ | Use **Adam** per frozen configs |

---

## Benchmarks and statistics

| Claim | Verdict | Approved wording |
| --- | --- | --- |
| S1/B07 beats classical on macro MAE | ✅ | Table 4; Bonferroni α = 0.0083 |
| RF has highest per-region R² | ✅ | 0.984 vs 0.674; footnote macro vs pooled (Exp02A) |
| T-GCN substantially underperforms | ✅ | 257.21 MW MAE |
| Deep model beats RF on R² | ❌ | Clarify primary metric is macro MAE |

---

## Explainability

| Claim | Verdict | Approved wording |
| --- | --- | --- |
| G8 drives stress | ✅ | \|φ\| = 0.0191 (top coalition) |
| G6 drives Dhaka demand | ✅ | \|φ\| = 162.34 |
| Dhaka dominates node attribution | ✅ | Mass 340.36 |
| Strong attention–graph alignment | ⚠️ | "Moderate alignment (ρ = 0.422)" |
| Temporal attention uniform | ✅ | Peak t−6; near-uniform α_t |
| SHAP confirms permutation (demand) | ❌ | "Methods disagree (ρ = −0.564)" |
| OSI drivers validated | ⚠️ | "Partial agreement 52.2% (13/24)" |
| Fully interpretable model | ⚠️ | "Multi-method attribution with documented limits" |

---

## Scope and lineage

| Claim | Verdict | Approved wording |
| --- | --- | --- |
| S2 is proposed final model | ✅ | Distinguish from B07/S1 throughout |
| B07 = S1 historical reference | ✅ | Clarify in Exp02 benchmark discussion |
| Results generalise beyond Bangladesh | ❌ | State as limitation |
| Reproducible pipeline | ✅ | MD5-locked artefacts, Table 1 |
| 749,058 parameters (S2) | ✅ | Tables 2, 6 |

---

## Abstract-safe number block

Use only these frozen values in Abstract cross-check:

| Quantity | Value |
| --- | ---: |
| S2 demand MAE | 88.65 MW |
| S2 vs S1 ΔMAE | −4.66 MW (p = 5.5×10⁻⁵) |
| S2 stress R² | 0.745 |
| RF baseline MAE | 97.03 MW |
| S1 reference MAE | 93.31 MW |
| A4 demand bound | 86.89 MW (do not claim S2 beats) |

---

## Wording downgrade table

| Risky | Safer |
| --- | --- |
| improves (S2 vs RF, untested) | achieves lower point-estimate MAE than |
| proves | demonstrates empirically |
| validates interpretability | provides attribution analysis |
| confirms OSI drivers | shows partial alignment (52.2%) |
| eliminates task interference | mitigates via W20 weighting |
| uniform attention ⇒ transformer useless | uniform on hybrid; required on corr (S4) |

---

## Claims to remove entirely

1. State-of-the-art demand forecasting  
2. Transformer universally dispensable  
3. Geographical adjacency improves spatial modelling  
4. SHAP validates permutation rankings on demand  
5. S2 significantly outperforms RF (without S1 transitive caveat)  
6. Multi-task improves demand vs single-task (unqualified)

---

## Pre-submission claim checklist

- [ ] S2 labelled as proposed model; B07/S1 as historical reference
- [ ] A4 cited as demand-only upper bound
- [ ] Bonferroni α stated with p-values
- [ ] S2-vs-RF uses point estimate + significance chain
- [ ] S4 cited for transformer necessity on corr graph
- [ ] OSI agreement = 52.2% (partial)
- [ ] Demand SHAP–permutation disagreement disclosed
- [ ] Adam (not AdamW) in Methods
- [ ] All numbers match `MASTER_REFERENCE.md`
