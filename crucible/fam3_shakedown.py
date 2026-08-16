"""F3 shakedown — moment-matched transfer estimator (P2's debt), planted
stage with a probe-budget sweep. No bars, no evidential weight, per
FAMILIES-CRUCIBLE-3.md.

    .venv/Scripts/python crucible/fam3_shakedown.py
"""

from __future__ import annotations

import json
import os

import numpy as np

SEED = 20260816
D = 64
N_PROBES = (24, 48, 96)
N_TRUTH = 400_000
N_TRIALS = 20
OFF1, OFF2 = -1.0, 0.5
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "FAM3-shakedown.json")


def mean_operator(xs, a1, a2):
    f1 = 1 - np.tanh(xs @ a1 + OFF1) ** 2
    f2 = 1 - np.tanh(xs @ a2 + OFF2) ** 2
    g = f1[:, None] * a1[None, :] + f2[:, None] * a2[None, :]
    return g.T @ g / len(xs)


def rel(p, t):
    return float(np.linalg.norm(p - t) / np.linalg.norm(t))


def main():
    rng = np.random.default_rng(SEED)
    q, _ = np.linalg.qr(rng.normal(size=(D, 2)))
    a1, a2 = q[:, 0], q[:, 1]

    mu_a = 0.6 * rng.normal(size=D)
    m = rng.normal(size=(D, D)) / np.sqrt(D)
    cov_a = np.eye(D) * 0.4 + m @ m.T
    chol_a = np.linalg.cholesky(cov_a)

    truth = mean_operator(
        mu_a[None, :] + rng.normal(size=(N_TRUTH, D)) @ chol_a.T, a1, a2)

    budgets = {}
    for n_probe in N_PROBES:
        rows = []
        for trial in range(N_TRIALS):
            tr = np.random.default_rng(SEED + 100 + trial)
            p_iso = mean_operator(tr.normal(size=(n_probe, D)), a1, a2)
            cells = {"iso": rel(p_iso, truth)}
            for n_fit, tag in ((None, "matched_true_moments"),
                               (64, "matched_fit64")):
                if n_fit is None:
                    mu, ch = mu_a, chol_a
                else:
                    samp = mu_a[None, :] + tr.normal(
                        size=(n_fit, D)) @ chol_a.T
                    mu = samp.mean(axis=0)
                    cv = np.cov(samp.T) + 0.1 * (
                        np.trace(np.cov(samp.T)) / D) * np.eye(D)
                    ch = np.linalg.cholesky(cv)
                xs = mu[None, :] + tr.normal(size=(n_probe, D)) @ ch.T
                cells[tag] = rel(mean_operator(xs, a1, a2), truth)
            rows.append(cells)
        med = {k: float(np.median([r[k] for r in rows]))
               for k in rows[0]}
        budgets[n_probe] = {
            "median_err": med,
            "reduction_true": med["iso"] / med["matched_true_moments"],
            "reduction_fit64": med["iso"] / med["matched_fit64"]}
        print(f"n={n_probe:>3}: iso {med['iso']:.4f}  "
              f"matched {med['matched_true_moments']:.4f}  "
              f"fit64 {med['matched_fit64']:.4f}  "
              f"reductions {budgets[n_probe]['reduction_true']:.1f}x / "
              f"{budgets[n_probe]['reduction_fit64']:.1f}x")
    json.dump({"family": "F3", "seed": SEED,
               "budgets": {str(k): v for k, v in budgets.items()}},
              open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}  (shakedown, no verdict)")


if __name__ == "__main__":
    main()
