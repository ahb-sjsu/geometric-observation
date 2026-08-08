# GO-P-2026-074 — the m-record moment-convexity lemma: Theorem 9's uniqueness resolved, the two-price rule made sufficient

The endgame stroke: for any P ⪰ Q ⪰ 0 and any record dimension m,
G(C,V) = logdet(V−C′QC) − logdet(V−C′PC) is jointly convex on
{V−C′PC ≻ 0} — PROVED (prover-grade R-IND-5), four elementary steps
via the identity G = −logdet(I−Z) = tr f(Z), Z = R^{1/2}CM_Q⁻¹C′R^{1/2},
f(z) = −log(1−z): M_Q jointly matrix-concave, CM⁻¹C′ jointly
matrix-convex + monotone (matrix-fractional Schur certificate — the
block lift of the m=1 aa′/s argument), Z jointly matrix-convex, tr f
finishes with scalar convexity alone. Hessian decomposition
d²G = tr[(I−Z)⁻¹Z̈] + Σ|Ż_ij|²/((1−λ_i)(1−λ_j)): flats of G = level
flats of Z. Corollaries: the weighted m=2 program is CONVEX in moment
coordinates; V9 jointly convex in (D_A,D_B); optimal invariants
unconditionally unique; (C,V) unique for w∈(0,1], S₁≻0, full-rank
optimal C (failure modes: shut-off record = the water-filling
price-out; S₁-kernel meeting col(C)); the GL(m) gauge does not break
constrained uniqueness. RESOLVES GO-11 Theorem 9's uniqueness flag
(folded, GO-11 tex) and UPGRADES 073's two-price rule from necessity
to sufficiency (folded, GO-13 tex v0.7 Theorem 5).

Governs `experiments/go13_m2_convexity.py` (numpy, single run;
sentinel `===GO13MC-JSON===` with `===END===`; flag `GO13MC_supported`).

```yaml
id: GO-P-2026-074
date: 2026-08-05
retrospective: false
kind: theorem-verification (C3 numerical falsification of a PROVED analytic result)
claim: "The m-record moment-convexity lemma: G = logdet(V-C'QC) -
  logdet(V-C'PC) is jointly convex on {V-C'PC>0} for all P>=Q>=0 and
  all m, via G = -logdet(I-Z) with Z jointly matrix-convex; the
  weighted m=2 program is convex in moments, V9 jointly convex,
  Theorem 9's uniqueness resolved (full-rank scoping), the spectral
  two-price rule sufficient."
harness: experiments/go13_m2_convexity.py   # GOVERNED seed 20261013; pilot seed 20261012, disclosed below
power: |
  Deterministic analytic-reproduction gates; per PROTOCOL 5.1 the
  bars carry pilot margins: s1 identity bar 1e-11 vs pilot 1.2e-14;
  s2 zero-Jensen-violation gate over 1500 pairs across three
  families incl. m>dT (pilot 0 violations, worst midpoint excess
  exactly 0.0); s3 zero negative-curvature directions over 300
  probes (pilot 0, min curvature +0.369); s4 corollary-F and m=1
  rank-one control zero violations (pilot 0/0). Every margin >= 1.3x
  where numeric.
pilot: |
  ONE pilot, seed 20261012, full harness, 0.3 s: ALL PASS with
  drafted bars unchanged (zero bar recalibrations). Values: identity
  1.2e-14; Jensen 0/1500; curvature 0 negative with min +0.369;
  corollary 0/800 and m=1 control 0/400.
prediction:
  s1_identity: |G - (-logdet(I-Z))| <= 1e-11 over 90 feasible points,
    three (dT,m) families
  s2_jensen: zero midpoint violations (>1e-9) over 1500 random pairs
  s3_curvature: zero directions with second difference < -1e-6 over
    300 generic probes
  s4_corollary: zero violations for the weighted F (800 pairs) and
    the m=1 rank-one control (400 pairs)
falsification: any s2/s3/s4 violation refutes the lemma (and with it
  the uniqueness resolution and the sufficiency upgrade -- a
  cross-contradiction with the prover's four-step proof, to be
  investigated at the failing point); s1 refutes the Z-identity.
design:
  stopping: fixed design, single governed run, seed 20261013, after
    the one disclosed pilot (seed 20261012); no further pilots or
    attempts under this ID
  runtime: ~1 s single-threaded (pilot: 0.3 s)
controls: [m>dT family (s2), m=1 rank-one flat-by-design control
  (s4), identity gate tying numerics to the proof object (s1)]
amendments: []
hash: sha256:c7c3ee632edfb23a00cf8d8b8d8629d31dc8c44d94709bc117f5337834f7eb63
```

## Falsification

A pass nets the proof that closes the static m=2 theory: Theorem 9
fully resolved, the spectral two-price allocation globally optimal.
The lemma's proof is elementary and self-contained; the harness is a
falsification net, not the proof.

## Attribution amendment (dated 2026-08-07, post-seal, disclosed)

The (R1) novelty sweep grepped this registration and
paper/go11-conditional-region-NOVELTY.md and found the lemma
recorded only as "the verifier PROVED the assigned lemma", with **no
external attribution anywhere in the program**. Both the scalar
(aa'/s) and matrix instances are **standard convex analysis**:
the matrix-fractional function A*B^-1 A is jointly matrix-convex and
Loewner-nonincreasing in B (Boyd & Vandenberghe, *Convex
Optimization*, CUP 2004, Sec. 3.1.7 and 3.2.4), and the
Schur-complement/operator-concavity ingredient is Ando, *Concavity
of certain maps on positive definite matrices*, Linear Algebra Appl.
26 (1979) 203-241. **The program's contribution here is the LIFT
INTO THE MOMENT CHART, not the convexity.** No sealed gate, verdict
or number changes; this amendment corrects the attribution record
only. The same citations are owed wherever the lemma is invoked
(GO-13 tex; GO-14 tex Theorem R1 step 3a).