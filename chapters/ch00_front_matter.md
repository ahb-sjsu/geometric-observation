# Geometric Observation
## The Mathematical Structure of What an Observer Can Use

**Volume 14 of the Geometric Series**

Andrew H. Bond
Department of Computer Engineering, San José State University
`andrew.bond@sjsu.edu` · ORCID 0009-0003-2599-6158 · Senior Member, IEEE

---

> *Keep the structure the observer can use.*

---

### Epistemic status of this volume (2026-11-28)

**The framework is defined, its falsifiable core has been measured, and four theorem
rows are `[proved]`.** This is the meta-volume of the series. The domain volumes each
posit one domain's geometry, and this one asks what *any* observer's geometry is made
of. Its answer is a mechanism, the read metric $P_C$, whose consequences were sealed
before measurement, run, and reported as they came out, losses included. This volume
shares a house rule with *Geometric Ethics* and *Geometric Cognition*, the other
volumes that keep claim ledgers. **The book may not assert what the ledger cannot
show.** The ledger is `claims/LEDGER.md`, one row per claim, kept under `CHARTER.md`
and `PROTOCOL.md`. Much of the text is written with an AI assistant, and the charter
forbids the assistant to be the sole grader of its own work. The fresh-context checks
it requires instead are logged in the ledger as verification incidents VI-1 to VI-57.
On the date above the parts of the book stand as follows.

- **The falsifiable core (Chapter 14).** GO-1 to GO-6 were each sealed before their
  runs. GO-4 and the positive half of GO-2 are `[replicated]`. GO-3 and the negative
  half of GO-2 are `[demonstrated]`. GO-1 is `[predicted]` and GO-5 is `[refuted]`.
  GO-6 is `[demonstrated]` and disputed, because its harness charges two of the coders
  a rate outside the matched-rate premise and its isotropic control, as coded, cannot
  fail (VI-32, VI-34). A re-run is owed.
- **The consumer-relative flip (Chapters 8 and 13).** The flip was **put at risk in
  twelve domains and confirmed as a sealed flip in six of them**. Real recordings from
  three physical media are among the twelve. The flip is sealed on both acoustic
  corpora (LOCATA and AV16.3) and on the seismic array, and partial on automotive
  radar. Gate B hits carry `[predicted]` with the hit recorded, as the ledger's class
  cells do, and every miss and partial is printed beside the hits.
- **Observation Theory v1.0 (Chapter 16 and `crucible/`).** Four sealed campaigns, the
  Crucibles, tested the theory's five principles. The first two ended without
  graduation. OT-4 and OT-5 refuted predictions of the fourth and fifth principles, and
  both principles were revised at v0.2 to absorb the refutations. Later campaigns
  earned the revised statements, and v1.0 was declared on 2026-08-18 with no owed
  prediction outstanding (`crucible/DECLARATION-V1.md`). Chapter 16 carries the
  Crucibles' losses. Their passes (OT-1, OT-2, OT-3, OT-6, OT-7 and OT-8) are ledger
  rows that no chapter carries yet.
- **Theorems (Chapters 7, 17, 24 and 25, Appendices B and F).** Four rows have been
  `[proved]` since 2026-11-21. PAPER-III.a and PAPER-III.b carry consumer-relative
  rate–distortion (Chapter 7), and PAPER-V.a and PAPER-V.b the rate–work–distortion
  region (Chapter 25). Each has a complete written proof, logged fresh-context passes, a
  harness that runs in CI and is built to fail, and a custody file of constants and
  slack. The rate–leakage–distortion series (RLD-I to RLD-IV.4, Chapter 24), the
  learn-then-serve note (T1 and T1-MK, Chapter 17) and Paper V's coding theorems and
  accounting identities (PAPER-V.c and PAPER-V.d) have written proofs and fresh-context
  audits and stay `[exploratory]`. Each lacks at least one of the four requirements of
  `[proved]`, and its ledger row says which. The legibility theorems of Paper I
  (Chapter 9) have no ledger row yet and are marked "proved in Paper I; not yet a
  ledger row".
- **Part VIII, reliability (Chapters 19 to 23).** Chapter 19 is drafted and Chapters 20
  to 23 are outlines. Their classes rest on the sealed tracks of the
  `observation-theory-campaigns` repository, and this volume's ledger has no rows for
  them yet.
