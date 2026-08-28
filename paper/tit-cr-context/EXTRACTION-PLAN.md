# T-IT extraction plan â€” "The Common-Reconstruction Rateâ€“Distortion Function with Noisy Context"

**Created 2026-08-26, after the T-IT rejection of the Paper III synthesis.**
Target: IEEE Transactions on Information Theory (rolling submission, no
deadline pressure; expect a 12â€“24 month review cycle). This is the program's
"best shot" paper: a single new rateâ€“distortion object in the classical genre,
extracted from `../go11-conditional-region.tex` (v0.11) with the operational
layer imported from `../consumer-relative-landauer.tex` (Paper V).

## The paper in one paragraph

An encoder observes a Gaussian pair (Y, V) and describes Y for a consumer that
sees only the description. A third party holds a noisy, possibly stale copy
S = V + U of the context V. Neither the encoder's consumer nor the encoder
uses S; S prices the description's conditional content I(X; XÌ‚ | S), the
Landauer cost of resetting the record against what the third party retains.
We characterize the minimal conditional content at consumer distortion D: a
closed form Â½logâ‚‚ g* with g* the larger root of an explicit quadratic, in any
ambient dimension (pair sufficiency); the exact rateâ€“content region with its
two-water-level frontier and the misalignment theorem (a strict tradeoff opens
iff the context is misaligned with the read); vector context; the work-floor
attainment iff; and the complete binary (DSBS + BSC context) solution with an
elementary proof. The function recovers the classical RDF, Gray's conditional
RDF, and Steinberg's common-reconstruction function as degenerations, and is
provably NOT a functional of the (Y, S) joint law alone: the encoder's access
to V is load-bearing.

## The novelty claim, sharpened by today's sweeps

The single-letter functional min I(X; XÌ‚ | S) under the Markov chain
XÌ‚ â€“ X â€“ S is Steinberg's common-reconstruction RDF **when the encoder sees
only the reproduced source**. Our object differs in one structural respect
that changes the function: the encoder observes the pair (Y, V) and reproduces
Y, so the encoder holds side information (the clean context) that neither
decoder nor conditioner has. GO-11 Cor. 2 exhibits two instances with the SAME
(Y, S) joint law and DIFFERENT values of L â€” the proof that this is not
Steinberg's function, not Gray's, and not a re-parameterization of either.
That corollary is the paper's delineation centerpiece; lead with it.

**Binary prior-art sweep (2026-08-26, this session):** Steinberg's
"Coding and common reconstruction" (IEEE T-IT 55(11), 2009,
doi:10.1109/TIT.2009.2030487) is the operational CR framework, and the
Heegardâ€“Berger/cascade-with-CR literature (arXiv:1112.1762) carries explicit
DSBS/Hamming CR calculations â€” all in the DECODER-side-information setting.
No published binary CR-type function with (i) encoder pair access and (ii) a
third-party BSC-noised conditioner was found. OWED before final wording: an
institutional read of Steinberg 2009's binary example and of arXiv:1112.1762's
DSBS calculation to confirm neither contains the q-interpolated object; also
re-run the sweep at submission time (house rule).

## Source â†’ target mapping

