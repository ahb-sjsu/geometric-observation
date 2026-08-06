# GO-P-2026-080 — the n-transfer theorem, the (H*) refutation, and the certified within-class ladder

The GO-14 limit face closed as far as it honestly goes, with the
part that did NOT survive gated as a finding. Prover + R-IND-5 pass
on record (paper/go14-causal-erasure-PROBE.md); tex v0.5 carries all
six mandatory restatements.

**UNCONDITIONAL (Theorem T).** Exact subadditivity
f(n1+n2) ≤ f(n1)+f(n2) by block concatenation (per-cell numerator
shrinks under the superset conditioning; denominators block-local by
U-independence), hence by Fekete — with the hygiene the verifier
demanded (φ_n ≥ 0 because each per-cell term is a CMI; ε-optimal
concatenation, attainment never used) — **L^∞ = lim φ_n = inf φ_n
EXISTS**, and the lower transfer side 0 ≤ φ_n − L^∞ is a theorem
(giving L^∞(0) ≤ 0.5647419677).

**REFUTED, and gated as such.** "Per-side boundary charge ≤ κ" is
FALSE as an F0 lemma: D-feasible U-independent counterexamples reach
D2 ≈ 0.77 (exceeding the sharpened c(0) = 0.4202858) and ≈ 13.9 bits
≈ 19κ, with worst case Θ(m) — no universal constant exists, and no
proof of the reverse direction can avoid optimizer structure. (The
verifier's own witnesses gave 0.4563 and 18.93 bits; the harness
pins independently re-derived witnesses of the same class — same
refutation, different records, both on record.)

**CONDITIONAL on (H*)** — the numbered hard hypothesis "at every
optimizer of the dyadic chain n·2^k, D1+D2 ≤ c(Δ;n)", with
c(Δ;n) = (2−1{Δ=0})κ − I_n, I_n monotone increasing (so the constant
is uniformly valid from the base n), c(0) ≤ 0.42029, **c(1) ≤ 1.1258**
(the 5th-decimal erratum corrected), c(2) ≤ 1.1219: the reverse
direction, the upper transfer bound φ_n − L^∞ ≤ c/n, and the plateau
corollary L^∞(0) ≥ 0.5515989 > 0.5479448 (sealed 079
LB(32,0) = 0.5647327869; margin 3.654e-3 = 215× the tex-v0.4 width,
398× the sealed width). Base n=24 FAILS by 4.7e-5 — (H*) carries no
slack. Optimizer verifications: D2 = 0.076971/0.076926 and
I(E;T^{b2}) = 0.543 (0.19 bits under κ) at m ∈ {8,16} ONLY.
REPAIR PATH recorded: an optimizer-regularity bound on I(E;T^{b2})
via the Theorems R+C convex structure restores the unconditional
label with the same constants.

**Within-class ladder EXECUTED**: nine diag-class ladder cells
(24/32/48 × 4/5/6) plus three block values certified two-sided
(widths 2.2e-7–1.6e-6); the E_∞ re-assembly is tagged
1/n-MODEL-conditional, not certificates (E_∞(4) in bar, E_∞(5)
positive, E_∞(6) bracket contains 0 — re-ratifying the raw-anchor
demotion); the unverifiable "4/9 endpoints were true class minima"
claim is WITHDRAWN.

Governs `experiments/go14_transfer.py` (numpy/scipy, CPU, single
run; sentinel `===GO14TR-JSON===` with `===END===`; flag
`GO14TR_supported`). Model as netted; family F0 (U-independent),
κ = ½log₂(1/(1−a²)) = 0.736966.

