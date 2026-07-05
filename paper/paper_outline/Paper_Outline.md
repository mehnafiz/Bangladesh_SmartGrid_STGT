# Paper Outline — Manuscript Blueprint

**Stage:** 05C — Paper Outline  
**Generated:** 2026-06-16  
**Status:** Blueprint only — no manuscript prose  
**Asset sources:** `paper/publication_freeze/`, `paper/final_results_package/`  
**Final model:** S2 — Correlation-Aware Multi-Task Forecasting Framework (A6, seed 42)

---

## Working Title

Correlation-Aware Multi-Task Forecasting Framework for Regional Electricity Demand and Operational Stress Prediction in Bangladesh Smart Power Networks

---

## Execution Record — Stage 05C

| Field | Value |
| --- | --- |
| **Inputs read** | Publication Asset Freeze, Final Results Package, Final Architecture Decision, Exp01–04 (+01A, 01B, 02A, 03A, 03B) |
| **Output** | `paper/paper_outline/Paper_Outline.md` |
| **Experiments rerun** | None |
| **Figures/tables modified** | None |
| **Manuscript text written** | None (structure and mapping only) |

---

# Part I — Manuscript Hierarchy

Numbering follows standard journal IMRaD structure. Bullet items list **topics to address** when drafting; they are not draft prose.

---

## 1. Title

- Final publication title (working title above or journal-adjusted variant)
- Optional subtitle clarifying dual-task scope (demand + operational stress)

---

## 2. Abstract

**Structure (5 sentences max per block; draft later):**

| Block | Content directive | Primary evidence source |
| --- | --- | --- |
| Background | Bangladesh grid forecasting context; multi-region demand + operational stress | Dataset freeze, Introduction |
| Problem | Limitations of single-task / non-graph approaches for coupled demand–stress forecasting | Related Work gap |
| Proposed method | S2: correlation-graph PF-STGT with multi-task W20 training | Architecture freeze, Methodology |
| Results | S2 test MAE 88.65 MW; beats RF (97.03 MW) and S1 (93.31 MW); stress R² 0.745 | Tables 3, 5, 6; `statistical_summary.md` |
| Contributions | 4–5 numbered contributions (see Part V) | Contribution mapping |

**Key numbers for abstract cross-check (frozen):**

| Claim | Value |
| --- | ---: |
| S2 demand MAE | 88.65 MW |
| S2 vs S1 ΔMAE | −4.66 MW (p = 5.5×10⁻⁵) |
| S2 stress R² | 0.745 |
| Best classical baseline | RF 97.03 MW |

---

## 3. Keywords

Target 6–8 terms (select during drafting):

- Load forecasting
- Operational stress index
- Graph neural network
- Spatio-temporal transformer
- Multi-task learning
- Explainable AI (XAI)
- Bangladesh power grid
- Correlation graph

---

## 4. Introduction

### 4.1 Background

- National grid context (9 divisions, daily operational reporting)
- Simultaneous need for demand and stress visibility
- Role of data-driven forecasting in smart-grid planning

### 4.2 Motivation

- Operational Stress Index (OSI) as system-health signal alongside demand
- Spatial coupling across regions; temporal lag structure (T=7)
- Need for interpretable multi-task models for operator trust

### 4.3 Research Gap

- Gap vs classical per-region ML (no graph, no stress head)
- Gap vs pure GNN/temporal baselines (T-GCN underperforms)
- Gap vs hybrid-graph assumptions (geographical prior may add noise — Exp03A)
- Gap in explainability for coupled demand–stress forecasting (Exp04)

### 4.4 Research Questions

| ID | Question | Answered in |
| --- | --- | --- |
| RQ1 | Can a spatio-temporal graph transformer outperform classical and GNN baselines on macro demand MAE? | §8.1 (Exp02) |
| RQ2 | Which graph and architectural components contribute to demand and stress performance? | §8.3–8.4 (Exp03, 03A, 03B) |
| RQ3 | Does correlation-only adjacency outperform hybrid geographical graphs? | §8.4, §9.2 (Exp03, 03A, 03B) |
| RQ4 | Can multi-task learning deliver accurate stress forecasting without sacrificing demand accuracy vs single-task? | §8.3, §9.3 (Exp03 A4 vs A6) |
| RQ5 | Are S2 predictions interpretable via SHAP, attention, and OSI driver alignment? | §8.5 (Exp04) |

