# Chapter 1 — Why Observation Needs a Theory

Three engineers, in three different buildings, are about to make the same mistake.

The first is Maya, whom you met in the Preface. She has quantized a language model's
key–value cache to the lowest reconstruction error her team has ever recorded, and
the model has quietly gotten worse. The second is Devi, who builds the retrieval
index for a legal-search product; she has a new embedding compressor that shrinks
her vector database by 60% with almost no change in average vector fidelity, and her
citation-ranking accuracy has fallen off a cliff for reasons her dashboards cannot
locate. The third is Sun-ho, who works on a direction-finding array — microphones,
in his case, though it could as easily be radar or a seismometer network. He has a
codec that compresses the array snapshots with beautiful waveform fidelity, and his
estimator now points a few degrees wrong, consistently, in a way that averages out
to nothing and so hides in every summary statistic he trusts.

None of the three has a bug. Each has a compressor that does exactly what it was
asked to do — minimize the difference between the input and its reconstruction — and
each has a *downstream system that does not care about that difference.* The
attention head reads a few directions of Maya's keys. The ranking function reads a
projection of Devi's embeddings. The estimator reads the angle, not the magnitude,
of Sun-ho's snapshots. In every case the compressor spread its error to be small
*on average*, which is to say it put error everywhere, which is to say it put error
exactly where the consumer was looking. They optimized a quantity that was never the
one that mattered, and they optimized it well.

This book is about the quantity that mattered.

## The claim

Here is the thesis of the whole volume, stated once, plainly, so that everything
after it is commentary.

> Operational geometry, distortion, and reliability are not properties of an object.
> They are properties of a *relation* — among an object $x$, an observer $O$, a
> channel that carries $x$ to $O$, and a resolution budget $B$ — and they are
> ill-posed until all four are named.

The word doing the work is *observer*. In this book an observer is not a viewpoint,
not a person, not a measuring instrument in the physicist's sense. It is a triple

$$ O = (C, G, B): $$

a **consumer** $C$ — the thing that acts on the representation, a classifier, an
attention head, an estimator, a ranking function; an **output metric** $G$ — how the
consumer's downstream errors are scored; and a **budget** $B$ — the bits, or the
resolution, you are allowed to spend. Give me those three and I can tell you what
the observer can distinguish, what it must discard, and what it will cost to serve
it. Withhold any one of them and the questions "how much geometry survived this
compression?" and "how good is this code?" have no answers — not hard answers,
*no* answers, the way "how far away is it?" has no answer until you say from where.

The engineers' mistake was to answer a relational question with an absolute number.
Reconstruction error — mean squared error, PSNR, cosine similarity — is a property
of $x$ and its reconstruction $\hat x$ alone. It names no consumer. It is, as
Chapter 2 will make precise, the special case of the right quantity when the
consumer happens to read *everything* equally, and that case is neither typical nor
the one any of the three engineers were in.

## What the observer reads: the read metric

The mechanism that resolves all three stories is a single operator. Fix a consumer
$C$ and ask the only question that matters: how much does the consumer's output move
when you perturb its input? Differentiate $C$ at the operating point to get its
Jacobian $J$, pull the output metric $G$ back through it, and you have

$$ P_C = J^{\top} G\, J, $$

a symmetric, positive-semidefinite operator we will call the **read metric**. Its
range is the small set of directions the consumer can actually tell apart — the
*read subspace*. Its kernel is everything the consumer is constitutionally blind to
— the *nuisance*. Maya's attention head has a read metric whose range is spanned by
its query directions; the across-token mean is in the kernel. Sun-ho's estimator has
a read metric that sees the angle and not the magnitude. Devi's ranker reads a
projection and discards the off-subspace energy. Three unrelated systems, one object.

And the quantity the engineers should have been minimizing is not the size of the
coding error $\delta = \hat x - x$, but the size of the error *where the consumer
looks*:

$$ \operatorname{tr}(P_C\, \Sigma_\delta), $$

the error covariance projected onto the read metric. This trace and the total
reconstruction error $\operatorname{tr}(\Sigma_\delta)$ are different numbers, and —
this is the entire drama of the book — they can move in *opposite directions*. A
code that makes the first small can make the second large, and vice versa. When they
disagree about which of two codes is better, we call the disagreement the
**consumer-relative flip**, and Chapter 8 shows it is not a curiosity but a
reproducible property of observation, sealed across twelve domains and three
branches of physics.

## One object, three shadows

The read metric $P_C$ is the whole book, seen once. But it casts three shadows, and
the three shadows were discovered as three separate subjects before anyone noticed
they were one. This volume is organized around that unification.

- **COST** — what observation charges. If a consumer reads only $P_C$, the bits you
  must pay to serve it to a given distortion are governed by a *tilted*
  rate–distortion function $R_C(D)$, not Shannon's. The tilt bends the optimal
  bit-allocation toward the read subspace, and it comes with achievability and
  converse theorems, a rate region for two observers, a tax for using the wrong read
  metric, and a floor of irreducible error you hit when your code is blind to a
  direction the consumer needs. This is Part III's Chapter 7. *(Paper III.)*

- **VALUE** — what preserving the read buys. This is the flip: at matched bits,
  keeping $P_C$ beats reconstructing $x$, and the gap is real money on real tasks.
  Chapter 8. *(Papers II and IV.)*

- **LEGIBILITY** — what the quotient reveals. When you quotient an object by what an
  observer cannot see, the structure that survives is often the structure you wanted.
  In spectral embeddings, the observer that ranks by geodesic distance reads the
  *angle* and discards the radius, and so the angle carries the geometry that the
  distance-based reading loses. This is Keep-the-Angle, Chapter 9. *(Papers I and I.5.)*

Cost, value, legibility: the price of the read, the payoff of the read, the meaning
of the read. Three literatures, three sets of tools, one operator. The intellectual
content of this book is the claim that they are the same, and the discipline of this
book is the ledger that keeps the claim honest.

## Why a theory, and not just a warning

One could stop at the warning: *do not trust reconstruction error; know your
consumer.* That warning is true and it is not enough, because it gives no way to
*act*. A theory has to do three things the warning cannot.

It has to say **which** directions the consumer reads — and it does, via the read
metric, which Chapter 10 shows can be recovered *blind*, from the consumer's outputs
alone, with no labels and no oracle. It has to say **when** the flip appears and when
it does not — and it does, via the alignment law $\kappa$ of Chapter 12, which turns
"know your consumer" from folklore into a dial you can measure before you compress.
And it has to say **what it costs** to do the right thing — and it does, via the
rate–distortion theory of Chapter 7. A warning tells you to be careful. A theory
tells you what to compute.

The rest of Part I clears the ground: Chapter 2 shows precisely how
reconstruction-error thinking fails and why it was ever plausible, and Chapter 3
places the read metric where it belongs in the histories of information theory and
information geometry — as an old object we did not invent, pressed into a new job we
claim it was always the right tool for. Then Part II builds the framework from the
operator up.

A last word before we begin, because it governs everything. This is a program
co-designed with an embedded AI assistant, and it operates under a written charter
whose first rule is that the assistant may not be the sole grader of its own work,
and whose house rule — inherited from every volume of this series — is that *the book
may not assert what the ledger cannot show.* When a sentence in this book carries a
tag like [demonstrated] or [refuted], that tag is a promise about a specific row in
a specific ledger, sealed before it was measured. The three engineers' mistake was
to trust a number that named no consumer. The correction is not to trust a different
number more; it is to say, every time, whose number it is, and to show the receipt.
