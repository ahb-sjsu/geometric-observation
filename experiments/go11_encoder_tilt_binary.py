# GO-11 encoder-tilt face, SECOND SOURCE FAMILY (binary)
# (GO-P-2026-062; first family = Gaussian, GO-P-2026-058-lineage 061
# ALL PASS 6/6). Same mechanism, discrete twin:
#
# Source: iid pairs (Y_i, V_i), fair bits with P(Y != V) = p = 0.25;
# reset context S = V (X-measurable; the attainment face). Consumer reads
# Y at Hamming distortion D = 0.2. Three records:
#   MARG  covers Y alone (crossover-D channel; content ~ h2(D*p) - h2(D)
#         ~ 0.212 b/sym -- the marginalized-class optimum, BA-exact target
#         computed in-harness),
#   TILT  implements the pair-BA L-optimal channel q*(yh|y,v) at consumer
#         distortion D (content = the binary Gray-side value, BA-exact
#         target ~ 0.10 b/sym; the analytic warm-start channel "flip Y
#         toward V only on disagreement" gives 0.106 by hand),
#   FLIP  covers W = Y xor V, which is EXACTLY independent of V under the
#         symmetric coupling -- the analytic context-blindness probe,
#         audit-exempt (W alone is useless to the consumer: P(Y != W-hat)
#         ~ 1/2), gated on S-vs-S' independence only.
# Instrument: 053/059 decode-threshold lineage; binary MAP context decode
# scores each codeword by the per-symbol log-likelihood log P(cw_i | v_i)
# under the record|V law (from q* / the cascade), ties uniform via
# strided_argmin. disc = thr(|none) - thr(|S). Noisy-context face
# S = V xor Bern(0.1) measured and REPORTED (not gated).
#
# Usage: python go11_encoder_tilt_binary.py [--pilot]
#   pilot seed 20260901 (logged in-prereg) / governed seed 20260902.
# Output: sentinel JSON ===GO11ETB-JSON===.  Tier B (CPU, numpy).  MIT.
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

P_YV = 0.25
D_T = 0.20
N_BLK, SHIFT = 24, 7
T_PILOT, T_GOV = 250, 400
RB = [0.05, 0.125, 0.20, 0.275, 0.35, 0.425, 0.50, 0.60, 0.70, 0.80]
EXC = 0.05
Q_NOISY = 0.10                              # reported-only context noise
LOG2 = math.log(2.0)


def h2(x):
    x = min(max(x, 1e-12), 1 - 1e-12)
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)


