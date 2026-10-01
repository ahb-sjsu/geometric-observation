"""Checks for the general (weighted distortion, general side-information map) theorems, 2026-10-01.
Model: T ~ N(0, Sigma) in R^p, Y = F T (m coords), distortion E (Y-Yhat)^T W (Y-Yhat), Q = F^T W F.
Holder: S = H T + U, U ~ N(0, Sigma_U); J = H^T Sigma_U^{-1} H; K = Sigma_{T|S} = (Sigma^{-1} + J)^{-1}.
Description W_d = G T + N(0,I): P = Sigma_e0 = (Sigma^{-1} + G^T G)^{-1}; Sigma_e = (P^{-1} + J)^{-1}.
  rate r(P) = 1/2 log det Sigma/det P;  leakage l(P) = 1/2 log det K/det Sigma_e;  distortion tr(Q P).
G1 weighted pencil: best 1-D leakage = 1/2 log2(1 + Delta/mu_max), mu_max top root of det(Sigma Q Sigma - Delta Sigma - mu K)
G2 convexity of r and l in P (midpoint tests) and frontier uniqueness (multi-start agreement of weighted minimizers)
G3 general turning: read constant across Delta iff Q Sigma b = lam b and J Sigma b = kap b (common generalized eigvec)
G4 misalignment criterion in the 1-D regime: rate read b_R; J Sigma b_R parallel to b_R  <=>  b_R is a leakage-pencil eigvec
"""
import numpy as np, math
from scipy.optimize import minimize
LN2 = math.log(2); rng = np.random.default_rng(31)
fails = 0
def check(n, ok, info=""):
    global fails; print(("PASS " if ok else "FAIL ") + n + ("  " + info if info else "")); fails += (not ok)

def rand_spd(k, floor=0.1):
    A = rng.normal(size=(k, k)); return A @ A.T / k + floor * np.eye(k)

def model(m, r_extra, s_dim, h_touches_y=True):
    p = m + r_extra
    Sig = rand_spd(p, 0.2)
    Wm = rand_spd(m, 0.3)
    F = np.zeros((m, p)); F[:, :m] = np.eye(m)
    Q = F.T @ Wm @ F
    H = rng.normal(size=(s_dim, p))
    if not h_touches_y: H[:, :m] = 0
    SU = rand_spd(s_dim, 0.2)
    J = H.T @ np.linalg.inv(SU) @ H
    K = np.linalg.inv(np.linalg.inv(Sig) + J)
    return Sig, Q, J, K, F, Wm

def rate(P, Sig): return 0.5 * (np.linalg.slogdet(Sig)[1] - np.linalg.slogdet(P)[1]) / LN2
def leak(P, J, K): return 0.5 * (np.linalg.slogdet(K)[1] + np.linalg.slogdet(np.linalg.inv(P) + J)[1]) / LN2

def Pof(g, Sig):
    p = Sig.shape[0]; G = g.reshape(p, p); return np.linalg.inv(np.linalg.inv(Sig) + G.T @ G)

def brute(Sig, Q, J, K, D, alpha=0.0, starts=14):
    p = Sig.shape[0]; best = np.inf; Pb = None
    obj = lambda g: alpha * rate(Pof(g, Sig), Sig) + (1 - alpha) * leak(Pof(g, Sig), J, K)
    for _ in range(starts):
        res = minimize(obj, rng.normal(0, 1.5, p * p), method='SLSQP',
                       constraints=[{'type': 'ineq', 'fun': lambda g: D - np.trace(Q @ Pof(g, Sig))}],
                       options={'maxiter': 4000, 'ftol': 1e-13})
        if res.success and np.trace(Q @ Pof(res.x, Sig)) <= D + 1e-8 and res.fun < best:
            best, Pb = res.fun, Pof(res.x, Sig)
    return best, Pb