### 4.5 Contributions

List only — expand in §9 and §10 (see Part V).

1. Correlation-Aware Multi-Task Forecasting Framework (S2) for joint regional demand and OSI prediction  
2. Evidence-driven architecture freeze replacing hybrid graph with correlation-only adjacency  
3. W20 multi-task loss repair enabling simultaneous stress learning (Exp01B)  
4. Rigorous benchmark and ablation programme with Bonferroni-corrected Wilcoxon tests  
5. Integrated explainability analysis (SHAP, attention, case studies) on frozen S2  

### 4.6 Paper Organization

- One-sentence roadmap of §5–§10

**Assets:** None

**Experiments referenced:** Architecture freeze (motivation framing only)

---

## 5. Related Work

### 5.1 Load Forecasting

- Classical statistical and ML load forecasting
- Regional / national grid forecasting in developing economies

### 5.2 Graph Neural Networks for Power Systems

- GCN / T-GCN for spatio-temporal load
- Geographic vs data-driven graph construction

### 5.3 Transformer-Based Forecasting

- Temporal transformers for sequence forecasting
- Graph transformers with adjacency bias

### 5.4 Multi-Task Learning in Energy Systems

- Shared representations for related targets
- Task interference and loss balancing (link to Exp01A/01B)

### 5.5 Explainable AI for Forecasting

- SHAP / integrated gradients for time-series and graph models
- Operator-facing attribution requirements

### 5.6 Research Gap Summary

- Synthesize gaps; position S2 as correlation-aware multi-task framework with XAI validation

**Assets:** None

**Experiments referenced:** None (literature only)

---

## 6. Methodology

### 6.1 Problem Definition

- Notation: regions N=9, window T=7, horizon H=1
- Task 1: regional demand vector (MW); Task 2: scalar OSI ∈ [0,1]
- Leakage policy: OSI(t) excluded when predicting OSI(t+1)

### 6.2 Dataset

- Source: processed Bangladesh Smart Grid timeline
- Chronological splits; MD5-locked artefacts
- **→ Table 1**

### 6.3 Feature Engineering

- Node features (9 per region): lags, rolling, regional blocks
- Global features (17): calendar, grid aggregates, limitation stack, generation scalars
- Feature coalition groups G1–G11 (for Exp04 cross-reference)

### 6.4 Graph Construction

- Geographic adjacency (reference / S1)
- Correlation graph: τ = 0.65, 33 undirected edges (S2)
- Row-normalisation and attention bias derivation

### 6.5 PF-STGT Architecture (General)

- Parallel-fusion spatio-temporal graph transformer trunk
- Graph branch + temporal branch + gated fusion
- Dual heads: demand (9×MW), stress (OSI)
- **→ Figure 1**

### 6.6 Final S2 Architecture

- S2 = `PFSTGT` + `GraphVariant.CORR`
- Removed vs S1: geographical hybrid edges only
- Retained: full transformer trunk (Exp03B S4 justifies retention)
- Checkpoint and parameter count (749,058)
- **→ Figure 2**

### 6.7 Multi-Task Learning

- Combined loss: Huber(demand)/100 + λ₂·MSE(OSI)
- λ₂ = 20 (W20 protocol from Exp01B)
- Motivation: Exp01A OSI collapse → Exp01B repair

### 6.8 Training Strategy

- Optimiser, lr, weight decay, batch size, early stopping criterion
- Seed 42; validation-based model selection
- **→ Table 2**

**Assets in §6:**

| Asset | ID | Section |
| --- | --- | --- |
| `figures/figure_01_framework.png` | Figure 1 | §6.5 |
| `figures/figure_02_s2_architecture.png` | Figure 2 | §6.6 |
| Table 1 — Dataset Summary | Table 1 | §6.2 |
| Table 2 — Training Configuration | Table 2 | §6.8 |

**Experiment mapping:**

