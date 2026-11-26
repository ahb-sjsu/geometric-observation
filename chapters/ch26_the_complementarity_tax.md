# Chapter 26 — The Complementarity Tax

Chapter 7 priced two observers served in sequence, a coarse one and then a fine one.
Chapter 25 priced the reset of one stored description against a context $S$ that the
eraser holds and the consumer never sees. This chapter joins the two: one description
serves two read operators at once, and the question is what the second consumer adds, in
bits stored and in ideal reset work. Two ledger rows carry it. Row GO-10 is the
complementarity tax. Row GO-11 is the exact conditional region behind the tax. Both rows
are class `[replicated]` today, and every result below carries that class. The replication
is of the rows' operational faces, each measured on two source families (registrations 058
and 059, 061 and 062); the registry grades the theorems netted by the sealed harnesses 060,
063 and 064 as citable at `[predicted]` grade (`claims/REGISTRY-ACCOUNTING.md`). No theorem of
this chapter has a `[proved]` row.

## The setting: two rank-one reads and the read plane

The source is $X\sim\mathcal N(0,\Sigma)$ on $\mathbb R^d$ with $\Sigma\succ0$ (the papers
write $\Sigma_x$). Consumers $A$ and $B$ have linearly independent read directions $u,v$,
read operators $P_A=uu^{\mathsf T}$ and $P_B=vv^{\mathsf T}$, and distortions
$d_A(x,\hat x)=(u^{\mathsf T}(x-\hat x))^2$, $d_B(x,\hat x)=(v^{\mathsf T}(x-\hat x))^2$.
Write $B=[u\ \ v]$ and call $Y=B^{\mathsf T}X$ the read plane: it is all that the two
consumers can be judged on. Its covariance is $\Sigma_Y=B^{\mathsf T}\Sigma B$, and

$$
\kappa=\det(B^{\mathsf T}\Sigma B)=\sigma_u^2\,\sigma_v^2\,(1-\rho_{AB}^2),
$$

where $\sigma_u^2=u^{\mathsf T}\Sigma u$, $\sigma_v^2=v^{\mathsf T}\Sigma v$ and
$\rho_{AB}$ is the correlation of the two reads under the source. $\kappa$ tends to zero
as the reads align.

The costs are the two coordinates of Chapter 25: a description $(\hat X_A,\hat X_B)$ has
rate $R\ge I(X;\hat X_A,\hat X_B)$ and reset content $L\ge I(X;\hat X_A,\hat X_B\mid S)$,
with ideal isothermal reset work $W^\star=k_{\mathrm B}T\ln 2\cdot L$ ($L$ in bits), for
$S$ jointly Gaussian with $X$ and the chain $(\hat X_A,\hat X_B) - X - S$. The conditional
coordinate is not new: conditional leakage comes from secure source coding
(Villard and Piantanida 2013, Ekrem and Ulukus 2013; Chapter 24). The multi-consumer
region that supplies these coordinates is proved in its source paper for finite alphabets
and bounded distortion; its Gaussian use here is an extension that the note flags and does
not re-prove (VI-10).

With $R_{AB}$, $L_{AB}$ the joint optima and $R_A,R_B,L_A,L_B$ the single-consumer ones,
the tax is the excess of joint service over the more expensive consumer alone:

$$
\mathrm{CT}_R=R_{AB}-\max(R_A,R_B),\qquad \mathrm{CT}_W=L_{AB}-\max(L_A,L_B).
$$

## The rate floor and when it is exact

For any description meeting $\mathbb E\,d_A\le D_A$ and $\mathbb E\,d_B\le D_B$,

$$
I(X;\hat X_A,\hat X_B)\ \ge\ \tfrac12\log_2\frac{\kappa}{D_AD_B},
\qquad\text{equivalently}\qquad D_A\,D_B\ \ge\ \kappa\,2^{-2R}.
$$

The floor is exactly the joint rate-distortion function if and only if
$\mathrm{diag}(D_A,D_B)\preceq B^{\mathsf T}\Sigma B$ (for
$0<D_A\le\sigma_u^2$, $0<D_B\le\sigma_v^2$). Outside that regime it is a strict floor
and $R_{AB}$ is the simultaneous-service max-determinant program of the two-observer
paper (Chapter 7). On the regime the tax has the closed form
$\mathrm{CT}_R=\tfrac12\log_2\bigl(\sigma_m^2(1-\rho_{AB}^2)/D_m\bigr)$, with $m$ the
consumer of smaller single rate. [`[replicated]`, ledger row GO-10; the information-level
statements are netted by the sealed harness 055: all 7 gates passed, the floors never
violated on 8000 channels, exactness switching exactly at the regime, the discount
identity below to $4.3\times10^{-11}$.]

