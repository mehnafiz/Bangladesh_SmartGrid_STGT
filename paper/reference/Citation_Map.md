# Citation Map

**Revised:** 2026-06-30  
**Purpose:** Map manuscript sections to required literature domains and citation placement  
**Manuscript files:** §4 = `04_Introduction.md`; §5 = `05_Related_Work.md`; §6 = `06_Methodology.md`  
**Note:** This document lists **citation needs** only — no `.bib` entries generated here. Add references to `manuscript/overleaf/bibliography/` during drafting.

---

## Citation coverage by section

| Section | File | Literature domains required | Priority |
| --- | --- | --- | ---: |
| §4 Introduction | `04_Introduction.md` | Bangladesh grid context; load forecasting; smart grids; research gap | High |
| §5 Related Work | `05_Related_Work.md` | All domains below (primary citation section) | **Critical** |
| §6 Methodology | `06_Methodology.md` | GNNs; graph transformers; multi-task learning; Huber loss | High |
| §7 Experimental Setup | `07_Experimental_Setup.md` | Wilcoxon test; Bonferroni correction; bootstrap CIs | Medium |
| §8 Results | `08_Results.md` | Baseline method citations (RF, XGB, LSTM, T-GCN) | Medium |
| §9 Discussion | `09_Discussion.md` | Compare findings to prior GNN/transformer forecasting work | High |
| §10 Conclusion | `10_Conclusion.md` | Minimal new citations | Low |

---

## Literature domain catalogue

### D1 — Load and demand forecasting

| Topics to cite | Manuscript use |
| --- | --- |
| Classical statistical forecasting (ARIMA, regression) | Related Work §5.1; B01 baseline context |
| ML load forecasting (RF, boosting) | Related Work §5.1; B02/B03 baselines |
| Regional/national grid forecasting | Introduction §4.1; Bangladesh context |
| Developing-economy power systems | Introduction motivation |

**Suggested placement:** §5.1, §8.1 (when introducing B01–B03)

---

### D2 — Graph neural networks for power systems

| Topics to cite | Manuscript use |
| --- | --- |
| GCN / spatio-temporal GNN for load | Related Work §5.2; B06 T-GCN baseline |
| Geographic graph construction | Contrast with S2 correlation-only approach |
| Data-driven / correlation graphs | Methods §6.4; Contribution C2 |
| T-GCN and temporal GNN variants | Benchmark discussion §8.1, §9.6 |

**Suggested placement:** §5.2, §6.4, §9.2

---

### D3 — Transformer-based forecasting

| Topics to cite | Manuscript use |
| --- | --- |
| Temporal transformers for sequences | Related Work §5.3; PF-STGT temporal branch |
| Graph transformers / attention with adjacency bias | Methods §6.5–6.6 |
| Parallel-fusion architectures | Figure 1 framework positioning |

**Suggested placement:** §5.3, §6.5

---

### D4 — Multi-task learning

| Topics to cite | Manuscript use |
| --- | --- |
| Shared representations for related tasks | Related Work §5.4 |
| Task interference and loss balancing | §6.7 W20 motivation; §9.3 Exp01A |
| Multi-output energy forecasting | Position dual demand + stress task |

**Suggested placement:** §5.4, §6.7, §9.3

---

### D5 — Explainable AI (XAI)

| Topics to cite | Manuscript use |
| --- | --- |
| SHAP / integrated gradients | Methods explainability; §8.5 |
| Permutation feature importance | Table 7 cross-method validation |
| XAI for time-series and graph models | Related Work §5.5 |
| Operator-facing attribution | Discussion §9.5 |

**Suggested placement:** §5.5, §8.5, §9.5

---

### D6 — Bangladesh energy and grid context

| Topics to cite | Manuscript use |
| --- | --- |
| Bangladesh power sector structure | Introduction §4.1 |
| Grid operations / regional divisions | Dataset Table 1 context |
| Energy policy / smart grid initiatives | Introduction background |

**Suggested placement:** §4.1 (minimum 2–3 authoritative sources)

---

### D7 — Statistical methodology

| Topics to cite | Manuscript use |
| --- | --- |
| Wilcoxon signed-rank test | §7.5, Table 4 |
| Multiple comparison correction (Bonferroni) | §7.5, Tables 4–5 |
| Bootstrap confidence intervals | §7.5, statistical_summary |
| Effect sizes (Cohen's d) | Table 4 reporting |

**Suggested placement:** §7.5 (brief); optional footnote in §8.2

---

## Baseline method citations (Results §8.1)

| Model ID | Citation need |
| --- | --- |
| B01 Linear Regression | Standard ML textbook or sklearn reference |
| B02 Random Forest | Breiman (2001) or equivalent |
| B03 XGBoost | Chen & Guestrin (2016) or equivalent |
| B04 LSTM | Hochreiter & Schmidhuber (1997) or LSTM forecasting survey |
| B05 GRU | Cho et al. (2014) or equivalent |
| B06 T-GCN | Original T-GCN / spatio-temporal GNN paper |
| B07/S1 PF-STGT | This work (no external citation) |
| S2 | This work (proposed) |

---

## Project-internal references (no external citation)

| Item | How to reference |
| --- | --- |
| S2 architecture | This paper; `Final_Architecture_Decision.md` |
| W20 protocol | This paper; Exp01B |
| Dataset MD5 | This paper Table 1 |
| Frozen experiment results | This paper Tables 3–7 |

---

## Citation map by research question

| RQ | Domains |
| --- | --- |
| RQ1 | D1, D2, D3, D7 |
| RQ2 | D2, D3 |
| RQ3 | D2 (geo vs corr graphs) |
| RQ4 | D4 |
| RQ5 | D5 |

---

## Citation map by contribution

| Contribution | Domains |
| --- | --- |
| C1 | D1, D2, D3, D4 |
| C2 | D2 (graph construction literature) |
| C3 | D4 (task balancing) |
| C4 | D7 (statistical testing) |
| C5 | D5 (SHAP, XAI surveys) |

---

## Bibliography file plan

| File (to create during drafting) | Contents |
| --- | --- |
| `manuscript/overleaf/bibliography/references.bib` | All external citations |
| `manuscript/overleaf/bibliography/citation_keys.md` | Key → short description (optional) |

**Minimum estimated references:** 35–50 for Q1/Q2 engineering journal (Related Work heavy).

---

## Keywords → literature alignment

| Keyword (§3) | Domain |
| --- | --- |
| Load forecasting | D1 |
| Operational stress index | D1, D6 (operational metrics) |
| Graph neural network | D2 |
| Spatio-temporal transformer | D3 |
| Multi-task learning | D4 |
| Explainable AI (XAI) | D5 |
| Bangladesh power grid | D6 |
| Correlation graph | D2 |

---

## Citation discipline rules

1. Every baseline in Table 3 must have a method citation at first mention.
2. SHAP and permutation importance require foundational XAI citations.
3. Do not cite papers to support claims beyond what frozen evidence shows.
4. Bangladesh context claims require regional energy sources — not generic smart-grid papers alone.
5. Bonferroni/Wilcoxon: cite standard statistics reference once in §7.5.
