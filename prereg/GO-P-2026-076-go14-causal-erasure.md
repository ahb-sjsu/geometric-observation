# GO-P-2026-076 — causal erasure netted: the Δ-lagged causally-conditioned coordinate L_a (GO-14 Theorem 1)

The definitional fork settled (definition (a) adopted, (b) rejected
with the 0.0136-bit floor, (c) known-collapsing) and the first GO-14
theorem netted: (i) exact chain rule n·L_a(Δ) = I(T^n;Ŷ^n|S^n) + C_Δ
with C_Δ ≥ 0 the smoothing-leakage charge, = 0 iff Δ-lag causally
simulatable; (ii) collapse is a FEASIBILITY face — N-only records
collapse exactly while carrying bits, a feasible collapsing boundary
record exists exactly at D = ρ²(n−Δ−1)/n, and below that bound
strictness routes through block-optimality + C_Δ > 0 at the block
optimizer; (iii) class-conditional sandwich block_n < min L_a(Δ) ≤
diag-class value < slice(Δ), strictly DECREASING in Δ (v0.1's
"increasing" was a sign error, fixed at v0.2), lower margin closing
at rate λ_s^{2Δ}; (iv) the smoothing pole λ_s = a(1−K) with
CELL-LOCAL scope — per-cell leak ratio → λ_s⁻² = 7.955 for
time-local records, aggregate ratio carrying the (n−Δ−1)/(n−Δ−2)
cell-count prefactor; code-mixing records measurably decay slower
(rwf ≈ 0.255/lag, characterization OPEN, recorded not gated);
(v) not bookkeeping — gap_n = static(q_path) − block_n is n-pinned
(0.0213/0.0263 at n=8/16) and converges to the spectral gain ≈0.0313
(block_∞ = 0.52995 by direct per-frequency Lagrangian allocation —
the closed-form g* quadratic does NOT survive the per-frequency ρ²
generalization; the harness uses direct single-letter minimization,
cross-checked against the exact per-mode decomposition of block_16).
HARD SEAL TERM (verifier): all quoted minima are diagonal-class
upper bounds; the diagonal class is PROVABLY BEATEN for L_a
(s5 nets the failed first-order certificate and an explicit feasible
non-diagonal improvement); any presentation of 0.572255 as THE
minimum FAILS this registration.

Governs `experiments/go14_causal_erasure.py` (numpy/scipy, single
run; sentinel `===GO14CE-JSON===` with `===END===`; flag
`GO14CE_supported`). Model: V AR(1) a=0.8 unit variance, Y = 0.7·V+N
Var(Y)=1, S = V+U τ²=0.4, D=0.3, linear window (non-circulant —
erasure order is inherently non-circular), T=(V,Y).

