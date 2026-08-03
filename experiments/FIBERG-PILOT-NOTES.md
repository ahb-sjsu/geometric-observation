# FIBER-G pilots P0/P1 — `[exploratory]`, not claim-bearing

Harness [`fiberg_pilot.py`](fiberg_pilot.py) · seed 20260818 · CPU (Atlas), no NRP.
Per the campaign plan's §11 the pilot's job is to validate estimators, expose
conditioning problems, measure numerical floors and size the resource envelope —
**not** to support a claim. No sealed prereg; no ledger row.

## Why this did not go to NRP yet

P0/P1 are small CPU jobs. NRP carries real friction (OIDC cache/lock dance, pod
policy limits, the standing rule that bursts go through the existing
`burst.submit` NATS flow) and cluster goodwill is finite. Sequencing rule adopted:
**no NRP manifest until a model family survives P1**, because P1 is where the
idea most plausibly dies.

## P1 — the decisive dissociation: occupancy is NOT the force witness ✅

Exact finite-state, no sampling. Two reversible birth-death chains on 40 radial
states, built from detailed balance, sharing **one global conductance scale** so
the comparison is not a time-rescaling artifact:

| | |
|---|---|
| detailed-balance residual | **3.3e-24** and **6.6e-24** — exact to machine precision |
| stationary law | **bit-identical by construction** (the 7.4e-09 gap seen earlier was the eigensolver, not the chains) |
| max\|drift_A\| | 5.19e-03 |
| max\|drift_B\| | 2.08e-02 |
| **max\|drift_A − drift_B\|** | **1.56e-02 = 3.00× max\|drift_A\|** |
| **drift sign differs** | at **32 of 40 states** |

**Identical occupancy, drifts differing by 300% and disagreeing in sign at 80% of
states.** So "the stationary distribution is denser near the source, therefore the
source attracts" is not merely weak — it is *uninformative about the sign of the
force*. This is the Bell lesson (aggregate hub skew was not the generator)
reproduced in exact arithmetic, and it means any FIBER-G arm must witness
**conditional transition moments**, never occupancy. Family A (fiber multiplicity)
is therefore not sufficient on its own; Family B (transition geometry) is where the
content must live.

## P0 — estimator net: partial, with the floors measured (this is the deliverable)

| arm | target | measured | status |
|---|---|---|---|
| P0a projected d-ball, d=30 | −κ(d−3)r/(1−r²) | max rel resid **0.026** | ✅ recovered |
| P0a d=12 | ″ | 0.078, inward | ✅ |
| P0a d=6 | ″ | 0.153, but innermost bin **not** inward | ❌ below floor |
| P0c injected harmonic | +1 | **+0.946** | ✅ |
| P0b injected 1/r² | −2 | **−0.897** | ❌ see below |

**P0a's floor, quantified.** Near-centre drift is κ(d−3)r ≈ 4.5e-05 at d=6, r=0.1
with κ≈1.5e-4, against a per-step radial noise of ≈0.011; at 2e5 samples/bin the
standard error is ≈2.5e-05, so the signal is only **~1.8σ**. The estimator needs
≈10× more samples (or a restricted radial window) at small d. **That number is the
resource envelope the real campaign needs**, and it is the main thing P0 bought.

**P0b's failure is the injection, not the estimator.** The injected drift reached
0.2 per step at r=0.1 against a 0.01 diffusion step, so walkers slam into the inner
cutoff and the conditional moment measures boundary dynamics. The positive control
must be run in the **linear-response regime** (drift ≪ diffusion step) with the fit
window clear of both boundaries. Until it recovers −2, the estimator is not
certified to detect an inverse-square law — so **no FIBER-G arm may claim one yet.**

## Instrument defects found (all mine, all pre-claim)

1. **Detailed balance destroyed by row renormalisation.** `birth_death` rescaled any
   row summing above 1, which silently moved π — while my own print banner said
   "occupancy identical" over a number (2.4e-02) that said otherwise. Fixed with a
   single global conductance scale; residual now 1e-24. The N5 gate caught it.
2. **N5's threshold (1e-9) was below float64 eigensolver precision** for a 40-state
   eigenproblem. The right check is detailed balance plus the *constructed* π, not an
   eigen-extracted one.
3. P0b's injection strength (above) and P0a's sample floor (above).

That is the ninth instrument-side defect this session against zero failed physics
predictions. Standing rule reinforced: **verify the estimator against an exact
target before believing any arm, and never let a print banner assert what the
adjacent number contradicts.**

## Status and what P1's result implies for the campaign

The plan's G-series stands, with one ordering change earned here: **G3 (transition
geometry) should precede G2 (fiber multiplicity)**, because P1 shows fiber
multiplicity alone does not determine even the *sign* of the projected drift.
G4 (conserved defect) remains the arm most likely to produce a "success" that is
really inserted field theory — its gate must be that the mediator's universal
coupling is *derived*, not assumed.

---

# Estimator certification — **PASSED**, and the Jacobian trap is now quantified

Harness [`fiberg_estimator_cert.py`](fiberg_estimator_cert.py) · result
[`GO-fiberg-estimator-cert.json`](../results/GO-fiberg-estimator-cert.json) ·
seed 20260819, 12M steps, CPU, 73 s.

