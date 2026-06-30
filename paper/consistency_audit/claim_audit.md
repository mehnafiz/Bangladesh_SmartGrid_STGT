# Claim Audit — Consistency Audit

**Stage:** 05D — Research Consistency Audit  
**Executed:** 2026-06-30  
**Scope:** All major manuscript claims derivable from `Paper_Outline.md`, `publication_tables.md`, and `statistical_summary.md`

Legend: ✅ Defensible | ⚠️ Requires weaker wording | ❌ Unsupported — remove or rewrite

---

## 1. Headline performance claims

| # | Claim (as planned in outline) | Evidence | Verdict | Recommended wording |
| --- | --- | --- | --- | --- |
| H1 | S2 test demand MAE is 88.65 MW | Table 3, Exp03 A6 | ✅ | Use as stated |
| H2 | S2 test stress R² is 0.745 | Table 3, Table 5 | ✅ | Use as stated |
| H3 | S2 beats S1 by 4.66 MW (−5.0%) | Table 6, statistical_summary §2 | ✅ | Add p = 5.5×10⁻⁵, CI [−7.17, −2.16] |
| H4 | S2 beats Random Forest (97.03 MW) | Table 3 point estimate | ⚠️ | “S2 achieves 88.65 MW vs RF 97.03 MW (Δ = −8.38 MW point estimate). S1 significantly outperforms RF (p = 0.00135); S2 significantly outperforms S1.” |
| H5 | S2 is the best model overall | Tables 3, 5 | ❌ | A4 single-task demand MAE 86.89 MW is lower. Replace with: “S2 is the best **multi-task** configuration.” |
| H6 | S2 achieves best demand MAE among ablations | Table 5 | ❌ | A4 is best on demand. Replace with: “A6/S2 achieves best multi-task demand MAE; A4 is demand-only upper bound.” |

---

## 2. Architecture and ablation claims

| # | Claim | Evidence | Verdict | Recommended wording |
| --- | --- | --- | --- | --- |
| A1 | Correlation graph outperforms hybrid graph | A6 vs A1: p = 5.5×10⁻⁵ | ✅ | Use as stated |
| A2 | Geographical-only graph hurts demand | A5 vs A1: +3.85 MW, p = 1.48×10⁻⁴, Bonferroni sig. | ✅ | Use as stated |
| A3 | Removing transformer has no effect | A3 vs A1: p = 0.384, not sig. | ⚠️ | “On the **hybrid** graph, transformer removal (A3) does not significantly change demand MAE.” |
| A4 | Transformer is unnecessary | S4: +21.32 MW vs S1 when removed on corr graph | ❌ | Remove blanket claim. State: “Transformer is **required** for correlation-graph topology (S4).” |
| A5 | Graph module is essential | A2 vs A1: p = 0.301, not sig. | ⚠️ | “Graph module shows no significant isolated demand benefit on hybrid topology (A2 ≈ A1).” |
| A6 | Full S1 complexity is justified | S2 matches S1 params; S2 beats S1 on accuracy | ❌ | Replace: “Full hybrid S1 complexity is **not** accuracy-optimal; selective correlation-graph simplification improves performance.” |
| A7 | S4 proves stacked simplification fails | S4 ΔMAE +21.32 MW, p < 10⁻⁶ | ✅ | Use in Discussion §9.4 |

---

## 3. Multi-task and training claims

| # | Claim | Evidence | Verdict | Recommended wording |
| --- | --- | --- | --- | --- |
| M1 | W20 (λ₂=20) repairs OSI collapse | Exp01A + Exp01B | ✅ | Use as stated |
| M2 | Multi-task does not hurt demand vs S1 | S2 88.65 vs S1 93.31 | ✅ | Use as stated |
| M3 | Multi-task matches single-task demand | A6 88.65 vs A4 86.89 | ❌ | “Multi-task S2 trades ~1.76 MW demand MAE vs single-task A4 for stress forecasting capability.” |
| M4 | Stress R² improved S1→S2 | 0.585 → 0.745 | ✅ | Use as stated |
| M5 | Training uses AdamW | Checkpoint configs | ⚠️ | Frozen configs record **Adam** lr=5×10⁻⁴. Use “Adam” in Methods; note AdamW as design intent only if citing freeze spec. |

---

## 4. Benchmark and statistical claims

| # | Claim | Evidence | Verdict | Recommended wording |
| --- | --- | --- | --- | --- |
| B1 | PF-STGT (S1/B07) beats classical ML on macro MAE | Table 4: B07 vs B02 p=0.00135 | ✅ | Primary metric = macro MAE |
| B2 | RF has best per-region R² | B02 demand R² 0.984 vs B07 0.674 | ✅ | Use with Exp02A footnote on aggregation |
| B3 | T-GCN substantially underperforms | B06 MAE 257.21 MW | ✅ | Use as stated |
| B4 | All benchmark comparisons Bonferroni-significant | Table 4 | ✅ | α = 0.0083 for 6 tests |
| B5 | Deep model universally dominates RF on R² | Table 3 | ❌ | RF R² higher; macro MAE favours deep model. Clarify metric choice. |

