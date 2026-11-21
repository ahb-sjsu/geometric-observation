# VI-34: R-IND-5 re-check of the Paper III corrections (2026-11-20)

**Target.** The corrections written in response to VI-32 (`claims/audits/VI-32-PaperIII-B.md`),
before any of them was committed:
- in `paper/observation-theory.tex`: `cor:dispersion` (the corrected parallel-Gaussian
  dispersion), the new Blocks step of `thm:region`'s converse, the forward part of
  `prop:separation`, the rescoped `cor:kobs`, and the added $0\prec\Sigma_f$, $0\prec\Sigma_k$;
- the rewritten `chapters/appendix_b_cost_ledger.md` and the COST table of
  `chapters/appendix_f_mathematical_ledger.md`.

**Verifier.** A fresh-context general-purpose agent, working from local files only, with no
browser, connector or network tools and no access to the assistant's verdict. It re-derived
the $D$-tilted information from Kostina and Verdú's definition and ran its own Monte Carlo at
four configurations, including the boundary $\gamma_k=\theta$.

**Verdict.** 2 errors, 4 gaps, 4 overclaims, 3 exposition items. The new derivations are
right; the errors are in a bound the first correction added and in a statement the first
correction left unchanged.

## What the verifier checked and found right

- **The tilted information.** $j=-\lambda^\ast D-\sum_k\log\mathbb E\exp(-\lambda^\ast(y_k-\hat Y_k)^2)$
  at $\lambda^\ast=1/(2\theta)$; numerically $-R'(D)=0.5000$ at $\theta=1$ and $2.5000$ at
  $\theta=0.2$. The active and inactive per-mode terms are as stated, and $\mathbb E j=R(D)$.
- **The variance formula**, by Monte Carlo at four configurations, including $\gamma_k=\theta$
  (1.635 against 1.625). $V$ is continuous at $\gamma_k=\theta$, and $\ker\PC$ contributes
  nothing, by `prop:dispersion`.
- **The Blocks step,** line by line: the chain rule and conditioning; the Gaussian
  maximum-entropy bound with $\mathbb E\,\mathrm{Cov}(X_i\mid M)$; Jensen on $\log\det$; the
  trace bounds through `lem:cm` (the reconstruction is $\sigma(M)$-measurable); the nesting
  $\bar\Sigma_f\preceq\bar\Sigma_b\preceq\Sigma_x$ from per-letter total covariance, preserved by
  averaging.
- **The separation argument, given a valid expurgation.** The quadratic triangle inequality
  holds for a fixed $\PC$, and the error-event bound $2\mathbb E[S_n\mathbf 1_E]+2BP_e$ is right.
- **The $0\prec$ additions** make `thm:region`, $\Sigma^\circ$ in `thm:multiobs-loss` (the
  argmax is attained at an interior point and is unique) and `cor:kobs` true as written.
- **Appendix B's B4** matches `thm:multiobs`; both counterexamples were re-verified
  ($\Sigma_1^\ast=\mathrm{diag}(0.5,1)$ against $\Sigma_2^\ast=0.6I$ does not nest;
  $0.25I$ against $0.1I$ nests). **B6's** sandwich hypothesis matches `thm:commission`, whose
  proof the verifier re-checked.
- No `[proved]` tag remains in Appendix B, so CHARTER T-CUST-1 is respected.

## Findings and dispositions (all applied, 2026-11-20)

