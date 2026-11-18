"""Independent referee numerics for Theorem 6 of the T1 note v3.

E loss of the Gaussian test channel is computed two ways: forward form That=(I-B)T+V and
backward form T = That + Z (Z indep of That), by tensor Gauss-Hermite quadrature.
Compares with tr(Q Delta), with the note's rho, with a backward-channel bound rho_b
(auditor's), and with the exact second-order coefficient
   c2(Delta) = E sum_i [ 1/4 (tr H_i Delta)^2 - 1/2 tr(H_i Delta H_i Delta) ],
H_i the Hessians of the components of G^{1/2} C (auditor's derivation).
M_j and omega are estimated by sup over grids (lower estimates -> stringent test of validity)."""
import itertools
import numpy as np

out = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

def gh(n):
    x, w = np.polynomial.hermite_e.hermegauss(n); return x, w/w.sum()

def msqrt(A):
    w, V = np.linalg.eigh((A+A.T)/2); return (V*np.sqrt(np.clip(w, 0, None))) @ V.T

def rho_note(M1, M2, M3, om, s, th):
    return (om*th + M1*M2*(3*th**0.5*s + 3**0.75*th**1.5) + (0.75*M2**2 + M1*M3)*s**2
            + np.sqrt(5)/2*M2*M3*s**2.5 + 5/12*M3**2*s**3)

def rho_back(M1, M2, M3, s):
    return ((1.75*M2**2 + 2*M1*M3)*s**2 + np.sqrt(5)/2*M2*M3*s**2.5 + 5/12*M3**2*s**3)

# ------------------------------------------------------------------ 1-D consumers (G = 1)
# each: f, f1, f2, f3 (vectorized); M1,M2,M3 from grid sup
def cons1d():
    L = []
    L.append(("circle", lambda x: np.stack([np.cos(x), np.sin(x)], -1),
              lambda x: np.stack([-np.sin(x), np.cos(x)], -1),
              lambda x: np.stack([-np.cos(x), -np.sin(x)], -1),
              lambda x: np.stack([np.sin(x), -np.cos(x)], -1)))
    for k in (0.5, 1.0, 3.0):
        L.append((f"sin({k}x)/{k}", lambda x, k=k: (np.sin(k*x)/k)[..., None],
                  lambda x, k=k: np.cos(k*x)[..., None], lambda x, k=k: (-k*np.sin(k*x))[..., None],
                  lambda x, k=k: (-k*k*np.cos(k*x))[..., None]))
    for (b, k) in ((0.2, 1.0), (0.5, 1.0), (0.3, 3.0)):
        L.append((f"x+{b}sin({k}x)", lambda x, b=b, k=k: (x + b*np.sin(k*x))[..., None],
                  lambda x, b=b, k=k: (1 + b*k*np.cos(k*x))[..., None],
                  lambda x, b=b, k=k: (-b*k*k*np.sin(k*x))[..., None],
                  lambda x, b=b, k=k: (-b*k**3*np.cos(k*x))[..., None]))
    for wd in (0.3, 1.0, 3.0):
        t = lambda x, wd=wd: np.tanh(x/wd)
        L.append((f"{wd}tanh(x/{wd})", lambda x, wd=wd: (wd*np.tanh(x/wd))[..., None],
                  lambda x, wd=wd: (1/np.cosh(x/wd)**2)[..., None],
                  lambda x, wd=wd: (-2*np.tanh(x/wd)/np.cosh(x/wd)**2/wd)[..., None],
                  lambda x, wd=wd: ((-2/np.cosh(x/wd)**4 + 4*np.tanh(x/wd)**2/np.cosh(x/wd)**2)/wd**2)[..., None]))
    for (g, wd) in ((3.0, 1.0), (8.0, 0.5), (1.0, 2.0)):   # slope grows in the tails
        L.append((f"x+{g}(x-{wd}tanh(x/{wd}))",
                  lambda x, g=g, wd=wd: (x + g*(x - wd*np.tanh(x/wd)))[..., None],
                  lambda x, g=g, wd=wd: (1 + g*np.tanh(x/wd)**2)[..., None],
                  lambda x, g=g, wd=wd: (2*g*np.tanh(x/wd)/np.cosh(x/wd)**2/wd)[..., None],
                  lambda x, g=g, wd=wd: (g*(2/np.cosh(x/wd)**4 - 4*np.tanh(x/wd)**2/np.cosh(x/wd)**2)/wd**2)[..., None]))
    for wd in (0.5, 2.0):   # bump: read metric concentrated away from 0, vanishes at 0 and infinity
        L.append((f"bump{wd}", lambda x, wd=wd: (wd*np.exp(-x**2/(2*wd*wd)))[..., None],
                  lambda x, wd=wd: (-(x/wd)*np.exp(-x**2/(2*wd*wd)))[..., None],
                  lambda x, wd=wd: (((x/wd)**2 - 1)/wd*np.exp(-x**2/(2*wd*wd)))[..., None],
                  lambda x, wd=wd: ((3*(x/wd) - (x/wd)**3)/wd**2*np.exp(-x**2/(2*wd*wd)))[..., None]))
    return L

