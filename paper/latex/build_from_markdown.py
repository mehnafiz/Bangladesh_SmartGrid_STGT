#!/usr/bin/env python3
"""Convert paper/sections/*.md to paper/latex/ IEEE conference format."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SECTIONS = ROOT / "paper" / "sections"
TEMPLATE = ROOT / "paper" / "template" / "IEEE-conference-template-062824"
LATEX = ROOT / "paper" / "latex"
FIG_SRC = ROOT / "paper" / "final_results_package" / "figures"

SECTION_MAP = [
    ("04_Introduction.md", "sections/01_introduction.tex", "Introduction"),
    ("05_Related_Work.md", "sections/02_related_work.tex", "Related Work"),
    ("06_Methodology.md", "sections/03_methodology.tex", "Methodology"),
    ("07_Experimental_Setup.md", "sections/04_experimental_setup.tex", "Experimental Setup"),
    ("08_Results.md", "sections/05_results.tex", "Results"),
    ("09_Discussion.md", "sections/06_discussion.tex", "Discussion"),
    ("10_Conclusion.md", "sections/07_conclusion.tex", "Conclusion"),
    ("11_Appendix_A_Supplementary_Materials.md", "sections/08_appendix.tex", "Supplementary Materials"),
]

UNICODE_MAP = {
    "\u2014": "---",
    "\u2013": "--",
    "\u2212": "-",
    "\u00d7": "$\\times$",
    "\u03b1": "$\\alpha$",
    "\u03b2": "$\\beta$",
    "\u03c1": "$\\rho$",
    "\u03c6": "$\\phi$",
    "\u03bb": "$\\lambda$",
    "\u03b7": "$\\eta$",
    "\u03b5": "$\\varepsilon$",
    "\u03c3": "$\\sigma$",
    "\u03c4": "$\\tau$",
    "\u2299": "$\\odot$",
    "\u00b7": "$\\cdot$",
    "\u0394": "$\\Delta$",
    "\u2264": "$\\leq$",
    "\u2265": "$\\geq$",
    "\u2248": "$\\approx$",
    "\u00b1": "$\\pm$",
}

FIGURE_DEFS = {
    1: ("figure_01_framework.png", "fig:1",
        "End-to-end PF-STGT multi-task forecasting framework."),
    2: ("figure_02_s2_architecture.png", "fig:2",
        "Architecture freeze: S2 correlation-only graph PF-STGT."),
    3: ("figure_03_training_curves.png", "fig:3",
        "Training and validation loss curves (W20 protocol reference)."),
    4: ("figure_04_benchmark_comparison.png", "fig:4",
        "Test-set macro demand MAE benchmark comparison."),
    5: ("figure_05_ablation_comparison.png", "fig:5",
        "Ablation study demand MAE on the test set."),
    6: ("figure_06_shap_summary_stress.png", "fig:6a",
        "Grouped SHAP attributions for stress (global)."),
    "6b": ("figure_06_shap_summary_demand.png", "fig:6b",
           "Grouped SHAP attributions for Dhaka demand."),
    7: ("figure_07_node_importance.png", "fig:7",
        "Node-level attribution heatmap."),
    8: ("figure_08_temporal_attribution.png", "fig:8",
        "Temporal attention weights across the lookback window."),
    9: ("figure_09_stress_attribution.png", "fig:9",
        "Dual-path stress attribution vs.\\ OSI component drivers."),
}

SECTION_ASSETS = {
    "sections/03_methodology.tex": [
        "tables/table_01_dataset.tex",
        "tables/table_02_training.tex",
        "figures/figure_01.tex",
        "figures/figure_02.tex",
    ],
    "sections/04_experimental_setup.tex": ["figures/figure_03.tex"],
    "sections/05_results.tex": [
        "tables/table_03_benchmark.tex",
        "tables/table_04_benchmark_stats.tex",
        "tables/table_05_ablation.tex",
        "tables/table_06_architecture.tex",
        "tables/table_07_explainability.tex",
        "figures/figure_04.tex",
        "figures/figure_05.tex",
        "figures/figure_06a.tex",
        "figures/figure_06b.tex",
        "figures/figure_07.tex",
        "figures/figure_08.tex",
        "figures/figure_09.tex",
    ],
}


def setup_dirs():
    for d in ["sections", "figures", "tables", "bibliography", "assets"]:
        (LATEX / d).mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEMPLATE / "IEEEtran.cls", LATEX / "IEEEtran.cls")
    shutil.copy2(SECTIONS / "12_References.bib", LATEX / "bibliography" / "12_References.bib")
    for png in FIG_SRC.glob("*.png"):
        shutil.copy2(png, LATEX / "figures" / png.name)


def unicode_fix(text: str) -> str:
    for k, v in UNICODE_MAP.items():
        text = text.replace(k, v)
    return text


SUPERSCRIPT_DIGITS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
SUBSCRIPT_DIGITS = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def normalize_scientific(text: str) -> str:
    def sci_coeff(m):
        exp = m.group(2).translate(SUPERSCRIPT_DIGITS)
        return f"${m.group(1)} \\times 10^{{-{exp}}}$"

    text = re.sub(
        r"(\d+(?:\.\d+)?)\s*×\s*10⁻([⁰¹²³⁴⁵⁶⁷⁸⁹]+)",
        sci_coeff,
        text,
    )
    text = re.sub(
        r"(\d+(?:\.\d+)?)\s*×\s*10\^?\{-?(\d+)\}",
        r"$\1 \\times 10^{-\2}$",
        text,
    )

    def sci_exp_only(m):
        exp = m.group(1).translate(SUPERSCRIPT_DIGITS)
        return f"$10^{{-{exp}}}$"

    text = re.sub(r"10⁻([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", sci_exp_only, text)
    text = re.sub(r"λ₂", r"$\\lambda_2$", text)
    text = re.sub(r"R²", r"$R^2$", text)
    text = re.sub(r"Δ", r"$\\Delta$", text)
    return repair_broken_math(text)


def repair_broken_math(text: str) -> str:
    """Fix partial unicode-to-LaTeX conversions from earlier runs."""
    text = re.sub(r"\$\\lambda\$\$_2\$", r"$\\lambda_2$", text)
    text = re.sub(r"\$\\lambda\$\$_\{2\}\$", r"$\\lambda_2$", text)

    def fix_sci(m):
        base = m.group(1)
        digits = "".join(re.findall(r"\^(\d+)", m.group(0)))
        return f"${base} \\times 10^{{-{digits}}}$"

    text = re.sub(
        r"(\d+(?:\.\d+)?)\$\\times\$10\$\{\-\}\$(?:\$?\^(\d+)\$)+",
        fix_sci,
        text,
    )

    def fix_exp10(m):
        digits = "".join(re.findall(r"\^(\d+)", m.group(0)))
        return f"$10^{{-{digits}}}$"

    text = re.sub(r"10\$\{\-\}\$(?:\$?\^(\d+)\$)+", fix_exp10, text)
    return text


def escape_latex_text(text: str) -> str:
    """Escape LaTeX specials in non-math segments."""
    text = normalize_scientific(text)
    text = unicode_fix(text)
    pattern = (
        r"(\\cite\{[^}]+\}|\\textbf\{[^}]+\}|\\textit\{[^}]+\}|\\texttt\{[^}]+\}|"
        r"\$[^$]+\$|\\\((?:[^\\]|\\.)*?\\\)|\\\[.*?\\\])"
    )
    parts = re.split(pattern, text, flags=re.DOTALL)
    out = []
    for i, part in enumerate(parts):
        if not part:
            continue
        if i % 2 == 1:
            out.append(part)
            continue
        part = part.replace("&", "\\&")
        part = part.replace("%", "\\%")
        part = part.replace("#", "\\#")
        part = part.replace("_", "\\_")
        out.append(part)
    return "".join(out)


def escape_pct_in_text_commands(text: str) -> str:
    def repl(m):
        inner = m.group(2).replace("%", "\\%")
        return f"\\{m.group(1)}{{{inner}}}"
    return re.sub(r"\\(textbf|textit|texttt)\{([^}]*)\}", repl, text)


def convert_inline(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\textit{\1}", text)

    def tt_repl(m):
        inner = m.group(1).replace("_", "\\_").replace("%", "\\%")
        return f"\\texttt{{{inner}}}"

    text = re.sub(r"`([^`]+)`", tt_repl, text)
    text = escape_pct_in_text_commands(text)
    # Table/Figure refs
    text = re.sub(r"\\textbf\{Table (\d+)\}", r"Table~\\ref{tab:\1}", text)
    text = re.sub(r"\\textbf\{Figure (\d+)\}", r"Fig.~\\ref{fig:\1}", text)
    text = re.sub(r"\bTable (\d+)\b", r"Table~\\ref{tab:\1}", text)
    text = re.sub(r"\bFigure (\d+)\b", r"Fig.~\\ref{fig:\1}", text)
    text = re.sub(r"Table~\\ref\{tab:S(\d+)\}", r"Table~S\\ref{tab:s\1}", text)
    text = re.sub(r"Section (\d+(?:\.\d+)*)", r"Section~\1", text)
    return escape_latex_text(text)


def escape_title_text(text: str) -> str:
    parts = re.split(r"(\$[^$]+\$)", text)
    out = []
    for i, part in enumerate(parts):
        if not part:
            continue
        if i % 2 == 1:
            out.append(part)
        else:
            out.append(part.replace("_", r"\_"))
    return "".join(out)


def parse_header(line: str) -> tuple[int, str] | None:
    m = re.match(r"^(#{1,3})\s+(.*)$", line.strip())
    if not m:
        return None
    level = len(m.group(1))
    title = re.sub(
        r"^(?:Appendix\s+[A-Z]\.\s*|A\.\d+(?:\.\d+)*\s+|\d+(?:\.\d+)*\s+)",
        "",
        m.group(2),
    ).strip()
    title = title.replace(" — ", " --- ")
    title = normalize_scientific(title)
    title = escape_title_text(title)
    return level, title


def convert_table_block(lines: list[str]) -> str:
    rows = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        if re.match(r"^\|[-:\s|]+\|$", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    if not rows:
        return ""
    ncol = len(rows[0])
    colspec = "|" + "l|" * ncol
    body = []
    for i, row in enumerate(rows):
        row = row + [""] * (ncol - len(row))
        cells = []
        for c in row[:ncol]:
            cells.append(convert_inline(c))
        if i == 0:
            body.append("\\hline")
            body.append(" & ".join(cells) + " \\\\")
            body.append("\\hline")
        else:
            body.append(" & ".join(cells) + " \\\\")
    body.append("\\hline")
    return "\\begin{tabular}{" + colspec + "}\n" + "\n".join(body) + "\n\\end{tabular}\n"


def convert_markdown(content: str, section_title: str | None) -> str:
    lines = content.splitlines()
    out: list[str] = []
    i = 0
    skip_first_h1 = bool(section_title)
    if section_title:
        label = re.sub(r"[^a-z0-9]+", "_", section_title.lower()).strip("_")
        out.append(f"\\section{{{section_title}}}\\label{{sec:{label}}}")
    in_table = False
    table_lines: list[str] = []

    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("|"):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            i += 1
            continue
        if in_table:
            out.append(convert_table_block(table_lines))
            in_table = False
            table_lines = []

        if line.strip() == "---":
            i += 1
            continue

        hdr = parse_header(line)
        if hdr:
            level, title = hdr
            if skip_first_h1 and level == 1:
                skip_first_h1 = False
                i += 1
                continue
            cmd = {1: "section", 2: "subsection", 3: "subsubsection"}[min(level, 3)]
            slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
            out.append(f"\\{cmd}{{{title}}}\\label{{{cmd}:{slug}}}")
            i += 1
            continue

        if line.strip().startswith("#"):
            i += 1
            continue

        if not line.strip():
            out.append("")
            i += 1
            continue

        # display math block
        if line.strip().startswith("\\["):
            block = [line]
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("\\]"):
                block.append(lines[i])
                i += 1
            if i < len(lines):
                block.append(lines[i])
            out.extend(block)
            i += 1
            continue

        out.append(convert_inline(line))
        i += 1

    if in_table:
        out.append(convert_table_block(table_lines))

    return "\n".join(out) + "\n"


def write_figure_snippets():
    for key, (fname, label, caption) in FIGURE_DEFS.items():
        num = key if isinstance(key, str) else f"{key:02d}"
        name = f"figure_{num}.tex" if key != "6b" else "figure_06b.tex"
        if key == 6:
            name = "figure_06a.tex"
        fig_label = label.replace("fig:", "")
        content = f"""\\begin{{figure}}[!t]