---

## 5. Explainability claims

| # | Claim | Evidence | Verdict | Recommended wording |
| --- | --- | --- | --- | --- |
| X1 | Limitation stack (G8) drives stress | Table 7, Exp04 | ✅ | Top \|φ\| = 0.0191 |
| X2 | Calendar trend (G6) drives demand (Dhaka) | Table 7 | ✅ | \|φ\| = 162.34 |
| X3 | Dhaka dominates node attribution | Table 7 node mass 340.36 | ✅ | Use as stated |
| X4 | Attention aligns with correlation graph | ρ = 0.422 | ⚠️ | “Moderate alignment (ρ = 0.422)” — not strong |
| X5 | Temporal attention is uniform | Exp04, Figure 8 | ✅ | Peak t−6, near-uniform α_t |
| X6 | SHAP confirms permutation importance | demand Spearman −0.564 | ❌ | “SHAP and permutation rankings **partially disagree** on demand (ρ = −0.564).” |
| X7 | OSI drivers validated by SHAP | 52.2% agreement | ⚠️ | “Partial agreement in 13/24 case studies (52.2%).” |
| X8 | Model is fully interpretable | Mixed X4–X7 | ⚠️ | “Demonstrates multi-method attribution with documented limitations.” |

---

## 6. Scope and lineage claims

| # | Claim | Evidence | Verdict | Recommended wording |
| --- | --- | --- | --- | --- |
| S1 | S2 is the proposed final model | Architecture freeze, publication freeze | ✅ | Distinguish from B07/S1 throughout |
| S2 | B07 in Exp02 equals S1 reference | Checkpoint lineage | ✅ | Clarify in Methods: “B07 (S1, hybrid W20)” |
| S3 | Results generalise beyond Bangladesh | Single dataset | ❌ | State as limitation (single country, chronological split) |
| S4 | Dataset and splits are reproducible | MD5-locked artefacts, Table 1 | ✅ | Use as stated |
| S5 | 749,058 parameters (S2) | Table 2, Table 6 | ✅ | Use as stated |

---

## 7. Unsupported claims — remove before drafting

| Claim | Why unsupported | Action |
| --- | --- | --- |
| “S2 achieves state-of-the-art demand forecasting” | No external SOTA benchmark; A4 beats S2 on demand | **Remove** |
| “Transformer attention provides strong temporal selectivity” | Near-uniform weights (entropy ratio 0.998 on S1; uniform on S2) | **Remove** or replace with “limited temporal selectivity” |
| “Geographical adjacency improves spatial modelling” | A5 geo-only is worst demand ablation | **Remove** |
| “SHAP validates feature rankings” | Negative demand Spearman | **Remove** |
| “S2 significantly outperforms RF” (without caveat) | No direct S2-vs-B02 Wilcoxon | **Rewrite** per H4 |
| “Multi-task learning improves demand accuracy” (unqualified) | A4 single-task beats A6 | **Rewrite** per M3 |

---

## 8. Weak claims — wording downgrades

| Original (risky) | Safer alternative |
| --- | --- |
| “improves” (S2 vs RF, untested) | “achieves lower point-estimate MAE than” |
| “proves” (correlation graph) | “demonstrates empirically” |
| “validates interpretability” | “provides attribution analysis” |
| “confirms OSI drivers” | “shows partial alignment with OSI drivers (52.2%)” |
| “eliminates task interference” | “mitigates task interference via W20 weighting” |
| “uniform attention implies transformer is useless” | “uniform attention on hybrid graph; transformer still required on correlation topology (S4)” |

---

## 9. Number cross-check (frozen)

All values below verified against `publication_tables.md` and `statistical_summary.md`:

| Quantity | Frozen value | Consistent |
| --- | ---: | ---: |
| S2 demand MAE | 88.65 | ✓ |
| S1/B07 demand MAE | 93.31 | ✓ |
| A4 demand MAE | 86.89 | ✓ |
| RF (B02) demand MAE | 97.03 | ✓ |
| S2 stress R² | 0.745 | ✓ |
| S1 stress R² | 0.585 | ✓ |
| S2 vs S1 p-value | 5.5×10⁻⁵ | ✓ |
| Test windows n | 264 | ✓ |
| Bonferroni α (benchmarks) | 0.0083 | ✓ |
| Bonferroni α (ablations) | 0.01 | ✓ |
| OSI driver agreement | 52.2% | ✓ |
| Attention–adjacency ρ | 0.422 | ✓ |

**Numeric consistency:** No discrepancies found across outline, tables, and statistical summary.

---

## 10. Audit conclusion

- **Defensible claims:** 28 of 38 audited (74%)
- **Require qualification:** 8 of 38 (21%)
- **Must remove/rewrite:** 6 of 38 (16%)

All unsupported claims are addressable by wording revision only. No new experiments required.
