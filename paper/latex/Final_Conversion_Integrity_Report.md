# Final Conversion Integrity Report — Phase 15 Post-Conversion Audit

**Audit date:** 2026-07-04  
**Auditor role:** Independent release verification (read-only audit + one targeted label repair)  
**Scope:** `paper/latex/` vs frozen Markdown source `paper/sections/`  
**Conversion status:** Not re-run; existing artefacts validated

---

## 1. Repository Integrity

### Required directory structure

| Path | Status |
|------|--------|
| `paper/sections/` | ✓ Present (12 manuscript files + README) |
| `paper/latex/` | ✓ Present (complete IEEE project) |
| `paper/latex/sections/` | ✓ 8 section `.tex` files |
| `paper/latex/figures/` | ✓ 10 PNGs + 11 float `.tex` snippets |
| `paper/latex/tables/` | ✓ 7 table float `.tex` files |
| `paper/latex/bibliography/` | ✓ `12_References.bib` |
| `paper/template/` | ✓ Official IEEE conference template |
| `paper/publication_freeze/` | ✓ Freeze inventories present |
| `paper/final_results_package/` | ✓ Source figures/tables |

### Duplicate / stale artefact scan

| Check | Result |
|-------|--------|
| Duplicate bibliography files | **Expected pair only:** canonical `paper/sections/12_References.bib` + build copy `paper/latex/bibliography/12_References.bib` (MD5-identical) |
| Duplicate `IEEEtran.cls` | **Expected pair only:** `paper/template/.../IEEEtran.cls` + `paper/latex/IEEEtran.cls` (MD5-identical) |
| Duplicate manuscript LaTeX project | **None.** `manuscript/overleaf/` holds legacy figure copies and README stubs only — no `main.tex`, no section `.tex` files |
| Abandoned partial conversion | **None detected** |
| Empty `.tex`/`.bib`/`.cls` files | **0** |
| Temp files (`~`, `.swp`, `.bak`) | **0** |
| TODO / FIXME / TBD in `.tex` | **0** |
| Build artefacts | `main.aux`, `main.bbl`, `main.blg`, `main.log`, `main.pdf` (normal post-compile) |

---

## 2. Conversion Completeness

Every frozen manuscript component maps to exactly one LaTeX destination:

| Component | Markdown source | LaTeX destination | Status |
|-----------|-----------------|-------------------|--------|
| Title | `01_Title.md` | `main.tex` `\title{}` | ✓ Exact match |
| Abstract | `02_Abstract.md` | `main.tex` `\begin{abstract}` | ✓ Jaccard 1.000 |
| Keywords | `03_Keywords.md` | `main.tex` `\begin{IEEEkeywords}` | ✓ Exact match |
| Introduction | `04_Introduction.md` | `sections/01_introduction.tex` | ✓ |
| Related Work | `05_Related_Work.md` | `sections/02_related_work.tex` | ✓ |
| Methodology | `06_Methodology.md` | `sections/03_methodology.tex` | ✓ |
| Experimental Setup | `07_Experimental_Setup.md` | `sections/04_experimental_setup.tex` | ✓ |
| Results | `08_Results.md` | `sections/05_results.tex` | ✓ |
| Discussion | `09_Discussion.md` | `sections/06_discussion.tex` | ✓ |
| Conclusion | `10_Conclusion.md` | `sections/07_conclusion.tex` | ✓ |
| Appendix | `11_Appendix_A_Supplementary_Materials.md` | `sections/08_appendix.tex` | ✓ |
| Bibliography | `12_References.bib` | `bibliography/12_References.bib` | ✓ Identical copy |

`main.tex` contains **8 unique** `\input{}` directives — no missing or duplicated section imports.

Section order matches frozen manuscript: Introduction → Related Work → Methodology → Experimental Setup → Results → Discussion → Conclusion → Appendix (`\appendices`).

---

## 3. Citation Integrity

| Metric | Value |
|--------|-------|
| Total `\cite{}` invocations | 260 |
| Unique citation keys used | 38 |
| Bibliography entries | 38 |
| Missing keys (cite → bib) | **0** |
| Unused bib entries | **0** |
| Duplicate bib keys | **0** |

Bibliography configuration in `main.tex`:

