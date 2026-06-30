# Experiment Index

**Revised:** 2026-06-30 (final reference revision)  
**Status:** All experiments frozen (publication freeze 2026-06-25)  
**Purpose:** Traceability from experiment → manuscript section → assets  
**Section numbering:** Manuscript §6 = `06_Methodology.md`; §8 = `08_Results.md`, etc.

---

## Master traceability table

| Experiment | Used in Section(s) | Used in Subsection(s) | Purpose in Manuscript | Supporting Figures | Supporting Tables |
| --- | --- | --- | --- | --- | --- |
| **Foundation / Phases** | 6 | 6.2, 6.3, 6.4 | Dataset, features, splits, reproducibility | — | 1 |
| **Exp01** | 6, 7 | 6.5, 7.6 | Training stability context; W20 convergence diagnostic | 3 | — |
| **Exp01A** | 6, 9 | 6.7, 9.3 | Motivate OSI collapse and W20 loss repair | — | — |
| **Exp01B** | 6, 7, 9 | 6.7, 6.8, 7.2, 9.3 | Freeze W20 protocol; S1 reference checkpoint | 3 | 2 |
| **Exp02** | 7, 8, 9 | 7.3, 7.4, 7.5, 8.1, 8.2, 9.6 | Benchmark B01–B07 vs S1; statistical significance | 4 | 3, 4 |
| **Exp02A** | 7, 8, 9 | 7.3 (note), 8.1 (note), 9.6 | Macro vs pooled R² audit; MAE ranking confirmation | S2, S3 (supp.) | S1 (supp.) |
| **Exp03** | 6, 7, 8, 9 | 6.6, 7.5, 8.3, 9.1–9.3 | Ablation A1–A6; S2 checkpoint (A6) | 5 | 5 |
| **Exp03A** | 8, 9 | 8.3 (bullets), 9.1, 9.2, 9.4 | Interpret ablation surprises (attention, geo noise) | — | — |
| **Exp03B** | 6, 7, 8, 9 | 6.6, 7.5, 8.4, 9.1, 9.4 | S1–S4 simplification; **S2 selected** | — | 6 |
| **Exp04** | 6, 8, 9 | 6.3, 8.5, 9.5, 9.8 | XAI on frozen S2: SHAP, attention, case studies | 6a, 6b, 7, 8, 9 | 7 |
| **Architecture freeze** | 6, 8, 9 | 6.6, 8.4, 9.1 | Approve S2; document S1→S2 transition | 1, 2 | 2, 6 |
| **Publication freeze** | 8 | 8.1–8.5 | Asset lock for all Results tables/figures | 1–9 | 1–7 |

---

## Summary matrix (legacy quick view)

| Experiment | Methodology | Exp. Setup | Results | Discussion | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| Exp01 | §6.5 | §7.6 | — | — | Frozen |
| Exp01A | §6.7 | — | — | §9.3 | Frozen |
| Exp01B | §6.7, §6.8 | §7.2 | — | §9.3 | Frozen |
| Exp02 | §7.4 | §7.3, §7.5 | §8.1, §8.2 | §9.6 | Frozen |
| Exp02A | §7.3 note | — | §8.1 note | §9.6 | Frozen |
| Exp03 | §6.6 | §7.5 | §8.3 | §9.1–9.3 | Frozen |
| Exp03A | — | — | §8.3 bullets | §9.1, §9.2, §9.4 | Frozen |
| Exp03B | §6.6 | §7.5 | §8.4 | §9.1, §9.4 | Frozen |
| Exp04 | §6.3 | — | §8.5 | §9.5, §9.8 | Frozen |
| Arch. freeze | §6.6 | — | §8.4 | §9.1 | Approved |

---

## Experiment details

### Foundation / Phases (data pipeline)

| Field | Value |
| --- | --- |
| **Authority** | `src/constants.py`, Phase 04 splits, Phase 05B features |
| **Used in Section** | 6 (Methodology) |
| **Used in Subsection** | 6.2 Dataset; 6.3 Feature Engineering; 6.4 Graph Construction |
| **Purpose in Manuscript** | Define reproducible data protocol, MD5-locked artefacts, chronological splits |
| **Supporting Figures** | — |
| **Supporting Tables** | 1 (Dataset Summary) |

---

### Exp01 — Initial PF-STGT Training

