# Publication Graphics Enhancement Report — Phase 19

**Date:** 7 July 2026  
**Authority:** `paper/prompts/19_Publication_Graphics_Enhancement.md`  
**Inputs:** `Explainability_Publication_Mapping_Report.md`, `paper/latex/`, `paper/conference/`, `paper/template/`, `paper/final_results_package/`  
**Constraint:** Blueprint only — no manuscript edits, no figure regeneration, no experiments

---

## 1. Graphics Quality Assessment

### 1.1 Overall verdict

| Venue | Current grade | Target | Primary gap |
|---|---|---|---|
| **Journal** (`paper/latex/`) | **C+** | **A** | Figs. 1–2 matplotlib raster; Figs. 6–9 mixed quality; no unified vector master |
| **Conference** (`paper/conference/`) | **B−** | **A−** | Figs. 1–2 TikZ improved but below Transactions standard; Fig. 5 raster |
| **Asset pipeline** (`final_results_package/`) | **B** | **A** | PDF exists for Figs. 1–2, 4–5; not propagated to journal |

**Science:** Frozen and correct across all figures.  
**Visual communication:** Inconsistent venue styling, raster-heavy journal, sub-8 pt labels in conference TikZ, grayscale weakness in pale blue fills.

### 1.2 Cross-cutting issues

| Issue | Affected assets | IEEE impact |
|---|---|---|
| **Raster schematics** | Journal Figs. 1–2 (200 KB / 131 KB PNG) | Blur at print; non-editable |
| **Font inconsistency** | Matplotlib sans vs LaTeX Times vs TikZ CM | Unprofessional mixed typography |
| **Palette drift** | `#ebf8ff` fills vs `#3182ce` bars vs Exp04 SHAP colours | Figures do not look co-authored |
| **Weak visual hierarchy** | Figs. 1–2 equal-weight boxes | Reviewer reads as auto-diagram |
| **Grayscale failure** | Light blue fills, green accent only on S2 bar | B&W print loses structure |
| **Caption under-spec** | Several captions lack sample size / method tag | Reviewer must hunt in prose |
| **Venue divergence** | Journal PNG Fig. 1 ≠ conference TikZ Fig. 1 | Maintenance risk |
| **Frozen Exp04 lock** | Figs. 6–9 cannot be recomputed | Style harmonisation only via replot from CSV |

### 1.3 Design system (recommended master)

Adopt **`paper/conference/figures/ieee_fig_colors.tex`** as canonical:

| Token | Hex | Use |
|---|---|---|
| `ieeeblue` | `#2c5282` | Primary borders, axis labels |
| `ieeelightblue` | `#ebf8ff` | Fill (use 15% tint for print) |
| `ieeegreen` | `#276749` | S2 / final emphasis |
| `ieeered` | `#c53030` | Superseded S1 |
| `ieeegray` | `#4a5568` | Arrows, secondary text |
| `ieeedark` | `#1a202c` | Titles |
| `ieeeaccent` | `#3182ce` | Baseline models in bar charts |

**Typography:** IEEE Times (journal body font); minimum **8 pt** in figures at final column width; tensor annotations **7 pt** italic subscript style.  
**Line weights:** 0.6 pt arrows (primary), 0.45 pt box borders, 1.0 pt axis spines.  
**Export:** PDF vector primary; 600 DPI PNG fallback for heatmaps only.

---

## 2. Figure-by-Figure Review

### 2.1 Architecture & workflow figures

#### Figure 1 — PF-STGT framework (HIGHEST PRIORITY)

| Attribute | Journal | Conference |
|---|---|---|
| **File** | `figure_01_framework.png` (200 KB raster) | `figure_01_tikz.tex` (vector) |
| **Source** | `build_publication_assets.py` matplotlib | TikZ inline |
| **Verdict** | **REDRAW** | **REDRAW** (unify with journal master) |

| Criterion | Assessment | Action |
|---|---|---|
| Scientific content | Correct — preserve exactly | No change |
| Vector quality | Journal: raster; Conference: vector but crude | Single PDF/SVG master |
| Typography | 8.5 pt matplotlib / 6 pt TikZ tensors | ≥8 pt labels, 7 pt annotations |
| Visual hierarchy | Flat — all boxes equal | Three-band layout (see §6) |
| Colour / grayscale | Pale fills wash out | Add border weight; test B&W |
| Caption | Generic | Enrich with T, N, F dimensions (caption only phase) |
| Placement | Journal §3 after architecture intro; Conference §II-C inline | Keep |

