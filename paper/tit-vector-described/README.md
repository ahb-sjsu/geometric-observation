# Rate and Conditional Content for Gaussian Vector Sources with Encoder-Observed Context

Companion to `../tit-cr-context/` (the scalar paper, cited as [1]). Split off on 2026-10-01 so the scalar paper stays focused. Status: draft, not submitted.

## Contents

- Theorem 3: the coding theorem for a vector described variable, proved by listing the changes to [1, Theorem 29]. Proposition 2: Gaussian descriptions, indexed by error covariance, exhaust the region.
- Section III (independent coordinates):
  - Lemma 4: slope and curvature of the scalar function in closed form; strict convexity.
  - Theorem 5: the region is a union of Minkowski sums; the content-optimal allocation equalizes slopes; activation order σ²(1+ρ²/τ²).
  - Corollary 6: the rate-optimal and content-optimal descriptions can describe disjoint coordinates.
- Section IV (coupled coordinates):
  - Theorem 7: max-det program in the holder's error covariance.
  - Theorem 8: one-dimensional regime in closed form, as a pencil eigenvalue, with a certificate.
  - Theorem 9: the read direction turns with the budget unless it is a principal axis uncorrelated with the context.

## Checks (run on Atlas)

| File | What it checks |
|---|---|
| `verify_parallel.py` | Lemma 4 identities (symbolic and finite differences), allocation vs brute force, no correlated Gaussian channel beats the allocation, the Section III instance |
| `verify_coupled.py` | Scalar pencil identity (symbolic), max-det vs brute force (32 cases), certificate vs optimizer, the Section IV instance and D_1 |
| `exploration-2026-10-01/` | The exploratory scripts and FINDINGS note from the day the coupled case was worked out |

Build: `pdflatex tit-vector.tex` twice.
