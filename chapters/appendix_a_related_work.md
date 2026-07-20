# Appendix A — Related Work and Differentiation

This appendix collects, in one place, what the framework owes to which literature and
where it differs. The governing honesty is Chapter 3's: almost none of the *components*
are new, and the contribution is the *synthesis and its falsification*. The four-column
posture below — literature, what it owns, what this program adds, the differentiating
sentence — is meant to let a referee find the seam fast.

## Information geometry (Amari, Čencov)

*Owns.* The pullback metric $P_C = J^\top G J$; the Fisher information metric as the
canonical output metric $G$ for likelihood consumers; Čencov's uniqueness theorem;
natural-gradient geometry.

*This program adds.* The claim that this pullback is the operative object for *lossy
representation across domains* — the thing that decides whether a quantizer, embedding,
or array codec is good — and that it is recoverable *blind* from a consumer's outputs.

*Differentiation.* Information geometry studies the pullback to understand estimation
and inference *on* statistical manifolds; this program uses it to decide *how to
compress inputs to* a consumer. Same operator, different load. The Skeptic's Appendix
answers "isn't $P_C$ just Fisher information?" directly (Appendix E): yes, when the
consumer is a likelihood — and the point is the job, not the algebra.

## Rate–distortion theory (Shannon, Berger; Kostina–Verdú; Kostina–Tuncel; Rimoldi)

*Owns.* $R(D)$, reverse water-filling, dispersion (finite-blocklength), successive
refinement, the multi-stage/$k$-observer rate regions.

*This program adds.* The consumer-relative $R_C(D)$ with its tilt toward the read
subspace; the two-observer region whose refinability is exactly Loewner-nesting of read
metrics; the mismatch **tax** $(r/2)\log(M/m)$ and the omission **floor**
$\operatorname{tr}(\tilde P\Pi)$ for using the wrong read metric.

*Differentiation.* Classical rate–distortion fixes the fidelity measure (usually squared
error) and is recovered here as the $P_C = I$ slice; this program promotes the fidelity
measure to the observer-dependent variable it always was. Citations are exact:
the $k \ge 3$ region is Kostina–Tuncel (not an iteration of the two-stage map — VI-5);
dispersion constants are flagged [C7] to Kostina–Verdú, not re-derived (VI-7).

## Perceptual / weighted-distortion coding

*Owns.* The practice of replacing $I$ with a perceptual weighting because the human
sensory consumer does not read uniformly.

*This program adds.* A principled account of *where the weighting comes from* (the
consumer's Jacobian pullback), for *any* consumer, recoverable when the consumer is a
trained black box.

*Differentiation.* Perceptual coding hand-tunes one tilt for one consumer (the eye/ear);
the read metric says every consumer has such a tilt and you can get it from the consumer
rather than guessing it.

## Spectral embedding & clustering (von Luxburg–Radl–Hein; Ng–Jordan–Weiss; Coifman–Lafon)

*Owns.* The commute/resistance embedding and its large-graph degeneracy; row-
normalization; diffusion maps and the $\alpha$ family of density normalizations.

*This program adds.* The polar decomposition that confines the collapse to the radius and
keeps geodesics in the angle [proved]; the identification of row-normalization as the
read-subspace projection of the geodesic-rank consumer; the exact $S^1$ rank-collapse and
flat-torus bounds; the spectral-filter phase diagram (critical dimension $d = 4$) and the
Green-kernel rank-limit theorem.

*Differentiation.* Diffusion maps' $\alpha = 1$ is *retained as the optimal diffusion
exponent* but its density-quotient is **refuted outside diffusion** (NEG-11) — a sharp
statement of exactly how far the density normalization generalizes.

## Task-aware / downstream-aware compression (learned compression, bit-allocation for a task)

*Owns.* The engineering intuition that compression should serve the downstream task, and
various end-to-end trained codecs that do so implicitly.

*This program adds.* An explicit, *identifiable* task operator $P_C$; a theory of when
task-awareness *matters* (the $\kappa$ law and the four degeneracies); and a falsifiable
prediction — the flip — sealed across domains rather than assumed.

*Differentiation.* Task-aware compression usually *trains* a code against a task
end-to-end; this program *identifies the read operator* (blind, no labels) and derives
what to keep, giving a transparent recipe with stated boundaries rather than an opaque
learned one. The Skeptic's Appendix answers "isn't this just task-aware compression?"
(Appendix E).

## Decoder-robustness / invariance methodology (the series' own lineage)

*Owns.* The Bond Index (Geometric Ethics) and its bioacoustic descendant the Decoder
Robustness Index (DRI): scoring a system by its distortion under read-relevant versus
invariant transforms.

*This program adds.* The recognition that these are the *same* read-operator-distortion
methodology — invariant transforms are $\ker P_C$, stress transforms are the read
direction — instantiated in different domains.

*Differentiation.* This is not a competitor but a unification: the DRI for whale decoders
and $\operatorname{tr}(P_C\Sigma_\delta)$ for quantizers are one methodology seen in two
domains, which is itself evidence for the framework's generality.