```latex
\bibliographystyle{IEEEtran}
\bibliography{bibliography/12_References}
```

`bibtex main` produces `main.bbl` via `IEEEtran.bst`. All 38 keys resolve after full compile cycle.

---

## 4. Figure Integrity

| Check | Result |
|-------|--------|
| PNG files in `figures/` | **10** (all source figures from `final_results_package`) |
| Figure float snippets | **11** (`figure_01`–`09`, `06a`, `06b`) |
| `\includegraphics` paths | **10** — all resolve |
| Duplicate PNG content (MD5) | **0** |
| Broken image paths | **0** |

### Figure labels vs references

| Label | Floated | `\ref{}` in body |
|-------|---------|------------------|
| `fig:1` | ✓ Methodology | ✓ |
| `fig:2` | ✓ Methodology | — (not cited in source Markdown either) |
| `fig:3` | ✓ Experimental Setup | — (not cited in source Markdown) |
| `fig:4` | ✓ Results | ✓ (multiple) |
| `fig:5` | ✓ Results | ✓ (multiple) |
| `fig:6a` | ✓ Results | — (cited as plain text "Figure 6a") |
| `fig:6b` | ✓ Results | — (cited as plain text "Figure 6b") |
| `fig:7` | ✓ Results | ✓ |
| `fig:8` | ✓ Results | ✓ |
| `fig:9` | ✓ Results | ✓ |

Figures 6a/6b are present and floated but use bold plain-text references instead of `\ref{fig:6a}` / `\ref{fig:6b}`. This is a **minor cross-reference formatting gap**, not a missing asset.

---

## 5. Table Integrity

| Check | Result |
|-------|--------|
| Table float files | **7** (`table_01`–`table_07`) |
| Duplicate table files | **0** |
| Broken `\input{tables/...}` paths | **0** |

### Table labels vs references

| Label | Floated | `\ref{}` in body |
|-------|---------|------------------|
| `tab:1` | ✓ Methodology | ✓ |
| `tab:2` | ✓ Methodology | ✓ |
| `tab:3` | ✓ Results | ✓ |
| `tab:4` | ✓ Results | ✓ |
| `tab:5` | ✓ Results | ✓ |
| `tab:6` | ✓ Results (architecture comparison) | — (not cited in source Markdown body) |
| `tab:7` | ✓ Results | ✓ |

Table 6 is included as a float but not referenced in prose — consistent with the frozen Markdown (architecture data appears in appendix tables; main text discusses S1–S4 without a "Table 6" callout).

Appendix contains **158** inline `\begin{tabular}` rows — matches **158** Markdown table data rows in source appendix.

---

## 6. Cross-Reference Integrity

| Metric | Value |
|--------|-------|
| Total `\label{}` commands | 143 |
| Unique labels | 142 → **143 after repair** |
| Total `\ref{}` / `\eqref{}` | 75 (12 unique targets) |
| Undefined `\ref{}` targets | **0** |
| Duplicate labels (pre-repair) | **1** — `subsection:hyperparameter_configuration` in Experimental Setup + Appendix |
| Duplicate labels (post-repair) | **0** |

**Repair applied:** Appendix hyperparameter subsection relabelled to `subsection:appendix_hyperparameter_configuration` (see §9).

Section cross-references use plain text `Section~N.N` (not `\ref{}`), matching the conversion design — no undefined section refs.

Equation references: display math blocks preserved from Markdown; no broken `\eqref{}` detected.

---

## 7. Compile Status

**Build command** (executed from `paper/latex/`):

