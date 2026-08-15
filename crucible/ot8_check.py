"""OT-8: ensemble composition on real heads, per PREREG-OT8-APPENDIX.md.
Component machinery identical to OT-1 Arm H (ot1_arm_h.py).

    .venv/Scripts/python crucible/ot8_check.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, r"C:\source\readscope")
from readscope.probe import jacobian_probe  # noqa: E402

SEED = 20260815
D = 128
K_DIRS = 160
P_STAR = 96
EPS_PROBE = 1e-3
TRACE = 0.01
N_DRAWS = 20_000
LAYERS = (7, 14, 21)
HEADS = (0, 1, 2)
N_W = 10
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "armH_data")
OUT = os.path.join(HERE, "..", "results", "OT8-composition.json")


def load(layer, head):
    z = np.load(os.path.join(DATA, f"llama32-3b_L{layer}_H{head}.npz"))
    return z["Q"], z["K"]


def consumer_single(q, k):
    s = q @ k.T / np.sqrt(D)
    z_rest = np.exp(s).sum(axis=1) - np.exp(s[:, P_STAR])

    def f(key_vec):
        sp = q @ key_vec / np.sqrt(D)
        e = np.exp(sp)
        return e / (z_rest + e)
    return f


def alpha_batch(q, k, keys_pert):
    s = q @ k.T / np.sqrt(D)
    z_rest = np.exp(s).sum(axis=1) - np.exp(s[:, P_STAR])
    sp = keys_pert @ q.T / np.sqrt(D)
    e = np.exp(sp)
    return e / (z_rest[None, :] + e)          # (n, 24)


def main():
    probes, qs, k_shared = {}, {}, {}
    for layer in LAYERS:
        k_ref = None
        for h in HEADS:
            q, k = load(layer, h)
            if k_ref is None:
                k_ref = k
            assert np.array_equal(k, k_ref)
            res = jacobian_probe(consumer_single(q, k),
                                 k[P_STAR][None, :],
                                 n_directions=K_DIRS, eps=EPS_PROBE,
                                 rng=np.random.default_rng(SEED))
            probes[(layer, h)] = res.S
            qs[(layer, h)] = q
        k_shared[layer] = k_ref

    w_rng = np.random.default_rng(SEED)
    codec_rng = np.random.default_rng(SEED + 1)   # 20260816
    cells, graded, hits = [], 0, 0
    ci = 0
    for layer in LAYERS:
        for _ in range(N_W):
            w = w_rng.dirichlet(np.ones(3))
            sig = []
            for _ in range(2):
                g = codec_rng.normal(size=(D, 4))
                m = g @ g.T
                sig.append(m * (TRACE / np.trace(m)))
            pred = np.sign(sum(
                w[i] * np.trace(probes[(layer, h)] @ (sig[0] - sig[1]))
                for i, h in enumerate(HEADS)))
            chol = [np.linalg.cholesky(m + 1e-15 * np.eye(D))
                    for m in sig]
            draws = np.random.default_rng(SEED + 2 + ci).normal(
                size=(2, N_DRAWS, D))
            k = k_shared[layer]
            base = k[P_STAR]
            d_meas = []
            for si in range(2):
                keys_pert = base[None, :] + draws[si] @ chol[si].T
                ens0 = sum(
                    w[i] * alpha_batch(qs[(layer, h)], k,
                                       base[None, :])[0]
                    for i, h in enumerate(HEADS))
                ens = sum(
                    w[i] * alpha_batch(qs[(layer, h)], k, keys_pert)
                    for i, h in enumerate(HEADS))
                d_meas.append(float(np.mean(
                    np.sum((ens - ens0[None, :]) ** 2, axis=1))))
            meas = np.sign(d_meas[0] - d_meas[1])
            cell = {"layer": layer, "w": [round(float(x), 3) for x in w],
                    "pred": int(pred), "meas": int(meas)}
            if meas != 0:
                graded += 1
                hit = bool(pred == meas)
                hits += hit
                cell["hit"] = hit
            cells.append(cell)
            ci += 1
    floor = graded >= 25
    bar = int(np.ceil(25 / 30 * graded))
    e1 = floor and hits >= bar
    print(f"graded {graded}/30, hits {hits} (bar {bar})")
    verdict = "VOID" if not floor else ("PASS" if e1 else "FAIL")
    json.dump({"claim": "OT-8", "seed": SEED, "cells": cells,
               "graded": graded, "hits": hits, "bar": bar,
               "verdict": verdict}, open(OUT, "w"), indent=1)
    print(f"OT-8: {verdict} -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