xg = np.linspace(-60, 60, 1200001)
x1, w1 = gh(160)
x1b, w1b = gh(260)
worst_note = worst_back = np.inf; viol = []
rows = []
for name, f, f1, f2, f3 in cons1d():
    M1 = np.sqrt((f1(xg)**2).sum(-1)).max(); M2 = np.sqrt((f2(xg)**2).sum(-1)).max()
    M3 = np.sqrt((f3(xg)**2).sum(-1)).max()
    for s2 in (0.05, 0.5, 2.0, 10.0):
        sig = np.sqrt(s2)
        P = lambda x: (f1(x)**2).sum(-1)
        Q = np.sum(w1*P(sig*x1))
        om = np.abs(P(xg) - Q).max()
        EC2 = np.sum(w1*(f2(sig*x1)**2).sum(-1))
        for frac in (1.0, 0.5, 0.1, 0.02, 0.004):
            Dl = frac*s2
            # backward: That ~ N(0, s2 - Dl), Z ~ N(0, Dl)
            Th = np.sqrt(max(s2 - Dl, 0))*x1[:, None]; Z = np.sqrt(Dl)*x1[None, :]
            l = ((f(Th + Z) - f(Th))**2).sum(-1)
            El_b = np.einsum("i,j,ij->", w1, w1, l)
            Thb = np.sqrt(max(s2 - Dl, 0))*x1b[:, None]; Zb = np.sqrt(Dl)*x1b[None, :]
            El_b2 = np.einsum("i,j,ij->", w1b, w1b, ((f(Thb + Zb) - f(Thb))**2).sum(-1))
            Q2 = np.sum(w1b*P(sig*x1b))
            if abs((El_b2 - Q2*Dl) - (El_b - Q*Dl)) > 1e-3*abs(El_b2 - Q2*Dl) + 1e-14:
                continue  # quadrature not converged for this case; skip
            # forward: That = (1 - Dl/s2) T + V
            T = sig*x1[:, None]; V = np.sqrt(max(Dl - Dl*Dl/s2, 0))*x1[None, :]
            l2 = ((f((1 - Dl/s2)*T + V) - f(T))**2).sum(-1)
            El_f = np.einsum("i,j,ij->", w1, w1, l2)
            exc = El_b - Q*Dl
            th = Dl*Dl/s2
            rn = rho_note(M1, M2, M3, om, Dl, th); rb = rho_back(M1, M2, M3, Dl)
            c2 = -0.25*EC2*Dl*Dl
            rows.append((name, s2, frac, El_b, El_f, exc, c2, rn, rb))
            if abs(exc) > 1e-13:
                worst_note = min(worst_note, rn/abs(exc)); worst_back = min(worst_back, rb/abs(exc))
            if abs(exc) > rn*(1+1e-9) + 1e-13: viol.append(("note", name, s2, frac, exc, rn))
            if abs(exc) > rb*(1+1e-9) + 1e-13: viol.append(("back", name, s2, frac, exc, rb))
fb = max(abs(r[3]-r[4])/max(r[3], 1e-300) for r in rows)
say(f"1-D: {len(rows)} converged cases (of 340); max rel |E_back - E_fwd| = {fb:.2e} (forward form = backward channel)")
say(f"1-D: min rho_note/|excess| = {worst_note:.3f}; min rho_back/|excess| = {worst_back:.3f}; violations: {viol[:5]}")
# second-order coefficient check: excess/c2 at the smallest frac
sm = [(r[0], r[1], r[5]/r[6]) for r in rows if r[2] == 0.004 and abs(r[6]) > 1e-14]
say("1-D: excess / (-(1/4) E C''^2 Delta^2) at Delta = 0.004 Sigma: range [%.3f, %.3f]" % (min(x[2] for x in sm), max(x[2] for x in sm)))
# where is rho_note relatively tightest
best = sorted([r for r in rows if abs(r[5]) > 1e-13], key=lambda r: r[7]/abs(r[5]))[:6]
for r in best:
    say("   tightest(note): %-22s s2=%5.2f frac=%5.3f excess=% .3e rho_note=%.3e ratio=%.2f rho_back=%.3e" % (r[0], r[1], r[2], r[5], r[7], r[7]/abs(r[5]), r[8]))
