# GO-8 second setting (GO-P-2026-051): the staleness-work complement on a
# GAUSSIAN AR(1) source -- an independent source family from the binary
# Markov instance of GO-P-2026-048/049, and simultaneously an operational
# test of the paper's Sec.-VI scalar-corner discount formula.
#
# X_0 ~ N(0, I_n) is described by a random codebook (index M, MSE target D);
# the retained side information at age t is the AR(1) state
#     X_t = phi^t X_0 + sqrt(1 - phi^{2t}) Z,      rho_t = phi^t,
# so (X_0, X_t) is jointly Gaussian with correlation rho_t -- exactly the
# paper's scalar-corner setting with a decaying rho.  M is binned ONCE; the
# reset decoder recovers it in-bin by ML against the conditional mean
# c_hat * rho_t * x_t.  The paper's discount then predicts the threshold
#     thr(t) = Rc - 1/2 log2( 1 / (1 - rho_t^2 + rho_t^2 * D_hat) ),
# which RISES with age from Rc - R (fresh record, side information reveals
# the source) to Rc (dead correlation).  Same record, same bins, same
# decoder; age is the only manipulated variable.
#
# Usage: python experiments/landauer_staleness_gaussian.py [--pilot]
# Output: sentinel JSON ===GOLSG-JSON===.  Tier B (Atlas CPU).  MIT.
import argparse
import json
import sys
import time

import numpy as np

SEED = 20260810
PHI = 0.9
DT = 0.25
R_AN = 0.5 * np.log2(1.0 / DT)
RC_EXCESS = 0.03


