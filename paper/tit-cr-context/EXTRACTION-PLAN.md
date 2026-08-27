# T-IT extraction plan — "The Common-Reconstruction Rate–Distortion Function with Noisy Context"

**Created 2026-08-26, after the T-IT rejection of the Paper III synthesis.**
Target: IEEE Transactions on Information Theory (rolling submission, no
deadline pressure; expect a 12–24 month review cycle). This is the program's
"best shot" paper: a single new rate–distortion object in the classical genre,
extracted from `../go11-conditional-region.tex` (v0.11) with the operational
layer imported from `../consumer-relative-landauer.tex` (Paper V).

## The paper in one paragraph

An encoder observes a Gaussian pair (Y, V) and describes Y for a consumer that
sees only the description. A third party holds a noisy, possibly stale copy
S = V + U of the context V. Neither the encoder's consumer nor the encoder
uses S; S prices the description's conditional content I(X; X̂ | S), the
Landauer cost of resetting the record against what the third party retains.
We characterize the minimal conditional content at consumer distortion D: a
closed form ½log₂ g* with g* the larger root of an explicit quadratic, in any
ambient dimension (pair sufficiency); the exact rate–content region with its
two-water-level frontier and the misalignment theorem (a strict tradeoff opens
iff the context is misaligned with the read); vector context; the work-floor
attainment iff; and the complete binary (DSBS + BSC context) solution with an
elementary proof. The function recovers the classical RDF, Gray's conditional
RDF, and Steinberg's common-reconstruction function as degenerations, and is
provably NOT a functional of the (Y, S) joint law alone: the encoder's access
to V is load-bearing.

## The novelty claim, sharpened by today's sweeps

The single-letter functional min I(X; X̂ | S) under the Markov chain
X̂ – X – S is Steinberg's common-reconstruction RDF **when the encoder sees
only the reproduced source**. Our object differs in one structural respect
that changes the function: the encoder observes the pair (Y, V) and reproduces
Y, so the encoder holds side information (the clean context) that neither
decoder nor conditioner has. GO-11 Cor. 2 exhibits two instances with the SAME
(Y, S) joint law and DIFFERENT values of L — the proof that this is not
Steinberg's function, not Gray's, and not a re-parameterization of either.
That corollary is the paper's delineation centerpiece; lead with it.

**Binary prior-art sweep (2026-08-26, this session):** Steinberg's
"Coding and common reconstruction" (IEEE T-IT 55(11), 2009,
doi:10.1109/TIT.2009.2030487) is the operational CR framework, and the
Heegard–Berger/cascade-with-CR literature (arXiv:1112.1762) carries explicit
DSBS/Hamming CR calculations — all in the DECODER-side-information setting.
No published binary CR-type function with (i) encoder pair access and (ii) a
third-party BSC-noised conditioner was found. OWED before final wording: an
institutional read of Steinberg 2009's binary example and of arXiv:1112.1762's
DSBS calculation to confirm neither contains the q-interpolated object; also
re-run the sweep at submission time (house rule).

## Source → target mapping

| Paper section | Source | Work needed |
|---|---|---|
| I. Introduction | new | Write fresh in house voice. Lead: the object, the closed form, the three anchors, the not-a-functional-of-(Y,S) corollary. NO program language (no "Observation Theory", no read operators beyond one paragraph, no registry IDs). |
| II. Problem formulation + operational theorem | Paper V §II + Thm 1 (proved, R-IND-5 0-error) | Import the block-coding definitions (R_n, L_n = H(M|Sⁿ)/n) and the region coding theorem with its converse + WZ-binning achievability, restated for the (Y,V) encoder. Verify the restatement changes nothing in the proof (encoder map f_n(Xⁿ) already allows it). This makes the paper self-contained; cite Paper V's Zenodo DOI for provenance, do not depend on it. |
| III. Pair sufficiency | go11 Thm 1 (full proof, clean) | Transplant nearly verbatim. |
| IV. The function: scalar context | go11 Thm 2 (closed form; converse COMPRESSED) + Prop 1 (marginalization dichotomy, full) | **PROOF DEBT 1:** write out the converse's determinant identity and the (a,b) linear system in full; the current text asserts them and outsources detail to a NOVELTY.md addendum. |
| V. The rate–content region + misalignment | go11 Thm 3 (frontier; sketch-grade) + Cor 1 (misalignment) + Prop 2 (interior uniqueness, compressed) | **PROOF DEBT 2:** Thm 3's two determinant identities and the four-gradient reduction, in full. Prop 2's matrix-convexity lemma written out. |
| VI. Work-floor attainment | go11 Thm 6 (full proof, strongest Gaussian argument) | Transplant; light editing. |
| VII. Vector context | go11 Thm 7 (explicitly a sketch) | **PROOF DEBT 3:** the FOC derivation at vector S, full. (If it resists, scope the paper to scalar S + binary and move vector S to a remark; the paper stands without it.) |
| VIII. The binary solution | go11 Thm 10 (full elementary proof, the best in the corpus) | Transplant. Add the delineation paragraph vs Steinberg/HB-CR binary calculations (owed sweep above). |
| IX. Discussion | new | Anchors recovered; what is open (m=2 region → cite as future work, do NOT include Thms 5/9 — they are necessary-condition results and would soften the paper; higher-rank reads likewise out). One paragraph on the Landauer reading (Paper V), one sentence on the program, nothing more. |
| Appendix | single-letterization from Paper V App. A | Import. |

