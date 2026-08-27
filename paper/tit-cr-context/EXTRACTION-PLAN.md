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
- **Next: M3** (related work + citation verification + the owed binary
  delineation reads), then M4 (notation table, numerical-verification
  appendix content, abstract polish, cover letter).
