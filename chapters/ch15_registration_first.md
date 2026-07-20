# Chapter 15 — Registration-First: How the Program Keeps Itself Honest

I have deferred this chapter for fourteen chapters, and I made it a *part* rather than an
appendix, for one reason: this is a program co-designed with an embedded AI assistant, and
in such a program *how* the claims are kept honest is not separable from *what* they are.
An assistant that can propose, derive, implement, and draft can also — fluently,
persuasively — be wrong, and can pass its own work. The discipline in this chapter exists
because that assistant **may not be the sole grader of its own work**, and because the
program must be able to **lose in public and continue smaller.** Everything the book claims
rests on the machinery described here; if the machinery does not convince you, the results
should not either, and that is the intended order of reading.

The whole apparatus serves one house rule, inherited from every volume of the series and
enforced here by a written charter: *the book may not assert what the ledger cannot show.*

## Seal before measure

The foundational rule is **REG-1**: a prereg — the claim, the arms, the sample size, and
the pass/fail bar — is hashed and **git-committed before** the first governed measurement
it covers. The binding registration timestamp is the git commit, not the file's
modification time; the sealed state is externally anchored in a DOI deposit (Zenodo concept
DOI 10.5281/zenodo.21423315), so the registered claim is not merely local (REG-3).
Corrections to a sealed prereg are appended as dated amendments and re-sealed, with the
reason stated, and the original remains in git history (REG-2). Registration IDs are a
single monotone sequence `GO-P-2026-###` — never reused, never backfilled (REG-4) — which
is what lets Appendix D present a *gap-free* disposition table and lets the "no file drawer"
claim mean something: an unexplained hole in the sequence would be visible.

Sealing before measuring is the difference between a prediction and a description. Every
[demonstrated] and [predicted] tag in this book points to a bar that was written down
before the number that had to clear it was known. When a bar is missed, the miss is a
miss — the sealed threshold is not quietly relaxed afterward (the standing over-strict-gate
rule, below).

## Independent verification: the R-IND rules

Analytic and load-bearing claims are verified by a context **independent of the author's
chain of reasoning** — not merely re-read by the same author. The rules:

- **R-IND-1 (separation).** The verifier works in a fresh context with no access to the
  derivation's working notes; it receives the claim and the toolkit and reconstructs the
  argument itself.
- **R-IND-2 (adversarial default).** The verifier is tasked to **refute**, defaulting to
  "wrong/unproven," and must be moved off that prior by its own reconstruction.
- **R-IND-3 (two grades).** *Derivation-grade* = the argument re-derived line by line.
  *Conclusion-grade* = a committed numerical falsification net that fails if the result is
  false. A result is not `[proved]` until it has **both**.
- **R-IND-4 (record before assertion).** The verdict, corrections, and citation flags are
  logged *before* any paper asserts the result. A pass with caveats is a caveated pass.
- **R-IND-5 (the fresh-context derivation-grade pass).** The operative instance for a
  theorem: a fresh-context, adversarial, line-by-line pass on every lemma it supports,
  logged with its verdict. This is the rule cited by name throughout the ledger.
- **R-IND-6 (out-of-sample for upgrades).** Promoting `[exploratory]` → `[demonstrated]`
  requires a fresh sealed prereg and a run on *held-out* data — never a replay of the
  calibration set.

## The AI-assistant conflict, stated plainly

The charter names the conflict rather than papering over it. The assistant **may** propose,
derive, implement, and draft (C-AI-1); it **may not** be the sole grader of an item it
authored — independence is supplied by R-IND-5 (a separate context) and R-IND-6 (held-out,
sealed-first runs). When the assistant reports its own work as verified, it must state the
*grade* (derivation vs conclusion), the verifier's identity, and any caveat — never
"verified" unqualified (C-AI-2). Human authorship and accountability are unchanged: the
human author owns every claim (C-AI-3).

The standing reminder that this is necessary, not ceremonial, is **VI-4**. An in-context
self-check of the assistant's own `sigma_star` formula was partly tautological and *passed
a wrong formula*; the two-observer max-determinant error covariance is reverse
water-filling in the whitened basis, and the cap the formula claimed "never binds" does
bind on $\ker P$. A fresh-context adversarial pass caught it, the formula was corrected, the
prereg amended and re-sealed, and the false pass was logged with the prominence of a
positive. An assistant grading its own work would have shipped the error. The composition
that caught it — a fresh-context verifier, differential testing against a second
implementation, and (for the flagship theorem) a proof assistant — is the program's
approximation to a standard that does not yet exist.

## Theorem custody

Every `[proved]` item ships four things (T-CUST-1): a complete written proof; the R-IND-5
fresh-context pass (verdict + findings logged); a **C3 numerical falsification harness** —
pure, CPU-reproducible, committed, CI-run, and built to *fail* if the theorem is false; and
a constants/slack + known-gaps table. And the standing caution (T-CUST-2): a green harness
is a *net, not a proof* — it can only refute. A green C3 with an unverified derivation is
`[exploratory]`, not `[proved]`. Citation flags on external results are checked against the
source before assertion and grepped out before export (T-CUST-3).

## The rule earns its place: the verification incidents

R-IND is not a posture; it has a track record, and the track record is the argument. Caught
*before publication*: an extreme-value scaling error (VI-2 — $\exp(-x^a)$ tails give
$(\ln N)^{1/a}$, not $\sqrt{\ln N}$); the `sigma_star` false pass (VI-4); a non-iterating
$k$-stage construction and a mis-attributed citation (VI-5 — the two-stage map does not
iterate; an accumulating rotation ambiguity leaks Fisher information by $O(0.1)$); a
naive-kernel floor error (VI-6 — the omission floor uses the *whitened* kernel, overstated
$\sim 30\%$ otherwise, and is a *floor*, not unbounded distortion); and a "bijection"
argument that had to be a covering argument (VI-7). Six catches, each a place the book
would have asserted something false had the rule not fired. A rule earns its cost by its
catches, and these are the catches.

## Standards alignment, and the honest frontier gap

R-IND is not *sui generis*: REG-1 instantiates registered reports (OSF, AsPredicted);
R-IND-3's conclusion grade instantiates ACM Artifact Review and CODECHECK; the C3 nets are
property-based / metamorphic testing; the `[proved]` theorems are queued for Lean. Naming
the standard gives a referee a handhold and keeps the charter honest about what is
established versus frontier.

And there is a frontier gap, stated rather than hidden: **no mature standard toolkit exists
for verifying AI-assisted work independently of the assistant that produced it.** The
program's approximation — a fresh-context verifier (R-IND-5), differential testing against a
second implementation (R-IND-3), and, for theorems, a proof assistant — is a reasonable
*composition* of established methods, not a recognized methodology in its own right. VI-4 is
the standing evidence that the composition both works and was needed. The charter discloses
the gap; it does not claim to have closed it.

## The stand-down clause

The last rule is the one that makes the rest credible. The program's pre-committed
kill/narrow criteria **may fire** (SD-1). When they do, the *claims* narrow — publicly, in
the ledger and the umbrella text — and the program **continues smaller.** Losing a bet does
not end the program; hiding the loss would. No umbrella statement may cite `[exploratory]`
rows, and no result earns the name "Observation Theory" until its ledger row meets its class
bar (SD-2): the name is load-bearing only where the ledger is.

This is why Chapter 16 exists, and why it is next. A discipline that can only be described is
a wish; a discipline that can be *seen losing* is a method. The honest negatives are the
method, visible.
