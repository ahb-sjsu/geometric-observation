# Rate, Leakage, and Distortion for Stationary Gaussian Sources: Water-Filling on a Tilted Spectrum

Second paper of the series that begins with `../tit-rate-leakage/` (in review at IEEE T-IT, cited here as [1]). Paper one treats memoryless Gaussian vector sources. This one treats stationary Gaussian vector processes: sources with memory, and a holder whose observation is filtered, delayed, or incomplete.

**Status: first complete draft, 2026-11-13. Not reviewed by the author, not submitted.** The prose and the proofs were drafted by Claude (Fable 5.2) from the GO-12 material and paper one; the author has not yet read the proofs.

**→ [manuscript (PDF, 12 pp)](tit-stationary.pdf)** · [Observation Theory companion (PDF, 4 pp)](supplement-ot.pdf) · [executed notebook](reproduce-executed-2026-11-13.ipynb)

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
| Theorem 10 | Affine spectra Sigma = B + f A: windows split exactly in the Toeplitz eigenbasis and converge (Szego); converse for the stationary source | [1, Thm. 12], Lemma 2 |
| Conjecture 11 | Window convergence for general spectra | numerical evidence only |

Theorem numbers of [1] are those of the submitted version (`../tit-rate-leakage/tit-rate-leakage.tex` as of 2026-11-13). If paper one is revised, recheck every `\cite[...]{part1}`.

**Not proved, and said so in the paper:** achievability for the stationary source itself (proved for independent blocks only); window convergence outside the affine class; block codes against a holder that keeps a causal prefix; holders whose filter has memory in the window setting.

## Relation to the GO-12 records

The results are the GO-12 material (`../go12-process-region.tex`, preregistrations 065, 066, 070, 071) restated in paper one's rate-leakage notation and re-derived from paper one's theorems. Differences from GO-12: the whole frontier (every alpha) is treated through the tilted fixed point instead of the two-water-level system; the Toeplitz transfer, which GO-12 listed as four imported lemmas, is proved for affine spectra and left as a conjecture otherwise; the access-family theorem is stated for one-symbol descriptions only. The numerical checks here are new scripts and are **not** sealed registrations; the sealed GO-12 harnesses remain in `experiments/go12_*.py`.

## Files

| File | What it is |
|---|---|
| `tit-stationary.tex` / `.pdf` | the manuscript (IEEEtran, one column, 12 pp) |
| `supplement-ot.tex` / `.pdf` | Observation Theory companion, on the pattern of `../tit-rate-leakage/supplement-ot.tex` |
| `spectral_core.py` | costs and one solver (the water-filling iteration of [1, Prop. 11] with a bisection on the level); numpy only |
| `verify_spectral.py` | nine checks, fixed seed 20261113; writes `verify_spectral.json` |
| `verify_spectral-2026-11-13.txt` | recorded output: 9 passed, 0 failed, 499 s |
| `plot_bands.py`, `fig_bands.pdf/.png` | Fig. 1 |
| `sweep_bands.py`, `sweep_bands.json`, `sweep_bands-2026-11-13.txt` | Table II: the disjoint-bands instance across budgets (about 12 minutes) |
| `build_notebook.py`, `reproduce.ipynb` | the reproduction notebook and its generator |
| `reproduce-executed-2026-11-13.ipynb` | the notebook as executed on this machine |
| `lean-spectral-2026-11-13.txt` | Lean build record and axiom audit |
| `../../lean/ObservationTheory/SpectralRateLeakage.lean` | 21 theorems, no `sorry`, standard axioms only |

## Reproduce

```
python verify_spectral.py                      # about 8 minutes, numpy only
python plot_bands.py                           # Fig. 1 from verify_spectral.json
python build_notebook.py
jupyter nbconvert --to notebook --execute reproduce.ipynb --output reproduce-executed.ipynb
pdflatex tit-stationary.tex   (three times)
pdflatex supplement-ot.tex    (twice, after the manuscript: it reads tit-stationary.aux)
```

Lean: in `lean/`, `lake update && lake exe cache get && lake build ObservationTheory.SpectralRateLeakage`.

