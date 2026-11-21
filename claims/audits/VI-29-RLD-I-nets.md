# VI-29: R-IND-5 passes on the new RLD-I nets (2026-11-20)

**Targets.** Two new C3 harnesses, written after VI-27 found that RLD-I's Theorem 3
ingredients had no net and Theorem 20's net was weak:
- `experiments/verify_rld1_turning.py`, for Theorem 20 (`thm:turning`);
- `experiments/verify_rld1_lemma1.py`, for Lemma 1 (`lem:gauss`) and Proposition 2's
  identity Σ_e⁻¹ = Σ_e0⁻¹ + J.

**Verifiers.** Two fresh-context general-purpose agents, one per round. They used local files
only, with no network, browser or connector tools. Each ran the scripts once and checked the
formulas independently.

## Round 1, on the first versions

**An error of mine, caught here.**
- *The claim.* The turning harness claimed to refute the variant "constancy requires only
  QΣb₀ = λb₀".
- *Why it was wrong.* That variant is equivalent to the theorem. Once b₀ = b(Δ₀) lies on the
  eigenvector curve, either equation implies the other:
  - QΣb₀ = λb₀ gives Σb₀ = c·K_c·b₀ with c = μ/(λ − Δ₀), hence JΣb₀ = (c − 1)b₀;
  - the converse is the same computation.
- *Consequences.* The "half-common" instances never had b₀ on the curve, so they were generic
  instances, and the check claiming the refutation was mislabeled. I re-derived both
  directions.
- *The pattern.* An in-context claim that a fresh context catches: VI-4's lesson again.
- *For the paper.* This shows that Theorem 20's condition needs only one equation, which is
  now recorded for the owner in VI-27's record.

**Other findings:**
- the real false variant, dropping b₀ = b(Δ₀), was untested;
- the simplicity test was blind to crossings between grid points;
- arccos could not resolve small angles;
- the lemma harness's equality check was tautological;
- the hypothesis Cov(N′,S) = 0 was never exercised;
- the scope was unstated;
- no custody: both files were untracked when they first ran.

All of these were applied in round 2's version.

## Round 2, on the revised versions

**The verdict:** no wrong formula in either harness, with every formula confirmed
independently. The lemma formulas were checked against scipy `quad` and Monte Carlo. The
pass criteria were weaker than the docstrings said, and all of those findings were applied:

**Turning harness:**
- t1 now requires the whole interval on b₀'s branch, and μ_max simple, with relative gap
  > 1e-8.
- t3 confirms each crossing is real: b₀'s branch is the second eigenvalue just after it.
- Instance searches are capped at 2000 tries, so a family that cannot be filled fails; the
  rejection counts are recorded.
- The constancy threshold is 1e-11, so it no longer overlaps the turning threshold.
- t5 is rebalanced: unperturbed < 1e-10, ε = 1e-6 > 1e-8, and the ratio from 1e-4 to 1e-6
  must lie in [30, 300].
- The docstring no longer says "arbitrarily small".

**Lemma harness:**
- Cov N′ ≻ 0 is asserted.
- l5 gains two power arms: a wrong replacement must fail it (l5a), and so must the
  hypothesis-violating family (l5b).
- The docstring now says that the identity, the determinant identity and the equality clause
  all use Cov(N′,S) = 0. Only the bounds do not.
- The scope is corrected: the scalar Jensen step is exercised; the matrix one is not.

**Provenance.** This record exists, and both files are committed before CI runs them.

## Results after round 2 (2026-11-20, seeds 20261120 and 20261121)

**Turning harness, all PASS in 2.9 s:**

| Check | Result |
|---|---|
| t1 | 12/12 constant; worst angle 2.7e-15; relative gap ≥ 0.43 |
| t2 | 12/12 turn; total ≥ 0.032 rad |
| t3 | 6/6 real crossings (164 rejections); constant before, to 1.2e-13 |
| t4 | 12/12 turn |
| t5 | unperturbed ≤ 3.7e-13; ε = 1e-6 gives ≥ 7.4e-7; ratio 99.95–100.00 |

**Lemma harness, all PASS in 0.6 s:**

| Check | Result |
|---|---|
| Smallest bound slack | 9.1e-5 nats |
| Identity | 9.7e-15 |
| Replacement | 2.6e-13 |
| Σ_N smallest eigenvalue | 1.5e-4 |
| Wrong replacement's error | ≥ 2.0e-2 |
| Variants (a), (b), (c) violated | 59/60, 60/60, 60/60 |
| Hypothesis-violating family | identity error ≥ 3.05e-3 and determinant error ≥ 3.06e-3, both 20/20 |

## What these nets do not cover

- Theorem 20's singular-Q case (`cor:context`) and ς = 0.
- Matrix T (p > 1).
- Proposition 2's other steps.
- **Theorem 3's coding argument itself.** These nets cover its converse ingredients, not its
  achievability.