The first draft stated the regime wrongly for the isotropic case ($\Sigma=\sigma^2I$,
unit reads at angle $\theta$, $D_A=D_B=D$). It read $D\le\sigma^2(1-\cos\theta)$, which
is false for obtuse angles. A fresh-context derivation pass (VI-10, 2026-08-03) ran the
counterexample $\theta=120^\circ$, $D=0.7$: the printed condition holds, yet the
max-determinant program exceeds the floor by $0.061$ bits. The correct condition is
$D\le\sigma^2(1-\lvert\cos\theta\rvert)$. The error was caught before the note asserted
it, the matrix statement survived a 135-instance net with no mismatch, and the obtuse
probe is a gate of 055. The same pass recorded five sharpenings. The recorded content
hash of registration 055 matches no stored version of its file; the file is unchanged
since its seal commit and the cause cannot be shown (VI-25, disclosed in
`prereg/SEAL-DISCLOSURES.json`).

![Figure 26.1](figures/ch26_fig1.svg)

*Figure 26.1. The rate floor for one description that serves two reads. Each curve is the set of distortion pairs at which the floor is met with equality at the stated rate, drawn for a read plane with kappa = 1 (two orthogonal reads of unit variance). Below a curve the pair cannot be reached at that rate. Lowering one consumer's distortion at a fixed rate raises the other's. In this case the floor is the joint rate-distortion function on the whole square shown, since the exactness condition is that both distortions are at most 1.*

## The work floor and the discount

Put $\Sigma_{X\mid S}=\mathbb E[\operatorname{Cov}(X\mid S)]$ and
$\kappa_S=\det(B^{\mathsf T}\Sigma_{X\mid S}B)$. For $(X,S)$ jointly Gaussian and any
description meeting the two distortion constraints,

$$
I(X;\hat X_A,\hat X_B\mid S)\ \ge\ \tfrac12\log_2\frac{\kappa_S}{D_AD_B},
\qquad
W^\star\ \ge\ k_{\mathrm B}T\ln 2\cdot\tfrac12\log_2^{+}\frac{\kappa_S}{D_AD_B}.
$$

The inequality needs no Markov hypothesis (a strengthening found by VI-10); the chain
scopes the model in which the left side is the reset coordinate. The two floors differ by
exactly

$$
\tfrac12\log_2\frac{\kappa}{\kappa_S}=I(u^{\mathsf T}X,\,v^{\mathsf T}X;\,S),
$$

the information the reset context holds about the read plane. So $\kappa_S\le\kappa$
always, and a context independent of the read plane discounts nothing.
[`[replicated]`, ledger row GO-10, registration 055.] Unlike the rate floor, the work
floor is generally not attained at $D>0$. Row GO-11 says exactly when it is.

A worked instance sets the operational targets: $\Sigma=I_2$, orthogonal reads, equal
distortion $D$, and $S=u^{\mathsf T}X+N$ with $s^2=\operatorname{Var}(X_1\mid S)$. Then
$\mathrm{CT}_W=\tfrac12\log_2\bigl((s^2+(1-s^2)D)/D\bigr)$ and

$$
\mathrm{CT}_R-\mathrm{CT}_W=\tfrac12\log_2\frac{1}{s^2+(1-s^2)D},
$$

which is zero for a useless context ($s^2=1$) and rises to $I(X_1;S)$ as $D\to0$.

## What is prior work and what the record found no prior for

The novelty record (`paper/complementarity-tax-NOVELTY.md`, four independent searches,
2026-08-03) rescoped the note. After the reduction to the read plane, the rate floor is
the Gaussian evaluation of Gray's 1973 conditional rate-distortion lower bound, and the
exactness regime is the low-distortion branch of the bivariate individual-distortion
problem: Xiao and Luo 2005, Lapidoth and Tinguely 2010, and the semidefinite-condition
literature (Stylianou and coauthors 2021, Chen and coauthors 2026). The book attributes
both and keeps the proofs for completeness. The Xiao and Luo paper was checked through two
restatements, not at the source. The record found no prior, under its recorded queries,
for the tax quantity, for the packaging of two rank-one reads through $\kappa$, and for
the whole work side (the conditional floor, the discount identity, the tax gap). That is
absence under those queries, not a proof of novelty. One literature chore is open:
the full text of Kastner and Schlatter 2024, which could not be retrieved.

