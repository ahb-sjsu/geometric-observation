"""F2 shakedown v2 — mixture-drift dial, redesigned per the fixes
recorded in FAMILIES-CRUCIBLE-3.md's status block. No bars, no
evidential weight; interior evidence only.

Changes from v1: drift = normalized operator Frobenius distance
(linear in tau by construction, vs the saturating top-8 subspace
measure); tau log-spaced near zero where v1 showed the action is;
lever hardened to 1.5 bits/dim and graded on both top-10 overlap and
top-1 flip damage.

    .venv/Scripts/python crucible/fam2_shakedown_v2.py
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
BITS = 1.5
N_PROBE_CELLS = 24
N_Q = 100
TAUS = [0.0, 0.01, 0.03, 0.06, 0.125, 0.25, 0.5, 1.0]
N_RESAMPLE = 10
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "FAM2-shakedown-v2.json")

sys.path.insert(0, HERE)
from ot11_check import quantize_against, margin_consumer  # noqa: E402


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


def damages(queries, fp_index, q_index):
    d10 = d1 = 0.0
    for q in queries:
        r_fp = np.argsort(-(fp_index @ q))
        r_q = np.argsort(-(q_index @ q))
        d10 += 1 - len(set(r_fp[:10]) & set(r_q[:10])) / 10
        d1 += float(r_fp[0] != r_q[0])
    n = len(queries)
    return d10 / n, d1 / n


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

    ops = {}
    for t in TAUS:
        ops[t] = probe_operator(stratum(t, SEED + int(t * 10000)), index)
        print(f"probed tau={t}", flush=True)

    p0 = ops[0.0]
    n0 = np.linalg.norm(p0)
    drift = {t: float(np.linalg.norm(ops[t] - p0) / n0) for t in TAUS}

    stale = quantize_against(index, p0, BITS)
    fresh1 = quantize_against(index, ops[1.0], BITS)
    s10, s1, f10, f1 = [], [], [], []
    for i in range(N_RESAMPLE):
        qres = stratum(1.0, SEED + 5000 + i)
        a, b = damages(qres, index, stale)
        c, d = damages(qres, index, fresh1)
        s10.append(a)
        s1.append(b)
        f10.append(c)
        f1.append(d)
    s10, s1 = np.array(s10), np.array(s1)
    f10, f1 = np.array(f10), np.array(f1)

    nz = [t for t in TAUS if t > 0]
    dr = [drift[t] for t in nz]
    rho = float(stats.spearmanr(nz, dr).statistic)
    rng_ratio = max(dr) / max(min(dr), 1e-12)
    interior = sum(0.1 * max(dr) < d_ < 0.9 * max(dr) for d_ in dr)
    lev10 = float(s10.mean() - f10.mean())
    lev1 = float(s1.mean() - f1.mean())
    n10, n1 = float(s10.std()), float(s1.std())
    for t in TAUS:
        print(f"tau={t:>6}: drift={drift[t]:.4f}")
    print(f"\nmonotonicity spearman(drift, tau) = {rho:.3f} (want >=0.9)")
    print(f"drift range ratio = {rng_ratio:.1f}x (want >=3)")
    print(f"interior strata (10-90% of max) = {interior} (want >=4)")
    print(f"lever top-10: stale-fresh {lev10:+.4f}, noise {n10:.4f} "
          f"-> {lev10 / max(n10, 1e-12):+.1f}x (want >=3)")
    print(f"lever top-1:  stale-fresh {lev1:+.4f}, noise {n1:.4f} "
          f"-> {lev1 / max(n1, 1e-12):+.1f}x (want >=3)")
    json.dump({"family": "F2-v2", "seed": SEED,
               "drift": {str(t): round(drift[t], 4) for t in TAUS},
               "spearman_tau": rho, "range_ratio": rng_ratio,
               "interior_strata": interior,
               "lever_top10": lev10, "noise_top10": n10,
               "lever_top1": lev1, "noise_top1": n1},
              open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}  (shakedown, no verdict)")


if __name__ == "__main__":
    main()
