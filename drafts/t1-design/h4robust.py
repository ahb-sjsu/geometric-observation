# Design calculation for drafts/T1-WORKED-RESULT-REGISTRATION-DRAFT.md (2026-11-17): closed forms
# from the instance parameters only, no simulated data. Not a governed measurement.
import numpy as np
from math import comb
print("P(Bin(20,0.1)>=7) =", sum(comb(20,k)*0.1**k*0.9**(20-k) for k in range(7,21)))
Sig = np.diag([2.0, 0.5]); G = np.diag([4.0, 1.0]); S12 = np.sqrt(Sig)
def q(s2,b): return 1+2*b*np.exp(-s2/2)+(b*b/2)*(1+np.exp(-2*s2))
def design(W, R):
    # Gaussian rate-only design for weight W at rate R: water-fill on the whitened weight S^1/2 W S^1/2
    M = S12 @ W @ S12; w, U = np.linalg.eigh((M+M.T)/2)
    lo, hi = 1e-12, w.max()
    for _ in range(200):
        th = np.sqrt(lo*hi); r = sum(0.5*np.log2(x/th) for x in w if x > th)
        lo, hi = (th, hi) if r > R else (lo, th)
    # whitened error covariance X = U diag(min(1, th/w)) U^T ; Delta = S^1/2 X S^1/2
    X = U @ np.diag(np.minimum(1.0, th/np.maximum(w,1e-300))) @ U.T
    return S12 @ X @ S12
rng = np.random.default_rng(1)
for b in (0.0, 0.05, 0.2):
    Q = G @ np.diag([q(2.0,b), q(0.5,b)]); Q12 = np.sqrt(Q)
    d_rec = np.trace(Q @ design(np.eye(2), 2.0)); d_opt = np.trace(Q @ design(Q, 2.0))
    red0 = 1 - d_opt/d_rec; worst = red0
    for _ in range(20000):
        E = rng.standard_normal((2,2)); E = (E+E.T)/2; E *= 0.3/np.linalg.norm(E, 2) * rng.uniform(0,1)**0.25
        Qh = Q12 @ (np.eye(2)+E) @ Q12
        worst = min(worst, 1 - np.trace(Q @ design(Qh, 2.0))/d_rec)
    print(f"beta={b}: reduction at true Q {red0:.3f}; worst over ||E||<=0.3: {worst:.3f}; half of true: {red0/2:.3f}; holds: {worst >= red0/2}")
