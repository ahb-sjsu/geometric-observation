"""Audit VI-24: Theorem 5 restated for the weighted map g = G^{1/2} C, and Corollary 8(a).

Theorem 5: |E l_C(T,That) - tr(Q Delta)| <= min(rho_b, rho_f), M_j = sup ||D^j g||.
 Consumers chosen to exercise the v4 restatement:
  (a) G singular, C itself NOT Lipschitz (third output x1^2 unseen by G),
  (b) G full rank, non-diagonal,
  (c) G of rank one (C's second output not Lipschitz-relevant beyond G),
  (d) softmax(Wx), G = I (no sandwich).
 M_j and omega are grid sups (lower estimates), so a pass is stringent.
 E l is computed by 4-D Gauss-Hermite on (That, Z) = independent (N(0,Sigma-Delta), N(0,Delta)).

Corollary 8(a): with Qhat on the boundary of the event (1-e-)Q <= Qhat <= (1+e+)Q,
 Dhat = (1-e-)(D - rhobar), rhobar = rho_b at s = D/lmin(Qhat): every Gaussian test channel
 with tr(Qhat Dhat_) <= Dhat must have consumer loss <= D.  Adversarial Delta's are tried.
 Also the frontier inequality V_Qhat(a, Dhat) <= V_Q(a, D) + taubar with a small solver.
"""
import numpy as np
import sympy as sp
from numpy.polynomial.hermite_e import hermegauss
from scipy.optimize import minimize

rng = np.random.default_rng(1118)
x1, x2 = sp.symbols("x1 x2", real=True)
X = [x1, x2]


def psd_sqrt(A):
    w, U = np.linalg.eigh(A)
    return U @ np.diag(np.sqrt(np.clip(w, 0, None))) @ U.T


def build(Cexpr, G):
    Gh = psd_sqrt(np.array(G, float))
    g = sp.Matrix(Gh) * sp.Matrix(Cexpr)
    k = g.shape[0]
    J = g.jacobian(X)
    D2 = [[[sp.diff(g[i], X[a], X[b]) for b in range(2)] for a in range(2)] for i in range(k)]
    D3 = [[[[sp.diff(g[i], X[a], X[b], X[c]) for c in range(2)] for b in range(2)] for a in range(2)] for i in range(k)]
    fg = sp.lambdify((x1, x2), list(g), "numpy")
    fJ = sp.lambdify((x1, x2), J.tolist(), "numpy")
    f2 = sp.lambdify((x1, x2), D2, "numpy")
    f3 = sp.lambdify((x1, x2), D3, "numpy")

    def arr(f, a, b, shape):
        out = f(a, b)
        res = np.zeros(shape + a.shape)
        it = np.ndindex(*shape)
        for idx in it:
            v = out
            for i in idx:
                v = v[i]
            res[idx] = np.broadcast_to(v, a.shape)
        return np.moveaxis(res, list(range(len(shape))), list(range(-len(shape), 0))) if False else res

    def gv(a, b):
        return arr(lambda u, v: fg(u, v), a, b, (k,))       # (k, *shape)

    def Jv(a, b):
        return arr(fJ, a, b, (k, 2))

    def D2v(a, b):
        return arr(f2, a, b, (k, 2, 2))

    def D3v(a, b):
        return arr(f3, a, b, (k, 2, 2, 2))

    return k, gv, Jv, D2v, D3v


def specnorm_k2(M):
    """spectral norm of k x 2 matrices; M shape (k,2,N)."""
    A = np.einsum("kiN,kjN->ijN", M, M)
    tr = A[0, 0] + A[1, 1]
    det = A[0, 0] * A[1, 1] - A[0, 1] ** 2
    return np.sqrt(np.maximum(tr / 2 + np.sqrt(np.maximum(tr ** 2 / 4 - det, 0)), 0))


