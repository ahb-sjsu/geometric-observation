# GO-14 probe record (2026-08-05, pre-registration numerics)

Definitional fork SETTLED at probe level (full report in session task
output; code in scratchpad probe_go14/):

- ADOPT definition (a): L_Delta = (1/n) sum_t I(T^n; Yhat_t |
  S^{t+Delta}, Yhat^{t-1}) -- the Delta-lagged causally-conditioned
  CMI. EXACT chain rule (residual 3e-12): n L_a = I(T^n;Yhat^n|S^n)
  + C_Delta, C_Delta >= 0 the smoothing-leakage charge
  sum_t I(Yhat_t; S_{>t+Delta} | past), = 0 iff the record is
  Delta-lag causally simulatable from S; decay pole identified:
  lambda_s = a(1-K), K the steady Kalman gain (ratio 7.95/lag
  measured = lambda_s^{-2}).
- REJECT definition (b) (memoryless eraser): monotone but floors
  0.0136 bits above the netted block coordinate (wrong
  Delta->infinity invariant; chain-rule-inconsistent).
- Interpolation conjecture SURVIVES: min L_a strictly inside
  (path 0.5350, slice 0.6219/0.7879/0.8490) at Delta = 0/2/5, D=0.3,
  n=16; strict monotonicity PROVABLE (per-term identity), lower
  margin collapses like lambda_s^{2 Delta}.
- Bookkeeping candidate REFUTED: fixed-lag static quadratic misses by
  a gap converging to the spectral gain 0.0263 bits -- record memory
  + cross-cell code structure carry real value.
- First-theorem draft (for the R-IND-5 + seal loop): the chain-rule
  identity + iff-condition + strict sandwich + geometric convergence
  at rate (a(1-K))^{2 Delta}; corollary: L_a is NOT the fixed-lag
  bookkeeping value, deficit -> spectral gain.
- Caveats on record: stationary-symmetric record class only (local
  certificates); finite-n drift quantified (n=8/16/24); Var(Y)=1
  normalization validated against the netted g* endpoint (1e-6), not
  assumed; Delta=5 strictness 2.7e-6 quoted as "strict,
  O(lambda_s^{2 Delta})", never as a numeric margin.

Next loop (when picked up): R-IND-5 verifier on the identity +
sandwich; GO-14 tex v0.2; seal GO-P-2026-076 (ID after 075); pilot;
governed. Novelty sweep owed for the causally-conditioned-CMI
framing (Kramer/Lev-Khina line mapped in GO-12 novelty record).