## What the checks do and do not show

- Theorem 3 is checked by solving the period-n problem as one real matrix program with no structure assumed and comparing with the per-frequency solution (48 instances, costs agree to 9e-14 bits).
- The window gaps for Conjecture 11 decay like 1/N from above in every case computed. That is evidence, not a proof.
- The Lean module checks algebraic steps only (see the paper's appendix for the list of what is and is not formalized). The module was built on its own on Atlas; the whole library was **not** rebuilt with the new import line in `lean/ObservationTheory.lean`.

## Mock review, 2026-11-13

An external mock T-IT review of the first draft recommended **major revision**. It independently reproduced the disjoint-bands instance (same rates, leakages, and supports, and an onset of overlap near D/D_max = 0.9503 against 0.9501 here). Its points and what was done:

| Review point | Status |
|---|---|
| 1. No operational region for the stationary source: achievability is proved for independent blocks only | **Open, and the main gap.** The Discussion now lists the four scopes separately and says a coding theorem for sources with memory is missing. Not fixed by rewording. |
| 2. Contribution beyond paper one needs sharpening | Introduction and Discussion now say the allocation, activation order, and disjoint supports are inherited from [1, Thm. 27, Cor. 28], and list what is new. Still weak without point 1. |
| 3. Sankar et al. comparison was made against the 2011 conference version but cited the 2013 journal | The claim that their rate-optimal solution is also leakage-optimal was removed. Both versions are cited and only the model difference is stated. The journal text is still unread (see below). |
| 4. Commuting formula omitted q_i = 0; activation threshold undefined at H = 0 | Fixed: x_i = 1 where q_i = 0; threshold written as 1 / (2 ln2 G) with G defined at H = 0. |
| 5. Delay interpretation too broad | Narrowed in the paper and the supplement: the invariance is for circular blocks and the spectral limit, finite windows have edge terms, and a party that has not yet received observations also holds less. |
| 6. Placeholders, missing figure, budget near the zero-rate end | The placeholders were an artifact of the draft the reviewer saw and are filled. Table II sweeps the budget and gives the disjointness range. |

The reviewer's suggested route to Conjecture 11 (compare the window and circulant problems in the same whitened variable at a fixed level; the log det X terms cancel) is recorded after the conjecture as a route not carried out.

## Open items before submission

- [ ] **Stationary-source achievability**, at least for the affine class. This needs a secure source coding theorem for Gaussian sources with memory. Liu, Cuff, and Verdu (T-IT 2016) pass from a one-shot achievability argument to stationary Gaussian processes for key agreement and are the methodological model. Without it the headline result is a characterization of circular approximations plus a stationary converse.
- [ ] Read the T-SG 2013 journal text of Sankar et al. and restore a precise comparison. The reviewer reports that it says rate and leakage cannot in general be minimized together and develops an interference-aware spectral allocation. Also verify the conference entry's author order, title, and pages.
- [ ] Author reads every proof. Lemma 2 and Theorem 10(b) are the ones most worth a hostile read.
- [ ] Independent referee pass on the proofs (fresh context), as was done for paper one.
- [ ] References marked `% verify` in the bibliography: Pearl 1973, Rauch-Tung-Striebel 1965 (volume and pages not checked); Gutierrez-Gutierrez and Crespo (year 2011 or 2012).
- [ ] Unread lead: Gao and Soleymani, 25th Biennial Symp. Commun., 2010, pp. 44-48 (parametric Wyner-Ziv function for stationary Gaussian sources via the Toeplitz distribution theorem). Read before submission; it may need citing next to Theorem 10.
- [ ] Gray 1973 and Leiner-Gray 1974 were seen as abstracts only in this pass (the GO-12 novelty record has a fuller read of Gray's 1972 report).
- [ ] Prior-art search for the delay statement (Proposition 7) was a single targeted search.
- [ ] Rebuild the whole Lean library with the new import.
- [ ] Decide whether to seal a registration for the new checks.
- [ ] Add the two tex files to the CI compile list if they should be guarded.
- [ ] Venue, title, and authorship are the author's decisions; nothing here is submitted.