| Experiment | Role in §6 |
| --- | --- |
| **Foundation / Phase docs** | Dataset, features, splits (`src/constants.py`) |
| **Exp01** | Initial PF-STGT training validation; convergence context |
| **Exp01A** | Motivation for W20 loss repair (§6.7) |
| **Exp01B** | Frozen W20 training protocol (§6.7, §6.8) |
| **Architecture freeze** | S2 definition, I/O spec, rationale summary (§6.6) |

---

## 7. Experimental Setup

### 7.1 Hardware and Software

- Compute device policy (cuda / mps / cpu)
- Framework versions (PyTorch, etc.) — from project environment

### 7.2 Hyperparameters

- Reference Table 2; point to checkpoint configs
- Note: executed runs use Adam lr=5×10⁻⁴ per freeze record

### 7.3 Evaluation Metrics

- Task 1: macro MAE (primary), RMSE, MAPE, macro R²
- Task 2: stress MAE, RMSE, R²
- Primary ranking metric: test macro demand MAE

### 7.4 Baselines

- B01–B06 definitions; B07/S1 as historical PF-STGT reference
- S2 reported as proposed final model (not B07)

### 7.5 Statistical Testing

- Wilcoxon signed-rank on per-sample macro MAE
- Bonferroni correction (Exp02: α=0.0083; Exp03: α=0.01)
- Bootstrap 95% CIs — cite `statistical_summary.md`

### 7.6 Training Diagnostics

- **→ Figure 3** (historical W20 convergence reference)

**Assets in §7:**

| Asset | ID | Section |
| --- | --- | --- |
| Table 2 — Training Configuration | Table 2 | §7.2 (cross-ref) |
| `figures/figure_03_training_curves.png` | Figure 3 | §7.6 |

**Experiment mapping:**

| Experiment | Role in §7 |
| --- | --- |
| **Exp01** | Training curves (Figure 3) |
| **Exp01B** | Hyperparameter / loss-weight selection |
| **Exp02** | Baseline definitions, metric protocol |
| **Exp02A** | Metric aggregation note (macro vs per-region R²) — brief §7.3 footnote |

---

## 8. Results

### 8.1 Benchmark Comparison

- Report B01–B07 and **S2** on test set
- Highlight: S2 (88.65 MW) vs RF (97.03 MW) vs S1/B07 (93.31 MW)
- Stress metrics alongside demand
- **→ Table 3, Figure 4**

### 8.2 Statistical Significance of Benchmarks

- Wilcoxon B07 vs baselines (Table 4)
- Note S2 vs S1 tested in §8.4 (Exp03/03B), not Exp02
- **→ Table 4**

### 8.3 Ablation Studies

- A1–A6 results; A6 = S2
- A4 as demand-only upper bound (86.89 MW); multi-task trade-off
- A5 geographical-only degradation
- **→ Table 5, Figure 5**

### 8.4 Architecture Selection (S1–S4)

- Simplification study outcomes; S2 selected as final
- S4 failure when both graph simplification and transformer removal stacked
- Wilcoxon S1 vs S2 (p = 5.5×10⁻⁵)
- **→ Table 6**

### 8.5 Explainability Analysis

- Global SHAP: stress (G8, G6); demand Dhaka (G6, G4, G10)
- Node importance: Dhaka dominance; attention–adjacency ρ = 0.422
- Temporal: near-uniform α_t; peak t−6
- Stress attribution vs OSI components; 52.2% driver agreement
- Case studies: high-stress, peak demand, shedding strata
- **→ Table 7, Figures 6–9**

**Assets in §8:**

