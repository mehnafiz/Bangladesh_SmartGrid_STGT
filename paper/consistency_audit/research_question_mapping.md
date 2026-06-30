# Research Question Mapping — Consistency Audit

**Stage:** 05D — Research Consistency Audit  
**Executed:** 2026-06-30  
**Sources:** `paper/paper_outline/Paper_Outline.md`, `paper/final_results_package/`, `paper/publication_freeze/`, `experiments/` (read-only)  
**Constraint:** No experiments rerun; no results modified

---

## Summary

| RQ | Status | Evidence strength |
| --- | --- | --- |
| RQ1 | **Supported** | Strong (with S2-vs-baseline wording caveat) |
| RQ2 | **Supported** | Strong |
| RQ3 | **Supported** | Strong |
| RQ4 | **Partially Supported** | Multi-task trade-off must be stated explicitly |
| RQ5 | **Partially Supported** | Interpretability demonstrated; dual-path agreement incomplete |

**Verdict:** All five research questions are answerable in the manuscript. RQ4 and RQ5 require qualified wording (see Wording Revisions).

---

## RQ1 — Baseline superiority on macro demand MAE

**Question:** Can a spatio-temporal graph transformer outperform classical and GNN baselines on macro demand MAE?

| Field | Detail |
| --- | --- |
| **Manuscript section** | §8.1, §8.2 |
| **Supporting experiments** | Exp02, Exp02A, Exp03 (A6), Exp03B (S2) |
| **Supporting tables** | Table 3 (benchmark), Table 4 (significance), Table 6 (architecture) |
| **Supporting figures** | Figure 4 (benchmark bar chart) |
| **Primary evidence** | S2 test demand MAE **88.65 MW** vs RF **97.03 MW**, S1/B07 **93.31 MW**, T-GCN **257.21 MW** |
| **Statistical evidence** | B07 vs B02: p = 0.00135 (Bonferroni sig.); B07 vs B06: p < 10⁻⁴⁰; S2 vs S1: p = 5.5×10⁻⁵ |
| **Conclusion** | Deep graph-transformer models significantly outperform classical sequence/GNN baselines on macro demand MAE. S2 improves over the historical S1 reference and point-estimate beats RF; formal paired S2-vs-B02 Wilcoxon was not run in Exp02. |
| **Status** | **Supported** |

### Wording note

- ✅ Defensible: “S2 achieves 88.65 MW macro demand MAE, outperforming RF (97.03 MW) and the original hybrid PF-STGT S1 (93.31 MW) on the held-out test set.”
- ⚠️ Qualify: “S2 significantly outperforms S1 (p = 5.5×10⁻⁵); S1 significantly outperforms RF (p = 0.00135). S2-vs-RF improvement (−8.38 MW) is a point estimate; no independent paired test was computed for S2 vs B02.”

---

## RQ2 — Component contributions

**Question:** Which graph and architectural components contribute to demand and stress performance?

| Field | Detail |
| --- | --- |
| **Manuscript section** | §8.3, §8.4; Discussion §9.1–9.4 |
| **Supporting experiments** | Exp03, Exp03A, Exp03B |
| **Supporting tables** | Table 5 (ablations), Table 6 (S1–S4) |
| **Supporting figures** | Figure 5 (ablation bar chart) |
| **Primary evidence** | A6 (corr graph) −4.66 MW vs A1; A5 (geo-only) +4.67 MW worse; A3 ≈ A1 (no sig. diff); A2 ≈ A1; S4 (+21.32 MW) when corr graph + no transformer |
| **Interpretive layer** | Exp03A: uniform attention on S1 (entropy 0.998); geo edges add noise on Dhaka; correlation carries predictive signal |
| **Conclusion** | Correlation graph is the dominant graph contribution. Transformer removal is negligible on hybrid graph (A3) but **critical** on correlation graph (S4). Graph module (A2) and transformer (A3) show no significant isolated demand benefit on hybrid topology. |
| **Status** | **Supported** |

---

## RQ3 — Correlation vs geographical graph

**Question:** Does correlation-only adjacency outperform hybrid geographical graphs?

