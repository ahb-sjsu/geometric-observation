# Paper four (working name `tit-unstable-ergodic`)

Fourth paper in the rate-leakage-distortion series, after
`paper/tit-rate-leakage` (one), `paper/tit-stationary` (two) and
`paper/tit-beyond-stationary` (three). It takes up open problems listed at
the end of paper three.

**Status (2026-11-16): working draft, started this day, 13 pages. Not
submitted, no venue chosen.** The folder name and the title are
provisional; title, venue and authorship are the owner's decisions. No
human has read any of it. Two readings by a reader (pasted into the
session) are recorded below; the second rated it short of final for
density, two compressed proofs, a missing appendix, and the open
problems. All four are addressed in this version except the remaining
open problems, which are listed.

## Scope

The paper treats two of paper three's open problems in full. The third
topic named for this paper, non-Gaussian linear processes with infinite
dependence, is not drafted; whether it goes here or into a later paper is
open (recommendation recorded 2026-11-16: decide after reading its prior
art).

| Result | Statement | Main tools |
|---|---|---|
| Theorem 1 | Vector autoregressive source with unstable poles; holder observing a linear filter of finite memory of the source in white noise. The region is the stationary spectral region of paper two for f = Phi^{-1} Sigma Phi^{-*} and the same holder, moved by rho_star (sum of log modulus over all unstable poles) in rate and by rho_hid (the same sum over the unstable poles hidden from the holder: Kalman-unobservable, i.e. cancelled by the holder's filter) in leakage. The window cost converges to the shifted spectral cost. | Lemmas 2 to 9 |
| Lemma 2 | The inverse covariance of a window is block Toeplitz minus a term on the last d blocks: the window is a stationary bridge plus its final state | Full convolution matrix |
| Lemma 3 | Group covariances of the bridge interior are within a geometrically small term of a stationary window | Matrix Fejer-Riesz, banded precision of a stationary autoregression |
| Lemma 4 | The holder's Kalman innovation covariance has log det = integral of log det(Sigma_U + G f G^*) + 2 (rho_star - rho_hid); proof written out (Riccati to factorization, determinant, Jensen) | Kalman decomposition, Riccati convergence |
| Lemma 5 | The final state's covariance grows at rho_star, its covariance given the holder at rho_hid; explicit N-independent lower bounds | Lemmas 2 and 4, circulant log-determinants |
| Lemma 6 | Low-rank changes of the precision and of the holder's information matrix change the window cost by a computable constant plus O(log N) | Feasible sets in the precision variable |
| Lemma 7 | The block circulant window cost tends to the spectral cost | Shift invariance, convexity, paper two's Lemma 2 |
| Lemma 8 | Paper three's Lemma 12 for a holder of finite memory (drop each group's first m observations) | Paper three's Lemmas 11 and 12 |
| Lemma 9 | Finite clipped quantizer for the final state: log alphabet size, conditional entropy, and error together | Gaussian tails, a lattice entropy bound |
| Theorem 10 | Scalar source whose window covariances have a limiting eigenvalue distribution mu, scalar holder in white noise: the region is one quadrant, reverse water-filling on mu | Paper three's Lemma 24 and Theorem 26 |
| Proposition 11 | Sources driven by a uniquely ergodic homeomorphism with continuous, finite-range correlations have a limiting eigenvalue distribution, the same for every starting point | Moments, Oxtoby's uniform ergodic theorem |
| Corollary 12 | Cyclostationary process sampled at an incommensurate rate: the limit exists, does not depend on the sampling phase, and is given in closed form, with the leakage. This proves the conjecture of Tan, Dabora and Poor (ISIT 2024, arXiv 2405.11405, Remark 1) | Theorem 10, Proposition 11 |
| Lemma 13 | The frozen-block program V_n over a phase law: convex and continuous in the distortion, continuous under weak convergence, convex in the law (by duality), Lipschitz in the weight | Paper two's Lemma 2 |
| Theorem 14 | Vector source driven by a totally uniquely ergodic map, finite-range correlations, a white floor, memoryless matrix holder: the region is given by the limit of the frozen-block programs, error O(1/n), the same for every starting phase; the window cost converges to it uniformly in the phase. Added after pull request 26 was opened; not in it. | Paper three's Lemmas 10 and 12, paper one's Theorem 3, Oxtoby |

