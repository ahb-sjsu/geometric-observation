# Custody: T1-MK

**Class of the row: `[exploratory]`.** This file is written ahead of any promotion, at the
author's request of 2026-11-22 ("write the FT.7 custody table"). It records what a
`[proved]` row would rest on and what is still missing. The class is the author's to set.

## Claim

The numbered statements of the T1 addendum on moving read kernels,
`paper/t1-moving-kernel/t1-moving-kernel.tex` (v0.6), by label. The source is
$T\sim N(0,\Sigma)$ in $\mathbb R^p$, $\Sigma\succ0$. The consumer acts through a $C^3$ map
$g:\mathbb R^p\to\mathbb R^k$ with three bounded derivatives, loss
$\|g(\hat x)-g(x)\|^2$, local read metric $P_C(x)=J_g(x)^{\mathsf T}J_g(x)$ and
$Q=\mathbb E\,P_C(T)$. Rates are in nats.

- **`lem:kernel`.** $\ker Q=\{v: J_g(T)v=0$ almost surely$\}$.
- **`thm:A`.** For $0\prec\Delta\preceq\Sigma$, the fixed-covariance Gaussian test channel
  is $T=\hat T+Z$ with $Z\sim N(0,\Delta)$ independent of $\hat T$; its rate is
  $\tfrac12\log\det(\Sigma\Delta^{-1})$ and its consumer loss is $L(\Delta)$.
  $R_{\rm fixed}(D)$ is the least rate over such $\Delta$ with $L(\Delta)\le D$. Suppose
  $Q\succ0$, with $\lambda=\lambda_{\min}(Q)$, $K$ any positive constant not less than the value of the note's `eq:K`,
  and $s_0=\lambda/(2K)$.
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
- **`thm:sharp`.** Suppose $Q\succ0$. With
  $R_0(D)=\tfrac p2\log\tfrac pD+\tfrac12\log\det(\Sigma Q)$ and $B=K(\operatorname{tr}Q^{-1})^2$:
  (a) for $D<D_0$, $R_{\rm fixed}(D)\ge R_0(D)-\tfrac p2\log(1+4KD/\lambda^2)$;
  (b) for $D<\min\{p\lambda_{\min}(\Sigma)\lambda,\ p^2/B\}$,
  $R_{\rm fixed}(D)\le R_0(D)-\tfrac p2\log(1-BD/p^2)$. So $R_{\rm fixed}=R_0+O(D)$.
- **`thm:reduce`.** Let $q=\operatorname{rank}Q\ge1$, $H=\Sigma^{1/2}Q\Sigma^{1/2}$, $O$
  orthogonal with first $q$ columns $O_1$ spanning the range of $H$, and
  $f(s)=g(\Sigma^{1/2}O_1s)$ with source $S\sim N(0,I_q)$. Then (a)
  $g(\Sigma^{1/2}Ow)=f(w_1,\dots,w_q)$ for all $w$; (b) $R_{\rm fixed}$ of $(T,g)$ equals
  that of $(S,f)$ for every $D>0$; (c) $f$ has three bounded derivatives and
  $Q_f=O_1^{\mathsf T}HO_1\succ0$. Hence
  $R_{\rm fixed}(D)=\tfrac q2\log\tfrac qD+\tfrac12\log{\det}^+H+O(D)$.
- **`cor:gapq`.** For $q\ge1$, under the hypotheses of `prop:B`(c) and the output
  hypotheses of `cor:C`: as $D\to0$,
  $R_{\rm fixed}(D)-R_C(D)=\tfrac{q-k}2\log(1/D)+O(1)$, between the note's explicit
  $c'_-+O(D)$ and $c'_++O(D)$.
- **The example** $g_a(x_1,x_2)=x_1+a\sin x_2$, $a\ne0$, at $\Sigma=I$:
  $\det Q=\tfrac{a^2}2(1-e^{-1})^2>0$; the image is $\mathbb R$; $s(u)=(u,0)$ is a right
  inverse; $U$ has a smooth density, finite entropy and variance
  $1+\tfrac{a^2}2(1-e^{-2})$. So `cor:C` and `cor:gapq` apply with $p=q=2$, $k=1$.
