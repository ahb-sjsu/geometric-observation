# Operational staleness demonstration (GO-P-2026-048): the paper's
# staleness-work complement (stale Markov record) made operational.  A record
# M -- the random-codebook index of a lossy description of X_0^n (binary
# symmetric Markov chain, flip p = 0.05/step) -- is random-binned ONCE; the
# reset decoder recovers M from (bin, X_t^n), the chain state at age t.  As
# the side information ages, the decodable bin-rate threshold must RISE,
# tracking  thr(t) ~ Rc - 1 + h2(d^ * q_t)  (binary convolution *, q_t the
# age-t flip probability), until at large t the side information is useless
# and the threshold approaches the full description rate.  Same record, same
# bins, same decoder -- only the age changes: relevance lost to time is
# gained exactly as conditional erasure work.
#
# Usage: python experiments/landauer_staleness.py [--pilot]
# Output: sentinel JSON ===GOLST-JSON===.  Tier B (Atlas CPU).  MIT.
import argparse
import json
import sys
import time

import numpy as np

SEED = 20260807
P_FLIP = 0.05
D_TGT = 0.11                      # per-symbol Hamming distortion target
R_AN = 1.0 - (-D_TGT * np.log2(D_TGT) - (1 - D_TGT) * np.log2(1 - D_TGT))
RC_EXCESS = 0.03

_LUT = np.array([bin(i).count("1") for i in range(65536)], dtype=np.uint16)


def pop64(a):
    return _LUT[np.ascontiguousarray(a).view(np.uint16).reshape(-1, 4)].sum(
        axis=1, dtype=np.int64)


def h2(t):
    t = float(t)
    if t <= 0.0 or t >= 1.0:
        return 0.0
    return -t * np.log2(t) - (1 - t) * np.log2(1 - t)


def conv(a, b):
    return a * (1 - b) + b * (1 - a)


