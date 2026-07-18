# GO-P-2026-023 — Complete two-stage rate region + k-observer chain: C3 numerical harness

Registers the **C3 numerical falsification harness** for the region generalization of the
two-observer theorem (§\ref{sec:multiobs}; corner = GO-P-2026-022). Analytic result;
harness is a falsification net, per charter rule R-IND-5. Governs
`experiments/verify_rate_region.py`.

**Claim.** For $X\sim\mathcal N(0,\Sigma_x)$ and $P_1,P_2\succeq0$, the closure of the
achievable two-stage rate region is
$\mathcal R=\{(R_1,R_2):\exists\,\Sigma_f\preceq\Sigma_b\preceq\Sigma_x,\
\tr(P_1\Sigma_b)\le D_1,\ \tr(P_2\Sigma_f)\le D_2,\ R_1\ge\tfrac12\log\det\Sigma_x/\det\Sigma_b,\
R_2\ge\tfrac12\log\det\Sigma_x/\det\Sigma_f\}$. The **converse uses only** the
conditional-mean lemma, the law of total covariance, and the information bound — **neither
Markov monotonicity nor max-det uniqueness**. Refinability ($\Sigma_2^\star\preceq\Sigma_1^\star$)
and the exact rate loss are the min-sum-rate **corner** (uniqueness enters only there). The
$k$-observer region is the nested-chain analogue.

```yaml
id: GO-P-2026-023
date: 2026-07-17
retrospective: false
kind: theorem-verification (C3 numerical falsification of an analytic result)
claim: "Complete two-stage rate region R(D1,D2); corner = refinability iff Sigma_2*<=Sigma_1*; k-observer nested chain."
harness: experiments/verify_rate_region.py   # pure numpy; achievability via independent Fisher increments
prediction:
  achievability: for feasible nested (Sigma_b,Sigma_f), the independent-increment Gaussian channels
    reproduce Cov(X|Z1)=Sigma_b, Cov(X|Z1,Z2)=Sigma_f and the boundary rates to 1e-10
  converse: no random admissible two-stage code (5000+ trials, d in {2,3}) beats the region boundary
  corner: the Thm5/Thm6 corner is the min-sum-rate vertex; L>=0 and L=0 <=> Sigma_2*<=Sigma_1*
  kchain: the k=3 nested chain is reproduced exactly by independent Fisher increments
falsification: an achievability residual > 1e-6; any converse violation; L<0 or the corner not the
  nesting characterization; the k=3 chain not reproduced — refutes the corresponding claim.
verification:
  - R-IND-5 derivation-grade fresh-context pass on Theorem A (region), its converse provenance, and Theorem B (k-chain).
  - CORRECTIONS the pass caught (logged VI-5): (a) "Rimoldi is two-stage only" is wrong — Rimoldi is the
    finite-alphabet L-stage carrier, abstract k>=3 is Kostina-Tuncel 2019; (b) for k>=3 the two-stage
    K-map does NOT iterate (rotation ambiguity leaks Fisher info) — use independent Fisher increments.
amendments: []
hash: sha256:14326ab1b5b50c6abddba8f476cee7bd94267e325fe1abd159a588b30e78f2be
```

## Falsification
The theorem is analytic; the harness is a falsification net, not the proof. A mismatch on any
registered prediction sends the corresponding claim back to the proof. The derivation is additionally
checked by a fresh-context adversarial pass (R-IND-5) whose verdict and the corrections are recorded
before the paper asserts the result.
