# OT-13 instrument appendix — P5's two floor curves on the F1 family

**STATUS: SEALED 2026-08-16. Drafted unsealed 2026-08-15 at
`afdae4d`; sealed the following working session per the rate-limit
rule, with no edits to bars, constants, or claim between draft and
seal. Runner: `ot13_check.py`. Result: `results/OT13-floor-curves.json`.**

## Claim under test

P5 v0.2 (readscope `PRINCIPLES.md`), the owed prediction: **the two
floor curves** — as output quantization coarsens, the *informative
fraction* of codec pairs decays smoothly, while prediction accuracy on
pairs whose signal is above the estimator's noise **stays at ceiling**.
The forbids-clause at stake: the metric is never
wrong-while-decisively-differential; silence is permitted only at the
response floor.

## Family (cited, not modified)

F1 per `FAMILIES-CRUCIBLE-3.md` and `results/FAM1-shakedown.json`
(interior DEMONSTRATED): 30 codec pairs, pair energies log-spread over
three decades (trace ∈ logspace(1e−4, 1e−1, 30)), **equal trace within
each pair** so every prediction is a pure geometry call; the OT-12
consumer (16-unit softmax head, d = 64, temperature 1); damage = mean
squared change of the quantized output over 2000 codec draws; margin
m = |ΔD| / σ_meas with σ_meas from a 200-resample bootstrap over
draws. Decisive band from the shakedown: quantization steps 30×–1000×
the calibrated rms.

## Instrument

- Consumer output quantized at step = M · rms, where rms is the
  median absolute output change of the *unquantized* consumer under
  the codec draws, **recomputed this run** (lesson: derived grids,
  OT-12 v2). Grid M = {3000, 1000, 562, 316, 178, 100, 56, 30, 10, 1}
  — seven log-spaced steps refining the decisive band, plus anchors
  on both sides.
- Operator recovery: readscope `blind_probe` (lstsq, sketch 80,
  eps 1e−3) **on the quantized consumer at each step** — the probe
  sees only what the step leaves visible.
- Prediction per pair: sign of tr(P̂ · (Σ₁ − Σ₂)). Measured truth:
  sign of ΔD on the quantized outputs.
- A pair at a step is **informative** if measured ΔD ≠ 0; **graded**
  if additionally its margin ≥ 3. On graded pairs a silent prediction
  (tr = 0) **counts as a miss** — that is precisely the forbids-clause.
  A step is graded only if it has ≥ 8 graded pairs; steps with fewer
  are recorded ungraded.
- Constants: SEED 20260817, D 64, K 16, N_PTS 24, N_PAIRS 30,
  N_DRAWS 2000, BOOT_B 200, SKETCH 80, EPS 1e−3.

## Manipulation checks (any failure → VOID)

- **MC1 (interior):** ≥ 4 decisive-band steps (M ∈ [30, 1000]) with
  informative fraction strictly inside (0.10, 0.90).
- **MC2 (margin straddle):** at every MC1 step, ≥ 20% of informative
  pairs on each side of margin 3 — the graded/ungraded split must
  itself have interior.
- **MC3 (window):** informative fraction ≥ 0.9 at M = 1 and ≤ 0.1 at
  M = 3000 — the grid spans floor to ceiling.

## Bars

- **B1 (fraction decay):** informative fraction monotone
  non-increasing as the step coarsens, tolerance 0.05 per grid step.
- **B2 (conditional ceiling):** accuracy ≥ 0.85 at **every** graded
  step.
- **B3 (never wrong-while-decisive):** no graded step with accuracy
  ≤ 0.60.

**PASS = B1 ∧ B2 ∧ B3** (given no VOID). Any bar failing → FAIL as
executed.

## Recorded ungraded (no evidential weight, by prior declaration)

Accuracy on sub-noise informative pairs (margin < 3) per step — the
Second Crucible's 0.633 band, finally measured on an instrument that
can separate law from noise; and the silence share among sub-noise
pairs. Neither enters any bar.