best = sorted([r for r in rows if abs(r[5]) > 1e-13], key=lambda r: r[8]/abs(r[5]))[:4]
for r in best:
    say("   tightest(back): %-22s s2=%5.2f frac=%5.3f excess=% .3e rho_back=%.3e ratio=%.2f" % (r[0], r[1], r[2], r[5], r[8], r[8]/abs(r[5])))
# cases where rho_back beats rho_note and vice versa
nb = sum(1 for r in rows if r[8] < r[7]); say(f"1-D: rho_back < rho_note in {nb}/{len(rows)} cases")

# ------------------------------------------------------------------ 2-D / 3-D consumers, correlated Sigma
def sm_derivs(z, c):
    e = np.exp(z - z.max(-1, keepdims=True)); s = e/e.sum(-1, keepdims=True)
    mu = (s*c).sum(-1, keepdims=True); d = c - mu
    k2 = (s*d*d).sum(-1, keepdims=True); k3 = (s*d**3).sum(-1, keepdims=True)
    return s, s*d, s*(d*d - k2), s*(d**3 - 3*k2*d - k3)

rng = np.random.default_rng(7)
Wb = np.random.default_rng(20261117).standard_normal((3, 2)); Wb /= np.linalg.norm(Wb, 2)
def mk_softmax(Wm, scale):
    Wm = scale*Wm
    def f(X): return sm_derivs(X @ Wm.T, np.zeros(X.shape[:-1] + (Wm.shape[0],)))[0]
    def dirj(X, h, j): return sm_derivs(X @ Wm.T, np.broadcast_to(np.asarray(h) @ Wm.T, X.shape[:-1] + (Wm.shape[0],)))[j]
    return f, dirj, np.eye(Wm.shape[0])
def mk_sinmix(A, B, beta, Gm):
    def f(X): return X @ np.eye(X.shape[-1]).T[:A.shape[0]].T if False else X + beta*np.sin(X @ B.T) @ A.T
    def dirj(X, h, j):
        Z = X @ B.T; c = np.asarray(h) @ B.T
        if j == 1: return h + beta*(np.cos(Z)*c) @ A.T
        if j == 2: return beta*(-np.sin(Z)*c**2) @ A.T
        if j == 3: return beta*(-np.cos(Z)*c**3) @ A.T
    return f, dirj, Gm
def mk_cossum(p):
    # C(x) = sum_j cos(x_j), scalar output: isotropic curvature -> positive second-order excess for p >= 3
    def f(X): return np.cos(X).sum(-1, keepdims=True)
    def dirj(X, h, j):
        if j == 1: return (-np.sin(X)*h).sum(-1, keepdims=True)
        if j == 2: return (-np.cos(X)*h**2).sum(-1, keepdims=True)
        if j == 3: return (np.sin(X)*h**3).sum(-1, keepdims=True)
    return f, dirj, np.eye(1)

def sup_norms(dirj, Gm, p, box, n=60000):
    X = rng.uniform(-box, box, (n, p)); H = rng.standard_normal((n, p)); H /= np.linalg.norm(H, axis=1, keepdims=True)
    G12 = msqrt(Gm); Ms = []
    for j in (1, 2, 3):
        v = dirj(X, H, j) @ G12.T if False else np.einsum("kl,nl->nk", G12, dirj(X, H, j))
        Ms.append(np.linalg.norm(v, axis=1).max())
    return Ms

def jac(dirj, X, p):
    return np.stack([dirj(X, np.eye(p)[a], 1) for a in range(p)], -1)  # (..., k, p)

