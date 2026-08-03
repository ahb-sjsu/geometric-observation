# GO-P-2026-044 — Gaussian region with reset side information: scalar corner + vector frontier, C3 harness

Registers the **numerical falsification harness** for the Gaussian-with-side-information
extension of the consumer-relative Landauer paper (new §VI propositions, added in response
to review): for jointly Gaussian scalar $(X,S)$ under MSE the rate–work region is a
**single-corner quadrant** (no scalar rate–work tradeoff; both minima attained by one
reverse channel), and for independent Gaussian read modes the frontier **reappears through
distortion allocation**, traced by a generalized water-filling whose $\alpha=1$ endpoint is
classical reverse water-filling and whose $\alpha=0$ endpoint tilts distortion toward
side-information-opaque modes — the Gaussian analogue of Prop 2. Governs
`experiments/verify_gaussian_sideinfo.py`.

**Claims under net.**
(Scalar) $R\ge\tfrac12\log_2(\sigma^2/D)$, $L\ge\tfrac12\log_2((\sigma^2(1-\rho^2)+\rho^2D)/D)$,
region $=$ the corner quadrant; converse at the second-moment level (Markov identity
$\mathrm{Cov}(S,\hat X)=\rho\,\mathrm{Cov}(X,\hat X)$, LMMSE bound
$e_{\mathrm{lin}}=(1-\rho^2)(v-c^2)/(v-\rho^2c^2)$, budget-binding reduction, stationary
point $c=1-D$), valid for arbitrary (incl. quantizer) reproductions; the side-information
discount $R_{\min}-L_{\min}$ decreases in $D$ and $\to I(X;S)$ as $D\to0$; among Gaussian
channels $L$ is pinned by $R$ (single curve).
(Vector, independent modes) per-mode single-letterization + scalar converse ⇒ frontier =
allocation program with per-mode quadratic
$2\mu p_i\rho_i^2d^2+(2\mu p_ic_i-\alpha\rho_i^2)d-c_i=0$, $c_i=\sigma_i^2(1-\rho_i^2)$,
clipped at $d_i=\sigma_i^2$ (omitted modes cost zero in both coordinates).

```yaml
id: GO-P-2026-044
date: 2026-08-03
retrospective: false
kind: theorem-verification (C3 numerical falsification of analytic results)
claim: "Scalar Gaussian rate-work region is a single-corner quadrant with side-information discount -> I(X;S) as D->0; vector region with independent read modes has a generalized-water-filling frontier whose endpoints are reverse water-filling (rate) and opacity-tilted allocation (work)."
harness: experiments/verify_gaussian_sideinfo.py   # pure numpy + math.erf, Tier A, seed 20260803
prediction:
  s1_moments: LMMSE algebra exact to 1e-10 on 2000 random (rho,c,v); grid minimum of
    l(c,v) over the admissible moment set matches the closed form and minimizer
    (1-D,1-D) to 5e-4 (grid resolution)
  s2_single_curve: 3000 random Gaussian channels satisfy L = 1/2 log2(1+(1-rho^2)(2^{2R}-1))
    to 1e-10
  s3_quantizers: no K-level quantizer channel (erf-exact R, L, D; ~hundreds tested)
    beats either scalar bound at its own distortion by 1e-9
  s4_discrete_corner: 41x21-quantized joint source + eq.-(20) optimizer reproduces the
    analytic corner within 0.06 bits at rho in {0.5, 0.9}, D=0.25, INCLUDING the corner
    degeneracy (alpha=0 vs alpha=1 channels within 0.03 bits of each other)
  s5_allocation: quadratic+mu-bisection is feasible (1e-9) and KKT-stationary (1e-5,
    scale-free) on 30 random instances x 4 alpha; 5000 random feasible allocations per
    case never beat the alpha-weighted optimum by 1e-9; alpha=1 equals classical reverse
    water-filling; fully omitted modes cost zero in both coordinates
  s6_strictness: registered example sigma=(1,1), rho=(0.95,0), p=(1,1), D=0.5 has
    L-gap and R-gap >= 0.05 bits between endpoint allocations; SEPARABILITY net on
    the quantized 2-mode product source (13^2 x 7^2): the full-channel optimizer's
    weighted objective at alpha in {0,1} is never below the per-mode discrete
    envelope (min over budget splits of per-mode optima ON THE SAME GRIDS) minus
    5e-3 solver tolerance. Exact-to-exact, so grid coarseness cannot false-fail;
    a joint channel beating the envelope would refute the separability step of
    the vector converse. PILOT NOTE (logged, pre-seal): the first pilot design
    gated the full-channel (R,L) against the ANALYTIC continuous endpoints with a
    [-0.07,+0.18] bracket and FAILED at alpha=0 (L +0.209 over) -- a net-design
    artifact, not a theory violation: the alpha=0 minimizer does not pin R, and
    coarse grids + finite iterations push the discrete optimum above the
    continuous value in the unconstrained coordinate. Redesigned to the
    envelope comparison above BEFORE sealing; the analytic-proximity numbers are
    REPORTED, not gated.
  s7_discount: monotone decreasing in D; -> I(X;S) at D->0 within 2e-3
falsification: any section failing its bar refutes the corresponding claim and sends it
  back to the proof; in particular a random allocation or full-channel point strictly
  below the frontier refutes the convexity/separability converse.
verification:
  - R-IND-5 derivation-grade fresh-context adversarial pass on both propositions,
    logged 2026-08-03 (ledger VI-9). VERDICT: CONFIRMED, 0 errors, 5 statement-level
    sharpenings (all folded into the .tex before seal): (a) WLOG E[Xh]=0 centering
    sentence; (b) c>0 on the feasible set so the discarded stationarity root is
    visibly infeasible, f''(1-D)>0 noted; (c) "L is a function of R alone within the
    Gaussian family" (non-corner Gaussian channels still realize other points on the
    pinned curve); (d) strict convexity => unique minimizer at every alpha, endpoints
    included; (e) the conditional single-letterization is an EQUALITY at the h(X|S)
    step and genuinely uses full cross-pair independence (S_{!=i} independent of
    (X_i,S_i)) -- stated in the proof hypothesis. The pass's prime suspect
    (non-convexity of L_i) is refuted exactly: L_i'' = c_i(c_i+2 rho_i^2 d) /
    (2 ln2 d^2 (c_i+rho_i^2 d)^2) > 0. Non-Gaussian nets run by the verifier:
    moment identity under a nonlinear channel (4M MC), 16 quantizer cases (uniform +
    Lloyd-Max), 200k admissible-moment probes at 20 (rho,D) combos, 40k-point
    brute-force 2-mode frontier -- zero violations. One redundant check left
    unchecked by the verifier (discretized alpha=0 fixed point) is EXACTLY harness
    section [4], which this registration governs.
amendments: []
hash: sha256:c728351a5cd637fe2d42595167d617ee49eb22c2c0edf4f84a300fa4671dda55
```

## Falsification
The results are analytic; the harness is a falsification net, not the proof. A mismatch on
any registered prediction sends the corresponding claim back to the proof (charter rules
R-IND-5, C-AI-2).