\\centering
\\includegraphics[width=\\linewidth]{{figures/{fname}}}
\\caption{{{caption}}}
\\label{{{label}}}
\\end{{figure}}
"""
        (LATEX / "figures" / name).write_text(content)


def write_tables():
    (LATEX / "tables" / "table_01_dataset.tex").write_text(r"""\begin{table}[!t]
\caption{Dataset summary.}
\label{tab:1}
\centering
\small
\begin{tabular}{|l|l|}
\hline
\textbf{Property} & \textbf{Value} \\
\hline
Domain & Bangladesh national power grid (9 divisions) \\
Input window ($T$) & 7 days \\
Forecast horizon & 1 day \\
Node features & 9 \\
Global features & 17 \\
Train windows & 1,281 \\
Validation windows & 263 \\
Test windows & 264 \\
\hline
\end{tabular}
\end{table}
""")

    (LATEX / "tables" / "table_02_training.tex").write_text(r"""\begin{table}[!t]
\caption{Frozen training configuration (S2 / A6).}
\label{tab:2}
\centering
\small
\begin{tabular}{|l|l|}
\hline
\textbf{Setting} & \textbf{Value} \\
\hline
Loss & $\mathcal{L} = \mathrm{Huber(demand)}/100 + \lambda_2 \cdot \mathrm{MSE(OSI)}$ \\
$\lambda_2$ & 20.0 \\
Optimiser & Adam, lr $= 5\times 10^{-4}$, wd $= 10^{-4}$ \\
Batch size & 32 \\
Early stopping & Patience 15 (composite val.\ score) \\
Parameters & 749,058 \\
\hline
\end{tabular}
\end{table}
""")

    (LATEX / "tables" / "table_03_benchmark.tex").write_text(r"""\begin{table}[!t]
