"""Numerical checks of the steps in the proof of the window theorem
(general spectra): the unwhitened form of the cost, the order sandwich,
subadditivity, the finite-memory embedding, the one-sided gap, and the
explicit 1/N bound.

The source is a random moving-average vector process of memory m = 2 with
a memoryless holder (the setting of the theorem).  Nothing here proves the
theorem; each check is an inequality or identity used in its proof, tested
on instances.

Run:  python verify_windows.py     (about two minutes; writes verify_windows.json)
"""
import json
import sys
import time

import numpy as np

import spectral_core as sc
from verify_spectral import random_source, dmax

SEED = 20261115
LN2 = np.log(2.0)
OUT = {}
FAILED = []


def report(name, ok, **kv):
    OUT[name] = dict(ok=bool(ok), **kv)
    if not ok:
        FAILED.append(name)
    brief = ", ".join(f"{k}={v:.3e}" if isinstance(v, float) else f"{k}={v}" for k, v in kv.items() if k != "table")
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {brief}", flush=True)


def ld(A):
    return float(np.linalg.slogdet(sc.herm(A))[1])            # natural log


def toeplitz_cov(acov, N, p):
    S = np.zeros((N * p, N * p))
    for a in range(N):
        for b in range(N):
            S[a * p:(a + 1) * p, b * p:(b + 1) * p] = acov(a - b)
    return S


def G_fun(Delta, J, N, alpha):
    """G_N(Delta) per symbol in bits: (1/2N) [ -log det Delta + (1-alpha) log det (I + J_N Delta) ]."""
    JN = np.kron(np.eye(N), J)
    return (-ld(Delta) + (1 - alpha) * ld(np.eye(len(Delta)) + sc.psd_sqrt(JN) @ Delta @ sc.psd_sqrt(JN))) / (2 * N * LN2)


def window(sp, N, alpha, D):
    Qt, Ht, SUn, Sig = sc.toeplitz_problem(sp, N)
    s = sc.solve([(Qt, Ht, SUn)], [1.0 / N], alpha, D)
    Rt = np.real(sc.psd_sqrt(Sig))
    return s["cost"], Rt @ np.real(s["X"][0]) @ Rt, Sig


