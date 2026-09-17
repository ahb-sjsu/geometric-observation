# Fresh-context referee pass, Appendix B (Gaussian operational theorem), 2026-09-16

Run at the owner's request after the 2026-09-09 pre-submission review named the
Gaussian operational proof as the decision-making item. The pass was a separate
agent with access to the manuscript source only (no README, no notes, no earlier
review, no author reasoning). Scope: Appendix B (`\label{app:gaussian}`, Theorem
`thm:gaussop`, lines 2689 to 2985 of `tit-cr-context.tex` at commit c58fa19) and
the results it invokes. Line numbers refer to that commit. Nothing in the
manuscript was changed by this pass.

## Verdict

Sound with repairable gaps. None of the gaps threatens the result; every one is
a one-to-three-sentence repair. The two most substantive are a missing
cross-reference (Lemma `lem:gauss`'s hypotheses) and an overclaimed citation
(Lemma `thm:pair` used for something it does not state).

## Findings

1. **Lines 2799 to 2808, restriction step.** The text says "For any admissible
   channel, Lemma gauss produces the jointly Gaussian channel with the same
   second moments and the same distortion." Lemma gauss (996 to 1025) requires
   Ŷ centered with finite second moments, Σ_N ≻ 0, and Cov(N′, S) = 0. None is
   verified or cross-referenced in the appendix. All are verified elsewhere
   (centering at 1209 to 1211; ν = 0 dispatched by Remark degenerate at 1222 to
   1226; Cov(N′, S) = 0 from the Markov chain at 1228 to 1233 and 2274 to 2282).
   Finite second moments follow from E(Y − Ŷ)² ≤ D and EY² = 1. Repair: one
   sentence pointing to those lines, noting that centering leaves both mutual
   informations and the Markov chain unchanged and lowers the distortion by
   (EŶ)², and that ν = 0 with c ≠ 0 gives an empty quadrant while ν = 0 with
   c = 0 is the zero reproduction.

2. **Lines 2696 to 2697 and 2730 to 2731.** The text says the pair T is "taken
   as the source letter, which Lemma thm:pair permits." Lemma thm:pair (883 to
   898) proves only that the conditional coordinate of the single-letter
   minimization is unchanged by restricting to T-channels; it says nothing about
   the rate coordinate I(X; Ŷ) and nothing about codes whose encoder observes
   the ambient Xⁿ. Since Definition def:problem (438 to 441) fixes the Gaussian
   source letter to be T, the theorem as stated is about T-codes and the proof
   matches it, so this is a wrong justification rather than a wrong claim. If
   the operational statement is meant to cover an encoder observing the ambient
   Xⁿ of Section sec:pair (836), two lines are needed and absent: the resampled
   T-channel Ŷ′ of the lemma also satisfies I(X; Ŷ′) = I(T; Ŷ′) = I(T; Ŷ) ≤
   I(X; Ŷ) with equal distortion, so the union over ambient channels equals the
   union over T-channels; and any Tⁿ-code is an Xⁿ-code. Repair: either drop
   the parenthetical and say the source letter is T by Definition def:problem,
   or add the two lines.

3. **Lines 2754 to 2761, converse single-letterization.** The text says every
   conditional differential entropy "differs from an unconditional one by a
   mutual information pinned between 0 and H(M)." For h(X_i | X^{i−1}, Ŷⁿ, Sⁿ)
   the reference quantity is h(X_i | S_i), a Gaussian conditional value, not an
   unconditional one; the sentence is loose, and the mixed discrete/continuous
   conditioning is asserted, not justified. The argument is correct as
   intended. Smallest repair: single-letterize with mutual information only,
   which needs no differential entropy: I(Xⁿ; Ŷⁿ) = Σ_i I(X_i; Ŷⁿ, X^{i−1}) ≥
   Σ_i I(X_i; Ŷ_i) by the chain rule and independence of X_i from X^{i−1};
   I(Xⁿ; Ŷⁿ | Sⁿ) = Σ_i [I(X_i; Ŷⁿ, X^{i−1}, Sⁿ) − I(X_i; S_i)] ≥
   Σ_i I(X_i; Ŷ_i | S_i) by the same, using I(X_i; X^{i−1}, Sⁿ) = I(X_i; S_i).
   All terms are finite because they are bounded by H(M).

4. **Line 2765** invokes Remark convgeneral (474 to 482), which asserts the
   general-alphabet convexity lemma "holds verbatim" without proof or citation
   for the conditional coordinate. Repair, one line: under Ŷ − X − S,
   I(X; Ŷ | S) = ∫ D(P_{X|S=s} ⊗ q ‖ P_{X|S=s} ⊗ (P_{X|S=s} q)) dP_S(s); both
   arguments of D are affine in q, so the integrand is convex in q by joint
   convexity of relative entropy, and so is the integral.

5. **Lines 2935 to 2937, Step B (iii).** The text attributes E[f(Ŷ_m, j) | X_m]
   → E[f(Ŷ, j) | X] to the martingale convergence theorem. That theorem gives
   only E[f(Ŷ, j) | X_m] → E[f(Ŷ, j) | X]; the other piece, E|f(Ŷ_m, j) −
   f(Ŷ, j)| → 0 by bounded convergence (Ŷ_m → Ŷ pointwise, f continuous and
   bounded), is elided, as is the L¹ convergence of the product with
   P(S_Δ = j | X_m). Repair: one triangle inequality.

