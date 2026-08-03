# GO-P-2026-054: second attempt at GO-9's Gaussian setting.
#
# GO-P-2026-052 MISSED 5/6.  Coordination saved 0.216 bits/symbol (65% of the
# asymptotic information) on the S-opaque record, and every gate passed EXCEPT
# C2: the M1 discount came in at 0.1316 against the sealed 0.40*gap = 0.1331
# bar -- short by 1.1%.  That bar is NOT moved here.  The only changes are a
# larger pre-committed design (n 12 -> 14, T 150 -> 250) and the strided-view
# speedup that makes it affordable; C1-C6 bars are byte-identical to 052.  If
# the shortfall was real rather than noise, this fails again and GO-9 stays
# [demonstrated] -- accepted in advance.
#
# Output: sentinel JSON ===GOLCG2-JSON===.  Tier B (Atlas CPU).  MIT.
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landauer_gaussian_v2_common import (exact_binom_ok,  # noqa: E402
                                         strided_argmin, thr_interp)
from landauer_coordinated_gaussian import DT, R_AN, RC_EXCESS  # noqa: E402

SEED = 20260813
N_BLK, TRIALS = 14, 250
RBS = [0.40, 0.55, 0.70, 0.85, 1.00, 1.15, 1.30, 1.45, 1.60, 1.75]
SHIFT = 7


