"""GO-16 theorem harness -- the revelation reduction and the partition/tie
theorem (development netting run; the governed seal is owed separately).

Nets, numerically, every load-bearing claim of GO-16 v0.2:

  V1  Achievability algebra: F* = SK, Sigma_w* = SK(I-K)S' implements
      revelation K at cost exactly tr(S(I-K)S'), with N = SKS' and
      leakage spectrum equality  spec+(G) = spec+(M^1/2 K M^1/2).
  V2  Cost lower bound: for random (F, Sigma_w), cost >= tr(S(I-K)S')
      with K the induced revelation operator (2000 samples, 0 violations).
  V3  Spectrum reduction: phi_k(G) = phi_k(M^1/2 K M^1/2) on random policies.
  V4  Dither necessity: noiseless records have idempotent K (projections);
      fractional revelation therefore REQUIRES dither -- v0.1 Conjecture 2
      is refuted and probe check C4 is diagnosed (EPS jitter = free noise).
  V5  Diagonal closed form (water level) == direct full-matrix minimization
      of the original (F, Sigma_w) game (co-diagonalization tested
      empirically; the closed form is proved at diagonal scope).
  V6  Partition + tie: the four classes (conceded / contested / level /
      submerged), theta_i = s_i^2/(lambda mu_i) on contested, attention
      budget sums to k, and lambda_k(G*) = lambda_{k+1}(G*) iff contested
      is nonempty (hand-derived instance: J* = 4.05277..., tie at t* = 1.0).
  V7  Saddle point (no commitment gap once the reader may mix): random
      feasible perturbations on both sides never improve.
  V8  Exact m=2 example: J* = 7/4, t* = mu_2 = 1, theta = (1/4, 3/4).
  V9  General (non-diagonal) instance: projected-subgradient solve of the
      SDP matches direct (F, Sigma_w) minimization; tie appears when the
      revelation spectrum is fractional.

Deterministic; numpy + scipy only.  Seed 20260821.
"""

import json
import numpy as np
from scipy.optimize import minimize

SEED = 20260821
JIT = 1e-12


def kyfan(A, k):
    w = np.sort(np.linalg.eigvalsh(A))[::-1]
    return float(np.sum(w[:k]))


def spec_desc(A):
    return np.sort(np.linalg.eigvalsh(A))[::-1]


def G_of(F, Sw, M):
    m = F.shape[0]
    N = F @ F.T + Sw + JIT * np.eye(m)
    w, V = np.linalg.eigh(N)
    Nmh = V @ np.diag(w ** -0.5) @ V.T
    return Nmh @ F @ M @ F.T @ Nmh


def K_of(F, Sw):
    m = F.shape[0]
    N = F @ F.T + Sw + JIT * np.eye(m)
    return F.T @ np.linalg.solve(N, F)


def sqrtm_psd(M):
    w, V = np.linalg.eigh(M)
    return V @ np.diag(np.sqrt(np.clip(w, 0, None))) @ V.T


# ---------------------------------------------------------------- V1
def v1(rng):
    n = m = 5
    S = rng.standard_normal((m, n))
    kappa = rng.uniform(0.05, 0.95, n)
    U, _ = np.linalg.qr(rng.standard_normal((n, n)))
    K = U @ np.diag(kappa) @ U.T
    F = S @ K
    Sw = S @ K @ (np.eye(n) - K) @ S.T
    cost = np.sum((F - S) ** 2) + np.trace(Sw)
    cost_pred = float(np.trace(S @ (np.eye(n) - K) @ S.T))
    K_ind = K_of(F, Sw)
    M = rng.standard_normal((n, n)); M = M @ M.T
    Ms = sqrtm_psd(M)
    e1 = spec_desc(G_of(F, Sw, M))
    e2 = spec_desc(Ms @ K @ Ms)
    return {
        "cost_err": abs(cost - cost_pred),
        "K_err": float(np.max(np.abs(K_ind - K))),
        "spec_err": float(np.max(np.abs(e1 - e2))),
        "pass": bool(abs(cost - cost_pred) < 1e-9
                     and np.max(np.abs(K_ind - K)) < 1e-7
                     and np.max(np.abs(e1 - e2)) < 1e-7),
    }


