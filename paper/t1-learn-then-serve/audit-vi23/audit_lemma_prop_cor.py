"""Independent referee numerics for T1 note v3: Lemma 1 constants, Lemma coverage on a
non-commuting variance-extremal law, Proposition 4 (own solver), Corollary 5, softmax W,
leaky ReLU numbers, circle formula.  Written by the auditor; does not import the author's script."""
import numpy as np
from scipy.optimize import minimize
import sys

rng = np.random.default_rng(12345)
LN2 = np.log(2)
out = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

# ---------------------------------------------------------------- A. Lemma constants, arm S
def q_sin(s2, b):  # E(1+b cos X)^2, X~N(0,s2)
    return 1 + 2*b*np.exp(-s2/2) + b*b/2*(1+np.exp(-2*s2))
# check q_sin by quadrature
x, w = np.polynomial.hermite_e.hermegauss(80); w = w/w.sum()
for s2 in (2.0, 0.5):
    assert abs(np.sum(w*(1+0.2*np.cos(np.sqrt(s2)*x))**2) - q_sin(s2, 0.2)) < 1e-12
for beta in (0.05, 0.2):
    q = np.array([q_sin(2.0, beta), q_sin(0.5, beta)])   # G scales cancel in Q^{-1/2} P Q^{-1/2}
    nup = max((1+beta)**2/q) - 1; num = 1 - min((1-beta)**2/q)
    p, m, d = 2, 32, 0.1; L = np.log(2*p/d)
    r = np.sqrt(2*nup*num*L/m)
    ep, em = r + 2*nup*L/(3*m), r + 2*num*L/(3*m)
    nu = max(nup, num); ev2 = nu*(np.sqrt(2*L/m) + 2*L/(3*m))
    # exact roots t_pm
    tp = nup*L/(3*m) + np.sqrt((nup*L/(3*m))**2 + 2*nup*num*L/m)
    tm = num*L/(3*m) + np.sqrt((num*L/(3*m))**2 + 2*nup*num*L/m)
    say(f"A beta={beta}: nu+={nup:.4f} nu-={num:.4f} eps+={ep:.4f} eps-={em:.4f} v2={ev2:.4f} t+={tp:.4f} t-={tm:.4f}")

# ---------------------------------------------------------------- B. Lemma coverage, non-commuting extremal law
def haar(p):
    Z = rng.standard_normal((p, p)); Qm, R = np.linalg.qr(Z); return Qm*np.sign(np.diag(R))
worst = 1.0
for (nup, num, p, m) in [(0.25, 0.5, 3, 8), (0.9, 0.9, 3, 16), (2.0, 0.3, 4, 32), (5.0, 1.0, 3, 64), (0.05, 1.0, 2, 4)]:
    delta = 0.1; L = np.log(2*p/delta)
    r = np.sqrt(2*nup*num*L/m); ep, em = r+2*nup*L/(3*m), r+2*num*L/(3*m)
    pr = num/(nup+num); reps = 3000; ok = 0
    for _ in range(reps):
        S = np.zeros((p, p))
        for i in range(m):
            U = haar(p); z = np.where(rng.random(p) < pr, nup, -num)
            S += (U*z) @ U.T
        ev = np.linalg.eigvalsh(S/m)
        ok += (ev.max() <= ep) and (ev.min() >= -em)
    cov = ok/reps; worst = min(worst, cov)
    say(f"B nu+={nup} nu-={num} p={p} m={m}: coverage {cov:.4f} (need >= {1-delta})")

# ---------------------------------------------------------------- C. Proposition 4
# p = 1 closed form: V(alpha,D) objective decreasing in delta -> delta = min(D/w, s2)
def V1(alpha, D, w, s2, j):
    d = min(D/w, s2)
    r = 0.5*np.log2(s2/d); l = 0.5*np.log2((1/d + j)/(1/s2 + j))
    return alpha*r + (1-alpha)*l
