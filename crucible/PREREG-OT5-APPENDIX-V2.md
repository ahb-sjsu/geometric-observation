# OT-5 instrument appendix v2 — sealed before the v2 run

**Supersedes v1 after its manipulation-check VOID (`results/
OT5-regime-boundary.json`, committed as executed): the temperature grid
never reached the selection regime as the package's instrument defines
it. In float64, `softmax` responses stay exactly nonzero until the
score gap over T approaches ~700, so at T = 0.01 the measured DF was
still 0.98 — and the trace metric was still predicting at 0.93–1.00,
consistent with the frozen claim (high DF → metric works). The knob,
not the theory, fell short. Two changes; claims untouched.**

1. **Grid extended into genuine flatness:**
   T ∈ {3, 1, 0.3, 0.1, 0.03, 0.01, 3e-3, 1e-3, 3e-4, 1e-4} (10 cells).
2. **Degenerate pairs defined:** at flat cells both trace-difference and
   measured-damage-difference can be exactly zero. A pair is
   *informative* when both signs are nonzero; cell accuracy =
   hits / informative. If a cell has < 10 informative pairs, its
   accuracy is recorded at the operational chance convention **0.5**
   (the metric has nothing to say = a coin flip for the user), and the
   cell is flagged. This prevents both-zero "matches" from spuriously
   crediting the metric exactly where it has gone silent.

All other constants unchanged (d = 64, K = 16, 24 probe points, 200 DF
points, 30 pairs, trace 0.01, sketch 80, seed 20260815). Bars V1–V4 and
the manipulation check unchanged. Result:
`results/OT5-regime-boundary-v2.json`. **Declared final instrument
revision: a v2 manipulation VOID or bar FAIL closes OT-5 accordingly.**