# ---------------------------------------------------------------- V2
def v2(rng):
    n = m = 4
    S = rng.standard_normal((m, n))
    worst = np.inf
    viol = 0
    for _ in range(2000):
        F = S + rng.uniform(0.1, 2.0) * rng.standard_normal((m, n))
        L = 0.7 * rng.standard_normal((m, m))
        Sw = L @ L.T
        cost = np.sum((F - S) ** 2) + np.trace(Sw)
        K = K_of(F, Sw)
        bound = np.trace(S @ (np.eye(n) - K) @ S.T)
        gap = cost - bound
        worst = min(worst, gap)
        if gap < -1e-7:
            viol += 1
    return {"violations": viol, "worst_gap": float(worst),
            "pass": bool(viol == 0)}


# ---------------------------------------------------------------- V3
def v3(rng):
    n = m = 5
    H = rng.standard_normal((3, n))
    M = H.T @ H
    Ms = sqrtm_psd(M)
    worst = 0.0
    for _ in range(200):
        F = rng.standard_normal((m, n))
        L = rng.standard_normal((m, m)) * 0.5
        Sw = L @ L.T
        K = K_of(F, Sw)
        for k in range(1, m + 1):
            d = abs(kyfan(G_of(F, Sw, M), k) - kyfan(Ms @ K @ Ms, k))
            worst = max(worst, d)
    return {"worst_phi_gap": float(worst), "pass": bool(worst < 1e-6)}


# ---------------------------------------------------------------- V4
def v4(rng):
    worst = 0.0
    for _ in range(200):
        F = rng.standard_normal((4, 6))
        K = F.T @ np.linalg.solve(F @ F.T, F)   # noiseless record
        worst = max(worst, float(np.max(np.abs(K @ K - K))))
    return {"worst_idempotency_gap": float(worst),
            "pass": bool(worst < 1e-8)}


# --------------------------------------------- diagonal closed form
def diag_solve(mu, s2, lam, k):
    """Water-level solution of the diagonal game; exact on breakpoints."""
    mu = np.asarray(mu, float); s2 = np.asarray(s2, float)
    m = len(mu)
    shieldable = lam * mu > s2

    def eval_t(t):
        rho = np.ones(m)
        rho[shieldable] = np.minimum(1.0, t / mu[shieldable])
        g = mu * rho
        cost = float(np.sum(s2 * (1 - rho)))
        leak = float(np.sum(np.sort(g)[::-1][:k]))
        return cost + lam * leak, rho, g

    bps = sorted(set([0.0] + list(mu)))
    cands = list(bps)
    for a, b in zip(bps[:-1], bps[1:]):
        cands.append(0.5 * (a + b))
    best = min(cands, key=lambda t: eval_t(t)[0])
    J, rho, g = eval_t(best)
    return {"t": float(best), "J": float(J), "rho": rho, "g": g}


def diag_attention(mu, s2, lam, k, sol, tol=1e-9):
    mu = np.asarray(mu, float); s2 = np.asarray(s2, float)
    t, rho, g = sol["t"], sol["rho"], sol["g"]
    m = len(mu)
    theta = np.zeros(m)
    above = g > t + tol
    level = np.abs(g - t) <= tol
    contested = level & (rho < 1 - tol)
    level_unshielded = level & ~contested
    theta[above] = 1.0
    theta[contested] = s2[contested] / (lam * mu[contested])
    slack = k - theta.sum()
    idx = np.where(level_unshielded)[0]
    if len(idx) > 0:
        theta[idx[0]] = slack
    classes = {
        "conceded_above": [int(i) for i in np.where(above & (lam * mu <= s2))[0]],
        "shieldable_above": [int(i) for i in np.where(above & (lam * mu > s2))[0]],
        "contested": [int(i) for i in np.where(contested)[0]],
        "level_unshielded": [int(i) for i in idx],
        "submerged": [int(i) for i in np.where(g < t - tol)[0]],
    }
    return theta, classes


def direct_solve(S, M, lam, k, rng, restarts=8, scale=0.4):
    """Full-matrix minimization of the original (F, Sigma_w) game."""
    m, n = S.shape
    tril = np.tril_indices(m)

    def unpack(z):
        F = z[: m * n].reshape(m, n)
        L = np.zeros((m, m))
        L[tril] = z[m * n:]
        return F, L @ L.T

    def obj(z):
        F, Sw = unpack(z)
        return (np.sum((F - S) ** 2) + np.trace(Sw)
                + lam * kyfan(G_of(F, Sw, M), k))

    best = None
    for r in range(restarts):
        F0 = S + scale * r * rng.standard_normal((m, n)) / max(1, r)
        z0 = np.concatenate([F0.ravel(),
                             0.2 * rng.standard_normal(len(tril[0]))])
        res = minimize(obj, z0, method="L-BFGS-B",
                       options=dict(maxiter=6000, maxfun=300000))
        if best is None or res.fun < best.fun:
            best = res
    F, Sw = unpack(best.x)
    return float(best.fun), F, Sw


