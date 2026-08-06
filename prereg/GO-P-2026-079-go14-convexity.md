# GO-P-2026-079 — Theorems R and C: the causal-erasure family optimization is a convex program; the 078 anchors certified two-sided

The convexity stroke of the GO-14 campaign, R-IND-5-verified (pass
on record in paper/go14-causal-erasure-PROBE.md, seven mandatory
restatements ALL in force at tex v0.4): **Theorem R** — in moment
coordinates H = A·Σ_W, Γ = Cov(Ŷ) on the convex cone D, for ANY
nondecreasing access schedule with the schedule-general
k(j) = #{t : se(t) < j} (staircase reduction k(j) = max(0, j−Δ−1)),
2ln2·n·L_a = [lndet(Γ−HQH′) − lndet(Γ−HPH′)] + Σ_j S-side leakage
pivots — re-proving the 076 chain rule in one line, with
U-independence (Hypothesis 1) a single premise load-bearing in TWO
legs (leg-by-leg counter-values on record; Δ-causal U-coupling
extends the record-space chain rule but does NOT rescue the moment
form — the non-conflation is itself gated). **Theorem C** — the
block bracket is the exact 074 G-form (C↔H′, V↔Γ, P−Q =
Σ_W⁻¹Σ_{W|S}Σ_W⁻¹ ⪰ 0), each leak term is −ln of an inf-of-affine
pivot floored at τ², distortion is affine: n·L_a is JOINTLY CONVEX
on D, every KKT point is the GLOBAL family minimum, strong duality
yields computable lower bounds. Consequences sealed here: all seven
078 anchors carry certified two-sided brackets (widths 3.0e-6 –
1.7e-5; floating-point certificates, disclosed); the sandwich margin
is the interval [0.0317872, 0.0317906]; the no-tested-spectrum gaps
are certificate-strict at every computed n (O(1/n)-model-conditional
in the limit; the n-monotonicity lemma is the named open face); the
diagonal class is a CONVEX linear section (ladder UB-only because
class ⊊ family); per-cell convexity stays OPEN; minimizer uniqueness
NOT claimed.

Governs `experiments/go14_convexity.py` (numpy/scipy, CPU, single
run, self-contained cold-start brackets — legitimate precisely
because Theorem C makes every KKT point global; sentinel
`===GO14CX-JSON===` with `===END===`; flag `GO14CX_supported`;
internal generator pinned, CLI seed stamps). Model as netted.