| # | Severity | Finding | Applied |
|---|---|---|---|
| 1 | **ERROR** | The corrected bound $r_D\le 2V/\log^2e<r$ is false whenever every tilted mode has $\gamma_k\ge\theta$, which is the whole low-distortion regime: then $2V/\log^2e=r$ exactly. The verifier's Monte Carlo: $\gamma=(4,2,1.5,1.2)$, $\theta=1$ gives Var $j$ = 2.010 against $r/2=2.0$. VI-32's "each inactive term is below 1" overlooks the case with no inactive modes. The same text was in the NEG-18 row and in VI-32's record. | The paper, Appendices B and F and NEG-18 now read $r_D\le 2V\le r$, with equality on the right iff $\gamma_k\ge\theta$ for every $k$, and strict iff some $\gamma_k<\theta$. VI-32's record keeps its sentence, with a dated correction above it. |
| 2 | GAP | "The parallel formula is derived here from [the scalar case]" is wrong: the modes share one distortion budget, so the scalar result does not give it. What is derived is the variance of $j$; identifying the dispersion with it, and the $O(\log n/n)$ remainder, is Kostina–Verdú's general Gaussian approximation applied to an $\mathbb R^r$-valued letter. "In the regime where the normal approximation holds" assumed the result instead of stating its hypotheses. | `cor:dispersion` now states $0<D<\sum_k\gamma_k$, names the general theorem, lists its hypotheses (a unique optimal kernel, which holds; moment conditions on the distortion), and says they are to be checked at the source. Carried in FRONTIER G12. The verifier's recollection that the formula matches Tian–Kostina's Gauss–Markov dispersion is **unverified** and is not cited. |
| 3 | exposition | Units: §consequences uses natural logarithms, so $\log^2e=1$, yet the corollary carried a factor $\log^2e$ beside "in nats". | The corollary states $V_Y$ in nats$^2$ and drops the factor; Appendices B and F follow. |
| 4 | GAP | The expurgation step does not follow: from $d(\hat x_0,c)>B$ the quadratic triangle inequality gives only $d(X,\hat x_0)>B/4$ **or** $d(X,c)>B/4$. The second case needs a per-block distortion bound, uniform in $n$, that `thm:coding`'s statement does not give. | The reference word is added to the codebook (one codeword, no rate cost) and encoding is by minimum distortion, so $d(X,c)\le S_n:=d(X^n,\hat x_0^n)$ and $d(\hat x_0^n,c)\le4S_n$; then $\varepsilon(B)=\sup_n\mathbb E[S_n\mathbf 1\{S_n>B/4\}]\to0$ by uniform integrability of the block averages $S_n$. Block distortion is the per-letter average. |
| 5 | GAP | Source indices are not uniform, so an average-error channel code does not give $\Pr E=P_e$. | The channel code has maximal error probability $\lambda_n\to0$, and $\mathbb E[S_n\mathbf 1_E]\to0$ by uniform integrability. |
| 6 | OVERCLAIM | "The only property used is that $d_{\mathcal C}$ is an admissible distortion" is false once the argument uses the quadratic triangle inequality; $d_{\mathcal C}$ is a squared seminorm in the read space, not "in output space", and the argument does not cover the point-dependent surrogate or the true divergence. | The proposition is stated for a fixed $\PC$ with $d_{\mathcal C}(x,\hat x)=\lVert\PC^{1/2}(x-\hat x)\rVert^2$; the sentence is replaced by the scope statement. |
| 7 | **ERROR** | `cor:kobs` still stated "the achievable region is …" and "refinable iff nested" for every $k$, and its proof said "the refinability criterion does not depend on this step", which is false for the sufficiency direction: nested ⇒ the corner is achievable is exactly $k$-stage achievability. Appendix B's B5 had the same mislabel. | The statement gives the outer bound and refinable ⇒ nested for every $k$, with equality and the iff for $k=2$; the proof says sufficiency for $k\ge3$ waits on the coding step. Appendix B's B5 is split the same way. |
| 8 | OVERCLAIM | Five passages still claimed the $k$-observer result: the abstract, the introduction, the opening of §multiobs, related work, and the open-problems list ("settles completely … the $k$-observer chain"). Related work said Effros and Kostina–Tuncel "supply the operational region", contradicting "Effros gives bounds" in the proof. | Each rescoped to the $k$-observer converse and the necessity of nesting; related work now says Effros gives bounds and the Kostina–Tuncel attribution for $k\ge3$ is to be checked at the source. |
| 9 | GAP (minor) | `cor:kobs`'s converse is single-letter and never called the new Blocks step, which is what gives $0\prec\Sigma_k$; Appendix B claimed the $n$-block step covers it. | The proof now says the Blocks step of `thm:region` applies verbatim, and gives $0\prec\Sigma_k$. |
| 10 | exposition | "$\bar\Sigma_f\succ0$ because the rates are finite": valid, but which inequality? Passing from $(D+\varepsilon,R+\varepsilon)$ codes to the closure needs a compactness line. | The proof cites $R_2\ge\tfrac12\log\det\Sigma_x/\det\bar\Sigma_f$, and adds that $\det\bar\Sigma_f\ge\det\Sigma_x e^{-2R_2}$ keeps limits positive definite. |
| 11 | exposition | Appendix B's B6 tax statement dropped "on the shared range", the design $\Sigma^\ast(\hat P,D/M)$, the coding regime and the sharpness of $r/2$; its floor statement ("a code blind to a direction") was wider than the theorem's scope (every allocation in the $\hat P$-water-filling family). | Both statements rewritten to the theorem's scope. |
| 12 | OVERCLAIM | Classes. By Appendix B's own rule (a theorem netted by a sealed C3 is `[predicted]`-grade), B5's region converse and B7's finite-$n$ reduction have no net that can fail: in 023, check [1] is an identity, [2] cannot fail, and only [3] is real, and it nets the corner; in 025, C4 and D1–D3 are tautological and C3/C3b circular. B2/B3 kept `[demonstrated]` though GO-6's harness does not meet the claim's matched-rate premise and its isotropic control cannot fail. The LEDGER GO-6 row still asserts the "$\ker P_C$ entropy share", which Appendix B calls undefined. | B5's region converse and B7's reduction retagged `[exploratory]` until a net exists (the corner stays `[predicted]`-grade). B2/B3 and the LEDGER GO-6 row are marked **disputed, re-run owed**; the class of GO-6, a sealed registration's outcome, is left to the author. |

## Owed

- The nets VI-32 asked for: max-det optimality, the region's coupling, the dispersion with
  inactive modes (and now also at the boundary $\gamma_k=\theta$ and in the all-active regime,
  where $2V=r$).
- FRONTIER G12: Kostina–Verdú's general theorem and its hypotheses for the vector letter,
  checked at the source.
- A GO-6 re-run at matched rate, if the author wants the class kept.
- A confirming pass on this round's changes before any B-theorem is promoted.