| Asset | ID | Section | File |
| --- | --- | --- | --- |
| Benchmark comparison | Table 3 | §8.1 | `publication_tables.md` §3 |
| Benchmark statistics | Table 4 | §8.2 | `publication_tables.md` §4 |
| Ablation results | Table 5 | §8.3 | `publication_tables.md` §5 |
| Architecture comparison | Table 6 | §8.4 | `publication_tables.md` §6 |
| Explainability summary | Table 7 | §8.5 | `publication_tables.md` §7 |
| Benchmark bar chart | Figure 4 | §8.1 | `figures/figure_04_benchmark_comparison.png` |
| Ablation bar chart | Figure 5 | §8.3 | `figures/figure_05_ablation_comparison.png` |
| SHAP stress | Figure 6a | §8.5 | `figures/figure_06_shap_summary_stress.png` |
| SHAP demand (Dhaka) | Figure 6b | §8.5 | `figures/figure_06_shap_summary_demand.png` |
| Node importance heatmap | Figure 7 | §8.5 | `figures/figure_07_node_importance.png` |
| Temporal attention | Figure 8 | §8.5 | `figures/figure_08_temporal_attribution.png` |
| Stress attribution | Figure 9 | §8.5 | `figures/figure_09_stress_attribution.png` |

**Experiment mapping (Results):**

| Experiment | Results subsection | Tables | Figures |
| --- | --- | --- | --- |
| **Exp02** | §8.1, §8.2 | 3, 4 | 4 |
| **Exp02A** | §8.1 (metric interpretation footnote) | — | Supp. optional |
| **Exp03** | §8.3 | 5 | 5 |
| **Exp03A** | §8.3 (interpretive bullets only; detailed discussion in §9) | — | — |
| **Exp03B** | §8.4 | 6 | — |
| **Exp04** | §8.5 | 7 | 6, 7, 8, 9 |
| **Architecture freeze** | §8.4 (S2 adoption statement) | 6 | — |

---

## 9. Discussion

Each subsection maps to one or more **contributions** (Part V). Draft prose later; outline topics only.

### 9.1 Why S2 Outperforms S1

- Correlation graph captures predictive inter-region coupling; hybrid geo edges add noise (Exp03A)
- Empirical ΔMAE −4.66 MW, p < 0.001 (Exp03B)
- **Contribution:** #2 (architecture freeze), #4 (statistical evidence)

### 9.2 Correlation Graph vs Geographical Prior

- A5 (geo-only) worst demand among ablations; A6 (corr-only) best multi-task demand
- Attention–adjacency alignment (ρ = 0.422) supports learned spatial structure (Exp04)
- **Contribution:** #1, #2

### 9.3 Multi-Task Trade-offs

- A4 single-task demand ceiling (86.89 MW) vs A6/S2 multi-task (88.65 MW) with stress R² 0.745
- Task interference from Exp01A; W20 repair from Exp01B
- When single-task is preferable vs operational dual forecasting
- **Contribution:** #3, #1

### 9.4 Temporal Transformer Role

- A3 ≈ A1 on hybrid graph; uniform attention (Exp03A)
- S4 shows correlation graph **requires** temporal branch (−21 MW when removed)
- **Contribution:** #2 (selective simplification, not blanket removal)

### 9.5 Explainability and Operator Trust

- Limitation stack (G8) and calendar trend (G6) as stress drivers
- 52.2% OSI driver agreement — partial dual-path consistency
- SHAP vs permutation disagreement on demand (−0.564 Spearman)
- **Contribution:** #5

### 9.6 Comparison with Classical ML

- RF strong per-region R² but higher macro MAE; Exp02A aggregation audit
- Deep model advantage vs T-GCN / RNN baselines
- **Contribution:** #4

### 9.7 Practical Implications

- Deployability: frozen checkpoint, reproducible MD5 data pipeline
- Use cases: day-ahead regional demand + stress visibility for dispatch planning

### 9.8 Limitations

- Single country / single grid dataset
- Chronological split only; no cross-year external validation
- OSI driver agreement incomplete (47.8% disagreement cases)
- A4 demand-only bound not reached by multi-task S2
- Historical S1 (B07) in Exp02 vs S2 in Exp03 — clarify lineage in text

**Assets:** None (interpret Tables 3–7, Figures 4–9)

**Experiment mapping (Discussion):**

| Experiment | Discussion subsection |
| --- | --- |
| **Exp01A** | §9.3 (OSI collapse, task interference) |
| **Exp01B** | §9.3 (W20 rationale) |
| **Exp02A** | §9.6 (R² vs MAE ranking) |
| **Exp03A** | §9.1, §9.2, §9.4 (root causes of ablation surprises) |
| **Exp03B** | §9.1, §9.4 (S2 selection, S4 failure) |
| **Exp04** | §9.5 (interpretability claims and limits) |
| **Architecture freeze** | §9.1 (decision summary) |

