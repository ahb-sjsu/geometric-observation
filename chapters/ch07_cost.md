# Chapter 7 — COST: What Observation Charges

*This chapter and the two that follow are the thesis chapters of the book (staging
tier [B]). Their theorems are stated here with their status; the proofs and the
committed falsification harnesses live in Appendix B, and every numbered result
resolves to a ledger row.*

If a consumer reads only $P_C$, what does it cost — in bits — to serve it? The answer
is a rate–distortion theory in which the fidelity measure is the read distortion, and
its entire content is that the optimal bit-allocation *tilts* toward the read
subspace. This is the COST shadow, and it is where Observation Theory reconnects with
Shannon: classical rate–distortion is the slice $P_C = I$, and everything below is
what happens when the slice is allowed to tilt.

## The consumer rate–distortion function

Fix a source $x$ with covariance $\Sigma_x$, an observer with read metric $P_C$, and a
target read distortion $D$. Define

$$ R_C(D) = \min_{\,p(\hat x \mid x)\,:\; \operatorname{tr}(P_C\Sigma_\delta) \le D\;}
   I(x; \hat x), $$

the fewest bits per symbol needed so that the *consumer's* distortion — not the
reconstruction distortion — stays within $D$. For a Gaussian source this has a closed
form, and the form is the point: the optimal test channel does reverse water-filling
in the **joint basis** that diagonalizes $P_C$ against $\Sigma_x$ (the whitened
operator $\Sigma_x^{1/2} P_C \Sigma_x^{1/2}$), pouring bits into directions that are
both high-source-variance *and* high-consumer-sensitivity, and abandoning any
direction that either the source does not populate or the consumer does not read. The
tilt away from Shannon's source-only allocation is precisely the factor $P_C$. (An
earlier sentence here, that the "true-divergence reduction" relative to reconstruction
coding *is* that tilt, matched no statement in Paper III and is withdrawn; VI-32, VI-39.)
[`[exploratory]` pending a net and custody — Appendix B, B1; tagged `[proved]` until
2026-11-21, VI-38]

Two operational consequences frame the rest of the chapter.

**Reconstruction is wasteful by a computable amount.** A code that reconstructs $x$
(optimizes $P_C = I$) spends bits on $\ker P_C$ that buy the consumer nothing. GO-6
measures this end to end: at matched rate, **output coding $\le$ surrogate $\le$
reconstruction** on the consumer metric, the ordering holding at *every* rate, with
reconstruction up to $\sim 500\times$ worse downstream at high rate because its bits
went to the unread directions [demonstrated — GO-P-2026-028, all bars pass, nonlinear
consumer $d=8, r=4$; **disputed**: the harness is off the matched-rate premise, re-run
owed (VI-32, VI-34)]. The isotropic control $P_C = I$ collapses the three coders, as
it must — when the consumer reads everything, there is nothing to save.

**The surrogate–output gap vanishes with rate.** GO-6 also supports Thm B3: the
relative gap between an output-optimal code and a good surrogate shrinks (measured
$0.41 \to 0.005$) as the budget grows [demonstrated, disputed (VI-32, VI-34)]. At high resolution you do not
need to know the consumer exactly; a surrogate for $P_C$ suffices. At low resolution
you do. This is the rate-dependence that makes the blind probe (Chapter 10)
load-bearing precisely in the bit-starved regime where compression matters.

## Two observers: the rate region and refinability

Serving *two* consumers from one code is a network-information-theory problem with an
exact outer structure. For observers with read metrics $P_1, P_2$, Paper III proves that
every two-stage code lies in a max-determinant region, and that the region is tight under
a successive-refinement achievability assumption (Assumption SR, attributed to
Effros and not yet checked at the source). Its corner decides **refinability** — whether a
single scalable code can serve the coarse observer with a prefix of the bits it serves the
fine one. Refinability requires the observers' optimal error covariances to **nest**,
$\Sigma_2^\star \preceq \Sigma_1^\star$, and under the assumption nesting suffices.
Nesting depends on the targets $D_1, D_2$, not only on the read metrics: $P_1 \preceq P_2$
neither implies it nor follows from it (VI-32; Appendix B, B4). Nesting is the precise sense
in which one observer is "a refinement of" another: it can be served by adding bits, not
resending them. When the optima do *not* nest, serving both costs a rate loss, which the
theory bounds below (exactly, under the assumption). [The max-det corner identity `[predicted]`-grade; the region and its
coding statements `[exploratory]` — Appendix B.] (This paragraph said until 2026-11-21 that
refinability holds exactly when $P_1 \preceq P_2$, tagged `[proved]`; that criterion is
false both ways, VI-32.)