The pilot left the estimator **uncertified** (an injected 1/r² came back as
−0.897). Re-run in the **linear-response regime** — injected drift at 5% of the
diffusion step, fit window [0.30, 0.90] clear of both boundaries, exiting walkers'
steps *recorded* and only their next start resampled:

| injected law | recovered exponent | verdict |
|---|---|---|
| b_r ∝ −r^−2 | **−2.035** | ✅ |
| b_r ∝ −r^−1 | **−0.997** | ✅ |
| b_r ∝ −r^+1 | **+0.990** | ✅ |

All three recovered to better than 0.04, and cleanly separated. **The estimator is
certified to detect an inverse-square law**, so the C1 gate on FIBER-G is lifted.
The earlier −0.897 was entirely the injection strength, not the method.

## The Jacobian trap — a real hazard for this whole research direction

Two radial estimators are **not** the same quantity:

$$\mathbb E[\Delta x\cdot\hat u]=b_r\,dt \qquad\text{vs}\qquad
\mathbb E[\Delta|x|]=b_r\,dt+\frac{(n_{\rm obs}-1)\sigma^2}{2r}dt$$

The second carries a spurious **outward 1/r** term that is pure coordinate
Jacobian. Measured against the analytic prediction it matched to **0.2–0.6%** in
all three arms. Its effect on inference is severe:

| injected law | clean estimator | naive \|x\| estimator |
|---|---|---|
| −r^−2 | −2.035 | **−3.004** |
| −r^+1 (harmonic) | +0.990 | **+2.692** |

So a researcher measuring E[Δ|x|] would report an exponent wrong by a full power,
and — critically — **this spurious term has exactly the 1/r outward form that the
gravity note derives as the "naive entropic force."** At least part of that
much-discussed 1/r term is not a force at all; it is the radial coordinate change.
Any FIBER-G arm, and any entropic-gravity toy model of this kind, must either use
the Cartesian-projection estimator or subtract $(n_{\rm obs}-1)\sigma^2/2r$
explicitly. This is now a standing requirement for the campaign.

## Sample floors for the NRP manifest (measured, not guessed)

At σ = 0.01 with a 5%-of-σ signal, SE per bin ≈ 1.2e−05 and signal/SE ≈ 26–55×.
For a **10σ** determination per radial bin:

| law | N per bin |
|---|---|
| inverse square | 9.6e4 |
| inverse r | 5.9e4 |
| harmonic | 2.5e4 |

With 12 bins that is ~1.2M recorded transitions per configuration for the hardest
law — trivial per job, so the eventual campaign is **bounded by configuration
count, not by per-configuration cost**. That is the resource envelope P0 was
supposed to produce.

---

# G3 locality probe — transition geometry alone produces **no exterior field at all**

Harness [`fiberg_g3_locality.py`](fiberg_g3_locality.py) · result
[`GO-fiberg-g3-locality.json`](../results/GO-fiberg-g3-locality.json) · seed
20260820 · uses the certified estimator.

## The argument, stated before the run

Family B modifies how motion passes among states while holding the state count
fixed. The anti-circularity contract forbids the modification from referencing
distance to the source or direction toward it, so the conductance can only be a
**local** function of the source, c(x) = f(ρ(x)). For a reversible walk with a
uniform stationary law the projected drift is proportional to ∇log c(x), hence to
(f′/f)·∇ρ(x).

Outside the compact support of ρ the density is zero and constant, so **∇ρ vanishes
and the drift is identically zero.** The exterior field is not wrong in exponent.
It does not exist. That is a support argument, not a numerical accident.

## Measured, with a live positive control

| conductance law | drift in the source shell (∇ρ ≠ 0) | drift outside the source |
|---|---|---|
| c = exp(3ρ) | **213.2 σ** | **1.3 σ** (max \|b\| 1.6e−05, SE 1.1e−05) |
| c = 1 + 3ρ | **82.0 σ** | **1.4 σ** (max \|b\| 1.5e−05, SE 1.1e−05) |

The estimator resolves a 213σ signal where the density gradient is nonzero and
sees nothing outside the source. So the exterior null is a bounded measurement
against a demonstrably live instrument, not an absence of sensitivity.

## What this prunes

The campaign had three candidate families. Two are now closed on the evidence
gathered here.

**Family A, fiber multiplicity.** P1 showed two chains with bit-identical
stationary laws whose drifts differ by 3.00× and disagree in *sign* at 32 of 40
states. Occupancy does not determine even the direction of motion, so multiplicity
alone cannot carry the mechanism.

**Family B, transition geometry.** Closed by the support argument above and
confirmed at 1.3σ. Any purely local modification of conductance gives zero
exterior field.

**Family C, conserved defect or flux.** The only route left, and the one the plan
already identified as carrying the highest burden. A long range law requires the
source to modify something that *propagates* away from it. Once a mediator is
sourced by mass and coupled universally to probes, the structure of a field theory
has been assumed rather than derived, so Family C's gate must be that the mediator
and its universal coupling follow from the same microstate architecture that
produces the observed geometry, not from a postulate.

Reducing three families to one is the useful outcome. It is also the plan's own
stated aim, since sprawl was named as the failure mode.
