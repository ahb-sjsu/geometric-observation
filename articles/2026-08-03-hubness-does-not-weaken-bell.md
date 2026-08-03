# Hubness does not weaken Bell

### A preregistered audit of query dependent sampling in latent geometry

Andrew H. Bond, San Jose State University. 3 August 2026. Revised after review.

## Abstract

Retrieval experiments in high dimensional spaces concentrate their nearest
neighbour counts on a small number of points, and that concentration depends on
the query distribution and the distance function and the neighbour count rather
than on the corpus alone. Measurement settings in a Bell experiment can be read as
queries, which invites the thought that query dependent concentration might
produce correlations stronger than a local hidden variable model allows. We tested
that thought and it is false as stated. When the shared state is sampled
independently of the settings, each side responds only to its own setting, and
every emitted trial is counted, the measured four term correlation combination
never exceeds two, and for the setting geometry registered in advance it equals two
to five decimal places across seventy two configurations spanning dimensions three
through one hundred and twenty eight, concentrated density cores, and heavily
skewed sampling weights. We show that equality is forced pointwise by the chosen
settings rather than achieved on average, which makes the audit maximally
sensitive to any departure. The correlation between the measured combination and
the standard concentration statistic is negative and negligible. The same
simulated trials, rescored by keeping only pairs in which both sides registered an
outcome, give two point seven three. Three deliberately broken controls confirm
the instrument detects a violation when one is present, and the control that
discards unregistered trials leaves each side's own statistics untouched, which is
why that error survives the checks an experimenter is most likely to run. What
survives is a way of speaking about one of the assumptions behind Bell
inequalities. What does not survive is a mechanism.

## Why anyone would look here

Nearest neighbour concentration is usually described as a property of a data set.
Work on vector retrieval shows it is better described as a property of the whole
experiment, meaning the corpus distribution together with the query distribution
and the distance function and the number of neighbours retrieved. Change the
queries and the same corpus concentrates differently.

A Bell experiment has queries. Each side chooses a setting, and the pair of
settings selects which correlation is measured. If the choice of settings changed
which shared states actually contributed to the recorded data, the four
correlations entering the inequality would be averages over four different
populations rather than one, and the standard argument for the bound would not
apply. That possibility has been studied for decades under two names, measurement
dependence and unfair sampling. The question we asked is whether high dimensional
concentration supplies it, and the answer is that it does not.

## Status of the evidence

The formal claim rests only on the sealed audit. The remaining rows are retained
because they were run, and they are marked so no number is mistaken for a
claim bearing one.

| Evidence | Status | Role |
|---|---|---|
| Seventy two configuration audit, seed 20260817 | Sealed and preregistered before running | Carries the null and the broken controls |
| One hundred and sixty eight configuration sweep, seed 20260816 | Exploratory, no registration | Diagnosed the mechanism and sized the sample floors |
| A second random realisation of that sweep | Exploratory | Shows the observed ceiling is not structural |
| Corrected audit verdict | Sealed rerun, identical simulated data | Scoring correction described in its own section |

## The two statistics that differ

Let the shared state be a point in a high dimensional space drawn from a fixed
distribution. Each side produces an outcome and a registration indicator. Write
the outcome functions and the registration functions as

$$A_x(\lambda)\in\{-1,+1\},\qquad B_y(\lambda)\in\{-1,+1\},$$
$$D_A(x,\lambda)\in\{0,1\},\qquad D_B(y,\lambda)\in\{0,1\}.$$

Every trial is emitted, and a side that fails to register contributes the value
zero rather than being removed, so the recorded outcomes are $A_xD_A$ and
$B_yD_B$, both bounded in magnitude by one. The all trials correlation and the
four term combination are

$$E_{xy}=\mathbb E_{\rho}\!\left[A_x D_A\,B_y D_B\right],\qquad
S=\left|E_{00}+E_{01}+E_{10}-E_{11}\right|.$$

Discarding unregistered trials replaces this with a conditional average,

$$E^{\mathrm{coinc}}_{xy}
=\mathbb E\!\left[A_xB_y \,\middle|\, D_A=D_B=1,\,x,\,y\right],$$

which is an average with respect to a different distribution for each pair of
settings,

$$\rho^{\mathrm{coinc}}_{xy}(\lambda)\;\propto\;
\rho(\lambda)\,\eta_A(x,\lambda)\,\eta_B(y,\lambda),$$

