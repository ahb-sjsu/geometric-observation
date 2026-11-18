# Audit VI-23 — T1 note, version 3 (2026-11-17)

A fresh-context general-purpose agent audited `t1-learn-then-serve.tex` v3 as it stood at
18:12 on 2026-11-17 (md5 6944ed45…; the only later change before the audit returned was
hard-coded result numbers replaced by `\ref`). It was given the files, not the author's
conclusions, and wrote its own numerics (`audit-vi23/`, which do not import
`verify_t1_v3.py`). Its verdict: **no false mathematical step.**

## Findings and what was done

| Finding | Class | Disposition in v3 |
|---|---|---|
| Lemma 1: one-sided Bernstein and matrix Bhatia–Davis step | confirmed | — ; the exact roots t± (0.177, 0.189 on the draft's consumer) are now mentioned as usable |
| Setting: "V_W(α,·) is convex" asserted without proof, used for continuity | gap | replaced by right-continuity from (P3) in one line |
| Proposition 4: correction term did not shrink with ε, so the bound was vacuous unless D ≪ ε | sharpening | term is now λmax(J)·D·(1/a − 1/b)/(2 ln2 λmin W); the regret's correction scales with ε₊ + ε₋ |
| Proposition 4: "Theorem 3(b) with ν± = 0 attains it" inconsistent; knowledge model implicit; linear witnesses are recovered exactly from probes | gap | the minimax set-up is stated; the attaining design is named; both limits are stated |
| Theorem 6: every step confirmed; no violation in 262 one-dimensional and 21 multi-dimensional cases, closest within a factor of 12 | confirmed | — |
| Theorem 6: expanding about the reproduction kills the cubic term exactly and gives ρ_b with no ω, θ or Σ | sharpening | adopted: ρ = min{ρ_b, ρ_f}; Corollary 8 uses ρ_b (ρ̄/D falls from 0.15–0.19 to 0.002–0.025 on the checks) |
| Exact second-order coefficient c₂ | sharpening (formal, numerical) | recorded in Remark 7 as derived and checked by the audit, not proved |
| Softmax kernel stated as the output's all-ones direction | error (wording) | corrected: the logits' all-ones direction; softmax(Wx) has a kernel iff range W contains it |
| "Theorem 6 applies" was tied to Q ≻ 0 | overstatement | Theorem 6 needs no Q ≻ 0; Corollary 8 does; the registered arm B has λmin(Q) ≈ 2×10⁻⁴ |
| "the audit of version 2" for the 0.301 figure; the exact loss is 0.29999 | error (attribution) | corrected |
| Abstract: sharpness, test channels covered, what certification needs | overstatement | all three qualified (RLD I; as D → 0; an encoder given Q̂ and ε± but not the probes; Σ and an a priori λ) |
| "at least 38" and "0.44D–0.90D" | reproduced only by rerunning the author's script | numbers recomputed after the changes: at least 30; 0.53D–0.90D |

Not checked by the audit: the series' own theorems (converse with private randomness,
region identification, (P1)–(P3) with shifts), the unchanged low-rank, finite-difference
and probe-distribution remarks, Linder–Zamir, and Tropp's journal numbering.

**Disclosure for the registration draft:** the audit computed the eigenvalues of arm B's Q
on the registered instance, (1.97×10⁻⁴, 0.0689). This is a property of the instance, not
an outcome (arm B has no bars), and the draft's note for the cold reread records it.

## The auditor's details (verbatim)

