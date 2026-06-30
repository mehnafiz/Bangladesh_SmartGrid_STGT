# Table Index

**Revised:** 2026-06-30  
**Numbering authority:** `paper/paper_outline/Paper_Outline.md` Part III, `publication_tables.md`  
**Numeric source:** `paper/final_results_package/publication_tables.md` (frozen CSV/JSON transcription)  
**Manuscript mapping:** Table *n* appears in Section 6 or 8 per outline; §6 = `06_Methodology.md`

---

## Main-text tables

| ID | Title | Section | Source doc § | Frozen primary artefact | Supporting claim |
| --- | --- | --- | --- | --- | --- |
| **1** | Dataset Summary | §6.2 Methodology | §1 | `src/constants.py`, freeze inventory | N=9, T=7, splits, MD5 reproducibility |
| **2** | Training Configuration | §6.8 Methodology, §7.2 Exp. Setup | §2 | A6 `config.yaml`, Exp01B `best_configuration.md` | W20 protocol: λ₂=20, Adam, ES criterion |
| **3** | Benchmark Comparison | §8.1 Results | §3 | Exp02 `benchmark_results.csv` + A6 row | S2 88.65 MW; B07 93.31; RF 97.03 |
| **4** | Benchmark Statistical Significance | §8.2 Results | §4 | Exp02 `statistical_significance.md` | B07 vs baselines Wilcoxon; Bonferroni α=0.0083 |
| **5** | Ablation Study Results | §8.3 Results | §5 | Exp03 `ablation_results.csv` | A1–A6; A4=86.89; A6=S2=88.65 |
| **6** | Architecture Comparison (S1–S4) | §8.4 Results | §6 | Exp03B `simplification_results.csv` | S2 selected; S4 +21.32 MW vs S1 |
| **7** | Explainability Summary | §8.5 Results | §7 | Exp04 `xai_metrics.json` | SHAP rankings, ρ metrics, 52.2% agreement |

---

## Table placement by section

| Section | Tables | Count |
| --- | --- | ---: |
| §6 Methodology | 1, 2 | 2 |
| §7 Experimental Setup | 2 (cross-ref) | — |
| §8 Results | 3, 4, 5, 6, 7 | 5 |
| **Total main text** | | **7** |

---

## Key frozen values by table

### Table 3 — Benchmark (test set, demand MAE MW)

| ID | Model | MAE | Stress R² |
| --- | --- | ---: | ---: |
| **S2** | Correlation-Only PF-STGT | **88.65** | **0.745** |
| B07 | PF-STGT W20 hybrid (S1) | 93.31 | 0.585 |
| B02 | Random Forest | 97.03 | 0.555 |
| B06 | T-GCN | 257.21 | −0.304 |

### Table 5 — Ablation (demand MAE MW, ranked)

| ID | MAE | Notes |
| --- | ---: | --- |
| A4 | 86.89 | Single-task; demand-only bound |
| A6 (S2) | 88.65 | Best multi-task |
| A3 | 92.64 | No transformer |
| A1 (S1) | 93.31 | Reference |
| A5 | 97.98 | Geo-only (worst demand) |

### Table 6 — Architecture (ΔMAE vs S1)

| ID | MAE | ΔMAE | Stress R² |
| --- | ---: | ---: | ---: |
| S2 | 88.65 | **−4.66** | 0.745 |
| S3 | 92.64 | −0.66 | 0.701 |
| S1 | 93.31 | 0 | 0.585 |
| S4 | 114.63 | +21.32 | 0.747 |

### Table 7 — Explainability headline rows

| Metric | Value |
| --- | ---: |
| Top stress coalition | G8 (0.0191) |
| Top demand coalition (Dhaka) | G6 (162.34) |
| Attention–adjacency ρ | 0.422 |
| SHAP–permutation ρ (demand) | −0.564 |
| OSI driver agreement | 52.2% |

---

## LaTeX export targets

| Table | Overleaf file |
| --- | --- |
| 1 | `manuscript/overleaf/tables/table_01_dataset.tex` |
| 2 | `manuscript/overleaf/tables/table_02_training.tex` |
| 3 | `manuscript/overleaf/tables/table_03_benchmarks.tex` |
| 4 | `manuscript/overleaf/tables/table_04_benchmark_stats.tex` |
| 5 | `manuscript/overleaf/tables/table_05_ablations.tex` |
| 6 | `manuscript/overleaf/tables/table_06_architecture.tex` |
| 7 | `manuscript/overleaf/tables/table_07_explainability.tex` |

---

## Supplementary tables (optional)

| ID | Title | Frozen source |
| --- | --- | --- |
| S1 | Classical benchmark metric verification | Exp02A reports |
| S2 | Global grouped SHAP (full) | Exp04 SHAP CSVs |
| S3 | Permutation feature importance | Exp04 permutation exports |
| S4 | Case-study attribution summary | Exp04 `case_studies.md` |

---

## Table pairing with figures

| Results subsection | Table | Figure |
| --- | --- | --- |
| §8.1 Benchmarks | 3 | 4 |
| §8.2 Significance | 4 | — |
| §8.3 Ablations | 5 | 5 |
| §8.4 Architecture | 6 | — |
| §8.5 Explainability | 7 | 6a, 6b, 7, 8, 9 |

---

## Reporting notes

- Table 4 uses **B07 (S1)** as Wilcoxon reference; S2 vs S1 significance reported in Table 5/6 footnotes.
- Table 3 includes S2 row from Exp03 A6, not Exp02 checkpoint.
- Macro R² in Table 3: RF per-region R² (0.984) exceeds deep models — cite Exp02A when discussing metric choice.

---

## Existence verification

All 7 table definitions verified in `publication_tables.md` (2026-06-30).