# ---------------------------------------------------------------- V5/V6/V7
def v567(rng):
    mu = np.array([4.0, 2.5, 1.8, 1.0, 0.55, 0.3])
    s2 = np.array([0.5, 3.0, 0.4, 2.0, 0.3, 0.25])
    lam, k = 1.0, 2
    m = len(mu)

    sol = diag_solve(mu, s2, lam, k)
    theta, classes = diag_attention(mu, s2, lam, k, sol)

    # hand-derived reference values
    J_hand = 0.5 * (1 - 0.25) + 0.4 * (1 - 1.0 / 1.8) + lam * (2.5 + 1.0)
    ok_cf = abs(sol["J"] - J_hand) < 1e-9 and abs(sol["t"] - 1.0) < 1e-12

    # direct full-matrix solve of the same instance
    S = np.diag(np.sqrt(s2))
    M = np.diag(mu)
    J_dir, F_dir, Sw_dir = direct_solve(S, M, lam, k, rng)
    ok_dir = abs(J_dir - sol["J"]) < 1e-3 * (1 + abs(sol["J"]))

    # tie + budget + theta formula
    g_sorted = np.sort(sol["g"])[::-1]
    tie = abs(g_sorted[k - 1] - g_sorted[k])
    ok_tie = tie < 1e-12 and len(classes["contested"]) > 0
    ok_budget = abs(theta.sum() - k) < 1e-9 and np.all(theta > -1e-12) \
        and np.all(theta < 1 + 1e-12)
    ok_theta = (abs(theta[0] - 0.125) < 1e-9
                and abs(theta[2] - 0.4 / 1.8) < 1e-9
                and abs(theta[3] - (k - 1 - 0.125 - 0.4 / 1.8)) < 1e-9)

    # dither necessity at the optimum (V4's consequence, checked live)
    K_star = np.diag(sol["rho"])
    Sw_star = S @ K_star @ (np.eye(m) - K_star) @ S.T
    ok_dither = np.trace(Sw_star) > 1e-3

    # V7 saddle check on the bilinear payoff
    Ms = np.diag(np.sqrt(mu))
    SigS = S.T @ S

    def Lpay(K, W):
        return (np.trace(SigS @ (np.eye(m) - K))
                + lam * np.trace(W @ Ms @ K @ Ms))

    W_star = np.diag(theta)
    L0 = Lpay(K_star, W_star)
    worst_w, worst_k = 0.0, 0.0
    for _ in range(500):
        # random feasible W: 0 <= W <= I, tr W = k
        v = rng.uniform(0, 1, m)
        lo, hi = 0.0, 1e3
        for _ in range(60):
            a = 0.5 * (lo + hi)
            if np.sum(np.minimum(1.0, a * v)) < k:
                lo = a
            else:
                hi = a
        w = np.minimum(1.0, 0.5 * (lo + hi) * v)
        U, _ = np.linalg.qr(rng.standard_normal((m, m)))
        W = U @ np.diag(w) @ U.T
        worst_w = max(worst_w, Lpay(K_star, W) - L0)
        # random feasible K
        P = K_star + 0.5 * rng.standard_normal((m, m))
        P = 0.5 * (P + P.T)
        wp, Vp = np.linalg.eigh(P)
        Kp = Vp @ np.diag(np.clip(wp, 0, 1)) @ Vp.T
        worst_k = max(worst_k, L0 - Lpay(Kp, W_star))
    ok_saddle = worst_w < 1e-9 and worst_k < 1e-9

    return {
        "closed_form": {"t": sol["t"], "J": sol["J"], "J_hand": J_hand,
                        "rho": [float(x) for x in sol["rho"]],
                        "g": [float(x) for x in sol["g"]]},
        "direct_J": J_dir,
        "theta": [float(x) for x in theta],
        "classes": classes,
        "tie_gap": float(tie),
        "dither_trace_at_optimum": float(np.trace(Sw_star)),
        "saddle_worst_w": float(worst_w),
        "saddle_worst_k": float(worst_k),
        "pass_V5": bool(ok_cf and ok_dir),
        "pass_V6": bool(ok_tie and ok_budget and ok_theta),
        "pass_V7": bool(ok_saddle and ok_dither),
    }


