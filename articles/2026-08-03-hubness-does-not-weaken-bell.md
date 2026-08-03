# Hubness does not weaken Bell

### An audit of setting dependent sampling in retrieval geometry

Andrew H. Bond, San Jose State University. 3 August 2026.

## Abstract

Retrieval experiments in high dimensional spaces concentrate their nearest
neighbour counts on a small number of points. That concentration depends on the
query distribution and the metric and the neighbour count, not on the corpus
alone, which invites the thought that measurement settings in a Bell experiment
act as queries and that the resulting concentration might produce correlations
stronger than a local hidden variable model allows. We tested that thought and it
is false as stated. When the shared state is sampled independently of the
settings, each side responds only to its own setting, and every emitted trial is
counted, the measured Clauser Horne Shimony Holt value stays at two to five
decimal places across seventy two configurations spanning dimensions three
through one hundred and twenty eight, concentrated density cores, and heavily
skewed sampling weights. The correlation between that value and the standard
hubness statistic is negative and negligible. The same simulated data, rescored
by discarding trials in which one side failed to register an outcome, returns a
value of two point seven three. The excess is produced by the discarding and not
by the geometry. Three deliberately broken controls confirm the measurement can
see a violation when one is present, and the control that discards trials leaves
the marginal distributions of each side untouched, which is why that particular
error is easy to make and hard to notice. What survives is a way of speaking
about one of the assumptions behind Bell inequalities. What does not survive is a
mechanism.

## Why anyone would look here

Nearest neighbour concentration is usually described as a property of a data set.
Recent work on vector retrieval shows it is better described as a property of the
whole experiment, meaning the corpus distribution together with the query
distribution and the distance function and the number of neighbours retrieved.
Change the queries and the same corpus concentrates differently.

A Bell experiment has queries. Each side chooses a setting, and the pair of
settings selects which correlation is being measured. If the choice of settings
changed which shared states actually contributed to the recorded data, the four
correlations entering the inequality would be averages over four different
populations rather than one, and the standard argument for the bound would not
apply. That is a real possibility and it has been studied for decades under two
names, measurement dependence and unfair sampling. The question we asked is
whether high dimensional concentration supplies it.

## Setting independent sampling leaves the value at two exactly

The argument that answers this needs no simulation. For a shared state drawn
without reference to the settings, with each side producing an outcome bounded in
magnitude by one from its own setting and that state, the combination entering the
inequality is bounded by two for each individual state, so it is bounded by two
after averaging over any distribution of states whatever. The bound holds for a
state space of any dimension, with any density, with any amount of nearest
neighbour concentration, and it holds when a side sometimes fails to register an
outcome provided that failure is recorded as an outcome rather than removed.

We measured it anyway, because a null result carries no information unless the
instrument that produced it is known to work. Across seventy two configurations
the largest measured value was 2.00000 against a finite sample tolerance of
0.0089. Dimension ranged from three to one hundred and twenty eight. Density
ranged from uniform on the sphere to two percent of the mass in a tight core.
Sampling weights ranged from uniform to a Zipf law. The correlation between the
measured value and the skewness of the neighbour count was minus 0.036.

The largest deviation of each side's marginal outcome from independence of the
other side's setting was 0.00464, which is finite sample noise. That number is a
check on the code rather than a finding, because locality was imposed by
construction and not tested.

## Discarding trials produces the violation, and the geometry is not involved

Taking the same simulated trials and computing the correlations only over pairs
in which both sides registered an outcome raises the measured value from 2.00000
to 2.7308. Nothing about the state space changed. No parameter changed. The
entire excess comes from which trials were counted.

An earlier unregistered probe made this quantitative in a different way. Across
one hundred and sixty eight configurations with retention that depended on the
local setting, one hundred and twenty nine exceeded the bound, and every one of
those did so with fewer than forty percent of trial pairs registering both
outcomes. Not one configuration reached the two thirds registration rate that a
sampling argument requires. At the configuration with the largest excess, counting
every trial dropped the value from 2.617 to 0.019.

That probe also failed to support the original thought in a second way. The excess
correlated with the neighbour count skewness at plus 0.258, with an exact measure
of how much the effective state distribution moved between settings at minus
0.027, and with the mutual information between the state and the setting pair at
minus 0.302. The last of these has the wrong sign for the idea being tested.
More statistical dependence between state and setting went with less excess, not
more.

## The broken controls show the measurement works

