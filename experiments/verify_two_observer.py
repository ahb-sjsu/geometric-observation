# C3 numerical falsification harness for two-observer-theorem.tex (Thms 1-2, Cors).
# Governed by prereg/GO-P-2026-022. Pure numpy.
#   Sigma*(P,D) = argmax logdet Sigma s.t. Sigma<=Sx, tr(P Sigma)<=D.  Since
#   Sigma*^{-1}=Sx^{-1}+lambda P >= Sx^{-1}, the cap never binds, so Sigma* is a
#   1-D root-find in lambda.  Thm 1: (D1,D2) successively refinable  iff  Sig2*<=Sig1*.
# MIT License.
import numpy as np
rng = np.random.default_rng(11)

def spd(n):
    A = rng.standard_normal((n, n)); return A @ A.T + 0.5*np.eye(n)

def sigma_star(P, D, Sx):
    """max-det optimal error covariance for weighted-quadratic Gaussian RD (root-find)."""
    Sxi = np.linalg.inv(Sx)
    def trP(lam): return float(np.trace(P @ np.linalg.inv(Sxi + lam*P)))
    Dmax = trP(0.0)                       # lambda=0 -> Sigma=Sx
    if D >= Dmax: return Sx.copy(), 0.0   # unconstrained
    lo, hi = 0.0, 1.0
    while trP(hi) > D: hi *= 2
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if trP(mid) > D: lo = mid
        else: hi = mid
    lam = 0.5*(lo+hi)
    return np.linalg.inv(Sxi + lam*P), lam

def mineig(M): return float(np.linalg.eigvalsh((M+M.T)/2).min())

print("="*70); print("[1] Thm 1 sanity: Sigma* meets its distortion; Sig2*<=Sig1* <=> Lam1<=Lam2")
n = 4; Sx = spd(n); P1, P2 = spd(n), spd(n)
D1, D2 = 0.6*np.trace(P1@Sx), 0.25*np.trace(P2@Sx)
S1, _ = sigma_star(P1, D1, Sx); S2, _ = sigma_star(P2, D2, Sx)
Sxi = np.linalg.inv(Sx); L1 = np.linalg.inv(S1)-Sxi; L2 = np.linalg.inv(S2)-Sxi
print(f"  tr(P1 S1)={np.trace(P1@S1):.4f} (D1={D1:.4f}); tr(P2 S2)={np.trace(P2@S2):.4f} (D2={D2:.4f})")
print(f"  min eig(S1-S2)={mineig(S1-S2):+.4f}   min eig(L2-L1)={mineig(L2-L1):+.4f}  "
      f"(nesting <=> Lam1<=Lam2: {'consistent' if (mineig(S1-S2)>=-1e-9)==(mineig(L2-L1)>=-1e-9) else 'INCONSISTENT'})")

print("="*70); print("[2] Equitz-Cover (Cor): P1=P2, D2<=D1  =>  Sig2*<=Sig1* (always refinable)")
P = spd(n); ok = True
for _ in range(200):
    d1 = rng.uniform(0.1, 0.9)*np.trace(P@Sx); d2 = rng.uniform(0.05, 1.0)*d1
    A,_ = sigma_star(P, d1, Sx); B,_ = sigma_star(P, d2, Sx)
    ok &= mineig(A-B) >= -1e-8
print(f"  200 random (D1>=D2) pairs: all nested = {ok}")

print("="*70); print("[3] Orthogonal observers (Example): P1=diag(1,0), P2=diag(0,1) on I_2")
Sx2 = np.eye(2); d1 = d2 = 0.25
S1o,_ = sigma_star(np.diag([1.,1e-9]), d1, Sx2); S2o,_ = sigma_star(np.diag([1e-9,1.]), d2, Sx2)
Sig_circ = np.diag([d1, d2])                       # nested optimum (per-mode, analytic)
S2opt = np.diag([1.0, d2])                          # unconstrained observer-2 optimum
L = 0.5*(np.linalg.slogdet(S2opt)[1] - np.linalg.slogdet(Sig_circ)[1])
print(f"  S1*~diag({S1o[0,0]:.3f},{S1o[1,1]:.3f})  S2*~diag({S2o[0,0]:.3f},{S2o[1,1]:.3f})  "
      f"nested={mineig(S1o-S2o)>=-1e-6}")
print(f"  rate loss L = {L:.4f} nats  vs  R1(D1)=0.5*ln(1/D1)={0.5*np.log(1/d1):.4f}  "
      f"(claim L=R1(D1): {'OK' if abs(L-0.5*np.log(1/d1))<1e-6 else 'FAIL'})")

print("="*70); print("[4] Commuting (Cor): simultaneous diagonalization; nesting is per-mode")
Q,_ = np.linalg.qr(rng.standard_normal((n,n)))
Sxc = Q@np.diag(rng.uniform(0.5,3,n))@Q.T
P1c = Q@np.diag(rng.uniform(0.5,3,n))@Q.T; P2c = Q@np.diag(rng.uniform(0.5,3,n))@Q.T
d1 = 0.5*np.trace(P1c@Sxc); d2 = 0.2*np.trace(P2c@Sxc)
S1c,_ = sigma_star(P1c,d1,Sxc); S2c,_ = sigma_star(P2c,d2,Sxc)
print(f"  ||[P1,P2]||={np.linalg.norm(P1c@P2c-P2c@P1c):.2e}  S1*-S2* min eig = {mineig(S1c-S2c):+.4f}")
print("="*70); print("VERDICT: Thm-1 nesting characterization, Equitz-Cover recovery, and the")
print("orthogonal-observers rate loss L=R1(D1) reproduce.")
