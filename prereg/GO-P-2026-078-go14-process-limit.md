# GO-P-2026-078 — the GO-14 process-limit face: U-independence load-bearing, the innovations rate scoped, the mechanism netted

Conjecture v0.2 verified adversarially (R-IND-5 pass on record in
paper/go14-causal-erasure-PROBE.md) and folded as tex v0.3 with all
SIX mandatory restatements: (R1) the record family — jointly
Gaussian with (V,Y), INDEPENDENT of U — is a numbered hard
hypothesis on the chain rule and every minimum (the identity extends
exactly iff U-coupling is Δ-lag causal; outside the family it FAILS
at 0.015–4.59 bits and the minima collapse: trivial Δ-causal
U-record 0.539536 < family min 0.566758; general U-coupled feasible
record 0.092864 < block₁₆ — sandwich inverted); (R2) c_diag quoted
as the bracket [0.105, 0.125] only, not converged through Δ=6;
(R3) raw finite-n anchors (family min L_a(0) ≤ 0.5667581 at n=16,
La(48,Δ=6) = 0.5316222730), E_∞(6) ±10% explicit; (R4) "not matched
by any TESTED causal-conditioning spectrum" — the causal-spectral
allocation is a reference construction, neither UB nor LB;
(R5) time-symmetric = transpose symmetry Ay=Ayᵀ; the mechanism
clause (V-coupling sign boundary EXACTLY at lag Δ — horizon-matched
V-cancellation) is the testable face; (R6) dated erratum block_∞
0.52991 → 0.529950 in Theorem 1(v), ratio "→ λ_s⁻² from below,
unresolved beyond Δ≈6", c_fs ∈ (0.07, 0.125] data-supported.

Governs `experiments/go14_process_limit.py` (numpy/scipy, CPU,
single run; sentinel `===GO14PL-JSON===` with `===END===`; flag
`GO14PL_supported`). Model as netted (a=0.8, ρ²=0.49, τ²=0.4,
D=0.3, T=(V,Y), λ_s=0.354554). Record draws internally pinned
(20260805) so pilot and governed verify identical numbers; the CLI
seed stamps the run.

```yaml
id: GO-P-2026-078
date: 2026-08-05
retrospective: false
kind: theorem-verification (C3 falsification net for the GO-14 process-limit face; R-IND-5 pass + six restatements on record)
claim: "GO-14 process-limit face (tex v0.3): the chain rule and all minima
  hold under the U-independence hypothesis (exact Delta-lag-causal
  extension; identity false and sandwich inverted outside the family);
  the family min L_a(0) <= 0.5667581 at n=16; the optimizer mechanism is
  horizon-matched V-cancellation (Ay transpose-symmetric, Av sign
  boundary exactly at lag Delta); the diag ladder and rising per-lag
  ratios approach lambda_s^-2 from below; the causal-spectral reference
  construction sits 0.0148/0.0041/0.0008 below the measured full-family
  limits (no tested spectrum matches)."
harness: experiments/go14_process_limit.py   # GOVERNED seed 20261111; pilot seed 20261110, disclosed below
power: |
  Deterministic gates; per PROTOCOL 5.1 the bars carry pilot margins:
  s1 anchors/cross-check/identity at 44x-9e6x; s2a U-break bar 0.01 vs
  0.0634 (6.3x); s2b exact extension 9e6x; s2c counter-value 0.539536
  vs bar 0.55 (bar-val 0.0105); s3 family min 0.5667581350 vs bars
  0.5668 / 0.567353 (two starts agree 6e-11); s4 transpose symmetry
  66x, sign boundary EXACT [0,1,2] at all three Deltas; s5 ladder
  9 cells at ~8e6x, ratio rise 7.584 < 7.726 with 0.379 headroom to
  the cap; s6 allocation 455x, block_inf 675x, plateau gaps
  436x-8094x their calibrated error.
pilot: |
  ONE pilot, seed 20261110, full harness, 390.6 s: ALL PASS 19/19 on
  the first run, zero bar recalibrations. One disclosed
  implementation note: the literal s2c noise variance 0.1625 gives
  distortion 0.30004 by rounding; the 076-s5 per-cell noise shave
  (z -> 0.16246) restores exact feasibility and reproduces the
  R-IND-5 counter-value 0.539536 to all quoted digits (raw values in
  the artifact). s5's ratio face pins the (32,48) extrapolation pair
  in code (the (24,32) pair sits inside the +/-10% pair sensitivity
  R-IND-5 flagged -- exactly why R3 demotes E_inf(6)).
prediction:
  s1_anchors: block_16 and diag UB(0) reproduced (<1e-7 / <5e-6);
    evaluator routes agree <1e-9; identity residual <1e-9 in-family
  s2a_U_break: random U-coupled records have |residual| > 0.01
  s2b_Delta_causal_exact: Delta-lag-causal U-coupling residual <1e-9
  s2c_counter_value: the shaved trivial U-record is D-feasible and
    achieves L_a(0) < 0.55 AND < the s3 family minimum
  s3_family_min: full-space min L_a(0) at n=16 <= 0.5668 and
    < 0.567353 (beats the 076 verifier record)
  s4_mechanism: Ay transpose-symmetry rel-residual < 1e-3; Av
    interior-row sign boundary at EXACTLY lag Delta for Delta=0,1,2
  s5_ladder_rate: nine (n,Delta) diag La cells within 1e-6 of the
    verifier-confirmed values; extrapolated per-lag ratios rise
    monotonically and stay < lambda_s^-2 + 0.15
  s6_reference_gaps: causal-spectral allocation within 1e-4 of
    {0.547945, 0.532344, 0.530253}; block_inf within 1e-5 of
    0.529950; full-space plateau gaps > 3x calibrated error
falsification: s2 fail refutes the U-scoping (Hypothesis 1 either
  unnecessary or insufficient -- the theorem's family statement is
  wrong either way); s3 fail refutes the family anchor; s4 fail
  refutes the mechanism clause; s5 fail refutes the ladder/rate
  scoping; s6 fail refutes the no-tested-spectrum-matches statement;
  s1 fail = instrument, investigate before any claim. Single
  governed run, no silent reruns.
design:
  stopping: fixed design, single governed run, seed 20261111, after
    the one disclosed pilot (seed 20261110); no further pilots or
    attempts under this ID
  runtime: ~7 min single-threaded (pilot: 390.6 s)
controls: [dual-route evaluator cross-check (s1), in-family vs
  out-of-family identity contrast (s2a/s2b), the trivial-record
  counter-value reproducing the R-IND-5 number exactly (s2c),
  two-start agreement on the family min (s3), pinned extrapolation
  pair disclosed in code (s5)]
amendments: []
hash: sha256:728f59fd832defc91e1a89860c5708f2e0f9d129ef452f82539c49306b5aca6a
```

## Falsification

A pass nets the GO-14 process-limit face at tex v0.3: the
U-independence hypothesis load-bearing with its exact extension and
counter-values, the family anchor, the horizon-matched
V-cancellation mechanism, the scoped innovations rate, and the
no-tested-spectrum-matches statement. The lower bound (via the
interleaved-Cholesky convexity route), the U-coupled coordinate, the
reset protocol, and the constant beyond Δ≈6 remain OPEN and are so
marked. The S2/DBLP novelty residual pass stays OWED before headline
novelty language.