---

## 10. Conclusion

### 10.1 Summary

- Restate problem, method (S2), and headline results (88.65 MW, stress R² 0.745)

### 10.2 Contributions

- Repeat numbered contributions from §4.5 with one-line evidence each

### 10.3 Future Work

- External validation; probabilistic forecasting; improved OSI driver alignment
- Explore demand–stress Pareto frontier (A4 vs A6 trade-off)
- Real-time deployment and operator-in-the-loop XAI

**Assets:** None

---

## 11. Appendix A — Supplementary Materials

- Manuscript file: `paper/sections/11_Appendix_A_Supplementary_Materials.md`
- Supporting tables, statistics, hyperparameters, features, graph specs, XAI paths, reproducibility checklist

| ID | Content | Source |
| --- | --- | --- |
| Table S1 | Classical benchmark metric verification | Exp02A |
| Table S2 | Full grouped SHAP values | Exp04 |
| Table S3 | Permutation feature importance | Exp04 |
| Table S4 | Case-study attribution detail | Exp04 `case_studies.md` |
| Figure S1 | Signed stress SHAP bar | Exp04 |
| Figure S2 | Actual vs predicted — Dhaka | Exp02A |
| Figure S3 | Residual distribution — S1 | Exp02A |
| Figure S4 | Permutation ΔMAE ranking | Exp04 |
| Figure S5 | Regional SHAP contribution | Exp04 |

---

## 12. References

- Official bibliography: `paper/sections/12_References.bib` (BibTeX; maintained exclusively here)
- Include: GNN forecasting, transformers, multi-task learning, SHAP, Bangladesh energy context
- Do not create a Markdown references chapter (`11_References.md`, `12_References.md`, or similar)

---

# Part II — Figure Placement

Complete figure catalogue with manuscript location. Do not regenerate; use frozen assets.

| Figure | Title | Section | First mention | Asset path |
| --- | --- | --- | --- | --- |
| **1** | Overall Framework | §6.5 | End of architecture overview | `paper/final_results_package/figures/figure_01_framework.png` |
| **2** | Final S2 Architecture | §6.6 | S2 definition / S1→S2 transition | `paper/final_results_package/figures/figure_02_s2_architecture.png` |
| **3** | Training Curves | §7.6 | Training diagnostics | `paper/final_results_package/figures/figure_03_training_curves.png` |
| **4** | Benchmark Comparison | §8.1 | After Table 3 intro | `paper/final_results_package/figures/figure_04_benchmark_comparison.png` |
| **5** | Ablation Comparison | §8.3 | After Table 5 intro | `paper/final_results_package/figures/figure_05_ablation_comparison.png` |
| **6a** | SHAP Summary — Stress | §8.5 | Global feature importance | `paper/final_results_package/figures/figure_06_shap_summary_stress.png` |
| **6b** | SHAP Summary — Demand (Dhaka) | §8.5 | Adjacent to 6a (panel or subfigure) | `paper/final_results_package/figures/figure_06_shap_summary_demand.png` |
| **7** | Node Importance | §8.5 | Spatial attribution | `paper/final_results_package/figures/figure_07_node_importance.png` |
| **8** | Temporal Attribution | §8.5 | Temporal α_t analysis | `paper/final_results_package/figures/figure_08_temporal_attribution.png` |
| **9** | Stress Attribution | §8.5 | OSI driver comparison | `paper/final_results_package/figures/figure_09_stress_attribution.png` |

**Figure density guideline:**

| Section | Count | Figures |
| --- | ---: | --- |
| Methodology | 2 | 1, 2 |
| Experimental Setup | 1 | 3 |
| Results | 6 (+1 subfigure) | 4, 5, 6a, 6b, 7, 8, 9 |
| **Total main text** | **9 (+1 subfigure)** | |

**Caption sources:** `paper/final_results_package/publication_figures.md`

---

# Part III — Table Placement

