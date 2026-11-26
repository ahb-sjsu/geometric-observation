# Chapter 25 — The Reset: Rate, Work, and Distortion

Chapter 7 charged a description one cost, its rate. Chapter 24 added a holder and a
second cost, the leakage $I(X;\hat X\mid S)$. This chapter keeps that information
quantity and changes who holds $S$ and what the quantity is read as. The holder is now
a physical reset agent, and the quantity is the content that must be discarded when the
memory carrying the description is cleared. The source is Paper V,
`paper/consumer-relative-landauer.tex`. Its results sit in four theorem rows of the
ledger (PAPER-V.a and PAPER-V.b at `[proved]`, PAPER-V.c and PAPER-V.d at
`[exploratory]`) and three operational rows (GO-7, GO-8, GO-9, each `[replicated]`,
the last two with a recorded caveat). Each result below carries its row and class.

## Two parties and two costs

A source block $X^n$ is drawn i.i.d. together with a correlated block $S^n$. An encoder
$f_n$ that sees only $X^n$ writes an index $M=f_n(X^n)$ into a memory with alphabet
$\mathcal M_n$. The consumer reads $\hat X^n=g_n(M)$ from the memory alone and is judged
by a bounded consumer distortion
$d_C(x,\hat x)=D_{\mathcal Y}(\mathcal C(x),\mathcal C(\hat x))$, where $\mathcal C$ is
the consumer's map and $D_{\mathcal Y}$ the loss on its output. Later the memory is
reset to a standard state by an agent that holds $S^n$. The consumer never sees $S^n$.
Three numbers describe a code:

$$
R_n=\frac1n\log_2\lvert\mathcal M_n\rvert,\qquad
D_n=\frac1n\sum_{i=1}^n\mathbb{E}\,d_C(X_i,\hat X_i),\qquad
L_n=\frac1n H(M\mid S^n).
$$

$R_n$ is the description rate. $L_n$ is the reset content of the memory relative to the
retained side information. Landauer's bound, in its conditional form, reads it as work:
an ideal isothermal reset at temperature $T$ costs at least

$$ W_n\ \ge\ n\,k_B T\ln 2\;L_n , $$

with $k_B$ Boltzmann's constant. This bound, its asymptotic tightness, and the memory
model are imported, not proved here (the paper cites Landauer 1961, del Rio and
co-authors 2011, and Faist and co-authors 2015; ledger rows PAPER-V.a and PAPER-V.d
record the import). It prices only the reversible lower limit of resetting a classical
degenerate memory, not sensing, transmission, error correction, or finite-time
operation.

The two coordinates are separate because they answer to different parties. The consumer
needs the whole index and has no side information, so $R_n$ counts the size of the
memory. The reset agent holds $S^n$, so only the part of $M$ that $S^n$ does not predict
has to be discarded. The consumer enters the work only through the codes its distortion
admits: once the joint law of $(M,S^n)$ is fixed, the minimum reset work does not depend
on who the consumer is.

## Whose quantity this is

The conditional information $I(X;\hat X\mid S)$ is not new. It is the conditional
leakage of secure source coding (Villard and Piantanida 2013; Ekrem and Ulukus 2013).
The repository's novelty assessment (`articles/2026-10-01-ot-novelty-assessment.md`)
records that Paper V's discrete region is Villard and Piantanida's Theorem 3 with no
decoder side information, up to a constant, and that the paper's contribution is the
thermodynamic reading and the Gaussian corners. It lists that credit as owed by the
paper, and the paper's related-work section in the repository does not yet carry it.
The paper does credit the minimum of the work coordinate as the common-reconstruction
rate-distortion function of Steinberg (2009), and conditional entropy-constrained
quantization (Chou and co-authors, 1989 and 1990) as a precursor of the two-resource
view. Chapter 24 reads the same quantity as what a holder learns. Here it is what a
reset agent cannot recover from $S$.

## The single-letter region and the coding theorem

For a test channel $q(\hat x\mid x)$ the chain $\hat X - X - S$ holds, because the
description is formed without $S$. Let $\mathcal T_C(D)$ be the channels with
$\mathbb{E}\,d_C(X,\hat X)\le D$, and define the single-letter region