- **`prop:exact`**, for that example with $0\preceq\Delta\preceq I$ and $v=d_{22}$:
  (a) $L(\Delta)=d_{11}+2ae^{-1/2}d_{12}+a^2F(v)$ with
  $F(v)=1-e^{-v/2}+e^{-2}(e^{3v/2}-\tfrac12(1+e^{2v}))$;
  (b) $F$ is concave on $[0,1]$, so $L(\Delta)\ge\operatorname{tr}(\Theta_a\Delta)\ge\mu\operatorname{tr}\Delta$
  with $\mu=\lambda_{\min}(\Theta_a)>0$; (c) $D_0\ge\mu s_0$.
- **`prop:gapex`**, for that example: $\mathrm{SLB}(D)\le R_C(D)\le\mathrm{SLB}(D)+\tfrac12\log(1+D)$
  with $\mathrm{SLB}(D)=h(U)-\tfrac12\log(2\pi eD)$, so
  $R_{\rm fixed}(D)-R_C(D)=\tfrac12\log(1/D)+C_*+O(D)$ with
  $C_*=\log2+\tfrac12\log\det Q+\tfrac12\log(2\pi e)-h(U)$, the constant $c'_+$ of `cor:gapq`.
  The argument came in review notes passed on by the author on 2026-11-22, whose writer
  is not stated; the assistant checked it.

