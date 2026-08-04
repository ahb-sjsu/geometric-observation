# GO-P-2026-063 — GO-11 v0.9 closing theorems: C3 falsification harness

Registers the **numerical falsification harness** for GO-11 v0.9's three
closing results ([`paper/go11-conditional-region.tex`](../paper/go11-conditional-region.tex),
each R-IND-5-verified pre-assertion — VERIFICATION addendum 6 in
[`paper/go11-conditional-region-NOVELTY.md`](../paper/go11-conditional-region-NOVELTY.md)):

- **T7** (Thm. 7, vector S solved): the whitened two-water-level system
  with per-mode closed form
  $u=(1-\alpha\gamma_0-(1-\alpha)\gamma_1)\,[(1-(1-\alpha)\gamma_1)I+
  (1-\alpha)\gamma_1\Lambda]^{-1}y_0$; Theorem 3 as the r=1 case;
  dimension-free moment converse.
- **T8** (Thm. 8, higher-rank reads): the k×(k+r) matrix program with the
  EXACT per-mode decomposition under simultaneous block-diagonality
  (superadditivity proof), and strict misalignment advantage.
- **U** (interior-α uniqueness, proved): convexity of the weighted
  objective on the active slice — netted operationally via Hessian
  positivity, fixed-point root uniqueness, and multi-start dispersion.

Governs `experiments/verify_go11_rungs.py` (numpy+scipy, single run,
~1 min; sentinel `===GO11R-JSON===`; summary flag `GO11R_supported`).

```yaml
id: GO-P-2026-063
date: 2026-08-05
retrospective: false
kind: theorem-verification (C3 numerical falsification of R-IND-5-verified analytic results)
claim: "GO-11 v0.9: the vector-S frontier is the generalized two-water-level
  system (per-mode closed form; Thm 3 = r=1); higher-rank reads are the
  k x (k+r) matrix program with exact block-diagonal decomposition and
  strict misalignment advantage; the weighted objective's minimizer is
  unique at interior alpha (convexity on the active slice)."
harness: experiments/verify_go11_rungs.py   # GOVERNED seed 20260906; pilot seed 20260905, disclosed below
power: |
  Deterministic analytic-reproduction gates; per PROTOCOL 5.1 the bars
  carry pilot margins: s1 FOC bar 5e-4 vs pilot 1.1e-8 (>1e4x); s3 moment
  bar 5e-4 vs 1.0e-14; s5 aligned bar 8e-3 vs 8e-4 (10x), misaligned-gap
  bar 2e-3 vs 5.7e-3 (2.9x); s6 dispersion bar 1e-5 vs 3.6e-14, root bar
  1e-6 vs 1.3e-12, Hessian bar 0.02 vs 3.27 (163x); s2 Thm-3 windows 2e-3
  (values reproduced); s4 BA window [-0.03, +0.15] is the grid-bias
  envelope of the 055-lineage instruments. Every margin >= 1.3x.
pilot: |
  ONE pilot, seed 20260905, full harness, 45.0 s: ALL PASS with the
  drafted bars unchanged (zero bar recalibrations -- third consecutive
  clean first pilot under 5.1, after 060 and 062). Values: worst FOC
  residual 1.09e-8 across r in {1,2,3,4} incl. the extreme instance
  (lambda_min = 0.02, D = 0.92); Thm-3 frontier reproduced; moment-vs-
  system 1.0e-14; BA 0.5625 vs system 0.5331 (inside window); aligned
  decomposition |diff| 0.0008; misaligned strict gap 0.0057; uniqueness
  nets: dispersion 3.6e-14, fixed-point root spread 1.3e-12 (36-start
  hunts), min Hessian eigenvalue 3.268.
prediction:
  s1_vecfoc: worst FOC residual of eq. (vecfoc) at the 50-start optimum
    <= 5e-4, over r in {1,2,3,4} random instances (3 alphas each) plus the
    extreme instance (lambda_min = 0.02, y0 tilted low, D = 0.92)
  s2_thm3_consistency: the r=1 whitened program reproduces Theorem 3's
    frontier values (0.9085/0.5228, 0.8772/0.5328, 0.8685/0.5577) at
    (rho2, tau2, D) = (0.75, 0.5, 0.3) within 2e-3 bits
  s3_moment_converse: |weighted moment program - whitened system| <= 5e-4
    at r=2 general coupling, alpha in {0, 0.5, 1}
  s4_ba_net: unrestricted conditional-BA (11^3 grid, 5x5 S-bins) at the
    alpha=0 endpoint within [-0.03, +0.15] of the system value
  s5_thm8: aligned instance |matrix program - per-mode decomposition|
    <= 8e-3; misaligned instance forced-decomposition minus program
    >= 2e-3 (strict advantage)
  s6_uniqueness: multi-start J-dispersion <= 1e-5; (g0,g1) fixed-point
    root spread <= 1e-6 over 36-start hunts; finite-difference Hessian of
    the sliced objective has min eigenvalue >= 0.02 at all probes
falsification: any section failing its bar refutes the corresponding v0.9
  statement and sends it back to the proof (charter rules R-IND-5, C-AI-2).
  Instrument-vs-physics separation per PROTOCOL 5.1: SLSQP non-convergence
  is a logged instrumentation miss (dated-amendment rerun only); an s4 BA
  point BELOW the converse by more than the 0.03 envelope refutes the
  converse outright; an s6 second root or negative Hessian eigenvalue
  refutes the uniqueness proposition.
design:
  stopping: fixed design, single governed run, seed 20260906, after the
    one disclosed pilot (seed 20260905); no further pilots or attempts
    under this ID
  runtime: ~1 min single-threaded (pilot: 45.0 s)
controls: [extreme-instance probe (s1), Thm-3 anchor (s2), independent
  moment program (s3), unrestricted-BA net (s4), misalignment strictness
  (s5), three independent uniqueness nets (s6)]
amendments: []
hash: sha256:45de568ebb3bf45c6cbe8a7b8382dc8ab05b8113f025ddac68660e4e43942944
```

## Falsification

The results are analytic and R-IND-5-verified; the harness is a
falsification net, not the proof. A pass supports citing the v0.9 theorems
at `[predicted]`-grade alongside the 060-netted content; GO-11's overall
`[replicated]` class (operational, 061/062) is unaffected either way.
