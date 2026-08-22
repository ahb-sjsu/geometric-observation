"""GO-16 opening probe -- the adversarial observer (EXPLORATORY, disclosed).

The LQG disclosure game
-----------------------
Encoder E has private type X ~ N(0, I_n). E commits to a record (its
long-run observable strategy)

    A = F X + W,   W ~ N(0, D_w),  D_w diagonal >= 0,

wanting A to track the value-ideal (exploitative) policy S X:

    value loss  = ||F - S||_F^2 + tr(D_w).

The adversary D reads the record through a BUDGETED read operator: a
k-dimensional orthonormal frame Theta (k x m), Y = Theta A, and then
exploits the statistic Z = H X.  E's leakage penalty is lambda * R,
R = tr Cov(E[Z | Y]) (the variance of Z the reader resolves).

With N = F F' + D_w and G = N^{-1/2} F H' H F' N^{-1/2}, the
best-responding reader's value is the Ky Fan sum

    R*(F, D_w) = sum of top-k eigenvalues of G          (Prop 2)

so E's Stackelberg objective (E commits, pool adapts) is

    J(F, D_w) = ||F - S||^2 + tr D_w + lambda * KyFan_k(G).

Probe questions
  C1  kernel-freeness: for FIXED Theta, the optimum has
      P_ker (F* - S) = 0 and zero kernel dither (exact; Prop 1).
  C2  indifference ties: at the Stackelberg optimum, does the G-spectrum
      tie at the k-th eigenvalue (reader indifferent at the margin --
      the eigen-analog of poker's bluff-catcher indifference)?
  C3  exploitation captured vs reader budget k (phase structure).
  C4  shrinkage vs dither: is D_w* ever active in the LQG game?
      (If never: randomized bluffing is the discrete shadow of
      shrinkage, forced by action-support constraints, absent here.)
  C5  rank saturation: with rank-1 H, reader budget beyond k=1 is wasted.

Deterministic: fixed seeds, numpy + scipy only.  Exploratory -- no
prereg governs this run; numbers are for the GO-16 statement v0.1.
"""

import json
import numpy as np
from scipy.optimize import minimize

RNG_SEED = 20260821
EPS = 1e-9


def make_instance(n=6, m=6, p=6, seed=RNG_SEED):
    rng = np.random.default_rng(seed)
    S = rng.standard_normal((m, n))
    H = rng.standard_normal((p, n))
    # normalize so tr(HH') = n (leakage ceiling comparable across p)
    H *= np.sqrt(n / np.trace(H @ H.T))
    return S, H


def leakage_fixed_theta(F, Dw, H, Theta):
    N = F @ F.T + np.diag(Dw) + EPS * np.eye(F.shape[0])
    C_zy = H @ F.T @ Theta.T
    C_y = Theta @ N @ Theta.T
    return float(np.trace(C_zy @ np.linalg.solve(C_y, C_zy.T)))


def G_spectrum(F, Dw, H):
    m = F.shape[0]
    N = F @ F.T + np.diag(Dw) + EPS * np.eye(m)
    w, V = np.linalg.eigh(N)
    Nmh = V @ np.diag(w ** -0.5) @ V.T
    M = Nmh @ F @ H.T
    return np.sort(np.linalg.eigvalsh(M @ M.T))[::-1]  # descending


def kyfan(F, Dw, H, k):
    return float(np.sum(G_spectrum(F, Dw, H)[:k]))


def pack(F, u):
    return np.concatenate([F.ravel(), u])


def unpack(z, m, n):
    F = z[: m * n].reshape(m, n)
    u = z[m * n:]
    return F, u ** 2  # Dw = u^2 >= 0


