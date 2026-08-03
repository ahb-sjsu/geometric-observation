# Novelty-sweep record — `complementarity-tax.tex`

**Date:** 2026-08-03 · **Method:** four independent fresh-context web-search
agents (WebSearch + direct arXiv/publisher fetches), each sweeping one area
flagged by the manuscript's `[NOVELTY-CHECK]` comments plus one area added after
VI-10 (the individual-distortion Gaussian RD literature). Full agent reports in
the session transcript; this file is the durable record. **Standing caveat on
every "clear" verdict below:** absence of evidence under the recorded queries,
not provable novelty. **Disposition:** all findings folded into note v0.3
(abstract rescoped, §3 attributed, §7 delineation rewritten, 12 references
added).

## Headline result — the rate side is prior art

After the read-plane reduction Y = B′X, **Theorem 1 and Proposition 2 are known
results** and are now presented as attributed (proofs kept for completeness in
the consumer-relative notation):

- **Theorem 1** (product floor D_A·D_B ≥ κ·2^(−2R)) = the Gaussian evaluation of
  **Gray 1973** (IEEE T-IT 19(4):480, conditional-RD lower bound
  R_{X₁X₂}(D₁,D₂) ≥ R₁+R₂−I(X₁;X₂)); equivalently the vector Shannon lower
  bound. Chen et al. 2026 call the det-ratio form the "Hadamard lower bound"
  and treat it as known.
- **Proposition 2** (exact iff diag(D) ⪯ Σ_Y) = the low-distortion branch of the
  bivariate Gaussian RDF under individual MSE criteria: **Xiao–Luo, Allerton
  2005, Thm. 6** (scalar regime condition ρ² ≤ (1−D₁)(1−D₂) — algebraically
  identical to diag(D) ⪯ Σ); re-derived with explicit three-regime display by
  **Lapidoth–Tinguely, IEEE T-IT 56(6):2714, 2010, Thm. III.1**; matrix-ordering
  ("semidefinite condition") iff + max-det SDP + multivariate extension by
  **Stylianou–Charalambous–Charalambous, ISIT 2021 (arXiv:2102.07236; explicit
  formulas arXiv:2508.16301, 2025)**; the whole package is "it is known"
  material in **Chen–Gao–Shi–Wu–Caire–Poor–Zhang, arXiv:2602.06464 (Feb
  2026)**, whose SDC (K ⪰ E) is exactly diag(D) ⪯ Σ. Also relevant:
  Nayak–Tuncel–Gündüz–Erkip (IEEE T-IT 54(4), 2008) restate Xiao–Luo Thm. 6
  with the backward-channel tightness structure; Op 't Veld–Gastpar (ISIT 2016)
  treat the single-projection reduction as a "trivial first observation".
- **Evidence caveat:** the Xiao–Luo Allerton PDF is not openly retrievable;
  Thm. 6 was verified through two independent verbatim restatements (Nayak et
  al. 2008; Stylianou et al. 2021). Acceptable for delineation; pull the
  primary before journal submission.

## What no sweep found (the note's surviving contributions)

1. **The tax quantity** CT_R = R_AB − max(R_A,R_B) under any name. Nearest:
   the "rate penalty" A(Θ) of universal rate-distortion-classification
   representations (Nguyen et al., arXiv:2504.09025, 2025; ancestor Zhang et
   al., NeurIPS 2021) — prices one-at-a-time universality across operating
   points, not simultaneous constraints, and vanishes in their Gaussian case.
   Gray-line comparisons are always against R₁+R₂, never max.
2. **The read-operator packaging**: two rank-one reads of a d-dimensional
   source with κ = det(B′Σ_xB) as the geometric incompatibility invariant and
   the two-read reduction stated as a lemma (folklore for one projection;
   unstated for the pair).
3. **The entire work side** — Theorem 4 (D_A·D_B ≥ κ_S·2^(−2I(X;X̂|S))), the
   discount identity Cor. 5 (rate floor − work floor = I(u′X,v′X;S)), CT_W, and
   the tax gap → I(X₁;S). Nearest ancestors, all ADJACENT-FRAMEWORK: del Rio et
   al. (Nature 474:61, 2011 — erasure priced by conditional entropy);
   Berta–Brandão–Majenz–Wilde (PRA 98:042320, 2018 — CQMI exactly prices
   conditional erasure/decoupling of ONE record given ONE retained system);
   Sagawa–Ueda (PRL 102:250602, 2009); Faist et al. (Nat. Comm. 6:7669, 2015);
   Anderson (Springer 2018, conditional erasure w/ referent); Ji–Gour–Wilde
   (arXiv:2503.09012, 2025). The discount identity's information-theoretic
   skeleton is again Gray 1973 (R_X(D) − R_{X|S}(D) ≤ I(X;S)) — single
   consumer, no thermodynamic asymmetry.
