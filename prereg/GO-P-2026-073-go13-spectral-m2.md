# GO-P-2026-073 — GO-13 Theorem 4: the spectral m=2 theorem

The campaign's unification: per-frequency Theorem-9 matrix
water-level systems, two per-consumer distortion budgets allocated by
TWO common Lagrange prices — where Conjecture 1's "pair of prices"
genuinely lives after its m=1 refutation. R-IND-5 pre-seal PASS with
five sharpenings folded (circulant load-bearing — the verifier's
Toeplitz control breaks the mapping at O(0.1); two-price rule scoped
as KKT NECESSITY with joint convexity of the per-mode value UNPROVEN
while m=2 uniqueness is open — numerically audited only, min Hessian
eig +0.33; normalization/record-class/white-residual hypotheses
pinned; slack-D_B collapses to the m=1 one-price structure at
1.4e-14). Novelty flank swept (GO-13 novelty record): the static
kernel is Xiao–Luo 2005 / Stylianou–Charalambous 2021/2024 (their
implicit static two-water-level system); claimable here: the spectral
lift, two common prices, the conditional/weighted face, the
third-party conditioner. A parallel prover attack on the m=2
moment-convexity lemma (which would upgrade necessity to sufficiency)
is in flight and does not gate this seal.

Governs `experiments/go13_spectral_m2.py` (numpy+scipy, single run;
sentinel `===GO13SM-JSON===` with `===END===`; flag `GO13SM_supported`).

```yaml
id: GO-P-2026-073
date: 2026-08-05
retrospective: false
kind: theorem-verification (C3 numerical falsification of an R-IND-5-verified analytic result)
claim: "GO-13 Theorem 4 (spectral m=2, circulant scope): the weighted
  two-consumer coordinate decomposes per-frequency into static
  Theorem-9 matrix water-level values, with the two per-consumer
  distortion budgets allocated across frequency by two common
  Lagrange prices (equal per-consumer slopes at interior modes, KKT
  necessity; sufficiency pending the m=2 convexity lemma); n=1
  recovers static Theorem 9."
harness: experiments/go13_spectral_m2.py   # GOVERNED seed 20261010; pilot seed 20261009, disclosed below
power: |
  Deterministic analytic-reproduction gates; per PROTOCOL 5.1 the
  bars carry pilot margins: s1 decomposition bar 3e-3 vs pilot
  9.9e-13 (~1e9x; deterministic per-mode warm start, 070/071
  lineage); s2 spread bars 2e-2 vs 8.7e-6/5.7e-6 with a strict
  price-gap gate 0.02 vs 0.0784 (3.9x; two genuinely distinct
  prices); s3 anchor bar 1e-6 vs 8.1e-14. Every margin >= 1.3x.
pilot: |
  ONE pilot, seed 20261009, full harness, 336.7 s: ALL PASS with
  drafted bars unchanged (zero bar recalibrations). Values: s1
  9.9e-13; s2 spreads 8.7e-6 (A) / 5.7e-6 (B), prices
  (-2.80690, -2.88527) matching the R-IND-5 verifier's independent
  values to all printed digits, gap 0.0784; s3 8.1e-14.
prediction:
  s1_decomposition: |full 6-row cross-mode program - two-price
    allocation| <= 3e-3 at n=3, w=0.5, D=(0.25,0.25),
    (rAB,rAV,rBV,a,tau2) = (0.3,0.7,0.2,0.8,0.4)
  s2_two_prices: per-consumer slope spreads <= 2e-2 across interior
    modes AND |mu_A - mu_B| >= 0.02
  s3_anchor: n=1 allocation within 1e-6 of the static Theorem-9
    program
falsification: s1 refutes the spectral m=2 decomposition; s2 refutes
  the two-price structure (equal-slope necessity); s3 breaks the
  Theorem-9 anchor (cross-contradiction with 064/067).
  Instrument-vs-physics per PROTOCOL 5.1: SLSQP non-convergence is a
  logged instrumentation miss (dated-amendment rerun only).
design:
  stopping: fixed design, single governed run, seed 20261010, after
    the one disclosed pilot (seed 20261009); no further pilots or
    attempts under this ID
  runtime: ~6 min single-threaded (pilot: 336.7 s)
controls: [deterministic per-mode warm start (070/071 lineage),
  strict price-gap gate distinguishing two prices from one (s2),
  static Theorem-9 anchor against independently netted 064/067
  machinery (s3)]
amendments: []
hash: sha256:3b7298114f6b5cfd8d57b1cded146413a6ee9b6d36166d2d41d495ff42c35fe9
```

## Falsification

A pass nets the campaign's unifying theorem at [predicted]-grade:
matrix water levels per frequency under two common prices — the third
promotion at full two-consumer generality, novelty-gated per the
multiterminal sweep. The sufficiency upgrade rides on the parallel
m=2 convexity-lemma attack (a future registration if proved).
