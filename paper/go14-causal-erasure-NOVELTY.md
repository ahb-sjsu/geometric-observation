# GO-14 novelty record — the 085-era sweeps (Lemma A′, Lemma W, R1 residuals)

**Date:** 2026-08-08. **Scope:** the three sweeps owed at the close of
GO-P-2026-085. Earlier GO-14 novelty rounds are folded into
`go14-causal-erasure-PROBE.md`; this file records only this round.

**Standing rule this record does not relax:** no novelty language is printed
for Lemma A′, Lemma W or Theorem D anywhere in the tex until the owed
channels below are actually run. Two of the three sweeps are complete; one
is blocked and is recorded as blocked, not as clear.

---

## Channel disclosure (read this before quoting any verdict)

| Channel | Status |
|---|---|
| WebSearch (general) | RUN |
| arXiv abstract + full PDF | RUN |
| Semantic Scholar Graph API | **NOT RUN — HTTP 429 on three attempts.** Still owed. |
| ScienceDirect full text | **BLOCKED — HTTP 403.** |
| MIT DSpace (thesis version) | **BLOCKED — HTTP 405** on the bitstream and the item page. |

The S2/full-text channel was already the named residual from the R1 sweep
("the 1983–85 robust-prediction layer and any journal-only convexity result
are INVISIBLE to an arXiv-abstract sweep"). **It is still invisible.** That
residual is NOT discharged by this round.

---

## 1. R1 residual (a) — Zheng–Lamperski: **DISCHARGED, page-verified**

**Zheng & Lamperski, "Non-Asymptotic Error Bounds for Causally Conditioned
Directed Information Rates of Gaussian Sequences", arXiv:2512.06238, IFAC
World Congress 2026.**

The prior round flagged this as "the paper a referee will raise — closest
single item to the object, full text unchecked". The full PDF has now been
searched, not the abstract:

- **The words "convex", "convexity", "concave" and "Jensen" do not occur
  anywhere in the paper.**
- It gives an explicit formula for the causally conditioned directed
  information rate in terms of one-step-ahead prediction error variances,
  defines an **estimator** from that formula, and proves an
  `O(N^{-1/2} log N)` high-probability error bound.
- **It never optimizes or minimizes the rate over a class of processes or
  records.** It quantifies estimation error.

**Verdict: adjacent, not overlapping — and the distinguish is one line.**
Zheng–Lamperski *evaluate and estimate* the species; Theorem R1 *convexifies*
it, as a functional on a window-free class of records. No convexity claim
exists there to collide with. The citation should be carried as related work
with exactly that sentence.

## 2. Lemma A′ packaging — **NOT novel, and the adjacent literature must be distinguished**

Lemma A′ is one line of Hilbert space: σ(x) = dist²(R_u, M) with M the
*closed* span, finite combinations are dense in a closed span by definition,
and the distance to a set equals the distance to its closure. Nobody should
claim that. The sweep's real finding is that **the neighbouring literature
says something that sounds like a contradiction of A′(1), and the tex must
say why it isn't.**

**Nearest item: "Uniform FIR approximation of causal Wiener filters, with
applications to causal coherence", *Signal Processing*, December 2015
(ScienceDirect S0165168415004065).** It proves **L_p convergence of the
frequency responses** of the FIR causal Wiener filter to the IIR causal
Wiener filter **under Hölder-continuity conditions on the power spectra**,
with asymptotic upper bounds on the convergence error, plus a corollary on
uniform convergence of AR-approximation spectra. Secondary search summaries
in the same channel state the general negative reading directly: optimal
Wiener predictors are always IIR, and approximating them by FIR filters is
"generally not possible under the control of the approximation error".

**Why this does not touch Lemma A′, and why the distinction is load-bearing:**

| | The 2015 result (and the negative reading) | Lemma A′(1) |
|---|---|---|
| Object converging | the **filter** / frequency response | the **value** σ |
| Mode | L_p (and uniform, for the AR corollary) | none — a plain infimum identity |
| Hypotheses | **Hölder continuity** of the spectra | **Φ_R, f_S ∈ L¹ and nothing else** |
| Attainment | approximants converge *to* the optimal filter | infimum **not attained** by any finite filter |

A′ claims strictly less and therefore needs strictly less. The literature's
negative statements are about controlling *filter* error under weak
smoothness; A′ never controls a filter and never needs a rate. The tex
already prints the hypothesis line ("no spectral floor, no H² ball, no
uniform convergence, no membership in W") — **that line should now cite this
paper explicitly and say the mode of convergence is the difference.**

**Verdict: A′ is a packaging of a textbook fact (correct, and labelled as
such). No novelty language. One distinguishing citation OWED in the tex.**
⚠ Page-verification of the 2015 paper's exact theorem statements is
**incomplete** — ScienceDirect 403, DSpace 405. The characterization above
rests on two independent search-channel summaries agreeing, not on the
theorem text. Verify before the sentence is printed.

## 3. Lemma W combination — **no prior found, coverage partial**

Swept for: a quantitative transfer between a finite-window and a
stationary/infinite-horizon causal rate, with a per-symbol boundary charge,
and a repair step restoring **exact** distortion feasibility on the window.

- **Nonanticipative RDF line (Stavrou–Charalambous et al.)** is the most
  likely home and does not contain it. The asymptotic reverse-waterfilling
  paper (CDC 2018) gives **structural** characterization of the asymptotic
  NRDF, not a rate of convergence: no `R_n ≤ R_∞ + C/n`, no boundary charge,
  no window-rescaling construction. The finite-horizon DP line
  (arXiv:2411.11698) is finite-horizon *computation*, and its convexity
  results are the definitional convexity in the reproduction kernel already
  recorded in the prior round — not a transfer.
- **Classical truncation/blocking** for stationary sources (Berger/Gray
  lineage) defines the limit *as* a limit of finite-horizon problems. That is
  the existence statement 080 already proves by subadditivity + Fekete; it is
  not a quantitative per-symbol charge.
- **Closest structural analogue found, and it is worth citing:**
  arXiv:2605.25085, *Polynomial Context-Truncation Sensitivity in
  Autoregressive Language Models: Sequential Wyner–Ziv Bounds for KV Cache
  Compression* — a sliding-window truncation achievability with matching
  converse. **The distinguish is sharp and favourable:** that scheme meets
  the distortion only up to an additive residual (`D_n ≤ D + O(·)`, window
  `w = O(ε^{-1/α})`), whereas Lemma W's repairing rescale `c` restores
  feasibility **exactly**, so the whole charge lands on the rate and none on
  the distortion. (Note for the other lane: this paper is also directly
  adjacent to the vector-u KV successor.)

**Verdict: HOLD-NOVEL on the swept channels — with coverage explicitly
partial.** The combination (exact-feasibility repair + two opposite,
both-favourable legs + exactly-zero edge cells + C(L,n) monotone decreasing
with finite sup) did not surface anywhere. **This is not yet a licence for
novelty language**, because the S2/full-text channel that would see
journal-only work is the one that failed.

---

## What is owed before any novelty sentence for A′, W or D

1. **Re-run the Semantic Scholar / full-text channel** when the rate limit
   clears — for Lemma W's combination *and* for the R1 sweep's channels 1/3/4
   (the 1983–85 robust-prediction layer).
2. **Page-verify the 2015 FIR-approximation paper** through an institutional
   route (Syed's venue package can pull it), then print the mode-of-
   convergence distinguish next to Lemma A′'s hypothesis line.
3. Add Zheng–Lamperski as related work with the evaluate-vs-convexify
   sentence, and arXiv:2605.25085 as the truncation analogue with the
   exact-vs-approximate-feasibility distinguish.