```
T1 note v3 referee audit: details (auditor's scratch, 2026-11-17)
Audited file state: t1-learn-then-serve.tex md5 6944ed45e8b1c09c10a09dd842f1b06f (mtime 18:12:36).
The file changed during the audit (hard-coded "Corollary~7" in thanks/abstract -> \ref). Compiled numbering:
Remark 7 shares the theorem counter, so the certificate corollary is COROLLARY 8 (the brief's "Corollary 7").

Scripts (auditor's own; none imports verify_t1_v3.py):
  audit_lemma_prop_cor.py  (+ .out.txt)  Lemma constants, Lemma coverage on a non-commuting variance-extremal law,
                                         Prop 4 (p=1 closed form; p=2 own SLSQP solver, cross-checked with
                                         spectral_core to 1.2e-6), Cor 5 random test, softmax W, leaky ReLU, circle.
  audit_thm6.py            (+ .out.txt)  Thm 6: forward vs backward channel, note's rho, auditor's rho_back,
                                         exact second-order coefficient c2; 1-D families + 2-D/3-D consumers.
  audit_remarks.py         (+ .out.txt)  0.998 ratio recomputed, softmax lambda(Q), Cor 8 rhobar comparison.
  audit_v2_0301.py         (+ .out.txt)  exact loss for x+0.05 sin x at D=0.3 (author's Sigma/G/holder).
  v2.tex, v3_snapshot_1812.tex           the two versions compared.

1. Prop 4 sharpening. In the proof, for c>=1 and mu>=0, ln(1+c mu)-ln(1+mu) <= (c-1) mu, so
   (1/2)log det(I+cD'J)/det(I+D'J) <= (c-1) tr(D'J)/(2 ln2) <= lmax(J) D (1/a-1/b) / (2 ln2 lmin(W)).
   Consequence: regret >= tau_eps - (1-alpha) lmax(J) D (eps+ + eps-) / (2 ln2 lmin(Qhat)),
   i.e. tau_eps * (1 - (1-alpha) lmax(J) D/(p lmin(Qhat))) + O(eps^2): non-vacuous uniformly in eps.
   The note's term (1-alpha) lmax(J) D (1+eps+)/(2 ln2 lmin(Qhat)) does not shrink with eps, so for small eps the
   note's lower bound is vacuous unless D << eps. In p=1 the sharpened term is the exact first-order deficit
   (deficit/term in [0.031, 1.000] over 20000 random cases). p=2 example (a=.8,b=1.25,alpha=0,D at the validity
   edge): gap .488, note's lower bound -.841, sharpened .109.

2. Theorem 6 via the backward channel (auditor's). With Z = T - That ~ N(0,Delta) independent of That ~ N(0,Sigma-Delta)
   (RLD-I's channel: That = E[T|Z'], Z' = G T + N; its forward form is exactly the note's):
     loss = Z^T P(That) Z + kappa_That(Z) + R,  E kappa = 0 (cubic in Z, Z independent of That),
     E Z^T P(That) Z = tr(Q' Delta), Q' = E P(That);  Q = E P(That+Z);
     ||Q - Q'|| <= (1/2) sup||D^2 P|| E||Z||^2 <= (M2^2 + M1 M3) s  (first-order term vanishes).
   Hence |E loss - tr(Q Delta)| <= rho_b := (7/4 M2^2 + 2 M1 M3) s^2 + (sqrt5/2) M2 M3 s^(5/2) + (5/12) M3^2 s^3,
   with no omega, no theta, no lambda_min(Sigma). Neither rho nor rho_b dominates (rho is smaller when Sigma is large,
   e.g. the circle at sigma^2 = 10); min(rho, rho_b) is valid. rho_b < rho in 197/262 converged 1-D cases and all 2-D
   cases except softmax(4Wx). In Cor 8 on arm S: rhobar/D 0.151 -> 0.0067 (beta=.05), 0.1875 -> 0.0248 (beta=.2).

3. Exact second-order term (auditor's derivation, numerically confirmed):
     E loss - tr(Q Delta) = c2(Delta) + o(s^2),  c2 = E sum_i [ 1/4 (tr H_i Delta)^2 - 1/2 tr(H_i Delta H_i Delta) ],
   H_i = Hessian of component i of G^{1/2} C at T. In 1-D c2 = -(1/4) E[C''(T)^2] Delta^2 (<0; circle: -Delta^2/4,
   matches the note's expansion). Not sign-definite in general: C(x)=sum_j cos x_j, p=3, small Sigma gives c2>0
   (measured excess +1.537e-7 vs c2 +1.536e-7). Checks: 1-D excess/c2 in [0.943, 1.001] at Delta=0.004 Sigma;
   2-D/3-D agreement to 3 digits at the smallest s.
   Tightness: by Landau-Kolmogorov M2^2 <= 2 M1 M3, so rho's s^2-coefficient >= 1.25 M2^2 while |c2| <= M2^2 s^2/2
   (<= M2^2 s^2/4 in 1-D): rho/|excess| >= 2.5 (>= 5 in 1-D) at leading order; minimum found numerically 11.85
   (circle, Sigma=10, Delta=0.04). No violation of rho or rho_b in 262 converged 1-D cases and 21 multi-D cases
   (M_j and omega estimated as grid sups, i.e. from below, so the test is stringent).

4. Numbers reproduced: nu+=.2334, nu-=.5220, eps+=.1855, eps-=.2077, v2 eps=.2908 (x+0.2 sin x, m=32, delta=.1);
   exact roots t+=.1768, t-=.1888 (usable directly in place of eps+-). Ratio 0.99813 for all alpha (own quadrature,
   spectral_core design). x+0.05 sin x at D=0.3: exact loss 0.299994 (the "0.301" is sampling noise; the excess is
   negative at second order for componentwise consumers). Softmax arm B: rank W = 2, dist(1/sqrt3, range W) = 0.197,
   so P(x) > 0 everywhere and Q > 0, but eig(Q) = (1.97e-4, 0.0689) under Sigma=diag(2,.5): nonsingular but
   condition number ~350, lambda_min(P) -> 0 (1e-19 at |x|=20). Leaky ReLU: 6.6439p, 2.3219p. Circle formula: MC agrees.
   "at least 38" and "0.44D-0.90D": reproduced only by re-running the author's script (38.87; 0.442-0.898), not
   independently. Running it rewrote the untracked verify_t1_v3.json in the worktree (seeded; same content expected).

5. Continuity: right-continuity of V_W(alpha,.) follows from (P3)+(P2) alone: V(D) <= V(D') + (p/2)log(D'/D) for
   D' > D. Convexity (asserted, unproved in the note) is also true: log det(Delta^{-1}+J) = -log det(Delta : J^{-1})
   with the parallel sum jointly operator concave and -log det decreasing and convex.

6. Ledger: VI-22 records that it audited v1 (not v2); Remark 7 says "the audit of version 2".
```
