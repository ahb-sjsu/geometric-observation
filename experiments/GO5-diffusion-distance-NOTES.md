# GO-P-2026-019 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO5-diffusion-distance.json`](../results/GO5-diffusion-distance.json).
**Registered verdict: MISS — `GO5_supported: false` (2/3 gated). Per the prereg's
own terms, this makes GO-5 `[refuted]` (as the stated decisive, density-specific
claim), with one honest positive nuance.** Reported as-is (sealed, registered
commit 4b587cd).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| density_regime (max/min density ≥ 5) | 417 / 283 / 12745 | ✅ |
| **restoration** (recall gain ≥ 0.03, >0 all seeds) | **+0.019** (positive but sub-threshold) | ❌ |
| alpha1_optimal (α=1 near-argmax) | ✅ all seeds | ✅ |

Per-α recall (seed0): 0.784 / 0.793 / **0.803** / 0.801 — α=1 is the optimum.

## The honest read: correct direction, wrong magnitude, no specificity

Two things are finally right, and one is decisively wrong:

- ✅ **α=1 is the optimal diffusion exponent** for geodesic-neighbor recall, and it
  is recovered by a **non-spectral** computation (P^t via matrix powers, no
  eigendecomposition) — consistent with the Laplace–Beltrami theory. This is a real,
  if modest, positive: the α=1 optimum transfers out of the eigen-basis.
- ❌ **The effect is small** (+0.019 < 0.03), because the flat/linear manifold's
  ambient distance already recovers geodesics well, so the density bias the α=1
  quotient removes from the diffusion base is modest.
- ❌ **The effect is not density-specific.** The uniform-density control gains
  **+0.015** — nearly as much as the non-uniform +0.019. If α=1 were *removing a
  density nuisance*, the uniform control should gain ~0. It doesn't. So the small
  benefit is a **generic α=1 preference, not density-nuisance removal** — which is
  precisely the mechanism GO-5 asserts. The density-*specific* restoration is
  ~0.004, indistinguishable from noise.

## Resolution: GO-5 `[refuted]` (+ NEG-11)

Across four prospective, diverse non-spectral operationalizations —
self-tuning/global direct affinity (v1/v2), ADC/PQ on real embeddings (v3), and
diffusion-distance retrieval (v4) — the α=1 density/hubness quotient does **not**
produce a decisive, density-specific restoration of the invariant. In the direct/
ADC domains it *hurts* (density not in the base, density entangled with the
invariant); in the diffusion domain the direction is right and α=1 is optimal, but
the effect is <2% and not density-specific.

Per the sealed prereg ("a miss makes GO-5 `[refuted]`"), GO-5's stated claim is
**refuted** → **NEG-11**. The precise, retained positive: *α=1 is the optimal
diffusion exponent, recoverable non-spectrally* — a weaker statement than the book
claimed, honestly logged.

**This is the falsifiable core doing its job.** The core is not 5/5 green: GO-1
`[predicted]`, GO-2 `[demonstrated]`/`[replicated]`+Gate-B, GO-3 `[demonstrated]`,
GO-4 `[replicated]`, **GO-5 `[refuted]`** — four faces of Observation Theory stand,
the fifth (the density-quotient as a general non-spectral restorer) does not, and
the ledger says so with the same prominence. That is a *more* credible book than an
all-pass would have been.
