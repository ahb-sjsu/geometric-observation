# Chapter 3 — Historical Precursors: Shannon, Rate–Distortion, and Information Geometry

I want to be scrupulous about what is new here and what is not, because the honest
answer is that almost none of the *components* are new, and the claim of the book is
entirely about the *composition*. This chapter is the positioning paragraph, written
once, at length, so that later chapters can point back and no reader is left thinking
the read metric was pulled from nowhere. It was pulled from four places, each of
which owns part of it. A fifth group of parents, the ones the first drafts of this book
left uncited, is named in the section "Parents the first drafts missed" below.

## Shannon, and the birth of the slice

Rate–distortion theory begins with Shannon: to reproduce a source $x$ to within an
average distortion $D$ under a fidelity measure $d(x,\hat x)$, you need at least
$R(D)$ bits, and $R(D)$ is achievable. For a Gaussian source under squared-error
distortion the theory is at its most beautiful — the optimal bit-allocation across
the source's eigen-directions is *reverse water-filling*, pouring bits into the
high-variance directions and abandoning the ones below a threshold. This is the
mathematics behind transform coding, behind JPEG, behind essentially every codec of
the twentieth century.

Notice what fixed the fidelity measure. Squared error weights every coordinate of
$x$ equally; it is the distortion of an observer that reads all directions the same.
Shannon's theory is not wrong to make this choice — it is a theory *given* a fidelity
measure, and squared error is a fine one to develop first. But the choice quietly
installed the slice as the default. Everything downstream inherited it: reverse
water-filling allocates bits by *source* variance, because under squared error the
directions that matter are the directions where the source varies. The moment the
distortion measure is not isotropic — the moment it is $\operatorname{tr}(P_C
\Sigma_\delta)$ for some non-identity $P_C$ — the water-filling must be done in a
*different* basis, the one that diagonalizes $P_C$ against the source, and the bits
flow toward what the *observer* reads rather than what the *source* varies. That
retilting is the whole content of the COST shadow (Chapter 7). It is Shannon's
theory with the fidelity measure taken seriously as a variable, not a constant.

## Weighted and perceptual distortion: the slice, tilted, but ad hoc

Engineers did not wait for a theory to notice that squared error was the wrong
yardstick. Perceptual coding — weighting quantization error by a model of human
vision or hearing — is exactly the practice of replacing $I$ with a non-identity
weighting because the *consumer* (an eye, an ear) does not read uniformly. So is
weighted MSE in a hundred application papers. The read metric is not a stranger to
this tradition; it is its formalization and its generalization. What those literatures
lacked was (i) a principled account of *where the weighting comes from* — it was
hand-tuned per application — and (ii) the recognition that the weighting is the
pullback of the consumer's own output metric, computable from the consumer, and often
recoverable *blind* (Chapter 10). Perceptual coding tilted the slice by hand for one
consumer, the human sensory system. The read metric says: every consumer has such a
tilt, it is $P_C = J^\top G J$, and you can get it from the consumer instead of
guessing it.

The information-theory side of this tradition is older and more exact than the
perceptual practice. Sakrison (1968) treated the Gaussian source under a weighted
squared error. The rate–distortion function $R_C(D)$ of Chapter 7 is that weighted
rate–distortion function. Indirect, or remote, source coding goes further
(Dobrushin and Tsybakov 1962; Wolf and Ziv 1970; Witsenhausen 1980). There the decoder
cares about a hidden variable, not the observed one. In the linear Gaussian case the
induced distortion is a weighted squared error whose weight comes from the task. So
point (i) above holds for perceptual coding, but indirect source coding already
derives the weight from the task in that case. Machine learning has the same idea in
Hessian-aware and sensitivity-weighted quantization (Choi et al. 2017; Dong et al.
2019). Signal processing has it in task-based quantization, which designs the
quantizer for the downstream estimate rather than the signal (Shlezinger, Eldar and
Rodrigues 2019). The flip of Chapter 8 is the premise of that line of work, stated as
a ranking reversal between reconstruction error and task loss.

## Amari and Čencov: the pullback metric already exists

Here is the component I least want to over-claim. The object $P_C = J^\top G J$ — a
metric on an input space obtained by pulling a metric on an output space back through
a map — is the **pullback metric**, and it is old. In information geometry, Čencov's
theorem singles out the Fisher information metric as the unique (up to scale) metric
invariant under sufficient statistics, and Amari's program develops the differential
geometry of statistical manifolds on exactly this foundation: a model is a manifold,
the Fisher information is its metric, and pulling it back through reparametrizations
is the daily bread of the subject. When the consumer $C$ is a probability model and
$G$ is the Fisher metric on its outputs, $P_C$ *is* a Fisher-information pullback.
The machinery is Amari's and Čencov's, and I claim none of it.

What I claim is the job. The information-geometry tradition studies the pullback
metric to understand *estimation and inference* on statistical manifolds — natural
gradient, the geometry of the EM algorithm, the second-order structure of learning.
It does not, as far as this program found, treat the pullback as the governing object
for *lossy representation across domains* — as the thing that decides whether your
quantizer, your embedding, your array codec is good, and that unifies compression,
spectral embedding, and physical estimation under one operator. The synthesis is the
claim: this classical pullback is the operative object for serving representations to
consumers, and naming it as such dissolves a family of unrelated engineering
surprises into one mechanism with one dial. The components are Čencov's and Amari's;
the *sentence* is the contribution. I state this here so that when the Skeptic's
Appendix meets the objection "isn't $P_C$ just Fisher information?", the answer is
already on the table: yes, in the case where the consumer is a likelihood — and the
point is not the operator but the load it is asked to bear.

