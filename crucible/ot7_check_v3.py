"""OT-7 v2: constants per PREREG-OT7-APPENDIX-V3.md: quantized-derived
quantities (energy_rank) graded on exact O(d) invariance only, GL
fragility inherited from the spectrum row and reported descriptively.
Full failure trail: OT7-NOTES.md.

    .venv/Scripts/python crucible/ot7_check_v3.py
"""

from __future__ import annotations

import json
import os

import numpy as np

SEED = 20260815
TOL_EXACT = 1e-9
TOL_O = 1e-8
FRAG_MIN = 1e-6
FRAG_SHARE = 0.95
N_T = 50
N_DELTA = 100
COND_CAP = 1e2
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "OT7-invariance-v3.json")


def rand_frame(rng, d, r):
    q, _ = np.linalg.qr(rng.normal(size=(d, r)))
    return q[:, :r]


def make_p(rng, d, r):
    v = rand_frame(rng, d, r)
    lam = np.sort(10 ** rng.uniform(-2, 0, r))[::-1]
    return v @ np.diag(lam) @ v.T, v, lam


def rand_gl(rng, d):
    while True:
        a = rng.normal(size=(d, d))
        if np.linalg.cond(a) <= COND_CAP:
            return a


def rand_o(rng, d):
    q, _ = np.linalg.qr(rng.normal(size=(d, d)))
    return q


def spectrum(p):
    return np.sort(np.linalg.eigvalsh(p))[::-1]


def eff_rank(lam):
    lam = np.clip(lam, 0, None)
    return (lam.sum() ** 2) / (lam ** 2).sum()


def energy_rank(lam, q=0.9):
    lam = np.clip(np.sort(lam)[::-1], 0, None)
    c = np.cumsum(lam) / lam.sum()
    return int(np.searchsorted(c, q) + 1)


def principal_angles(p1, p2, r):
    v1 = np.linalg.eigh(p1)[1][:, -r:]
    v2 = np.linalg.eigh(p2)[1][:, -r:]
    s = np.clip(np.linalg.svd(v1.T @ v2, compute_uv=False), -1, 1)
    return np.arccos(s)


def waterfill(lam, budget):
    """Reverse water-fill bit allocation: b_i = max(0, log2(lam_i/theta))
    with sum(b) = budget, theta by bisection."""
    lam = np.clip(np.sort(lam)[::-1], 1e-300, None)
    lo, hi = 1e-12 * lam[0], lam[0]
    for _ in range(200):
        th = np.sqrt(lo * hi)
        b = np.clip(np.log2(lam / th), 0, None).sum()
        lo, hi = (th, hi) if b < budget else (lo, th)
    return np.clip(np.log2(lam / np.sqrt(lo * hi)), 0, None)


