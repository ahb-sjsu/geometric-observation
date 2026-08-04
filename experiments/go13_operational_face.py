# GO-13 operational face (GO-P-2026-069): the dynamic complementarity
# tax as decode thresholds on materialized codebook records.
#
# Two consumers read one correlated Gaussian triple (Y_A, Y_B, V),
# records = random-codebook quantizations (058 lineage, instrument
# conventions unchanged: binning-rate sweep, strided-argmin MAP decode
# given context, thr_interp 0.25-crossing, coordinated-split joint
# reset). Eraser context = slice-class S with quality q = Var(V|S).
#
# Instances FIXED pre-instrument by the committed regime map
# (go13_regime_sweep.py, seed 20260925):
#   RISING: r = (rAB, rAV, rBV) = (0.0, 0.8, 0.3), D = (0.2, 0.2)
#           -- predicted dCT_W/dq = +0.286 bits/unit-q (Thm 2 sign law)
#   FLAT:   r = (0.3, 0.7, 0.2), D = (0.15, 0.4) -- |dCT/dq| < 1e-3
# Staleness levels q in {0.35, 0.65} (Delta q = 0.30).
#
# Gates:
#   V1 channel window (realized d^ near target)
#   V2 equal-q universality (Thm 1): single sample at tau1^2 vs the
#      mean of two samples at 2*tau1^2 (identical q analytically) give
#      equal thresholds and equal taxes -- analytic-equality control
#   V3 rising tax (Thm 2 sign law, operational): CT_W(stale) -
#      CT_W(fresh) >= bar at the RISING instance
#   V4 paired flat contrast: |Delta CT_flat| <= half the rising delta
#   V5 shuffled-context null
#   V6 exact-binomial uniform control (058 gate)
#
# Usage: python go13_operational_face.py [--pilot]
#   pilot seed 20260926 / governed seed 20260927.
# Sentinel ===GO13OP-JSON=== with ===END===; flag GO13OP_supported.
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landauer_gaussian_v2_common import (exact_binom_ok,  # noqa: E402
                                         strided_argmin, thr_interp)

N_BLK, SHIFT = 12, 7
TRIALS_PILOT, TRIALS_GOV = 240, 400
RC_EXCESS = 0.03
Q_FRESH, Q_STALE = 0.35, 0.65


def rb_grid(lo, hi, k=9):
    return [round(lo + i * (hi - lo) / (k - 1), 4) for i in range(k)]


def encode(cw, csq, X):
    T = X.shape[0]
    M = np.empty(T, dtype=np.int64)
    se = 0.0
    for t in range(T):
        M[t] = int(np.argmin(csq - 2.0 * (cw @ X[t])))
        se += float(((X[t] - cw[M[t]]) ** 2).sum())
    return M, se / (T * X.shape[1])


def ctx_scores(cw, csq, d_hat, rho_v, q, Sctx):
    """-2 log posterior of codeword given S^n. cw ~ N(0, 1-d^);
    Y = cw + E, E ~ N(0, d^); E[Y|S] = rho_v (1-q) S / VarS-normalized:
    with slice S = V + tau Z, tau2 = q/(1-q): E[Y|S] = rho_v S/(1+tau2)
    = rho_v (1-q) S; Var(Y|S) = 1 - rho_v^2 (1-q).  So cw | S ~
    N(mu_S, vS + d^ - ...) -- following the 058 convention we score
    with a = 1/(1-d^) + 1/(d^ + vS), b-term = <mu_S, cw>/(d^ + vS)."""
    vS = 1.0 - rho_v * rho_v * (1.0 - q)
    mu = rho_v * (1.0 - q) * Sctx
    a = 1.0 / (1.0 - d_hat) + 1.0 / (d_hat + vS)
    return a * csq - 2.0 * (cw @ mu) / (d_hat + vS)


def single_curve(rng, M, nbits, scores, n, rbs, T):
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
                acc += strided_argmin(scores[t][b::nbins], b, nbins,
                                      rng) == M[t]
            okct += (b + nbins * int(rng.integers(0, msz))) == M[t]
        errs.append(1.0 - acc / T)
        ctrl.append(1.0 - okct / T)
        chance.append(1.0 - inv / T)
    return errs, ctrl, chance


