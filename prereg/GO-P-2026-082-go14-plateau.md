# GO-P-2026-082 — the plateau: Collapse, periodization, shift-averaging, and a two-sided certificate for Ψ at Δ = 0, 1, 2

The campaign's standing goal, reached and honestly scoped. Two
provers and two adversarial verification passes on record
(paper/go14-causal-erasure-PROBE.md); tex v0.7 carries the material
with all twenty restatements in force.

**THE COLLAPSE IDENTITY.** 2ln2·n·L_a = Σ_t ln σ_t − lndet N, exact
for every record, schedule and n. It requires **Δ-lag-causal
U-coupling, NOT U-independence** (F0 is the special case; dense and
anticausal coupling fail by 0.2018 and 0.3329 bits) — and the
non-conflation rule stands: this does not extend moment-form
Theorem R.

**STEP (A), PERIODIZATION.** Tiling a window record along ℤ **with
independent noise copies** preserves distortion exactly, keeps
lndet N additive, and only decreases every σ_t — the conditioning
sets are genuine supersets. Hence the process value is at most φ_n
for every n, with no boundary charge, because the argument runs the
easy direction. **The independent-copies clause is a numbered
hypothesis, not a convenience**: correlating the copies breaks the
conclusion outright (0.7987/0.9218/1.3977 against φ₅ = 0.7757).

**STEP (B), SHIFT-AVERAGING.** For every period-n record there is a
**stationary record in the same cone, with identical per-symbol
distortion and no larger rate** — delivered explicitly, never
"attained"; lower semicontinuity is not used. Its only convexity
input is **(R1)**, stated as its own lemma (F_T convex on the linear
section; F_T/T → rate pointwise; pointwise limits of convex
functions are convex) on the **cyclostationary** class — not a
citation of Theorem C.

**THE CERTIFICATE**, stated via the **box-free per-frequency dual**:
for any μ ≥ 0 with β > 0 and any *admissible* frozen filters, weak
duality plus a per-frequency cell infimum bounds Ψ below. It needs
**no optimality of the fixed point, no convexity of the process
rate, and no differentiability**; the moment box is a corroboration
only. *Admissible* is a hypothesis with content — C monic causal in
S, B causal including lag 0 — and a non-monic C inverts the bound
(ŝ − s = −0.5447) so loudly that it returns values 2.3–3.5× the true
rate. Supporting lemmas: **Lemma S** (Collapse + Szegő, with its
non-degeneracy scope and the deep-notch evaluator caveat) and
**Lemma C-stat** (quadratic-over-linear composed with a concave M_Q,
then −ln(1−u); Q ⪰ 0 and R = P−Q ⪰ 0 both load-bearing; 074 an
antecedent only).

**THE BRACKETS** (outward-rounded, floating point, house
convention): Ψ(0) ∈ [0.5627264963, 0.5627264964]; Ψ(1) ∈
[0.5364013784, 0.5364013785]; Ψ(2) ∈ [0.5310500198, 0.5310500199].

**THE PLATEAU.** L^∞(Δ) ≥ Ψ(Δ) ≥ LB, **unconditional modulo (R1)
and the independent-copies hypothesis alone**, at margins over the
sealed causal-spectral reference construction of **+0.0147817164 /
+0.0040574952 / +0.0007968190** — retiring (H\*), (H\*\*), (H\*\*\*),
(D), (F) and the boundary charge from the plateau at three lags, two
of which the transfer route provably could not reach. **(R2) is
discharged.** The chain remains **one-directional**: it yields a
lower bound and nothing more.

Governs `experiments/go14_plateau.py` (numpy/scipy, CPU, single run;
sentinel `===GO14PL2-JSON===` with `===END===`; flag
`GO14PL2_supported`). Sealed bars read from
results/GO14-process-limit.json at run time and cross-checked
against pinned literals.

