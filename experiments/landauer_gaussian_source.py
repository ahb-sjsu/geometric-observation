# Cross-source replication of GO-7 on a SCALAR GAUSSIAN source
# (GO-P-2026-046): the operational rate-work separation demonstrated by
# GO-P-2026-043/045 on the binary two-bit source, rerun on a continuous
# source family -- X ~ N(0,1) with jointly Gaussian reset side information
# at rho = 0.98, MSE distortion, target D = 0.25.  This is the paper's own
# scalar-corner setting (new Sec. VI), so the run also exercises the
# Gaussian theory operationally: analytic R = 1.000, L = 0.081 bits/symbol.
#
# Scheme per blocklength n: one random codebook of 2^ceil(n(R+0.03))
# codewords i.i.d. N(0, 1-D) (the reverse-channel marginal, float32);
# minimum-distortion (= ML) encoding; the stored index M is random-binned at
# bin rate r_b and recovered from (bin, s^n) by in-bin ML -- the nearest
# codeword to c_hat*rho*s^n, the conditional mean of X_hat given S under the
# realized channel moments.  Controls: a no-side-information decoder
# (uniform in-bin pick) and a below-content bin rate.  Empirical channel
# reported via second moments (c_hat, v_hat) with the jointly-Gaussian
# moment surrogates R_mom = 1/2 log2(v/(v-c^2)),
# L_mom = 1/2 log2((v-rho^2 c^2)/(v-c^2)).
#
# Usage: python experiments/landauer_gaussian_source.py [--pilot]
# Output: sentinel JSON ===GOLGS-JSON===.  Tier B (Atlas CPU).  MIT.
import argparse
import json
import sys
import time

import numpy as np

SEED = 20260805
RHO = 0.98
DT = 0.25
R_AN = 0.5 * np.log2(1.0 / DT)                     # 1.0000
C1 = 1.0 - RHO * RHO                               # 0.0396
L_AN = 0.5 * np.log2((C1 + RHO * RHO * DT) / DT)   # 0.0810
RC_EXCESS = 0.03


