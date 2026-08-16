"""F2 shakedown — mixture-drift dial (P4's debt). No bars, no
evidential weight; interior evidence only, per FAMILIES-CRUCIBLE-3.md.

    .venv/Scripts/python crucible/fam2_shakedown.py
"""

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, r"C:\source\readscope")
from readscope.probe import blind_probe  # noqa: E402

SEED = 20260816
D = 768
SKETCH = 960
BITS = 2.0
N_PROBE_CELLS = 24
N_Q = 100
TAUS = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0]
N_RESAMPLE = 10
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "FAM2-shakedown.json")

sys.path.insert(0, HERE)
from ot11_check import (quantize_against, margin_consumer,  # noqa: E402
                        top10, damage)


def probe_operator(queries, corpus):
    p_hat = np.zeros((D, D))
    for qi in range(N_PROBE_CELLS):
        q = queries[qi % len(queries)]
        j = int(np.argmax(corpus @ q))
        pts = np.repeat(corpus[j][None, :], 4, axis=0)
        p_hat += blind_probe(margin_consumer(q, corpus, j), pts,
                             mode="lstsq", sketch_dim=SKETCH, eps=1e-3,
                             rng=np.random.default_rng(SEED + qi)).S
    return p_hat / N_PROBE_CELLS


def main():
    files = sorted(glob.glob(os.path.join(HERE, "ot6_data", "*.npy")))
    books = {os.path.basename(f)[:-4]: np.load(f).astype(np.float64)
             for f in files}
    names = sorted(books, key=lambda n: (not n.startswith("cs"), n))
    index = np.concatenate([books[n][:100] for n in names])
    cs_pool = books[names[0]][100:]
    de_pool = np.concatenate([books[n][100:] for n in names[1:]])

    def stratum(tau, seed):
        r = np.random.default_rng(seed)
        n_far = int(round(tau * N_Q))
        qs = []
        if n_far < N_Q:
            qs.append(cs_pool[r.choice(len(cs_pool), N_Q - n_far,
                                       replace=False)])
        if n_far:
            qs.append(de_pool[r.choice(len(de_pool), n_far,
                                       replace=False)])
        return np.concatenate(qs)

    ops = {t: probe_operator(stratum(t, SEED + int(t * 1000)), index)
           for t in TAUS}

    def u8(p):
        return np.linalg.eigh(p)[1][:, -8:]
    u0 = u8(ops[0.0])
    drift = {t: 1 - float(np.linalg.norm(u0.T @ u8(ops[t])) ** 2) / 8
             for t in TAUS}

    stale = quantize_against(index, ops[0.0], BITS)
    fresh1 = quantize_against(index, ops[1.0], BITS)
    d_stale, d_fresh = [], []
    for i in range(N_RESAMPLE):
        qres = stratum(1.0, SEED + 5000 + i)
        d_stale.append(damage(qres, index, stale))
        d_fresh.append(damage(qres, index, fresh1))
    d_stale, d_fresh = np.array(d_stale), np.array(d_fresh)

    nz = [t for t in TAUS if t > 0]
    dr = [drift[t] for t in nz]
    rho = float(stats.spearmanr(nz, dr).statistic)
    rng_ratio = max(dr) / max(min(dr), 1e-12)
    interior = sum(0.1 * max(dr) < d < 0.9 * max(dr) for d in dr[:-1])
    spread = float(d_stale.mean() - d_fresh.mean())
    noise = float(d_stale.std())
    for t in TAUS:
        print(f"tau={t:>5}: drift={drift[t]:.4f}")
    print(f"\nmonotonicity spearman(drift, tau) = {rho:.3f} (want >=0.9)")
    print(f"drift range ratio = {rng_ratio:.1f}x (want >=3)")
    print(f"interior strata (10-90% of max drift) = {interior} (want >=4)")
    print(f"resolvability at tau=1: stale-fresh = {spread:.4f}, "
          f"resample std = {noise:.4f} -> ratio "
          f"{spread / max(noise, 1e-12):.1f}x (want >=3)")
    json.dump({"family": "F2", "seed": SEED,
               "drift": {str(t): round(drift[t], 4) for t in TAUS},
               "spearman_tau": rho, "range_ratio": rng_ratio,
               "interior_strata": interior,
               "stale_minus_fresh": spread, "resample_std": noise},
              open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}  (shakedown, no verdict)")


if __name__ == "__main__":
    main()
