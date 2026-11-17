# Paper four (working name `tit-unstable-ergodic`)

Fourth paper in the rate-leakage-distortion series, after
`paper/tit-rate-leakage` (one), `paper/tit-stationary` (two) and
`paper/tit-beyond-stationary` (three). It takes up open problems listed at
the end of paper three.

**Status (2026-11-16, evening): working draft, 24 pages. Not submitted, no
venue chosen.** The folder name and the title are provisional; title,
venue and authorship are the owner's decisions. No human has read any of
it. All proofs were drafted by Claude models; every referee pass recorded
below was made by a model.

Numbering changed on 2026-11-16 (evening). Theorems 10 and 11 and Lemma
12 are new; the old Theorem 10, Proposition 11, Corollary 12, Lemma 13,
and Theorem 14 are now Theorem 13, Proposition 14, Corollary 15, Lemma
16, and Theorem 18; Lemma 17 is new. Records and docstrings written
before that day use the old numbers.

## Scope

The paper treats three of paper three's open problems: unstable vector
sources (with holders of finite memory and with stable rational filters),
poles on the unit circle (scalar sources), and fast variation without a
period (scalar closed form; vector sources with a holder of finite
memory). Non-Gaussian linear processes with infinite dependence are not
drafted; whether they go here or into a later paper is open
(recommendation recorded 2026-11-16: decide after reading their prior art).

| Result | Statement | Main tools |
|---|---|---|
| Theorem 1 | Vector autoregressive source with unstable poles; holder observing a linear filter of finite memory of the source in white noise. The region is the stationary spectral region of paper two for f = Phi^{-1} Sigma Phi^{-*} and the same holder, moved by rho_star (sum of log modulus over all unstable poles) in rate and by rho_hid (the same sum over the unstable poles hidden from the holder: Kalman-unobservable, i.e. cancelled by the holder's filter) in leakage. The window cost converges to the shifted spectral cost. | Lemmas 2 to 9 |
| Lemma 2 | The inverse covariance of a window is block Toeplitz minus a term on the last d blocks: the window is a stationary bridge plus its final state | Full convolution matrix |
| Lemma 3 | Group covariances of the bridge interior are within a geometrically small term of a stationary window | Matrix Fejer-Riesz, banded precision of a stationary autoregression |
| Lemma 4 | The holder's Kalman innovation covariance has log det = integral of log det(Sigma_U + G f G^*) + 2 (rho_star - rho_hid) | Kalman decomposition, Riccati convergence, Jensen |
| Lemma 5 | The final state's covariance grows at rho_star, its covariance given the holder at rho_hid; explicit N-independent lower bounds | Lemmas 2 and 4, circulant log-determinants |
| Lemma 6 | Low-rank changes of the precision and of the holder's information matrix change the window cost by a computable constant plus O(log N) | Feasible sets in the precision variable |
| Lemma 7 | The block circulant window cost tends to the spectral cost | Shift invariance, convexity, paper two's Lemma 2 |
| Lemma 8 | Paper three's Lemma 12 for a holder of finite memory (drop each group's first m observations) | Paper three's Lemmas 11 and 12 |
| Lemma 9 | Finite clipped quantizer for the final state | Gaussian tails, a lattice entropy bound |
| **Theorem 10** (new) | Theorem 1 for a holder whose filter is rational and stable (infinite impulse response). rho_hid is defined through the joint state space of source and filter; a simple pole is hidden iff G(1/rho) v = 0. Every truncation of a filter that cancels a pole sees the pole, so the result does not follow by truncation; the proof truncates only on the bridge and treats the final state exactly. | Joint realization, low-rank-plus-small-norm split of the information matrix (eq. 3), paper two's noise splitting (Theorem 22) |
| **Theorem 11** (new) | Scalar autoregressive source with poles anywhere, including on the unit circle, scalar holder gain: the region is the quadrant above (rho_star + r_f, rho_star 1{H=0} + l_f) for every D > 0. Poles on the circle cost nothing. | Lemma 12, paper three's Lemma 24 and Theorem 26 |
| **Lemma 12** (new) | Eigenvalues of the window covariance with poles on the circle: polynomial bounds, weak convergence of the bulk, the log-determinant split, uniform integrability of log | Interlacing, an elementary log-det bound, Szego for a bounded symbol |
| Theorem 13 | Scalar source with uniformly bounded window covariances whose eigenvalue distributions converge, scalar holder in white noise: the region is one quadrant, reverse water-filling on the limit | Paper three's Lemma 24 and Theorem 26 |
| Proposition 14 | Sources driven by a uniquely ergodic homeomorphism with continuous, finite-range correlations have a limiting eigenvalue distribution, the same for every starting point | Moments, Oxtoby's uniform ergodic theorem |
| Corollary 15 | Cyclostationary process sampled at an incommensurate rate: the limit exists, does not depend on the sampling phase, and is the reverse water-filling of Theorem 13, with the leakage. This proves the conjecture of Tan, Dabora and Poor (ISIT 2024, arXiv 2405.11405, Remark 1) | Theorem 13, Proposition 14 |
| Lemma 16 | The frozen-block program V_n over a phase law, with the interior holder of a block: convex and continuous in the distortion, continuous under weak convergence, convex in the law, Lipschitz in the weight | Paper two's Lemmas 1 and 2 |
| **Lemma 17** (new) | Paper three's Lemma 10 (block decomposition) for a holder of finite memory: the first m_h observations of each block are bounded as further observations | Paper three's Lemma 10 |
| Theorem 18 | Vector source driven by a totally uniquely ergodic map, continuous finite-range correlations, a floor on the covariances, holder of finite memory (new; was memoryless): the region is given by the limit of the frozen-block programs, error O(1/n), the same for every starting phase; the window cost converges to it uniformly in the phase | Lemmas 8, 16, 17, paper one's Theorem 3, Oxtoby |