where the two registration probabilities are the expectations of $D_A$ and $D_B$
at fixed state and local setting. The four terms of the combination are then no
longer averages over one population, and the argument for the bound does not
apply to them. This is the entire content of the paper in two lines, and it is
also where query dependent accessibility enters, since the two factors
$\eta_A$ and $\eta_B$ are exactly a statement about which states are accessible
under which query.

## The combination is forced to two pointwise, not on average

Bell's argument gives an inequality rather than an equality, and many local models
sit strictly inside the bound, so the exact value we measure needs its own
explanation. For our registered settings it has one.

Both sides respond by the sign of an inner product with a direction, and all four
directions lie in a common plane, so each response depends only on the angle of the
state's projection into that plane. Writing that angle as $\varphi$, with the two
directions on one side at $0$ and $\pi/2$ and the two on the other side at
$\pm\pi/4$, the combination

$$K(\varphi)=A_0(B_0+B_1)+A_1(B_0-B_1)$$

takes the value $-2$ in every one of the eight sectors of width $\pi/4$. We
verified this directly. Across two million sampled angles the set of values taken
by $K$ has exactly one element, and in ambient dimensions three, eight and one
hundred and twenty eight, and for a strongly anisotropic distribution with most of
its mass in a tight core, the same holds and the combination equals two to ten
decimal places.

So the registered construction is extremal pointwise. The measured value is not an
average that happens to land on the bound, it is the mean of a constant, which is
why it carries no statistical scatter. Two consequences follow. The measurement of
the null is a check that the code implements the intended construction rather than
a discovery. And the audit is maximally sensitive, because a model that departed
from local realistic behaviour anywhere would move the combination away from a
noiseless baseline rather than out of a noisy one.

## Geometry does not move the value

Across seventy two configurations the largest measured combination was 2.00000
against a finite sample tolerance of 0.0089. Dimension ranged from three to one
hundred and twenty eight. Density ranged from uniform on the sphere to two percent
of the mass in a tight core. Sampling weights ranged from uniform to a Zipf law.
The correlation between the measured combination and the skewness of the neighbour
count was minus 0.036.

The largest deviation of either side's marginal outcome from independence of the
distant setting was 0.00464, which is finite sample noise. That number checks the
code rather than testing a hypothesis, because locality was imposed by construction.

## Conditioning on coincident registration produces the excess

Taking the same simulated trials and computing the correlations only over pairs in
which both sides registered raises the measured combination from 2.00000 to
2.7308. No parameter and no property of the state space changed between the two
numbers. For this paired rescoring the entire excess is attributable to
conditioning on coincident registration.

The exploratory sweep made the same point across a wider family. Of one hundred and
sixty eight configurations with registration that depended on the local setting,
one hundred and twenty nine exceeded the bound, and every one of those had a
coincidence efficiency below 0.40. That is well below the efficiency any standard
two setting analysis requires. For the symmetric case with maximally entangled
states the critical value is $2(\sqrt2-1)$, close to 0.83, and the often quoted two
thirds belongs to a different construction using nonmaximally entangled states in
the Clauser and Horne form rather than being a general threshold. Our conclusion
does not depend on which of these is chosen, because no configuration in the sweep
came near either. At the configuration with the largest excess, counting every
trial dropped the combination from 2.617 to 0.019.

That sweep also failed to support the original thought in a second way. The excess
correlated with the neighbour count skewness at plus 0.258, with an exact measure
of how far the effective state distribution moved between settings at minus 0.027,
and with the mutual information between the state and the setting pair at minus
0.302. The last has the wrong sign for the idea under test, since more statistical
dependence between state and setting went with less excess rather than more.

## The broken controls show the instrument responds

A null cannot be distinguished from a dead instrument without a positive control.
We broke one assumption at a time and required each to exceed the bound.

Discarding unregistered trials gave 2.748 while leaving the largest marginal
deviation at 0.0022. Making the state distribution depend on the setting pair gave
2.386 with a marginal deviation of 0.272. Letting one side read the distant setting
gave 3.174 with a marginal deviation of 1.025.

The first of the three is why this error persists in practice. It breaks the bound
while leaving each side's own statistics as a local model would predict, so an
experimenter who checks only the marginals sees nothing wrong. The third announces
itself in the marginals immediately. Any proposal that exceeds the bound in a model
of this kind should be required to say which of the three it occupies.

The second control is not a faithful model of setting dependence, because it also
disturbs the marginals. Constructions exist that make the state distribution depend
on the settings while preserving the marginals exactly, and ours is not one of them,
so it serves only to show that the measurement responds.

## The full angular dependence fails, not only four settings