# ---------------- exact BA targets on the 4-state joint (no seed needed)
def ba_targets():
    """Returns (L_marg, L_tilt, R_tilt, q_tilt[ (y,v) -> P(yh=1) ])."""
    # states: (y,v) in {00,01,10,11}; p(y,v): P(y=v)=1-p
    pj = np.array([(1 - P_YV) / 2, P_YV / 2, P_YV / 2, (1 - P_YV) / 2])
    yv = [(0, 0), (0, 1), (1, 0), (1, 1)]
    dH = np.array([[abs(y - yh) for yh in (0, 1)] for y, v in yv],
                  dtype=float)
    sbin = np.array([v for y, v in yv])

    def cond_mi(q):
        L = 0.0
        for s in (0, 1):
            msk = sbin == s
            ps = pj[msk].sum()
            pxg = pj[msk] / ps
            J = pxg[:, None] * q[msk]
            pm = J.sum(0)
            Hj = -(J[J > 1e-15] * np.log2(J[J > 1e-15])).sum()
            Hx = -(pxg * np.log2(np.maximum(pxg, 1e-15))).sum()
            Hm = -(pm[pm > 1e-15] * np.log2(pm[pm > 1e-15])).sum()
            L += ps * (Hx + Hm - Hj)
        return L

    def rate(q):
        J = pj[:, None] * q
        pm = J.sum(0)
        Hj = -(J[J > 1e-15] * np.log2(J[J > 1e-15])).sum()
        Hx = -(pj * np.log2(pj)).sum()
        Hm = -(pm[pm > 1e-15] * np.log2(pm[pm > 1e-15])).sum()
        return Hx + Hm - Hj

    def ba_min(beta, restrict_y=False, iters=8000):
        q = np.full((4, 2), 0.5)
        for _ in range(iters):
            lq = np.zeros((4, 2))
            for s in (0, 1):
                msk = sbin == s
                ps = pj[msk].sum()
                r = (pj[msk, None] * q[msk]).sum(0) / ps
                lq[msk] += np.log(np.maximum(r, 1e-300))[None, :]
            lq -= beta * LOG2 * dH
            qn = np.exp(lq - lq.max(1, keepdims=True))
            qn /= qn.sum(1, keepdims=True)
            if restrict_y:                    # channel sees y only
                for y in (0, 1):
                    msk = np.array([yy == y for yy, vv in yv])
                    avg = (pj[msk, None] * qn[msk]).sum(0) / pj[msk].sum()
                    qn[msk] = avg
            if np.abs(qn - q).max() < 1e-13:
                q = qn
                break
            q = qn
        return q

    def solve(restrict_y):
        blo, bhi = 0.05, 400.0
        for _ in range(60):
            bm = math.sqrt(blo * bhi)
            q = ba_min(bm, restrict_y)
            dd = float((pj[:, None] * q * dH).sum())
            if dd > D_T:
                blo = bm
            else:
                bhi = bm
        q = ba_min(bhi, restrict_y)
        return cond_mi(q), rate(q), q

    L_m, R_m_eff, _ = solve(True)
    L_t, R_t, q_t = solve(False)
    return L_m, L_t, R_t, q_t


def encode_ll(cw, llt0, llt1):
    """Max-loglik encode: per trial, per codeword sum of log q*(cw_i|y,v)."""
    # llt0/llt1: (T, n) log-lik of cw bit 0 / 1 at each position
    T = llt0.shape[0]
    M = np.empty(T, dtype=np.int64)
    for t in range(T):
        sc = (1 - cw) @ llt0[t] + cw @ llt1[t]
        M[t] = int(np.argmax(sc))
    return M