```bash
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

| Check | Result |
|-------|--------|
| Exit code | **0** |
| Fatal LaTeX errors | **0** |
| Missing files | **0** |
| Undefined citations | **0** |
| Undefined references | **0** |
| Missing bibliography | **0** |
| Output | `main.pdf` — **41 pages**, 1,147,191 bytes |

### Warnings (non-fatal)

| Category | Count |
|----------|-------|
| Overfull `\hbox` | 41 |
| Underfull `\hbox` | 56 |
| Underfull `\vbox` | 2 |
| Float-only page | 1 ("Text page 30 contains only floats") |
| Multiply-defined labels | **0** (after repair + clean rebuild) |

Typographic warnings are expected for IEEE two-column layout with wide tables and equations. No package conflicts or duplicate `\usepackage` declarations detected.

### LaTeX quality checks

| Check | Result |
|-------|--------|
| `\documentclass[conference]{IEEEtran}` | ✓ |
| `IEEEtran.cls` matches template | ✓ MD5-identical |
| Bibliography style | ✓ `IEEEtran` |
| Packages | `cite`, `amsmath`, `amssymb`, `amsfonts`, `algorithmic`, `graphicx`, `textcomp`, `xcolor`, `booktabs`, `url` — no conflicts observed |
| Broken `\input{}` | **0** |

---

## 8. Duplication Scan

| Category | Result |
|----------|--------|
| Duplicated section content in `main.tex` | **None** |
| Duplicated figure PNGs (content hash) | **None** |
| Duplicated table files | **None** |
| Duplicated bibliography keys | **None** |
| Duplicated citation keys in `.bib` | **None** |
| Duplicated LaTeX labels | **1 found, repaired** |
| `assets/main.tex` vs `main.tex` | Intentional snapshot (not a manuscript duplicate) |

---

## 9. Files Repaired

| File | Issue | Repair |
|------|-------|--------|
| `sections/08_appendix.tex` | Duplicate `\label{subsection:hyperparameter_configuration}` conflicted with `sections/04_experimental_setup.tex` | Renamed appendix label to `subsection:appendix_hyperparameter_configuration` |

No other files modified. Scientific content, references, figures, and tables unchanged.

---

## 10. Remaining Manual Actions

| Priority | Action |
|----------|--------|
| **Required** | Replace placeholder `\author{}` block in `main.tex` (`Author Name(s)`, `email@institution.edu`) |
| Optional | Convert "Figure 6a" / "Figure 6b" plain-text citations to `\ref{fig:6a}` / `\ref{fig:6b}` for IEEE-style cross-linking |
| Optional | Add `\ref{tab:6}` callout if architecture table should be cited in Results prose |
| Optional | Tune overfull appendix `tabular` blocks for column width (formatting only) |
| Optional | Decide whether `manuscript/overleaf/` legacy figure directory should be archived now that `paper/latex/figures/` is canonical |

---

## 11. Consistency Check (`paper/sections/` ↔ `paper/latex/`)

Word-level Jaccard similarity (body text, citations stripped, tables normalised):

| Section pair | Jaccard |
|--------------|---------|
| Introduction | 0.9985 |
| Related Work | 0.9989 |
| Methodology | 0.9710 |
| Experimental Setup | 0.9754 |
| Results | 0.9963 |
| Discussion | 0.9984 |
| Conclusion | 0.9976 |
| Appendix | 0.4348* |

\*Appendix Jaccard is depressed by Markdown pipe-table syntax vs LaTeX `\begin{tabular}` markup. Row-level validation confirms **158/158** appendix table rows converted. Key frozen metrics (88.65 MW, 293.98 Dhaka MAE, 0.684 R², etc.) present in both sources.

Results numeric anchor check: **161/162** unique decimal tokens from Markdown appear in LaTeX (1 token `8.6` is a substring artefact of larger numbers like `88.65` — not a content omission).

**No scientific content differences detected.** Formatting differences (em-dash, `\cite{}`, math delimiters, `Section~8.1` vs `Section 8.1`) are expected and acceptable.

---

## Final Verdict

### 🟡 Verified with Minor Issues

The IEEE LaTeX conversion is **complete, compiles cleanly, and is publication-ready** pending author metadata. All manuscript sections, figures, tables, and 38/38 bibliography entries are present and consistent with the frozen Markdown source.

**Minor issues (non-blocking):**
1. Author placeholder in `main.tex` (pre-submission requirement)
2. Figures 6a/6b cited as plain text rather than `\ref{}` (assets present and floated)
3. Table 6 floated but not cited in body (consistent with source Markdown)
4. Typographic overfull/underfull box warnings (41/56) — normal for dense IEEE tables

**Integrity defect repaired during audit:**
- Duplicate hyperparameter subsection label (multiply-defined warning eliminated)

---

*Audit performed without re-running `build_from_markdown.py` or regenerating section content.*
