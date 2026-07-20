# Chapter 4 — The Observer Triple $O = (C, G, B)$

Part I argued that geometry, distortion, and reliability are relational and that the
missing term in the relation is the observer. This chapter defines the observer
precisely enough to compute with, and then spends its second half doing the one thing
that makes an abstraction believable: naming six real observers and reading off, for
each, what it sees and what it throws away.

## The definition

An **observer** is a triple

$$ O = (C, G, B). $$

- $C : X \to Y$ is the **consumer**: the map from the representation to whatever acts
  on it. $C$ can be a linear read-out, a trained classifier, an attention head, a
  direction-of-arrival estimator, a ranking function. It is, deliberately, whatever
  is downstream. $X$ is the space of the thing you are compressing or embedding; $Y$
  is the space of the consumer's outputs.

- $G$ is the **output metric** on $Y$: how the consumer's downstream errors are
  scored. For a classifier producing logits, $G$ might be the Fisher metric of the
  softmax; for an estimator producing an angle, $G$ is squared angular error; for a
  ranker, the metric that scores rank distortion. $G$ is where "what counts as a
  downstream mistake" is written down.

- $B$ is the **budget**: the resolution you may spend — bits per symbol, codebook
  size, embedding dimension. Every verdict in this book is *budget-relative*; a code
  that wins at one budget can lose at another, and Chapter 8's flip and Chapter 7's
  rate–distortion curves are statements about how the verdict moves with $B$.

The triple is the whole of the observer. Nothing else about "who is looking" enters
the theory. In particular there is no privileged, observer-free description of $x$
that the observer then "sees imperfectly." There is $x$, and there are observers, and
each observer induces its own geometry on the space of $x$. That is the content of
calling the framework *consumer-relative*: the relativity is not epistemic modesty,
it is the structure.

## What the triple induces

Two objects follow immediately from the triple, and they are the objects the rest of
the book computes with. The first is the **read metric**

$$ P_C = J^{\top} G\, J, \qquad J = \partial C \big|_{x_0}, $$

the pullback of the output metric through the consumer's Jacobian at the operating
point $x_0$ (Chapter 5 develops it in full). The second is the **quotient** $X /
\!\sim_C$, in which two inputs are identified when the consumer cannot tell them
apart — when their difference lies in $\ker P_C$. The read metric says *how finely*
the observer resolves each direction; the quotient says *which world* the observer
actually acts on, the world with the unreadable directions collapsed to points.

An observer, operationally, *is* its read metric and quotient, up to budget. Two
consumers with the same $P_C$ are the same observer for our purposes even if their
internals differ wildly; two consumers with different $P_C$ are different observers
even if they share a name. This is why the framework can carry a single mechanism
across a language model and a seismometer array: they are unrelated machines with,
sometimes, the same read metric structure.

## The consumer table

Here is the abstraction cashed out. Each row is a real consumer from the program's
work; each says what the observer reads (the range of $P_C$) and what it discards
(the kernel).

| Consumer | reads (range of $P_C$) | in $\ker P_C$ (discarded) | instance |
|---|---|---|---|
| softmax attention | query-weighted directions | across-token mean | KV keys |
| geodesic rank | angle | radius = density | spectral embeddings |
| optimizer | curvature-weighted error | flat directions of the loss | gradients, Adam |
| retrieval ranking | read-subspace projection | off-subspace energy | ADC / vector search |
| classifiers (moral, genre, dialect) | weight geometry | invariant transforms | ETHICS, FMA, whale codas |
| recognizer | low multiplets + angular distances | high modes | rewrite substrates |

Read the table slowly, because every later result lives in it.

**Softmax attention** reads the directions its queries point along; an attention
logit is $q^\top k$, so perturbing a key along $q$ moves the output and perturbing it
orthogonal to every query does not. The read metric is (to leading order) the query
second-moment matrix. The across-token mean of the keys is a gauge the softmax
quotients away. This is Maya's consumer, and it is why her uniform-error quantizer
failed: uniform error has a component along $q$.

**Geodesic rank** — ranking embedding points by their geometric distance — reads the
*angle* in the polar decomposition and discards the radius, which von Luxburg's
theorem tells us is exactly the coordinate that collapses to density. The read metric
sees the sphere; the density is in the kernel. This is Keep-the-Angle (Chapter 9).

**An optimizer** reads its update against the loss curvature: a gradient error in a
high-curvature direction changes the trajectory, an error in a flat direction is
nearly free. The read metric is the Hessian (or its preconditioned form). This
consumer is why gradient compression has a consumer-relative theory too — and, as
Chapter 12's boundary shows, why the flip is *subtle* here: in a trained model the
high-curvature directions coincide with the high-energy directions, so the read
metric is coupled to the source (a true boundary, D4, [refuted-as-flip]).

**Retrieval ranking** reads the projection of a query onto a learned subspace and is
blind to off-subspace energy; the read metric is the projector onto that subspace.
This is Devi's consumer.

**Classifiers** — the moral-judgment classifier on ETHICS, the genre classifier on
music, the clan/dialect classifier on whale codas — read the geometry of their weight
vectors and are invariant to transformations that do not cross a decision boundary.
The read metric is recovered blind from the classifier's margin (Chapter 10), and
these consumers supply three of the sweep's confirmations (Chapter 13).

**The recognizer** — a consumer of a different flavor, the subject of Chapter 11 —
reads the low eigen-multiplets and angular distances of a representation to decide
which manifold it lies on, discarding the high modes. Its kernel is where "which
manifold" information is not.

Six observers, six read metrics, one operator. The table is not an illustration of
the theory; it is the theory's extension, the set of things it is *about*.

## Why all three of $C$, $G$, $B$ are load-bearing

It is tempting to think the consumer $C$ is the whole story and $G$, $B$ are
bookkeeping. They are not, and the ledger has the receipts.

**$G$ matters** because the same $C$ under a different output metric is a different
observer. A classifier scored by accuracy and the same classifier scored by
calibrated log-loss have different $G$, hence different $P_C$, hence potentially
different verdicts on the same code. Naming $G$ is naming what a downstream mistake
*is*, and there is no consumer-free answer to that.

**$B$ matters** because verdicts invert with budget. Chapter 8's flip is stated at
*matched bits* for a reason: change the budget and the ranking of two codes can
reverse (this is GO-4, the budget-inversion result, [replicated] — the same substrate
gives opposite refinement verdicts at fixed versus budget-matched observation). A
claim about a code that does not name its budget is, like a reconstruction number
that names no consumer, unanswerable-as-posed.

The observer triple is the smallest object that makes the questions of this book
well-formed. With it defined, the next chapter can build its two induced objects — the
read metric and the quotient — with the care they need to carry the rest of the book.
