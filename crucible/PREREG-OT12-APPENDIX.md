# OT-12 instrument appendix — sealed before the run

**Claim frozen in `OT-CRUCIBLE-2.md`: the two floor curves — under
output quantization to g levels, the informative fraction of codec
comparisons decays as g falls while accuracy on informative pairs
stays at ceiling. Kill: accuracy sags while informative pairs remain
in meaningful number. Committed before `ot12_check.py` executes.**

## Family and knob

- Base consumer = OT-5 v2's smoothest cell, constants unchanged for
  comparability: d = 64, K = 16 unit prototypes, `C(x) =
  softmax(Wx/T)[0]` at **T = 1.0** (measured DF 1.0, accuracy 1.0
  there).
- **The knob:** output quantization — `C_g(x) = round(C(x)·g)/g`
  (nearest of g+1 uniform levels on [0,1]).
- g grid: {∞, 256, 64, 16, 8, 4, 2} — 7 cells.
- Probe, codecs, damage, informative-pair rule: **identical to OT-5
  v2** (`blind_probe` lstsq sketch 80, `check_regime=False` recorded
  as deliberate, 24 operating points, 30 rank-4 equal-trace codec
  pairs at trace 0.01, 2,000 draws, damage = mean squared change of
  the *quantized* output — the output the consumer actually emits;
  a pair is informative iff both the trace-difference sign and the
  measured-damage sign are nonzero). Seed 20260815.
- Descriptive per cell: measured DF (zero-response fraction on 200
  points), recorded, no bar.

## Bars

- **Manipulation check (window):** informative fraction ≥ 0.9 at
  g = ∞ and ≤ 0.5 at g = 2, else VOID (the knob failed, not the
  theory). One re-knob of the g grid is permitted on a VOID; a second
  VOID closes OT-12 as VOID.
- **F1 (curve one — the fraction decays):** informative fraction is
  non-increasing along the grid within a 0.05 per-step tolerance.
- **F2 (curve two — the ceiling holds):** accuracy on informative
  pairs ≥ **0.85** in every cell with ≥ 10 informative pairs.
- **F3 (the frozen kill, verbatim):** no cell with ≥ 10 informative
  pairs and accuracy ≤ 0.6.

Verdict: window, then F1 ∧ F2 ∧ F3, else FAIL. This file is the final
instrument revision for bars; only the g grid may move, once, on a
window VOID. Result: `results/OT12-floor-curves.json`; ledger row
OT-12.