def Mconsts(Jv, D2v, D3v, box=6.0, n=61, nang=48):
    a = np.linspace(-box, box, n)
    A, B = np.meshgrid(a, a, indexing="ij")
    A, B = A.ravel(), B.ravel()
    A = np.concatenate([A, rng.normal(0, 2, 3000)]); B = np.concatenate([B, rng.normal(0, 2, 3000)])
    J = Jv(A, B)
    M1 = specnorm_k2(J).max()
    T2 = D2v(A, B)
    T3 = D3v(A, B)
    angs = np.linspace(0, np.pi, nang, endpoint=False)
    U = np.stack([np.cos(angs), np.sin(angs)], 1)
    M2 = 0.0
    for u in U:
        M2 = max(M2, specnorm_k2(np.einsum("kabN,a->kbN", T2, u)).max())
    M3 = 0.0
    for u in U[::2]:
        Tu = np.einsum("kabcN,a->kbcN", T3, u)
        for v in U[::2]:
            M3 = max(M3, specnorm_k2(np.einsum("kbcN,b->kcN", Tu, v)).max())
    P = np.einsum("kaN,kbN->abN", J, J)
    return M1, M2, M3, (A, B, P)


def gh2(n):
    z, w = hermegauss(n)
    w = w / w.sum()
    Z1, Z2 = np.meshgrid(z, z, indexing="ij")
    W = np.outer(w, w)
    return np.stack([Z1.ravel(), Z2.ravel()]), W.ravel()


def Qmat(Jv, Sig, n=70):
    Zs, W = gh2(n)
    T = psd_sqrt(Sig) @ Zs
    J = Jv(T[0], T[1])
    P = np.einsum("kaN,kbN->abN", J, J)
    return np.einsum("abN,N->ab", P, W)


def Eloss(gv, Sig, Dl, n=26):
    Zs, W = gh2(n)
    Lh = psd_sqrt(Sig - Dl)
    Ld = psd_sqrt(Dl)
    Th = Lh @ Zs                     # (2, n^2)
    Zd = Ld @ Zs
    gh = gv(Th[0], Th[1])            # (k, n^2)
    tot = 0.0
    for j in range(Zd.shape[1]):
        T = Th + Zd[:, j:j + 1]
        gt = gv(T[0], T[1])
        tot += W[j] * np.sum(W * np.sum((gt - gh) ** 2, 0))
    return tot


def rho_b(M1, M2, M3, s):
    return (1.75 * M2 ** 2 + 2 * M1 * M3) * s ** 2 + np.sqrt(5) / 2 * M2 * M3 * s ** 2.5 + 5 / 12 * M3 ** 2 * s ** 3


def rho_f(M1, M2, M3, om, s, th):
    return (om * th + M1 * M2 * (3 * th ** 0.5 * s + 3 ** 0.75 * th ** 1.5)
            + (0.75 * M2 ** 2 + M1 * M3) * s ** 2 + np.sqrt(5) / 2 * M2 * M3 * s ** 2.5 + 5 / 12 * M3 ** 2 * s ** 3)


Wsm = np.array([[1.0, 0.0], [0.3, 1.0], [-0.8, 0.5]])
lg = [Wsm[i, 0] * x1 + Wsm[i, 1] * x2 for i in range(3)]
den = sum(sp.exp(l) for l in lg)
CONSUMERS = {
    "(a) G=diag(1,1,0), C=(x1+.3sin x2, x2+.2sin x1, x1^2)": ([x1 + 0.3 * sp.sin(x2), x2 + 0.2 * sp.sin(x1), x1 ** 2], np.diag([1.0, 1.0, 0.0])),
    "(b) G=[[2,1,0],[1,1,0],[0,0,1]], C=(tanh(x1+.5x2), sin x2, .5x1)": ([sp.tanh(x1 + 0.5 * x2), sp.sin(x2), 0.5 * x1], [[2, 1, 0], [1, 1, 0], [0, 0, 1]]),
    "(c) G=vv^T, v=(1,2), C=(cos x1, sin x2 + x1)": ([sp.cos(x1), sp.sin(x2) + x1], np.outer([1, 2], [1, 2])),
    "(d) softmax(Wx), G=I": ([sp.exp(l) / den for l in lg], np.eye(3)),
}
SIGMAS = [np.diag([1.0, 0.5]), np.array([[2.0, 0.6], [0.6, 1.0]]), 0.2 * np.eye(2), 5.0 * np.eye(2)]

