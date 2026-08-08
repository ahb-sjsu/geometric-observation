# GO-P-2026-085 — Theorem D, Lemma A′, Lemma M restated, and the scoped equality L^∞ = Ψ at Δ = 0, 1, 2

The terminal result for this face of GO-14. Prover + R-IND-5 pass on
record (paper/go14-causal-erasure-PROBE.md); tex v1.0 carries the
material with **F1–F14 folded, F5–F8 not optional**.

**THE SCOPED EQUALITY.** For Δ = 0, 1, 2, **L^∞(Δ) = Ψ(D;Δ)** — the
lower inequality by Corollary `cor:onedir` with its scope items, the
upper by Corollary `cor:lower` together with Lemma W (steps (1)–(4)),
Lemma M and Theorem D. Beyond `cor:onedir`'s scope the equality
carries five named inputs: (i) Lemma W step (3)'s classical
rational-spectral-factorization/Riccati citation, cited **with** its
hypotheses, verified to hold on the depth-L FIR record (spectrum
rational by construction; joint (S,R) density ⪰ 0.2394·I uniformly
in ω); (ii) Fejér–Riesz and L¹/L² convergence of Fejér means;
(iii) the model hypothesis f_V ∈ [0.1111, 9.0000]; (iv) continuity
of D ↦ Ψ(D) at D = 0.3 from convexity; (v) a window-length threshold
n ≥ n₀(L). **"Unconditional" does NOT attach to this equality** — it
attaches only to `cor:onedir`. **Ψ remains a two-sided certified
bracket** (Remark `fpcert`): the equality **identifies two objects**
and is **not a licence to quote a value as exact**; `cor:brackets`
continues to govern the quotable numeric statement.

**THEOREM D (FIR density) — the residual, closed.** Ψ(D;Δ) =
inf_L U_tr(L). The proof approximates an **arbitrary near-optimal
feasible record**, never the fixed point, so the circularity that
blocked the Wiener-algebra route is gone: Fejér means keep the
truncated noise non-negative, and Fejér–Riesz returns a genuine
finite MA. Hypotheses printed (F4): f_V bounded above and below
(what turns feasibility into L² kernel bounds), continuity of
D ↦ Ψ(D), Lemma C′ load-bearing — and **Lemma B′ (the cap) DELETED
from the proof as dispensable**, feasibility alone giving
‖g‖₂ ≤ 2.343168 and ‖a_y‖₂ ≤ 1.766965.

**LEMMA A′.** σ = dist²(R_u, **closed** span); finite combinations
are dense *by definition* and the norm is continuous, so the infima
agree exactly. Hypotheses: Φ_R, f_S ∈ L¹ **and nothing else** — no
floor, no H² ball, no Wiener algebra. The infimum is **not attained**
by any finite filter; only ε-optimality is used (F1). Its
admissibility is the **mirror** of Definition `adm`'s and attaches
to a **different pivot** — the two are defined side by side and
never conflated (F2).

**LEMMA M, RESTATED (F5–F8, mandatory).** **WITHDRAWN**: that its
constant is independent of n (measured 72.444 / 20.434 / 15.194 /
13.426 / 12.676 over n = 64…1024 — the same factor-5.7 decrease W1
refuted, in the very build written to fix it); that ~18.7 bounds it
at L = 6 (exceeded at n = 64 and 128; asymptote ≈ 12.0); and that
there is no feasibility threshold (at L = 10, n = 64 the shifted
target is −0.01864 < 0, the same threshold W2 recorded). **CAUSE
PRINTED**: D ↦ U(L;D) is **convex**, so the linear estimate is a
**lower** bound on the repair cost; the correct estimate takes the
multiplier at the shifted point. **Lemma M does NOT discharge W1 or
W4; W1 and W2 STAND.** What it does deliver is an exact three-leg
decomposition with η_n = 2L(1+ε−D)/(n−2L) **exactly**, each leg
bounded, giving sup C(L,n) < ∞ — and **only C(L,n) = o(n) is used
downstream, so the conclusion is untouched** (F9).

Governs `experiments/go14_density.py` (numpy/scipy, CPU, single run;
sentinel `===GO14FD-JSON===` with `===END===`; flag
`GO14FD_supported`). Grid-free evaluator built from the model
primitives.