def pencil(Sig, Q, K, D):
    Delta = np.trace(Q @ Sig) - D
    A = Sig @ Q @ Sig - Delta * Sig
    w, U = np.linalg.eigh(K); Kih = U @ np.diag(w ** -0.5) @ U.T
    cw, cV = np.linalg.eigh(Kih @ A @ Kih)
    if cw[-1] <= 0: return None, None
    return 0.5 * math.log2(1 + Delta / cw[-1]), Kih @ cV[:, -1]

# G1: weighted pencil equals brute force whenever the brute-force optimum is rank one
ok = True; n1 = 0; worst = 0
for _ in range(12):
    m, re, sd = int(rng.integers(1, 3)), int(rng.integers(1, 3)), int(rng.integers(1, 3))
    Sig, Q, J, K, F, Wm = model(m, re, sd, h_touches_y=bool(rng.integers(0, 2)))
    lam_max = np.linalg.eigvalsh(np.linalg.cholesky(Wm).T @ (F @ Sig @ F.T) @ np.linalg.cholesky(Wm)).max()
    D = np.trace(Q @ Sig) - rng.uniform(0.05, 0.6) * lam_max
    pv, _ = pencil(Sig, Q, K, D)
    bv, Pb = brute(Sig, Q, J, K, D)
    Qv = np.sort(np.linalg.eigvalsh(np.linalg.inv(Pb) - np.linalg.inv(Sig)))[::-1]
    rank = int(np.sum(Qv > 1e-5 * Qv[0]))
    if pv is None: continue
    n1 += 1
    if rank == 1: worst = max(worst, abs(pv - bv)); ok = ok and abs(pv - bv) < 1e-5
    else: ok = ok and (pv >= bv - 1e-6)
check(f"G1 weighted pencil == optimum when rank one, >= optimum otherwise ({n1} cases, general H)", ok, f"max |diff| rank-one {worst:.2e}")

# G2 convexity of r and l in P (midpoint), on random feasible P pairs
viol = 0; tests = 0
for _ in range(40):
    Sig, Q, J, K, F, Wm = model(2, 2, 2)
    for _ in range(200):
        P0 = Pof(rng.normal(0, 1, 16), Sig); P1 = Pof(rng.normal(0, 1, 16), Sig); Pm = 0.5 * (P0 + P1)
        for f in (lambda P: rate(P, Sig), lambda P: leak(P, J, K)):
            tests += 1
            if f(Pm) > 0.5 * (f(P0) + f(P1)) + 1e-10: viol += 1
check(f"G2 rate and leakage convex in Sigma_e0 (midpoint, {tests} tests)", viol == 0, f"violations {viol}")
# frontier uniqueness: weighted minimizers from many starts agree
ok = True
for _ in range(6):
    Sig, Q, J, K, F, Wm = model(2, 1, 1)
    D = 0.5 * np.trace(Q @ Sig); alpha = rng.uniform(0.1, 0.9)
    vals = []; Ps = []
    for _ in range(5):
        v, P = brute(Sig, Q, J, K, D, alpha=alpha, starts=3); vals.append(v); Ps.append(P)
    spread = max(vals) - min(vals); pspread = max(np.linalg.norm(P - Ps[0]) for P in Ps)
    ok = ok and spread < 1e-6 and pspread < 1e-3
check("G2b weighted frontier minimizer unique across starts (6 cases)", ok)

# G3 general turning. (i) aligned construction: common eigvec -> read constant; (ii) generic -> read turns
def read_angle_track(Sig, Q, K, Ds):
    bs = []
    for D in Ds:
        _, b = pencil(Sig, Q, K, D)
        bs.append(b / np.linalg.norm(b) * np.sign(b[np.argmax(np.abs(b))]))
    return max(np.linalg.norm(bs[i] - bs[0]) for i in range(len(bs)))