def spectral(sp, alpha, D, n=1024):
    """Spectral value and the optimal error spectrum Delta*(w_k) on the full grid."""
    s = sc.spectral_solve(sp, n, alpha, D, half=True)
    Xh = s["X"]
    Xs = [Xh[k] if k <= n // 2 else Xh[n - k].conj() for k in range(n)]
    Ds = []
    for k in range(n):
        R = sc.psd_sqrt(sp.Sigma(2 * np.pi * k / n))
        Ds.append(sc.herm(R @ Xs[k] @ R))
    return s["cost"], np.array(Ds)


def coeffs(F, lags):
    """Real matrix Fourier coefficients R(tau) = mean_k F(w_k) e^{+i w_k tau}, tau = 0..lags-1."""
    n = len(F)
    w = 2 * np.pi * np.arange(n) / n
    return [np.real(np.tensordot(np.exp(1j * w * t), F, axes=(0, 0))) / n for t in range(lags)]


def acov_from(co):
    def f(tau):
        t = abs(tau)
        if t >= len(co):
            return np.zeros_like(co[0])
        return co[t] if tau >= 0 else co[t].T
    return f


def K_of(co):
    return float(sum(t * np.linalg.norm(co[t], "fro") ** 2 for t in range(1, len(co))))


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    sp = random_source(rng, 2, 1, 1, taps=3, htaps=1)
    p, m = sp.p, len(sp.G) - 1
    H = sp.Hk[0]
    J = H.T @ np.linalg.inv(sp.SU) @ H
    Dm = dmax(sp)
    D = 0.4 * Dm
    alphas = (0.0, 0.5, 1.0)

    # 1. unwhitened form: cost = G(Delta) - G(Sigma_N)
    err = 0.0
    for al in alphas:
        for N in (3, 8):
            v, Delta, Sig = window(sp, N, al, D)
            err = max(err, abs(v - (G_fun(Delta, J, N, al) - G_fun(Sig, J, N, al))))
    report("unwhitened_form", err < 1e-9, max_err=err)

    # window and spectral values
    Ns = (2, 3, 4, 6, 8, 12, 16, 24, 32)
    Vw = {(al, N): window(sp, N, al, D)[0] for al in alphas for N in Ns}
    Vs, Dstar = {}, {}
    for al in alphas:
        Vs[al], Dstar[al] = spectral(sp, al, D)

    # 2. one-sided gap: V_N >= V for every N
    gmin = min(Vw[al, N] - Vs[al] for al in alphas for N in Ns)
    report("window_above_spectral", gmin > -1e-8, min_gap=gmin,
           table=[dict(alpha=al, N=N, gap=Vw[al, N] - Vs[al], N_gap=N * (Vw[al, N] - Vs[al])) for al in alphas for N in Ns])

    # 3. subadditivity: (N+M) V_{N+M} <= N V_N + M V_M
    worst = -np.inf
    for al in alphas:
        for (a, b) in ((2, 2), (2, 4), (4, 4), (4, 8), (8, 8), (8, 16), (16, 16), (12, 12), (3, 3), (6, 6)):
            worst = max(worst, (a + b) * Vw[al, a + b] - a * Vw[al, a] - b * Vw[al, b])
    report("subadditivity", worst < 1e-8, max_violation=worst)

    # 4. finite-memory embedding: n V^c_n(D') <= N V^w_N(D), n = N + m, D' = (N D + m Dmax)/n
    worst = -np.inf
    sub = 0.0
    for N in (3, 6, 12, 24):
        n = N + m
        _, _, _, SigC = sc.circulant_problem(sp, n)
        _, _, _, SigW = sc.toeplitz_problem(sp, N)
        sub = max(sub, float(np.abs(SigC[:N * p, :N * p] - SigW).max()))
        for al in alphas:
            Dp = (N * D + m * Dm) / n
            vc = sc.spectral_solve(sp, n, al, Dp)["cost"]
            worst = max(worst, n * vc - N * Vw[al, N])
    report("finite_memory_embedding", worst < 1e-8 and sub < 1e-12, max_violation=worst, submatrix_err=sub)

    # 5. order sandwich: Sigma' = Sigma - eps I <= Sigma <= (1 + kappa) Sigma'
    eps = 0.05
    sp2 = sc.Spectrum(sp.G, sp.B - eps * np.eye(p), sp.Hk, sp.SU, sp.Q)
    lam_min = min(np.linalg.eigvalsh(sp2.Sigma(w)).min() for w in np.linspace(0, np.pi, 400))
    kappa = eps / lam_min
    slack_lo, slack_hi = np.inf, np.inf
    for al in alphas:
        for N in (4, 8):
            v = Vw[al, N]
            v2 = window(sp2, N, al, D)[0]
            v2s = window(sp2, N, al, D / (1 + kappa))[0]
            c = 0.5 * p * np.log2(1 + kappa)
            slack_hi = min(slack_hi, v2 + c - v)            # V <= V' + c
            slack_lo = min(slack_lo, v - (v2s - c))         # V >= V'(D/(1+kappa)) - c
    report("order_sandwich", slack_lo > -1e-8 and slack_hi > -1e-8, kappa=float(kappa), slack_lower=slack_lo, slack_upper=slack_hi)

    # 6. Toeplitz point and the explicit 1/N bound
    lam = np.array([np.linalg.eigvalsh(sp.Sigma(w)) for w in np.linspace(0, np.pi, 800)])
    a_S, b_S = float(lam.min()), float(lam.max())
    n_grid = len(Dstar[0.0])
    coS = [sp.autocov(t) for t in range(m + 1)]
    KS = K_of(coS)
    Jn = float(np.linalg.norm(J, 2))
    rows = []
    ok = True
    mean_ld_S = float(np.mean([ld(sp.Sigma(2 * np.pi * k / n_grid)) for k in range(n_grid)]))
    for al in alphas:
        coD = coeffs(Dstar[al], 200)
        KD = K_of(coD)
        bound_const = (b_S / a_S ** 3 * KS + (1 - al) * (1 + Jn * b_S) * Jn ** 2 * KD) / (2 * LN2)
        for N in (4, 8, 16, 32):
            Tdel = toeplitz_cov(acov_from(coD), N, p)
            Sig = toeplitz_cov(sp.autocov, N, p)
            feas = float(np.linalg.eigvalsh(Sig - Tdel).min())
            dist = float(np.trace(np.kron(np.eye(N), sp.Q) @ Tdel)) / N
            cost_pt = G_fun(Tdel, J, N, al) - G_fun(Sig, J, N, al)
            # sharper form: [ s_N(Sigma) + (1 - alpha) s_N(F*) ] / (2 N ln 2),  F* = I + J^{1/2} Delta* J^{1/2}
            Jh = sc.psd_sqrt(J)
            Fst = np.array([np.eye(p) + Jh @ d @ Jh for d in Dstar[al]])
            sF = ld(np.eye(N * p) + np.kron(np.eye(N), Jh) @ Tdel @ np.kron(np.eye(N), Jh)) - N * float(np.mean([ld(f) for f in Fst]))
            sS = ld(Sig) - N * mean_ld_S
            bound_s = (sS + (1 - al) * sF) / (2 * N * LN2)
            gap_pt = cost_pt - Vs[al]
            gap_w = Vw[al, N] - Vs[al]
            rows.append(dict(alpha=al, N=N, gap_window=gap_w, gap_toeplitz_point=gap_pt, bound_s=bound_s, bound=bound_const / N,
                             feasible_min_eig=feas, distortion=dist))
            ok &= feas > -1e-9 and abs(dist - D) < 1e-6 and gap_pt >= gap_w - 1e-7 and bound_s >= gap_pt - 1e-7 and bound_const / N >= bound_s - 1e-9
    report("toeplitz_point_and_bound", ok, a=a_S, b=b_S, K_Sigma=KS, table=rows,
           worst_ratio_bound_over_gap=float(min(r["bound"] / max(r["gap_window"], 1e-300) for r in rows)),
           worst_ratio_sharp_bound_over_gap=float(min(r["bound_s"] / max(r["gap_window"], 1e-300) for r in rows)),
           largest_ratio_sharp_bound_over_gap=float(max(r["bound_s"] / max(r["gap_window"], 1e-300) for r in rows)))

    # 7. the excess log-determinant: 0 <= s_N(F) <= (b / a^3) K(F)  (natural log)
    ok = True
    worst = 0.0
    grid = [sp.Sigma(2 * np.pi * k / n_grid) for k in range(n_grid)]
    mean_ld = float(np.mean([ld(F) for F in grid]))
    for N in (2, 4, 8, 16, 32):
        sN = ld(toeplitz_cov(sp.autocov, N, p)) - N * mean_ld
        ok &= -1e-8 <= sN <= b_S / a_S ** 3 * KS + 1e-9
        worst = max(worst, sN)
    report("excess_logdet", ok, max_s_N=worst, bound=b_S / a_S ** 3 * KS)

    OUT["_meta"] = dict(seed=SEED, numpy=np.__version__, failed=FAILED, seconds=round(time.time() - t0, 1),
                        D=D, Dmax=Dm, memory=m)
    json.dump(OUT, open("verify_windows.json", "w"), indent=1)
    print(f"{len(OUT) - 1 - len(FAILED)} passed, {len(FAILED)} failed, {OUT['_meta']['seconds']} s")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
