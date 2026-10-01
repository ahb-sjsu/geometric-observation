# Coupled described variables: findings (2026-10-01)

Status: derived and checked numerically on Atlas. Not yet written into any manuscript. Proof write-ups are pending.

## Setting

The described variable Y is in R^m, and the context V and the side information S = V + U are vectors. The coordinates are coupled: no change of coordinates separates them into independent triples. A description W is Gaussian, P is the posterior covariance of T = (Y, V) given W, and J = H^T Sigma_U^{-1} H is the holder's Fisher information about T.

## Results

1. **The two costs in posterior-covariance form.** R = 1/2 log det Sigma_T / det P and L = 1/2 log det K (P^{-1} + J), where K = (Sigma_T^{-1} + J)^{-1}. The rate is the case J = 0.

2. **A convex program in the holder's posterior.** Let X = (P^{-1} + J)^{-1}. Then L(D) is the value of: minimize -1/2 log det X subject to tr E (X^{-1} - J)^{-1} E^T <= D and X <= K. The distortion constraint is an LMI. The program is convex with a unique optimum, and its KKT conditions are necessary and sufficient.
   - Check: max-det = brute force on 20 random instances with m in {2, 3} and r in {1, 2}, max |diff| 5.8e-8 (maxdet_check.out).
   - Prior art: the error-covariance parameterization is a standard vector-Gaussian technique. Credit it; do not claim it as new.

3. **The one-dimensional regime in closed form.** Let Delta = tr Sigma_Y - D. Among one-dimensional descriptions the best content is L_1(D) = 1/2 log2(1 + Delta / mu_max(Delta)), where mu_max is the largest generalized eigenvalue of (Sigma_T E^T E Sigma_T - Delta Sigma_T) v = mu K v. The read direction is the corresponding eigenvector.
   - Scalar check: this equals the closed form 1/2 log2 g* to 7e-15 (pencil_check.py check (a), run 2026-10-01: max abs err 7.3e-15). In the scalar case the pencil's eigenvalue equation is the paper's quadratic P(g).
   - Global optimality: L_1 is the global optimum exactly when the KKT certificate holds, which defines the regime boundary D_1. The certificate agreed with the optimizer's rank at every tested point (regime_check.out (A)). D_1 was 1.057, 1.057, 0.814 and 1.178 for the four test sources, each with tr Sigma_Y = 1.4.

4. **The read direction turns with the budget.** This holds whenever the holder's information touches the read.
   - Derivation: the direction is constant on a budget interval iff it is a principal axis of Sigma_Y uncorrelated with the context.
   - Rate: the rate-optimal read never turns (J = 0).
   - Gaussian information bottleneck: its projections are fixed eigenvectors (Chechik et al. 2005).
   - Example: with Sigma_Y = diag(1, 0.4) and the context along 50 degrees, the content-optimal read moves 47.5 -> 46.8 -> 45.1 -> 41.2 degrees as D goes 1.38 -> 1.1. The rate-optimal read stays at 0 degrees.

5. **Frame non-determination.** Three sources with the identical (Y, S) law have content-optimal reads at 50.0, 42.8 and 37.6 degrees (regime_check.out (C)). This is the frame-level version of Corollary 21.

## Observation Theory reading (for the OT papers, not the T-IT text)

There are two observers.
- **The decoder.** It is the consumer that judges distortion on Y; its read operator is E^T E.
- **The holder of S.** It pays the content; its information is J.

Classical single-observer theory always produces a fixed frame. PCA and reverse water-filling do, and so does the Gaussian bottleneck. Here the optimal read is the top eigenvector of a pencil that combines the decoder's read, the holder's information and the budget. It turns with the budget exactly when the two observers do not share an eigenvector, which is the encyclopedia's alignment condition ("pairing ... is valid only when they share an eigenbasis"). The cost is convex in the paying observer's posterior coordinate and indefinite in the encoder's.

Caveat: this is a reading of the results, not a theorem that nothing else can explain them.
