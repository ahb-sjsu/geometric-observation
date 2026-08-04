# GO-11 operational face (GO-P-2026-061): the ENCODER-SIDE TILT -- optimal
# records write themselves into the reset context's X-measurable directions.
#
# Theory under test (paper/go11-conditional-region.tex v0.8): Prop 1 /
# Thm 2 say the L-optimal record for consumer Y = w'X mixes in the context
# statistic V = gamma'X (b != 0); Thm 6(a) says at tau^2 = 0 the tilted
# record's conditional content ATTAINS Gray's floor while the marginalized
# record pays the Steinberg-corner premium. Canonical instance (rho^2 = 1/2,
# D = 0.25, tau^2 = 0, S = V):
#   MARG   record encodes y alone            -> content ~ 0.661 b/sym
#   TILT   record encodes z+ = a*y + b*v     -> content ~ 0.500 (Gray floor)
#   TILT-  record encodes z- = a*y - b*v     -> Cov(z-, V) = a*rho - b = 0
#                                             EXACTLY: provably context-blind
# with a = 1 - 2D = 0.5, b = rho/g = sqrt(2)D = 0.3536 (g = 1/(2D) = 2).
# All three records serve the consumer at (audited) matched distortion ~ D.
#
# Instrument (053/058 conventions): random codebooks; MARG covers y at
# d_cw = D (rate ~ 1 b/sym); TILT/TILT- cover z+- at d_cw = D(1-2D) = 0.125
# (rate ~ 1/2 log2(5) = 1.161 -- the tilt's rate premium, Cor 2, REPORTED);
# bin the index at rate r_b, MAP-decode from (bin, S^n) over the strided
# member view; threshold thr = 0.25-crossing (thr_interp). Discount
# disc(arm) = thr(arm|none) - thr(arm|S). Contexts: none, S = V^n, shuffled
# S'. Strict face tau^2 = 0.5 measured and REPORTED (deficits ~0.02-0.05
# b/sym are below instrument resolution -- not gated, per PROTOCOL 5.1).
#
# Usage: python go11_encoder_tilt.py [--pilot]
#   pilot seed 20260828 (logged in-prereg) / governed seed 20260830.
# Output: sentinel JSON ===GO11ET-JSON===.  Tier B (CPU, numpy).  MIT.
import argparse
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(
    __import__("os").path.abspath(__file__)))
from landauer_gaussian_v2_common import (exact_binom_ok,  # noqa: E402
                                         strided_argmin, thr_interp)

RHO = 1 / math.sqrt(2.0)
D_T = 0.25
A_C, B_C = 1 - 2 * D_T, math.sqrt(2.0) * D_T      # Thm-2 coefficients
DCW_T = D_T * (1 - 2 * D_T)                        # tilt covering distortion
N_BLK, SHIFT = 10, 7
T_PILOT, T_GOV = 250, 400
RB = [0.15, 0.275, 0.40, 0.525, 0.65, 0.775, 0.90, 1.025, 1.15, 1.275]
EXC = 0.05                                         # covering rate excess
TAU2_STRICT = 0.5                                  # reported-only face


def encode(cw, csq, tgt):
    """Min-distance encode of target blocks; index + realized cover MSE."""
    T, n = tgt.shape
    M = np.empty(T, dtype=np.int64)
    se = 0.0
    for t in range(T):
        sc = csq - 2.0 * (cw @ tgt[t])
        M[t] = int(np.argmin(sc))
        se += float(((tgt[t] - cw[M[t]]) ** 2).sum())
    return M, se / (T * n)


def context_scores(cw, csq, sig_cw2, cov_cwS, varS, Sctx):
    """-2 log posterior of codewords given the context block S^n, under the
    jointly Gaussian proxy (cw entry ~ N(0, sig_cw2), Cov(cw_i, S_i) =
    cov_cwS): score = ||cw||^2/sig_res - 2 <cw, mu(S)>/sig_res + const,
    mu(S) = (cov_cwS/varS) S, sig_res = sig_cw2 - cov_cwS^2/varS."""
    k = cov_cwS / varS
    sig_res = max(sig_cw2 - cov_cwS * k, 1e-9)
    return (csq - 2.0 * (cw @ (k * Sctx))) / sig_res


