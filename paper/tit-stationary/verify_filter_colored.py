"""Numerical checks of steps of the proof of the coding theorem for a holder
with a filter, on an instance with a TWO-SIDED filter and COLORED noise.

Source: a random moving-average vector process of memory 2, p = 2.
Holder: S_t = H_{-1} T_{t+1} + H_0 T_t + H_1 T_{t-1} + U_t, r = 2, with
U_t = C_0 e_t + C_1 e_{t-1} + w_t a moving-average noise of memory 1.
The holder's observations at the times of a window depend on one source
symbol on each side of the window.

Checked on this instance:
  1. interior cost >= window cost >= spectral cost, and the gaps shrink;
  2. subadditivity of the window cost;
  3. the embedding of a window in a periodic source, with the circular
     filter and the circular colored noise (n = N + 2 m_H + max(m, m_U));
  4. the edge bound at the optimal window description;
  5. the comparison of spectral costs when the noise spectrum is raised
     from Sigma_U to P = Sigma_U + delta I (not a multiple of Sigma_U);
  6. the same degradation at the level of windows: more noise, larger cost.

Nothing here proves the theorem.

Run:  python verify_filter_colored.py   (a few minutes; writes verify_filter_colored.json)
"""
import json
import sys
import time

import numpy as np

import spectral_core as sc
from verify_spectral import random_source, dmax

SEED = 20261117
OUT = {}
FAILED = []


def report(name, ok, **kv):
    OUT[name] = dict(ok=bool(ok), **kv)
    if not ok:
        FAILED.append(name)
    brief = ", ".join(f"{k}={v:.3e}" if isinstance(v, float) else f"{k}={v}" for k, v in kv.items() if k != "table")
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {brief}", flush=True)


class FilteredSpectrum(sc.Spectrum):
    """Source as in spectral_core.Spectrum; holder with two-sided real taps
    H_k, k = -mH..mH (dict), and moving-average noise with real taps C_j plus
    a white floor:  Sigma_U(w) = C(w) C(w)^* + floor."""

    def __init__(self, G, B, taps, C, floor, Q):
        self.mH = max(abs(k) for k in taps)
        self.taps = {k: np.asarray(h, float) for k, h in taps.items()}
        self.C = [np.asarray(c, float) for c in C]
        self.floor = np.asarray(floor, float)
        r = self.floor.shape[0]
        super().__init__(G, B, [np.zeros((r, np.asarray(B).shape[0]))], self.floor, Q)
        self.r = r

    def H(self, w, delay=0):
        return sum(h * np.exp(-1j * w * k) for k, h in self.taps.items())

    def SUw(self, w):
        c = sum(cj * np.exp(-1j * w * j) for j, cj in enumerate(self.C))
        return sc.herm(c @ c.conj().T + self.floor)

    def block(self, w, delay=0):
        R = sc.psd_sqrt(self.Sigma(w))
        return sc.herm(R @ self.Q @ R), self.H(w) @ R, self.SUw(w)

    def noise_autocov(self, tau):
        """E[U_{t+tau} U_t^T]."""
        out = self.floor.copy() if tau == 0 else np.zeros_like(self.floor)
        K = len(self.C)
        for k in range(K):
            j = k - tau
            if 0 <= j < K:
                out = out + self.C[k] @ self.C[j].T
        return out