Imports from paper two: codes for stationary sources with a holder filter
(Theorems 16, 20, 22), the noise splitting of Theorem 22, real minimizers
(Lemma 1), continuity of the spectral program in the measure (Lemma 2),
and the order inequalities of Lemma 11: (c) re-derived per frequency for
any holder in (iii) of Section II, and (b), whose proof holds for any
information matrix, in the upper bound of Theorem 18.

## Prior art

Sweep of 2026-11-16 by a model, extended the same evening. Read the cited
items before relying on this list.

- Scalar unstable autoregressive rate-distortion: Gray 1970, Hashimoto and
  Arimoto 1980, Gray and Hashimoto 2008. Vector case: only a sketch and an
  upper bound in Sahai and Mitter (arXiv cs/0610143). Gutierrez-Gutierrez
  et al. 2018 cover asymptotically WSS vector sources, which excludes
  unstable poles. For poles on the unit circle the paper attributes the
  no-holder rate to Gray 1970 and Gray and Hashimoto 2008 and says it has
  not read their full texts on that point.
- Gutierrez-Gutierrez et al., Probl. Inf. Transm. 60(1), 2024: its Theorem 4
  assumes companion spectral radius below one, which excludes unstable
  poles (reported by a reader with access; not read here). An outside
  reader notes that it reproduces the vector formula of Toms and Berger
  under that assumption, which supports the distinction but does not
  settle the scope of the original.
- Toms and Berger 1971, "Information rates of stochastically driven
  dynamic systems" (IEEE Trans. Inf. Theory 17(1):113-114, DOI
  10.1109/TIT.1971.1054569): only the abstract and index records were
  found (searched again 2026-11-16; the full text is paywalled). Related:
  W. Toms, "Information rates of dynamic systems", a 1972 Ph.D. thesis
  abstract in the same journal. **The paper claims no priority for the
  rate of an unstable vector source** until the correspondence is read.
- No leakage or equivocation result for unstable sources was found.
- Lemma 4 is a discrete-time relative of Braslavsky et al. 1999 (continuous
  time). The discrete identity was not found stated; it is derived, not
  claimed as new.