| Paper section | Source | Work needed |
|---|---|---|
| I. Introduction | new | Write fresh in house voice. Lead: the object, the closed form, the three anchors, the not-a-functional-of-(Y,S) corollary. NO program language (no "Observation Theory", no read operators beyond one paragraph, no registry IDs). |
| II. Problem formulation + operational theorem | Paper V Â§II + Thm 1 (proved, R-IND-5 0-error) | Import the block-coding definitions (R_n, L_n = H(M|Sâ¿)/n) and the region coding theorem with its converse + WZ-binning achievability, restated for the (Y,V) encoder. Verify the restatement changes nothing in the proof (encoder map f_n(Xâ¿) already allows it). This makes the paper self-contained; cite Paper V's Zenodo DOI for provenance, do not depend on it. |
| III. Pair sufficiency | go11 Thm 1 (full proof, clean) | Transplant nearly verbatim. |
| IV. The function: scalar context | go11 Thm 2 (closed form; converse COMPRESSED) + Prop 1 (marginalization dichotomy, full) | **PROOF DEBT 1:** write out the converse's determinant identity and the (a,b) linear system in full; the current text asserts them and outsources detail to a NOVELTY.md addendum. |
| V. The rateâ€“content region + misalignment | go11 Thm 3 (frontier; sketch-grade) + Cor 1 (misalignment) + Prop 2 (interior uniqueness, compressed) | **PROOF DEBT 2:** Thm 3's two determinant identities and the four-gradient reduction, in full. Prop 2's matrix-convexity lemma written out. |
| VI. Work-floor attainment | go11 Thm 6 (full proof, strongest Gaussian argument) | Transplant; light editing. |
| VII. Vector context | go11 Thm 7 (explicitly a sketch) | **PROOF DEBT 3:** the FOC derivation at vector S, full. (If it resists, scope the paper to scalar S + binary and move vector S to a remark; the paper stands without it.) |
| VIII. The binary solution | go11 Thm 10 (full elementary proof, the best in the corpus) | Transplant. Add the delineation paragraph vs Steinberg/HB-CR binary calculations (owed sweep above). |
| IX. Discussion | new | Anchors recovered; what is open (m=2 region â†’ cite as future work, do NOT include Thms 5/9 â€” they are necessary-condition results and would soften the paper; higher-rank reads likewise out). One paragraph on the Landauer reading (Paper V), one sentence on the program, nothing more. |
| Appendix | single-letterization from Paper V App. A | Import. |

**Deliberately EXCLUDED from this paper** (keep it clean): the m=2 region and
matrix water levels (Thms 5/9 â€” necessary conditions only), higher-rank reads
(Thm 8 â€” partial), the complementarity tax (its own note), everything
spectral/dynamic (GO-12/13 â€” the sequel paper once the Toeplitz lemmas are
proved), all empirical/campaign material.

## Citation spine (verify each against the primary record before submission)

Load-bearing and currently MISSING from go11's bibliography:
- R. M. Gray, "Conditional rate-distortion theory," Stanford ISL TR 6502-2,
  1972; and "A new class of lower bounds to information rates of stationary
  sources via conditional rate-distortion functions," IEEE T-IT 19(4), 1973.
- Y. Steinberg, "Coding and common reconstruction," IEEE T-IT 55(11), 2009.
- A. Lapidoth, A. MalÃ¤r, M. Wigger â€” the scalar Gaussian CR function with
  general jointly Gaussian SI (verify exact venue/year; likely T-IT 2014).
