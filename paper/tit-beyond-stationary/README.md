# Rate, Leakage, and Distortion Beyond Stationary Gaussian Sources

Third paper of the series. Paper one (`../tit-rate-leakage/`) treats a
Gaussian vector source, paper two (`../tit-stationary/`) a stationary
Gaussian process. This draft treats Gaussian sources that are not
stationary and sources that are not Gaussian.

**Status (2026-11-15): draft, not submitted, no venue chosen.** Title,
venue and authorship are the owner's decisions. No human has read the
proofs. The three referee passes recorded below were made by models.

## Why it is a separate paper

Paper two's proofs use stationarity at every step (Fourier
diagonalization, subadditivity of window costs, embedding in periodic
sources, a Gaussian split into finite memory plus remainder). None of
that is available here. The draft uses two other tools: a comparison of a
long Gaussian vector with its blocks (Lemmas 10 and 11), and
maximum-entropy bounds for the two costs together (Theorems 2 and 3).

## What the draft proves

| Result | Statement | Rests on |
|---|---|---|
| **Theorem 12** | **Locally stationary Gaussian source: the region is water-filling over the time-frequency plane under one level** | Lemmas 10, 11; paper two's Lemma 2, Lemma 11, Theorems 15, 16 |
| Lemma 10 | Costs of a Gaussian vector are superadditive over blocks, up to the information between blocks | Paper one's Proposition 2 |
| Lemma 11 | A code for a smaller covariance serves a larger one through a coupling | The coupling inside paper two's Theorem 16 |
| Proposition 13 | A time-varying moving average with a white floor is locally stationary | Direct estimate |
| Corollary 14 | The stationary source with the time-averaged spectrum has a region no larger | Corollary 6 |
| Corollary 15 | A source that becomes stationary has the spectral region of its limit | Lemmas 10, 11 |
| Theorem 16 | Cyclostationary Gaussian process: the region is the spectral region of the process stacked over one period | Paper two's Theorems 15, 22, 23 |
| Proposition 17 | Harmonic form: frequencies couple within cosets of the cycle frequency | Direct computation |
| Corollary 18 | For a stationary source the stacked region is paper two's region | Theorem 16 |
| Theorem 20 | The stationary source with the phase-averaged spectrum has a region no larger (time-invariant parties) | Corollary 6 |
| Proposition 21 | Independent stationary regimes share one water level | Lemma 10, paper two's Theorem 15 |
| Proposition 1 | Coding theorem for any memoryless pair with finite second moments and finite I(T;S) | Proof of paper one's Theorem 3 |
| Theorem 2 | The Gaussian region with the same second moments is achievable for a source that is not Gaussian | Gaussian test channel on the source as it is |
| Theorem 3 | Every code is bounded below by the Gaussian frontier less two relative entropies | Maximum entropy, concavity of the linear-estimation error |
| Theorem 5 | The lower bound of Theorem 3 is asymptotically tight as the distortion tends to zero, when the whole source is reproduced. The Gaussian upper bound is not attained. | Lemma 4 |
| Corollary 6 | Mixing: the Gaussian cost of an averaged covariance is at least the cost of the mixture | Theorem 2 applied to a Gaussian mixture |
| Theorem 7 | Lower bound for stationary processes that are not Gaussian, with the relative entropy rate | Theorem 3 on windows, paper two's Theorem 15 |
| Theorem 8 | The spectral region is achievable for processes of finite dependence | Theorem 2, guard intervals |

Theorem numbers are those printed by the build of 2026-11-15. Check them
against the PDF before quoting. At the weight that counts only the rate,
Theorem 12 gives the rate-distortion function of a locally stationary
Gaussian vector source; the search below did not find that statement for
this class.

## What it does not prove

- Theorem 12 and Corollary 15 need private randomness at the encoder.
  Whether deterministic encoders suffice is open.
- Theorem 12 is for a time-invariant weight and holder, with a memoryless
  holder map and white noise. Slowly varying parties are not covered.
- No rate of convergence in the blocklength for Theorem 12.
- Sources that vary fast without a period, and unstable sources.
- The upper bound for processes that are not Gaussian and have infinite
  dependence.
- Tightness of the non-Gaussian lower bound at any positive distortion,
  or its limit when the decoder's weight is singular.
- A lower bound when the holder's noise is not additive.

## Files

| File | What it is |
|---|---|
| `tit-beyond-stationary.tex`, `.pdf` | The draft, 20 pages |
| `example_ls.py`, `example_ls.json`, `fig_ls.pdf`, `fig_ls.png` | The worked example after Proposition 13 and its figure (needs matplotlib) |
| `verify_nongauss.py`, `.json` | Seven checks of Section III on a Gaussian-mixture source (about one minute) |
| `verify_ls.py`, `.json` | Six checks of Sections V and VI on a time-varying moving average (about eleven minutes) |
| `verify_cyclo.py`, `.json` | Seven checks of Sections VII and VIII on periodic moving averages (about eleven minutes) |

The scripts import `spectral_core.py` and `verify_spectral.py` from
`../tit-stationary/`. Run them from this folder. numpy only (numpy 2.5.2,
Python 3.12.2 on 2026-11-15). On 2026-11-15 `verify_nongauss.py` and `verify_cyclo.py` passed 7 of 7, and `verify_ls.py` passed 6 of 6 after one pass criterion was changed: the first run failed a fixed threshold on the local-closeness distance that had been set too tight, and the criterion now asks for what (L2) says, that the distance shrink in proportion to the block length. The measured distances did not change.

Build: `pdflatex tit-beyond-stationary.tex` three times.

## Referee passes (models, 2026-11-15)

Three independent passes, each told to find errors and given the
companion papers to check imported results against. None was a human.

| Pass | Scope | Outcome |
|---|---|---|
| A | Sections II to IV (non-Gaussian) | No error. Four gaps, six minor points. All fixed: hypotheses of the moving-average example, the entropy-rate limit may be infinite, deterministic encoders in Theorem 8, a Markov chain stated in Theorem 3. |
| B | Cyclostationary and regimes sections | No error. Four gaps, five minor points. All fixed: Theorem 16(b) for blocklengths that are not multiples of the period, convexity of the achievable set in Proposition 21, the stacked hypotheses in Corollary 18. |
| C | Lemmas 9 to 11, Theorem 12 and its corollaries | One false sentence (which stationary processes satisfy the definition), one unproved remark (softened), nine minor points. All fixed. The pass also found that the constant in Lemma 10 does not depend on the holder. |

Passes A and B were made before Sections V and VI existed, and before
the fixes from pass C. No pass has read the final text end to end.

An outside reader's comments of 2026-11-15 were then applied: the
abstract and introduction no longer say the two non-Gaussian bounds
"meet" (only the lower bound is tight at high resolution); the scope of
Theorem 12 is stated in the abstract, the introduction and the theorem;
the subsection on the phase-averaged spectrum says at its start that it
compares two Gaussian models and not the penalty of not knowing the
phase; and a worked example with a figure follows Proposition 13.

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
  the closest prior result to Theorem 12 at the rate-only weight. Only
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

- [ ] A human reads the proofs, Theorem 12 first.
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
