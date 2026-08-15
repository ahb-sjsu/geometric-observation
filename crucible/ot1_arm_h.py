"""OT-1 Arm H — real heads, zero refit. Constants per PREREG-OT1.md.

Eight Llama-3.2-3B head-pairs sharing a KV head (verified: identical K),
consumer = attention mass each of the head's 24 real queries gives the
probed key position, operators recovered blind by readscope's
jacobian_probe at k/d = 1.25, codecs random equal-trace rank-4 (seeded,
independent of the probes). Bar H1: sign of preference disagreement
predicted by tr((P1-P2)(SA-SB)) on >= 7/8 pairs.

    .venv/Scripts/python crucible/ot1_arm_h.py
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
K_DIRS = 160                 # k/d = 1.25 per the sealed spec
P_STAR = 96                  # probed key position (mid-sequence, settled)
EPS_PROBE = 1e-3
TRACE = 0.01                 # codec energy (equal by construction)
N_DRAWS = 20_000
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "armH_data")
OUT = os.path.join(HERE, "..", "results", "OT1-arm-h.json")

LAYERS = (7, 14, 21)
PAIR_IDS = [(L, a, b) for L in LAYERS for a, b in ((0, 1), (0, 2), (1, 2))][:8]


def load(layer, head):
    z = np.load(os.path.join(DATA, f"llama32-3b_L{layer}_H{head}.npz"))
    return z["Q"], z["K"]


def consumer_single(q, k):
    """f(key_vec) -> attention mass at P_STAR per query (24,)."""
    s = q @ k.T / np.sqrt(D)                    # (24, 192) base scores
    z_rest = np.exp(s).sum(axis=1) - np.exp(s[:, P_STAR])

    def f(key_vec):
        sp = q @ key_vec / np.sqrt(D)           # (24,)
        e = np.exp(sp)
        return e / (z_rest + e)
    return f


def damage_batch(q, k, deltas):
    """Mean squared change of the consumer output over perturbation draws."""
    s = q @ k.T / np.sqrt(D)
    z_rest = np.exp(s).sum(axis=1) - np.exp(s[:, P_STAR])
    sp0 = q @ k[P_STAR] / np.sqrt(D)
    a0 = np.exp(sp0) / (z_rest + np.exp(sp0))
    sp = (k[P_STAR][None, :] + deltas) @ q.T / np.sqrt(D)   # (n, 24)
    e = np.exp(sp)
    a = e / (z_rest[None, :] + e)
    return float(np.mean(np.sum((a - a0[None, :]) ** 2, axis=1)))


def principal_angle_deg(p1, p2, r=4):
    v1 = np.linalg.eigh(p1)[1][:, -r:]
    v2 = np.linalg.eigh(p2)[1][:, -r:]
    s = np.clip(np.linalg.svd(v1.T @ v2, compute_uv=False), -1, 1)
    return float(np.rad2deg(np.arccos(s).mean()))


def main():
    codec_rng = np.random.default_rng(SEED + 1)
    rows, hits = [], 0
    for i, (layer, ha, hb) in enumerate(PAIR_IDS):
        qa, k = load(layer, ha)
        qb, kb = load(layer, hb)
        assert np.array_equal(k, kb), "pair must share the KV stream"
        # blind operators (probe rng fixed per pair for determinism)
        p_hat = []
        for q in (qa, qb):
            res = jacobian_probe(consumer_single(q, k), k[P_STAR][None, :],
                                 n_directions=K_DIRS, eps=EPS_PROBE,
                                 rng=np.random.default_rng(SEED))
            p_hat.append(res.S)
        theta = principal_angle_deg(*p_hat)     # recorded before damages
        # codecs: random rank-4, exactly equal trace, probe-independent
        sig = []
        for _ in range(2):
            g = codec_rng.normal(size=(D, 4))
            m = g @ g.T
            sig.append(m * (TRACE / np.trace(m)))
        pred = np.sign(np.trace((p_hat[0] - p_hat[1]) @ (sig[0] - sig[1])))
        # measured damages
        chol = [np.linalg.cholesky(m + 1e-15 * np.eye(D)) for m in sig]
        draws = np.random.default_rng(SEED + 2 + i).normal(
            size=(2, N_DRAWS, D))
        d_meas = np.zeros((2, 2))               # [consumer, codec]
        for ci, q in enumerate((qa, qb)):
            for si in range(2):
                deltas = draws[si] @ chol[si].T
                d_meas[ci, si] = damage_batch(q, k, deltas)
        meas = np.sign((d_meas[0, 0] - d_meas[0, 1])
                       - (d_meas[1, 0] - d_meas[1, 1]))
        hit = bool(pred == meas)
        hits += hit
        rows.append({"pair": f"L{layer}:H{ha}/H{hb}",
                     "theta_hat_deg": round(theta, 1),
                     "pred_sign": int(pred), "meas_sign": int(meas),
                     "d": [[float(f"{x:.3e}") for x in r_] for r_ in d_meas],
                     "hit": hit})
        print(f"L{layer} H{ha}/H{hb}: theta={theta:5.1f}deg  "
              f"pred={int(pred):+d} meas={int(meas):+d}  "
              f"{'HIT' if hit else 'MISS'}")
    h1 = hits >= 7
    print(f"\nH1: {hits}/8 (bar 7) -> {'PASS' if h1 else 'FAIL'}")
    json.dump({"claim": "OT-1-arm-H", "seed": SEED, "pairs": rows,
               "hits": hits, "H1": bool(h1)}, open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