---

#### Figure 2 — S2 architecture decision

| Attribute | Journal | Conference |
|---|---|---|
| **File** | `figure_02_s2_architecture.png` (131 KB) | `figure_02_tikz.tex` |
| **PDF available** | Yes (`final_results_package/figures/figure_02_s2_architecture.pdf`) | TikZ only |
| **Verdict** | **VECTORISE** (use PDF) + **REDRAW** | **REDRAW** (match Fig. 1 style) |

| Criterion | Assessment | Action |
|---|---|---|
| Scientific content | S1→S2, −4.66 MW, metrics correct | Preserve |
| Visual hierarchy | S1/S2 equal prominence except colour | Enlarge S2; mute S1 |
| Typography | 9 pt body inconsistent with Fig. 1 | Unify with Fig. 1 system |
| Panel layout | Trunk + two metric boxes cramped | Widen trunk; align metric boxes |
| Caption | Adequate | Add "frozen test split" in caption phase |

---

#### Figure 3 — Training curves (journal only)

| Attribute | Value |
|---|---|
| **File** | `figure_03_training_curves.png` (233 KB) |
| **Type** | Stitched raster panels from Exp01 |
| **Verdict** | **KEEP** (low priority) or **IMPROVE PANEL LAYOUT** |

| Criterion | Assessment | Action |
|---|---|---|
| Role | Historical diagnostic; not headline science | No conference inclusion |
| Quality | Embedded PNG screenshots; axis labels inconsistent | Re-export as vector line plots from frozen CSV if data available; else harmonise panel borders/fonts |
| Caption | Must stress "W20 reference run, not S2-specific" | Clarify in caption phase |
| Priority | **Low** — consider supplementary only |

---

### 2.2 Results bar charts

#### Figure 4 — Benchmark comparison

| Attribute | Journal | Conference |
|---|---|---|
| **File** | PNG 89 KB | PDF 26 KB ✓ |
| **Verdict** | **VECTORISE** (switch to PDF) | **KEEP** + minor typography |

| Criterion | Assessment | Action |
|---|---|---|
| Data | Frozen CSV — correct | No change |
| Colour | S2 green, others accent blue — good | Apply design tokens |
| Labels | Value annotations (+2 MW offset) — good | Ensure 9 pt min |
| Legend | In-bar labels — good for IEEE | Keep |
| Whitespace | Moderate right margin for values | Tighten to column width |
| Caption | Add n=264, macro MAE definition | Caption phase |

---

#### Figure 5 — Ablation comparison

| Attribute | Journal | Conference |
|---|---|---|
| **File** | PNG 108 KB | PDF 27 KB ✓ |
| **Verdict** | **VECTORISE** | **KEEP** + minor typography |

| Criterion | Assessment | Action |
|---|---|---|
| Ordering | MAE-sorted — correct | Keep |
| A4 distinction | Demand-only — caption notes | Bold or hatch A4 bar |
| Colour | S2 green — consistent with Fig. 4 | Unify palette |
| Caption | Note A4 lacks OSI output | Caption phase |

---

### 2.3 Explainability figures (frozen Exp04 — style only)

#### Figures 6a / 6b — SHAP coalition summaries

| Attribute | Value |
|---|---|
| **Files** | `figure_06_shap_summary_stress.png`, `figure_06_shap_summary_demand.png` (~80 KB each) |
| **Verdict** | **IMPROVE TYPOGRAPHY & COLOUR** (replot from frozen CSV via `replot_frozen_explainability.py`) |

| Criterion | Assessment | Action |
|---|---|---|
| Scientific | G8/G6 stress; G6/G4/G10 demand — frozen | No recomputation |
| Readability | Beeswarm dense at column width | Increase figure height; coalition labels horizontal |
| Colour map | Default SHAP cmap may clash | Use sequential blue-green diverging from design system |
| Panel layout | Two separate figures — correct per Phase 18 | Keep split (not merged) |
| Placement | Journal §5.5 Error Analysis | Keep; cross-ref §5.6 |
| Caption | Add "validation n=20, grouped \|φ\|" | Caption phase |

---

#### Figure 7 — Node attribution heatmap

