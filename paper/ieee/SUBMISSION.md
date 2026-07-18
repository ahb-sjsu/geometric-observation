# IEEE Transactions on Information Theory — submission package

Manuscript: **Observation Theory: Geometry, Distortion, and Reliability as Properties
of Observation**

## Files

| File | Purpose |
|---|---|
| `observation-theory-ieee.tex` / `.pdf` | Manuscript, `IEEEtran` **single-column** review format (required for review), 12 pp |
| `cover-letter.tex` / `.pdf` | Cover letter to the Editor-in-Chief |
| `graphical-abstract.tex` / `.pdf` / `.png` | Graphical abstract (T-IT supports one; part of the technical content, reviewed with the paper) |
| `observation-theory-ieee.docx` | Word conversion (see note below) |

The self-contained repository version of the paper (article class, with the full
Appendix B) is `../observation-theory.tex`; the content is identical, reformatted here
for IEEE.

### On format

- **Single vs. two column.** T-IT requires a **single-column** manuscript *for review*
  (this file). The **two-column** ≤ 25-page format is only the *final accepted* version,
  produced at camera-ready; it is not generated here.
- **DOCX.** For a LaTeX-authored paper, IEEE accepts the LaTeX/PDF; a Word file is not
  required. `observation-theory-ieee.docx` is a best-effort `pandoc` conversion provided
  for convenience: section structure, numbered theorems/propositions, editable
  (OMML) equations, the three tables, both figures, index terms, and the
  author/affiliation/ORCID line all carry over. Known limitations to fix by hand if the
  Word file is used as the master: display-equation auto-numbering is not preserved, and
  the bibliography formatting is plain. The **LaTeX/PDF is canonical.**

### Rebuild

```
pdflatex observation-theory-ieee.tex        # x3 (pgfplots/refs)
pdflatex cover-letter.tex
pdflatex graphical-abstract.tex
# DOCX (needs pandoc + poppler pdftocairo):
pdflatex fig1_flip.tex && pdflatex fig2_vacuity.tex
pdftocairo -png -singlefile -r 300 fig1_flip.pdf fig1_flip
pdftocairo -png -singlefile -r 300 fig2_vacuity.pdf fig2_vacuity
pandoc observation-theory-ieee-docx.tex -o observation-theory-ieee.docx --number-sections
```

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
