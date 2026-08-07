# GO-P-2026-081 — Theorem K, the H-repair lemma chain, split-causality, and (H***)

The conditionality of GO-14's transfer face, reduced and re-based.
Two provers plus a build cross-check on record
(paper/go14-causal-erasure-PROBE.md); tex v0.6 carries the material.

**THEOREM K (unconditional, new).** Because E[S|W] = V with V a
coordinate block of W, every Q-factor term lives on the V-columns;
because Y is a coordinate block of W, the distortion gradient lives
on the Y-columns. **The supports are DISJOINT**, so stationarity
splits by column block: (K1) A_y = θN; (K2) N⁻¹ = θI + VΣ_σ⁻¹V′;
(K3) A_v = −NVΣ_σ⁻¹V_S′. Corollaries: A_y = θN is symmetric
positive definite — which **upgrades the 078-era empirical mechanism
finding to a theorem** (transpose-symmetric A_y and noise kernel;
all causal structure confined to A_v, entering through a matrix
whose column support ends exactly at t+Δ); 0 ≺ N ⪯ I/θ and
0 ≺ A_y ⪯ I **uniformly in m** — the program's first m-uniform
optimizer regularity; θ ≥ 2ln2·φ_n(D)/(1−D) ≥ 1.119, hence
N ⪯ 0.894 I. CAUTION netted: (K2)/(K3) hold with the **record-pivot**
Gram; with the reference-pivot Gram they fail at 47% and 120%.

**THE H-REPAIR CHAIN (unconditional, F0-wide, optimizer-free).**
With X := I(Ŷ^{b1}; W^{b2} | W^{b1}) the cross-block read:
L1 κ is an *identity*, not a bound (I(T^{b1};T^{b2}) = κ exactly,
every m,n); L2 I(E;T^{b2}) ≤ κ + X and I(E′;E) ≤ κ + X, **tight at
the two-V-copy witness to 5.67e-7** — sharp exactly where the
universal claim dies; L3 D2 ≤ I(E;T^{b2}) − I_m; L4 D1 ≤ I(E′;E),
= 0 at Δ=0. Hence **D1 + D2 ≤ c(Δ;m) + (2−1{Δ=0})X**.

**SPLIT-CAUSALITY.** On F0^sc(m) (records whose block-1 cells read
no block-2 source — a *linear* moment condition, hence a convex
section) X = 0, so **(H\*) is a THEOREM there with the tex's own
constants**; the certified split-causality price is flat in n at
≈0.0041 bits. The Π-retraction preserves distortion and the entire
block-1 joint law exactly, kills X, and improves generic records.
**φ^sc_{2m} ≤ φ_m unconditionally** (concatenation is split-causal),
which re-bases the hypothesis: **(H\*\*\*)** constrains
p_m := m(φ^sc_m − φ_m), a gap between **two convex programs** —
two-sided certifiable by Theorem C, unlike the previously used
scalar which is only measurable at a computed optimizer. Certified
flat at 27× headroom (vs 18× for (H\*\*), 5.5× for (H\*)).

**HYGIENE REPAIR (independent).** Theorem T\*(ii)'s restriction step
assumed each block distortion ≤ D, but the 2m-optimizer's blocks
**straddle** D (0.299486/0.300514 at n=16, mean exactly D). Repaired
by convexity of D ↦ φ_m(D); the omission would have cost ~9.13e-3
bits — larger than the whole repair term.

Governs `experiments/go14_hrepair.py` (numpy/scipy, CPU, single run;
sentinel `===GO14HR-JSON===` with `===END===`; flag
`GO14HR_supported`). Model as netted; κ = 0.736966.

