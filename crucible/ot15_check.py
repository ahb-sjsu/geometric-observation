"""OT-15: forward transfer by moment-matched probing on real heads,
constants per PREREG-OT15-APPENDIX.md. Refuses to run until the
appendix is SEALED.

    .venv/Scripts/python crucible/ot15_check.py
"""

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, r"C:\source\readscope")
from readscope.probe import jacobian_probe  # noqa: E402

SEED = 20260817
D = 128
K_DIRS = 160
EPS = 1e-3
P_STAR = 96
N_TARGET = 96
N_FIT = 64
N_PROBES = (48, 96)
N_GRADED = 48
N_TRIALS = 10
RIDGE = 0.1
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "armH_data")
OUT = os.path.join(HERE, "..", "results", "OT15-moment-transfer.json")
APPENDIX = os.path.join(HERE, "PREREG-OT15-APPENDIX.md")


def require_seal():
    text = open(APPENDIX, encoding="utf-8").read()
    if "STATUS: DRAFT-UNSEALED" in text or "STATUS: SEALED" not in text:
        sys.exit("REFUSED: PREREG-OT15-APPENDIX.md is not SEALED. "
                 "Per OT-CRUCIBLE-3.md no run may execute before a "
                 "dated seal declaration in a later working session.")


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


def probe_at(f, xs):
    return jacobian_probe(f, xs, n_directions=K_DIRS, eps=EPS,
                          rng=np.random.default_rng(SEED)).S


def fitted(samp):
    mu = samp.mean(axis=0)
    cv = np.cov(samp.T)
    cv = cv + RIDGE * (np.trace(cv) / D) * np.eye(D)
    return mu, np.linalg.cholesky(cv)      # MC2: chol must succeed


def main():
    require_seal()
    files = sorted(glob.glob(os.path.join(DATA, "*.npz")))
    rows = []
    for fi, path in enumerate(files):
        z = np.load(path)
        q, k = z["Q"], z["K"]
        f = consumer_single(q, k)
        rng = np.random.default_rng(SEED + fi)
        idx = rng.choice(len(k), size=N_TARGET, replace=False)
        target = probe_at(f, k[idx])
        mu_full, ch_full = fitted(k)

        cell = {"cell": os.path.basename(path)}
        for n_probe in N_PROBES:
            errs = {"iso": [], "matched": [], "full": []}
            for trial in range(N_TRIALS):
                tr = np.random.default_rng(
                    SEED + 100 * (fi + 1) + trial)
                samp = k[tr.choice(len(k), size=N_FIT, replace=False)]
                mu, ch = fitted(samp)
                sd = float(samp.std())
                # equal information, equal budget; geometry differs
                errs["iso"].append(rel_err(probe_at(
                    f, mu[None, :] + tr.normal(
                        scale=1.5 * sd, size=(n_probe, D))), target))
                errs["matched"].append(rel_err(probe_at(
                    f, mu[None, :] + tr.normal(
                        size=(n_probe, D)) @ ch.T), target))
                errs["full"].append(rel_err(probe_at(
                    f, mu_full[None, :] + tr.normal(
                        size=(n_probe, D)) @ ch_full.T), target))
            for arm, es in errs.items():
                cell[f"{arm}{n_probe}"] = round(
                    float(np.median(es)), 4)
        cell["win48"] = bool(cell["matched48"] < cell["iso48"])
        cell["ratio48"] = round(
            cell["iso48"] / max(cell["matched48"], 1e-12), 3)
        rows.append(cell)
        print(f"{cell['cell']:<24} iso={cell['iso48']:.3f} "
              f"matched={cell['matched48']:.3f} "
              f"full={cell['full48']:.3f} "
              f"ratio={cell['ratio48']:.2f}x "
              f"{'WIN' if cell['win48'] else 'loss'}")

    med_iso = float(np.median([r["iso48"] for r in rows]))
    mc1 = med_iso >= 0.05
    wins = sum(r["win48"] for r in rows)
    b1 = wins >= 10
    med_ratio = float(np.median([r["ratio48"] for r in rows]))
    b2 = med_ratio >= 1.5
    verdict = "VOID" if not mc1 else \
        ("PASS" if (b1 and b2) else "FAIL")

    print(f"\nMC1 room to improve (median iso err {med_iso:.3f}, "
          f"floor 0.05): {'ok' if mc1 else 'VOID'}")
    print(f"B1 wins {wins}/12 (bar 10): {'PASS' if b1 else 'FAIL'}")
    print(f"B2 median ratio {med_ratio:.2f}x (bar 1.5x): "
          f"{'PASS' if b2 else 'FAIL'}")
    json.dump({"claim": "OT-15", "seed": SEED, "rows": rows,
               "median_iso48": med_iso, "wins48": wins,
               "median_ratio48": med_ratio,
               "MC1": bool(mc1), "B1": bool(b1), "B2": bool(b2),
               "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"\nOT-15: {verdict} -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
