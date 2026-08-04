# GO-10 operational face, SECOND SOURCE FAMILY (binary): the complementarity
# tax as decode thresholds on materialized binary codebook records
# (GO-P-2026-059; first family = Gaussian, GO-P-2026-058 ALL PASS 6/6).
#
# Two consumers read one two-bit-per-symbol source: A reads the U bit, B reads
# the V bit (independent fair bits -- the binary analog of the Gaussian
# orthogonal instance).  Records are random binary codebooks at Hamming
# distortion d^ (GO-7 043/045 lineage).  Reset side information S = U xor W,
# W ~ Bern(q), is aligned with consumer A and available only to the eraser.
#
# Binary floor, derived (prereg carries the derivation; the mechanism is the
# one GO-8 verified operationally): the BSC cascade Uhat -(d^)- U -(q)- S has
# crossover d^*q = d^(1-q) + q(1-d^), so the per-symbol side information about
# A's record is I(Uhat;S) = 1 - h2(d^*q), and
#   thr_A|S ~ Rc - (1 - h2(d^*q)),   thr_B|any ~ Rc,
#   GAP_pred(q) = CT_R - CT_W = 1 - h2(d^*q)  -> 1 bit as d^, q -> 0.
#
# Instrument identical in shape to GO-P-2026-058: bin the record index, MAP
# decode from (bin, context) over the strided member view (binary MAP = min
# Hamming distance to S, ties broken uniformly -- integer scores tie often,
# which is exactly what strided_argmin's uniform tie-break is for); joint
# record (M_A, M_B) reset by coordinated-split binning, error-minimizing split
# per r_b in every context alike; thr = 0.25-crossing of the error curve.
#
# Usage: python go10_operational_tax_binary.py [--pilot]
#   pilot seed 20260821 (logged in-prereg) / governed seed 20260822.
# Output: sentinel JSON ===GO10OPB-JSON===.  Tier B (CPU, pure numpy).  MIT.
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landauer_gaussian_v2_common import (exact_binom_ok,  # noqa: E402
                                         strided_argmin, thr_interp)


def h2(p):
    p = min(max(float(p), 1e-12), 1 - 1e-12)
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)


DT = 0.11                                    # Hamming distortion target
R1 = 1.0 - h2(DT)                            # binary R(d)
RC_EXCESS = 0.04                             # coverage excess for random codes
N_BLK, SHIFT = 24, 7
TRIALS_PILOT, TRIALS_GOV = 240, 400
Q_LIST = (0.1, 0.25)                         # S-channel crossover settings
RB_SINGLE = [0.10, 0.175, 0.25, 0.325, 0.40, 0.475, 0.55, 0.625]
RB_JOINT = [0.55, 0.65, 0.75, 0.85, 0.95, 1.05, 1.15, 1.25]


def encode(cw, X):
    """Min-Hamming-distance encoding; index array + realized distortion."""
    T, n = X.shape
    M = np.empty(T, dtype=np.int64)
    err = 0
    for t in range(T):
        dist = (cw ^ X[t]).sum(1)
        mn = int(dist.min())
        locs = np.flatnonzero(dist == mn)
        M[t] = int(locs[0])                   # deterministic first-min encode
        err += mn
    return M, err / (T * n)


def single_curve(rng, M, nbits, dists, n, rbs, T):
    """Error curves for one record.  dists: (T, Ncw) Hamming-to-context
    scores, or None (context-free: uniform member pick = chance)."""
    errs, ctrl, chance = [], [], []
    for rb in rbs:
        bbits = min(nbits, max(1, int(np.ceil(n * rb))))
        nbins = 1 << bbits
        acc = okct = 0
        inv = 0.0
        for t in range(T):
            b = int(M[t]) % nbins
            msz = ((1 << nbits) - b + nbins - 1) // nbins
            inv += 1.0 / msz
            if dists is None:
                acc += (b + nbins * int(rng.integers(0, msz))) == M[t]
            else:
                acc += strided_argmin(dists[t][b::nbins], b, nbins, rng) == M[t]
            okct += (b + nbins * int(rng.integers(0, msz))) == M[t]
        errs.append(1.0 - acc / T)
        ctrl.append(1.0 - okct / T)
        chance.append(1.0 - inv / T)
    return errs, ctrl, chance


