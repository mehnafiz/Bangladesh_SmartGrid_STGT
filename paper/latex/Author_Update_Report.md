# Author Update Report

**Date:** 2026-07-05  
**Manuscript:** `paper/latex/main.tex`  
**Scope:** Author information and Acknowledgment section only (no scientific content modified)

---

## 1. Author Information Updated

The placeholder author block in `main.tex` was replaced with six IEEE-compliant `\IEEEauthorblockN` / `\IEEEauthorblockA` entries, separated by `\and`, in the specified order:

| Order | Name | Email |
|------:|------|-------|
| 1 | MD. Nafiz Ahmed Tanim | 24-56644-1@student.aiub.edu |
| 2 | MD. Tanvir Hasan | 23-54796-3@student.aiub.edu |
| 3 | MD. Robiul Islam | 24-56643-1@student.aiub.edu |
| 4 | Wasimul Bari Tonmoy | 24-56653-1@student.aiub.edu |
| 5 | MD. Hasanuzzaman | 24-56666-1@student.aiub.edu |
| 6 | Dipta Justin Gomes | diptagomes@aiub.edu |

**Shared affiliation (all authors):**
- Department of Computer Science & Engineering
- American International University-Bangladesh (AIUB)
- Dhaka, Bangladesh

No "Supervisor:" label was used in the author list.

---

## 2. Acknowledgment Section Added

A new file `paper/latex/sections/09_acknowledgment.tex` was created with an unnumbered IEEE-style section:

```latex
\section*{Acknowledgment}
```

**Placement:** Immediately after `\input{sections/07_conclusion}` and before `\appendices` / the bibliography — i.e., after Conclusion and before References, per IEEE conference convention.

**Content:** Formal acknowledgment of Dipta Justin Gomes for guidance, supervision, suggestions, and feedback. No funding or conflict-of-interest statements were added.

---

## 3. Formatting Adjustments

| Item | Action |
|------|--------|
| Author block structure | Standard IEEE `\and`-separated six-author layout; no custom spacing or font changes |
| Department ampersand | Escaped as `\&` in LaTeX |
| Acknowledgment heading | IEEE-preferred spelling: "Acknowledgment" (no *e* after *g*) |
| Page count | Unchanged at **41 pages** |
| Bibliography / appendix order | Preserved (Acknowledgment → Appendix → References) |

No additional formatting patches were required. The build log reported no overfull boxes in the author block.

---

## 4. Compile Status

| Step | Result |
|------|--------|
| `pdflatex main.tex` | ✅ Success (exit code 0) |
| `bibtex main` | ✅ Success |
| `pdflatex` × 2 (cross-ref pass) | ✅ Success |
| Output | `paper/latex/main.pdf` — 41 pages, ~1.55 MB |
| Errors | None |
| Warnings | Standard underfull hbox/vbox warnings in body text only (pre-existing pattern); no new layout errors |

---

## 5. First-Page Layout Verification

From `main.log`:

- **Page 1** contains the title, six-author block, abstract, IEEE keywords, and the opening of Section I (Introduction).
- No overfull hbox or vbox warnings were emitted during `\maketitle` or the author block.
- Author names and affiliations compiled without line-break failures.
- The long paper title plus six full affiliation blocks fit within the IEEE two-column header area without manual intervention.

---

## 6. Remaining Manual Verification

| Check | Status |
|-------|--------|
| Visual review of author name alignment in PDF viewer | Recommended — confirm three-column author grid appearance on page 1 |
| Confirm acknowledgment text on page 37 (after Conclusion, before Appendix) | Verified via compile log `[37]` marker for `09_acknowledgment.tex` |
| Conference submission author-order / corresponding-author policy | Confirm with target venue if a designated corresponding author is required |

---

## Files Modified

- `paper/latex/main.tex` — author block + acknowledgment `\input`
- `paper/latex/sections/09_acknowledgment.tex` — **new**
- `paper/latex/main.pdf` — regenerated

## Files Not Modified

Title, abstract, all section `.tex` files (except new acknowledgment), figures, tables, equations, citations, and bibliography were left unchanged.

---

## Status

🟢 **Author Information Updated Successfully**
