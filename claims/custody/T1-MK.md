# Custody: T1-MK

**Class of the row: `[exploratory]`.** This file is written ahead of any promotion, at the
author's request of 2026-11-22 ("write the FT.7 custody table"). It records what a
`[proved]` row would rest on and what is still missing. The class is the author's to set.

## Claim

The numbered statements of the T1 addendum on moving read kernels,
`paper/t1-moving-kernel/t1-moving-kernel.tex` (v0.2), by label. The source is
$T\sim N(0,\Sigma)$ in $\mathbb R^p$, $\Sigma\succ0$. The consumer acts through a $C^3$ map
$g:\mathbb R^p\to\mathbb R^k$ with three bounded derivatives, loss
$\|g(\hat x)-g(x)\|^2$, local read metric $P_C(x)=J_g(x)^{\mathsf T}J_g(x)$ and
$Q=\mathbb E\,P_C(T)$. Rates are in nats.

- **`lem:kernel`.** $\ker Q=\{v: J_g(T)v=0$ almost surely$\}$.
- **`thm:A`.** For $0\prec\Delta\preceq\Sigma$, the fixed-covariance Gaussian test channel
  is $T=\hat T+Z$ with $Z\sim N(0,\Delta)$ independent of $\hat T$; its rate is
  $\tfrac12\log\det(\Sigma\Delta^{-1})$ and its consumer loss is $L(\Delta)$.
  $R_{\rm fixed}(D)$ is the least rate over such $\Delta$ with $L(\Delta)\le D$. Suppose
  $Q\succ0$, with $\lambda=\lambda_{\min}(Q)$, $K$ the constant of the note's `eq:K` with
  $K>0$, and $s_0=\lambda/(2K)$.
  - (a) If $0\prec\Delta\preceq\Sigma$ and $\operatorname{tr}\Delta\le s_0$, then
    $\operatorname{tr}\Delta\le2L(\Delta)/\lambda$.
  - (b) $D_0=\inf\{L(\Delta):0\prec\Delta\preceq\Sigma,\ \operatorname{tr}\Delta\ge s_0\}$
    is positive, and is $+\infty$ when that set is empty.
  - (c) For $D<D_0$: $R_{\rm fixed}(D)\ge\tfrac p2\log\tfrac{p\lambda}{2D}+\tfrac12\log\det\Sigma$.
  - (d) For $D<D_1$: $R_{\rm fixed}(D)\le\tfrac p2\log(1/D)+c$, with
    $c=\tfrac12\log\det(\Sigma Q)+\tfrac p2\log(2p)$ and
    $D_1=2p\min\{\lambda_{\min}(\Sigma)\lambda,\ p/(K(\operatorname{tr}Q^{-1})^2)\}$.
- **`prop:B`.** With $U=g(T)$ and image $\mathcal U$: (a) $R_C\ge R_U^{\mathcal U}\ge R_U$;
  (b) $R_C=R_U^{\mathcal U}$ if $g$ has a measurable right inverse on $\mathcal U$;
  (c) $R_C=R_U$ if moreover $\mathcal U$ is closed and convex.
- **`cor:C`.** Under the hypotheses of `thm:A` and `prop:B`(c), with $U$ having a density
  with finite differential entropy $h(U)$ and a finite, positive definite covariance with
  least eigenvalue $\kappa$: for $D<\min\{D_0,D_1,k\kappa\}$,
  $\tfrac{p-k}2\log\tfrac1D+c_-\le R_{\rm fixed}(D)-R_C(D)\le\tfrac{p-k}2\log\tfrac1D+c_+$,
  with the note's explicit $c_\pm$.
- **The example** $g_a(x_1,x_2)=x_1+a\sin x_2$, $a\ne0$, at $\Sigma=I$:
  $\det Q=\tfrac{a^2}2(1-e^{-1})^2>0$; the image is $\mathbb R$; $s(u)=(u,0)$ is a right
  inverse; $U$ has a smooth density, finite entropy and variance
  $1+\tfrac{a^2}2(1-e^{-2})$. So `cor:C` applies with $p=2$, $k=1$.

