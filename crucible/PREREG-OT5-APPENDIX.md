# OT-5 instrument appendix — sealed before the run

**Claim frozen in `OT-CRUCIBLE.md` §OT-5: `tr(P_C Σ_δ)` damage-ranking
accuracy degrades monotonically in the consumer's measured differential
fraction along a smooth→selection family. Committed before
`ot5_check.py` executes.**

## The family and the knob

- d = 64; K = 16 unit-norm random prototypes `W`; scalar consumer
  `C_T(x) = softmax(Wx / T)[0]` — smooth margin at high T, indicator of
  "prototype 0 wins" as T → 0.
- Temperature grid: T ∈ {3, 1, 0.3, 0.1, 0.03, 0.01} (6 cells).
- Operating points: 24 draws x ~ N(0, I_d) (shared across cells);
  200 further draws reserved for the smoothness measurement.
- **Measured differential fraction** (the package's own instrument, not
  a theory quantity): `DF(T) = 1 − zero_response_fraction` from
  `readscope.regimes.applicability` evidence (ε = 1e-3, its internal
  64-trial cap, seeded). The knob must actually work: **manipulation
  check** max DF ≥ 0.9 and min DF ≤ 0.3 across the grid, else the run
  is void (not a theory failure).
- Blind operator per cell: `blind_probe(mode="lstsq", sketch_dim = 80
  = 1.25d, eps = 1e-3, check_regime=False)` — **the regime gate is
  deliberately bypassed**, because OT-5's purpose is to measure the
  failure the gate exists to prevent; this is recorded as intentional.
- Codecs: 30 pairs of random rank-4 equal-trace covariances
  (trace = 0.01); ground-truth damage = mean squared output change over
  2,000 draws per codec across the operating points; prediction =
  `sign(tr(P̂_T (Σ_A − Σ_B)))`; accuracy(T) = matched share of 30.
- Seed 20260815 throughout.

## Bars

- **V1 (smooth end):** accuracy ≥ **0.90** in every cell with
  DF ≥ 0.9.
- **V2 (selection end):** accuracy ≤ **0.70** at the sharpest cell
  (chance is 0.5; n = 30 pairs).
- **V3 (monotone coupling — the frozen claim):** Spearman correlation
  of accuracy(T) with DF(T) over the six cells ≥ **0.80**.
- **V4 (the frozen kill guard):** no cell with DF ≥ 0.8 and accuracy
  ≤ 0.6 — the metric must not fail while the consumer is still
  measurably differential.

Verdict: manipulation check, then V1 ∧ V2 ∧ V3 ∧ V4, else FAIL.
Result: `results/OT5-regime-boundary.json`; ledger row OT-5.
