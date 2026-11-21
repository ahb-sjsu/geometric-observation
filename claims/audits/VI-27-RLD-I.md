# VI-27: R-IND-5 pass on RLD-I (2026-11-20)

**What was checked:**
- In `paper/tit-rate-leakage/tit-rate-leakage.tex`, the results behind the ledger row RLD-I:
  - Theorem 3 (`thm:op`, the operational region), with Lemma 1, Proposition 2 and
    Appendix A's Lemma A;
  - Theorem 5, which Theorem 7 uses;
  - Theorem 7 (`thm:tilted`);
  - Theorem 16(a), which defines μ_max and b;
  - Theorem 20 (`thm:turning`).
- Their numerical nets: `verify_tilted.py` and `verify_mm.py`, and
  `paper/tit-vector-described/verify_general.py` G3.

**Verifier:** a fresh-context general-purpose agent, told nothing about whether the results
are right and asked to find what is wrong. It worked from local files only, with no network,
browser or connector tools.

**The paper is under review**, so nothing in it was changed. The paper's items below are for
the owner's next revision. Only the ledger row was changed.

**Verdict:** the three theorems hold. No errors; 1 gap; 1 overclaim (in the ledger row, not the
paper); 4 exposition items. Theorem 7 has real numerical nets, Theorem 20's net is weak, and
Theorem 3 has none.

## Findings, and what was done with each

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | overclaim (ledger) | The row says "the optimal directions turn with the budget". Theorem 20 is narrower. It is about α = 0 and the eigenvector b(Δ) of the best one-dimensional description, on an interval where μ_max is simple. There b is constant on the whole interval iff b(Δ₀) is a common generalized eigenvector of the pencils (Σ_TQΣ_T, Σ_T) and (Σ_TJΣ_T, Σ_T); otherwise it is constant on no open subinterval. That description is leakage-optimal only where Theorem 16(b)'s certificate holds. The rate-optimal description (Proposition 19) and every frontier description in commuting geometry (Corollary 14) read fixed directions. | **Ledger row narrowed, 2026-11-20.** |
| 2 | gap | Theorem 3's achievability rests on the paper's paraphrase of Villard–Piantanida, Theorem 3 (Theorem `dmc` outline, Lemma A). The paraphrase covers: deterministic encoders; reproduction alphabet equal to the source alphabet; zero-probability letters; one code per tolerance; and the equivocation term −I(X;E\|V₀), not −I(V;E\|V₀). The last carries weight: with V in place of X, Lemma A's leakage bound would not follow. The verifier's recollection matches the paraphrase, but this could not be confirmed without the source. | **Source check done, 2026-11-20 (T-CUST-3). Gap closed.** Checked against arXiv:1105.1658 (v2, 2013), the preprint of the cited journal paper (IEEE Trans. IT 59(6), 2013). I read the arXiv text, not the journal's typeset pages. All five points match. (i) Encoders are deterministic: Definition 3 gives an encoding *function* f : Aⁿ → {1,…,2^{nR_A}}. (ii) The reproduction is a function Â : V × C → A, so the reproduction alphabet is the source alphabet. (iii) §II-A takes finite alphabets with an arbitrary joint pmf p(a,c,e) and states no full-support assumption, so zero-probability letters are allowed. (iv) Achievability (Definition 4) asks, "for any ε > 0", for one (n, R_A+ε)-code. (v) Theorem 3 (§III) bounds the equivocation by H(A\|VC) + I(A;C\|U) − I(A;E\|U), with U − V − A − (C,E). The last term is conditioned on the *source* A, not on V. With no decoder side information (C constant) and Eve's E the holder's S, this is H(X\|V) − I(X;S\|U), as the paper states. The verifier's suggested quotation, with equation numbers, remains a possible improvement for the next revision. |
| 3 | exposition | Proposition 2's proof, line 365: "So Σ_e0 ∈ P(D)" is false in the empty case (Σ_e0 = Σ_T). The case is vacuous, since its distortion is at least D_max > D, and the proof should say so. | For the owner's revision. |
| 4 | exposition | Theorem 20's statement, lines 1238–1251: "positive" is redundant by Theorem 16(a), and the "that is" restatement drops λ > 0 and ς ≥ 0. Both are automatic for b₀ = b(Δ₀), and one clause should say so. The forward direction does not need Kato. | For the owner's revision. |
| 5 | exposition (ledger) | The row says "is reverse water-filling on … tilted weight". It should say "is the fixed point of", as the abstract does: the tilt is evaluated at the solution, with no closed form for holder rank above 1 (lines 712–713). | **Ledger row corrected, 2026-11-20.** |
| 6 | exposition | The numerical-checks appendix, lines 2699–2702: its "Not formalized" list omits Theorem 3, Lemma 1 and Proposition 2, which have neither a formal nor a numerical check. It also lists Theorem 7 as not formalized, although `lean/ObservationTheory/TiltedWaterFilling.lean` and `TiltedExistence.lean` exist (`lean-tilted-complete-2026-10-07.txt` records a build with no `sorry`). The verifier did not check that the Lean statements match Theorem 7. | For the owner's revision. The Lean–statement correspondence is owed. |

