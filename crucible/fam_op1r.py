"""OP1-R family: cross-consumer codec transfer on REAL Llama heads —
the substrate OWED-V1 names for OP1's discharge. Measurement core +
family shakedown; the graded runner (op1r_check.py) imports run_pairs
unchanged.

Consumers: the OT-15 real-head form — softmax attention probability to
key position P_STAR, built from cached Q/K of 12 Llama-3.2-3B heads
(crucible/armH_data, d=128). Per head h: operator P_h blind-probed with
readscope.jacobian_probe (no analytic access). For an ordered pair
(A, B): the A-optimal codec water-fills RATE_BITS against P_A's
spectrum; its quantization noise Sigma_A lands where A is insensitive.
B's damage is MEASURED functionally: mean squared change of f_B under
delta ~ N(0, Sigma_A) at real key points (Monte Carlo), never through
B's operator. The prediction uses ONE scalar: overlap = tr(Pn_A Pn_B)
on trace-normalized operators. OWED-V1's claim: measured damage is
predictable from that scalar alone (mechanism sign: decreasing — B is
spared where A protects).

Family split is HEAD-DISJOINT: shakedown pairs draw from heads {0..5},
the graded runner from heads {6..11} — the graded heads are never seen
before grading, the strongest available form of the blind claim.

    python crucible/fam_op1r.py            # shakedown (heads 0-5)
"""

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, r"C:\source\readscope")
from readscope import jacobian_probe, water_fill  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "armH_data")

# ---- sealed constants (bars reference these; do not tune) ------------
D = 128
P_STAR = 96                 # attended key position (OT-15's consumer)
K_DIRS = 160                # blind-probe directions
EPS = 1e-3
RATE_BITS = 2.0 * D         # codec budget
NOISE_SCALE = 0.05          # codec noise magnitude (x source scale)
N_MC = 4000                 # Monte Carlo draws for measured damage
PROBE_SEED = 20260820
SHAKE_HEADS = range(0, 6)   # family construction heads
GRADE_HEADS = range(6, 12)  # graded heads (disjoint, untouched today)


def load_heads(indices):
    files = sorted(glob.glob(os.path.join(DATA, "*.npz")))
    out = []
    for i in indices:
        z = np.load(files[i])
        out.append((os.path.basename(files[i])[:-4], z["Q"], z["K"]))
    return out


def consumer(q, k):
    s = q @ k.T / np.sqrt(D)
    z_rest = np.exp(s).sum(axis=1) - np.exp(s[:, P_STAR])

    def f(key_vec):
        sp = q @ key_vec / np.sqrt(D)
        e = np.exp(sp)
        return float(np.mean(e / (z_rest + e)))
    return f


def probe_operator(f, pts, seed):
    S = jacobian_probe(f, pts, n_directions=K_DIRS, eps=EPS,
                       rng=np.random.default_rng(seed)).S
    return S


def a_codec_sigma(P_A, scale):
    """A-optimal codec: water-fill RATE_BITS against P_A's spectrum in
    its eigenbasis; quantization noise var 2^-2b per direction, overall
    magnitude set by `scale` (x the mean key norm)."""
    evals, evecs = np.linalg.eigh(P_A)
    evals = np.clip(evals[::-1], 1e-12, None)
    evecs = evecs[:, ::-1]
    alloc = water_fill(sensitivity=evals, variance=np.ones(D),
                       budget=RATE_BITS)
    var = np.power(2.0, -2.0 * alloc.bits) * scale ** 2
    return (evecs * var) @ evecs.T


def measured_damage(f_B, pts, Sigma_A, seed):
    """Functional damage to B under A's codec noise, by Monte Carlo at
    real key points — B's operator is never used here."""
    rng = np.random.default_rng(seed)
    L = np.linalg.cholesky(Sigma_A + 1e-15 * np.eye(D))
    idx = rng.integers(0, len(pts), N_MC)
    deltas = rng.standard_normal((N_MC, D)) @ L.T
    d2 = 0.0
    for j in range(N_MC):
        x = pts[idx[j]]
        d2 += (f_B(x + deltas[j]) - f_B(x)) ** 2
    return d2 / N_MC


