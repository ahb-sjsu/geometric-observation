# Observation Theory: novelty assessment and the foundational paper

Date: 2026-10-01. Scope: the whole programme, read from its own documents.

## Sources and method

The repositories read were:

- **geometric-observation:** the Volume 14 monograph (ch01–ch23 and appendices), `claims/LEDGER.md`, `crucible/DECLARATION-V1.md`, and every manuscript in `paper/`.
- **observation-theory-campaigns:** 29 campaign tracks, the encyclopedia (310 entries), and the Lean proofs.
- **observation-data-mining:** the textbook and about 650 Lean theorems.
- **readscope:** SPEC, CALIBRATION, and PRINCIPLES.
- **geometric-evaluation-theory, geometric-methods, discovery-philosophy-engineering:** read for their relationship to OT.

Five independent read-only reviews inventoried every theorem-level claim. Each claim got its evidence status and a first-pass literature check. I then read the decisive priors from the primary sources:

- Villard and Piantanida, *IEEE Trans. Inf. Theory* 59(6), 2013 (arXiv:1105.1658): Sections II–III and V.
- Ekrem and Ulukus, *IEEE Trans. Inf. Theory* 59(9), 2013 (arXiv:1108.3544): Sections 1–3.

Novelty verdicts below mean "no prior found after a search". They are not proofs of absence.

## Bottom line

1. **As components, OT is mostly classical mathematics under new names.** The read operator is the active-subspace matrix. Consumer-relative rate–distortion is Sakrison's weighted rate–distortion, or indirect source coding. The flip is the premise of task-based quantization. Conditional Landauer work is del Rio et al. (2011). Many of these parents are uncited in the monograph and the textbook, and that pattern is what sank the July synthesis submission (IT-26-0996).
2. **The synthesis is genuinely productive where it generates theorems.** It does so in one place above all. The question OT keeps asking is who observes what and who pays the cost of a description. Asked of Gaussian sources, it produced results the parent literatures do not have.
3. **The strongest result's coordinate already has a standard name.** Under a deterministic encoder, H(Xⁿ|M,Sⁿ) = H(Xⁿ|Sⁿ) − H(M|Sⁿ). So the programme's "conditional content" or "conditional work", H(M|Sⁿ)/n, is the *conditional leakage* I(Xⁿ;M|Sⁿ)/n of secure source coding. Minimizing it is the same optimization as maximizing the eavesdropper's equivocation. Two consequences follow:
   - The discrete rate–content region (Paper V and Theorem 6 of the scalar T-IT paper) is Villard–Piantanida 2013, Theorem 3, with no decoder side information and U = V.
   - The vector Gaussian content endpoint is close to Ekrem–Ulukus 2013, Theorem 5. Their theorem uses a matrix distortion on the whole source and Gaussian decoder side information, so it does not cover our case directly.
4. **This is good news if it is stated plainly.** Ekrem and Ulukus write that they "have been unable to solve" the joint rate–leakage problem L(μ₁, μ₂) (their p. 8). The programme's Gaussian results solve that problem in the case without decoder side information, with an informed encoder and an arbitrary weighted distortion. The solution is explicit and has structure the parent literature lacks. That is the foundational paper.

## What is new (theorem level), ranked

| # | Result | Where | Evidence | Verdict |
|---|---|---|---|---|
| 1 | The exact Gaussian rate–leakage region with an informed encoder (it observes the described variable and a correlated context) and no decoder side information. Includes the closed form ½log₂g★, the two-noise-fraction frontier, misalignment (the rate-optimal and leakage-optimal descriptions differ iff 0<ρ²<1, with an unbounded gap at the clean boundary), and non-determination by the law of (Y,S) | `paper/tit-cr-context` | proved; numerical and Lean checks; four review passes | **New**. It solves the no-decoder-side-information case of the problem Ekrem–Ulukus left open. The Gaussian optimality of the endpoint is close to their Theorem 5 and must be credited |
| 2 | Pencil characterization: the endpoint is 1+Δ/μ_max of a matrix pencil, which gives the vector-context function explicitly | `tit-cr-context`, Prop. 24 | proved; verified | **New** |
| 3 | Vector structure: both coordinates convex in the error covariance (the whole frontier is a convex program); the endpoint as a max-det program; the one-dimensional regime in closed form with a certificate; the leakage-optimal read direction turns with the distortion budget unless aligned; the parallel allocation is not water-filling (activation order σ²(1+ρ²/τ²)) | `paper/tit-vector-described` | proved; two referee passes; verified | **New** (the covariance device is standard and credited) |
| 4 | GO-16 adversarial observer: linear revelation cost, partition and spectral-tie theorem, binary twin | `paper/go16-adversarial-observer.tex` | proved; Lean lemmas | **New** per its sweep. The SDP reduction is Sayin–Akyol–Başar and Tamura. Fits IEEE TAC or a game-theory venue, not T-IT |
| 5 | GO-10 work-side identity: discount = I(·;S) | `paper/complementarity-tax.tex` | proved | Small. The rate side is Gray / Xiao–Luo. Fold into 1 |
| 6 | Identifying a read operator from threshold queries: one radius fixes it only up to a one-parameter pencil, two radii fix it exactly | GET `articles/2026-09-09-identifiability-at-a-budget.md` | proved, not in Lean | Unclear. An IT paper would need sample complexity and noise |
| 7 | Dynamic and causal extensions (GO-12, GO-14) | `paper/go12*`, `go14*` | partly proved, partly bracketed | Unclear. GO-14 still owes a sweep against causal conditioning (Kramer) and nonanticipative rate–distortion (Charalambous, Stavrou) |