# (i) aligned: Sigma block diagonal with an uncontacted principal Y-axis having the largest weighted variance
p = 3
Sig = np.diag([2.0, 1.0, 1.0]); Sig[1, 2] = Sig[2, 1] = 0.6
F = np.zeros((2, 3)); F[:, :2] = np.eye(2); Wm = np.diag([1.0, 0.5]); Q = F.T @ Wm @ F
H = np.array([[0.0, 0.0, 1.0]]); J = H.T @ H / 0.1; K = np.linalg.inv(np.linalg.inv(Sig) + J)
b0 = np.array([1.0, 0, 0])
cond = (np.linalg.norm(np.cross(Q @ Sig @ b0, b0)) < 1e-12) and (np.linalg.norm(J @ Sig @ b0) < 1e-12)
lam_max = np.linalg.eigvalsh(np.sqrt(Wm) @ (F @ Sig @ F.T) @ np.sqrt(Wm)).max()
Ds = [np.trace(Q @ Sig) - t * lam_max for t in (0.05, 0.2, 0.4)]
drift_aligned = read_angle_track(Sig, Q, K, Ds)
check("G3a aligned (common eigvec) read is constant across budgets", cond and drift_aligned < 1e-9, f"drift {drift_aligned:.1e}")
# (ii) generic: condition fails -> read moves
Sig, Q, J, K, F, Wm = model(2, 1, 1)
lam_max = np.linalg.eigvalsh(np.linalg.cholesky(Wm).T @ (F @ Sig @ F.T) @ np.linalg.cholesky(Wm)).max()
Ds = [np.trace(Q @ Sig) - t * lam_max for t in (0.05, 0.2, 0.4)]
drift_generic = read_angle_track(Sig, Q, K, Ds)
check("G3b generic source: read moves with the budget", drift_generic > 1e-3, f"drift {drift_generic:.3f}")
# (iii) eigenvalue formula for an aligned b: (lam - Delta)(1 + kap)
Sig = np.diag([2.0, 1.0, 1.0]); Sig[1, 2] = Sig[2, 1] = 0.6
F = np.zeros((2, 3)); F[:, :2] = np.eye(2); Wm = np.diag([1.0, 0.5]); Q = F.T @ Wm @ F  # reset Q (the generic block overwrote it)
H = np.array([[1.0, 0.0, 0.0]]); J = H.T @ H / 0.5; K = np.linalg.inv(np.linalg.inv(Sig) + J)  # holder sees the aligned axis itself
b0 = np.array([1.0, 0, 0]); lam = (Q @ Sig @ b0)[0]; kap = (J @ Sig @ b0)[0]
Delta = 0.3; A = Sig @ Q @ Sig - Delta * Sig
resid = np.linalg.norm(A @ b0 - (lam - Delta) * (1 + kap) * (K @ b0))
check("G3c common eigvec has pencil eigenvalue (lam-Delta)(1+kap), holder touching the axis", resid < 1e-12, f"resid {resid:.1e}")

# G4 misalignment criterion: b_R = top generalized eigvec of (Sigma Q Sigma, Sigma)
ok = True
for trial in range(20):
    Sig, Q, J, K, F, Wm = model(2, 1, 1, h_touches_y=bool(trial % 2))
    w, U = np.linalg.eigh(Sig); Sih = U @ np.diag(w ** -0.5) @ U.T
    cw, cV = np.linalg.eigh(Sih @ Sig @ Q @ Sig @ Sih); bR = Sih @ cV[:, -1]
    par = np.linalg.norm(np.cross(J @ Sig @ bR, bR)) / (np.linalg.norm(J @ Sig @ bR) * np.linalg.norm(bR) + 1e-300) if np.linalg.norm(J @ Sig @ bR) > 1e-12 else 0.0
    Delta = 0.3 * cw[-1]; A = Sig @ Q @ Sig - Delta * Sig
    # is bR a generalized eigvec of (A, K)?
    x = A @ bR; y = K @ bR; ge = np.linalg.norm(x - (x @ y) / (y @ y) * y) / np.linalg.norm(x)
    ok = ok and ((par < 1e-9) == (ge < 1e-9))
check("G4 J Sigma b_R parallel to b_R  <=>  b_R is an eigvec of the leakage pencil (20 cases)", ok)
print("FAILS:", fails)
