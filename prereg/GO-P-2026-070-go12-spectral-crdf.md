# GO-P-2026-070 — GO-12 Theorem 2-spectral: the spectral conditional RDF (work endpoint)

Settles GO-12 Conjecture 1's core (m=1, work endpoint): the
frequency-integral conditional rate-distortion function for the
jointly stationary Gaussian pair model — the "third promotion"
(scalars → matrices → spectra) landed for the single-consumer face.
Novelty standing: Sweep A + both library pulls + the Leiner–Gray/
Wyner frontier check all SUSTAINED (record in
`paper/go12-process-region-NOVELTY.md`); named residual library
checks on file for the venue package.

**The theorem under net (circulant embedding, work endpoint).**
L(D) = min over allocations with mean D(ω) = D of
∫ ½log₂ g*(ρ²(ω), s(ω), D(ω)/S_Y(ω)) dω/2π — per-frequency static
Theorem-2 quadratics under an equal-slope distortion allocation
(Gray's Theorem-5 decomposition pushed to the frequency continuum);
cross-mode records gain nothing (Theorem-8-style decomposition);
anchors: τ²→∞ = classical Kolmogorov–Pinsker reverse water-filling of
S_Y(ω), flat spectrum = static Theorem 2.

Governs `experiments/go12_spectral_crdf.py` (numpy+scipy, single run;
sentinel `===GO12SP-JSON===` with `===END===`; flag `GO12SP_supported`).

```yaml
id: GO-P-2026-070
date: 2026-08-05
retrospective: false
kind: theorem-verification (C3 numerical falsification of an R-IND-5-verified analytic result)
claim: "GO-12 Theorem 2-spectral (work endpoint, circulant embedding):
  the per-symbol conditional coordinate equals the equal-slope
  allocation of per-frequency static quadratic values -- L(D) = min
  over mean-D allocations of the frequency average of
  1/2 log2 g*(rho^2(w), s(w), D(w)/S_Y(w)) -- with cross-mode records
  gaining nothing, and with classical reverse water-filling (tau2 ->
  inf) and static Theorem 2 (flat spectrum) as exact anchors."
harness: experiments/go12_spectral_crdf.py   # GOVERNED seed 20261001; pilot seed 20260930, disclosed below
power: |
  Deterministic analytic-reproduction gates; per PROTOCOL 5.1 the
  bars carry pilot margins: s1 decomposition bar 2e-3 vs pilot
  2.6e-14 (~1e11x); s2 slope-spread bar 1e-6 vs 7.5e-10-scale with
  convexity probe and >=3 interior modes; s3 convergence bar 1e-4 vs
  8.1e-08 with strict Cauchy ordering; s4 anchor bars 1e-3 / 1e-9 vs
  4.4e-10 / exact. Every margin >= 1.3x.
pilot: |
  ONE pilot, seed 20260930, full harness, 95.8 s: ALL PASS with
  drafted bars unchanged (zero bar recalibrations). Values: s1 gap
  2.6e-14 (full 6-mode cross-mode matrix program vs equal-slope
  allocation); s2 spread at interior modes ~1e-9, convexity probes
  clean; s3 values 0.526349/0.529950/0.529950 (|64-256| = 8.1e-8);
  s4 classical-RWF anchor 4.4e-10, static anchor exact. Two sanity
  iterations pre-pilot fixed ALLOCATOR bugs only (grid quantization,
  then an inverted saturation clamp), both caught by the n=1 and
  slope gates themselves -- the instrument self-diagnosed; physics
  values never moved. R-IND-5 pass completed pre-seal.
prediction:
  s1_decomposition: |full - allocation| <= 2e-3 at n=6, D=0.3
  s2_slopes_convexity: interior-mode slope spread <= 1e-6 with >= 3
    interior modes; per-mode second differences nonnegative
  s3_convergence: |v64 - v256| <= 1e-4 and < |v16 - v64|
  s4_anchors: tau2=1e9 allocation within 1e-3 of classical reverse
    water-filling; n=1 within 1e-9 of static Theorem 2
falsification: s1 refutes the cross-mode decomposition (and with it
  the spectral form); s2 refutes the equal-slope/convexity structure;
  s3 refutes convergence to the integral; s4 breaks consistency with
  the classical limit or the netted static theorem
  (cross-contradiction). Instrument-vs-physics per PROTOCOL 5.1:
  SLSQP non-convergence is a logged instrumentation miss
  (dated-amendment rerun only).
design:
  stopping: fixed design, single governed run, seed 20261001, after
    the one disclosed pilot (seed 20260930); no further pilots or
    attempts under this ID
  runtime: ~2 min single-threaded (pilot: 95.8 s)
controls: [full cross-mode record matrix with dense Sigma_N (s1),
  convexity probe alongside the slope gate (s2), Cauchy-ordered
  n-sweep (s3), two independent classical anchors (s4)]
amendments: []
hash: sha256:735dcaf44f478432b0a8c0235d8b0253b004fb3d7d244f46242801ae012d8e6e
```

## Falsification

A pass completes GO-12's theory core at the work endpoint: the
spectral conditional RDF that four sweeps and three library checks
say has never been written down, netted and CI-enforced. The weighted
(two-coupled-water-levels) extension and the Toeplitz-transfer rigor
follow the verifier's scoping, recorded in the tex.