def main():
    rng = np.random.default_rng(SEED)
    n, T = N_BLK, TRIALS
    nbits = int(np.ceil(n * (R_AN + RC_EXCESS)))
    Ncw = 1 << nbits
    Rc = nbits / n
    print("coordinated reset on a Gaussian source -- SECOND ATTEMPT (054)")
    print(f"seed={SEED}  n={n} T={T}  D={DT}  R={R_AN:.4f}  Rc={Rc:.4f}  "
          f"codebooks=2^{nbits} x2")
    t0 = time.time()

    sd = np.sqrt(1.0 - DT)
    cw1 = rng.normal(0.0, sd, size=(Ncw, 2 * n)).astype(np.float32)
    cw2 = rng.normal(0.0, sd, size=(Ncw, 2 * n)).astype(np.float32)
    c1sq = (cw1 * cw1).sum(1)
    c2sq = (cw2 * cw2).sum(1)
    n1sq_a = (cw1[:, :n] ** 2).sum(1)
    n1sq_b = (cw1[:, n:] ** 2).sum(1)
    n2sq_b = (cw2[:, :n] ** 2).sum(1)
    V1 = rng.normal(0, 1, size=(T, n))
    V2 = rng.normal(0, 1, size=(T, n))
    V3 = rng.normal(0, 1, size=(T, n))
    M1 = np.empty(T, dtype=np.int64)
    M2 = np.empty(T, dtype=np.int64)
    se = 0.0
    for t in range(T):
        u1 = np.concatenate([V1[t], V2[t]]).astype(np.float32)
        u2 = np.concatenate([V2[t], V3[t]]).astype(np.float32)
        M1[t] = int(np.argmin(c1sq - 2.0 * (cw1 @ u1)))
        M2[t] = int(np.argmin(c2sq - 2.0 * (cw2 @ u2)))
        se += float(((u1 - cw1[M1[t]]) ** 2).sum() + ((u2 - cw2[M2[t]]) ** 2).sum())
    d_hat = se / (4 * n * T)
    om = 1.0 - d_hat
    gap = -0.5 * np.log2(max(1.0 - om * om, 1e-12))
    w1 = 1.0 / (d_hat * om)
    w2 = 1.0 / (om * (1.0 - om * om))
    print(f"  encoded: d^={d_hat:.4f}  gap_pred={gap:.4f}  "
          f"C2 bar (0.40*gap)={0.40 * gap:.4f}  ({time.time()-t0:.0f}s)", flush=True)

    keys = ("m1_indep", "m1_coord", "m1_shuf", "m2_indep", "m2_coord", "m2_shuf")
    reg = {k: [] for k in keys}
    ctrl, chance = [], []
    for rb in RBS:
        bbits = max(1, int(np.ceil(n * rb)))
        nbins = 1 << bbits
        acc = {k: 0 for k in keys}
        okct = 0
        inv_mem = 0.0
        for t in range(T):
            ts = (t + SHIFT) % T
            v1 = V1[t].astype(np.float32)
            # ---- record 1
            b = int(M1[t]) % nbins
            va = cw1[b::nbins, :n]
            vb = cw1[b::nbins, n:]
            msz = va.shape[0]
            inv_mem += 1.0 / msz
            base = w1 * (n1sq_a[b::nbins] - 2.0 * (va @ v1))
            acc["m1_indep"] += strided_argmin(base, b, nbins, rng) == M1[t]
            for name, tt in (("m1_coord", t), ("m1_shuf", ts)):
                tgt = (om * cw2[M2[tt], :n]).astype(np.float32)
                sc = base + w2 * (n1sq_b[b::nbins] - 2.0 * (vb @ tgt))
                acc[name] += strided_argmin(sc, b, nbins, rng) == M1[t]
            okct += (b + nbins * int(rng.integers(0, msz))) == M1[t]
            # ---- record 2 (S-opaque: independent reset = chance)
            b = int(M2[t]) % nbins
            vb2 = cw2[b::nbins, :n]
            msz2 = vb2.shape[0]
            acc["m2_indep"] += (b + nbins * int(rng.integers(0, msz2))) == M2[t]
            for name, tt in (("m2_coord", t), ("m2_shuf", ts)):
                tgt = (om * cw1[M1[tt], n:]).astype(np.float32)
                sc = n2sq_b[b::nbins] - 2.0 * (vb2 @ tgt)
                acc[name] += strided_argmin(sc, b, nbins, rng) == M2[t]
        for k in keys:
            reg[k].append(1.0 - acc[k] / T)
        ctrl.append(1.0 - okct / T)
        chance.append(1.0 - inv_mem / T)
        print(f"  rb={rb:.2f}  " + "  ".join(f"{k}={reg[k][-1]:.2f}" for k in keys)
              + f"  ({time.time()-t0:.0f}s)", flush=True)

    thr = {k: thr_interp(reg[k], RBS) for k in keys}
    pred = dict(m1_indep=Rc - 0.5 * np.log2(1 / d_hat),
                m1_coord=Rc - 0.5 * np.log2(1 / d_hat) - gap,
                m2_indep=Rc, m2_coord=Rc - gap)
    disc1 = thr["m1_indep"] - thr["m1_coord"]
    disc2 = thr["m2_indep"] - thr["m2_coord"]
    verdict = dict(
        # --- C1-C5: bars byte-identical to the sealed GO-P-2026-052 ---
        C1_s_discount_m1=bool(abs(thr["m1_indep"] - pred["m1_indep"]) <= 0.25),
        C2_coordination_m1=bool(0.40 * gap <= disc1 <= gap + 0.15),
        C3_coordination_m2=bool(0.40 * gap <= disc2 <= gap + 0.15),
        C4_shuffled_null=bool(thr["m1_shuf"] >= thr["m1_indep"] - 0.16
                              and thr["m2_shuf"] >= thr["m2_indep"] - 0.16),
        C5_channel_realized=bool(0.28 <= d_hat <= 0.48),
        # --- C6: exact binomial in place of the normal approximation ---
        C6_uniform_control_exact=bool(all(
            exact_binom_ok(c, ch, T) for c, ch in zip(ctrl, chance))),
    )
    result = dict(
        claim="coordinated reset, Gaussian source -- second attempt",
        prereg="GO-P-2026-054", supersedes="GO-P-2026-052",
        seed=SEED, n=n, trials=T, d_hat=d_hat, Rc=Rc, gap_pred=gap,
        c2_bar=0.40 * gap, discount_m1=disc1, discount_m2=disc2,
        frac_m1=disc1 / gap, frac_m2=disc2 / gap,
        rb_grid=RBS, thresholds=thr, thresholds_pred=pred,
        regimes=reg, ctrl_err=ctrl, chance_err=chance,
        verdict=verdict,
        GOLCG2_supported=bool(all(verdict.values())),
        seconds_total=round(time.time() - t0, 1),
    )
    print(f"\nthresholds : { {k: round(v, 3) for k, v in thr.items()} }")
    print(f"gap {gap:.4f} | bar {0.40*gap:.4f} | m1 {disc1:.4f} "
          f"({disc1/gap:.2f}x)  m2 {disc2:.4f} ({disc2/gap:.2f}x)")
    print(f"verdict: {verdict}")
    print(f"GOLCG2_supported: {result['GOLCG2_supported']}")
    print("===GOLCG2-JSON===")
    print(json.dumps(result, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
