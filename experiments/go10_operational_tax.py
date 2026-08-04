# GO-10 operational face (GO-P-2026-058): the complementarity tax as decode
# thresholds on materialized codebook records.
#
# Two consumers read one 2-D Gaussian source through orthogonal rank-one
# functionals (the registered worked instance of paper/complementarity-tax.tex
# Sec. 5, theta = 90 deg).  Each consumer's record is a real random-codebook
# quantization (GO-7/8/9 lineage); the JOINT record is the pair (M_A, M_B).
# Reset side information S = X1 + tau*Z is aligned with consumer A and is
# available only to the eraser, never to the consumers.
#
# Instrument (053/054 conventions, unchanged): sweep a binning rate r_b; bin
# the record index; MAP-decode the index from (bin, context) over the bin's
# strided member view; the decodable reset threshold thr = the r_b where the
# error curve crosses 0.25 (thr_interp).  The JOINT record is binned by a
# coordinated split (k_A, k_B), k_A + k_B = total bin bits, decoded
# per-component; the instrument takes the error-minimizing split per r_b in
# every context alike (the eraser allocates its budget -- the operational
# form of the note's per-coordinate reduction).
#
# Measured tax quantities (bits/symbol):
#   CT_R_op = thr_AB|none - max(thr_A|none, thr_B|none)
#   CT_W_op = thr_AB|S    - max(thr_A|S,    thr_B|S)
#   GAP_op  = CT_R_op - CT_W_op
# Prediction (note Sec. 5, with the realized channel d^):
#   GAP_pred(s^2) = 1/2 log2( 1 / (s^2 + (1 - s^2) d^) ),
# monotone in the quality of S; zero for a shuffled context S'.
#
# Usage: python go10_operational_tax.py [--pilot]
#   pilot seed 20260818 (logged in-prereg) / governed seed 20260820.
# Output: sentinel JSON ===GO10OP-JSON===.  Tier B (CPU, pure numpy).  MIT.
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landauer_gaussian_v2_common import (exact_binom_ok,  # noqa: E402
                                         strided_argmin, thr_interp)

DT = 0.35                                   # per-component MSE target
R1 = 0.5 * np.log2(1.0 / DT)                # single-component R(D)
RC_EXCESS = 0.03
N_BLK, SHIFT = 12, 7
TRIALS_PILOT, TRIALS_GOV = 240, 400         # governed design enlarged
                                            # pre-commit (054 precedent);
                                            # means unchanged, noise ~ -23%
S2_LIST = (0.2, 0.5)                        # Var(X1|S) settings
RB_SINGLE = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05]
RB_JOINT = [0.85, 1.00, 1.15, 1.30, 1.45, 1.60, 1.75, 1.90, 2.05]


def encode(rng, cw, csq, X):
    """MAP (min-distance) encoding; returns index array and realized MSE."""
    T, n = X.shape
    M = np.empty(T, dtype=np.int64)
    se = 0.0
    for t in range(T):
        M[t] = int(np.argmin(csq - 2.0 * (cw @ X[t])))
        se += float(((X[t] - cw[M[t]]) ** 2).sum())
    return M, se / (T * n)


def context_scores(cw, csq, d_hat, tau2, Sctx):
    """-2 log posterior (up to consts) of each codeword given S^n:
    cw ~ N(0, 1-d^), S = cw + E + tau Z, E ~ N(0, d^).
    score_i = (1/(1-d^) + 1/(d^+tau2)) ||cw_i||^2 - 2/(d^+tau2) <S, cw_i>."""
    a = 1.0 / (1.0 - d_hat) + 1.0 / (d_hat + tau2)
    b = 1.0 / (d_hat + tau2)
    return a * csq - 2.0 * b * (cw @ Sctx)


def single_curve(rng, M, nbits, scores, n, rbs, T):
    """Error curves for one record.  scores: (T, Ncw) context scores or None
    (context-free reset: uniform member pick = the chance instrument)."""
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
            if scores is None:
                acc += (b + nbins * int(rng.integers(0, msz))) == M[t]
            else:
                acc += strided_argmin(scores[t][b::nbins], b, nbins, rng) == M[t]
            okct += (b + nbins * int(rng.integers(0, msz))) == M[t]
        errs.append(1.0 - acc / T)
        ctrl.append(1.0 - okct / T)
        chance.append(1.0 - inv / T)
    return errs, ctrl, chance


