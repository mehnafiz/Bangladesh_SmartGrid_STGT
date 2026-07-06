# Explainability Publication Mapping Report — Phase 18

**Date:** 6 July 2026  
**Authority:** `paper/prompts/18_Explainability_Publication_Mapping.md`  
**Inputs:** `Explainability_Audit_Report.md`, frozen Exp04 artefacts, journal (`paper/latex/`), conference (`paper/conference/`), publication freeze  
**Constraint:** Publication planning only — no experiments, figures, code, or manuscript modifications

---

## 1. Executive Summary

Experiment 04 produced **eight explainability figures**, **four table families**, **24 case-study folders**, and **eight markdown reports** on the frozen S2 checkpoint. The explainability programme is scientifically complete and already mapped into both manuscripts at a level appropriate to each venue.

**Journal strategy (recommended):** Retain the current **five-figure + one-table** explainability block (Figs. 6a, 6b, 7, 8, 9; Table 7) within Results §5.6, with three outputs moved to **supplementary material** (permutation ranking figure, regional contribution panel, signed SHAP bar). This preserves multi-method rigour without overcrowding the main narrative.

**Conference strategy (recommended):** Retain the **current distillation** — one figure (node heatmap) plus dense prose metrics. No additional explainability figures are justified within a 6-page budget.

**Manuscript updates:** **None required** for scientific completeness. Optional clarifications only (Captum vs custom IG wording; validation-sample scope).

**Figure 1 (framework diagram):** Scientific content is correct; visual redesign is deferred to a future graphics phase. Section 9 provides IEEE-quality redesign specifications preserving identical semantics.

**Final verdict:** The existing publication mapping is **near-optimal**. Future revisions should prioritise **visual quality** (Fig. 1 vector rebuild, Fig. 7 PDF vectorisation) over new explainability experiments.

---

## 2. Explainability Inventory

### 2.1 Figures (Experiment 04)

| ID | File | Method | Status |
|---|---|---|---|
| E04-F1 | `figure_shap_summary_stress.png` | Grouped GradientSHAP (global stress) | Real, frozen |
| E04-F2 | `figure_shap_summary_demand.png` | Grouped GradientSHAP (Dhaka demand) | Real, frozen |
| E04-F3 | `figure_shap_bar_stress.png` | Signed stress φ bar chart | Real, frozen |
| E04-F4 | `figure_feature_importance_ranking.png` | Permutation ΔMAE ranking | Real, frozen |
| E04-F5 | `figure_node_importance_heatmap.png` | Node mass + spatial attention | Real, frozen |
| E04-F6 | `figure_temporal_importance.png` | Mean temporal α_t (T=7) | Real, frozen |
| E04-F7 | `figure_stress_attribution.png` | Dual-path SHAP vs OSI components | Real, frozen |
| E04-F8 | `figure_regional_contribution.png` | Regional SHAP contribution panel | Real, frozen |

**Paths:** `experiments/experiment_04_explainability_analysis/figures/` (authoritative); copies in `manuscript/overleaf/figures/`, `paper/latex/figures/`, `paper/final_results_package/figures/`.

### 2.2 Tables

| ID | Content | Primary source |
|---|---|---|
| T7 | Explainability headline summary | `paper/latex/tables/table_07_explainability.tex` |
| TS2 | Global grouped SHAP (stress + Dhaka demand) | `results/explainability/shap/global_*.csv` |
| TS3 | Permutation importance (demand + stress) | `results/explainability/permutation/*.csv` |
| TS4 | Case-study records (24 dates) | `results/explainability/case_studies/<date>/` |

### 2.3 Machine-readable artefacts

| Artefact | Path | Role |
|---|---|---|
| `xai_metrics.json` | `experiments/experiment_04_explainability_analysis/` | Headline metrics, case metadata |
| Case-study CSVs (×4 per date) | `results/explainability/case_studies/` | `stress_shap`, `node_importance`, `temporal_alpha`, `osi_components` |
| Global SHAP CSVs | `results/explainability/shap/` | Coalition φ values |
| Permutation CSVs | `results/explainability/permutation/` | ΔMAE by coalition |

### 2.4 Reports

| Report | Path |
|---|---|
| `xai_summary.md` | Experiment 04 root |
| `shap_summary.md` | Coalition rankings |
| `feature_importance.md` | Permutation + Spearman ρ |
| `node_attribution.md` | Spatial mass + attention ρ |
| `temporal_attribution.md` | α_t weights |
| `stress_attribution.md` | Dual-path agreement |
| `case_studies.md` | 24 stratified records |
| `regional_analysis.md` | Per-region φ averages |

