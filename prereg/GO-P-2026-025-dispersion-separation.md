# GO-P-2026-025 — Dispersion counts read dimensions + observer separation: C3 harness

Registers the **C3 numerical falsification harness** for the two coding-theoretic
consequences (§`sec:consequences`): a finite-blocklength reduction and a source–channel
separation. Analytic results; harness is a falsification net, per R-IND-5. Governs
`experiments/verify_dispersion_separation.py`.

**Claims.**
- **(C) Dispersion.** For fixed $P_C$ of rank $r$, the finite-blocklength consumer coding
  problem for $d_{\mathcal C}$ is operationally identical, **at every blocklength $n$**, to the
  MSE problem for the $r$-dimensional tilted source $Y=P_C^{1/2}X$ (covering argument; encoder
  kernel side-information inert). Effective dimension $r_D=\#\{\text{active modes}\}\le r$, $=r$
  as $D\to0$. Kostina–Verdú constants transcribed, not derived (**[C7]**).
- **(D) Separation.** Transmissible within $D$ iff $\rho\,R_{\mathcal C}(D)\le C_{\mathrm{ch}}$
  (concatenation + data-processing converse). §VI's vacuity threshold is an **identification**
  limit, not this Shannon-capacity result.

```yaml
id: GO-P-2026-025
date: 2026-07-17
retrospective: false
kind: theorem-verification (C3 numerical falsification of two analytic results)
claim: "R_C(n,eps,D)=R_Y(n,eps,D) exactly (r-dim tilted MSE); r_D<=r; separation rho R_C(D) <=> C_ch."
harness: experiments/verify_dispersion_separation.py   # pure numpy
prediction:
  tilt_exact: R_C(D) = R_Y(D) (reverse water-filling on P_C^{1/2} Sx P_C^{1/2}) to 1e-14; ker P_C zero rate
  effective_dim: r_D = #active water-filling modes <= r, stepping r->..->1 as D grows; = r as D->0
  side_info_inert: an X-encoder with kernel side-info correlated with Y (corr ~0.30) cannot beat Y-covering
  separation: R_C(D)=C_ch boundary coincides with the Gaussian/AWGN OPTA D = gamma * 2^{-2 C_ch}
falsification: R_C != R_Y; a finite-n benefit from encoder kernel side-info; r_D > r; the separation
  boundary not matching OPTA — refutes the corresponding claim.
verification:
  - R-IND-5 derivation-grade fresh-context pass on (C) and (D).
  - SHARPENINGS the pass added (logged VI-7): (a) "exact at every n" rests on a COVERING argument, not
    "bijection on the range" (a first-order data-processing argument does NOT establish it); (b) the
    effective dimension is r_D <= r (= r only as D->0), NOT a flat r; (c) verbatim KV transfer is for the
    fixed-P_C Gaussian-quadratic case; the true-nonlinear (non-difference) case keeps a "should port" hedge.
  - [C7]: the dispersion CONSTANTS (scalar V=(1/2)log2^2 e; parallel V=(r_D/2)log2^2 e; third-order term)
    are cited from Kostina-Verdu 2012, not derived; verify theorem/equation numbers against the source.
amendments: []
hash: sha256:3fb3a825dd6b8e7166c3465321de4abbeb7ba624e2c624eecb08a1c1f19fe43e
```

## Falsification
The results are analytic; the harness is a falsification net. A mismatch on any registered prediction
sends the corresponding claim back to the proof. The derivation is additionally checked by a
fresh-context adversarial pass (R-IND-5) whose verdict, sharpenings, and [C7] citation flags are
recorded before the paper asserts the results.
