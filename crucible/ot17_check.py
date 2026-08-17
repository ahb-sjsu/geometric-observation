"""OT-17: the two floor curves, fourth campaign, constants per
PREREG-OT17-APPENDIX.md — OT-13 v2's instrument verbatim, fresh seed,
band-level straddle MC. Refuses to run until the appendix is SEALED.

    .venv/Scripts/python crucible/ot17_check.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, r"C:\source\readscope")
from readscope.probe import blind_probe  # noqa: E402

SEED = 20260819
D = 64
K = 16
TEMP = 1.0
N_PTS = 24
N_PAIRS = 30
N_DRAWS = 2000
BOOT_B = 200
SKETCH = 80
EPS = 1e-3
M_GRID = [3000, 1000, 300, 100, 30, 10, 3, 1]
BAND = [m for m in M_GRID if 30 <= m <= 1000]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "OT17-floor-curves.json")
APPENDIX = os.path.join(HERE, "PREREG-OT17-APPENDIX.md")


def require_seal():
    text = open(APPENDIX, encoding="utf-8").read()
    if "STATUS: DRAFT-UNSEALED" in text or "STATUS: SEALED" not in text:
        sys.exit("REFUSED: PREREG-OT17-APPENDIX.md is not SEALED.")


def smooth_out(w, xs):
    s = xs @ w.T / TEMP
    s = s - s.max(axis=1, keepdims=True)
    e = np.exp(s)
    return e[:, 0] / e.sum(axis=1)


def main():
    require_seal()
    rng = np.random.default_rng(SEED)
    w = rng.normal(size=(K, D))
    w /= np.linalg.norm(w, axis=1, keepdims=True)
    pts = rng.normal(size=(N_PTS, D))
    traces = np.logspace(-4, -1, N_PAIRS)
    draws = rng.normal(size=(N_DRAWS, D))

    sigmas, cache = [], []
    for tr in traces:
        s_pair, v_pair = [], []
        for _ in range(2):
            g = rng.normal(size=(D, 4))
            m = g @ g.T
            m *= tr / np.trace(m)
            s_pair.append(m)
            cl = np.linalg.cholesky(m + 1e-15 * np.eye(D))
            deltas = draws @ cl.T
            v_pair.append(np.stack([smooth_out(w, x0[None, :] + deltas)
                                    for x0 in pts]))      # (24, 2000)
        sigmas.append(s_pair)
        cache.append(v_pair)

    v0 = smooth_out(w, pts)
    rms = float(np.median(np.abs(np.concatenate(
        [(p - v0[:, None]).ravel() for pair in cache[len(cache) // 2:]
         for p in pair]))))
    print(f"calibrated rms={rms:.3e} (derived grid, per the appendix)")

    # v2 change 1: probe the SMOOTH consumer once (OT-5 precedent)
    def consumer(x):
        s = w @ np.asarray(x, float) / TEMP
        s = s - s.max()
        e = np.exp(s)
        return float(e[0] / e.sum())

    p_hat = blind_probe(consumer, pts, mode="lstsq", sketch_dim=SKETCH,
                        eps=EPS, rng=np.random.default_rng(SEED),
                        check_regime=False).S
    preds = [np.sign(np.trace(p_hat @ (sp[0] - sp[1])))
             for sp in sigmas]

    boot_idx = np.random.default_rng(SEED + 1).integers(
        0, N_DRAWS, (BOOT_B, N_DRAWS))

    cells = []
    for m_mult in M_GRID:
        step = m_mult * rms

        def q(v, step=step):
            return np.round(v / step) * step

        q0 = q(v0)
        n_inf = 0
        graded_hits = graded_n = 0
        sub_hits = sub_pred = sub_n = 0
        lo_margin = hi_margin = 0
        for pred, v_pair in zip(preds, cache):
            dd, per_draw = [], []
            for vp in v_pair:
                sq = (q(vp) - q0[:, None]) ** 2
                per_draw.append(sq.mean(axis=0))
                dd.append(float(sq.mean()))
            diff = dd[0] - dd[1]
            if diff == 0:
                continue
            n_inf += 1
            delta = per_draw[0] - per_draw[1]
            sd = float(delta[boot_idx].mean(axis=1).std())
            margin = abs(diff) / max(sd, 1e-300)
            hit = int(pred == np.sign(diff))
            if margin >= 3:
                hi_margin += 1
                graded_n += 1
                graded_hits += hit          # pred == 0 counts as a miss
            else:
                lo_margin += 1
                sub_n += 1
                if pred != 0:
                    sub_pred += 1
                    sub_hits += hit
        frac = n_inf / N_PAIRS
        straddle = (n_inf > 0
                    and hi_margin / n_inf >= 0.2
                    and lo_margin / n_inf >= 0.2)
        acc = graded_hits / graded_n if graded_n else None
        cells.append({
            "m_mult": m_mult, "informative_frac": round(frac, 4),
            "n_informative": n_inf, "n_graded": graded_n,
            "graded_acc": None if acc is None else round(acc, 4),
            "step_graded": graded_n >= 8, "straddles": straddle,
            "subnoise_n": sub_n, "subnoise_pred": sub_pred,
            "subnoise_acc": (round(sub_hits / sub_pred, 4)
                             if sub_pred else None),
            "subnoise_silence": (round(1 - sub_pred / sub_n, 4)
                                 if sub_n else None)})
        acc_s = "--" if acc is None else f"{acc:.3f}"
        print(f"m={m_mult:>5}: informative {n_inf}/30 ({frac:.2f})  "
              f"graded {graded_n} acc={acc_s}  "
              f"straddle={'y' if straddle else 'n'}")

    by_m = {c["m_mult"]: c for c in cells}
    band_cells = [by_m[m] for m in BAND]
    mc1 = [c for c in band_cells
           if 0.10 < c["informative_frac"] < 0.90]
    # MC2 at BAND level (the OT-13 lesson): >= 2 interior steps
    # straddle, not every one
    mc2 = sum(c["straddles"] for c in mc1) >= 2
    mc3 = (by_m[1]["informative_frac"] >= 0.9
           and by_m[3000]["informative_frac"] <= 0.1)
    void = not (len(mc1) >= 4 and mc2 and mc3)

    fr = [c["informative_frac"] for c in cells]   # coarse -> fine
    b1 = all(fr[i] <= fr[i + 1] + 0.05 for i in range(len(fr) - 1))
    graded_cells = [c for c in cells if c["step_graded"]]
    b2 = all(c["graded_acc"] >= 0.85 for c in graded_cells)
    b3 = not any(c["graded_acc"] <= 0.60 for c in graded_cells)
    verdict = "VOID" if void else \
        ("PASS" if (b1 and b2 and b3) else "FAIL")

    print(f"\nMC1 interior band steps: {len(mc1)} (need >=4)")
    print(f"MC2 band-level straddle "
          f"({sum(c['straddles'] for c in mc1)} of {len(mc1)} interior "
          f"steps, need >=2): {'ok' if mc2 else 'VOID'}")
    print(f"MC3 window (>=0.9 at m=1, <=0.1 at m=3000): "
          f"{'ok' if mc3 else 'VOID'}")
    print(f"B1 fraction decay (tol 0.05/step): "
          f"{'PASS' if b1 else 'FAIL'}")
    print(f"B2 ceiling >=0.85 on {len(graded_cells)} graded steps: "
          f"{'PASS' if b2 else 'FAIL'}")
    print(f"B3 never wrong-while-decisive: {'PASS' if b3 else 'FAIL'}")
    json.dump({"claim": "OT-17", "seed": SEED, "rms": rms,
               "cells": cells, "mc1_steps": len(mc1), "mc2": bool(mc2),
               "mc3": bool(mc3), "B1": bool(b1), "B2": bool(b2),
               "B3": bool(b3), "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"\nOT-13 v2: {verdict} -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
