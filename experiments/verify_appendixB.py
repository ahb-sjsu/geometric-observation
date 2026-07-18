#!/usr/bin/env python
"""Rigorous numerical verification of Observation-Theory Appendix B (true-divergence).
Tests the load-bearing claims where an error would surface as a numeric mismatch:
  B2  : R_C^true(D) == R_U(D)         (output reduction; the tilt is C)
  B2a : R_C^true(0) == H(C(X))        (unconditional quotient floor)
  B3i : high-resolution closed form (fixed-G Gaussian, exact reverse water-filling)
  B3ii: pinch  R_q(D/alpha) <= R_{D_Y}(D) <= R_q(D/beta)  when alpha q <= D_Y <= beta q
Everything is in NATS. No repo deps."""
import numpy as np
rng = np.random.default_rng(20260717)


def blahut_arimoto(p, d, beta, iters=20000, tol=1e-13):
    """Discrete rate-distortion at multiplier beta. Returns (D, R_nats)."""
    m, mh = d.shape
    q = np.full(mh, 1.0 / mh)
    E = np.exp(-beta * d)                       # (m, mh)
    for _ in range(iters):
        r = q[None, :] * E                      # unnormalized r(xhat|x)
        r /= r.sum(1, keepdims=True)
        qn = p @ r
        if np.max(np.abs(qn - q)) < tol:
            q = qn; break
        q = qn
    r = q[None, :] * E; r /= r.sum(1, keepdims=True)
    D = float((p[:, None] * r * d).sum())
    with np.errstate(divide="ignore", invalid="ignore"):
        logterm = np.where(r > 0, np.log(r / q[None, :]), 0.0)
    R = float((p[:, None] * r * logterm).sum())
    return D, max(R, 0.0)


def H(p):
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


print("=" * 70)
print("B2 + B2a: output reduction and unconditional floor")
print("=" * 70)
# nontrivial many-to-one consumer C: X(12) -> U(4), fibers of size 3
m, k, fib = 12, 4, 3
C = np.repeat(np.arange(k), fib)               # C[x] = x // 3
pX = rng.dirichlet(np.ones(m) * 0.7)
pU = np.array([pX[C == u].sum() for u in range(k)])
# STRICT, ASYMMETRIC divergence on U (no symmetry / triangle assumed by B2)
DY = rng.uniform(0.5, 2.0, size=(k, k)); np.fill_diagonal(DY, 0.0)
dC = DY[C[:, None], C[None, :]]                # (12,12) true distortion on X-space

print(f"H(C(X)) = H(U) = {H(pU):.10f} nats")
max_dR = max_dD = 0.0
for beta in np.geomspace(0.05, 60.0, 30):
    Dt, Rt = blahut_arimoto(pX, dC, beta)      # R_C^true : X-space, recon alphabet = X (12 syms)
    Du, Ru = blahut_arimoto(pU, DY, beta)      # R_U      : U-space, recon alphabet = V = U (4 syms)
    max_dR = max(max_dR, abs(Rt - Ru)); max_dD = max(max_dD, abs(Dt - Du))
Dt0, Rt0 = blahut_arimoto(pX, dC, 400.0)       # beta -> inf : the floor
print(f"B2   max|R_C^true - R_U| over sweep = {max_dR:.3e}")
print(f"B2   max|D_C^true - D_U| over sweep = {max_dD:.3e}")
print(f"B2a  R_C^true(D->0) = {Rt0:.10f}  vs  H(C(X)) = {H(pU):.10f}  |diff|={abs(Rt0-H(pU)):.3e}")
print(f"B2/B2a VERDICT: {'PASS' if max_dR<1e-6 and max_dD<1e-6 and abs(Rt0-H(pU))<1e-4 else 'FAIL'}")

