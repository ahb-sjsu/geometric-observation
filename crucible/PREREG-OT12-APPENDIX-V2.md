# OT-12 instrument appendix v2 — sealed before the v2 run; final

**The v1 run passed its bars vacuously and is recorded as
VOID-in-substance (`results/OT12-floor-curves.json`, kept as
executed): informative pairs fell 30/30 → 0/30 in a single grid step —
the g grid's coarsest step (1/256 ≈ 4e-3) already exceeded nearly all
output changes, so the family jumped over its floor instead of
approaching it, and F2's "ceiling at every graded cell" was graded on
one cell. This is the pattern the program's standing rule exists for
(a bar of the form "X holds along Y" requires a prior check that Y has
interior points), and that check was missing from v1 — an
instrument-spec defect of the OT-5-v1 class. Two changes; the frozen
claim is untouched.**

1. **Interior-coverage manipulation check (new, narrowing):** the run
   is VOID unless ≥ **3** cells have informative fraction strictly
   inside (0.10, 0.90). A curve claim needs a curve.
2. **The grid is derived, not guessed:** a calibration step (same
   seeds) measures `rms` = the median RMS output change of the
   *unquantized* consumer under the codec draws; quantization steps
   are then placed relative to it — step = m·rms for
   m ∈ {30, 10, 3, 1, 0.3, 0.1, 0.03}, i.e. `g = round(1/(m·rms))`
   (plus the unquantized cell) — spanning from far-above to far-below
   the response scale by construction.

All other constants and bars (F1 tolerance, F2 ceiling 0.85 with the
≥10-informative floor, F3 kill) unchanged from v1. **This is the final
instrument revision; a v2 VOID or FAIL closes OT-12 accordingly.**
Result: `results/OT12-floor-curves-v2.json`.
