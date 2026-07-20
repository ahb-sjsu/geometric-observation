# Chapter 10 — The Blind Probe: Recovering $P_C$ From Outputs Alone

Everything so far assumed you know the read metric. For a linear read-out you do; for a
trained classifier or a frontier attention head you do not have the Jacobian in closed
form, and the honest objection — "your theory needs an object I cannot compute" — has
to be answered or the framework is a curiosity. This chapter answers it. The read
metric is **identifiable from the consumer's behavior alone**: you can recover the read
subspace by finite-differencing the consumer's output, with no labels and no oracle
direction. The instrument that does it is the blind probe, and it is what makes the
theory operational rather than aspirational.

## The idea

The read metric is $P_C = J^\top G J$, and $J$ is a derivative. Derivatives are
measurable: perturb the input, watch the output move. Concretely, for a
scalar-margin consumer (a classifier logit, a ranking score) the blind probe estimates
the margin sensitivity

$$ S = \mathbb{E}\big[\, g\, g^\top \,\big], \qquad g = \nabla_x\, C(x), $$

recovered by finite differences of $C$ around each operating point — the consumer's own
output, nothing else. The top eigenvectors of $S$ span the read subspace. No labels
enter (we never ask what the *correct* class is), and no oracle direction enters (we
never tell the probe which way to look). It sees $C(\cdot)$ and reconstructs what
$C$ is sensitive to.

For the retrieval consumer the same idea takes the margin-gradient form $g = \hat a -
\cos(a,b)\,\hat b$ — the sensitivity of a cosine-ranking score to its query — and
$S = \mathbb{E}[g g^\top]$ recovers a read operator that (this is the crucial property)
*strips the source anisotropy* and keeps only the task-tied directions. That property
is why the probe succeeds where a naive estimate fails, and it is the whole content of
the legal-domain story below.

## What the probe can promise: GO-1

On planted read subspaces — where the truth is known and the probe is graded against
it — the blind probe is decisive. It recovers the read subspace at overlap **0.936 vs
0.059 chance (≈16×)**, seeing only $C(\cdot)$; its blind projected-variance statistic
predicts the flip **12/12 in both consumers**, with Spearman 1.00 against the true
subspace; and reconstruction cannot (0.40) [predicted — GO-P-2026-011, blinded,
prospective, PASS 5/5]. The scope is stated: a planted low-rank read subspace with a
tanh consumer; the real-model consumer is the hardening, and the rest of the chapter is
that hardening.

The probe also generalizes to a *Hessian* read operator. In gradient compression
against a curvature consumer, the blind projected variance $\operatorname{tr}(H
\Sigma_\delta)/\operatorname{tr}(H\Sigma_0)$ tracks the update distortion 12/12 at
identical reconstruction, while reconstruction is uninformative (Spearman $-0.20$)
[predicted — GO-P-2026-010, Gate B, PASS 5/5]. The read operator $P_C$ is not tied to
classification; it is whatever the consumer's second-order sensitivity is, and the
probe finds it.

## The decisive test: a real consumer, recovered blind

Planted subspaces are a laboratory. The question that matters is whether the probe
recovers a *real* consumer's read operator — one that is both misaligned with the
signal energy and *generalizing* to held-out data. The legal-retrieval sequence is the
program's cleanest answer, and it is worth telling in full because it is also a story
about how the discipline distinguishes a failure of the flip from a failure of the
instrument.

**035 (miss).** The first attempt estimated the read operator as the centered document
covariance — a stand-in fit on calibration data. On the held-out set the recon-trade and
anti-control passed, but the **flip failed**: reconstruction-optimal *beat*
read-preserving (O=0.773 > R=0.757) [refuted — NEG, the estimated subspace overfit and
did not transfer]. A weaker program would have concluded the flip does not hold on real
retrieval. The discipline's diagnosis was sharper: *this is a read-operator
identifiability failure, not a failure of the flip* — the covariance estimate captured
what the *signal* varies in, not what the *consumer* reads.

**036 (rehab, confirmed).** The single fix: replace the estimated covariance with the
GO-1 **blind probe** margin-sensitivity operator, kept low-rank ($r = 32$), with the
config chosen on an internal cal-A/cal-B split and **sealed before** touching the
held-out set. On the *same* held-out data the verdict flipped: R=0.779 > O=0.771, flip
200/200, recon O=0.220 ≪ R=0.584 (reconstruction-optimal reconstructs 2.6× better yet
is downstream-worse) [demonstrated — GO-P-2026-036, 4/4]. The blind probe recovered a
read operator that was *both* misaligned-with-energy and generalizing — the two
conditions the 035 negative proved necessary.

**039 (fresh split).** Because 036's held-out set had already delivered the 035 verdict
and its margin was thin ($\Delta = 0.008$), the frozen 036 recipe was re-run on a fully
virgin opinion-disjoint split, blind probe refit. All four bars passed with **double the
margin** (R=0.796 > O=0.780, $\Delta = 0.016$; R even edges the uncompressed baseline —
nuisance-stripping *denoises* the ranking), flip 200/200 [demonstrated —
GO-P-2026-039]. The held-out-reuse asterisk was removed.

This is the first demonstration that the GO-1 blind probe, previously only
[predicted] on planted subspaces, recovers a *real* consumer's read operator with the
two properties the theory needs. It is the chapter's central result.

## What the probe cannot promise

The probe is an instrument, and instruments have limits the ledger records at full
prominence.

**On a frontier attention head, blind recovery is real but was sub-bar (NEG-12).** On
Llama-3.2-3B post-RoPE keys, the blind Jacobian probe recovered the read operator at
median overlap 0.567 — real, ≈4.5× chance, with strong heads near 0.96 — but **missed
the sealed 0.60 bar**, and because the registered quantizer pair was not
reconstruction-matched, `proj_beats_recon` could not fire [refuted — NEG-12]. Two of
three sealed triggers missed, bounding the theory to synthetic consumers *on that
evidence*. The corrected rematch (recon-matched key codes) then passed cleanly —
blind $\operatorname{tr}(\hat P\Sigma_\delta)$ predicts the worse arm 16/16, probe
overlap 0.647 ≥ 0.60 [demonstrated — GO-P-2026-021] — but NEG-12 *stands as its own
negative*. The instrument works; the first sealed design for testing it on a real model
was flawed, and both facts are on the record.

**Blind direction transfers; blind point-magnitude does not (yet).** The most stringent
test — recover $P_C$ non-oracle on a fresh untouched domain and commit the winning
code *and* its magnitude before opening the test split — came back **partial** on 20
Newsgroups (041): the blind winning-*code* prediction passed (AUROC R=0.975 > O=0.910,
the framework chose the better code before any label), but the two-metric flip tied on
held-out and the point *magnitude* overshot its sealed band [refuted, as a full flip;
mechanism confirmed]. The blind downstream *direction* is recoverable prospectively;
the cross-domain magnitude *scale constant* is an open problem (Chapter 17). Across
rates the magnitude tracks (Pearson 0.995, both decreasing per the finite-rate
criterion); across *domains* the constant does not yet transfer. The book claims the
direction and flags the magnitude.

## Why blindness is the point

The probe's blindness is not a limitation to be apologized for; it is the property that
makes the theory deployable. If recovering $P_C$ required labels, an oracle, or the
consumer's source code, the framework would apply only where you already know
everything. Because it requires only the ability to *query the consumer and watch it
respond*, it applies to trained networks, third-party estimators, and physical
instruments alike. You do not need to be given the observer. You need to be able to
poke it. The next chapter turns the probe outward — from recovering an observer's read
metric to recovering the *manifold* a representation lives on.
