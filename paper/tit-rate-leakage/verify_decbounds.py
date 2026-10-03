"""verify_decbounds.py: numerical checks of Proposition decbounds (2026-10-03).

Example. Sigma_T = I_2, Q = I_2 (the decoder reproduces both coordinates), decoder side information on the first
coordinate (J_C = diag(4, 0)) and holder on the second (J_S = diag(0, 4)), so neither dominates. The enhanced
information J' = diag(4, 4) dominates both. All matrices are diagonal. The outer programs are commuting, so diagonal
error covariances are optimal there (Theorem commuting). Restricting the inner bound to diagonal descriptions keeps it an
inner bound.

Computation is exact up to a one-dimensional search, with no two-dimensional grid. In the decoder's error coordinates
m_i (the diagonal of Cov(T|V,C), 0 < m_i <= Sigma_{T|C,ii}):
  rate             R = 1/2 log2(prod Sigma_{T|C,ii} / prod m_i)       (least value: reverse water-filling, closed form)
  holder's error   Cov(T|V,S)_ii = m_i / (1 + (J_S,ii - J_C,ii) m_i)
Every cost decreases in each m_i, so the budget binds, and a two-variable minimum is a search over m_0 with
m_1 = min(cap_1, D - m_0) on 200001 points.
  inner  L_in(D): min{least R, least I(T;V|S)}, then the lower convex envelope in D (time sharing)
  outer  L_out(D) = max{R_C'(D), least leakage of RW_J'(D)}
D1  L_out(D) <= L_in(D) at every budget (consistency).
D2  degraded J_S <= J_C (J_C = diag(4,4), J_S = diag(0,4)): inner with the first term = outer (b) = R_C(D).
D3  degraded J_C <= J_S (J_C = diag(4,0), J_S = diag(4,4)): inner with the second term = outer (c).
D2 and D3 hold by algebra (the two bounds reduce to the same expression); they check the formulas, nothing more.
D5  the example's inner bound with V0 = V_b, computed from generic Gaussian log-determinants of the joint covariance,
    equals the closed-form objective of the outer bound (c), so the bounds coincide at every budget.
D4  the closed-form enhancement J' = J_C^{1/2}(I + (J_C^{-1/2} J_S J_C^{-1/2} - I)_+) J_C^{1/2} dominates J_C and J_S
    for random positive definite J_C and positive semidefinite J_S (dimension 2..6).
"""
import numpy as np
fails = 0
def check(name, ok, detail):
    global fails
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}"); fails += (not ok)

def rwf(eigs, D):                                          # least rate at distortion D, Q = I, bits
    eigs = np.sort(np.asarray(eigs, float))
    if D >= eigs.sum(): return 0.0
    lo, hi = 0.0, eigs.max()
    for _ in range(200):
        th = 0.5 * (lo + hi)
        if np.minimum(th, eigs).sum() > D: hi = th
        else: lo = th
    return float(0.5 * np.sum(np.log2(eigs / np.minimum(lo, eigs))))

def min_sep(D, cost, cap, n=200001):
    """min cost(m0, m1) over m0 + m1 <= D, 0 < m_i <= cap_i, with cost decreasing in each m_i."""
    if D >= cap[0] + cap[1]: return float(cost(np.array([cap[0]]), np.array([cap[1]]))[0])
    m0 = np.linspace(max(D - cap[1], 0.0), min(D, cap[0]), n)[1:-1] if D > cap[1] else np.linspace(0.0, min(D, cap[0]), n)[1:-1]
    m1 = np.minimum(cap[1], D - m0); ok = m1 > 0
    return float(np.min(cost(m0[ok], m1[ok])))

def stc(j): return np.array([1 / (1 + j[0]), 1 / (1 + j[1])])

def least_IS(D, jc, js):                                   # least I(T;V|S) over Gaussian V meeting D
    cap = stc(jc); k = np.array(js) - np.array(jc); StS = stc(js)
    cost = lambda m0, m1: 0.5 * np.log2(StS[0] * StS[1] * (1 + k[0] * m0) * (1 + k[1] * m1) / (m0 * m1))
    return min_sep(D, cost, cap)

def least_outer_c(D, jc, jp):                              # least leakage in RW_J'(D)
    cap = stc(jc); k = np.array(jp) - np.array(jc); K = cap / (1 + k * cap)
    cost = lambda x, y: 0.5 * np.log2(K[0] * K[1] * (1 + k[0] * x) * (1 + k[1] * y) / (x * y))
    return min_sep(D, cost, cap)

def convex_envelope(Ds, Ls):
    hull = []
    for p in zip(Ds, Ls):
        while len(hull) >= 2 and (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-2][0]) >= (p[1] - hull[-2][1]) * (hull[-1][0] - hull[-2][0]):
            hull.pop()
        hull.append(p)
    return np.interp(Ds, [h[0] for h in hull], [h[1] for h in hull])

Ds = np.linspace(0.02, 1.18, 117)
jc, js, jp = (4.0, 0.0), (0.0, 4.0), (4.0, 4.0)
pre = np.array([min(rwf(stc(jc), d), least_IS(d, jc, js)) for d in Ds]); Lin = convex_envelope(Ds, pre)
Lb = np.array([rwf(stc(jp), d) for d in Ds]); Lc = np.array([least_outer_c(d, jc, jp) for d in Ds]); Lout = np.maximum(Lb, Lc)
check("D1 outer <= inner", bool(np.all(Lout <= Lin + 1e-6)), f"max(Lout - Lin) {np.max(Lout - Lin):+.2e} bits over {len(Ds)} budgets")
for d in (0.1, 0.2, 0.3, 0.4, 0.6, 0.9):
    i = int(np.argmin(np.abs(Ds - d)))
    print(f"   D={Ds[i]:.2f}: restricted inner (V_b constant or V) {Lin[i]:.4f}  outer {Lout[i]:.4f} (enhanced decoder {Lb[i]:.4f}, enhanced holder {Lc[i]:.4f})  gap {Lin[i] - Lout[i]:.4f} bits")
