# Rate, Leakage, and Distortion Beyond Stationary Gaussian Sources

Third paper of the series. Paper one (`../tit-rate-leakage/`) treats a
Gaussian vector source, paper two (`../tit-stationary/`) a stationary
Gaussian process. This draft treats Gaussian sources that are not
stationary and sources that are not Gaussian.

**Status (2026-11-16): draft, not submitted, no venue chosen.** The
manuscript cites the tag `tit-beyond-stationary-1.3`
(https://github.com/ahb-sjsu/geometric-observation/tree/tit-beyond-stationary-1.3/paper/tit-beyond-stationary),
cut on the merge commit of the change that set this citation. Tag
`tit-beyond-stationary-1.2` has the same manuscript, Section IX
(unstable autoregressive sources) included, except that it cites
itself; its notebook does not run the Section IX checks. Tag
`tit-beyond-stationary-1.1` is the previous version, without Section IX. Title,
venue and authorship are the owner's decisions. No human has read the
proofs. The four referee passes recorded below were made by models.

**Changed after tag 1.3 (2026-11-16, branch `paper/beyond-stationary-identity`),
on an outside reviewer's notes on the series.** Text only; no statement,
proof, script, or record changed, and the appendix still cites tag 1.3
for the scripts, which are unchanged. (1) The introduction opens with
what the paper is about: one inequality, the covariance-mixture
inequality of Corollary 6, proved through the bound for sources that are
not Gaussian (Theorem 2), is also what shows that averaging a spectrum
over time or over a cycle never lowers the cost (Corollary 16, Theorem
22); so both branches say that the model that forgets structure is
conservative, and the rest of the paper measures by how much. The old
paragraph "The two halves of the paper meet in one place" is shortened
to a pointer. The abstract ends with the same inequality and drops the
sentence on time averaging that it subsumes (254 words). (2) The Open
Problems section opens with a paragraph on what the companion paper four
(`../tit-unstable-ergodic/`, cited as a manuscript in preparation, by
directory, since it has no tag) treats, and each affected problem says
what is treated there and what remains open. A tag 1.4 would fix this
text; none is cut.

## Why it is a separate paper

Paper two's proofs use stationarity at every step (Fourier
diagonalization, subadditivity of window costs, embedding in periodic
sources, a Gaussian split into finite memory plus remainder). None of
that is available here. The draft uses two other tools: a comparison of a
long Gaussian vector with its blocks (Lemmas 10 to 12), and
maximum-entropy bounds for the two costs together (Theorems 2 and 3).

## What the draft proves

