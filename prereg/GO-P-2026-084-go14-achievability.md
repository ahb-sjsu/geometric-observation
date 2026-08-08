# GO-P-2026-084 — Lemma W, the FIR-density residual, and the unconditional brackets

The converse direction, taken as far as it honestly goes. Prover +
R-IND-5 pass on record (paper/go14-causal-erasure-PROBE.md); tex
v0.9 carries the material with **W1–W12 folded into the statements
themselves**, not appended as remarks — the verifier was explicit
that a seal carrying the old wording should FAIL.

**THE HEADLINE, and it depends on NO LEMMA OF THIS DOCUMENT.**
L^∞(Δ) ∈ [Ψ^LB(Δ), V(10,2048;Δ)] at Δ = 0, 1, 2:
**[0.5627264963, 0.5627656412] / [0.5364013784, 0.5364458112] /
[0.5310500198, 0.5310994872]** — the lower end by Corollary
`cor:onedir`, the upper end the value of an **explicit,
exactly-D-feasible F0 record on n = 2048** (depth-10 truncated
stationary FIR kernels with a closed-form scalar noise rescale),
evaluated by exact Cholesky and admitted through Corollary
`cor:lower`. Upper ends outward-rounded at 1e-10 under the house
convention. **A 51.5× narrowing at Δ=0.** The only inputs are F0
membership, exact feasibility, and correct evaluation — all three
checked independently.

**LEMMA W (window transfer).** For a stationary F0 record with FIR
kernels of depth ≤ L and MA(L) noise bounded away from 0, and for
every window length **n ≥ n₀(L)** (an explicit hypothesis — the
zero-edge build is INFEASIBLE at small n: the repairing rescale is
c = −0.832 at n=64, L=10), the repaired windowed record is in F0,
is exactly D-feasible, and satisfies
φ_n ≤ L_a(x^(n)) ≤ rate(x) + C(L,n)/n where **C(L,n) is MONOTONE
DECREASING in n with sup_{n≥n₀(L)} C(L,n) < ∞ — only C(L,n) = o(n)
is used, and NO CLAIM THAT C IS INDEPENDENT OF n IS MADE ANYWHERE**
(the witness: 71.76 → 12.65 over n = 64…1024). Its two legs carry
**opposite and both-favourable signs**: the boundary leg
Σ_t δ_t ≥ 0 is *exactly* n-independent (0.043994832 / 0.051454447 /
0.052333440 at Δ = 0/1/2, L = 10, identical to 9 decimals over
n = 128…1024 and L = 4…12) and the Szegő noise leg is ≥ 0 and
n-independent (+8.622e-3 / +1.079e-2 / +1.076e-2), entering with the
helping sign. Edge cells contribute **exactly** zero.

**THREE BUILDS, KEPT APART** (W3): zero-edge (what steps 1–2
prove), truncated-taps (**what every quoted constant and every
bracket endpoint comes from**), and repaired (what feasibility
requires) — with the explicit statement that **steps (1)–(2) do NOT
apply to the truncated-taps build**. The **repair leg is a SEPARATE
estimate** not covered by steps (1)–(5) (W4).

**THE RESIDUAL — exactly one thing**: FIR-kernel stationary records
dense in value. R is **measured ≤ 1.5e-12 against a NAMED reference**
(the grid fixed point, Nf=4096/P=180); against the 082 certified LB
endpoints the gap is +4.0e-11 / +7.2e-11 / +5.3e-11; **L ≥ 11
entries are f64 noise going NEGATIVE at Δ=0 and are explicitly NOT
cited as convergence evidence** (W8). The squaring is quoted in its
sharp form — (U−Ψ)/T² = 4.3–4.8, constant over L = 1…6 — and the ρ*
cross-link is labelled a **consistency check, not an independent
reproduction** (W7).

Governs `experiments/go14_achiev.py` (numpy/scipy, CPU, single run;
sentinel `===GO14AC-JSON===` with `===END===`; flag
`GO14AC_supported`). **No optimizer, no fixed point, no root find
anywhere** — stationary kernels are pinned data.