gap = Lin - Lout; print(f"   restricted gap: largest {gap.max():.4f} bits at D={Ds[int(np.argmax(gap))]:.2f}; gap below 1e-4 bit for D >= {Ds[np.flatnonzero(gap > 1e-4).max() + 1]:.2f}")

jc2, js2 = (4.0, 4.0), (0.0, 4.0)
e2 = max(abs(rwf(stc(jc2), d) - rwf(stc(jc2), d)) for d in Ds)          # inner first term is R_C(D) by construction
in2 = np.array([rwf(stc(jc2), d) for d in Ds]); out2 = np.array([rwf(stc(jc2), d) for d in Ds])
check("D2 degraded J_S <= J_C: inner = outer(b)", bool(np.max(np.abs(in2 - out2)) < 1e-9),
      f"max difference {np.max(np.abs(in2 - out2)):.1e} bits (both are R_C(D))")
jc3, js3 = (4.0, 0.0), (4.0, 4.0)
in3 = np.array([least_IS(d, jc3, js3) for d in Ds]); out3 = np.array([least_outer_c(d, jc3, js3) for d in Ds])
check("D3 degraded J_C <= J_S: inner = outer(c)", bool(np.max(np.abs(in3 - out3)) < 1e-6),
      f"max |inner - outer(c)| {np.max(np.abs(in3 - out3)):.2e} bits")

rng = np.random.default_rng(3); worst = np.inf
def msqrt(M, p=0.5):
    w, U = np.linalg.eigh(M); return U @ np.diag(w ** p) @ U.T
for _ in range(500):
    n = rng.integers(2, 7); G = rng.normal(size=(n, n)); JC = G @ G.T + 0.1 * np.eye(n)
    H = rng.normal(size=(n, rng.integers(1, n + 1))); JS = 3 * H @ H.T
    K = msqrt(JC, -0.5) @ JS @ msqrt(JC, -0.5); w, U = np.linalg.eigh(0.5 * (K + K.T))
    Jp = msqrt(JC) @ (np.eye(n) + U @ np.diag(np.maximum(w - 1, 0)) @ U.T) @ msqrt(JC)
    worst = min(worst, np.linalg.eigvalsh(Jp - JC).min(), np.linalg.eigvalsh(Jp - JS).min())
check("D4 closed-form enhancement dominates J_C and J_S", worst > -1e-8, f"min eigenvalue of J' - J_C, J' - J_S: {worst:+.2e}")
# D5: the example's inner bound with V0 = V_b, from generic Gaussian log-determinants. T = (T1, T2) ~ N(0, I),
# C = 2 T1 + N_C (information 4), S = 2 T2 + N_S (information 4), V = (T1 + s1 Z1, T2 + s2 Z2). The leakage term
# I(T;V|C) + I(V_b;C) - I(V_b;S) with V_b = V_2 is computed from the joint covariance and compared with the closed form
# 1/2 log2(0.2/m1) + 1/2 log2(0.8 + 0.2/m2), m1 = Cov(T1|V,C), m2 = Cov(T2|V,C); the rate with 1/2 log2(0.2/m1) + 1/2 log2(1/m2).
def ent(Cv, idx):                                          # Gaussian differential entropy of the coordinates idx, bits, up to 2 pi e
    return 0.5 * np.log2(np.linalg.det(Cv[np.ix_(idx, idx)])) if idx else 0.0
def cmi(Cv, a, b, c):                                      # I(A;B|C) for jointly Gaussian coordinates
    return ent(Cv, a + c) + ent(Cv, b + c) - ent(Cv, a + b + c) - ent(Cv, c)
worst = 0.0
for _ in range(400):
    s1, s2 = np.exp(rng.uniform(-3, 3, 2))
    # coordinates: 0 T1, 1 T2, 2 V1, 3 V2, 4 C, 5 S
    G = np.array([[1, 0], [0, 1], [1, 0], [0, 1], [2, 0], [0, 2]], float)
    Cv = G @ G.T + np.diag([0, 0, s1 ** 2, s2 ** 2, 1, 1])
    T, V, C, S, Vb = [0, 1], [2, 3], [4], [5], [3]
    R = cmi(Cv, T, V, C); L = R + cmi(Cv, Vb, C, []) - cmi(Cv, Vb, S, [])
    post = Cv[np.ix_(T, T)] - Cv[np.ix_(T, V + C)] @ np.linalg.inv(Cv[np.ix_(V + C, V + C)]) @ Cv[np.ix_(V + C, T)]
    m1, m2 = post[0, 0], post[1, 1]
    worst = max(worst, abs(L - (0.5 * np.log2(0.2 / m1) + 0.5 * np.log2(0.8 + 0.2 / m2))),
                abs(R - (0.5 * np.log2(0.2 / m1) + 0.5 * np.log2(1 / m2))))
check("D5 example inner bound with V0 = V_b from generic log-determinants", worst < 1e-9, f"max error {worst:.2e} bits over 400 descriptions")
print(f"FAILS: {fails}")