| Result | Statement | Rests on |
|---|---|---|
| **Theorem 13** | **Locally stationary Gaussian source: the region is water-filling over the time-frequency plane under one level, with deterministic encoders** | Lemmas 10, 11, 12; paper two's Lemma 2, Lemma 11, Theorems 15, 16 |
| Lemma 10 | Costs of a Gaussian vector are superadditive over blocks, up to the information between blocks | Paper one's Proposition 2 |
| Lemma 11 | A code for a smaller covariance serves a larger one through a coupling | The coupling inside paper two's Theorem 16 |
| Lemma 12 | The coupling's randomness can be removed when one code is repeated on many blocks with nearly the same law | Chebyshev over independent seeds |
| Proposition 14 | Converse with a rate: for Lipschitz covariances no code falls more than a constant times N^(-1/2) below the frontier | Three elementary facts about the program |
| Proposition 15 | A time-varying moving average with a white floor is locally stationary | Direct estimate |
| Corollary 16 | The stationary source with the time-averaged spectrum has a region no larger | Corollary 6 |
| Corollary 17 | A source that becomes stationary has the spectral region of its limit, with deterministic encoders | Lemmas 10, 12 |
| Theorem 18 | Cyclostationary Gaussian process: the region is the spectral region of the process stacked over one period | Paper two's Theorems 15, 22, 23 |
| Proposition 19 | Harmonic form: frequencies couple within cosets of the cycle frequency | Direct computation |
| Corollary 20 | For a stationary source the stacked region is paper two's region | Theorem 18 |
| Theorem 22 | The stationary source with the phase-averaged spectrum has a region no larger (time-invariant parties) | Corollary 6 |
| Proposition 23 | Independent stationary regimes share one water level | Lemma 10, paper two's Theorem 15 |
| **Theorem 26** | **Unstable scalar autoregressive source: the region is the spectral region of the reflected stationary source moved by the sum of log moduli of the unstable poles in rate, and in leakage only when the holder does not observe the source; deterministic encoders** | Lemmas 24, 25, 12; paper two's Lemma 2 and Theorem 16 |
| Lemma 24 | For a scalar source with a scalar holder gain and white noise, the vector cost separates over the eigenvalues of the covariance, and one allocation, delta = min(lambda, theta), is optimal at every weight, so the region is a single quadrant | Courant-Fischer, an exchange argument |
| Lemma 25 | The window covariance of an unstable AR source has at most d exceptional eigenvalues, whose log-sum is 2N times the instability rate (not all of them need grow), and a bulk with the law of the reflected spectrum | Rank-d interlacing, Szego, Jensen's formula |
| Corollary 27 | In the setting of Theorem 26 the region is the quadrant above (instability rate + r_f(D), instability rate x [H=0] + l_f(D)), with r_f the rate-distortion function by reverse water-filling; there is no rate-leakage trade-off in this scalar model | Lemma 24 |
| Proposition 1 | Coding theorem for any memoryless pair with finite second moments and finite I(T;S) | Proof of paper one's Theorem 3 |
| Theorem 2 | The Gaussian region with the same second moments is achievable for a source that is not Gaussian | Gaussian test channel on the source as it is |
| Theorem 3 | Every code is bounded below by the Gaussian frontier less two relative entropies | Maximum entropy, concavity of the linear-estimation error |
| Theorem 5 | The lower bound of Theorem 3 is asymptotically tight as the distortion tends to zero, when the whole source is reproduced. The Gaussian upper bound is not attained. | Lemma 4 |
| Corollary 6 | Mixing: the Gaussian cost of an averaged covariance is at least the cost of the mixture | Theorem 2 applied to a Gaussian mixture |
| Theorem 7 | Lower bound for stationary processes that are not Gaussian, with the relative entropy rate | Theorem 3 on windows, paper two's Theorem 15 |
| Theorem 8 | The spectral region is achievable for processes of finite dependence | Theorem 2, guard intervals |

Theorem numbers are those printed by the build of 2026-11-16. Check them
against the PDF before quoting. At the weight that counts only the rate,
Theorem 13 gives the rate-distortion function of a locally stationary
Gaussian vector source; the search below did not find that statement for
this class.

## What it does not prove

- Theorem 13 is for a time-invariant weight and holder, with a memoryless
  holder map and white noise. Slowly varying parties are not covered.
- Conditions (L1) to (L3) describe a stable source that varies slowly.
  Sources that vary fast without a period are not covered. Unstable
  sources are covered only for a scalar autoregressive source with a
  scalar holder gain in white noise (Theorem 26); unstable vector sources,
  holders with memory, poles on the unit circle, and unstable sources
  whose spectrum varies in time are not.
- Theorem 26's rate term is classical (Gray 1970; Hashimoto and Arimoto
  1980; Gray and Hashimoto 2008; Tian and Kostina for coding theorems in
  the first-order case). What is new is the leakage.
- The achievability of Theorem 13 has no rate in the blocklength (none is
  known for stationary sources either). Proposition 14 gives a rate for
  the converse only, and the computed examples suggest it is not the true
  order.
- The upper bound for processes that are not Gaussian and have infinite
  dependence.
- Tightness of the non-Gaussian lower bound at any positive distortion,
  or its limit when the decoder's weight is singular.
- A lower bound when the holder's noise is not additive.

## Files

