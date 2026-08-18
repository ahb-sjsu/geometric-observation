# Revision Notes — Observation Theory for Estimation and Control

**Date:** 2026-08-18 · **v2 (final).** Actionable edits for
`paper/Observation Theory for Estimation and Control.docx`, following the
prior-art sweep (`PRIOR-ART-SWEEP-estimation-control.md`), the Lean
formalization (`lean/ObservationTheory/WeightedMeanInvariance.lean`), and the
author's refinement pass of 2026-08-18.

## 0. The revised architecture: three interfaces, not two

The composition `U_C = tr(P_C Σ)` is one of **three** interfaces between OT and
the classical stack, and the paper should be organized around all three:

```
              ⎧ Estimator geometry     — if P_C varies with state, the optimal
              ⎪                          estimate leaves the posterior mean
  P_C(x)  →   ⎨ Resource value         — tr(P_C ΔΣ): the consumer-relative
              ⎪                          value of a measurement / bit / update
              ⎩ Dynamic relevance      — S_C(Δ) = tr[P_C(t+Δ) Σ(t+Δ|I_t)]:
                                         age of operationally relevant uncertainty
```

Interface 1 is opened (not closed) by Proposition 1: the invariance holds for
fixed P, and its failure under state-dependent P_C(x) is where consumer
geometry changes the estimator itself. Interface 2 is the paper's original
spine. Interface 3 is §10's staleness quantity, promoted (see §4.6 below).
This is a considerably bigger program than the original draft's two-question
frame, and the paper should say so.

## 1. Restate the novelty hypothesis as an explicit conjunction (§11)

Suggested replacement for the hypothesis paragraph:

> Each pillar of this hypothesis exists separately in prior art: local
> quadratic task metrics are recovered from black-box decision oracles by
> sampled probing in decision-focused learning (LODL/EGL); consumer-derived
> weights composed with estimator covariances drive prospective sensor and bit
> allocation in LQG sensing co-design, goal-oriented Bayesian OED, VoI
> scheduling, and rate-cost control — in analytic, white-box form. The research
> hypothesis is the conjunction: a downstream consumer's operational metric,
> recovered from the consumer itself under query access only and a declared
> observation distribution, composed with classical estimator uncertainty,
> prospectively predicts and allocates operational resources for consumers
> outside the analytic families, validated out-of-sample at matched budgets on
> the actual consumer. The analytic LQG case is conceded entirely to prior art.

## 2. The access-model triangulation sentence (add to §1 or §8)

> Inverse optimal control recovers objectives from *demonstrations*;
> decision-focused learning differentiates through a *known* consumer;
> Observation Theory probes a *black-box* consumer under a declared observation
> distribution. The three access models are distinct, and only the third is
> available when the consumer is a learned perception stack, a physical link,
> or another party's system.

## 3. New related-work obligations (by name)

- **Functional observability** (§2 must engage it): Darouach 2000 line;
  Montanari–Duan–Aguirre–Motter PNAS 2022. OT §2's linear case C(x)=Lx sits
  inside their subject matter; OT adds metric structure + nonlinear consumers +
  recovery.
- **Balanced truncation / FWBT** (Enns 1984): for a linear consumer z = Lx
  with output metric G, the pointwise OT geometry is P_C = LᵀGL, and the
  output-weighted observability Gramian is its **dynamics-propagated
  accumulated analogue**:

      W_C(T) = ∫₀ᵀ e^{Aᵀt} P_C e^{At} dt.

  Do NOT say the Gramian *is* the dynamic P_C. The correct — and stronger —
  statement is that classical observability geometry *emerges from accumulated
  OT geometry* in the linear case: the Gramian is what the consumer's
  instantaneous read metric integrates to under the flow.
- **Empirical Gramians** (Krener–Ide): concede the probing *methodology*;
  claim only the probed *object* (consumer utility vs plant observability).
- **LQG co-design** (Tzoumas–Carlone–Pappas–Karaman), **VoI**
  (Soleymani–Baras–Hirche–Johansson), **GO-OED** (Attia et al. + 2025 quadratic
  extension), **rate-cost** (Kostina–Hassibi; Tanaka), **goal-oriented
  quantization** (Zou et al.), **task-based quantization** (Shlezinger et al.),
  **LODL/EGL/TaskMet** (decision-focused learning), **LPIPS** (as narrative
  caution: consumer-derived metrics already steer codec allocation in
  practice).

## 4. Technical corrections and additions

### 4.1 Proposition 1 — state-dependence caveat; keep P ⪰ 0 in the main text
Prop 1 holds for FIXED P. For a nonlinear consumer, P_C(x) depends on x, and
the optimal estimate is **no longer the posterior mean** — state this both as a
caveat and as an opportunity (Interface 1: consumer geometry can change the
estimator itself, not just resource allocation).

**Presentation rule:** the main theorem statement keeps the natural
hypothesis **P ⪰ 0** and probability weights. The Lean formalization
(`weighted_mean_invariance`) shows the algebra survives under weaker
hypotheses (only `∀v, 0 ≤ vᵀPv` and weights summing to 1 — no symmetry, no
sign condition on weights), but "weights need not be nonnegative" will
distract control readers when those weights resemble probabilities. Put the
machine-checked weakening in a remark or appendix, cited to the Lean file.

