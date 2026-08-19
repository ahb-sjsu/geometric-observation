# The tilted filter closes over the Kalman statistics (affine case)

**Status: [exploratory] — derivation + 20-trial numerical check
(`crucible/verify_tilted_filter.py`), NOT sealed, NOT independently
verified, NOT yet in any manuscript.** Written 2026-08-19 as the first
result on the open problem exactly as verification pass VI-11 narrowed
it (claims/LEDGER.md): whether the state-dependent optimal estimate
admits a RECURSIVE/filtering form.

## The problem VI-11 left open

Paper VIII, Remark 2: for a state-dependent read operator $P_s(x)$ the
optimal estimate leaves the posterior mean and becomes the tilted mean

$$\hat x^{\star} = \big(\mathbb{E}[P_s(X)\mid Y]\big)^{-1}\,
\mathbb{E}[P_s(X)\,X\mid Y].$$

The open problem, after VI-11 removed the static case: does this
estimator admit a recursive form, or does state-dependent read geometry
break the filtering structure itself?

## Result (linear-Gaussian dynamics, affine operator)

Let the dynamics and measurements be linear-Gaussian, so the posterior
is exactly Gaussian, $X\mid Y \sim \mathcal N(m_t, S_t)$ with
$(m_t,S_t)$ from the ordinary Kalman recursion — a fact independent of
any loss, since the conditional law does not depend on how it will be
scored. Let the read operator be affine,

$$P_s(x) = P_0 + \sum_{k=1}^d x_k P_k,\qquad P_k=P_k^{\top},$$

with $P_s(x)\succeq 0$ on the support region and
$\bar P(m) := P_0+\sum_k m_k P_k$ invertible. Gaussian moment identities
($\mathbb E[X_kX_j] = m_km_j+S_{kj}$) give both conditional expectations
in closed form over $(m,S)$:

$$\mathbb E[P_s(X)\mid Y] = \bar P(m),\qquad
\mathbb E[P_s(X)X\mid Y] = \bar P(m)\,m + \textstyle\sum_k P_k S e_k,$$

hence

$$\boxed{\;\hat x^{\star} \;=\; m \;+\; \bar P(m)^{-1}\sum_{k} P_k\,S\,e_k.\;}$$

**Consequences.**

1. **The Kalman pair stays sufficient.** The tilted filter is the
   unmodified Kalman filter followed by a static output map
   $(m,S)\mapsto \hat x^{\star}$. No filter-state enlargement, no new
   recursion, no propagation of the tilted estimate itself (propagating
   $\hat x^{\star}$ in place of $m$ would corrupt the recursion — the
   tilt must be applied at read-out, never fed back).
2. **The tilt is a covariance phenomenon.** The correction is linear in
   $S$ and vanishes as $S\to 0$: with no uncertainty, state dependence
   of the read geometry is irrelevant, as it must be.
3. **Polynomial extension (claimed, unchecked).** For polynomial
   $P_s(x)$ of any fixed degree, Isserlis' theorem closes both moments
   over $(m,S)$ as explicit polynomials; sufficiency of the Kalman pair
   persists. Only the numeric affine case is checked so far.

## What remains genuinely open

- Non-Gaussian posteriors (nonlinear dynamics or measurements), where
  $(m,S)$ is not sufficient and the interesting question actually
  lives.
- Non-polynomial $P_s$ (threshold/cliff consumers) — though the
  belief-averaged smoothed operator of Paper VIII §VI is again an
  expectation, i.e. exactly the object computed here.
- Closed-loop use: whether certainty-equivalent control with
  $\hat x^{\star}$ in place of $m$ preserves any separation principle
  (almost surely not in general; quantifying the gap is a campaign
  candidate).
- Conditions on $(P_0, P_k, \text{support})$ making $P_s(x)\succeq 0$
  and $\bar P(m)$ uniformly invertible — the check script uses strongly
  PSD $P_0$ with small $P_k$, which guarantees both only with high
  probability.

## Verification state

`crucible/verify_tilted_filter.py` (seed 20260819): 20 random 4-dim
instances; the closed form matches direct numerical minimization of the
exact expected loss to $10^{-6}$ and beats the posterior mean on every
trial (margins $+0.001$ to $+0.072$); 8 random perturbations per trial
never beat it beyond Monte-Carlo noise (200{,}000 samples). Promotion
path per CHARTER: R-IND fresh-context derivation pass, then a Lean
statement of the affine identity, then (if wanted as a paper claim) a
sealed prereg for the closed-loop consequence.
