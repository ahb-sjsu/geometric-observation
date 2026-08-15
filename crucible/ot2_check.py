"""OT-2: the change-of-measure loading law, constants per
PREREG-OT2-APPENDIX.md.

    .venv/Scripts/python crucible/ot2_check.py
"""

from __future__ import annotations

import json
import os

import numpy as np
from scipy import stats

SEED = 20260815
D = 32
EPS = 0.05
N = 400_000
ALPHAS = [0, 15, 30, 45, 60, 75, 90]
OFF1, OFF2 = -1.0, 0.5
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "OT2-loading-law.json")


def grads(xs, a1, a2):
    """Analytic gradient rows of C(x) = tanh(a1.x+OFF1) + tanh(a2.x+OFF2)."""
    f1 = 1 - np.tanh(xs @ a1 + OFF1) ** 2
    f2 = 1 - np.tanh(xs @ a2 + OFF2) ** 2
    return f1[:, None] * a1[None, :] + f2[:, None] * a2[None, :]


def mean_operator(xs, a1, a2):
    g = grads(xs, a1, a2)
    return g.T @ g / len(xs)


def run(eps, rng_base):
    q, _ = np.linalg.qr(rng_base.normal(size=(D, 3)))
    a1, a2, b = q[:, 0], q[:, 1], q[:, 2]
    xs = rng_base.normal(size=(N, D))          # CRN base draws
    p_base = mean_operator(xs, a1, a2)
    e, p = [], []
    for al in ALPHAS:
        t = np.deg2rad(al)
        u = np.cos(t) * a1 + np.sin(t) * b
        e.append(float(np.linalg.norm(
            mean_operator(xs + eps * u[None, :], a1, a2) - p_base)))
        # law's prediction under the BASE measure only: eps*||E[h * A]||_F
        g = grads(xs, a1, a2)
        h = xs @ u
        p.append(float(eps * np.linalg.norm((g * h[:, None]).T @ g / N)))
    return np.array(e), np.array(p), (a1, a2, b, xs)


def main():
    rng = np.random.default_rng(SEED)
    e, p, (a1, a2, b, xs) = run(EPS, rng)
    ratio_dev = float(np.max(np.abs(e / e[0] - p / p[0])))
    b1 = ratio_dev <= 0.08
    orth = float(e[-1] / e[0])
    b2 = orth <= 0.10
    rho = float(stats.spearmanr(e, p).statistic)
    spread = float(e.max() / e.min())
    b3 = rho >= 0.95 and spread >= 5
    rel0 = float(abs(e[0] - p[0]) / e[0])
    rng2 = np.random.default_rng(SEED)
    e2, p2, _ = run(EPS / 2, rng2)
    rel0_half = float(abs(e2[0] - p2[0]) / e2[0])
    b4 = rel0 <= 0.10 and rel0_half <= 0.7 * rel0

    print("alpha   e(alpha)      p(alpha)      e/e0     p/p0")
    for al, ev, pv in zip(ALPHAS, e, p):
        print(f"{al:>5}   {ev:.6e}  {pv:.6e}  {ev / e[0]:.4f}   "
              f"{pv / p[0]:.4f}")
    print(f"\nB1 shape dev {ratio_dev:.4f} (<=0.08) -> "
          f"{'PASS' if b1 else 'FAIL'}")
    print(f"B2 orthogonal ratio {orth:.4f} (<=0.10) -> "
          f"{'PASS' if b2 else 'FAIL'}")
    print(f"B3 spearman {rho:.3f} (>=0.95), spread {spread:.1f}x (>=5) -> "
          f"{'PASS' if b3 else 'FAIL'}")
    print(f"B4 rel err {rel0:.4f} (<=0.10), at eps/2 {rel0_half:.4f} "
          f"(<= 0.7x) -> {'PASS' if b4 else 'FAIL'}")

    # descriptive covariance-shift cell (no bar)
    cov_cells = {}
    for name, v in (("aligned_a1", a1), ("orthogonal_b", b)):
        xs_s = xs + (np.sqrt(1 + EPS) - 1) * np.outer(xs @ v, v)
        cov_cells[name] = float(np.linalg.norm(
            mean_operator(xs_s, a1, a2) - mean_operator(xs, a1, a2)))
    print(f"covariance shift (descriptive): {cov_cells}")

    ok = b1 and b2 and b3 and b4
    json.dump({"claim": "OT-2", "seed": SEED,
               "alphas": ALPHAS, "e": e.tolist(), "p": p.tolist(),
               "B1": bool(b1), "ratio_dev": ratio_dev,
               "B2": bool(b2), "orth_ratio": orth,
               "B3": bool(b3), "spearman": rho, "spread": spread,
               "B4": bool(b4), "rel0": rel0, "rel0_half": rel0_half,
               "cov_shift_descriptive": cov_cells,
               "verdict": "PASS" if ok else "FAIL"},
              open(OUT, "w"), indent=1)
    print(f"\nOT-2: {'PASS' if ok else 'FAIL'} -> "
          f"{os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
