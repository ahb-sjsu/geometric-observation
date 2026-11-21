# VI-26: R-IND-5 passes on RLD-IV.3 (2026-11-20)

**What was checked.** In `paper/tit-unstable-ergodic/tit-unstable-ergodic.tex`:

- Theorem 13 (`thm:law`), Proposition 14 (`prop:ergodic`) and Corollary 15 (`cor:sampled`);
- every result those proofs use, with paper three (`paper/tit-beyond-stationary`) read at
  tag `tit-beyond-stationary-1.3`, the version the paper cites;
- the harness `verify_spectral_law.py`.

**The paper is a working draft, not submitted.**

**The three passes.** Each pass was run by a fresh-context general-purpose agent. None was told
whether the text was right; each was asked to find what is wrong. All three used local files
only, with no network, browser or connector tools.

- **Pass 1** reviewed the original text.
- **Pass 2** reviewed the first rewrite.
- **Pass 3** reviewed the second rewrite.

Verdicts:

| Pass | Errors | Gaps | Overclaims | Exposition | Harness |
|---|---|---|---|---|---|
| 1, original text | 0 | 2 | 2 | 4 | weak (no power) |
| 2, first rewrite | 0 | 3 | 2 | 5 | as described |
| 3, second rewrite | 0 | 1 | 1 | 7 | as described |

No pass found a false mathematical step.

## Pass 1 findings and their final disposition

| # | Severity | Finding | Final disposition |
|---|---|---|---|
| F1 | overclaim | The abstract, introduction and ledger row state the cyclostationary result without its hypotheses. | Applied. "Continuous correlation of finite range" was added to the abstract, the introduction and the ledger row. The introduction also says "a scalar source seen through a scalar gain in white noise" (pass 2). |
| F2 | gap | The achievability works at D'' < D but leaves three adaptations unstated: the cutoff below θ(D''); the zero-reproduced distortion counted in the budget; v_B ≤ (1+κ)b. | Applied, then rebuilt after pass 2. The final achievability argues from the explicit allocation min{λ, θ''}. It defines no V_μ and cites no optimality lemma. It chooses D'' by the continuity of r_μ and ℓ_μ, which the converse now proves (pass 3). The cutoff is ε₀ ∈ (0, θ''), with no atom at ε₀. The bins satisfy b < v_B ≤ (1+κ)b, and ℬ_κ is formed with budget D'' − D₀. In each bin the variance moves to the left end, then the ratios are averaged. Rate and leakage are each convex in x. The budget split is D_i = Qv_{i−1}x̄_i. |
| F3 | overclaim | The remark after Theorem 13 applies it beyond what is proved. | Applied. The remark now says: stationary sources need an essentially bounded density; the theorem holds for triangular arrays; for paper three's scalar sources, with a constant weight and a constant holder (gain and noise variance), it applies only once their eigenvalue limits are shown, which is not proved here. |
| F4 | gap | The rational counterexample's eigenvalue floor and its class are not stated. | Applied. Z now has unit variance, a continuous finite-range correlation, and a sampled spectral density of at least m_Z > 0. The text uses D < Qm_Z and "for even N" (pass 3). |
| F5 | exposition | A finite-n lemma is cited for the minimizer over μ. | Superseded. The final achievability needs no minimizer. |
| F6 | exposition | Corollary 15 at D ≥ D_max. | Applied. D > D_max gives r_N = 0 eventually. D = D_max is handled by monotonicity, θ(D′) ↑ θ* ≥ λ μ-a.e., and dominated convergence (passes 2 and 3). |
| F7 | exposition | σ_U² > 0; Proposition 14's PSD clause. | Applied. |
| F8 | exposition | Stale theorem numbers in the harness docstring. | Applied. |
| H | harness | `phase_independence` has no power: rational runs pass it too. | Applied. `strong_phase_independence` was added (amplitude 4, irrational), along with `strong_rational_control`, a power control that must stay phase-dependent. Their criteria were set after pass 1's exploratory run, as the docstring and the paper's appendix disclose. |

## Pass 2 findings on the first rewrite (all applied)

1. **Gap.** A finite-n lemma had been cited for a general μ. *Fix:* the achievability was
   rebuilt on the explicit allocation.
2. **Gap.** The D ≥ D_max case had been dropped. *Fix:* restored, with the zero code.
3. **Gap.** An atom of μ at 0 made the old V_μ infeasible. *Fix:* removed with V_μ.
4. **Overclaim.** The remark dropped "scalar". *Fix:* restored.
5. **Overclaim.** The introduction lacked the scalar-gain hypothesis. *Fix:* added.
6. **Exposition, items 6–10.**
   - Arguments and order of choices: rewritten.
   - Corollary 15 at D_max: argued.
   - The docstring, and the appendix with Table `tab:checks`: they now describe every check.

