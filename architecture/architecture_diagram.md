# STGT Architecture Diagram — Phase 09

Generated: 2026-06-24

## PF-STGT block diagram

```mermaid
flowchart TB
    subgraph Input
        X["Node tensor<br/>(B,T,N,F_n)"]
        G["Global context<br/>(B,T,F_g)"]
        A["Hybrid adjacency A<br/>(N,N)"]
    end

    subgraph Embedding
        EMB["Linear + Regional + PosEnc<br/>H0 (B,T,N,d)"]
    end

    subgraph ParallelBranches
        GT["Graph Transformer × L_s<br/>adjacency-biased attention"]
        TE["Transformer Encoder × L_t<br/>temporal self-attention"]
    end

    subgraph Fusion
        GF["Gated Parallel Fusion<br/>H_fused (B,T,N,d)"]
        HS["H_shared = H_fused[:,−1]"]
    end

    subgraph Heads
        DH["Demand Head<br/>9 × MW"]
        SH["Stress Head<br/>OSI ∈ [0,1]"]
    end

    subgraph Explainability
        ATTN["Attention maps export"]
        SHAP["SHAP attribution hooks"]
    end

    X --> EMB
    G --> EMB
    EMB --> GT
    EMB --> TE
    A --> GT
    GT --> GF
    TE --> GF
    GF --> HS
    HS --> DH
    HS --> SH
    GT --> ATTN
    TE --> ATTN
    DH --> SHAP
    SH --> SHAP
```

## Tensor shape trace

| Stage | Shape |
| --- | --- |
| Input node | (B, 7, 9, 9) |
| Input global | (B, 7, 17) |
| Embedded H0 | (B, 7, 9, 128) |
| H_shared | (B, 9, 128) |
| Task 1 output | (B, 9) |
| Task 2 output | (B, 1) |

---

## S2 (final) vs S1 (original) diagram note

The block diagram above describes the **shared PF-STGT trunk** used by both S1 and S2.
For **S2**, replace the hybrid adjacency input with the **correlation graph** built at
τ = 0.65 (33 undirected edges, 91.7% density). All other blocks are unchanged.

```mermaid
flowchart LR
    S1["S1 Original<br/>Hybrid A<br/>24 edges"]
    S2["S2 Final<br/>Correlation A<br/>33 edges"]
    TRUNK["Shared trunk<br/>GT + TE + Fusion + Heads"]
    S1 --> TRUNK
    S2 --> TRUNK
```

Frozen checkpoint: `experiments/experiment_03_ablation_studies/checkpoints/A6/seed_42/best.pt`
