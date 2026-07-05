# Master Reference — Frozen Project Snapshot

**Revised:** 2026-06-30 (final reference revision)  
**Status:** Authoritative consolidated reference for manuscript writing  
**Sources:** Publication freeze, Final Results Package, Architecture Decision, Consistency Audit

---

## Current Paper Status

| Stage | Status | Notes |
| --- | --- | --- |
| Research Design | **Complete** | Phases 01–12; targets frozen (Phase 08.5) |
| Engineering | **Complete** | `src/`, models, training, evaluation, explainability modules |
| Experiments | **Complete** | Exp01–04 (+01A, 01B, 02A, 03A, 03B); all frozen |
| Explainability | **Complete** | Exp04 on frozen S2; figures and metrics locked |
| Publication Freeze | **Complete** | 2026-06-25; commit `dda83f1d` |
| Final Results Package | **Complete** | Tables 1–7, Figures 1–9, statistical summary |
| Paper Outline | **Complete** | `paper/paper_outline/Paper_Outline.md` |
| Consistency Audit | **Complete** | `paper/consistency_audit/`; ready for writing |
| Reference Repository | **Complete** | `paper/reference/` (this revision) |
| Manuscript Writing | **In progress** | §6.1 drafted in `06_Methodology.md`; remaining sections pending |
| Internal Review | **Pending** | After full draft assembly |
| Journal Formatting | **Pending** | `manuscript/overleaf/` export |
| Submission | **Pending** | Post-review final package |

---

## Official Manuscript Writing Order

Sections are **written** in this sequence (not journal appearance order):

| Order | Section | File |
| ---: | --- | --- |
| 1 | 6 — Methodology | `paper/sections/06_Methodology.md` |
| 2 | 7 — Experimental Setup | `paper/sections/07_Experimental_Setup.md` |
| 3 | 8 — Results | `paper/sections/08_Results.md` |
| 4 | 9 — Discussion | `paper/sections/09_Discussion.md` |
| 5 | 4 — Introduction | `paper/sections/04_Introduction.md` |
| 6 | 5 — Related Work | `paper/sections/05_Related_Work.md` |
| 7 | 10 — Conclusion | `paper/sections/10_Conclusion.md` |
| 8 | 2 — Abstract | `paper/sections/02_Abstract.md` |
| 9 | 1 — Title | `paper/sections/01_Title.md` |
| 10 | 3 — Keywords | `paper/sections/03_Keywords.md` |

**Final paper order** (journal IMRaD): 1 Title → 2 Abstract → 3 Keywords → 4 Introduction → 5 Related Work → 6 Methodology → 7 Experimental Setup → 8 Results → 9 Discussion → 10 Conclusion → 11 Appendix A (`11_Appendix_A_Supplementary_Materials.md`) → 12 References (`12_References.bib`).

---

## Manuscript section map

| § | Title | File | Draft status |
| ---: | --- | --- | --- |
| 1 | Title | `01_Title.md` | Pending |
| 2 | Abstract | `02_Abstract.md` | Pending |
| 3 | Keywords | `03_Keywords.md` | Pending |
| 4 | Introduction | `04_Introduction.md` | Pending |
| 5 | Related Work | `05_Related_Work.md` | Pending |
| 6 | Methodology | `06_Methodology.md` | §6.1 complete |
| 7 | Experimental Setup | `07_Experimental_Setup.md` | Pending |
| 8 | Results | `08_Results.md` | Pending |
| 9 | Discussion | `09_Discussion.md` | Pending |
| 10 | Conclusion | `10_Conclusion.md` | Pending |
| 11 | Appendix A | `11_Appendix_A_Supplementary_Materials.md` | Complete |
| 12 | References | `12_References.bib` | Complete (BibTeX) |

---

## Working title

Correlation-Aware Multi-Task Forecasting Framework for Regional Electricity Demand and Operational Stress Prediction in Bangladesh Smart Power Networks

---

## Final model (S2)

| Property | Value |
| --- | --- |
| **Publication name** | Correlation-Aware Multi-Task Forecasting Framework |
| **Architecture ID** | S2 |
| **Ablation ID** | A6 |
| **Benchmark ID (historical)** | B07 = S1 (not the proposed final model) |
| **Implementation** | `PFSTGT` + `GraphVariant.CORR` |
| **Graph** | Correlation-only, τ = 0.65, 33 undirected edges |
| **Parameters** | 749,058 |
| **Tasks** | Multi-task: 9-region demand + graph-level OSI |
| **Checkpoint** | `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt` |
| **S1 checkpoint (reference)** | `experiments/experiment_01B_multitask_optimization_repair/checkpoints/W20/B07/seed_42/best.pt` |

---

## Frozen test performance (n = 264 windows)

| Model | Role | Demand MAE (MW) | Demand R² | Stress MAE | Stress R² |
| --- | --- | ---: | ---: | ---: | ---: |
| **S2 / A6** | **Proposed final** | **88.65** | **0.684** | **0.0371** | **0.745** |
| S1 / A1 / B07 | Historical reference | 93.31 | 0.674 | 0.0499 | 0.585 |
| A4 | Demand-only upper bound | 86.89 | 0.731 | — | — |
| B02 (RF) | Best classical baseline | 97.03 | 0.984 | 0.0481 | 0.555 |
| B03 (XGBoost) | Classical baseline | 109.73 | 0.979 | 0.0497 | 0.525 |
| B06 (T-GCN) | GNN baseline | 257.21 | −0.483 | 0.0891 | −0.304 |
| A5 | Geo-only ablation | 97.98 | 0.554 | 0.0340 | 0.764 |
| S4 | Corr + no transformer | 114.63 | 0.362 | — | 0.747 |

