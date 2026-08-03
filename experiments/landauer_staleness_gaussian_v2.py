# GO-P-2026-053: second attempt at GO-8's Gaussian AR(1) setting.
#
# GO-P-2026-051 MISSED 3/5.  Its PHYSICS gate passed (the paper's Sec.-VI
# discount predicted the age-dependence to 0.154 bits over a 0.90-bit range);
# the two failures were G3 short by ONE trial (13/120 errors against a bar of
# 12) and G5 failing an INVALID normal-approximation control test at
# p = 0.99994 (N p (1-p) = 0.05, exact tail P(X>=1) = 5%).
#
# This attempt changes exactly two things and nothing else:
#   * G5 becomes an EXACT two-sided binomial test (the invalid instrument is
#     replaced, which is a correction, not a bar move);
#   * the design is larger -- n 20 -> 22, T 120 -> 250 -- pre-committed here.
# G1, G2, G3 and G4 carry over BYTE-IDENTICAL bars from the sealed 051.  If
# the one-trial G3 margin was luck, this run fails again and GO-8 stays
# [demonstrated]; that outcome is accepted in advance.
#
# Output: sentinel JSON ===GOLSG2-JSON===.  Tier B (Atlas CPU).  MIT.
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landauer_gaussian_v2_common import (exact_binom_ok,  # noqa: E402
                                         strided_argmin, thr_interp)
from landauer_staleness_gaussian import PHI, DT, R_AN, RC_EXCESS, discount  # noqa: E402

SEED = 20260812
N_BLK, TRIALS = 22, 250
AGES = [0, 1, 2, 4, 8, 16, 32]
RBS = [0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.95, 1.10, 1.25]