## The tax measured on stored records

Two registrations measured the gap between rate tax and work tax on codebook records,
with the decode-threshold instrument of rows GO-7 to GO-9 (Chapter 25), each sealed with a logged pilot and
run once.

| Registration | Source | Predicted gap | Measured gap | Fraction of prediction | Mismatched-context null |
|---|---|---|---|---|---|
| 058 | Gaussian, orthogonal reads | $\tfrac12\log_2\bigl(1/(s^2+(1-s^2)\hat d)\bigr)$ | $0.266$, $0.094$ bits at $s^2=0.2$, $0.5$ | $0.57$, $0.37$ | within $\pm0.003$ |
| 059 | binary | $1-h_2(\hat d\ast q)$ | $0.207$, $0.043$ bits at $q=0.1$, $0.25$ | $0.77$, $0.43$ | $0.001$, $-0.002$ |

Here $\hat d$ is the record's measured distortion, $q$ the crossover of the binary
context, $h_2$ the binary entropy and $a\ast q=a(1-q)+q(1-a)$. Both runs passed 6 of 6
gates. The measured gap is monotone in context quality and zero for a mismatched context
[`[replicated]` on two source families, ledger row GO-10, registrations 058 and 059].
The instrument realized between $0.37$ and $0.77$ of the predicted gap, not all of it;
the Gaussian strong-side fraction matches the $0.56$ of row GO-9. In both runs the joint
eraser put its bin bits on the record its context cannot resolve, which the row reports
and does not gate. The pilots changed the gates before sealing: 058's tracking gate was
reshaped to a fraction window, and for 059 an instrument crash was fixed and two bars
were calibrated on the pilot, all disclosed in the registrations.

The sweep of the rate tax over the angle $\theta$ was deliberately left unregistered on
2026-08-04. Its predictions are the attributed rate theory, already checked by 055, so
it is at most `[exploratory]`, and nothing in this chapter rests on it.

## GO-11: the exact conditional function for one rank-one read

Theorem and conjecture numbers from here to the end of the chapter are those of the GO-11
manuscript (`paper/go11-conditional-region.tex`, v0.11), not of this book.
Take one consumer with read $Y=w^{\mathsf T}X$, normalized to unit variance, and a context
$S=V+U$, where $V$ is a unit-variance linear function of $X$ with $\rho=\mathbb E[YV]$,
$\lvert\rho\rvert<1$, and $U\sim\mathcal N(0,\tau^2)$ is independent noise. $V$ is the
part of the context the encoder can compute. Theorem 1 (pair sufficiency): the channel may
depend on $X$ only through $(Y,V)$, so in any dimension the problem depends on
$(\rho,\tau^2)$ alone. Theorem 2: with $s=1+\tau^2$ (not the $s^2$ of the instance
above), for $0<D<1$ the minimum of $I(X;\hat Y\mid S)$ subject to
$\mathbb E(Y-\hat Y)^2\le D$ is

$$
L(D)=\tfrac12\log_2 g^\star,\qquad
g^\star=\text{the larger root of }\ D\,s\,g^2-(D+s-\rho^2)\,g+(1-\rho^2)=0 .
$$

Since the quadratic equals $(D-1)\tau^2<0$ at $g=1$, exactly one root exceeds $1$. The
value reduces to the classical $1/D$ at $\rho=0$, to Gray's conditional function as
$\tau^2\to0$, and to Steinberg's scalar common-reconstruction corner as $\rho^2\to1$.
[`[replicated]`, ledger row GO-11; harness 060 passed 6 of 6, the quadratic against
direct optimization to $2.0\times10^{-13}$.] The row calls this the first vector-Gaussian
function of common-reconstruction type; the targeted search found none in print. The
attribution is recorded with it: the chain-rule identity
$I(X;\hat X)-I(X;\hat X\mid S)=I(\hat X;S)$ and the one-constraint region are Paper V's
or folklore, and the scalar single-distortion instance of the frontier is prior work
(Wang and coauthors; Günlü and coauthors for the conditional coordinate under
degradedness).