def optimize(obj, m, n, S, restarts=6, seed=RNG_SEED):
    rng = np.random.default_rng(seed + 1)
    best = None
    for r in range(restarts):
        F0 = S + 0.3 * r * rng.standard_normal((m, n))
        u0 = 0.1 * rng.standard_normal(m)
        res = minimize(obj, pack(F0, u0), method="L-BFGS-B",
                       options=dict(maxiter=4000, maxfun=200000))
        if best is None or res.fun < best.fun:
            best = res
    return best


def run():
    n = m = 6
    out = {"seed": RNG_SEED, "n": n, "m": m, "checks": {}}

    # ---------- C1: kernel-freeness at fixed Theta ----------
    S, H = make_instance(p=6)
    rng = np.random.default_rng(RNG_SEED + 7)
    k = 2
    Q, _ = np.linalg.qr(rng.standard_normal((m, k)))
    Theta = Q.T                        # k x m, orthonormal rows
    P_ker = np.eye(m) - Theta.T @ Theta
    lam = 1.0

    def obj_fixed(z):
        F, Dw = unpack(z, m, n)
        return (np.sum((F - S) ** 2) + np.sum(Dw)
                + lam * leakage_fixed_theta(F, Dw, H, Theta))

    res = optimize(obj_fixed, m, n, S)
    F1, Dw1 = unpack(res.x, m, n)
    out["checks"]["C1_kernel_freeness"] = {
        "lambda": lam, "k": k,
        "kernel_residual_norm": float(np.linalg.norm(P_ker @ (F1 - S))),
        "read_deviation_norm": float(np.linalg.norm(Theta @ (F1 - S))),
        "kernel_dither": float(np.sum(np.diag(Dw1) * 0
                                      + (P_ker @ np.diag(Dw1) @ P_ker).diagonal().sum() * 0
                                      )),  # replaced below
        "max_dither": float(np.max(Dw1)),
        "J": float(res.fun),
    }
    # kernel dither: energy of D_w seen only through kernel directions
    out["checks"]["C1_kernel_freeness"]["kernel_dither"] = float(
        np.trace(P_ker @ np.diag(Dw1) @ P_ker))

    # ---------- C2/C3/C4: Stackelberg optimum, sweep k and lambda ----------
    sweep = []
    for lam in [0.01, 0.3, 1.0, 3.0]:
        for k in range(1, m + 1):
            def obj_mm(z, k=k, lam=lam):
                F, Dw = unpack(z, m, n)
                return (np.sum((F - S) ** 2) + np.sum(Dw)
                        + lam * kyfan(F, Dw, H, k))
            res = optimize(obj_mm, m, n, S)
            F2, Dw2 = unpack(res.x, m, n)
            spec = G_spectrum(F2, Dw2, H)
            gap_rel = (float((spec[k - 1] - spec[k]) / max(spec[0], EPS))
                       if k < m else None)
            sweep.append({
                "lambda": lam, "k": k, "J": float(res.fun),
                "value_loss": float(np.sum((F2 - S) ** 2)),
                "dither_total": float(np.sum(Dw2)),
                "leak": float(kyfan(F2, Dw2, H, k)),
                "spec": [float(x) for x in spec],
                "tie_gap_rel_at_k": gap_rel,
            })
    out["checks"]["C2_C3_C4_sweep"] = sweep

    # ---------- C5: rank-1 exploit statistic -- budget saturation ----------
    S1, H1 = make_instance(p=1, seed=RNG_SEED + 100)
    sat = []
    lam = 1.0
    for k in range(1, m + 1):
        def obj_r1(z, k=k):
            F, Dw = unpack(z, m, n)
            return (np.sum((F - S1) ** 2) + np.sum(Dw)
                    + lam * kyfan(F, Dw, H1, k))
        res = optimize(obj_r1, m, n, S1)
        sat.append({"k": k, "J": float(res.fun)})
    out["checks"]["C5_rank1_saturation"] = sat

    return out


if __name__ == "__main__":
    result = run()
    print("GO16_PROBE_RESULT_BEGIN")
    print(json.dumps(result, indent=1))
    print("GO16_PROBE_RESULT_END")