out = []
P = out.append
P("=== Theorem 5 with M_j of g = G^{1/2} C (grid sups: lower estimates, stringent) ===")
built = {}
for name, (Ce, G) in CONSUMERS.items():
    k, gv, Jv, D2v, D3v = build(Ce, G)
    M1, M2, M3, (Ag, Bg, Pg) = Mconsts(Jv, D2v, D3v)
    built[name] = (gv, Jv, M1, M2, M3, Ag, Bg, Pg)
    P(f"{name}: M1={M1:.4f} M2={M2:.4f} M3={M3:.4f}")
    worst = np.inf; nviol = 0; ncase = 0; wins_b = 0
    for Sig in SIGMAS:
        Q = Qmat(Jv, Sig)
        om = np.max(np.abs(np.linalg.eigvalsh(np.moveaxis(Pg - Q[:, :, None], -1, 0))))
        Si = np.linalg.inv(Sig)
        Lsig = psd_sqrt(Sig)
        for rep in range(6):
            U, _ = np.linalg.qr(rng.normal(size=(2, 2)))
            f = 10 ** rng.uniform(-2.5, 0, 2)
            Dl = Lsig @ U @ np.diag(f) @ U.T @ Lsig
            Dl = 0.5 * (Dl + Dl.T)
            s = np.trace(Dl); th = np.trace(Dl @ Si @ Dl)
            El = Eloss(gv, Sig, Dl)
            ex = abs(El - np.trace(Q @ Dl))
            rb, rf = rho_b(M1, M2, M3, s), rho_f(M1, M2, M3, om, s, th)
            r = min(rb, rf)
            ncase += 1; wins_b += rb < rf
            if ex > r:
                nviol += 1
            worst = min(worst, r / max(ex, 1e-300))
    P(f"    {ncase} cases over 4 Sigmas: violations={nviol}; min rho/|excess|={worst:.2f}; rho_b<rho_f in {wins_b}/{ncase}")

# quadrature-accuracy spot check
gv, Jv, M1, M2, M3, *_ = built["(b) G=[[2,1,0],[1,1,0],[0,0,1]], C=(tanh(x1+.5x2), sin x2, .5x1)"]
Sig = SIGMAS[1]; Dl = 0.1 * Sig
P(f"GH accuracy spot check (b): E l with 26 vs 34 nodes: {Eloss(gv, Sig, Dl, 26):.12f} vs {Eloss(gv, Sig, Dl, 34):.12f}")
# loss depends on C only through g: consumer (a) vs the same g without the unseen x1^2 output
k2, gv2, *_ = build([x1 + 0.3 * sp.sin(x2), x2 + 0.2 * sp.sin(x1)], np.eye(2))
gva = built["(a) G=diag(1,1,0), C=(x1+.3sin x2, x2+.2sin x1, x1^2)"][0]
P(f"(a) vs its g alone: E l = {Eloss(gva, SIGMAS[0], 0.3 * SIGMAS[0]):.12f} vs {Eloss(gv2, SIGMAS[0], 0.3 * SIGMAS[0]):.12f}")

P("")
P("=== Corollary 8(a): loss <= D for every test channel with tr(Qhat Dhat) <= Dhat ===")
Hh = np.array([[1.0, 0.5]]); SU = np.array([[0.3]])
Jinfo = Hh.T @ np.linalg.inv(SU) @ Hh


def r_l(Sig, Dl):
    K = np.linalg.inv(np.linalg.inv(Sig) + Jinfo)
    r = 0.5 * np.log2(np.linalg.det(Sig) / np.linalg.det(Dl))
    l = 0.5 * np.log2(np.linalg.det(K)) + 0.5 * np.log2(np.linalg.det(np.linalg.inv(Dl) + Jinfo))
    return r, l


def V(W, D, Sig, alpha, starts=12):
    """min alpha r + (1-alpha) l over 0 < Delta <= Sigma, tr(W Delta) <= D."""
    Ls = psd_sqrt(Sig)
    if np.trace(W @ Sig) <= D:
        return 0.0, Sig
    best = (np.inf, None)

    def Dof(z):
        th, a, b = z
        U = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        m = 1 / (1 + np.exp(-np.array([a, b])))
        return Ls @ U @ np.diag(m) @ U.T @ Ls

    def obj(z):
        r, l = r_l(Sig, Dof(z))
        return alpha * r + (1 - alpha) * l

    for _ in range(starts):
        z0 = np.array([rng.uniform(0, np.pi), rng.normal(-1, 1), rng.normal(-1, 1)])
        res = minimize(obj, z0, method="SLSQP", constraints=[{"type": "ineq", "fun": lambda z: D - np.trace(W @ Dof(z))}],
                       options={"maxiter": 500, "ftol": 1e-12})
        if res.success and np.trace(W @ Dof(res.x)) <= D * (1 + 1e-7) and res.fun < best[0]:
            best = (res.fun, Dof(res.x))
    return best


