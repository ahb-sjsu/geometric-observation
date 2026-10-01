# Appendix A — Related Work and Differentiation

This appendix collects, in one place, what the program owes to which literature and
where it differs. Most of the components are classical. The contribution is the
synthesis, the theorems the synthesis produces, and their falsification. The first
section states each classical parent plainly. The sections after it keep the
four-part posture (literature, what it owns, what this program adds, the
differentiating sentence) so that a referee can find the seam fast. Full references
are at the end.

## Classical parents at a glance

Each line names an object of this book, its classical name, and what this program
adds in one sentence.

- **Read metric $P_C = J^\top G J$ (averaged, $\bar P_C$).** Classical names are the
  active-subspace matrix (Constantine, Dow and Wang 2014; Constantine 2015), the
  expected gradient outer product or outer product of gradients (Hristache et al.
  2001; Xia et al. 2002), and the pullback metric of information geometry (Rao 1945;
  Amari and Nagaoka 2000). *Adds.* The program uses this matrix to decide what a lossy
  code should keep, and tests that use across domains.
- **Read distortion $\operatorname{tr}(P_C\Sigma_\delta)$.** Classically a weighted, or
  sensitivity-weighted, mean squared error (Sakrison 1968), as in Hessian-aware
  quantization (Choi et al. 2017; Dong et al. 2019). *Adds.* The weight is derived
  from the consumer and can be measured blind.
- **Consumer rate–distortion function $R_C(D)$.** Classically the weighted-MSE
  rate–distortion function (Sakrison 1968) with reverse water-filling (Kolmogorov
  1956; Berger 1971). For a nonlinear consumer it is an indirect, or remote, source
  coding problem (Dobrushin and Tsybakov 1962; Wolf and Ziv 1970; Witsenhausen 1980).
  *Adds.* The mismatch tax, the omission floor, and their measurement on trained
  models.
- **The flip.** Classically a ranking reversal between reconstruction error and task
  loss. It is the premise of task-based quantization (Shlezinger, Eldar and Rodrigues
  2019). *Adds.* The reversal is sealed in advance and tested across twelve domains,
  with its absences diagnosed.
- **Blind probe.** Classically finite-difference active-subspace estimation
  (Constantine 2015). *Adds.* The probe is run on a consumer's margin with no labels
  and graded against sealed bars.
- **Quotient $X/\!\sim_C$.** The quotient by the kernel of the gradient outer-product
  matrix. *Adds.* The quotient is read as the world the observer acts on, which is
  the LEGIBILITY result.
- **Conditional content, conditional work.** For a description $M$ and a party
  holding $S^n$, the program's $H(M\mid S^n)/n$ is, under a deterministic encoder, the
  conditional leakage $I(X^n;M\mid S^n)/n$ of secure source coding. Equivalently it is
  $H(X^n\mid S^n)/n$ minus the equivocation. The discrete region is the
  rate–distortion–equivocation region of Villard and Piantanida (2013, Theorem 3). The
  vector Gaussian case is Ekrem and Ulukus (2013). *Adds.* The operational reading is
  the re-encoding cost at the holder, and the Gaussian results for an informed encoder
  without decoder side information.
- **Conditional Landauer work.** Erasure work with side information is del Rio,
  Åberg, Renner, Dahlsten and Vedral (2011). *Adds.* The rate–work–distortion region
  that tracks description rate and reset work as separate resources.
- **Budget cliff.** The identifiability limit of confined probes. Lower bounds for
  adaptive sensing and matrix-vector queries make it quantitative (Arias-Castro,
  Candès and Davenport 2013; Simchowitz, El Alaoui and Recht 2018; Rashtchian,
  Woodruff and Zhu 2020), as does the dimension dependence of zeroth-order
  optimization (Duchi et al. 2015). *Adds.* The limit is stated for read operators and
  checked against the program's own probe budgets.
