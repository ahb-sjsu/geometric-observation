# IEEE Transactions on Information Theory — submission package

Manuscript: **Observation Theory: Geometry, Distortion, and Reliability as Properties
of Observation**

## Files

| File | Purpose |
|---|---|
| `observation-theory-ieee.tex` | Manuscript, `IEEEtran` **single-column** review format (required for review) |
| `observation-theory-ieee.pdf` | Compiled manuscript (12 pp, single column) |
| `cover-letter.tex` / `.pdf` | Cover letter to the Editor-in-Chief |

The self-contained repository version of the paper (article class, with the full
Appendix B) is `../observation-theory.tex`; the content is identical, reformatted here
for IEEE.

## Author

- **Andrew H. Bond**, Senior Member, IEEE
- Department of Computer Engineering, San José State University, San José, CA 95192, USA
- andrew.bond@sjsu.edu · ORCID **0009-0003-2599-6158**
- Sole author.

## Submission portal & format checklist

- **Portal:** IEEE Author Portal — <https://ieee.atyponrex.com/journal/t-it> (ORCID required to submit).
- **Review format:** single-column (this manuscript). ✔
- **Length:** 12 pp single-column, well under the 50-page review limit. ✔ (Final accepted version converts to two-column, ≤ 25 pp.)
- **Abstract:** one paragraph, ≤ 250 words, no displayed equations / abbreviations / references / tabular material. ✔
- **Index terms:** 9 terms after the abstract. ✔
- **Prior publication:** none; not presented at any conference; not under review elsewhere. Two companion works (Papers I, II) are cited and are distinct publications.
- **Preprint:** posting to arXiv at submission is encouraged by the Society and intended.
- **Reproducibility:** every empirical claim resolves to a sealed pre-registration and committed artifact; CI re-runs the reproducible experiments and verifies the theory. Repo: <https://github.com/ahb-sjsu/geometric-observation>.

## Build

```
pdflatex observation-theory-ieee.tex   # x3 (pgfplots/refs)
pdflatex cover-letter.tex
```

Both are compiled on every commit by the repository's CI (`paper` job).