Reporting one value computed at four chosen settings makes it easy to match four
numbers and claim agreement. We swept the angle between the two sides over half a
turn. A local model built from signs of inner products produces a correlation that
falls linearly with angle, scaled by the fraction of trials that register. The
measured curve matched that linear form with a root mean square error between 0.20
and 0.45, and departed from the cosine form of quantum theory with a root mean
square error between 0.61 and 0.72, the largest single departure reaching between
0.98 and 1.21. The failure covers the whole angular dependence rather than only the
settings that make the four term combination large.

## A coarse estimate of the quantity under test produced a false null

The first attempt estimated how far the effective state distribution moved between
settings by projecting onto one random direction and building a histogram. In one
hundred and twenty eight dimensions that estimate reached 0.740 where the exact
value reached 0.883, and it allowed a loose inequality relating the excess to that
movement to fail in three of one hundred and sixty eight cases. Computing the
movement in closed form from the registration probabilities removed both problems,
after which the inequality held in all one hundred and sixty eight cases. A poorly
conditioned estimate of the quantity under test manufactured a null before the
physics was reached, and every correlation reported above uses the exact
computation.

## Audit correction

As executed, the sealed audit reported five of its six tests passing. The test
covering the positive controls read the all trials combination for every control,
including the one whose defining feature is that trials are discarded, for which
that quantity cannot show a violation by construction. The error was in the scoring
and not in the simulation. Reading the appropriate quantity for that control and
rerunning at the same seed reproduced the simulated data bit for bit and changed
only the verdict. The originally executed record is retained beside the corrected
one, and the substantive requirement behind the failed test was already met
independently by the paired rescoring reported above.

## What survives is a vocabulary and not a mechanism

Measurement settings can be treated as queries, and the accessibility of a state
under a given query is a natural way to talk about the assumption that the shared
state is distributed independently of the settings. The two registration factors in
the conditional distribution above are that statement written down. This gives a
compact way to name an assumption that is otherwise hard to state without technical
language, and it connects the assumption to a measurable property of retrieval
experiments.

The mechanism is absent. Concentration of nearest neighbour counts does not move
the bound. Within the local and setting independent model under test, the observed
route past the bound was conditioning on coincident registration, which is a known
and closed error rather than a new account of the correlations. Our controls show
that setting dependent state distributions and explicit access to the distant
setting also exceed the bound, so postselection is not the only possible route in
general, only the one this family took. Reaching a value below the quantum maximum
in these runs is not evidence of any bound, because two random realisations of the
same exploratory family reached 2.82 and 2.62, so the observed ceiling depends on
the realisation rather than on structure.

Three requirements remain for a model of this kind to be a physical account rather
than a restatement. It must reproduce the cosine dependence at all angles. It must
leave each side's statistics independent of the distant setting by construction
rather than by measurement. It must reproduce the specific quantum maximum rather
than merely exceeding the classical one.

## Relation to existing work

The inequality and its four term form are due to Bell and to Clauser, Horne,
Shimony and Holt. That the bound is equivalent to the existence of one joint
distribution over all four settings is due to Fine, and the general obstruction to
assembling context specific distributions into a global one is developed by
Abramsky and Brandenburger. The quantum maximum is due to Tsirelson.

Local models that reproduce singlet correlations by rejecting data go back to
Pearle and were developed by Gisin and Gisin. Efficiency requirements for two
setting tests are given by Garg and Mermin, and the lower requirement available
with nonmaximally entangled states is due to Eberhard. Larsson reviews the
loopholes collectively. Experiments closing the detection and locality loopholes
together are reported by Hensen and colleagues. Local deterministic models that
relax measurement independence are constructed by Hall, and Wood and Spekkens show
that causal explanations of Bell correlations require fine tuning to preserve the
observed independences. The concentration statistic we use is that of Radovanovic,
Nanopoulos and Ivanovic.

The contribution here is none of those results. It is the combination of a
retrieval geometric statement of the assumption, a null proved analytically and
then measured across concentration settings, a paired comparison of all trials
against coincidence only scoring on identical data, evaluation over the full
angular dependence, controls that break distinct assumptions, and a registration
and audit record that keeps the failed conjecture and the scoring error visible.

## Records

The sealed registration is GO-P-2026-057 in the geometric observation repository,
with the run record in the results directory and the full account in the experiment
notes. The earlier unregistered probe is retained with its own record and marked
exploratory, which under the governing protocol means it cannot support a claim.
The negative result is carried as NEG-15 in the claim ledger. The bibliographic
details of the works cited above should be checked against the published records
before submission.