def run_multi(name, f, dirj, Gm, Sig, n_gh, deltas):
    p = Sig.shape[0]
    M1, M2, M3 = sup_norms(dirj, Gm, p, box=8*np.sqrt(np.linalg.eigvalsh(Sig).max()))
    x, w = gh(n_gh)
    idx = np.array(list(itertools.product(range(n_gh), repeat=p)))
    zT, wT = x[idx], np.prod(w[idx], 1)
    S12 = msqrt(Sig); T = zT @ S12.T
    Jt = jac(dirj, T, p); P = np.einsum("nkp,kl,nlq->npq", Jt, Gm, Jt); Q = np.einsum("n,npq->pq", wT, P)
    Xg = rng.uniform(-8, 8, (40000, p)) @ S12.T
    Jg = jac(dirj, Xg, p); Pg = np.einsum("nkp,kl,nlq->npq", Jg, Gm, Jg)
    om = max(np.linalg.norm(Pg - Q, ord=2, axis=(1, 2)).max(), 0)
    # Hessians for c2: H_i[a,b] via polarization of dirj(.,.,2)
    E = np.eye(p); G12 = msqrt(Gm)
    Hd = {}
    for a in range(p):
        for b in range(p):
            Hd[a, b] = 0.25*(dirj(T, E[a]+E[b], 2) - dirj(T, E[a]-E[b], 2))
    Hm = np.einsum("kl,nlab->nkab", G12, np.stack([np.stack([Hd[a, b] for b in range(p)], -1) for a in range(p)], -2))
    res = []
    for Dl in deltas:
        s = np.trace(Dl); th = np.trace(Dl @ np.linalg.solve(Sig, Dl))
        # backward: That ~ N(0, Sig - Dl) on the T-grid, Z ~ N(0, Dl) on the same 1-D nodes
        A = msqrt(Sig - Dl); Bz = msqrt(Dl)
        nz = n_gh
        idz = np.array(list(itertools.product(range(nz), repeat=p))); zz, wz = x[idz], np.prod(w[idz], 1)
        Th = zT @ A.T; Zs = zz @ Bz.T
        El = 0.0
        for i0 in range(0, len(Th), 2000):
            th_blk = Th[i0:i0+2000]
            d = f(th_blk[:, None, :] + Zs[None]) - f(th_blk)[:, None, :]
            El += np.einsum("i,j,ijk,kl,ijl->", wT[i0:i0+2000], wz, d, Gm, d)
        exc = El - np.trace(Q @ Dl)
        HD = np.einsum("nkab,bc->nkac", Hm, Dl)
        c2 = np.einsum("n,nk->", wT, 0.25*np.einsum("nkaa->nk", HD)**2 - 0.5*np.einsum("nkab,nkba->nk", HD, HD))
        rn = rho_note(M1, M2, M3, om, s, th); rb = rho_back(M1, M2, M3, s)
        res.append((name, s, El, exc, c2, rn, rb))
    return (M1, M2, M3, om), res

Sig2 = np.array([[2.0, 0.6], [0.6, 0.5]])
D0 = np.array([[0.5, -0.2], [-0.2, 0.3]])
deltas2 = []
for t in (1.0, 0.3, 0.1, 0.03, 0.01):
    Dl = t*D0
    if np.linalg.eigvalsh(Sig2 - Dl).min() < 0:  # keep Delta <= Sigma
        Dl = Dl*0.9*np.linalg.eigvalsh(np.linalg.solve(msqrt(Dl), np.linalg.solve(msqrt(Dl), Sig2).T)).min()
    deltas2.append(Dl)
deltas2.append(0.98*Sig2)  # near the maximal distortion
allres = []
A = np.array([[1.0, 0.6], [-0.4, 1.0]]); Bm = np.array([[0.8, -0.5], [0.3, 1.1]])
for name, (f, dirj, Gm) in [("x+0.3 A sin(Bx), G=diag(4,1)", mk_sinmix(A, Bm, 0.3, np.diag([4.0, 1.0]))),
                            ("x+0.9 A sin(2Bx), G=I", mk_sinmix(A, 2*Bm, 0.9, np.eye(2))),
                            ("softmax(W x) arm B", mk_softmax(Wb, 1.0)),
                            ("softmax(4 W x)", mk_softmax(Wb, 4.0))]:
    Ms, res = run_multi(name, f, dirj, Gm, Sig2, 40, deltas2)
    say(f"2-D {name}: M=({Ms[0]:.3f},{Ms[1]:.3f},{Ms[2]:.3f}) omega={Ms[3]:.3f}")
    for r in res:
        say("    s=%.4f E l=%.6f excess=% .3e c2=% .3e  rho_note=%.3e (x%.0f)  rho_back=%.3e (x%.1f)" %
            (r[1], r[2], r[3], r[4], r[5], r[5]/max(abs(r[3]), 1e-300), r[6], r[6]/max(abs(r[3]), 1e-300)))
    allres += res
Sig3 = np.diag([0.02, 0.02, 0.02]) + 0.005
deltas3 = [t*Sig3 for t in (0.5, 0.1, 0.02)]
f, dirj, Gm = mk_cossum(3)
Ms, res = run_multi("cos-sum p=3 (positive c2)", f, dirj, Gm, Sig3, 14, deltas3)
say(f"3-D cos-sum: M=({Ms[0]:.3f},{Ms[1]:.3f},{Ms[2]:.3f}) omega={Ms[3]:.4f}")
for r in res:
    say("    s=%.4f E l=%.7f excess=% .3e c2=% .3e  rho_note=%.3e (x%.1f)  rho_back=%.3e (x%.1f)" %
        (r[1], r[2], r[3], r[4], r[5], r[5]/max(abs(r[3]), 1e-300), r[6], r[6]/max(abs(r[3]), 1e-300)))
allres += res
v = [r for r in allres if abs(r[3]) > r[5]*(1+1e-9) or abs(r[3]) > r[6]*(1+1e-9)]
say(f"multi-D: violations of either bound: {v}")
open(__file__.replace('.py', '.out.txt'), 'w').write("\n".join(out))