Imports from paper two: codes for stationary sources with a holder filter
(Theorems 16 and 22), continuity of the spectral program in the measure
(Lemma 2), and the order inequality at each frequency (Lemma 11(b)). The
last is applied per frequency with the holder's response; verify that
reading against paper two before submission.

## Prior art (sweep of 2026-11-16, by a model; read the cited items before relying on it)

- Scalar unstable autoregressive rate-distortion: Gray 1970, Hashimoto and
  Arimoto 1980, Gray and Hashimoto 2008. Vector case: only a sketch and an
  upper bound in Sahai and Mitter (arXiv cs/0610143). Gutierrez-Gutierrez
  et al. 2018 cover asymptotically WSS vector sources, which excludes
  unstable poles.
- Gutierrez-Gutierrez et al., Probl. Inf. Transm. 60(1), 2024: its Theorem 4
  assumes companion spectral radius below one, which excludes unstable
  poles (reported by a reader with access; not read here).
- Toms and Berger 1971 (IEEE Trans. Inf. Theory 17(1):113-114, DOI
  10.1109/TIT.1971.1054569): only the abstract was found. Rate-distortion
  function of linear finite-memory Gaussian dynamic systems; at small
  distortions it equals that of the driving noise. The draft notes the
  agreement at small distortion and that its scope is unknown.
- No leakage or equivocation result for unstable sources was found.
- Lemma 4 is a discrete-time relative of Braslavsky et al. 1999 (continuous
  time). The discrete identity was not found stated; it is derived, not
  claimed as new.
- Sampled cyclostationary sources: Abakasanga, Shlezinger and Dabora 2020
  (memoryless samples, small distortion, a limit superior); Tan, Dabora and
  Poor 2024 (memory; an average over the phase of limits superior; phase
  independence conjectured). Their arXiv 2405.11405v2 was read, pages 1 to
  6 (Theorem 1, Corollary 1, Remark 1). A 2026 IEEE Trans. Commun. paper by
  the same group (timing jitter) was seen only as an abstract.

## Committed checks (Appendix A)

Both run on the Atlas workstation, 2026-11-16, numpy 2.4.4.

`verify_unstable_vector.py`, record `verify_unstable_vector.json` (515 s),
twelve sources. Its pass criteria were written after exploratory probes of
the same computations, so they record agreement rather than test a fixed
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
  cost changes by at most 2e-8 bits between M = 1e5 and 1e7, so the values
  are settled far below the gaps. After the run only the docstring and the
  follow-up function of the script changed.
- The twelfth source, built in double precision with a mode hidden only to
  6e-17, shows the discontinuity of rho_hid: its posterior growth falls from
  0.44 to 0.10 per symbol as the holder starts to see the mode.

`verify_spectral_law.py`, record `verify_spectral_law.json` (30 s): pass
criteria fixed before the first run.

- Phase independence (Corollary 12): over four phases, the spread of rate
  and leakage falls from 1.5e-4 bits at N = 500 to 7e-6 at N = 8000. Pass.
- Moments (Proposition 11): the first six moments match the integral
  formula to 2.4e-4 relative. Pass.
- Rational contrasts, recorded without a criterion: periods of 7 and 3
  samples (the second added after the first run) show no measurable phase
  dependence for this weakly modulated source. The draft gives an exact
  example of phase dependence instead.

## Vector sources under fast variation (added after pull request 26)

Theorem 14 and Lemma 13 close the open problem on vector sources under fast
variation for a memoryless holder, with a floor on the covariances.

- Check `verify_vector_ergodic.py`: its first run, with criteria fixed before
  it (record `verify_vector_ergodic.json`), **failed all six checks**: the
  absolute tolerances (phase spread 2e-3 bits at N = 200; frozen-block gap
  5e-3 at n = 16) were too tight for those sizes, though the relative parts
  passed and both sequences decreased with halving differences. A follow-up
  (`--followup`, record `verify_vector_ergodic_followup.json`, criteria written
  before it ran) passed all nine: monotone sequences, extrapolated limits that
  agree to 1.6e-5 bits or better, and the phase spread at N = 400 at most a
  quarter of that at N = 100.
- A fresh-context model audit of Lemma 13 and Theorem 14 found no error that
  breaks a result and three gaps, fixed: the averaging over block offsets
  with budgets and weights that depend on the offset (monotonicity and
  nonnegativity before the convexity in the law); the identification of the
  region from bounds uniform in the weight, without assuming convexity of the
  achievable set (Lemma 13(d) gives the Lipschitz constant); and uniformity in
  the starting phase (an argument by contradiction, and the sandwich for cell
  indicators). Also fixed: the maximal distortion of a non-invariant phase law,
  the equality of the frozen program with paper two's program, the slope
  bound, the leftover symbols, and the closing paragraph's wording (no closed
  form is known, rather than none exists).