## The verifier's coverage: checked and found correct

- **Lemma 1:** the divergence form; the infinite case; the Pythagorean split; the trace and mean
  terms; the Jensen direction with E C ⪯ Σ_e; the determinant identity and its Schur
  complement; equality in the Gaussian case.
- **Proposition 2:** both inclusions, including the singular Cov(N′) reduction, Cov(N′,U) = 0,
  Σ_e⁻¹ = Σ_e0⁻¹ + J, the LMMSE distortion bound, and the converse construction.
- **Theorem 3, converse:** the chain rule, finiteness, the Markov chain, and
  I(T;Ŷ,τ|S) = I(T;Ŷ|S,τ).
- **Theorem 3, closedness.**
- **Theorem 3, achievability, everything the paper adds around the citation:**
  - quantizing S;
  - the nested saturating quantizers (q_κ∘q_k = q_κ);
  - convergence of the surrogate distortion and channel;
  - martingale and bounded convergence;
  - the parameter order;
  - the diagonal argument;
  - in Lemma A: the rate, leakage additivity, the distortion bounds, and the threshold
    n ≥ n₀d_max/ε.
- **Theorem 5:**
  - fixed-gain concavity;
  - (a) existence, uniqueness, the active constraint, and Pareto points equal to weighted
    minima;
  - (b) the bijection, Woodbury and the LMI;
  - (c) dh, Slater, KKT and ϖ > 0.
- **Theorem 7:**
  - whitening, with ℓ = r − I(Ŷ;S);
  - the gradient and Slater;
  - KKT ⟺ X = Φ(Ã) in both directions;
  - ν > 0, uniqueness, and the tilt identity.
- **Theorem 16(a).**
- **Theorem 20:** the forward direction, the converse eigenvalue (λ−Δ)(1+ς), and the
  open/closed/connected argument.

**The verifier's own checks**, kept in this session's scratchpad (not in the repo):
- `chk7.py`: SLSQP over G on 6 instances and 5 values of α. At the optimum, tr(Q̃X)/D =
  1.000000, and the water-filling residual is ≤ 2.5e-8. Dropping the (1−α) factor leaves
  residuals of 5e-2 to 2e-1.
- `chk20.py`: a common eigenvector with ς = 4 holds a constant line over 8 budgets. A
  QΣb = λb case with JΣb not parallel to b turns.

## Harness assessment

- **Theorem 3, Lemma 1, Proposition 2: no net.** Every script parameterizes descriptions as
  Gaussian GT+N, which already assumes Proposition 2.
- **Theorem 7: real nets.**
  - `verify_tilted.py` W1 solves an independent CVXPY/Clarabel determinant program. Its
    tolerance is 2e-3 against a recorded 3.0e-5. Solver status is never checked, and
    failed solves are skipped.
  - W2 and W4 are real nets. W3a is real for α = 1. W3c is consistency only.
  - `verify_mm.py` M2 is an indirect net for sufficiency. M3 always passes.
- **Theorem 20: weak.** `verify_general.py` G3 would catch gross falsity. But the variants
  "requires ς = 0" and "requires only QΣb = λb" also pass it.
- **How a failure shows up:** the scripts exit 0 either way. A pass is the line "FAILS: 0".
  An exception exits nonzero without that line.

## Owed before `[proved]`

- New nets, as new files outside the paper directory: one for Theorem 3's ingredients
  (Lemma 1 and Proposition 2, against non-Gaussian descriptions), and a stronger one for
  Theorem 20 (a ς > 0 constancy case and a turning case).
- The Lean–statement correspondence for Theorem 7. (The Villard–Piantanida source check is
  done; see finding 2.)
- CI wiring that reads "FAILS: 0".
- The custody table.

**The owner sets RLD-I's class.**
