# Overleaf Upload Instructions

## Problem (fixed in `conference_overleaf.zip`)

The original `conference.zip` contained **symlink stubs** (49-byte text files) instead of real PNG images. Overleaf reported:

```
libpng: internal error — figure_07_node_importance.png
```

Undefined citations on the first compile are normal until BibTeX runs.

## Upload steps

1. Download **`paper/conference_overleaf.zip`** (not the old `conference.zip`).
2. In Overleaf: **New Project → Upload Project** → select the zip.
3. Ensure the project root contains `main.tex` directly (inside the `conference/` folder Overleaf creates, open that folder or move files to root if needed).
4. Menu → Compiler: **pdfLaTeX**
5. Menu → Bibliography: **BibTeX**
6. Click **Recompile** twice (LaTeX → BibTeX → LaTeX × 2).

## Required files (all included in zip)

```
main.tex
authors.tex
IEEEtran.cls
bibliography/12_References.bib
sections/*.tex
tables/*.tex
figures/figure_01_tikz.tex
figures/figure_02_tikz.tex
figures/ieee_fig_colors.tex
figures/figure_04_benchmark_comparison.pdf
figures/figure_05_ablation_comparison.pdf
figures/figure_07_node_importance.png   ← real 67 KB PNG, not symlink
```

## Rebuild zip locally

```bash
cd paper/conference
./build_overleaf_zip.sh
```

Output: `paper/conference_overleaf.zip`
