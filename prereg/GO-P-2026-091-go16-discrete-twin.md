# GO-P-2026-091 — GO-16 discrete twin: binary water level, tie survival, the fifth class (probe-promotion net)

Governs `experiments/go16_discrete_twin.py` for the discrete-twin
results of `paper/go16-adversarial-observer.tex` v0.3 §7: in the
binary disclosure game (n spots, private bits, randomized bet/check
policies, reader watching k of n, leakage = μ_i × resolved-variance
ratio), (i) the per-coordinate shielding frontier is the symmetric
channel exactly, e(ρ) = (1−√ρ)/2 — convex, so the LQG linear cost is
a Gaussian privilege; (ii) deterministic policies achieve ρ ∈ {0,1}
only — mixing is the discrete carrier of dither; (iii) the tie among
fractional-attention coordinates survives exactly with the
generalized pricing θ_i = −c_i′(ρ_i)/(λμ_i) = s_i²/(4λ√(μ_i t*));
(iv) a fifth class impossible in LQG (interior-contested-above:
shielded, fully watched, strictly above the water, no tie) exists at
the hand-derived instance. Sentinel `GO16_DISCRETE_TWIN_BEGIN/END`;
flag `ALL_PASS`.

```yaml
id: GO-P-2026-091
date: 2026-08-21
retrospective: false
kind: probe-promotion net (exploratory probe promoted to a governed
  seal; the analytic solver is a closed-form construction verified by
  two-sided saddle checks and an independent grid solver)
claim: "In the binary disclosure game: the shielding frontier equals
  the symmetric channel (1-sqrt(rho))/2 exactly; deterministic
  policies are all-or-nothing revelators; the fractional-attention tie
  and the water-level structure survive with pricing
  theta_i = s_i^2/(4 lambda sqrt(mu_i t*)); and interior-contested-
  above spots (partial balancing without indifference) exist —
  exhibited at mu=(4,1,0.5), s2=(12,5,1), lambda=1, k=1 with
  rho_1 = 0.5625, J* = 3.75, g-gap 1.25 exactly."
harness: experiments/go16_discrete_twin.py   # GOVERNED seed 20260822
hash: sha256:1725c8e5e63f0ea609a14e06258b27970d0b69d2df13a217a960f05aecdbc2fb
power: |
  Margins at the final pilot (dev): P1 monotonicity 2.8e-17 vs 1e-6;
  convexity 2.5e-4 vs 2e-3 (8x, grid-noise scale, declared); SLSQP
  frontier refinement equal to symmetric within 1e-12 at five interior
  rho (gate: full <= sym + 1e-9). P2 tie spread 0.0 vs 1e-9; budget
  4.4e-16 vs 1e-6 (2e9x); saddle 0.0/1.1e-16 vs 1e-9; grid-vs-analytic
  1.11e-3 vs 2.5e-3 (2.3x — INSTRUMENT, the grid solver carries a
  half-bin downward bias, declared). P3 exact-value gates at 1e-9
  (closed-form reproduction) with the same instrument-grade grid
  cross-check (1.0e-3 vs 2.5e-3). P4 all shielded policies strictly
  randomized.
pilot: |
  THREE dev runs, seed 20260821, ALL DISCLOSED, with every gate change
  itemized (commits 9890b02 and prior working-tree iterations):
  run 1 — 1/4. TWO failures were MIS-SPECIFIED GATES OF MINE, one was
    an INSTRUMENT DEFECT: (a) P1 gated "full frontier == symmetric
    channel" as a hypothesis; the binned data showed an apparent
    asymmetric advantage — subsequently PROVEN to be a binning artifact
    by SLSQP refinement (the symmetric channel IS the frontier to
    1e-12); the gate was replaced by the refinement check. (b) P2's
    theta-reconstruction used finite-difference slopes on the binned
    (staircase) frontier — replaced by derivative-free inverse pricing
    plus two-sided saddle checks. (c) P3's tolerance was based on the
    grid solver, whose half-bin downward cost bias shifted rho by
    0.0155 — the ANALYTIC solver (licensed by the SLSQP frontier
    validation) became primary, the grid solver retained as an
    independent cross-check. THE HAND PREDICTIONS (rho_1 = 0.5625,
    J* = 3.75, gap 1.25) WERE MADE BEFORE ANY RUN AND NEVER MOVED;
    run 1's J = 3.7489 was within a grid bias of them.
  run 2 — 2/4 (P1, P4 pass; P2/P3 still on the old instruments).
  run 3 — ALL PASS 4/4 with the final instruments; committed as
    results/go16-discrete-twin.json at 9890b02.
  NO physics value moved between runs: tie spread, budget, class
  structure, and the P3 exact values were stable throughout; only
  instruments and mis-specified gates changed, each itemized above.
prediction:
  P1_frontier: monotone (<1e-6), convex at grid scale (<2e-3),
    deterministic rhos exactly {0,1}, SLSQP-refined frontier <= the
    symmetric curve + 1e-9 at rho in {0.1,0.3,0.5,0.7,0.9}
  P2_main: 5-way tie spread <1e-9 at t* = 0.36754...; budget error
    <1e-6; theta in [0,1]; two-sided saddle (FRESH perturbations at
    the governed seed) 0 violations at 1e-9; grid cross-check <2.5e-3
    (instrument)
  P3_fifth_class: rho_1 = 0.5625 and J* = 3.75 and g-gap = 1.25 all
    exact (<1e-9); class = interior-contested-above with theta_1 = 1;
    FRESH saddle perturbations clean; grid cross-check <2.5e-3
    (instrument)
  P4_mixing: every shielded coordinate's implementing policy strictly
    randomized
falsification: physics gates are P1 (frontier facts + determinism),
  P2's tie/budget/saddle, P3's exact values and class, P4: a fail
  refutes the corresponding twin claim as stated in the tex §7 and
  demotes it from probe-settled. Instrument gates are the two
  grid-vs-analytic cross-checks: a fail voids the run — logged
  instrumentation miss, rerun under dated amendment. Single governed
  run, no silent reruns.
design:
  stopping: fixed design, single governed run, seed 20260822 (fresh
    randomness enters ONLY the saddle-perturbation draws; all other
    gates are deterministic reproductions and declared as such); no
    further pilots under this ID
  runtime: ~1 min CPU single-threaded
controls: [the SLSQP frontier refinement (analytic, binning-free,
  licenses the analytic solver), the independent grid solver
  cross-checks, the two-sided saddle perturbations, deterministic-
  policy enumeration (the idempotency twin)]
provenance: |
  The P3 hand predictions predate every run (derived from the LQG
  interior-FOC construction before the harness existed; on record in
  the probe docstring from its first commit). The binning-bias lesson
  and both mis-specified gates are on record in the 9890b02 commit
  message and above.
amendments: []
```

## What this registration does not claim

No theorem-grade status for the binary water-level construction (the
write-up is owed; this seal nets the probe results at governed grade).
No claim about larger alphabets, extensive-form games, or the
operational face. No novelty language (flank posture governs).
