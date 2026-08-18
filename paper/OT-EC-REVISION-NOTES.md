# Revision Notes — Observation Theory for Estimation and Control

**Date:** 2026-08-18. Actionable edits for
`paper/Observation Theory for Estimation and Control.docx`, following the
prior-art sweep (`PRIOR-ART-SWEEP-estimation-control.md`) and the Lean
formalization (`lean/ObservationTheory/WeightedMeanInvariance.lean`).

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
- **Balanced truncation / FWBT** (Enns 1984): for linear consumers the
  output-weighted observability Gramian is the dynamic P_C — say so.
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

### 4.1 Proposition 1 — add the state-dependence caveat (now machine-checked)
Prop 1 holds for FIXED P. For a nonlinear consumer, P_C(x) depends on x, and
the optimal estimate is **no longer the posterior mean** — a fact worth stating
both as a caveat and as an opportunity (consumer geometry can change the
estimator itself, not just resource allocation). The Lean formalization
(`weighted_mean_invariance`) also shows the proposition needs *weaker*
hypotheses than the prose states: only `∀v, 0 ≤ vᵀPv` and weights summing
to 1 — neither symmetry, PSD structure, nor nonnegative weights.

### 4.2 Greedy guarantees for V_C-based selection (§6, Campaigns 2/4)
`tr(P_C ΔΣ)` objectives are **not supermodular in general**
(Jawaid–Smith, Automatica 2015 counterexamples cover trace objectives);
greedy selection loses its constant-factor guarantee. Either prove conditions
under which V_C-greedy retains approximation bounds (candidate standalone
result), or route through approximate-supermodularity machinery
(Chamon et al.) / convex relaxations (Joshi–Boyd).

### 4.3 Threshold consumers break the local metric — and the FSO exemplar is one (§13/§14)
The exemplar's endpoints (BER, outage) are threshold-like; near the cliff the
Hessian-based G is degenerate or explosive. Add a robustified read operator:
an **uncertainty-averaged** P̄_C = E[∇D over the estimator's ellipsoid] rather
than the point Hessian. This is both the fix and a contribution.

### 4.4 Probing cost must enter the resource budget (§8/§12)
Black-box recovery and trajectory-dependent re-probing consume exactly the
resources OT allocates. Campaigns should account probe cost explicitly
(probe-vs-exploit), or a reviewer will note the geometry arrives "for free."

### 4.5 Campaign baseline upgrades
- Campaigns 2/4: where an analytic model exists, the baseline must include the
  Riccati/VoI-derived weight — not just hand-tuned or isotropic. OT should
  *match* the analytic weight where it exists and *win* where it doesn't.
- Campaign 3 (blind recovery → scheduling) is the flagship: no prior work found
  runs probed-consumer-metric → sensor scheduling.
- Campaign 5: sweep confirms the FSO gap on current evidence, with an explicit
  caveat that SPIE proceedings need a targeted pass before asserting the gap
  in print.
- Flagship framing overall: aim the program at consumers that are hard to
  hand-model (learned stacks, physical links, third-party systems) — where
  black-box recovery is *necessary*, not convenient.

### 4.6 Anisotropic staleness (§10) appears open
No found work weights staleness by task-relevant directions of state
uncertainty; nearest is VoI's analytic quadratic form. This subsection may be
closer to a standalone contribution than the paper currently treats it.

## 5. Lean status and charter accounting

`lean/ObservationTheory/WeightedMeanInvariance.lean` machine-checks
Proposition 1 (discrete form, weakened hypotheses) and the §5 rank-one
identity `V_C = (gᵀΣh)²/(hᵀΣh + r)`. Build: Lean v4.32.2 / Mathlib v4.32.2,
`lake build` clean on Atlas 2026-08-18 (8659 jobs, zero errors, zero `sorry`).
Per CHARTER R-IND: the kernel check is conclusion-grade mechanical
verification; a `[proved]` ledger row still requires the fresh-context
derivation-grade pass by the program's own process. No ledger rows were added
by this revision pass.
