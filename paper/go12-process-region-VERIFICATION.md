# GO-12 verification record

## Pass 1 — the opening control (Facts 1–2), pre-seal, 2026-08-04

Fresh-context R-IND-5 verifier, independent numerics from scratch.
**VERDICT: FAIL as drafted — one claim confirmed, one refuted and
corrected before seal.**

**Claim 1 (noncausal Δ-invariance): CONFIRMED** with mandatory
sharpenings, all folded into v0.2:

- The cross-covariance in the draft proof sketch had a transpose typo:
  Cov(Y, S^Δ) = ρ·C_V·P^{−Δ}, not ρ·C_V·P^{+Δ} (the latter is its
  transpose, Cov(S^Δ, Y)). Harmless to the conclusion (orthogonality +
  commutation give the same cancellation either way); fixed.
- Σ_{Y|S}-invariance alone is WEAKER than "any functional": the
  conditional-mean map A_Δ depends on Δ, so label-aligned functionals
  (e.g. E[Y_t S_t]) are not invariant. The airtight form is the
  **recoding identity** (Y, V, S^Δ) =d (Y, V, P^Δ S⁰) (all three
  cross-covariances verified block-by-block to exactly 0), which makes
  every σ(S)-measurable conditional functional invariant. Folded as
  the statement of Fact 1.
- The Toeplitz edge claim is exactly O(1/n) at fixed Δ (verifier:
  n·dev constant to 4+ digits across n = 64…512, doubling ratios
  2.000/2.000/2.000) but mildly super-linear in Δ over the probed
  range; wording weakened accordingly.
- Verifier numerics: circulant invariance ≤ 7.8e-16 at two parameter
  sets with Δ up to n/2; per-symbol conditional-RD invariant to
  2.2e-16.

**Claim 2 (slice access): REFUTED AS DRAFTED, corrected.** The draft
asserted the substitution ρ → ρ·a^Δ (τ² unchanged) for single-letter
(Y_t, V_t)-records. The verifier showed by exact direct minimization
(reproducing the static quadratic to 2e-16 as its own sanity) that this
substitution is the value of a DIFFERENT problem — records granted the
context-epoch latent V_{t±Δ} (equivalently any path encoder with a
single-symbol target, by pair sufficiency). For (Y_t, V_t)-records the
exact value is ρ unchanged, **s → s/a^{2Δ}** (derivation:
S = a^Δ·V_t + (W+U), W ⊥ (Y_t, V_t); MI-invariant rescaling lands in
the static normal form; AR(1) reversibility covers both slice
directions). The two differ systematically — L_B − L_A ≥ 0 at all 72
grid points, max 0.0529 bits, median 2.0e-3 — orders of magnitude above
the project's verification tolerances. Monotonicity in Δ and the
Δ→∞ limit ½log₂(1/D) hold for BOTH substitutions (P(1) < 0,
P(1/D) > 0 bracket the root; derivative signs analytic; factorization
at ρ_eff = 0 exact).

**Consequences.** The claim, prereg scoping, and harness s3 were rebuilt
to gate both pairings against their own direct programs plus the strict
encoder-access ordering; both pilots disclosed in GO-P-2026-065
(20260912 on the refuted draft, 20260914 as sealed). The corrected
dichotomy is *stronger* than the draft: access width matters at the
eraser (path vs slice) AND at the encoder (context epoch vs time-t).

## Governed run (065)

GO-P-2026-065, seed 20260915, ALL PASS 4/4 (artifact
`results/GO12-delta-invariance.json`, CI-enforced). Facts 1–2 citable
at `[predicted]`-grade.

## Pass 2 — Theorem 1 (conditional-variance reduction), pre-seal, 2026-08-05

Fresh-context R-IND-5 verifier, independent numerics. **VERDICT:
PASS** — all four parts confirmed: the reduction at machine precision
(16 combos, 2 instances × 8 access classes incl. asymmetric {−1,+3},
gapped {−5,+2,+7}, far slice; max residual 1.7e-13); the sufficiency
step proven channel-agnostic ((T,Ŷ) ⊥⊥ G | V̂ for every randomized
record, so the min transfers term-by-term); Kalman fixed-lag and
Wiener closed forms to 9e-16; the verifier DERIVED the exact
prefix–path gap C^{2Δ}(P_f − q_∞) — strict at every finite Δ, never
zero, geometrically below float resolution past
Δ ≈ log ε/log C². Five sharpenings folded into v0.4: (1) σ-algebra
scope corrected (observation subsets, or any G jointly Gaussian with V
and independent of the noises — G correlated with N_t breaks
sufficiency); (2) q_G < 1 with the continuous extension ½log₂(1/D) at
empty access; (3) active regime D ∈ (0,1) stated; (4) exact gap
formula + float-resolution flag; (5) a ∈ (0,1) load-bearing (at a=0
the classes coincide/degenerate). Provenance qualification on record:
record-class optimality is IMPORTED from the static theorem's converse
via the channel-agnostic reduction, not re-proved.

## Governed run (066)

GO-P-2026-066, seed 20260918, ALL PASS 4/4 (artifact
`results/GO12-prefix-family.json`, CI-enforced). Theorem 1 citable at
`[predicted]`-grade. Open: the process-rate causal object
(Conjecture 2′ v0.4), the spectral program (Conjecture 1, pending the
Gray-1973 and Pinsker library pulls).