def window_problem(sp, N, interior=False):
    """The memoryless problem for T^N with the holder's observations at the
    times of the window (interior=True: only those that are functions of T^N)."""
    p, r, mH = sp.p, sp.r, sp.mH
    L = N + 2 * mH                                     # extended window: times 1-mH .. N+mH
    SigE = np.zeros((L * p, L * p))
    for a in range(L):
        for b in range(L):
            SigE[a * p:(a + 1) * p, b * p:(b + 1) * p] = sp.autocov(a - b)
    HE = np.zeros((N * r, L * p))                      # row t <-> time t+1; column j <-> time j+1-mH
    for t in range(N):
        for k, Hk in sp.taps.items():
            j = t + mH - k
            HE[t * r:(t + 1) * r, j * p:(j + 1) * p] = Hk
    CUU = np.zeros((N * r, N * r))
    for a in range(N):
        for b in range(N):
            CUU[a * r:(a + 1) * r, b * r:(b + 1) * r] = sp.noise_autocov(a - b)
    win = slice(mH * p, (mH + N) * p)
    Sig = SigE[win, win]
    CST = HE @ SigE[:, win]
    CSS = HE @ SigE @ HE.T + CUU
    A = CST @ np.linalg.inv(Sig)
    CU = CSS - A @ Sig @ A.T                           # effective noise, independent of T^N
    if interior:
        keep = slice(mH * r, (N - mH) * r)
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
    base = random_source(rng, 2, 1, 1, taps=3, htaps=1)
    p, r = 2, 2
    taps = {-1: 0.5 * rng.standard_normal((r, p)), 0: rng.standard_normal((r, p)), 1: 0.6 * rng.standard_normal((r, p))}
    C = [0.8 * rng.standard_normal((r, r)), 0.5 * rng.standard_normal((r, r))]
    floor = 0.4 * np.eye(r)
    sp = FilteredSpectrum(base.G, base.B, taps, C, floor, base.Q)
    m, mH, mU = len(sp.G) - 1, sp.mH, len(sp.C) - 1
    Dm = dmax(sp)
    D = 0.4 * Dm
    alphas = (0.0, 0.5)
    Ns = (4, 6, 8, 12, 16, 24)
    grid = 512

    Vs = {al: sc.spectral_solve(sp, grid, al, D, half=True)["cost"] for al in alphas}
    W = {(al, N): cost(sp, N, al, D) for al in alphas for N in Ns}
    Wi = {(al, N): cost(sp, N, al, D, interior=True) for al in alphas for N in Ns}

    # 1. ordering and convergence
    rows = [dict(alpha=al, N=N, gap_window=W[al, N]["cost"] - Vs[al], gap_interior=Wi[al, N]["cost"] - Vs[al])
            for al in alphas for N in Ns]
    ok = all(x["gap_interior"] >= x["gap_window"] - 1e-8 and x["gap_window"] > -1e-7 for x in rows)
    for al in alphas:
        g = [x["gap_interior"] for x in rows if x["alpha"] == al]
        ok &= g[-1] < g[0]
    report("ordering_and_convergence", ok, table=rows,
           last_gap_window=max(x["gap_window"] for x in rows if x["N"] == Ns[-1]),
           last_gap_interior=max(x["gap_interior"] for x in rows if x["N"] == Ns[-1]))

    # 2. subadditivity of the window cost
    worst = max((a + b) * W[al, a + b]["cost"] - a * W[al, a]["cost"] - b * W[al, b]["cost"]
                for al in alphas for (a, b) in ((4, 4), (4, 8), (8, 8), (6, 6), (12, 12), (8, 16), (4, 12)))
    report("subadditivity", worst < 1e-8, max_violation=worst)

    # 3. embedding in the periodic source with circular filter and circular colored noise
    worst = -np.inf
    for N in (4, 8, 16):
        n = N + 2 * mH + max(m, mU)
        for al in alphas:
            Dp = D + (n - N) / n * (Dm - D)
            worst = max(worst, n * sc.spectral_solve(sp, n, al, Dp)["cost"] - N * W[al, N]["cost"])
    report("embedding_filter_colored_noise", worst < 1e-8, max_violation=worst)

    # 4. edge bound at the optimal window description
    ws = np.linspace(0, np.pi, 400)
    b_S = float(max(np.linalg.eigvalsh(sp.H(w) @ sp.Sigma(w) @ sp.H(w).conj().T + sp.SUw(w)).max() for w in ws))
    a_U = float(min(np.linalg.eigvalsh(sp.SUw(w)).min() for w in ws))
    e_H = mH * r * np.log2(2 * b_S / a_U)
    worst = 0.0
    for al in alphas:
        for N in (4, 8, 16):
            Qt, Ht, CU, _ = window_problem(sp, N)
            Qi, Hi, CUi, _ = window_problem(sp, N, interior=True)
            X = W[al, N]["X"][0]
            worst = max(worst, sc.leak(X, Hi, CUi) - sc.leak(X, Ht, CU))     # bits for the whole block
    report("edge_bound", -1e-9 <= worst <= e_H, max_edge_bits=float(worst), e_H=float(e_H), a_U=a_U, b_S=b_S)

    # 5. noise comparison at the spectral level: P = Sigma_U + delta I, kappa = delta / a_U
    delta = 0.15
    sp2 = FilteredSpectrum(base.G, base.B, taps, C, floor + delta * np.eye(r), base.Q)
    kappa = delta / a_U
    ok = True
    slack = np.inf
    V2 = {}
    for al in alphas:
        V2[al] = sc.spectral_solve(sp2, grid, al, D, half=True)["cost"]
        up = Vs[al] + (1 - al) * 0.5 * p * np.log2(1 + kappa)
        ok &= Vs[al] - 1e-9 <= V2[al] <= up + 1e-9
        slack = min(slack, V2[al] - Vs[al], up - V2[al])
    report("noise_comparison_spectral", ok, kappa=float(kappa), min_slack=float(slack))

    # 6. degradation at the level of windows: more noise, larger window and interior costs
    worst = np.inf
    for al in alphas:
        for N in (4, 8, 16):
            worst = min(worst, cost(sp2, N, al, D)["cost"] - W[al, N]["cost"],
                        cost(sp2, N, al, D, interior=True)["cost"] - Wi[al, N]["cost"])
    report("degradation_windows", worst > -1e-9, min_increase=float(worst))

    OUT["_meta"] = dict(seed=SEED, numpy=np.__version__, failed=FAILED, seconds=round(time.time() - t0, 1),
                        D=D, Dmax=Dm, source_memory=m, filter_half_length=mH, noise_memory=mU, p=p, r=r)
    json.dump(OUT, open("verify_filter_colored.json", "w"), indent=1)
    print(f"{len(OUT) - 1 - len(FAILED)} passed, {len(FAILED)} failed, {OUT['_meta']['seconds']} s")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