| Field | Detail |
| --- | --- |
| **Manuscript section** | §8.3, §8.4; Discussion §9.2 |
| **Supporting experiments** | Exp03 (A5, A6 vs A1), Exp03A, Exp03B (S1 vs S2), Exp04 (attention–adjacency ρ = 0.422) |
| **Supporting tables** | Table 5, Table 6, Table 7 (ρ row) |
| **Supporting figures** | Figure 5, Figure 7 |
| **Primary evidence** | A6 vs A1: median ΔMAE −5.43 MW, p = 5.5×10⁻⁵; A5 vs A1: +3.85 MW, p = 1.48×10⁻⁴ (Bonferroni sig. worse); S2 vs S1: −4.66 MW (−5.0%) |
| **Conclusion** | Correlation-only graph (S2/A6) significantly outperforms hybrid (S1/A1) on demand while improving stress R² (0.585 → 0.745). Geographical-only graph (A5) is significantly worse on demand. |
| **Status** | **Supported** |

---

## RQ4 — Multi-task trade-off

**Question:** Can multi-task learning deliver accurate stress forecasting without sacrificing demand accuracy vs single-task?

| Field | Detail |
| --- | --- |
| **Manuscript section** | §8.3; Discussion §9.3 |
| **Supporting experiments** | Exp01A (OSI collapse), Exp01B (W20 repair), Exp03 (A4 vs A6) |
| **Supporting tables** | Table 2 (W20 config), Table 5 (A4 vs A6) |
| **Supporting figures** | Figure 3 (training convergence context) |
| **Primary evidence** | A4 (single-task): **86.89 MW** demand MAE (best demand-only); A6/S2 (multi-task): **88.65 MW** with stress R² **0.745**; A1/S1 multi-task before corr fix: 93.31 MW, stress R² 0.585; W20 restores stress learning (Exp01B) |
| **Conclusion** | Multi-task S2 **does not sacrifice demand vs single-task S1** (improves by 4.66 MW) and enables stress R² 0.745. It **does** sacrifice ~1.76 MW vs demand-only A4 — an explicit Pareto trade-off. The question is answered affirmatively only when the comparator is the original multi-task S1, not the single-task ceiling. |
| **Status** | **Partially Supported** |

### Required manuscript framing

- State A4 as demand-only upper bound (86.89 MW).
- Do **not** claim S2 matches or beats A4 on demand.
- Frame S2 as the best **joint** demand + stress configuration.

---

## RQ5 — Interpretability

**Question:** Are S2 predictions interpretable via SHAP, attention, and OSI driver alignment?

| Field | Detail |
| --- | --- |
| **Manuscript section** | §8.5; Discussion §9.5, §9.8 |
| **Supporting experiments** | Exp04 |
| **Supporting tables** | Table 7 |
| **Supporting figures** | Figures 6a/6b, 7, 8, 9 |
| **Primary evidence** | Top stress drivers: G8 (limitation_stack), G6 (calendar_trend); Dhaka demand: G6, G4, G10; Dhaka node dominance; attention–adjacency ρ = 0.422; temporal α_t near-uniform (peak t−6); OSI driver agreement **52.2%** (13/24 cases); SHAP–permutation Spearman demand **−0.564** |
| **Conclusion** | Global and spatial attributions are coherent and operator-relevant. Dual-path OSI agreement is **partial** (not full validation). Demand SHAP and permutation rankings **disagree** — methods must be reported separately. |
| **Status** | **Partially Supported** |

### Required manuscript framing

- Use “demonstrates interpretability” rather than “fully validated interpretability.”
- Report 52.2% agreement as partial consistency, with 47.8% disagreement cases in Limitations.
- Do not claim SHAP and permutation agree on demand features.

---

## Cross-RQ dependency graph

```
Exp01/01B (W20 protocol)
    → Exp02 (+02A) ──────────────→ RQ1 (S1 vs baselines)
    → Exp03 (+03A) ──────────────→ RQ2, RQ3, RQ4
    → Exp03B (S2 selection) ─────→ RQ1 (S2 final), RQ2, RQ3
    → Exp04 (XAI on S2) ─────────→ RQ5
```

---

## Audit checklist

- [x] Every RQ mapped to ≥1 experiment
- [x] Every RQ mapped to ≥1 table or figure (RQ4 uses Table 2 + Table 5; no dedicated figure required)
- [x] Partially supported RQs flagged with wording guidance
- [x] No unsupported RQs identified