This region carries one of the program's standing verification incidents, and it is
worth stating because it is exactly the kind of error the discipline exists to catch.
The in-context derivation of the two-observer error covariance used a water-filling
formula with an inline claim that a certain cap "never binds"; a fresh-context
adversarial pass found the max-determinant error covariance is reverse water-filling
in the *whitened* basis and the cap **does** bind on $\ker P$ (VI-4). The formula was
corrected, the prereg amended and re-sealed, and the false pass logged with the same
prominence as a positive. The theorem statements — the abstract max-det program — were
unaffected; the harness was wrong and the harness was fixed. This is what checking both
the analytic claim and its numerical net buys you: they disagreed, and the disagreement was
the alarm. (A later custody pass, VI-32, found that the check added then cannot fail
either: re-inserting the original bug still passes it. The corner is now netted by
prereg 023's check [3] and by `verify_paper3_nets.py`.)

## The $k$-chain and what counts a dimension

For $k \ge 3$ observers in a chain, Paper III proves the outer bound and that
refinability requires the optima to nest; equality, and the sufficiency of nesting, rest on
the same achievability assumption. The chain is not a naive iteration of the two-stage
map — another caught error (VI-5): the two-stage construction *does not iterate*, because
an accumulating rotation ambiguity leaks Fisher information by $O(0.1)$ per stage; the
correct single-letter construction uses independent Fisher increments from physically
degraded channels, exact to $10^{-14}$ [corrected; prereg GO-P-2026-023; the coding step
is assumed, not proved]. The lesson survives the technicality: a
chain of observers is not a stack of two-observer problems, and the geometry that
makes it work is the nesting of the observers' optimal error covariances, not of their
read metrics.

Dispersion — the second-order term governing finite-blocklength performance — counts at
most the **read** dimensions, never the source dimensions: $r_D \le 2V \le r$ in nats$^2$,
with $r_D$ the modes above the water level and equality on the right exactly when every
read mode is active. Modes below the water level still contribute, $(\gamma_k/\theta)^2/2$
each, because fluctuations of their energy are absorbed by the active ones. As the target
distortion falls, more modes become active and $2V$ rises to $r$. (This paragraph said
until 2026-11-21, following VI-7's "sharpening", that the dispersion counts only the active
modes, an "effective dimension $r_D$"; that is refuted, NEG-18, Chapter 16.)

## Mismatch: the tax and the floor

The two results with the most operational bite are about using the *wrong* read
metric — which is what every reconstruction-optimal code does.

**The commission tax.** Coding for a read metric $\hat P$ when the consumer's is $P$,
with $m\hat P\preceq P\preceq M\hat P$ on their shared range (Loewner constants
$0<m\le M$), costs an excess rate of at most $(r/2)\log(M/m)$ in the regime
`thm:commission` states, and the $r/2$ is sharp — you pay for weighting directions as the
consumer does not [`[predicted]`-grade — Appendix B, B6; prereg GO-P-2026-024]. (Until
2026-11-21 this paragraph gave the metrics ranks $M$ and $m$, confusing the Loewner
constants with ranks, and tagged it `[proved]`; VI-32, VI-38.)
This is the rate-domain shadow of "reconstruction is wasteful": the waste has a
closed-form price.

**The omission floor.** The dangerous mismatch is the other direction — a code
*blind* to a direction the consumer *reads*. Then downstream distortion does not
merely cost extra bits; it hits a **floor** it cannot descend below at any rate:

$$ D \;\ge\; D_{\text{floor}} = \operatorname{tr}(\tilde P \, \Pi), $$

where $\tilde P$ is the read metric in the *whitened* basis $\Sigma_x^{-1/2}$ and
$\Pi$ projects onto the omitted direction. Two subtleties the discipline forced: the
omission gives a *floor*, a compact distortion band $[D_{\text{floor}},
\operatorname{tr}(P\Sigma_x)]$, **not** the "unbounded distortion" a first draft
claimed; and the floor uses the *whitened* kernel, which a naive kernel projector
overstates by $\sim 30\%$ when $\Sigma_x \ne I$ (VI-6, corrected;
`[predicted]`-grade, prereg GO-P-2026-024, and the floor's measurement `[demonstrated]` —
Appendix B, B6; tagged `[proved]` until 2026-11-21, VI-38).

The omission floor is not only a theorem. It was **measured biting a real language
model.** On trained Llama-3.2-3B read operators, the read-metric floor is reached on
16/16 heads — $\operatorname{tr}(P\Sigma_\delta)$ saturates at the measured
whitened-kernel value, while a naive $\Sigma_x = I$ assumption is off by 20–60% — and,
crucially, a misidentified coder plateaus at a softmax divergence $\sim 10^5\times$
the matched operator's (median $0.10$ nats versus $\sim 6\times10^{-7}$)
[demonstrated — GO-P-2026-027, sealed before the run on held-out layers {4,20}]. This
row has a history worth carrying: the *first* sealed finite-rate gate for it **missed**
(0/16), because softmax-KL was still improving at the top swept rate — a shallow-sweep
artifact that conflated *floor-reached* with *floor-exists* (NEG-13). The gate flaw was
logged, and the claim was resolved not by relaxing the sealed bar but by a fresh,
held-out test that passed. The floor is real; the first instrument for seeing it was
too shallow, and the ledger says both.

## A second party: the rate–leakage–distortion series

The theorems above price one consumer and no one else. A companion series of four
papers for the *IEEE Transactions on Information Theory* (the RLD series: paper I in
review, II–IV in preparation) adds a second party, a **holder** that observes the
source through its own noisy map and learns from the description without decoding
it, and charges a second cost beside the rate: the **leakage**, the conditional
information $I(X;\hat X\mid S)$ the description gives the holder beyond its own
observation. For a fixed per-symbol weight $Q$ the series finds the region of pairs
of rate and leakage:

- **I** — Gaussian vectors: every frontier point is reverse water-filling on the
  weight *tilted* by the holder's information, and the optimal directions turn with
  the budget.
- **II** — stationary Gaussian processes: the same frequency by frequency under one
  level, and the spectral region is the operational one, for holders whose
  observation is filtered (with finite or infinite memory), delayed, or the whole
  observation process.
- **III** — slowly varying sources (water-filling over time and frequency),
  cyclostationary sources, scalar unstable sources, and sources that are not
  Gaussian (the Gaussian region is achievable; every code is bounded below by the
  Gaussian frontier less two relative entropies). One inequality joins the
  branches: averaging a covariance, or a spectrum over time or a cycle, never lowers
  the cost.
- **IV** — unstable vector sources: an unstable pole costs the logarithm of its
  modulus in rate, and again in leakage only if the holder cannot observe it
  ($\rho_\star$ against $\rho_{\mathrm{hid}}$), for holders with finite or rational
  memory; poles on the unit circle (scalar) cost nothing; sources whose statistics
  vary without a period, including the proof that incommensurate sampling removes
  the dependence on the sampling phase, a conjecture of Tan, Dabora, and Poor; and
  ergodically driven vector sources.

Each result has a written proof, fresh-context model audits, and numerical checks
whose criteria were fixed before they ran but were not sealed; in this book's grammar
they are `[exploratory]` until promoted (ledger section RLD).

The series takes two things as given, and they are the business of other chapters.
**The weight.** The consumer's own geometry is the local read metric $P_C(x)$; the
series' $Q$ is a fixed input, and the optimal *description* — an error covariance
whose directions turn with the budget — depends on $Q$, the source, the holder, and
$D$ together. That turning is the description's geometry, not the observer's: it
does not mean the consumer's metric has changed. Replacing $P_C(x)$ by a constant $Q$
is the bridge of Chapter 5, which has conditions and a price. **The knowledge of the
weight.** The series assumes $Q$ known; Chapter 10 recovers the read operator from
the consumer, but its recovery result identifies the read *subspace*, under a
specified model, probe distribution, and output metric, and not the weights within
it, which an allocation also needs. Composing recovery with the series' coding
theorems, and charging for the probing, is the keystone T1 (Chapter 17).

And one thing the series establishes is read differently elsewhere. Its leakage is
the conditional information $I(X;\hat X\mid S)$; that this quantity is the ideal work
to reset a record against the holder's knowledge is a further claim, which uses the
physical memory and reset model of the consumer-relative Landauer paper, in which
the downstream consumer and the physical reset agent are different parties.

## COST, in one line

Observation charges a rate, the rate is $R_C(D)$, and its whole difference from
Shannon is a tilt of the bit-allocation toward the read subspace — with a commission
tax for protecting too much and an omission floor for protecting too little. The next
chapter shows what you *buy* by paying the tilted price instead of the reconstruction
price: the flip.
