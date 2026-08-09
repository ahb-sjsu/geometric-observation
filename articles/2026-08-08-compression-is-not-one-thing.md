# Compression is not one thing

### What a measured counterexample says about the claim that compression is intelligence

Andrew H. Bond, San Jose State University. 8 August 2026.

## Abstract

A familiar claim holds that compressing data well is the same activity as
understanding it, and that a system trained to compress is thereby trained to
be intelligent. The claim counts saved bits in one currency and does not ask
who the saving is for. We report a measurement that separates two encoders
whose compression quality is provably identical and whose downstream effects
are not. On sixteen attention heads of a trained three billion parameter
model, two key perturbations matched in reconstruction error to nine decimal
places differ in what the model does next by a median factor of nearly two,
and a blind probe of the reading operator predicts which one is worse on every
head, while reconstruction error, being tied, predicts nothing. The lesson is
not that the slogan is wrong in spirit. It is that the word compression in the
slogan is underdetermined until the reader is named, and that once the reader
is named the quantity is one information theory has had since nineteen fifty
nine. What is new here is not the quantity but the instrument. The reader can
be recovered from the system rather than assumed, and the cost of recovering
it is a hard floor set by dimension rather than by how much of the reader one
actually needs.

## Why anyone would look here

Work on lossy compression has always begun by choosing a measure of what
counts as damage. Textbooks say to choose one appropriate to the application
and then move on, and in practice the choice is made once, early, and rarely
revisited. Meanwhile a slogan has spread through machine learning that
compression is intelligence, supported by the observation that the loss used
to train language models is the same quantity that governs how well a
predictor can be turned into a compressor.

Both of these are reasonable. Together they invite an error. If damage is
whatever the chosen measure says it is, and if compressing well is the same as
understanding, then a system that lowers the chosen measure is understanding
more. That inference is only sound when the chosen measure is the one the
downstream use actually cares about, and nothing in the training loop checks
that.

We can now check it. The check has an answer, and the answer is that the two
measures come apart on real trained models by amounts large enough to reverse
a decision.

## The measurement

The setup compares two ways of perturbing the keys that an attention head
reads. They were constructed to be matched in reconstruction error, and the
match holds to within seven and a half parts in a billion, so no method that
scores an encoder by how far its output sits from the original can tell them
apart. Reconstruction is tied by construction.

Downstream they are not tied. The divergence in what the head attends to
differs between the two arms by a median relative factor of one point eight
five across sixteen heads drawn from two layers of a three billion parameter
model.

A probe that estimates the head's reading operator without being told what the
head does, and without seeing either arm's downstream behaviour, picks the
worse arm on sixteen heads out of sixteen. Reconstruction error picks the worse
arm on two out of sixteen. Chance is eight out of sixteen, so reconstruction is
not merely uninformative here. Its residual ordering, which is rounding noise
below the nanoscale, points the wrong way.

The probe recovers the head's reading subspace at a median overlap of zero
point six four seven where chance overlap is zero point one two six.

## What the counterexample does and does not show

It shows that two encoders can be equally good compressors under one honest
accounting and unequally good under another, on a trained model rather than a
synthetic one, with the discriminating quantity estimated blind.

It does not show that the slogan is false. For a reader that cares about every
bit equally, compressing well and serving the reader well are the same thing,
and the slogan is exactly right. That reader is the one implicitly assumed
whenever compression is discussed without an index. The measurement shows that
this reader is a special case and that real readers are not it.

## The framing that survives

Rate distortion theory has carried the general case since nineteen fifty nine.
One fixes a measure of damage, and the theory returns the fewest bits that
achieve a given level of it. Choosing that measure is choosing a reader. The
quadratic damage functional used throughout our work is a distortion measure in
exactly this sense, and the rule for spending bits across the reading
operator's spectrum is the classical rule for spending power across frequency
bands.

The deeper precedent is older still. Blackwell showed in the early nineteen
fifties that how informative one experiment is compared to another is a partial
order rather than a number, because different decision problems rank
experiments differently. Informativeness has never been scalar. A slogan that
treats compression as scalar was answered before it was coined.

So the correct statement of our position is modest. Compression is not one
thing, it is a family indexed by the reader, this has been known for seventy
years, and the useful work is not in restating it.

## What is new

Rate distortion assumes the distortion measure is handed to you. Ours is
measured. The probe estimates a trained model's reading operator without being
told the consumer, without labels, and without access to downstream behaviour,
and the estimate is accurate enough to reverse an encoder decision on every
head tested.

Two supporting measurements bound how much the choice matters and what it costs
to make it.

The choice matters more than a technicality. Two defensible references for a
single attention head, differing only in how the head's own queries are
weighted, disagree by about three tenths in overlap, and that disagreement
accounts for roughly two thirds of a gap that had previously been attributed to
the instrument.

The choice is expensive to avoid. Recovering the reading operator well enough
to act on requires a number of probe evaluations equal to the full dimension of
the space, and this requirement does not fall when only a few reading
directions are actually needed. Asking for one direction costs the same as
asking for sixteen. There is no low rank shortcut, because below full dimension
the estimate is a projection onto a random subspace and a projected operator's
leading direction is not the operator's leading direction unless that subspace
happens to contain it.

That last result is the one we would put in front of an information theorist.
It is not a statement about how many bits a source needs. It is a statement
about how many measurements it takes to learn the damage measure, and it says
the price is set by the dimension of the space rather than by the complexity of
the answer.

## The consequence for the slogan

A system trained to compress without a named reader is optimising for the
reader that weights every direction equally. That is a coherent thing to do and
it produces something broadly capable, which is why the slogan feels true. It
is also the most expensive reader to serve, because serving all directions is
what full dimension costs. The efficiency of a specialised system and the
generality of an unspecialised one are the same fact seen from two sides.

If intelligence is to be defined through compression at all, the definition has
to carry the index. Finding the coarsest representation that preserves what a
given reader needs is a definition that reduces correctly to the familiar one
when the reader is the undifferentiated one. It also inherits the familiar
one's limits, and it defines only relative intelligence, since the reader
enters from outside.

## What we do not claim

We do not claim a new information measure. We do not claim rate distortion
theory is incomplete. We do not claim that a system with no reading kernel is
impossible, only that we have measured what it costs. The counterexample is
sixteen heads across two layers of one model, and the reading operator's
recovery on that model is a conditional result that depends on how the
reference is weighted. Nothing here is a claim about biological intelligence.

The measurements cited are recorded with their preregistrations and their
failures in the project ledger, including the runs where our own bars were
wrongly set and the results were void.

## Sources

Shannon, C. E. Coding theorems for a discrete source with a fidelity criterion.
IRE National Convention Record, 1959.

Blackwell, D. Comparison of experiments. Proceedings of the Second Berkeley
Symposium on Mathematical Statistics and Probability, 1951, and Equivalent
comparisons of experiments, Annals of Mathematical Statistics, 1953.

Bernardo, J. M. Expected information as expected utility. Annals of Statistics,
1979, and Shuford, E. H., Albert, A., and Massengill, H. E. Admissible
probability measurement procedures. Psychometrika, 1966. These two are cited
for the result that the logarithmic score is the only local strictly proper
scoring rule. The attribution has not been checked against the originals and
should be before it is relied on.

Project records. GO-P-2026-021 for the matched arm counterexample, GO-P-2026-020
for the negative that preceded it, and the readscope calibration series for the
reference weighting spread and the dimension bound.