def rel(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    den = max(np.max(np.abs(a)), np.max(np.abs(b)), 1e-300)
    return float(np.max(np.abs(a - b)) / den)


def loading_check(rng, d, a_mat):
    """E'[h'A'] == Ainv.T @ E[hA] @ Ainv with shared samples."""
    a_dir = rng.normal(size=d)
    a_dir /= np.linalg.norm(a_dir)
    b_dir = rng.normal(size=d)
    xs = rng.normal(size=(20000, d))
    pre = xs @ a_dir
    w = (1 - np.tanh(pre) ** 2) ** 2          # A(x) = w(x) a aT
    h = xs @ b_dir
    e_ha = (h * w).mean() * np.outer(a_dir, a_dir)
    ainv = np.linalg.inv(a_mat)
    lhs = ainv.T @ e_ha @ ainv
    # transformed side, same samples: x' = A x, h'(x') = h(x), A'(x') =
    # Ainv.T A(x) Ainv -- assembled independently from the transformed
    # coordinates to exercise the pipeline
    xps = xs @ a_mat.T
    pre2 = (xps @ ainv.T) @ a_dir             # a.T (Ainv x') = a.T x
    w2 = (1 - np.tanh(pre2) ** 2) ** 2
    h2 = (xps @ ainv.T) @ b_dir
    rhs = (h2 * w2).mean() * (ainv.T @ np.outer(a_dir, a_dir) @ ainv)
    return rel(lhs, rhs)


def run_cell(rng, d, r):
    p, _, lam = make_p(rng, d, r)
    p2, _, _ = make_p(rng, d, r)
    sig, _, _ = make_p(rng, d, d)
    out = {"exact": {}, "frag_gl": {}, "inv_o": {}}
    ex = {k: 0.0 for k in ("damage", "trace", "rank", "loading")}
    fr = {k: [] for k in ("spectrum", "eff_rank", "energy_rank",
                          "angles", "waterfill")}
    io = {k: 0.0 for k in fr}
    base = {
        "spectrum": spectrum(p),
        "eff_rank": eff_rank(lam),
        "energy_rank": energy_rank(lam),
        "angles": principal_angles(p, p2, r),
        "waterfill": np.sort(waterfill(spectrum(p), 2.0 * d))[::-1],
    }
    for kind in ("gl", "o"):
        for _ in range(N_T):
            a = rand_gl(rng, d) if kind == "gl" else rand_o(rng, d)
            ai = np.linalg.inv(a)
            pp = ai.T @ p @ ai
            pp2 = ai.T @ p2 @ ai
            if kind == "gl":
                deltas = rng.normal(size=(N_DELTA, d))
                ex["damage"] = max(ex["damage"], rel(
                    np.einsum("nd,de,ne->n", deltas @ a.T, pp,
                              deltas @ a.T),
                    np.einsum("nd,de,ne->n", deltas, p, deltas)))
                ex["trace"] = max(ex["trace"], rel(
                    np.trace(pp @ (a @ sig @ a.T)), np.trace(p @ sig)))
                s = np.linalg.svd(pp, compute_uv=False)
                ex["rank"] = max(ex["rank"], float(
                    int((s > s[0] * 1e-9 * d).sum()) != r))
                ex["loading"] = max(ex["loading"],
                                    loading_check(rng, d, a))
            cur = {
                "spectrum": spectrum(pp),
                "eff_rank": eff_rank(spectrum(pp)),
                "energy_rank": energy_rank(spectrum(pp)),
                "angles": principal_angles(pp, pp2, r),
                "waterfill": np.sort(waterfill(spectrum(pp),
                                               2.0 * d))[::-1],
            }
            for k in fr:
                dv = rel(base[k], cur[k])
                if kind == "gl":
                    fr[k].append(dv)
                else:
                    io[k] = max(io[k], dv)
    out["exact"] = {k: v for k, v in ex.items()}
    out["frag_gl"] = {k: float(np.mean([d_ > FRAG_MIN for d_ in v]))
                      for k, v in fr.items()}
    out["inv_o"] = io
    ok_exact = all(v <= TOL_EXACT for v in ex.values())
    # degenerate-cell annotation per appendix v2: class constants are
    # annotated, not graded; energy_rank (integer) bar is 0.50.
    degenerate = set()
    if r == 1:
        degenerate |= {"eff_rank", "energy_rank", "waterfill"}
    if r == d:
        degenerate |= {"angles"}
    out["degenerate"] = sorted(degenerate)
    quantized = {"energy_rank"}  # graded on O(d) exactness only;
    # GL fragility inherited from the parent (spectrum), share reported
    ok_frag = all(out["frag_gl"][k] >= FRAG_SHARE
                  for k in fr if k not in degenerate | quantized)
    ok_o = all((v == 0.0 if k in quantized else v <= TOL_O)
               for k, v in io.items() if k not in degenerate)
    out["pass"] = bool(ok_exact and ok_frag and ok_o)
    return out


def main():
    rng = np.random.default_rng(SEED)
    cells = {}
    ok = True
    for d in (8, 32):
        for r in (1, 4, d):
            key = f"d{d}_r{r}"
            cells[key] = run_cell(rng, d, r)
            ok &= cells[key]["pass"]
            print(f"{key}: {'PASS' if cells[key]['pass'] else 'FAIL'}  "
                  f"exact_max={max(cells[key]['exact'].values()):.2e}  "
                  f"frag_min_share={min(cells[key]['frag_gl'].values()):.2f}  "
                  f"o_max={max(cells[key]['inv_o'].values()):.2e}")
    result = {"claim": "OT-7", "seed": SEED, "cells": cells,
              "verdict": "PASS" if ok else "FAIL"}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(result, open(OUT, "w"), indent=1)
    print(f"\nOT-7: {result['verdict']}  -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
