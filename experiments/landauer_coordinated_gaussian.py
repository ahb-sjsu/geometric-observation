# GO-9 second setting (GO-P-2026-052): coordinated reset on a GAUSSIAN
# source -- an independent source family from the binary instance of
# GO-P-2026-050.
#
# X = (V1, V2, V3), each ~ N(0, I_n) independent.  Record M1 describes
# U1 = (V1, V2), record M2 describes U2 = (V2, V3) (shared component V2);
# reset side information S = V1, so M2 is S-opaque.  Both records are binned
# and recovered in-bin by ML under:
#   independent reset : M1 from (bin, V1);  M2 from bin alone (S useless)
#   coordinated reset : + the OTHER record's reconstruction of V2, used as a
#                       noisy observation with the exact Gaussian weights
#                       w1 = 1/(d(1-d)) on the S-known half and
#                       w2 = 1/((1-d)(1-(1-d)^2)) on the shared half
#   shuffled null     : coordinated, other record from a mismatched trial
#   uniform control   : chance (pooled 4-sigma gate)
# For per-component reverse channels at distortion d, the two records'
# reconstructions of V2 have correlation (1-d), so the predicted coordination
# discount is the Gaussian analogue of the binary  1 - h2(d*d):
#     gap = -1/2 log2(1 - (1-d)^2)   bits/symbol,
# and the S-discount on M1 is 1/2 log2(1/d).
#
# Usage: python experiments/landauer_coordinated_gaussian.py [--pilot]
# Output: sentinel JSON ===GOLCG-JSON===.  Tier B (Atlas CPU).  MIT.
import argparse
import json
import sys
import time

import numpy as np

SEED = 20260811
DT = 0.35                     # per-component MSE target
R_AN = 2.0 * 0.5 * np.log2(1.0 / DT)      # two described components
RC_EXCESS = 0.03