**Deliberately EXCLUDED from this paper** (keep it clean): the m=2 region and
matrix water levels (Thms 5/9 — necessary conditions only), higher-rank reads
(Thm 8 — partial), the complementarity tax (its own note), everything
spectral/dynamic (GO-12/13 — the sequel paper once the Toeplitz lemmas are
proved), all empirical/campaign material.

## Citation spine (verify each against the primary record before submission)

Load-bearing and currently MISSING from go11's bibliography:
- R. M. Gray, "Conditional rate-distortion theory," Stanford ISL TR 6502-2,
  1972; and "A new class of lower bounds to information rates of stationary
  sources via conditional rate-distortion functions," IEEE T-IT 19(4), 1973.
- Y. Steinberg, "Coding and common reconstruction," IEEE T-IT 55(11), 2009.
- A. Lapidoth, A. Malär, M. Wigger — the scalar Gaussian CR function with
  general jointly Gaussian SI (verify exact venue/year; likely T-IT 2014).
- S. Xiao, Z.-Q. Luo (2005) — bivariate Gaussian individual-distortion RDF.
- A. Wyner, J. Ziv (1976) — decoder SI; delineate (our decoder has none).
- A. Kaspi (1994) — encoder side information; delineate (structurally closest:
  our encoder's V access is Kaspi-flavored; cite properly, currently uncited).
- C. Heegard, T. Berger (1985); the CR-constrained HB/cascade line
  (arXiv:1112.1762, verify published venue/authors).
- Nayak–Tuncel–Gündüz–Erkip (2008/2010); Stylianou–Charalambous–Charalambous;
  Lapidoth–Tinguely (2010) — as in the tax note's attributions.
- Berger 1971 (coding theorem lineage), Shannon 1959.
Delineation non-citations to add per Paper III's rejection lessons: task-based
quantization (Shlezinger–Eldar), semantic/goal-oriented (Gündüz et al. survey),
information bottleneck — one paragraph, precise, no containment claims.

## Style and hygiene (house rules + T-IT norms)

- IEEEtran, single shared theorem counter, notation table up front.
- Fix the overloads: u (read direction vs whitened coefficient), m (consumer
  count vs scalar in Thm 3's system), s (1+τ² vs τ²/(1+τ²) vs Schur pivot).
  Rename: the Thm-3 scalar m → μ_c; the tax-note s² convention does not enter
  this paper; whitened coefficient u → c.
- Kill "cubic family" (the polynomial is quadratic); label eq:quadratic stays.
- Strip ALL governance register (prereg IDs, R-IND-5 language, seeds) from the
  body; one Reproducibility paragraph at the end pointing at the repo + DOI
  with harness names, in the Paper V style.
- Numerical verification digests move to a short "Numerical verification"
  subsection or appendix table (T-IT tolerates this; Paper V's pattern).
- Abstract ≤ 250 words, plain declarative, no program vocabulary.
- No em-dashes in prose. Short sentences. Hedges as facts.

## Verification obligations before submission (house discipline)

1. R-IND-5 fresh-context derivation pass on the three closed converses
   (PROOF DEBTS 1–3) once written — they are new prose even if the math is
   settled; the pass gates assertion.
2. C3-style harness re-run tying every quoted number to
   `results/*.json` (existing harnesses 060/063/064 cover Thms 1–10; add the
   restated operational theorem to the harness list only if its statement
   changed materially).
3. The owed binary delineation reads (Steinberg 2009 §binary; 1112.1762 DSBS).
4. Full-sweep refresh at submission (arXiv + DBLP + the two library pulls).
5. Lean: OPTIONAL but high-value — the binary Thm 10 tilt-equation algebra and
   the quadratic-root uniqueness are elementary and would formalize cheaply;
   a "machine-checked" line strengthens a T-IT submission materially.

## Staging

1. **M1 (skeleton):** IEEEtran manuscript with §§I–III, VI, VIII transplanted
   (the already-full proofs), §§IV–V, VII stubbed with the debts marked.
2. **M2 (converse closure):** write PROOF DEBTS 1–3; R-IND-5 pass on each.
3. **M3 (delineation):** related-work section + binary delineation reads +
   citation verification sweep.
4. **M4 (polish):** notation table, numerical-verification appendix, abstract,
   cover letter (address the Paper III rejection: different object, classical
   genre, self-contained).
5. Owner reviews; owner submits.

Working file: `tit-cr-context.tex` in this directory. Do not modify
`go11-conditional-region.tex` (it stays the program's research log).

## Status log

- 2026-08-27: external-review mathematical repairs verified by fresh-context
  pass — CONFIRMED (no errors, no overclaims); the 2 GAPs (Wyner-import
  conditions enumerated and verified; τ=0 rate-side closed via the Λ-free
  α=1 uniqueness plus Cramér decomposition) and 4 NITs (finiteness line,
  binary convexity lemma hoisted, duplicate label, covering-import wording)
  closed same day. verify_converses.py 16/16.

## Status log

- **M1 (2026-08-26):** skeleton + this plan; binary prior-art sweep run
  (Steinberg 2009 / Ahmadi et al. carry DSBS-CR in the decoder-SI setting;
  third-party-conditioner + encoder-pair-access object not found;
  institutional reads owed).
- **M1b (2026-08-26):** five full-proof transplants in (operational theorem
  with the bounded-distortion scoping made visible; pair sufficiency;
  marginalization dichotomy; floor iff; binary Thm). 8 pp.
- **M2 (2026-08-26): ALL THREE CONVERSE DEBTS CLOSED AT FULL RIGOR.** Prover
  round: lem:gauss (Gaussian exhaustion + determinant identity, shared by
  Secs. IV/V/VI/VII), thm:function full converse with the exact reduction
  identity (g−1)(D−h) − Q₁ = (g−1)P(g)/(gk), cor:anchors, thm:region with
  both determinant identities + four gradient identities + two-water-level
  reduction, lem:mxconvex written out, prop:uniq STRENGTHENED to α∈[0,1],
  cor:misalign full, cor:notmarginal PROVED with exact surds, thm:vector
  closed at full rigor (not demoted). `verify_converses.py` 12/12 PASS.
  **Fresh-context adversarial verification (independent agent, forbidden from
  all sources, own scripts): CONFIRMED — no errors, no gaps, no overclaims;
  46 symbolic + 46 numeric checks pass** (`verifier_sym_checks.py`,
  `verifier_num_checks.py`, archived here). Four exposition NITs folded in
  same day (h=−∞ convention; endpoint-weight scalarization wording;
  regular-conditional-probability clause; cor:notmarginal τ²=0 boundary
  acknowledgment). 18 pp, zero undefined references.
- **M3 (2026-08-26):** related-work subsection written (end of Sec. I);
  binary delineation paragraph written (end of Sec. VIII); every bib entry
  verified against DBLP/arXiv/primary records and all % verify flags
  cleared (fixes: lapidoth2014 real title "Constrained source-coding with
  side information" T-IT 60(6):3218-3237; ahmadi2013 pages 1458-1474;
  xiaoluo2005 J.-J. Xiao, Allerton 2005 pp. 438-447; Kaspi = A. H. Kaspi,
  kept as the encoder-informed-SI cite; Gray 1972 TR 6502-2 added; Berger
  1971 full book title). New entries: nayak2010, stylianou2021,
  shlezinger2019, gunduz2023, tishby1999. 1112.1762 read in full (binary
  CR calculations are all erased-SI, decoder-side); Steinberg 2009 binary
  example (eq. (14), h(rho*D)-h(D), BSC(D) reverse channel) confirmed via
  Vellambi-Timo arXiv:1611.05467 Lemma 9(c) -- PRIMARY read of the
  paywalled T-IT text STILL OWED. Novelty re-sweep clean (no vector-
  Gaussian CR, no third-party-conditioner region, no rate-work region
  2024-2026; nearest adjacent title: Lu-Xu-Zhang-Feng-Wang WCSP 2016
  binary encoder-SI + CR, abstract inaccessible, 2016 so not a
  headline threat -- pull at submission sweep). 19 pp, zero undefined
  references.
- **M3b (2026-08-26):** terminology-defusing pass over the whole manuscript,
  motivated by T-IT's ill-defined-terms complaint on the predecessor paper:
  "consumer"->decoder (0 body uses left), noun "read"->described variable /
  Y coordinate (0 left), noun "record"->description/reproduction (0 left),
  "certificate"->criterion/checks/Lagrangian bounds (0 left); "context"
  formally introduced in abstract + Sec. III; "conditional content" defined
  at first use in abstract and intro (tied to H(M|S^n)/n and I(X;X-hat|S));
  reset mechanism = third party identified in abstract and Sec. II; abstract
  opening rewritten in standard encoder/decoder/description language. 19 pp,
  zero undefined references, no proof mathematics changed.
- **M3c (2026-08-26):** Sec. IX "Discussion and Conclusion" + Appendix B
  "Numerical Verification" written (all table numbers taken from the archived
  script outputs, two of the briefed numbers corrected against them; binary
  Lagrangian row sourced from results/GO11-m2sys-binary.json). 20 pp.
- **M3d (2026-08-26): owner review round applied.** MAJOR 1: Sec. II
  restructured (model paragraph + TikZ Fig. 1 who-sees-what diagram;
  R_min(D) and L(D) defined as displays BEFORE lemma/theorem; work-endpoint
  display moved up); all cross-section theorem forward refs eliminated
  (intro roadmap + related work now cite sections; in-proof thm:region ref
  -> section; the four unavoidable within-Sec.-V refs to prop:uniq /
  cor:misalign marked "below", reordering impossible since prop:uniq needs
  the whitened frame from thm:region's proof). MAJOR 2: prop:uniq convexity
  chain written out (I-W0 strict via n>0; sigma=Q1+n>0; Lambda-W1 strict via
  Q1<sigma; one-line Loewner-monotonicity proof of det; strictness mechanism
  named at the head of each case). MAJOR 3: cor:notmarginal sigma-algebra
  rescaling line + displayed L=(1/2)log2(1/(2D)) for the (1/2,0) instance.
  MAJOR 4: binary symmetrization justified (DSBS fair marginals + independent
  Bern(q) noise flips S with V); shared-channel convexity sentence rewritten
  (input laws depend on s; each I_s convex in the common channel C). MAJOR 5:
  companion-measurement paragraph added to Sec. IX (3 sentences, cites
  bond2026landauer, no equivalence claim). MINORS: hidelinks; s=1+tau^2
  recalled in thm:function statement; 1-rho^2>0 division justified in the
  region FOC; work-floor footnote (Landauer/Bennett/Faist); plot_frontier.py
  written + run (endpoint excesses 0.0400/0.0349 from its own output,
  endpoints tie closed forms at 1e-16), Fig. 2 in Sec. V.
  verify_converses.py re-run: 12/12 PASS. 21 pp, zero undefined references,
  zero errors; only residual overfull is the pre-existing 6.2pt one.
- **M3e (2026-08-26):** machine-check record added to Appendix B only: Lean 4
  module lean/ObservationTheory/CRContext.lean (built clean, zero sorry;
  quadratic/root/anchor/surd/binary-anchor algebra) + MATLAB Symbolic R2026a
  matlab_checks.m (11/11), with the honest-scope sentence on what stays
  written-proof-only; Table I extended by two rows. 21 pp, zero undefined
  references.
- **M3f (2026-08-27): external-review REPOSITIONING round (comments 1, 4, 7 +
  minors).** (1) Novelty reframe adopted fully: title now "Rate-Conditional-
  Content Tradeoffs with Encoder-Observed Context"; LMW Remark 8 verified
  verbatim against the ETH PDF (encoder observations = source augmentation
  with distortion ignoring the extra coordinate) and cited; abstract/intro/
  related-work/cor:notmarginal/Sec-IX rewritten: the functional IS
  Steinberg's on the augmented source, our contribution = conditional-
  erasure reading + closed-form augmented evaluation + joint tradeoff +
  reduced-marginal non-determination; "Steinberg's scalar Gaussian formula
  at the rho^2->1 boundary" wording everywhere; all three %% REPOSITION
  markers discharged with the repaired iff + determinant-lower-bound
  wording. (4) IB identity J_alpha = I(T;Yhat)-(1-alpha)I(S;Yhat) added as a
  display in related work; chechik2005 (JMLR 6:165-188, DBLP-verified)
  added; no-containment phrasing replaced by the precise GIB relationship.
  (7) bond2026landauer delineation paragraph at end of related work
  (preliminary manuscript; Sec.-II theorem + single-letterization + scalar
  corner appeared there; Secs. III+ new; supersedes its source-coding
  content); Sec-IX companion sentence rewritten without the cite; bibitem
  reworded "preliminary manuscript, archived at [same DOI as footnote,
  intentionally one record]". Minors: Fig. 1 reproduction now Yhat^n with
  general-theorem caveat; "possibly stale" removed; Fig. 2 regenerated at
  columnwidth/13pt with label moved inside; Table I merged to 6 rows (Lean
  + MATLAB kept); abstract verification sentence removed and abstract
  tightened. 27 pp, zero undefined refs. NOTE for owner (from reviewer):
  Section VI could be split out if length becomes an issue -- owner's
  decision, not taken.
- **Next: M4** (notation table, abstract polish, cover letter).