The drafting record carries two catches (verification addenda 1 to 8 of
`paper/go11-conditional-region-NOVELTY.md`). The draft stated a cubic; the fresh-context
pass showed one factor spurious, reduced it to the quadratic, proved uniqueness and closed
the converse analytically. The draft also claimed that Theorem 2 settled the whole
frontier. That was an overclaim, and correcting it produced the next result.

## The frontier: two water levels and two corners

Theorem 3 gives the whole rate-work region for $\rho^2\in(0,1)$, $\tau^2>0$, $0<D<1$. Its
Pareto frontier is traced by $\alpha\in[0,1]$ through channels $\hat Y=aY+bV+N$,
$N\sim\mathcal N(0,n)$, solving

$$
a=1-\alpha\gamma_0-(1-\alpha)\gamma_1,\qquad
m=\frac{a\rho}{s-(1-\alpha)\gamma_1},\qquad b=(1-\alpha)\gamma_1 m,
$$

$$
n=D-h(a,b),\qquad \gamma_0=\frac{n}{Q_0+n},\qquad \gamma_1=\frac{n}{Q_1+n},
$$

with $h=(1-a)^2-2(1-a)b\rho+b^2$, $Q_0=a^2+b^2+2ab\rho$ and
$Q_1=Q_0-(a\rho+b)^2/s$. The frontier point is
$(R,L)=\bigl(\tfrac12\log_2(1/\gamma_0),\ \tfrac12\log_2(1/\gamma_1)\bigr)$: two water
levels, one per coordinate. The rate-optimal channel has $b=0$ and the work-optimal one
has $b\ne0$, so whenever the context is misaligned, $\rho^2\in(0,1)$, no channel attains
both corners. At $(\rho^2,\tau^2,D)=(0.75,0.5,0.3)$ the two excesses are $0.0400$ and
$0.0349$ bits. The single-corner region of Paper V's scalar case (Chapter 25) is exactly the
alignment degeneracy ($\rho^2\to1$, or $\rho=0$). [`[replicated]`, ledger row GO-11,
harness 060: corner excesses exact.]

## Two consumers, and the correction of Conjecture 3

For two rank-one consumers and a scalar context, Theorems 4 and 5 reduce the problem to
the triple $T=(Y_A,Y_B,V)$ and show that Gaussian channels $\hat{\mathbf Y}=AT+N$ exhaust
the region, a nine-parameter matrix program. The conjectured scalar water-filling for two
consumers was withdrawn: none emerged. From the program the GO-10 gap formula above is
derived, not assumed (060: anchors to 4 decimals).

Conjecture 3 guessed that the work floor is attained when
$\Delta=\mathrm{diag}(D_A,D_B)\preceq\Sigma_{Y\mid S}$. Theorem 6 corrects it. With
$\beta=\operatorname{Cov}(Y,V)$ and $\Sigma_{Y\mid V}=\Sigma_Y-\beta\beta^{\mathsf T}$, the
floor $\tfrac12\log_2(\det\Sigma_{Y\mid S}/\det\Delta)$ is attained if and only if

$$
\text{(a)}\ \ \tau^2=0\ \text{ and }\ \Delta\preceq\Sigma_{Y\mid V},
\qquad\text{or}\qquad
\text{(b)}\ \ \beta=0\ \text{ and }\ \Delta\preceq\Sigma_Y .
$$

The context must be computable from $X$ and satisfy the semidefinite condition, or be
blind to the read plane. The matrix that matters is the encoder-accessible
$\Sigma_{Y\mid V}$, not $\Sigma_{Y\mid S}$. In every other case the floor is strict, with
a deficit that tends to zero as $\Delta\to0$. [`[replicated]`, ledger row GO-11.]

## Theorems 7 to 10

- **Theorem 7** (vector context, one rank-one read). After whitening
  ($\Sigma_T\to I$, $\Sigma_{T\mid S}\to\Lambda$, read direction $y_0$), the frontier is
  the generalized two-water-level system
  $u=\bigl(1-\alpha\gamma_0-(1-\alpha)\gamma_1\bigr)\bigl[(1-(1-\alpha)\gamma_1)I+(1-\alpha)\gamma_1\Lambda\bigr]^{-1}y_0$,
  $n=D-\lvert y_0-u\rvert^2$.
- **Theorem 8** (higher-rank reads). The region is a matrix program. It decomposes
  exactly into per-mode Theorem 7 systems when $\Sigma_T$ and $\Sigma_{T\mid S}$ are
  simultaneously block-diagonal. A companion proposition proves the minimizer unique at
  every interior $\alpha$ by matrix convexity, which retires a hedge in Theorem 3.