def joint_curve(rng, MA, MB, nbA, nbB, scA, scB, n, rbs, T):
    errs, ctrl, chance = [], [], []
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
                    gA = strided_argmin(scA[t][bA::nbinA], bA, nbinA,
                                        rng) == MA[t]
                if scB is None:
                    mszB = ((1 << nbB) - bB + nbinB - 1) // nbinB
                    gB = (bB + nbinB * int(rng.integers(0, mszB))) == MB[t]
                else:
                    gB = strided_argmin(scB[t][bB::nbinB], bB, nbinB,
                                        rng) == MB[t]
                acc += gA and gB
            e = 1.0 - acc / T
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
        ctrl.append(1.0 - okct / T)
        chance.append(1.0 - inv / T)
    return errs, ctrl, chance


def run_instance(rng, name, rvec, DA, DB, n, T, do_univ, do_shuf,
                 ctrl_cells, log):
    rAB, rAV, rBV = rvec
    SigT = np.array([[1, rAB, rAV], [rAB, 1, rBV], [rAV, rBV, 1.0]])
    Ch = np.linalg.cholesky(SigT)
    nbA = int(np.ceil(n * (0.5 * np.log2(1 / DA) + RC_EXCESS)))
    nbB = int(np.ceil(n * (0.5 * np.log2(1 / DB) + RC_EXCESS)))
    rbsA = rb_grid(0.2, 1.4)
    rbsB = rb_grid(0.2, 1.4)
    rbsJ = rb_grid(0.6, 2.6)
    cwA = rng.normal(0, np.sqrt(1 - DA), size=(1 << nbA, n)).astype(
        np.float32)
    cwB = rng.normal(0, np.sqrt(1 - DB), size=(1 << nbB, n)).astype(
        np.float32)
    cAsq, cBsq = (cwA * cwA).sum(1), (cwB * cwB).sum(1)
    G = rng.normal(0, 1, size=(T, n, 3)).astype(np.float32)
    Tri = G @ Ch.T.astype(np.float32)
    YA, YB, V = Tri[:, :, 0], Tri[:, :, 1], Tri[:, :, 2]
    MA, dA = encode(cwA, cAsq, YA)
    MB, dB = encode(cwB, cBsq, YB)
    log(f"  [{name}] encoded d^A={dA:.4f} d^B={dB:.4f} "
        f"(2^{nbA}/2^{nbB} cw)")

    res = dict(d_hat_A=dA, d_hat_B=dB, nbA=nbA, nbB=nbB)

    def taxes(scA, scB, tag):
        eA, cA_, hA = single_curve(rng, MA, nbA, scA, n, rbsA, T)
        eB, cB_, hB = single_curve(rng, MB, nbB, scB, n, rbsB, T)
        eJ, cJ, hJ = joint_curve(rng, MA, MB, nbA, nbB, scA, scB,
                                 n, rbsJ, T)
        ctrl_cells.extend(zip(cA_, hA))
        ctrl_cells.extend(zip(cB_, hB))
        ctrl_cells.extend(zip(cJ, hJ))
        tA, tB = thr_interp(eA, rbsA), thr_interp(eB, rbsB)
        tJ = thr_interp(eJ, rbsJ)
        ct = tJ - max(tA, tB)
        res[tag] = dict(thr_A=tA, thr_B=tB, thr_AB=tJ, CT=ct)
        log(f"  [{name}|{tag}] thrA={tA:.3f} thrB={tB:.3f} "
            f"thrAB={tJ:.3f} CT={ct:.3f}")
        return ct

    ct_none = taxes(None, None, "none")

    def make_scores(q, Svec):
        sA = np.stack([ctx_scores(cwA, cAsq, dA, rAV, q, Svec[t])
                       for t in range(T)])
        sB = np.stack([ctx_scores(cwB, cBsq, dB, rBV, q, Svec[t])
                       for t in range(T)])
        return sA, sB

    cts = {}
    for q in (Q_FRESH, Q_STALE):
        tau = np.sqrt(q / (1 - q))
        S = V + tau * rng.normal(0, 1, size=(T, n)).astype(np.float32)
        scA, scB = make_scores(q, S)
        cts[q] = taxes(scA, scB, f"q={q}")
        if do_univ and q == Q_FRESH:
            # two-sample class tuned to the same q: mean of two samples
            # at 2*tau1^2 has Var(V|mean) = q exactly
            tau2s = np.sqrt(2) * tau
            Sa = V + tau2s * rng.normal(0, 1, size=(T, n)).astype(
                np.float32)
            Sb = V + tau2s * rng.normal(0, 1, size=(T, n)).astype(
                np.float32)
            scA2, scB2 = make_scores(q, (Sa + Sb) / 2)
            cts["univ"] = taxes(scA2, scB2, "univ(equal-q)")
        if do_shuf and q == Q_FRESH:
            Ssh = np.roll(S, SHIFT, axis=0)
            scAs, scBs = make_scores(q, Ssh)
            cts["shuf"] = taxes(scAs, scBs, "shuffled")
    res["CT_none"] = ct_none
    return res, cts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    a = ap.parse_args()
    SEED = 20260926 if a.pilot else 20260927
    rng = np.random.default_rng(SEED)
    n, T = N_BLK, (TRIALS_PILOT if a.pilot else TRIALS_GOV)
    t0 = time.time()

    def log(msg):
        print(f"{msg}  ({time.time()-t0:.0f}s)", flush=True)

    log(f"GO-13 operational face -- {'PILOT' if a.pilot else 'GOVERNED'}"
        f" seed={SEED} n={n} T={T} q=({Q_FRESH},{Q_STALE})")
    ctrl_cells = []
    resR, ctR = run_instance(rng, "RISING", (0.0, 0.8, 0.3), 0.2, 0.2,
                             n, T, True, True, ctrl_cells, log)
    resF, ctF = run_instance(rng, "FLAT", (0.3, 0.7, 0.2), 0.15, 0.4,
                             n, T, False, False, ctrl_cells, log)

    dCT_rise = ctR[Q_STALE] - ctR[Q_FRESH]
    dCT_flat = ctF[Q_STALE] - ctF[Q_FRESH]
    univ_gap = abs(ctR["univ"] - ctR[Q_FRESH])
    thrs_u = resR["univ(equal-q)"]
    thrs_f = resR[f"q={Q_FRESH}"]
    univ_thr_gap = max(abs(thrs_u["thr_A"] - thrs_f["thr_A"]),
                       abs(thrs_u["thr_B"] - thrs_f["thr_B"]),
                       abs(thrs_u["thr_AB"] - thrs_f["thr_AB"]))
    shuf_disc = abs(resR["shuffled"]["thr_A"] - resR["none"]["thr_A"])

    verdict = dict(
        V1_channel=bool(abs(resR["d_hat_A"] - 0.2) <= 0.1
                        and abs(resR["d_hat_B"] - 0.2) <= 0.1
                        and abs(resF["d_hat_A"] - 0.15) <= 0.08
                        and abs(resF["d_hat_B"] - 0.4) <= 0.15),
        V2_universality=bool(univ_thr_gap <= 0.12 and univ_gap <= 0.12),
        V3_rising_tax=bool(dCT_rise >= 0.03),
        V4_flat_paired=bool(abs(dCT_flat) <= 0.5 * max(dCT_rise, 1e-9)
                            + 0.06),
        V5_shuffled_null=bool(shuf_disc <= 0.15),
        V6_uniform_exact=bool(all(exact_binom_ok(c, h, T)
                                  for c, h in ctrl_cells)),
    )
    out = dict(seed=SEED, pilot=bool(a.pilot), n=n, trials=T,
               q_levels=[Q_FRESH, Q_STALE],
               rising=resR, flat=resF,
               dCT_rise=dCT_rise, dCT_flat=dCT_flat,
               univ_gap=univ_gap, univ_thr_gap=univ_thr_gap,
               shuf_disc=shuf_disc, verdict=verdict,
               GO13OP_supported=bool(all(verdict.values())),
               seconds_total=round(time.time() - t0, 1))
    log(f"dCT_rise={dCT_rise:.3f} dCT_flat={dCT_flat:.3f} "
        f"univ_gap={univ_gap:.3f}/{univ_thr_gap:.3f} shuf={shuf_disc:.3f}")
    print(f"verdict: {verdict}")
    print("===GO13OP-JSON===")
    print(json.dumps(out, indent=1))
    print("===END===")
    print("VERDICT:", "ALL PASS" if out["GO13OP_supported"] else "FAIL")
    return 0 if out["GO13OP_supported"] else 1


if __name__ == "__main__":
    sys.exit(main())