```yaml
id: GO-P-2026-085
date: 2026-08-08
retrospective: false
kind: theorem-verification (C3 net for Theorem D, Lemma A', the restated Lemma M, and the scoped equality; prover + R-IND-5 pass with F1-F14 on record)
claim: "Theorem D: FIR-kernel stationary records are dense in value, proved
  by approximating an arbitrary near-optimal FEASIBLE record (never the
  fixed point) via Fejer means and Fejer-Riesz, so no appeal to the
  optimum's regularity is made anywhere. Lemma A' is the Hilbert-space
  projection fact with L1 hypotheses only. Lemma M is restated: its
  n-independence and no-threshold claims are WITHDRAWN and W1/W2 stand;
  only C(L,n) = o(n) is used. Consequently L^inf(Delta) = Psi(D;Delta)
  at Delta = 0,1,2 as a SCOPED theorem with five named inputs -- an
  identification of two objects, NOT a licence to quote a value as
  exact."
harness: experiments/go14_density.py   # GOVERNED seed 20261181; pilot seed 20261180, disclosed below
power: |
  Deterministic gates. The ONLY search is s7's Nelder-Mead (pinned
  starts and budget), and BOTH its gates read the minimum over EVERY
  feasible record the search evaluated -- not the stopping point --
  so both are monotone-improving in effort: a longer search can only
  make them easier. No fixed point or root find anywhere else; no
  bracket, width or certificate endpoint is gated (the 082 lower
  endpoints enter only as fixed comparison literals, on the safe
  side); NO GATE READS OR ASSERTS THE EQUALITY. Margins: s1 6.0x
  with six must-fail controls at 2.13x; s2 18.3x over 22 adversarial
  pairs; s3 1.33x/24x/20.6x with the root-finding control failing at
  188x; s4 3.71x on the load-bearing floor; s5 4.5x/36x with four
  must-fails at 1.43x-18.6x; s6 54x/36x; s7 4.0x/2.82x/11.2x/9.2x;
  s8 19x over 28 rungs.
pilot: |
  TWO runs, seed 20261180: iter 1 = 22/23; iter 2 = ALL PASS 23/23,
  31.7 s; the governed payload is bit-identical apart from the seed
  stamp and pilot flag. **THE SINGLE ITER-1 FAILURE WAS A
  MIS-SPECIFIED BAR, NOT A MOVED MEASUREMENT**: s4 compared the
  feasibility constants to six-decimal literals at 1e-9 -- four
  orders below those literals' own precision, unmeetable by any
  correct computation. It was replaced by two correctly-specified
  bars (closed forms at 1e-12; printed literals at 5e-7). The
  measurement did not move and no other bar was touched in either
  direction. FOUR DISCLOSURES: (a) s3's root-finding control needs a
  numerically-exact tail, so the pinned noise is carried through a
  symbol round trip FOR THAT CONTROL ONLY; (b) the harness's direct
  search is deliberately smaller than the R-IND-5 addendum's
  full-strength run (900x2 vs 8000x4) and lands ~1e-6 higher -- the
  gate is against Psi^LB, never against the addendum's literals, and
  both are printed; (c) s3 runs 42 rungs where the verifier ran 33;
  (d) five new bibliography entries carry page-verification-owed
  flags.
prediction:
  s1_Aprime1: the K-lag admissible ladder decreases to sigma from
    above and hits it (|excess| < 1e-15 by K=60); AND all SIX
    must-fail controls BREAK (worst < -5e-3)
  s2_Aprime2: zero violations of both A'(2) inequalities over >= 20
    adversarial pairs incl. records far from the optimum
  s3_fejer: positivity at every rung to L=200 (min n^(L) > 0.10);
    ROOT-FREE realisability (< 1e-14, MA tail < 1e-15); Theta(L^-2)
    (slope in [-2.2,-1.8]); AND the ROOT-FINDING control DEGRADES at
    L=128 (> 1e-3) -- F12's warning
  s4_cap_dispensable: feasibility alone gives the L2 bounds; AND the
    FLOOR is load-bearing (at nu ~ 3e-6 the <ln n> error does NOT
    vanish, > 0.10)
  s5_lemmaM: the distortion identity EXACT (< 1e-15, edge cell
    exactly 1+eps) and D-feasible with no rescale (< 1e-14); AND the
    F5-F8 must-fails -- C(6,n) DECREASES by a factor > 4 (i.e.
    n-independence is FALSE), 18.7 is EXCEEDED at n=64, the shifted
    target at L=10,n=64 is NEGATIVE, and the secant exceeds the
    tangent (convexity)
  s6_decomposition: the three-leg residual < 1e-11 at every row;
    eta_n exact
  s7_not_too_much: every U_tr rung above the 082 certified LB
    endpoints; the Delta-ladder above block_inf; AND the DIRECT
    optima also above Psi^LB (9/9) while below U_tr
  s8_modulus: valid at every one of 28 rungs, zero violations
falsification: s1/s2 fail refute Lemma A' -- and their controls
  failing would mean admissibility is not load-bearing; s3 fail
  refutes the Fejer construction Theorem D actually uses; s4 fail
  refutes the hypothesis accounting; s5 fail refutes the exact
  identity -- while its must-fails failing would mean Lemma M's
  withdrawn claims were true after all and F5-F8 were wrong;
  s6 fail refutes the decomposition that saves the conclusion;
  s7 fail would mean the machinery proves too much; s8 fail refutes
  the modulus. Single governed run, no silent reruns.
design:
  stopping: fixed design, single governed run, seed 20261181, after
    the disclosed two-run pilot (seed 20261180); no further pilots
    or attempts under this ID
  runtime: ~32 s single-threaded (pilot 31.7 s, governed 30.6 s)
controls: [the six admissibility must-fails of s1 (S-peek, R-peek,
  their two-step variants, non-monic, fully-reoptimised non-monic),
  the root-finding degradation control of s3, the floor control of
  s4, the four F5-F8 must-fails of s5 -- which GATE THAT LEMMA M's
  WITHDRAWN CLAIMS ARE FALSE -- and s7's does-not-prove-too-much
  triple]
amendments: []
hash: sha256:6135c49552ea70a4f7fd8eed41f747a1de5d0dcd4b275279577e4b94e8eb9eea
```

## Falsification

A pass nets Theorem D, Lemma A′, the restated Lemma M, and with them
the scoped equality at three lags. What this registration does NOT
claim, and what a seal printing otherwise must FAIL: that anything
here is hypothesis-free; that "unconditional" attaches to the
equality or to the Ψ value; any free-standing reverse inequality
outside the scoped theorem; or any novelty for Lemma A′'s packaging,
Lemma W's combination, or Theorem D — **all three sweeps are OWED**.
Also owed: the window-side `la_cmi` cross-check. The equality
identifies two objects; the quotable numeric statement remains
`cor:brackets`.