6. **Lines 2857 and 2862, Step B.** The surrogate channel p_m(ŷ | x_m) and
   distortion d_m(x_m, ŷ) are conditional expectations given X_m = x_m and
   require P(X_m = x_m) > 0 for every cell of the alphabet. This holds because
   the Gaussian density is positive on every rectangle (Σ_T ≻ 0), but it is not
   said. Repair: say it, or define the source alphabet as the support of X_m.

7. **Line 2850.** "Ŷ_m → Ŷ in L²" needs EŶ² < ∞ (true, from the distortion
   constraint) and dominated convergence for the tail term E[Ŷ² 1{|Ŷ| > 2^m}].
   One clause.

8. **Lines 2741 to 2744, endpoints.** The remark sits outside the theorem
   statement. For D ≥ 1 the claimed equality also needs the trivial inclusion
   RW(D) ⊆ [0, ∞)², since R_n, L_n ≥ 0. For D = 0 the phrase "extended-real
   limit with both coordinates diverging" is informal; the precise statement is
   that both RW(0) and the union at D = 0 are empty as subsets of R² (any code
   has D_n > 0 with R_n ≥ ½ log(1/D_n), and the only channels at zero distortion
   have Ŷ = Y a.s. with infinite coordinates). Repair: one sentence each, or
   move into the theorem.

9. **Lines 2787 to 2789, closedness step.** "the θ_j eventually lie in the
   compact set at level D + δ for each δ > 0" and the exclusion of c = 0 both
   need D + δ < 1 (line 2782 uses 1 > D′). Say δ < 1 − D.

10. **Lines 2969 to 2975, Collect.** The diagonal argument requires codes at
    every sufficiently large blocklength for each ε_j, which Lemma construction
    supplies ("for all sufficiently large n", 677 to 678); the interleaving of
    blocklengths (use the ε_j-code for N_j ≤ n < N_{j+1}) is left to the
    reader, as it is in the discrete theorem (654 to 659). Acceptable, but one
    clause would close it.

11. **Line 2812.** "a channel with ν = 0 has both coordinates infinite, by the
    closedness step" is a circular-looking pointer; the fact comes from the
    formulas at 2778 to 2779 (and Remark degenerate), and the divergence of the
    conditional coordinate uses Λ ≻ 0, that is τ² > 0. Minor wording.

## The six items the 2026-09-09 review required

1. H(M | Sⁿ) ≤ H(M | S_Δⁿ): established, lines 2958 to 2967, direction correct
   and justified by σ(S_Δⁿ) ⊆ σ(Sⁿ).
2. Convergence of the coordinates: established in the one-sided form the
   argument needs (2814 to 2841; 2917 to 2947). The elision in finding 5 is the
   only gap.
3. Tail control: established, 2892 to 2915. The exact-transfer claim is correct
   (ŷ_i is X_mⁿ-measurable; by memorylessness E[(Y_i − ŷ_i)² | X_mⁿ] =
   d_m(X_{m,i}, ŷ_i) exactly). The limit is an L² statement, not weak
   convergence. Tails are absorbed in the L² convergence of Ŷ_m (finding 7).
4. Finite reproduction alphabet: established, 2848 to 2865.
5. Markov kernel preservation: established, 2866 to 2867 and 2887 to 2889. The
   chain holds under the surrogate law by construction; the operational
   quantities depend only on the (X_m, S_Δ) marginal, which is the true law, so
   the surrogate coupling never enters H(M | S_Δⁿ) or D_n. This is the
   structural point and it is handled correctly.
6. Lower semicontinuity and endpoints: the converse uses the explicit
   extended-real continuity of the Gaussian coordinates on a compact parameter
   set (2769 to 2797), which is correct; endpoints are the remark at 2741 to
   2744 (finding 8).

## Verified as correct

The converse chain (2752 to 2754) and the induced per-letter chains and mixture
channel (2761 to 2767); the closedness and right-continuity argument (2769 to
2797); Step A (2810 to 2841); every hypothesis of Lemma construction (673 to 685)
against the surrogate, and that its guarantee (2870 to 2878) matches the lemma's
constants with ε_n depending only on (ε, k, m); the limit order (2882 to 2887),
with no n-dependence hidden in any ε; all inequality directions in (iii) and in
eq. quant-fano2 (2945 to 2956), the 5ε count included; the weak-convergence
computation (2925 to 2938); and that the theorem statement matches what the
proof delivers for source letter T. No step uses uniqueness of the Gaussian
optimizer.

## Not checked

The two imported results (Pinsker Ch. 2 on mutual information as a supremum
over finite partitions; Posner 1975 on weak lower semicontinuity), used in their
standard forms at 2819 to 2827 and 2938 to 2941. The internal correctness of
Theorem main-region's achievability (615 to 659) beyond confirming that Lemma
construction states its output in the form the appendix invokes. The LaTeX was
not compiled by the pass.

## Applied, 2026-09-16 evening PDT

All eleven repairs were made in `tit-cr-context.tex` with the Edit tool, one
edit per finding, in the commit that adds this section. Finding 2 took the
second branch: the theorem now cites Definition def:problem for the source
letter, and the appendix preamble carries the two lines that extend the
statement to codes whose encoder observes the ambient source. Finding 3
replaced the differential-entropy sentence with the mutual-information chain.
Finding 8 states the endpoints as set equalities beside the theorem, not
inside it. The PDF rebuilt at 32 pages with no undefined references, and the
control-character and lost-backslash guards returned clean.
