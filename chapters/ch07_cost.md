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
tilt away from Shannon's source-only allocation is precisely the factor $P_C$; the
"true-divergence reduction" relative to reconstruction coding *is* that tilt.
[proved — Appendix B, Thm B1; conclusion-grade via a committed Blahut–Arimoto harness]

Two operational consequences frame the rest of the chapter.

**Reconstruction is wasteful by a computable amount.** A code that reconstructs $x$
(optimizes $P_C = I$) spends bits on $\ker P_C$ that buy the consumer nothing. GO-6
measures this end to end: at matched rate, **output coding $\le$ surrogate $\le$
reconstruction** on the consumer metric, the ordering holding at *every* rate, with
reconstruction up to $\sim 500\times$ worse downstream at high rate because its bits
went to the unread directions [demonstrated — GO-P-2026-028, all bars pass, nonlinear
consumer $d=8, r=4$]. The isotropic control $P_C = I$ collapses the three coders, as
it must — when the consumer reads everything, there is nothing to save.

**The surrogate–output gap vanishes with rate.** GO-6 also confirms Thm B3: the
relative gap between an output-optimal code and a good surrogate shrinks (measured
$0.41 \to 0.005$) as the budget grows [demonstrated]. At high resolution you do not
need to know the consumer exactly; a surrogate for $P_C$ suffices. At low resolution
you do. This is the rate-dependence that makes the blind probe (Chapter 10)
load-bearing precisely in the bit-starved regime where compression matters.

## Two observers: the rate region and refinability

Serving *two* consumers from one code is a network-information-theory problem, and it
has an exact structure. For observers with read metrics $P_1, P_2$ the achievable
rate region is characterized, and its **refinability** — whether a single scalable
code can serve the coarse observer with a prefix of the bits it serves the fine one —
holds exactly when the read metrics are **Loewner-nested**, $P_1 \preceq P_2$
[proved — Appendix B; the two-observer max-determinant program, prereg GO-P-2026-022].
Nesting is the precise sense in which one observer is "a refinement of" another: it
can be served by adding bits, not resending them. When the read metrics are *not*
nested, there is an exact rate loss for serving both, and the theory quantifies it.

This region carries one of the program's standing verification incidents, and it is
worth stating because it is exactly the kind of error the discipline exists to catch.
The in-context derivation of the two-observer error covariance used a water-filling
formula with an inline claim that a certain cap "never binds"; a fresh-context
adversarial pass found the max-determinant error covariance is reverse water-filling
in the *whitened* basis and the cap **does** bind on $\ker P$ (VI-4). The formula was
corrected, the prereg amended and re-sealed, and the false pass logged with the same
prominence as a positive. The theorem statements — the abstract max-det program — were
unaffected; the harness was wrong and the harness was fixed. This is what "[proved]
means both grades" buys you: the analytic claim and the numerical net disagreed, and
the disagreement was the alarm.

## The $k$-chain and what counts a dimension

For $k \ge 3$ observers in a chain the tight region is Kostina–Tuncel's, not a naive
iteration of the two-stage map — another caught error (VI-5): the two-stage
construction *does not iterate*, because an accumulating rotation ambiguity leaks
Fisher information by $O(0.1)$ per stage; the correct achievability uses independent
Fisher increments from physically-degraded channels, exact to $10^{-14}$
[proved, corrected; prereg GO-P-2026-023]. The lesson survives the technicality: a
chain of observers is not a stack of two-observer problems, and the geometry that
makes it work is the nesting of read metrics.

Dispersion — the second-order term governing finite-blocklength performance — counts
the **read** dimensions, not the source dimensions. The effective dimension is $r_D
\le r$, equal to the read rank only as $D \to 0$; a fresh-context pass sharpened a
draft that had claimed a flat $r$ (VI-7). The number of directions that cost you at
finite blocklength is the number the *consumer* resolves at the target distortion, and
that number grows from few to $r$ as you demand more fidelity.

## Mismatch: the tax and the floor

The two results with the most operational bite are about using the *wrong* read
metric — which is what every reconstruction-optimal code does.

**The commission tax.** Coding for a read metric of rank $M$ when the consumer's is
rank $m < M$ costs an excess rate of order $(r/2)\log(M/m)$ — you pay to protect
directions the consumer does not read [proved — Appendix B; prereg GO-P-2026-024].
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
[proved — prereg GO-P-2026-024]).

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

## COST, in one line

Observation charges a rate, the rate is $R_C(D)$, and its whole difference from
Shannon is a tilt of the bit-allocation toward the read subspace — with a commission
tax for protecting too much and an omission floor for protecting too little. The next
chapter shows what you *buy* by paying the tilted price instead of the reconstruction
price: the flip.
