# Runs of `experiments/verify_paper3_nets.py` (Paper III's C3 nets)

The harness's own docstring gives its history through version 3. This file records what
happened after version 4 was committed, so that the harness stays byte-identical to the
file that ran, and its recorded sha256 still matches it.

| Version | Commit | Seed | Output | Outcome |
|---|---|---|---|---|
| 3 | 5375b7b | 20261126 | `PAPER3-nets-v3.json` (renamed from `PAPER3-nets.json` on 2026-11-21; the docstring's reference to the old name predates the rename) | 7/7 pass. VI-38 then found m4's tolerance doubled without disclosure. |
| 4, attempt 1 | 57bccec | 20261127 | none | **Crashed at m1's first solver call; no check completed** (2026-11-21, Atlas). The harness was run with `python -I`. In the Atlas venv (`--system-site-packages`) that loads the system numpy 1.26.4 instead of the 2.4.6 in the user site. The lazy `import cvxpy` in m1's first solve then failed: `ModuleNotFoundError: No module named 'numpy.lib.array_utils'`. Stdout was empty. |
| 4, attempt 2 | 57bccec | 20261127 | `PAPER3-nets.json` | **7/7 pass** (2026-11-21, Atlas, 4 BLAS threads, 35.5 s). The same commit and criteria were used; the only change was running without `-I`, the environment version 3 used (numpy 2.4.6, scipy 1.18.1, cvxpy 1.9.3, Python 3.12.3). |

Version 4 was run from a clean clone of 57bccec. The recorded `harness_sha256` is
`6dfa9e68fc54f64ab2d71596ecd09dfaefd0268c631d390a8a47d6050a298e9e`, the sha256 of
`experiments/verify_paper3_nets.py` at that commit as checked out on Linux, and of
`git show 57bccec:experiments/verify_paper3_nets.py`. A Windows checkout with
`core.autocrlf` has CRLF line endings and hashes differently until they are normalized.

Version 4, attempt 2, in numbers (the bar follows each value):

| Check | Measured | Bar |
|---|---|---|
| m1, logdet vs the solver | 3.6e-7 | 1e-5 |
| m1, trace residual (relative) | 2.8e-15 | 1e-9, two-sided |
| m2, duality gap | 6.6e-14 | 1e-8 |
| m3, corner closed form vs solver | 7.5e-8 | 1e-5 |
| m3, pairs | 70 with a binding cap; 41 nested, 41 not nested, none excluded | |
| m4, worst intercept \|a\| over all 82 pairs | 3.6e-6 nats | 1e-5, absolute |
| m4, informative pairs | 28 | at least 20 |
| m4, solves "optimal_inaccurate" | 12 of 574 (2.1%) | 5% |
| m4, solver failures | none | |
| m7, VI-4's bug beaten by the solver | 101 of 150 | 10 |
| m7, a level of 1.2θ fails m2 | 150 of 150 | 90% |
| m7, "always refinable" refuted | 40 | 10 |
| m7, the κ family | 21/21 | |
| m7, dropped inactive terms | 21/21 | |
| m7, the old constant r_D/2 | 9/9 | |
| m5, definition | 8.9e-16 | 1e-9 |
| m5, Csiszár, λ⋆ | pass | |
| m6, Monte Carlo mean and variance | within 5 SE | 5 SE |
| m6, configurations | 15, of which 4 all-active and 11 mixed | |

From version 4 on, the net is in CI's re-run tier (`ci/reproduce.py`, section [2/3]),
which must reproduce the `verdict` dict and the `PAPER3NETS_supported` flag of
`PAPER3-nets.json`.

## What the review VI-45 added (2026-11-21)

A fresh-context review of version 4, its output and its CI wiring found 0 errors. Its
points that bear on reading the numbers above:

- **m1's two-sided trace clause is an identity of the closed form.** `water_level` solves
  Σ min(p_k, θ) = D, and tr(PΣ⋆) = Σ min(p_k, θ). So the clause can fail only on a bug,
  and the 2.8e-15 is roundoff. It does not test that the max-det optimum binds the trace,
  which is the fact `cor:dispersion`'s uniqueness argument uses. That test would apply the
  check to the solver's solution.
- **m4's intercepts are the fit's bias, not corner error.** All 28 informative intercepts
  are positive. A quadratic through the same three gaps gives |a| ≤ 2.1e-7. So the 3.6e-6
  is the bias of the a + c√δ model. m4's resolution is therefore asymmetric: a corner value
  too high fails above about 6.4e-6 nats, and one too low passes until about 1.36e-5 nats.
  "Resolution 1e-5 nats" in the docstring holds only roughly.
- **m4 has two discrete solver-status clauses:** no solver failure, and at most 5%
  "optimal_inaccurate". One failure, or an iteration limit, among 574 Clarabel solves at
  tolerance 1e-9 flips m4. How they behave on GitHub's Ubuntu runner is not known. The
  other margins are comfortable: the reviewer recomputed them and found every discrete
  branch at least 0.5% from its threshold.
- **The run metadata is thin.** The JSON records no start time, no commit, no Clarabel
  version and no thread count. Clarabel on Atlas is 0.11.1 (queried on 2026-11-21 after the
  run). That the harness was committed before it ran therefore rests on git's order
  (commit 08:28:44 −0800, push 08:28:48) and on this account, not on the artifact.
- **Two smaller gaps, present since version 2:**
  - the redraw loop for the nested-distinct pairs keeps its last draw after 50 tries without
    recording it (on this seed every pair met the floor within 4 draws);
  - the rows do not record `cap_binds`. The reviewer regenerated the pairs: the 28
    informative pairs are exactly those that are independent, have a binding cap and are not
    nested.
- **Docstring.** Its "results/PAPER3-nets.json" now names version 4's output, and "a
  version 4 … is owed" is stale. The file stays byte-identical so that its hash still
  matches.

**Owed in a version 5:**
- apply the trace check to the solver's solution;
- a quadratic intercept fit on four δ;
- record the start time, the commit and a dirty flag, Clarabel's version and the thread
  settings;
- record each nested-distinct pair's draws, and fail when the floor is not met;
- record `cap_binds` per row;
- fix the docstring.
