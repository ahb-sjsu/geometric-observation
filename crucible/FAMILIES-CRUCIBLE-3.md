# Families for a Third Crucible — designed against the recorded debts

**2026-08-16. Per `OT-CRUCIBLE-2-VERDICT.md`: the next campaign starts
with families, not principles. This document designs one family per
recorded debt, states each family's *interior requirements* — the
evidence a shakedown must show before any appendix may bind bars to
it — and the rule that governs the cadence: shakedowns today,
seals another day, bars never on the day of first construction.**

## F1 — the log-spread signal family (P5's debt, from OT-12)

**Defect it answers:** OT-12's family had one global response scale,
so output quantization crossed every pair's signal at once — a cliff
with no interior, and no way to separate "the floor law has a degraded
band" from "the damage estimator is quantization-contaminated"
(the ungraded 0.633 band).

**Design:** keep OT-12's consumer and knob; make the *codec pairs*
heterogeneous — pair energies log-spread across three decades
(trace ∈ logspace(1e-4, 1e-1, 30)). At any quantization step, some
pairs sit far above their floor and some below: the informative
fraction decays *smoothly* in the step by construction.

**The estimator-noise budget (the separability OT-12 lacked):** per
pair, a bootstrap over damage draws yields the measurement std of the
damage difference; define the **margin** m = |ΔD|/σ_meas. The floor
law's eventual claim becomes conditional and separable: accuracy at
ceiling for pairs with m ≥ 3 at every step (a sag there is the law
failing); pairs with m < 3 are the estimator's noise regime (a sag
there is measurement). The 0.633 band question becomes decidable.

**Interior requirements (shakedown must show, committed, before any
seal):** ≥ 4 steps with informative fraction strictly in (0.10, 0.90);
at every such step, the margin distribution straddles 3 (≥ 20% of
informative pairs on each side).

## F2 — the mixture-drift dial (P4's debt, from OT-11)

**Defect it answers:** book identity gave one cluster jump — drift
0.81–0.87 with no gradient, so damage-tracks-drift had no field, and
the stale-vs-fresh spread (4%) was near the noise.

**Design:** drift as a *population mixture*, which is also what real
query streams do: stratum τ draws its query set as (1−τ)·N from the
t₀ pool (Czech book) and τ·N from the far pool (German books),
τ ∈ {0, 0.125, …, 1.0}. `P̂(τ)` interpolates between the two query
geometries, so measured subspace drift rises smoothly in τ by
construction — a dial, not a step. Sensitivity repair: bit budget
lowered to 2 bits/dim so allocation differences bite harder.

**Interior requirements:** measured drift(τ) monotone in τ (Spearman
≥ 0.9 against τ, descriptive), range ≥ 3× between smallest and
largest nonzero-τ strata, ≥ 4 strata between 10% and 90% of max
drift; and resolvability — at τ = 1, stale-minus-fresh damage ≥ 3×
the query-resampling std of the damage estimate.

## F3 — the annealed transfer estimator (P2's debt, from OT-9)

**Defect it answers:** single-shot importance weighting between a
synthetic and a fitted measure collapses to ESS ≈ 1 in 128-d; the
"correction" was one point, not the law.

**Design — and a correction made in the designing:** OT-9's
importance weighting was needlessly indirect. The probe may evaluate
the consumer at *any* point it synthesizes, so when the fitted target
measure is samplable (a Gaussian is), the transfer estimator is
**direct moment-matched probing**: draw the probe's operating points
from `N(μ̂, Σ̂)` (moments estimated from whatever activation
statistics are available) and probe there. No weights, no ESS
pathology — the estimator OT-9 should have been. The residual error is
exactly the fitted family's inadequacy (non-Gaussianity of the true
activation measure), which is the honest content of the transfer
claim. Annealed reweighting is reserved for the case the fitted
family cannot be sampled, and is out of scope until such a case is
named.

**Validation ladder (before any real head):** stage 1, planted
synthetic where the target `E_{D_a}[A]` is computable by brute MC
(the OT-2 two-feature consumer) — moment-matched probing must beat
iso-Gaussian probing by ≥ 2× there or the design never advances;
stage 2, real heads with moments fitted from limited key samples.
**Interior requirements:** stage-1 error reduction ≥ 2× at the probe
budget (n = 24 points); the reduction must persist when the fitted
moments are themselves estimated from ≤ 64 samples.