**Not claimed** (the note's remark on scope and its section "What is not claimed"; VI-52
#1, #2; VI-53 #1, #3):
- **Codes.** The lower bound is for fixed-covariance Gaussian test channels. It is not a
  bound on every code built from a weight. No coding theorem is invoked for $R_C$;
  carrying `prop:B` to codes would need, among other things, a second moment for the right
  inverse's output.
- **The case $\operatorname{rank}Q<p$,** and in particular a fixed kernel. `thm:A` assumes
  $Q\succ0$ and the note proves nothing outside it.
- **Learning.** `prop:B` does not show what a learner must learn. How a learner obtains the
  right inverse from queries, and at what cost, is frontier item FT.9.
- **Priority.** See "Known gaps".

## Proof

`paper/t1-moving-kernel/t1-moving-kernel.tex`, the proofs following `lem:kernel`, `thm:A`,
`prop:B` and `cor:C`, and the section "An example". The proofs last changed in 45cbc15.
Version 0.2 (2026-11-22) changed the remark `rem:scope` and the example's numerical
paragraphs only: it adds the upper bound $D_0\le3\lambda^2/(4K)$ and says what the quoted
gap numbers do and do not bound.

`thm:A` imports one result: the second-order remainder
$|L(\Delta)-\operatorname{tr}(Q\Delta)|\le\rho_b(\Delta)$ of the T1 note v4.1 (its theorem
"The test channel is exact to second order"). Ledger row T1, which carries that theorem, is
`[exploratory]`.

## R-IND-5

- **VI-52** read every proof line and re-derived each constant by hand, including $K$
  against T1's proof. It reviewed the net as committed in ec4367b, before check c5 existed.
  - No mathematical error in any numbered statement.
  - Two overclaims in the prose.
  - Against the net: the slope checks could not fail if `thm:A`(c) were false (#3); c1 never
    sampled the tight direction (#4); mutants m2 to m4 only compared numbers (#5); c3 for
    $g_1$ never called $g$ and was vacuous (#6, an error).
  - Against the text: the restricted output rate was undefined and measurability unaddressed
    (#7); one unproved assertion, since dropped (#10).
- **VI-53** was a confirming pass at commit 4f55b41.
  - No error in the mathematics or the net code; all 14 dispositions present.
  - Three overclaims in the prose and one misrounded numeral.
  - Gaps in the net's checks: c5 was one-sided and compared two different samples (#11);
    m5 and m6 passed on "slope is not 1" (#12).
  - Of its 16 findings, 14 were applied in 45cbc15. #13 (c3 for $g_1$ is nearly trivial) was
    left as is; #14 (CI wall time) needed no change.
- **No pass with a VI row has read the state after 45cbc15.** That includes the bound
  $D_0\le3\lambda^2/(4K)$ of v0.2, which the reviewer of this file derived and the
  assistant re-derived, and the present form of c5 (same
  sample, two-sided, the closed-form $\lambda$) and the present m5 and m6. c5 is the only
  check on the lower bound.

Neither pass checked the prior-art sources. A separate fresh-context pass read this custody
file on 2026-11-22, before it was committed; its findings are applied here. It is not a pass
on the proofs and has no VI row.

## C3 harness

| Harness | Tier | CI section |
|---|---|---|
| `experiments/verify_ft7_moving_kernel.py` | re-run | `ci/reproduce.py` [2/3], file mode; seed 20261131, 22 checks |

**What CI compares.** The re-run must reproduce the committed file's 22 pass/fail flags and
its overall verdict. It does not compare the numbers. Every measured number below is from
the committed output of one local run.

**What the checks can and cannot fail on:**
- **c1** tests the inequality of `thm:A`(a) on random small $\Delta$ and on $\Delta$ nearly
  of rank one along the least eigenvector of $Q$, for the four moving instances.
- **c2** tests the slope of a hand-picked achievable family. It is an upper bound on
  $R_{\rm fixed}$, so it tests `thm:A`(d) and T1's second-order statement, not `thm:A`(c).
- **c3** tests that the right inverse, after projection onto the image, inverts $g$, and
  that projecting does not raise the consumer loss (the step of `prop:B`(c)). Both are
  informative for the radial instances, whose image is $[1,\infty)$. For $g_1$ the first
  is identically zero and cannot fail (VI-53 #13), and the expression is typed inline, not
  shared with the loss.
- **c4** only checks that a bracket is finite.
- **c5**, for $g_1$ only, searches for the least rate over all $2\times2$ $\Delta$ and tests
  its slope, its agreement with the family $tQ^{-1}$ on the same sample, and that it is not
  below the expression of `thm:A`(c). This is the only check on the lower bound.
- **Fire test** (`--fire`): six mutants. Two run the c5 search on a changed instrument and
  must return slope 1/2. It is not run in CI.

## Constants and slack

Instance I5 is $g_1$. Instances I1 to I3 are radial consumers with a moving kernel; I4 is a
fixed-kernel control. Where the "Proved bound" cell is not something the note proves, it
says what it is.

| Constant | Defined at | Proved bound | Measured | Source | Slack |
|---|---|---|---|---|---|
| Net verdict, 22 checks | the net | all pass (the script's criteria) | `True` | `results/FT7-moving-kernel-net.json#FT7NET_supported` | |
| $\lambda_{\min}(Q)$ for $g_1$, closed form | example | $>0$ | `0.13993` | `results/FT7-moving-kernel-net.json#instances.I5.c5.lambda_min_Q_exact` | |
| $\lambda_{\min}(Q)$ for $g_1$, Monte Carlo | example | — (an estimate of the closed form) | `0.1395` | `results/FT7-moving-kernel-net.json#instances.I5.lambda_min_Q` | differs by 0.0004 at 10⁶ samples; c1 uses this value |
| $K$ for $g_1$ | `eq:K` | — | `6.993` | `results/FT7-moving-kernel-net.json#instances.I5.c5.K` | from $M_1=\sqrt2$, $M_2=M_3=1$, upper bounds on the derivatives |
| $s_0=\lambda/(2K)$ for $g_1$ | `thm:A` | — | `0.0100` | `results/FT7-moving-kernel-net.json#instances.I5.c5.s0` | (a) is proved only for tr Δ ≤ 0.0100; c1 samples tr Δ up to 0.03, so about a third of its random cases and two of its three adversarial cases are in the proved range |
| c1, largest $\lambda\operatorname{tr}\Delta/(2L)$, I5 | `thm:A`(a) | ≤ 1, for tr Δ ≤ $s_0$ | `0.4982` | `results/FT7-moving-kernel-net.json#instances.I5.c1_worst_ratio` | factor 2; the ratio tends to 1/2 along the least eigenvector |
| c1, the same, I1 | `thm:A`(a) | ≤ 1, for tr Δ ≤ $s_0$; $s_0$ not computed for I1 | `0.5056` | `results/FT7-moving-kernel-net.json#instances.I1.c1_worst_ratio` | factor 2; not shown to be in the proved range |
| c1, the same, I2 | `thm:A`(a) | as for I1 | `0.5038` | `results/FT7-moving-kernel-net.json#instances.I2.c1_worst_ratio` | as for I1 |
| c1, the same, I3 | `thm:A`(a) | as for I1 | `0.4993` | `results/FT7-moving-kernel-net.json#instances.I3.c1_worst_ratio` | as for I1 |
| c5, least rate found at $D=10^{-2}$ | `thm:A`(c) | none: $D$ is outside the proved range ($D_0\le0.0021$). The expression of (c) is 2.639 | `4.485` | `results/FT7-moving-kernel-net.json#instances.I5.c5.min_rate_all_Delta.0` | 1.85 nats over the expression |
| c5, least rate found at $D=10^{-3}$ | `thm:A`(c) | ≥ 4.941 if $D<D_0$, which is not shown | `6.794` | `results/FT7-moving-kernel-net.json#instances.I5.c5.min_rate_all_Delta.1` | 1.85 nats |
| c5, least rate found at $D=10^{-4}$ | `thm:A`(c) | ≥ 7.244 if $D<D_0$, which is not shown | `9.097` | `results/FT7-moving-kernel-net.json#instances.I5.c5.min_rate_all_Delta.2` | 1.85 nats |
| c5, least rate found at $D=10^{-5}$ | `thm:A`(c) | ≥ 9.546 if $D<D_0$, which is not shown | `11.400` | `results/FT7-moving-kernel-net.json#instances.I5.c5.min_rate_all_Delta.3` | 1.85 nats |
| The expression of `thm:A`(c) at $D=10^{-5}$ | `thm:A`(c) | — | `9.546` | `results/FT7-moving-kernel-net.json#instances.I5.c5.thmA_c_bound.3` | from the closed-form λ |
| c5, slope of the least rate in $\log(1/D)$ | `thm:A` | $p/2=1$ as $D\to0$; the script's tolerance is 0.03 | `1.0009` | `results/FT7-moving-kernel-net.json#instances.I5.c5.slope` | the fit includes $D=10^{-2}$, outside the proved range; a slope of 1/2 would mean (c) fails |
| c5, search agrees with the family $tQ^{-1}$ on one sample | the net | — (script tolerance: within 10⁻³ nats, two-sided) | `True` | `results/FT7-moving-kernel-net.json#verdict.c5_I5_matches_family_same_sample` | observed at most 10⁻⁴ |
| c5, search not below the expression of (c) | `thm:A`(c) | as in the four rows above | `True` | `results/FT7-moving-kernel-net.json#verdict.c5_I5_above_thmA_bound` | |
| Family $tQ^{-1}$ rate at $D=10^{-5}$, larger sample | `thm:A`(d) | ≤ 12.094 | `11.403` | `results/FT7-moving-kernel-net.json#instances.I5.rows.6.R_fix` | 0.69 nats; the bound is $\log(1/D)+c$ with $c=0.5810$, proved for $D<D_1=0.0186$, both computed here from the note's formulas; the whole grid is below $D_1$ |
| c2, family slope, I5 | `thm:A`(d) | 1 as $D\to0$; tolerance 0.03 | `1.0007` | `results/FT7-moving-kernel-net.json#instances.I5.slope_R_fix` | upper bound only |
| c2, family slope, I1 | `thm:A`(d) | 1 as $D\to0$; $D_1$ not computed for I1 | `1.0002` | `results/FT7-moving-kernel-net.json#instances.I1.slope_R_fix` | upper bound only |
| c2, family slope, I2 | `thm:A`(d) | 1.5, as for I1 | `1.4995` | `results/FT7-moving-kernel-net.json#instances.I2.slope_R_fix` | upper bound only |
| c2, family slope, I3 | `thm:A`(d) | 1.5, as for I1 | `1.5001` | `results/FT7-moving-kernel-net.json#instances.I3.slope_R_fix` | upper bound only |
| c2, family slope, the control I4 | the net | — (the script's prediction, 0.5; the note proves nothing for a fixed kernel) | `0.5000` | `results/FT7-moving-kernel-net.json#instances.I4.slope_R_fix` | |
| Family rate less the Shannon lower bound on $R_U$, $D=10^{-5}$ | `cor:C`, upper side | ≤ 6.158, if $D<D_0$ | `5.4676` | `results/FT7-moving-kernel-net.json#instances.I5.c4_excess_bracket_at_1e-5.1` | 0.69 nats. Not an independent test: $h(U)$ cancels, and this is the `thm:A`(d) row again. $c_+=0.402$, computed here |
| c3, error of the right inverse after projection, I1 | `prop:B`(c) | 0 | `8.9e-16` | `results/FT7-moving-kernel-net.json#instances.I1.c3.section_max_error` | rounding; the same value for I2 to I4 |
| Fire test, mutants caught | the net | must fail | `6 of 6` | `claims/audits/VI-53-ft7-confirming.md` | the assistant's run after the VI-53 fixes ("After these fixes"). The VI-53 verifier's own 6 of 6 was on the earlier m5 and m6. Not CI-run, not independently re-run |

## Known gaps

- **The row is `[exploratory]`.** This file does not promote it.
- **The author's read.** No statement by the author that he has read these proofs is on
  record; the note's own footnote of 2026-11-21 says they are unread.
- **The prior art is unread.** Linder–Zamir (1999) and Linder–Zamir–Zeger (1999), on
  high-resolution coding for non-difference distortion measures, could not be obtained.
  Misra–Goyal–Varshney (2011) was read in part, through an automated summary. The note makes
  no claim of priority, and part of `prop:B` or `cor:C` may be in those papers.
- **A citation flag stays in the source.** The Cover–Thomas reference for the Shannon lower
  bound and the Gaussian upper bound, used in `cor:C`, has not been checked at the page.
- **The imported remainder is not `[proved]`.** `thm:A` rests on T1 v4.1's second-order
  theorem, and row T1 is `[exploratory]`. VI-52 checked $K$ against T1's proof, and the T1
  row records that VI-24 found no false step in T1 v4, but T1 has no custody file.
- **No tested $D$ is shown to be in the proved range of `thm:A`(c).** The note
  (v0.2, `rem:scope`) gives only an upper bound: letting $\Delta$ tend to
  $s_0vv^{\mathsf T}$ along the least eigenvector gives
  $D_0\le\lambda s_0+Ks_0^2=3\lambda^2/(4K)$, which is 0.0021 for $g_1$. So $D=10^{-2}$ is outside the range. $D_0$ has no lower bound on record, so
  $10^{-3}$, $10^{-4}$ and $10^{-5}$ are not shown to be inside. The same holds for `cor:C`.
- **Proved ranges are computed for $g_1$ only.** $K$, $s_0$, $c$ and $D_1$ are not computed
  for I1 to I3, so none of their cases is shown to be in a proved range.
- **Only one instance tests the lower bound.** c5 runs for $g_1$ alone, $p=2$. I1 to I3 test
  `thm:A`(a) and upper bounds, not (c).
- **c5 is a numerical search, not a certified minimum.** A lower rate that the grid and the
  simplex polish both miss would pass unseen. The VI-53 verifier's independent optimizer
  agreed to 10⁻⁵, on the form of c5 before 45cbc15.
- **`cor:C` has no test of its own.**
  - Its upper side, tested with the family, repeats the `thm:A`(d) row.
  - Its lower side would be tested by the search's minimum less the Gaussian upper bound on
    $R_U$. At $D=10^{-5}$ that is $11.3996-5.9361=5.4635$ against
    $\tfrac12\log(1/D)+c_-=3.610$, with $c_-=-2.146$. This is the `thm:A`(c) comparison
    again, and no check computes it.
  - The number 5.4672 that the note quotes is the family less the Gaussian upper bound. It
    bounds the true gap in neither direction; the note says so since v0.2.
  - What `cor:C` adds to `thm:A` has no check: $R_C=R_U$, the Shannon lower bound and the
    Gaussian upper bound on $R_U$.
- **No check can fail on some statements.** `lem:kernel`, `thm:A`(b), `prop:B`(a) and the
  measurability clause of `prop:B`(b) have no check. $R_C$ is never computed, so the
  equalities of `prop:B`(b) and (c) are tested only through c3's two steps.
- **CI reproduces flags, not numbers.** A re-run with different values passes while the 22
  flags hold.
- **Monte Carlo.** Every loss is a Monte Carlo mean at one seed. The Monte Carlo
  $\lambda_{\min}(Q)$ differs from the closed form by 0.0004, and c1 uses the Monte Carlo
  value.
- **Constants computed here.** $c$, $D_1$, $c_-$, $c_+$, the bound on $D_0$ and the
  number 5.4635 for $g_1$ are computed from the note's formulas and the JSON's entries; they
  are not themselves in the JSON, and no check computes them. $c_+$ uses
  $h(U)=1.598$, recovered from the script's bracket for $R_U$. The reviewer of this file
  recomputed all of them, and $h(U)$ by its own quadrature.
- **The fire test is not in CI,** and its result on the present mutants is the assistant's
  own run.
- **No fresh pass has read the proofs or the net since 45cbc15.**