- **Two-observer refinability.** Gaussian successive refinement (Equitz and Cover
  1991) under individual distortion criteria (Nayak, Tuncel, Gündüz and Erkip 2010;
  Op 't Veld and Gastpar 2017). The general achievable region is Rimoldi (1994).
  *Adds.* The exact condition $\Sigma^\star(P_2,D_2) \preceq \Sigma^\star(P_1,D_1)$ and
  the exact excess rate as a pair of max-det programs.
- **Alignment law $\kappa$.** A matrix cosine, the normalized inner product of kernel
  alignment (Cristianini et al. 2002). *Adds.* $\kappa$ is used as a dial that predicts
  when the flip appears.
- **Observer triple $(C, G, B)$.** A task map, an output metric, and a rank or rate
  constraint. *Adds.* The triple is the unit every verdict in the book is relative to.

## Information geometry (Amari, Čencov)

*Owns.* The pullback metric $P_C = J^\top G J$; the Fisher information metric as the
canonical output metric $G$ for likelihood consumers; Čencov's uniqueness theorem;
natural-gradient geometry. The Fisher metric itself goes back to Rao (1945).

*This program adds.* The claim that this pullback is the operative object for *lossy
representation across domains* — the thing that decides whether a quantizer, embedding,
or array codec is good — and that it is recoverable *blind* from a consumer's outputs.

*Differentiation.* Information geometry studies the pullback to understand estimation
and inference *on* statistical manifolds; this program uses it to decide *how to
compress inputs to* a consumer. Same operator, different load. The Skeptic's Appendix
answers "isn't $P_C$ just Fisher information?" directly (Appendix E): yes, when the
consumer is a likelihood — and the point is the job, not the algebra.

## Active subspaces and gradient outer products (Constantine; Xia et al.; Hristache et al.)

*Owns.* The averaged matrix $\mathbb E[\nabla f\,\nabla f^\top]$ and its estimation
from gradients or finite differences. In uncertainty quantification it is the
active-subspace matrix (Constantine, Dow and Wang 2014; Constantine 2015). In
dimension reduction it is the outer product of gradients, whose range estimates the
central subspace (Hristache et al. 2001; Xia et al. 2002).

*This program adds.* A general output metric $G$ in place of the identity, and the use
of the matrix as the fidelity weight of a code.

*Differentiation.* The averaged read metric $\bar P_C$ is this matrix. The blind probe
of Chapter 10 is finite-difference active-subspace estimation on a consumer's margin.
The parents use the matrix to reduce the dimension of an input space. This program uses
it to decide what a compressor should keep.

## Rate–distortion theory (Shannon, Kolmogorov, Berger, Sakrison; Kostina–Verdú; Kostina–Tuncel; Rimoldi)

*Owns.* $R(D)$, reverse water-filling (Kolmogorov 1956; Berger 1971), the weighted
squared-error Gaussian case (Sakrison 1968), dispersion (finite-blocklength),
successive refinement (Equitz and Cover 1991; Rimoldi 1994), successive refinement
under individual distortion criteria (Nayak, Tuncel, Gündüz and Erkip 2010; Op 't Veld
and Gastpar 2017), and the multi-stage and $k$-observer rate regions.

*This program adds.* The function $R_C(D)$ is Sakrison's weighted rate–distortion
function with the weight set by the consumer. The program adds its measurement on
trained consumers. The two-observer region is successive refinement with two weighted
measures. The program adds the exact refinability condition, Loewner nesting of the
optimal error covariances $\Sigma^\star(P_2,D_2) \preceq \Sigma^\star(P_1,D_1)$, and the
exact excess rate. It also adds the mismatch **tax** $(r/2)\log(M/m)$ and the omission
**floor** $\operatorname{tr}(\tilde P\Pi)$ for using the wrong read metric.

*Differentiation.* Shannon's theory allows any fidelity measure, and Sakrison solved
the weighted Gaussian case. Most practice still fixes the measure to squared error,
which is the $P_C = I$ slice here. This program treats the fidelity measure as the
observer-dependent variable and measures it. Citations are exact:
the $k \ge 3$ region is Kostina–Tuncel (not an iteration of the two-stage map — VI-5);
dispersion constants are flagged [C7] to Kostina–Verdú, not re-derived (VI-7).

## Indirect (remote) source coding (Dobrushin–Tsybakov; Wolf–Ziv; Witsenhausen)

*Owns.* Coding an observed variable when the decoder's fidelity is judged on a hidden
or derived variable (Dobrushin and Tsybakov 1962; Wolf and Ziv 1970; Witsenhausen
1980). In the linear Gaussian case the induced distortion is a weighted squared error
whose weight comes from the task.

*This program adds.* The consumer as a trained black box whose weight is measured, and
the falsification record of the resulting predictions.

*Differentiation.* Indirect source coding already derives the fidelity weight from the
task. This program does not claim that step. It claims the cross-domain use and the
sealed tests.

## Secure source coding and leakage (Villard–Piantanida; Ekrem–Ulukus)

*Owns.* The rate–distortion–equivocation region for a source described to a decoder
while a second party holds correlated side information (Villard and Piantanida 2013,
Theorem 3). The vector Gaussian case with matrix distortion and Gaussian decoder side
information (Ekrem and Ulukus 2013). Ekrem and Ulukus leave the joint rate–leakage
problem open in general.

*This program adds.* The conditional leakage $I(X^n;M\mid S^n)/n$ read as the
re-encoding cost at the side-information holder. For Gaussian sources with an informed
encoder and no decoder side information, the companion papers give the exact
rate–leakage region in closed form.

*Differentiation.* The program's "conditional content" or "conditional work" is this
leakage. The discrete region is Villard and Piantanida's and is credited to them. The
Gaussian endpoint is close to Ekrem and Ulukus (2013, Theorem 5) and is credited to them.

## Thermodynamics of erasure (del Rio et al.; Sagawa–Ueda)

*Owns.* The work cost of erasing a system given side information, which is the
conditional entropy and can be negative (del Rio, Åberg, Renner, Dahlsten and Vedral
2011). Feedback control and information thermodynamics (Sagawa and Ueda 2009).

*This program adds.* The rate–work–distortion region, which treats description rate
and conditional reset work as separate resources for one description.

*Differentiation.* Conditional Landauer work is del Rio et al.'s quantity. The program
adds the coding-theoretic region around it.

## Perceptual / weighted-distortion coding

*Owns.* The practice of replacing $I$ with a perceptual weighting because the human
sensory consumer does not read uniformly.

*This program adds.* A principled account of *where the weighting comes from* (the
consumer's Jacobian pullback), for *any* consumer, recoverable when the consumer is a
trained black box.

*Differentiation.* Perceptual coding hand-tunes one tilt for one consumer (the eye/ear);
the read metric says every consumer has such a tilt and you can get it from the consumer
rather than guessing it. Indirect source coding (above) already derives the tilt in the
linear Gaussian case.

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
various end-to-end trained codecs that do so implicitly. Task-based quantization makes
this exact for estimation tasks (Shlezinger, Eldar and Rodrigues 2019). Hessian-aware
quantization weights error by loss curvature (Choi et al. 2017; Dong et al. 2019).

*This program adds.* An explicit, *identifiable* task operator $P_C$; a theory of when
task-awareness *matters* (the $\kappa$ law and the four degeneracies); and a falsifiable
prediction — the flip — sealed across domains rather than assumed.

*Differentiation.* Task-aware compression usually *trains* a code against a task
end-to-end; this program *identifies the read operator* (blind, no labels) and derives
what to keep, giving a transparent recipe with stated boundaries rather than an opaque
learned one. The flip is the premise of task-based quantization. This program does not
claim the premise. It claims the sealed cross-domain test of it. The Skeptic's
Appendix answers "isn't this just task-aware compression?" (Appendix E).

## Query complexity and confined probes (Arias-Castro–Candès–Davenport; Simchowitz–El Alaoui–Recht; Rashtchian–Woodruff–Zhu; Duchi et al.)

*Owns.* Lower bounds on what adaptive linear measurements can recover (Arias-Castro,
Candès and Davenport 2013). Query lower bounds for eigenvector and matrix problems
(Simchowitz, El Alaoui and Recht 2018; Rashtchian, Woodruff and Zhu 2020). The
dimension dependence of zeroth-order optimization (Duchi et al. 2015).

*This program adds.* The budget cliff, stated for read operators. A probe confined to a
span cannot identify the read operator outside it.

*Differentiation.* The budget cliff is the identifiability limit of confined probes.
The parents give the general lower bounds. The program states the instance it needs.

## Kernel alignment (Cristianini et al.)

*Owns.* The normalized Frobenius inner product of two positive semidefinite matrices as
a measure of their agreement (Cristianini et al. 2002).

*This program adds.* The alignment between the averaged read metric and the source
covariance, used to predict when the flip appears.

*Differentiation.* The alignment law $\kappa$ is this matrix cosine. The prediction is
the program's.

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

## References

Amari, S. and Nagaoka, H. (2000). *Methods of Information Geometry*. American
Mathematical Society and Oxford University Press.

Arias-Castro, E., Candès, E. J. and Davenport, M. A. (2013). On the fundamental limits
of adaptive sensing. *IEEE Transactions on Information Theory* 59(1).

Berger, T. (1971). *Rate Distortion Theory: A Mathematical Basis for Data
Compression*. Prentice-Hall.

Choi, Y., El-Khamy, M. and Lee, J. (2017). Towards the limit of network quantization.
*International Conference on Learning Representations (ICLR)*.

Constantine, P. G. (2015). *Active Subspaces: Emerging Ideas for Dimension Reduction in
Parameter Studies*. SIAM. doi:10.1137/1.9781611973860.

Constantine, P. G., Dow, E. and Wang, Q. (2014). Active subspace methods in theory and
practice: applications to kriging surfaces. *SIAM Journal on Scientific Computing*
36(4).

Cristianini, N., Shawe-Taylor, J., Elisseeff, A. and Kandola, J. (2002). On
kernel-target alignment. *Advances in Neural Information Processing Systems* 14.

del Rio, L., Åberg, J., Renner, R., Dahlsten, O. and Vedral, V. (2011). The
thermodynamic meaning of negative entropy. *Nature* 474, 61–63.

Dobrushin, R. L. and Tsybakov, B. S. (1962). Information transmission with additional
noise. *IRE Transactions on Information Theory* 8(5), 293–304.

Dong, Z., Yao, Z., Gholami, A., Mahoney, M. W. and Keutzer, K. (2019). HAWQ: Hessian
aware quantization of neural networks with mixed-precision. *IEEE/CVF International
Conference on Computer Vision (ICCV)*.

Duchi, J. C., Jordan, M. I., Wainwright, M. J. and Wibisono, A. (2015). Optimal rates
for zero-order convex optimization: the power of two function evaluations. *IEEE
Transactions on Information Theory* 61(5).

Ekrem, E. and Ulukus, S. (2013). Secure lossy transmission of vector Gaussian sources.
*IEEE Transactions on Information Theory* 59(9). arXiv:1108.3544.

Equitz, W. H. R. and Cover, T. M. (1991). Successive refinement of information. *IEEE
Transactions on Information Theory* 37(2), 269–275.

Hristache, M., Juditsky, A., Polzehl, J. and Spokoiny, V. (2001). Structure adaptive
approach for dimension reduction. *Annals of Statistics* 29(6).

Kolmogorov, A. N. (1956). On the Shannon theory of information transmission in the
case of continuous signals. *IRE Transactions on Information Theory* 2(4).

Nayak, J., Tuncel, E., Gündüz, D. and Erkip, E. (2010). Successive refinement of vector
sources under individual distortion criteria. *IEEE Transactions on Information Theory*
56(4), 1769–1781.

Op 't Veld, G. J. and Gastpar, M. C. (2017). Successive refinement of Gaussian
projections. Technical report, EPFL Infoscience.

Rao, C. R. (1945). Information and the accuracy attainable in the estimation of
statistical parameters. *Bulletin of the Calcutta Mathematical Society* 37, 81–91.

Rashtchian, C., Woodruff, D. P. and Zhu, H. (2020). Vector-matrix-vector queries for
solving linear algebra, statistics, and graph problems. *APPROX/RANDOM 2020*.

Rimoldi, B. (1994). Successive refinement of information: characterization of the
achievable rates. *IEEE Transactions on Information Theory* 40(1), 253–259.

Sagawa, T. and Ueda, M. (2009). Minimal energy cost for thermodynamic information
processing: measurement and information erasure. *Physical Review Letters* 102,
250602.

Sakrison, D. J. (1968). A geometric treatment of the source encoding of a Gaussian
random variable. *IEEE Transactions on Information Theory* 14(3).

Shlezinger, N., Eldar, Y. C. and Rodrigues, M. R. D. (2019). Hardware-limited
task-based quantization. *IEEE Transactions on Signal Processing* 67(20), 5223–5238.

Simchowitz, M., El Alaoui, A. and Recht, B. (2018). Tight query complexity lower bounds
for PCA via finite sample deformed Wigner law. *Proceedings of the 50th ACM Symposium on
Theory of Computing (STOC)*.

Villard, J. and Piantanida, P. (2013). Secure multiterminal source coding with side
information at the eavesdropper. *IEEE Transactions on Information Theory* 59(6),
3668–3692.

Witsenhausen, H. S. (1980). Indirect rate distortion problems. *IEEE Transactions on
Information Theory* 26(5), 518–521.

Wolf, J. K. and Ziv, J. (1970). Transmission of noisy information to a noisy receiver
with minimum distortion. *IEEE Transactions on Information Theory* 16(4), 406–411.

Xia, Y., Tong, H., Li, W. K. and Zhu, L.-X. (2002). An adaptive estimation of dimension
reduction space. *Journal of the Royal Statistical Society, Series B* 64(3), 363–410.