def joint_curve(rng, MA, MB, nbA, nbB, dA, dB, n, rbs, T):
    """Coordinated-split joint reset (058 semantics verbatim)."""
    errs, splits, ctrl, chance = [], [], [], []
    for rb in rbs:
        bbits = min(nbA + nbB, max(1, int(np.ceil(n * rb))))
        best_err, best_kA = 1.0, None
        for kA in range(max(0, bbits - nbB), min(nbA, bbits) + 1):
            kB = bbits - kA
            nbinA, nbinB = 1 << kA, 1 << kB
            acc = 0
            for t in range(T):
                bA, bB = int(MA[t]) % nbinA, int(MB[t]) % nbinB
                if dA is None:
                    mszA = ((1 << nbA) - bA + nbinA - 1) // nbinA
                    gA = (bA + nbinA * int(rng.integers(0, mszA))) == MA[t]
                else:
                    gA = strided_argmin(dA[t][bA::nbinA], bA, nbinA, rng) == MA[t]
                if dB is None:
                    mszB = ((1 << nbB) - bB + nbinB - 1) // nbinB
                    gB = (bB + nbinB * int(rng.integers(0, mszB))) == MB[t]
                else:
                    gB = strided_argmin(dB[t][bB::nbinB], bB, nbinB, rng) == MB[t]
                acc += gA and gB
            e = 1.0 - acc / T
            # NOTE: `is None or` guards the all-splits-at-error-1.0 case
            # (binary chance decode can be exactly 1.0 across every split at
            # low r_b), which left best_kA unset in the 058 harness's version
            # of this loop -- latent there (continuous scores always decoded
            # something), fatal here.  First split wins ties, as in 058.
            if best_kA is None or e < best_err:
                best_err, best_kA = e, kA
        kA = best_kA
        kB = bbits - kA
        nbinA, nbinB = 1 << kA, 1 << kB
        okct = 0
        inv = 0.0
        for t in range(T):
            bA, bB = int(MA[t]) % nbinA, int(MB[t]) % nbinB
            mszA = ((1 << nbA) - bA + nbinA - 1) // nbinA
            mszB = ((1 << nbB) - bB + nbinB - 1) // nbinB
            inv += 1.0 / (mszA * mszB)
            okct += ((bA + nbinA * int(rng.integers(0, mszA))) == MA[t]
                     and (bB + nbinB * int(rng.integers(0, mszB))) == MB[t])
        errs.append(best_err)
        splits.append(int(best_kA))
        ctrl.append(1.0 - okct / T)
        chance.append(1.0 - inv / T)
    return errs, splits, ctrl, chance


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    a = ap.parse_args()
    SEED = 20260821 if a.pilot else 20260822
    rng = np.random.default_rng(SEED)
    n, T = N_BLK, (TRIALS_PILOT if a.pilot else TRIALS_GOV)
    nbits = int(np.ceil(n * (R1 + RC_EXCESS)))
    Rc = nbits / n
    print(f"GO-10 operational tax, BINARY family -- "
          f"{'PILOT' if a.pilot else 'GOVERNED'} run")
    print(f"seed={SEED} n={n} T={T} d_target={DT} R1={R1:.4f} Rc={Rc:.4f} "
          f"codebooks=2^{nbits} x2  q={Q_LIST}", flush=True)
    t0 = time.time()

    cwA = (rng.integers(0, 2, size=(1 << nbits, n))).astype(np.uint8)
    cwB = (rng.integers(0, 2, size=(1 << nbits, n))).astype(np.uint8)
    U = rng.integers(0, 2, size=(T, n)).astype(np.uint8)
    V = rng.integers(0, 2, size=(T, n)).astype(np.uint8)
    MA, dA_hat = encode(cwA, U)
    MB, dB_hat = encode(cwB, V)
    print(f"  encoded: d^A={dA_hat:.4f} d^B={dB_hat:.4f}  "
          f"({time.time()-t0:.0f}s)", flush=True)

    out = dict(seed=SEED, pilot=bool(a.pilot), n=n, trials=T, d_target=DT,
               Rc=Rc, nbits=nbits, d_hat_A=dA_hat, d_hat_B=dB_hat,
               rb_single=RB_SINGLE, rb_joint=RB_JOINT, contexts={})
    ctrl_cells = []

    def register(name, errs, ctrl, chance, rbs, splits=None):
        thr = thr_interp(errs, rbs)
        out["contexts"][name] = dict(errs=errs, thr=thr,
                                     **({"splits": splits} if splits else {}))
        ctrl_cells.extend(zip(ctrl, chance))
        return thr

    eA, cA, hA = single_curve(rng, MA, nbits, None, n, RB_SINGLE, T)
    thrA0 = register("A|none", eA, cA, hA, RB_SINGLE)
    eB, cB, hB = single_curve(rng, MB, nbits, None, n, RB_SINGLE, T)
    thrB0 = register("B|none", eB, cB, hB, RB_SINGLE)
    eJ, sJ, cJ, hJ = joint_curve(rng, MA, MB, nbits, nbits, None, None,
                                 n, RB_JOINT, T)
    thrJ0 = register("AB|none", eJ, cJ, hJ, RB_JOINT, sJ)
    CT_R = thrJ0 - max(thrA0, thrB0)
    print(f"  [none] thrA={thrA0:.3f} thrB={thrB0:.3f} thrAB={thrJ0:.3f} "
          f"CT_R={CT_R:.3f}  ({time.time()-t0:.0f}s)", flush=True)

    per_q = {}
    for q in Q_LIST:
        W = (rng.random(size=(T, n)) < q).astype(np.uint8)
        S = U ^ W
        distA = np.stack([(cwA ^ S[t]).sum(1) for t in range(T)])
        distAsh = np.stack([(cwA ^ S[(t + SHIFT) % T]).sum(1)
                            for t in range(T)])
        eAS, cAS, hAS = single_curve(rng, MA, nbits, distA, n, RB_SINGLE, T)
        thrAS = register(f"A|S(q={q})", eAS, cAS, hAS, RB_SINGLE)
        eBS, cBS, hBS = single_curve(rng, MB, nbits, None, n, RB_SINGLE, T)
        thrBS = register(f"B|S(q={q})", eBS, cBS, hBS, RB_SINGLE)
        eJS, sJS, cJS, hJS = joint_curve(rng, MA, MB, nbits, nbits, distA,
                                         None, n, RB_JOINT, T)
        thrJS = register(f"AB|S(q={q})", eJS, cJS, hJS, RB_JOINT, sJS)
        eASh, cASh, hASh = single_curve(rng, MA, nbits, distAsh, n,
                                        RB_SINGLE, T)
        thrASh = register(f"A|S'(q={q})", eASh, cASh, hASh, RB_SINGLE)
        eJSh, sJSh, cJSh, hJSh = joint_curve(rng, MA, MB, nbits, nbits,
                                             distAsh, None, n, RB_JOINT, T)
        thrJSh = register(f"AB|S'(q={q})", eJSh, cJSh, hJSh, RB_JOINT, sJSh)

        dq = dA_hat * (1 - q) + q * (1 - dA_hat)
        disc_pred = 1.0 - h2(dq)
        CT_W = thrJS - max(thrAS, thrBS)
        gap = CT_R - CT_W
        CT_W_sh = thrJSh - max(thrASh, thrBS)
        per_q[q] = dict(
            thr_A_S=thrAS, thr_B_S=thrBS, thr_AB_S=thrJS,
            thr_A_shuf=thrASh, thr_AB_shuf=thrJSh,
            discount_A=thrA0 - thrAS, discount_A_pred=float(disc_pred),
            opacity_B=abs(thrB0 - thrBS),
            CT_W=CT_W, gap=gap, gap_pred=float(disc_pred),
            gap_shuf=CT_R - CT_W_sh,
            discount_A_shuf=thrA0 - thrASh,
            splits_S=sJS)
        print(f"  [q={q}] thrA|S={thrAS:.3f} (disc {thrA0-thrAS:.3f} "
              f"pred {disc_pred:.3f})  thrB|S={thrBS:.3f}  thrAB|S={thrJS:.3f}"
              f"  CT_W={CT_W:.3f}  GAP={gap:.3f} (pred {disc_pred:.3f})"
              f"  GAP_shuf={CT_R - CT_W_sh:.3f}  ({time.time()-t0:.0f}s)",
              flush=True)

    out.update(CT_R=CT_R, per_q={str(k): v for k, v in per_q.items()})

    # ---------------- gates (bars sealed in prereg GO-P-2026-059)
    g = per_q
    verdict = dict(
        B1_channel_window=bool(0.06 <= dA_hat <= 0.18
                               and 0.06 <= dB_hat <= 0.18),
        # B2 bar 0.12 (not the Gaussian face's 0.22): the binary instrument
        # tracked within 0.013 in the pilot, and 0.12 is the largest bar that
        # still fails a zero discount at q=0.1 (|0-0.270| > 0.12).
        B2_discount_tracks=bool(all(
            abs(g[q]["discount_A"] - g[q]["discount_A_pred"]) <= 0.12
            for q in Q_LIST)),
        B3_opacity=bool(all(g[q]["opacity_B"] <= 0.12 for q in Q_LIST)),
        # B4 secondary at 0.20x (not 0.30x): pilot measured 0.039 vs a 0.30x
        # bar of 0.030 -- a 1.29x margin, the 052 failure mode; 0.20x gives
        # 1.9x margin and still fails on a zero gap.
        B4_tax_gap=bool(
            0.40 * g[0.1]["gap_pred"] <= g[0.1]["gap"]
            <= g[0.1]["gap_pred"] + 0.15
            and g[0.25]["gap"] >= 0.20 * g[0.25]["gap_pred"]
            and (g[0.1]["gap"] - g[0.25]["gap"]) >= 0.06),
        B5_shuffled_null=bool(all(
            abs(g[q]["gap_shuf"]) <= 0.15
            and g[q]["discount_A_shuf"] <= 0.15 for q in Q_LIST)),
        B6_uniform_control_exact=bool(all(
            exact_binom_ok(c, h, T) for c, h in ctrl_cells)),
    )
    out["verdict"] = verdict
    out["GO10OPB_supported"] = bool(all(verdict.values()))
    out["seconds_total"] = round(time.time() - t0, 1)
    print(f"\nCT_R={CT_R:.3f}; gaps: "
          + "  ".join(f"q={q}: {g[q]['gap']:.3f}/(pred {g[q]['gap_pred']:.3f})"
                      for q in Q_LIST))
    print(f"verdict: {verdict}")
    print(f"GO10OPB_supported: {out['GO10OPB_supported']}")
    print("===GO10OPB-JSON===")
    print(json.dumps(out, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
