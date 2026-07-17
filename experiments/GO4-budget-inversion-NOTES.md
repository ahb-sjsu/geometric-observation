# GO-P-2026-015 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO4-budget-inversion.json`](../results/GO4-budget-inversion.json).
**Registered verdict: PASS — `GO4_supported: true`. All three gated conditions,
3/3 seeds.** GO-4 is `[replicated]` (a substrate beyond Paper I §5.10). Reported
as-is (sealed, registered commit ccd7123).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| inversion (≥2/3 seeds) | **3/3** | ✅ |
| convergence at N_min (≥2/3) | **3/3** (gap 0.002 / 0.000 / 0.000) | ✅ |
| mechanism m_grows (all seeds) | yes | ✅ |

## The result: the verdict is the observer's, not the substrate's

On real 768-d book-paragraph embeddings, geometry-preservation (angle-ρ) under
refinement flips sign with the mode budget — every seed:

| seed | trend_fixed (m=10) | trend_matched (m grows) | inversion |
|---|---|---|---|
| 0 | **+0.40** | **−1.00** | ✅ |
| 1 | **+1.00** | **−1.00** | ✅ |
| 2 | **+1.00** | **−1.00** | ✅ |

- **Fixed low budget (m=10):** angle-ρ *rises* with N — 0.35→0.44 (seed0),
  0.31→0.42 (seed1), 0.34→0.43 (seed2). Refining the corpus sharpens the coarse
  manifold in a fixed low-mode band. Verdict: *geometry gets cleaner.*
- **Spectral-gap-matched budget (m grows to hold τ=λ₁₀(N=2000)):** angle-ρ
  *collapses* — 0.35→0.14, 0.31→0.12, 0.34→0.14. The matched budget grows
  10→121 / 10→126 / 10→159 modes, and those added high modes inject sub-geodesic
  (sub-wavelength) detail that destroys the geodesic correlation. Verdict:
  *geometry gets noisier.*
- **Convergence:** at N_min the two budgets coincide (m_matched=10=m_fixed by
  construction) and angle-ρ agrees to ≤0.002 — the divergence is *emergent with
  refinement*, not baked in.

Same substrate, opposite refinement verdict, decided entirely by the observer's
mode budget — exactly the §5.10 wavelength mechanism, now on a real embedding
manifold rather than RGG / Wolfram graphs. "No single budget is optimal" is not a
synthetic-graph artifact.

## Observation Theory: the rate axis

This is the **rate** face of Observation Theory (memory: consumer-relative
rate–distortion–capacity). GO-4 shows the observation *budget* (rate) sets the
verdict, and no substrate invariant survives changing it — the observer's
resolution relative to substrate scale is what "clean geometry" means. With GO-1
(identifiability), GO-2 (distortion), GO-3 (capacity), all four faces are now
demonstrated/replicated on real or prospective substrates.

## Reproducibility note (result-identical solver swap)

The registered compute note named `scipy sparse eigsh`; the run used
**AMG-preconditioned LOBPCG** (pyamg) for the bottom-K eigenpairs — validated
**result-identical** to shift-invert eigsh (max |Δλ| = 3e-15 at N=4000), ~5×
faster at N=32k (eigsh's sparse-LU fill-in blew up; the first run was killed mid
N=32k). angle-ρ uses row-normalized eigenvector distances, invariant to sign /
degenerate-subspace rotation, so the measurement is unchanged. The first
(killed) run's eigenvalues match this run's exactly (λ₁₀(N=2000)=0.4174), and no
angle-ρ was ever computed before the swap — no unblinding.

## Substrate provenance

`/archive/results_aesthetics/book_translation_cache` on Atlas — 4683 real
book-paragraph embedding files (≤200×768 float16); per seed, 250 files sampled
(seeded), concatenated, L2-normalized, 32000-vector nested pool. Assembled on
Atlas (read-only on the corpus; one temp write to /tmp, cleaned), pulled locally.

## Ledger

GO-4 → `[replicated]`. Falsifiable-core scoreboard: **GO-1 `[predicted]` · GO-2
`[demonstrated]`/`[replicated]`+Gate-B · GO-3 `[demonstrated]` · GO-4
`[replicated]`.** Only GO-5 pending. 16 registered runs; NEG-5…10 stand.
