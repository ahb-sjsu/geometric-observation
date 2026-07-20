# Preface

> **RUNNING EXAMPLE — Maya's Cache**
>
> Meet Maya Okonkwo. She is twenty-nine, an inference engineer at a company that
> serves a large language model to millions of users a day, and she has just built
> something she is proud of: a quantizer for the model's key–value cache that halves
> its memory footprint. She measured it the way everyone measures a compressor. The
> reconstruction error — the average squared difference between the original cached
> vectors and their compressed versions — is the lowest her team has ever recorded.
> By every number on her dashboard, the compression is nearly lossless. She ships it
> behind a flag to one percent of traffic.
>
> The model gets dumber. Not catastrophically; subtly. It loses the thread in long
> conversations. It misattributes quotes. Its answers drift. The reconstruction
> error is beautiful and the product is worse, and for two weeks nobody can say why,
> because the one number everyone trusts says nothing is wrong.
>
> The problem, Maya will discover, is not in any bit of her quantizer. It is
> geometric. The attention head that consumes her cache does not read the key
> vectors. It reads a few *directions* of them — the ones its queries point along —
> and it is blind to the rest. Her quantizer spent its bits reconstructing the whole
> vector faithfully, which meant spreading its error evenly, which meant putting
> error exactly where the head was looking. A worse-reconstructing quantizer that
> happened to protect those few directions would have kept the model sharp. She had
> been optimizing the wrong metric with great precision. This book is about the
> right one.

---

This book began as a footnote to someone else's collapse.

In 2025 I was reading a result I did not like. Ulrike von Luxburg, Agnes Radl, and
Matthias Hein had proved that the commute-time distance — the resistance metric you
get from a graph Laplacian, the workhorse of spectral embedding — *degenerates* on
large graphs. As the graph grows, the distance between two nodes stops depending on
the graph's global structure and collapses to a function of their local degrees.
The embedding everyone used to *see* the geometry of a dataset was, in the limit,
seeing almost nothing but density. It was a clean, discouraging theorem, and the
natural conclusion was that the tool was broken.

I did not believe the geometry had vanished. It had to have gone *somewhere*. So I
did the pedantic thing and wrote each node's low-dimensional embedding in polar
coordinates — a magnitude times a direction — and asked which half was collapsing.
The answer was immediate and, in retrospect, obvious: the magnitude was carrying
the degree, the density, the nuisance that von Luxburg's theorem said would swamp
everything. And the *direction* — the angle — was carrying the graph geodesics,
almost undamaged. The geometry had not died. It had moved into the coordinate
nobody was reading. Keeping only the angle is exactly the row-normalization step in
Ng–Jordan–Weiss spectral clustering, a move practitioners had been making for years
on the grounds that it "worked"; the polar decomposition said *why* it worked, and
gave it a metric-geometric justification. [proved]

That was supposed to be the whole story: a small correction to a spectral-embedding
folk theorem. It was a footnote. It refused to stay one.

Because the shape of the correction generalized before I was ready for it. The
angle was not special. What was special was that there existed a *reader* — the
geodesic-ranking use of the embedding — for whom the angle was signal and the
radius was nuisance, and the collapse theorem was a theorem about the nuisance
coordinate only. Change the reader and you change which coordinate is which. An
attention head reads query-weighted directions and discards the across-token mean.
An optimizer reads curvature-weighted error and is blind to the flat directions of
its loss. A retrieval index reads the projection onto its query subspace and throws
away the rest. Each of these is *the same picture as the polar decomposition*: a
reader that keeps a few directions and quotients out the others. The angle was one
instance of a structure I had mistaken for a special case.

I started calling the general object the **read metric**. Fix any consumer $C$ — a
classifier, an estimator, an attention head — and ask how much its output moves
when you perturb its input. The answer is a symmetric operator, $P_C = J^{\top} G
J$, the pullback of the consumer's own output metric through its Jacobian. Its
range is the handful of directions the consumer can actually distinguish; its
kernel is everything the consumer is constitutionally blind to. This is not a new
object — it is the pullback metric of classical information geometry, the thing
Amari and Čencov studied — and I want to be scrupulous that the *components* are
old. What was not old, and what this book is about, is the claim that this pullback
is the operative object for *lossy representation*: that the right way to compress,
embed, or quantize anything is to keep the structure inside $P_C$ and spend nothing
on $\ker P_C$, and that "reconstruct the object faithfully" is the special, and
usually wrong, case $P_C = I$.

Then the correspondences began to accumulate, and each one cost me a month.