k_, gv_, Jv_, D2v_, D3v_ = build([x1 + 0.1 * sp.sin(x2), x2 + 0.1 * sp.sin(x1) + 0.3 * x1], [[1.5, 0.5], [0.5, 1.0]])
M1_, M2_, M3_, _ = Mconsts(Jv_, D2v_, D3v_)
built["(e) G=[[1.5,.5],[.5,1]], C=(x1+.1sin x2, x2+.1sin x1+.3x1)"] = (gv_, Jv_, M1_, M2_, M3_, None, None, None)
for name in ["(a) G=diag(1,1,0), C=(x1+.3sin x2, x2+.2sin x1, x1^2)", "(e) G=[[1.5,.5],[.5,1]], C=(x1+.1sin x2, x2+.1sin x1+.3x1)", "(d) softmax(Wx), G=I"]:
    gv, Jv, M1, M2, M3, *_ = built[name]
    Sig = SIGMAS[0]
    Q = Qmat(Jv, Sig)
    Qh_half = psd_sqrt(Q)
    P(f"{name}: M=({M1:.3f},{M2:.3f},{M3:.3f}) eig(Q)={np.linalg.eigvalsh(Q)}")
    worst_ratio = 0.0; ncert = 0; vfail = 0; vcount = 0
    for (ep, em) in [(0.25, 0.6), (0.1, 0.3), (0.5, 0.9)]:
        for rep in range(4):
            U, _ = np.linalg.qr(rng.normal(size=(2, 2)))
            ev = [1 - em, 1 + ep] if rep < 2 else list(rng.uniform(1 - em, 1 + ep, 2))
            Qhat = Qh_half @ U @ np.diag(ev) @ U.T @ Qh_half
            lminQh = np.linalg.eigvalsh(Qhat)[0]
            for fD in [0.001, 0.003, 0.01, 0.03, 0.1, 0.2]:
                D = fD * np.trace(Q @ Sig)
                rbar = rho_b(M1, M2, M3, D / lminQh)
                if rbar >= D:
                    continue
                ncert += 1
                Dhat = (1 - em) * (D - rbar)
                # worst direction: minimise u^T Qhat u / u^T Q u
                w, Vv = np.linalg.eigh(np.linalg.inv(Qh_half) @ Qhat @ np.linalg.inv(Qh_half))
                u = np.linalg.inv(Qh_half) @ Vv[:, 0]
                cands = []
                for frac in [1.0, 0.98, 0.9]:
                    Dl = frac * np.outer(u, u) + (1 - frac) * np.eye(2) * 0.05
                    cands.append(Dl)
                for _ in range(4):
                    A = rng.normal(size=(2, 2)); cands.append(A @ A.T + 1e-3 * np.eye(2))
                for Dl in cands:
                    Dl = Dl * Dhat / np.trace(Qhat @ Dl)
                    # enforce Delta <= Sigma by shrinking (keeps tr(Qhat Delta) <= Dhat)
                    lm = np.max(np.linalg.eigvalsh(np.linalg.inv(psd_sqrt(Sig)) @ Dl @ np.linalg.inv(psd_sqrt(Sig))))
                    if lm > 1:
                        Dl = Dl / lm * 0.999
                    El = Eloss(gv, Sig, Dl, n=22)
                    worst_ratio = max(worst_ratio, El / D)
                if rep == 0 and fD in (0.01, 0.1):
                    taubar = np.log2((1 + ep) / ((1 - em) * (1 - rbar / D)))  # p/2 log(.) with p = 2
                    for alpha in [0.0, 0.5, 1.0]:
                        vh, _ = V(Qhat, Dhat, Sig, alpha)
                        vq, _ = V(Q, D, Sig, alpha)
                        vcount += 1
                        if vh > vq + taubar + 1e-6:
                            vfail += 1
    P(f"    certified (D, Qhat) pairs: {ncert}; max E l / D over adversarial test channels = {worst_ratio:.4f} (must be <= 1)")
    P(f"    V_Qhat(a,Dhat) <= V_Q(a,D) + taubar: {vcount - vfail}/{vcount} hold")

open(__file__.replace(".py", ".out.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