def joint_curve(rng, MA, MB, nbA, nbB, scA, scB, n, rbs, T):
    """Coordinated-split joint reset.  Per r_b: try every split
    (kA, kB), kA + kB = bbits; decode each component over its strided members
    (context scores or uniform); success = both indices recovered; take the
    error-minimizing split.  Returns errors, best splits, controls."""
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
                if scA is None:
                    mszA = ((1 << nbA) - bA + nbinA - 1) // nbinA
                    gA = (bA + nbinA * int(rng.integers(0, mszA))) == MA[t]
                else:
                    gA = strided_argmin(scA[t][bA::nbinA], bA, nbinA, rng) == MA[t]
                if scB is None:
                    mszB = ((1 << nbB) - bB + nbinB - 1) // nbinB
                    gB = (bB + nbinB * int(rng.integers(0, mszB))) == MB[t]
                else:
                    gB = strided_argmin(scB[t][bB::nbinB], bB, nbinB, rng) == MB[t]
                acc += gA and gB
            e = 1.0 - acc / T
            if e < best_err:
                best_err, best_kA = e, kA
        # uniform joint control at the best split
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
    SEED = 20260818 if a.pilot else 20260820
    rng = np.random.default_rng(SEED)
    n, T = N_BLK, (TRIALS_PILOT if a.pilot else TRIALS_GOV)
    nbits = int(np.ceil(n * (R1 + RC_EXCESS)))
    Rc = nbits / n
    print(f"GO-10 operational tax -- {'PILOT' if a.pilot else 'GOVERNED'} run")
    print(f"seed={SEED} n={n} T={T} D={DT} R1={R1:.4f} Rc={Rc:.4f} "
          f"codebooks=2^{nbits} x2  s2={S2_LIST}", flush=True)
    t0 = time.time()

    sd = np.sqrt(1.0 - DT)
    cwA = rng.normal(0.0, sd, size=(1 << nbits, n)).astype(np.float32)
    cwB = rng.normal(0.0, sd, size=(1 << nbits, n)).astype(np.float32)
    cAsq, cBsq = (cwA * cwA).sum(1), (cwB * cwB).sum(1)
    X1 = rng.normal(0, 1, size=(T, n)).astype(np.float32)
    X2 = rng.normal(0, 1, size=(T, n)).astype(np.float32)
    MA, dA = encode(rng, cwA, cAsq, X1)
    MB, dB = encode(rng, cwB, cBsq, X2)
    d_hat = 0.5 * (dA + dB)
    print(f"  encoded: d^A={dA:.4f} d^B={dB:.4f}  ({time.time()-t0:.0f}s)",
          flush=True)

    out = dict(seed=SEED, pilot=bool(a.pilot), n=n, trials=T, D_target=DT,
               Rc=Rc, nbits=nbits, d_hat_A=dA, d_hat_B=dB,
               rb_single=RB_SINGLE, rb_joint=RB_JOINT, contexts={})
    ctrl_cells = []          # (ctrl_err, chance_err) for the exact-binomial gate

    def register(name, errs, ctrl, chance, rbs, splits=None):
        thr = thr_interp(errs, rbs)
        out["contexts"][name] = dict(errs=errs, thr=thr,
                                     **({"splits": splits} if splits else {}))
        ctrl_cells.extend(zip(ctrl, chance))
        return thr

    # ---------------- single records, context-free (the rate-side contents)
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

    per_s2 = {}
    for s2 in S2_LIST:
        tau2 = s2 / (1.0 - s2)
        Z = rng.normal(0, 1, size=(T, n)).astype(np.float32)
        S = X1 + np.sqrt(tau2) * Z
        scA = np.stack([context_scores(cwA, cAsq, dA, tau2, S[t])
                        for t in range(T)])
        scAsh = np.stack([context_scores(cwA, cAsq, dA, tau2,
                                         S[(t + SHIFT) % T])
                          for t in range(T)])
        # S is independent of X2: B's conditional decode = context-free
        eAS, cAS, hAS = single_curve(rng, MA, nbits, scA, n, RB_SINGLE, T)
        thrAS = register(f"A|S(s2={s2})", eAS, cAS, hAS, RB_SINGLE)
        eBS, cBS, hBS = single_curve(rng, MB, nbits, None, n, RB_SINGLE, T)
        thrBS = register(f"B|S(s2={s2})", eBS, cBS, hBS, RB_SINGLE)
        eJS, sJS, cJS, hJS = joint_curve(rng, MA, MB, nbits, nbits, scA, None,
                                         n, RB_JOINT, T)
        thrJS = register(f"AB|S(s2={s2})", eJS, cJS, hJS, RB_JOINT, sJS)
        # shuffled context S'
        eASh, cASh, hASh = single_curve(rng, MA, nbits, scAsh, n, RB_SINGLE, T)
        thrASh = register(f"A|S'(s2={s2})", eASh, cASh, hASh, RB_SINGLE)
        eJSh, sJSh, cJSh, hJSh = joint_curve(rng, MA, MB, nbits, nbits, scAsh,
                                             None, n, RB_JOINT, T)
        thrJSh = register(f"AB|S'(s2={s2})", eJSh, cJSh, hJSh, RB_JOINT, sJSh)

        d_eff = dA
        disc_pred = 0.5 * np.log2(1.0 / (s2 + (1.0 - s2) * d_eff))
        CT_W = thrJS - max(thrAS, thrBS)
        gap = CT_R - CT_W
        CT_W_sh = thrJSh - max(thrASh, thrBS)
        per_s2[s2] = dict(
            thr_A_S=thrAS, thr_B_S=thrBS, thr_AB_S=thrJS,
            thr_A_shuf=thrASh, thr_AB_shuf=thrJSh,
            discount_A=thrA0 - thrAS, discount_A_pred=float(disc_pred),
            opacity_B=abs(thrB0 - thrBS),
            CT_W=CT_W, gap=gap, gap_pred=float(disc_pred),
            gap_shuf=CT_R - CT_W_sh,
            discount_A_shuf=thrA0 - thrASh,
            splits_S=sJS)
        print(f"  [s2={s2}] thrA|S={thrAS:.3f} (disc {thrA0-thrAS:.3f} "
              f"pred {disc_pred:.3f})  thrB|S={thrBS:.3f}  thrAB|S={thrJS:.3f}"
              f"  CT_W={CT_W:.3f}  GAP={gap:.3f} (pred {disc_pred:.3f})"
              f"  GAP_shuf={CT_R - CT_W_sh:.3f}  ({time.time()-t0:.0f}s)",
              flush=True)

    out.update(CT_R=CT_R, per_s2={str(k): v for k, v in per_s2.items()})

    # ---------------- gates (bars sealed in prereg GO-P-2026-058)
    # W4's shape follows GO-9's C2 pattern (fraction-of-asymptotic window),
    # NOT absolute tracking of the asymptotic value: the finite-n instrument
    # realizes ~0.44-0.54x of the asymptotic gap (pilot, seed 20260818;
    # cf. GO-9's 0.56x realized fraction).  Bars set from the pilot with
    # >= 1.3x margins per the power-first rule (GO-KV-SERVING-POWER-NOTE).
    g = per_s2
    verdict = dict(
        W1_channel_window=bool(0.28 <= dA <= 0.48 and 0.28 <= dB <= 0.48),
        W2_discount_tracks=bool(all(
            abs(g[s]["discount_A"] - g[s]["discount_A_pred"]) <= 0.22
            for s in S2_LIST)),
        W3_opacity=bool(all(g[s]["opacity_B"] <= 0.12 for s in S2_LIST)),
        W4_tax_gap=bool(
            0.40 * g[0.2]["gap_pred"] <= g[0.2]["gap"]
            <= g[0.2]["gap_pred"] + 0.15
            and g[0.5]["gap"] >= 0.30 * g[0.5]["gap_pred"]
            and (g[0.2]["gap"] - g[0.5]["gap"]) >= 0.08),
        W5_shuffled_null=bool(all(
            abs(g[s]["gap_shuf"]) <= 0.15
            and g[s]["discount_A_shuf"] <= 0.15 for s in S2_LIST)),
        W6_uniform_control_exact=bool(all(
            exact_binom_ok(c, h, T) for c, h in ctrl_cells)),
    )
    out["verdict"] = verdict
    out["GO10OP_supported"] = bool(all(verdict.values()))
    out["seconds_total"] = round(time.time() - t0, 1)
    print(f"\nCT_R={CT_R:.3f}; gaps: "
          + "  ".join(f"s2={s}: {g[s]['gap']:.3f}/(pred {g[s]['gap_pred']:.3f})"
                      for s in S2_LIST))
    print(f"verdict: {verdict}")
    print(f"GO10OP_supported: {out['GO10OP_supported']}")
    print("===GO10OP-JSON===")
    print(json.dumps(out, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
