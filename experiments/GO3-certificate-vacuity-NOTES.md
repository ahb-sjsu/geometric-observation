# GO-P-2026-012 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO3-certificate-vacuity.json`](../results/GO3-certificate-vacuity.json).
**Registered verdict: MISS — `GO3_supported: false`. A degenerate harness (query-
noise scale bug), not a refutation of the certificate.** Reported as-is (sealed,
registered commit abf65ed).

## What happened

All 14 corpora landed in the **dead** regime: ρ = μ̂/μ_crit ∈ [0.066, 0.296] (all
≪ 1) and recall@1 ∈ [0.000, 0.015] (all ~0). The sweep produced **no alive
corpus**, so:
- `vacuity_locates_death` ❌ — recall never crossed 0.5, so the ρ-at-death
  interpolation is undefined (the registered control "the sweep must bracket
  recall=0.5" failed).
- `ordering` ❌ — Spearman(ρ, recall) = 0.64, weak, because all recalls are ~0
  (no variation to order).
- `sharp_separation` ✅ and `beats_baseline` ✅ pass trivially (everything dead).

## Diagnosis: a scale bug, not the certificate

The queries were `q = normalize(e_t + σ z)` with `z ~ N(0, I_D)` — but unit-norm
items and `‖z‖ ≈ √D ≈ 8` mean the query is **almost pure noise** even at σ=1, so
the signal never clears the distractor bulk and every corpus is dead. Note the
certificate was **consistent**: it reported ρ < 1 (vacuous) for all 14 corpora,
and all 14 were dead — the prediction "vacuous → dead" held. What the run could
**not** test is the alive→dead *transition* (there were no alive corpora), which
is the actual GO-3 claim (the threshold *locates* death).

Fix: scale the query noise to `z ~ N(0, I_D/D)` (‖z‖ ≈ 1), matching the unit
items. Then `μ̂ ≈ √D / √(1+σ²)`, and sweeping σ ∈ {1,…,4} at D=64 spans ρ ≈
1.65 → 0.57 — bracketing ρ=1 and recall=0.5.

## Disposition & next step

- No scientific claim is refuted (no NEG): the certificate's vacuity prediction
  held for every corpus tested; the harness simply never entered the alive regime.
- GO-3 remains **pending**. The corrected experiment must be **newly registered**
  (I have unblinded): **GO-P-2026-013** — identical certificate and derived
  threshold, query noise scaled to `N(0, I_D/D)` so the σ-sweep spans alive→dead,
  plus a registered check that the sweep brackets recall=0.5.

A degenerate first run, caught by its own "must bracket recall=0.5" control, and
fixed with a one-line noise-scaling correction — re-registered, not tuned in place.