| Attribute | Journal | Conference |
|---|---|---|
| **File** | PNG 67 KB (1050×900) | Same PNG |
| **Verdict** | **VECTORISE / REDRAW** | **VECTORISE** (highest conference XAI figure) |

| Criterion | Assessment | Action |
|---|---|---|
| Scientific | Dhaka mass 340.36 — correct | Preserve |
| Resolution | Adequate at column width; soft text | Rebuild as vector heatmap from frozen CSV |
| Colour | Default matplotlib heatmap | Use `ieeeblue`→`ieeelightblue` sequential |
| Labels | Division names must be readable | 8 pt; rotate if needed |
| Annotation | ρ=0.422 in caption not on figure | Add subtle in-figure ρ annotation |
| Placement | Conference §IV-D — only XAI figure | Keep |

---

#### Figure 8 — Temporal attribution

| Attribute | Value |
|---|---|
| **File** | `figure_08_temporal_attribution.png` (43 KB) |
| **Verdict** | **IMPROVE TYPOGRAPHY** |

| Criterion | Assessment | Action |
|---|---|---|
| Scientific | Near-uniform α_t — honest null | Preserve |
| Visual interest | Low — line/bar flat | Simplify to clean bar chart with error band |
| Risk | Over-designed figure implies false precision | Minimal style; muted colours |
| Caption | Emphasise "near-uniform" | Critical for reviewer trust |

---

#### Figure 9 — Dual-path stress attribution

| Attribute | Value |
|---|---|
| **File** | `figure_09_stress_attribution.png` (77 KB) |
| **Verdict** | **IMPROVE PANEL LAYOUT** |

| Criterion | Assessment | Action |
|---|---|---|
| Scientific | 52.2% agreement — correct | Preserve |
| Layout | Multi-panel may be cramped | Align panels; shared y-axis for coalitions |
| Colour | Path A vs Path B need distinct tokens | SHAP=`ieeeblue`, OSI components=`ieeegreen`/`ieeered` |
| Caption | State 24 case studies, 4 on test | Caption phase |

---

### 2.4 Supplementary figures (journal)

| ID | File | Verdict | Notes |
|---|---|---|---|
| **S1** | `figure_shap_bar_stress.png` | Improve typography | Signed φ detail |
| **S4** | `figure_feature_importance_ranking.png` | Improve + vectorise | Permutation ΔMAE |
| **S5** | `figure_regional_contribution.png` | Improve panel layout | Extends Fig. 7 |
| **S2–S3** | Exp02A verification plots | Keep as-is | Diagnostic |

---

### 2.5 Summary action matrix

| Figure | Journal action | Conference action | Priority |
|---|---|---|---|
| **1** | Redraw vector | Redraw (unify) | **P0** |
| **2** | Redraw + PDF | Redraw (unify) | **P0** |
| **3** | Keep / minor improve | N/A | P4 |
| **4** | Switch to PDF | Keep PDF | P1 |
| **5** | Switch to PDF | Keep PDF | P1 |
| **6a/6b** | Replot style | N/A | P2 |
| **7** | Vectorise heatmap | Vectorise heatmap | **P1** |
| **8** | Replot style | N/A | P3 |
| **9** | Panel layout | N/A | P2 |

---

## 3. Table-by-Table Review

### 3.1 Journal tables (`paper/latex/tables/`)

| Table | File | Readability | Recommended improvements |
|---|---|---|---|
| **I** Dataset | `table_01_dataset.tex` | Good | Add `\arraystretch{1.2}`; align property column left; consider two-column narrow layout |
| **II** Training | `table_02_training.tex` | Good | Merge visual style with Table I; ensure optimizer line breaks |
| **III** Benchmark | `table_03_benchmark.tex` | Cramped | Already `\resizebox` — add `\arraystretch{1.15}`; right-align numerics; footnote for subset models |
| **IV** Benchmark stats | `table_04_benchmark_stats.tex` | Dense | Consider splitting Wilcoxon to table footnote row (conference pattern) |
| **V** Ablation | `table_05_ablation.tex` | Good | Sort rows by MAE; dash `--` for A4 OSI columns OK |
| **VI** Architecture | `table_06_architecture.tex` | Good | Highlight S2 row with `\rowcolor` (gray 10%) — grayscale safe |
| **VII** Explainability | `table_07_explainability.tex` | Sparse | Add second column group for demand vs stress metrics; widen |