viol_note = viol_sharp = 0; nchk = 0; tight = []
for _ in range(20000):
    w, s2, j = np.exp(rng.uniform(-2, 2, 3))
    a = np.exp(rng.uniform(-2, 1)); b = a*np.exp(rng.uniform(0, 2)); alpha = rng.random()
    Dmax = a*w*s2; D = Dmax*np.exp(rng.uniform(-6, 0))
    gap = V1(alpha, D/b, w, s2, j) - V1(alpha, D/a, w, s2, j)
    up = 0.5*np.log2(b/a)
    lo_note = up - (1-alpha)*j*D/(2*LN2*a*w)
    lo_sharp = up - (1-alpha)*j*D*(1/a - 1/b)/(2*LN2*w)
    nchk += 1
    viol_note += (gap < lo_note - 1e-12) or (gap > up + 1e-12)
    viol_sharp += (gap < lo_sharp - 1e-12)
    if alpha < 0.5: tight.append((up-gap)/((1-alpha)*j*D*(1/a-1/b)/(2*LN2*w)))
say(f"C p=1: {nchk} cases, violations of note bound {viol_note}, of sharpened (c-1) bound {viol_sharp}; "
    f"deficit/sharpened-term in [{min(tight):.3f},{max(tight):.3f}]")

# p = 2, own solver (SLSQP on Cholesky factor), objective: alpha*r + (1-alpha)*l, bits
def own_V(Sig, W, J, alpha, D, starts=6):
    p = Sig.shape[0]; iu = np.tril_indices(p)
    ldS = np.linalg.slogdet(Sig)[1]; ldK = np.linalg.slogdet(np.linalg.inv(Sig)+J)[1]
    def unpack(v):
        Lm = np.zeros((p, p)); Lm[iu] = v; return Lm @ Lm.T
    def f(v):
        Dl = unpack(v)
        s, ld = np.linalg.slogdet(Dl)
        if s <= 0: return 1e6
        r = 0.5*(ldS - ld)/LN2
        l = 0.5*(np.linalg.slogdet(np.linalg.inv(Dl)+J)[1] - ldK)/LN2
        return alpha*r + (1-alpha)*l
    cons = [dict(type='ineq', fun=lambda v: D - np.trace(W @ unpack(v))),
            dict(type='ineq', fun=lambda v: np.linalg.eigvalsh(Sig - unpack(v)).min())]
    best = None
    for k in range(starts):
        M = rng.standard_normal((p, p)); D0 = M @ M.T + 0.1*np.eye(p)
        D0 *= 0.5*min(D/np.trace(W @ D0), np.linalg.eigvalsh(Sig).min()/np.linalg.eigvalsh(D0).max())
        v0 = np.linalg.cholesky(D0)[iu]
        res = minimize(f, v0, method='SLSQP', constraints=cons, options=dict(ftol=1e-14, maxiter=2000))
        if best is None or res.fun < best.fun: best = res
    return best.fun, unpack(best.x)

sys.path.insert(0, r"C:\source\worktrees\geometric-observation-t1-v3\paper\tit-stationary")
try:
    import spectral_core as sc
    have_sc = True
except Exception as e:
    have_sc = False; say("spectral_core import failed", e)

def msqrt(A):
    w_, V_ = np.linalg.eigh(A); return (V_*np.sqrt(np.clip(w_, 0, None))) @ V_.T
def sc_V(Sig, W, H, SU, alpha, D):
    S12 = msqrt(Sig); Qt = S12 @ W @ S12; Qt = (Qt+Qt.T)/2
    r = sc.solve([(Qt, np.array(H) @ S12, np.array(SU))], [1.0], alpha, D)
    return r["cost"]

Sig = np.array([[2.0, 0.6], [0.6, 0.7]]); W = np.array([[3.0, -0.8], [-0.8, 1.2]])
H = np.array([[1.0, 0.5], [0.2, -1.0]]); SU = np.diag([0.3, 0.5]); J = H.T @ np.linalg.solve(SU, H)
lw, ls, lJ = np.linalg.eigvalsh(W).min(), np.linalg.eigvalsh(Sig).min(), np.linalg.eigvalsh(J).max()
maxdiff = 0; rows = []
for (a, b) in [(0.8, 1.25), (1/1.3, 1/0.7), (0.5, 2.0)]:
    for alpha in (0.0, 0.3, 1.0):
        for frac in (1.0, 0.3, 0.05, 0.005):
            D = frac*a*lw*ls
            vb, _ = own_V(Sig, W, J, alpha, D/b); va, _ = own_V(Sig, W, J, alpha, D/a)
            if have_sc:
                maxdiff = max(maxdiff, abs(vb - sc_V(Sig, W, H, SU, alpha, D/b)), abs(va - sc_V(Sig, W, H, SU, alpha, D/a)))
            gap = vb - va; up = np.log2(b/a)  # p/2 * log2(b/a), p=2
            lo_n = up - (1-alpha)*lJ*D/(2*LN2*a*lw)
            lo_s = up - (1-alpha)*lJ*D*(1/a-1/b)/(2*LN2*lw)
            rows.append((a, b, alpha, frac, gap, up, lo_n, lo_s))
