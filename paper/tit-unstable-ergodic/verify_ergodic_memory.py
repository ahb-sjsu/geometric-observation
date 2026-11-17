"""Numerical checks for the extension of Theorem 18 (numbered 14 before 2026-11-16; vector sources driven by a totally
uniquely ergodic map) to a holder with memory, paper-four draft.

Source: that of verify_vector_ergodic.py (R^2, driven by the rotation by the golden mean,
range of correlation m = 1, floor a = 0.2), extended to all integer times. Holder with
memory m_h = 1: S_t = H0 T_t + H1 T_{t-1} + U_t, H0 = (1, 0.5), H1 = (0.4, -0.3), U white
with variance 1; weight Q = I.

Quantities (bits per symbol), at alpha in {0, 0.5, 1} and D = 0.3 Dmax:
  W(N, th0)  window cost (1/N) V_G(alpha, N D; Gamma_N(th0), J_N) of the window T_1..T_N
             against the holder's observations S_1..S_N. S_1 involves T_0, which lies
             before the window; it is written as H1 E[T_0 | T^N] plus independent noise
             H1 (T_0 - E[T_0 | T^N]) + U_1, so the holder is a linear map of the window in
             Gaussian noise that is not white in its first coordinate.
             th0 in {0, .25, .5, .75}, N in {50, 100, 200, 400}.
  V_n        frozen-block program with the interior holder of a block of n symbols (its
             observations at the block's times 2..n, which involve only the block),
             int (1/n) V_G(alpha, n D(th); Gamma_n(th), J'_n) d th under one budget, on a
             grid of 64 phases, n in {4, 8, 16, 32, 64}.
Pass criteria (written before the first run, 2026-11-16):
  monotone: V_n (n = 4, ..., 64) and the phase mean of W(N) (N = 50, ..., 400) are
    decreasing, at each alpha;
  common_limit: the extrapolations 2 V_64 - V_32 and 2 W(400) - W(200) (phase means)
    differ by at most 1e-3 bits, at each alpha;
  phase_spread: the spread of W over the four phases at N = 400 is at most half of that
    at N = 100, at each alpha.
Recorded without a criterion: the same frozen programs with the memoryless holder H0
(memory ignored) at n = 64, to show that the memory changes the costs.

Usage: python verify_ergodic_memory.py [out.json]

Record of the first run (2026-11-16, local Windows machine, python 3.12.2, numpy 2.5.2,
OPENBLAS_NUM_THREADS=3, 2642 s): verify_ergodic_memory.json, all nine checks passed.
Before that run, and after the criteria above were in this file, a timing test computed
W(50) and W(100) at phase 0 and V_4, V_8 at alpha = 0.5, and one scalar conversion in
window_block was fixed. After the run only this docstring changed. Note: W here is the
window cost against all the observations of the window, the J_N named above being that of
the whole observation with T_0 projected out; Theorem 18 states its window cost against
the interior observations (times 2..N), which has the same limit by the remark after the
theorem.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify_vector_ergodic as ve  # noqa: E402  (sets the solver tolerances)

sc = ve.sc
H0 = np.array([[1.0, 0.5]])
H1 = np.array([[0.4, -0.3]])
Q = ve.Q


def holder_rows(n, first):
    """Rows t = first..n (1-based) of the map T^n -> sum_j H_j T_{t-j}, within the window."""
    rows = []
    for t in range(first, n + 1):
        r = np.zeros((1, 2 * n))
        r[:, 2 * (t - 1):2 * t] = H0
        if t >= 2:
            r[:, 2 * (t - 2):2 * (t - 1)] = H1
        rows.append(r)
    return np.vstack(rows) if rows else np.zeros((0, 2 * n))


def window_block(N, th0):
    Gb = ve.gamma(N + 1, (th0 - ve.G_ROT) % 1.0)        # covariance of T_0, ..., T_N
    G = Gb[2:, 2:]
    c0 = Gb[:2, 2:]
    Gi = np.linalg.inv(G)
    K = c0 @ Gi                                           # E[T_0 | T^N] = K T^N
    Ce = Gb[:2, :2] - c0 @ Gi @ c0.T                       # Cov(T_0 - E[T_0 | T^N])
    Hm = holder_rows(N, 1)
    Hm[0:1, :] += H1 @ K
    Sn = np.eye(N)
    Sn[0, 0] += float((H1 @ Ce @ H1.T)[0, 0])
    R = np.real(sc.psd_sqrt(G))
    return (sc.herm(R @ np.kron(np.eye(N), Q) @ R), Hm @ R, Sn)


def frozen_block(n, th, interior=True):
    G = ve.gamma(n, th)
    R = np.real(sc.psd_sqrt(G))
    Hm = holder_rows(n, 2) if interior else np.kron(np.eye(n), H0)
    return (sc.herm(R @ np.kron(np.eye(n), Q) @ R), Hm @ R, np.eye(Hm.shape[0]))


def window_cost(N, th0, alpha, D):
    return sc.solve([window_block(N, th0)], [1.0 / N], alpha, D)["cost"]


def frozen_cost(n, alpha, D, grid=64, interior=True):
    ths = (np.arange(grid) + 0.5) / grid
    blocks = [frozen_block(n, t, interior) for t in ths]
    return sc.solve(blocks, np.full(grid, 1.0 / (grid * n)), alpha, D)["cost"]


def main(path=None):
    t0 = time.time()
    ths = (np.arange(4096) + 0.5) / 4096
    dmax = float(np.mean([np.trace(Q @ (ve.Amat(t) @ ve.R0 @ ve.Amat(t).T)) + 2 * ve.A_FLOOR for t in ths]))
    D = 0.3 * dmax
    Ns = [50, 100, 200, 400]
    phases = [0.0, 0.25, 0.5, 0.75]
    ns = [4, 8, 16, 32, 64]
    rows, fails = {}, 0
    for alpha in (0.0, 0.5, 1.0):
        W = {N: [window_cost(N, p, alpha, D) for p in phases] for N in Ns}
        V = {n: frozen_cost(n, alpha, D) for n in ns}
        V_memoryless = frozen_cost(64, alpha, D, interior=False)
        mW = {N: float(np.mean(W[N])) for N in Ns}
        spread = {N: max(W[N]) - min(W[N]) for N in Ns}
        mono = all(V[a] > V[b] for a, b in zip(ns, ns[1:])) and all(mW[a] > mW[b] for a, b in zip(Ns, Ns[1:]))
        exV, exW = 2 * V[64] - V[32], 2 * mW[400] - mW[200]
        lim = abs(exV - exW) <= 1e-3
        ph = spread[400] <= spread[100] / 2
        fails += (not mono) + (not lim) + (not ph)
        rows[str(alpha)] = {"W": {str(k): v for k, v in W.items()}, "V": {str(k): v for k, v in V.items()},
                            "V64_memoryless_holder_H0": V_memoryless,
                            "extrapolated_V": exV, "extrapolated_W": exW,
                            "spread": {str(k): v for k, v in spread.items()},
                            "ok": {"monotone": bool(mono), "common_limit": bool(lim), "phase_spread": bool(ph)}}
        print(f"alpha={alpha:.1f} V_n {[round(V[n], 5) for n in ns]} | mean W {[round(mW[N], 5) for N in Ns]} | "
              f"extrap V {exV:.5f} W {exW:.5f} | spread {[f'{spread[N]:.1e}' for N in Ns]} | "
              f"memoryless V64 {V_memoryless:.5f} | {rows[str(alpha)]['ok']}", flush=True)
    if path is None:
        path = os.path.join(HERE, "verify_ergodic_memory.json")
    with open(path, "w") as fh:
        json.dump({"D": D, "Dmax": dmax, "rows": rows,
                   "_meta": {"failed": int(fails), "seconds": round(time.time() - t0, 1),
                             "numpy": np.__version__}}, fh, indent=1)
    print("FAILED CHECKS:", fails)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
