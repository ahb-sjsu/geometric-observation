# Geometric Observation
## The Mathematical Structure of What an Observer Can Use

**Volume 14 of the Geometric Series**

Andrew H. Bond
Department of Computer Engineering, San José State University
`andrew.bond@sjsu.edu` · ORCID 0009-0003-2599-6158 · Senior Member, IEEE

---

> *Keep the structure the observer can use.*

---

### Epistemic status of this volume (2026-07-20)

**Posited framework with an instrumented spine.** This is the meta-volume of the
series: where the earlier books each posit one domain's geometry, this one asks
what *any* observer's geometry is made of, and answers with a mechanism that has
been sealed, run, and — where it failed — reported failing. The falsifiable core
(GO-1 … GO-6) is registered before measurement, verified in fresh contexts, and
carried in a living ledger; the consumer-relative flip has **replicated across
twelve domains and three distinct branches of physics**, and its boundaries are
printed beside its wins. Everything the ledger cannot show is marked as posited
theory at licensed strength. **The house rule of the whole series applies here in
its strongest form: the book may not assert what the ledger cannot show.** Formal
claims are tracked, one row per claim, in `claims/LEDGER.md`; the discipline that
governs those rows is in `CHARTER.md` and `PROTOCOL.md`.

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
| $R_C(D)$ (the consumer rate–distortion function) | the price of observation | Achievability + converse for the read metric; the true-divergence reduction is the *tilt* toward $P_C$ (Ch. 7, the COST shadow) |
| The **flip** | preserving the read can beat reconstructing the object | Reconstruction-tied codes rank oppositely per consumer; sealed across 12 domains + 3 physics (Ch. 8, the VALUE shadow) |
| Keep-the-Angle | in spectral embeddings the *angle* carries geodesics, the radius carries density | Angular coordinate is the read subspace of the geodesic-rank consumer; radius $\in \ker P_C$ (Ch. 9, the LEGIBILITY shadow) |
| The blind probe (GO-1) | recover $P_C$ from the consumer's outputs alone, no labels, no oracle | Finite-difference the consumer margin; recovers the read subspace ex ante (Ch. 10) |
| The recognizer | name the manifold a representation lies on, or certify that none exists | Low multiplets + angular distances; "dimension emerges before shape" (Weyl ordering) (Ch. 11) |
| $\kappa = \operatorname{tr}(\bar P_C \bar\Sigma_x)$ (the alignment law) | *when* the flip appears — read/energy misalignment on a dial | Normalized read–energy overlap; flip magnitude decreasing in $\kappa$; $\kappa\to 1$ is the coupling null (Ch. 12) |
| The four degeneracies of $P_C$ | the four ways the flip is *absent* | coupling ($\operatorname{range} P_C$ aligned with source energy), precondition ($P_C \approx 0$), identifiability (wrong $\hat G$), mechanism-absent (direction $\notin \ker P_C$) (Ch. 12) |
| The ledger | the living record of record | Six classes `[proved] [demonstrated] [replicated] [predicted] [exploratory] [refuted]`; every table ID resolves to a row (Ch. 15–16) |

---

## The Epistemic Status Classification

Every load-bearing statement in this book carries one of six tags, inline, in
brackets. They are not decoration; they are the terms on which you are asked to
trust a sentence. They come straight from the claim ledger, and a sentence may not
wear a tag its ledger row has not earned.

- **`[proved]`** — a complete written proof *and* a committed numerical
  falsification harness that would fail if the theorem were false, *and* a
  fresh-context adversarial re-derivation on record. Both grades, or it is not
  proved.
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
converse, the two-observer region and its Loewner-nesting refinability, the
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

**Appendices**
- A. Related Work and Differentiation
- B. The COST Ledger: Theorems, Proofs, and Falsification Harnesses
- C. Reproduction Cookbook
- D. The Registry: Every GO-P-2026 ID and Its Disposition
- E. Skeptic's Appendix: Objections, Alternatives, and FAQ
- F. Mathematical Ledger: Status of Formal Claims

*Bibliography · Table of Figures · Index*