def discount(rho2, D):
    """Paper Sec.-VI side-information discount, sigma = 1."""
    return 0.5 * np.log2(1.0 / (1.0 - rho2 + rho2 * D))


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
    ages = [0, 1, 2, 4, 8, 16, 32]
    rbs = [0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.95, 1.10, 1.25]
    n, T = (14, 80) if args.pilot else (20, 120)
    nbits = int(np.ceil(n * (R_AN + RC_EXCESS)))
    Ncw = 1 << nbits
    Rc = nbits / n
    print(f"staleness on a Gaussian AR(1) source "
          f"({'PILOT' if args.pilot else 'FULL'})  seed={SEED}  n={n} T={T}")
    print(f"phi={PHI}  D={DT}  R={R_AN:.4f}  Rc={Rc:.4f}  codebook=2^{nbits}")
    t0 = time.time()

    cw = rng.normal(0.0, np.sqrt(1.0 - DT), size=(Ncw, n)).astype(np.float32)
    cw2 = (cw * cw).sum(axis=1)
    X0 = rng.normal(0.0, 1.0, size=(T, n))
    M = np.empty(T, dtype=np.int64)
    se = cxy = 0.0
    for t in range(T):
        sc = cw2 - 2.0 * (cw @ X0[t].astype(np.float32))
        M[t] = int(np.argmin(sc))
        xh = cw[M[t]].astype(np.float64)
        se += float(((X0[t] - xh) ** 2).sum())
        cxy += float((X0[t] * xh).sum())
    D_hat = se / (n * T)
    c_hat = cxy / (n * T)
    print(f"  encoded: D^={D_hat:.4f}  c^={c_hat:.4f}", flush=True)

    rows = []
    for age in ages:
        rho = PHI ** age
        Xt = rho * X0 + np.sqrt(max(1.0 - rho * rho, 0.0)) * \
            rng.normal(0.0, 1.0, size=(T, n))
        thr_pred = Rc - discount(rho * rho, D_hat)
        row = dict(age=age, rho=float(rho), thr_pred=float(thr_pred),
                   rb=[], err_si=[], err_ctrl=[], chance_err=[])
        for rb in rbs:
            bbits = max(1, int(np.ceil(n * rb)))
            nbins = 1 << bbits
            ok_si = ok_ct = 0
            inv_mem = 0.0
            for t in range(T):
                mem = np.arange(int(M[t]) % nbins, Ncw, nbins, dtype=np.int64)
                inv_mem += 1.0 / mem.size
                target = (c_hat * rho * Xt[t]).astype(np.float32)
                sc = cw2[mem] - 2.0 * (cw[mem] @ target)
                pick = mem[np.flatnonzero(sc == sc.min())]
                ok_si += int(pick[rng.integers(0, pick.size)]) == M[t]
                ok_ct += int(mem[rng.integers(0, mem.size)]) == M[t]
            row["rb"].append(float(rb))
            row["err_si"].append(1.0 - ok_si / T)
            row["err_ctrl"].append(1.0 - ok_ct / T)
            row["chance_err"].append(1.0 - inv_mem / T)
        row["thr_meas"] = thr_of(row["err_si"], rbs)
        rows.append(row)
        print(f"  age={age:3d} rho={rho:.3f} thr_pred={thr_pred:.3f} "
              f"thr_meas={row['thr_meas']:.3f}  "
              f"err={['%.2f' % e for e in row['err_si']]}", flush=True)

    thr_m = [r["thr_meas"] for r in rows]
    i_fix = rbs.index(0.35)
    err_fix = [r["err_si"][i_fix] for r in rows]
    # With interpolated thresholds the deviation from the asymptotic Gaussian
    # discount is small but NOT a constant offset (pilot: +0.15 at young ages
    # drifting to -0.04 at old ages -- the measured rise is slightly
    # compressed).  So gate absolute agreement at every uncensored age plus
    # the dynamic range, over a predicted rise of ~0.92 bits/symbol; there is
    # no exact finite-n counterpart to the asymptotic formula to gate tighter.
    usable = [r for r in rows
              if r["thr_meas"] == r["thr_meas"] and r["thr_meas"] < rbs[-1] - 1e-9]
    devs = [r["thr_meas"] - r["thr_pred"] for r in usable]
    rise_m = (max(r["thr_meas"] for r in usable)
              - min(r["thr_meas"] for r in usable)) if usable else float("nan")
    rise_p = (max(r["thr_pred"] for r in usable)
              - min(r["thr_pred"] for r in usable)) if usable else float("nan")
    verdict = dict(
        G1_threshold_monotone=bool(all(thr_m[i + 1] >= thr_m[i] - 1e-9
                                       for i in range(len(thr_m) - 1))),
        G2_tracks_gaussian_discount=bool(
            len(usable) >= 6 and max(abs(d) for d in devs) <= 0.20
            and 0.70 <= rise_m / rise_p <= 1.30),
        G3_same_binrate_flips_with_age=bool(err_fix[0] <= 0.10
                                            and min(err_fix[-2:]) >= 0.90),
        G4_channel_realized=bool(0.22 <= D_hat <= 0.36),
        G5_no_si_control=bool(all(
            abs(np.mean([r["err_ctrl"][j] for r in rows])
                - np.mean([r["chance_err"][j] for r in rows]))
            <= 4.0 * np.sqrt(max(np.mean([r["chance_err"][j] for r in rows])
                                 * (1 - np.mean([r["chance_err"][j] for r in rows])),
                                 1e-12) / (T * len(rows))) + 1e-9
            for j in range(len(rbs)))),
    )
    result = dict(
        claim="staleness-work complement, Gaussian AR(1) second setting",
        prereg="GO-P-2026-051",
        second_setting_for="GO-8 (binary Markov instance = GO-P-2026-048/049)",
        mode="pilot" if args.pilot else "full",
        seed=SEED, n=n, trials=T, phi=PHI, D_hat=D_hat, c_hat=c_hat, Rc=Rc,
        ages=ages, rb_grid=rbs, rows=rows,
        thr_measured=thr_m, thr_predicted=[r["thr_pred"] for r in rows],
        deviations_uncensored=devs,
        dev_max_abs=float(max(abs(d) for d in devs)) if devs else float("nan"),
        rise_measured=float(rise_m), rise_predicted=float(rise_p),
        verdict=verdict,
        GOLSG_staleness_gaussian_supported=bool(all(verdict.values())),
        seconds_total=round(time.time() - t0, 1),
    )
    print(f"\nthr measured : {[round(v, 3) for v in thr_m]}")
    print(f"thr predicted: {[round(r['thr_pred'], 3) for r in rows]}")
    print(f"verdict: {verdict}")
    print(f"GOLSG_staleness_gaussian_supported: "
          f"{result['GOLSG_staleness_gaussian_supported']}")
    print("===GOLSG-JSON===")
    print(json.dumps(result, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
