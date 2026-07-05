# Final Polish Report

**Phase:** 21 — Final Camera-Ready Polish  
**Manuscript:** `paper/conference/main.pdf`  
**Template reference:** `paper/template/IEEE-conference-template-062824/`  
**Date:** 5 July 2026

---

## Executive Summary

A full end-to-end review was conducted across all six pages, five figures, three tables, three numbered equations, 22 references, and the complete author block. The manuscript was already camera-ready following Phase 20. This phase applied **only objective, non-scientific micro-polishes** and halted at the stop condition: further edits would be subjective.

**No numerical values, experimental outcomes, figures, tables, or conclusions were modified.**

---

## 1. Author Block Refinements

### Verification against IEEE template

The author block was compared line-by-line with `IEEE-conference-template-062824.tex` (lines 22–57).

| Template element | Manuscript status |
|---|---|
| `\author{` opens directly into `\IEEEauthorblockN` | ✓ Matches |
| Line 1: `\textit{Department...} \\` (space before break) | ✓ Matches |
| Line 2: `\textit{American International...}\\` (no trailing space) | ✓ Matches |
| Line 3: `Dhaka, Bangladesh \\` | ✓ Matches |
| Line 4: email address | ✓ Matches |
| Six `\and`-separated blocks, equal depth | ✓ Matches |

**Action taken:** None required. Author block already conforms to template visual structure.

---

## 2. Writing Refinements

| Location | Change | Rationale |
|---|---|---|
| Discussion opening | “The frozen evaluation demonstrates” → “These results demonstrate” | Removes redundant “frozen” without altering scope |
| Discussion opening | “deployment judgement” → “deployment decisions” | Clearer operator-facing language |
| Results §Explainability | “frozen S2 checkpoint” → “S2 checkpoint” | Avoids repetitive qualifier; frozen protocol unchanged |

**No paragraph-level rewrites.** Scientific meaning preserved throughout.

---

## 3. Figure Refinements

| Figure | Resolution | Width | Placement | Action |
|---|---|---|---|---|
| Fig. 1 (framework) | 3261×1911 px | `\linewidth` | Post-citation §III-C | Verified ✓ |
| Fig. 2 (S2 arch.) | 2961×1610 px | `\linewidth` | After architecture text | Verified ✓ |
| Fig. 4 (benchmark) | 2661×1461 px | `\linewidth` | With Table II | Verified ✓ |
| Fig. 5 (ablation) | 2660×1461 px | `\linewidth` | With Table III | Verified ✓ |
| Fig. 7 (attribution) | 1050×900 px | `\linewidth` | Post-citation §V-D | Verified ✓ |

- All figures use `\centerline{\includegraphics[width=\linewidth]{...}}` per IEEE template
- All cited before first appearance
- No clipping, overlap, or column overflow detected
- Fig. 7 source resolution is lower than benchmark figures but sufficient at column width (~300 dpi equivalent)

**Action taken:** None to PNG assets (declared FINAL). LaTeX presentation confirmed optimal.

---

## 4. Table Refinements

| Table | Change | Rationale |
|---|---|---|
| Table I | Removed trailing period from caption | IEEE template table-head style |
| Table II | Removed trailing period from caption | Consistency |
| Table III | Removed trailing period from caption | Consistency |

Existing `\arraystretch{1.15}` and `\resizebox{\columnwidth}{!}` retained. All data values unchanged.

---

## 5. Layout Refinements

| Item | Status |
|---|---|
| Page count | 6 (within 7-page limit) |
| Overfull hbox | **0** |
| Compile errors | **0** |
| Broken citations/references | **0** |
| Float placement | Inline after first `\ref{}` |
| Figure wall | None (Fig. 1 / Fig. 2 separated by equation) |
| Column balance | Acceptable across all pages |

**Preamble addition:**
```latex
\setlength{\abovecaptionskip}{4pt}
\setlength{\belowcaptionskip}{0pt}
```

Minor `Underfull \vbox` (badness 3029–10000) on pages 1 and 5 from float-to-text ratio — cosmetic only, not visible as white gaps.

---

## 6. Typography Refinements

| Check | Status |
|---|---|
| `microtype` enabled | ✓ |
| Widow/orphan penalties | ✓ |
| British spelling consistent (`synchronised`, `emphasise`, `Optimiser`) | ✓ |
| En-dash compounds (`demand--stress`, `spatial--temporal`) | ✓ |
| `Task~1`, `Fig.~`, `Table~`, `Eq.~` non-breaking spaces | ✓ |
| Math typography (`\mathrm`, `\mathcal`, `\hat`) | ✓ |
| Figure captions end with period; table captions without period | ✓ (aligned post-polish) |

---

## 7. Consistency Checks

| Category | Finding |
|---|---|
| **Terminology** | PF-STGT, S2, B07, A1–A6, OSI used consistently |
| **Abbreviations** | OSI defined at first use; MW, MAE, RMSE consistent |
| **Capitalization** | Section titles sentence case; proper nouns preserved |
| **Figure style** | All `[htbp]`, `\centerline`, `\linewidth` |
| **Table style** | All `[htbp]`, `center`, `\scriptsize`, bordered |
| **Citation style** | IEEE numeric, compressed ranges via `cite` package |
| **Reference style** | IEEEtran.bst, 22 entries, compile-clean |

---

## 8. IEEE Template Compliance

| Element | Compliant |
|---|---|
| `\documentclass[conference]{IEEEtran}` | ✓ |
| `\IEEEoverridecommandlockouts` | ✓ |
| Author block structure | ✓ |
| Abstract + IEEEkeywords | ✓ |
| Table environment | ✓ |
| Figure environment | ✓ |
| Acknowledgment spelling (American) | ✓ |
| Bibliography | ✓ |

---

## 9. Remaining Manual Recommendations

| Item | Priority | Notes |
|---|---|---|
| Fig. 7 source resolution | Low | 1050×900 px vs 2660+ for other figures; acceptable at print but could be re-exported at higher dpi if venue requires |
| Last-page column height | Low | References column slightly shorter than left; typical for 6-page papers |
| PDF metadata | Optional | Add title/author metadata in submission portal |
| Author ORCID | Optional | Template permits ORCID; emails provided |

**No blocking issues identified.**

---

## 10. Final Page Count

| Metric | Value |
|---|---|
| **Pages** | **6** |
| Body words | ~2,655 |
| Bibliography entries | 22 |
| Figures | 5 |
| Tables | 3 |

### Compile verification
```
pdflatex → bibtex → pdflatex × 2
Exit code: 0 | main.pdf (6 pages, 796,550 bytes)
Overfull: 0 | Errors: 0 | Undefined refs: 0
```

---

## Stop Condition Applied

After the micro-polishes above, further edits (paragraph rewrites, float forcing, figure rescaling) were assessed as **subjective** with no measurable gain. Refinement halted per Phase 21 instructions.

---

## 🟢 Camera-Ready

The manuscript at `paper/conference/main.pdf` is scientifically frozen, visually conformant with the IEEE conference template, and ready for submission.
