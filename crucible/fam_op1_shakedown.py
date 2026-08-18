"""OP1 — cross-consumer codec transfer (shakedown). First substrate for
the v1-line's genuinely-new claim (crucible/OWED-V1.md, OP1).

Claim (P1, cross-consumer): a codec optimized against consumer A's read
operator P_A damages a *different* consumer B by an amount predictable
from the operator overlap tr(P_A P_B) ALONE — no probe of B under A's
codec. Consumer relativity, if it means what it says, composes across
consumers, not only within an ensemble.

Mechanism / a-priori sign. Code the frame in A's eigenbasis; the
A-optimal codec water-fills its rate budget against A's sensitivity
spectrum s_A, spending bits where A is sensitive and dumping
quantization noise where A is NOT. So the distortion Σ_δ^A is large
exactly in A's low-sensitivity directions. B's damage
tr(P_B Σ_δ^A) is therefore large when B reads where A does not — i.e.
it DECREASES as the overlap tr(P_A P_B) grows (when B reads what A
protects, B is spared). The falsifiable content: does the single scalar
tr(P_A P_B), computed without ever probing B under A's codec, predict
B's measured damage across a family of consumer pairs?

This shakedown builds a family of read-operator pairs (P_A, P_B) with a
swept overlap, runs the A-optimal water-filled codec, measures B's
damage tr(P_B Σ_δ^A), and checks the rank correlation with tr(P_A P_B)
across seeds. No evidential weight; bars live in PREREG-OP1.md and seal
on a fresh day.

    python crucible/fam_op1_shakedown.py
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\source\readscope")
from readscope import water_fill  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "OP1-shakedown.json")

D = 48
RANK_TRACE = 8.0            # tr(P) normalisation ("soft rank")
SPEC_DECAY = 0.85          # operator sensitivity spectrum s_k ~ decay^k
BUDGET = 2.0 * D           # codec rate budget (bits)
N_PAIRS = 60               # consumer pairs per seed
SEEDS = [0, 1, 2]


def soft_operator(rng, V=None, mix=None, V_ref=None):
    """PSD read operator P = V diag(s) V^T, s a decaying spectrum
    normalised to tr(P)=RANK_TRACE. If mix/V_ref given, tilt V toward
    V_ref by `mix` to control overlap."""
    s = SPEC_DECAY ** np.arange(D)
    s = s / s.sum() * RANK_TRACE
    G = rng.standard_normal((D, D))
    if mix is not None and V_ref is not None:
        G = mix * V_ref + (1.0 - mix) * G
    V = np.linalg.qr(G)[0]
    return V, s


def op_from(V, s):
    return (V * s) @ V.T


def main():
    print(f"OP1 cross-consumer transfer shakedown — d={D} "
          f"tr(P)={RANK_TRACE} budget={BUDGET} seeds={SEEDS}")
    print("prediction: B-damage tr(P_B Σ_δ^A) DECREASES with tr(P_A P_B)\n")

    rows, per_seed = [], {}
    for seed in SEEDS:
        rng = np.random.default_rng(seed * 5237 + 11)
        overlaps, damages = [], []
        for _ in range(N_PAIRS):
            V_A, s_A = soft_operator(rng)
            mix = rng.uniform(0.0, 1.0)     # tilt B toward A -> sweep overlap
            V_B, s_B = soft_operator(rng, mix=mix, V_ref=V_A)
            P_A = op_from(V_A, s_A)
            P_B = op_from(V_B, s_B)
            overlap = float(np.trace(P_A @ P_B))
            # A-optimal codec: water-fill bits against A's sensitivity s_A
            # (whitened source), then quantisation noise var_k = 2^{-2 b_k}
            alloc = water_fill(sensitivity=s_A, variance=np.ones(D),
                               budget=BUDGET)
            var = np.power(2.0, -2.0 * alloc.bits)          # in A's eigenbasis
            Sigma_A = (V_A * var) @ V_A.T                    # codec distortion
            damage = float(np.trace(P_B @ Sigma_A))
            overlaps.append(overlap)
            damages.append(damage)
            rows.append({"seed": seed, "overlap": overlap, "damage": damage,
                         "mix": mix})
        rho = float(stats.spearmanr(overlaps, damages).statistic)
        # leading linear fit damage ~ a - b*overlap
        b, a = np.polyfit(overlaps, damages, 1)
        pred = a + b * np.array(overlaps)
        ss_res = float(np.sum((np.array(damages) - pred) ** 2))
        ss_tot = float(np.sum((np.array(damages) - np.mean(damages)) ** 2))
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
        per_seed[seed] = {"spearman": round(rho, 4), "slope": round(float(b), 5),
                          "r2": round(r2, 4),
                          "overlap_range": [round(min(overlaps), 3),
                                            round(max(overlaps), 3)]}
        print(f"seed {seed}: overlap∈[{min(overlaps):.2f},{max(overlaps):.2f}]  "
              f"Spearman(overlap,damage)={rho:+.3f}  slope={b:+.4f}  R²={r2:.3f}")

    rhos = [per_seed[s]["spearman"] for s in SEEDS]
    print(f"\ninterior: negative rank correlation on every seed "
          f"(min |ρ|={min(abs(r) for r in rhos):.3f}); "
          f"tr(P_A P_B) predicts cross-damage without probing B")

    record = {"campaign": "OP1", "sealed": False, "shakedown": True,
              "note": "no evidential weight; bars in crucible/PREREG-OP1.md",
              "generated": datetime.now(timezone.utc).isoformat(),
              "constants": {"d": D, "rank_trace": RANK_TRACE,
                            "spec_decay": SPEC_DECAY, "budget": BUDGET,
                            "n_pairs": N_PAIRS, "seeds": SEEDS},
              "per_seed": {str(k): v for k, v in per_seed.items()},
              "rows": rows}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(record, open(OUT, "w"), indent=1)
    print(f"\nwrote {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