| Field | Value |
| --- | --- |
| **Directory** | `experiments/experiment_01_pf_stgt/` |
| **Used in Section** | 6, 7 |
| **Used in Subsection** | 6.5 PF-STGT Architecture (context); 7.6 Training Diagnostics |
| **Purpose in Manuscript** | Document initial training stability; provide historical loss curves for W20 reference |
| **Supporting Figures** | 3 (Training Curves) |
| **Supporting Tables** | — |
| **Key outputs** | `metrics.json`, `train_loss.png`, `val_loss.png` |
| **Decision** | Superseded by Exp01B W20 for S1 reference |

---

### Exp01A — OSI Failure Investigation

| Field | Value |
| --- | --- |
| **Directory** | `experiments/experiment_01A_osi_failure_investigation/` |
| **Used in Section** | 6, 9 |
| **Used in Subsection** | 6.7 Multi-Task Learning (motivation); 9.3 Multi-Task Trade-offs |
| **Purpose in Manuscript** | Diagnose OSI prediction variance collapse; justify W20 stress-weight repair |
| **Supporting Figures** | — |
| **Supporting Tables** | — |
| **Key outputs** | `root_cause_report.md`, `loss_weight_analysis.md` |
| **Finding** | Task interference; default loss weights collapse OSI variance |

---

### Exp01B — Multitask Optimization Repair

| Field | Value |
| --- | --- |
| **Directory** | `experiments/experiment_01B_multitask_optimization_repair/` |
| **Used in Section** | 6, 7, 9 |
| **Used in Subsection** | 6.7, 6.8 Training Strategy; 7.2 Hyperparameters; 9.3 |
| **Purpose in Manuscript** | Freeze W20 protocol (λ₂=20); define S1/B07 reference checkpoint and training config |
| **Supporting Figures** | 3 |
| **Supporting Tables** | 2 (Training Configuration) |
| **Key outputs** | `best_configuration.md`, `checkpoints/W20/B07/seed_42/best.pt` |
| **S1 test metrics** | Demand MAE 93.31 MW; stress R² 0.585 |

---

### Exp02 — Benchmark Models

| Field | Value |
| --- | --- |
| **Directory** | `experiments/experiment_02_benchmark_models/` |
| **Used in Section** | 7, 8, 9 |
| **Used in Subsection** | 7.3 Evaluation Metrics; 7.4 Baselines; 7.5 Statistical Testing; 8.1, 8.2; 9.6 |
| **Purpose in Manuscript** | Compare B01–B07 on identical splits; Wilcoxon vs S1/B07 |
| **Supporting Figures** | 4 (includes S2 row from A6) |
| **Supporting Tables** | 3 (Benchmark Comparison), 4 (Statistical Significance) |
| **Key outputs** | `benchmark_results.csv`, `statistical_significance.md` |
| **Best deep model** | B07 (S1): 93.31 MW |
| **Best classical** | B02 (RF): 97.03 MW |

---

### Exp02A — Classical Benchmark Verification

| Field | Value |
| --- | --- |
| **Directory** | `experiments/experiment_02A_classical_benchmark_verification/` |
| **Used in Section** | 7, 8, 9 |
| **Used in Subsection** | 7.3 (footnote); 8.1 (footnote); 9.6 Comparison with Classical ML |
| **Purpose in Manuscript** | Resolve macro vs pooled R² discrepancy; confirm MAE rankings unchanged |
| **Supporting Figures** | S2, S3 (supplementary: actual vs predicted, residuals) |
| **Supporting Tables** | S1 (supplementary verification) |
| **Key outputs** | `aggregation_audit.md`, `benchmark_verification_report.md` |
| **Finding** | RF per-region R² inflated vs macro; MAE order preserved |

---

### Exp03 — Ablation Studies

| Field | Value |
| --- | --- |
| **Directory** | `experiments/experiment_03_ablation_studies/` |
| **Used in Section** | 6, 7, 8, 9 |
| **Used in Subsection** | 6.6 (context); 7.5; 8.3 Ablation Studies; 9.1–9.3 |
| **Purpose in Manuscript** | Quantify component effects A1–A6; host **S2 checkpoint (A6)** |
| **Supporting Figures** | 5 |
| **Supporting Tables** | 5 |
| **Key outputs** | `ablation_results.csv`, `statistical_significance.md` |
| **Final model row** | A6 = S2: 88.65 MW, stress R² 0.745 |

---

### Exp03A — Ablation Failure Investigation