### 2.5 Attention analysis (no standalone figure)

Attention is exported via `return_attention=True` and aggregated in `attention_extractor.py`. Metrics appear in node heatmap and `xai_metrics.json` (ρ = 0.422). No dedicated attention-only figure exists.

---

## 3. Per-Output Assessment (Task 2)

| Output | Scientific objective | Novelty | Reviewer value | Journal | Conference | Decision |
|---|---|---|---|---|---|---|
| **SHAP summary (stress)** | Identify stress-driving coalitions | Medium — G8/G6 dominance validates OSI design | High — links limitation inputs to stress head | **Main** Fig. 6a | Exclude | **Retain (journal main)** |
| **SHAP summary (demand)** | Identify Dhaka demand drivers | Medium — calendar/lag vs supply discordance | High — explains MAE geography | **Main** Fig. 6b | Exclude | **Retain (journal main)** |
| **SHAP bar (stress)** | Signed φ direction for stress | Low — redundant with summary | Medium — supplementary detail | **Supp.** Fig. S1 | Exclude | **Supplementary** |
| **Permutation ranking** | Model-agnostic feature ablation | Medium — exposes ρ = −0.564 demand discordance | High — reviewer credibility | **Supp.** Fig. S4 | Exclude (prose only) | **Supplementary** |
| **Node heatmap** | Spatial attribution on correlation graph | **High** — unique graph-temporal XAI | **Highest** — Dhaka mass + graph structure | **Main** Fig. 7 | **Main** Fig. 5 | **Retain both venues** |
| **Regional contribution** | Per-division SHAP panel | Medium — extends Fig. 7 spatially | Medium — overlaps node heatmap | **Supp.** Fig. S5 | Exclude | **Supplementary** |
| **Temporal α_t** | Lag importance within T=7 | Low — near-uniform weights | Low–medium — honest null result | **Main** Fig. 8 | Exclude | **Retain (journal main)** with tempered claims |
| **Stress dual-path** | Validate SHAP against OSI physics | **High** — engineered-index audit | High — 52.2% agreement is scientifically honest | **Main** Fig. 9 | Exclude (prose) | **Retain (journal main)** |
| **Attention ρ metric** | Graph-learning interpretability | Medium | Medium | Table 7 + Fig. 7 caption | Prose | **Retain as metric** |
| **Case studies (24)** | Stratified operational scenarios | Medium | High for rebuttal | **Supp.** Table S4 | Prose (52.2%) | **Supplementary** |
| **Table 7** | Cross-method headline consolidation | Medium | High — single reference point | **Main** | Exclude (inline prose) | **Retain (journal main)** |
| **CSV / JSON** | Reproducibility | N/A | Low in PDF | Appendix URLs | N/A | **Appendix only** |
| **Markdown reports** | Internal audit trail | N/A | N/A | Appendix refs | N/A | **Repository only** |

### Justification for exclusions

- **Conference SHAP figures:** Coalition rankings are fully expressible in three sentences; page cost exceeds marginal information gain.
- **Conference temporal figure:** Near-uniform α_t does not justify a quarter-column; one sentence suffices.
- **Conference dual-path figure:** 52.2% agreement is more credible in prose than as a small multi-panel chart at conference scale.
- **Journal permutation figure:** Table 7 + §5.6 paragraph convey discordance; separate bar chart duplicates Table TS3 without new science.

---

## 4. Journal Publication Plan (Task 3)

### 4.1 Section architecture

| Location | Content |
|---|---|
| **§3 Methodology** | G1–G11 coalition registry (already present); no XAI method equations required |
| **§4 Experimental Setup** | Post-hoc attribution scope: S2 checkpoint, validation n=20 global, 24 case studies, no retraining |
| **§5.5 Error Analysis** | Figs. 6a/6b — coalition association with forecast deviations (bridge to explainability) |
| **§5.6 Explainability Analysis** | Figs. 7–9, Table 7, cross-method paragraph |
| **§6 Discussion** | Five explainability subsubsections (already present) |
| **§8 Appendix** | Table S2–S4, Figure S1, artefact URLs, Captum disclosure |

### 4.2 Figure mapping (recommended — matches current manuscript)

#### Figure 6a — Grouped SHAP attributions for stress (global)

