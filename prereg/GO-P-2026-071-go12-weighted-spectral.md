# GO-P-2026-071 — GO-12 weighted spectral theorem: Conjecture 1 closed (circulant scope)

Completes the spectral pair: the weighted coordinate decomposes
per-frequency at every w, each mode carrying GO-11 Theorem 3's
two-water-level system, allocated by ONE common distortion price.
R-IND-5 pre-seal PASS with five sharpenings folded (full-region
convexity citation; for-all-D program identity + saturation extension
+ affine rescaling stated; w-coverage split (Proposition for w∈(0,1],
work-endpoint proof for w=0); Conjecture 1's "common pair of Lagrange
prices" refuted-as-phrased and rescoped to (w, μ); Gaussian-record
class + monotonicity closure stated). Verifier bonus: two independent
per-mode engines (channel SLSQP vs stationarity-system root solver)
agree to 8.2e-15 over 120 configs with a unique system root
everywhere.

Governs `experiments/go12_weighted_spectral.py` (numpy+scipy, single
run; sentinel `===GO12WS-JSON===` with `===END===`; flag
`GO12WS_supported`).

```yaml
id: GO-P-2026-071
date: 2026-08-05
retrospective: false
kind: theorem-verification (C3 numerical falsification of an R-IND-5-verified analytic result)
claim: "GO-12 weighted spectral theorem (circulant scope): J_w(D) =
  equal-slope allocation of per-mode static weighted values at every
  w in [0,1]; per-mode convexity via full-region moment convexity +
  perturbation; per-frequency two-water-level profiles coupled
  through one common distortion price; anchors w=1 classical RWF,
  w=0 the 070 theorem, n=1 static."
harness: experiments/go12_weighted_spectral.py   # GOVERNED seed 20261004; pilot seed 20261003, disclosed below
power: |
  Deterministic analytic-reproduction gates; per PROTOCOL 5.1 the
  bars carry pilot margins: s1 decomposition bar 2e-3 vs pilot
  6.9e-14 (~1e10x) at w in {0.5, 0.75} with deterministic warm start
  (070-amendment lineage, environment-robust by design); s2 slope
  bar 5e-3 vs 3.7e-6 with convexity probes; s3 anchor bars 5e-3 vs
  1.6e-5 (classical RWF at w~1) and 2.2e-7 (070 closed form at w~0).
  Every margin >= 1.3x.
pilot: |
  ONE pilot, seed 20261003, full harness, 219.6 s: ALL PASS with
  drafted bars unchanged (zero bar recalibrations). Values: s1 worst
  gap 6.9e-14; s2 spread 3.7e-6, second differences nonnegative; s3
  RWF dev 1.6e-5, w~0 dev 2.2e-7. R-IND-5 pass completed pre-seal;
  harness computationally unchanged from the piloted version.
prediction:
  s1_decomposition: |full - allocation| <= 2e-3 at n=5, D=0.3,
    w in {0.5, 0.75}
  s2_convex_slopes: per-mode second differences >= -1e-6 on 3 probe
    modes; interior slope spread <= 5e-3 at the w=0.5 optimum
  s3_anchors: w=0.9999 allocation within 5e-3 of classical reverse
    water-filling of S_Y; w=1e-6 allocation within 5e-3 of the
    070-theorem closed form at the same allocation
falsification: s1 refutes the weighted decomposition; s2 refutes
  per-mode convexity/equal slopes; s3 breaks consistency with the
  classical limit or the netted 070 theorem (cross-contradiction).
  Instrument-vs-physics per PROTOCOL 5.1: SLSQP non-convergence is a
  logged instrumentation miss (dated-amendment rerun only).
design:
  stopping: fixed design, single governed run, seed 20261004, after
    the one disclosed pilot (seed 20261003); no further pilots or
    attempts under this ID
  runtime: ~4 min single-threaded (pilot: 219.6 s)
controls: [deterministic warm start (070 lineage), two weights for
  s1, convexity probe with the slope gate (s2), both endpoint anchors
  against independently netted theorems (s3)]
amendments: []
hash: sha256:2d520f23578d98a4519c90d3846f1d3eb484a4b618cb5bf711a04b89b05f9b01
```

## Falsification

A pass closes GO-12 Conjecture 1 at circulant scope: the complete
weighted spectral theory — the third promotion on both faces of the
region. Remaining GO-12 opens: the Toeplitz-transfer lemmas and the
process-rate causal object.