def curves(rng, M, nbits, scores, n, T, sign=1.0):
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
                acc += strided_argmin(sign * scores[t][b::nbins], b, nbins,
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
    SEED = 20260901 if a.pilot else 20260902
    rng = np.random.default_rng(SEED)
    n, T = N_BLK, (T_PILOT if a.pilot else T_GOV)
    print(f"GO-11 encoder-tilt BINARY face -- "
          f"{'PILOT' if a.pilot else 'GOVERNED'} run, seed {SEED}")
    t0 = time.time()
    L_m_t, L_t_t, R_t_t, q_t = ba_targets()
    R_m = 1 - h2(D_T)
    print(f"n={n} T={T} p={P_YV} D={D_T} | BA targets: L_marg={L_m_t:.4f} "
          f"L_tilt={L_t_t:.4f} R_tilt={R_t_t:.4f} R_marg={R_m:.4f} "
          f"(tilt rate premium {R_t_t - R_m:.4f}, reported)", flush=True)

    nb_m = int(math.ceil(n * (R_m + EXC)))
    nb_t = int(math.ceil(n * (R_t_t + EXC)))
    nb_f = int(math.ceil(n * (h2(P_YV) - h2(D_T) + EXC))) if h2(P_YV) > \
        h2(D_T) else int(math.ceil(n * 0.15))
    cw_m = rng.integers(0, 2, size=(1 << nb_m, n)).astype(np.int8)
    # tilt codewords from the BA reproduction marginal
    pj4 = np.array([(1 - P_YV) / 2, P_YV / 2, P_YV / 2, (1 - P_YV) / 2])
    p_yh1 = float((pj4 * q_t[:, 1]).sum())
    cw_t = (rng.random(size=(1 << nb_t, n)) < p_yh1).astype(np.int8)
    cw_f = (rng.random(size=(1 << nb_f, n)) < P_YV).astype(np.int8)

    Y = rng.integers(0, 2, size=(T, n)).astype(np.int8)
    Flip = (rng.random(size=(T, n)) < P_YV).astype(np.int8)
    V = (Y ^ Flip).astype(np.int8)
    Wx = (Y ^ V).astype(np.int8)

    # encode: MARG min-Hamming to Y; TILT max-loglik under q*; FLIP min-H to W
    M_m = np.array([int(np.argmin(((cw_m ^ Y[t]) != 0).sum(1)))
                    for t in range(T)], dtype=np.int64)
    idx4 = (2 * Y + V).astype(np.int64)
    lq0 = np.log(np.maximum(q_t[:, 0], 1e-12))
    lq1 = np.log(np.maximum(q_t[:, 1], 1e-12))
    llt0 = lq0[idx4]
    llt1 = lq1[idx4]
    M_t = encode_ll(cw_t, llt0, llt1)
    M_f = np.array([int(np.argmin(((cw_f ^ Wx[t]) != 0).sum(1)))
                    for t in range(T)], dtype=np.int64)
    dcons = dict(
        MARG=float(np.mean([(Y[t] != cw_m[M_m[t]]).mean() for t in range(T)])),
        TILT=float(np.mean([(Y[t] != cw_t[M_t[t]]).mean() for t in range(T)])),
        FLIP=float(np.mean([(Y[t] != cw_f[M_f[t]]).mean() for t in range(T)])))
    print(f"  encoded: consumer distortion = "
          + "/".join(f"{dcons[k]:.4f}" for k in dcons)
          + f"  ({time.time()-t0:.0f}s)", flush=True)

    # per-symbol record|V log-lik tables for context decode
    # MARG record ~ Y through crossover-D: P(cw != v) = D*p convolution
    dm = D_T + P_YV - 2 * D_T * P_YV
    # TILT record law given v: P(yh=1|v) from q* and p(y|v)
    pt = np.zeros((2, 2))                     # [v, yh]
    for v in (0, 1):
        for y in (0, 1):
            pt[v, :] += (P_YV if y != v else 1 - P_YV) * q_t[2 * y + v, :]
    out = dict(seed=SEED, pilot=bool(a.pilot), n=n, trials=T, p=P_YV,
               D=D_T, ba_targets=dict(L_marg=L_m_t, L_tilt=L_t_t,
                                      R_tilt=R_t_t, R_marg=R_m),
               rates=dict(nb_m=nb_m, nb_t=nb_t, nb_f=nb_f),
               consumer_d=dcons, contexts={})
    cells = []

    def reg(name, errs, ctrl, chance):
        thr = thr_interp(errs, RB)
        out["contexts"][name] = dict(errs=errs, thr=thr)
        cells.extend(zip(ctrl, chance))
        return thr

    def ctx_scores(cw, Vctx, law):
        """-loglik of codewords given context bits; law[v, bit]."""
        l0 = np.log(np.maximum(law[:, 0], 1e-12))[Vctx]     # (T, n)
        l1 = np.log(np.maximum(law[:, 1], 1e-12))[Vctx]
        return np.stack([-((1 - cw) @ l0[t] + cw @ l1[t]) for t in
                         range(Vctx.shape[0])])

    law_m = np.array([[1 - dm, dm], [dm, 1 - dm]])
    law_f = np.array([[1 - P_YV, P_YV], [1 - P_YV, P_YV]])  # v-independent
    arms = (("MARG", cw_m, M_m, nb_m, law_m),
            ("TILT", cw_t, M_t, nb_t, pt),
            ("FLIP", cw_f, M_f, nb_f, law_f))
    thr0, thrS, thrSh = {}, {}, {}
    for name, cw, M, nb, law in arms:
        e0, c0, hh0 = curves(rng, M, nb, None, n, T)
        thr0[name] = reg(f"{name}|none", e0, c0, hh0)
        scS = ctx_scores(cw, V, law)
        eS, cS, hS = curves(rng, M, nb, scS, n, T)
        thrS[name] = reg(f"{name}|S", eS, cS, hS)
        Vsh = V[(np.arange(T) + SHIFT) % T]
        scH = ctx_scores(cw, Vsh, law)
        eH, cH, hH = curves(rng, M, nb, scH, n, T)
        thrSh[name] = reg(f"{name}|S'", eH, cH, hH)
        print(f"  [{name}] thr none/S/S' = {thr0[name]:.3f}/"
              f"{thrS[name]:.3f}/{thrSh[name]:.3f}  "
              f"({time.time()-t0:.0f}s)", flush=True)

    disc = {k: thr0[k] - thrS[k] for k in thr0}
    disc_sh = {k: thr0[k] - thrSh[k] for k in thr0}
    Rc = dict(MARG=nb_m / n, TILT=nb_t / n, FLIP=nb_f / n)
    Lhat = {k: Rc[k] - disc[k] for k in disc}
    pred_adv = (R_t_t - L_t_t) - (R_m - L_m_t)
    meas_adv = disc["TILT"] - disc["MARG"]
    content_gap_t = L_m_t - L_t_t
    print(f"  discounts: " + "  ".join(f"{k}={disc[k]:.3f}" for k in disc))
    print(f"  contents: " + "  ".join(f"{k}={Lhat[k]:.3f}" for k in Lhat)
          + f"  (targets TILT={L_t_t:.3f} MARG={L_m_t:.3f})")
    print(f"  tilt advantage = {meas_adv:.4f} (asymptotic {pred_adv:.4f})",
          flush=True)

    # noisy-context face (REPORTED)
    Vn = (V ^ (rng.random(size=(T, n)) < Q_NOISY)).astype(np.int8)
    ptn = np.zeros((2, 2))
    for v in (0, 1):
        ptn[v] = (1 - Q_NOISY) * pt[v] + Q_NOISY * pt[1 - v]
    scN = ctx_scores(cw_t, Vn, ptn)
    eN, cN, hN = curves(rng, M_t, nb_t, scN, n, T)
    thrN = reg("TILT|S_q0.1", eN, cN, hN)
    out["noisy_face"] = dict(thr=thrN, disc=thr0["TILT"] - thrN)
    print(f"  noisy face (q=0.1, reported): disc="
          f"{thr0['TILT'] - thrN:.3f}", flush=True)

    # ---------------- gates (bars sealed in prereg GO-P-2026-062)
    verdict = dict(
        B1_consumer_audit=bool(
            all(0.14 <= dcons[k] <= 0.30 for k in ("MARG", "TILT"))
            and abs(dcons["TILT"] - dcons["MARG"]) <= 0.06),
        B2_tilt_advantage=bool(
            0.40 * pred_adv <= meas_adv <= pred_adv + 0.30),
        B3_content_ordering=bool(
            (Lhat["MARG"] - Lhat["TILT"]) >= 0.40 * content_gap_t),
        B4_flip_context_blindness=bool(
            abs(thrS["FLIP"] - thrSh["FLIP"]) <= 0.10),
        B5_shuffled_null=bool(all(abs(disc_sh[k]) <= 0.15
                                  for k in ("MARG", "TILT"))),
        B6_uniform_control_exact=bool(all(
            exact_binom_ok(c, hc, T) for c, hc in cells)),
    )
    out["discounts"] = disc
    out["contents_hat"] = Lhat
    out["tilt_advantage"] = meas_adv
    out["pred_advantage"] = pred_adv
    out["verdict"] = verdict
    out["GO11ETB_supported"] = bool(all(verdict.values()))
    out["seconds_total"] = round(time.time() - t0, 1)
    print(f"verdict: {verdict}")
    print(f"GO11ETB_supported: {out['GO11ETB_supported']}")
    print("===GO11ETB-JSON===")
    print(json.dumps(out, indent=1, default=float))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