# ---------------------------------------------------------------- V8
def v8(rng):
    mu = np.array([4.0, 1.0]); s2 = np.array([1.0, 2.0])
    lam, k = 1.0, 1
    sol = diag_solve(mu, s2, lam, k)
    theta, _ = diag_attention(mu, s2, lam, k, sol)
    S = np.diag(np.sqrt(s2)); M = np.diag(mu)
    J_dir, _, _ = direct_solve(S, M, lam, k, rng)
    ok = (abs(sol["J"] - 1.75) < 1e-12 and abs(sol["t"] - 1.0) < 1e-12
          and abs(theta[0] - 0.25) < 1e-12 and abs(theta[1] - 0.75) < 1e-12
          and abs(J_dir - 1.75) < 1e-3)
    return {"J": sol["J"], "t": sol["t"], "theta": [float(x) for x in theta],
            "direct_J": J_dir, "pass": bool(ok)}


# ---------------------------------------------------------------- V9
def v9(rng):
    n = m = 5
    S = rng.standard_normal((m, n))
    H = rng.standard_normal((n, n))
    M = H.T @ H
    Ms = sqrtm_psd(M)
    SigS = S.T @ S
    lam, k = 0.7, 2

    def Jk(K):
        return (np.trace(SigS @ (np.eye(n) - K))
                + lam * kyfan(Ms @ K @ Ms, k))

    # projected subgradient with averaging
    K = 0.5 * np.eye(n)
    K_avg = np.zeros((n, n)); wsum = 0.0
    for t in range(1, 20001):
        Gm = Ms @ K @ Ms
        w, V = np.linalg.eigh(Gm)
        idx = np.argsort(w)[::-1][:k]
        W = V[:, idx] @ V[:, idx].T
        grad = -SigS + lam * Ms @ W @ Ms
        step = 0.5 / np.sqrt(t)
        K = K - step * grad
        K = 0.5 * (K + K.T)
        wk, Vk = np.linalg.eigh(K)
        K = Vk @ np.diag(np.clip(wk, 0, 1)) @ Vk.T
        if t > 10000:
            K_avg += K; wsum += 1
    K_sdp = K_avg / wsum
    J_sdp = Jk(K_sdp)

    J_dir, F_dir, Sw_dir = direct_solve(S, M, lam, k, rng, restarts=10)

    spec = spec_desc(Ms @ K_sdp @ Ms)
    kap = np.linalg.eigvalsh(K_sdp)
    frac = bool(np.any((kap > 0.02) & (kap < 0.98)))
    tie_rel = float((spec[k - 1] - spec[k]) / max(spec[0], 1e-12))
    ok = abs(J_sdp - J_dir) < 2e-2 * (1 + abs(J_dir))
    return {"J_sdp": float(J_sdp), "J_direct": float(J_dir),
            "K_spectrum": [float(x) for x in np.sort(kap)[::-1]],
            "G_spectrum": [float(x) for x in spec],
            "fractional_K": frac, "tie_rel_gap_at_k": tie_rel,
            "tie_when_fractional_ok": bool((not frac) or tie_rel < 0.05),
            "pass": bool(ok)}


def main():
    rng = np.random.default_rng(SEED)
    out = {"seed": SEED}
    out["V1_achievability"] = v1(rng)
    out["V2_lower_bound"] = v2(rng)
    out["V3_spectrum_reduction"] = v3(rng)
    out["V4_noiseless_idempotent"] = v4(rng)
    out["V567_diagonal_partition"] = v567(rng)
    out["V8_m2_exact"] = v8(rng)
    out["V9_general_instance"] = v9(rng)
    gates = [out["V1_achievability"]["pass"], out["V2_lower_bound"]["pass"],
             out["V3_spectrum_reduction"]["pass"],
             out["V4_noiseless_idempotent"]["pass"],
             out["V567_diagonal_partition"]["pass_V5"],
             out["V567_diagonal_partition"]["pass_V6"],
             out["V567_diagonal_partition"]["pass_V7"],
             out["V8_m2_exact"]["pass"], out["V9_general_instance"]["pass"]]
    out["ALL_PASS"] = bool(all(gates))
    out["gates_passed"] = f"{sum(gates)}/{len(gates)}"
    return out


if __name__ == "__main__":
    res = main()
    print("GO16_PARTITION_VERIFY_BEGIN")
    print(json.dumps(res, indent=1))
    print("GO16_PARTITION_VERIFY_END")
