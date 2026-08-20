# OP3-C desk analysis — the dynamic law re-diagnosed (2026-08-20)

Desk work on committed data only (`readscope/calibration/records/
op3-frontlaw.json`, family seeds {0,1,2}); reproduce with
`crucible/op3c_desk.py`. No seal, no new measurement.

## What OP3-B's fail actually was

The continuous recovered-mass statistic `M(m) = Σᵢ cos²θᵢ` (16 modes)
shows the problem was never just an integer-statistic fragility:

| | measured (family seeds) | γ=1 collapse law predicts |
|---|---|---|
| M(4) | 7.9 – 8.4 | 6.39 |
| M(1000) | 9.1 – 9.8 | 11.18 |
| ΔM(4→1000) | 0.65 – 1.68 | 4.79 |
| rate dM/d ln m | 0.17 – 0.29 | 0.869 |

The measured curve starts **higher** and advances **~4× slower** than
the single-A collapse law implies. Yet the front in *i* is sharp
(that's why B1′ kept passing). Sharp in `i`, flat in `m` means the
**collapse variable is wrong**, not the front picture: the data wants

    s = m^γ · w^(4i),   γ < 1.

## The two-parameter collapse, fitted

`cos²θ = s/(s+A)` with `s = m^γ w^(4i)`: pooled best **γ = 0.30**
(RMS 0.123 vs 0.157 at γ = 1), per-seed best γ = 0.2 / 0.4 / 0.4.
With (γ=0.30, A=2.17e-4) the law now reproduces the measured masses:
M(4) = 8.19, M(1000) = 9.63, ΔM = 1.44, rate = 0.261 — all inside the
measured seed band. The i-front sharpness (p = 4) survives unchanged.

**Amended empirical law:** per-mode recovery collapses in
`m^0.3 · w^(4i)` — the budget enters with an effective exponent ≈ 1/3,
not 1. Equivalently the front advances at `γ/ln(w⁻⁴) ≈ 0.26` modes per
e-fold of budget, ~3× slower than the √n-based derivation.

## What is now owed (the a-priori gap)

The v1-line standard is derivability, so OP3's discharge now owes a
derivation of **γ**. Candidate mechanisms, to be worked before any
OP3-C prereg:

1. **Estimator sample-efficiency.** The lstsq blind probe reuses
   sketch structure across points; if effective independent operator
   samples grow sublinearly in n, the √n fluctuation shrinks as a
   weaker power. The derivation must model the actual estimator, not
   an idealized i.i.d. average (the naive model's original sin,
   repeated one level deeper).
2. **Nonlinear regime of eigenvector convergence.** For transition
   modes the eigengap is comparable to the fluctuation, Davis–Kahan's
   linear regime never holds, and spiked-model results (BBP-type:
   overlap turning on and growing nonlinearly in SNR) predict flatter
   budget-dependence exactly where the front lives.

Both are testable a priori: derive γ from either mechanism, predict it
before the next sweep, then build the OP3-C family. Until γ is derived,
**no OP3-C prereg is drafted** — the previous two acts both sealed
operationalizations ahead of the theory, and the record (OP3 FAIL on
bars, OP3-B FAIL on B3′) says exactly what that buys.

## OP3 campaign ledger (all kept)

1. OP3 (2026-08-19): FAIL — bars miscalibrated against the theory's
   own predictions (authoring class).
2. OP3-B (2026-08-20): FAIL on B3′ — static laws confirmed (p=4
   collapse, recovery level), dynamic advance over-predicted; the
   integer statistic also seed-fragile.
3. This desk act: the dynamic misfit isolated to the collapse
   variable's budget exponent; two-parameter law fits (γ ≈ 0.3);
   γ-derivation owed before a third sealed act.

OP3's owed prediction remains **live**: the collapse structure is
confirmed twice; the budget exponent is measured but not yet derived —
which is precisely the state the v1-line was minted to expose.
