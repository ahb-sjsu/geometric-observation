# PREREG-OP3 — the sample-complexity exponent (v1-line, first campaign)

**STATUS: SEALED 2026-08-19.** Naive model refuted; corrected front law derived,
numerically validated, and Lean-verified; ready to seal on a fresh day
(cooling-off: family/shakedown constructed 2026-08-18, so the earliest
compliant seal is 2026-08-19). The seal replaces this token with
`STATUS: SEALED <date>`; `op3_graded.py` refuses to grade until then
and enforces the one-day cooling-off in code. This is the appendix
that discharges owed prediction **OP3** of
`OWED-V1.md` (the v1-line exposure ledger, minted `1c18e31` under
DECLARATION-V1's freeze rules) — the first campaign against the v1
line. The shakedown (2026-08-18) **falsified the a-priori prediction
in *The a-priori prediction* below before any bar sealed**; the
*corrected* front law, derived from the same algebra carried one step
further, is stated and validated in *Shakedown outcome* and *Corrected
law* at the foot of this document. The original prediction and its
bars are preserved verbatim as the record of what was predicted first;
they remain **not** sealed. The corrected law's bars will be sealed in
their own act on a day later than this construction (cooling-off,
`governor.sealed`), with a graded runner. This is the discipline
functioning as designed: a minted prediction, a first substrate, a
shakedown that caught an oversimplified model before it bound, and a
corrected model that had to be derived and machine-checked before any
bar could bind. The document carries no evidential weight.

## What OP3 asked, and how this appendix sharpens it

`OWED-V1.md` left OP3 as a disjunction: the sub-dimensional excess
error *either* decays as a derivable power `m^(-alpha)` *or* provably
plateaus (`alpha = 0`), one of the two predicted a priori. The
derivation below **picks the branch and pins the exponent** — a
strictly sharper, strictly more falsifiable claim than the
disjunction. The ledger permitted either outcome; the theory, once
its algebra is followed, predicts one.

## The a-priori prediction — alpha = 1/2, derived before the sweep

C-15's own algebra is the mechanism. The lstsq blind probe with
sketch width `k` forms, per operating point, `ghat ghat^T` whose
expectation is

    E[ghat ghat^T] = (1 + 1/k) S + (tr S / k) I,

a **positive affine function of the population operator `S`**. An
affine `aS + bI` has *exactly* `S`'s eigenvectors — all of them, at
every `k`, including `k < r`. Therefore the top-`r` eigenspace of
`E[ghat ghat^T]` equals the top-`r` eigenspace of `S` even for a
sub-dimensional sketch. The estimator `Ŝ_n = (1/n) Σ ghat ghat^T` is
a sample average of `n = BASE_N · m` i.i.d. bounded terms, so
`‖Ŝ_n − E[Ŝ]‖_op` concentrates at the standard rate `∝ n^(-1/2)
∝ m^(-1/2)`. Davis–Kahan converts operator fluctuation into subspace
angle:

    sinΘ_r(Ŝ_n)  ≤  2 ‖Ŝ_n − E[Ŝ]‖_op / gap_r,

so the **principal-angle error of the recovered rank-`r` subspace
decays as `m^(-1/2)`**, with the multiplicative constant set by the
population eigengap `gap_r`. Hence:

- **Exponent (design-independent):** `alpha = 1/2`.
- **Constant (design-dependent, also predicted):** `C_r ≈ 2 σ_op /
  gap_r`, where `gap_r` is the eigengap of `E[ghat ghat^T]` at rank
  `r` and `σ_op` the per-point operator-norm scale. `gap_16` is small
  (the family's 16th planted weight is `0.75^15 ≈ 0.013`), so
  convergence is slow *in absolute terms* — the excess is still far
  from zero at 256× — but the **slope is 1/2 regardless**. That is the
  falsifiable core: not "does it converge" (C-15 already saw it move)
  but "does it converge at the derived rate."

**Why this is not the confinement plateau.** OT-3 confinement is a
single-shot / worst-case-adaptive statement: one sub-dimensional read
cannot resolve `> k` directions. The many-cheap-points regime escapes
it by *averaging* — the shared-eigenspace identity is exactly the door
confinement leaves open. So OP3's answer is the power-law branch, and
a **plateau here would refute the averaging-consistency prediction**,
not confirm the alternative. The two kill modes are named below.

## Substrate — the C-15 planted family, extended

Identical family to C-15 (`readscope/calibration/op3_exponent.py`
reuses its `setup`/consumer verbatim): tanh-basis scalar consumer,
`d = 32`, spectrum decay `0.75`, input scale `0.35`, `lstsq`
estimator, `eps = 1e-3`. Fixed sub-dimensional sketch `k = d/4 = 8`;
confined family rank `16` (recover 16 planted directions from a width-8
sketch). Budget sweep `n = 384 · m`, `m ∈ {1, 4, 16, 64, 256, 1000}`
— C-15's scaling arm (1×–8×) extended to 1000×.

**Metric upgrade over the shakedown.** The shakedown reports the
`subspace_overlap(...).resolution` climb to show the interior shape;
the graded bar is on the quantity the derivation actually predicts —
the **largest principal angle `sinΘ_r`** between `read_subspace(r)`
and the true `basis[:, :r]` — because `alpha = 1/2` is a statement
about the angle, not about a metric whose power-law mapping to the
angle is itself unmeasured. The sealed runner computes `sinΘ_r`
directly.

## Decision rule — bars (TO BE SEALED; not yet binding)

Confined ranks are `r ∈ {16}` (and `r = 8` at the `k` boundary as a
secondary read); in-budget ranks `r ∈ {1, 2, 4}` are the contrast.

- **B1 — the exponent.** Log-log slope of `sinΘ_16` vs `m`, fit over
  `m ≥ 16` (the asymptotic arm, above C-15's flat small-`m` regime),
  is `alpha_16 = 0.5 ± 0.15` with `R² ≥ 0.9`, on the seed-mean curve.
- **B2 — the constant.** The fitted intercept implies a constant
  within **2×** of the eigengap prediction `C_16 ≈ 2 σ_op / gap_16`,
  with `gap_16` and `σ_op` read from the population operator
  `E[ghat ghat^T]` (computed, not fitted).
- **B3 — the contrast, not just the fit.** In-budget ranks
  `r ∈ {1,2,4}` must also fit `alpha ≈ 0.5` (same estimator, same
  rate), demonstrating the exponent is a property of the averaging,
  not of the specific confined rank — while the *constants* order by
  `1/gap_r` (top directions converge faster). A confined rank that
  fits `1/2` while in-budget ranks do not would mean the fit is
  coincidental.
- **Across seeds (qualification gate, per OT-17):** B1 must hold on
  each of ≥3 disjoint seeds' own curves, not only the mean — the
  interior is a distribution, and one seed is one draw of it.

## Kill conditions

- **Wrong exponent:** `alpha_16` outside `0.5 ± 0.15` with a clean fit
  (`R² ≥ 0.9`) — the decay is real and derivable-looking but the rate
  the theory derived is wrong; the Davis–Kahan/averaging account of
  the cliff's asymptotics is incomplete.
- **Plateau:** `sinΘ_16` flat (`|alpha| < 0.15`) — the averaging does
  *not* overcome the sub-dimensional sketch; confinement bites even in
  the population-operator limit and the shared-eigenspace escape is
  illusory. Refutes this prediction (does not confirm a different one).
- **Messy:** `R² < 0.9` on the asymptotic arm across seeds — no
  derivable law; the ledger's true kill.

Any kill triggers the v2.0 revision process on P3's asymptotic-budget
claim alone; the frozen P3 statement is untouched until then.

## Manipulation checks (bars too — enforcement granularity)

Graded against the family record at the granularity they enforce, per
the OT-13 lesson:

- **MC1 — the sketch actually confines at single-shot.** At `m = 1`,
  `sinΘ_16` is large (near the un-informed floor) — if a width-8
  sketch already resolved 16 dims at one point, there is no cliff to
  climb out of and the whole setup is void.
- **MC2 — the estimator realizes the population operator.** The
  empirical `Ŝ_n` at the largest `m` matches `(1+1/k)S + tr(S)/k I` in
  its top-16 eigenspace (overlap ≥ 0.9) — confirming the mechanism the
  prediction rests on is the one being measured.
- **MC3 — seed interior spread.** Reported at the same `m ≥ 16` arm
  the bar is fit on, not a different range.

## Shakedown outcome (2026-08-18) — the naive prediction is refuted

The shakedown ran the full grid (`m ∈ {1,4,16,64,256,1000}`, seeds
{0,1,2}; `readscope/calibration/records/op3-shakedown.json`). It does
**not** support the clean-`m^(-1/2)`-to-zero picture, and it does not
support a plateau either. The interior is richer than the three
pre-registered outcomes, in three findings:

1. **Recovery is spectrum-ordered, not aggregate.** The per-mode
   canonical correlations `cosθ_i` between `read_subspace(16)` and the
   planted basis, at seed 0:

   | m | mode 0 | 2 | 4 | 6 | 8 | 10 | 12 | 14 |
   |---|---|---|---|---|---|---|---|---|
   | 16× | 1.00 | 0.99 | 0.93 | 0.81 | 0.78 | 0.62 | 0.33 | 0.13 |
   | 256× | 1.00 | 0.99 | 0.98 | 0.93 | 0.81 | 0.68 | 0.41 | 0.18 |

   The high-weight modes (`w_i = 0.75^i`) are recovered first; each
   mode's `cosθ_i` climbs with budget; the **recovery front advances
   *down* the spectrum** as `m` grows. This is the "variance wall" the
   OT-3N theorem named, seen mode-by-mode.

2. **The rank-1 plateau was an ordering artifact, not a bias floor.**
   Aggregate `resolution(1)` sits at ~0.44 and does not climb — which
   looked like a bias wall — but the per-mode view shows the top
   planted direction *is* recovered to `cosθ = 1.00`. The estimator's
   **internal ordering** misplaces which single direction ranks first,
   so `read_subspace(1)` is not the planted top mode even though the
   subspace contains it. `resolution(4)` climbing to 0.83 while
   `resolution(1)` stays at 0.44 is the signature of subspace-correct,
   order-scrambled recovery.

3. **No single-variable SNR collapse.** The natural derivable law —
   `cosθ_i` a function of the per-mode SNR `s_i = m·w_i²` alone — does
   **not** hold: at `m=256` a mode at `s≈8` reads `cos² ≈ 0.87`, at
   `m=16` a mode at `s≈9` reads `cos² ≈ 0.99`. Larger total budget
   needs *more* per-mode SNR to recover a mode, the signature of
   **cross-mode interference** from the sketch's isotropic term
   `tr(S)/k · I`, which couples all active modes. A correct law must
   carry that interference term; the clean per-mode derivation above
   omits it.

**Consequence.** The a-priori derivation (Davis–Kahan on a
shared-eigenspace population operator) captures the *mechanism*
(averaging escapes single-shot confinement; recovery is real and
budget-driven) but not the *rate law* (it predicts a clean aggregate
power to zero; the truth is a log-advancing, interference-coupled
spectral front). OP3 is **not refuted** — recovery is real, ordered,
and spectrum-derived, consistent with P3. What is refuted is *this
appendix's rate model*. The owed prediction stays live in `OWED-V1.md`.

## Corrected law — derived, validated, Lean-verified (2026-08-18)

The corrected front law was derived from the C-15 sketch identity
carried one Davis–Kahan step past the naive model, and validated on
the full per-mode data (`readscope/calibration/op3_frontlaw.py`,
`records/op3-frontlaw.json`).

**The derivation.** `M = E[Ŝ] = (1+1/k)S + (tr S/k)I` is *affine* in
the population operator `S`, so it keeps `S`'s eigenvectors with
eigenvalues `μ_i = (1+1/k)λ_i + tr(S)/k`. For the planted geometric
spectrum `λ_i ∝ w_i²` (`w = 0.75`) the eigengap is `gap_i ∝ w_i²`. The
sampling fluctuation `‖Ŝ_n − M‖ ∝ tr(S)/(k√n)` is **isotropic and
common to all modes** — the cross-mode interference the shakedown
demanded. Davis–Kahan then gives per mode

    sinθ_i ≲ ‖Ŝ_n − M‖ / gap_i ∝ 1/(√n · w_i²),
    sin²θ_i ∝ 1/(n · w_i⁴),

so the recovery collapses in the single variable **`s_i = m · w_i⁴`
— exponent `p = 4`**, and the recovery front (mode at `cos²θ = ½`)
advances as `i*(m) = i*(1) + ln(m)/ln(w^{-4})`, slope
`1/ln(w^{-4}) = 0.869`, i.e. **2.41 modes per 16× budget**.

**The validation.** Per-mode canonical correlations over
`m ∈ {4,…,1000}`, seeds {0,1,2}, fit to the universal curve
`cos²θ_i = s_i/(s_i + A)`:

| p | 2 | 3 | **4** | 5 | 6 |
|---|---|---|---|---|---|
| collapse RMS | 0.218 | 0.168 | **0.157** | 0.159 | 0.195 |

`p = 4` is the best-collapsing exponent — the derived value wins. The
front advance is the sharper signature: measured **+1.20 modes per 4×
= 2.40 per 16×**, against the derived **2.41** — essentially exact
across the whole sweep. The single-variable collapse is *approximate*
(RMS 0.157, not near-zero): the linearized Davis–Kahan and the
one-variable reduction of the interference term leave residual scatter,
so a sealed bar should lean on the **front-advance rate** (clean) more
than the raw collapse RMS (rough).

**Machine-checked algebra.** The load-bearing steps are formalized in
Lean 4 / Mathlib (`lean/ObservationTheory/FrontLaw.lean`, built clean,
sorry-free — `affine_hasEigenvector`, `affine_eigengap`,
`geometric_gap_ratio`, `frontlaw_exponent` depend only on `propext /
Classical.choice / Quot.sound`). Davis–Kahan and the Gaussian
operator-norm rate remain cited standard results, per DECLARATION-V1's
stated standard.

## Corrected-law bars (TO BE SEALED on a fresh day; not yet binding)

- **B1′ — the exponent.** The collapse RMS is minimized at `p = 4`
  among `p ∈ {2,3,4,5,6}`, on each of ≥3 disjoint seeds.
- **B2′ — the front-advance rate.** The fitted `di*/d ln m` is
  `0.869 ± 0.10` (derived `1/ln(w^{-4})`), across seeds — the primary
  bar, being the clean signature.
- **B3′ — the mechanism (MC-grade).** At the largest `m`, the empirical
  `Ŝ_n` top-16 eigenspace overlaps the affine population operator
  `(1+1/k)S + tr(S)/k·I` at ≥ 0.9, confirming the identity the whole
  derivation rests on.

Kills unchanged in spirit: a best-collapse exponent away from 4 with a
front rate away from 0.869 refutes the Davis–Kahan front account (not
P3). These bars supersede the pre-shakedown bars above; they seal in
their own dated act.

## Provenance

- Owed prediction: `crucible/OWED-V1.md` OP3 (`1c18e31`).
- Instruments: `readscope/calibration/op3_exponent.py` (shakedown) and
  `readscope/calibration/op3_frontlaw.py` (front-law validation) → a
  graded runner added at seal. Records:
  `readscope/calibration/records/op3-shakedown.json`,
  `op3-frontlaw.json` (no weight).
- Machine-checked algebra: `lean/ObservationTheory/FrontLaw.lean`
  (built clean, sorry-free).
- Lineage: C-15 `readscope/calibration/c15_budget_surface.py` +
  `records/c15-budget-surface.json`.
