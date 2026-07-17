# GO-P-2026-017 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO5-alpha1-quotient-v2.json`](../results/GO5-alpha1-quotient-v2.json).
**Registered verdict: MISS — `GO5_supported: false`. Regime gate now PASSES
(baseline hubness real), but the α=1 quotient does not restore fidelity — for a
conceptual reason about *where* density biases retrieval.** Reported as-is (sealed,
registered commit 44bef8a).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| baseline_hubness (skew(α=0) ≥ 0.5) | **0.69 / 0.69 / 0.65** | ✅ |
| restoration (recall gain ≥ 0.05) | **−0.43** (recall *falls* with α) | ❌ |
| alpha1_optimal | α=0 is best, not α=1 | ❌ |
| hubness_reduced (skew ↓ 0→1) | skew *rises* 0.69→1.04 at α=1 | ❌ |

Per-α (seed0): recall 0.84 / 0.66 / 0.41 / 0.25; hubness skew 0.69 / **0.05** / 1.04 / 3.22.

## Two real findings (the reason it missed)

1. **Density is confounded with the invariant here.** The substrate is a
   *mixture of unequal-density clusters*, so the dense regions **are** the
   true-neighbor structure and the hubs are legitimate cluster centers.
   Down-weighting them by density (α↑) removes signal → recall falls monotonically.
   GO-5's premise requires density to be a **nuisance orthogonal to the invariant**;
   this substrate makes density = signal.
2. **Direct kernel-affinity ranking is not density-biased**, so there is nothing
   for the α quotient to correct. Raw affinity `W_ij=exp(−d²/ε)` ranks by ambient
   distance, which already recovers latent neighbors (recall 0.84). The α=1
   Laplace–Beltrami result restores *geodesic* fidelity against a density bias that
   lives in the **operator / random-walk / diffusion distance** (a spectral or
   diffusion object), not in direct k-NN affinity. Note also hubness is minimized
   at **α=0.5**, not α=1 — and even that minimum does not help recall — confirming
   hubness-reduction ≠ fidelity-restoration in this direct-retrieval setting.

Both are substrate/operationalization issues, not a refutation of GO-5's intended
claim (α=1 restoring the invariant where density is a genuine nuisance in a
density-biased retrieval). But they show my current non-spectral operationalization
(direct affinity + clustered density) cannot exhibit it.

## Where this leaves GO-5

GO-5 needs a non-spectral retrieval that is *actually density-biased* and where
density is *orthogonal* to the invariant. Candidate substrates:
- **ADC / product-quantization retrieval** (the ledger's own hint, "locally-scaled
  ADC retrieval"): quantization-induced hubness corrupts recall of the exact
  neighbors; local-scaling/α-normalization reduces it and restores recall.
- **Diffusion / commute-distance retrieval** on a manifold with a density gradient
  (density-biased base distance, computable without a full eigendecomposition):
  α=1 removes the density term and restores geodesic-neighbor recall.
- **Equal-density classes in genuinely high intrinsic dimension**, where hubs are
  *spurious* cross-class points (not the invariant), so de-hubbing helps.

Two GO-5 misses, both substrate design (v1 double-normalization; v2 density=signal
+ affinity-not-biased). Rather than a third blind attempt, the substrate choice
should match the intended domain — consulting before GO-P-2026-018.