## Active subspaces and gradient outer products: the estimator already exists

The average of $J^\top J$ over a data distribution has two more names, and both
come with estimators. In sensitivity analysis and uncertainty quantification it is
the active-subspace matrix (Constantine, Dow and Wang 2014; Constantine 2015). Its
dominant eigenvectors are the directions a model's output is sensitive to. It is
estimated from gradients or from finite differences. In statistical dimension
reduction it is the expected gradient outer product, or outer product of gradients
(Hristache et al. 2001; Xia et al. 2002). Its range estimates the central subspace
of a regression. The averaged read metric $\bar P_C$ of this book is this matrix with
a general output metric $G$ in place of the identity. The blind probe of Chapter 10
is finite-difference active-subspace estimation applied to a consumer's margin. The
quotient by $\ker P_C$ is the quotient by the kernel of the gradient outer-product
matrix. What this book adds is the use of the matrix to decide what a lossy code
should keep.

## Parents the first drafts missed

Several results in later chapters and in the companion papers have direct classical
parents. They are listed here so that no chapter has to claim them.

- **Conditional leakage.** The programme's "conditional content" or "conditional
  work" of a description $M$ to a party holding $S^n$ is $H(M\mid S^n)/n$. Under a
  deterministic encoder this equals the conditional leakage
  $I(X^n;M\mid S^n)/n$ of secure source coding. The discrete rate–distortion–leakage
  region is the rate–distortion–equivocation region of Villard and Piantanida (2013,
  Theorem 3). The vector Gaussian case is treated by Ekrem and Ulukus (2013).
- **Conditional Landauer work.** Erasure work with side information is del Rio,
  Åberg, Renner, Dahlsten and Vedral (2011).
- **Two observers.** Serving two observers with one scalable code is Gaussian
  successive refinement (Equitz and Cover 1991), under individual distortion criteria
  (Nayak, Tuncel, Gündüz and Erkip 2010; Op 't Veld and Gastpar 2017).
- **The budget cliff.** A probe confined to a span cannot identify a read operator
  outside it. This is the identifiability limit of confined probes. Lower bounds for
  adaptive sensing and matrix queries make it quantitative (Arias-Castro, Candès and
  Davenport 2013; Simchowitz, El Alaoui and Recht 2018; Rashtchian, Woodruff and Zhu
  2020), as does the dimension dependence of zeroth-order methods (Duchi et al. 2015).
- **Alignment.** The alignment law $\kappa$ is a matrix cosine. Kernel alignment uses
  the same normalized inner product (Cristianini et al. 2002).

Appendix A states each parent with full references and one sentence on what this
programme adds.

## von Luxburg–Radl–Hein, and the collapse that started it

The empirical seed of the book is a discouraging theorem. Von Luxburg, Radl, and
Hein showed that the commute-time (resistance) distance derived from a graph
Laplacian *degenerates* as the graph grows: pairwise commute distances converge to a
function of the two nodes' local degrees, losing the global geometry the embedding
was supposed to reveal. Read as a verdict on the tool, it says spectral embedding
dies at scale.

Read through the observer, it says something narrower and recoverable. The commute
distance is the reading of the embedding by *one* consumer — the one that ranks by
that distance — and the theorem is a statement about that consumer's read metric. Put
the embedding in polar form and the collapse is confined to the *radial* coordinate;
the *angular* coordinate keeps the geodesics [proved]. The geometry did not vanish;
it moved into the coordinate the distance-reading discards. This is the LEGIBILITY
shadow (Chapter 9), and it is the concrete case that taught the program the general
lesson: a degeneracy theorem for a representation is often a theorem about *one
observer's* read metric, and a different observer reads the surviving structure fine.

## Ng–Jordan–Weiss: the folk practice awaiting a reason

There is one more precursor, and it is a piece of folklore that turned out to be a
theorem. In spectral clustering, the Ng–Jordan–Weiss algorithm *row-normalizes* the
embedding — projects every node onto the unit sphere, keeping direction and throwing
away magnitude — before clustering. Practitioners did this because it worked; the
justifications were heuristic. The polar decomposition of the collapse theorem
supplies the missing reason: row-normalization is *exactly* the projection onto the
angular coordinate, which is exactly the read subspace of the geodesic-ranking
consumer, which is exactly the coordinate the collapse spares. A move made for a
decade on the grounds that it improved results turns out to be the optimal thing to
do for a specific, identifiable observer. Folk practice is often a theory that has
not been written down; here the read metric writes it down.

## The lineage, in one sentence

The read metric inherits its algebra from the pullback metric of Čencov and Amari,
its purpose-of-compression from Shannon and rate–distortion, its acknowledgment that
the fidelity measure is a free variable from perceptual coding, weighted
rate–distortion and indirect source coding, its estimator from active subspaces and
gradient outer products, and its founding
empirical puzzle from von Luxburg's collapse and its NJW resolution. What it adds is
the load: the claim that this one operator is the right object for lossy
representation *in general*, across compression, embedding, and physical estimation,
and that the claim is falsifiable, has been put at risk, and — where it survived and
where it did not — is written in a ledger. With the lineage on the table, Part II can
build the framework without owing anyone an unpaid debt.