$$
\mathcal U_C(D)=\bigcup_{q\in\mathcal T_C(D)}
\bigl\{(R,L):\ R\ge I(X;\hat X),\ \ L\ge I(X;\hat X\mid S)\bigr\}.
$$

Both coordinates are convex in the test channel `[proved]` (Lemma 1, ledger row
PAPER-V.a, net sealed as registration 042). The proof writes
$I(X;\hat X\mid S)=\sum_s p(s)\,I_{p(x\mid s)}(q)$. The route through
$I(X;\hat X)-I(S;\hat X)$ fails, because $I(S;\hat X)$ is itself convex in $q$; a
fresh-context audit (VI-8) caught that the first draft asserted the convexity without
an argument.

**Theorem 1 (region).** For a discrete memoryless pair $(X,S)$ on finite alphabets and
a bounded $d_C$, the closure of the achievable pairs at distortion $D$ equals the
single-letter region, $\mathrm{RW}_C(D)=\mathcal U_C(D)$, and no time sharing is
needed. This is `[exploratory]` (ledger row PAPER-V.c). The proof is written, and the
audits VI-8, VI-41, VI-43 and VI-44 found no false step, but the row records that no
numerical check can fail on it: the tested corner is an identity, and every other code
tested sits at least 0.311 bits above the boundary. Promotion needs a net on the
converse steps and on binning, then a custody file. The same row and class hold the
work endpoint, $W^\star_C(D,T\mid S)=k_BT\ln2\,L_C(D\mid S)$ with
$L_C(D\mid S)=\min_{q\in\mathcal T_C(D)}I(X;\hat X\mid S)$ (Corollary 1).

The scope is exact. Achievability is claimed for finite alphabets only. On general
alphabets the paper proves a per-code converse, $(R_n,L_n)\in\mathcal U(D_n)$, and the
passage to the limit $\mathcal U(D)$ uses a closed-graph property proved only for the
Gaussian regions below (also row PAPER-V.c, `[exploratory]`). Achievability with reset
side information on continuous alphabets is not claimed.