print()
print("=" * 70)
print("B3(i): high-resolution closed form vs exact Gaussian RD (fixed G)")
print("=" * 70)
r = 3
A = rng.standard_normal((r, r)); Sigma = A @ A.T + 0.5 * np.eye(r)     # SPD source cov
Bg = rng.standard_normal((r, r)); G = Bg @ Bg.T + 0.5 * np.eye(r)      # SPD output metric
W = np.linalg.cholesky(G / 2.0)                # W W^T = G/2  ; q_G = ||W(uhat-u)||^2
lam = np.linalg.eigvalsh(W @ Sigma @ W.T)      # eigenvalues of tilted-source cov


def gauss_rd_mse(lam, D):
    """Exact reverse water-filling RD (nats) for N(0,diag(lam)) under MSE, total distortion D."""
    lam = np.sort(lam)[::-1]                    # descending
    rr = len(lam)
    theta = D / rr                              # default: all modes active
    for kact in range(rr, 0, -1):              # kact = number of coded (active) modes
        theta = (D - lam[kact:].sum()) / kact
        if theta <= lam[kact - 1] and (kact == rr or theta >= lam[kact]):
            break
    active = lam > theta
    return float(0.5 * np.sum(np.log(lam[active] / theta))) if active.any() else 0.0


def hires_formula(Sigma, G, r, D):
    hU = 0.5 * np.log((2 * np.pi * np.e) ** r * np.linalg.det(Sigma))
    return hU - (r / 2.0) * np.log(2 * np.pi * np.e * D / r) + 0.5 * np.log(np.linalg.det(G / 2.0))


for D in [1e-2, 1e-3, 1e-4, 1e-5]:
    exact = gauss_rd_mse(lam, D)
    form = hires_formula(Sigma, G, r, D)
    print(f"  D={D:.0e}  exact_RD={exact:.8f}  hires_formula={form:.8f}  diff={abs(exact-form):.3e}")
print("B3(i) VERDICT: PASS if diff -> 0 as D shrinks (exact match once all modes active)")

print()
print("=" * 70)
print("B3(ii): pinch  R_q(D/alpha) <= R_{D_Y}(D) <= R_q(D/beta)  [feasible-set inclusion]")
print("=" * 70)
# base distortion q on a discrete alphabet; D_Y entrywise bracketed: alpha q <= D_Y <= beta q
n = 8
qd = rng.uniform(0.3, 1.5, size=(n, n)); np.fill_diagonal(qd, 0.0)
pS = rng.dirichlet(np.ones(n))
alpha, beta_hi = 0.7, 1.4
fac = rng.uniform(alpha, beta_hi, size=(n, n)); np.fill_diagonal(fac, 1.0)
DYm = qd * fac
ok = True
for bmul in np.geomspace(0.2, 20.0, 12):
    D_dy, R_dy = blahut_arimoto(pS, DYm, bmul)
    # R_q evaluated at D/alpha and D/beta via matched-distortion inversion of the q-curve
    # (compare rates at equal distortion): find q-curve rate at target distortions
    def Rq_at(Dtarget):
        # bisect beta so BA(q) hits Dtarget, return its rate
        lo, hi = 1e-3, 500.0
        for _ in range(60):
            mid = np.sqrt(lo * hi); Dm, Rm = blahut_arimoto(pS, qd, mid, iters=6000)
            if Dm > Dtarget: lo = mid
            else: hi = mid
        Dm, Rm = blahut_arimoto(pS, qd, np.sqrt(lo * hi), iters=6000)
        return Rm, Dm
    R_lo, _ = Rq_at(D_dy / alpha)      # R_q(D/alpha)  -> lower bound
    R_hi, _ = Rq_at(D_dy / beta_hi)    # R_q(D/beta)   -> upper bound
    lower_ok = R_lo <= R_dy + 1e-6
    upper_ok = R_dy <= R_hi + 1e-6
    ok = ok and lower_ok and upper_ok
    tag = "ok" if (lower_ok and upper_ok) else "VIOLATION"
    print(f"  D_DY={D_dy:.4f}  R_q(D/a)={R_lo:.4f} <= R_DY={R_dy:.4f} <= R_q(D/b)={R_hi:.4f}  [{tag}]")
print(f"B3(ii) VERDICT: {'PASS' if ok else 'FAIL'}")