The first was the one that still surprises audiences: the **flip**. If the read
metric is the object, then at a matched bit budget two codes can be ranked
*oppositely* by two different consumers, and — the sharp version — a code that
reconstructs the source *worse* can serve a consumer *better*. This is not a
tendency; it is a reversal, and it should either be everywhere or be an artifact.
So we went looking for it, under a discipline I will describe in a moment, and it
was everywhere. It appears on transformer KV-keys [demonstrated]. It appears on
embedding retrieval [replicated]. It appears in gradient compression against a
curvature consumer [predicted]. And then it walked out of machine learning
entirely: it appears in direction-of-arrival estimation on a microphone array
[predicted], in a second, independent acoustic corpus [predicted], and — the one I
did not expect — in *seismic backazimuth*, elastic waves from real earthquakes read
by a thirteen-element array in the ground, where a compressor that reconstructs the
waveform better points at the wrong epicenter [predicted]. Twelve domains. Three
distinct branches of physics — electromagnetic, acoustic, elastic. One mechanism.
When a picture drawn from a graph-embedding footnote predicts which quantizer will
best locate an earthquake, either it is a coincidence of unusual size or the
footnote was never small.

The second correspondence was that the read metric has a *price*, and the price is
a rate–distortion theory. If a consumer only reads $P_C$, then the number of bits
you must pay to serve it to distortion $D$ is not Shannon's $R(D)$ but a tilted one,
$R_C(D)$, whose whole content is that the tilt bends the water-filling toward the
read subspace. This gave achievability and converse theorems, a two-observer rate
region whose refinability is exactly a Loewner nesting of read metrics, a mismatch
tax you pay for using the wrong $P_C$, and an *omission floor* — a wall of
irreducible downstream error you hit when your code is blind to a direction the
consumer reads, no matter how many bits you spend. That floor, predicted from the
theory, was later measured biting a real language model [demonstrated].

The third correspondence closed the loop. Cost, value, and legibility were not
three theories. They were three shadows of one object. The read metric $P_C$ is
what observation *charges* for (its rate–distortion function is the COST), what
preserving it *buys* (the flip is the VALUE), and what its quotient *reveals* (the
angle carrying geodesics is the LEGIBILITY). An observer, I came to think, is not a
viewpoint or a measurement device. It is a triple $O = (C, G, B)$ — a consumer, an
output metric, and a budget — and geometry, distortion, and reliability are not
properties of an object at all. They are properties of the *relation* among an
object, an observer, a channel, and a budget, and they are ill-posed until all four
are named.

The footnote, it turned out, was the thesis. This book develops it.

---

**A word on what this book is, and is not.**

*It is a mathematics book with an instrumented spine.* The central contribution is a
structural claim — that a single pullback operator organizes lossy representation
across domains — together with the theorems that make it precise and the sealed
experiments that make it falsifiable. Chapter 6 develops the needed machinery from
pullbacks and projections, assuming linear algebra and a first course in
probability. But the mathematics is not ornamental, and neither are the
experiments. Each is load-bearing for the other: the theory says where to look,
and the ledger says whether it was there.

*It is not a new compression algorithm, and it is not a claim to have invented the
pullback metric.* The components — the pullback of an output metric, reverse
water-filling, rate–distortion, spectral embedding — are classical, and I have
tried to cite them exactly where they are owed. The claim is the *synthesis*: that
this old object is the operative one for the modern problem of serving
representations to consumers, and that naming it dissolves a family of apparently
unrelated engineering surprises into one mechanism with one dial.

*It is not a claim that reconstruction never matters.* It matters exactly when the
consumer reads everything — when $P_C = I$ — and that case is common and important
and is the one all our tools were built for. The book's argument is that this case
is a *slice*, not the whole, and that the practice of measuring every compressor by
its reconstruction error is a habit inherited from the slice.

*And it is not a program that hides its losses.* This is the part I most want a
skeptical reader to test first. Every risk-bearing prediction in this book was
**sealed before it was measured** — hashed and git-committed as a prereg, with its
pass/fail bar written in advance — and the misses are printed at the same
prominence as the hits. There is a whole chapter of them (Chapter 16). The
consumer-relative flip does *not* appear when the read operator is aligned with the
signal's energy; we predicted it would appear in real-model gradient compression
and it did not, because in a trained model curvature and gradient energy are
coupled, and we say so [refuted]. A density quotient we hoped would generalize
outside diffusion was refuted across four domains [refuted]. A blind probe on a real
frontier model recovered the read operator but missed its sealed bar, bounding the
theory to synthetic consumers on that evidence until a corrected design passed
[refuted → demonstrated]. These are not embarrassments to be managed. They are the
boundaries of the result, and a result without stated boundaries is not a result.
The program's governing sentence, inherited from the series and enforced here by a
written charter, is: *the book may not assert what the ledger cannot show.*

---

The book has seven parts, moving from the problem through the framework and its
three shadows to the instruments, the evidence, and the discipline that produced
it. Part VI, on that discipline, could have been an appendix; I have made it a part
because in a program co-designed with an embedded AI assistant — one that may
propose and derive and draft, but that *may not be the sole grader of its own
work* — how the claims are kept honest is not separable from what they are.

I did not set out to write it. I set out to fix a footnote about an angle. The
angle turned out to be one shadow of a thing that casts three, and the thing has a
name, and this is its book.

*A.H.B.*
*San José, 2026*