| Table | Title | Section | When to introduce | Source |
| --- | --- | --- | --- | --- |
| **1** | Dataset Summary | §6.2 | After dataset description | `publication_tables.md` §1 |
| **2** | Training Configuration | §6.8 | After training strategy | `publication_tables.md` §2 |
| **3** | Benchmark Comparison | §8.1 | Opening of Results | `publication_tables.md` §3 |
| **4** | Benchmark Statistical Significance | §8.2 | After Table 3 discussion | `publication_tables.md` §4 |
| **5** | Ablation Study Results | §8.3 | Before Figure 5 | `publication_tables.md` §5 |
| **6** | Architecture Comparison (S1–S4) | §8.4 | Architecture selection subsection | `publication_tables.md` §6 |
| **7** | Explainability Summary | §8.5 | Opening of explainability subsection | `publication_tables.md` §7 |

**Table density guideline:**

| Section | Count | Tables |
| --- | ---: | --- |
| Methodology | 2 | 1, 2 |
| Results | 5 | 3, 4, 5, 6, 7 |
| **Total main text** | **7** | |

**LaTeX export targets:** `manuscript/overleaf/tables/table_01_dataset.tex` … `table_07_explainability.tex`

---

# Part IV — Experiment-to-Section Mapping

Master traceability matrix for all completed experiments.

| Experiment | Objective (short) | Methodology | Exp. Setup | Results | Discussion | Tables | Figures |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Exp01** — PF-STGT Training | Validate training stability | §6.5 | §7.6 | — | — | — | 3 |
| **Exp01A** — OSI Failure Investigation | Diagnose OSI collapse | §6.7 (motivation) | — | — | §9.3 | — | — |
| **Exp01B** — Multi-Task Repair | W20 loss protocol | §6.7, §6.8 | §7.2 | — | §9.3 | 2 | 3 |
| **Exp02** — Benchmark Models | Compare B01–B07 vs PF-STGT | §7.4 | §7.3, §7.5 | §8.1, §8.2 | §9.6 | 3, 4 | 4 |
| **Exp02A** — Benchmark Verification | MAE vs R² audit | §7.3 (note) | — | §8.1 (note) | §9.6 | S1 (opt.) | S2–S3 (opt.) |
| **Exp03** — Ablation Studies | A1–A6 component effects | §6.6 (context) | §7.5 | §8.3 | §9.1–9.3 | 5 | 5 |
| **Exp03A** — Ablation Investigation | Explain ablation surprises | — | — | §8.3 (bullets) | §9.1, §9.2, §9.4 | — | — |
| **Exp03B** — Architecture Simplification | S1–S4; select S2 | §6.6 | §7.5 | §8.4 | §9.1, §9.4 | 6 | — |
| **Exp04** — Explainability | XAI on frozen S2 | §6.3 (coalitions) | — | §8.5 | §9.5 | 7 | 6–9 |
| **Architecture Freeze** | Approve S2 as final | §6.6 | — | §8.4 | §9.1 | 2, 6 | 1, 2 |
| **Publication Freeze** | Asset lock | — | — | All §8 | — | All | All |
| **Foundation / Phases** | Data, features, splits | §6.2, §6.3, §6.4 | — | — | — | 1 | — |

### Narrative flow across experiments (for Results drafting order)

```
Exp01/01B → training protocol established
     ↓
Exp02 (+02A) → S1 competitive vs ML; metric caveats
     ↓
Exp03 (+03A) → components diagnosed; corr graph wins
     ↓
Exp03B → S2 selected as final
     ↓
Exp04 → S2 interpretability validated
```

---

# Part V — Contribution Mapping

