# GO-P-2026-072 — GO-13 Theorem 3: the binary twin of the access-class theory

Settles GO-13 Question 2. R-IND-5 pre-seal PASS at machine/50-digit
precision with six sharpenings folded (two numeric corrections now in
the statement: the D=0.05 gap is +7.1e-5 and the near-universality
envelope is ≤2.1e-4 over D∈[0.02,0.40], one-point fit; the
H(Ŷ|G=g)=h₂(a∗r_g) mechanism is per-atom independence J ⊥ (V_t,G),
not atom pairing; slice convexity upgraded to a proof; explicit
finite-G hypotheses; d_j ∈ (0,1) regime wording).

**The theorem under net.** (i) Slice collapse exact: q_eff = q∗δ_Δ
(chain reversibility + BSC composition). (ii) The σ-symmetric family
is optimal for every finite access class, with closed form
L_G = E_r[h₂(a∗r)] − (1−p)h₂(d₀) − p·h₂(d₁), r the posterior
reliability distribution. (iii) Generalized tilt
ℓ(d₀)−ℓ(d₁) = 2·E_r[(1−2r)ℓ(a∗r)], sufficient by slice convexity.
(iv) Exact non-collapse: no single q_eff reproduces a general class's
curve (true model gap ~9e-5, 46 orders above precision) — the
Gaussian equal-q universality is exactly a Gaussian privilege — while
the binary family is numerically NEAR-universal (envelope reported,
observation-grade only).

Governs `experiments/go13_binary_twin.py` (numpy+scipy, single run;
sentinel `===GO13BT-JSON===` with `===END===`; flag `GO13BT_supported`).

```yaml
id: GO-P-2026-072
date: 2026-08-05
retrospective: false
kind: theorem-verification (C3 numerical falsification of an R-IND-5-verified analytic result)
claim: "GO-13 Theorem 3 (binary twin): slice access collapses exactly
  to Theorem 10 at q_eff = q * delta_Delta; the sigma-symmetric
  family is optimal for every finite access class with
  L_G = E_r[h2(a*r)] - (1-p)h2(d0) - p h2(d1) and generalized tilt
  l(d0)-l(d1) = 2 E_r[(1-2r) l(a*r)]; single-q universality fails
  EXACTLY in binary (gap ~9e-5, real at 50-digit precision) though
  the family is numerically near-universal."
harness: experiments/go13_binary_twin.py   # GOVERNED seed 20261007; pilot seed 20261006, disclosed below
power: |
  Deterministic analytic-reproduction gates; per PROTOCOL 5.1 the
  bars carry pilot margins: s1 slice bar 1e-8 vs pilot 8.1e-15; s2
  closed-form bar 1e-7 vs 9.7e-15, tilt bar 1e-4 vs 6.3e-8; s3
  two-sided window [1e-11, 5e-4] vs 8.9e-5 (the exact-non-collapse
  gate: below 1e-11 would mean the gap is solver noise, above 5e-4
  would contradict the verifier's 50-digit values); s4 anchor bars
  1e-8 / 1e-9 vs 1.4e-14 / 1.1e-16. Every margin >= 1.3x.
pilot: |
  ONE pilot, seed 20261006, full harness, 3.2 s: ALL PASS with
  drafted bars unchanged (zero bar recalibrations). Values: s1
  8.1e-15; s2 9.7e-15 / 6.3e-8; s3 gaps +7.11e-5 (D=0.05) and
  -8.88e-5 (D=0.15), matching the verifier's independent 50-digit
  computation to all printed digits; s4 1.4e-14 / 1.1e-16. Two
  pre-pilot sanity iterations fixed a two-sided chain-enumeration
  bug (caught by the direct-optimization cross-check) and re-gated
  s3 from an arbitrary 1e-4 threshold to the exact-non-collapse
  criterion after the honest finding that near-universality holds.
prediction:
  s1_slice: |thm10(q*delta_2) - direct| <= 1e-8 at D=0.1
  s2_family: closed form vs direct <= 1e-7 and generalized-tilt
    residual <= 1e-4 at D in {0.05, 0.10, 0.15}, class {S_{t-1},
    S_{t+1}}, (p,f,q) = (0.25, 0.15, 0.1)
  s3_noncollapse: with q_eff fitted at D=0.10, the max |gap| at
    D in {0.05, 0.15} lies in [1e-11, 5e-4]
  s4_anchors: Delta=0 slice matches static Thm 10 to 1e-8; useless
    context matches 1 - h2(D) to 1e-9
falsification: s1 refutes the BSC-composition collapse; s2 refutes
  family optimality or the reliability-distribution closed form; s3
  BELOW 1e-11 refutes exact non-collapse (would establish binary
  universality, contradicting the verifier's 50-digit gap — a
  cross-contradiction to investigate), ABOVE 5e-4 contradicts the
  verified gap values; s4 breaks the Theorem-10 anchor.
  Instrument-vs-physics per PROTOCOL 5.1: SLSQP non-convergence is a
  logged instrumentation miss (dated-amendment rerun only).
design:
  stopping: fixed design, single governed run, seed 20261007, after
    the one disclosed pilot (seed 20261006); no further pilots or
    attempts under this ID
  runtime: ~4 s single-threaded (pilot: 3.2 s)
controls: [direct channel optimization as ground truth throughout,
  two-sided s3 window pinned to the verifier's independent 50-digit
  values, exact-joint enumeration (no sampling), both anchors]
amendments: []
hash: sha256:33fc7f6f3744d227d83db7534891aa3966d7ef3999953f05b5948a9e465eb7f8
```

## Falsification

A pass nets the binary twin: the access-class theory's dichotomy —
universality exactly Gaussian, approximately binary — becomes a
harness-enforced result, completing GO-13's theory rungs.
