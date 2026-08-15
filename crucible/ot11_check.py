"""OT-11: feedback-free staleness, per PREREG-OT11-APPENDIX.md.

    .venv/Scripts/python crucible/ot11_check.py
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

SEED = 20260815
D = 768
SKETCH = 960
BITS = 3.0
N_PROBE_CELLS = 24
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "OT11-staleness.json")


def waterfill_bits(lam, budget, cap=12):
    lam = np.clip(np.asarray(lam, float), 1e-300, None)
    lo, hi = 1e-12 * lam.max(), max(lam.max(), 1e-12)
    for _ in range(200):
        th = np.sqrt(lo * hi)
        if np.clip(np.log2(lam / th), 0, cap).sum() < budget:
            hi = th
        else:
            lo = th
    b = np.clip(np.log2(lam / np.sqrt(lo * hi)), 0, cap)
    ib = np.floor(b).astype(int)
    rem = int(round(budget)) - int(ib.sum())
    if rem > 0:
        for i in np.argsort(-(b - ib))[:rem]:
            if ib[i] < cap:
                ib[i] += 1
    return ib


def quantize_against(k, m, bits_per_dim=BITS):
    d = k.shape[1]
    lam, v = np.linalg.eigh(m)
    lam, v = lam[::-1], v[:, ::-1]
    bits = waterfill_bits(lam, bits_per_dim * d)
    y = k @ v
    yq = np.empty_like(y)
    for i in range(d):
        col = y[:, i]
        if bits[i] < 1:
            yq[:, i] = col.mean()
            continue
        lo, hi = float(col.min()), float(col.max())
        if hi <= lo:
            yq[:, i] = col
            continue
        step = (hi - lo) / ((1 << int(bits[i])) - 1)
        yq[:, i] = np.round((col - lo) / step) * step + lo
    return yq @ v.T


def margin_consumer(q, corpus, j):
    others = np.delete(corpus, j, axis=0) @ q

    def c(x):
        return float(q @ x) - float(others.max())
    return c


def probe_operator(queries, corpus):
    p_hat = np.zeros((D, D))
    for qi in range(N_PROBE_CELLS):
        q = queries[qi]
        j = int(np.argmax(corpus @ q))
        pts = np.repeat(corpus[j][None, :], 4, axis=0)
        p_hat += blind_probe(margin_consumer(q, corpus, j), pts,
                             mode="lstsq", sketch_dim=SKETCH, eps=1e-3,
                             rng=np.random.default_rng(SEED + qi)).S
    return p_hat / N_PROBE_CELLS


def top10(q, corpus):
    return set(np.argsort(-(corpus @ q))[:10])


def damage(queries, fp_index, q_index):
    out = 0.0
    for q in queries:
        out += 1 - len(top10(q, fp_index) & top10(q, q_index)) / 10
    return out / len(queries)


def main():
    files = sorted(glob.glob(os.path.join(HERE, "ot6_data", "*.npy")))
    books = {os.path.basename(f)[:-4]: np.load(f).astype(np.float64)
             for f in files}
    names = sorted(books, key=lambda n: (not n.startswith("cs"), n))
    index = np.concatenate([books[n][:100] for n in names])
    strata = {n: books[n][100:] for n in names}
    t0 = names[0]

    ops = {n: probe_operator(strata[n], index) for n in names}

    def u8(p):
        return np.linalg.eigh(p)[1][:, -8:]
    u0 = u8(ops[t0])
    drift = {n: 1 - float(np.linalg.norm(u0.T @ u8(ops[n])) ** 2) / 8
             for n in names}

    stale_index = quantize_against(index, ops[t0])
    rows = []
    for n in names[1:]:
        fresh_index = quantize_against(index, ops[n])
        d_stale = damage(strata[n], index, stale_index)
        d_fresh = damage(strata[n], index, fresh_index)
        rows.append({"stratum": n, "drift": round(drift[n], 4),
                     "damage_stale": round(d_stale, 4),
                     "damage_fresh": round(d_fresh, 4)})
        print(f"{n:<12} drift={drift[n]:.4f}  stale={d_stale:.4f}  "
              f"fresh={d_fresh:.4f}")

    dr = [r["drift"] for r in rows]
    ds = [r["damage_stale"] for r in rows]
    dfr = [r["damage_fresh"] for r in rows]
    check = (max(dr) >= 2 * min(dr)) and (float(np.median(ds)) >= 0.02)
    rho = float(stats.spearmanr(ds, dr).statistic)
    s1 = rho >= 0.8
    med_drift = float(np.median(dr))
    high = [r for r in rows if r["drift"] > med_drift]
    s2a = all(r["damage_fresh"] <= r["damage_stale"] for r in high)
    reds = [1 - f / s if s > 0 else 0.0 for f, s in zip(dfr, ds)]
    med_red = float(np.median(reds))
    s2 = s2a and med_red >= 0.30
    verdict = "VOID" if not check else \
        ("PASS" if (s1 and s2) else "FAIL")
    print(f"\ncheck: drift range {min(dr):.4f}-{max(dr):.4f}, "
          f"median stale {np.median(ds):.4f} -> "
          f"{'ok' if check else 'VOID'}")
    print(f"S1 spearman(damage, drift) = {rho:.3f} (bar 0.8): "
          f"{'PASS' if s1 else 'FAIL'}")
    print(f"S2 fresh<=stale on high-drift: {s2a}; median reduction "
          f"{med_red:+.1%} (bar 30%): {'PASS' if s2 else 'FAIL'}")
    json.dump({"claim": "OT-11", "seed": SEED, "t0": t0, "rows": rows,
               "spearman": rho, "median_reduction": med_red,
               "verdict": verdict}, open(OUT, "w"), indent=1)
    print(f"\nOT-11: {verdict} -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
