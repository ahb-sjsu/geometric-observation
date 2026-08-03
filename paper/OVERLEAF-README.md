# Overleaf project — A Rate–Work–Distortion Region for Consumer-Relative Observation

Upload the zip via Overleaf → New Project → Upload Project. It compiles
out of the box.

- Compiler: **pdfLaTeX** (Overleaf default)
- TeX Live: 2023 or later (any current Overleaf image)
- Main document: `consumer-relative-landauer.tex`
- Bibliography: `consumer-relative-landauer.bib` (bibtex, IEEEtran style —
  Overleaf runs bibtex automatically)
- All figures are inline TikZ/pgfplots; there are no external assets.

Provenance: every theorem in this manuscript carries a fresh-context
adversarial verification pass (0 errors) and a committed numerical
falsification harness in the reproducibility repository
(github.com/ahb-sjsu/geometric-observation — `experiments/
verify_consumer_landauer.py`, `verify_gaussian_sideinfo.py`,
`landauer_operational.py`; sealed preregistrations GO-P-2026-042/043/044).
