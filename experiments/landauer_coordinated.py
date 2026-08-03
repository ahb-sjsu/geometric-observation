# Operational coordinated-reset demonstration (GO-P-2026-050): the paper's
# several-consumers corollary -- coordinated reset saves the conditional
# total correlation -- made operational.  Source X = (A,B,C) i.i.d. fair
# bits; reset side information S = A; two records: M1 = codebook index
# describing U1 = (A,B), M2 = codebook index describing U2 = (B,C), both at
# per-component Hamming target d = 0.05.  Each record is random-binned and
# recovered in-bin by ML under four regimes:
#   independent reset:  from (bin, a^n) only
#   coordinated reset:  from (bin, a^n, the OTHER record's reconstruction)
#   shuffled null:      coordinated, but with the other record from a
#                       cyclically mismatched trial (must save nothing)
#   uniform control:    no information (chance; pooled 4-sigma gate)
# Predictions from the measured channel: the coordination discount for both
# records is the empirical shared-component information gap_TC = 1 - h2(d^*d^)
# (binary convolution), the operational face of TC(U1;U2|S) = I(B;B) = 1 bit
# in the exact-consumer limit d -> 0.  M2 is S-opaque (U2 independent of A),
# so its independent threshold sits at the full description rate; M1's
# independent threshold already carries the S discount 1 - h2(d^).
#
# Usage: python experiments/landauer_coordinated.py [--pilot]
# Output: sentinel JSON ===GOLCR-JSON===.  Tier B (Atlas CPU).  MIT.
import argparse
import json
import sys
import time

import numpy as np

SEED = 20260809
D_TGT = 0.05
R_AN = 2.0 * (1.0 - (-D_TGT * np.log2(D_TGT)
                     - (1 - D_TGT) * np.log2(1 - D_TGT)))
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


def encode(cwX, cwY, xX, xY, rng):
    """min-Hamming over both packed components; returns (index, err bits)."""
    sc = pop64(cwX ^ xX) + pop64(cwY ^ xY)
    mins = np.flatnonzero(sc == sc.min())
    m = int(mins[rng.integers(0, mins.size)])
    return m, int(sc[m])


