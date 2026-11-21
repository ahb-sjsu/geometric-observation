# VI-32: custody pass on the COST-face theorems B1–B7 (2026-11-20)

**Target.**
- The theorems the book calls B1–B7 (`chapters/appendix_b_cost_ledger.md`), as they stand in
  `paper/observation-theory.tex` (Paper III) and `paper/two-observer-theorem.tex`.
- The corrections recorded in VI-3 through VI-7.
- Their C3 harnesses (preregs 022–028).

**Verifier.** A fresh-context general-purpose agent, working from local files only. It was
told what today's other passes had found and asked to look for the same pattern: fixes that
were themselves wrong, and regimes that no gate samples.

**Verdict.** 4 errors, 4 gaps, 5 overclaims, 6 exposition items. The worst repeats the pattern
it was asked to look for.

## The worst error, independently confirmed: the parallel dispersion constant (NEG-18)

**What the record says.** `cor:dispersion` (Paper III), prereg 025 (its [C7] line) and the
book's B7 give the dispersion of the parallel Gaussian under total squared error as
V = (r_D/2) log² e, with r_D the number of active water-filling modes. VI-7 introduced this as
a "sharpening".

**What is true.** The d-tilted information, in nats with λ* = 1/(2θ), is

j = Σ_active [½ log(γ_k/θ) + ½(y_k²/γ_k − 1)] + Σ_inactive (y_k² − γ_k)/(2θ).

So **V = ½[r_D + Σ_{inactive, γ_k > 0} (γ_k/θ)²]**. Modes below the water level still
contribute: fluctuations in their energy must be absorbed by the active modes. With this, V is
continuous in D. The r_D/2 version jumps by ½ each time a mode activates.

**Confirmation (by me, 2026-11-20).** Monte Carlo, 2 million draws, at γ = (4, 2, 0.6, 0.3) and
θ = 1:

| Quantity | Value |
|---|---|
| Var j (simulated) | **1.2260** |
| Claimed r_D/2 | 1.0000 |
| Corrected formula | **1.2250** |
| E j (simulated) | 1.0395 |
| R(D) | 1.0397 |

**What survives.** Each inactive term is below 1, since γ_k < θ. So r_D ≤ 2V/log²e < r: the
dispersion counts at most the r read dimensions and never the ambient d. Prereg 025's gated
claims also stand: R_C = R_Y, and r_D ≤ r as defined. The false part is the identification of
the dispersion with the active modes alone.

**Why its harness passed.** Check C3b of `verify_dispersion_separation.py` is circular, and it
samples only distortions at which every read mode is active.

## The other errors

- **Book B4.** The book says "refinable iff P₁ ⪯ P₂". That is false. The paper's condition is
  Σ₂* ⪯ Σ₁*, which depends on D.
  - Not refinable although P₁ ⪯ P₂: Σ_x = I₂, P₁ = diag(1, 0), P₂ = I, D₁ = 0.5, D₂ = 1.2.
  - Refinable although P₁ ⪯̸ P₂: P₁ = 2I, P₂ = I, D₁ = 1, D₂ = 0.2.
  - **The paper is right; the book misstates it.**
- **Book B6.** The book states the tax as "rank-M vs rank m < M", confusing the Loewner
  constants with ranks. `thm:commission` requires mP̂ ⪯ P ⪯ MP̂, so the two ranges are equal.
  The book misstates the paper.
- **Paper III `thm:region`, `cor:kobs` and the Σ° program** omit Σ_f ≻ 0. For d ≥ 2,
  Σ_f = −εI₂ satisfies every stated constraint, so the region as written contains spurious
  points. The proof uses Σ_f ≻ 0.

## Gaps

- **The region converses** are written single-letter but claimed to be self-contained for the
  operational region. The n-block step is missing: block-averaged covariances, Fischer's
  inequality, and concavity of log det.
- **`cor:kobs`, achievability for k ≥ 3,** rests on "extend verbatim", which is unproved. The
  covering argument cited belongs to the converse side.
- **`prop:separation`, the forward part.** On the error event the distortion is
  d(X, wrong codeword), which the second-moment hypothesis does not bound. *Fix:* expurgate,
  then use the quadratic triangle inequality.
- **`thm:B3`'s Linder–Zamir conditions** are still cited, not checked ([C7]). The formula also
  needs E log det G < ∞, which the conditions as restated do not supply.

## Overclaims

- **The book's B2/B3 and its custody table** say "the analytic statement is proved". No
  theorem gives the bound b ≤ c, the kernel entropy share, or the vanishing relative gap.
  Surrogate coding with a singular P_C(x) falls outside Linder–Zamir.
- **VI-4's "decisive" check, and the book's "nested-Gaussian" harness for B4, are not a net.**
  The verifier put the original VI-4 bug back into `verify_two_observer.py` checks [1]–[3],
  and all of them still pass. Only `verify_rate_region.py` [3] catches it.