Three further statements about $\mathcal U_C(D)$ are `[proved]` (row PAPER-V.a). Every
exposed boundary point minimizes $\alpha I(X;\hat X)+(1-\alpha)I(X;\hat X\mid S)
+\beta\,\mathbb{E}\,d_C$ and satisfies a fixed-point equation that generalizes
Blahut and Arimoto's (Proposition 1). For a deterministic consumer output
$U=\mathcal C(X)$ recovered exactly, the minima are $R_C(0)=H(U)$ and
$L_C(0\mid S)=H(U\mid S)$ (Paper V's Cor. 2). And for two independent fair bits $X=(A,B)$
with $S=A$ and average Hamming distortion $D\le 1/4$, the lower boundary is

$$
R(t)=2-h_2(t)-h_2(2D-t),\qquad L(t)=1-h_2(2D-t),\qquad 0\le t\le D,
$$

with $h_2$ the binary entropy and $t$ the error placed on $A$ (Proposition 2). At
$D=0.15$ the endpoints are $(1.1187,\,0.1187)$ at $t=0$ and $(0.7803,\,0.3902)$ at
$t=D$. Reversing the two error allocations at $t=0$ keeps the rate $1.1187$ and raises
the content to $1$ bit, a ratio of $8.42$. Two limits stand beside this row. The
boundary is that of the achievable region only through Theorem 1, which is
`[exploratory]`. The custody file `claims/custody/PAPER-V.a.md` records that the
net covers $D=0.15$ only, with slack from 0.0074 to 0.13 bits depending on direction,
and that a 0.015-bit raise of the boundary for $t<0.9D$ was not caught. A mutation test
of the nets fired 18 of 18 gates and 9 of 17 probes, and was committed only after its
runs.

![Figure 25.1](figures/ch25_fig1.svg)

*Figure 25.1. The lower boundary of the rate and reset-content region for two fair bits (A, B) with the reset agent holding A, at average Hamming distortion D = 0.15 (Proposition 2). Moving along the curve shifts the allowed error from B to A. The endpoint at the lower right puts all error on B, the bit the reset agent does not know, and has the least content, 0.1187 bits, at rate 1.1187. The endpoint at the upper left splits the error evenly and has the least rate, 0.7803 bits, at content 0.3902. Rate and reset content trade against each other.*

## Gaussian sources

For a Gaussian source the alphabets are continuous, so the results are statements about
the single-letter region $\mathcal U(D)$. All three below are `[proved]` (ledger row
PAPER-V.b, net sealed as registration 044; its fresh-context passes are VI-9, VI-41,
VI-43, VI-44 and VI-46 to VI-49).

*No side information.* Let $X\sim\mathcal N(0,\Sigma)$ with $\Sigma\succ0$, let the
distortion be $(x-\hat x)^{\mathsf T}P_C(x-\hat x)$, and let $\lambda_i$ be the nonzero
eigenvalues of $\Sigma^{1/2}P_C\Sigma^{1/2}$. With $\theta$ set by
$\sum_i\min\{\lambda_i,\theta\}=D$,

$$ R_C(D)=L_C(D)=\frac12\sum_i\Bigl[\log_2\frac{\lambda_i}{\theta}\Bigr]_+ $$

(Paper V's Cor. 4). The row excludes its operational
reading and the case of singular $\Sigma$, which is proved but not netted. Its own check
in Paper V's sealed net is circular (VI-41), so its net is Paper III's rate-identity
harness.

*Scalar source.* Let $(X,S)$ be jointly Gaussian with variance $\sigma^2$, correlation
$\rho\in(-1,1)$, squared error, and $0<D<\sigma^2$. Then

$$
\mathcal U(D)=\Bigl\{(R,L):\ R\ge\tfrac12\log_2\frac{\sigma^2}{D},\ \
L\ge\tfrac12\log_2\frac{\sigma^2(1-\rho^2)+\rho^2D}{D}\Bigr\}
$$

(Paper V's Prop. 3). The region is one quadrant, and one channel attains both bounds, so a
scalar source has no trade-off between rate and work. The discount
$R_{\min}-L_{\min}=\tfrac12\log_2\frac{\sigma^2}{\sigma^2(1-\rho^2)+\rho^2D}$ decreases
in $D$ and tends to $I(X;S)=\tfrac12\log_2\frac{1}{1-\rho^2}$ as $D\to0$.

*Vector source.* For $r$ independent pairs $(X_i,S_i)$ with variances $\sigma_i^2$,
correlations $\rho_i$, weights $p_i>0$, and $c_i=\sigma_i^2(1-\rho_i^2)$, the lower
boundary is traced by $\alpha\in[0,1]$. Mode $i$ receives distortion
$d_i=\min\{\sigma_i^2,\delta_i\}$, with $\delta_i$ the positive root of

$$ 2\mu p_i\rho_i^2\,\delta^2+(2\mu p_ic_i-\alpha\rho_i^2)\,\delta-c_i=0 $$

and $\mu$ set by $\sum_ip_id_i=D$, and the boundary point is

$$
R=\sum_i\tfrac12\log_2\frac{\sigma_i^2}{d_i},\qquad
L=\sum_i\tfrac12\log_2\frac{c_i+\rho_i^2d_i}{d_i}
$$

(Paper V's Prop. 4, reset water-filling). At $\alpha=1$ this is classical reverse
water-filling. At $\alpha=0$ it moves distortion toward the modes the reset agent knows
least. The trade-off returns because modes differ in $\rho_i$: for two unit-variance
modes with $\rho=(0.95,0)$, equal weights, and $D=0.5$ the two endpoints differ by $0.1105$ bits of
content and $0.1306$ bits of rate. The custody file `claims/custody/PAPER-V.b.md`
records that the component inequalities of the proof are netted only in part, and that
the code-level reading of both propositions belongs to row PAPER-V.c.

If eigenmode $i$ is reset in a separate bank at temperature $T_i$, the least work is at
$d_i^\star=\min\{\lambda_i,\nu T_i\}$ (Paper V's Prop. 5, `[proved]`, row PAPER-V.a, as an
optimization inside an imported memory model).

## Storing the full block before projecting

**Theorem 2 (materialization).** If one register holds the full block $A=X^n$ and a
second holds any deterministic description $M=f_n(A)$, the reset content of the pair is

$$ H(A,M\mid S^n)=n\,H(X\mid S), $$

whatever distortion $M$ meets. This is `[exploratory]` (ledger row PAPER-V.d). The
mathematics is one line of the chain rule, its content is the imported Landauer
reading, and the row records that no net can fail on it.

## Several consumers

One memory serving consumers $1,\dots,m$ has the joint single-letter region, with
coordinates $I(X;\hat X_1,\dots,\hat X_m)$ and $I(X;\hat X_1,\dots,\hat X_m\mid S)$
(Theorem 3, `[exploratory]`, row PAPER-V.c). For exact outputs $U_j=\mathcal C_j(X)$,
with consumer $j$ decoding from its own memory $M_j$ alone, the least summed content
under independent reset is $\sum_jH(U_j\mid S)$ per symbol, and under coordinated reset
(each reset may use the memories not yet cleared) it is $H(U_1,\dots,U_m\mid S)$. They
differ by the conditional total correlation

$$ \mathrm{TC}(U_1;\dots;U_m\mid S)=\sum_{j=1}^mH(U_j\mid S)-H(U_1,\dots,U_m\mid S)\ \ge 0 $$

(Corollary 3, `[exploratory]`, row PAPER-V.d). Its history is part of the result. The
audit VI-41 found that Corollary 3 had no written proof. The audit VI-43 found that the
restated corollary omitted the condition that consumer $j$ reads $M_j$ alone, without
which the independent-reset clause is false. Both were fixed on 2026-11-21. The ledger
also records that the class of row PAPER-V.d was written by the assistant after the
author's reply of 2026-11-21 ("yes, I accept. Proceed as you recommend") to a question
about the split and the class of that row, a question that carried no recommendation
for the row, and that the class is open to the author's revision.

## Staleness

Let $X_0,X_1,\dots$ be a stationary Markov chain and let $M$ be made from $X_0$,
conditionally independent of the future given $X_0$. If the reset agent holds $X_t$,

$$ L_t=H(M\mid X_t)=H(M)-I(M;X_t), $$

and $L_t$ is nondecreasing in $t$ (Paper V's Prop. 6, `[proved]`, row PAPER-V.a). For a fair
bit that flips with probability $p$ per step and $M=X_0$, with
$q_t=\tfrac12\bigl(1-(1-2p)^t\bigr)$, the content is $L_t=h_2(q_t)$ and the predictive
information is $1-h_2(q_t)$. Chapter 19 treats age as what makes a certificate false.
Here the same age raises the work of clearing the record that the certificate was read
from. Chapter 27 takes up which access to the context makes age matter (ledger row
GO-12, `[predicted]`).

![Figure 25.2](figures/ch25_fig2.svg)

*Figure 25.2. Reset content against the age of the side information, for a record of one fair bit that flips with probability 0.05 per step (Paper V's Proposition 6). At age 0 the reset agent knows the bit and the content is 0. As the side information ages the content rises toward 1 bit, and the predictive information, the complement, falls toward 0. The curve is the formula of the text, not a measurement; the measured thresholds are under GO-8 below.*

## What is machine-checked

The build record `paper/consumer-relative-landauer-lean-blocks-2026-11-21.txt` and
`lean/README.md` state that seven Lean modules compile with no `sorry` and that the
audited theorems use only the standard axioms. On a finite-alphabet entropy layer they
cover Theorem 2's identity, Corollary 3 for $m$ consumers at every blocklength,
Paper V's Prop. 6 on the law of the whole path, and the per-code converse chain of
Theorem 1 for deterministic codes. Not formalized: the Landauer reading, randomized
encoders, Lemma 1, the region and all of achievability, Paper V's Cor. 2, and every
Gaussian result. The audits VI-50 and VI-51 read the formal statements of six modules against
the paper and found none unfaithful. `Covering.lean` has had no such reading. `claims/FRONTIER.md`
(row G14) records that no class changes on this account until a charter rule is added.

## Three operational results

These experiments run finite-length random codebooks and ask at what bin rate a
maximum-likelihood decoder recovers the stored index from its bin and the side
information. No physical work is measured.

**GO-7, separation** `[replicated]` (registrations 043, 045, 047; 046 is a miss). An
index needing $\hat R\approx0.67$ bits per symbol to describe is recovered from side
information at bin rate $0.26=0.39\hat R$ (error at $n=32$: 0.15, 0.06, 0.03 at bin
rates 0.13, 0.19, 0.26). Below its conditional content, at bin rate 0.03, the error
rises from 0.445 to 0.67 with $n$. Without $S$ the error is 1.00 at every bin rate.
Registration 043 passed 7 of 7 gates, 045 passed 6 of 6 across 5 codebooks (spread
0.03), and 047, on a scalar Gaussian source, passed 6 of 6 (decoding at $0.41\hat R$
with error 0.17 at $n=24$). Registration 046, the first Gaussian run, is a recorded
miss at 4 of 6: two instrumentation windows were set wrongly, the four physics gates
passed, and 047 is the corrected rerun with those gates unchanged. In 250 random
sources, 29.6% show endpoint gaps above 0.01 bit (median 0.004, maximum 0.067), so the
separation is small without structure in $S$.

**GO-8, staleness** `[replicated]`, with a caveat (registrations 049 and 053,
superseding 048 and 051; 048 missed at 4 of 5 on its control gate). For a fixed record of a binary Markov chain with $p=0.05$,
the decodable bin rate rises from 0.10 to 0.55 bits per symbol across ages 0 to 64,
within one grid step of the prediction at every age, and a fixed bin rate goes from 1%
error at age 0 to 100% at age 32. On a Gaussian first-order autoregressive source the
thresholds rise from 0.189 to 1.051, and the error at bin rate 0.35 goes from 0.076 to
1.00. The caveat stands at the same weight as the result. Registration 051 missed at 3
of 5. Registration 053, as executed, also recorded a miss: it failed only its control
gate, only on bins holding a single codeword, where an exact test must return a
p-value of 1.0 and the function `binom_sf` ignored its count argument when the success
probability was 1. The fix was made after the run. The as-executed result file is
committed unchanged, the rerun used the same seeds, the experimental data is
bit-identical, and the physics gates passed in the as-executed run too. The notes
(`experiments/GO-landauer-gaussian-secondsettings-NOTES.md`) call this the third
control-instrument defect of the campaign, and the `[replicated]` class of GO-8 rests
on the correction.

**GO-9, coordinated reset** `[replicated]`, with the same caveat (registrations 050
and 054, the latter superseding 052). With two records sharing a component, recovering either
record with the other intact lowers the decodable threshold by 0.60 and 0.45 bits per
symbol against 0.476 predicted (050, binary, 6 of 6 gates), including on the record
whose own side information is useless. A mismatched pairing saves nothing. On the
Gaussian source, 054 measured 0.193 and 0.196, which is 0.56 of the asymptotic gap.
Registration 052 missed at 5 of 6, and 054's pass rests on the same post-hoc fix to the
control statistic, with the same record: as executed a miss on single-codeword bins
only, data bit-identical between runs.

## What is still open

- Theorem 1, Theorem 3 and Corollary 1: nets on the converse steps and on binning, then
  a custody file (row PAPER-V.c, `[exploratory]`).
- Corollary 3: a search net over small codes for the independent-reset clause.
  Theorem 2 stays `[exploratory]` unless the charter gains a rule for such identities
  (row PAPER-V.d).
- Achievability with reset side information on continuous alphabets: not proved.
- The Lean attempt at Theorem 1's finite-alphabet achievability: paused on 2026-11-21
  with two of four milestones done (`claims/FRONTIER.md`, row G14).
- Gaussian coupling in which $\Sigma$, the conditional covariance given $S$, and $P_C$
  are not simultaneously diagonal: left open in the paper.
- Sources with memory, finite blocklength, quantum memories, and the cost of acquiring
  $S$: outside the model.
- Proposition 2's net at other distortions, and Paper V's Cor. 4 for singular
  $\Sigma$: not netted.
- The citation of Villard and Piantanida and of Ekrem and Ulukus in the paper: owed.