def run_pairs(head_indices, probe_seed=PROBE_SEED):
    heads = load_heads(head_indices)
    scale = float(np.mean([np.linalg.norm(k, axis=1).mean()
                           for _, _, k in heads])) * NOISE_SCALE
    ops, fs, ptss = {}, {}, {}
    for name, q, k in heads:
        f = consumer(q, k)
        P = probe_operator(f, k[:64], probe_seed)
        ops[name], fs[name], ptss[name] = P, f, k
        print(f"  probed {name} (tr={np.trace(P):.3g})", flush=True)
    rows = []
    names = [n for n, _, _ in heads]
    for a in names:
        Pn_A = ops[a] / np.trace(ops[a])
        Sigma_A = a_codec_sigma(ops[a], scale)
        for bd in names:
            if bd == a:
                continue
            Pn_B = ops[bd] / np.trace(ops[bd])
            overlap = float(np.trace(Pn_A @ Pn_B))
            sd = probe_seed + hash((a, bd)) % 9973
            dmg = measured_damage(fs[bd], ptss[bd], Sigma_A, seed=sd)
            # DIRECTIONAL SELECTIVITY: heads differ in intrinsic output
            # sensitivity, so raw damage is incomparable across B. The
            # theory's quantity is damage under A's codec RELATIVE to
            # isotropic noise of equal total power (shakedown lesson,
            # first run: raw pooled rho -0.25 from scale contamination).
            Sigma_iso = (np.trace(Sigma_A) / D) * np.eye(D)
            dmg_iso = measured_damage(fs[bd], ptss[bd], Sigma_iso,
                                      seed=sd + 1)
            rows.append({"A": a, "B": bd, "overlap": round(overlap, 5),
                         "damage": float(dmg / max(dmg_iso, 1e-300)),
                         "damage_raw": dmg, "damage_iso": dmg_iso})
        print(f"  codec {a}: {len(names)-1} cross-damages", flush=True)
    # per-A rank statistics (the within-codec ranking is the claim's
    # cleanest form: given A's codec, which B suffers?)
    per_a = []
    for a in names:
        sub = [r for r in rows if r["A"] == a]
        rho = float(stats.spearmanr([r["overlap"] for r in sub],
                                    [r["damage"] for r in sub]).statistic)
        per_a.append({"A": a, "spearman": round(rho, 4), "n": len(sub)})
    pooled = float(stats.spearmanr([r["overlap"] for r in rows],
                                   [r["damage"] for r in rows]).statistic)
    return {"rows": rows, "per_a": per_a,
            "pooled_spearman": round(pooled, 4),
            "overlap_range": [round(min(r["overlap"] for r in rows), 4),
                              round(max(r["overlap"] for r in rows), 4)]}


def main():
    print(f"OP1-R shakedown — heads {list(SHAKE_HEADS)} "
          f"(graded heads {list(GRADE_HEADS)} untouched)", flush=True)
    rec = run_pairs(SHAKE_HEADS)
    print(f"\npooled Spearman(overlap, damage) = {rec['pooled_spearman']}")
    for e in rec["per_a"]:
        print(f"  codec {e['A']}: rho={e['spearman']} (n={e['n']})")
    print(f"overlap range {rec['overlap_range']}")
    out = os.path.join(HERE, "..", "results", "OP1R-shakedown.json")
    json.dump({"campaign": "OP1-R", "sealed": False, "shakedown": True,
               "heads": list(SHAKE_HEADS), **rec}, open(out, "w"), indent=1)
    print(f"wrote {os.path.relpath(out, HERE)}")


if __name__ == "__main__":
    main()
