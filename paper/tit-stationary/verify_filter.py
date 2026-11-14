"""Numerical checks of the steps in the proof of the coding theorem for a
holder with a filter (the last subsection of the section on the stationary
source).

The source is a random moving-average vector process of memory 2, and the
holder sees it through a causal filter with two taps in white noise.  The
holder's observations at the times of a window depend on one source symbol
before the window.  Checked on this instance:

  1. interior cost >= window cost >= spectral cost, and both gaps shrink;
  2. subadditivity of the window cost;
  3. the embedding of a window in a periodic source with a filter;
  4. the edge bound: dropping the edge observations changes the leakage of
     the optimal description by at most e_H bits in total;
  5. the comparison of spectral costs under a change of the noise power.

Colored noise is not exercised (the solver's spectrum class has white
noise).  Nothing here proves the theorem.

Run:  python verify_filter.py     (about two minutes; writes verify_filter.json)
"""
import json
import sys
import time

import numpy as np

import spectral_core as sc
from verify_spectral import random_source, dmax

SEED = 20261116
OUT = {}
FAILED = []


def report(name, ok, **kv):
    OUT[name] = dict(ok=bool(ok), **kv)
    if not ok:
        FAILED.append(name)
    brief = ", ".join(f"{k}={v:.3e}" if isinstance(v, float) else f"{k}={v}" for k, v in kv.items() if k != "table")
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {brief}", flush=True)


def window_problem(sp, N, interior=False):
    """The memoryless problem for T^N with the holder's observations at the
    times of the window (or only those that are functions of T^N).
    Causal filter with taps H_0..H_{mH}: S_t = sum_k H_k T_{t-k} + U_t."""
    p, r, mH = sp.p, sp.Hk[0].shape[0], len(sp.Hk) - 1
    L = N + mH                                         # extended window: times 1-mH .. N
    SigE = np.zeros((L * p, L * p))
    for a in range(L):
        for b in range(L):
            SigE[a * p:(a + 1) * p, b * p:(b + 1) * p] = sp.autocov(a - b)
    HE = np.zeros((N * r, L * p))                      # row t <-> time t+1, column j <-> time j+1-mH
    for t in range(N):
        for k, Hk in enumerate(sp.Hk):
            j = t + mH - k
            HE[t * r:(t + 1) * r, j * p:(j + 1) * p] = Hk
    win = slice(mH * p, L * p)
    Sig = SigE[win, win]
    CST = HE @ SigE[:, win]                            # Cov(S, T^N)
    CSS = HE @ SigE @ HE.T + np.kron(np.eye(N), sp.SU)
    A = CST @ np.linalg.inv(Sig)
    CU = CSS - A @ Sig @ A.T                           # effective noise, independent of T^N
    if interior:
        keep = slice(mH * r, N * r)
        A, CU = A[keep], CU[keep, keep]
    Rt = np.real(sc.psd_sqrt(Sig))
    Qn = np.kron(np.eye(N), sp.Q)
    return sc.herm(Rt @ Qn @ Rt), A @ Rt, sc.herm(CU), Sig