| # | Contribution | Introduction | Results evidence | Discussion | Conclusion |
| --- | --- | --- | --- | --- | --- |
| **C1** | **Correlation-Aware Multi-Task Forecasting Framework (S2)** for joint regional demand + OSI prediction | §4.5 | §8.1 (Table 3), §8.4 (Table 6), §8.5 (Table 7) | §9.1, §9.7 | §10.2 |
| **C2** | **Evidence-driven architecture simplification**: correlation-only graph replaces hybrid (S1→S2) | §4.3–4.5 | §8.3 (A5 vs A6), §8.4 (S1–S4) | §9.1, §9.2, §9.4 | §10.2 |
| **C3** | **W20 multi-task loss repair** enabling stress R² 0.745 alongside demand accuracy | §4.5 | §8.3 (A4 vs A6 stress), Table 2 | §9.3 | §10.2 |
| **C4** | **Rigorous empirical evaluation**: benchmarks, ablations, Bonferroni Wilcoxon tests | §4.4 RQ1–RQ4 | §8.1–8.4 (Tables 3–6, Figs 4–5) | §9.6 | §10.2 |
| **C5** | **Integrated explainability** on frozen S2: SHAP, attention, OSI driver case studies | §4.4 RQ5 | §8.5 (Table 7, Figs 6–9) | §9.5, §9.8 | §10.2, §10.3 |

### Contribution-to-asset anchor table

| Contribution | Key frozen numbers | Primary experiment |
| --- | --- | --- |
| C1 | Demand MAE 88.65 MW; stress R² 0.745 | Exp03B / Exp04 |
| C2 | ΔMAE −4.66 MW vs S1; p = 5.5×10⁻⁵ | Exp03, 03A, 03B |
| C3 | λ₂=20; stress R² 0.585→0.745 (S1→S2) | Exp01A, 01B, 03 |
| C4 | B07 vs B02 p=0.001; 6 Bonferroni tests | Exp02, 02A |
| C5 | G8/G6 top SHAP; ρ=0.422; 52.2% agreement | Exp04 |

---

# Part VI — Section Order Summary

| Order | Section | Est. tables | Est. figures |
| ---: | --- | ---: | ---: |
| 1 | Title | 0 | 0 |
| 2 | Abstract | 0 | 0 |
| 3 | Keywords | 0 | 0 |
| 4 | Introduction | 0 | 0 |
| 5 | Related Work | 0 | 0 |
| 6 | Methodology | 2 | 2 |
| 7 | Experimental Setup | 0 | 1 |
| 8 | Results | 5 | 7 (+1 subfigure) |
| 9 | Discussion | 0 | 0 |
| 10 | Conclusion | 0 | 0 |
| 11 | Appendix A | — | — | `11_Appendix_A_Supplementary_Materials.md` |
| 12 | References | 0 | 0 | `12_References.bib` |

---

# Part VII — Drafting Checklist

Use when writing full manuscript (Stage 06+):

- [ ] Cross-check all numbers against `paper/final_results_package/statistical_summary.md`
- [ ] Use S2 (not B07 alone) as proposed model in Abstract and Conclusion
- [ ] Cite B07/S1 as historical reference where Exp02 benchmarks are discussed
- [ ] Include Bonferroni α values when reporting p-values
- [ ] Note A4 as demand-only upper bound; do not claim S2 beats A4 on demand
- [ ] Figure 6: use subfigures (6a stress, 6b demand) or side-by-side panel
- [ ] Do not modify frozen CSV/JSON/checkpoints/figures under `experiments/`
- [ ] Export tables to `manuscript/overleaf/tables/`
- [ ] Copy figures from `paper/final_results_package/figures/`

---

## Definition of Done — Stage 05C

✔ Complete manuscript hierarchy finalized  
✔ Figure placement finalized (Figures 1–9)  
✔ Table placement finalized (Tables 1–7)  
✔ Experiment-to-section mapping completed (Exp01–04 + sub-studies)  
✔ Contribution mapping to Discussion completed  
✔ Section order finalized  

**Ready for manuscript writing (Stage 06).**

---

## Asset References

| Document | Path |
| --- | --- |
| Publication freeze | `paper/publication_freeze/Publication_Asset_Freeze.md` |
| Final results package | `paper/final_results_package/Final_Results_Package.md` |
| Publication tables | `paper/final_results_package/publication_tables.md` |
| Publication figures | `paper/final_results_package/publication_figures.md` |
| Statistical summary | `paper/final_results_package/statistical_summary.md` |
| Asset inventory | `paper/final_results_package/manuscript_assets_inventory.md` |
| Architecture decision | `experiments/architecture_freeze_revision/Final_Architecture_Decision.md` |