---

## Key statistical results

| Comparison | Median ΔMAE (MW) | Mean ΔMAE (MW) | p (two-sided) | Bootstrap 95% CI | Bonferroni α |
| --- | ---: | ---: | ---: | --- | --- |
| S2 vs S1 (A6 vs A1) | −5.43 | −4.66 | 5.5×10⁻⁵ | [−7.17, −2.16] | 0.01 |
| B07 vs B02 (RF) | −4.92 | — | 0.00135 | [−8.87, 2.62] | 0.0083 |
| A1 vs A5 (geo-only worse) | +3.85 | — | 1.48×10⁻⁴ | [2.19, 6.90] | 0.01 |
| S1 vs S4 (simplification hurts) | +14.47 | +21.32 | <10⁻⁶ | [16.47, 26.40] | 0.01 |

**S2 vs RF:** Point estimate ΔMAE = −8.38 MW (97.03 − 88.65). No formal paired S2-vs-B02 Wilcoxon in frozen artefacts.

---

## Dataset and splits

| Property | Value |
| --- | --- |
| Regions (N) | 9 administrative divisions |
| Input window (T) | 7 days |
| Horizon (H) | 1 day (next-day) |
| Node features (F_n) | 9 per region |
| Global features (F_g) | 17 |
| Train windows | 1,281 (2019-11-21 → 2023-06-15) |
| Validation windows | 263 (2023-06-16 → 2024-03-19) |
| Test windows | 264 (2024-03-20 → 2024-12-30) |
| Primary metric | Macro demand MAE (MW) over 9 regions |
| Model selection | Validation only |

### MD5-locked artefacts

| File | MD5 |
| --- | --- |
| `data/interim/bangladesh_smartgrid_clean.parquet` | `4255024d735a91a4b53b2edee203d0ca` |
| `data/features/train_features.parquet` | `b8b3bda95d0fd6cc65f4910d85a98e16` |
| `graphs/adjacency_matrix.csv` | `dacb7ac3a827d00a4b61ea9400e75686` |

### Region order (fixed)

Barishal, Chattogram, Cumilla, Dhaka, Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet

---

## Training configuration (W20 — frozen)

| Setting | Value |
| --- | --- |
| Loss | `L = Huber(demand)/100 + λ₂ · MSE(OSI)` |
| λ₂ (stress weight) | 20.0 |
| Optimiser | **Adam**, lr = 5×10⁻⁴, weight decay = 10⁻⁴ |
| Batch size | 32 |
| Max epochs | 200 |
| Early stopping | Patience 15; score = 0.7·(val_demand_MAE/100) + 0.3·val_stress_MAE |
| Scheduler | ReduceLROnPlateau on validation demand MAE |
| Seed | 42 |
| Training time (S2 ref.) | ~393 s |

---

## Explainability headline metrics (Exp04, S2)

| Metric | Value |
| --- | ---: |
| Top stress coalition | G8 (limitation_stack), \|φ\| = 0.0191 |
| Top demand coalition (Dhaka) | G6 (calendar_trend), \|φ\| = 162.34 |
| Attention–adjacency Spearman ρ | 0.422 |
| SHAP–permutation Spearman (demand) | −0.564 |
| SHAP–permutation Spearman (stress) | 0.366 |
| OSI driver agreement (case studies) | 52.2% (13/24) |
| Peak temporal lag | t−6 (mean α = 0.162; near-uniform α_t) |
| Dhaka node SHAP mass (mean) | 340.36 |

---

## Research questions (summary)

| ID | Status |
| --- | --- |
| RQ1 — Baseline superiority on macro MAE | Supported (S2-vs-RF wording caveat) |
| RQ2 — Component contributions | Supported |
| RQ3 — Correlation vs hybrid geo graph | Supported |
| RQ4 — Multi-task without sacrificing demand | Partially supported (vs A4 trade-off) |
| RQ5 — Interpretability | Partially supported (52.2% OSI agreement) |

---

## Contributions (summary)

| ID | Status |
| --- | --- |
| C1 — S2 multi-task framework | Supported |
| C2 — Correlation-only simplification | Supported |
| C3 — W20 loss repair | Supported |
| C4 — Rigorous evaluation programme | Supported |
| C5 — Integrated explainability | Partially supported |

---

## Manuscript asset counts

| Type | Main text | Supplementary |
| --- | ---: | ---: |
| Sections | 11 | — |
| Tables | 7 | 4 (S1–S4) |
| Figures | 9 (+6b subfigure) | 5 (S1–S5) |

---

## Primary source files

| Content | Path |
| --- | --- |
| Publication tables | `paper/final_results_package/publication_tables.md` |
| Statistical summary | `paper/final_results_package/statistical_summary.md` |
| Publication figures | `paper/final_results_package/publication_figures.md` |
| Asset inventory | `paper/final_results_package/manuscript_assets_inventory.md` |
| Paper outline | `paper/paper_outline/Paper_Outline.md` |
| Claim audit | `paper/consistency_audit/claim_audit.md` |
| Architecture decision | `experiments/architecture_freeze_revision/Final_Architecture_Decision.md` |
| Model specification | `experiments/architecture_freeze_revision/final_model_specification.md` |
