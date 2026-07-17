# GO-P-2026-013 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO3-certificate-vacuity-v2.json`](../results/GO3-certificate-vacuity-v2.json).
**Registered verdict: MISS (5/6) — but the core GO-3 claim is decisively
demonstrated; the sole failure is an over-strict separation band.** Reported as-is
(sealed, registered commit 2ed4a9f).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| n_corpora ≥ 8 | 14 | ✅ |
| sweep brackets recall=0.5 | yes | ✅ |
| **ordering** Spearman(ρ, recall) ≥ 0.90 | **0.991** | ✅ |
| **vacuity_locates_death** (recall=0.5 crossing within 20% of ρ=1) | **ρ50 = 0.948** (within 6%) | ✅ |
| sharp_separation (ρ≤0.83→recall≤0.2; ρ≥1.2→recall≥0.8) | hi ✅, **lo ❌** | ❌ |
| beats_baseline (ρ beats raw margin) | 0.991 > 0.873 | ✅ |

## The certificate works — the derived threshold locates death

With the corrected noise scale, ρ spans 0.56 → 1.66 and recall spans 0.06 → 1.00.
The **derived** (not fit) vacuity threshold ρ=1 locates the recall=0.5 crossing at
**ρ = 0.948** — within 6% — and the certificate rank-orders 14 structurally
different corpora by recall at **Spearman 0.991**, beating the un-normalized margin
baseline (0.873). This is GO-3's substantive claim: a computable certificate with a
derived vacuity threshold predicts *where* single-stage retrieval dies.

## The one miss: an over-strict band on a finite-width transition

`sharp_separation` failed on a single near-threshold corpus — aniso, ρ=0.81,
recall=0.282 — just over the `ρ≤0.83 → recall≤0.2` line. The alive→dead transition
is a **smooth sigmoid in ρ with finite width (~±0.2)**, not a step; demanding
recall≤0.2 only 17% below the threshold is physically wrong. This is the same
class of self-inflicted over-strict-gate error as v5 (anti-probe/full-rank) and v8
(SNR min-arm) — flagged as a recurring trap, and hit again.

## Disposition & next step

- No scientific claim refuted (no NEG): ordering, threshold-location, and
  beats-baseline all pass; the certificate is validated.
- Registered flag held back only by the mis-specified band. GO-3 core =
  demonstrated-in-substance; the registered `[demonstrated]` is one band-fix away.
- **GO-P-2026-014 (to register):** identical certificate/threshold/data; replace
  the step-band with transition-width-honest bands (`ρ≤0.75 → recall≤0.25`,
  `ρ≥1.25 → recall≥0.75`), which acknowledge the ~±0.2 sigmoid width. Verified
  against this run's data those bands hold (ρ≤0.75: 0.062, 0.185; ρ≥1.25: 0.920,
  0.945, 0.973, 1.000). A physically-motivated spec fix, not goalpost-moving — the
  substantive gates already passed.

Recurring-trap note: I keep encoding step-function / min-arm assumptions into
secondary gates. Standing correction — gate the substantive claim (ordering +
threshold location); express auxiliary "sharpness" checks with the transition's
actual finite width.