```yaml
id: GO-P-2026-080
date: 2026-08-06
retrospective: false
kind: theorem-verification (C3 net for Theorem T + the (H*) refutation + the within-class ladder; prover + R-IND-5 pass with six restatements on record)
claim: "GO-14 transfer face (tex v0.5): exact subadditivity + Fekete give
  the process limit UNCONDITIONALLY and the lower transfer side as a
  theorem; 'per-side boundary charge <= kappa' is REFUTED as an F0 lemma
  by D-feasible counterexamples (Theta(m) worst case); the reverse
  direction, the upper bound, and the Delta=0 plateau corollary hold
  conditional on the numbered hypothesis (H*) with c(0) <= 0.42029,
  c(1) <= 1.1258, c(2) <= 1.1219; the diag-class ladder is certified
  two-sided within class."
harness: experiments/go14_transfer.py   # GOVERNED seed 20261131; pilot seed 20261130, disclosed below
power: |
  Deterministic gates; CI-ROBUSTNESS BY DESIGN -- no gate races an
  optimizer stopping point (s1/s2/s3/s6 contain no optimizer at all;
  s4 is fully analytic; s5/s7 gate identities between independent
  evaluators, fat-margin inequalities, or reproduction bands 5-6
  orders above the endpoint spread; no width, bracket, or
  certificate is gated anywhere -- the 079 lesson). Margins:
  s1 49x/47x + slack 2.0e-2; s2 exact (0 failures, 160 cells);
  s3 49x and 4.4x/1.9x on the counter-values, reproduction exact;
  s4 1.84x and 1.39x (the refutation, analytic witnesses);
  s5 5.5x on D2, 0.19 bits on I(E;T^b2), reproduction 450x-75000x,
  evaluator identity 1.6e5x; s6 770x, exact sealed-LB match, 1.2x
  on the plateau margin and 4.7x on the n=24 shortfall;
  s7 exact anchors, 6.5x Fekete slack, 6.7-40x decreases, 9.1x
  worst ladder cell.
pilot: |
  TWO pilot runs, seed 20261130, disclosed: run 1 = 21/23 (a rec_of
  bug -- noise covariance halved twice -- and two too-weak s4
  witness constructions); run 2 = ALL PASS 23/23, 348 s, two
  consecutive runs bit-identical. NO BAR WAS LOOSENED AGAINST A
  MEASUREMENT: the s4 records were STRENGTHENED until the refutation
  carried at the constants already written down. Four further
  disclosures: (a) s4 witnesses are independent re-derivations (the
  verifier's records are not in-repo) giving 0.7749 / 13.94 bits vs
  the recorded 0.4563 / 18.93 -- same refutation, different
  witnesses, both in the tex; (b) s7 takes the RECOMPUTE route
  (winner parameters not in-repo), gated at 1e-5 against recorded
  raw values rather than bracket-containment, because the two
  recorded end-to-end computations of (48,6) differ by 1.1e-6 at the
  UB end -- a 2x-widened bracket gate would have raced; the
  recomputed (48,6) sits 1.2e-8 above the prover's certified UB (a
  slightly worse feasible point, no contradiction); (c) s5 bands are
  deliberately loose (5e-3/2e-2) because they are the only
  quantities read at an optimizer endpoint -- the requested 1e-4
  would have passed at 9x, the shipped bar passes at 450x;
  (d) I_n monotonicity carries a 1e-12 tolerance because the
  n=24->32 step is -2e-16 (f64 noise), so a strict gate would fail
  on arithmetic rather than on the claim.
prediction:
  s1_subadditivity: per-term big <= own at all 168 cells for
    (n1,n2) in {(8,8),(8,4)} x Delta in {0,2}; block-local
    denominators to 1e-12; totals inequality strict
  s2_set_identity: bigC_t = ownC_t union E as a formal set-diff,
    plus the interleaved order and k(j), zero failures over 160
    cells at m in {3,5,8} x Delta in {0,1,2,m-1,m}
  s3_zero_claim: |I(E;S'_j|pfx_j,T^b2)| < 1e-12 for pinned F0
    records; the pinned U-coupled counterexamples exceed 0.05 bits
    (block-1 and block-2-only); recorded counter-values reproduced
  s4_refutation: the pinned two-V-copy record gives D2 > c(0) =
    0.4202858 and the three-Y-copy record gives D2 > 10 bits --
    "kappa per side" is FALSE (gated as a finding, 076 s2a
    precedent)
  s5_optimizer_values: D2 < c(0) and I(E;T^b2) < kappa - 0.10 at
    m in {8,16}; recorded values reproduced within the disclosed
    bands; evaluator identity vs the certified UB < 1e-9
  s6_constants: I_n monotone and converged by n=16; c(0/1/2) equal
    the stated values to 1e-6 with c(1) > 1.1257 (the erratum); the
    sealed LB(32,0) matches results/GO14-convexity.json exactly; the
    plateau arithmetic clears with ratio in [210, 220]; the n=24
    base FAILS with shortfall > 1e-5
  s7_anchors_ladder: phi_4/phi_8/phi_12 reproduced to 1e-5; Fekete
    slack > 1e-2; phi_8 > phi_16 > phi_24 > phi_32 with gaps > 1e-4;
    the 9 diag-class ladder values and 3 block values reproduce the
    recorded raw values to 1e-5
falsification: s1/s2 fail refutes Theorem T's concatenation or its
  set identity (the unconditional limit dies); s3 fail refutes the
  F0-conditionality structure; s4 fail would mean the counterexamples
  do not carry -- (H*) would be unnecessary and the recorded
  refutation wrong; s5 fail breaks the optimizer evidence that
  motivates (H*); s6 fail refutes a constant, the sealed-LB
  bookkeeping, or the plateau arithmetic (incl. the n=24 no-slack
  claim); s7 fail refutes an anchor or a ladder value. Single
  governed run, no silent reruns.
design:
  stopping: fixed design, single governed run, seed 20261131, after
    the disclosed two-run pilot (seed 20261130); no further pilots
    or attempts under this ID
  runtime: ~6 min single-threaded (pilot run 2: 348 s)
controls: [independent-evaluator identity checks (s5), F0 vs
  U-coupled contrast on the same zero-claim (s3), the refutation
  gated with independently re-derived witnesses (s4), committed-value
  reproduction from results/GO14-convexity.json (s6), the n=24
  no-slack negative control (s6)]
amendments: []
hash: sha256:b73e6214110c01727c8f23fdcef01f0c463554d25e504944011204162ffa3f19
```

## Falsification

A pass nets the GO-14 transfer face at tex v0.5: the process limit
exists unconditionally, the lower transfer side is a theorem, the
κ-per-side lemma is refuted with witnesses on record, the remaining
transfer results stand openly conditional on (H*), and the diag
ladder is certified within class. OPEN and so marked: the (H*)
repair (an optimizer-regularity bound on I(E;T^{b2}) via Theorems
R+C — which would restore the unconditional label with the same
constants), the Δ=1,2 plateaus (model-conditional), per-cell
convexity, minimizer uniqueness, the U-coupled coordinate (now
GO-15), and the reset protocol.
