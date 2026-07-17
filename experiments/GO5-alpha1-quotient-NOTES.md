# GO-P-2026-016 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO5-alpha1-quotient.json`](../results/GO5-alpha1-quotient.json).
**Registered verdict: MISS — `GO5_supported: false` — a degenerate harness
(double density-normalization), not a refutation of GO-5.** Reported as-is
(sealed, registered commit 7b221fc).

## What happened

All three gated conditions failed, and in the *opposite* direction to the
prediction: recall falls monotonically with α (seed0: 0.746 → 0.671 → 0.581 →
0.493 for α=0/0.5/1/1.5) and hubness skew *rises* (0.01 → 0.11 → 0.24 → 0.76). The
uniform-density control shows the same monotone decline (gain −0.13).

## Diagnosis: no baseline hubness to restore

The tell is **baseline hubness skew ≈ 0.01** — essentially zero. The substrate,
as observed through the harness, had *no hubness for the α quotient to fix*. Cause:
the affinity used a **self-tuning** local scale `σ_i = 7th-NN distance`
(Zelnik-Manor), which is *itself* a per-point density normalization — it removes
hubness at the kernel level. Stacking the α density-quotient `1/(q_i q_j)^α` on top
is a **second** density normalization, so α just over-corrects (down-weights dense
regions past neutral), which *hurts* recall and *adds* anti-hub imbalance. Two
density normalizations, not one.

This is a harness/design bug (like GO-3 v1's noise scale), not a property of GO-5:
the test never created the density-corrupted regime the claim addresses. No
scientific claim is refuted (no NEG).

## Fix → GO-P-2026-017

Use a **global-scale** kernel `W_ij = exp(−d²_ij / ε)`, `ε = median_i(7th-NN
dist)²` — a global bandwidth that *keeps* density in the affinity, so raw (α=0)
retrieval is genuinely hubbed and mis-ranks true neighbors near dense clusters.
Then the α=1 quotient is the *only* density normalization and can restore fidelity.
Add a **regime-precondition gate**: baseline hubness skew(α=0) ≥ 0.5 (the substrate
must actually be hubbed, else the test is void — mirrors GO-3's "must bracket
recall=0.5"). Re-registered prospectively; I have unblinded, so it is a fresh
prereg, not an in-place edit.

Standing behavioral-correction note (again): I keep needing a regime-coverage gate
to catch degenerate substrates (GO-3 bracket, now GO-5 baseline-hubness). Build the
precondition gate in from the start.
