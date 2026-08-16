# OT-13 instrument appendix v2 — sealed before the v2 run

**STATUS: SEALED 2026-08-16. First instrument revision (one remains
in the budget; no final-revision clause, per `OT-CRUCIBLE-3.md`).
The v1 run is recorded FAIL-as-executed
(`results/OT13-floor-curves.json`, kept); its death is diagnosed in
`OT13-NOTES.md` from its own record: the probe was structurally
silent at every decisive step (silence 1.0, accuracy exactly 0.000 —
no prediction was ever made), and the refined grid aliased below the
family's validated spacing. Runner: `ot13_check_v2.py`. Result:
`results/OT13-floor-curves-v2.json`.**

Two instrument changes; the claim, the family, the margins, the
silence-counts-as-miss clause, all manipulation checks, and bars
B1–B3 are **unchanged from the v1 appendix**.

1. **The probe reads the smooth consumer (the OT-5 precedent).** The
   operator P̂ is recovered once by `blind_probe` (lstsq, sketch 80,
   eps 1e−3) on the *unquantized* consumer; each pair's prediction
   sign tr(P̂ · (Σ₁ − Σ₂)) is then graded against the measured
   quantized damage ordering at every step. v1's choice to probe the
   quantized consumer conflated the probe's perturbation channel
   (excursions ~1e−4) with the damage channel (codec-scale draws),
   demanding non-silence where the probe channel transmits nothing —
   the metric under test is the geometry read where the instrument
   can read, predicting damage where the codec acts, which is
   exactly how OT-5 ran and precisely P5's floor-law setting.
2. **The grid reverts to the family-validated spacing:**
   M = {3000, 1000, 300, 100, 30, 10, 3, 1} (the shakedown's own
   steps; decisive band {1000, 300, 100, 30}), steps still derived
   as M · rms with rms recomputed in-run. v1's 1.78×-spaced
   refinement sat below the family's aliasing scale and produced a
   non-monotone artifact (0/30 informative at 562× between 5/30 at
   1000× and 15/30 at 316×) that B1 then graded as a decay failure.

Everything else binds as sealed in `PREREG-OT13-APPENDIX.md`:
MC1 ≥ 4 decisive-band steps with informative fraction in
(0.10, 0.90); MC2 margin straddle at every such step; MC3 window
(≥ 0.9 at m = 1, ≤ 0.1 at m = 3000); B1 fraction decay (tol
0.05/step); B2 accuracy ≥ 0.85 at every graded step (≥ 8 graded
pairs, margin ≥ 3, silence = miss); B3 no graded step ≤ 0.60;
sub-noise accuracy and silence recorded ungraded. SEED 20260817
unchanged.