## What is known or renamed: the credit list a submission needs

| OT term or claim | Classical name and source | Cited in OT now? |
|---|---|---|
| read operator P_C = E[JᵀGJ] | active-subspace matrix (Constantine, Dow & Wang 2014; Constantine 2015); expected gradient outer product / outer product of gradients (Xia et al. 2002; Hristache et al. 2001); pullback metric (Rao, Amari) | encyclopedia yes; monograph and textbook **no** |
| consumer-relative R_C(D), weighted water-filling | weighted-MSE rate–distortion (Sakrison 1968); indirect/remote source coding (Dobrushin–Tsybakov 1962; Wolf–Ziv 1970; Witsenhausen 1980); reverse water-filling (Kolmogorov 1956; Berger 1971) | water-filling yes; Sakrison and indirect coding **no** |
| read distortion tr(P_C Σ_δ), the flip | Hessian- or sensitivity-weighted distortion (Choi et al. 2017; HAWQ, Dong et al. 2019–20; OBS/GPTQ); task-based quantization (Shlezinger, Eldar & Rodrigues 2019) | **no** |
| conditional content / conditional work H(M\|Sⁿ)/n | conditional leakage I(Xⁿ;M\|Sⁿ)/n = H(Xⁿ\|Sⁿ)/n − source equivocation; the rate–distortion–equivocation region (Villard–Piantanida 2013); vector Gaussian (Ekrem–Ulukus 2013) | Ekrem–Ulukus only in GO-11; Villard–Piantanida mis-delineated in the T-IT paper |
| conditional Landauer work | erasure work with side information (del Rio, Åberg, Renner, Dahlsten & Vedral 2011; Sagawa–Ueda; Wolf ISIT 2017) | papers yes; textbook **no** |
| budget cliff (OT-3) | not identifiable outside the queried span; adaptive-sensing and matrix-query lower bounds (Arias-Castro, Candès & Davenport; Simchowitz, El Alaoui & Recht 2018; Rashtchian, Woodruff & Zhu 2020); zeroth-order dimension dependence (Duchi et al., T-IT 2015) | **no** |
| two-observer refinability | Gaussian successive refinement (Equitz–Cover 1991; Nayak, Tuncel, Gündüz & Erkip, T-IT 2010; Op 't Veld & Gastpar) | Equitz–Cover yes; Nayak et al. and Op 't Veld–Gastpar **no** |
| alignment κ | matrix cosine / kernel alignment (Cristianini et al. 2002) | no |
| front law p = 4 | Davis–Kahan | yes |
| directional staleness trigger | weighted event-triggered estimation (Trimpe–D'Andrea); L-optimal design | partly |
| GET semiorder threshold; hull law; representability; grid channel; incompatibility | Luce 1956 / Scott–Suppes 1958; quasiconvexity; Xu & Davenport 2020 / metric learning; subtractive dither (Roberts; Schuchman); Ky Fan / common principal components (Flury 1984) | partly |
| law.txt | rational inattention (Sims) | — |

## Corrections owed (found in this assessment)

1. **Scalar T-IT paper:** its related work says the secrecy line "prices the equivocation of the source and seeks to make it large" and that "its encoder does not observe the clean context". Both are wrong: by the identity above the problems coincide, and the source alphabet can be augmented. Credit Villard–Piantanida Theorem 3 for the discrete region and Ekrem–Ulukus Theorem 5 for the Gaussian endpoint. `NOVELTY-SWEEP.md` §3 is wrong for the same reason.
2. **Monograph:** the B4 statement "refinable iff P₁ ⪯ P₂" (ch07:58, App B:66, App A:31, App F:39, OBSERVATION.md:15) disagrees with `two-observer-theorem.tex` ("iff Σ★(P₂,D₂) ⪯ Σ★(P₁,D₁)"). Chapters ch01–ch18 predate v1.0 and the ledger. Appendix A omits the parents listed above.
3. **LEDGER.md:** the GO-14 row is broken by a backslash corruption (`\r` in `\rho` became a carriage return). Theorem rows carry empirical labels such as `[replicated]` that a theory reader will misread.
4. **DPE Proposition 3:** the "only if" half was false. **Fixed and pushed today (a57cf04).**
5. **Paper V:** its region is Villard–Piantanida Theorem 3 with C = ∅, up to a constant. Its contribution is the operational (thermodynamic) reading and the Gaussian corners, and it should say so.

## Is the synthesis novel?

Yes, in the sense that matters, but only where it produces a theorem the parts do not. "The cost of a description is relative to who observes what" is OT's central claim. In classical terms it says this:

> One description carries one rate, paid by its decoder, and as many conditional leakages as there are parties holding different side information, and the encoder's observations decide how those costs trade off.

Stated that way, it produced:

- the non-determination theorem
- the misalignment dichotomy
- the pencil
- the budget-dependent read direction, which no single fixed-geometry observer (principal components, reverse water-filling, the Gaussian information bottleneck) reproduces

None of these was a question in the parent literatures. That is a real synthesis contribution, and it has to be demonstrated by those theorems in classical language, not asserted in OT vocabulary.

## The foundational paper

**Working title:** *Rate, Leakage, and Distortion for Gaussian Sources with an Informed Encoder.*

**Problem.** The encoder observes a jointly Gaussian source T = (Y, V): the described vector and a context. The decoder sees the description alone, under a weighted quadratic distortion E[(Y−Ŷ)ᵀW(Y−Ŷ)] ≤ D. A second party holds S = HT + U and never decodes. Two costs are tracked: the rate, and the conditional leakage to the holder I(Tⁿ;M|Sⁿ)/n. The leakage reads both as secrecy (the eavesdropper's equivocation) and as the holder's re-encoding cost.

**Results:**

- the coding theorem: Villard–Piantanida for the discrete case, credited, plus a direct Gaussian proof
- the error-covariance form, in which both costs are convex, so the full frontier is a convex program; the leakage endpoint is a max-det program
- the one-dimensional regime in closed form via a pencil, with a certificate
- the turning theorem for general weights and side-information maps
- non-reducibility to any single fixed-geometry observer
- the parallel allocation
- the scalar closed form, the misalignment dichotomy and non-determination as corollaries

**Positioning.** It solves the no-decoder-side-information case of the rate–leakage problem that Ekrem and Ulukus could not solve, for every weight and side-information map, and exhibits structure the problem was not known to have.

**What a strong accept needs:**

- the credits above, stated in the first pages
- a full proof of the Gaussian coding theorem
- the general turning theorem verified numerically
- one figure showing the turning read
- length held near 25 pages

**Relation to the two drafts.** This paper subsumes the vector companion and the Gaussian core of the scalar paper. If it goes to T-IT, the scalar paper should not go separately as written. Its binary frontier can become a short separate note, or an appendix.

## Terminology map (to apply across the work)

| Retire | Use | Note |
|---|---|---|
| conditional content / conditional (Landauer) work, L | conditional leakage I(Xⁿ;M\|Sⁿ)/n (equivalently, H(Xⁿ\|Sⁿ)/n minus the equivocation) | keep "re-encoding cost at the holder" as the operational reading |
| content-optimal | leakage-optimal | |
| third party, consumer of S | side-information holder (or eavesdropper in secrecy framing) | |
| consumer | decoder, or downstream task / estimator | "consumer" is acceptable only in the OT papers, with its definition |
| read operator P_C | active-subspace (gradient outer-product) matrix; in coding, the distortion weight matrix W | cite Constantine; in IT papers write W |
| read distortion tr(P_C Σ_δ) | weighted (sensitivity-weighted) mean squared error | cite Sakrison; task-based quantization |
| consumer-relative R_C(D) | weighted / indirect rate–distortion function | cite Sakrison; Wolf–Ziv |
| observer triple (C,G,B) | (task map, output metric, budget) | OT papers only, with the definition |
| resolution budget | rank or rate constraint | |
| budget cliff | identifiability limit of confined probes | cite the query lower bounds |
| flip | ranking reversal between reconstruction error and task loss | cite task-based quantization |
| blind probe | finite-difference active-subspace estimation | cite Constantine |
| quotient (by the read operator) | quotient by the kernel of the gradient outer-product matrix | |