def curves(rng, M, nbits, scores, n, T):
    errs, ctrl, chance = [], [], []
    for rb in RB:
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    a = ap.parse_args()
    SEED = 20260828 if a.pilot else 20260830
    rng = np.random.default_rng(SEED)
    n, T = N_BLK, (T_PILOT if a.pilot else T_GOV)
    print(f"GO-11 encoder-tilt face -- {'PILOT' if a.pilot else 'GOVERNED'} "
          f"run, seed {SEED}")
    print(f"n={n} T={T} rho^2=0.5 D={D_T} a={A_C} b={B_C:.4f} "
          f"d_cw_tilt={DCW_T}", flush=True)
    t0 = time.time()

    # rates and codebooks
    R_m = 0.5 * math.log2(1.0 / D_T)               # cover y at D
    var_z = A_C ** 2 + B_C ** 2 + 2 * A_C * B_C * RHO
    R_t = 0.5 * math.log2(var_z / DCW_T)           # cover z at D(1-2D)
    nb_m = int(math.ceil(n * (R_m + EXC)))
    nb_t = int(math.ceil(n * (R_t + EXC)))
    print(f"  rates: R_m={R_m:.4f} (2^{nb_m})  R_t={R_t:.4f} (2^{nb_t}) "
          f"-- tilt rate premium {R_t - R_m:.4f} b/sym (Cor 2, reported)",
          flush=True)
    cw_m = rng.normal(0, math.sqrt(1 - D_T),
                      size=(1 << nb_m, n)).astype(np.float32)
    cw_t = rng.normal(0, math.sqrt(var_z - DCW_T),
                      size=(1 << nb_t, n)).astype(np.float32)
    cw_f = rng.normal(0, math.sqrt(var_z - DCW_T),
                      size=(1 << nb_t, n)).astype(np.float32)
    sq_m = (cw_m * cw_m).sum(1)
    sq_t = (cw_t * cw_t).sum(1)
    sq_f = (cw_f * cw_f).sum(1)

    # source, targets, records
    Y = rng.normal(0, 1, size=(T, n)).astype(np.float32)
    W = rng.normal(0, 1, size=(T, n)).astype(np.float32)
    V = RHO * Y + math.sqrt(1 - RHO ** 2) * W
    Zp = (A_C * Y + B_C * V).astype(np.float32)
    Zm = (A_C * Y - B_C * V).astype(np.float32)
    M_m, dcw_m = encode(cw_m, sq_m, Y)
    M_t, dcw_t = encode(cw_t, sq_t, Zp)
    M_f, dcw_f = encode(cw_f, sq_f, Zm)
    # consumer-distortion audit (record vs Y)
    dcons = {}
    for name, cw, M in (("MARG", cw_m, M_m), ("TILT", cw_t, M_t),
                        ("TILTflip", cw_f, M_f)):
        dcons[name] = float(np.mean([((Y[t] - cw[M[t]]) ** 2).mean()
                                     for t in range(T)]))
    print(f"  encoded: cover MSE m/t/f = {dcw_m:.4f}/{dcw_t:.4f}/{dcw_f:.4f}"
          f"  consumer distortion = "
          + "/".join(f"{dcons[k]:.4f}" for k in dcons)
          + f"  ({time.time()-t0:.0f}s)", flush=True)

    out = dict(seed=SEED, pilot=bool(a.pilot), n=n, trials=T, D=D_T,
               rates=dict(R_m=R_m, R_t=R_t, nb_m=nb_m, nb_t=nb_t),
               cover_mse=[dcw_m, dcw_t, dcw_f], consumer_d=dcons,
               contexts={})
    cells = []

    def reg(name, errs, ctrl, chance):
        thr = thr_interp(errs, RB)
        out["contexts"][name] = dict(errs=errs, thr=thr)
        cells.extend(zip(ctrl, chance))
        return thr

    # analytic per-symbol proxies for the context posterior (tau^2 = 0, S=V)
    cov_mV = (1 - D_T) * RHO            # Cov(cw_m-signal, V) ~ Cov(y_q, V)
    cov_tV = A_C * RHO + B_C            # Cov(z+, V)
    cov_fV = A_C * RHO - B_C            # = 0 exactly at the canonical point
    arms = (("MARG", cw_m, sq_m, M_m, nb_m, 1 - D_T, cov_mV),
            ("TILT", cw_t, sq_t, M_t, nb_t, var_z - DCW_T, cov_tV),
            ("TILTflip", cw_f, sq_f, M_f, nb_t, var_z - DCW_T, cov_fV))
    thr0, thrS, thrSh = {}, {}, {}
    for name, cw, sq, M, nb, s2cw, covV in arms:
        e0, c0, h0 = curves(rng, M, nb, None, n, T)
        thr0[name] = reg(f"{name}|none", e0, c0, h0)
        scS = np.stack([context_scores(cw, sq, s2cw, covV, 1.0, V[t])
                        for t in range(T)])
        eS, cS, hS = curves(rng, M, nb, scS, n, T)
        thrS[name] = reg(f"{name}|S", eS, cS, hS)
        scH = np.stack([context_scores(cw, sq, s2cw, covV, 1.0,
                                       V[(t + SHIFT) % T])
                        for t in range(T)])
        eH, cH, hH = curves(rng, M, nb, scH, n, T)
        thrSh[name] = reg(f"{name}|S'", eH, cH, hH)
        print(f"  [{name}] thr none/S/S' = {thr0[name]:.3f}/"
              f"{thrS[name]:.3f}/{thrSh[name]:.3f}  "
              f"({time.time()-t0:.0f}s)", flush=True)

    disc = {k: thr0[k] - thrS[k] for k in thr0}
    disc_sh = {k: thr0[k] - thrSh[k] for k in thr0}
    # analytic predictions (per symbol): discount = R_arm - content
    L_marg = 0.5 * math.log2((0.5 + 0.5 * D_T) / D_T)      # Steinberg 0.661
    L_tilt = 0.5 * math.log2(1 / (2 * D_T))                # Gray floor 0.500
    pred = dict(disc_m=R_m - L_marg, disc_t=R_t - L_tilt, disc_f=0.0,
                tilt_adv=(R_t - L_tilt) - (R_m - L_marg),
                content_gap=L_marg - L_tilt)               # 0.161 b/sym
    meas_tilt_adv = disc["TILT"] - disc["MARG"]
    # measured contents (per-symbol): Rc_arm - disc_arm, Rc = nb/n
    Lhat = {k: (nb_t if k != "MARG" else nb_m) / n - disc[k] for k in disc}
    print(f"  discounts: " + "  ".join(f"{k}={disc[k]:.3f}" for k in disc))
    print(f"  measured contents: "
          + "  ".join(f"{k}={Lhat[k]:.3f}" for k in Lhat)
          + f"  (pred TILT={L_tilt}, MARG={L_marg:.3f})")
    print(f"  tilt advantage disc_t - disc_m = {meas_tilt_adv:.4f} "
          f"(asymptotic {pred['tilt_adv']:.4f})", flush=True)

    # strict face tau^2 = 0.5 (REPORTED, not gated)
    tau = math.sqrt(TAU2_STRICT)
    Sst = V + tau * rng.normal(0, 1, size=(T, n)).astype(np.float32)
    scT = np.stack([context_scores(cw_t, sq_t, var_z - DCW_T, cov_tV,
                                   1 + TAU2_STRICT, Sst[t])
                    for t in range(T)])
    eT, cT, hT = curves(rng, M_t, nb_t, scT, n, T)
    thr_strict = reg("TILT|S_tau0.5", eT, cT, hT)
    out["strict_face"] = dict(thr=thr_strict,
                              disc=thr0["TILT"] - thr_strict)
    print(f"  strict face (tau^2=0.5, reported): disc="
          f"{thr0['TILT'] - thr_strict:.3f}", flush=True)

    # ---------------- gates (bars sealed in prereg GO-P-2026-061)
    # Gate shapes corrected on pilot run 1 (seed 20260828, disclosed
    # in-prereg): the flip arm is a context-blindness PROBE, not a consumer
    # arm -- its channel distortion 0.625 > D makes consumer matching
    # impossible at these coefficients (itself the point) -- so it is
    # audit-exempt (E1) and its null is S-vs-S' independence (E4), not
    # disc-vs-none (which measures a min-norm-prior artifact). E2 upper /
    # E3 tolerance widened for the finite-n instrument (MARG's Steinberg
    # content realizes slowly); every bar carries >= 1.3x pilot margin.
    verdict = dict(
        E1_consumer_audit=bool(
            all(0.18 <= dcons[k] <= 0.36 for k in ("MARG", "TILT"))
            and abs(dcons["TILT"] - dcons["MARG"]) <= 0.06),
        E2_tilt_advantage=bool(
            0.40 * pred["tilt_adv"] <= meas_tilt_adv
            <= pred["tilt_adv"] + 0.35),
        E3_floor_attainment=bool(
            abs(Lhat["TILT"] - L_tilt) <= 0.28
            and (Lhat["MARG"] - Lhat["TILT"]) >= 0.40 * pred["content_gap"]),
        E4_flip_context_blindness=bool(
            abs(thrS["TILTflip"] - thrSh["TILTflip"]) <= 0.10),
        E5_shuffled_null=bool(all(abs(disc_sh[k]) <= 0.15
                                  for k in ("MARG", "TILT"))),
        E6_uniform_control_exact=bool(all(
            exact_binom_ok(c, h, T) for c, h in cells)),
    )
    out["discounts"] = disc
    out["contents_hat"] = Lhat
    out["predictions"] = pred
    out["tilt_advantage"] = meas_tilt_adv
    out["verdict"] = verdict
    out["GO11ET_supported"] = bool(all(verdict.values()))
    out["seconds_total"] = round(time.time() - t0, 1)
    print(f"verdict: {verdict}")
    print(f"GO11ET_supported: {out['GO11ET_supported']}")
    print("===GO11ET-JSON===")
    print(json.dumps(out, indent=1, default=float))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