**Global table rules (implementation phase):**
- Captions: no trailing period (IEEE table style) — already correct in conference
- Use `\scriptsize` + `\resizebox` only when necessary; prefer `tabularx` for wide tables
- Vertical rules: keep for IEEE consistency but ensure `\hline` spacing uniform
- Numerals: `siunitx` `S` column type for decimal alignment (optional upgrade)

---

### 3.2 Conference tables (`paper/conference/tables/`)

| Table | File | Readability | Recommended improvements |
|---|---|---|---|
| **I** Setup | `table_01_setup.tex` | Good | Merged dataset+training — effective space use; verify resizebox not needed |
| **II** Benchmark | `table_02_benchmark.tex` | Good | Wilcoxon footer row — excellent; ensure italic footer doesn't wrap awkwardly |
| **III** Ablation | `table_03_ablation.tex` | Good | Six rows after Phase 23 review — verify column fit without resize |

**Conference-specific:** Tables already production-tuned. Graphics phase should **not** widen tables; figure reduction compensates.

---

## 4. Required Improvements

### 4.1 Mandatory (blocks Transactions-quality print)

1. **Figure 1** — Full vector redraw; unified journal + conference master  
2. **Figure 2** — Match Fig. 1 design language; journal adopts PDF vector  
3. **Journal Figs. 4–5** — Replace PNG with existing PDF from `final_results_package/`  
4. **Figure 7** — Vector heatmap rebuild from frozen node-attribution CSV  
5. **Design system document** — Export `ieee_fig_colors` as matplotlib/TikZ shared JSON or YAML for build script  

### 4.2 High-value (reviewer perception)

6. Harmonise Fig. 6a/6b replot colours with design system  
7. Fig. 9 panel alignment and legend clarity  
8. Fig. 8 simplified bar form with explicit "near-uniform" annotation  
9. Table III / conference Table II — `siunitx` alignment  
10. Caption enrichment pass (separate editorial phase — list specs here only)

### 4.3 Optional (polish)

11. Fig. 3 training curves vectorisation or supplementary demotion  
12. Supplementary S4/S5 style harmonisation  
13. Conference Fig. 1–2 icon additions (minimal line icons)  
14. Grayscale compliance test on all figures before upload  

### 4.4 Explicitly out of scope

- Rerunning Experiment 04  
- Changing numerical values, bar heights, SHAP φ, or heatmap masses  
- Manuscript prose edits (this phase)  
- New figures not in Phase 18 mapping  

---

## 5. Graphics Priority Ranking

| Rank | Asset | Action | Impact |
|---|---|---|---|
| **P0** | Figure 1 (both venues) | Full vector redraw | First impression; supervisor feedback |
| **P0** | Figure 2 (both venues) | Redraw + unify | Pairs with Fig. 1; methodology credibility |
| **P1** | Journal Figs. 4–5 | PNG → PDF | Quick win; assets exist |
| **P1** | Figure 7 heatmap | Vectorise | Conference only XAI figure; journal spatial XAI |
| **P2** | Figs. 6a/6b | Replot style from CSV | Explainability block cohesion |
| **P2** | Figure 9 | Panel layout | Dual-path narrative clarity |
| **P3** | Figure 8 | Typography simplify | Honest null result presentation |
| **P3** | Tables I–VII | Spacing / alignment | Readability without data change |
| **P4** | Figure 3 | Keep or supp. | Low scientific weight |
| **P4** | Supplementary S1/S4/S5 | Style pass | Appendix only |

---

## 6. Figure 1 Final Redesign Plan

### 6.1 Objective

Produce one **master vector figure** (`figure_01_framework.pdf` + `.svg`) that reads as an IEEE Transactions system diagram while preserving **identical** modules, tensor shapes, and data flow.

### 6.2 Layout specification

```
┌─────────────────────────────────────────────────────────────────┐
│  PF-STGT Multi-Task Forecasting Framework          [title band]   │
├──────────────┬──────────────────────────────┬─────────────────┤
│   INPUTS     │         ENCODING             │    OUTPUTS      │
│  (col 1)     │         (col 2)              │    (col 3)      │
│              │                              │                 │
│ Node tensor  │   Embedding + PE             │  Demand Head    │
│ Global ctx   │   ┌────────┐ ┌────────┐     │  (9 MW)         │
│ Graph adj    │   │ Graph  │ │Temporal│     │                 │
│              │   │ Trans. │ │ Trans. │     │  Stress Head    │
│              │   └───┬────┘ └───┬────┘     │  (OSI)          │
│              │       └────┬─────┘          │                 │
│              │      Gated Fusion            │                 │
└──────────────┴──────────────────────────────┴─────────────────┘
   Footer (caption-level): S2 correlation graph (τ=0.65)
```