**Added on pass 2's suggestion:** `rational_example_exact`, the paper's own counterexample
(T_s = T_c/2, phases 0 and T_c/4). Its expected value is the paper's ½log₂(5/3), and its
eigenvalue floor is 0.15, derived from Z's sampled spectral density. It is not a blind
prediction: pass 1 had computed a similar configuration first. The docstring and the appendix
say so.

## Pass 3 findings on the second rewrite (all applied, 2026-11-20)

1. **Gap.** The continuity of r_μ and ℓ_μ in D was used but not shown. *Fix:* one sentence was
   added to the converse. θ(D) is continuous as an inverse, and the integrands are bounded and
   jointly continuous. Pass 3 had checked this argument.
2. **Exposition.** The budget split D_i, the white-source quadrant (paper three, Lemma 24 with
   S = vI), and upward closedness of the sum are now named. The undefined "δ = λ" is replaced
   by "x = 1".
3. **Exposition.** In the counterexample: unit variance, even N, and D < Qm_Z.
4. **Exposition.** Z's correlation length is fixed in samples, so its sampled correlation is
   (1, 0.6, 0.2) at every rate. The appendix and the docstring now say so.
5. **Harness.** The exact check now also asserts that the minimum eigenvalue is ≥ 0.15 (observed:
   0.257). Its limited power is stated: it tests the variances, the factor ½ and the floor,
   not Z.
6. **Overclaim.** The period-3 control is a power control, not a statement of Corollary 15. The
   table and the appendix now label it so and quote its actual criterion.
7. **Custody.** "Derived before any run" was not accurate. This is now disclosed.
8. **This record was stale.** Rewritten.
9. **Exposition.** "Constant holder (gain and noise variance)".

These last fixes are exposition, plus the continuity sentence that pass 3 checked. They were not
put through a fourth pass.

## Fresh run after the final changes (2026-11-20)

| Check | Result |
|---|---|
| phase_independence | spread 1.54e-4 → 7.29e-6 |
| moments | relative error to 2.4e-4 |
| strong_phase_independence | spread 2.63e-3 → 1.27e-4 |
| strong_rational_control | spread 1.85e-2 → 2.08e-2 |
| rational_example_exact | 0.36848279708311 and 0.36848279708310, against ½log₂(5/3) = 0.36848279708310 |

All checks pass. The paper compiles with no undefined references or citations.

## Source check (T-CUST-3), done 2026-11-20

Tan, Dabora and Poor, arXiv:2405.11405v2, read through its HTML full text.

**Their model:**
- a zero-mean Gaussian process;
- a correlation that is bounded, uniformly continuous in both arguments, periodic in t with
  period T_c, and zero for |λ| > λ_c;
- sampling at T_s = T_c/(p+ε) ≤ λ_c, with ε irrational.

**Their conjecture (Remark 1):** R_ε^{φ_s}(D) = R_ε^0(D).

**Comparison.** Their class satisfies Corollary 15's hypotheses: a continuous, periodic,
finite-range correlation is uniformly continuous, and Corollary 15 does not need T_s ≤ λ_c.
Corollary 15 proves phase-independence of the limit at every D. So "proving a published
conjecture" holds within their class.

**Not re-derived:** the identification of their Theorem 1 window program with r_N, which the
paper makes through paper three's Lemma 24. The ISIT pages were not read.

## The passes' coverage, checked and found correct

- **Theorem 13's converse.** The bound for any code; the singular reduction; Lemma 24's
  hypotheses as used; the uniform convergence and the limit θ_N → θ; the joint continuity of the
  integrands; the quadrant.
- **The final achievability (pass 3).**
  - The D ≥ D_max zero code under the paper's lim-sup definition.
  - The per-component costs and the convexity of the leakage,
    d²/dx² ln(a/x + J) = a(a + 2Jx)/(x²(a + Jx)²) > 0.
  - The choices θ'', ε₀ and D₀, valid with an atom at 0.
  - The bins and Lemma 12's hypotheses.
  - The move-to-left-end bound ∂ℓ/∂λ ∈ [−1/(2λ ln 2), 0], and the per-bin Jensen step. A numeric
    test over 200 random measures with atoms at 0 found no positive excess.
  - The total distortion D'' + ε_Q + 2η + o(1) < D.
- **Proposition 14.** The Schur bound; the index-shift identity; the uniform ergodic theorem;
  moments to weak convergence; the PSD clause.
- **Corollary 15.** The indexing; unique ergodicity of the rotation; the band m = ⌊λ_c/T_s⌋;
  the D > D_max and D = D_max steps.
- **The counterexample.** Its arithmetic and its hypotheses.

## Still owed before `[proved]`

- CI wiring of the harness.
- The custody table.

The row stays `[exploratory]` until then.