```yaml
id: GO-P-2026-082
date: 2026-08-07
retrospective: false
kind: theorem-verification (C3 net for the Collapse identity, periodization, shift-averaging, and the two-sided Psi certificate; two provers + two R-IND-5 passes with twenty restatements on record)
claim: "GO-14 v0.7: the Collapse identity holds under Delta-lag-causal
  U-coupling; periodization with independent noise copies gives the
  process value below every finite-window value with no boundary charge;
  shift-averaging delivers an explicit stationary record of no larger
  rate; and a box-free per-frequency weak-duality certificate brackets
  Psi two-sided at Delta = 0, 1, 2 without optimality, convexity of the
  process rate, or differentiability -- hence L^inf(Delta) >= Psi(Delta)
  at margins +0.0147817164 / +0.0040574952 / +0.0007968190 over the
  sealed causal-spectral bars, unconditional modulo (R1) and the
  independent-copies hypothesis."
harness: experiments/go14_plateau.py   # GOVERNED seed 20261151; pilot seed 20261150, disclosed below
power: |
  Deterministic gates; CI-ROBUST BY DESIGN -- no gate races an
  optimizer stopping point and NO GATE GATES A CERTIFICATE WIDTH
  (the 079 lesson, sharpened by the Delta=2 anchor agent's finding
  that LB endpoints are BLAS-sensitive at ~1e-7 through rn*R_box).
  s1/s2/s4/s5 contain no optimizer at all; s3 and s7 read cold-start
  endpoints only through analytic inequalities with 1.3e-3 margins
  and 1e-4 reproduction bands against an endpoint spread <= 4.4e-8;
  the tightest band anywhere is s7's 1e-8, which is 100x the
  quotable bracket width. Certified widths and
  endpoints-inside-bracket are RECORDED, never gated. Margins:
  s1 177x/578x/1493x/7.4x; s2 562x/352x and 0/1200 violations with
  the control at 2.9x; s3 140x/12.9x; s4 0/60000 violations with the
  psd control at 60x; s5 45x over 2880 pairs with the non-monic
  control at 5.4x; s6 3.6x/1.6x; s7 141x/22x/91x/2.0x; s8 39x/3.9x.
pilot: |
  TWO runs, seed 20261150, disclosed: iter 1 ALL PASS 30/30 (38.9 s)
  with every bar fixed IN ADVANCE from the committed prover and
  verifier artifacts; iter 2 ALL PASS 30/30 (44.8 s) after ONE BAR
  WAS TIGHTENED FOR ROBUSTNESS AGAINST NO FAILURE (s6's
  finite-bound count 20 -> 15, since 24 measured gave only 1.2x on a
  discrete BLAS-sensitive count). NO BAR WAS EVER LOOSENED AGAINST A
  MEASUREMENT. Payload bit-identical across re-runs; the governed
  run differs from pilot only in the seed stamp.
  THREE DISCLOSURES: (a) cold-start anchors differ from the
  committed phi values by <= 4.4e-8 and are re-valued through an
  independent time-domain evaluator (<= 2.2e-16); (b) the s3
  shift-averaged records reproduce the constructive upper bounds
  Psi(1) <= 0.5364993215 and Psi(2) <= 0.5311645087 to 10 digits but
  are REPORTED, not gated; (c) the Lemma C-stat control uses
  Q' = 1.3P (R negative definite) rather than the verifier's sampler,
  giving 60000/60000 rather than 12532/20000.
prediction:
  s1_collapse: exact at random F0 records, non-staircase schedules
    and edge Delta (< 1e-12); the Delta-lag-causal U-extension exact
    (< 1e-12) while dense and anticausal coupling FAIL (> 0.02)
  s2_periodization: distortion preserved and lndet N additive
    (< 1e-12 / 1e-11); zero sigma-violations over 1200 pairs; AND
    the correlated-copies control EXCEEDS phi_n (excess > 0.01)
  s3_shiftavg: the averaged pair is in the cone (> 1e-3); distortion
    preserved (< 1e-12); the constructed stationary record's rate is
    strictly below the cyclostationary rate (gap < -1e-4)
  s4_cstat: zero Jensen violations over 60000 chords at 1e-9 from
    the cone boundary; AND the Q > P control VIOLATES (> 1000)
  s5_minorant: shat >= s over 2880 pinned pairs (min > -1e-11);
    AND the NON-MONIC control INVERTS it (shat - s < -0.1)
  s6_no_optimality: the dual bound is valid at deliberately
    non-optimal anchors and mistuned mu (worst violation < 1e-9);
    the detector has power (< -1e-6); >= 15 of 25 random anchors
    give finite bounds
  s7_reproduction: the Psi brackets reproduce (< 1e-8); the margins
    against the SEALED bars reproduce +0.0147817164/+0.0040574952/
    +0.0007968190 (< 1e-9); block_inf reproduces 0.5299499808119
    (< 1e-9) with the committed s6_block_inf high by 3-6e-9; the
    O(1/n) constants are Delta-DEPENDENT (0.064506/0.070483/0.077503,
    min separation > 3e-3)
  s8_not_too_much: the block-program certificate does NOT exceed the
    known block_inf (LB - block_inf < 1e-9); the Delta-ladder
    approaches from above without crossing; Delta <= 6 fat margin
    > 1e-7 and the ladder strictly decreasing
falsification: s1 fail refutes the Collapse identity or its U-scope;
  s2 fail refutes periodization (and with it the whole bypass) or
  shows the independent-copies hypothesis unnecessary; s3 fail
  refutes shift-averaging; s4/s5 fail refute the certificate's two
  supporting lemmas -- and s5's control failing would mean the
  sign-slip failure mode is silent rather than loud; s6 fail refutes
  the no-optimality strengthening; s7 fail refutes the brackets, the
  corrected margins, or the erratum; s8 fail would mean the
  machinery proves too much and the whole certificate is suspect.
  Single governed run, no silent reruns.
design:
  stopping: fixed design, single governed run, seed 20261151, after
    the disclosed two-run pilot (seed 20261150); no further pilots
    or attempts under this ID
  runtime: ~40-75 s single-threaded (pilot runs: 38.9 s, 44.8 s)
controls: [the correlated-copies control breaking periodization
  (s2), the Q > P control breaking Lemma C-stat (s4), the non-monic
  filter inverting the minorant (s5), deliberately non-optimal
  anchors and mistuned mu (s6), and the block-program
  does-not-prove-too-much control against an independently known
  value (s8)]
amendments: []
hash: sha256:e07830121bbee5c3a5edc84b150586475490adbd2db11b08a9b161b2bc424545
```

## Falsification

A pass nets the plateau at tex v0.7: the Collapse identity with its
true U-scope, periodization and shift-averaging as theorems with
their hypotheses stated, the two supporting lemmas, and the
box-free certificate bracketing Ψ two-sided at three lags. What this
registration does NOT claim, and what a seal printing otherwise must
FAIL: that L^∞ equals Ψ (the chain is one-directional), that the
limit is thereby determined, or that the plateau is free of
hypotheses. **(R1) — convexity of the process rate on the
cyclostationary class — and the independent-copies hypothesis remain
load-bearing, and (R1) is now the campaign's single highest-leverage
open target.** Also open: the achievability/truncation lemma that
would supply the converse direction; the U-coupled coordinate
(GO-15); the reset protocol.
