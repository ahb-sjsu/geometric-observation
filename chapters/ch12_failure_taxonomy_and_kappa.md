# Chapter 12 — The Failure Taxonomy and the $\kappa$ Alignment Law

The flip is a property of observation — *wherever the read operator can be identified,
is misaligned with the signal energy, and (on learned representations) generalizes.*
That sentence has three conditions, and each names a way the flip can be absent. This
chapter makes the list complete and then makes it quantitative: the four degeneracies
of $P_C$ are the exhaustive taxonomy of failure, and the alignment law $\kappa$ turns
the decisive condition from a bucket into a dial you can read before you compress. This
is where "know your consumer" stops being folklore.

## The four degeneracies of $P_C$

Every honest negative in the program's flip experiments sorts into exactly one of four
kinds, and the four are the four ways the read metric can fail to do its job. They are
derived, not catalogued: they are the degeneracies of the object $P_C$ itself.

**1. Identifiability — the read operator is mis-*estimated*.** $P_C$ exists and is
misaligned with the signal, but your *estimate* $\hat P_C$ is wrong, typically because
you used what the *signal* varies in (a covariance) as a stand-in for what the
*consumer* reads. This is the **fixable** failure. Legal-035 is the reference instance:
a document-covariance read operator overfit and reconstruction-optimal won on held-out;
replacing it with the GO-1 blind probe (036/039) flipped the verdict on the identical
data [refuted → demonstrated]. *The 035 miss was an identifiability failure, not a
failure of the flip* — and the blind probe is its fix.

**2. Coupling — the read operator is *intrinsically* aligned with the signal energy.**
$P_C$ is estimated correctly and is *still* aligned with the source, because in this
domain the directions the consumer reads *are* the directions the signal has energy in.
Then reconstruction-optimal coding already protects the read directions, and the flip
cannot appear no matter how well you recover $P_C$. This is a **true boundary**, not a
bug. D4 (real-model gradient compression) is the reference: the Hessian's high-curvature
directions and the high-gradient-energy directions both come from $X^\top X$, so they
coincide; the anti-probe stays robust (300/300 — the read operator *does* govern the
task) but the subtle flip is 27% [refuted, as a flip; not rehabilitatable by any
read-operator recovery].

**3. Precondition — there is no working consumer.** $P_C \approx 0$ on the relevant
directions because the consumer does not actually read the task. Moral judgment on
*frozen* embeddings sits at chance (LaBSE 0.60 vs 0.63 majority): there is no moral read
direction to protect until the consumer is fine-tuned, at which point (bert-base → 0.74)
the flip appears [refuted-as-stated; needs a competent consumer, not a read-operator
fix].

**4. Mechanism-absent — the claimed effect does not exist.** The direction you hoped to
exploit is not in $\ker P_C$ at all. GO-5/NEG-11 is the reference: the $\alpha = 1$
density restoration is $<2\%$ and not density-specific, so the density-nuisance-removal
mechanism is simply absent outside diffusion [refuted]. This is a genuine refutation, not
a rehabilitatable miss.

The taxonomy is useful because it is *actionable*: identifiability failures are fixed by
a better probe, precondition failures by a better consumer, and coupling and
mechanism-absent failures are *stated as boundaries* — the flip does not apply there, and
the honest thing is to say so. Three of the four are diagnosable *before* you run the
flip experiment, which is the subject of the rest of the chapter.

## From bucket to dial: the $\kappa$ alignment law

The decisive condition — misalignment between what the consumer reads and where the
signal has energy — is naturally continuous, and the program made it so. Define the
normalized read–energy alignment

$$ \kappa = \operatorname{tr}\!\big(\bar P_C\, \bar\Sigma_x\big), $$

the (normalized) overlap of the average read metric with the source covariance on the
read subspace. $\kappa$ is small when the consumer reads directions the signal is quiet
in (strong misalignment — the flip regime) and approaches 1 when the read subspace *is*
the high-energy subspace (the coupling regime — no flip). The **alignment law** is the
claim that **flip magnitude decreases in $\kappa$**, with $\kappa \to 1$ the coupling
null.

This converts boundary condition #2 from a discrete bucket ("coupled or not") into a
continuous, *ex-ante* dial: measure $\kappa$ before compressing and you have a
prediction of whether — and how strongly — the flip will appear, without running the
downstream task. The law is tested two ways. **Retrospectively**, across the twelve
measured domains, flip magnitude is decreasing in $\kappa$, with D4 sitting at the
$\kappa \to 1$ null exactly as predicted [exploratory → the retrospective fit is labeled
retrospective and does not license the umbrella claim]. **Prospectively**, one sealed
prediction at an intermediate $\kappa$ is the confirmatory test [predicted]. The
retrospective/prospective distinction is enforced, not cosmetic: the retrospective fit is
an [exploratory] row and PROTOCOL Rule 1.1 forbids the umbrella text from leaning on it;
only the sealed prospective point can promote the law.

## Two axes, not one

The alignment law is necessary but not sufficient to pick the *code*, because the flip's
regime is governed by **two** independent axes, not one — and this is why no single
statistic and no single encoder suffices. The axes are **concentration** (how
anisotropic the source is, roughly $\operatorname{unit\_disp}$) and **correlation** (how
cross-channel-correlated it is). The regime map:

| | isotropic (unit_disp ≈ √2) | concentrated (unit_disp small) |
|---|---|---|
| **low correlation** | moral, music → generic **polar** | *(rare)* |
| **cross-channel correlated** | whale → **whitened** | KV-keys → **whitened** |
| **channel-structured** | — | legal → **per-channel / blind-probe** |

Whale codas are the clean proof the map needs two axes: they are isotropic like moral,
yet require whitening like KV-keys, *because their inter-click intervals are correlated.*
Concentration alone cannot tell moral from whale; the correlation axis — which the
probe's `probe_quotient` measures directly — is decisive. A tempting one-number shortcut
(`median_unit_displacement` as a regime predictor) was sealed and **refuted on its first
prospective test** (NEG-14): a synthetic per-dimension-offset source had unit_disp 0.649
(rule says "needs blind-probe") yet generic polar won at 1 bit. The reconciliation to the
two-axis probe *stands*; only the single-number shortcut is refuted. The reliable
diagnostic is `probe_quotient`, per domain, at low bits [refuted, for the shortcut;
demonstrated, for the two-axis diagnostic].

## Why this is the last instrument

The three instruments of Part IV compose into a workflow. The blind probe (Chapter 10)
recovers $P_C$; the recognizer (Chapter 11) recovers the manifold the representation
lives on; and the taxonomy-plus-$\kappa$ of this chapter says *whether the flip applies*
and *which code to use* — all before a single downstream evaluation. This is what turns
Observation Theory from a diagnosis into a procedure: measure $\kappa$ and the two axes,
place the domain on the map, read off the code family, and — if $\kappa$ is near 1 or the
consumer is at chance — know in advance that the flip will not save you and reconstruction
is (locally) fine. The failure taxonomy is not a list of disappointments. It is the part
of the theory that tells you where the theory does not apply, which is the part that makes
the rest of it trustworthy. Part V puts the whole apparatus on trial: the twelve-domain
sweep and the falsifiable core.
