# Computational Budget — Phase 11

Generated: 2026-06-24
Status: **FROZEN**

## Dataset scale

| Split | Rows | Approx. windows (T=7) |
| --- | --- | --- |
| Train | 1295 | ~1287 |
| Validation | 277 | ~269 |

## Model scale (9-node PF-STGT)

| Component | Typical parameter count |
| --- | --- |
| d_model=128, L_s=2, L_t=2, H=4 | ~0.8–1.2 M parameters |
| d_model=192, L_s=3, L_t=3, H=8 | ~2.5–3.5 M parameters (upper bound) |

Small graph (N=9) keeps attention O(N²) negligible vs temporal O(T²), T=7.

## Trial budget

| Stage | Runs | Description |
| --- | --- | --- |
| Stage 1 HPO | 20 | Random search, seed 42 |
| Stage 2 confirmation | 9 | Top-3 configs × 3 seeds |
| Stage 3 test | 1 | Final selected config, best seed |
| **Total training runs** | **30** | Before benchmark comparison |

## Runtime estimates (single GPU, e.g. Apple M-series / T4)

| Item | Estimate |
| --- | --- |
| Avg epochs to early stop | 35–60 |
| Time per epoch (B=32, ~1M params) | 15–30 s |
| Time per Stage-1 trial | 10–20 min |
| **Stage 1 total** | **4–6 h** (~4–7 h) |
| **Stage 2 total** | **1–3 h** (~1–2 h) |
| **HPO subtotal** | **~5–9 GPU-hours** |

## Resource requirements

| Resource | Minimum | Recommended |
| --- | --- | --- |
| GPU VRAM | 4 GB | 8 GB |
| System RAM | 8 GB | 16 GB |
| Storage per trial | ~50 MB checkpoint | ~1 GB total HPO artifacts |
| CPU fallback | Supported (3–5× slower) | GPU preferred |

## Budget guardrails

- Hard cap: **20** Stage-1 trials (no adaptive expansion).
- Stop trial early if val MAE diverges (>2× train MAE after epoch 10).
- No nested cross-validation (insufficient data; Phase 06 chronological split frozen).
