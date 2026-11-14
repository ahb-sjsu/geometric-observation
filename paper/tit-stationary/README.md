# Rate, Leakage, and Distortion for Stationary Gaussian Sources: Water-Filling on a Tilted Spectrum

Second paper of the series that begins with `../tit-rate-leakage/` (in review at IEEE T-IT, cited here as [1]). Paper one treats memoryless Gaussian vector sources. This one treats stationary Gaussian vector processes: sources with memory, and a holder whose observation is filtered, delayed, or incomplete.

**Status: draft, revised 2026-11-14 (general-spectrum theorems). Not reviewed by the author, not submitted.** The prose and the proofs were drafted by Claude (Fable 5.2) from the GO-12 material and paper one; the author has not yet read the proofs.

**→ [manuscript (PDF, 25 pp)](tit-stationary.pdf)** · [Observation Theory companion (PDF, 4 pp)](supplement-ot.pdf) · [executed notebook](reproduce-executed-2026-11-14.ipynb)

## What the paper proves

| Statement | Content | Rests on |
|---|---|---|
| Lemma 1 | Hermitian data: the tilted water-filling fixed point of [1] holds for Hermitian blocks | [1, Thms. 5, 7], realification |
| Lemma 2 | One compactness lemma: values converge when the measures over blocks converge weakly | Lemma 1, Berge |
| Theorem 3 | Source of period n: the region splits exactly over the n Fourier frequencies, one common level | [1, Thms. 5, 7], shift symmetry |
| Theorem 4 | Spectral region: per-frequency tilted water-filling under one level; Kolmogorov's formula at alpha = 1 | Lemma 2 |
| Theorem 5 | Scalar pair: minimum leakage is an integral of the closed form of [1, Cor. 17]; activation order | [1, Cor. 17, Lemma 26] |
| Corollary 6 | Rate-optimal and leakage-optimal descriptions can occupy disjoint bands | Theorem 5 |
| Proposition 7 | A delay or any invertible filter at the holder changes nothing | identity for J |
| Proposition 8 | One-symbol description: what the holder keeps enters through one conditional variance; AR(1) closed forms | [1, Cor. 17], RTS smoother |
| Proposition 9 | Stationary source: every blocklength-N code lies in the N-window region | [1, Prop. 2, Thm. 3] |
| Theorem 10 | Affine spectra Sigma = B + f A: windows split exactly in the Toeplitz eigenbasis at every N, and the frontier points converge (Szego) | [1, Thm. 12], Lemma 2 |
| Lemma 11 | Order: in the unwhitened error covariance the objective does not depend on the source and is monotone; a sandwich Sigma' <= Sigma <= (1+kappa) Sigma' moves every cost by at most (p/2) log(1+kappa) | determinant identities |
| Lemma 12 | Window costs are subadditive over adjacent windows, so they converge to their infimum | [1, Prop. 2], Fekete |
| Lemma 13 | A window of a finite-memory source is exactly a piece of a periodic source, which bounds the periodic cost by the window cost | aliasing, [1, Prop. 2] |
| Lemma 14 | First Szego limit for matrix symbols, with the excess log-determinant bounded by (b/a^3) sum tau \|F_tau\|^2 | prediction errors, past-future information |
| Theorem 15 | **Windows of a general spectrum** (was a conjecture until 2026-11-14): for every continuous positive definite spectrum and a memoryless holder, the window cost is at least the spectral cost at every N and converges to it (not monotonically in general); the gap is at most (s_N(Sigma) + (1-alpha) s_N(F*)) / (2 N ln 2); O(1/N) for Lipschitz spectra; every code obeys the spectral bound | Lemmas 11-14, Theorem 4 |
| Theorem 16, Lemma 17 | **Coding theorem for the stationary source, every continuous positive definite spectrum, memoryless holder map and white noise**: the spectral region is the operational region, with deterministic encoders | [1, Thm. 3], guard intervals, coupling, Theorem 15, Lemma 18 |
| Theorem 20, Lemma 21 | **Coding theorem for a holder with a filter of finite length and colored noise**: the spectral region is the operational region, deterministic encoders. Proof by operational comparison: more noise degrades the holder, the source is perturbed by the coupling in both directions, edge observations are dropped at a bounded cost; a stationary test channel gives the upper bound and the embedding with a filter the lower bound | Theorem 16's coupling, Lemmas 13, 14, 18, 19, [1, Thm. 3] |
| Lemma 18 | Concatenation: codes used on consecutive windows have the averaged rate and distortion and at most the averaged leakage, with no guard intervals and for any memory (the subadditivity of the leakage of codes) | subadditivity of entropy, conditioning, stationarity |
| Lemma 19 | Derandomization: a code with private randomness is matched by a deterministic code on k consecutive windows with a fixed schedule of seeds | stationarity, H(M \| S, Z) <= H(M \| S), law of large numbers |

Theorem numbers of [1] are those of the submitted version (`../tit-rate-leakage/tit-rate-leakage.tex` as of 2026-11-13). If paper one is revised, recheck every `\cite[...]{part1}`.