- S. Xiao, Z.-Q. Luo (2005) â€” bivariate Gaussian individual-distortion RDF.
- A. Wyner, J. Ziv (1976) â€” decoder SI; delineate (our decoder has none).
- A. Kaspi (1994) â€” encoder side information; delineate (structurally closest:
  our encoder's V access is Kaspi-flavored; cite properly, currently uncited).
- C. Heegard, T. Berger (1985); the CR-constrained HB/cascade line
  (arXiv:1112.1762, verify published venue/authors).
- Nayakâ€“Tuncelâ€“GÃ¼ndÃ¼zâ€“Erkip (2008/2010); Stylianouâ€“Charalambousâ€“Charalambous;
  Lapidothâ€“Tinguely (2010) â€” as in the tax note's attributions.
- Berger 1971 (coding theorem lineage), Shannon 1959.
Delineation non-citations to add per Paper III's rejection lessons: task-based
quantization (Shlezingerâ€“Eldar), semantic/goal-oriented (GÃ¼ndÃ¼z et al. survey),
information bottleneck â€” one paragraph, precise, no containment claims.

## Style and hygiene (house rules + T-IT norms)

- IEEEtran, single shared theorem counter, notation table up front.
- Fix the overloads: u (read direction vs whitened coefficient), m (consumer
  count vs scalar in Thm 3's system), s (1+Ï„Â² vs Ï„Â²/(1+Ï„Â²) vs Schur pivot).
  Rename: the Thm-3 scalar m â†’ Î¼_c; the tax-note sÂ² convention does not enter
  this paper; whitened coefficient u â†’ c.
- Kill "cubic family" (the polynomial is quadratic); label eq:quadratic stays.
- Strip ALL governance register (prereg IDs, R-IND-5 language, seeds) from the
  body; one Reproducibility paragraph at the end pointing at the repo + DOI
  with harness names, in the Paper V style.
- Numerical verification digests move to a short "Numerical verification"
  subsection or appendix table (T-IT tolerates this; Paper V's pattern).
- Abstract â‰¤ 250 words, plain declarative, no program vocabulary.
- No em-dashes in prose. Short sentences. Hedges as facts.

## Verification obligations before submission (house discipline)

1. R-IND-5 fresh-context derivation pass on the three closed converses
   (PROOF DEBTS 1â€“3) once written â€” they are new prose even if the math is
   settled; the pass gates assertion.
2. C3-style harness re-run tying every quoted number to
   `results/*.json` (existing harnesses 060/063/064 cover Thms 1â€“10; add the
   restated operational theorem to the harness list only if its statement
   changed materially).
3. The owed binary delineation reads (Steinberg 2009 Â§binary; 1112.1762 DSBS).
4. Full-sweep refresh at submission (arXiv + DBLP + the two library pulls).
5. Lean: OPTIONAL but high-value â€” the binary Thm 10 tilt-equation algebra and
   the quadratic-root uniqueness are elementary and would formalize cheaply;
   a "machine-checked" line strengthens a T-IT submission materially.

## Staging

1. **M1 (skeleton):** IEEEtran manuscript with Â§Â§Iâ€“III, VI, VIII transplanted
   (the already-full proofs), Â§Â§IVâ€“V, VII stubbed with the debts marked.
2. **M2 (converse closure):** write PROOF DEBTS 1â€“3; R-IND-5 pass on each.
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
  pass â€” CONFIRMED (no errors, no overclaims); the 2 GAPs (Wyner-import
  conditions enumerated and verified; Ï„=0 rate-side closed via the Î›-free
  Î±=1 uniqueness plus CramÃ©r decomposition) and 4 NITs (finiteness line,
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
  identity (gâˆ’1)(Dâˆ’h) âˆ’ Qâ‚ = (gâˆ’1)P(g)/(gk), cor:anchors, thm:region with
  both determinant identities + four gradient identities + two-water-level
  reduction, lem:mxconvex written out, prop:uniq STRENGTHENED to Î±âˆˆ[0,1],
  cor:misalign full, cor:notmarginal PROVED with exact surds, thm:vector
  closed at full rigor (not demoted). `verify_converses.py` 12/12 PASS.
  **Fresh-context adversarial verification (independent agent, forbidden from
  all sources, own scripts): CONFIRMED â€” no errors, no gaps, no overclaims;
  46 symbolic + 46 numeric checks pass** (`verifier_sym_checks.py`,
  `verifier_num_checks.py`, archived here). Four exposition NITs folded in
  same day (h=âˆ’âˆž convention; endpoint-weight scalarization wording;
  regular-conditional-probability clause; cor:notmarginal Ï„Â²=0 boundary
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
- **M4 (2026-08-27): DONE.** (1) Result-role labeling: "Results at a glance"
  table (Table I) early in the intro, role words in ten bracketed titles
  (Core: thm:function/region/binary; Consequence: cor:misalign+
  rem:cleanboundary, thm:floor, cor:notmarginal; Extension: thm:vector,
  thm:gaussop; Anchor: cor:anchors, prop:marg + the IB identity), roadmap
  rewritten to walk the roles. (2) Novelty strengthening: "What is new"
  subsection with the six-row theorem-level comparison table (Table II:
  vs Steinberg 2009 / LMW 2014 / GIB 2005 / Xiao-Luo+Chen / Steinberg-
  binary+Ahmadi; every prior-column claim matches what was verified) and
  the four direct answers (reduction-vs-evaluation, operational theorem is
  mathematics, classical machinery vs new objects, no two-coupled-level
  water-filling and no such quadratic in the cited literature); related-
  work duplication trimmed to a table pointer. (3) Polish: notation table
  at end of Sec. II; abstract at 249 rendered words, no verification
  claims; header compressed to a STATUS block; 1pt psi-display overfull
  fixed (qquad->quad); zero em-dashes / % verify flags / program vocab
  (single "consumer" = cited title). (4) cover-letter-tit.tex written and
  built (1 page): contributions by role, frank paragraph on the rejected
  synthesis (different single-object work, no shared theorems, standard
  vocabulary adopted), Zenodo-record relationship (supersedes its source-
  coding content), verification apparatus sentence, standard statements.
  Manuscript: 29 pp, zero undefined refs, zero overfull.
- **M4b (2026-08-27): final fix round** (third verification pass, verdict
  submit-ready, + new reviewer set): V1 limsup-D_n closure sentences added
  to both operational converses; V2/V3 cover-letter overclaim fixed ("two
  written independently") + declined-submission vs Zenodo-record
  distinctness made explicit; V4 nits (markboth draft tag, shannon1959
  cited, ALL internal comments stripped from the tex, abstract quadratic
  wording "(D, rho^2, tau^2)", Table-I floor row, per-bin packing-threshold
  wording, in-bin check moved to App C, rho^2->1 reverse-channel clause).
  R1 problem-in-one-box Definition + Gaussian-scope handoff sentence +
  Yhat^n sweep in the Gaussian appendix; R2 one-clause recaps at every
  cross-section lemma invocation in Secs. VI-VII; R3 Fig-2 pointer in
  cor:misalign statement + NEW Fig. 3 (plot_binary.py at p,q,D=
  0.25,0.15,0.15: tilt root d0*=0.1173, d1*=0.2480, L*=0.3346 bits, one
  sign change); R4 s-scope note in notation table, pCov zero-term dropped
  with the Gaussian-conditional-mean clause, (44)-bracket invertibility
  confirmed present. Manuscript 30 pp, cover letter 1 p, zero undefined,
  zero overfull; verify_converses.py 16/16.
- **M5 (2026-08-27): MINOR REVISION round applied** (external review:
  "technical core appears sound"): App. B quantizers made explicit (nested
  saturating dyadic family, sigma-fields to Borel, Pinsker Ch. 2 monotone
  convergence) + cell-bound lemma PROVED (inf/sup density-ratio on bounded
  cells, Mills-type tails, clipped-rectangle bound for vector S) closing
  the Wyner integrability import + closedness/right-continuity made
  self-contained in the appendix; Fig. 1 corrected (M-branch into the
  reset mechanism, relabeled "accesses M, retains S^n", caption + Sec. II
  prose aligned); endpoint symbols renamed L_R*(D)/R_L*(D) throughout
  (cor:misalign, rem:cleanboundary, Fig. 2 labels regenerated via
  plot_frontier.py, notation-table row added); dimension claim narrowed
  everywhere to "Y and V scalar linear functionals of an
  arbitrary-dimensional jointly Gaussian source"; "What is new" recast as
  neutral "Relation to prior formulations" with to-our-knowledge
  softening; Table I (results-at-a-glance) folded into the roadmap prose;
  App. C compressed to one paragraph + table, full inventory moved to
  VERIFICATION.md (new); Chen et al. checked — still no IEEE
  volume/pages/DOI, bibitem stays "to be published". Manuscript 31 pp,
  zero undefined, zero overfull; verify_converses.py 16/16.
- **M6 (2026-08-27): camera-ready deltas** — binary Pareto frontier: the
  sigma-symmetrization extension to the weighted objective PROVED
  (rem:binfrontier: R convex by lem:binconvex with trivial conditioner,
  flip preserves both coordinates, R-minimizer d0=D unique by strict
  concavity, tilt root < D strict for q in (0,1/2)); Fig. 3 third panel at
  (0.1, 0.1, 0.05): d0*=0.0282, L_min=0.4341, R_min=0.7136, excesses
  0.0391/0.0248 bits (binary.pdf/png regenerated, caption quotes script);
  appendix recaps added at every cross-section invocation in app:gaussian;
  Zenodo record made provenance-only (rho^2->1 collapse now proved inline
  via the (a,b,n) limit, two formula cites reduced to steinberg2009);
  Sigma_S = Sigma_V + Sigma_U made explicit in Sec. VII (no s-collision;
  I_r+Sigma_U would presume a normalization the section does not impose).
  Manuscript 32 pp, zero undefined, zero overfull; verify_converses.py
  extended to 17/17 (new N10: binary frontier closed forms vs joint-pmf).
- **M7 (2026-08-27): R-IND-5 pass #5 on the complete 32-pp manuscript —
  CONFIRMED.** Fresh-context adversarial verifier (no prover access):
  re-derived rem:binfrontier end to end (flip invariance, weighted-objective
  convexity, R-minimizer uniqueness, psi(D)<0 sign chain), sympy-verified
  all seven rho^2->1 limits, checked every appendix recap against its
  target, re-ran both plot scripts (all caption numbers exact), swept all
  265 refs post-renumbering (all resolve correctly), brute-forced the
  binary theorem over general 4-parameter channels (family optimum never
  beaten; the one apparent break was the verifier's own soft-penalty
  infeasibility leak). Scripts: 17/17, 46/46 sym, 42/42 num. Six findings,
  all applied: (MINOR) rem:binfrontier constraint-activeness sentence added
  (slack optima slide to the segment: coordinates vanish at (1/2,1/2),
  convexity makes the path non-increasing, distortion rises to 1/2>D);
  (MINOR) VERIFICATION.md numeric count 46->42; (NIT) "nine"->"ten"
  numeric items; (NIT) cor:misalign limit display scoped to rho->1 with
  the rho->-1 sign-of-b clause; (NIT) g^{*}->g^\star in abstract+intro;
  (NIT) "decisions consumed by parties"->"descriptions read by parties"
  in the Discussion. Rebuilt clean: 32 pp, zero undefined, zero overfull.
- **M8 (2026-08-27): mock T-IT review round (Weak Accept, clarity 7.5)** —
  proof-architecture roadmap before Thm 4 (six steps, WZ-confusion
  preempted; proof itself untouched per freeze); abstract + Sec. I
  restructured so the trio leads (closed form / region+misalignment /
  non-determination; role brackets updated: cor:misalign + cor:notmarginal
  -> Core, thm:binary -> Extension); Landauer demoted to interpretation
  (abstract, L_n definition IT-first with "Landauer content" marked as our
  term, thm title -> Rate--content--distortion, work-vocabulary sweep);
  non-determination significance sentence added; reset-model sentence
  written against delrio2011/faist2015 (classical specialization: ideal
  joint ops conditioned on undisturbed classical S^n, only M to standard
  state) + terminology stabilized (third party primary; reset mechanism /
  conditioner defined as synonyms); water-level analogy scoped;
  assumptions-and-degeneracies paragraph in Sec. III; necessity map before
  Thm 20's proof (audit: no gap; tacit h(Z)-finiteness step made
  explicit); binary-section purpose sentences; cor:notmarginal values ->
  Table (surds kept in caption/proof); no-time-sharing mechanism attached
  in statement; "machinery classical" strengthened; frontier magnitudes
  quantified (box maxima 0.1138/0.0770 bits; dR unbounded at the
  tau^2->0, D=1-rho^2 edge, 1.537 bits at (0.5,1e-3,0.5); dL saturates at
  (1/2)log2(1+rho^2)) with new script check N11; box retitled; s named
  the context-noise parameter. NOT done (deliberate): no second Fig-2
  curve; no 15-20% cut; no section moves. 33 pp, 0 undefined, 0 overfull;
  verify_converses.py 18/18.
- **M8b (2026-08-27): Thm-4 audit closeout** — audit verdict SOUND on all
  five probes, freeze lifted; three presentational fixes applied:
  right-continuity/closure prose promoted to standalone
  lem:rightcont (closed, nondecreasing, right-continuous single-letter
  region; three-line compactness proof; converse + theorem statement now
  invoke it in one clause each); Gaussian L(D)'s operational meaning
  co-cited to Sec. II + App. app:gaussian at the intro definition and the
  Discussion thermodynamic-reading sentence; thm:region's opening
  qualified ("single-letter pairs ... which thm:gaussop identifies with
  the operational region"). Also caught and fixed the M8 role-bracket
  miss on cor:notmarginal (now Core). Numbering shifted by one from
  lem:rightcont on: main-region Thm 5, pair Thm 8, exhaustion Lem 10,
  closed form Thm 12, region Thm 14, misalign Cor 17, notmarginal Cor 19,
  cleanctx Lem 20, floor Thm 21, vector Thm 22, binary Thm 25, cell bound
  Lem 27, Gaussian operational Thm 28. 34 pp, 0 undefined, 0 overfull;
  verify_converses.py 18/18.
- **M9 (2026-08-27): reviewer round, three items.** (1) Thermodynamics
  consolidated into ONE numbered remark (rem:thermo, Remark 6, after
  Thm 5): the delrio2011/faist2015 classical-side-information protocol
  sentence moved there, eq:landauer-bound restated as the tight form
  W_n^min = kB T ln2 H(M|S^n) + o(n), "L(D) = least asymptotic erasure
  work per symbol" derived from Thm 5 + Thm 30, scope sentences
  (volatile index only; apparatus not erased) moved in; audit swept the
  rest: intro para-2 + para-3, relation-to-prior, related-work Landauer
  paragraph, Sec-VI floor footnote, thm:gaussop statement, Discussion
  all now POINT at the remark; Thm 5's "physical reset-work coordinate"
  sentence deleted; L_n definition IT-only; "work-only endpoint" ->
  "content-only" (Sec. V opener); abstract's single interpretation
  sentence and the Sec-I motivation paragraph kept (allowed carve-outs).
  (2) cor:notmarginal mechanized: mechanism paragraph after the proof
  (common Corr(Y,S) = rho/sqrt(s) = 1/sqrt2; L depends on (rho^2,tau^2)
  separately, not through rho^2/s; encoder acts on (Y,V) not (Y,S));
  Corr(Y,S) column added to tab:notmarginal; NEW Fig. 3
  (plot_notmarginal.py, house style): L(D) vs D for both instances,
  gaps 0.0495 bits at D=0.1 and 0.1543 at D=0.3 (script-printed,
  caption-quoted); binary figure shifts to Fig. 4. (3) Anchor
  convergence rates (rem:anchorrates, Remark 15, after cor:anchors),
  sympy-derived FIRST by implicit differentiation at the simple root
  (dg/de = -P_e/P_g), all linear: rho^2->0 gap to classical RDF =
  -(1-D)/(2 ln2 (s-D)) * rho^2 (from below); tau^2->0 gap to Gray =
  rho^2/(2 ln2 (1-rho^2-D)) * tau^2 for D<1-rho^2 (coefficient diverges
  at the double root D=1-rho^2; far branch D>1-rho^2 has L itself
  linear with coeff (1-D)/(2 ln2 (D-(1-rho^2)))); rho^2->1 gap to
  Steinberg = tau^2(1-D)/(2 ln2 (D+tau^2)^2) * (1-rho^2). New check
  N12 (symbolic exact + numeric ratios to 8.0e-4); verify_converses.py
  19/19; appendix Table row added; VERIFICATION.md updated. Numbering
  shifted: rem:thermo=6 pushes 7+, rem:anchorrates=15 pushes 16+; new
  landmark map: Lem 4 rightcont, Thm 5 main-region, Rem 6 thermo,
  Thm 9 pair, Prop 10 marg, Lem 11 gauss, Thm 13 function, Cor 14
  anchors, Rem 15 anchorrates, Thm 16 region, Cor 19 misalign, Cor 21
  notmarginal, Thm 23 floor, Thm 24 vector, Thm 27 binary, Rem 28
  binfrontier, Lem 29 cellbound, Thm 30 gaussop. 35 pp, zero
  undefined, zero overfull.
- **REMAINING (owner items only):** Steinberg 2009 + Lu et al. WCSP 2016
  primary reads; the reviewer's Sec-VI split-out suggestion (owner
  decision); submission-time full sweep; ScholarOne upload.