## What is deliberately NOT here

No bars, no thresholds destined for appendices, no verdict language.
When the shakedowns above are committed and their interior evidence
stands, appendices may be sealed **no earlier than the following
working session**, citing this document and the shakedown records.
P1 and P3 carry no debts and are not re-tested by these families.

---

## Shakedown status (2026-08-16, committed with the runs; no evidential weight)

**F1 — interior DEMONSTRATED** (`results/FAM1-shakedown.json`): with
pair energies log-spread over three decades, the informative fraction
decays smoothly over quantization steps 30×–1000× the reference rms —
four steps strictly inside (0.10, 0.90), every one with the margin
distribution straddling m = 3 on both sides. The decisive band for a
future appendix is steps ∈ [30×, 1000×]; a finer log grid there is the
seal-time refinement.

**F3 — interior DEMONSTRATED at n ≥ 48** (`results/FAM3-shakedown.json`):
moment-matched probing beats iso probing 1.9×/2.2×/2.6× at probe
budgets 24/48/96, with 64-sample fitted moments costing almost nothing
(1.8×/2.0×/2.6×). At n = 24 the reduction is capped by the sampling
floor, not the method — any appendix must budget n ≥ 48. The estimator
OT-9 should have been.

**F2 — interior NOT demonstrated; redesign required**
(`results/FAM2-shakedown.json`): the mixture dial saturates — 12.5%
admixture already rotates the top-8 subspace to drift 0.61, the curve
is non-monotone (Spearman 0.5 vs τ), range 1.6× — and the staleness
lever does not move retrieval damage resolvably at 2 bits/dim
(stale − fresh = −0.010 against resample noise 0.009). Named candidate
fixes for the next session, none tried tonight per the rate-limit
rule: (i) a smoother drift functional (normalized operator Frobenius
distance or trace-mispricing, not top-8 subspace affinity) and more
probe cells against estimator noise; (ii) log-spaced τ near zero
(the action is all below τ = 0.125); (iii) a stronger damage lever
(harder quantization, or margin-weighted rank damage). P4's test
remains blocked on F2; sealing anything against tonight's F2 is
forbidden by this file.

## F2 redesign trail (v2, v3 — 2026-08-16)

**v2** (`fam2_shakedown_v2.py`): all three recorded fixes applied and
the interior still failed — because the *probe estimator*, not the
dial, was the confound: a 24-cell blind probe of a 768² operator has a
~0.5 relative-Frobenius noise floor, burying every stratum except
τ = 1 (drift read 0.57 at τ = 0.01, which no mixture geometry can
produce).

**v3** (`fam2_shakedown_v3.py`): the dot consumer's operator is
analytic (gradient = the query), so the family's intrinsic dial was
qualified directly. **Interior DEMONSTRATED in the qualified
configuration:**

- **Dial** — τ = 0 reference fixed as the *full* cs query pool,
  German-side draws only: drift 0.039 → 0.657 across τ = 0.01 → 1,
  Spearman **1.000**, range **16.9×**, 5 interior strata, all 7
  nonzero strata above 2× the sampling floor.
- **Lever** — 1 bit/dim, analytic operators, honestly-varying 250-of-
  500 eval subsamples: stale 0.550 vs fresh 0.107 top-10 damage,
  **+72.5×** noise; top-1 **+37.0×**. Sign and magnitude both
  decisively resolvable.

**Caveats that bind any future appendix:** (i) qualification used
analytic operators — a sealed test either declares the analytic
operator as its instrument (legitimate for the dot consumer) or must
budget blind-probe cells until estimator noise sits below the dial
signal (24 cells demonstrably does not); (ii) the N_Q = 400 arm is
invalid (bootstrap pollution from the 100-item cs pool) — the
reference must be the full fixed pool; (iii) eval-noise estimates must
use proper subsamples (drawing a full pool makes the noise zero by
construction — two degenerate zeros were caught and fixed in v3's own
runs, both recorded in the JSON history).

With this, all three families hold demonstrated interiors and P4's
test is unblocked. Appendix seals: next working session at the
earliest, per the rate-limit rule.