**Not proved, and said so in the paper:** the coding theorem for a filter with an infinite impulse response (the periodic and spectral results cover it, the stationary-source results do not); the sign and the bound of the window gap (Theorem 15) for a filter or colored noise; whether the window gap is of exact order 1/N and with what constant (the theorem gives an upper bound, and the explicit form of it is far from the computed gap); block codes against a holder that keeps a causal prefix; finite-blocklength coding performance.

## Relation to the GO-12 records

The results are the GO-12 material (`../go12-process-region.tex`, preregistrations 065, 066, 070, 071) restated in paper one's rate-leakage notation and re-derived from paper one's theorems. Differences from GO-12: the whole frontier (every alpha) is treated through the tilted fixed point instead of the two-water-level system; the Toeplitz transfer, which GO-12 listed as four imported lemmas, is proved for every continuous spectrum with a memoryless holder (Theorem 15), by a route that does not use Toeplitz-circulant equivalence; the access-family theorem is stated for one-symbol descriptions only. The numerical checks here are new scripts and are **not** sealed registrations; the sealed GO-12 harnesses remain in `experiments/go12_*.py`.

## Files

| File | What it is |
|---|---|
| `tit-stationary.tex` / `.pdf` | the manuscript (IEEEtran, one column, 25 pp) |
| `supplement-ot.tex` / `.pdf` | Observation Theory companion, on the pattern of `../tit-rate-leakage/supplement-ot.tex` |
| `spectral_core.py` | costs and one solver (the water-filling iteration of [1, Prop. 11] with a bisection on the level); numpy only |
| `verify_spectral.py` | nine checks, fixed seed 20261113; writes `verify_spectral.json` |
| `verify_spectral-2026-11-13.txt` | recorded output: 9 passed, 0 failed, 499 s |
| `plot_bands.py`, `fig_bands.pdf/.png` | Fig. 1 |
| `sweep_bands.py`, `sweep_bands.json`, `sweep_bands-2026-11-13.txt` | Table II: the disjoint-bands instance across budgets (about 12 minutes) |
| `verify_achievability.py`, `.json`, `verify_achievability-2026-11-14.txt` | covariance steps of the proof of Theorem 16 on Gaussian stand-ins, three instances including the general decomposition (a few seconds); not a check of the coding theorem. The 2026-11-13 record of the first two instances is kept |
| `verify_filter.py`, `.json`, `verify_filter-2026-11-14.txt` | five checks of steps of the proof of Theorem 19 for a causal two-tap filter in white noise, seed 20261116 (about three minutes); colored noise is not exercised |
| `verify_filter_colored.py`, `.json`, `verify_filter_colored-2026-11-14.txt` | six checks of steps of the proof of Theorem 19 for a two-sided three-tap filter and moving-average noise, seed 20261117 (about three minutes, run on Atlas): 6 passed. Standalone, not a notebook cell |
| `verify_filter_chains.py`, `.json`, `verify_filter_chains-2026-11-14.txt` | the two leakage chains of the proof of Theorem 19 on Gaussian stand-ins, seed 20261118 (under a second): 6 passed. Standalone, not a notebook cell |
| `prior-art-window-rate-2026-11-14.md` | the search agent's report on finite-block results in the rate-only case, with what was read and what was not |
| `verify_windows.py`, `.json`, `verify_windows-2026-11-14.txt` | seven checks of the steps of the proof of Theorem 15 on a moving-average source of memory two, seed 20261115 (about a minute): 7 passed |
| `build_notebook.py`, `reproduce.ipynb` | the reproduction notebook and its generator |
| `reproduce-executed-2026-11-14.ipynb` | the notebook as executed (14 code cells, all executed, no errors, 24 PASS lines and no FAIL; run on Atlas, Linux, python 3.12.3, numpy 2.4.6, because two local re-runs did not complete: one hit a one-hour cell timeout and one was stopped when this machine ran low on memory. It was re-run there after the third, general-decomposition instance of `verify_achievability.py` was added, and its output includes that instance); the 2026-11-13 run is kept beside it |
| `lean-spectral-2026-11-13.txt` | Lean build record and axiom audit |
| `lean-library-2026-11-14.txt` | whole-library build with the new import |
| `../../lean/ObservationTheory/SpectralRateLeakage.lean` | 21 theorems, no `sorry`, standard axioms only |

## Reproduce

```
python verify_spectral.py                      # about 8 minutes, numpy only
python verify_windows.py                       # about 1 minute
python verify_filter.py                        # about 3 minutes
python verify_filter_colored.py                # about 3 minutes
python verify_filter_chains.py                 # under a second
python plot_bands.py                           # Fig. 1 from verify_spectral.json
python build_notebook.py
jupyter nbconvert --to notebook --execute reproduce.ipynb --output reproduce-executed.ipynb
pdflatex tit-stationary.tex   (three times)
pdflatex supplement-ot.tex    (twice, after the manuscript: it reads tit-stationary.aux)
```

