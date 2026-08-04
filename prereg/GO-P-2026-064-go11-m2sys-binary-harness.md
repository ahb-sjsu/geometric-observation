# GO-P-2026-064 — GO-11 v0.11 closing theorems: C3 falsification harness

Registers the **numerical falsification harness** for GO-11's two newest
R-IND-5-verified results
([`paper/go11-conditional-region.tex`](../paper/go11-conditional-region.tex),
verification addenda 7–8 in
[`paper/go11-conditional-region-NOVELTY.md`](../paper/go11-conditional-region-NOVELTY.md)):

- **T9** (Thm. 9, the m=2 frontier system): the two-water-level structure
  survives two consumers with **matrix water levels** — FOC-N
  Σ_N⁻¹ = wM₀⁻¹ + (1−w)M₁⁻¹ + diag(μ) *including its off-diagonal*, the
  per-mode 2×2 resolvent formula
  a_j = [Σ_N⁻¹ + (1−w)(λ_j−1)M₁⁻¹]⁻¹ diag(μ) ỹ_j, and the strengthened
  w=1 anchor (read-span record; μᵢ = 1/Dᵢ and error covariance
  exactly diag(D) with **no symmetry assumption**, on the Xiao–Luo regime).
- **T10** (Thm. 10, binary conditional CR function): for the DSBS(p) pair
  with context S = V⊕Bern(q), the exact conditional coordinate is attained
  in the symmetric (d₀,d₁) family with the **tilt equation**
  ℓ(d₀) − ℓ(d₁) = 2(1−2q)ℓ(u), closed form
  L = h₂(u) − (1−p)h₂(d₀) − p·h₂(d₁), Fact-1 face R − L = 1 − h₂(u),
  Gray (q=0) and marginal (q=½) anchors.
- **X** (cross-net): T10 retro-derives the 062 noisy-face discount
  (sealed artifact 0.34324, previously formula-less) as
  1 − h₂(1/12 ∗ 0.1) = 1 − h₂(1/6) = 0.34998, with instrument bias
  required to match the same run's explained face.

Governs `experiments/verify_go11_m2sys_binary.py` (numpy+scipy, single
run; sentinel `===GO11MB-JSON===`; summary flag `GO11MB_supported`).

