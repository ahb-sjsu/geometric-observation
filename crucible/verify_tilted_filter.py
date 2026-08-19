"""Numerical check: tilted-mean closed form for affine P(x), Gaussian posterior.

Claim: for P(x) = P0 + sum_k x_k P_k (symmetric parts PSD on support region),
X ~ N(m, S), the minimizer of E[(X-a)^T P(X) (X-a)] is
    a* = Pbar(m)^{-1} (Pbar(m) m + v(S)),  Pbar(m) = P0 + sum_k m_k P_k,
    v(S) = sum_k P_k S e_k
i.e. a* = m + Pbar(m)^{-1} v(S).
Check by direct Monte-Carlo loss evaluation + numeric minimization.
"""
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(20260819)
D = 4
fails = 0
for trial in range(20):
    # random symmetric P0 (strongly PSD to keep P(x) PSD w.h.p. on support), small P_k
    A = rng.normal(size=(D, D))
    P0 = A @ A.T + 3.0 * np.eye(D)
    Pk = []
    for k in range(D):
        B = 0.15 * rng.normal(size=(D, D))
        Pk.append((B + B.T) / 2)
    m = rng.normal(size=D)
    C = rng.normal(size=(D, D))
    S = 0.5 * (C @ C.T) / D + 0.1 * np.eye(D)

    # closed form
    Pbar = P0 + sum(m[k] * Pk[k] for k in range(D))
    v = sum(Pk[k] @ S[:, k] for k in range(D))
    a_closed = m + np.linalg.solve(Pbar, v)

    # exact expected loss, computable in closed form too (independent route):
    # E[(X-a)^T P(X) (X-a)] with X = m + Z, Z ~ N(0,S), d = m - a:
    # P(X) = Pbar + sum_k Z_k P_k
    # E = d^T Pbar d + 2 d^T (sum_k P_k S e_k) + tr(Pbar S) + E[Z^T (sum Z_k P_k) Z]
    # (last term independent of a). Minimize the a-dependent part directly numerically.
    def exact_loss_part(a):
        d = m - a
        return d @ Pbar @ d + 2 * d @ v + a * 0 @ a if False else d @ Pbar @ d + 2 * d @ v

    res = minimize(lambda a: exact_loss_part(a), m, method="BFGS")
    a_exact = res.x

    # Monte-Carlo brute check of the full loss at both candidates + perturbations
    Z = rng.normal(size=(200000, D)) @ np.linalg.cholesky(S).T
    X = m + Z

    def mc_loss(a):
        dxa = X - a
        PX = np.einsum("ij,nj->ni", P0, dxa) + np.einsum(
            "nk,kij,nj->ni", X, np.array(Pk), dxa
        )
        return np.mean(np.einsum("ni,ni->n", dxa, PX))

    l_closed = mc_loss(a_closed)
    l_mean = mc_loss(m)
    # random perturbations around a_closed must not beat it (beyond MC noise)
    worse = 0
    for _ in range(8):
        ap = a_closed + 0.05 * rng.normal(size=D)
        if mc_loss(ap) < l_closed - 1e-3:
            worse += 1

    ok = np.allclose(a_closed, a_exact, atol=1e-6) and worse == 0
    if not ok:
        fails += 1
        print(f"trial {trial}: FAIL closed-vs-exact diff {np.abs(a_closed-a_exact).max():.2e}, beaten {worse}/8")
    else:
        tilt = np.linalg.norm(a_closed - m)
        gain = l_mean - l_closed
        print(f"trial {trial:2d}: OK  |tilt|={tilt:.4f}  loss(mean)-loss(tilt)={gain:+.5f}")

print("\nRESULT:", "ALL OK" if fails == 0 else f"{fails} FAILURES")