4. **The term** "complementarity tax": no prior use found in information
   theory; economics has complementarity-and-taxation literature (Corlett–Hague
   1953) but not the term.

## Uncertainty-analog delineation (sweep B)

- **Hall, PRL 74:3307 (1995)** information exclusion: I_X + I_P ≤
  log₂(ΔXΔP/ℏ) — nearest in *shape* (rearranges to a spread-product floored by
  2^(information)); quantum overlaps, accessible-information sums, no rate, no
  distortions. Refinements: Coles–Piani PRA 89:022112 (2014); Zhang et al. Sci.
  Rep. 6:30440 (2016). **No rate-constrained exclusion relation found.**
- **Berta et al., Nature Physics 6:659 (2010)** memory-assisted entropic UR:
  side information relaxes the floor via H(A|B) — the conceptual parallel of
  κ → κ_S; entropy-sum form, quantum overlap constant.
- **Dembo–Cover–Thomas (IEEE T-IT 37:1501, 1991)** Fisher/Stam route to
  Weyl–Heisenberg: no coding rate anywhere in the line.
- **Safaryan–Shulgin–Richtárik (Inf. Inference 2022, arXiv:2002.08958)**: a
  genuine classical bits-vs-distortion "uncertainty principle" for ONE
  compressed vector; no two observables, no incompatibility functional.
- **Donoho–Stark / Elad–Bruckstein**: support-product bounds, no bit-budget
  versions found. Quantum rate-distortion (Datta–Hsieh–Wilde 2013): no
  product-of-distortions floor for incompatible observables found.

## Thermodynamics delineation (sweep C)

- **Name-collision disclaimer required and added:** Theorem 4 is NOT a
  thermodynamic uncertainty relation in the Barato–Seifert sense (PRL
  114:158101, 2015 — current fluctuations vs entropy production in NESS).
- Groisman–Popescu–Winter (PRA 72:032317, 2005): erasing *correlations* costs
  I(A;B) — different object. Still ("thermodynamics of prediction" PRL 2012;
  PRL 124:050601, 2020): dissipation ≥ retained non-predictive information —
  same moral, one implicit consumer, no side information at the eraser, no
  product floor. Kolchinsky–Wolpert semantic-information line: no multi-consumer
  erasure pricing found (2018–2026).
- **Open follow-up (flagged in the note's §7 and STATUS):**
  Kastner–Schlatter, "Entropy Cost of 'Erasure' in Physically Irreversible
  Processes," Mathematics 12(2):206 (2024) — the only found item pairing
  complementarity with erasure cost. Full text 403-blocked; snippet indicates a
  qualitative quantum-foundations argument (position-information compression
  paid in momentum-entropy), no quantitative floor. **Read the full text before
  submission.** Also paywalled: Anderson's Springer chapter (verdict from
  secondary sources).

## Query coverage

~80 distinct WebSearch queries + ~25 direct fetches across the four sweeps
(full query lists in the session transcript, reproduced in each agent report).
Coverage limits: English-language, web-indexed; the natural tightening before
journal submission is a citation-graph pass on Berta et al. 2018, Still 2020,
and Chen et al. 2026, plus primary retrieval of Xiao–Luo 2005.

## Consequences applied to the manuscript (v0.3)

- Abstract rewritten: rate side explicitly attributed ("we claim no novelty for
  it"); contributions restated as (1) tax quantity, (2) packaging, (3) work
  side.
- §3 opens with the attribution paragraph; Thm. 1 retitled "…; classical after
  reduction"; Prop. 2 retitled "…; transport of [XL05, LT10, SCC21]".
- §6 Interpretation: NOVELTY-CHECK replaced with the Hall/Berta/DCT/Safaryan
  delineation.
- §7 Delineation: new governing paragraph (individual-fidelity literature), new
  thermodynamics paragraph (incl. TUR disclaimer and the Kastner–Schlatter
  flag); two-observer paragraph rescoped.
- 12 references added (Gray 73; Xiao–Luo 05; Lapidoth–Tinguely 10; Nayak et al.
  08; Stylianou et al. 21; Chen et al. 26; Nguyen et al. 25; Berta et al. 10;
  Safaryan et al. 22; del Rio et al. 11; BBMW 18; Barato–Seifert 15).
