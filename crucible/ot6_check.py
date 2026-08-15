"""OT-6: cross-domain transfer to embedding ranking, constants per
PREREG-OT6-APPENDIX.md.

    .venv/Scripts/python crucible/ot6_check.py
"""

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, r"C:\source\readscope")
from readscope.probe import blind_probe  # noqa: E402

SEED = 20260815
D = 768
SKETCH = 960
EPS_C = 0.15
N_INDEX, N_QUERY, N_PROBE_CELLS = 1000, 200, 24
N_DRAWS = 20
BOOT_B = 2000
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "OT6-transfer.json")


def load_corpus():
    files = sorted(glob.glob(os.path.join(HERE, "ot6_data", "*.npy")))
    x = np.concatenate([np.load(f).astype(np.float64) for f in files])
    rng = np.random.default_rng(SEED)
    x = x[rng.permutation(len(x))]
    return x[:N_INDEX], x[N_INDEX:N_INDEX + N_QUERY]


def scores(cell, q, e):
    if cell == "dot":
        return e @ q
    qn = q / np.linalg.norm(q)
    return (e / np.linalg.norm(e, axis=-1, keepdims=True)) @ qn


def margin_consumer(cell, q, corpus, j):
    others = scores(cell, q, np.delete(corpus, j, axis=0)).max()

    def c(x):
        if cell == "dot":
            s = float(q @ x)
        else:
            s = float(q @ x / (np.linalg.norm(q) * np.linalg.norm(x)))
        return s - others
    return c


def top10(cell, q, corpus):
    return set(np.argsort(-scores(cell, q, corpus))[:10])


def run_cell(cell, corpus, queries):
    # blind operator: mean of 24 per-(query, top-1 item) probes
    p_hat = np.zeros((D, D))
    for qi in range(N_PROBE_CELLS):
        q = queries[qi]
        j = int(np.argmax(scores(cell, q, corpus)))
        pts = np.repeat(corpus[j][None, :], 4, axis=0)
        res = blind_probe(margin_consumer(cell, q, corpus, j),
                          pts, mode="lstsq",
                          sketch_dim=SKETCH, eps=1e-3,
                          rng=np.random.default_rng(SEED + qi))
        p_hat += res.S
    p_hat /= N_PROBE_CELLS

    lam, v = np.linalg.eigh(p_hat)
    lam, v = lam[::-1], v[:, ::-1]
    top = v[:, :8]
    sig_a = top @ np.diag(lam[:8] / lam[:8].sum()) @ top.T
    sig_a *= EPS_C ** 2 / np.trace(sig_a)
    tail = v[:, 64:72]
    sig_b = tail @ tail.T / 8.0
    sig_b *= EPS_C ** 2 / np.trace(sig_b)
    assert abs(np.trace(sig_a) - np.trace(sig_b)) < 1e-9
    tr_a, tr_b = float(np.sum(p_hat * sig_a)), float(np.sum(p_hat * sig_b))

    chol = {k: np.linalg.cholesky(s + 1e-12 * np.eye(D))
            for k, s in (("A", sig_a), ("B", sig_b))}
    clean = [top10(cell, q, corpus) for q in queries]
    dmg = {k: np.zeros(N_QUERY) for k in ("A", "B")}
    rng = np.random.default_rng(SEED + 500)
    for k in ("A", "B"):
        for _ in range(N_DRAWS):
            pert = corpus + rng.normal(size=corpus.shape) @ chol[k].T
            for qi, q in enumerate(queries):
                ov = len(clean[qi] & top10(cell, q, pert))
                dmg[k][qi] += (1 - ov / 10) / N_DRAWS
    d_a, d_b = float(dmg["A"].mean()), float(dmg["B"].mean())

    diff = dmg["A"] - dmg["B"]
    boot = np.random.default_rng(SEED + 900)
    reps = sorted(float(np.mean(diff[boot.integers(0, N_QUERY, N_QUERY)]))
                  for _ in range(BOOT_B))
    lo, hi = reps[int(0.025 * BOOT_B)], reps[int(0.975 * BOOT_B) - 1]
    any_dmg = (dmg["A"] + dmg["B"]) > 0
    sign_share = float(np.mean(dmg["A"][any_dmg] > dmg["B"][any_dmg])) \
        if any_dmg.any() else 0.0

    window = 0.01 <= d_a <= 0.95
    x1 = lo > 0
    x2 = d_b == 0 or d_a / max(d_b, 1e-12) >= 2
    x3 = sign_share >= 0.75
    print(f"[{cell}] tr(P Sig): A={tr_a:.3e} B={tr_b:.3e} "
          f"(ratio {tr_a / max(tr_b, 1e-300):.0f}x)")
    print(f"[{cell}] damage: A={d_a:.4f} B={d_b:.4f} "
          f"ratio={d_a / max(d_b, 1e-12):.1f}x  diff CI=[{lo:.4f},{hi:.4f}]")
    print(f"[{cell}] window={'ok' if window else 'VOID'} "
          f"X1={'PASS' if x1 else 'FAIL'} X2={'PASS' if x2 else 'FAIL'} "
          f"X3={sign_share:.2f} {'PASS' if x3 else 'FAIL'}")
    return {"cell": cell, "tr_A": tr_a, "tr_B": tr_b,
            "damage_A": d_a, "damage_B": d_b,
            "diff_ci": [lo, hi], "sign_share": sign_share,
            "window": bool(window), "X1": bool(x1), "X2": bool(x2),
            "X3": bool(x3)}


def main():
    corpus, queries = load_corpus()
    cells = [run_cell(c, corpus, queries) for c in ("dot", "cosine")]
    window = all(c["window"] for c in cells)
    ok = window and all(c["X1"] and c["X2"] and c["X3"] for c in cells)
    verdict = ("VOID" if not window else "PASS" if ok else "FAIL")
    json.dump({"claim": "OT-6", "seed": SEED, "cells": cells,
               "verdict": verdict}, open(OUT, "w"), indent=1)
    print(f"\nOT-6: {verdict} -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