def q_age(t):
    return 0.5 * (1.0 - (1.0 - 2.0 * P_FLIP) ** t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    args = ap.parse_args()
    rng = np.random.default_rng(SEED + (1 if args.pilot else 0))
    ages = [0, 1, 2, 4, 8, 16, 32, 64]
    rbs = [0.10, 0.175, 0.25, 0.325, 0.40, 0.475, 0.55, 0.625]
    if args.pilot:
        n, T = 32, 80
    else:
        n, T = 40, 200
    nbits = int(np.ceil(n * (R_AN + RC_EXCESS)))
    Ncw = 1 << nbits
    Rc = nbits / n
    print(f"staleness operational run ({'PILOT' if args.pilot else 'FULL'})  "
          f"seed={SEED}  n={n} T={T}")
    print(f"chain p={P_FLIP}  d_tgt={D_TGT}  R={R_AN:.4f}  Rc={Rc:.4f}  "
          f"codebook=2^{nbits}")
    t0 = time.time()

    cw = rng.integers(0, 1 << n, size=Ncw, dtype=np.uint64)
    x0 = rng.integers(0, 1 << n, size=T, dtype=np.uint64)
    M = np.empty(T, dtype=np.int64)
    dbits = 0
    for t in range(T):
        sc = pop64(cw ^ x0[t])
        mins = np.flatnonzero(sc == sc.min())
        M[t] = int(mins[rng.integers(0, mins.size)])
        dbits += int(sc[M[t]])
    d_hat = dbits / (n * T)
    print(f"  encoded: d^ = {d_hat:.4f}", flush=True)

    # age the side information: per-bit flips with prob q_t (exact marginal
    # of the chain at age t; the per-letter Markov structure is all the
    # decoder uses, so sampling the marginal is faithful)
    rows = []
    for age in ages:
        qt = q_age(age)
        flips = np.zeros(T, dtype=np.uint64)
        if age > 0:
            fb = (rng.random((T, n)) < qt)
            for t in range(T):
                v = np.uint64(0)
                for i in np.flatnonzero(fb[t]):
                    v |= np.uint64(1) << np.uint64(i)
                flips[t] = v
        xt = x0 ^ flips
        thr_pred = Rc - 1.0 + h2(conv(d_hat, qt))
        row = dict(age=age, q_t=qt, thr_pred=float(thr_pred), rb=[],
                   err_si=[], err_ctrl=[])
        for rb in rbs:
            bbits = max(1, int(np.ceil(n * rb)))
            nbins = 1 << bbits
            ok_si = ok_ct = 0
            inv_mem = 0.0
            for t in range(T):
                b = int(M[t]) % nbins
                members = np.arange(b, Ncw, nbins, dtype=np.int64)
                sc = pop64(cw[members] ^ xt[t])
                mins = members[np.flatnonzero(sc == sc.min())]
                ok_si += int(mins[rng.integers(0, mins.size)]) == M[t]
                ok_ct += int(members[rng.integers(0, members.size)]) == M[t]
                inv_mem += 1.0 / members.size
            row["rb"].append(float(rb))
            row["err_si"].append(1.0 - ok_si / T)
            row["err_ctrl"].append(1.0 - ok_ct / T)
            row.setdefault("chance_err", []).append(1.0 - inv_mem / T)
        # measured threshold: smallest rb with err <= 0.25 (inf -> Rc cap)
        ok_idx = [i for i, e in enumerate(row["err_si"]) if e <= 0.25]
        row["thr_meas"] = float(rbs[ok_idx[0]]) if ok_idx else float("nan")
        rows.append(row)
        print(f"  age={age:3d} q_t={qt:.3f} thr_pred={thr_pred:.3f} "
              f"thr_meas={row['thr_meas']:.3f}  "
              f"err={['%.2f' % e for e in row['err_si']]}", flush=True)

    thr_m = [r["thr_meas"] for r in rows]
    thr_p = [r["thr_pred"] for r in rows]
    mid = [r for r in rows if r["age"] in (0, 1, 2, 4, 8, 16)]
    err_fixed_rb = [r["err_si"][rbs.index(0.175)] for r in rows]
    verdict = dict(
        S1_threshold_monotone=bool(all(thr_m[i + 1] >= thr_m[i] - 1e-9
                                       for i in range(len(thr_m) - 1))),
        S2_tracks_prediction=bool(all(abs(r["thr_meas"] - r["thr_pred"]) <= 0.11
                                      for r in mid)),
        S3_same_binrate_flips_with_age=bool(err_fixed_rb[0] <= 0.10
                                            and min(err_fixed_rb[-2:]) >= 0.90),
        S4_channel_realized=bool(0.10 <= d_hat <= 0.17),
        # chance-relative: uniform in-bin picking succeeds at 1/|bin|, so the
        # control is gated against its own chance level (pilot lesson: at high
        # r_b bins hold 2-8 members and a flat 0.90 bar misreads chance as
        # side-information)
        S5_no_si_control=bool(all(e >= ch - 0.05
                                  for r in rows
                                  for e, ch in zip(r["err_ctrl"], r["chance_err"]))),
    )
    result = dict(
        claim="staleness-work complement, operational (aged Markov side information)",
        prereg="GO-P-2026-048",
        mode="pilot" if args.pilot else "full",
        seed=SEED, n=n, trials=T, p_flip=P_FLIP, d_hat=d_hat, Rc=Rc,
        rb_grid=rbs, ages=ages, rows=rows,
        thr_measured=thr_m, thr_predicted=thr_p,
        verdict=verdict,
        GOLST_staleness_supported=bool(all(verdict.values())),
        seconds_total=round(time.time() - t0, 1),
    )
    print(f"\nthr measured vs predicted by age: "
          f"{[(a, round(m, 3), round(p, 3)) for a, m, p in zip(ages, thr_m, thr_p)]}")
    print(f"verdict: {verdict}")
    print(f"GOLST_staleness_supported: {result['GOLST_staleness_supported']}")
    print("===GOLST-JSON===")
    print(json.dumps(result, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
