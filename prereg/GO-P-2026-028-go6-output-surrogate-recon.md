# GO-P-2026-028 — GO-6: output vs surrogate vs reconstruction coding at matched rate

Closes the last promised-but-unrun registration (the paper's proposed **GO-6**). At matched
rate $R$, three coders are compared on the downstream consumer metric $d_O$; the predictions
are the qualitative content of Theorems B2 (output reduction) and B3 (high-resolution) plus
the $\ker P_C$ entropy-share gap. Synthetic (Tier A). Governs `experiments/verify_go6.py`.
Predictions are theorem-derived, not fitted; sealed before the governed run.

**Setup.** Nonlinear consumer $U=\mathcal C(X)=\phi(AX)$, $A\in\mathbb R^{r\times d}$ ($r<d$),
$\phi$ saturating and monotone; downstream $d_O(X,\hat X)=\|\mathcal C(X)-\mathcal C(\hat
X)\|^2$; local read operator $P_C=A^\top\mathrm{diag}(\E\phi'(AX)^2)A$ has rank $r$, so
$\dim\ker P_C=d-r>0$. Three coders at matched rate (matched as mutual information in each
coder's own space): **(a) output** — code $U$ under $D_Y$ (Thm B2-optimal); **(b) surrogate**
— code $X$ under the quadratic $d_{P_C}$, measure the true $d_O$; **(c) reconstruction** —
code $X$ under MSE, measure the true $d_O$.

```yaml
id: GO-P-2026-028
date: 2026-07-18
retrospective: false
kind: GO-6 synthetic coding experiment (Tier A; C3 falsification of Thms B2/B3 + kernel-gap)
harness: experiments/verify_go6.py   # pure numpy
instance:
  representation: X ~ N(0, Sx) on R^d (d=8)
  consumer: U = phi(A X), A in R^{r x d} (r=4), phi(z)=2.2 tanh(1.2 z); d_O = ||C(X)-C(Xhat)||^2
  coders: [output (code U under D_Y), surrogate (code X under d_{P_C}), reconstruction (code X under MSE)]
prediction:
  ordering: d_O(a) <= d_O(b) <= d_O(c) at every tested rate (3% tolerance), nonlinear consumer
  kernel_gap: median(d_O(c) - d_O(a)) > 0 with dim ker P_C = d-r = 4 > 0; the isotropic control
    (P_C = I) collapses the three coders (|d_O(c) - d_O(a)| < 1e-3)
  convergence: (d_O(b) - d_O(a)) / (d_O(c) - d_O(a)) < 0.15 at the highest tested rate
    (Thm B3 high-resolution: the quadratic surrogate approaches output-optimal as R grows)
falsification: an ordering violation beyond tolerance; no strict kernel gap (or the control not
  collapsing); or the surrogate-output relative gap not < 0.15 at high rate -> refutes the
  corresponding prediction (output-optimality / kernel-governed gap / B3 convergence).
verification:
  - synthetic C3 net; CI re-runs verify_go6.py and asserts "VERDICT: ALL PASS".
  - the predictions are the qualitative content of Thms B2 (output reduction) and B3 (high-res),
    which have their own R-IND-5 fresh-context passes (App. B; VI-3, VI-7); this is their operational net.
amendments: []
hash: sha256:a08188676c7418227df85102c5037ca6f8a50e93eef661541cd9eeee0d1e4770
```

## Falsification
The three predictions are theorem-derived. A miss on ordering refutes output-optimality (B2)
operationally; a missing kernel gap refutes the entropy-share account; a non-shrinking
surrogate-output gap refutes the B3 high-resolution convergence. Sealed and committed before
the governed run per REG-1 (CHARTER §4).
