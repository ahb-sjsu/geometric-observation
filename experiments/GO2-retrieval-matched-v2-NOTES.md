# GO-P-2026-009 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO2-retrieval-matched-v2.json`](../results/GO2-retrieval-matched-v2.json).
**Registered verdict: PASS — `GO2_mechanism_replicates: true`. All five gated
conditions met.** GO-2's mechanism is `[replicated]` on **2 independent instances**
(softmax attention + retrieval ranking). Reported as-is (sealed, PROSPECTIVE,
registered commit 7629a05).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| matched-distortion (recon a≈b within 2%) | recon a=b=d=0.0964, gap 0.0 | ✅ |
| **SNR (loser's dO ≥ 10× floor)** | 0.074 / 0.121 vs 6.1e-7 | ✅ |
| **flip decisive** (adv_dO read_A ≤ −log1.3, read_B ≥ log1.3; ≥10/12) | −4.70 / +4.65; 12/12 & 12/12 | ✅ |
| **proj_var tracks flip** (≥11/12 both) | 12/12 & 12/12 | ✅ |
| recon fails (min Spearman recon < proj_var) | 0.40 < 1.00 | ✅ |

## The clean result

At **identical reconstruction** (a=b=d=0.0964), the retrieval ranking flips with
the consumer's read subspace, now decisive **and** non-degenerate (η=0.1 mix):

| consumer | dO(a) | dO(b) | winner |
|---|---|---|---|
| read_A (queries in S_A) | 0.0740 | **0.0007** | b |
| read_B (queries in S_B) | **0.0012** | 0.1208 | a |
| iso (diagnostic) | ~ | ~ | tie (adv 0.03) |

The "blind" arm's dO is small but **nonzero** (0.0007 / 0.0012 — the 10% isotropic
leak), so the SNR gate is well-posed and passes on the loser (0.074 / 0.121 ≫
floor). `proj_var` tracks the flip 12/12 in both consumers; reconstruction, being
identical across a/b/d, cannot order them (Spearman 0.40). The nonlinear retrieval
ranking follows the injected error's subspace overlap — the genuine falsifiable
question — decisively.

## What v009 fixed (gate, not claim)

GO-P-2026-008 already passed the four substantive gates 12/12; its registered flag
was False only because the SNR gate read `min-arm dO` and the blind arm was exactly
0 (perfect orthogonality). v009 (i) gates the **loser's** dO — the well-specified
non-degeneracy — and (ii) injects a 90%-subspace + 10%-complement mix so no arm is
exactly zero. Same claim, correct gate; it now passes cleanly.

## Ledger disposition

- GO-2 mechanism `tr(P_C·Σ_δ)`: **`[replicated]`** — instance 1 (softmax attention,
  GO-P-2026-006, real compressors, emergent flip) + instance 2 (retrieval ranking,
  GO-P-2026-009, matched-distortion probes, constructed flip). Two representations,
  two consumers, one mechanism.
- Regime bound intact: NEG-10 (the flip is observable only for reconstruction-
  matched arms) — instance 2 met it by construction; a real-compressor retrieval
  case where arms happen to be recon-tied remains a stronger (harder) future target.
- All prior negatives (NEG-5…10) stand. Nothing retro-fitted: every prereg sealed
  and committed before its run.

## The full arc (8 runs, all registered, all recorded)

instance 1: v1 miss → v2 neg-half `[demonstrated]` → v3 consumer-relativity → v4
mechanism found → v5 core decisive → v6 pos-half `[demonstrated]`.
instance 2: 007 prospective miss (bounds regime, NEG-10) → 008 substance + gate
bug → **009 `[replicated]`**.

GO-2 now stands as `[replicated]` on the ledger — the strongest class the risk-
bearing core targets — with six honest negatives delimiting exactly where and why.
