# TMLR submission package — Observation Theory for Estimation and Control

Prepared 2026-08-19. Venue: Transactions on Machine Learning Research
(OpenReview, double-blind, no page limit, rolling submission).

## Files

- `ot-estimation-control-tmlr.tex` — TMLR-format source, converted from
  the IEEEtran master (`../ot-estimation-control.tex`). 14 pp
  single-column, natbib author–year, `tmlr.sty` submission mode
  (auto-anonymized: "Anonymous authors / Paper under double-blind
  review", running head "Under review as submission to TMLR").
- `ot-estimation-control-tmlr.pdf` — the submission PDF. **Leak-checked**:
  text layer and PDF metadata scanned; no author name, institution,
  e-mail, ORCID, or repository handle present.
- `tmlr.sty`, `fancyhdr.sty` — official style files
  (JmlrOrg/tmlr-style-file).

## What was changed from the IEEEtran master (content-identical otherwise)

1. Class/style: IEEEtran → `article` + `tmlr`; IEEEkeywords dropped;
   theorem environments and all macros unchanged.
2. Citations: numeric → natbib author–year; all 36 `\bibitem`s carry
   `[Author(Year)]` labels; two name-in-prose citations converted to
   `\citet` to avoid author-name duplication.
3. Anonymization (submission mode only — reverted for camera-ready):
   - author block typeset only under `[accepted]`/`[preprint]` options;
   - repository names redacted ("the theory repository", "the program's
     campaign repository") with a footnote: links withheld for
     double-blind review; quoted sealing-commit hashes and seal IDs
     remain verifiable and links are restored in the camera-ready;
   - "the Paper-IV/Campaign-2 flip" → "the program's earlier
     coding-side (Campaign-2) flip";
   - `pdfauthor` unset.
4. Added a Broader Impact Statement (methodological transparency;
   generic dual-use note on resource-allocation machinery).

## OpenReview steps

1. Submit at openreview.net → TMLR → "Submit". Upload the PDF; fill
   title/abstract; declare the submission is not under review elsewhere.
2. Certifications to consider requesting: none required; this is a
   regular submission. (A "Featured" or "Outstanding" certification is
   reviewer-initiated.)
3. TMLR's two review criteria, and where this paper meets them:
   - **Claims and evidence**: every empirical claim maps to a sealed
     preregistration with frozen gates and a single governed run
     reported regardless of sign (ten campaigns: EC-2..7 incl. two
     registered instrument failures; DR-1..3); both boundary
     propositions machine-checked in Lean 4/Mathlib; five independent
     fresh-context verification passes (VI-11..15) on the record;
     34/34 references quote-verified against primary sources.
   - **Audience**: estimation/control + decision-focused-learning +
     task-aware-sensing readers; the prior-art section concedes every
     adjacent line explicitly.
4. Camera-ready (on acceptance): switch `\usepackage{tmlr}` →
   `\usepackage[accepted]{tmlr}`, restore `pdfauthor`, restore the two
   repository URLs in the footnote, restore the series/repo phrasing if
   desired, set `\def\month` / `\def\year` and the OpenReview forum URL.

## Known reviewer-facing notes (be ready to answer)

- Reproducibility: all runs are deterministic at sealed seeds; the
  verification passes reproduced every governed JSON bitwise (numpy
  2.3.5). Supplementary zip of harnesses + result JSONs can be attached
  in OpenReview if asked; links restored at camera-ready regardless.
- The two EC-7 instrument failures are presented as evidence of the
  protocol working, not weaknesses to defend.
- No optimality claims anywhere: greedy selection (Jawaid–Smith cited),
  threshold policies (both heuristics), stated in §VIII and the
  non-claims of the sealed preregs.