| File | What it is |
|---|---|
| `tit-beyond-stationary.tex`, `.pdf` | The draft, 28 pages |
| `example_ls.py`, `example_ls.json`, `fig_ls.pdf`, `fig_ls.png` | The worked example after Proposition 15 and its figure (needs matplotlib) |
| `verify_nongauss.py`, `.json` | Seven checks of Section III on a Gaussian-mixture source (about one minute) |
| `verify_ls.py`, `.json` | Seven checks of Sections V and VI on a time-varying moving average (about ten minutes) |
| `build_notebook.py`, `reproduce.ipynb`, `reproduce-executed-2026-11-16.ipynb` | The notebook that reruns everything, and one executed copy |
| `lean-beyond-2026-11-16.txt`, `lean-library-2026-11-16.txt` | Lean build records and axiom audit |
| `verify_cyclo.py`, `.json` | Seven checks of Sections VII and VIII on periodic moving averages (about eleven minutes) |
| `verify_unstable.py`, `.json` | Checks of Section IX on four unstable AR sources: eigenvalue split, log-sum of the growing eigenvalues, bulk law, window cost against the theorem's limit, the common optimizer of Lemma 24 and Corollary 27, and a high-precision check of the determinant identity (about twenty seconds; needs scipy and mpmath) |

The scripts import `spectral_core.py` and `verify_spectral.py` from
`../tit-stationary/`. Run them from this folder. numpy only (numpy 2.5.2,
Python 3.12.2 on 2026-11-15). On 2026-11-15 `verify_nongauss.py` and `verify_cyclo.py` passed 7 of 7, and `verify_ls.py` passed 7 of 7 after one pass criterion was changed: the first run failed a fixed threshold on the local-closeness distance that had been set too tight, and the criterion now asks for what (L2) says, that the distance shrink in proportion to the block length. The measured distances did not change.

On 2026-11-16 `verify_unstable.py` passed every check, run on the Atlas workstation (numpy 2.4.4, scipy, mpmath). Its first full run failed on the two sources with poles of different moduli, for a numerical reason: it took the growing eigenvalues from the covariance in double precision, which cannot resolve two eigenvalues that grow at different rates (at N = 320 their ratio is about 10^43). It now takes their log-sum from det(Gamma_N) = sigma^(2N), the identity the proof uses, and checks that identity against an 80-digit computation. Its pass criteria were also changed after that first run had been seen, from fixed tolerances to the rate the proofs predict (N times the error must not grow from N = 40 to N = 320). One failure of the first run, the bulk-law check on the complex-pole source, came from a bug in the check: it averaged the bulk eigenvalues over N instead of N - d. With the average over N - d the error is 0.016 at N = 320 and halves with each doubling of N. The recorded errors are in `verify_unstable.json`. A later check, `common_optimizer`, was added with its tolerance (10^-6 bits) written before it ran; the largest difference was 4e-16 bits. `reproduce.ipynb` runs it as Section 5.

Build: `pdflatex tit-beyond-stationary.tex` three times.

**Notebook.** `build_notebook.py` writes `reproduce.ipynb`, which reruns
the four check scripts and the example and prints the numbers of the
appendix and of Section IX. `reproduce-executed-2026-11-16.ipynb` is one
executed copy, run on the Atlas workstation (Linux, Python 3.12.3,
numpy 2.4.6) in thirty-two minutes; all 45 entries pass (7, 7, 8 and 23).
It replaces an earlier executed copy of the same day, run on Windows,
which did not include Section IX. A first run on Atlas also passed every
entry; it was repeated only so that the printed lists show plain numbers.
Executing the notebook needs nbformat, nbclient and ipykernel besides the
packages the scripts use.

