# Chapter 6 — Mathematical Preliminaries: Pullbacks, Projections, and the Read Distortion

This chapter assembles the machinery the rest of the book uses and assumes only
linear algebra and a first course in probability. A reader fluent in these can skim to
the two boxed results — the reverse-water-filling structure of the read distortion and
the magnitude-is-not-structure lemma — and refer back as needed. Nothing here is
deep; the discipline is in stating it exactly, because the program's honest negatives
are, one after another, the price of a preliminary taken loosely.

## Pullbacks

Let $C : X \to Y$ be differentiable with Jacobian $J = \partial C|_{x_0}$, and let $G
\succeq 0$ be a metric on $Y$. The **pullback** of $G$ through $C$ at $x_0$ is
$P_C = J^\top G J$. Two facts are used constantly.

*Composition.* Pullbacks compose contravariantly: if $C = C_2 \circ C_1$, then
$P_C = J_1^\top (J_2^\top G J_2) J_1 = J_1^\top P_{C_2} J_1$. The read metric of a
pipeline is the read metric of the last stage, pulled back through the earlier stages.
This is why a deep consumer still has a low-rank read metric: rank cannot increase
under pullback, so a scalar-output head forces the whole pipeline's read subspace to
be low-dimensional.

*Kernel.* $\ker P_C = \{ \delta : GJ\delta = 0 \}$. When $G \succ 0$ this is $\ker J$
— the directions the consumer's output is flat along. When $G$ is only PSD (a
degenerate output metric, e.g. a ranking that ignores some output coordinates), the
kernel grows accordingly. The nuisance is exactly this kernel.

## Projections and the read subspace

Diagonalize $P_C = \sum_i \lambda_i v_i v_i^\top$ with $\lambda_1 \ge \dots \ge
\lambda_r > 0 = \lambda_{r+1} = \dots$. The $\{v_i\}_{i \le r}$ span the read subspace;
the orthogonal projector onto it is $\Pi_C = \sum_{i \le r} v_i v_i^\top$. The
$\{v_i\}_{i>r}$ span $\ker P_C$. The eigenvalues $\lambda_i$ are the *sensitivities*:
how much a unit perturbation along $v_i$ costs the consumer. A code should protect
directions in proportion to $\lambda_i$ — pour bits where the consumer is sensitive,
spend nothing on the kernel. That instruction, made precise, is the COST theory.

## The read distortion as a reverse water-filling

Here is the first result worth boxing. Let a code produce error covariance
$\Sigma_\delta$ subject to a rate budget, and suppose (for this preliminary) that we
may choose $\Sigma_\delta$ freely along the eigenbasis of $P_C$ subject to a total
"resolution" constraint $\sum_i 1/d_i \le B$ where $d_i$ is the error variance
allocated to direction $v_i$ (smaller $d_i$ = more bits). Minimizing the read
distortion

$$ \operatorname{tr}(P_C\Sigma_\delta) = \sum_i \lambda_i\, d_i $$

subject to the budget yields, by a Lagrange argument identical in form to Shannon's,
an allocation that pours resolution into the high-$\lambda_i$ (high-sensitivity)
directions and abandons the low ones below a threshold:

$$ \boxed{\; d_i^\star \propto \lambda_i^{-1/2} \text{ above a water-line; } d_i^\star
   = \text{(free)} \text{ on } \ker P_C. \;} $$

The content is entirely in *which basis* the water-filling happens. Classical reverse
water-filling allocates by *source* variance (the eigenbasis of $\Sigma_x$); the read
distortion allocates by *consumer* sensitivity (the eigenbasis of $P_C$). When
$P_C = I$ these coincide up to the source shaping and you recover the slice. When
$P_C \ne I$ they diverge, and the divergence is the tilt of the COST shadow (Chapter
7) and the room for the flip of the VALUE shadow (Chapter 8). The full theory works in
the *joint* basis that simultaneously accounts for source energy $\Sigma_x$ and read
metric $P_C$ — the whitened basis $\Sigma_x^{1/2} P_C \Sigma_x^{1/2}$ — which is where
the two-observer max-determinant program lives and where a naive kernel projector
overstates the omission floor by $\sim 30\%$ (the VI-4 and VI-6 corrections, Chapter
15). Get the basis wrong and every constant is wrong; this is why the preliminary is
worth stating exactly.

## Magnitude is not structure

The second boxed result is a lemma the program learned by refuting four proxies for
it (NEG-6 through NEG-9). It is elementary and it is the difference between a working
theory and a plausible-sounding one.

> **Lemma (magnitude $\ne$ downstream structure).** The read distortion
> $\operatorname{tr}(P_C\Sigma_\delta)$ is *not* a function of the error magnitude
> $\operatorname{tr}(\Sigma_\delta)$ nor of any scalar norm of $\delta$. Two error
> covariances with identical total magnitude can have read distortions differing by an
> arbitrary factor, determined entirely by how $\Sigma_\delta$ is *oriented* relative
> to $\operatorname{range}(P_C)$.

The proof is one line: $\operatorname{tr}(P_C\Sigma_\delta) = \sum_{ij} (P_C)_{ij}
(\Sigma_\delta)_{ji}$ depends on the *alignment* of the two operators, not on
$\operatorname{tr}(\Sigma_\delta) = \sum_i (\Sigma_\delta)_{ii}$ alone. Concretely, on
KV-keys the controlling quantity was found to be the across-token variance of the
query-projected error $\operatorname{Var}_s(q\cdot\delta_s)$ — a *structured*
projection — and every attempt to replace it with an error-magnitude scalar failed:
the demeaned-norm proxy misordered the arms (NEG-6), the variance-ratio proxy achieved
only Spearman 0.80 (NEG-8), and even the read-distortion trace, while nailing the
discriminating flip, was not a complete order (NEG-9). The lesson, stated as a
preliminary so later chapters can lean on it: *the downstream-relevant content of a
coding error is its projection onto $P_C$, not its size.* Any method that scores a
code by the size of its error — which is every reconstruction metric — is measuring a
quantity the lemma says is decoupled from what it wants to know.

## The output metric $G$, concretely

For completeness, the output metrics used across the book:

- **Classifier (softmax):** $G$ is the Fisher information of the output distribution,
  so $P_C$ is the Fisher pullback and the read subspace is the span of the
  logit-gradient directions. For a near-decision-boundary operating point this is
  low-rank, dominated by the margin direction.
- **Estimator (DOA, backazimuth):** $Y$ is an angle, $G$ is squared angular error, and
  $P_C$ is the outer product of the estimator's angular sensitivity — the array
  manifold derivative $a'(\theta_0)$, projected off the manifold span (the corrected
  read operator $\hat g = P_a^\perp a'(\theta_0)$ of the DOA work; using $\operatorname{span}(A)$
  instead gives a degenerate scale-invariant reading, the VI that the DOA prereg
  caught).
- **Ranking (retrieval):** $G$ scores rank distortion; $P_C$ is (to leading order) the
  projector onto the query-response subspace, recovered blind by the margin-sensitivity
  probe $S = \mathbb{E}[g g^\top]$, $g = \hat a - \cos(a,b)\hat b$.

These are worked in their home chapters; collected here so the pullback $P_C = J^\top
G J$ is never an abstraction without an instance. With the machinery in hand, Part III
takes the read metric through its three shadows — the price of the read, the payoff of
the read, and the meaning of the read.