### 4.2 Greedy guarantees for V_C-based selection (§6, Campaigns 2/4)
`tr(P_C ΔΣ)` objectives are **not supermodular in general**
(Jawaid–Smith, Automatica 2015 counterexamples cover trace objectives);
greedy selection loses its constant-factor guarantee. **Do not try to solve
this in the foundational paper** unless a clean sufficient condition drops
out: state the limitation plainly, cite the approximate-supermodularity
machinery (Chamon et al.) and convex relaxations (Joshi–Boyd) as the
available workarounds, and register "conditions for OT-greedy approximation
guarantees" as a **campaign theorem** — a named target, not a claimed result.

### 4.3 Threshold consumers break the local metric — and the FSO exemplar is one (§13/§14)
The exemplar's endpoints (BER, outage) are threshold-like; near the cliff the
Hessian-based G is degenerate or explosive. Define the robustified operator
precisely, as the **belief-averaged read operator**: where the local geometry
exists,

    P̄_C(b) = E_{X∼b}[ J_C(X)ᵀ G(C(X)) J_C(X) ],

where b is the estimator's belief (the posterior over X). For genuinely
threshold/nonsmooth outage metrics no Hessian exists to average — there use a
**finite-perturbation or smoothed operational metric** instead of pretending
one does. This is more than a fix: **belief-relative Observation Theory**
(the read operator as a functional of the belief, not the point) is a
substantial extension candidate, and the paper should flag it as such.

### 4.4 Probe cost enters the optimization, not just the caveats (§8/§12)
Black-box recovery and trajectory-dependent re-probing consume exactly the
resources OT allocates. Elevate this from an accounting caveat into the
policy objective itself:

    min_π  D_C(π) + λ_s·C_sensing(π) + λ_c·C_communication(π) + λ_p·C_probing(π)

This makes the explore/exploit structure explicit and first-class: **when is
another consumer query worth its cost?** The recovered P̂_C has value only
insofar as it changes downstream allocations; the marginal value of a probe is
itself an OT quantity. Campaigns must run under this objective (probe cost on
the same budget line), or a reviewer will note the geometry arrives "for free."

### 4.5 Campaign baseline upgrades; Campaign 3 is the flagship
- Campaigns 2/4: where an analytic model exists, the baseline must include the
  Riccati/VoI-derived weight — not just hand-tuned or isotropic. OT should
  *match* the analytic weight where it exists and *win* where it doesn't.
- **Campaign 3 (blind recovery → scheduling) is the flagship** — the point
  where the pieces stop looking like pre-existing analytic LQG/VoI machinery.
  The killer experiment:

      unknown consumer → query-only recovery of P̂_C → sensor scheduling
                       → held-out real consumer

  at **equal sensing budgets** (probe cost included per §4.4), with an
  **analytic-consumer positive-control arm**: on a consumer whose optimal
  weight is known (LQG/VoI), OT is required to *recover and match* the known
  optimum — not beat it. Matching the analytic optimum blind is the
  calibration proof; winning on non-analytic consumers is the contribution.
- Campaign 5: sweep confirms the FSO gap on current evidence, with an explicit
  caveat that SPIE proceedings need a targeted pass before asserting the gap
  in print.
- Flagship framing overall: aim the program at consumers that are hard to
  hand-model (learned stacks, physical links, third-party systems) — where
  black-box recovery is *necessary*, not convenient.

### 4.6 Anisotropic staleness (§10) — likely its own paper
Define the quantity explicitly:

    S_C(Δ) = tr[ P_C(t+Δ) · Σ(t+Δ | I_t) ]

— the **age of operationally relevant uncertainty**: what "age of
information" becomes when staleness is weighted by the consumer's read
directions rather than by the clock. The sweep found no anisotropic-staleness
formulation; the nearest neighbor is analytic VoI (Soleymani et al.), which is
scalar-LQG. Disposition: **keep S_C(Δ) in the foundational paper as a
conjectural branch (Interface 3), then pursue it as an independent paper.**
It has its own natural venue (AoI/semantic-comms community), its own
baselines (AoI, AoII, VoI), and its own falsifier (does directional staleness
beat age-based scheduling at matched update budgets on a real consumer?).

## 5. Lean status and charter accounting

`lean/ObservationTheory/WeightedMeanInvariance.lean` machine-checks
Proposition 1 (discrete form, weakened hypotheses) and the §5 rank-one
identity `V_C = (gᵀΣh)²/(hᵀΣh + r)`. Build: Lean v4.32.2 / Mathlib v4.32.2,
`lake build` clean on Atlas 2026-08-18 (8659 jobs, zero errors, zero `sorry`).
Per CHARTER R-IND: the kernel check is conclusion-grade mechanical
verification; a `[proved]` ledger row still requires the fresh-context
derivation-grade pass by the program's own process. No ledger rows were added
by this revision pass.
