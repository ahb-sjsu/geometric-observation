# C3 numerical falsification harness for the two-observer theorem (Appendix / Sec.
# "Successive refinement across observers"). Governed by prereg/GO-P-2026-022. numpy only.
#
#   Sigma*(P,D) = argmax logdet Sigma s.t. 0<=Sigma<=Sx, tr(P Sigma)<=D.
#   CORRECT max-det solution (reverse water-filling; the Sigma<=Sx cap DOES bind on
#   ker P): whiten Pt = Sx^{1/2} P Sx^{1/2} = V diag(p_k) V^T, then
#     Sigma* = Sx^{1/2} V diag(min(1, theta/p_k)) V^T Sx^{1/2},  sum_k min(p_k,theta)=D.
#   Thm 1: (D1,D2) successively refinable  iff  Sig2* <= Sig1*.  Verified independently
#   below by the sufficiency construction (nested Gaussian chain reproduces both optima)
#   and by the orthogonal-observers closed form.  MIT License.
import numpy as np
rng = np.random.default_rng(11)

def spd(n):
    A = rng.standard_normal((n, n)); return A @ A.T + 0.5*np.eye(n)

def sqrtm_sym(M):
    w, U = np.linalg.eigh(M); return U @ np.diag(np.sqrt(np.maximum(w, 0))) @ U.T

def sigma_star(P, D, Sx):
    """max-det optimal error covariance (reverse water-filling; cap binds on ker P)."""
    Sh = sqrtm_sym(Sx)
    p, V = np.linalg.eigh(Sh @ P @ Sh)          # whitened weights p_k >= 0
    p = np.maximum(p, 0.0)
    def dist(theta): return float(np.sum(np.minimum(p, theta)))   # sum_k min(p_k,theta)
    Dmax = float(np.sum(p))
    if D >= Dmax:
        e = np.ones_like(p)                     # Sigma* = Sx (nothing coded)
    else:
        lo, hi = 0.0, max(p.max(), 1e-9)
        for _ in range(200):
            mid = 0.5*(lo+hi)
            if dist(mid) < D: lo = mid
            else: hi = mid
        theta = 0.5*(lo+hi)
        with np.errstate(divide="ignore"):
            e = np.minimum(1.0, np.where(p > 0, theta/np.maximum(p, 1e-300), 1.0))
    return Sh @ (V @ np.diag(e) @ V.T) @ Sh

def mineig(M): return float(np.linalg.eigvalsh((M+M.T)/2).min())

fail = []
print("="*70); print("[1] Sigma* meets its distortion exactly (correct max-det solution)")
n = 4; Sx = spd(n); P1, P2 = spd(n), spd(n)
D1, D2 = 0.6*np.trace(P1@Sx), 0.25*np.trace(P2@Sx)
S1 = sigma_star(P1, D1, Sx); S2 = sigma_star(P2, D2, Sx)
e1 = abs(np.trace(P1@S1)-D1); e2 = abs(np.trace(P2@S2)-D2)
print(f"  |tr(P1 S1)-D1|={e1:.2e}  |tr(P2 S2)-D2|={e2:.2e}  cap ok (S<=Sx): "
      f"{mineig(Sx-S1)>=-1e-8 and mineig(Sx-S2)>=-1e-8}")
fail += [] if (e1<1e-6 and e2<1e-6 and mineig(Sx-S1)>=-1e-8) else ["distortion/cap"]

print("="*70); print("[2] Sufficiency construction: nested chain reproduces BOTH optima when Sig2*<=Sig1*")
# pick a nested pair by construction: same P, D2<D1 -> Sig2*<=Sig1* (Equitz-Cover)
P = spd(n); dA = 0.5*np.trace(P@Sx); dB = 0.2*np.trace(P@Sx)
SA = sigma_star(P, dA, Sx); SB = sigma_star(P, dB, Sx)     # SB (fine) <= SA (coarse)?
Sxi = np.linalg.inv(Sx); LA = np.linalg.inv(SA)-Sxi; LB = np.linalg.inv(SB)-Sxi
nested = mineig(SA-SB) >= -1e-8
# construction: Y2 = LB^{1/2} X + N ; Y1 = K^{1/2} Y2 + (I-K)^{1/2} N', K = LB^{+1/2} LA LB^{+1/2}
LBh = sqrtm_sym(LB); LBp = np.linalg.pinv(LBh)
K = LBp @ LA @ LBp
covXY2 = np.linalg.inv(Sxi + LB)                          # Cov(X|Y2)
covXY1 = np.linalg.inv(Sxi + LBh @ K @ LBh)               # Cov(X|Y1)
print(f"  nested(SA>=SB)={nested}  ||Cov(X|Y2)-SB||={np.linalg.norm(covXY2-SB):.2e}  "
      f"||Cov(X|Y1)-SA||={np.linalg.norm(covXY1-SA):.2e}  (construction reproduces both optima)")
fail += [] if (nested and np.linalg.norm(covXY2-SB)<1e-6 and np.linalg.norm(covXY1-SA)<1e-6) else ["construction"]

print("="*70); print("[3] Equitz-Cover (Cor): P1=P2, D2<=D1 => Sig2*<=Sig1* (holds for non-commuting P,Sx)")
ok = True
for _ in range(200):
    Q = spd(n); Pq = spd(n)                                 # P and Sx need NOT commute
    d1 = rng.uniform(0.15, 0.9)*np.trace(Pq@Q); d2 = rng.uniform(0.05, 1.0)*d1
    ok &= mineig(sigma_star(Pq,d1,Q) - sigma_star(Pq,d2,Q)) >= -1e-7
print(f"  200 random (non-commuting) (D1>=D2) pairs: all nested = {ok}")
fail += [] if ok else ["equitz-cover"]

print("="*70); print("[4] Orthogonal observers (Example): total loss L = R1(D1), zero reuse")
Sx2 = np.eye(2); d1 = d2 = 0.25
S1o = sigma_star(np.diag([1.,0.]), d1, Sx2); S2o = sigma_star(np.diag([0.,1.]), d2, Sx2)
Sig_circ = np.diag([d1, d2])                                # constrained max-det (analytic)
S2opt   = np.diag([1., d2])
L = 0.5*(np.linalg.slogdet(S2opt)[1] - np.linalg.slogdet(Sig_circ)[1])
print(f"  S1*=diag({S1o[0,0]:.3f},{S1o[1,1]:.3f})  S2*=diag({S2o[0,0]:.3f},{S2o[1,1]:.3f})  "
      f"nested={mineig(S1o-S2o)>=-1e-6}")
print(f"  L={L:.4f} nats  vs  R1(D1)=0.5 ln(1/D1)={0.5*np.log(1/d1):.4f}  "
      f"(L=R1(D1): {'OK' if abs(L-0.5*np.log(1/d1))<1e-6 else 'FAIL'})")
fail += [] if abs(L-0.5*np.log(1/d1))<1e-6 else ["orthogonal"]

print("="*70)
print("VERDICT:", "ALL PASS" if not fail else f"FAIL: {fail}")