- **Part IX, beyond one consumer (Chapters 24 to 29).** Drafted by the assistant on
  2026-11-25 from the ledger rows and the program's papers, one chapter per ledger
  group, with each claim at its row's class, and read by the author (the author's
  statement, 2026-11-28). The reset and the complementarity tax
  (GO-7 to GO-11) are `[replicated]`. The dynamic tax (GO-13) is `[demonstrated]`.
  Access width and causal erasure (GO-12 and GO-14) are `[predicted]`, and a
  measurement on a production serving stack (registration 077) passed one of its two
  sealed predictions and refuted the other. The adversarial observer (GO-16) is
  `[predicted]` for its first two theorems, and its third theorem is refuted as sealed
  (NEG-17). The estimation-and-control rows (GO-EC-2 to GO-EC-7) are `[predicted]`. The
  ledger has no row GO-15.
- **Losses (Chapter 16).** The ledger's negative rows NEG-1 to NEG-18 and the
  Crucibles' refuted and void tests are carried at the prominence of the results they
  bound. NEG-13 was later resolved by a sealed run and stays in the record.
- **Not yet settled.** Some classes wait on rulings the ledger does not yet record,
  among them the class of the Gate B hits, rows for the Gate B misses and partials, and
  rows for Part VIII and for the legibility results. They are listed in
  `CORRECTIONS-2026-11-26.md` under "Open, for the author".

---

## For the reader in a hurry

If you read one paragraph, read this. Fix an object $x$, a channel that compresses
it, and a *consumer* $C$ that acts on the result — a classifier, an attention head,
a direction-finder, a retrieval index. The consumer does not read $x$; it reads a
few directions of $x$, weighted by how much its own output moves when those
directions move. Write that as a symmetric operator $P_C$, the **read metric**.
Then the quality of a compression is not how faithfully it reconstructs $x$ — it is
how little error it leaves *inside* $P_C$. These come apart. A code that
reconstructs worse can serve the consumer better, and a code that reconstructs
best can be the worst thing you ship. That reversal — the **consumer-relative
flip** — is the empirical heart of this book, and $P_C$ is its single moving part.

---

## Core Objects at a Glance

The framework introduces a small set of objects, each with one job. Return here as
they appear in the text.

| Object / Symbol | Informal meaning | Formal character & chapter |
|---|---|---|
| $O = (C, G, B)$ (the observer) | *who is looking*: a consumer, its output metric, and a resolution budget | The triple that makes geometry, distortion, and reliability well-posed; nothing is a property of $x$ alone (Ch. 4) |
| $C : X \to Y$ (the consumer) | the downstream use — the thing that acts on the representation | A (possibly nonlinear) functional with Jacobian $J$; the classifier, the attention head, the estimator (Ch. 4–5) |
| $P_C = J^{\top} G\, J$ (the read metric) | *what the observer can distinguish* — the pullback of the output metric | Symmetric PSD operator; its range is the read subspace, its kernel the nuisance the observer discards (Ch. 5) |
| $X/\!\sim_C$ (the quotient) | *the world the observer can act on* — objects it cannot tell apart are one point | Equivalence under $\ker P_C$; the space on which the consumer's verdicts live (Ch. 5) |
| $\operatorname{tr}(P_C \Sigma_\delta)$ (read distortion) | how much of the coding error lands where the consumer looks | The quantity that controls downstream loss at matched rate — **not** $\|\delta\|^2$ (Ch. 6) |
| $R_C(D)$ (the consumer rate–distortion function) | the price of observation | Achievability + converse for the read metric, whose water-filling tilts toward $P_C$ (Ch. 7, the COST shadow) |
| The **flip** | preserving the read can beat reconstructing the object | Reconstruction-tied codes rank oppositely per consumer; tested in 12 domains + 3 physics, a sealed flip in 6 (Ch. 8, the VALUE shadow) |
| Keep-the-Angle | in spectral embeddings the *angle* carries geodesics, the radius carries density | Angular coordinate is the read subspace of the geodesic-rank consumer; radius $\in \ker P_C$ (Ch. 9, the LEGIBILITY shadow) |
| The blind probe (GO-1) | recover $P_C$ from the consumer's outputs alone, no labels, no oracle | Finite-difference the consumer margin; recovers the read subspace ex ante (Ch. 10) |
| The recognizer | name the manifold a representation lies on, or certify that none exists | Low multiplets + angular distances; "dimension emerges before shape" (Weyl ordering) (Ch. 11) |
| $\kappa = \operatorname{tr}(\bar P_C \bar\Sigma_x)$ (the alignment law) | *when* the flip appears — read/energy misalignment on an ordinal dial | Normalized read–energy overlap; $\kappa\to 1$ with read support equal to signal support is the coupling null; the magnitude law (flip decreasing in $\kappa$) failed (Ch. 12) |
| The four degeneracies of $P_C$ | the four ways the flip is *absent* | coupling ($\operatorname{range} P_C$ aligned with source energy), precondition ($P_C \approx 0$), identifiability (wrong $\hat G$), mechanism-absent (direction $\notin \ker P_C$) (Ch. 12) |
| The ledger | the living record of record | Six classes `[proved] [demonstrated] [replicated] [predicted] [exploratory] [refuted]`; every table ID resolves to a row (Ch. 15–16) |