def main():
    rng = np.random.default_rng(SEED)
    n, T = N_BLK, TRIALS
    nbits = int(np.ceil(n * (R_AN + RC_EXCESS)))
    Ncw = 1 << nbits
    Rc = nbits / n
    print(f"staleness on a Gaussian AR(1) source -- SECOND ATTEMPT (053)")
    print(f"seed={SEED}  n={n} T={T}  phi={PHI}  D={DT}  R={R_AN:.4f}  "
          f"Rc={Rc:.4f}  codebook=2^{nbits}")
    t0 = time.time()

    cw = rng.normal(0.0, np.sqrt(1.0 - DT), size=(Ncw, n)).astype(np.float32)
    cwsq = (cw * cw).sum(axis=1)
    X0 = rng.normal(0.0, 1.0, size=(T, n))
    M = np.empty(T, dtype=np.int64)
    se = cxy = 0.0
    for t in range(T):
        sc = cwsq - 2.0 * (cw @ X0[t].astype(np.float32))
        M[t] = int(np.argmin(sc))
        xh = cw[M[t]].astype(np.float64)
        se += float(((X0[t] - xh) ** 2).sum())
        cxy += float((X0[t] * xh).sum())
    D_hat = se / (n * T)
    c_hat = cxy / (n * T)
    print(f"  encoded: D^={D_hat:.4f}  c^={c_hat:.4f}  ({time.time()-t0:.0f}s)",
          flush=True)

    rows = []
    for age in AGES:
        rho = PHI ** age
        Xt = rho * X0 + np.sqrt(max(1.0 - rho * rho, 0.0)) * \
            rng.normal(0.0, 1.0, size=(T, n))
        thr_pred = Rc - discount(rho * rho, D_hat)
        row = dict(age=age, rho=float(rho), thr_pred=float(thr_pred),
                   rb=[], err_si=[], err_ctrl=[], chance_err=[])
        for rb in RBS:
            bbits = max(1, int(np.ceil(n * rb)))
            nbins = 1 << bbits
            ok_si = ok_ct = 0
            inv_mem = 0.0
            for t in range(T):
                b = int(M[t]) % nbins
                view = cw[b::nbins]                     # strided VIEW, no copy
                msz = view.shape[0]
                inv_mem += 1.0 / msz
                target = (c_hat * rho * Xt[t]).astype(np.float32)
                sc = cwsq[b::nbins] - 2.0 * (view @ target)
                ok_si += strided_argmin(sc, b, nbins, rng) == M[t]
                ok_ct += (b + nbins * int(rng.integers(0, msz))) == M[t]
            row["rb"].append(float(rb))
            row["err_si"].append(1.0 - ok_si / T)
            row["err_ctrl"].append(1.0 - ok_ct / T)
            row["chance_err"].append(1.0 - inv_mem / T)
        row["thr_meas"] = thr_interp(row["err_si"], RBS)
        rows.append(row)
        print(f"  age={age:3d} rho={rho:.3f} thr_pred={thr_pred:.3f} "
              f"thr_meas={row['thr_meas']:.3f}  "
              f"err={['%.2f' % e for e in row['err_si']]}  "
              f"({time.time()-t0:.0f}s)", flush=True)

    thr_m = [r["thr_meas"] for r in rows]
    i_fix = RBS.index(0.35)
    err_fix = [r["err_si"][i_fix] for r in rows]
    usable = [r for r in rows
              if r["thr_meas"] == r["thr_meas"] and r["thr_meas"] < RBS[-1] - 1e-9]
    devs = [r["thr_meas"] - r["thr_pred"] for r in usable]
    rise_m = max(r["thr_meas"] for r in usable) - min(r["thr_meas"] for r in usable)
    rise_p = max(r["thr_pred"] for r in usable) - min(r["thr_pred"] for r in usable)
    Npool = T * len(rows)
    ctrl_p = [float(np.mean([r["err_ctrl"][j] for r in rows])) for j in range(len(RBS))]
    chan_p = [float(np.mean([r["chance_err"][j] for r in rows])) for j in range(len(RBS))]
    verdict = dict(
        # --- G1-G4: bars byte-identical to the sealed GO-P-2026-051 ---
        G1_threshold_monotone=bool(all(thr_m[i + 1] >= thr_m[i] - 1e-9
                                       for i in range(len(thr_m) - 1))),
        G2_tracks_gaussian_discount=bool(
            len(usable) >= 6 and max(abs(d) for d in devs) <= 0.20
            and 0.70 <= rise_m / rise_p <= 1.30),
        G3_same_binrate_flips_with_age=bool(err_fix[0] <= 0.10
                                            and min(err_fix[-2:]) >= 0.90),
        G4_channel_realized=bool(0.22 <= D_hat <= 0.36),
        # --- G5: invalid normal approximation replaced by an EXACT test ---
        G5_no_si_control_exact=bool(all(
            exact_binom_ok(ctrl_p[j], chan_p[j], Npool) for j in range(len(RBS)))),
    )
    result = dict(
        claim="staleness-work complement, Gaussian AR(1) -- second attempt",
        prereg="GO-P-2026-053", supersedes="GO-P-2026-051",
        seed=SEED, n=n, trials=T, phi=PHI, D_hat=D_hat, c_hat=c_hat, Rc=Rc,
        ages=AGES, rb_grid=RBS, rows=rows,
        thr_measured=thr_m, thr_predicted=[r["thr_pred"] for r in rows],
        deviations_uncensored=devs,
        dev_max_abs=float(max(abs(d) for d in devs)),
        rise_measured=float(rise_m), rise_predicted=float(rise_p),
        err_at_rb035=err_fix, ctrl_pooled=ctrl_p, chance_pooled=chan_p,
        n_pooled=Npool, verdict=verdict,
        GOLSG2_supported=bool(all(verdict.values())),
        seconds_total=round(time.time() - t0, 1),
    )
    print(f"\nthr measured : {[round(v, 3) for v in thr_m]}")
    print(f"thr predicted: {[round(r['thr_pred'], 3) for r in rows]}")
    print(f"err@rb=0.35  : {[round(e, 3) for e in err_fix]}   (G3 bar: <=0.10 @age0)")
    print(f"verdict: {verdict}")
    print(f"GOLSG2_supported: {result['GOLSG2_supported']}")
    print("===GOLSG2-JSON===")
    print(json.dumps(result, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