A null needs a positive control or it cannot be distinguished from a dead
instrument. We broke exactly one assumption at a time and required each to exceed
the bound.

Discarding unregistered trials gave 2.748 while leaving the largest marginal
deviation at 0.0022. Making the state distribution depend on the setting pair gave
2.386 with a marginal deviation of 0.272. Letting one side read the other side's
setting gave 3.174 with a marginal deviation of 1.025.

The first of those three is the reason this class of error persists. It breaks the
bound while leaving each side's own statistics exactly as they would be under a
local model, so an experimenter examining only the marginals sees nothing wrong.
The third announces itself immediately in the marginals. Any future proposal that
exceeds the bound in a model of this kind should be required to say which of these
three columns it occupies.

The second control is not a faithful model of setting dependence, because it also
disturbs the marginals. Constructions exist that make the state distribution
depend on the settings while preserving the marginals exactly, and ours is not one
of them. It serves only to show that the measurement responds.

## The full angular dependence fails, not only four settings

Reporting a single value computed at four chosen settings makes it easy to fit
four numbers and claim a match. We swept the angle between the two sides over half
a turn. A local model built from signs of inner products on a sphere produces a
correlation that falls linearly with angle, scaled down by the fraction of trials
that register. The measured curve matched that linear form with a root mean square
error between 0.20 and 0.45, and departed from the cosine form of quantum theory
with a root mean square error between 0.61 and 0.72. The largest single departure
reached between 0.98 and 1.21. The failure is across the whole angular dependence
and not confined to the settings that make the four term combination large.

## A coarse measure of the thing being tested produced a false null

The first attempt estimated how much the effective state distribution moved
between settings by projecting onto one random direction and building a histogram.
In one hundred and twenty eight dimensions that estimate reached 0.740 where the
exact value reached 0.883, and it let a loose inequality relating the excess to
that movement fail in three of one hundred and sixty eight cases. Computing the
movement in closed form from the retention weights removed both problems and the
inequality then held in all one hundred and sixty eight. A poorly conditioned
estimate of the quantity under test manufactured a null before the physics was
reached, and the correlations reported above use the exact computation.

One correction belongs next to the main result. As executed, the registered
audit reported five of its six tests passing, because the test for the positive
controls read a value computed over all trials for the control whose defining
feature is that trials are discarded. That was an error in the scoring and not in
the simulation. Reading the appropriate value for that control and rerunning at
the same seed reproduced the simulated data bit for bit and changed only the
verdict. The originally executed record is retained alongside the corrected one.

## What survives is a vocabulary and not a mechanism

Measurement settings can be treated as queries, and the accessibility of a state
under a given query is a natural way to talk about the assumption that the shared
state is distributed independently of the settings. That is a clear way to name an
assumption that is otherwise hard to state without technical language, and it
connects the assumption to a measurable property of retrieval experiments.

The mechanism is absent. Concentration of nearest neighbour counts does not move
the bound, and the only route past the bound in this family of models is to stop
counting trials in which a side failed to register, which is a known and closed
error rather than a new account of the correlations. Reaching a value below the
quantum maximum in these runs is not evidence of any bound, because two random
realisations of the same sweep reached 2.82 and 2.62, so the ceiling observed
depends on the realisation and not on structure.

Three requirements remain for any model of this kind to be a physical account
rather than a restatement. It must produce the cosine dependence on angle across
all angles. It must leave the marginals independent of the distant setting by
construction rather than by measurement. It must produce the specific quantum
maximum rather than merely exceeding the classical one.

## Using the harness

The measurement is available as a preregistered and sealed script with its
predictions and tolerances fixed before it ran. It takes a state space, a
sampling law, a response rule and a registration rule, and it reports the four
term combination computed over every emitted trial, the marginal deviations, the
angular dependence, and the same combination computed over discarded data for
comparison. A conjecture routed through it must declare which assumption it
relaxes, and the three broken controls give the three available answers.

The scope is the family of models specified in advance. Retention that depends on
the local setting through a smooth function of alignment with the query is one
choice among many, and constructions are known that reach the algebraic maximum
of four by discarding data adversarially. Nothing here bounds those.

## Records

The sealed registration is GO-P-2026-057 in the geometric observation repository,
with the run record in results and the full account in the experiment notes. The
earlier unregistered probe is retained with its own record and is marked as
exploratory, which under the governing protocol means it cannot support a claim.
The negative result is carried as NEG-15 in the claim ledger.