```yaml
id: GO-P-2026-076
date: 2026-08-05
retrospective: false
kind: theorem-verification (C3 falsification net for the GO-14 first netting; R-IND-5 pass 1 + closure on record in paper/go14-causal-erasure-PROBE.md)
claim: "GO-14 Theorem 1 (v0.2): exact chain rule nL_a = block + C_Delta;
  collapse = feasibility face at D = rho^2(n-Delta-1)/n; class-conditional
  sandwich block_n < min L_a <= diag-class < slice, strictly decreasing in
  Delta; cell-local smoothing pole lambda_s^{-2} with the
  (n-Delta-1)/(n-Delta-2) aggregate prefactor; bookkeeping refuted with
  n-pinned gap -> spectral gain ~0.0313."
harness: experiments/go14_causal_erasure.py   # GOVERNED seed 20261102; pilot seed 20261101, disclosed below
power: |
  Deterministic gates (seed feeds only the s1 random-channel draw;
  optimizers are deterministic warm-started, the 070 lesson). Per
  PROTOCOL 5.1 the bars carry pilot margins >= 1.3x where numeric:
  s1 identity bar 1e-8 vs pilot 9.0e-12 (~1000x); s2a leak bar 1e-9
  vs 4.1e-12, block-bits bar 0.5 vs 1.743, infeasibility strict
  (0.54 > D); s2b boundary-record distortion inside
  [bound-1e-9, D] with bound 0.275625 (pilot lands within 1e-7 of
  the bound) and leak bar 1e-9 vs 4.4e-12; s3 sandwich strict at all
  three Deltas (pilot margins: UB(0) 0.0497 below slice, 0.0373
  above block) with decrease bar 1e-3 vs pilot 0.0362 (36x) and
  leak-strictness bar 1e-9 vs worst 2.1e-6 (2000x); s4 cell bar 0.01
  vs pilot 1.7e-4 (60x), aggregate bar 0.02 vs pilot ~8e-3 (2.5x);
  s5 slope bar 1e-3 vs 0.0924 (92x), improvement bar 1e-4 vs 2.4e-3
  (24x); s6 monotonicity strict (pilot 0.0213 < 0.0263 < 0.0313)
  and gain bar |gap_inf - 0.0313| < 0.004 vs pilot 1.0e-5 headroom
  0.0040 (met by construction of the band).
pilot: |
  Pilot phase, seed 20261101, disclosed in full: THREE runs. Run 1
  (as-drafted): s1/s2/s3/s5 PASS bit-identically to the probe/verifier
  numbers; three DESIGN BUGS found and fixed openly -- (a) json bool
  serialization crash; (b) s4 measured at the rwf channel where the
  pole is genuinely different (~3.93/lag, the record-dependence now
  scoped into the theorem and recorded as s4_rwf_ratio_obs) and gated
  in the window-edge zone; (c) s6 used a closed-form per-frequency g*
  generalization that is WRONG (0.656 vs true 0.530) -- replaced by
  direct per-frequency Lagrangian minimization validated against the
  exact per-mode decomposition of block_16 (machine-precision match)
  and against the verifier's block_inf = 0.52991 (harness: 0.52995).
  Run 2 (fixes in): ALL sections PASS except s4 aggregate, whose gate
  range Delta=5..11 extended into the ~1e-11 CMI jitter floor;
  characterization run showed the prefactor holds to <=1% over
  Delta=0..7 where leaks are numerically meaningful -- gate rescoped
  to Delta=0..6 with the noise-floor scope disclosed in-code. Run 3
  (final form): expected ALL PASS; its values are the bars' pilot
  reference. No bar was loosened against a measured value at any
  point; every change was a measurement-scope or implementation fix.
prediction:
  s1_identity: max |mean(La) - (Iblock/n + mean(leak))| <= 1e-8 over
    24 (n, channel, Delta) cells incl. Delta=n
  s2a_Nonly_collapse: max|leak| <= 1e-9 AND block bits > 0.5 AND
    dist > D (the theorem's V-free infeasibility)
  s2b_boundary_collapse: the exhibited Delta=6 record has
    dist in [rho^2(n-Delta-1)/n - 1e-9, D] and max|leak| <= 1e-9
  s3_sandwich: block16 < UB(Delta) < slice(Delta) for Delta in {0,2,5}
  s3_decreasing: UB(0) > UB(2) > UB(5) with UB(0)-UB(2) > 1e-3
  s3_strict_leak: leak at every La-optimizer > 1e-9
  s4_pole_cell: max relerr of cell-12 ratios (Delta 2..5, n=32,
    scalar channel) vs lambda_s^{-2} < 0.01
  s4_pole_prefactor: max relerr of aggregate ratios (Delta 0..6,
    n=16) vs lambda_s^{-2}(n-Delta-1)/(n-Delta-2) < 0.02
  s5_certificate_fails: projected feasible slope at the diag Delta=0
    optimum > 1e-3
  s5_diag_beaten: feasible non-diagonal improvement > 1e-4 bits
  s6_gain_monotone: gap_8 < gap_16 < gap_inf
  s6_gain_value: |gap_inf - 0.0313| < 0.004
falsification: any gate failure refutes the corresponding face of
  Theorem 1 as netted (s1 the identity; s2 the feasibility scoping;
  s3 the sandwich/monotonicity; s4 the pole or its prefactor; s5 the
  class-conditional hard term -- if s5 FAILS the diagonal class might
  be optimal after all and the theorem's Remark must be retracted;
  s6 the bookkeeping refutation). Investigation at the failing gate,
  no silent re-runs.
design:
  stopping: fixed design, single governed run, seed 20261102, after
    the disclosed pilot phase (seed 20261101, three runs, all bugs
    and rescopes on record above); no further pilots or attempts
    under this ID
  runtime: ~75 s single-threaded (pilot run 2: 74.3 s)
controls: [N-only infeasible-collapse face (s2a), boundary-record
  existence exactly at the feasibility bound (s2b), rwf
  record-dependence observation recorded ungated (s4), identity gate
  tying every leak to the chain rule (s1), per-mode decomposition
  cross-check of the s6 spectral machinery (pilot, disclosed)]
amendments: []
hash: sha256:a843fb7ad3518d3871401eb63865a91d0c141d5fc7a2f17642fb48cf62ce2595
```

## Falsification

A pass nets GO-14 Theorem 1 at statement v0.2 (paper/go14-causal-
erasure.tex): the definitional fork closed, the chain rule exact,
collapse scoped to its feasibility face, the sandwich
class-conditional and decreasing, the pole cell-local-scoped with
its prefactor, and the bookkeeping reduction refuted. The full-space
minimum, the n→∞ process limit, the reset-protocol construction, and
the rwf pole characterization remain OPEN and are so marked in the
tex. The novelty sweep for the causally-conditioned-CMI framing is
OWED before any novelty language anywhere in GO-14.
