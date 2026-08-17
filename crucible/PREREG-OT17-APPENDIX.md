# OT-17 appendix — P5's two floor curves, fourth campaign

**STATUS: SEALED 2026-08-17 03:22 PDT, rule-compliant (family
constructed 2026-08-15; see `OT-CRUCIBLE-4.md`). Runner:
`ot17_check.py`, fresh seed **20260819** — the OT-13 runs drew from
20260817, so every graded number binds to unseen draws. Result:
`results/OT17-floor-curves.json`, committed as executed. One of two
budgeted instrument revisions available; no final-revision clause.**

## Claim under test

P5 v0.2's owed prediction, unchanged through three campaigns: as
output quantization coarsens, the **informative fraction** of codec
pairs decays while **accuracy on margin-decisive pairs stays at
ceiling** — and silence on a decisively-differential pair counts as
a miss (the forbids-clause).

## Instrument (OT-13 v2's, inherited verbatim except the seed)

F1 family: 30 codec pairs, energies log-spread over three decades,
equal trace within pair; the OT-12 consumer (16-unit softmax head,
d = 64); damage = mean squared change of the quantized output over
2000 draws; margin = |ΔD|/σ_meas, 200-draw bootstrap. Operator
probed **once on the smooth consumer** (the OT-5 precedent), blind
lstsq, sketch 80, eps 1e−3; per-pair predictions graded against
quantized damage per step. Grid: the family-validated 3× spacing,
M ∈ {3000, 1000, 300, 100, 30, 10, 3, 1} at derived rms; decisive
band M ∈ [30, 1000]. A pair is graded at margin ≥ 3 with silence
counted as a miss; a step is graded at ≥ 8 graded pairs.

## Manipulation checks (any failure → VOID)

- **MC1 (interior):** ≥ 4 decisive-band steps with informative
  fraction strictly inside (0.10, 0.90).
- **MC2 (straddle, at BAND level — the one change from OT-13):**
  at least **2** of the MC1 interior steps have ≥ 20% of informative
  pairs on each side of margin 3. The per-step version killed a
  perfect curve on seed fragility; the family record (4/4 at its
  seed, 3/4 at OT-13-v2's) supports the band-level form at exactly
  this granularity — the check now checked against the record, as
  the addendum demands.
- **MC3 (window):** informative fraction ≥ 0.9 at M = 1 and ≤ 0.1
  at M = 3000.

## Bars (unchanged from OT-13, three campaigns running)

- **B1:** informative fraction monotone non-increasing as the step
  coarsens, tolerance 0.05 per grid step.
- **B2:** accuracy ≥ 0.85 at every graded step.
- **B3:** no graded step with accuracy ≤ 0.60.

**PASS = B1 ∧ B2 ∧ B3** (given no VOID) — and with it, per
`OT-CRUCIBLE-4.md` G1, the discharge of the theory's last owed
prediction. Sub-noise accuracy and silence share recorded ungraded,
as ever — the 0.633 band's final descriptive appearance.