**Lean.** `lean/ObservationTheory/BeyondStationary.lean` has fifteen
theorems, no `sorry`, standard axioms only. It checks algebraic steps:
the scalar inequality of Lemma 9, the covariance identities of the
explicit-seed draw (matrices), the determinant identity of Theorem 2
(matrices) and its evaluations in one direction, the scalar bound on a
linear estimate's error, the scaling of the point cost behind facts (F1)
to (F3), and the arithmetic of Lemma 12. The matrix concavity used in
Theorem 3 is in `LogDet.lean`, paper one's module. **Not formalized:**
every coding theorem, every statement about entropy or mutual
information, the limit arguments, Lemma 10, the probabilistic step of
Lemma 12, and the harmonic identity of Proposition 19. Build records:
`lean-beyond-2026-11-16.txt` (module and axiom audit) and
`lean-library-2026-11-16.txt` (the whole library with the new import).
Both builds ran on the Atlas workstation; CI does not build Lean.

## Referee passes (models, 2026-11-15)

Four independent passes, each told to find errors and given the
companion papers to check imported results against. None was a human.

| Pass | Scope | Outcome |
|---|---|---|
| A | Sections II to IV (non-Gaussian) | No error. Four gaps, six minor points. All fixed: hypotheses of the moving-average example, the entropy-rate limit may be infinite, deterministic encoders in Theorem 8, a Markov chain stated in Theorem 3. |
| B | Cyclostationary and regimes sections | No error. Four gaps, five minor points. All fixed: Theorem 18(b) for blocklengths that are not multiples of the period, convexity of the achievable set in Proposition 23, the stacked hypotheses in Corollary 20. |
| C | Lemmas 9 to 11, the main theorem and its corollaries | One false sentence (which stationary processes satisfy the definition), one unproved remark (softened), nine minor points. All fixed. The pass also found that the constant in Lemma 10 does not depend on the holder. |
| D | Lemma 12, the deterministic achievability of Theorem 13, Proposition 14 | No error in the mathematics. Two small gaps and seven wording points, all fixed: a misleading sentence in the introduction about the rate, the order in which the proof's parameters are chosen, the definition of the program for fields that are not continuous. |

Passes A and B were made before Sections V and VI existed, and before
the fixes from passes C and D. No pass has read the final text end to end.

An outside reader's comments of 2026-11-15 were then applied: the
abstract and introduction no longer say the two non-Gaussian bounds
"meet" (only the lower bound is tight at high resolution); the scope of
the main theorem is stated in the abstract, the introduction and the theorem;
the subsection on the phase-averaged spectrum says at its start that it
compares two Gaussian models and not the penalty of not knowing the
phase; and a worked example with a figure follows Proposition 15.

## Prior art (searched 2026-11-15)

The search used general web search, arXiv pages and index records. IEEE
Xplore, Google Scholar and DBLP were not queried directly, and no
forward-citation pass was made. A negative result below means "not
found", not "does not exist".

**Known, and cited in the draft**

- Rate-distortion function of cyclostationary Gaussian processes by
  stacking: Kipnis, Goldsmith, Eldar, IEEE Trans. Inf. Theory 2018
  (arXiv:1505.05586, content read; volume and pages from a snippet).
  Sampled cyclostationary processes: Abakasanga, Shlezinger, Dabora,
  Entropy 2020 (arXiv:2003.00262). Not cited: Tan, Dabora, Poor,
  arXiv:2405.11405 (ISIT 2024), the case with memory.
- Rate-distortion function of asymptotically stationary Gaussian vector
  processes: Gutiérrez-Gutiérrez, Zárraga-Rodríguez, Crespo, Insausti,
  Entropy 20(9):719, 2018 (read on PubMed Central).
- Water-filling in the time-frequency plane for the rate-distortion
  function of a class of nonstationary sources in continuous time:
  Hammerich, IEEE Trans. Inf. Theory 2016 (arXiv:1509.05668). **This is
  the closest prior result to Theorem 13 at the rate-only weight. Only
  its abstract was read. Read the paper before claiming the
  rate-distortion statement as new.**
