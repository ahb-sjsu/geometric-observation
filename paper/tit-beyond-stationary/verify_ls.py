"""Checks for the locally stationary results of "Rate, Leakage, and
Distortion Beyond Stationary Gaussian Sources".

The source is a time-varying moving average with a white floor
(Proposition "tvma"):

    T_t = sum_k A_k(t/N) xi_{t-k} + B0^{1/2} zeta_t ,   t = 1..N .

  local_closeness   the covariance of every short block is close in operator
                    norm to the block-Toeplitz matrix of the local spectrum,
                    and the distance shrinks with the block fraction (L2)
  window_to_ls      the frontier cost per symbol of the whole window tends to
                    the time-frequency water-filling cost V_ls (Theorem "ls")
  riemann           the cost of B frozen spectra under one level tends to V_ls
  blocks_lemma      N V_S >= min over allocations of sum n_b V_{S_b}
                    - a c(T) - (1-a) c(T|S), with the exact information
                    between blocks (the inequality inside Lemma "blocks")
  coupling_lemma    V_S(a, D + tr(Q(S-S'))/n) <= V_S'(a, D)
                    + (1-a) tr(J(S-S'))/(2 n ln 2)  for S' <= S
                    (the Gaussian content of Lemma "coupling")
  averaged          V_ls <= the spectral cost of the time-averaged spectrum
                    (Corollary "lsavg")

Solver: spectral_core.py of the companion paper.  numpy only.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tit-stationary"))
import spectral_core as sc  # noqa: E402

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


class TVMA:
    """Time-varying moving average in R^p with a white floor."""

    def __init__(self, A, B0, Q, H, SU):
        self.A = A            # list of callables u -> p x p
        self.B0, self.Q, self.H, self.SU = B0, Q, H, SU
        self.m = len(A) - 1
        self.p = B0.shape[0]
        self.J = H.T @ np.linalg.solve(SU, H)

    def cov(self, N):
        p, m = self.p, self.m
        Ak = [[self.A[k](t / N) for k in range(m + 1)] for t in range(1, N + 1)]
        S = np.zeros((N * p, N * p))
        for s in range(N):
            for t in range(max(0, s - m), min(N, s + m + 1)):
                blk = np.zeros((p, p))
                for k in range(m + 1):
                    l = k + (t - s)
                    if 0 <= l <= m:
                        blk += Ak[s][k] @ Ak[t][l].T
                if s == t:
                    blk += self.B0
                S[s * p:(s + 1) * p, t * p:(t + 1) * p] = blk
        return S

    def acov(self, u, tau):
        """Autocovariance at lag tau of the stationary process frozen at u."""
        p, m = self.p, self.m
        out = self.B0.copy() if tau == 0 else np.zeros((p, p))
        for k in range(m + 1):
            l = k - tau
            if 0 <= l <= m:
                out = out + self.A[k](u) @ self.A[l](u).T
        return out

    def toeplitz(self, u, n):
        p = self.p
        S = np.zeros((n * p, n * p))
        for s in range(n):
            for t in range(n):
                S[s * p:(s + 1) * p, t * p:(t + 1) * p] = self.acov(u, s - t)
        return S

    def sigma(self, u, w):
        Aw = sum(self.A[k](u) * np.exp(-1j * w * k) for k in range(self.m + 1))
        return sc.herm(Aw @ Aw.conj().T + self.B0)

    def block(self, u, w):
        R = sc.psd_sqrt(self.sigma(u, w))
        return sc.herm(R @ self.Q @ R), self.H @ R, self.SU.astype(complex)

    def dmax(self, G=64, W=64):
        return float(np.mean([np.real(np.trace(self.Q @ self.sigma((j + 0.5) / G, 2 * np.pi * k / W)))
                              for j in range(G) for k in range(W)]))


def vec_problem(S, Q, H, SU):
    """One real block for a Gaussian vector of n symbols (weight left to the caller)."""
    n = S.shape[0] // Q.shape[0]
    R = np.real(sc.psd_sqrt(S))
    return sc.herm(R @ np.kron(np.eye(n), Q) @ R), np.kron(np.eye(n), H) @ R, np.kron(np.eye(n), SU)


def vec_cost(S, Q, H, SU, alpha, D):
    """Frontier cost per symbol of a Gaussian vector at distortion D per symbol."""
    n = S.shape[0] // Q.shape[0]
    return sc.solve([vec_problem(S, Q, H, SU)], [1.0 / n], alpha, D)["cost"]


def v_ls(src, alpha, D, G=16, W=32):
    blocks = [src.block((j + 0.5) / G, 2 * np.pi * k / W) for j in range(G) for k in range(W)]
    return sc.solve(blocks, np.full(G * W, 1.0 / (G * W)), alpha, D)["cost"]


def v_frozen(src, alpha, D, B, W=32):
    blocks = [src.block(b / B, 2 * np.pi * k / W) for b in range(1, B + 1) for k in range(W)]
    return sc.solve(blocks, np.full(B * W, 1.0 / (B * W)), alpha, D)["cost"]


def source_scalar():
    A = [lambda u: np.array([[1.0 + 0.8 * u]]),
         lambda u: np.array([[0.9 * np.cos(np.pi * u)]]),
         lambda u: np.array([[0.5 * u * u]])]
    return TVMA(A, np.array([[0.3]]), np.array([[1.0]]), np.array([[0.8]]), np.array([[0.5]]))


def source_vector():
    A = [lambda u: np.array([[1.0, 0.3 * u], [0.2, 0.6 + 0.7 * u]]),
         lambda u: np.array([[0.7 * np.sin(np.pi * u), 0.0], [0.4, -0.5 * u]])]
    F = np.array([[1.0, 0.4]])
    return TVMA(A, 0.25 * np.eye(2), F.T @ F, np.array([[0.3, 0.9]]), np.array([[0.4]]))


def logdet(A):
    return float(np.linalg.slogdet(A)[1])


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)

    # ---------------------------------------------------------------- (L2)
    src = source_scalar()
    N = 256
    S = src.cov(N)
    rows = []
    for frac in (4, 8, 16, 32):
        n = N // frac
        worst = 0.0
        for b in range(frac):
            I = slice(b * n * src.p, (b + 1) * n * src.p)
            for t in (b * n + 1, (b + 1) * n):
                worst = max(worst, float(np.linalg.norm(S[I, I] - src.toeplitz(t / N, n), 2)))
        rows.append(dict(block_fraction=1.0 / frac, max_op_distance=worst))
    d = [r["max_op_distance"] for r in rows]
    # (L2) asks that the distance tend to zero with the block fraction.  For
    # Lipschitz coefficients it is of the order of the fraction: each halving
    # should cut it by about half.
    report("local_closeness", all(d[i + 1] < 0.6 * d[i] for i in range(3)),
           first=d[0], last=d[-1], table=rows)

    # ---------------------------------------------------------------- Theorem ls
    ok = True
    table = []
    for name, src, Ns in (("scalar", source_scalar(), (16, 32, 64, 128)),
                          ("vector", source_vector(), (8, 16, 32, 64))):
        dm = src.dmax()
        for alpha in (0.0, 0.5, 1.0):
            D = 0.35 * dm
            ref = v_ls(src, alpha, D)
            gaps = [vec_cost(src.cov(N), src.Q, src.H, src.SU, alpha, D) - ref for N in Ns]
            table.append(dict(source=name, alpha=alpha, v_ls=ref, N=list(Ns), gaps=gaps))
            ok = ok and abs(gaps[-1]) < 0.25 * abs(gaps[0]) and abs(gaps[-1]) < 6e-3
    report("window_to_ls", ok, worst_last=max(abs(r["gaps"][-1]) for r in table),
           worst_first=max(abs(r["gaps"][0]) for r in table), table=table)

    # ---------------------------------------------------------------- Riemann sums
    src = source_scalar()
    dm = src.dmax()
    ok = True
    table = []
    for alpha in (0.0, 0.5, 1.0):
        D = 0.35 * dm
        ref = v_ls(src, alpha, D, G=64)
        gaps = [v_frozen(src, alpha, D, B) - ref for B in (2, 4, 8, 16)]
        table.append(dict(alpha=alpha, gaps=gaps))
        ok = ok and abs(gaps[-1]) < abs(gaps[0]) and abs(gaps[-1]) < 0.02
    report("riemann", ok, worst_last=max(abs(r["gaps"][-1]) for r in table), table=table)

    # ---------------------------------------------------------------- Lemma blocks
    worst = np.inf
    cases = 0
    for (p, sizes) in [(1, (5, 7, 4)), (2, (3, 4)), (1, (8, 8)), (2, (2, 3, 3))]:
        n = sum(sizes)
        Gm = rng.standard_normal((n * p, n * p))
        Sv = Gm @ Gm.T / (n * p) + 0.4 * np.eye(n * p)
        F = rng.standard_normal((1, p))
        Q = F.T @ F + 0.1 * np.eye(p)
        H = rng.standard_normal((1, p))
        SU = np.array([[0.6]])
        Hn = np.kron(np.eye(n), H)
        Phi = np.block([[Sv, Sv @ Hn.T], [Hn @ Sv, Hn @ Sv @ Hn.T + np.kron(np.eye(n), SU)]])
        SS = Hn @ Sv @ Hn.T + np.kron(np.eye(n), SU)
        edges = np.cumsum((0,) + sizes)
        cT = -logdet(Sv)
        cTS = -(logdet(Phi) - logdet(SS))
        blocks, wts = [], []
        for i, nb in enumerate(sizes):
            I = np.arange(edges[i] * p, edges[i + 1] * p)
            Sb = Sv[np.ix_(I, I)]
            Hb = np.kron(np.eye(nb), H)
            SSb = Hb @ Sb @ Hb.T + np.kron(np.eye(nb), SU)
            Phib = np.block([[Sb, Sb @ Hb.T], [Hb @ Sb, SSb]])
            cT += logdet(Sb)
            cTS += logdet(Phib) - logdet(SSb)
            blocks.append(vec_problem(Sb, Q, H, SU))
            wts.append(1.0 / n)
        cT *= 0.5 / LN2
        cTS *= 0.5 / LN2
        dm = float(np.trace(np.kron(np.eye(n), Q) @ Sv)) / n
        for alpha in (0.0, 0.4, 1.0):
            for frac in (0.2, 0.6):
                D = frac * dm
                joint = n * vec_cost(Sv, Q, H, SU, alpha, D)
                split = n * sc.solve(blocks, wts, alpha, D)["cost"]
                worst = min(worst, joint - (split - alpha * cT - (1 - alpha) * cTS))
                cases += 1
    report("blocks_lemma", worst > -1e-8, min_margin=float(worst), cases=cases)

    # ---------------------------------------------------------------- Lemma coupling
    worst = np.inf
    cases = 0
    for (p, n) in [(1, 6), (2, 4), (1, 10), (2, 5)]:
        Gm = rng.standard_normal((n * p, n * p))
        Sp = Gm @ Gm.T / (n * p) + 0.3 * np.eye(n * p)
        Em = rng.standard_normal((n * p, n * p))
        Sv = Sp + 0.08 * Em @ Em.T / (n * p)
        F = rng.standard_normal((1, p))
        Q = F.T @ F + 0.1 * np.eye(p)
        H = rng.standard_normal((1, p))
        SU = np.array([[0.6]])
        J = H.T @ np.linalg.solve(SU, H)
        dQ = float(np.trace(np.kron(np.eye(n), Q) @ (Sv - Sp))) / n
        dJ = float(np.trace(np.kron(np.eye(n), J) @ (Sv - Sp))) / (2 * n * LN2)
        dm = float(np.trace(np.kron(np.eye(n), Q) @ Sp)) / n
        for alpha in (0.0, 0.4, 1.0):
            for frac in (0.2, 0.6):
                D = frac * dm
                lhs = vec_cost(Sv, Q, H, SU, alpha, D + dQ)
                rhs = vec_cost(Sp, Q, H, SU, alpha, D) + (1 - alpha) * dJ
                worst = min(worst, rhs - lhs)
                cases += 1
    report("coupling_lemma", worst > -1e-8, min_margin=float(worst), cases=cases)

    # ---------------------------------------------------------------- Corollary lsavg
    worst = np.inf
    cases = 0
    rows = []
    for src in (source_scalar(), source_vector()):
        dm = src.dmax()
        G, W = 16, 32
        blocks = []
        for k in range(W):
            w = 2 * np.pi * k / W
            Sbar = sum(src.sigma((j + 0.5) / G, w) for j in range(G)) / G
            Rb = sc.psd_sqrt(Sbar)
            blocks.append((sc.herm(Rb @ src.Q @ Rb), src.H @ Rb, src.SU.astype(complex)))
        for alpha in (0.0, 0.5, 1.0):
            for frac in (0.1, 0.35, 0.7):
                D = frac * dm
                vbar = sc.solve(blocks, np.full(W, 1.0 / W), alpha, D)["cost"]
                vl = v_ls(src, alpha, D, G=G, W=W)
                worst = min(worst, vbar - vl)
                rows.append(dict(p=src.p, alpha=alpha, D_over_Dmax=frac, v_ls=vl, v_averaged=vbar))
                cases += 1
    report("averaged", worst > -1e-9, min_saving=float(worst),
           max_saving=max(r["v_averaged"] - r["v_ls"] for r in rows), cases=cases, table=rows)

    OUT["_meta"] = dict(seed=SEED, numpy=np.__version__, failed=FAILED, seconds=round(time.time() - t0, 1))
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(OUT, open(os.path.join(here, "verify_ls.json"), "w"), indent=1)
    print(f"{len(OUT) - 1 - len(FAILED)} passed, {len(FAILED)} failed, {OUT['_meta']['seconds']} s")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