\caption{Benchmark comparison (test set).}
\label{tab:3}
\centering
\scriptsize
\begin{tabular}{|l|l|r|r|r|r|r|r|}
\hline
\textbf{ID} & \textbf{Model} & \textbf{MAE} & \textbf{RMSE} & \textbf{MAPE} & \textbf{$R^2$} & \textbf{OSI MAE} & \textbf{OSI $R^2$} \\
\hline
S2 & Corr.-Only PF-STGT & 88.65 & 127.29 & 6.55 & 0.684 & 0.0371 & 0.745 \\
B07 & PF-STGT W20 hybrid & 93.31 & 128.81 & 6.76 & 0.674 & 0.0499 & 0.585 \\
B02 & Random Forest & 97.03 & 156.99 & 7.04 & 0.984 & 0.0481 & 0.555 \\
B03 & XGBoost & 109.73 & 178.53 & 7.99 & 0.979 & 0.0497 & 0.525 \\
B06 & T-GCN & 257.21 & 301.06 & 15.72 & $-$0.483 & 0.0891 & $-$0.304 \\
\hline
\end{tabular}
\end{table}
""")

    (LATEX / "tables" / "table_04_benchmark_stats.tex").write_text(r"""\begin{table}[!t]
\caption{Benchmark Wilcoxon tests (demand MAE; ref.\ B07).}
\label{tab:4}
\centering
\scriptsize
\begin{tabular}{|l|r|r|r|}
\hline
\textbf{Comparison} & \textbf{Median $\Delta$MAE} & \textbf{$p$ (two-sided)} & \textbf{Bonferroni sig.} \\
\hline
B07 vs B01 & $-$58.98 & $1.72\times 10^{-31}$ & Yes \\
B07 vs B02 & $-$4.92 & 0.00135 & Yes \\
B07 vs B06 & $-$160.66 & $1.48\times 10^{-40}$ & Yes \\
\hline
\end{tabular}
\end{table}
""")

    (LATEX / "tables" / "table_05_ablation.tex").write_text(r"""\begin{table}[!t]
