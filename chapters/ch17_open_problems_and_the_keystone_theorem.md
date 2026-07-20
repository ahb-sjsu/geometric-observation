# Chapter 17 — Open Problems and the Keystone Theorem

A framework is honest about its frontier when it can say not only what it has shown
but what it has *not yet* shown, and which of the unshown things it is chasing versus
which it has deliberately named and set aside. This chapter is that accounting. It has
one recommended keystone — a theorem the program should prove next — and a short list
of genuine open problems, each stated with its current status so no reader mistakes an
aspiration for a result.

## The keystone: learn-then-serve (T1)

The single theorem worth proving next is the one that would bridge the two shadows that
are still only connected empirically: COST and VALUE. Call it **T1, learn-then-serve.**

The empirical situation is this. The COST theory (Chapter 7) prices serving a *known*
read metric $P_C$. The blind probe (Chapter 10) recovers $P_C$ from finitely many
queries. The flip (Chapter 8) shows that serving the recovered $P_C$ beats
reconstruction. What is missing is a theorem that composes the *sample complexity of
recovering $P_C$* with the *mismatch bounds of serving an imperfect $\hat P_C$* — a
single guarantee of the form:

> Given $N$ blind queries, the probe recovers $\hat P_C$ to accuracy $\varepsilon(N)$,
> and serving $\hat P_C$ instead of $P_C$ costs at most the mismatch tax
> $(r/2)\log(\cdot)$ plus a term in $\varepsilon(N)$ — so that with $N \gtrsim
> (\text{something explicit})$ queries, the learned-then-served code is within a
> stated factor of the oracle code, end to end.

This is the COST↔VALUE bridge, and it is the recommended keystone because it converts
the program's central practical claim — *recover the observer, then serve it* — from a
two-step empirical recipe into one theorem with an end-to-end guarantee. The pieces
exist: the probe's recovery rate is measured (GO-1, and the rate-dependence of the
surrogate gap in GO-6), and the mismatch tax and omission floor are proved (Chapter 7,
Appendix B). T1 would fuse them. It carries no result yet — it is a **stated target**,
not a theorem — and I flag it as such [status: open, recommended].

## The cross-domain magnitude constant

The sharpest *quantitative* gap is inherited from the 20-Newsgroups blind test (041,
Chapter 10). The blind non-oracle probe recovers the winning code's *direction*
prospectively — it chooses the better code before any label — and *across rates* the
predicted magnitude tracks the measured downstream gap almost perfectly (Pearson
0.995, both decreasing per the finite-rate criterion). But the *cross-domain scale
constant* — the single number that would turn "the flip is larger here than there" into
a calibrated point prediction transferable from one domain to the next — did not
transfer: the point magnitude overshot its sealed band on 041 [refuted, as a point
prediction; the direction and the within-domain rate-scaling hold]. Finding the
invariant that fixes this constant across domains is a concrete open problem with a
clean falsification test already built (the sealed-magnitude protocol of 041). It is
the difference between a theory that says *which* code wins and one that says *by how
much*, portably.

## The Green-rank positivity conjecture

From the LEGIBILITY leg (Chapter 9) comes a clean mathematical conjecture. The
Green-kernel rank-limit theorem reduces Angular Preservation, for intrinsic dimension
$d \le 3$, to the **positivity of a single geometric coefficient** — the leading
Green-kernel rank coefficient — and proves rank 1 on the two-point homogeneous spaces
$S^2, S^3, \mathbb{RP}^2, \mathbb{RP}^3$ [proved]. The **conjecture** is that this
coefficient is positive on a broad class of manifolds beyond the two-point homogeneous
ones, which would extend Angular Preservation's rank form from the exactly-solvable
symmetric cases to the general $d \le 3$ setting [status: conjectured]. It is a
self-contained problem in spectral geometry, and unlike T1 it does not need any new
empirical apparatus — only a proof.

## Named, not chased

Two directions are deliberately *named and set aside* — real, but not on the critical
path, and stated here so that their absence from the program's active work is a choice
rather than an oversight.

**The channel dual.** The COST theory prices the observer; a dual theory would price
the *channel* symmetrically, treating the compression channel and the observer as two
sides of one variational problem. The structure is visible (the two-observer max-det
program hints at it) but the program has not developed it, and it is named-not-chased
[status: named].

**The common-observation problem.** Given a *population* of observers, is there a single
representation that serves all of them near-optimally, and what is the price of the
compromise? The two-observer rate region (Chapter 7) is the $k = 2$ corner; the general
common-observation problem — the representation-design analogue of a public good — is
named and deferred [status: named]. The regime map's empty cell (concentrated /
low-correlation, Chapter 12) is a small instance of the same question and is flagged for
a synthetic fill or a structural-emptiness argument.

## The discipline's own frontier

The last open problem is methodological and was stated in Chapter 15: there is **no
mature standard toolkit for verifying AI-assisted work independently of the assistant
that produced it.** The program's composition — fresh-context adversarial verification,
differential testing against a second implementation, and a proof assistant for the
flagship theorem — is a reasonable approximation, and VI-4 is the standing evidence it
works and was needed. But it is not a recognized methodology, and building one is a real
open problem that this program can only gesture at from inside. The adopt-now upgrades
are concrete (mirror sealed preregs to OSF for a third-party timestamp; rewrite the C3
nets as property-based tests); the *general* solution is open [status: open, frontier].

## What is settled enough to build on

To end the chapter honestly the other way: the read metric as the operative object, the
three shadows as one object, the flip as a property of observation wherever the read
operator is identifiable, the blind probe as a working recovery instrument, and the
registration discipline as a functioning method — these are settled enough to build the
next volume on, in the precise sense that they carry ledger rows at their class bars. The
open problems above are the *edges* of a solid interior, not cracks in it. Chapter 18
states what that interior reduces to.