bad = [r for r in rows if not (r[6]-1e-7 <= r[4] <= r[5]+1e-7)]
bad_s = [r for r in rows if r[4] < r[7]-1e-7]
say(f"C p=2: {len(rows)} cases; own solver vs spectral_core max |diff| = {maxdiff:.2e}; "
    f"note-bound violations {len(bad)}; sharpened-bound violations {len(bad_s)}")
for r in rows[:12]:
    say("   a=%.3f b=%.3f alpha=%.1f frac=%.3f gap=%.5f up=%.5f lo_note=%.5f lo_sharp=%.5f" % r)

# ---------------------------------------------------------------- E. Corollary 5
worst = 0
for _ in range(200000):
    p = int(rng.integers(1, 200)); eta = p*rng.random()**3 + 1e-9
    nup = np.exp(rng.uniform(-6, 3)); num = rng.choice([1.0, rng.random()])
    delta = np.exp(rng.uniform(-20, -0.1)); L = np.log(2*p/delta); nu = max(nup, num)
    m = np.ceil(L*max(200/9*nup*num*p*p/eta**2, 20/9*nu*p/eta))
    r = np.sqrt(2*nup*num*L/m); ep, em = r+2*nup*L/(3*m), r+2*num*L/(3*m)
    if em >= 1: worst = np.inf; break
    worst = max(worst, p/2*np.log2((1+ep)/(1-em))/eta)
say(f"E Cor 5: max tau_eps/eta over 2e5 random cases = {worst:.4f}")
xs = np.linspace(1e-6, 1, 100001)
say(f"E tanh(ln2 x) >= 0.6 x on (0,1]: min ratio {np.min(np.tanh(LN2*xs)/(0.6*xs)):.6f}; tanh(ln2)={np.tanh(LN2):.12f}")

# ---------------------------------------------------------------- F. softmax arm-B W
Wb = np.random.default_rng(20261117).standard_normal((3, 2)); Wb /= np.linalg.norm(Wb, 2)
one = np.ones(3)/np.sqrt(3)
dist = np.linalg.norm(one - Wb @ np.linalg.lstsq(Wb, one, rcond=None)[0])
def smx(z):
    e = np.exp(z - z.max()); return e/e.sum()
mins = []
for rad in (0.0, 1.0, 5.0, 20.0, 60.0):
    lm = []
    for th in np.linspace(0, 2*np.pi, 721):
        xx = rad*np.array([np.cos(th), np.sin(th)]); s = smx(Wb @ xx)
        A = np.diag(s) - np.outer(s, s); P = Wb.T @ A @ A @ Wb
        lm.append(np.linalg.eigvalsh(P).min())
    mins.append((rad, min(lm)))
say(f"F softmax W: rank={np.linalg.matrix_rank(Wb)}, dist(1/sqrt3, range W)={dist:.4f}; min eig P on circles {mins}")

# ---------------------------------------------------------------- G. leaky ReLU, circle
for a in (0.01, 0.2):
    nu = (1-a*a)/(1+a*a); tau = 0.5*np.log2((1+nu)/(1-nu))
    say(f"G leaky a={a}: nu={nu:.4f}, tau_nu/p={tau:.4f}, log2(1/a)={np.log2(1/a):.4f}")
for Dl in (0.01, 0.3, 2.0):
    z = rng.standard_normal(2_000_000)*np.sqrt(Dl)
    say(f"G circle Delta={Dl}: MC E(2-2cos d)={np.mean(2-2*np.cos(z)):.5f}  formula={2*(1-np.exp(-Dl/2)):.5f}")

open(__file__.replace('.py', '.out.txt'), 'w').write("\n".join(out))