\caption{Ablation study results (test set).}
\label{tab:5}
\centering
\scriptsize
\begin{tabular}{|l|l|r|r|r|r|}
\hline
\textbf{ID} & \textbf{Variant} & \textbf{MAE} & \textbf{$R^2$} & \textbf{OSI MAE} & \textbf{OSI $R^2$} \\
\hline
A4 & Single-Task & 86.89 & 0.731 & -- & -- \\
A6 (S2) & Corr.\ Graph & 88.65 & 0.684 & 0.0371 & 0.745 \\
A1 & PF-STGT W20 & 93.31 & 0.674 & 0.0499 & 0.585 \\
A5 & Geo Graph & 97.98 & 0.554 & 0.0340 & 0.764 \\
\hline
\end{tabular}
\end{table}
""")

    (LATEX / "tables" / "table_06_architecture.tex").write_text(r"""\begin{table}[!t]
\caption{Architecture comparison (S1--S4).}
\label{tab:6}
\centering
\scriptsize
\begin{tabular}{|l|l|r|r|r|}
\hline
\textbf{ID} & \textbf{Model} & \textbf{MAE} & \textbf{$R^2$} & \textbf{OSI $R^2$} \\
\hline
S2 & Corr.-Only PF-STGT & 88.65 & 0.684 & 0.745 \\
S3 & No-Transformer & 92.64 & 0.671 & 0.701 \\
S1 & PF-STGT W20 & 93.31 & 0.674 & 0.585 \\
S4 & Corr.\ + No-Trans. & 114.63 & 0.362 & 0.747 \\
\hline
\end{tabular}
\end{table}
""")

    (LATEX / "tables" / "table_07_explainability.tex").write_text(r"""\begin{table}[!t]
