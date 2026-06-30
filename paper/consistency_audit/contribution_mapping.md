# Contribution Mapping — Consistency Audit

**Stage:** 05D — Research Consistency Audit  
**Executed:** 2026-06-30  
**Sources:** `paper/paper_outline/Paper_Outline.md` Part V, frozen results package, architecture freeze

---

## Summary

| ID | Contribution | Status | Action |
| --- | --- | --- | --- |
| C1 | Correlation-Aware Multi-Task Framework (S2) | **Supported** | None |
| C2 | Evidence-driven architecture simplification (S1→S2) | **Supported** | None |
| C3 | W20 multi-task loss repair | **Supported** | None |
| C4 | Rigorous empirical evaluation programme | **Supported** | Note S2-vs-RF test gap |
| C5 | Integrated explainability on frozen S2 | **Partially Supported** | Qualify agreement claims |

**Verdict:** All five contributions are publishable. C5 requires moderated language on cross-method validation.

---

## C1 — Correlation-Aware Multi-Task Forecasting Framework (S2)

**Claim:** Joint regional demand and OSI prediction via correlation-graph PF-STGT.

| Layer | Evidence |
| --- | --- |
| **Experiment** | Exp03 (A6), Exp03B (S2), Exp04 |
| **Results** | Demand MAE 88.65 MW; demand R² 0.684; stress MAE 0.0371; stress R² 0.745 |
| **Tables** | Table 3 (S2 row), Table 5 (A6), Table 6 (S2 selected), Table 7 (XAI on S2) |
| **Figures** | Figures 1–2 (architecture), 4–9 (evaluation + XAI) |
| **Checkpoint** | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| **Manuscript** | Intro §4.5; Results §8.1, §8.4, §8.5; Discussion §9.1, §9.7; Conclusion §10.2 |

**Final evidence:** S2 is the empirically selected final model with documented dual-task performance on the frozen test set (n=264).

**Status:** ✅ **Supported**

---

## C2 — Evidence-driven architecture simplification (correlation-only graph)

**Claim:** Hybrid geographical graph replaced by correlation-only adjacency based on ablation and simplification evidence.

| Layer | Evidence |
| --- | --- |
| **Experiments** | Exp03 (A5, A6), Exp03A, Exp03B (S1–S4) |
| **Results** | S2 vs S1: ΔMAE −4.66 MW (−5.0%), p = 5.5×10⁻⁵; A5 geo-only worst ablation demand (97.98 MW); S4 shows transformer required on corr graph (+21.32 MW) |
| **Tables** | Table 5, Table 6 |
| **Figures** | Figure 2 (S1→S2 decision), Figure 5 (ablation) |
| **Authority** | `experiments/architecture_freeze_revision/Final_Architecture_Decision.md` |
| **Manuscript** | Intro §4.3–4.5; Results §8.3–8.4; Discussion §9.1, §9.2, §9.4 |

**Removed component:** Geographical hybrid edges only.  
**Retained (justified):** Full transformer trunk — S4 failure proves removal is not globally safe.

**Final evidence:** Statistically significant demand improvement; geo-only significantly worse; selective simplification documented.

**Status:** ✅ **Supported**

---

## C3 — W20 multi-task loss repair

**Claim:** λ₂ = 20 with demand loss normalization enables simultaneous stress learning without OSI collapse.

| Layer | Evidence |
| --- | --- |
| **Experiments** | Exp01A (diagnosis), Exp01B (repair), Exp03 (A4 vs A6 stress) |
| **Results** | Exp01A: OSI prediction variance collapse at default weights; Exp01B W20: stress R² 0.585 (S1 test), OSI pred std restored; S2 stress R² 0.745 with W20 |
| **Tables** | Table 2 (frozen W20 config) |
| **Figures** | Figure 3 (W20 training curves, historical reference) |
| **Authority** | `experiments/experiment_01B_multitask_optimization_repair/best_configuration.md` |
| **Manuscript** | Methodology §6.7; Discussion §9.3 |

**Final evidence:** Causal chain Exp01A → Exp01B → frozen W20 protocol → S2 stress R² 0.745 is complete.

**Status:** ✅ **Supported**

---

## C4 — Rigorous empirical evaluation (benchmarks, ablations, statistics)

**Claim:** Bonferroni-corrected Wilcoxon tests, bootstrap CIs, and systematic ablation/benchmark programme.

| Layer | Evidence |
| --- | --- |
| **Experiments** | Exp02, Exp02A, Exp03, Exp03B |
| **Results** | 6 Bonferroni benchmark tests (α=0.0083); 5 ablation tests (α=0.01); bootstrap CIs in `statistical_summary.md`; Exp02A resolves R² aggregation audit |
| **Tables** | Tables 3, 4, 5, 6 |
| **Figures** | Figures 4, 5 |
| **Manuscript** | Exp. Setup §7.3–7.5; Results §8.1–8.4; Discussion §9.6 |

**Gap (document, do not overclaim):** Formal paired S2-vs-B02 Wilcoxon not in frozen artefacts. Transitive evidence (S2 < S1 < RF by point estimate; S1 vs RF p = 0.00135) is adequate if stated transparently.

**Status:** ✅ **Supported** (with reporting caveat)

---

## C5 — Integrated explainability on frozen S2

**Claim:** SHAP, attention export, and OSI driver case studies provide operator-facing interpretability.

| Layer | Evidence |
| --- | --- |
| **Experiment** | Exp04 |
| **Results** | G8/G6 top stress coalitions; G6/G4/G10 top Dhaka demand; ρ(attention, adjacency) = 0.422; 24 case studies; 52.2% OSI driver agreement |
| **Tables** | Table 7 |
| **Figures** | Figures 6a, 6b, 7, 8, 9 |
| **Manuscript** | Results §8.5; Discussion §9.5, §9.8; Conclusion §10.3 |

**Limitations (must appear in text):**

- SHAP–permutation Spearman (demand) = −0.564 → methods disagree on demand ranking.
- OSI agreement 52.2% → partial, not definitive dual-path validation.

**Recommended wording:** “provides integrated attribution analysis” / “demonstrates partial alignment with OSI drivers” — not “confirms” or “validates fully.”

**Status:** ⚠️ **Partially Supported** — contribution stands with qualified language.

---

## Contribution-to-RQ matrix

| Contribution | RQ1 | RQ2 | RQ3 | RQ4 | RQ5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| C1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| C2 | ✓ | ✓ | ✓ | — | ✓ |
| C3 | — | — | — | ✓ | — |
| C4 | ✓ | ✓ | ✓ | ✓ | — |
| C5 | — | — | — | — | ✓ |

---

## Contributions requiring revision (wording only)

| Contribution | Risky phrase | Recommended replacement |
| --- | --- | --- |
| C1 | “best demand forecasting model” | “best multi-task demand–stress trade-off” |
| C4 | “S2 significantly outperforms all baselines” | “S2 outperforms S1 and classical baselines on point estimates; S2-vs-S1 significant at p = 5.5×10⁻⁵” |
| C5 | “validates model interpretability” | “demonstrates interpretable attributions with partial OSI driver agreement (52.2%)” |

No contribution requires removal or new experiments.