| Field | Specification |
|---|---|
| **Source** | `figure_06_shap_summary_stress.png` |
| **Title** | Grouped SHAP attributions for stress (global) |
| **Caption objective** | Show coalition-level \|φ\| spread for OSI task; G8 limitation stack and G6 calendar dominate |
| **Section** | §5.5 Error Analysis (first); cross-ref in §5.6 |
| **Placement** | After error-analysis introduction; paired with Fig. 6b |
| **First citation** | §5.5 opening paragraph on coalition-level error association |
| **Discussion** | §6 — Explainability contribution; §6 — Operator support (limitation/calendar monitoring) |
| **Interpretation** | Model stress sensitivity aligns with limitation-stack supervision design; validates multi-task feature geometry |

#### Figure 6b — Grouped SHAP attributions for Dhaka demand

| Field | Specification |
|---|---|
| **Source** | `figure_06_shap_summary_demand.png` |
| **Title** | Grouped SHAP attributions for Dhaka demand |
| **Caption objective** | Contrast demand coalition spread (G6, G4, G10) with stress figure |
| **Section** | §5.5 Error Analysis |
| **Placement** | Immediately after or below Fig. 6a |
| **First citation** | Same §5.5 paragraph as Fig. 6a |
| **Discussion** | §6 — Multi-task learning (different coalition families per head) |
| **Interpretation** | Demand head prioritises calendar and lag channels over limitation stack — supports task-specialisation claim |

#### Figure 7 — Node-level attribution heatmap

| Field | Specification |
|---|---|
| **Source** | `figure_07_node_importance.png` |
| **Title** | Node-level attribution heatmap |
| **Caption objective** | Spatial concentration of GradientSHAP mass; Dhaka dominance; attention–adjacency ρ = 0.422 |
| **Section** | §5.6 Explainability Analysis — Spatial node attribution |
| **Placement** | After coalition paragraphs; before temporal subsection |
| **First citation** | §5.6 `\subsubsection{Spatial node attribution}` opening sentence |
| **Discussion** | §6 — Bangladesh implications (Dhaka planning); §6 — Explainability limits (macro vs spatial) |
| **Interpretation** | Learned spatial explanations mirror load geography and correlation-graph structure — core graph-XAI result |

#### Figure 8 — Temporal attention weights

| Field | Specification |
|---|---|
| **Source** | `figure_08_temporal_attribution.png` |
| **Title** | Temporal attention weights across the lookback window |
| **Caption objective** | Report near-uniform α_t with slight t−6 emphasis; avoid overclaiming lag selectivity |
| **Section** | §5.6 — Temporal attribution |
| **Placement** | After Fig. 7; before dual-path stress |
| **First citation** | §5.6 `\subsubsection{Temporal attribution}` |
| **Discussion** | §6 — Explainability limits (uniform weights limit sharp lag claims) |
| **Interpretation** | Seven-day window is used coherently but without strong single-lag dominance — honest reporting strengthens credibility |

#### Figure 9 — Dual-path stress attribution

| Field | Specification |
|---|---|
| **Source** | `figure_09_stress_attribution.png` |
| **Title** | Dual-path stress attribution vs. OSI component drivers |
| **Caption objective** | Compare gradient coalition rankings with c₂/c₃ OSI decomposition across 24 cases |
| **Section** | §5.6 — OSI dual-path stress attribution |
| **Placement** | After temporal figure; before cross-method paragraph |
| **First citation** | §5.6 `\subsubsection{OSI dual-path stress attribution}` |
| **Discussion** | §6 — Explainability limits (52.2% agreement); §6 — Future work (operator validation) |
| **Interpretation** | Partial alignment validates stress head somewhat; disagreement mandates cautious operator use |

### 4.3 Table placement

| Table | Location | Role |
|---|---|---|
| **Table 7** | End of §5.6 (after Figs. 7–9 cited) | Headline cross-method metrics |
| **Table S2** | Appendix | Full coalition φ CSV export |
| **Table S3** | Appendix | Permutation ΔMAE CSV export |
| **Table S4** | Appendix | Case-study index |

### 4.4 Cross-references (recommended)

- §5.5 → Figs. 6a, 6b (error–coalition bridge)
- §5.6 scope → Table 7
- §5.6 spatial → Fig. 7
- §5.6 temporal → Fig. 8
- §5.6 dual-path → Fig. 9
- §5.6 cross-method → Table 7 (ρ values)
- §6 discussion → Table 7, Figs. 7–9
- Appendix → all CSV paths, Figure S1

### 4.5 Supplementary material (journal)

