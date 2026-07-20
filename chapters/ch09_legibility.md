# Chapter 9 — LEGIBILITY: What the Quotient Reveals (Keep the Angle)

The COST shadow prices the read; the VALUE shadow shows what preserving it buys. The
third shadow is the quietest and, to me, the most beautiful: when you quotient a
representation by what an observer cannot see, the structure that survives can be
*cleaner* than the original. Discarding the nuisance does not merely avoid harm; it
reveals. This is LEGIBILITY, and its paradigm is the result that started the whole
program — Keep the Angle.

## The collapse, and where the geometry went

Recall von Luxburg–Radl–Hein (Chapter 3): the commute-time distance from a graph
Laplacian degenerates as the graph grows, converging to a function of local degree and
losing the global geometry. Read as a verdict, the spectral embedding dies at scale.

Put each node's low-mode embedding in polar form, $x = r\,u$ with $u$ on the unit
sphere. The commute distance is the reading of this embedding by one observer — the
geodesic-rank consumer — and its read metric, worked out, is *nondegenerate on the
angular coordinate and degenerate on the radial one.* The collapse is confined to the
radius; the radius carries the degree and density (the nuisance the theorem says will
swamp everything), and the **angle carries the graph geodesics, almost undamaged**
[proved]. The geometry did not vanish. It moved into the coordinate the
distance-reading discards, which is to say into the read subspace of the
geodesic-rank observer and out of the kernel where density lives.

Quotient by the nuisance — drop the radius, keep the angle — and the surviving object
is the geodesic structure you wanted. This is legibility through quotient: the
observer that ranks by geodesics reads exactly the coordinate the collapse spares, so
for *that* observer the embedding never degenerated at all.

## The folk practice, explained

The practical payoff is that a decade-old heuristic turns out to be optimal. Spectral
clustering's Ng–Jordan–Weiss step row-normalizes the embedding — projects every node
onto the unit sphere, keeping direction, discarding magnitude — because it improved
results. Row-normalization *is* the projection onto the angular coordinate, which *is*
the read subspace of the geodesic-rank consumer, which *is* the coordinate the
collapse spares. The heuristic was doing consumer-relative coding without a name for
it: protecting the read subspace, quotienting the nuisance. Keep-the-Angle supplies the
name and the theorem [proved].

## The exact mechanism: tangential noncollapse, not radius constancy

It would be easy to mislocate the mechanism as "the radius is constant." It is not; the
radius varies (that is the density it carries). The exact normalization identity
locates the mechanism in **tangential noncollapse** (the (A2) condition of Chapter 5):
the angular reading is faithful precisely when the embedding velocity is not purely
radial — when moving along the manifold turns the *direction* $u$ and not only the
magnitude $r$. Where (A2) holds, the angular read metric is nondegenerate and the
geodesics survive; where the velocity goes purely radial, it does not. The condition is
sharp, and getting it right mattered: an early over-claim (that a certain heat-taper
reversal held on a real embedding model) is carried as a standing negative pending
confirmation (NEG-3, [refuted, pending confirm]).

## The exactly-solvable cases

Legibility is not only asymptotic; on symmetric spaces it is exact, and the exact cases
are where the theory is most testable.

**The circle $S^1$: rank collapse, proved.** For the plain (unfiltered) commute filter
on the circle, the angular read metric collapses to **rank 1** — an exact statement,
provable in closed form [proved]. This is the cleanest instance of the read metric
being genuinely low-rank: on $S^1$ the geodesic-rank observer reads *one* direction.

**Flat tori: a uniform lower angular bound.** On flat tori the program proves a uniform
lower bound on the angular preservation via a dyadic-block argument — the numerator and
denominator of the angular sensitivity grow at the same dyadic rate and compensate,
giving co-Lipschitz control that does *not* degrade with the mode count [proved]. Paired
with the exact upper-Lipschitz *divergence* for the commute filter (the sensitivity
$\|dN_R(e_j)\|^2 = |K_R|/(d\,S_R)$, Lipschitz constant growing like $R^{1/2}$,
$\sqrt{\log R}$, $R$ for $d = 1, 2, \ge 3$), these bracket the filter's behavior exactly
and locate the phase transition. The spectral-filter phase diagram has three Weyl
thresholds ($s > d/4$, $s > d/2$, $s > d/2 + 1$) and a **critical dimension $d = 4$**
where the rank form's uniformity breaks [proved]. The rank form of Angular Preservation
is uniform *below* $d = 4$ — a Green-kernel rank-limit theorem shows that for intrinsic
dimension $d \le 3$ the angular ranking converges, uniformly in the mode count, to a
fixed Green-kernel ranking (exactly rank 1 on two-point homogeneous spaces $S^2, S^3,
\mathbb{RP}^2, \mathbb{RP}^3$), reducing Angular Preservation to positivity of a single
geometric coefficient [proved]; the positivity itself is the standing Green-rank
conjecture (Chapter 17).

The negative that bounds all this is NEG-1: fixed-scale, *uniform-in-$m$*
bi-Lipschitzness for the commute filter is **refuted** — the bound is scale-dependent,
and the uniform version fails [refuted]. The heat filter, by contrast, *is*
uniform-in-truncation bi-Lipschitz. The dichotomy is sharp and it is stated both ways.

## Legibility beyond the angle: the $\alpha = 1$ test and dimension-before-shape

Two further legibility results generalize the idea past spectral embeddings.

**The $\ker P_C$ membership test.** For the density-quotient family indexed by an
exponent $\alpha$, the *sign* of the $\alpha = 1$ response is a membership test for
$\ker P_C$: it tells you whether a given nuisance direction is truly in the observer's
kernel [demonstrated, in the spectral/operator setting]. This is legibility as a
diagnostic — reading off, from a response sign, what the observer discards. Its
*boundary* is one of the program's sharpest negatives: the hope that an $\alpha = 1$
density quotient would restore fidelity *outside* diffusion was refuted across four
non-spectral domains — the restoration is $<2\%$ and not density-specific (a uniform
control gains as much), so the density-nuisance-removal mechanism is absent
[refuted — NEG-11]. The retained positive is exact and narrow: $\alpha = 1$ is the
optimal diffusion exponent, and the Laplace–Beltrami effect it names is
**operator/spectral-confined.** Legibility through the density quotient is a real
mechanism inside diffusion and a refuted one outside it, and the book says both.

**Dimension emerges before shape.** The recognizer (Chapter 11) exploits a Weyl-law
ordering: a representation's intrinsic *dimension* is legible from the low
eigen-multiplet structure before its *shape* is — the counting function fixes $d$ ahead
of the finer geometry [demonstrated]. You can read how many dimensions a manifold has
before you can read which manifold it is. This is legibility as staged revelation, and
it is the principle the recognizer is built on.

## What the quotient reveals, in one line

Quotient a representation by an observer's kernel and the surviving structure is what
that observer acts on — and when the kernel was carrying the nuisance that drowned the
signal (density, magnitude, degree), the quotient is *more* legible than the original,
not less. Keep the angle, and the geometry the distance lost comes back. With the three
shadows in hand — the price, the payoff, the meaning of the read — Part IV turns to the
instruments that make them usable: the probe that recovers $P_C$, the recognizer that
reads the manifold, and the taxonomy-and-dial that says when the flip appears.