def thr_of(errs, rbs, bar=0.25):
    """Continuous threshold: linear interpolation of the error curve's crossing
    of `bar`.  Grid-snapping quantizes discounts to multiples of the grid step
    (pilot: a 0.33-bit effect measured as exactly 0.15), which both biases the
    level and destroys resolution; interpolation removes that."""
    for i, e in enumerate(errs):
        if e <= bar:
            if i == 0:
                return float(rbs[0])
            e0, e1 = errs[i - 1], e
            if e0 <= e1:
                return float(rbs[i])
            f = (e0 - bar) / (e0 - e1)
            return float(rbs[i - 1] + f * (rbs[i] - rbs[i - 1]))
    return float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    args = ap.parse_args()
    rng = np.random.default_rng(SEED + (1 if args.pilot else 0))
    n, T = (10, 60) if args.pilot else (12, 150)
    rbs = [0.40, 0.55, 0.70, 0.85, 1.00, 1.15, 1.30, 1.45, 1.60, 1.75]
    nbits = int(np.ceil(n * (R_AN + RC_EXCESS)))
    Ncw = 1 << nbits
    Rc = nbits / n
    print(f"coordinated reset on a Gaussian source "
          f"({'PILOT' if args.pilot else 'FULL'})  seed={SEED}  n={n} T={T}")
    print(f"D={DT}  R={R_AN:.4f}  Rc={Rc:.4f}  codebooks=2^{nbits} x2")
    t0 = time.time()

    sd = np.sqrt(1.0 - DT)
    cw1 = rng.normal(0.0, sd, size=(Ncw, 2 * n)).astype(np.float32)  # (V1,V2)
    cw2 = rng.normal(0.0, sd, size=(Ncw, 2 * n)).astype(np.float32)  # (V2,V3)
    n1sq_a = (cw1[:, :n] ** 2).sum(1)      # V1 half
    n1sq_b = (cw1[:, n:] ** 2).sum(1)      # V2 half of record 1
    n2sq_b = (cw2[:, :n] ** 2).sum(1)      # V2 half of record 2
    V1 = rng.normal(0, 1, size=(T, n))
    V2 = rng.normal(0, 1, size=(T, n))
    V3 = rng.normal(0, 1, size=(T, n))
    M1 = np.empty(T, dtype=np.int64)
    M2 = np.empty(T, dtype=np.int64)
    se = 0.0
    for t in range(T):
        u1 = np.concatenate([V1[t], V2[t]]).astype(np.float32)
        u2 = np.concatenate([V2[t], V3[t]]).astype(np.float32)
        s1 = (cw1 * cw1).sum(1) - 2.0 * (cw1 @ u1)
        s2 = (cw2 * cw2).sum(1) - 2.0 * (cw2 @ u2)
        M1[t] = int(np.argmin(s1)); M2[t] = int(np.argmin(s2))
        se += float(((u1 - cw1[M1[t]]) ** 2).sum() + ((u2 - cw2[M2[t]]) ** 2).sum())
    d_hat = se / (4 * n * T)                       # per component-symbol
    om = 1.0 - d_hat
    gap = -0.5 * np.log2(max(1.0 - om * om, 1e-12))
    w1 = 1.0 / (d_hat * om)
    w2 = 1.0 / (om * (1.0 - om * om))
    print(f"  encoded: d^={d_hat:.4f}  gap_pred={gap:.4f}  "
          f"S_discount_pred={0.5 * np.log2(1 / d_hat):.4f}", flush=True)

    shift = 7
    keys = ("m1_indep", "m1_coord", "m1_shuf", "m2_indep", "m2_coord", "m2_shuf")
    reg = {k: [] for k in keys}
    ctrl, chance = [], []
    for rb in rbs:
        bbits = max(1, int(np.ceil(n * rb)))
        nbins = 1 << bbits
        acc = {k: 0 for k in keys}
        okct = 0
        inv_mem = 0.0
        for t in range(T):
            ts = (t + shift) % T
            v1 = V1[t].astype(np.float32)
            # ---- record 1
            mem = np.arange(int(M1[t]) % nbins, Ncw, nbins, dtype=np.int64)
            inv_mem += 1.0 / mem.size
            base = w1 * (n1sq_a[mem] - 2.0 * (cw1[mem, :n] @ v1))
            pick = mem[np.flatnonzero(base == base.min())]
            acc["m1_indep"] += int(pick[rng.integers(0, pick.size)]) == M1[t]
            for name, tt in (("m1_coord", t), ("m1_shuf", ts)):
                tgt = (om * cw2[M2[tt], :n]).astype(np.float32)
                sc = base + w2 * (n1sq_b[mem] - 2.0 * (cw1[mem, n:] @ tgt))
                pick = mem[np.flatnonzero(sc == sc.min())]
                acc[name] += int(pick[rng.integers(0, pick.size)]) == M1[t]
            okct += int(mem[rng.integers(0, mem.size)]) == M1[t]
            # ---- record 2 (S-opaque: independent = chance)
            mem = np.arange(int(M2[t]) % nbins, Ncw, nbins, dtype=np.int64)
            acc["m2_indep"] += int(mem[rng.integers(0, mem.size)]) == M2[t]
            for name, tt in (("m2_coord", t), ("m2_shuf", ts)):
                tgt = (om * cw1[M1[tt], n:]).astype(np.float32)
                sc = n2sq_b[mem] - 2.0 * (cw2[mem, :n] @ tgt)
                pick = mem[np.flatnonzero(sc == sc.min())]
                acc[name] += int(pick[rng.integers(0, pick.size)]) == M2[t]
        for k in keys:
            reg[k].append(1.0 - acc[k] / T)
        ctrl.append(1.0 - okct / T)
        chance.append(1.0 - inv_mem / T)
        print(f"  rb={rb:.2f}  " + "  ".join(f"{k}={reg[k][-1]:.2f}" for k in keys),
              flush=True)

    thr = {k: thr_of(reg[k], rbs) for k in keys}
    pred = dict(m1_indep=Rc - 0.5 * np.log2(1 / d_hat),
                m1_coord=Rc - 0.5 * np.log2(1 / d_hat) - gap,
                m2_indep=Rc, m2_coord=Rc - gap)
    se_ = [np.sqrt(max(c * (1 - c), 1e-12) / T) for c in chance]
    verdict = dict(
        C1_s_discount_m1=bool(abs(thr["m1_indep"] - pred["m1_indep"]) <= 0.25),
        # The asymptotic gap has no exact finite-n counterpart, and the pilot
        # realized ~50-60% of it at n=10.  Gate that coordination saves a
        # SUBSTANTIAL fraction of the predicted information and cannot
        # materially exceed it; the realized fraction is reported.
        C2_coordination_m1=bool(
            0.40 * gap <= thr["m1_indep"] - thr["m1_coord"] <= gap + 0.15),
        C3_coordination_m2=bool(
            0.40 * gap <= thr["m2_indep"] - thr["m2_coord"] <= gap + 0.15),
        C4_shuffled_null=bool(thr["m1_shuf"] >= thr["m1_indep"] - 0.16
                              and thr["m2_shuf"] >= thr["m2_indep"] - 0.16),
        C5_channel_realized=bool(0.28 <= d_hat <= 0.48),
        C6_uniform_control=bool(all(abs(e - c) <= 4.0 * s + 1e-9
                                    for e, c, s in zip(ctrl, chance, se_))),
    )
    result = dict(
        claim="coordinated reset saves the shared-structure information, Gaussian second setting",
        prereg="GO-P-2026-052",
        second_setting_for="GO-9 (binary instance = GO-P-2026-050)",
        mode="pilot" if args.pilot else "full",
        seed=SEED, n=n, trials=T, d_hat=d_hat, Rc=Rc, gap_pred=gap,
        rb_grid=rbs, thresholds=thr, thresholds_pred=pred,
        regimes=reg, ctrl_err=ctrl, chance_err=chance,
        verdict=verdict,
        GOLCG_coordination_gaussian_supported=bool(all(verdict.values())),
        seconds_total=round(time.time() - t0, 1),
    )
    print(f"\nthresholds : { {k: round(v, 3) for k, v in thr.items()} }")
    print(f"predicted  : { {k: round(v, 3) for k, v in pred.items()} }")
    print(f"gap pred {gap:.3f} | measured m1 "
          f"{thr['m1_indep'] - thr['m1_coord']:.3f}  m2 "
          f"{thr['m2_indep'] - thr['m2_coord']:.3f}")
    print(f"verdict: {verdict}")
    print(f"GOLCG_coordination_gaussian_supported: "
          f"{result['GOLCG_coordination_gaussian_supported']}")
    print("===GOLCG-JSON===")
    print(json.dumps(result, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