### 6.3 Element specifications

| Element | Specification |
|---|---|
| **Canvas** | 7.0 in × 3.2 in (full width); 3.5 in × 3.0 in (column) |
| **Input boxes** | Equal width 1.6 in; stacked vertical gap 0.25 in |
| **Encoder boxes** | Graph + Temporal side-by-side; Fusion centred below, **1.3× width** |
| **Head boxes** | Demand above Stress; equal width 0.9 in |
| **Arrows** | Orthogonal routing; 0.6 pt `#4a5568`; fusion paths `#276749` |
| **Title** | 10 pt bold `#1a202c`; sans-serif or Times bold |
| **Box labels** | 8 pt regular |
| **Tensor lines** | 7 pt italic beneath label: `(B,T=7,N=9,F=9)` etc. |
| **Fills** | Input/output: `#ebf8ff` @ 100%; encoders: white with `#2c5282` border |
| **Borders** | 0.75 pt `#2c5282`; corner radius 3 pt |
| **Grayscale test** | Borders must remain visible when fills → 15% gray |

### 6.4 Production workflow (next phase)

1. Build in **Illustrator / Figma / draw.io** using locked artboard  
2. Export PDF (vector text outlined OR embed Times)  
3. Generate `figure_01_tikz.tex` wrapper: `\includegraphics{figure_01_framework.pdf}` for conference  
4. Replace journal `figure_01.tex` PNG include with same PDF  
5. Visual regression: side-by-side with old figure — all 9 modules present  
6. Print test: 300 DPI laser + grayscale copy  

### 6.5 Acceptance criteria

- [ ] All tensor dimensions unchanged  
- [ ] All module names unchanged  
- [ ] Data-flow topology identical to `build_publication_assets.py` diagram  
- [ ] Readable at 3.5 in column width without zoom  
- [ ] Passes IEEE grayscale print test  
- [ ] Single source file used by journal and conference  

---

## 7. Journal Graphics Plan

### 7.1 Figure rollout sequence

| Phase | Figures | Deliverable |
|---|---|---|
| **J-G1** | 1, 2 | Vector PDF masters in `paper/latex/figures/` |
| **J-G2** | 4, 5 | Replace PNG includes in `figure_04.tex`, `figure_05.tex` with PDF |
| **J-G3** | 7 | Vector heatmap from `results/explainability/` CSV |
| **J-G4** | 6a, 6b, 8, 9 | `replot_frozen_explainability.py` style pass |
| **J-G5** | 3 | Optional supplementary demotion or panel polish |

### 7.2 Float & placement (no change — verify after resize)

| Fig | Section | Float | Notes |
|---|---|---|---|
| 1 | Methodology §3 | `[!t]` | After architecture intro |
| 2 | Methodology §3 | `[!t]` | After Eq. spatial attention |
| 3 | Experimental / Results | `[!t]` | Consider appendix move |
| 4 | Results benchmark | `[!t]` | With Table III |
| 5 | Results ablation | `[!t]` | With Table V |
| 6a/b | Error analysis §5.5 | `[!t]` | Paired subfigures |
| 7–9 | Explainability §5.6 | `[!t]` | Sequential after Table 7 |

### 7.3 Caption objectives (graphics phase — text draft only)

| Fig | Caption must communicate |
|---|---|
| 1 | End-to-end pipeline; T=7, N=9; parallel fusion; dual heads |
| 2 | S2 freeze; −4.66 MW vs S1; 749,058 params |
| 4 | Macro MAE; n=264; S2 lowest |
| 5 | Ablation MAE order; A4 demand-only |
| 6a | Stress coalition \|φ\|; validation n=20 |
| 6b | Dhaka demand coalitions |
| 7 | Spatial mass; Dhaka dominance; ρ=0.422 |
| 8 | Near-uniform α_t; peak t−6 |
| 9 | Dual-path; 52.2% agreement |

### 7.4 Table polish sequence

1. Tables I–II: spacing harmonisation  
2. Table III: numeric alignment + footnote  
3. Table VII: two-column metric layout  
4. Appendix tables S2–S4: monospace URL break improvement only  

