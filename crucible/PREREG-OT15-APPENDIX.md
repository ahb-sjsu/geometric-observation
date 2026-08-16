# OT-15 instrument appendix — P2's forward transfer via moment-matched probing

**STATUS: SEALED 2026-08-16. Drafted unsealed 2026-08-15 at
`afdae4d`; sealed the following working session per the rate-limit
rule, with no edits to bars, constants, or claim between draft and
seal. Runner: `ot15_check.py`. Result: `results/OT15-moment-transfer.json`.**

## Claim under test

P2 v0.2 (readscope `PRINCIPLES.md`), the owed prediction: **forward
transfer** — the operator under the real activation measure is
predicted from probes the instrument places itself, using only
low-order statistics of that measure. The estimator is F3's
correction of OT-9: **direct moment-matched probing** — draw the
probe's operating points from N(μ̂, Σ̂) fitted to a limited sample of
real activations, and probe there. No importance weights anywhere;
the ESS pathology that killed OT-9 cannot occur by construction. The
residual error is the fitted family's inadequacy — the honest content
of the transfer claim.

## Family (cited, with its budget requirement)

F3 per `FAMILIES-CRUCIBLE-3.md` and `results/FAM3-shakedown.json`
(stage-1 interior DEMONSTRATED: reductions 1.9×/2.2×/2.6× at budgets
24/48/96, fit-64 moments nearly free). The family record requires
**n ≥ 48**: at n = 24 the reduction is capped by the sampling floor,
not the method. This appendix grades at n = 48 and records n = 96.
This is stage 2 of the family's validation ladder: real heads,
moments fitted from limited key samples.

## Substrate and instrument

Twelve real Llama-3.2-3B attention heads (`armH_data/`, layers
7/14/21 × heads 0–3; Q 24×128, K 192×128), consumer = attention mass
at key position 96 (the OT-1/OT-9 consumer, `consumer_single`).

- **Reference target** (per head): `jacobian_probe` at 96 real keys,
  160 directions, eps 1e−3 — the same committed reference OT-9
  graded against (lesson 2: consistency with the program's record).
- **Fitting sample:** 64 keys drawn without replacement per trial.
  **Both arms see only this sample** — the iso arm takes its mean and
  scalar spread (μ₆₄, 1.5·sd₆₄, the OT-9 synthetic-measure form), the
  matched arm takes μ₆₄ and the ridge-regularized covariance
  (Σ₆₄ + 0.1·(tr Σ₆₄/d)·I). Equal information, equal probe budget,
  shared probe-direction rng; only the geometry differs. That
  difference is exactly F3's claim.
- **Arms** at n = 48 probe points per trial: `iso` — points from
  N(μ₆₄, (1.5·sd₆₄)²·I); `matched` — points from N(μ₆₄, Σ₆₄+ridge).
  Error = relative Frobenius distance to the reference target.
  10 trials per head (fresh fitting sample and probe points each
  trial); per-head score = median over trials.
- Constants: SEED 20260817, D 128, K_DIRS 160, EPS 1e−3, P_STAR 96,
  N_TARGET 96, N_FIT 64, N_PROBE 48 (graded) and 96 (recorded),
  N_TRIALS 10, RIDGE 0.1.

## Manipulation checks (any failure → VOID)

- **MC1 (room to improve):** median iso error across heads ≥ 0.05 —
  the OT-9 floor, kept.
- **MC2 (estimator health):** every fitted covariance admits a
  Cholesky factor after ridge; fitting samples drawn without
  replacement; both arms consumed identical budgets (asserted
  structurally).

## Bars

- **B1 (per-head wins):** matched beats iso (per-head medians) on
  ≥ 10 of 12 heads at n = 48.
- **B2 (magnitude):** median over heads of the error ratio
  iso/matched ≥ 1.5 at n = 48. (Stage 1 showed 2.0× with fitted
  moments; real-measure non-Gaussianity is expected to eat some of
  that — the bar prices it at a third.)

**PASS = B1 ∧ B2** (given no VOID). Any bar failing → FAIL as
executed.

## Recorded ungraded (no evidential weight, by prior declaration)

The n = 96 sweep (does the gap widen with budget?); a full-sample
arm (moments from all 192 keys) locating how much of the residual is
the 64-sample fit versus the Gaussian family itself; and per-head ESS
of nothing — there are no weights, which is the point.
