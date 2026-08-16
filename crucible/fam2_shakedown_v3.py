"""F2 shakedown v3 — qualify the family's INTRINSIC dial, separating it
from probe-estimator noise (v2's confound: 24-cell blind probes have a
~0.5 Frobenius noise floor on a 768^2 operator, burying every stratum
except tau=1).

For the dot-margin consumer the operator is analytic (gradient = q), so
the family dial can be measured exactly: P(tau) = empirical mean qq^T
over the stratum's query sample. Estimator noise is then only the
query-sampling noise, measured directly by resampling. The lever is
re-tested at 1 bit/dim with 500-query evaluation.

No bars, no evidential weight.

    .venv/Scripts/python crucible/fam2_shakedown_v3.py
"""

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np
from scipy import stats

SEED = 20260816
D = 768
BITS = 1.0
TAUS = [0.0, 0.01, 0.03, 0.06, 0.125, 0.25, 0.5, 1.0]
N_RESAMPLE = 10
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "FAM2-shakedown-v3.json")

sys.path.insert(0, HERE)
from ot11_check import quantize_against  # noqa: E402


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

    def stratum(tau, n_q, seed):
        r = np.random.default_rng(seed)
        n_far = int(round(tau * n_q))
        qs = []
        if n_far < n_q:
            qs.append(cs_pool[r.choice(len(cs_pool),
                                       min(n_q - n_far, len(cs_pool)),
                                       replace=n_q - n_far > len(cs_pool))])
        if n_far:
            qs.append(de_pool[r.choice(len(de_pool), n_far,
                                       replace=False)])
        return np.concatenate(qs)

    def op(queries):
        return queries.T @ queries / len(queries)

    report = {}
    for n_q in (100, 400):
        p0 = op(stratum(0.0, n_q, SEED))
        n0 = np.linalg.norm(p0)
        # query-sampling noise floor: drift between two tau=0 redraws
        floor = float(np.median([
            np.linalg.norm(op(stratum(0.0, n_q, SEED + 77 + i)) - p0) / n0
            for i in range(5)]))
        drift = {t: float(np.linalg.norm(
            op(stratum(t, n_q, SEED + int(t * 10000) + 1)) - p0) / n0)
            for t in TAUS}
        nz = [t for t in TAUS if t > 0]
        dr = [drift[t] for t in nz]
        rho = float(stats.spearmanr(nz, dr).statistic)
        above = [t for t in nz if drift[t] > 2 * floor]
        sig = [drift[t] for t in above]
        rng_ratio = (max(sig) / min(sig)) if len(sig) >= 2 else 0.0
        interior = sum(0.1 * max(dr) < d_ < 0.9 * max(dr) for d_ in dr)
        report[n_q] = {"floor": floor, "drift": drift, "spearman": rho,
                       "strata_above_2floor": len(above),
                       "range_ratio_above_floor": rng_ratio,
                       "interior": interior}
        print(f"\nN_Q={n_q}: sampling floor={floor:.4f}")
        for t in TAUS:
            mark = " *" if t > 0 and drift[t] > 2 * floor else ""
            print(f"  tau={t:>6}: drift={drift[t]:.4f}{mark}")
        print(f"  spearman={rho:.3f}  above-floor strata={len(above)}  "
              f"range(above floor)={rng_ratio:.1f}x  interior={interior}")

    # lever at 1 bit/dim, 500-query evaluation
    p_stale = op(stratum(0.0, 400, SEED))
    p_fresh = op(stratum(1.0, 400, SEED + 3))
    stale = quantize_against(index, p_stale, BITS)
    fresh = quantize_against(index, p_fresh, BITS)
    s10, s1, f10, f1 = [], [], [], []
    for i in range(N_RESAMPLE):
        # 250-of-500 subsamples so the eval set genuinely varies
        # (drawing the full pool made the noise estimate zero by
        # construction in the first v3 run)
        qres = stratum(1.0, 250, SEED + 5000 + i)
        a, b = damages(qres, index, stale)
        c, d_ = damages(qres, index, fresh)
        s10.append(a)
        s1.append(b)
        f10.append(c)
        f1.append(d_)
    s10, s1, f10, f1 = map(np.array, (s10, s1, f10, f1))
    lev10 = float(s10.mean() - f10.mean())
    lev1 = float(s1.mean() - f1.mean())
    n10, n1 = float(s10.std()), float(s1.std())
    print(f"\nlever (1 bit/dim, 500-query eval, analytic operators):")
    print(f"  top-10: stale {s10.mean():.4f} fresh {f10.mean():.4f} "
          f"diff {lev10:+.4f} noise {n10:.4f} -> "
          f"{lev10 / max(n10, 1e-12):+.1f}x (want >=3)")
    print(f"  top-1:  stale {s1.mean():.4f} fresh {f1.mean():.4f} "
          f"diff {lev1:+.4f} noise {n1:.4f} -> "
          f"{lev1 / max(n1, 1e-12):+.1f}x (want >=3)")
    json.dump({"family": "F2-v3", "seed": SEED,
               "dial": {str(k): v for k, v in report.items()},
               "lever": {"bits": BITS, "top10": lev10, "noise10": n10,
                         "top1": lev1, "noise1": n1}},
              open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}  (shakedown, no verdict)")


if __name__ == "__main__":
    main()