- Sampled cyclostationary sources:
  - Abakasanga, Shlezinger and Dabora 2020 (memoryless samples, small
    distortion, a limit superior).
  - Tan, Dabora and Poor, ISIT 2024, arXiv 2405.11405v2 (memory; an average
    over the phase of limits superior; phase independence conjectured,
    Remark 1). Read, pages 1 to 6.
  - Tan, Dabora and Poor, ISIT 2025, arXiv 2507.00656 (bounded processing
    delay, letting the encoder align each sequence's phase; the function
    is a limit superior of programs minimized over the phase). Its text was
    downloaded and searched on 2026-11-16: the only statement on phase is
    the numerical observation that the finite programs become nearly
    independent of the phase for long sequences; no conjecture is stated.
  - Tan, Dabora and Poor, "Rate-distortion analysis for sampled correlated
    cyclostationary Gaussian processes", IEEE Trans. Commun., vol. 74,
    pp. 5961-5978, 2026, DOI 10.1109/TCOMM.2026.3663539: only the
    Princeton record and a summary of its abstract were read (oscillator
    jitter as motivation, information-spectrum methods, the function is
    sensitive to synchronization and not monotone in the sampling rate).
    The abstract's motivation does not establish that its model has random
    sampling times, so the paper says only that the article treats sampled
    correlated cyclostationary Gaussian processes (an outside reader's
    correction, 2026-11-16). **Whether it addresses the conjecture of the
    2024 paper is not known**; the paper says so.
