# Runs of `experiments/verify_paper3_rate_identity.py` (the C3 net for `lem:maxdet`'s rate identity)

**What the net tests.** Paper III's rate identity is
R_P(D) = ½ log det Σx − ½ log det Σ⋆(P, D).
The net tests it against channels whose information and distortion are computed from the joint
law. There are three families: product quantizers, skew-rectangle quantizers and Gaussian
channels.

**History.** It was written on 2026-11-21, after VI-46 found that row PAPER-III.b rests on this
identity and that nothing netted it. The harness's docstring gives the criteria and the history.
This file records the runs, and what the review VI-48 found about them, so that the harness can
stay byte-identical to the file that ran.

| Version | Commit | Seed | Output | Outcome |
|---|---|---|---|---|
| 1, attempt 1 | 3073453 | 20261128 | none | **Crashed after 2 s, before any check was computed.** A dead-zone quantizer with a threshold near ±12 had an upper-tail cell whose probability cancelled to 0 in double precision. The fix, a tail-stable difference, was committed as b54ecab before attempt 2. |
| 1, attempt 2 | b54ecab | 20261128 | `PAPER3-rate-identity-v1.json` | **FAIL** (r3), 17 s. r1, r2, r4 and r5 passed. r3's clause "gap ≤ 1e-3 at eps = 1e-3" failed: the largest such gap was 1.7e-2, and the gaps fall at first order in eps. That clause was a wrong expectation, explained in the docstring. |
| 2 | 69c4359 | 20261129 | `PAPER3-rate-identity.json` | **ALL PASS** (r1 to r5), 18.6 s, on Windows with Python 3.12.2, numpy 2.5.2 and scipy 1.18.1. The JSON records the commit, `harness_modified: false` and the harness sha256 `05f0cc04…` (taken over the file with line endings normalized to LF). |

Version 2 made three changes, all informed by version 1's output and all committed before
version 2's first run, on a fresh seed:
- it removed that r3 clause;
- it added low-rate skew cells;
- it changed r3's docstring wording from "R_P(D)" to "R_P(E d)". The History omits this change.

**Reproduction.** VI-48 re-ran version 2 in a scratch copy: 17.6 s, ALL PASS. Every JSON field
matched the committed file except the timestamp, the git fields and the hash. The run emits
scipy `IntegrationWarning`s (roundoff) during the skew quadrature; they are not recorded in the
JSON. The quadrature guards still hold to 2.7e-15.