| Item | Rationale |
|---|---|
| Figure S1 — SHAP bar stress | Signed detail; not essential to main narrative |
| Figure S4 — Permutation ranking | Supports ρ = −0.564; redundant with Table 7 prose |
| Figure S5 — Regional contribution | Extends Fig. 7 without new headline finding |
| Tables S2–S4 | Full reproducibility for reviewers |
| 24 case-study CSV folders | Rebuttal-grade stratified evidence |

---

## 5. Conference Publication Plan (Task 4)

### 5.1 Selected output

#### Figure 5 (conference numbering) — Node-level attribution heatmap

| Field | Specification |
|---|---|
| **Source** | `figure_07_node_importance.png` |
| **Why included** | **Highest information density per square centimetre** among all XAI outputs; uniquely demonstrates graph-spatial explainability on Bangladesh divisions; visually communicates Dhaka dominance matching regional MAE discussion |
| **Why stronger than alternatives** | SHAP summaries are coalition tables in disguise; temporal plot is flat; dual-path is numerically summarized as 52.2%; permutation discordance is one ρ value |
| **Placement** | Results §IV-D Explainability; float after attribution paragraph |
| **Discussion paragraph** | §V-B Multi-task learning (G8/G6 coalitions); §V-D Deployment (monitor limitation/calendar); Limitations (ρ = −0.564, no causation) |

### 5.2 Prose-retained metrics (no figures)

| Metric | Why prose suffices |
|---|---|
| G8/G6 stress \|φ\| | Two numbers; reviewer learns coalition story without chart |
| G6/G4/G10 demand \|φ\| | Three numbers; supports multi-task narrative |
| ρ = 0.422 attention–adjacency | Single correlation; cited with Fig. 5 |
| ρ = −0.564 demand discordance | **Critical honesty signal** — stronger in text than hidden in supp. figure |
| 52.2% dual-path agreement | Percentage headline; figure would consume half a column for modest gain |

### 5.3 Excluded figures — justification

| Excluded | Reason reviewer understanding preserved |
|---|---|
| SHAP summaries (6a/6b) | Coalition rankings fully stated in prose with exact \|φ\| values |
| Permutation ranking | ρ = −0.564 and G2 vs G6 ranking described in one sentence |
| Temporal α_t | Near-uniform weights explicitly noted; no operational actionability |
| Dual-path stress | 13/24 agreement stated; limitation paragraph warns against over-interpretation |
| Regional contribution | Node heatmap already shows spatial mass concentration |
| SHAP bar | Signed direction not needed for conference claims |

**Conference page budget:** One XAI figure is optimal. Adding a second would displace benchmark or ablation evidence — higher rejection risk than explainability omission.

---

## 6. Figure Priority Ranking (Task 6)

Highest → lowest publication value:

| Rank | Output | Score rationale |
|---|---|---|
| 1 | **Node attribution heatmap** (E04-F5) | Unique graph-spatial XAI; Dhaka story; both venues |
| 2 | **Dual-path stress attribution** (E04-F7) | Novel OSI validation; journal essential |
| 3 | **SHAP summary stress** (E04-F1) | Core coalition evidence for stress task |
| 4 | **SHAP summary demand** (E04-F2) | Task contrast; Dhaka demand drivers |
| 5 | **Table 7 / headline metrics** | Cross-method consolidation |
| 6 | **Case studies (24)** | Rebuttal strength; supplementary |
| 7 | **Permutation CSV + prose** | Discordance reporting |
| 8 | **Permutation ranking figure** (E04-F4) | Visual duplicate of rank 7 |
| 9 | **Regional contribution** (E04-F8) | Extends rank 1 spatially |
| 10 | **SHAP bar stress** (E04-F3) | Supplementary signed view |
| 11 | **Temporal α_t** (E04-F6) | Low insight density (near-uniform) |
| 12 | **Attention ρ alone** | Subsumed by node heatmap |
| 13 | **JSON/CSV raw exports** | Reproducibility only |
| 14 | **Internal markdown reports** | Pipeline documentation |

---

## 7. Recommended Figure Order

### 7.1 Journal (full paper — explainability figures only)

1. Fig. 6a — SHAP stress summary  
2. Fig. 6b — SHAP demand summary  
3. Fig. 7 — Node heatmap  
4. Fig. 8 — Temporal α_t  
5. Fig. 9 — Dual-path stress  

*Supplementary:* S1 (SHAP bar), S4 (permutation), S5 (regional)

### 7.2 Conference