- **Theorem 9** (the frontier system for two consumers). The water levels become
  $2\times2$ matrices $M_0,M_1$. With $w\in[0,1]$ the weight on rate, $\Sigma_N$ the channel
  noise covariance and $\mu$ the distortion multipliers, and assuming an optimum is attained
  with $\Sigma_N\succ0$, every Pareto-optimal channel satisfies
  $\Sigma_N^{-1}=wM_0^{-1}+(1-w)M_1^{-1}+\mathrm{diag}(\mu)$, off-diagonal entry included;
  at $w=1$, on the regime where the two-consumer rate floor is exact, $\mu_i=1/D_i$ with no
  symmetry assumption. The frontier is contained in
  the solution set; the theorem does not claim the converse.
- **Theorem 10** (binary pair). For a doubly symmetric binary pair with
  $\Pr[Y\ne V]=p$ and $S=V\oplus\mathrm{Bern}(q)$, the conditional function is
  $L(D)=h_2(u)-(1-p)h_2(d_0)-p\,h_2(d_1)$, $u=a\ast q$, $a=(1-p)d_0+p(1-d_1)$, where
  $(d_0,d_1)$ solves $(1-p)d_0+p\,d_1=D$ and the tilt equation
  $\ell(d_0)-\ell(d_1)=2(1-2q)\,\ell(u)$, $\ell(x)=\ln\frac{1-x}{x}$. The discount is
  exactly $1-h_2(u)$.

All four are `[replicated]` under ledger row GO-11. Harness 064 passed 6 of 6 on
Theorems 9 and 10 (the off-diagonal identity to $1.3\times10^{-7}$, the binary
certificates to $3.4\times10^{-14}$). Harness 063 covers Theorems 7, 8 and uniqueness;
its pass (6 of 6) is recorded in `claims/REGISTRY-ACCOUNTING.md`, while the ledger
row's result cell lists no outcome for it.

## The encoder tilt measured

Theorem 2's optimal record is tilted toward the computable part of the context. Two
registrations tested this at matched consumer distortion, comparing a tilted record with
one that encodes the read alone.

| Registration | Source | Tilt advantage | Content of tilted record | Content of read-only record | Blind probe |
|---|---|---|---|---|---|
| 061 | Gaussian | $0.595$ bits per symbol | $0.621$ against Gray floor $0.500$ | $1.015$ against Steinberg $0.661$ | $0.000$ |
| 062 | binary | $0.5214$ against committed $0.5203$ | target $0.0894=h_2(p)-h_2(D)$ | target $0.2121$ | $0.000$ |

Both passed 6 of 6: the encoder-side tilt holds on two source families [`[replicated]`,
ledger row GO-11, registrations 061 and 062]. The blind probe is a record built to have
zero coupling with the context; its dependence on the context measured $0.000$. The
qualifications sit beside these numbers. The tilt costs rate, a premium of $0.161$ bits
in 061, reported and not gated. The Gaussian advantage of $0.595$ exceeds the
asymptotic prediction $0.3219$ of registration 061, whose pilot note attributes this to
the read-only record realizing its content slowly at finite block length ($1.015$
against $0.661$). The first 061 pilot exposed three gate defects, restated before
sealing. Theorem 10 later derived the noisy-context discount that 062 had reported
without a formula: $1-h_2(1/6)=0.3500$ against $0.3432$ measured.

## What is still open

- The full text of Kastner and Schlatter 2024 is unread (GO-10 row, open chore). The
  Xiao and Luo 2005 primary is also unretrieved (novelty record).
- The $\theta$ sweep of the rate tax is unregistered, at most `[exploratory]`.
- Uniqueness of Theorem 9's system was open in the manuscript; the GO-13 row records it
  resolved by a moment-convexity lemma (registration 074), in a row of class
  `[demonstrated]`.
- Whether decode thresholds track the exact frontier, and what the unrealized fraction
  ($0.37$ to $0.77$ realized) is made of, is posed in the manuscript and not registered.
- The strict-floor deficits of Theorem 6 are below the instrument's resolution and were
  not gated (registration 061).
- The GO-11 theorems have fresh-context passes and sealed harnesses but no `[proved]`
  row. The dynamic extension is Chapter 27.
