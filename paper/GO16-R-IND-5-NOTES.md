# GO-16 v0.2 — R-IND-5 fresh-context verification record (2026-08-21)

Independent adversarial pass over `paper/go16-adversarial-observer.tex`
(v0.2) + harness + results + Lean file, by a fresh-context verifier
with no shared derivation state; instructed to refute. The verifier
re-derived all twelve components with its own solvers (Monte-Carlo
read search, rectangular m>n instances, pseudoinverse checks,
coordinate descent and grid solvers — no shared code).

**VERDICT: 2 errors, 3 gaps, 2 overclaims out of 12 checks —
mathematical core intact.** Every theorem confirmed under independent
re-derivation; both hand instances reproduced exactly (t\*=1.0,
J\*=4.052777…, θ=(0.125, 1, 0.2̄2, 0.652777…, 0, 0), λ₂=λ₃ tie; m=2
J\*=7/4 at θ=(1/4, 3/4)); the hardest-flagged SVD step verified fully
and found to hold beyond its stated scope (exact attainment for
singular and projection K, m>n).

## Findings and v0.3 dispositions

1. Leakage/Ky Fan reduction — CONFIRMED.
2. Thm 1(i) spectrum sufficiency of K — CONFIRMED (incl. zero-padding
   edge cases to 7e-15).
3. Thm 1(ii) lower bound — CONFIRMED (every step; P⪰0 not needed,
   as claimed; 0 violations on 500 rectangular policies).
4. Thm 1(ii) achievability — CONFIRMED; **ERROR (exposition)**: the
   v0.2 K-verification display was garbled. → v0.3: display
   rewritten with the correct Moore–Penrose chain; ε-limit prose
   marked asserted-standard.
5. Thm 1(iii) SDP/saddle — CONFIRMED (extreme points of W_k are
   rank-k projections; verified two ways).
6. Thm 2 partition/attention/tie — CONFIRMED (all three parts
   re-derived, multiplicity counting checked).
7. Thm 3 — CONFIRMED in substance; **GAP**: (G3) as stated forced
   contested ≠ ∅, making the "iff empty branch" vacuous under the
   theorem's own hypotheses (verifier exhibited a real
   contested-empty instance outside G3: μ=(4,2.5,1.8), s²=(5,5,5),
   λ=1, k=2). → v0.3: re-scoped as the exhaustive
   fractional/integral two-regime alternative under G1–G2; the
   verifier's witness is quoted in the theorem.
8. Dither-necessity corollary — idempotency CONFIRMED; **GAP**: the
   v0.2 ε-jitter diagnosis of probe C4 is quantitatively untenable
   (jitter books blackout-level cost at mid-range revelation; cannot
   explain 0.19-magnitude missing dither). → v0.3: diagnosis
   withdrawn; V10 measurement added — the v0.1 instances' optima are
   near-projections (fractional mass ≤1e-13 at 3/4 cells, required
   dither ≤2e-12; 0.11/0.027 at the fourth): unrepresentative, not
   mismeasured. Three-step correction ledger kept at equal
   prominence. New observation folded into Conjecture 1: the
   contested phase concentrates on commuting-aligned (Σ_S, M) pairs.
9. No-commitment-gap corollary — **OVERCLAIM**: proved for the
   reduced attention-operator game; the concrete Θ-mixture reader
   cannot enforce a fixed W\* across encoder policies (P_U depends on
   N). → v0.3: restated for the whitened-attention (N-conditioned /
   population-HUD) game; fixed-instrument game explicitly OPEN.
10. Harness — CONFIRMED (byte-identical rerun; independent
    recompute of both instances exact); flags: V6 circular (V5/V7
    are the non-circular support — noted in-code), **V9 tie gate
    vacuous** (fractional_K=False this run), V4 does not net the C4
    diagnosis. → v0.3: V9 de-vacuated (rotated known-fractional
    instance; spectrum err 6.6e-3, tie gap 7e-4 — passing
    non-vacuously), V10 added, JIT comment added.
11. Lean — statements match; **ERROR (mis-attribution)**: the
    N\* = SKS′ step was cited to `shrink_dither_key` (the telescope),
    and was in fact machine-checked nowhere; remainder list
    incomplete; "only inequality" wording loose. → v0.3:
    `revelation_key` + `revelation_variance` added (N\* now
    machine-checked; rebuilt clean on Atlas, 8663 jobs, zero sorry);
    remainder list extended (Gaussian conditioning, AB/BA
    coincidence, symmetrization, ε-limits); "two inequalities"
    wording fixed and `trace_mul_transpose_self_nonneg` credited.
12. Scoping honesty — mostly good; residue = findings 7–9. → v0.3:
    abstract aligned with corrected scopes.

## Standing notes

- The ε-limit "changes no infimum" assertion remains asserted-standard
  prose (numerically supported, unproved) — carried as such.
- Thm 1(iii) inherits Thm 1(ii)'s m ≥ n / full-column-rank scope
  without restating it (minor, noted here).