```yaml
id: GO-P-2026-081
date: 2026-08-07
retrospective: false
kind: theorem-verification (C3 net for Theorem K + the H-repair chain + split-causality + (H***) + the T* hygiene repair; two provers and a build cross-check on record)
claim: "GO-14 v0.6: the KKT system splits by column block (Theorem K,
  unconditional), making the 078 mechanism finding a corollary and giving
  the first m-uniform optimizer regularity; the boundary charge obeys
  D1+D2 <= c(Delta;m) + (2-1{Delta=0})X unconditionally, so 'kappa per
  side' IS a theorem on the split-causal section; phi^sc_2m <= phi_m
  unconditionally, re-basing the transfer hypothesis onto a gap between
  two convex programs (H***), certified flat at 27x headroom; and
  Theorem T*(ii)'s per-block feasibility gap is repaired by
  value-function convexity."
harness: experiments/go14_hrepair.py   # GOVERNED seed 20261141; pilot seed 20261140, disclosed below
power: |
  Deterministic gates; CI-ROBUST BY DESIGN -- no gate races an
  optimizer stopping point (s1-s5, s7 and the s9 reproduction are
  optimizer-free or compare certified brackets; the four sections
  reading optimizer endpoints gate structural facts at 2.6x-47x; no
  certificate width or bracket is gated anywhere -- the 079 lesson,
  as in 080). Margins: s1 26x/24x; s2 tightness 17.6x; s3 10.7x and
  min slack 0.7682 vs 0.1 (7.7x); s4 97x/1.54x/9000x; s5
  90x/15x/49x/6.2x; sK 12x/47x/2.75x; s6 2.6x/2.9x; s7 58x/1.38x/
  3.1x; s8 5.0x and exact reproduction; s9 3.8x and exact.
pilot: |
  THREE runs, seed 20261140, all disclosed: iter 1 ALL PASS 24/24
  (162 s); iter 2 ALL PASS 29/29 (223 s) after the coordinator added
  Theorem K and the (H***) material to scope; final shipped-file run
  ALL PASS 29/29 (110 s) with the JSON payload BIT-IDENTICAL to iter
  2. NO BAR WAS EVER LOOSENED: every bar was fixed from the provers'
  committed artifacts BEFORE running, and every optimizer endpoint
  reproduced their committed values bitwise (0.0e0).
  SIX DISCLOSURES, all folded into the tex and the campaign record:
  (a) L2's tightness is at the TWO-V-COPY witness, not the
  three-Y-copy one the prover reported (value right, attribution
  wrong); (b) the refuting records measure L_a = 4.2187/4.7397 --
  the reported 1.73/2.25 are NOT reproducible from any artifact;
  (c) the m=16 charge is 0.07691493, not 0.0769152 (3e-7);
  (d) (K2)/(K3) require the RECORD-pivot Gram (47%/120% off with the
  reference-pivot one) -- a caution neither prover stated;
  (e) Pi-gains measured [-2.74,-0.31] vs the prover's [-3.11,-0.37]
  (draw order); both printed; (f) the Delta=1,2 rows of the m-table
  are the prover's and were NOT re-netted, and sK covers six of the
  seven certified optimizers ((24,1) omitted).
prediction:
  s1_L1: I(T^b1;T^b2) = kappa to < 1e-12 at m in {3,4,6,8,12,16},
    and m-INDEPENDENT to < 1e-12
  s2_L2: zero violations of I(E;T^b2) <= kappa + X on the pinned
    battery; tightness at the two-V-copy witness (slack < 1e-5)
  s3_L3_L4_Hrep: identity residuals < 1e-9; D1+D2 <= c + (2-1{0})X
    with min slack > 0.1 over the battery INCLUDING both refuting
    counterexamples
  s4_splitcausal: X < 1e-12 on projected records; (H*) holds there
    with min slack > 0.5; the section is LINEAR (midpoints stay in
    section to < 1e-12)
  s5_pi: distortion and block-1 law preserved < 1e-14; X killed
    < 1e-12; Pi strictly improves generic records (delta < -0.05)
  sK_theoremK: K1/K2/K3 residuals < 1e-6 at the certified
    optimizers; A_y transpose-symmetry < 1e-6; 0 < N <= I/theta with
    theta >= 1.119
  s6_hygiene: the 2m-optimizer's block distortions STRADDLE D
    (d1 < D < d2, reproducing recorded values within 1e-4) AND
    value-function convexity slack > 5e-4 on the pinned grid
  s7_constants: c(0)+X = 0.4266326 to 1e-6; the plateau 0.5514005 >
    0.5479448 with ratio in [200,210]; the base-24 control FAILS by
    > 1e-4; the sealed LB(32,0) matches results/GO14-convexity.json
  s8_monotone: D1+D2, I(E;T^b2) and X monotone DECREASING in m at
    Delta=0 over m in {8,12,16,24}, reproducing recorded values
  s9_scstep: UB(phi^sc_2m) < LB(phi_m) with slack > 5e-4; the
    certified p-values reproduce within 1e-5
falsification: s1/s2/s3 fail refutes the H-repair chain (the whole
  reduction dies and (H*) stands unreduced); s4 fail refutes the
  split-causal theorem or the section's convexity; s5 fail refutes
  the retraction; sK fail refutes Theorem K -- and with it the
  upgrade of the 078 mechanism from measurement to corollary;
  s6 fail refutes either the straddle (so T*(ii) needed no repair)
  or the convexity that repairs it; s7 fail refutes a constant or
  the corollary arithmetic; s8 fail refutes the monotonicity that
  retires the m in {8,16} caveat; s9 fail refutes phi^sc_2m <= phi_m
  and with it (H***). Single governed run, no silent reruns.
design:
  stopping: fixed design, single governed run, seed 20261141, after
    the disclosed three-run pilot (seed 20261140); no further pilots
    or attempts under this ID
  runtime: ~2-4 min single-threaded (pilot runs: 110-223 s)
controls: [the two refuting counterexamples carried through the
  H-repair inequality (s3), the split-causal section as the
  positive control against the F0-wide failure (s4), the
  reference-pivot Gram as the netted negative control for K2/K3
  (sK caution), the base-24 no-slack negative control (s7), and
  committed-value reproduction throughout (s8, s9)]
amendments: []
hash: sha256:a823acee3eb416c26b1b1da9853ccfe28224309932fd175de120a4cd9cfd4128
```

## Falsification

A pass nets GO-14 v0.6: the KKT structure theorem and its
corollaries, the unconditional boundary-charge chain, the
split-causal theorem and retraction, the unconditional
φ^sc_{2m} ≤ φ_m step with its (H\*\*\*) re-basing, and the T\*
hygiene repair. NOTHING here contradicts an 080 gate, and nothing
here makes the plateau corollary unconditional — it remains
conditional, on a hypothesis that is now certifiable rather than
merely observed. OPEN and so marked: the decay bound itself
(obstructed by circularity of the operator — the missing step is a
fixed-point argument in a weighted Banach algebra, plus an
independent uniform lower bound on λmin(N)); the stationary/spectral
route and the n-uniform dual certificate; the Δ=1,2 plateaus; the
U-coupled coordinate (GO-15); the reset protocol.
