"""F1 shakedown — log-spread signal family (P5's debt). No bars, no
evidential weight: this run exists to show (or fail to show) the
family's interior, per FAMILIES-CRUCIBLE-3.md.

    .venv/Scripts/python crucible/fam1_shakedown.py
"""

from __future__ import annotations

import json
import os

import numpy as np

SEED = 20260816
D = 64
K = 16
TEMP = 1.0
N_PTS = 24
N_PAIRS = 30
N_DRAWS = 2000
BOOT_B = 200
M_STEPS = [10000, 3000, 1000, 300, 100, 30, 10, 3, 1]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "FAM1-shakedown.json")


def smooth_out(w, xs):
    s = xs @ w.T / TEMP
    s = s - s.max(axis=1, keepdims=True)
    e = np.exp(s)
    return e[:, 0] / e.sum(axis=1)


def main():
    rng = np.random.default_rng(SEED)
    w = rng.normal(size=(K, D))
    w /= np.linalg.norm(w, axis=1, keepdims=True)
    pts = rng.normal(size=(N_PTS, D))
    traces = np.logspace(-4, -1, N_PAIRS)
    draws = rng.normal(size=(N_DRAWS, D))

    # cache continuous outputs per (pair, codec): v0 (pts) and v_pert
    v0 = smooth_out(w, pts)
    cache = []
    for tr in traces:
        pair = []
        for _ in range(2):
            g = rng.normal(size=(D, 4))
            m = g @ g.T
            m *= tr / np.trace(m)
            cl = np.linalg.cholesky(m + 1e-15 * np.eye(D))
            deltas = draws @ cl.T
            vp = np.stack([smooth_out(w, x0[None, :] + deltas)
                           for x0 in pts])        # (24, 2000)
            pair.append(vp)
        cache.append(pair)

    rms = float(np.median(np.abs(np.concatenate(
        [(p - v0[:, None]).ravel() for pair in cache[len(cache) // 2:]
         for p in pair]))))
    steps = [m * rms for m in M_STEPS]
    print(f"reference rms={rms:.3e}")

    boot_idx = np.random.default_rng(SEED + 1).integers(
        0, N_DRAWS, (BOOT_B, N_DRAWS))

    rows = []
    for m_mult, step in zip(M_STEPS, steps):
        def q(v):
            return np.round(v / step) * step
        q0 = q(v0)
        n_inf = 0
        margins = []
        for pair in cache:
            dd = []
            per_draw = []
            for vp in pair:
                sq = (q(vp) - q0[:, None]) ** 2      # (24, 2000)
                per_draw.append(sq.mean(axis=0))     # (2000,)
                dd.append(float(sq.mean()))
            diff = dd[0] - dd[1]
            if diff == 0:
                continue
            n_inf += 1
            delta = per_draw[0] - per_draw[1]
            boots = delta[boot_idx].mean(axis=1)
            sd = float(boots.std())
            margins.append(abs(diff) / max(sd, 1e-300))
        margins = np.array(margins)
        frac = n_inf / N_PAIRS
        hi = float((margins >= 3).mean()) if n_inf else 0.0
        rows.append({"m_mult": m_mult, "informative_frac": round(frac, 3),
                     "share_margin_ge3": round(hi, 3),
                     "n_informative": n_inf})
        print(f"step={m_mult:>6}xrms: informative {n_inf}/30 "
              f"({frac:.2f})  margin>=3 share {hi:.2f}")

    interior = [r for r in rows if 0.10 < r["informative_frac"] < 0.90]
    straddle = [r for r in interior
                if 0.2 <= r["share_margin_ge3"] <= 0.8]
    print(f"\nINTERIOR EVIDENCE: {len(interior)} steps in (0.1,0.9) "
          f"(need >=4); {len(straddle)} of them straddle margin 3 "
          f"(need >=len(interior) with >=20% both sides)")
    json.dump({"family": "F1", "seed": SEED, "rms": rms, "rows": rows,
               "interior_steps": len(interior),
               "straddling_steps": len(straddle)},
              open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}  (shakedown, no verdict)")


if __name__ == "__main__":
    main()
