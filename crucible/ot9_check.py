"""OT-9: forward transfer across measures, per PREREG-OT9-APPENDIX.md.

    .venv/Scripts/python crucible/ot9_check.py
"""

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, r"C:\source\readscope")
from readscope.probe import jacobian_probe  # noqa: E402

SEED = 20260815
D = 128
K_DIRS = 160
P_STAR = 96
N_DIRECT = 96
N_SYN = 24
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "armH_data")
OUT = os.path.join(HERE, "..", "results", "OT9-forward-transfer.json")


def consumer_single(q, k):
    s = q @ k.T / np.sqrt(D)
    z_rest = np.exp(s).sum(axis=1) - np.exp(s[:, P_STAR])

    def f(key_vec):
        sp = q @ key_vec / np.sqrt(D)
        e = np.exp(sp)
        return e / (z_rest + e)
    return f


def rel_err(p, target):
    return float(np.linalg.norm(p - target) / np.linalg.norm(target))


def main():
    files = sorted(glob.glob(os.path.join(DATA, "*.npz")))
    rows = []
    for fi, path in enumerate(files):
        z = np.load(path)
        q, k = z["Q"], z["K"]
        f = consumer_single(q, k)
        rng = np.random.default_rng(SEED + fi)

        idx = rng.choice(len(k), size=N_DIRECT, replace=False)
        p_direct = jacobian_probe(f, k[idx], n_directions=K_DIRS,
                                  eps=1e-3,
                                  rng=np.random.default_rng(SEED)).S

        mu = k.mean(axis=0)
        sd = float(k.std())
        xs = mu[None, :] + rng.normal(scale=1.5 * sd, size=(N_SYN, D))
        p_syn = jacobian_probe(f, xs, n_directions=K_DIRS, eps=1e-3,
                               rng=np.random.default_rng(SEED)).S

        cov = np.cov(k.T) + 0.1 * (np.trace(np.cov(k.T)) / D) * np.eye(D)
        cov_inv = np.linalg.inv(cov)
        sign, logdet_a = np.linalg.slogdet(cov)
        logdet_p = D * np.log((1.5 * sd) ** 2)
        a_ops, logr = [], []
        for x in xs:
            a_ops.append(jacobian_probe(
                f, x[None, :], n_directions=K_DIRS, eps=1e-3,
                rng=np.random.default_rng(SEED)).S)
            dx = x - mu
            lq_a = -0.5 * (dx @ cov_inv @ dx) - 0.5 * logdet_a
            lq_p = -0.5 * (dx @ dx) / (1.5 * sd) ** 2 - 0.5 * logdet_p
            logr.append(lq_a - lq_p)
        logr = np.array(logr)
        w = np.exp(logr - logr.max())
        w /= w.sum()
        p_corr = sum(wi * ai for wi, ai in zip(w, a_ops))

        e_syn = rel_err(p_syn, p_direct)
        e_corr = rel_err(p_corr, p_direct)
        rows.append({"cell": os.path.basename(path),
                     "err_syn": round(e_syn, 4),
                     "err_corr": round(e_corr, 4),
                     "improved": bool(e_corr < e_syn),
                     "ess": round(float(1.0 / np.sum(w ** 2)), 1)})
        print(f"{os.path.basename(path):<24} syn={e_syn:.3f} "
              f"corr={e_corr:.3f} ess={rows[-1]['ess']:>5} "
              f"{'IMPROVED' if e_corr < e_syn else 'worse'}")

    med_syn = float(np.median([r["err_syn"] for r in rows]))
    floor = med_syn >= 0.05
    wins = sum(r["improved"] for r in rows)
    t1 = wins >= 10
    imps = [(r["err_syn"] - r["err_corr"]) / r["err_syn"] for r in rows]
    med_imp = float(np.median(imps))
    t2 = med_imp >= 0.25
    verdict = "VOID" if not floor else \
        ("PASS" if (t1 and t2) else "FAIL")
    print(f"\nfloor: median syn err {med_syn:.3f} "
          f"{'ok' if floor else 'VOID'}")
    print(f"T1 improved on {wins}/12 (bar 10): "
          f"{'PASS' if t1 else 'FAIL'}")
    print(f"T2 median improvement {med_imp:+.1%} (bar 25%): "
          f"{'PASS' if t2 else 'FAIL'}")
    json.dump({"claim": "OT-9", "seed": SEED, "rows": rows,
               "median_err_syn": med_syn, "wins": wins,
               "median_improvement": med_imp, "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"\nOT-9: {verdict} -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
