# OT-18 appendix — P5's two floor curves, fifth campaign attempt

**STATUS: SEALED 2026-08-17 04:05 PDT, BY RECORDED OWNER OVERRIDE of
the same-day rule — the program's seventh recorded exception** (F1′
qualified earlier this session; `FAMILY-F1P.md` says next session;
the owner instructed the seal with that sentence on the table).
Mitigations: the graded seed **20260910 is disjoint from all five
qualification seeds**, on a family qualified across seeds precisely
so a fresh one has demonstrated room (interior margins 2× over both
floors at every qualification seed); and **every bar below was
checked against the five-seed family record at enforcement
granularity before sealing** — the check that OT-10, OT-13, and
OT-17 died for lack of. Runner: `ot18_check.py`. Result:
`results/OT18-floor-curves.json`, as executed. One of two budgeted
instrument revisions available; no final-revision clause.**

## Claim under test

P5 v0.2's owed prediction, unchanged through four campaigns: the
informative fraction of codec pairs decays with output quantization
while accuracy on margin-decisive pairs stays at ceiling; silence on
a decisive pair is a miss.

## Instrument (F1′ + the OT-17 probe, both verbatim)

Family F1′ (`FAMILY-F1P.md`): 100 pairs, traces
logspace(−4.5, −0.5), equal trace within pair; the OT-12 consumer;
damage over 2000 draws; margin = |ΔD|/σ_meas, 200-draw bootstrap;
the ⅝-decade dense grid M ∈ {3000, 1732, 1300, 1000, 750, 562, 422,
316, 237, 178, 133, 100, 75, 56, 42, 30, 10, 3, 1}, band [30, 1732],
steps derived as M·rms in-run. Operator probed once on the smooth
consumer (blind lstsq, sketch 80, eps 1e−3); per-pair sign
predictions graded against quantized damage per step; graded = 
informative ∧ margin ≥ 3, silence = miss; a step grades at ≥ 8
graded pairs. Seed 20260910.

## The pre-seal bar check, recorded

The B1 of three campaigns (per-step monotonicity, tol 0.05) **fails
at all five qualification seeds on the dense grid** (local aliasing
wobbles up to 0.81 between ⅓-octave neighbors) — sealing it verbatim
would have manufactured a fifth instrument death, and the check
caught it before the seal for the first time in this program. The
octave-subset variant fails at 2 of 5 seeds (excess +0.08). The
record-supported operationalization of "decays" is the trend form
below, with margins 0.09–0.15 at every qualification seed.

## Manipulation checks (any failure → VOID)

- **MC1:** ≥ 4 interior band steps (fraction ∈ (0.10, 0.90)).
- **MC2 (band level):** ≥ 2 of the interior steps straddle margin 3
  (≥ 20% of informative pairs each side).
- **MC3 (window):** fraction ≥ 0.9 at M = 1 and ≤ 0.1 at M = 3000.

## Bars

- **B1 (decay as trend):** Spearman correlation of informative
  fraction against log M over the full grid ≤ **−0.8**.
- **B2 (conditional ceiling):** accuracy ≥ 0.85 at every graded
  step.
- **B3 (never wrong-while-decisive):** no graded step with accuracy
  ≤ 0.60.

**PASS = MC1–3 ∧ B1 ∧ B2 ∧ B3** — and with it, the discharge of the
theory's last owed prediction. FAIL as executed returns P5 to
revision. Sub-noise accuracy and silence share recorded ungraded.
Per `OT-CRUCIBLE-4.md` G2's standing sentence: no v1.0 declaration
follows from any outcome here; a PASS opens that question for its
own sealed, unhurried act.