```yaml
id: GO-P-2026-079
date: 2026-08-06
retrospective: false
kind: theorem-verification (C3 falsification net for Theorems R+C; prover + R-IND-5 pass with seven restatements on record)
claim: "GO-14 Theorems R and C (tex v0.4): the moment-coordinate
  representation holds for any nondecreasing schedule with
  k(j) = #{t: se(t) < j}; n L_a is jointly convex on the cone D under
  Hypothesis 1 (one premise, two load-bearing legs; Delta-causal
  U-coupling does not rescue the moment form); every KKT point is the
  global family minimum; the 078 anchors are certified two-sided and
  the sandwich margin is [0.0317872, 0.0317906]."
harness: experiments/go14_convexity.py   # GOVERNED seed 20261121; pilot seed 20261120, disclosed below
power: |
  Deterministic gates, bars with pilot margins: s1 identity ~900x
  (staircase, 90 cells incl. edges) and ~17000x (non-staircase
  general k); s2 certificates 14x-2.6e6x; s3 Jensen 4200 pairs +
  per-piece 240, zero violations (worst gaps -3.66/-4.04/-0.041);
  s4 tangent-plane 320 pts zero violations (min slack +2.88);
  s5 brackets: widths 1.7x-3.7x inside gates, UB-vs-pinned-v* 4.5x,
  block_16 19x, margin interval inside [0.0317, 0.0318];
  s6 U-legs 8.3x minimum (2.68/3.51/0.83 vs 0.1), both-fixed ~5e5x,
  non-conflation 6.4x (chain 2.2e-16 vs moment 3.22).
pilot: |
  TWO pilot runs, seed 20261120, disclosed: run 1 = 13/14 (the s6
  denominator-leg counter-example at 0.10-scale dense Au measured
  0.055 vs the 0.1 bar -- the BAR WAS NOT LOOSENED; the pinned
  counter-example record was strengthened to 0.15N + 0.25I); run 2 =
  ALL PASS 14/14, 45.6 s. Also disclosed from the build: the mu-refit
  alternation is a false fixed point (converges to interior points
  with r~0); mu-bisection on dist(x(mu)) = D adopted. Bracket gates
  at (16,1)/(24,0)/(32,0) use the prover's quoted widths (the
  certified widths of record); (16,0) uses the verifier's tighter
  width.
prediction:
  s1_representation: staircase max residual < 1e-9 over 90 cells
    incl. Delta in {0, n-2, n-1, n}; non-staircase (general k(j),
    4 schedules) < 1e-9
  s2_certificates: eigmin(Q) > -1e-12; closed-form P-Q < 1e-12;
    eigmin(P-Q) vs pinned per-n values < 1e-6; Sylvester < 1e-9
  s3_jensen: zero violations (1e-9 threshold) over 4200 pinned
    midpoint pairs + 240 per-piece
  s4_tangent: zero violations over 320 pinned points at the (16,0)
    winner
  s5_brackets: certified LB <= winner at (16,0),(16,1),(24,0),(32,0)
    with widths < {6.9e-6, 7.2e-6, 8.6e-6, 3.4e-5}; UB vs pinned v*
    < 5e-7; block_16 UB err < 5e-7; margin within [0.0317, 0.0318]
  s6_ulegs: as-stated/num-only/den-only residuals each > 0.1 on the
    pinned U-coupled record; both-corrected < 1e-9; Delta-causal
    record-space chain rule < 1e-9 with moment-form residual > 0.5
falsification: s1 fail refutes Theorem R as stated (schedule
  generality or the k-convention); s2 fail breaks a certificate leg
  of Theorem C's proof; s3/s4 fail REFUTES joint convexity itself
  (a Jensen violation is a counterexample -- the theorem, not the
  harness, dies); s5 fail refutes the certified-anchor machinery;
  s6 fail refutes the two-leg U-independence structure or the
  non-conflation. Single governed run, no silent reruns.
design:
  stopping: fixed design, single governed run, seed 20261121, after
    the disclosed two-run pilot (seed 20261120); no further pilots
    or attempts under this ID
  runtime: ~1 min single-threaded (pilot run 2: 45.6 s)
controls: [dual evaluator routes (s1), closed-form PSD legs vs
  numerics (s2), per-piece Jensen isolating block vs leak (s3),
  cold-start brackets reproducing stored-winner values (s5, the
  KKT-global consequence exercised), the strengthened pinned
  counter-example with its first-pilot miss on record (s6)]
amendments: []
hash: sha256:0d76398081b19567a00135434a648e362911ea27c7a10cf53281051a76f02185
```

## Falsification

A pass nets Theorems R and C at tex v0.4: the causal-erasure family
program is convex, its numerics are certified global, the 078
anchors are two-sided values, and the U-independence hypothesis
carries its exact two-leg structure. Open and so marked: the
n-monotonicity lemma (unconditional limit transfer), per-cell
convexity, minimizer uniqueness, within-class certification of the
diag ladder, the U-coupled coordinate, the reset protocol.

## Amendment (dated 2026-08-06, instrumentation, post-seal, disclosed)

CI's ubuntu BLAS stops the s5 L-BFGS-B polish earlier than the local
platform, landing at a larger Lagrangian residual and hence a wider
(still VALID) certificate: runner width 2.12e-5 at (24,0) vs the
8.6e-6 gate (all other anchors passed on the runner). Fix: a
residual-targeted refinement loop (repeat bounded polishes until
rn <= 4e-8, the local as-sealed regime, or 8 rounds) -- the
certificate mathematics is untouched; only the solver's stopping
rule becomes platform-independent. Same-seed (20261121) local rerun:
verdicts IDENTICAL, ALL PASS 14/14; changed vals keys listed in the
commit. The original sealed body and hash are preserved in git
history (sealed at commit a4bb4b5); no bar was changed.
**Amendment revision (same date): the L-BFGS-B-restart refinement was
a measured NO-OP on the runner (bit-identical width at (24,0)) --
restarts terminate at the solver's own fixed point. Replaced by
Armijo gradient descent on the (convex, smooth) Lagrangian to
rn <= 4e-8: platform-independent by convexity. Local rnorms are
1.05e-8..2.15e-8, all under the target, so the local run remains
bit-identical (verified); the descent engages only on
early-stopping platforms.**