Lean: in `lean/`, `lake update && lake exe cache get && lake build ObservationTheory.SpectralRateLeakage`.

## What the checks do and do not show

- Theorem 3 is checked by solving the period-n problem as one real matrix program with no structure assumed and comparing with the per-frequency solution (48 instances, costs agree to 9e-14 bits).
- The window gaps decay like 1/N from above in every case computed. That is consistent with Theorem 15, which gives the sign and an upper bound of that order, not an exact 1/N law. On the instance of `verify_windows.py` the first bound of Theorem 15(b) is within a factor 2.4 to 5.0 of the gap; the explicit bound is several thousand times the gap. A numerical check on instances does not verify the theorem.
- The Lean module checks algebraic steps only (see the paper's appendix for the list of what is and is not formalized). The module was first built on its own on Atlas. On 2026-11-14 the library's root target was built there with the new import line in `lean/ObservationTheory.lean`, with no errors (`lean-library-2026-11-14.txt`). That was an incremental build: modules compiled earlier from identical sources were reused. `CRContext` and `RateLeakage` are not imported by the root file; they were built as separate targets and also pass.

**Numbering.** The records below and the older open items use the theorem numbers of the draft they were written against. Since the fifth-round revision (2026-11-14) a concatenation lemma is Lemma 18, so the derandomization lemma is Lemma 19, the filtered-holder theorem is Theorem 20, and its window lemma is Lemma 21; sections written before that say Lemma 18, Theorem 19 and Lemma 20 for those three. Theorem 11 and Lemmas 12 and 13 there are Theorem 16 and Lemmas 17 and 18 now; the conjecture (13, later 14) is Theorem 15.

## Mock review, 2026-11-13

An external mock T-IT review of the first draft recommended **major revision**. It independently reproduced the disjoint-bands instance (same rates, leakages, and supports, and an onset of overlap near D/D_max = 0.9503 against 0.9501 here). Its points and what was done:

| Review point | Status |
|---|---|
| 1. No operational region for the stationary source: achievability is proved for independent blocks only | **Proved for the affine class (Theorem 11), 2026-11-13, after the review.** The source is written as a finite-memory source plus an independent source of small power; blocks separated by guard intervals are independent and are coded by [1, Thm. 3]; the encoder draws the finite-memory part from its conditional law; the remainder changes the leakage by at most eps tr(JA) / (2 ln 2) bits per symbol. The encoder is randomized. **The proof has not been read by the author or refereed.** Outside the affine class achievability is conditional on Conjecture 14. |
| 2. Contribution beyond paper one needs sharpening | Introduction and Discussion now say the allocation, activation order, and disjoint supports are inherited from [1, Thm. 27, Cor. 28], and list what is new. Still weak without point 1. |
| 3. Sankar et al. comparison was made against the 2011 conference version but cited the 2013 journal | The claim that their rate-optimal solution is also leakage-optimal was removed. Both versions are cited and only the model difference is stated. The journal text is still unread (see below). |
| 4. Commuting formula omitted q_i = 0; activation threshold undefined at H = 0 | Fixed: x_i = 1 where q_i = 0; threshold written as 1 / (2 ln2 G) with G defined at H = 0. |
| 5. Delay interpretation too broad | Narrowed in the paper and the supplement: the invariance is for circular blocks and the spectral limit, finite windows have edge terms, and a party that has not yet received observations also holds less. |
| 6. Placeholders, missing figure, budget near the zero-rate end | The placeholders were an artifact of the draft the reviewer saw and are filled. Table II sweeps the budget and gives the disjointness range. |

The reviewer's suggested route to Conjecture 14 (compare the window and circulant problems in the same whitened variable at a fixed level; the log det X terms cancel) is recorded after the conjecture as a route not carried out.

## Second-round review, 2026-11-13

The same reviewer read the revision with Theorem 11 and moved to "a plausible T-IT submission needing a focused technical revision". It found no fatal gap in the achievability argument. Its points and what was done:

| Review point | Status |
|---|---|
| Deterministic encoders suffice | Added as Lemma 13 with the reviewer's argument: average over the seed (conditioning on the seed cannot raise H(M \| S)), pick finitely many seeds by the law of large numbers, run them on consecutive windows. Theorem 11 is now stated for deterministic encoders and the open question is removed. |
| The distortion cross term vanishes exactly | Adopted. The reconstruction is a function of T' and E is independent of T', so D_N = D'_N + tr(QA) int e. The auxiliary eta is gone and the constants are smaller. |
| Abstract should state the holder restriction | Done: memoryless map in white noise, in the abstract and the introduction. |
| "Liu" missing in related work | A line break had put the name at the end of a tex comment. Fixed. |
| Give Theorem 11 the central position | The introduction now says it is the main result that does not follow from paper one frequency by frequency. |

## General-spectrum theorems, 2026-11-14

After the second-round review asked for more than the affine class, the window-convergence conjecture was proved and the coding theorem extended to every continuous positive definite spectrum (Theorems 15 and 16), still for a holder with a memoryless map and white noise. The route is not the reviewer's suggested Frobenius-norm stability estimate. It uses the order structure in the unwhitened error covariance (Lemma 11), subadditivity over adjacent windows (Lemma 12), the exact embedding of a finite-memory window in a periodic source (Lemma 13), and a block-Toeplitz feasible point with a Szego-type lemma (Lemma 14).

Checks so far:

- `verify_windows.py`: every step of the proof tested on one moving-average instance, 7 of 7 pass. A check on instances does not verify a theorem.
- The mock reviewer read the draft and found four corrections, all applied: "decrease to" was false as monotonicity (its counterexample, window cost 0.0172783 at N = 5 and 0.0172881 at N = 6, was reproduced and is now in the paper); O(1/N) is an upper bound and not a law; colored noise and filtering are different limitations; a factor typo in Lemma 13.
- An independent fresh-context referee pass by a model went through Lemmas 11 to 14 and Theorems 15 and 16 line by line and tested edge cases numerically (singular J, N at most the memory, p = 3, alpha = 0 and 1). It found no error that invalidates a statement. Its gaps, all fixed: the passage to spectral costs at and above D_max in Lemma 11(c); periodicity of the spectrum and a single statement of the Fejer sandwich; what "a test channel that attains the frontier" means; a duplicated equation label that made Corollary 6 point at the wrong equation; a stale appendix sentence about `verify_achievability.py`; an "explicit constant" overstatement in the abstract; attribution of subadditivity to the classical rate-distortion argument.
- Not checked by that pass: paper one's proofs, Lemmas 1 and 2 and Theorems 3 and 4 beyond their statements, the Lean module. **No human has read these proofs.**

## Filtered holder, 2026-11-14

Theorem 19 extends the coding theorem to a holder that sees the source through a filter of finite length in noise of any continuous positive definite spectrum (real taps; the holder is given its observations at the times of the window). The window-level order argument of Lemma 11 is not available there, so the proof compares systems operationally: adding noise gives a degraded holder, the source is perturbed by the coupling of Theorem 16 in both directions, and the edge observations of a window are dropped at a cost bounded independently of the window. Lemma 20 gives the two window bounds (a stationary test channel for the upper bound, the embedding with a filter for the lower bound).

- `verify_filter.py`: five checks on one instance with a causal two-tap filter in white noise, all pass.
- `verify_filter_colored.py`: six checks on one instance with a two-sided filter and colored (moving-average) noise, all pass: ordering and convergence of the interior and window costs, subadditivity, the embedding in the periodic source with circular filter and circular colored noise, the edge bound (0.50 bits against a bound of 16.6), the noise comparison with a noise increase that is not a multiple of the spectrum, and degradation at the level of windows.
- `verify_filter_chains.py`: the two leakage chains of the proof (achievability and converse) on Gaussian stand-ins for the message, same kind of instance (two-sided filter, colored noise), 6 of 6 pass: each inequality of both chains, the achievability chain also in the order displayed in the paper (eq. for H(M | S^N), degrade to the block interiors first and then remove the remainder), the two couplings as the encoder performs them (errors 2e-14), independence and equal laws of the blocks, the edge bound (0.45 bits against 17.3), and the bounds on the information carried by the remainder (2.9 bits against 13.0; 3.2 against 25.9). The bounds are loose at this size, so the check confirms the direction of every step and not tightness. A Gaussian stand-in is not a code, and this does not verify the coding theorem.
- An independent fresh-context referee pass by a model checked every step by hand and probed numerically a two-sided filter with colored noise (the embedding to 6e-15, the noise comparison on 20000 random instances, the edge inequality and both leakage chains on Gaussian stand-ins). It could not break the theorem and found no error. Its gaps, all fixed: private randomness must be independent of the whole source process; the converse's leakage step now covers a randomized given code; the frontier costs are defined for a general linear Gaussian holder; real taps are stated; the monotonicity in the noise comparison is justified as addition of independent noise; ranges of D; the noise hypothesis in the abstract. It noted that its numerical tests of the two leakage chains are weak, because the bounds hold with a large margin. Its scripts are not in the repository.
- Not covered: a filter with an infinite impulse response; a holder given observations outside the window (achievability holds, the converse is not proved); the sign and the bound of the window gap for a filter or colored noise.
- **No human has read this proof.**

Known weak points:

- `verify_achievability.py` now has a third instance with the general decomposition of the proof (2026-11-14): a vector moving-average source whose spectrum is not affine, a Fejer mean of degree 14, eps = 0.49 against a smallest eigenvalue of 1.13. All steps pass: remainder spectrum within [0, eps], block independence, the coupling as performed (2e-14), both leakage steps (measured change 0.04 bits, bound 7.4), and the exact distortion split with the bound eps tr Q. A first choice of instance violated the proof's hypothesis eps < smallest eigenvalue (the Fejer mean of degree 3 was too far from the spectrum) and failed for that reason; the Fejer mean converges slowly, so the degree and with it the guard interval must be large.
- Novelty at alpha = 1, checked 2026-11-14: Gutierrez-Gutierrez, Zarraga-Rodriguez and Insausti (Entropy 19(10):554, 2017) was read in full. It treats a scalar source at small distortion only (D at most the minimum of the spectrum), bounds the finite-block rate-distortion function from above by the rates of schemes that code DFT coefficients separately (tighter than Pearl 1973), and shows those bounds converge. It states no rate in the block length and does not bound the distance of the window cost from its limit. It does not overlap Theorem 15(b). In its regime the window cost is explicit and the first bound of Theorem 15(b) holds with equality, which the paper now says (checked numerically to 10 digits). Not checked: other finite-block literature (a single paper was compared), and Pearl's paper itself.
- Gallager 1968 is cited for the classical subadditivity argument from memory (a check on 2026-11-14 could not reach the book).

## Prior art for the window bound in the rate-only case, 2026-11-14

A wider literature search (by a search agent; its full report with access labels is `prior-art-window-rate-2026-11-14.md`) changed what the paper may claim.

- **The first bound of Theorem 15(b) at alpha = 1 is not new.** It is the Wyner-Ziv (1971) memory bound applied to blocks of N symbols: R_N(D) - R(D) <= h(T^N)/N - entropy rate, which for a Gaussian source is s_N(Sigma) / (2 N ln 2), the same constant, at every distortion. The agent read the bound in Gray, *Source Coding Theory* (1990), Sec. 4.7.1. The step to blocks is one line and was not seen printed. Wyner and Ziv's paper itself was read as an abstract only.
- **The sign of the gap at alpha = 1 is classical** (subadditivity; Gray, *Entropy and Information Theory*, Lemma 10.6.2 of the corrected first edition; Gallager 1968 Theorem 9.8.1 for discrete sources, at second hand).
- **O(1/n) at every distortion is known for scalar autoregressive sources started at zero**, with constants that are not explicit (Tasci and Kostina, arXiv:2602.09176, eq. (53), read at first hand; related eigenvalue estimates in Tian and Kostina 2019, also read at first hand).
- **Not found in the literature:** the two-cost bound (the term s_N(F*)), the feasible block-Toeplitz point, any finite-window result for Gaussian Wyner-Ziv, conditional, or secrecy problems with memory, and a statement on non-monotone convergence.
- The manuscript now says this: the remark after Theorem 15 and a sentence in the introduction credit Wyner and Ziv for the rate-only bound and state what the paper adds (the second cost and the constructive proof).
- **Limits of this search.** None of Wyner-Ziv 1971, Berger 1971, Gallager 1968, or Pearl 1973 was read in full. Four Entropy papers were read through a summarizing fetch, not the PDFs. The new bibliography entries carry `% verify` notes saying exactly what was and was not read. A person with library access should open Wyner-Ziv 1971 and Berger 1971 Ch. 4 before submission.

## Fourth-round notes from the reviewer, 2026-11-14

| Point | Status |
|---|---|
| Display the two leakage chains of Theorem 19 | Done: the achievability chain and the converse chain are displayed equations, with notation for the retained block interiors and the interior of the window, and each bound on the remainder stated next to its chain. The achievability chain now degrades to the block interiors first, as the reviewer wrote it. `verify_filter_chains.py` checks it in that order. |
| The comparison with the finite-block literature was too broad | Narrowed: those are upper bounds on the window cost of a scalar source at small distortion by particular schemes, which bound the gap indirectly in that regime; Theorem 15(b) is an explicit window-to-spectrum bound for the two-cost problem, vector sources, every distortion. |
| State the holder's observation horizon beside the headline claim | Done in the introduction: in both coding theorems the holder has its observations at the times of the coded window; with the whole observation process the achievability holds and the converse is open. |
| Keep the numerical floats with the examples | Done: the two tables and the figure are pinned and now fall on the pages of Section IX. |

## Companion, reviewer's notes, 2026-11-14

The reviewer read the Observation Theory companion and asked for three corrections, all made in `supplement-ot.tex`: the hypotheses are restored where the prose had become universal (continuous positive definite spectral densities for the signal and the noise; "one number" is for the scalar Gaussian context, and a vector context would need a conditional covariance matrix); the holder's observation horizon is stated beside the operational claim (observations at the times of the coded window; with the whole observation process the coding theorem holds and the converse is open), and kept apart from the one-moment retention result; the account of the proofs now names the arguments beyond the per-frequency optimization (order and subadditivity for windows, approximation, coupling, guard intervals, degradation, edge control, derandomization).

## Fifth-round review, 2026-11-14

A further review was checked point by point against the manuscript. Part of it refers to things that are not in these documents: quantities D-tilde, D_crit and D_b with values 0.99, 1.05 and 1.13; an "Appendix C"; a "Theorem 16" for the O(1/N) bound; and, in the supplement, numbered theorems, an optimal-transport dual with potentials, log-determinant formulas, and a lemma with a factor 2. The supplement here is an Observation Theory reading with no theorems or formulas. Those points could not be acted on. The points that do apply, and what was done:

| Point | Status |
|---|---|
| Leakage of repeated codes needs a standalone lemma | Added as Lemma 18. The review's worry was that leakage does not add across blocks when the source has memory. For H(M \| S) it is subadditive whatever the memory, by subadditivity of entropy and conditioning, and no guard intervals are needed. The paper had this inside the derandomization proof and by reference elsewhere; it is now one lemma, cited by the derandomization lemma, the time-sharing step, the remark on blocklengths, and Theorem 20. The text also says this is a different statement from the subadditivity of test-channel costs (Lemma 12). |
| State who sees what | Added to the Model section: encoder sees the source only, decoder the message only with no side information, holder the message and its own observation; not the Wyner-Ziv arrangement. |
| State assumptions where used | Added to the Model section: what positive definiteness of the two spectra is used for and what it excludes (noiseless holder components, band-limited sources), with no claim of extension by continuity; continuous frequency response (absolutely summable taps suffice) for the periodic and spectral theorems and finite length for the coding theorem; the range 0 < D < D_max and what happens beyond it. |
| Null sets and uniqueness | Already in Theorem 4 ("attained, uniquely up to a null set, by the continuous field"); the minimizing field is continuous. No change. |
| Disjoint bands: sufficient, not necessary | A sentence after Corollary 6 says so, and that the distortion at which the described sets first meet is computed for an instance and has no formula here. |
| The O(1/N) bound is not a dimensioning tool | Said after Theorem 15; a and b are defined where the factor 314 is quoted. Non-monotone convergence was already stated with an example. |
| Proposition 8: define q in the statement | Done. The abstract already limits the statement to a one-symbol description. |
| Proposition 7: observation model in the statement | Done: the holder has its whole observation in the period-n and spectral models. |
| "At D = 0.97 D_max = 1.261" reads badly | Reworded. Coherence was already defined by its formula at the start of the section on the scalar pair. |
| Figure 1 caption ambiguous | Reworded: strictly below the spectrum means described, equal to it means not described. |
| Repository URL, scripts | The URL and the script names are in the appendix on numerical checks. A pinned commit or archived release is not cited yet; see open items. |
| Reference [1] theorem numbers | The Model section now says the numbers are those of the submitted version at the archived address. |
| Move proofs of Lemmas 11 to 14 to the supplement | Not done. It is a structural choice for the author; the supplement is currently an interpretive companion and would change character. |

## Open items before submission

- [ ] Pin the code: cite a commit hash or an archived release (as paper one does with its DOI) in the appendix on numerical checks.
- [ ] Decide whether to move the proofs of Lemmas 11 to 14 out of the body (25 pages now).

- [x] Read Gutierrez-Gutierrez, Zarraga-Rodriguez, Insausti, Entropy 19(10):554 (2017), and compare with Theorem 15(b) at alpha = 1 (done 2026-11-14, see above).
- [ ] Gallager 1968: attempted 2026-11-14, **not verified**. No accessible copy of the book was found. The citation is now at chapter level (Ch. 9), which is confirmed only at second hand as the chapter on rate distortion for sources with memory. That the subadditivity argument is there (recalled as Sec. 9.8) is still from memory. Needs a library copy, or a replacement source that has been read.
- [ ] Pearl 1973: attempted 2026-11-14, **partly verified**. Bibliographic details confirmed against an index record (vol. 19, no. 2, pp. 229-232, March 1973, DOI 10.1109/TIT.1973.1054985) and the abstract read. The full text is paywalled and was not read. From the abstract: the loss of DFT coding against the optimal transform is tied to a distance between the Toeplitz covariance and a circulant, which is O(1/N) for finite-order Markov processes. That is a comparison of schemes at one block length, not a bound on the distance of the block optimum from its limit, and the paper now says this. Read the full text before submission.
- [x] Wider search for finite-block convergence-rate results in the rate-only case (2026-11-14, see the section on prior art). Outcome: the rate-only bound is Wyner-Ziv on blocks; the paper is corrected.
- [ ] Wyner-Ziv 1971: **attempted 2026-11-14, abstract only.** The publisher's page was opened in a browser that is not signed in to a subscription. Confirmed there: vol. 17, issue 5, September 1971, pp. 508-513, DOI 10.1109/TIT.1971.1054699, and the abstract's statement R*(beta) - Delta <= R(beta) <= R*(beta), with R* the rate of the memoryless source with the same marginal and Delta a measure of the memory of the source. The full text was not read. The bound with the Gaussian value of Delta was read at first hand in an open-access survey (Gibson, Entropy 19(11):604, 2017, Sec. 4.6, eqs. (23)-(25)); it equals the N = 1 case of the paper's bound. The author has no access to IEEE Xplore, so the citation strategy was changed on 2026-11-14: the bound is used in the form given in Gray, *Source Coding Theory* (1990), Sec. 4.7.1, pp. 103-104, which **was read at first hand** in the author's posted PDF. It gives R(D) >= R_1(D) - (h(X_0) - entropy rate) for a stationary source with a density and an additive distortion, notes that the subtracted term does not depend on the distortion measure, and attributes the bounds to Wyner and Ziv. The step to letters that are blocks of N vector symbols is this draft's, not the book's. Wyner-Ziv 1971 itself remains credited but unread in full.
- [x] Source for subadditivity and convergence from above in the rate-only case: Gray, *Entropy and Information Theory*, Sec. 10.6, Lemma 10.6.2 (corrected first edition posted by the author, June 26, 2023), **read at first hand 2026-11-14**. It is stated for the distortion-rate function, with the two-block memoryless channel construction that the paper's Lemma 12 also uses. The paper now cites it as the source consulted, with Gallager 1968 and Berger 1971 as "see also". Neither of those two was read (no open copy), and the page numbering of the printed 1990 edition of Gray's book may differ from the posted one.
- [x] Tasci and Kostina, arXiv:2602.09176v2: **read at first hand 2026-11-14.** Confirmed, with two corrections to the search agent's description. The source is a scalar Gaussian autoregressive source of finite order started at zero (asymptotically stationary), under mean-squared error. The 1/n statement, |R_n(d) - R(d)| <= c_r / n for d in (0, d_max), is eq. (53) in the proof of Corollary 3, not Lemma 1 itself; Lemma 1 is the eigenvalue estimate behind it, for all sufficiently large n. The constants are not explicit. The paper's sentence now says "started at zero" and cites this paper for the statement, with Tian and Kostina 2019 as "see also".
- [x] Tian and Kostina 2019 (arXiv:1804.09418v4): **read at first hand 2026-11-14.** The search agent's description is confirmed. Source: the scalar Gauss-Markov source started at zero, squared error. Theorem 4 bounds the error of the eigenvalue distribution by C_L / n for bounded Lipschitz nondecreasing test functions and every n; the proof of Theorem 7 gives |d - d_n| <= C_d / n. A bound on the n-th order rate-distortion function minus its limit is not stated as such, so the paper cites it as "see also" only. It also cites Grenander and Szego "Chap. 5" for Szego's theorem, which supports the chapter-level citation here at second hand. The journal details were then verified against Crossref: IEEE Trans. Inf. Theory, vol. 65, no. 10, pp. 6355-6384, October 2019, DOI 10.1109/TIT.2019.2919718; the entry in the paper was already correct.
- [ ] Human referee pass on Lemmas 11 to 14 and Theorems 15 and 16, and on Theorem 19 and Lemma 20.
- [x] A recorded numerical check of Theorem 19's steps with colored noise and a two-sided filter (`verify_filter_colored.py`, 2026-11-14).
- [x] A recorded check of the two leakage chains in the proof of Theorem 19 (`verify_filter_chains.py`, 2026-11-14, Gaussian stand-ins).
- [x] Rerun `verify_achievability.py` on the general decomposition (2026-11-14, third instance, passes).

- [ ] **Author and a human referee read the achievability proof (Theorem 11, Lemma 12).** One independent fresh-context referee pass by a model was run on 2026-11-13: it found no error that invalidates the theorem and verified each step of the three bounds by hand. It found one real gap, that the closing claim (achievable region = spectral region) did not follow from supporting-line bounds as written, and smaller ones (no definition of achievable for the stationary source; a remark that overstated the reduction for general spectra; the holder is given the window only; small slips). All were fixed: the region is now defined as the intersection of half-planes (eq. for R(D)), the achievable set A(D) is defined, and the proof ends with a time-sharing and support-function argument. That argument was added after the referee pass and has **not** itself been refereed. Not checked by that pass: the cited external results, paper one's appendix proof of its coding theorem, and Lemma 1's proof. Points to attack: the independence claims in the coupling (T', E, U and the private randomness); the step H(M | S, E) = H(M | S'); the order of the limits (eta, eps, n, K); the use of Lemma 2 on the product space for continuity in eps; whether [1, Thm. 3] delivers rate, leakage, and distortion simultaneously at a frontier point as used.
- [x] Randomized encoder: removed by Lemma 13 (second-round review, below). An independent fresh-context referee pass by a model (2026-11-13) could not break Lemma 13 or its use in Theorem 11 and verified each step by hand. It also checked the closing region argument of Theorem 11, which had not been refereed before. It found no error and four gaps of one sentence each, all fixed: time sharing as written gave one mixing weight only (now a copies and b copies); joint measurability of the encoder in the seed; the stationarity step needs the memoryless holder map and independent noise; the remark on intermediate blocklengths. It also noted that the lemma depends on taking H(M | S) as the leakage of a randomized code, which the paper now says. Not checked by that pass: paper one's theorems (in particular that its Theorem 3 gives a deterministic encoder with the leakage bound in the form used by Lemma 12), Lemma 2, Theorem 10(a),(b). No human has read it.
- [x] Sankar et al., T-SG 2013 journal text: **read in full 2026-11-14** from the authors' version (the PDF the author saved to `docs/SM_privacy8.pdf`, which is not committed). What it says: a scalar stationary Gaussian load X = G_c + G_i + Z in a circular block model; leakage is the mutual information per symbol between the hidden component G_i and the revealed sequence, with no side information at the receiving party (their Remark 4 mentions side information as a possible extension); they minimize leakage at a given mean-square distortion and get an interference-aware reverse water-filling (eqs. (24)-(26)); they say minimizing both rate and leakage is in general not feasible and do not treat the rate (Sec. III-E); Remark 10: the rate-optimal allocation is ordinary water-filling on the total spectrum and differs from the leakage-optimal one; Remark 11: the joint problem has to be considered; Remark 9: when the whole measurement is private, leakage and rate coincide. The reviewer's report of the journal version was accurate. **Consequence for this paper:** that the rate-optimal and leakage-optimal allocations over frequency differ is already in their paper, for unconditional leakage of a component. The related-work paragraph now says so and states what is new here (the joint frontier, conditional leakage with the second party's own observation, vectors, the operational region). The conference entry was verified on 2026-11-14 against the Crossref record for its DOI and the arXiv abstract page: title "Smart meter privacy: A utility-privacy framework", authors in the order Rajagopalan, Sankar, Mohajer, Poor, Proc. IEEE SmartGridComm 2011, pp. 190-195. The entry in the paper was already correct.
- [ ] Author reads every proof.
- [x] Referee pass on Lemma 1, Lemma 2, Theorem 10(a)-(c), Proposition 9, and the two other uses of Lemma 2 (Theorem 4 and the "Limits" step of Theorem 11): an independent fresh-context pass by a model, 2026-11-14, by hand, no numerics. It found no error that invalidates a statement, and gaps of a sentence each, all fixed: Lemma 2(b) is now stated for any measure (it was used that way); Theorem 10(a) now argues the identification with V_mu_N (repeated Toeplitz eigenvalues, real versus Hermitian, equal maximal distortions, positivity of the blocks); Theorem 10(c) now carries the range 0 < D < D_max; the pushforward step in 10(b) is written out; the level-zero case and nonnegativity of the integrand are stated in Lemma 2; the spectral density is no longer defined through a Fourier series that need not converge. Not checked by that pass: paper one's proofs, Theorem 3 beyond its use of Lemma 2, and the cited books.
- [x] Szego's theorem for a continuous symbol. Checked 2026-11-14 against the text of Gray's monograph (the author's posted PDF): Theorem 4.2 assumes absolutely summable coefficients (the Wiener class) and Lemma 4.1 bounds the eigenvalues of a Hermitian Toeplitz matrix by the range of its symbol, both as cited. The proof of Theorem 10(b) now extends Theorem 4.2 to a continuous symbol by uniform approximation, using those two statements only.
- [ ] Grenander and Szego could **not** be opened. The citation is now at chapter level ("Ch. 5", inferred from the table of contents, where "Eigenvalues of Toeplitz forms" is the fifth chapter); the earlier "Sec. 5.2" was from memory and is removed. Check the chapter number and the theorem's hypotheses against the book. The proof no longer depends on it.
- [x] Third-round note from the reviewer (2026-11-14): the first remark after Theorem 11 claimed that limit points of the finite-memory window frontiers are achievable at a fixed approximation error. Corrected: the perturbed guarantees are stated first, and membership in A(D) is claimed only for limits as the error goes to zero. The main proof was already correct on this point.
- [ ] Independent referee pass on the proofs (fresh context), as was done for paper one.
- [ ] References marked `% verify` in the bibliography: Pearl 1973, Rauch-Tung-Striebel 1965 (volume and pages not checked); Gutierrez-Gutierrez and Crespo (year 2011 or 2012).
- [ ] Gao and Soleymani, "Rate-distortion function for Gauss-Markov source with side information at the decoder", 25th Biennial Symp. Commun., 2010 (DOI 10.1109/BSC.2010.5473007): **abstract read 2026-11-14, full text paywalled and not read.** From the abstract: a parametric Wyner-Ziv rate-distortion function for a general stationary Gaussian source by the Toeplitz distribution theorem, closed forms for first- and second-order Gauss-Markov sources at small distortion, asymptotic achievability by a conditional Karhunen-Loeve transform with Wyner-Ziv coding. It is side information at the decoder with no second party, and asymptotic only, so it does not overlap the window or coding theorems here. It is now cited in related work with a one-sentence description that rests on the abstract. Read the full text before submission, and confirm the pages (44-48, from an earlier search).
- [ ] Gray 1973 and Leiner-Gray 1974 were seen as abstracts only in this pass (the GO-12 novelty record has a fuller read of Gray's 1972 report).
- [ ] Prior-art search for the delay statement (Proposition 7) was a single targeted search.
- [x] Build the whole Lean library with the new import (2026-11-14, incremental, no errors; see `lean-library-2026-11-14.txt`). The root file does not import `CRContext` or `RateLeakage`; whether it should is a separate decision.
- [ ] Decide whether to seal a registration for the new checks.
- [x] The two tex files are in the CI compile list (2026-11-14), with the same undefined-reference guard as paper one.
- [ ] Venue, title, and authorship are the author's decisions; nothing here is submitted.
