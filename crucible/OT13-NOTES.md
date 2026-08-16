# OT-13 notes — the v1 instrument death, diagnosed from its own record

**2026-08-16. v1 verdict: FAIL as executed
(`results/OT13-floor-curves.json`, kept). The record shows the
failure is the instrument's, in two ways, both recognized classes.**

## 1. The probe was structurally silent at every decisive step

`subnoise_silence = 1.0` at every step except m = 1, and graded
accuracy exactly 0.000 everywhere — every graded pair was scored a
miss by the silence-counts-as-miss clause, because **no prediction
was ever made**. Cause: v1 probed the *quantized* consumer at
eps = 1e−3, whose induced output excursions (~1e−4) cannot cross a
quantization boundary at any step ≥ 10× rms (≥ 3.8e−3). Meanwhile
"decisively differential" (margin ≥ 3) was measured in the damage
channel, which uses codec-scale perturbations (input norms up to
~0.3). The appendix demanded non-silence from a channel that
physically transmits nothing at the graded steps — the OT-5-v1 class
(the instrument guaranteed its own verdict regardless of the theory),
compounded by a scale conflation between the probe's channel and the
damage channel. The program's own precedent runs the other way:
OT-5 probed the **smooth** consumer and graded selection-regime
damage. Even at m = 1 the probe was only partially visible
(excursions ≈ 0.3× step), which is why its 0.679 is not a graded
reading of anything.

## 2. The refined grid sat below the family's aliasing scale

Informative fraction 5/30 at 1000×, **0/30 at 562×**, 15/30 at 316×
— a non-monotone artifact of where quantization boundaries fall
relative to the base outputs, at a grid spacing (1.78×) finer than
anything the family shakedown validated (3× spacing, monotone).
B1's per-step monotonicity bar then failed on quantizer aliasing,
not on the decay claim.

## What v2 changes (instrument spec only; claim and bars untouched)

Per `PREREG-OT13-APPENDIX-V2.md`: (1) the operator is probed once on
the unquantized consumer — the OT-5 precedent — and its per-pair
predictions are graded against quantized damage at every step;
(2) the grid reverts to the family-validated 3×-spaced steps.
Margins, the silence-counts-as-miss clause, all MCs, and bars B1–B3
are unchanged. One revision remains in the budget after this.

## v2 verdict: VOID as sealed — OT-13 closes UNRESOLVED per G3

**2026-08-16, same session (`results/OT13-floor-curves-v2.json`,
kept).** The instrument fix worked completely: accuracy **1.000 at
every graded step** (m = 1 through 1000, 6 graded steps, 28→3 graded
pairs), fraction decay clean and monotone (1.00 → 0.00), window
intact, B1/B2/B3 all formally passing. The run died on **MC2**: at
m = 300, only 2 of 16 informative pairs (12.5%) sat below margin 3,
against the sealed ≥ 20%-each-side requirement at every interior
step. The straddle property held at the shakedown's seed (share
0.286 at 300×) but is seed-fragile at the band edges; demanding it
as a per-step VOID condition was appendix authoring, not family
qualification.

`OT-CRUCIBLE-3.md` G3 is explicit and was sealed twice: *"a VOID on
a pre-qualified family is an appendix-authoring failure, closes that
test unresolved, and may not be regraded or re-familied within this
campaign."* The revision budget does not override G3 — it exists for
diagnosed instrument deaths graded FAIL, and G3 is specific to
VOIDs. **OT-13 is closed, unresolved. P5's revision remains
untested-in-substance.** The v2 record — ceiling accuracy wherever
margin certifies, decay everywhere, zero silence from a
properly-scaled probe — is exploratory support of exactly the
OT-10-quantities kind: real, recorded, and carrying no verdict
weight. A future campaign's appendix should bar the straddle as a
*band-level* property (some interior step straddles) rather than a
per-step one, and this note is the only place that lesson may
legitimately live.