def cost(sp, N, alpha, D, interior=False):
    Qt, Ht, CU, _ = window_problem(sp, N, interior)
    return sc.solve([(Qt, Ht, CU)], [1.0 / N], alpha, D)


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    sp = random_source(rng, 2, 1, 1, taps=3, htaps=2)
    p, r, m, mH = sp.p, sp.Hk[0].shape[0], len(sp.G) - 1, len(sp.Hk) - 1
    Dm = dmax(sp)
    D = 0.4 * Dm
    alphas = (0.0, 0.5)
    Ns = (3, 4, 6, 8, 12, 16, 24)

    Vs = {al: sc.spectral_solve(sp, 1024, al, D, half=True)["cost"] for al in alphas}
    W = {(al, N): cost(sp, N, al, D) for al in alphas for N in Ns}
    Wi = {(al, N): cost(sp, N, al, D, interior=True) for al in alphas for N in Ns}

    # 1. ordering and convergence
    rows = [dict(alpha=al, N=N, gap_window=W[al, N]["cost"] - Vs[al], gap_interior=Wi[al, N]["cost"] - Vs[al])
            for al in alphas for N in Ns]
    ok = all(r_["gap_interior"] >= r_["gap_window"] - 1e-8 and r_["gap_window"] > -1e-8 for r_ in rows)
    ok &= all(max(r_["gap_interior"] for r_ in rows if r_["alpha"] == al and r_["N"] == Ns[-1])
              < min(r_["gap_interior"] for r_ in rows if r_["alpha"] == al and r_["N"] == Ns[0]) for al in alphas)
    report("ordering_and_convergence", ok, table=rows,
           last_gap_window=max(r_["gap_window"] for r_ in rows if r_["N"] == Ns[-1]),
           last_gap_interior=max(r_["gap_interior"] for r_ in rows if r_["N"] == Ns[-1]))

    # 2. subadditivity of the window cost
    worst = max((a + b) * W[al, a + b]["cost"] - a * W[al, a]["cost"] - b * W[al, b]["cost"]
                for al in alphas for (a, b) in ((3, 3), (4, 4), (4, 8), (8, 8), (6, 6), (12, 12), (8, 16)))
    report("subadditivity", worst < 1e-8, max_violation=worst)

    # 3. embedding in the periodic source: n V_n(D') <= N V^w_N(D), n = N + 2 mH + m
    worst = -np.inf
    for N in (4, 8, 16):
        n = N + 2 * mH + m
        for al in alphas:
            Dp = D + (n - N) / n * (Dm - D)
            worst = max(worst, n * sc.spectral_solve(sp, n, al, Dp)["cost"] - N * W[al, N]["cost"])
    report("embedding_with_filter", worst < 1e-8, max_violation=worst)

    # 4. edge bound for the optimal window description: N (L_int - L_window) <= e_H
    lam_S = max(np.linalg.eigvalsh(sp.H(w) @ sp.Sigma(w) @ sp.H(w).conj().T + sp.SU).max() for w in np.linspace(0, np.pi, 400))
    a_U = float(np.linalg.eigvalsh(sp.SU).min())
    e_H = mH * r * np.log2(2 * lam_S / a_U)            # the constant of the paper (two-sided filter, noise >= a_U / 2)
    worst = 0.0
    for al in alphas:
        for N in (4, 8, 16):
            Qt, Ht, CU, _ = window_problem(sp, N)
            Qi, Hi, CUi, _ = window_problem(sp, N, interior=True)
            X = W[al, N]["X"][0]
            # sc.leak is the leakage of the whole block in bits, so the difference is the edge information
            worst = max(worst, sc.leak(X, Hi, CUi) - sc.leak(X, Ht, CU))
    report("edge_bound", 0 <= worst <= e_H, max_edge_bits=float(worst), e_H=float(e_H))

    # 5. noise comparison: Sigma_U <= P <= (1 + kappa) Sigma_U
    kappa = 0.2
    sp2 = sc.Spectrum(sp.G, sp.B, sp.Hk, (1 + kappa) * sp.SU, sp.Q)
    ok = True
    slack = np.inf
    for al in alphas:
        v2 = sc.spectral_solve(sp2, 1024, al, D, half=True)["cost"]
        up = Vs[al] + (1 - al) * 0.5 * p * np.log2(1 + kappa)
        ok &= Vs[al] - 1e-9 <= v2 <= up + 1e-9
        slack = min(slack, v2 - Vs[al], up - v2)
    report("noise_comparison", ok, kappa=kappa, min_slack=float(slack))

    OUT["_meta"] = dict(seed=SEED, numpy=np.__version__, failed=FAILED, seconds=round(time.time() - t0, 1),
                        D=D, Dmax=Dm, memory=m, filter_taps=mH + 1)
    json.dump(OUT, open("verify_filter.json", "w"), indent=1)
    print(f"{len(OUT) - 1 - len(FAILED)} passed, {len(FAILED)} failed, {OUT['_meta']['seconds']} s")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