- The audit also checked a scalar case numerically: the frozen-block error
  halved with n from 0.0096 at n = 2 to 0.0003 at n = 64, and two phases agreed
  to 5e-6.

## Readings by a reader (pasted into the session, 2026-11-16)

First reading:
- Found a gap in the achievability of Theorem 1: rate is the log of a
  finite message set, but the final state was quantized on an unbounded
  lattice and only its entropy was bounded. Fixed by Lemma 9 (clipped
  quantizer).
- Reported the scope of Gutierrez-Gutierrez et al. 2024 and pointed to
  Toms and Berger 1971. Related work updated.
- Independent checks by the reader, not reproduced here: Lemma 4 on
  nonnormal three-dimensional examples, agreement within 5.3e-14 bits; a
  quasiperiodic moving-average example with shrinking phase differences.

Second reading (what keeps it from final):
- Density: Lemma 5(c) and Lemma 4 too compressed. Lemma 5(c) now states
  explicit constants independent of N and says which covariances are not
  bounded above; Lemma 4 now derives the factorization from the Riccati
  equation, the determinant, and Jensen's formula, with citations.
- No verification appendix: Appendix A added, with the two scripts above.
- Open problems narrowed, not closed: the first one (holders with memory)
  is now closed for finite memory by restructuring Section III (Lemmas 6
  to 8); the window-cost limit no longer imports paper two's memoryless
  window theorem or Szegő's theorem.

## Model audit of Sections II and III (2026-11-16, fresh-context model, not a human)

No error that breaks a result. It also re-derived Lemmas 2 to 5 numerically
on six examples of its own (agreement to 1e-16 for Lemma 2, to six decimals
for Lemma 4, to four for the growth slopes of Lemma 5) and confirmed the
block-Toeplitz orientation. Three gaps, all fixed:

- B1, closing argument of Theorem 1: the four steps from the codes for
  f - eta I to the inclusion are now written (choice of D'' via the uniform
  slope bound, the direction of (iii), the check D' < D_max of f - eta I,
  and the half-plane description).
- B2, Lemma 8: now says what the leakage is measured against (any
  observation containing G'(group j) + independent white noise for each
  group), and names the third use of the holder in paper three's proof
  (the joint law under which L' was measured).
- B3, remark after Lemma 8: the bound I(M; A | B) <= (rm/2) log(1 + kappa_0)
  is written out, with kappa_0 defined and bounded by Jbar M_f.

Smaller items, all fixed: the reduction from codes to test channels in
Section II; (i) now cites paper two's Theorem 20 for a finite filter (the
numbering 15, 16, 20, 22 was checked by counting environments); (iii) now
has its own two-line proof at each frequency instead of a reading of paper
two's Lemma 11; Lemma 6's proof now gets the stated constant through the
one-sided structure of the two steps; the window-cost display is stated
for every D > 0; the introduction claims o(N), not O(log N); Lemma 5's
note on unbounded covariances is conditioned on positive rates; the scalar
remark allows a singular A_d; the impulse-response bound uses (1 + j); the
dependence of L_eta on n_0; the quantizer width is fixed; the projection
step is written out; the formal spectral density is flagged; and the worst
notation collisions are renamed (c_W and varrho in Lemma 3, the function
sf c, rank bar k, Xi_N, sf q_N, sf w, sf g, bar rho, k_N, zeta).

## Open items

- [ ] Read Toms and Berger 1971 in full (two pages; needs library access).
- [ ] Holders with infinite memory (stable rational filters), by truncation
      as in paper two's Theorem 22.
- [x] Vector sources under fast variation, memoryless holder (Theorem 14).
- [ ] Holders with memory, and closed forms for vector sources, under fast variation.
- [ ] Poles on the unit circle: the bridge is then a Brownian bridge of growing variance, so Theorem 1's proof does not apply; the draft states the conjecture of no shift.
- [ ] Decide on the non-Gaussian part.
- [ ] Verify the references marked in the source, and the reading of
      paper two's Lemma 11(b) per frequency.
- [ ] A fresh-context audit of the restructured proofs, then a human
      reading.

## Build

`pdflatex tit-unstable-ergodic.tex` three times.
