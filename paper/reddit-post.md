# r/MachineLearning draft — [R] post

## Title options (pick one)

1. `[R] At matched bits, the downstream winner between two codes flips when you change the consumer — while reconstruction error says they're identical. 12-domain study, pre-registered, negative results included`
2. `[R] Reconstruction error is the wrong objective when a specific consumer reads the output: cross-domain evidence + coding theorems (code, preprints, all pre-registrations public)`

---

## Post body

**TL;DR.** At a matched bit budget, a code that preserves what the downstream
consumer is sensitive to can beat a reconstruction-optimal code on the task
while *losing* to it on reconstruction. Hold everything fixed and swap the
consumer, and the winner flips. We tested this under sealed pre-registrations
(predictions + pass/fail bars committed publicly before each run) across 12
domains. Confirmations and failures both published; the failures turned out
to be the informative part. Preprints, code, and every registration linked
at the bottom.

**The motivating bug.** A 4-bit KV-cache quantizer with reconstruction
cosine 0.995 that blew perplexity up by ~3 orders of magnitude, while a
"worse-reconstruction" per-channel quantizer was fine. The fidelity metric
and the task disagreed completely. That gap is the whole subject.

**Setup.** For a consumer C with output divergence D_Y, a second-order
expansion gives downstream distortion ≈ tr(P_C Σ_δ), with
P_C = E[JᵀGJ] the Fisher-weighted sensitivity of the consumer and Σ_δ the
error second moment. Reconstruction is the corner P_C = I.

**Relation to prior work, up front.** The quadratic object is classical:
this is Hessian-weighted / loss-aware compression (OBD → OBS → HAWQ → GPTQ)
written as a metric, and the coding problem is indirect/remote source coding
(Dobrushin–Tsybakov 1962; Witsenhausen), adjacent to rate–distortion–
perception and task-oriented communication. The papers cite all of this.
What we believe is new: (1) *blind* recovery of the read subspace from
black-box consumer queries, validated against a planted ground truth
(calibration-based Hessian estimation is standard, but it isn't validated
against truth); (2) the flip demonstrated prospectively across domains;
(3) coding theorems — a consumer-relative R(D) with achievability and
converse, a two-observer successive-refinement region (refinable iff the two
optimal error covariances nest in the Loewner order; the one-line corollary
is that rate spent on directions the next reader can't see is
unrecoverable), and mismatch bounds (mis-weighting a read direction costs a
bounded rate tax; *omitting* one erects a distortion floor no rate can
cross); (4) a taxonomy of when the flip cannot appear.

**Results** (sealed = pre-registered with bars committed before the run):

| Domain | Consumer | Outcome | Tier |
|---|---|---|---|
| Synthetic ULA | root-MUSIC DOA | flip 6/6 | sealed |
| Llama-3.2-3B keys | softmax attention (KL) | blind probe called the worse code 16/16 at reconstruction tied to 7.5e-9; reconstruction had no discriminative power | sealed |
| LOCATA acoustic array | wideband MUSIC | 11/13 | sealed |
| AV16.3 acoustic (2nd corpus) | MUSIC, circular array | 74% flip, 100% reconstruction control, disjoint held-out | sealed |
| PDAR seismic | backazimuth vs earthquake catalogue | 76% flip | sealed |
| 77 GHz FMCW radar | MUSIC DOA | partial; data-limited (within-recording split) | sealed |
| Gradient compression | update error in Hessian metric | **no flip — predicted null** (see below) | sealed |
| Legal citation retrieval | cosine ranking | failed with a proxy read operator; passed after switching to the blind probe (margin 0.008 — treat as marginal) | sealed |
| ETHICS moral classifier | fine-tuned head | confirmed | sealed |
| Music genre, whale coda dialects, KV regime map | classifier weights | consistent with the theory | exploratory, not sealed |

**Negative results, which are the part I'd actually read.** The gradient
domain is a structural null the theory predicts: the Hessian's top
directions coincide with the gradient-energy directions (both are built
from XᵀX), so reconstruction-optimal coding already protects what the
consumer reads and the flip cannot appear. A one-statistic regime diagnostic
we pre-registered broke on its first prospective test and forced a two-axis
replacement. And a density-quotient conjecture was refuted outright across
four prospective tests and is carried as a refutation. The overall pattern:
the flip appears where the read operator is identifiable, misaligned with
signal energy, and attached to a consumer that actually works — and fails,
informatively, in exactly the complement.

**Limitations.** The core distortion/identifiability validations use
synthetic consumers by design (planted ground truth, including an H = I
control where reconstruction becomes exactly optimal — and does). One
trained model so far; the Llama result is worse-arm prediction under one
consumer, not yet a two-consumer inversion on the trained model (that
experiment is next and already registered). Exploratory rows are marked and
are not evidence in the sealed sense. Solo author. Experiments and drafting
were AI-assisted under a written verification protocol; the assistant's
errors are logged in the same public ledger as everything else — disclosed
in the papers' acknowledgments, so mentioning it here too.

**Links.** Preprints are on Zenodo with DOIs (no arXiv endorsement, so
Zenodo): [Paper I DOI] · [Paper II DOI] · [theory paper DOI]. Code,
pre-registrations, result JSONs, and the claim ledger:
github.com/ahb-sjsu/{the-angular-observer, turboquant-pro,
geometric-observation}. Every number above resolves to a sealed
registration committed before the run it governs; if you want to tear any
of it apart, the ledger exists for exactly that.

---

## Posting notes (not part of the post)

- Flair **[R]**. Own-work research posts are allowed there when the content
  is in the post; this one is, with links last.
- Post early in a US weekday morning; be in the comments for the first
  2–3 hours — responsiveness is most of what separates "researcher sharing
  work" from "drive-by promo" in that community's eyes.
- Comments to expect, with the honest answers ready:
  - *"Isn't this just Hessian-aware quantization?"* → The metric is, and the
    post says so; the deltas are blind validated recovery, the cross-domain
    prospective flips, and the coding theorems. Don't get defensive — agree
    with the premise, point at the delta.
  - *"Isn't this the information bottleneck?"* → No containment claim; IB
    optimizes a stochastic relevance variable; this is a fixed geometric
    operator recoverable by probing. It's the middle term, and the paper
    says exactly that.
  - *"So reconstruction metrics are useless?"* → No: P_C = I is the corner
    where they're exactly right, and the H = I control confirms it
    empirically. This is the single most important calibrated answer.
  - *"Why Zenodo and not arXiv?"* → Endorsement gate; DOIs work fine; move
    on. Don't litigate it.
  - *"AI-assisted?"* → Point at the protocol and the logged errors; the
    disclosure is the answer.
- The framework name is deliberately absent from the body. It's in the
  papers; r/ML punishes grand names and rewards concrete claims. Let
  commenters find the name themselves.