- Variance in the upper bound, entropy power in the lower: Shannon lower
  bound; Lapidoth 1997; Linder and Zamir 1994; Koch 2016; Gastpar and
  Sula 2024 (conditional and Wyner-Ziv coding, arXiv:2409.14822);
  Shomorony, Avestimehr, Asnani, Weissman 2012 (distributed coding).

**Not found**

- Any bound of either kind for the pair of rate and leakage with a source
  that is not Gaussian.
- Any result with a second party (secrecy, leakage, equivocation, side
  information) for cyclostationary, asymptotically stationary or locally
  stationary sources.
- A rate-distortion theorem for locally stationary processes in the sense
  of Dahlhaus in discrete time, even without a second party.

**Named by a reviewer, not found**

- Velloso and Santos Filho, "Time-Frequency Waterfilling for the
  Nonstationary Gaussian CEO Problem", said to be at ISIT 2026. Two web
  searches on 2026-11-15, one of them extended, did not find a record of
  it, so it is not cited and nothing in the draft is compared with it.
  The owner should locate it (the reviewer reports having seen its
  record and abstract) and compare its local reduction and regularity
  assumptions with (L1) to (L3) before submission.

**Worth reading before submission, not yet read in full**

- Hammerich 2016 (above), and Dahlhaus 1996, whose full text was not
  opened.
- Fang and Zhu, arXiv:2008.04893 and arXiv:2011.00718: leakage of
  additive privacy masks for streaming data; the abstract mentions
  non-stationary cases. Not a source coding theorem as far as the
  abstract shows.
- Courtade, "A strong entropy power inequality", IEEE Trans. Inf. Theory
  2018 (arXiv:1602.03033): its conditional entropy power inequality gives
  another route to a lower bound on the leakage for Gaussian holder
  noise. Theorem 3 of the draft does not use it.
- Eswaran and Gastpar, "Remote source coding under Gaussian noise", IEEE
  Trans. Inf. Theory 2019 (arXiv:1805.06515).

**References marked `% verify` in the bibliography.** Ten entries carry a
mark saying what was and was not checked. Gladyshev 1961 is cited from
memory. The chapter of Gray's book that states the lower semicontinuity
of relative entropy was not looked up.

## Open items before submission

- [ ] A human reads the proofs, Lemmas 10 to 12 and Theorem 13 first.
- [ ] A human reads Section IX (Lemmas 24, 25, Theorem 26 and Corollary 27), new on 2026-11-16.
- [x] Model audit of Theorems 13 and 26 and their lemmas (2026-11-16, a fresh-context model, not a human): no error that breaks a result; two gaps (the duality step of Corollary 27, and the converse's uniformity as the distortion tends to zero, now scoped in Section VI) and six imprecisions (zero codes beyond the maximal distortion, the grid bound on v_B, a repeated-eigenvalue case in Lemma 25(b), uniform mass on the circles, monotonicity in the achievability of Theorem 13, the setting and symbols of Section IX), all fixed. It checked the companion-paper citations against the local copies of papers one and two, not against their tagged versions.
- [ ] Verify the published venue of Tian and Kostina (cited by arXiv number), and read Gray 1970 and Hashimoto-Arimoto 1980 to confirm the form of the rate term quoted after Theorem 26.
- [ ] Read Hammerich 2016 and Dahlhaus 1996 in full, and locate the
      Velloso and Santos Filho paper named above.
- [ ] Forward-citation pass on Kipnis 2018, Gutiérrez-Gutiérrez 2018,
      Hammerich 2016, Gastpar and Sula 2024.
- [ ] Verify the ten marked references against publisher records.
- [ ] One more referee pass on the final text end to end.
- [ ] Paper two is cited by its repository tag, and by theorem number.
      Replace the tag with the journal or arXiv reference when there is
      one, and update the numbers if paper one or two is revised.
- [ ] Running head: the draft has only the short title. Set the journal
      name once a venue is chosen.
- [ ] `verify_cyclo.py` takes about eleven minutes. Shorten it or add a
      notebook with recorded output.