```yaml
id: GO-P-2026-084
date: 2026-08-07
retrospective: false
kind: theorem-verification (C3 net for Lemma W, the residual's scoping, and the unconditional brackets; prover + R-IND-5 pass with W1-W12 on record)
claim: "Lemma W: any depth-L FIR stationary F0 record transfers to a
  finite window at n >= n0(L) with phi_n <= rate + C(L,n)/n, C monotone
  decreasing in n with finite supremum (NOT independent of n); its
  boundary and Szego legs are exactly n-independent and carry opposite,
  both-favourable signs; edge cells contribute exactly zero. Hence
  L^inf <= Psi + R with R measured against a named reference and proved
  zero only conditional on FIR density. Unconditionally, and depending
  on no lemma of the document: L^inf(Delta) lies in the stated brackets
  at Delta = 0,1,2, a 51.5x narrowing at Delta=0."
harness: experiments/go14_achiev.py   # GOVERNED seed 20261171; pilot seed 20261170, disclosed below
power: |
  Deterministic gates; CI-ROBUST BY CONSTRUCTION -- no optimizer,
  fixed point or root find anywhere, so no gate can race a solver,
  and the three certificate widths are REPORTED ONLY, never gated.
  Margins: s1 6.5e3x and 2252x with the must-fail reversed-kernel
  control at 1.26x (fat-margin twin 1.65x/3.29x) and the W5 negative
  control at 4.5x; s2 5848x with per-cell CMI exactly 0; s3 129x and
  zero negative cells past saturation; s4 5181x and 30x; s5 8.6x and
  93x; s6 6x/6x with the must-fail infeasibility control at 8.3x;
  s7 18/18 rows and 1.42x -- GATING MONOTONICITY, NEVER
  n-INDEPENDENCE; s8 bit-exact reproduction, 8/8 anchors at 5.0x,
  outward rounding 3/3; s9 86x and 89x.
pilot: |
  ONE pilot, seed 20261170, ALL PASS 31/31 on the FIRST iteration,
  47.2 s; the governed payload is BIT-IDENTICAL apart from the seed
  stamp. NO BAR WAS MOVED AT ANY POINT -- every bar was fixed
  beforehand from the verifier's artifacts plus a pre-pilot
  calibration.
  FOUR DISCLOSURES: (a) the 1.26x reversed-kernel gate is a labelled
  CLAIM REPRODUCTION, carried with a fat-margin twin (1.65x/3.29x);
  (b) the ~0.105/n block convergence and the +1.70e-12 ladder entry
  are carried as R-IND-5 LITERALS, not re-derived (they need per-
  Delta fixed-point solves), and the +1.19e-9 ladder excess is an
  artefact of the tex's 9-decimal printing; (c) the V(10,2048) gate
  is a REGRESSION gate, not independent confirmation; (d) the
  reversed-kernel >= 1e-2 gate holds at Delta=0 where it is
  recorded -- at Delta=1,2 the same defect measures +1.96e-3 and
  +2.98e-4, REPORTED UNGATED. Two measurement corrections to the
  record are printed rather than the recorded values: the Szego leg
  is 0.0086219/0.0107925/0.0107555 (the recorded 6-decimal form was
  wrong in the sixth decimal), and W12 closes to 3.7e-6 at n=2048,
  not 2e-6, with the residual itself O(1/n).
prediction:
  s1_orientation: canonical sigma_t offset < 1e-12 over 480 interior
    cells AND the reversed-a_v control >= 1e-2 at every interior
    cell (must-fail); AND the W5 NEGATIVE control -- distortion
    unchanged under reversal (< 1e-15), i.e. the distortion gate has
    ZERO power
  s2_edge: per-cell CMI exactly 0 (< 1e-15) and Nc block-diagonality
    < 1e-9
  s3_subset: zero negative delta_t over Delta in {0,1,2,3,5,9,20},
    including past saturation (min > -1e-13)
  s4_nindep: sum delta_t identical over n in {128,256,512} at
    L in {4,10} (spread < 1e-9), reproducing the recorded triple
    within 1e-8
  s5_szego: the leg >= 1e-3, flat in m (< 1e-9), and min-phase
    <ln n(w)> = 2 ln q0 (< 1e-12)
  s6_repair: affineness and dist-D < 1e-15; AND the zero-edge build
    at n=64, L=10 is INFEASIBLE (rescale < -0.10, must-fail), while
    n=128 is feasible (> 0.05)
  s7_monotone: C(L,n) STRICTLY DECREASING in n over the pinned
    (L,n) grid, 18/18 rows, with the witness factor > 4.0 --
    gating MONOTONICITY, never n-independence
  s8_brackets: V(10,2048) reproduces the three recorded values
    (< 1e-9); exact feasibility (< 1e-15); the 8/8 anchor
    cross-check with min margin > 1e-4; outward rounding 3/3
  s9_not_too_much: the block-schedule bound stays ABOVE
    block_inf = 0.5299499808119 (> 1e-4) and monotone; the
    Delta-ladder approaches from above without crossing
falsification: s1 fail refutes the orientation discipline -- and its
  must-fail control failing would mean the defect is harmless,
  contradicting the measured O(n) growth; s2/s3 fail refute Lemma
  W's exact-zero and subset steps; s4 fail refutes the boundary
  leg's n-independence (the one thing that IS n-independent);
  s5 fail refutes the sign of the helping leg; s6 fail refutes the
  repair or the feasibility threshold; s7 fail refutes the CORRECTED
  monotonicity claim -- and would vindicate nothing, since
  n-independence is not claimed; s8 fail refutes the brackets, which
  depend on no lemma and are the registration's headline; s9 fail
  would mean the machinery proves too much. Single governed run, no
  silent reruns.
design:
  stopping: fixed design, single governed run, seed 20261171, after
    the one disclosed pilot (seed 20261170); no further pilots or
    attempts under this ID
  runtime: ~50 s single-threaded (pilot 47.2 s, governed 53.6 s)
controls: [the reversed-kernel orientation control converting an
  n-independent charge into an O(n) one (s1), the W5 negative
  control showing the distortion gate has zero power (s1), the
  infeasible small-window build (s6), and the does-not-prove-too-
  much check against an independently certified value (s9)]
amendments: []
hash: sha256:927a53733ed4458e20f9789abf662f3a5a77143f115d3d17cd3a50cfdb367556
```

## Falsification

A pass nets Lemma W with its corrected constant and explicit
threshold, the three-build separation, the residual's scoping, and
the unconditional brackets. What this registration does NOT claim,
and what a seal printing otherwise must FAIL: that L^∞ coincides
with Ψ (the density residual is measured, not proved), that C is
independent of n (**refuted, and the refutation is why W1 exists**),
or any reverse inequality. The two inequalities come from
structurally independent arguments: **together they give a bracket,
never an equality.** OPEN: the FIR-density link — one contraction
estimate in the Wiener norm, a small well-posed problem — and the
novelty sweep on Lemma W's combination (Collapse + subset-
conditioning monotonicity + Toeplitz innovation monotonicity as a
signed two-leg boundary argument), OWED before any novelty language.