```yaml
id: GO-P-2026-064
date: 2026-08-04
retrospective: false
kind: theorem-verification (C3 numerical falsification of R-IND-5-verified analytic results)
claim: "GO-11 v0.11: the m=2 Pareto frontier satisfies the matrix
  water-level system (FOC-N with off-diagonal, per-mode 2x2 resolvents,
  strengthened w=1 anchor), and the binary conditional CR function is the
  symmetric-family tilt-equation solution with closed form and exact
  Fact-1 face, retro-deriving 062's noisy-face discount."
harness: experiments/verify_go11_m2sys_binary.py   # GOVERNED seed 20260910; pilot seed 20260909, disclosed below
power: |
  Deterministic analytic-reproduction gates; per PROTOCOL 5.1 the bars
  carry pilot margins: s1 off-diagonal bar 5e-4 vs pilot 1.3e-7 (~4000x),
  per-mode bar 5e-4 vs 2.3e-8; s2 read-span bar 5e-4 vs 1.0e-8, |mu D - 1|
  bar 2e-3 vs 1.5e-8, error-covariance bars 2e-3 vs <=4.7e-10; s3 tilt bar
  2e-5 vs 9.9e-8 (200x), Fact-1 bar 1e-10 vs 5.6e-17, closed-form bar 1e-9
  vs 1.1e-16; s4 certificate bar 1e-6 vs <=3.7e-14; s5 anchor bars 1e-8 vs
  1.1e-16, d0=d1=D bar 1e-5 vs 4.2e-9; s6 |bias| bar 0.015 vs 0.0067
  (2.2x), paired-bias bar 0.008 vs 0.0013 (6.3x). Every margin >= 1.3x.
pilot: |
  ONE pilot, seed 20260909, full harness, 192.8 s: ALL PASS with the
  drafted bars unchanged (zero bar recalibrations -- fourth consecutive
  clean first pilot under 5.1, after 060/062/063). Values: FOC-N
  off-diagonal 1.3e-7; per-mode column 2.3e-8; zero solver misses; w=1
  read-span 1.0e-8, |mu_i D_i - 1| 1.5e-8, error covariance off-diagonal
  4.7e-10 / diagonal 7.9e-15 vs diag(D); tilt 9.9e-8; Fact-1 5.6e-17;
  certificates <=5.7e-15 (K=2/4) and 3.6e-14 (K=6); Gray and marginal
  anchors 1.1e-16; noisy-face bias -0.0067 vs explained-face bias -0.0080
  (paired difference 0.0013).
prediction:
  s1_m2sys: FOC-N off-diagonal residual <= 5e-4 and per-mode resolvent
    column residual <= 5e-4 at the 50/60-start m=2 program optimum, over
    two scalar-context instances (w in {0, 0.5, 1}) and one r=2
    vector-context instance (w in {0, 0.5}); zero solver misses
  s2_w1_anchor: at w=1 with ASYMMETRIC distortions (0.15, 0.35):
    read-span residual |A - Sigma_N diag(mu) Ytil| <= 5e-4;
    |mu_i D_i - 1| <= 2e-3; error-covariance off-diagonal <= 2e-3 and
    diagonal within 2e-3 of diag(D)
  s3_bin_family: tilt-equation residual <= 2e-5, Fact-1 face
    |(R-L) - (1-h2(u))| <= 1e-10, closed-form-vs-channel match <= 1e-9,
    at four (p,q,D) instances
  s4_bin_cert: unconditional Lagrangian certificate gaps <= 1e-6 against
    reproduction alphabets K=2 and K=4 at all four instances and K=6 at
    (0.25, 0.2, 0.1)
  s5_bin_anchors: q=0 equals Gray h2(p)-h2(D) to 1e-8; q=1/2 equals
    1-h2(D) to 1e-8 with d0=d1=D to 1e-5; L monotone in q
  s6_062_crossnet: derived noisy discount 0.34998 within 0.015 of the
    sealed 062 artifact value 0.34324, AND the noisy-face bias matches
    the explained-face bias (measured 0.57818 vs derived 0.58618) within
    0.008
falsification: any section failing its bar refutes the corresponding
  theorem statement and sends it back to the proof (charter rules
  R-IND-5, C-AI-2). Instrument-vs-physics separation per PROTOCOL 5.1:
  SLSQP/BFGS non-convergence (s1 solver miss; certificate multi-start
  failure) is a logged instrumentation miss (dated-amendment rerun only);
  a NEGATIVE certificate gap beyond -1e-6 at s4 refutes family optimality
  outright; an s6 bias mismatch beyond the envelope refutes the
  retro-derivation claim (not the 062 verdict, which stands as sealed).
design:
  stopping: fixed design, single governed run, seed 20260910, after the
    one disclosed pilot (seed 20260909); no further pilots or attempts
    under this ID
  runtime: ~3 min single-threaded (pilot: 192.8 s)
controls: [r=2 vector-context instance (s1), asymmetric-distortion w=1
  anchor (s2), Fact-1 exact face (s3), alphabet-2/4/6 certificates (s4),
  two classical anchors + monotonicity (s5), sealed-artifact cross-net
  with paired-bias gate (s6)]
amendments: []
hash: sha256:ab9e928689b7b677cdf3e988aa347270895db18c439c6c74f9c4bd6dbbc19473
```

## Falsification

The results are analytic and R-IND-5-verified; the harness is a
falsification net, not the proof. A pass supports citing Theorems 9–10
at `[predicted]`-grade alongside the 060/063-netted content; GO-11's
overall `[replicated]` class (operational, 061/062) is unaffected either
way. The s6 cross-net is a consistency gate on already-sealed numbers:
it can refute the *retro-derivation remark*, never the 062 run.