def run_gauss(ngrid, trials, rbs, rng):
    rows = []
    for n, T in zip(ngrid, trials):
        t0 = time.time()
        nbits = int(np.ceil(n * (R_AN + RC_EXCESS)))
        Ncw = 1 << nbits
        cw = rng.normal(0.0, np.sqrt(1.0 - DT), size=(Ncw, n)).astype(np.float32)
        cw2 = (cw * cw).sum(axis=1)                # ||cw||^2, reused
        X = rng.normal(0.0, 1.0, size=(T, n))
        S = RHO * X + np.sqrt(1.0 - RHO * RHO) * rng.normal(0.0, 1.0, size=(T, n))
        M = np.empty(T, dtype=np.int64)
        se = 0.0
        cxy = vy = 0.0
        for t in range(T):
            x32 = X[t].astype(np.float32)
            score = cw2 - 2.0 * (cw @ x32)          # ||cw - x||^2 up to const
            M[t] = int(np.argmin(score))
            xh = cw[M[t]].astype(np.float64)
            se += float(((X[t] - xh) ** 2).sum())
            cxy += float((X[t] * xh).sum())
            vy += float((xh * xh).sum())
        D_hat = se / (n * T)
        c_hat = cxy / (n * T)
        v_hat = vy / (n * T)
        R_mom = 0.5 * np.log2(v_hat / max(v_hat - c_hat ** 2, 1e-12))
        L_mom = 0.5 * np.log2((v_hat - RHO * RHO * c_hat ** 2)
                              / max(v_hat - c_hat ** 2, 1e-12))
        row = dict(n=n, trials=T, codebook_bits=nbits, D_hat=D_hat,
                   c_hat=c_hat, v_hat=v_hat, R_mom=float(R_mom),
                   L_mom=float(L_mom), rb=[], err_si=[], err_ctrl=[])
        for rb in rbs:
            bbits = max(1, int(np.ceil(n * rb)))
            nbins = 1 << bbits
            ok_si = ok_ct = 0
            for t in range(T):
                b = int(M[t]) % nbins
                members = np.arange(b, Ncw, nbins, dtype=np.int64)
                target = (c_hat * RHO * S[t]).astype(np.float32)
                sc = cw2[members] - 2.0 * (cw[members] @ target)
                mins = members[np.flatnonzero(sc == sc.min())]
                ok_si += int(mins[rng.integers(0, mins.size)]) == M[t]
                ok_ct += int(members[rng.integers(0, members.size)]) == M[t]
            row["rb"].append(float(rb))
            row["err_si"].append(1.0 - ok_si / T)
            row["err_ctrl"].append(1.0 - ok_ct / T)
        row["seconds"] = round(time.time() - t0, 1)
        rows.append(row)
        print(f"  n={n:3d} T={T} cw=2^{nbits}  D^={D_hat:.3f} R_mom={R_mom:.3f} "
              f"L_mom={L_mom:.3f}  err_si={['%.2f' % e for e in row['err_si']]}"
              f"  ({row['seconds']}s)", flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    args = ap.parse_args()
    rng = np.random.default_rng(SEED + (1 if args.pilot else 0))
    rbs = [0.05, 0.12, 0.20, 0.28, 0.36, 0.60]
    if args.pilot:
        ngrid = [8, 12, 16, 20]
        trials = [100, 100, 100, 80]
    else:
        ngrid = [8, 12, 16, 20, 24]
        trials = [200, 200, 200, 200, 200]
    print(f"GO-7 cross-source replication: scalar Gaussian "
          f"({'PILOT' if args.pilot else 'FULL'})  seed={SEED}")
    print(f"rho={RHO}  D={DT}  analytic R={R_AN:.4f}  L={L_AN:.4f}  "
          f"I(Xh;S)={R_AN - L_AN:.4f}  codebook rate={R_AN + RC_EXCESS:.4f}")
    t0 = time.time()
    rows = run_gauss(ngrid, trials, rbs, rng)

    iSEP = rbs.index(0.36)
    iLOW = rbs.index(0.05)
    iDEEP = rbs.index(0.60)
    err_sep = [r["err_si"][iSEP] for r in rows]
    err_low = [r["err_si"][iLOW] for r in rows]
    err_low_big = [r["err_si"][iLOW] for r in rows if r["n"] >= 12]
    ctrl_sep = [r["err_ctrl"][iSEP] for r in rows if r["n"] >= 16]
    half = len(err_sep) // 2
    last = rows[-1]
    verdict = dict(
        # bars calibrated by the logged pilot (integer-ceiling jumps in the
        # effective bin rate make per-n error noisy; sealed in GO-P-2026-046)
        G1_separation_decodes=bool(err_sep[-1] <= 0.20 and err_sep[-2] <= 0.30
                                   and np.mean(err_sep[half:]) <= np.mean(err_sep[:half])),
        G2_bin_rate_below_050R=bool(0.36 <= 0.50 * last["R_mom"]),
        G3_converse_low_rb_fails=bool(min(err_low_big) >= 0.30
                                      and err_low[-1] >= 0.40),
        G4_side_info_specific=bool(min(ctrl_sep) >= 0.90) if ctrl_sep else False,
        G5_channel_realized=bool(0.22 <= last["D_hat"] <= 0.36
                                 and 0.72 <= last["R_mom"] <= 1.00
                                 and 0.02 <= last["L_mom"] <= 0.15),
        G6_deep_decode=bool(last["err_si"][iDEEP] <= 0.02),
    )
    result = dict(
        claim="GO-7 cross-source replication (scalar Gaussian, MSE, rho=0.98)",
        prereg="GO-P-2026-046",
        mode="pilot" if args.pilot else "full",
        seed=SEED,
        target=dict(rho=RHO, D=DT, R=R_AN, L=L_AN, codebook_excess=RC_EXCESS),
        rb_grid=rbs,
        rows=rows,
        err_at_rb036=err_sep,
        err_at_rb005=err_low,
        verdict=verdict,
        GOLGS_crosssource_supported=bool(all(verdict.values())),
        seconds_total=round(time.time() - t0, 1),
    )
    print(f"\nverdict: {verdict}")
    print(f"GOLGS_crosssource_supported: {result['GOLGS_crosssource_supported']}")
    print("===GOLGS-JSON===")
    print(json.dumps(result, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
