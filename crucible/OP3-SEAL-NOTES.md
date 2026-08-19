# OP3 seal outcome — FAIL (2026-08-19)

The graded run of the sealed OP3 front-law bars (`op3_graded.py`, on
disjoint seeds {20260819, 20260820, 20260821}) returned **FAIL** on all
three bars. Recorded exactly as executed; **no bar was adjusted.** The
verdict is in `results/OP3-frontlaw-graded.json`.

## Per-seed result

| seed | best_p (B1) | front_slope (B2) | affine overlap (B3) |
|---|---|---|---|
| 20260819 | 5.0 | 0.235 | 0.596 |
| 20260820 | 5.0 | −0.054 | 0.582 |
| 20260821 | 4.0 | 0.310 | 0.643 |

- **B1** (best-collapse exponent == 4 on every seed): **FAIL** — two of
  three seeds minimize at p=5. The collapse RMS is a near-tie at the
  bar: seed 0 read p4=0.1571 vs p5=0.1531. The exponent bar sat on a
  knife-edge the shakedown already showed (p4=0.157, p5=0.159).
- **B2** (front rate 0.869 ± 0.10, all seeds > 0.5): **FAIL** — mean
  slope 0.164, none above 0.5.
- **B3** (affine-operator overlap ≥ 0.9): **FAIL** — mean 0.607.

## Diagnosis — an authoring/bar-calibration defect, not a refuted law

The failure is in how the bars were operationalized, not in the front
law's physics (which stands: derived, Lean-checked in
`FrontLaw.lean`, and shakedown-supported — the collapse RMS is still
minimized *near* p=4, recovery is real and spectrum-ordered).

1. **B3 contradicts the law it tests.** The front law predicts recovery
   is only ~60–70% complete at m=1000 (the front reaches ~mode 10 of
   16); demanding the estimator realize M's top-16 subspace to ≥ 0.9
   there is inconsistent with the theory's own prediction. The measured
   ~0.60 is *what the front law expects*. This bar should never have
   been set at 0.9.
2. **B2 measures a different quantity than 0.869 was derived for.** The
   derived rate 0.869 = 1/ln(w⁻⁴) is the slope of the *smooth fitted*
   front position (`op3_frontlaw.py`, from the collapse constant A).
   `op3_graded.front_slope` instead reads the *empirical first-0.5-
   crossing* of the per-mode curve, which is noisy and non-monotonic
   (istar seed 0 = [8.31, 7.43, 7.52, 8.55, 9.37]). Barring the noisy
   crossing against the smooth-front rate is a runner–bar mismatch.
3. **B1 is a knife-edge.** p=4 vs p=5 are within 0.004 RMS; an exact
   `== 4` bar is brittle to the seed. A tolerance band (p ∈ {4,5}, or
   "RMS minimized at p ≤ 5 and monotone around it") would have held.

## Consequence (per the discipline)

- **OP3's owed prediction is NOT discharged and NOT refuted.** The
  graded seal caught defective bars — the first v1-line analogue of
  OT-10 (a recorded FAIL on an authoring defect) crossed with the
  bar-granularity lesson of OT-13.
- The front law (`FrontLaw.lean`, the p≈4 collapse, the front advance)
  is untouched and still supported; what failed is the sealed
  operationalization.
- A corrected re-run is a **new sealed act** (its own fresh-day seal),
  not an edit of these bars: B1 as a p-band, B2 on the fitted-front
  slope (not the empirical crossing), B3 at the front law's *predicted*
  overlap, not 0.9. This appendix's bars stay as sealed and FAILED.
- Frozen v1.0 statements untouched. Live exposure: OP3 remains open.

## Lesson (durable)

**Check every bar against the theory's own quantitative prediction and
against the exact quantity the runner computes — before sealing.** B3
was refuted by the front law itself; B2 barred a quantity the runner
does not measure. The pre-seal record-check (the practice that made
same-day sealing survivable) must include "does the law predict this
threshold, and does the runner measure this exact statistic." Recorded
for the corrected re-run and for future v1-line campaigns.
