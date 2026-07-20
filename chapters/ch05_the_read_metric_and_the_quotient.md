# Chapter 5 — The Read Metric and the Quotient

This chapter develops the two objects the observer triple induces — the read metric
$P_C$ and the quotient $X/\!\sim_C$ — with enough care to carry Parts III and IV. The
mathematics is elementary; the discipline is in taking it literally.

## The read metric

Fix an observer $O = (C, G, B)$ with consumer $C : X \to Y$ and output metric $G$ on
$Y$. Linearize the consumer at the operating point $x_0$: a small perturbation $\delta
\in X$ produces, to first order, an output change $J\delta$ where $J = \partial C
|_{x_0}$ is the Jacobian. The downstream cost of that perturbation, measured by the
output metric, is

$$ \|C(x_0 + \delta) - C(x_0)\|_G^2 \;\approx\; (J\delta)^\top G (J\delta)
   \;=\; \delta^\top \underbrace{(J^\top G J)}_{P_C}\, \delta. $$

The operator

$$ \boxed{\,P_C = J^{\top} G\, J\,} $$

is the **read metric**. It is symmetric and positive-semidefinite by construction (a
pullback of a PSD metric), and it is the quadratic form that turns an input
perturbation into a downstream cost. Everything the consumer "cares about," to first
order, is in this operator; everything it is blind to is in the operator's kernel.

Three properties matter.

**Range and kernel.** $\operatorname{range}(P_C)$ is the *read subspace* — the
directions in which a perturbation costs something. $\ker(P_C) = \ker(GJ)$ (and, when
$G \succ 0$, $= \ker J$) is the *nuisance* — the directions in which the consumer's
output does not move at all. A perturbation entirely inside $\ker P_C$ is invisible to
the observer, no matter how large.

**Rank.** The read subspace is usually *low-dimensional*. An attention head reads a
handful of query directions; a binary classifier reads essentially one direction (the
weight vector); a DOA estimator reads the one direction its array manifold is
sensitive to at the operating angle. The gap between $\dim X$ (large) and
$\operatorname{rank}(P_C)$ (small) is the entire opportunity: it is the room in which
a code can be terrible at reconstruction and excellent at serving the consumer.

**Operating-point dependence.** $P_C$ is a *local* object — it depends on $x_0$
through $J$. For a linear consumer it is global; for a nonlinear one it varies over
$X$, and the honest version of every result carries $P_C$ as a field, not a constant.
The blind probe of Chapter 10 recovers $P_C$ *at* an operating point precisely because
it is local; averaging it over a data distribution gives the $\bar P_C$ that enters
the alignment law $\kappa$ (Chapter 12).

## The read distortion

Now let a code introduce error $\delta = \hat x - x$ with covariance $\Sigma_\delta =
\mathbb{E}[\delta\delta^\top]$. Taking expectations of the local cost,

$$ \mathbb{E}\,\|C(\hat x) - C(x)\|_G^2 \;\approx\; \mathbb{E}[\delta^\top P_C \delta]
   \;=\; \operatorname{tr}(P_C\, \Sigma_\delta). $$

The **read distortion** $\operatorname{tr}(P_C \Sigma_\delta)$ is the quantity that
governs downstream loss at a fixed budget. Compare it to the total reconstruction
distortion $\operatorname{tr}(\Sigma_\delta)$: the two agree iff $P_C = I$ (Chapter 2)
and can otherwise disagree in both magnitude and *ordering*. The read distortion is
what the three engineers of Chapter 1 should have minimized; it is the objective the
COST theory optimizes (Chapter 7) and the quantity the flip is a statement about
(Chapter 8).

A warning the ledger insists on. The read distortion is the *controlling* quantity
for the discriminating comparison, but it is **not a complete rank statistic**. On the
KV-key domain, $\operatorname{tr}(P_C\Sigma_\delta)$ correctly predicts the flip 12/12
yet misorders a *middle* pair of codes whose per-token error has cross-token structure
the trace cannot see (NEG-9, [refuted, as a complete statistic]). The mechanism is
real; the scalar summarizing it is not exhaustive. When this book says "governed by
$\operatorname{tr}(P_C\Sigma_\delta)$," it means the trace governs the comparison the
theory is about, not that a single number reproduces the full downstream order. This
honesty is not a hedge; it is the difference between a [demonstrated] claim and an
over-claim.

## The quotient

The read metric measures directions; the quotient collapses them. Define an
equivalence on $X$ by

$$ x \sim_C x' \iff x - x' \in \ker P_C, $$

and form the quotient space $X/\!\sim_C$. Two inputs that differ only by a nuisance
direction are the *same point* of the quotient — the observer cannot separate them,
so for the observer they are one object. The consumer's verdicts live on $X/\!\sim_C$:
$C$ factors through the quotient (to first order), because it is constant along
$\ker P_C$.

The quotient is where LEGIBILITY happens. When you quotient an object by what an
observer cannot see, the structure that survives is the structure the observer acts
on — and sometimes, strikingly, that surviving structure is *cleaner* than the
original. The paradigm case is Keep-the-Angle (Chapter 9): quotient a spectral
embedding by the geodesic-rank consumer's kernel (the radius) and what remains — the
angle — carries the graph geodesics that the full embedding's distances had lost to
density. The quotient did not throw away signal; it threw away the nuisance that was
*drowning* the signal. This is the sense in which discarding structure can reveal it,
and it is one of the three shadows.

## An identity worth stating: the tangential-noncollapse condition

The LEGIBILITY leg turns on a small exact fact that is worth stating here because it
recurs. Writing an embedding in polar form $x = r\,u$ with $u$ on the unit sphere, the
angular reading is well-behaved precisely when the embedding velocity is not purely
radial — when moving along the manifold moves the *direction* $u$ and not only the
magnitude $r$. The program calls this **tangential noncollapse**, and it borrows the
label (A2) from the broader Observation-Theory framework as an organizing name. The
exact normalization identity behind Keep-the-Angle locates the mechanism *here* — in
tangential noncollapse — rather than in any constancy of the radius [proved]. The
point for this chapter is structural: the read metric of the geodesic-rank consumer is
nondegenerate on the angular coordinate exactly when (A2) holds, and the flip and the
legibility both trace back to whether the consumer's read subspace is *misaligned*
with the source's energy — a theme the alignment law $\kappa$ (Chapter 12) makes
quantitative.

## Identifiability, previewed

There is an obvious objection: all of this assumes you *know* $P_C$, and for a trained
consumer you do not have $J$ in closed form. The framework's answer, developed in
Chapter 10, is that $P_C$ is **identifiable from the consumer's behavior alone** — you
recover the read subspace by finite-differencing the consumer's output, with no
labels and no oracle direction, and this recovery has been demonstrated on planted
subspaces (GO-1, [predicted]) and on a real citation-ranking consumer (the legal
035→036→039 sequence, [demonstrated]). The read metric is not a quantity you must be
handed; it is a quantity you can measure. Chapter 6 assembles the linear-algebraic
machinery — pullbacks, projections, and the geometry of $\operatorname{tr}(P_C
\Sigma_\delta)$ — that both the theory and the probe stand on.