- Correction to Lemma 8 (outside reader, 2026-11-16, after commit ee4735c):
  the proof said that the seed and T'_j are independent of the remainder
  E_j; the seed is not (Cov(zeta, E_j) = -C_j^T). The step now uses that
  the given encoder is deterministic, so M_j = f(T'_j), and T'_j alone is
  independent of (E_j, U_j). The conclusion is unchanged. The same
  conflation of the seed with the code's private randomness was made when
  paper three's coupling was rewritten for Lemma 8; paper three's own
  Lemma 11 uses the code's private randomness Z', which is independent,
  and is correct as stated. The abstract's statement for vector sources
  now also says "with no poles on the unit circle", which Theorems 1 and
  10 assume.

## Committed checks (Appendix A)

Pass criteria of every check after `verify_unstable_vector.py` were
written into the scripts before their first runs. Failed criteria are
recorded with their records; the appendix summarizes and points here.

`verify_unstable_vector.py` (Atlas, numpy 2.4.4), record
`verify_unstable_vector.json` (515 s), twelve sources (Section III, Theorem
1). Its pass criteria were written after exploratory probes of the same
computations, so they record agreement rather than test a fixed
prediction; the appendix says so.

- Lemma 2 exact; the stationary-window precision structure to 1e-12;
  Lemma 4 to 2e-14; Lemma 5 growth rates with N times the error below 2 at
  N = 400; the Lemma 5(c) floor holds with a margin of 1.7 or more.
- Theorem 1 window cost (visible pole, hidden pole, second-order hidden
  pole; three weights): the gap to the limit shrinks by a factor of 8 from
  N = 40 to 320, at most 2e-3 bits at N = 320. The holder that sees only
  the innovations behaves the same (9e-4 bits); that run has no criterion.
- **One criterion failed**: the cost was to change by at most 1e-6 bits
  between caps M = 1e3 and 1e5; for the second-order source at N = 40 and
  80 it changed by up to 1.9e-6. The failing record is committed. A
  follow-up (`--caps`, record `verify_unstable_vector_caps.json`) shows the
  cost changes by at most 2e-8 bits between M = 1e5 and 1e7.
- The twelfth source, built in double precision with a mode hidden only to
  6e-17, shows the discontinuity of rho_hid: its posterior growth falls from
  0.44 to 0.10 per symbol as the holder starts to see the mode.

`verify_iir_holder.py` (Theorem 10; local Windows machine, python 3.12.2,
numpy 2.5.2), record `verify_iir_holder.json`. Six sources with stable
rational holder filters, hidden and visible poles, real and complex,
built with dyadic coefficients so that hidden modes are hidden exactly
(that choice was made before the first run, after a smoke test of the
case definitions only).

- Lemma 4 with the joint realization holds to 4e-15 in all six; the growth
  rates of Lemma 5 and its floor pass in all six.
- Window cost (A1, A2, A3, A6 at three weights): **still running when
  this version was committed** (started 2026-11-16 21:10 local; the
  window stage is slow on this machine). Finished so far: A1 (hiding
  filter) at alpha = 0, gaps -7.6e-3, -3.8e-3, -1.9e-3, -9.6e-4 bits at
  N = 40, 80, 160, 320, a factor of 7.9 (criterion: 4). The record
  `verify_iir_holder.json` is written at the end of the run and will be
  committed with the appendix sentence updated. The log of the run so
  far is not tracked.

`verify_unit_circle.py` (Theorem 11, Lemma 12; local, 261 s), record
`verify_unit_circle.json`: six scalar sources (random walk with and
without holder, unit pole with a stable pole, poles +-i, unit pole with an
unstable pole, double unit pole). **All 30 checks passed on the first
run.** Window rate and leakage approach the corner with differences that
halve as N doubles (at most 4.1e-4 bits at N = 3200); the log-mean of the
bulk approaches int log f roughly like log N / N; N^{2 r_0} times the
smallest Toeplitz eigenvalue is stable.

`verify_spectral_law.py` (Atlas), record `verify_spectral_law.json` (30 s):

- Phase independence (Corollary 15): over four phases, the spread of rate
  and leakage falls from 1.5e-4 bits at N = 500 to 7e-6 at N = 8000. Pass.
- Moments (Proposition 14): the first six moments match the integral
  formula to 2.4e-4 relative. Pass.
- Rational contrasts, recorded without a criterion: periods of 7 and 3
  samples (the second added after the first run) show no measurable phase
  dependence for this weakly modulated source. The draft gives an exact
  example of phase dependence instead.

`verify_vector_ergodic.py` (Theorem 18, memoryless holder; Atlas): its first
run (record `verify_vector_ergodic.json`) **failed all six checks** on
their absolute tolerances (phase spread at N = 200 of 3.9e-3, 4.9e-3, and
6.5e-3 bits at alpha = 0, 0.5, 1 against 2e-3; frozen-block gap at n = 16 of
1.1e-2 to 1.2e-2 against 5e-3), though the relative parts passed. The
follow-up (`--followup`, record `verify_vector_ergodic_followup.json`,
criteria written before it ran) passed all nine: monotone sequences,
extrapolated limits that agree to 1.6e-5 bits or better, and the phase
spread at N = 400 at 0.23 to 0.25 of that at N = 100 (criterion: at most
one half). The README and the appendix had said "at most a quarter"
until the audit of 2026-11-16 found that the alpha = 0 ratio is 0.2508.

`verify_ergodic_memory.py` (Theorem 18, holder with memory m_h = 1; local,
3 BLAS threads), record `verify_ergodic_memory.json`. Before the run, a
timing test computed W(50) and W(100) at phase 0 and V_4, V_8 at
alpha = 0.5, after the criteria were in the file.

- **All nine checks passed on the first run** (2642 s). V_n (n = 4 to 64,
  interior holder) and the phase mean of W(N) (N = 50 to 400) decrease at
  every weight; the extrapolations agree to 3.4e-5, 1.6e-5, and 3e-7 bits
  at alpha = 0, 0.5, 1; the phase spread at N = 400 is 0.23 of that at
  N = 100. Ignoring the memory (holder H0 alone) raises V_64 from 0.830
  to 0.847 bits at alpha = 0 and leaves it unchanged at alpha = 1, where
  the holder does not enter.
- The window cost W of this script is against all the observations of
  the window (T_0 projected out of the first), while Theorem 18 states
  its window cost against the interior observations; the remark after
  Theorem 18 shows the two have the same limit. The appendix says so.

## Model audit of Theorem 14 (now 18) and Lemma 13 (now 16), 2026-11-16

A fresh-context model, not a human. No false mathematical step. Fixed:

- F1 (gap): the distortion added by the coupling and the code tolerance
  was not taken out of the budget in the upper bound; the budget is now
  D - eps_n - eps_Q - 3 delta, with an intermediate budget D_eta so that
  the limit in the cells is taken at a fixed budget.
- F2 (gap, minor): the set B and its support value are now defined
  exactly, with "at most".
- F3 (error, appendix and README): "at most a quarter" was false at
  alpha = 0 (0.2508); now the recorded ratios.
- F4 to F9 (imprecisions): both directions of the identification of V_n
  with paper two's program, real minimizers; the extension of the block
  lemma to the window program; the slope bound only for large n; cells of
  small diameter; the index range, the phase of a block, the invariant
  measure as a consequence; the introduction's summary of the hypotheses
  and the constants of O(1/n).
- F10 (imprecision): the appendix no longer says the proof predicts
  monotone, halving sequences, and calls the extrapolation of the window
  cost a heuristic.

## Model audits of the new proofs, 2026-11-16 (two fresh-context models, not humans)

**Theorems 10 and 11, Lemma 12.** No false step in the proofs. Every lead
checked came back "holds" (controllability of the unstable modes of the
joint system; the split (3) uniform in N; the small-norm bound
independent of lambda_min of the precision; the noise splitting with a
message that depends on the bridge only; uniform integrability in Lemma
12(d); Szego and weak convergence with an unbounded f). The auditor also
verified realization independence of rho_hid numerically on two
non-minimal realizations. Fixed:

- F1 (error, introduction): "every truncation of a filter that cancels a
  pole sees the pole" is false; counterexample G = (1 - 1.5z)/(1 - 0.5z^2),
  whose odd truncations hide the pole. Now "can see", and the remark
  after Theorem 10 gives the general formula h_L rho^{-L}.
- F2 (error, abstract): the unit-circle sentence now says "observed
  through a scalar gain".
- F3 (gap, Theorem 11 achievability): the tail cut-off now needs
  v_B >= max{2, e theta''}, so that the tail's share is at most gamma'/2;
  the auditor's case with v_B = e theta'' had a 1.05-bit overhead. The
  constants' dependence on (eta, theta'', J, sigma_U) is stated.
- F4 (gap): the water levels theta_N are shown to stay in a compact set.
- F5: the auxiliary noise level is max{t^{1/2}, 1/L'}, positive for
  polynomial filters.
- F6: the converse cites Section II with paper three's Lemma 24 and
  checks D_N < (Q/N) tr Gamma_N.
- F7: Riccati convergence now rests on de Souza, Gevers, Goodwin 1986
  (Theorems 3.2 and 4.1, read at first hand), with a monotonicity
  argument for the singular initial covariance; Anderson-Moore and
  Kailath-Sayed-Hassibi are "see also". This changes the proof of Lemma
  4 as well.
- F8: the appendix reports the IIR check (partial; see above).
- F9: "grow like N^{2 r_0}" is now "at most like", in Section III and V.
- F10, F11: wording (rank rL, the source of the rank 2pd, "unstable
  poles", |rho| > 1, the noise-splitting chain written out) and the
  one-message code for bins at or below the water level.

**Lemmas 16, 17, Theorem 18 (Section IV).** No error; every lead negative;
Lemma 17 checked exactly on 450 random Gaussian instances. Fixed:

- F1 (gap): Lemma 8 is now stated for any holder matrix and groups in
  any position in time, which Theorem 18 needs (it applies Lemma 8 with
  I_l (x) G'_n to runs of blocks in a phase cell).
- F2 (gap): Lemma 17's block step now cites paper one's Proposition 2
  for both codes and test channels.
- F3: the upper bound's rate and leakage carry a third delta for the
  fluctuation of the cell fractions.
- F4: the appendix reports the memory check and says which window cost
  it uses.
- F5 to F8: the joint covariance of (T_-, T); measurability and the level
  scaling in Lemma 16; the step I(M;A|B) <= I(T;A|B) in the remark after
  Theorem 18, which also notes that the region equality follows from
  monotonicity alone; the quadrant convention for R_S(d) at or above
  the maximal distortion; p and r among the constants.

## Earlier model audits and readings

An earlier fresh-context audit of Lemma 13 and Theorem 14 (before the
memory extension) found three gaps, fixed: the averaging over block
offsets; the identification of the region from bounds uniform in the
weight; uniformity in the starting phase. It also checked a scalar case:
the frozen-block error halved with n from 0.0096 at n = 2 to 0.0003 at
n = 64.

Model audit of Sections II and III (fresh context): no error that breaks
a result; three gaps fixed (the closing argument of Theorem 1; what the
leakage of Lemma 8 is measured against; the bound in the remark after
Lemma 8), and many smaller items.

Readings by a reader (pasted into the session, 2026-11-16): the first
found the gap fixed by Lemma 9 (finite quantizer) and pointed to Toms and
Berger; the second asked for denser proofs of Lemmas 4 and 5(c), a
verification appendix, and narrower open problems, all done.

Outside readers' notes on paper four and on the series (pasted into the
session, 2026-11-16 evening). Applied in paper four:

- The abstract and introduction now carry the hypotheses: uniformly
  bounded window covariances for Theorem 13 (the unstable scalar sources
  of paper three show why: a few eigenvalues leave the empirical
  distribution and still cost rate), and continuous finite-range
  correlations and a floor for Theorem 18; the abstract says the whole
  source is reproduced, and Section II says this is narrower than papers
  one to three.
- Prior art: the 2025 bounded-delay paper and the 2026 journal article of
  Tan, Dabora and Poor are cited, with what was read; the April 2026
  seminar slides that restate the conjecture are cited; no priority is
  claimed for the rate of an unstable vector source until Toms and Berger
  is read.
- Lemma 8 is self-contained (the coupling and the choice of seeds are
  written out), Lemma 17 defines chi_b and states the cut bound it uses,
  and Theorem 18 says how a code for l independent copies of a block is
  applied to runs of blocks in a phase cell.
- "Closed form" is replaced by "reverse water-filling on the limiting
  eigenvalue distribution" where that measure is known only through its
  moments, and "learns nothing about the growth" by the precise statement
  (its entropy about the state still grows at rho_star per symbol).
- The introduction opens with the two questions (which unstable modes
  cost leakage; whether incommensurate sampling removes the phase), and
  the connection to papers one to three follows.
- Appendix A keeps the distinctions (window costs versus coding theorems;
  the proved O(1/n) versus the unclaimed window rate) and states each
  failed criterion in one sentence; the run histories are here.

Applied to paper three on the separate branch
`paper/beyond-stationary-identity` (worktree
`C:\source\worktrees\geometric-observation-p3-identity`): a sharper
identity around the covariance-mixture inequality, and a paragraph in
its Open Problems on what paper four treats. Held, on the owner's
instruction: paper one (under review).

## Open items

- [ ] Read Toms and Berger 1971 in full (two pages; needs library access),
      and Toms's thesis; until then no priority claim for the rate part.
- [ ] Read the 2026 IEEE Trans. Commun. paper of Tan, Dabora and Poor in
      full, to see whether it addresses the conjecture Corollary 15 proves.
- [x] Holders with infinite memory: stable rational filters (Theorem 10).
- [ ] Filters with infinite memory that are not rational (Section V).
- [x] Vector sources under fast variation, holder of finite memory
      (Theorem 18).
- [ ] Fast variation with holders of infinite memory, without the floor,
      and closed forms for vector sources.
- [x] Poles on the unit circle, scalar source and scalar holder gain
      (Theorem 11).
- [ ] Poles on the unit circle for vector sources or holders with memory.
- [ ] Decide on the non-Gaussian part.
- [ ] Verify the references marked in the source.
- [ ] A human reading of every proof.

## Build

`pdflatex tit-unstable-ergodic.tex` three times.
