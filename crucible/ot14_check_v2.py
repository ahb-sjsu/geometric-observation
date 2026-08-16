"""OT-14 v2: feedback-free staleness on the F2 dial, constants per
PREREG-OT14-APPENDIX-V2.md — codec operators are exact pool blends.
Refuses to run until the v2 appendix is SEALED.

    .venv/Scripts/python crucible/ot14_check_v2.py
"""

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ot11_check import quantize_against  # noqa: E402

SEED = 20260817
BITS = 1.0
TAUS = [0.0, 0.01, 0.03, 0.06, 0.125, 0.25, 0.5, 1.0]
N_DIAL = 100
N_EVAL = 80
N_RESAMPLE = 10
FLOOR_REDRAWS = 5
OUT = os.path.join(HERE, "..", "results", "OT14-staleness-dial-v2.json")
APPENDIX = os.path.join(HERE, "PREREG-OT14-APPENDIX-V2.md")


def require_seal():
    text = open(APPENDIX, encoding="utf-8").read()
    if "STATUS: DRAFT-UNSEALED" in text or "STATUS: SEALED" not in text:
        sys.exit("REFUSED: PREREG-OT14-APPENDIX-V2.md is not SEALED.")


def damages(queries, fp_index, q_index):
    d10 = d1 = 0.0
    for q in queries:
        r_fp = np.argsort(-(fp_index @ q))
        r_q = np.argsort(-(q_index @ q))
        d10 += 1 - len(set(r_fp[:10]) & set(r_q[:10])) / 10
        d1 += float(r_fp[0] != r_q[0])
    n = len(queries)
    return d10 / n, d1 / n


def main():
    require_seal()
    files = sorted(glob.glob(os.path.join(HERE, "ot6_data", "*.npy")))
    books = {os.path.basename(f)[:-4]: np.load(f).astype(np.float64)
             for f in files}
    names = sorted(books, key=lambda n: (not n.startswith("cs"), n))
    index = np.concatenate([books[n][:100] for n in names])
    cs_pool = books[names[0]][100:]
    de_pool = np.concatenate([books[n][100:] for n in names[1:]])

    def stratum(tau, n_q, seed):
        # caveat (iii): draws are without replacement, guarded
        r = np.random.default_rng(seed)
        n_far = int(round(tau * n_q))
        n_near = n_q - n_far
        if n_near > len(cs_pool) or n_far > len(de_pool):
            sys.exit("VOID: eval draw would need replacement")
        qs = []
        if n_near:
            qs.append(cs_pool[r.choice(len(cs_pool), n_near,
                                       replace=False)])
        if n_far:
            qs.append(de_pool[r.choice(len(de_pool), n_far,
                                       replace=False)])
        return np.concatenate(qs)

    def op(queries):
        return queries.T @ queries / len(queries)

    # dial -- unchanged from v1: sampled strata, full-pool reference
    p0 = op(stratum(0.0, N_DIAL, SEED))
    n0 = np.linalg.norm(p0)
    floor = float(np.median([
        np.linalg.norm(op(stratum(0.0, N_DIAL, SEED + 77 + i)) - p0) / n0
        for i in range(FLOOR_REDRAWS)]))
    drift = {t: float(np.linalg.norm(
        op(stratum(t, N_DIAL, SEED + int(t * 10000) + 1)) - p0) / n0)
        for t in TAUS}
    nz = [t for t in TAUS if t > 0]
    dr = [drift[t] for t in nz]
    rho_dial = float(stats.spearmanr(nz, dr).statistic)
    above = [t for t in nz if drift[t] > 2 * floor]
    sig = [drift[t] for t in above]
    rng_ratio = (max(sig) / min(sig)) if len(sig) >= 2 else 0.0
    interior = sum(0.1 * max(dr) < d_ < 0.9 * max(dr) for d_ in dr)
    print(f"dial: floor={floor:.4f} spearman={rho_dial:.3f} "
          f"above-floor={len(above)} range={rng_ratio:.1f}x "
          f"interior={interior}")
    for t in TAUS:
        print(f"  tau={t:>6}: drift={drift[t]:.4f}")
    mc1 = (rho_dial >= 0.9 and len(above) >= 5
           and rng_ratio >= 3.0 and interior >= 3)

    # v2 change: codec operators are the EXACT pool blends
    p_cs = op(cs_pool)
    p_de = op(de_pool)
    stale = quantize_against(index, p_cs, BITS)
    strata = {}
    for t in nz:
        fresh = quantize_against(index,
                                 (1 - t) * p_cs + t * p_de, BITS)
        ex10, s10, f10, ex1 = [], [], [], []
        for i in range(N_RESAMPLE):
            qs = stratum(t, N_EVAL, SEED + 5000 + int(t * 10000) + i)
            a10, a1 = damages(qs, index, stale)
            b10, b1_ = damages(qs, index, fresh)
            s10.append(a10)
            f10.append(b10)
            ex10.append(a10 - b10)
            ex1.append(a1 - b1_)
        ex10 = np.array(ex10)
        strata[t] = {"stale10": float(np.mean(s10)),
                     "fresh10": float(np.mean(f10)),
                     "excess10": float(ex10.mean()),
                     "noise10": float(ex10.std()),
                     "excess1": float(np.mean(ex1))}
        print(f"  tau={t:>6}: stale {strata[t]['stale10']:.4f} "
              f"fresh {strata[t]['fresh10']:.4f} "
              f"excess {strata[t]['excess10']:+.4f} "
              f"noise {strata[t]['noise10']:.4f}")

    mc3 = all(s["noise10"] > 0 for s in strata.values())
    lev = strata[1.0]
    mc2 = lev["excess10"] >= 3 * lev["noise10"]
    void = not (mc1 and mc2 and mc3)

    rho_track = float(stats.spearmanr(
        [strata[t]["excess10"] for t in nz],
        [drift[t] for t in nz]).statistic)
    b1 = rho_track >= 0.8
    b2 = lev["excess10"] >= 0.5 * lev["stale10"]
    verdict = "VOID" if void else ("PASS" if (b1 and b2) else "FAIL")

    print(f"\nMC1 dial interior: {'ok' if mc1 else 'VOID'}")
    print(f"MC2 lever resolvable at tau=1 "
          f"({lev['excess10'] / max(lev['noise10'], 1e-12):.1f}x, "
          f"need >=3): {'ok' if mc2 else 'VOID'}")
    print(f"MC3 noise honesty: {'ok' if mc3 else 'VOID'}")
    print(f"B1 excess tracks drift (spearman {rho_track:.3f}, "
          f"bar 0.8): {'PASS' if b1 else 'FAIL'}")
    print(f"B2 refresh removes >=50% at tau=1 "
          f"({lev['excess10'] / max(lev['stale10'], 1e-12):.0%}): "
          f"{'PASS' if b2 else 'FAIL'}")
    print("severing declaration: no feedback channel exists; "
          "severed control passes trivially, predicted in the "
          "sealed appendix (structural, not measured)")
    json.dump({"claim": "OT-14-v2", "seed": SEED, "floor": floor,
               "drift": {str(k): v for k, v in drift.items()},
               "dial_spearman": rho_dial,
               "strata": {str(k): v for k, v in strata.items()},
               "track_spearman": rho_track,
               "MC1": bool(mc1), "MC2": bool(mc2), "MC3": bool(mc3),
               "B1": bool(b1), "B2": bool(b2),
               "severing": "declared-trivial-by-construction",
               "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"\nOT-14 v2: {verdict} -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