| Field | Value |
| --- | --- |
| **Directory** | `experiments/experiment_03A_ablation_failure_investigation/` |
| **Used in Section** | 8, 9 |
| **Used in Subsection** | 8.3 (interpretive bullets); 9.1, 9.2, 9.4 |
| **Purpose in Manuscript** | Explain uniform attention on S1, geographical edge noise, correlation signal dominance |
| **Supporting Figures** | — |
| **Supporting Tables** | — |
| **Key outputs** | `task_interference_report.md`, `transformer_utilization_report.md` |
| **Findings** | Attention entropy ratio 0.998 on S1; geo edges noisy on Dhaka |

---

### Exp03B — Architecture Simplification

| Field | Value |
| --- | --- |
| **Directory** | `experiments/experiment_03B_architecture_simplification/` |
| **Used in Section** | 6, 7, 8, 9 |
| **Used in Subsection** | 6.6; 7.5; 8.4 Architecture Selection; 9.1, 9.4 |
| **Purpose in Manuscript** | Compare S1–S4; **adopt S2** as final model (−4.66 MW vs S1, p=5.5×10⁻⁵) |
| **Supporting Figures** | — |
| **Supporting Tables** | 6 |
| **Key outputs** | `simplification_results.csv`, `final_architecture_decision.md` |
| **Decision** | S2 selected; S4 demonstrates transformer requirement on corr graph |

---

### Exp04 — Explainability Analysis

| Field | Value |
| --- | --- |
| **Directory** | `experiments/experiment_04_explainability_analysis/` |
| **Used in Section** | 6, 8, 9 |
| **Used in Subsection** | 6.3 Feature Engineering (coalitions G1–G11); 8.5 Explainability; 9.5, 9.8 Limitations |
| **Purpose in Manuscript** | SHAP, permutation, attention, and case-study attribution on frozen S2 |
| **Supporting Figures** | 6a, 6b, 7, 8, 9 |
| **Supporting Tables** | 7 |
| **Key outputs** | `xai_metrics.json`, `xai_summary.md`, 8 figure files |
| **Case studies** | n = 24 dates; OSI driver agreement 52.2% |

---

### Architecture freeze

| Field | Value |
| --- | --- |
| **Authority** | `experiments/architecture_freeze_revision/Final_Architecture_Decision.md` |
| **Used in Section** | 6, 8, 9 |
| **Used in Subsection** | 6.6 Final S2 Architecture; 8.4; 9.1 Why S2 Outperforms S1 |
| **Purpose in Manuscript** | Document approved S2; S1→S2 rationale; I/O and training contract |
| **Supporting Figures** | 1 (Framework), 2 (S2 Architecture) |
| **Supporting Tables** | 2, 6 |
| **Decision** | S2 approved 2026-06-25 |

---

### Publication freeze

| Field | Value |
| --- | --- |
| **Authority** | `paper/publication_freeze/Publication_Asset_Freeze.md` |
| **Used in Section** | 8 (all Results subsections) |
| **Used in Subsection** | 8.1–8.5 |
| **Purpose in Manuscript** | Lock all Results tables and figures; prohibit regeneration during writing |
| **Supporting Figures** | 1–9 |
| **Supporting Tables** | 1–7 |
| **Freeze date** | 2026-06-25 |

---

## Narrative dependency chain

```
Foundation (data, features, splits)
    ↓
Exp01 → Exp01A → Exp01B (W20 protocol, S1 checkpoint)
    ↓
Exp02 (+02A) — benchmarks and metric audit
    ↓
Exp03 (+03A) — ablations and interpretation
    ↓
Exp03B — S2 selection
    ↓
Exp04 — explainability on S2
    ↓
Architecture freeze + Publication freeze
```

---

## Primary numeric artefacts (do not edit)

| Experiment | Authoritative file |
| --- | --- |
| 01 | `experiment_01_pf_stgt/metrics.json` |
| 01B | `experiment_01B_multitask_optimization_repair/results.json` |
| 02 | `experiment_02_benchmark_models/benchmark_results.csv` |
| 03 | `experiment_03_ablation_studies/ablation_results.csv` |
| 03B | `experiment_03B_architecture_simplification/simplification_results.csv` |
| 04 | `experiment_04_explainability_analysis/xai_metrics.json` |

---

## Research question mapping

| RQ | Primary experiments |
| --- | --- |
| RQ1 | Exp02, 02A, 03, 03B |
| RQ2 | Exp03, 03A, 03B |
| RQ3 | Exp03, 03A, 03B, 04 |
| RQ4 | Exp01A, 01B, 03 |
| RQ5 | Exp04 |
