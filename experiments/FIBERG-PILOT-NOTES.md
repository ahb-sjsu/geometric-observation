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
