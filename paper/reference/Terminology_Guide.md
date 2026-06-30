# Terminology Guide

**Revised:** 2026-06-30  
**Purpose:** Canonical naming for consistent manuscript terminology  
**Authority:** Architecture freeze, publication tables, consistency audit  
**Manuscript files:** Section 6 = `06_Methodology.md`; Section 8 = `08_Results.md`

---

## Model and architecture names

| Canonical term | Meaning | When to use | Avoid |
| --- | --- | --- | --- |
| **S2** | Final proposed model; correlation-only PF-STGT | Abstract, Conclusion, proposed-method claims | Calling S2 "B07" |
| **S1** | Original hybrid-graph PF-STGT W20 design | Historical comparison, design evolution | Calling S1 the proposed model |
| **PF-STGT** | Parallel-Fusion Spatio-Temporal Graph Transformer (class name) | Architecture description | Inconsistent hyphenation ("PFSTGT" OK in code) |
| **Correlation-Aware Multi-Task Forecasting Framework** | Publication name for S2 | Title, first mention of S2 | Overusing full name after first mention |
| **PFSTGT** | Python class (`src/models/pf_stgt.py`) | Methods implementation detail | In prose abstract |
| **B07** | Exp02 benchmark ID for S1 checkpoint | Benchmark tables, Exp02 discussion | As proposed final model label |
| **A6** | Exp03 ablation ID for S2 | Ablation tables, checkpoint paths | Interchangeably with S2 without noting equivalence |
| **A1** | Exp03 ablation ID for S1 | Ablation reference comparisons | Without noting A1 = S1 = B07 metrics |
| **A4** | Single-task demand-only hybrid variant | Demand upper-bound discussion | Calling A4 the final model |
| **W20** | Multi-task loss protocol (λ₂ = 20) | Training / loss discussion | Confusing with checkpoint folder name only |

### Equivalence table (frozen)

| Symbol | Equivalent IDs | Role |
| --- | --- | --- |
| S2 | A6 | **Final proposed model** |
| S1 | A1, B07 | Historical reference |
| Correlation-Only PF-STGT | S2, A6 | Descriptive name |
| PF-STGT W20 hybrid | S1, A1, B07 | Descriptive name for S1 |

---

## Task and target terminology

| Canonical term | Definition | Notes |
| --- | --- | --- |
| **Demand forecasting** | Task 1: next-day regional demand (MW) for N=9 regions | Primary ranking task |
| **Operational Stress Index (OSI)** | Task 2: scalar system-health signal ∈ [0, 1] | Also "operational stress" / "stress forecasting" |
| **Multi-task learning** | Joint demand + OSI prediction with shared trunk | Distinct from A4 single-task |
| **Macro demand MAE** | Mean of per-region MAE over 9 regions (MW) | **Primary evaluation metric** |
| **Macro demand R²** | Mean of per-region R² (not pooled) | Exp02A documents aggregation caveat |
| **Graph-level OSI** | Single OSI target per timestep (not per-region) | Stress head output shape (B, 1) |

---

## Graph terminology

| Canonical term | Definition | S2 value |
| --- | --- | --- |
| **Hybrid graph** | Geographical + correlation edges (S1) | Superseded for production |
| **Correlation graph** | Data-driven adjacency from inter-region demand correlation | τ = 0.65; 33 edges |
| **Geographical graph** | Adjacency from `graphs/adjacency_matrix.csv` | A5 geo-only ablation |
| **Correlation-only adjacency** | S2 graph variant | `GraphVariant.CORR` |
| **Attention bias** | Derived from row-normalised adjacency | Optional model input |
| **Row-normalised adjacency** | Standard graph preprocessing | Applied to corr and geo matrices |

---

## Experimental programme labels

| Label | Full name | Type |
| --- | --- | --- |
| Exp01 | PF-STGT Training | Training validation |
| Exp01A | OSI Failure Investigation | Diagnostic |
| Exp01B | Multitask Optimization Repair | Protocol freeze |
| Exp02 | Benchmark Models | B01–B07 comparison |
| Exp02A | Classical Benchmark Verification | Metric audit |
| Exp03 | Ablation Studies | A1–A6 |
| Exp03A | Ablation Failure Investigation | Interpretation |
| Exp03B | Architecture Simplification | S1–S4 selection |
| Exp04 | Explainability Analysis | XAI on frozen S2 |

---

## Baseline model IDs (Exp02)

| ID | Model |
| --- | --- |
| B01 | Linear Regression |
| B02 | Random Forest |
| B03 | XGBoost |
| B04 | LSTM |
| B05 | GRU |
| B06 | T-GCN |
| B07 | PF-STGT W20 hybrid (S1) |

---

## Ablation variant IDs (Exp03)

| ID | Variant | Graph | Multi-task |
| --- | --- | --- | --- |
| A1 | PF-STGT W20 (S1) | hybrid | Yes |
| A2 | No Graph | hybrid | Yes |
| A3 | No Transformer | hybrid | Yes |
| A4 | Single-Task | hybrid | No |
| A5 | Geographical Graph Only | geo | Yes |
| A6 | Correlation Graph Only (S2) | corr | Yes |

---

## Architecture simplification IDs (Exp03B)

| ID | Description |
| --- | --- |
| S1 | PF-STGT W20 hybrid (reference) |
| S2 | Correlation-Only PF-STGT (**final**) |
| S3 | No-Transformer PF-STGT (hybrid) |
| S4 | Correlation + No-Transformer |

---

## Feature coalition groups (Exp04)

| ID | Name | Scope |
| --- | --- | --- |
| G1 | regional_demand_block | node |
| G2 | regional_supply_block | node |
| G3 | regional_load_block | node |
| G4 | engineered_lags_rolling | node |
| G5 | regional_share_intensity | node |
| G6 | calendar_trend | global |
| G7 | grid_aggregates | global |
| G8 | limitation_stack | global |
| G9 | weather_anomaly | global |
| G10 | national_generation_scalars | global |
| G11 | shedding_indicator | global |

---

## Explainability method terms

| Term | Meaning |
| --- | --- |
| **Grouped SHAP** | Integrated gradients attributions aggregated to coalitions G1–G11 |
| **Permutation importance** | ΔMAE from feature coalition ablation |
| **Attention export** | Spatial (`attn_spatial`) and temporal (`attn_temporal`) weights |
| **OSI driver agreement** | Match between top SHAP coalition and OSI component driver in case studies |
| **Dual-path attribution** | SHAP coalition vs OSI component (reserve margin vs limitation stack) |

---

## Forbidden or discouraged phrasing

| Avoid | Use instead | Reason |
| --- | --- | --- |
| "Best demand model" (unqualified) | "Best multi-task configuration" | A4 lower MAE (86.89 MW) |
| "State-of-the-art" | "Compared baselines on held-out test set" | No external SOTA benchmark |
| "Validates interpretability" | "Demonstrates attribution analysis" | Partial OSI agreement |
| "Transformer is unnecessary" | "Required on correlation topology (S4)" | S4 +21.32 MW degradation |
| "AdamW" (in Methods) | "Adam" | Frozen checkpoint configs |
| "B07" as proposed model | "S2" | B07 is S1 historical reference |
| "Beats A4 on demand" | "Trades ~1.76 MW vs A4 for stress capability" | A4 = 86.89 MW |

---

## Region names (canonical spelling)

Use exactly: **Barishal, Chattogram, Cumilla, Dhaka, Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet**

Dhaka is the primary regional demand attribution focus in Exp04 tables and figures.