**Not claimed** (the note's remark on scope and its section "What is not claimed"; VI-52
#1, #2; VI-53 #1, #3):
- **Codes.** Every statement about $R_{\rm fixed}$ is about fixed-covariance Gaussian test
  channels. It is not a bound on every code built from a weight; a code that adapts its
  error covariance to the fiber, or describes $U=g(T)$ directly, can have a lower information rate. No coding
  theorem is invoked for $R_C$; carrying `prop:B` to codes would need, among other things,
  a second moment for the right inverse's output.
- **Beyond the model case.** Three bounded derivatives and a Gaussian source are used
  throughout. Images that are not closed and convex, and outputs with no density in
  $\mathbb R^k$ (a circle, a sine curve), are outside `cor:C` and `cor:gapq`.
- **A range of $D$ for a general consumer.** In general there is no explicit lower bound on
  $D_0$; `prop:exact` gives one for the example only.
- **Learning.** `prop:B` does not show what a learner must learn. Obtaining a right inverse
  means learning a selection of fiber representatives, which is frontier item FT.9. The price here
  is the price of stopping at $Q$ within the fixed-covariance class, not a price of
  learning $g$.
- **Priority.** See "Known gaps".

## Proof

`paper/t1-moving-kernel/t1-moving-kernel.tex`, the proofs following `lem:kernel`, `thm:A`,
`prop:B`, `cor:C`, `thm:sharp`, `thm:reduce`, `cor:gapq`, `prop:exact` and `prop:gapex`. The proofs of
the first four last changed in 45cbc15, apart from one support sentence added to the
proof of `thm:A`(b) in v0.4 and the constant $K$, which `thm:A` now takes as any positive
number at least the value of `eq:K`.
Version 0.2 (2026-11-22) changed the remark `rem:scope` and the example's numerical
paragraphs only: it adds the upper bound $D_0\le3\lambda^2/(4K)$ and says what the quoted
gap numbers do and do not bound. Version 0.3 (the same day) applies VI-54's wording
findings to those passages.

Version 0.4 (the same day) adds `thm:sharp`, `thm:reduce`, `cor:gapq` and `prop:exact`.
Their derivations came from a review of v0.2 passed on by the author; the assistant
re-derived each, and proved the rate step of `thm:reduce`(b) by a Schur-complement
determinant bound. v0.4 also retitles the note to name the channel class, rewrites the
prior-work paragraph from the sources, and adds limits and a paragraph on fibers and
selections on further review notes passed on by the author on 2026-11-22.

Version 0.5 (the same day) applies VI-56: the example of a curved image is now
$(x_1,\sin x_1)$; `prop:gapex`'s proof states both sides of the expansion with their
ranges; a new section "Main results" in v0.6 states the headline result first and calls
Theorem A a step toward it, with no change to any statement or proof; $H_a$ is renamed $\Theta_a$; wording.

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
- **VI-54** read the v0.2 changes: the bound $D_0\le3\lambda^2/(4K)$ of `rem:scope`, its use
  in the example, and the reworded gap paragraph.
  - No mathematical error; the bound is correct and correctly used, and every new number
    reproduces from the JSON.
  - One overclaim: gap figures quoted to four decimals, finer than the sampling error
    (about 0.003) of the rates they come from.
  - The script's docstring contradicted the note; gaps and wording. All applied in v0.3.
  - It did not re-run the net and did not re-read the proofs of `thm:A`, `prop:B` or `cor:C`.
- **VI-55** read v0.4's four new results and the new net.
  - No mathematical error in `thm:sharp`, `thm:reduce`, `cor:gapq` or `prop:exact`; every
    quoted number recomputed, $h(U)$ by its own quadrature; the net re-run and its search
    cross-checked with an independent optimizer.
  - Two stale passages contradicted the new results (the fixed-kernel remark; a caveat on
    $D<D_0$ at $10^{-5}$), and one figure was mislabelled. All applied.
- **VI-56** was a confirming pass on all of that later material, at commit 5b9d1c8.
  - No mathematical error. `prop:gapex` re-derived, with $h(U)$ by its own quadrature.
  - One example violated the standing assumption (a parabola, unbounded derivative);
    check e5 could not fail on a wrong $h(U)$; wording and record items. All applied in
    v0.5, with a second quadrature method for $h(U)$ and two more mutants.
  - No further pass is run on v0.5's changes.
- **Read by VI-56, and listed here as they stood before it:**
  - the first net's code since 45cbc15 (the present c5, m5 and m6);
  - the dispositions of VI-55, including the exact net's check e5 and mutant m6;
  - `prop:gapex` and its proof, added after VI-55's reading. It replaced an unsupported
    statement that the example's gap is $\tfrac12\log(1/D)-0.29+O(D)$: the two constants of
    `cor:gapq` differ by a fixed 0.0004. VI-55 did not catch that; review notes passed on
    by the author on 2026-11-22 did;
  - the other v0.4 text added after VI-55's reading: the prior-work paragraph, the support
    sentence in `thm:A`(b), the strict-inequality remark in `thm:reduce`(b), the paragraph
    on fibers, the method statement for $h(U)$, and the limits.

No fresh-context pass checked the prior-art sources; the assistant read the cited passages
(see "Known gaps"). VI-56 read this file as of 5b9d1c8. Before that, a separate
fresh-context pass read the first version of this custody
file on 2026-11-22, before it was committed; its findings are applied here. It is not a pass
on the proofs and has no VI row.

## C3 harness

| Harness | Tier | CI section |
|---|---|---|
| `experiments/verify_ft7_moving_kernel.py` | re-run | `ci/reproduce.py` [2/3], file mode; seed 20261131, 22 checks |
| `experiments/verify_ft7_exact.py` | re-run | `ci/reproduce.py` [2/3], file mode; seed 20261122, 5 checks |

**What CI compares.** Each re-run must reproduce its committed file's pass/fail flags and
overall verdict. It does not compare the numbers. Every measured number below is from
the committed output of one local run.

**What the first net's checks can and cannot fail on:**
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

**What the exact net's checks can and cannot fail on:**
- **e1** tests `prop:exact`(a) against Monte Carlo in six cases.
- **e2** tests `prop:exact`(b), (c): the sign of $F''$ on a grid, the chord inequality,
  $L\ge\operatorname{tr}(\Theta_a\Delta)$ and $L\ge\mu\operatorname{tr}\Delta$ on 20,000 random
  $\Delta$, and that a numerical estimate of $D_0$ lies between the two bounds.
- **e3** tests `thm:sharp` for $g_1$ with the exact loss: the search's least rate lies in
  the sandwich at three values of $D$ inside the proved range. The comparison with the
  lower side is only as good as the search.
- **e4** tests `thm:reduce`(b) on one instance with $p=3$, $q=2$ and a correlated $\Sigma$.
  The consumer is $g_1$ composed with a linear map, so part (a) holds by construction and
  is not tested. The rate inequality has a margin of 0.89 nats on the sampled $\Delta$ and
  guards only against a wrong direction.
- **e5** tests the numbers quoted for $g_1$: $h(U)$ at two quadrature resolutions and by a
  second method, the variance of $U$ by quadrature against its closed form, the entropy
  step of `prop:gapex` at two values of $D$, the
  family's exact rate against the search, and the family's excess over the two bounds on
  $R_U$ against `cor:gapq`.
- **Fire test** (`--fire`): eight mutants, each a changed formula or value. It is not run
  in CI.

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
| Family rate less the Shannon lower bound on $R_U$, $D=10^{-5}$ | `cor:C`, upper side | ≤ 6.158; this side needs only `thm:A`(d) and the Shannon bound, so $D<D_1$ suffices | `5.4676` | `results/FT7-moving-kernel-net.json#instances.I5.c4_excess_bracket_at_1e-5.1` | 0.69 nats; the measured figure carries sampling error of about 0.003, more than the 0.0004 between the two bounds on $R_U$. Not an independent test: $h(U)$ cancels, and this is the `thm:A`(d) row again. $c_+=0.402$, computed here |
| c3, error of the right inverse after projection, I1 | `prop:B`(c) | 0 | `8.9e-16` | `results/FT7-moving-kernel-net.json#instances.I1.c3.section_max_error` | rounding; the same value for I2 to I4 |
| Fire test, mutants caught | the net | must fail | `6 of 6` | `claims/audits/VI-53-ft7-confirming.md` | the assistant's run after the VI-53 fixes ("After these fixes"). The VI-53 verifier's own 6 of 6 was on the earlier m5 and m6. Not CI-run, not independently re-run |
| Exact net verdict, 5 checks | the exact net | all pass (the script's criteria) | `True` | `results/FT7-exact-net.json#FT7EXACT_supported` | |
| $\mu=\lambda_{\min}(H_1)$ | `prop:exact`(b) | $L\ge\mu\operatorname{tr}\Delta$ | `0.04651` | `results/FT7-exact-net.json#e2.mu` | not sharp: the least sampled ratio is 0.083 |
| Least sampled $L/\operatorname{tr}\Delta$, 20,000 $\Delta$ | `prop:exact`(b) | ≥ 0.04651 | `0.083` | `results/FT7-exact-net.json#e2.worst_ratio_L_over_trace` | factor 1.8 |
| Lower bound $\mu s_0$ on $D_0$ | `prop:exact`(c) | $D_0\ge\mu s_0$ | `0.000465` | `results/FT7-exact-net.json#e2.mu_s0` | $10^{-4}$, $10^{-5}$, $10^{-6}$ are inside the proved range of `thm:A`(c) |
| Upper bound on $D_0$ | `rem:scope` | $D_0\le3\lambda^2/(4K)$ | `0.0021` | `results/FT7-exact-net.json#e2.D0_upper_bound` | |
| Numerical estimate of $D_0$ | `thm:A`(b) | between 0.000465 and 0.0021 | `0.0014` | `results/FT7-exact-net.json#e2.D0_numerical_estimate` | a search, not a certified infimum; $10^{-3}$ is not shown to be inside |
| e3, least rate with exact loss, $D=10^{-5}$ | `thm:sharp` | between 11.38664 and 11.40190 | `11.40082` | `results/FT7-exact-net.json#e3.3.min_rate_exact_loss` | 0.014 above the lower side, 0.0011 below the upper side; the sandwich is 0.015 wide |
| e3, the same, $D=10^{-6}$ | `thm:sharp` | between 13.70198 and 13.70352 | `13.70341` | `results/FT7-exact-net.json#e3.4.min_rate_exact_loss` | the sandwich is 0.0015 wide |
| e3, lower side at $D=10^{-5}$ | `thm:sharp`(a) | — | `11.38664` | `results/FT7-exact-net.json#e3.3.lower` | |
| e3, upper side at $D=10^{-5}$ | `thm:sharp`(b) | — | `11.40190` | `results/FT7-exact-net.json#e3.3.upper` | |
| e4, rank of $Q$ in the reduction instance | `thm:reduce` | 2 | `2` | `results/FT7-exact-net.json#e4.rank_Q` | $p=3$ |
| e4, rate of the lift less $-\tfrac12\log\det E$ | `thm:reduce`(b) | 0 | `0.0` | `results/FT7-exact-net.json#e4.lift_rate_gap` | exact |
| e4, least full rate less reduced rate, 4 random $\Delta$ | `thm:reduce`(b) | ≥ 0 | `0.89` | `results/FT7-exact-net.json#e4.worst_rate_full_minus_reduced` | wide margin: guards the direction only |
| $h(U)$ for $g_1$, quadrature | example | — | `1.598216` | `results/FT7-exact-net.json#e5.h_U` | two resolutions agree to the last float digit; no proved error bound; VI-54 and VI-55 each recomputed it |
| $c'_-$ for $g_1$ | `cor:gapq` | — | `-0.2918` | `results/FT7-exact-net.json#e5.c_minus_prime` | |
| $c'_+$ for $g_1$, which is $C_*$ | `cor:gapq`, `prop:gapex` | — | `-0.291379` | `results/FT7-exact-net.json#e5.c_plus_prime` | 0.0004 above $c'_-$; by `prop:gapex` this is the gap's constant |
| Entropy increase $h(U+\sqrt D N)-h(U)$ at $D=0.01$ | `prop:gapex` | ≤ ½ log(1 + D) = 0.004975 | `0.003490` | `results/FT7-exact-net.json#e5.entropy_step.1.entropy_increase` | factor 1.4; by quadrature |
| Family's exact rate less the Gaussian upper bound on $R_U$, $D=10^{-5}$ | `cor:gapq`, lower side (not tight) | leading term $\tfrac12\log(1/D)+c'_-$ = 5.464709 | `5.464702` | `results/FT7-exact-net.json#e5.family_minus_gaussian_upper` | below the leading term by $7\cdot10^{-6}$, the $O(D)$ term; the Gaussian bound overstates $R_U$ by 0.0004, so this is not the gap; $h(U)$ cancels in this comparison |
| The same less the Shannon lower bound | `prop:gapex` | $\tfrac12\log(1/D)+C_*+O(D)$ = 5.465084 | `5.465077` | `results/FT7-exact-net.json#e5.family_minus_shannon_lower` | equal to $7\cdot10^{-6}$, the $O(D)$ term; $h(U)$ cancels, so this tests the constant of `thm:sharp`, not $h(U)$, $C_*$ or $R_C=R_U$ |
| $h(U)$, second method less first | example | — | `0.0` | `results/FT7-exact-net.json#e5.h_U_method_difference` | $3\cdot10^{-13}$; the VI-56 verifier's own value agrees to 12 decimals |
| Exact net's fire test, mutants caught | the exact net | must fail | `8 of 8` | `claims/audits/VI-56-ft7-v04-confirming.md` | the assistant's run after the VI-56 fixes; the VI-56 verifier's own run was 6 of 6, before mutants m7 and m8. Not CI-run |

## Known gaps

- **The row is `[exploratory]`.** This file does not promote it.
- **The author's read.** No statement by the author of having read these proofs is on
  record.
- **The prior art is read in part.** On 2026-11-22 the assistant read, in the author-hosted
  preprints, Section 2.1 and the concluding remarks of Linder–Zamir (1999) and Section 3.1
  of Linder–Zamir–Zeger (1999); and in the author copy of the published
  Misra–Goyal–Varshney (2011), Section I-B and Section VII through Theorem 15, with
  Example 6 read from the page image. The passages are the ones a review of v0.2 pointed
  to. The papers were not read in full, the preprints are not the published versions, no
  fresh context has checked the reading, and later literature is not surveyed. The note
  makes no claim of priority.
- **A citation flag stays in the source.** The Cover–Thomas reference for the Shannon lower
  bound and the Gaussian upper bound, used in `cor:C`, has not been checked at the page.
- **The imported remainder is not `[proved]`.** `thm:A` rests on T1 v4.1's second-order
  theorem, and row T1 is `[exploratory]`. VI-52 checked $K$ against T1's proof, and the T1
  row records that VI-24 found no false step in T1 v4, but T1 has no custody file.
- **The proved range of `thm:A`(c) is explicit for the example only.** There
  $0.000465\le D_0\le0.0021$, so $10^{-4}$, $10^{-5}$ and $10^{-6}$ are inside, $10^{-2}$ is
  outside, and $10^{-3}$ is not shown to be inside. For a general consumer there is no
  explicit lower bound on $D_0$.
- **Proved ranges are computed for $g_1$ only.** $K$, $s_0$, $c$ and $D_1$ are not computed
  for I1 to I3, so none of their cases is shown to be in a proved range.
- **Only one consumer tests the lower bounds.** c5 and e3 run for $g_1$ alone, $p=2$. I1 to
  I3 test `thm:A`(a) and upper bounds. `thm:reduce` is tested on one instance, built from
  $g_1$, and only its part (b).
- **c5 is a numerical search, not a certified minimum.** A lower rate that the grid and the
  simplex polish both miss would pass unseen. The VI-53 verifier's independent optimizer
  agreed to 10⁻⁵, on the form of c5 before 45cbc15.
- **`cor:C` and `cor:gapq` are tested only through $R_{\rm fixed}$.** Check e5 compares the
  family's exact rate, less each bound on $R_U$, with `cor:gapq`'s two constants, and they
  agree to $7\cdot10^{-6}$. That tests the constant of `thm:sharp` and the arithmetic of the
  corollary. What the corollaries add has no check: $R_C=R_U$, and that $R_U$ lies between
  the Shannon and Gaussian bounds. $R_C$ is never computed.
- **The first net's gap figures carry sampling error.** 5.4635, 5.4672 and 5.4676 in its
  rows above come from two Monte Carlo samples and are good to two decimals; the exact
  figures are 5.4647 and 5.4651.
- **No check can fail on some statements.** `lem:kernel`, `thm:A`(b), `prop:B`(a) and the
  measurability clause of `prop:B`(b) have no check. $R_C$ is never computed, so the
  equalities of `prop:B`(b) and (c) are tested only through c3's two steps.
- **CI reproduces flags, not numbers.** A re-run with different values passes while the
  flags hold.
- **Monte Carlo.** The first net's losses are Monte Carlo means at one seed; its
  $\lambda_{\min}(Q)$ differs from the closed form by 0.0004, and c1 uses the Monte Carlo
  value. The exact net uses Monte Carlo only to test the closed form (e1) and the
  three-dimensional loss (e4).
- **Constants computed here.** $c$, $D_1$, $c_-$, $c_+$ and the number 5.4635 for $g_1$ are
  computed from the note's formulas and the first net's JSON; they are not themselves in a
  JSON, and no check computes them. $h(U)$, $c'_\pm$ and the bounds on $D_0$ are in the
  exact net's JSON.
- **Neither fire test is in CI,** and each result on the present mutants is the assistant's
  own run.
- **The prior-work reading has no fresh-context check,** and v0.5's changes have none.
