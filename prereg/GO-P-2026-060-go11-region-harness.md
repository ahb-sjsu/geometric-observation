# GO-P-2026-060 — GO-11 conditional-region theorems: C3 falsification harness

Registers the **numerical falsification harness** for the GO-11 manuscript
([`paper/go11-conditional-region.tex`](../paper/go11-conditional-region.tex)
v0.7, every theorem R-IND-5-verified pre-assertion — VERIFICATION addenda 1–4
in [`paper/go11-conditional-region-NOVELTY.md`](../paper/go11-conditional-region-NOVELTY.md)):

- **P1** (Prop. 1): the marginalization dichotomy — vector CR value =
  Gray's $\tfrac12\log_2^+(1/(2D))$, strictly below the scalar corner
  $\tfrac12\log_2((1+D)/(2D))$ on the canonical instance.
- **T2** (Thm. 2): the exact single-consumer CR function, rank-one read:
  $L(D)=\tfrac12\log_2 g^\star$, $g^\star$ the larger root of
  $Dsg^2-(D+s-\rho^2)g+(1-\rho^2)$, $s=1+\tau^2$; explicit achieving
  channel; anchors classical/Gray/Steinberg; root unique ($P(1)<0$).
- **T3** (Thm. 3 + Cor. 2): the m=1 frontier via the two-water-level
  stationarity system; strict two-corner separation (0.0400/0.0349 bits at
  (0.75, 0.5, 0.3)).
- **T5** (Thm. 5 + Cor. 3): the m=2 region as the 9-parameter matrix
  program; α=1 rate = Xiao–Luo bivariate value on-regime; the GO-10 worked
  instance decomposes exactly (tax gap $\tfrac12\log_2(1/(s^2+(1-s^2)D))$
  derived from the region); tax-note floors never violated; the
  Conjecture-3 gap positive and shrinking (reported shape gate).

Governs `experiments/verify_go11_region.py` (numpy+scipy, single run,
~10 min; sentinel `===GO11-JSON===`; summary flag `GO11_supported`).

**Attribution scope.** Fact 1 and the one-constraint region are attributed
(Paper V / rate–distortion–equivocation folklore); the rate-side reduction
targets attributed results (Gray 1973; Xiao–Luo line) — netted here as
regression anchors. GO-11's novel content under net: Prop. 1, Thm. 2,
Thm. 3/Cor. 2, Thm. 5/Cor. 3 (no prior found; sweep record in the NOVELTY
file).

```yaml
id: GO-P-2026-060
date: 2026-08-05
retrospective: false
kind: theorem-verification (C3 numerical falsification of R-IND-5-verified analytic results)
claim: "GO-11 v0.7: marginalization dichotomy (Gray value, strict gap); exact
  rank-one CR function (quadratic root, explicit channel, three anchors,
  unique root); m=1 frontier (two-water-level system, strict two-corner
  separation); m=2 region (matrix program, Xiao-Luo anchor, GO-10 corollary
  decomposition with the tax-gap formula, floors, Conjecture-3 gap shape)."
harness: experiments/verify_go11_region.py   # GOVERNED seed 20260826; pilot seed 20260825, disclosed below
power: |
  All gates are deterministic analytic-reproduction checks (no count gates,
  no stochastic pass/fail at the registered seeds); per PROTOCOL 5.1 the
  continuous bars are stated with their pilot margins: s2 bar 5e-4 vs pilot
  worst 1.2e-12; s3 corner bars 2e-3 vs pilot deviation < 1e-4; s5 anchor
  bars 5e-3/8e-3 vs pilot deviations <= 1e-4; s5 C3-strictness bar 5e-3 vs
  pilot 0.0407 (8x); s1/s4 BA windows [-0.02, +0.10] are grid-bias envelopes
  carried from the (verified) discretization behavior of the 055-lineage
  instruments. Every margin >= 1.3x; most are orders of magnitude.
pilot: |
  ONE pilot, seed 20260825, full harness, 618.9 s: ALL PASS with the drafted
  bars unchanged (no bar was recalibrated -- first registration of the
  campaign for which the pilot forced zero instrument changes). Values:
  s2 worst dev 1.18e-12; P(1)<0 sweep clean; s3 system holds at 9 combos,
  corner excesses 0.0400/0.0349 exactly; s5 GO-10 anchors R/L/taxgap to 4
  decimals at D in {0.25, 0.1}, XL anchor dev 0.00000, L-floor strictness
  0.0407, C3 gaps 0.0664 -> 0.0187 -> 0.0053 shrinking; s6 Gray sandwich
  clean. Output retained in the session transcript.
prediction:
  s1_prop1: closed forms and named-channel algebra exact (1e-10); BA nets:
    vector value in [Gray-0.02, Gray+0.10], marginalized within 0.06 of the
    corner, gap >= 0.6x predicted, at D in {0.3, 0.5}
  s2_thm2: quadratic vs 40-start SLSQP direct optimum within 5e-4 at 10
    seed-drawn instances; anchors algebraic (1e-4..1e-6); P(1)<0 on the
    900-point uniqueness sweep
  s3_thm3: stationarity system holds (3e-4) at 9 (instance, alpha) combos;
    alpha=1 rate and alpha=0 work anchors (3e-4); corner excesses within
    2e-3 of 0.0400/0.0349
  s4_nongaussian: unrestricted conditional-BA never below Thm-2 value by
    more than 0.02, never above by more than 0.10 (grid-bias envelope), at
    4 (instance, D) points
  s5_thm5: GO-10 corollary anchors within 5e-3 (R, L) and 8e-3 (tax gap)
    with corner degeneracy (2e-2); Xiao-Luo alpha=1 anchor within 5e-3;
    tax-note floors never violated (1e-6); alpha-monotonicity; L-floor
    strictly loose by >= 5e-3 at D=0.2; C3 gaps positive and strictly
    decreasing over D in {0.3, 0.1, 0.03}
  s6_cross_floors: Thm-2 values respect the Gray floor (1e-9)
falsification: any section failing its bar refutes the corresponding
  manuscript statement and sends it back to the proof (charter rules
  R-IND-5, C-AI-2). Instrument-vs-physics separation per PROTOCOL 5.1:
  SLSQP/Nelder-Mead non-convergence (a returned None or a no-success
  multi-start) is a logged instrumentation miss -- rerun only under a dated
  amendment; every other miss is a physics/derivation refutation. A BA
  point BELOW a converse value by more than the 0.02 envelope refutes the
  corresponding converse outright.
design:
  stopping: fixed design, single governed run, seed 20260826, after the one
    disclosed pilot (seed 20260825); no further pilots or attempts under
    this ID
  runtime: ~10 min single-threaded (pilot: 618.9 s)
controls: [marginalized-vs-vector BA pair (s1), non-Gaussian/unrestricted
  BA net (s4), uniqueness sweep (s2), cross-document floor sandwich
  (s5/s6), degenerate-instance ridge disclosed in-harness (s5 GO-10
  anchor)]
amendments: []
hash: sha256:b163cb2fe7b696546276c161a92892b749a78befbd63491c912fdecdae5dd3d9
```

## Falsification

The results are analytic and were each verified by fresh-context R-IND-5
passes before assertion; the harness is a falsification net, not the proof.
A mismatch on any registered prediction sends the corresponding claim back
to the proof. A pass supports citing the GO-11 manuscript's theorems at
`[predicted]`-grade in the ledger sense (theory verified + harness green);
operational faces, if ever pursued (the encoder-side tilt prediction of
Remark rem:mechanism), carry separate future registrations.