- **The Llama overlap certificate** lists "omission + equal weights" but drops Σ_x = I, which
  is VI-6's own whitening lesson.
- **Evidence descriptions.**
  - "Converse survives 5,000+ random codes": these are Gaussian linear codes, for which the
    result is automatic.
  - "Reproduces every feasible pair": only corner-type pairs are tested.
  - "Verified to machine precision": B3(i) has no gate, and B2a's tolerance is 1e-4.
- **"The diffusion case is pure commission"**: the sandwich hypothesis is not established.

## Exposition

- The book's B1 custody note quotes VI-7 material.
- Paper III's GO-6 paragraph still says "proposed; to be sealed".
- `two-observer-theorem.tex` is stale in its status line, its novelty comments and its C3
  plan.
- In `thm:B3`, the softmax metric is given in the wrong chart. This is harmless, since the
  formula is chart-invariant.
- In `cor:B2a`, the indistinguishability relation need not be an equivalence relation.
- In `prop:dispersion`, the covering of probability 1 − ε is unstated.
- Citations: `cor:kobs` calls Effros "the discrete multiresolution region", which VI-5
  rejected. Paper III treats Kostina–Tuncel as two-stage "extended verbatim", while the ledger
  and the book treat it as *the* k ≥ 3 region. `two-observer-theorem.tex` still cites them as
  the general-source region.

## The book-to-paper map, and whether each correction was carried

| Book | Paper | Status |
|---|---|---|
| B1 | prop:rd, lem:tilt, thm:coding, cor:coding | The paper's own thm:B1 is a different result; **mismatch** |
| B2 | the GO-6 prediction | Not thm:B2; **mismatch** |
| B3 | GO-6 (iii) | thm:B3 is the high-resolution formula; **mismatch** |
| B4 | thm:region, thm:multiobs, thm:multiobs-loss, and the companion file | The book's statement is wrong |
| B5 | thm:region, cor:kobs | — |
| B6 | thm:commission, thm:omission | The book's tax statement is wrong |
| B7 | prop:dispersion, cor:dispersion, prop:separation | The constant is wrong (NEG-18) |

Whether each VI correction is in the current text:

| Record | Carried? |
|---|---|
| VI-3 (B3) | partly |
| VI-4 | yes in text and code, but the net cannot detect the bug |
| VI-5 | (b) yes; (a) partly (citation inconsistencies) |
| VI-6 | the floor and whitening yes; the certificate partly |
| VI-7 | the covering argument yes; **its r_D sharpening is wrong** |

## Harnesses (the verifier's assessment)

- `verify_two_observer.py` is not a net for max-det optimality, and its [4] is circular.
- `verify_rate_region.py`: [3] is real; [1] is an identity; [2] cannot fail on the coupling.
- `verify_observer_mismatch.py`: commission is real. The omission "alt" floor is a
  tautology, and the overstatement is printed but not asserted.
- `verify_dispersion_separation.py`: C3/C3b are circular and run in the all-active regime
  only; C4 and D1–D3 are tautological.
- `verify_go6.py`:
  - the isotropic control assigns all three curves the same array;
  - (b) and (c) are charged a backward-channel rate while their distortion uses forward noise,
    so the rates are not matched;
  - (a) is a Gaussian stand-in.
- `verify_appendixB.py`: B2/B2a and B3(ii) are real but easy; B3(i) has no gate; thm:B1 has
  no net.

## Checked and found correct

- **The two-observer core.**
  - lem:cm, lem:info and lem:maxdet.
  - Reverse water-filling in the whitened basis, with the cap binding on ker P (VI-4's
    correction).
  - The KKT condition, Fisher-additive achievability and nesting by total covariance.
  - Both corollaries, the commuting case, Equitz–Cover, and L = R₁(D₁).
  - The K-map is exact at k = 2, and the rotation leak at k ≥ 3 is real.
- **Commission and omission:** `thm:commission`, including its sharpness, and
  `thm:omission`.
- **Coding theorems:** `prop:dispersion` (both directions), `thm:coding`, `thm:B1`,
  `thm:B2` with its measurable selection, and `cor:B2a`.
- **High resolution:** `thm:B3(ii)`, and the form and chart invariance of B3(i).

## Disposition

- **NEG-18** (the dispersion constant).
- **Corrections owed** to Paper III (a working manuscript: the IEEE version was rejected
  without review on 27 July 2026). A corrected public preprint version is the owner's to post.
- **Corrections owed** to the book's Appendix B, for B1–B4, B6 and B7 and the custody table.
- **New nets owed:** max-det optimality, the region's coupling, and dispersion with inactive
  modes.
- **No B-theorem is promoted** until these are done.
