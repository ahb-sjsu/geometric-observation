# GO-P-2026-024 — The price of a misidentified observer: C3 numerical harness

Registers the **C3 numerical falsification harness** for the mismatch theorems (Appendix
`app:mismatch`): the operational cost of water-filling for an estimated read operator
$\hat P$ when the truth is $P$. Analytic result; harness is a falsification net, per R-IND-5.
Governs `experiments/verify_observer_mismatch.py`.

**Claim.** Two regimes with a sharp asymmetry.
- **Commission** (mis-weighting, $m\hat P\preceq P\preceq M\hat P$ on a shared range, rank $r$):
  bounded excess rate $0\le R_{\hat P}(D/M)-R_P(D)\le\tfrac r2\log(M/m)$, tight at $P=m\hat P$.
- **Omission** ($\mathrm{range}\,P\not\subseteq\mathrm{range}\,\hat P$): a distortion **floor**
  $D_{\mathrm{floor}}=\tr(\tilde P\Pi)$, $\Pi$ the projector onto the **whitened** kernel
  $\Sigma_x^{-1/2}\ker\hat P$; true distortion stays in the compact band
  $[D_{\mathrm{floor}},\tr(P\Sigma_x)]$ (never unbounded), and reaching any $D<D_{\mathrm{floor}}$
  costs infinite rate. Projector model ($\Sigma_x=I$): $D_{\mathrm{floor}}=r(1-o)$ for overlap $o$.

```yaml
id: GO-P-2026-024
date: 2026-07-17
retrospective: false
kind: theorem-verification (C3 numerical falsification of an analytic result)
claim: "Commission tax dR<=(r/2)log(M/m) tight; omission distortion floor tr(Pt*Pi) (whitened kernel), band [floor, tr(P Sx)], rate->inf below floor."
harness: experiments/verify_observer_mismatch.py   # pure numpy
prediction:
  commission: with m*P_hat <= P <= M*P_hat, the safe plan meets true D and excess rate <= (r/2)log(M/m),
    ratio = 1.000 at P = m*P_hat (tight), d in {2,3}
  omission_floor: D_floor = tr(Pt*Pi) with Pi the WHITENED kernel projector; true distortion in
    [D_floor, tr(P Sx)]; finite zero-rate distortion; rate diverges as D -> D_floor+
  whitened_vs_naive: naive kernel r(1-o) overstates the floor by ~30% when Sx != I
  probe: projector model Sx=I gives D_floor = r(1-o) to machine precision
falsification: commission excess rate exceeding (r/2)log(M/m); a finite-rate allocation below the floor;
  distortion unbounded; floor != tr(Pt*Pi) — refutes the corresponding claim.
verification:
  - R-IND-5 derivation-grade fresh-context pass on both theorems (commission + omission).
  - CORRECTION the pass caught (logged VI-6): the floor uses the WHITENED kernel Sx^{-1/2} ker(P_hat),
    NOT the naive ker(P_hat); the naive value is ~30% off when Sx != I. Confirmed omission = FLOOR
    (not unbounded distortion), four independent ways.
  - The 0.647 Llama overlap -> 35.3% floor is a CONDITIONAL certificate (omission + equal weights);
    the paper states it as such (Prop 4 recovers the subspace, not the eigenvalues).
amendments: []
hash: sha256:7da1da9002c1554db82133d4e644cba82c77cc3c0dddc7bd353e0d349fe0269f
```

## Falsification
The theorems are analytic; the harness is a falsification net. A mismatch on any registered
prediction sends the corresponding claim back to the proof. The derivation is additionally checked by
a fresh-context adversarial pass (R-IND-5) whose verdict and corrections are recorded before the paper
asserts the result.
