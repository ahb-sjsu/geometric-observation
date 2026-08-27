# Verification inventory — tit-cr-context

Detailed script inventory and check-level notes for the manuscript
"Tradeoffs Between Rate and Conditional Content with Encoder-Observed
Context". This file carries the material summarized in the manuscript's
Numerical Verification appendix. All scripts and archived run outputs
live in this directory and at the repository of the paper's title
footnote (doi:10.5281/zenodo.21776291).

## Script inventory

- `verify_converses.py` — the author's harness, written alongside the
  proofs. Seventeen checks: seven exact-symbolic (sympy) on the
  determinant identities, the four gradient identities, the linearity
  and closed-form solution of the stationarity system, the
  constraint-to-quadratic reduction with its cofactor, the floor value
  `P(g_f) = -rho^2 tau^2/s`, and the weighted-FOC reduction; nine
  numeric (numpy/scipy) on the closed form vs direct minimization, the
  frontier at alpha in {0, 1/2, 1}, the six values of the
  non-determination corollary, the endpoint excesses, the
  vector-context FOC at r = 2, the clean-boundary (tau = 0) displays,
  the binary tilt-root sign-change scan (729 grid cells), the
  clean-context conditional program vs the determinant bound, the
  quantization convergence I(Yhat; S_Delta) increasing to I(Yhat; S),
  and the binary rate--content frontier (closed forms vs joint-pmf
  evaluation, plus the Fig. 3 caption numbers).
- `verifier_sym_checks.py`, `verifier_num_checks.py` — a separately
  commissioned re-derivation, produced without access to the
  derivations or to the first script, archived with the repository:
  46 symbolic and 46 numeric checks. All pass.
- `verify_go11_m2sys_binary.py` (repository harness) — the
  unconditional Lagrangian bounds for the binary theorem: no convexity
  assumed, reproduction alphabets 2, 4, and 6; worst residual
  3.4e-14.
- `matlab_checks.m` — MATLAB Symbolic toolbox (R2026a), a third
  independent engine alongside sympy: 11 of 11 symbolic checks pass on
  the scalar-instantiation determinant identities of the Gaussian
  exhaustion lemma, the solution of the stationarity system, the
  constraint-to-quadratic reduction identity, and the four gradient
  identities. Run output archived in the script.
- `lean/ObservationTheory/CRContext.lean` (repository) — Lean 4 /
  Mathlib module, builds clean with zero `sorry`. Formalizes: the
  identity P(1) = (D-1) tau^2 and its negativity; positivity of the
  discriminant for 0 < D < 1 and tau^2 > 0 with no hypothesis on
  rho^2; the closed-form root g* satisfying P(g*) = 0 together with
  g* > 1; the identity P(g_f) = -rho^2 tau^2/s; all three anchor
  factorizations of the anchors corollary; the L_R*(D) endpoint
  algebra of the misalignment corollary; the two exact surds of the
  non-determination corollary; and the binary q = 1/2 anchor and the
  R - L chain-rule bookkeeping of the binary theorem with the binary
  entropy kept abstract.
- `plot_frontier.py`, `plot_binary.py` — figure scripts; the frontier
  script re-derives the endpoint excesses R_L* - R_min = 0.0400 and
  L_R* - L_min = 0.0349 bits quoted in the caption.

## Finite-blocklength diagnostic

A finite-blocklength check of the binning step of the discrete
operational theorem is archived with the repository record: in-bin
decoders recover M from (B, S^n) near the predicted bin rate
I(X; Xhat | S) and fail at every bin rate without S^n.

## Scope note

The matrix-general exhaustion lemma, the measure-theoretic steps
(single-letterization, covering and binning, disintegration), the
matrix-convexity lemma, the uniqueness proposition, and the binary
theorem's symmetrization and positivity arguments are verified by
written proof and the numerical harnesses, not by the proof assistant.