\caption{Explainability summary (S2).}
\label{tab:7}
\centering
\small
\begin{tabular}{|l|r|}
\hline
\textbf{Metric} & \textbf{Value} \\
\hline
Top stress coalition (G8 $|\phi|$) & 0.0191 \\
Top Dhaka demand coalition (G6 $|\phi|$) & 162.34 \\
Attention--adjacency Spearman $\rho$ & 0.422 \\
SHAP--permutation $\rho$ (demand) & $-$0.564 \\
OSI driver agreement (cases) & 52.2\% \\
\hline
\end{tabular}
\end{table}
""")


def write_main(title: str, abstract: str, keywords: str):
    kw = keywords.replace(";", ",")
    main = rf"""\documentclass[conference]{{IEEEtran}}
\IEEEoverridecommandlockouts
\usepackage{{cite}}
\usepackage{{amsmath,amssymb,amsfonts}}
\usepackage{{algorithmic}}
\usepackage{{graphicx}}
\usepackage{{textcomp}}
\usepackage{{xcolor}}
\usepackage{{booktabs}}
\usepackage{{url}}
\def\BibTeX{{\rm B\kern-.05em{{\sc i\kern-.025em b}}\kern-.08em
    T\kern-.1667em\lower.7ex\hbox{{E}}\kern-.125emX}}

\begin{{document}}

\title{{{title}}}

\author{{
\IEEEauthorblockN{{Author Name(s)}}
\IEEEauthorblockA{{\textit{{Department, Institution}}\\
City, Country \\
email@institution.edu}}
}}

\maketitle

\begin{{abstract}}
{convert_inline(abstract.strip())}
\end{{abstract}}

\begin{{IEEEkeywords}}
{kw}
\end{{IEEEkeywords}}

\input{{sections/01_introduction}}
\input{{sections/02_related_work}}
\input{{sections/03_methodology}}
\input{{sections/04_experimental_setup}}
\input{{sections/05_results}}
\input{{sections/06_discussion}}
\input{{sections/07_conclusion}}

\appendices
\input{{sections/08_appendix}}

\bibliographystyle{{IEEEtran}}
\bibliography{{bibliography/12_References}}

\end{{document}}
"""
    (LATEX / "main.tex").write_text(main)


def append_assets(rel_path: str, tex: str) -> str:
    assets = SECTION_ASSETS.get(rel_path, [])
    if assets:
        tex += "\n\n% --- Section floats (publication package) ---\n"
        for a in assets:
            tex += f"\\input{{{a}}}\n"
    return tex


def main():
    setup_dirs()
    write_figure_snippets()
    write_tables()

    title_lines = (SECTIONS / "01_Title.md").read_text().splitlines()
    title = title_lines[-1].strip() if title_lines else "Manuscript Title"
    abstract = "\n".join((SECTIONS / "02_Abstract.md").read_text().splitlines()[2:])
    keywords = (SECTIONS / "03_Keywords.md").read_text().splitlines()[-1].strip()

    for md_name, tex_rel, sec_title in SECTION_MAP:
        raw = (SECTIONS / md_name).read_text()
        tex = convert_markdown(raw, sec_title)
        tex = append_assets(tex_rel, tex)
        (LATEX / tex_rel).write_text(tex)
        print("Converted", md_name, "->", tex_rel)

    write_main(title, abstract, keywords)
    shutil.copy2(LATEX / "main.tex", LATEX / "assets" / "main.tex")
    print("Done. Output:", LATEX)


if __name__ == "__main__":
    main()