**Version 2 in numbers.** Some checks below hold by construction for the correct closed form
(VI-48 #5), so on their own they are not evidence for the identity. VI-49 found that two of
them, r3's optimum check and r4's trace check, still fail on a self-consistent formula that is
too low (a water level raised by 0.1% failed them at 1.5e-3 and 1e-3). They therefore guard the
formula's lower side.

| Check | Measured | Bar | Kind |
|---|---|---|---|
| r1, smallest `lem:info` slack, product quantizers | −9.4e-16 | ≥ −1e-9 | real; the smallest values come from trivial channels (H = 0) |
| r1, smallest `lem:info` slack, skew quantizers (two-dimensional) | 0.0164 | ≥ −1e-7 | real |
| r1, skew quadrature guards (worst) | 2.7e-15 | ≤ 1e-8 | guard |
| r2, smallest gap I − R_P(E d), skew quantizers | 0.0435 | ≥ −1e-7 | real, independent of the formula |
| r2, smallest gap, random Gaussian channels | 1.4e-7 | ≥ −1e-9 | real, independent of the formula; one instance, aligned by chance (VI-48) |
| r2, smallest gap over all families | −4.4e-15 (the optimum) | ≥ −1e-9 max(1, R) | the optimum term is an identity |
| r3, the optimum against the formula | 4.4e-15 | ≤ 1e-9 | holds by construction for the correct formula; fails on a too-low one (VI-49) |
| r3, near-optimal Gaussian gaps at eps = 1e-1, 1e-2, 1e-3 (smallest) | 1.6e-4, 6.0e-6, 6.1e-8 | ≥ −1e-9 | a one-sided first-order descent test around the formula's own optimum; see below |
| r3, the same (largest) | 0.92, 0.20, 0.024 | recorded only | |
| r4, min eig(Σx − Σ⋆)/‖Σx‖ and the trace residual | −2.5e-15, 2.9e-15 | ≥ −1e-10, ≤ 1e-9 | feasibility holds by the closed form; the trace check fails on a too-low formula (VI-49) |
| r4, Monte Carlo on 10 instances: worst \|z\| of the distortion and of the covariance | 0.95, 2.3 | ≤ 5 | **identity of the construction** |
| r5(a), formula raised by 1e-2 nats | all 120 optima; 50, 100 and 117 near-optimal channels | at least 1 | **cannot fail**: the optimum catches any raise by algebra. The 6 product catches are all trivial channels; the one other formula-independent catch is a random Gaussian channel aligned by chance |
| r5(b), `lem:info` raised by 0.05 | 13 product (random U), 11 product (aligned), 4 skew | at least 1 product | real, but the gate also counts trivial channels; 18 informative product catches were confirmed after the run (below) |
| r5(c), the "commuting" shortcut: instances caught | 67 | at least 1 | measures where the mutant exceeds the formula. The catches are by the optimum and near-optimal channels; informative channels independent of the formula catch it on 5 instances (VI-48) |
| r5(d), VI-4's bug: instances caught | 67 | at least 1 | likewise; formula-independent catches on 2 instances (VI-48) |
| r5(e), bits for nats: channels catching it | 517 | at least 1 | **cannot fail**, as for (a) |

**The r5(b) split, checked after the run.** A product quantizer with no thresholds has H = 0 and
`lem:info` slack exactly 0, so it "catches" a raised `lem:info` without showing any resolution.
Regenerating version 2's product channels from the seed reproduces the JSON's counts:
- **6 trivial:** 2 random-U and 4 aligned.
- **18 informative product quantizers within 0.05 nats** (11 random-U, 7 aligned), and **4 within
  0.01**.
- **Smallest informative slack:** 0.0050 (random U) and 0.0142 (aligned).
- **All 4 skew catches are informative.**

VI-48 reproduced this split.

## What the net can and cannot catch (after VI-48)

- **Its own power gates do not demonstrate its power.** The formula's own optimum passes all five
  r5 gates, and (a) and (e) cannot fail at all.
- **The power was shown after the fact, by VI-48.** VI-48 replaced `sigma_star` and
  `rate_formula` together, with two kinds of self-consistent wrong formula:
  - VI-4's Σ = (Σx⁻¹ + λP)⁻¹;
  - water-filling in a basis rotated by φ ∈ {0.001, 0.003, 0.01, 0.03, 0.1, 0.3}.

  Every such mutant failed r2 and r3, down to a median excess of 1.4e-7 nats. The near-optimal
  channels at eps = 1e-3 and the random Gaussian channels caught them. The mechanism: the
  near-optimal channels perturb the claimed optimum in random PSD directions, a one-sided
  first-order test of whether the claimed Σ⋆ really is optimal.
- **The power is thin per instance.** VI-49's rotation by 0.001 (median excess 3.4e-7 nats) was
  caught on only 2 of 120 instances. That is enough to fail the verdict.
- **The maximum-entropy step of `lem:info`** is tested only by non-Gaussian channels, and only
  weakly in relative terms:
  - every informative catch has H ≤ 0.13 nats;
  - the smallest slack/I over informative quantizers is 0.101 (product) and 0.207 (skew);
  - so a `lem:info` strengthened by a factor of about 1.11 (product) or 1.26 (two-dimensional)
    would pass;
  - per instance, the best formula-independent gap has median 0.31 nats, and only 1 instance in
    120 has one within 1e-2. These figures exclude trivial channels; with them included, they
    are 0.284 and 7. Near the optimum, the converse is tested by Gaussian channels only.
- **The achievability half.**
  - r3's optimum check and r4's trace check hold by construction for the correct formula, but
    catch one that is too low (VI-49).
  - r4's feasibility check holds by the closed form, and its Monte Carlo adds nothing.
  - The achievability itself rests on the proof: Σ⋆ ≻ 0, Σ⋆ ⪯ Σx, and the jointly Gaussian
    channel's information.
- **The removed r3 clause, checked.** VI-48 confirmed the stated reason quantitatively. At
  eps = 1e-4 on both seeds, the measured gap divided by eps times the predicted first-order term,
  ½·scale·Σ_k (1 − p̃_k/θ)₊ (VᵀΣx^{1/2}EΣx^{1/2}V)_kk, lies between 0.998 and 1.003. That
  prediction tests the proof's KKT multipliers μ_k directly.

**Owed in a version 3:**
- power gates built from self-consistent mutants (VI-4's Σ, a rotated basis, and a formula
  lowered rather than raised), with catches reported per family and the optimum and
  near-optimal channels excluded;
- r5(b) counting only channels with H > 0;
- the first-order prediction above as r3's convergence clause;
- the identities labelled as such in the output;
- a lowered-formula gate on the achievability checks (VI-49);
- catch counts per instance;
- the `IntegrationWarning`s counted.

## In CI

From 2026-11-21 the net is in CI's re-run tier, in file mode, and runs in shard 2/3:
- CI moves the committed JSON aside;
- it reruns the harness and requires a fresh JSON;
- it compares that JSON's `verdict` and `PAPER3RATE_supported` with the committed ones;
- it then restores the committed file.

Like sentinel mode, file mode cannot reproduce a committed FAIL, because a harness that exits
with 1 makes the runner raise. Version 2's verdict is a PASS.

**First CI runs:**
- **Atlas, before the push:** shard 2/3 ran on an Atlas clean clone. The net's unit took
  27.9 s, the verdict was reproduced, and the committed JSON was restored unchanged.
- **GitHub:** Actions run 44955486964 (commit 235ba32), job 137002514952 (shard 2/3), took 9.7 s
  and reproduced the verdict and `PAPER3RATE_supported=True`. The run was green on all four
  jobs.
