# Contribution Map

**Revised:** 2026-06-30  
**Source:** `paper/paper_outline/Paper_Outline.md` Part V, `paper/consistency_audit/contribution_mapping.md`  
**Manuscript files:** Introduction = `04_Introduction.md`; Results = `08_Results.md`; Discussion = `09_Discussion.md`  
**Purpose:** Link each contribution to experiments, results, assets, and manuscript sections

---

## Overview

| ID | Contribution | Status | Manuscript sections |
| --- | --- | --- | --- |
| **C1** | Correlation-Aware Multi-Task Forecasting Framework (S2) | ✅ Supported | Intro §4.5; Results §8.1, §8.4, §8.5; Discussion §9.1, §9.7; Conclusion §10.2 |
| **C2** | Evidence-driven architecture simplification (S1→S2) | ✅ Supported | Intro §4.3–4.5; Results §8.3–8.4; Discussion §9.1, §9.2, §9.4 |
| **C3** | W20 multi-task loss repair | ✅ Supported | Methods §6.7; Results §8.3; Discussion §9.3 |
| **C4** | Rigorous empirical evaluation programme | ✅ Supported | Intro §4.4; Results §8.1–8.4; Discussion §9.6 |
| **C5** | Integrated explainability on frozen S2 | ⚠️ Partial | Intro §4.4 RQ5; Results §8.5; Discussion §9.5, §9.8 |

---

## C1 — S2 Multi-Task Framework

**Statement:** Joint regional demand and OSI forecasting via correlation-graph PF-STGT.

| Evidence layer | Detail |
| --- | --- |
| **Experiments** | Exp03 (A6), Exp03B (S2), Exp04 |
| **Frozen results** | Demand MAE 88.65 MW; demand R² 0.684; stress MAE 0.0371; stress R² 0.745 |
| **Tables** | 3 (S2 row), 5 (A6), 6 (S2 selected), 7 |
| **Figures** | 1, 2, 4–9 |
| **Checkpoint** | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| **RQ link** | RQ1, RQ2, RQ3, RQ4, RQ5 |

**Evidence anchor:** Best **multi-task** demand–stress trade-off on frozen test set (n=264).

**Wording guardrail:** Do not claim best demand MAE overall (A4 = 86.89 MW).

---

## C2 — Architecture Simplification (Correlation-Only Graph)

**Statement:** Hybrid geographical graph replaced by correlation-only adjacency based on empirical evidence.

| Evidence layer | Detail |
| --- | --- |
| **Experiments** | Exp03 (A5, A6), Exp03A, Exp03B |
| **Frozen results** | S2 vs S1: ΔMAE −4.66 MW (−5.0%), p = 5.5×10⁻⁵; A5 geo-only +4.67 MW worse; S4 +21.32 MW when transformer removed on corr graph |
| **Tables** | 5, 6 |
| **Figures** | 2, 5, 7 |
| **Authority** | `Final_Architecture_Decision.md` |
| **RQ link** | RQ2, RQ3 |

**Removed:** Geographical hybrid edges only.  
**Retained:** Full transformer trunk (S4 justifies).

---

## C3 — W20 Multi-Task Loss Repair

**Statement:** λ₂ = 20 with demand loss normalisation restores stress learning without OSI collapse.

| Evidence layer | Detail |
| --- | --- |
| **Experiments** | Exp01A (diagnosis), Exp01B (repair), Exp03 (A4 vs A6) |
| **Frozen results** | Exp01A variance collapse; Exp01B stress R² 0.585 (S1); S2 stress R² 0.745 |
| **Tables** | 2 |
| **Figures** | 3 |
| **Authority** | `experiment_01B_multitask_optimization_repair/best_configuration.md` |
| **RQ link** | RQ4 |

**Causal chain:** Exp01A → Exp01B → frozen W20 → S2 dual-task performance.

---

## C4 — Rigorous Empirical Evaluation

**Statement:** Systematic benchmarks, ablations, Bonferroni-corrected Wilcoxon tests, bootstrap CIs.

| Evidence layer | Detail |
| --- | --- |
| **Experiments** | Exp02, Exp02A, Exp03, Exp03B |
| **Frozen results** | 6 benchmark tests (α=0.0083); 5 ablation tests (α=0.01); Cohen's d; bootstrap CIs |
| **Tables** | 3, 4, 5, 6 |
| **Figures** | 4, 5 |
| **RQ link** | RQ1, RQ2, RQ3, RQ4 |

**Reporting caveat:** No formal S2-vs-B02 Wilcoxon; use transitive evidence transparently.

---

## C5 — Integrated Explainability

**Statement:** SHAP, attention export, and OSI driver case studies on frozen S2.

| Evidence layer | Detail |
| --- | --- |
| **Experiments** | Exp04 |
| **Frozen results** | G8/G6 top stress; G6/G4/G10 top Dhaka demand; ρ=0.422; 52.2% OSI agreement; demand SHAP–perm ρ=−0.564 |
| **Tables** | 7 |
| **Figures** | 6a, 6b, 7, 8, 9 |
| **RQ link** | RQ5 |

**Wording guardrail:** "Demonstrates attribution" not "validates"; report partial OSI agreement and method disagreement.

---

## Contribution × research question matrix

|  | RQ1 | RQ2 | RQ3 | RQ4 | RQ5 |
| --- | :---: | :---: | :---: | :---: | :---: |
| C1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| C2 | ✓ | ✓ | ✓ | — | ✓ |
| C3 | — | — | — | ✓ | — |
| C4 | ✓ | ✓ | ✓ | ✓ | — |
| C5 | — | — | — | — | ✓ |

---

## Contribution × frozen numbers (quick reference)

| ID | Key numbers | Primary experiment |
| --- | --- | --- |
| C1 | MAE 88.65 MW; stress R² 0.745 | Exp03B / Exp04 |
| C2 | ΔMAE −4.66 MW; p = 5.5×10⁻⁵ | Exp03, 03A, 03B |
| C3 | λ₂=20; stress R² 0.585→0.745 | Exp01A, 01B, 03 |
| C4 | B07 vs B02 p=0.00135; 6 Bonferroni tests | Exp02, 02A |
| C5 | G8/G6 top SHAP; ρ=0.422; 52.2% agreement | Exp04 |

---

## Section placement for Conclusion (§10.2)

Repeat C1–C5 with one-line evidence each — use frozen numbers from table above; apply Claim_Guide guardrails for C1 and C5.