1. Fig. 5 — Node heatmap (only explainability figure)

### 7.3 Narrative flow rationale

Coalition overviews (6a/6b) → spatial structure (7) → temporal behaviour (8) → physical validation (9). This progression moves from **what inputs matter** → **where** → **when** → **whether explanations align with OSI physics**.

---

## 8. Recommended Table Order

| Order | Table | Venue | Placement |
|---|---|---|---|
| 1 | Table 7 — Explainability summary | Journal main | End of §5.6 |
| 2 | Table S2 — Global SHAP CSV | Journal appendix | Artefact index |
| 3 | Table S3 — Permutation CSV | Journal appendix | After S2 |
| 4 | Table S4 — Case studies | Journal appendix | After S3 |
| — | Inline metrics in conference prose | Conference | §IV-D Explainability |

---

## 9. Required Manuscript Updates (Task 5)

### 9.1 Verdict: **No mandatory changes**

Current manuscripts already implement the optimal mapping identified in this report. Scientific claims, figure selection, and cross-method discordance reporting are aligned with frozen Exp04 outputs.

### 9.2 Section-by-section assessment

| Section | Update required? | Rationale |
|---|---|---|
| **Abstract** | No | Quantitative headline metrics absent by design; scope statement present |
| **Contributions** | No | Fifth contribution (multi-method attribution) accurately stated |
| **Methodology** | No | G1–G11 coalitions defined; OSI leakage guard documented |
| **Experimental Setup** | Optional | Could add one sentence: global SHAP on n=20 validation windows |
| **Results** | No | §5.5–5.6 complete with correct figure/table set |
| **Discussion** | No | Five explainability subsubsections cover limits, operator use, future work |
| **Conclusion** | No | Fifth outcome references attribution with discordance |
| **Appendix** | No | Artefact URLs, Captum disclosure, Table S2–S4 present |

### 9.3 Optional future clarifications (non-blocking)

1. **Environment wording:** State explicitly that attribution uses a custom integrated-gradients implementation, not the `shap` or `captum` Python APIs (journal appendix partially covers this).
2. **Sample scope:** Footnote that global SHAP aggregates validation windows, not full test split.
3. **Fig. 6a/6b placement:** Consider moving from Error Analysis to Explainability §5.6 if reviewers confuse error association with attribution — cosmetic only.

---

## 10. Figure 1 Redesign Recommendations (Task 7)

**Scope:** Framework diagram (PF-STGT pipeline) — **not** an explainability figure. Supervisor feedback: *scientific content correct; not visually publication-quality.*

**Current state:**
- Journal: raster PNG (`figure_01_framework.png`, matplotlib-generated)
- Conference: TikZ vector (`figure_01_tikz.tex`) — improved but still below IEEE Transactions illustration standard

### 10.1 Current weaknesses

