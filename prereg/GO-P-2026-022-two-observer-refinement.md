# GO-P-2026-022 — Two-observer successive-refinement theorem: C3 numerical harness

The theorem (Appendix C of the Observation-Theory paper; standalone draft
`paper/two-observer-theorem.tex`) is analytic. This entry registers the **C3 numerical
falsification harness** that must reproduce its claims before the theorem is sealed, per
charter rule R-IND-5. Governs `experiments/verify_two_observer.py`.

**Claim.** For a Gaussian source $X\sim\mathcal N(0,\Sigma_x)$ and two read operators
$P_1,P_2\succeq0$ with weighted-quadratic distortions, the two-stage pair $(D_1,D_2)$ is
successively refinable **iff** the single-stage optimal error covariances nest,
$\Sigma_2^\star\preceq\Sigma_1^\star$; and when they do not, the exact excess rate is
$L=\tfrac12\log(\det\Sigma_2^\star/\det\Sigma^\circ)$.

```yaml
id: GO-P-2026-022
date: 2026-07-18
retrospective: false
kind: theorem-verification (C3 numerical falsification of an analytic result)
claim: "Two-observer successive refinability <=> Sigma_2* <= Sigma_1*; exact max-det rate loss otherwise."
harness: experiments/verify_two_observer.py   # pure numpy; Sigma* via 1-D root-find (cap never binds)
prediction:
  distortion_met: tr(P_i Sigma_i*) == D_i to 1e-6
  nesting_equiv: (Sigma_2* <= Sigma_1*)  iff  (Lambda_1 <= Lambda_2),  Lambda_i = Sigma_i*^{-1} - Sigma_x^{-1}
  equitz_cover: P1=P2, D2<=D1  =>  Sigma_2* <= Sigma_1*  on 200/200 random pairs
  orthogonal_loss: Sx=I2, P1=diag(1,0), P2=diag(0,1), D1=D2=1/4  =>  L = 1/2 ln(1/D1) = R1(D1) (zero reuse)
falsification: any of the above failing (nesting/Lambda inconsistency; an Equitz-Cover pair
  not nesting; orthogonal loss != R1(D1)) refutes the corresponding claim.
verification:
  - R-IND-5 derivation-grade fresh-context pass on Lemmas 1-4, Thm 1, Thm 2 (logged separately).
  - NOVELTY delineation vs Nayak-Tuncel "individual distortion criteria" line (mandatory).
amendments: []
hash: sha256:a04519f8b38a904fdae431f29b3d9ca8bb2324773feea6ab92694795b8a5e2a5
```

## Falsification
The theorem is analytic; the harness is a falsification net, not the proof. A mismatch on
any registered prediction sends the corresponding claim back to the proof. The derivation
is additionally checked by a fresh-context adversarial pass (R-IND-5) whose verdict and the
prior-art delineation are recorded before the theorem is sealed or the paper asserts it.
