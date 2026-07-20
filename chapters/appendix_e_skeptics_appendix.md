# Appendix E — Skeptic's Appendix: Objections, Alternatives, and FAQ

The best test of a framework is the strongest objection it can survive. This appendix
states the objections a hostile expert reader raises, in their sharpest form, and answers
each — conceding where the concession is real. An objection with no concession is usually
answered dishonestly; several below end in a "yes, and."

---

**"Isn't $P_C$ just the Fisher information metric? You've renamed a classical object."**

Yes, when the consumer is a likelihood: for a probability-model consumer with the Fisher
output metric, $P_C = J^\top G J$ *is* a Fisher-information pullback, and the algebra is
Amari's and Čencov's (Chapter 3, Appendix A). The concession is total at the level of the
operator. The claim is not the operator; it is the *load*: that this pullback is the
operative object for **lossy representation across domains** — the thing that decides
whether a quantizer, embedding, or array codec is good — and that it is recoverable
*blind*. Information geometry studies the pullback for inference *on* a manifold; this
program uses it to decide how to *compress inputs to* a consumer, proves a falsifiable
consequence (the flip), and seals it across twelve domains. The contribution is the
sentence and its ledger, not the symbol.

---

**"Isn't this just task-aware / downstream-aware compression, which people already do?"**

The intuition is shared; the method is not. Task-aware compression typically *trains* a
code end-to-end against a task, yielding an opaque code with no stated boundary. This
program *identifies the read operator* $P_C$ — blind, no labels, no oracle — and *derives*
what to keep, giving a transparent recipe plus a theory of *when task-awareness matters*
(the $\kappa$ law and the four degeneracies, Chapter 12) and *when it does not* (the D4
coupling boundary, the moral precondition). And it makes a sealed *prediction* — the flip
— rather than assuming the benefit. "Yes, and": where an end-to-end trained code already
protects the read subspace, it is implicitly doing what the framework prescribes; the
framework explains *why it works and when it will not.*

---

**"You fit the read operator on the data, then tested on the same data. This is circular."**

This is the objection the program takes most seriously, because it is exactly the failure
it *caught in itself* — twice. Legal-035 estimated the read operator from a document
covariance, and it **overfit**: reconstruction-optimal won on held-out (NEG, Chapter 10).
The fix was not to fit harder but to recover the operator *blind* from the consumer
(GO-1 probe) and to **seal the config before touching held-out data**, then confirm on a
**fully virgin** split (039, margin double). The commit-ordering audit (Appendix D) proves
every seal is a git *ancestor* of its run. The circularity objection is correct as a
danger and is answered by protocol, not by assertion: blind recovery, seal-before-measure,
and out-of-sample promotion (R-IND-6). Where the program could not meet this bar — the
20-Newsgroups magnitude (041) — it reports **partial**.

---

**"The AI assistant that built this also graded it. Why should I trust any of it?"**

You should not trust the assistant's self-grade, and the program does not ask you to. The
charter's first rule is that the assistant **may not be the sole grader of its own work**
(Chapter 15). Independence is supplied by fresh-context adversarial verification (R-IND-5),
differential testing against a second implementation (R-IND-3), and, for the flagship
theorem, a proof assistant. The standing evidence that this is necessary *and* works is
VI-4: an in-context self-check passed a **wrong** `sigma_star` formula; the fresh-context
pass caught it. "Yes, and": there is no *mature* standard for verifying AI-assisted work
independently of the assistant, and the program says so plainly (Chapter 15's frontier
gap). Its composition is a reasonable approximation, disclosed, not a solved problem.

---

**"The flip only appears where you say it does. A theory that predicts its own exceptions
is unfalsifiable."**

The opposite: the theory predicts its exceptions *in advance and mechanistically*, which
is what makes it falsifiable rather than elastic. The four degeneracies of $P_C$ (Chapter
12) are a closed list, three of them diagnosable *before* the experiment via the $\kappa$
dial and the two-axis regime map. D4 was predicted to be a coupling null *and was* (flip
27%, anti 300/300). The one-number regime shortcut (NEG-14) was **refuted on its first
prospective test** — a genuinely unfalsifiable theory cannot log a refutation of its own
diagnostic. The exceptions are sealed predictions, not retrofitted excuses.

---

**"Twelve domains, but several are (A2) verdicts, one is data-limited, one is a null. Isn't
the real count much smaller?"**

Read the labels — they are the point. A **flip** (sealed two-metric dissociation on
held-out data) is distinguished throughout from an **(A2) verdict** (one-metric proxy
recommendation); moral, music, and KV-keys are labeled *verdicts*, not flips, and are not
counted as flips. D1 is labeled **partial** (data-limited, anti below bar); D4 is labeled
an **honest null** (a true boundary). The sealed flips that clear their bars span
**≥5 independent domains and ≥3 distinct physics** (synthetic, acoustic, seismic) plus
non-physical consumers (attention, classifiers, retrieval) — that is the real count, and
it is stated without the verdicts or the null padding it.

---

**"Reconstruction error works fine in practice. You're overturning something that isn't
broken."**

It works fine *for isotropic consumers* — the $P_C = I$ slice — which is common and
important, and the framework agrees (Chapter 2, Chapter 18). It stops working the moment
the consumer reads some directions more than others, which on modern learned
representations is essentially always, and the program has the receipts: cosine 0.995 with
perplexity $10^4$ (NEG-2), a recalibration that improves reconstruction and *worsens* the
consumer metric (NEG-4). The claim is not that reconstruction is always wrong; it is that
it is the *slice*, and using it off-slice is a category error with measurable cost.

---

**"The magnitude of the flip doesn't transfer across domains. So you can't actually predict
anything quantitative."**

Conceded, and flagged as the sharpest open problem (Chapter 17). The framework predicts the
*direction* (which code wins) blind and prospectively (041: R 0.975 > O 0.910 before any
label), and *within a domain across rates* the magnitude tracks (Pearson 0.995). The
*cross-domain scale constant* does not yet transfer, and the book says so rather than
hiding it. A theory that predicts the winner everywhere and the margin within-domain, while
naming the portable-magnitude constant as open, is more useful than one that claims the
constant and cannot show it.
