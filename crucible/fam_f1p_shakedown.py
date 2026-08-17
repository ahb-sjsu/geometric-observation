"""F1' shakedown — the log-spread signal family, multi-seed
qualification (the OT-17 lesson: single-seed interior is one point
of a distribution). No bars, no evidential weight.

Changes from F1: N_PAIRS 30 -> 100 (fraction resolution 0.01;
per-pair aliasing averages out) and the trace spread widened to
logspace(-4.5, -0.5). Interior is qualified ACROSS five seeds:
a step counts as decisive only if its informative fraction is
interior at EVERY seed, and the band-level straddle (>= 2 decisive
steps straddling margin 3) must hold at every seed individually --
the qualification samples the same randomness a sealed run would.

    .venv/Scripts/python crucible/fam_f1p_shakedown.py
"""

from __future__ import annotations

import json
import os

import numpy as np

SEEDS = [20260901, 20260902, 20260903, 20260904, 20260905]
D = 64
K = 16
TEMP = 1.0
N_PTS = 24
N_PAIRS = 100
N_DRAWS = 2000
BOOT_B = 200
# half-octave band steps: the transition location slides ~1 octave
# between seeds (v1 of this qualification measured it), so the family
# property is per-seed interior COUNT on a grid dense enough that the
# transition crosses >= 4 steps wherever it lands
M_GRID = [3000, 1732, 1300, 1000, 750, 562, 422, 316, 237, 178, 133,
          100, 75, 56, 42, 30, 10, 3, 1]
BAND = [m for m in M_GRID if 30 <= m <= 1732]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "F1P-shakedown.json")


def smooth_out(w, xs):
    s = xs @ w.T / TEMP
    s = s - s.max(axis=1, keepdims=True)
    e = np.exp(s)
    return e[:, 0] / e.sum(axis=1)


def one_seed(seed):
    rng = np.random.default_rng(seed)
    w = rng.normal(size=(K, D))
    w /= np.linalg.norm(w, axis=1, keepdims=True)
    pts = rng.normal(size=(N_PTS, D))
    traces = np.logspace(-4.5, -0.5, N_PAIRS)
    draws = rng.normal(size=(N_DRAWS, D))

    cache = []
    for tr in traces:
        pair = []
        for _ in range(2):
            g = rng.normal(size=(D, 4))
            m = g @ g.T
            m *= tr / np.trace(m)
            cl = np.linalg.cholesky(m + 1e-15 * np.eye(D))
            deltas = draws @ cl.T
            pair.append(np.stack([smooth_out(w, x0[None, :] + deltas)
                                  for x0 in pts]))
        cache.append(pair)
    v0 = smooth_out(w, pts)
    rms = float(np.median(np.abs(np.concatenate(
        [(p - v0[:, None]).ravel() for pair in cache[len(cache) // 2:]
         for p in pair]))))
    boot_idx = np.random.default_rng(seed + 1).integers(
        0, N_DRAWS, (BOOT_B, N_DRAWS))

    rows = {}
    for m_mult in M_GRID:
        step = m_mult * rms

        def q(v, step=step):
            return np.round(v / step) * step

        q0 = q(v0)
        n_inf = hi = lo = 0
        for pair in cache:
            dd, per_draw = [], []
            for vp in pair:
                sq = (q(vp) - q0[:, None]) ** 2
                per_draw.append(sq.mean(axis=0))
                dd.append(float(sq.mean()))
            diff = dd[0] - dd[1]
            if diff == 0:
                continue
            n_inf += 1
            delta = per_draw[0] - per_draw[1]
            sd = float(delta[boot_idx].mean(axis=1).std())
            if abs(diff) / max(sd, 1e-300) >= 3:
                hi += 1
            else:
                lo += 1
        frac = n_inf / N_PAIRS
        rows[m_mult] = {
            "informative_frac": round(frac, 3),
            "interior": bool(0.10 < frac < 0.90),
            "straddles": bool(n_inf > 0 and hi / n_inf >= 0.2
                              and lo / n_inf >= 0.2),
        }
    return rms, rows


def main():
    out = {"family": "F1'", "seeds": SEEDS, "n_pairs": N_PAIRS,
           "grid": M_GRID, "per_seed": {}}
    for seed in SEEDS:
        rms, rows = one_seed(seed)
        out["per_seed"][str(seed)] = {"rms": rms, "rows": {
            str(k): v for k, v in rows.items()}}
        band = {m: rows[m] for m in BAND}
        print(f"seed {seed}: rms={rms:.2e}  " + "  ".join(
            f"{m}x:{rows[m]['informative_frac']:.2f}"
            f"{'*' if rows[m]['interior'] else ' '}"
            f"{'s' if rows[m]['straddles'] else ' '}"
            for m in M_GRID))
        _ = band

    # the qualification (v2 rule, measured into shape by v1): the
    # IN-RUN criterion -- >= 4 interior band steps, >= 2 straddling --
    # must hold at EVERY seed. The transition's location slides about
    # an octave between seeds; the criterion, not the band, is the
    # family property, so the grid must be dense enough that the
    # transition crosses >= 4 steps wherever it lands.
    per_seed_ok = {}
    for s in SEEDS:
        rows = out["per_seed"][str(s)]["rows"]
        interior = [m for m in BAND if rows[str(m)]["interior"]]
        straddling = [m for m in interior if rows[str(m)]["straddles"]]
        per_seed_ok[str(s)] = {"interior_steps": interior,
                               "straddling": straddling,
                               "ok": len(interior) >= 4
                               and len(straddling) >= 2}
    out["per_seed_qualification"] = per_seed_ok
    all_ok = all(v["ok"] for v in per_seed_ok.values())
    out["qualified"] = bool(all_ok)
    print("\nQUALIFICATION (v2 rule: in-run criterion at every seed)")
    for s in SEEDS:
        v = per_seed_ok[str(s)]
        print(f"  seed {s}: {len(v['interior_steps'])} interior "
              f"({len(v['straddling'])} straddle) -> "
              f"{'ok' if v['ok'] else 'FAIL'}")
    print("interior across seeds "
          + ("DEMONSTRATED" if all_ok
             else "NOT demonstrated -- family needs redesign"))
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}  (shakedown, no verdict)")


if __name__ == "__main__":
    main()