---

## 8. Conference Graphics Plan

### 8.1 Current figure set (5 figures)

| Conf. Fig. | Source | Action |
|---|---|---|
| 1 | `figure_01_tikz.tex` | Replace with unified PDF from §6 |
| 2 | `figure_02_tikz.tex` | Replace with unified PDF (match Fig. 1) |
| 3 | `figure_04_benchmark_comparison.pdf` | Keep; verify 9 pt labels |
| 4 | `figure_05_ablation_comparison.pdf` | Keep; hatch A4 optional |
| 5 | `figure_07_node_importance.png` | **Vectorise** (P1) |

### 8.2 Column-width constraints

- Full-width figures: **none** — all single column  
- Max height: ~2.8 in to avoid float page takeover  
- TikZ `\resizebox{\linewidth}{!}` — replace with designed column-width artboards (3.5 in) to avoid scale-induced thin lines  

### 8.3 Conference-specific caption notes

- Fig. 1: shorter than journal — drop footer to caption  
- Fig. 5: "Mass concentrates on high-load divisions" — add ρ=0.422 in caption (already in prose)  
- No period after table captions (IEEE) — already correct  

### 8.4 Overleaf package sync

After graphics phase, rebuild `conference_overleaf.zip` via `build_overleaf_zip.sh` with:
- Real PNG/PDF assets only (no symlinks)  
- Unified Fig. 1–2 PDFs  
- Vector Fig. 5  

---

## 9. Expected Publication Impact

### 9.1 Reviewer perception

| Before | After (planned) |
|---|---|
| "Diagrams look auto-generated" | "Professional IEEE system figures" |
| "Mixed raster/vector quality" | "Consistent vector pipeline" |
| "Explainability figures from different tools" | "Cohesive visual identity" |
| "Grayscale print weak" | "Print-safe design system" |

### 9.2 Quantitative targets

| Metric | Current | Target |
|---|---|---|
| Vector figures (journal) | 0/9 schematics + 0/2 bars | 9/9 |
| Min font size at column width | 6 pt (TikZ tensors) | ≥7 pt |
| Palette consistency | ~60% | 100% design tokens |
| Venue figure parity (1–2) | Divergent | Single master |
| Overleaf compile failures | libpng risk on symlinks | Zero (real assets) |

### 9.3 Risk mitigation

| Risk | Mitigation |
|---|---|
| Exp04 recomputation prohibited | Replot from frozen CSV only |
| Science drift during redraw | Checklist §6.5 acceptance criteria |
| Conference page overflow | Figure height cap 2.8 in |
| Journal page overflow | No new figures; replace in-place only |

### 9.4 Implementation phase handoff

**Next phase (20):** Execute graphics in priority order P0→P1→P2.  
**Deliverables:** Updated assets in `paper/final_results_package/figures/`, propagated to `paper/latex/figures/` and `paper/conference/figures/`.  
**Verification:** Visual QA report + grayscale print test + Overleaf clean compile.  
**Manuscript integration:** Separate editorial phase after assets frozen.

---

## Appendix A — File Path Reference

| Asset | Authoritative path |
|---|---|
| Build script | `paper/final_results_package/build_publication_assets.py` |
| Replot script | `paper/final_results_package/replot_frozen_explainability.py` |
| Colour tokens | `paper/conference/figures/ieee_fig_colors.tex` |
| Exp04 figures | `experiments/experiment_04_explainability_analysis/figures/` |
| Journal wrappers | `paper/latex/figures/figure_*.tex` |
| Conference wrappers | `paper/conference/figures/figure_*.tex` |
| Overleaf builder | `paper/conference/build_overleaf_zip.sh` |

---

## Appendix B — Caption & Legend Checklist (implementation phase)

- [ ] Every figure caption states task (demand vs stress) where dual-task  
- [ ] Sample sizes (n=264, n=20, 24 cases) in caption or first sentence  
- [ ] Units on all axes (MW, \|φ\|, α_t)  
- [ ] Abbreviations defined once per figure: OSI, PF-STGT, MAE  
- [ ] Table captions without terminal period (IEEE)  
- [ ] Figure captions with terminal period (IEEE)  
- [ ] No figure title duplicated verbatim in caption first line  

---

*Phase 19 complete. Publication graphics blueprint ready for implementation phase. No assets, manuscripts, or experiments were modified.*