---

## The Epistemic Status Classification

Every load-bearing statement in this book carries one of six tags, inline, in
brackets. They are not decoration; they are the terms on which you are asked to
trust a sentence. They come straight from the claim ledger, and a sentence may not
wear a tag its ledger row has not earned. The status note above names the two
exceptions. Paper I's legibility results carry no tag until they have ledger rows,
and Part VIII takes its tags from the sealed tracks of `observation-theory-campaigns`.

- **`[proved]`** — a complete written proof *and* a committed numerical
  falsification harness that would fail if the theorem were false, *and* a
  fresh-context adversarial re-derivation on record, *and* a table of its
  constants, slack and known gaps (the charter's T-CUST-1). Both grades, or it is
  not proved.
- **`[demonstrated]`** — a sealed, pre-registered empirical prediction that passed
  its ex-ante bar on a governed run.
- **`[replicated]`** — a `[demonstrated]` result reproduced on a second,
  independent instance or representation.
- **`[predicted]`** — a sealed prediction whose gate is stated but whose
  confirming run is prospective or single-instance.
- **`[exploratory]`** — a green numerical check with an unproven or unverified
  derivation; suggestive, not load-bearing. **No umbrella claim may cite an
  `[exploratory]` row.**
- **`[refuted]`** — a claim the program bet on and lost. These are carried into the
  text *at the same prominence as the wins they bound* (Chapter 16). Softening a
  sealed miss after the fact is prohibited.

A reader who wants to audit the book reads it tag-first: follow any `[proved]` to
its harness, any `[demonstrated]` to its sealed prereg, any `[refuted]` to the
negative it stands as. The framework earns trust not from any one sentence but
from the coherence of the ledger behind all of them.

---

## Notation

| Symbol | Meaning |
|---|---|
| $x \in X$ | the object / source vector; $\Sigma_x$ its covariance |
| $C,\ Y,\ G$ | consumer map, its output space, the output metric on $Y$ |
| $J = \partial C$ | the consumer Jacobian at the operating point |
| $P_C = J^{\top} G J$ | the read metric (pullback); $\operatorname{range}P_C$ read subspace, $\ker P_C$ nuisance |
| $\Sigma_\delta$ | covariance of the coding error $\delta = \hat x - x$ |
| $\operatorname{tr}(P_C\Sigma_\delta)$ | read distortion — downstream loss at matched rate |
| $R_C(D)$ | consumer rate–distortion function |
| $\kappa$ | normalized read–energy alignment $\operatorname{tr}(\bar P_C \bar\Sigma_x)$ |
| $B$ | the resolution / bit budget |
| $X/\!\sim_C$ | the consumer quotient (identify points $\ker P_C$ apart) |
| $\alpha$ | density-quotient exponent (spectral-embedding leg) |
| GO-$k$, NEG-$k$ | ledger rows: falsifiable-core claim $k$ / honest negative $k$ |
| $[\,\cdot\,]$ | epistemic-status tag on the preceding statement |

---

## How to Read This Book

The argument is cumulative and the parts serve different readers. Four routes in.

**The engineer who ships representations** — quantizers, embeddings, KV-caches,
retrieval indices — should start with the Preface's running example, then read
Part III's VALUE chapter (Ch. 8, the flip) and Part IV's instruments (Ch. 10 the
blind probe, Ch. 12 the alignment law $\kappa$). These tell you when
reconstruction error is lying to you and how to recover the operator you should
have been protecting. The theory in Part II makes the recipe transparent rather
than magical; do not skip it and then wonder why your compressor's guarantees are
opaque to you.

**The information theorist** will find the formal spine in Part III's COST chapter
(Ch. 7): the consumer rate–distortion function $R_C(D)$, its achievability and
converse, the two-observer region, whose refinability requires nested optimal
error covariances (sufficient under an achievability assumption), the
mismatch tax and the omission floor. The interest is in the *domain*, not the
tools — the operative object is a pullback metric that varies with the observer,
and classical rate–distortion is the slice where $P_C = I$.

**The geometer / spectral-methods reader** should read Part III's LEGIBILITY
chapter (Ch. 9, Keep-the-Angle) and Part IV's recognizer (Ch. 11): why the
commute-time embedding's distances collapse to degree while its *angles* keep the
geodesics, why row-normalization is the fix, and why a representation's dimension
is recoverable before its shape.

**The methodologist, referee, or skeptic** should read Part VI first — the
registration-first discipline (Ch. 15), the honest negatives (Ch. 16), and the
charter's account of verifying AI-assisted work independently of the assistant
that produced it. If the discipline does not convince you, the results should not
either; that is the intended order.

Every reader should read the Preface and Chapter 1. No single chapter carries the
weight alone.

---

## Table of Contents

**Part I — The Problem**
1. Why Observation Needs a Theory
2. The Failure of Observer-Free Measurement
3. Historical Precursors: Shannon, Rate–Distortion, and Information Geometry

**Part II — The Framework**
4. The Observer Triple $O=(C,G,B)$
5. The Read Metric and the Quotient
6. Mathematical Preliminaries: Pullbacks, Projections, and the Read Distortion

**Part III — One Object, Three Shadows**
7. COST — What Observation Charges (the consumer rate–distortion function)
8. VALUE — What Preserving the Read Buys (the consumer-relative flip)
9. LEGIBILITY — What the Quotient Reveals (Keep the Angle)

**Part IV — The Instruments**
10. The Blind Probe: Recovering $P_C$ From Outputs Alone
11. The Recognizer: Naming a Manifold, or Certifying None
12. The Failure Taxonomy and the $\kappa$ Alignment Law

**Part V — The Evidence**
13. The Domain-Generality Sweep: Twelve Domains, Three Physics
14. The Falsifiable Core: GO-1 … GO-6 and Gate B

**Part VI — The Discipline**
15. Registration-First: How the Program Keeps Itself Honest
16. Honest Negatives: The Boundaries, Kept With the Results

**Part VII — Horizons**
17. Open Problems and the Keystone Theorem
18. The Principle: Keep the Structure the Observer Can Use

**Part VIII — Reliability: The Witnessed Certificate**
19. The Certificate That Ages
20. The False-Clear Rate (outline)
21. The Refresh Floor (outline)
22. The Freshness Sweep (outline)
23. The Governor (outline)

**Part IX — Beyond One Consumer**
24. The Holder: Rate, Leakage, and Distortion
25. The Reset: Rate, Work, and Distortion
26. The Complementarity Tax
27. Access Width: Staleness, Processes, and Causal Erasure
28. The Adversarial Observer
29. Observation for Estimation and Control

**Appendices**
- A. Related Work and Differentiation
- B. The COST Ledger: Theorems, Proofs, and Falsification Harnesses
- C. Reproduction Cookbook
- D. The Registry: Every GO-P-2026 ID and Its Disposition
- E. Skeptic's Appendix: Objections, Alternatives, and FAQ
- F. Mathematical Ledger: Status of Formal Claims
- G. A Hub-Mechanism Catalog: One Scalar, Many Observer-Induced Geometries

*Bibliography · Table of Figures · Index*