def thr_of(errs, rbs, bar=0.25):
    ok = [i for i, e in enumerate(errs) if e <= bar]
    return float(rbs[ok[0]]) if ok else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    args = ap.parse_args()
    rng = np.random.default_rng(SEED + (1 if args.pilot else 0))
    if args.pilot:
        n, T = 14, 60
    else:
        n, T = 16, 150
    rbs = [0.35, 0.50, 0.65, 0.80, 0.95, 1.10, 1.25, 1.40, 1.55, 1.70]
    nbits = int(np.ceil(n * (R_AN + RC_EXCESS)))
    Ncw = 1 << nbits
    Rc = nbits / n
    print(f"coordinated-reset operational run ({'PILOT' if args.pilot else 'FULL'})"
          f"  seed={SEED}  n={n} T={T}")
    print(f"d_tgt={D_TGT}  R={R_AN:.4f}  Rc={Rc:.4f}  codebooks=2^{nbits} x2")
    t0 = time.time()

    # source bits and the two codebooks (packed per component)
    A = rng.integers(0, 1 << n, size=T, dtype=np.uint64)
    B = rng.integers(0, 1 << n, size=T, dtype=np.uint64)
    C = rng.integers(0, 1 << n, size=T, dtype=np.uint64)
    cw1A = rng.integers(0, 1 << n, size=Ncw, dtype=np.uint64)
    cw1B = rng.integers(0, 1 << n, size=Ncw, dtype=np.uint64)
    cw2B = rng.integers(0, 1 << n, size=Ncw, dtype=np.uint64)
    cw2C = rng.integers(0, 1 << n, size=Ncw, dtype=np.uint64)
    M1 = np.empty(T, dtype=np.int64)
    M2 = np.empty(T, dtype=np.int64)
    ebits = 0
    for t in range(T):
        M1[t], e1 = encode(cw1A, cw1B, A[t], B[t], rng)
        M2[t], e2 = encode(cw2B, cw2C, B[t], C[t], rng)
        ebits += e1 + e2
    d_hat = ebits / (4 * n * T)                       # per component-symbol
    dd = conv(d_hat, d_hat)
    gap_tc = 1.0 - h2(dd)                             # predicted coordination discount
    wA = np.log((1 - d_hat) / d_hat)
    wB = np.log((1 - dd) / dd)
    print(f"  encoded: d^={d_hat:.4f}  d^*d^={dd:.4f}  gap_TC={gap_tc:.4f}",
          flush=True)

    shift = 7                                          # shuffled-null pairing
    regimes = {}
    for name in ("m1_indep", "m1_coord", "m1_shuf",
                 "m2_indep", "m2_coord", "m2_shuf"):
        regimes[name] = dict(err=[], ctrl=[], chance=[])
    for rb in rbs:
        bbits = max(1, int(np.ceil(n * rb)))
        nbins = 1 << bbits
        acc = {k: 0 for k in regimes}
        okct = 0
        inv_mem = 0.0
        for t in range(T):
            ts = (t + shift) % T
            # --- record 1
            b1 = int(M1[t]) % nbins
            mem = np.arange(b1, Ncw, nbins, dtype=np.int64)
            inv_mem += 1.0 / mem.size
            sc = wA * pop64(cw1A[mem] ^ A[t])          # independent: S = A only
            pick = mem[np.flatnonzero(sc == sc.min())]
            acc["m1_indep"] += int(pick[rng.integers(0, pick.size)]) == M1[t]
            b2hat = cw2B[M2[t]]                        # coordinated: + record 2
            sc = wA * pop64(cw1A[mem] ^ A[t]) + wB * pop64(cw1B[mem] ^ b2hat)
            pick = mem[np.flatnonzero(sc == sc.min())]
            acc["m1_coord"] += int(pick[rng.integers(0, pick.size)]) == M1[t]
            b2s = cw2B[M2[ts]]                         # shuffled null
            sc = wA * pop64(cw1A[mem] ^ A[t]) + wB * pop64(cw1B[mem] ^ b2s)
            pick = mem[np.flatnonzero(sc == sc.min())]
            acc["m1_shuf"] += int(pick[rng.integers(0, pick.size)]) == M1[t]
            okct += int(mem[rng.integers(0, mem.size)]) == M1[t]
            # --- record 2 (S-opaque: independent = uniform pick, stated)
            b2 = int(M2[t]) % nbins
            mem = np.arange(b2, Ncw, nbins, dtype=np.int64)
            acc["m2_indep"] += int(mem[rng.integers(0, mem.size)]) == M2[t]
            b1hat = cw1B[M1[t]]
            sc = pop64(cw2B[mem] ^ b1hat)
            pick = mem[np.flatnonzero(sc == sc.min())]
            acc["m2_coord"] += int(pick[rng.integers(0, pick.size)]) == M2[t]
            b1s = cw1B[M1[ts]]
            sc = pop64(cw2B[mem] ^ b1s)
            pick = mem[np.flatnonzero(sc == sc.min())]
            acc["m2_shuf"] += int(pick[rng.integers(0, pick.size)]) == M2[t]
        for k in regimes:
            regimes[k]["err"].append(1.0 - acc[k] / T)
        regimes["m1_indep"]["ctrl"].append(1.0 - okct / T)
        regimes["m1_indep"]["chance"].append(1.0 - inv_mem / T)
        print(f"  rb={rb:.2f}  " + "  ".join(
            f"{k}={1.0 - acc[k] / T:.2f}" for k in regimes), flush=True)

    thr = {k: thr_of(regimes[k]["err"], rbs) for k in regimes}
    pred = dict(
        m1_indep=Rc - (1.0 - h2(d_hat)),
        m1_coord=Rc - (1.0 - h2(d_hat)) - gap_tc,
        m2_indep=Rc,
        m2_coord=Rc - gap_tc,
    )
    ctrl = regimes["m1_indep"]["ctrl"]
    chance = regimes["m1_indep"]["chance"]
    se = [np.sqrt(max(c * (1 - c), 1e-12) / T) for c in chance]
    verdict = dict(
        C1_s_discount_m1=bool(abs(thr["m1_indep"] - pred["m1_indep"]) <= 0.20),
        C2_coordination_m1=bool(
            thr["m1_indep"] - thr["m1_coord"] >= gap_tc - 0.20),
        C3_coordination_m2=bool(
            thr["m2_indep"] - thr["m2_coord"] >= gap_tc - 0.20),
        # one-sided: mismatched coordination must provide no BENEFIT; it may
        # legitimately be worse than independent, because a decoder that
        # weights garbage evidence degrades ML relative to ignoring it
        # (pilot lesson: m1_shuf landed 0.3 ABOVE independent)
        C4_shuffled_null=bool(
            thr["m1_shuf"] >= thr["m1_indep"] - 0.16
            and thr["m2_shuf"] >= thr["m2_indep"] - 0.16),
        C5_channel_realized=bool(0.03 <= d_hat <= 0.12),
        C6_uniform_control=bool(all(
            abs(e - c) <= 4.0 * s + 1e-9
            for e, c, s in zip(ctrl, chance, se))),
    )
    result = dict(
        claim="coordinated reset saves the conditional total correlation, operational",
        prereg="GO-P-2026-050",
        mode="pilot" if args.pilot else "full",
        seed=SEED, n=n, trials=T, d_hat=d_hat, Rc=Rc, gap_tc_pred=gap_tc,
        rb_grid=rbs,
        thresholds=thr, thresholds_pred=pred,
        regimes={k: v["err"] for k, v in regimes.items()},
        ctrl_err=ctrl, chance_err=chance,
        verdict=verdict,
        GOLCR_coordination_supported=bool(all(verdict.values())),
        seconds_total=round(time.time() - t0, 1),
    )
    print(f"\nthresholds measured: { {k: round(v, 3) for k, v in thr.items()} }")
    print(f"thresholds predicted: { {k: round(v, 3) for k, v in pred.items()} }")
    print(f"gap_TC predicted: {gap_tc:.3f}  "
          f"measured m1: {thr['m1_indep'] - thr['m1_coord']:.3f}  "
          f"m2: {thr['m2_indep'] - thr['m2_coord']:.3f}")
    print(f"verdict: {verdict}")
    print(f"GOLCR_coordination_supported: {result['GOLCR_coordination_supported']}")
    print("===GOLCR-JSON===")
    print(json.dumps(result, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
