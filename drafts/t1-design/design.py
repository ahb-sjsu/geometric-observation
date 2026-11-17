# Design calculation for drafts/T1-WORKED-RESULT-REGISTRATION-DRAFT.md (2026-11-17): closed forms
# from the instance parameters only, no simulated data. Not a governed measurement.
import numpy as np
L = np.log(40.0)                      # ln(2p/delta), p=2, delta=0.1
Sig = np.diag([2.0, 0.5]); G = np.diag([4.0, 1.0])
def q(s2, b): return 1 + 2*b*np.exp(-s2/2) + (b*b/2)*(1 + np.exp(-2*s2))
def wf_dist(lams, R):                 # reverse water-filling: distortion per component at total rate R (bits) over the eigen-variances lams
    lo, hi = 1e-12, max(lams)
    for _ in range(200):
        th = np.sqrt(lo*hi)
        r = sum(0.5*np.log2(l/th) for l in lams if l > th)
        lo, hi = (th, hi) if r > R else (lo, th)
    return np.minimum(lams, th)
for b in (0.0, 0.05, 0.2):
    qs = np.array([q(2.0, b), q(0.5, b)]); Q = G @ np.diag(qs)
    num = 1 - min((1-b)**2/qs); nup = max((1+b)**2/qs) - 1; nu = max(num, nup)
    print(f"beta={b}: q={qs.round(4)}, nu-={num:.3f} nu+={nup:.3f}, looseness part of tau (p=2) = {np.log2((1+nup)/(1-num)):.3f} bits")
    for m in (8, 32, 128, 512):
        e = nu*(np.sqrt(2*L/m) + 2*L/(3*m)); tau = np.log2((1+nup)*(1+e)/((1-num)*(1-e))) if e < 1 else float('nan')
        print(f"   m={m:4d}: eps_m={e:.3f}, tau={tau:.3f} bits/symbol")
    # H4 at the rate-only slice: consumer-weighted distortion tr(Q Delta) of the Q-design vs the reconstruction (Q=I) design at matched rate
    W = np.sqrt(Sig) @ Q @ np.sqrt(Sig)           # whitened weight (diagonal here)
    for R in (1.0, 2.0):
        d_q = wf_dist(np.diag(W), R).sum()        # consumer distortion of the Q-design: water-filling on the whitened weight
        dr = wf_dist(np.diag(Sig), R)             # reconstruction design: water-filling on Sigma
        d_r = float(np.diag(Q) @ dr)
        print(f"   R={R}: consumer distortion Q-design {d_q:.4f} vs reconstruction {d_r:.4f}: reduction {1-d_q/d_r:.1%}")