| Dimension | Issue | Reviewer perception |
|---|---|---|
| **Visual hierarchy** | All boxes similar weight; inputs, encoders, heads compete equally | Reads as block diagram, not engineered system |
| **Typography** | Mixed font sizes (6 pt tensor labels vs body text); conference TikZ uses `\scriptsize` | Appears auto-generated |
| **Spacing** | Dense horizontal layout; footer note cramped | Cluttered at column width |
| **Arrows** | Uniform thin arrows; parallel paths hard to trace | Fusion logic unclear |
| **Colour** | Pale fills (#ebf8ff) low contrast in print | Washed out in grayscale |
| **Icons** | No semantic icons (grid, clock, graph) | Generic ML diagram |
| **Consistency** | Journal PNG ≠ conference TikZ styling | Venue inconsistency |
| **Node sizing** | Demand head (9 MW) vs stress head (OSI) unequal visual weight | Accidental asymmetry |
| **Parallel fusion** | Gated fusion box same size as encoders | Understates architectural contribution |

### 10.2 Redesign specifications (next phase — identical science)

| Requirement | Specification |
|---|---|
| **Format** | Single SVG/PDF vector; IEEE Times-compatible labels |
| **Layout** | Three-band hierarchy: **Inputs** (left) → **Encoders** (centre) → **Outputs** (right) |
| **Inputs** | Stack three input blocks vertically with equal width; tensor shapes as subscript lines |
| **Encoders** | Graph and temporal transformers on parallel rows; fusion box centred below with **wider** emphasis |
| **Outputs** | Demand head (9 regional outputs) and stress head (scalar OSI) with distinct but balanced boxes |
| **Arrows** | 0.6 pt primary paths; 0.4 pt secondary; colour `#2c5282`; fusion paths in `#276749` |
| **Colour palette** | Match `ieee_fig_colors.tex`; ensure ≥4.5:1 contrast for grayscale |
| **Typography** | 8 pt labels, 7 pt tensor annotations; no font below 6 pt |
| **Footer** | Single line: *S2: correlation graph (τ=0.65)* — remove redundant hybrid note from figure (keep in caption) |
| **Icons** | Optional minimal line icons: grid nodes, calendar strip, adjacency matrix — only if consistent stroke weight |
| **Caption** | Carry scientific detail (T=7, N=9, F dimensions); figure itself should be self-explanatory at glance |

### 10.3 Recommended workflow (future phase)

1. Rebuild in **draw.io**, **Figma**, or **Illustrator** using frozen palette  
2. Export PDF at vector paths (no raster text)  
3. Unify journal and conference to **one source file**  
4. Verify at **3.5 in column width** and **full page width**  
5. Side-by-side compare with `paper/template/IEEE-conference-template-062824` figure aesthetics  

**Constraint:** Zero change to node labels, tensor dimensions, module names, or data-flow topology.

---

## 11. Optional Supplementary Material

| Asset | Audience | Priority |
|---|---|---|
| Figure S1 — SHAP bar stress | Reviewers wanting signed φ | Medium |
| Figure S4 — Permutation ranking | Methods reviewers | Medium |
| Figure S5 — Regional contribution | Spatial detail seekers | Low |
| Tables S2–S4 | Reproducibility auditors | High |
| `xai_metrics.json` | Open-science replication | High |
| 24 case-study folders | Rebuttal / operator scenarios | High |
| `explainability_protocol.md` | Methods appendix extension | Low |

---

## 12. Final Publication Strategy

### 12.1 Journal (IEEE Transactions target)

**Retain:** Figs. 6a, 6b, 7, 8, 9 + Table 7 in main text.  
**Move:** Permutation figure, regional panel, SHAP bar → supplementary.  
**Emphasise in rebuttal:** Multi-method discordance (ρ = −0.564) as strength, not weakness.  
**Do not add:** New XAI experiments before publication.

### 12.2 Conference (6-page IEEE)

**Retain:** One node heatmap + dense prose metrics.  
**Do not restore:** SHAP, temporal, or dual-path figures — page cost exceeds value.  
**Strengthen prose:** Keep exact \|φ\| values and ρ statistics; they substitute for figures.

### 12.3 Next implementation phase priorities

| Priority | Action | Type |
|---|---|---|
| P1 | Rebuild **Figure 1** framework (vector, IEEE quality) | Graphics |
| P2 | Vectorise **Fig. 7** node heatmap (currently raster PNG) | Graphics |
| P3 | Harmonise journal Fig. 1 PNG → match conference TikZ palette | Graphics |
| P4 | Optional environment/clarification sentence (Captum/custom IG) | Editorial |
| P5 | SHAP stability bootstraps | Research (post-publication) |

### 12.4 What not to do

- Do not rerun Exp04 for publication mapping purposes  
- Do not add explainability figures to conference paper  
- Do not remove journal Figs. 8–9 without Discussion restructuring  
- Do not claim causal attribution beyond frozen wording  

---

## Appendix A — Current vs Recommended Mapping

| Exp04 output | Journal (current) | Journal (recommended) | Conference (current) | Conference (recommended) |
|---|---|---|---|---|
| SHAP stress summary | Fig. 6a | **Retain** | Excluded | **Exclude** |
| SHAP demand summary | Fig. 6b | **Retain** | Excluded | **Exclude** |
| Node heatmap | Fig. 7 | **Retain** | Fig. 5 | **Retain** |
| Temporal α_t | Fig. 8 | **Retain** | Excluded | **Exclude** |
| Dual-path stress | Fig. 9 | **Retain** | Excluded | **Exclude** |
| Table 7 | Main | **Retain** | Inline prose | **Retain prose** |
| Permutation figure | Not in main | **Supplementary** | Excluded | **Exclude** |
| Regional panel | Not in main | **Supplementary** | Excluded | **Exclude** |
| SHAP bar | Appendix S1 | **Retain S1** | Excluded | **Exclude** |

**Delta from current state:** Zero mandatory changes. Supplementary promotion of permutation and regional figures is optional enrichment only.

---

*Phase 18 complete. Publication blueprint ready for next graphics/editorial implementation phase.*
