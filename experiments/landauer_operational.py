# Operational finite-n demonstration of the consumer-relative Landauer
# separation (paper/consumer-relative-landauer.pdf, Thm 1 + Prop 2), plus a
# genericity sweep of the rate-work frontier and a staleness Monte Carlo.
# Registered as GO-P-2026-043.  Tier B (Atlas CPU, single process, ~10 min).
#
# [A] OPERATIONAL SEPARATION (the headline).  Prop-2 source X=(A,B) iid fair
#     bits, reset side information S=A.  Target test channel BSC(0.08) on A x
#     BSC(0.32) on B: per-letter R = 0.6934 bits, L = I(X;Xh|S) = 0.0956 bits.
#     For each n we build one random codebook of 2^ceil(n(R+0.03)) uniform
#     codewords, encode T source blocks by ML/typicality scoring (weighted
#     Hamming, weights log((1-Di)/Di)), then RANDOM-BIN the stored index M at
#     bin rate rb and try to recover M from (bin, S^n) alone by max-likelihood
#     within the bin (equivalently min Hamming(cwA, a^n)).  Thm 1 predicts a
#     decoding threshold at rb ~ (R+0.03) - I(Xh;S) ~ 0.13 -- far below the
#     description rate: the memory that costs ~0.7 bits/symbol to DESCRIBE
#     costs only ~0.1-0.13 bits/symbol of residual uncertainty to RESET when
#     the side information is retained.  A no-side-information control decoder
#     (uniform pick within bin) must fail at the same bin rate: the gap is
#     bought by S, not by the binning.
# [B] GENERICITY SWEEP.  For random discrete sources (nx in 3..6, ns in 2..3,
#     random joint p_XS, random bounded distortion), solve both frontier
#     endpoints at a matched distortion (alpha=1 min-rate channel vs alpha=0
#     min-work channel via the eq.-(20) fixed point) and measure
#     gap_work = L(min-R) - L(min-L) and gap_rate = R(min-L) - R(min-R).
#     Measurement (the paper exhibits the separation, it does not claim
#     genericity); sanity gates only: gaps never negative beyond tolerance.
# [C] STALENESS.  Simulated binary Markov chain p=0.05: plug-in H(X0|Xt) from
#     1e6 chains matches h2(q_t) and the predictive complement I+L=1 bit at
#     every age; a random 4-state chain matches its exact L_t.
#
# Usage:  python experiments/landauer_operational.py [--pilot]
#         --pilot: reduced n-grid/trials for calibration only (never committed)
# Output: sentinel-delimited JSON (===GOLOP-JSON=== ... ===END===).  MIT.
import argparse
import json
import sys
import time

import numpy as np

SEED = 20260802
LOG2 = np.log(2.0)

def h2(t):
    t = float(t)
    if t <= 0.0 or t >= 1.0:
        return 0.0
    return -t * np.log2(t) - (1 - t) * np.log2(1 - t)

def Hb(p):
    p = np.asarray(p, dtype=float).ravel()
    p = p[p > 1e-300]
    return float(-(p * np.log2(p)).sum())

def mi(J):
    return Hb(J.sum(1)) + Hb(J.sum(0)) - Hb(J)

# --------------------------------------------------------------- popcount
_LUT = np.array([bin(i).count("1") for i in range(65536)], dtype=np.uint16)

def pop64(a):
    """Popcount of a uint64 array."""
    return _LUT[np.ascontiguousarray(a).view(np.uint16).reshape(-1, 4)].sum(
        axis=1, dtype=np.int64)

# =========================================================================
# [A] operational separation
# =========================================================================
DA, DB = 0.08, 0.32
R_AN = 2 - h2(DA) - h2(DB)          # 0.69344
L_AN = 1 - h2(DB)                   # 0.09562
RC_EXCESS = 0.03
WA, WB = np.log((1 - DA) / DA), np.log((1 - DB) / DB)   # ML-encoding weights

def run_partA(ngrid, trials, rbs, rng):
    rows = []
    for n, T in zip(ngrid, trials):
        t0 = time.time()
        nbits = int(np.ceil(n * (R_AN + RC_EXCESS)))
        Ncw = 1 << nbits
        cwA = rng.integers(0, 1 << n, size=Ncw, dtype=np.uint64)
        cwB = rng.integers(0, 1 << n, size=Ncw, dtype=np.uint64)
        # source blocks
        xA = rng.integers(0, 1 << n, size=T, dtype=np.uint64)
        xB = rng.integers(0, 1 << n, size=T, dtype=np.uint64)
        M = np.empty(T, dtype=np.int64)
        errA_bits = 0
        errB_bits = 0
        for t in range(T):
            score = WA * pop64(cwA ^ xA[t]) + WB * pop64(cwB ^ xB[t])
            mins = np.flatnonzero(score == score.min())
            M[t] = int(mins[rng.integers(0, mins.size)])
            errA_bits += int(pop64(np.array([cwA[M[t]] ^ xA[t]]))[0])
            errB_bits += int(pop64(np.array([cwB[M[t]] ^ xB[t]]))[0])
        DA_hat = errA_bits / (n * T)
        DB_hat = errB_bits / (n * T)
        D_hat = 0.5 * (DA_hat + DB_hat)
        # per-letter empirical joint over (x, xh), x = 2a+b -- for R^ and L^
        Jj = np.zeros((4, 4))
        for t in range(T):
            a = np.array([(int(xA[t]) >> i) & 1 for i in range(n)])
            b = np.array([(int(xB[t]) >> i) & 1 for i in range(n)])
            ah = np.array([(int(cwA[M[t]]) >> i) & 1 for i in range(n)])
            bh = np.array([(int(cwB[M[t]]) >> i) & 1 for i in range(n)])
            np.add.at(Jj, (2 * a + b, 2 * ah + bh), 1.0)
        Jj /= Jj.sum()
        R_hat = mi(Jj)
        # L^ = I(X;Xh|S), S = A: split by a
        L_hat = 0.0
        for s in (0, 1):
            sel = Jj[2 * s: 2 * s + 2, :]
            ps = sel.sum()
            if ps > 0:
                L_hat += ps * mi(sel / ps)
        row = dict(n=n, trials=T, codebook_bits=nbits, DA_hat=DA_hat,
                   DB_hat=DB_hat, D_hat=D_hat, R_hat=R_hat, L_hat=L_hat,
                   rb=[], err_si=[], err_ctrl=[])
        # ---- conditional-reset decode at each bin rate
        for rb in rbs:
            bbits = max(1, int(np.ceil(n * rb)))
            nbins = 1 << bbits
            ok_si = 0
            ok_ct = 0
            for t in range(T):
                b = int(M[t]) % nbins
                members = np.arange(b, Ncw, nbins, dtype=np.int64)
                # ML with side information a^n: min Hamming(cwA, a^n)
                sc = pop64(cwA[members] ^ xA[t])
                mins = members[np.flatnonzero(sc == sc.min())]
                pick = int(mins[rng.integers(0, mins.size)])
                ok_si += pick == M[t]
                # control: no side information -> uniform pick within bin
                ok_ct += int(members[rng.integers(0, members.size)]) == M[t]
            row["rb"].append(float(rb))
            row["err_si"].append(1.0 - ok_si / T)
            row["err_ctrl"].append(1.0 - ok_ct / T)
        row["seconds"] = round(time.time() - t0, 1)
        rows.append(row)
        print(f"  [A] n={n:3d} T={T} cw=2^{nbits}  D^={D_hat:.3f} "
              f"R^={R_hat:.3f} L^={L_hat:.3f}  "
              f"err_si={['%.2f' % e for e in row['err_si']]}  ({row['seconds']}s)",
              flush=True)
    return rows

# =========================================================================
# [B] genericity sweep -- eq.-(20) fixed point (same as verify harness)
# =========================================================================
def coords(pXS, q):
    pX = pXS.sum(1)
    R = mi(pX[:, None] * q)
    L = 0.0
    for s in range(pXS.shape[1]):
        ps = pXS[:, s].sum()
        if ps > 1e-15:
            pxg = pXS[:, s] / ps
            L += ps * mi(pxg[:, None] * q)
    return R, float(L)

def fixed_point(pXS, d, alpha, beta, rng, iters=4000, tol=1e-12):
    nx, ns = pXS.shape
    nxh = d.shape[1]
    pX = pXS.sum(1)
    pS = pXS.sum(0)
    psx = pXS / np.maximum(pX, 1e-300)[:, None]
    pxg = pXS / np.maximum(pS, 1e-300)[None, :]
    q = np.full((nx, nxh), 1.0 / nxh)
    for _ in range(iters):
        qm = pX @ q
        qs = pxg.T @ q
        lq = alpha * np.log(np.maximum(qm, 1e-300))[None, :] \
            + (1 - alpha) * (psx @ np.log(np.maximum(qs, 1e-300))) \
            - beta * LOG2 * d
        lq -= lq.max(axis=1, keepdims=True)
        qn = np.exp(lq)
        qn /= qn.sum(axis=1, keepdims=True)
        delta = float(np.abs(qn - q).max())
        q = qn
        if delta < tol:
            break
    return q

def solve_at_D(pXS, d, alpha, Dt, rng):
    """Bisect beta so that E d ~ Dt (distortion decreasing in beta)."""
    lo, hi = 0.0, 400.0
    pX = pXS.sum(1)
    for _ in range(48):
        beta = 0.5 * (lo + hi)
        q = fixed_point(pXS, d, alpha, beta, rng)
        Dd = float((pX[:, None] * q * d).sum())
        if Dd > Dt:
            lo = beta
        else:
            hi = beta
    return q, Dd

def run_partB(n_sources, rng):
    gaps_w, gaps_r, negs = [], [], 0
    for k in range(n_sources):
        nx = int(rng.integers(3, 7))
        ns = int(rng.integers(2, 4))
        pXS = rng.dirichlet(np.ones(nx * ns)).reshape(nx, ns)
        d = rng.uniform(0.0, 1.0, size=(nx, nx))
        np.fill_diagonal(d, 0.0)
        pX = pXS.sum(1)
        D0 = float(min((pX * d[:, y]).sum() for y in range(nx)))  # D at R=0
        Dt = 0.35 * D0
        if Dt < 1e-4:
            continue
        qR, _ = solve_at_D(pXS, d, 1.0, Dt, rng)   # min-rate endpoint
        qL, _ = solve_at_D(pXS, d, 0.0, Dt, rng)   # min-work endpoint
        Rr, Lr = coords(pXS, qR)
        Rl, Ll = coords(pXS, qL)
        gw, gr = Lr - Ll, Rl - Rr
        negs += (gw < -1e-6) + (gr < -1e-6)
        gaps_w.append(gw)
        gaps_r.append(gr)
    gaps_w = np.array(gaps_w)
    gaps_r = np.array(gaps_r)
    out = dict(
        n_sources=int(gaps_w.size), negative_gaps=int(negs),
        frac_sep_001=float(np.mean((gaps_w > 0.01) & (gaps_r > 0.01))),
        frac_sep_005=float(np.mean((gaps_w > 0.05) & (gaps_r > 0.05))),
        gap_work_median=float(np.median(gaps_w)),
        gap_work_p90=float(np.quantile(gaps_w, 0.9)),
        gap_work_max=float(gaps_w.max()),
        gap_rate_median=float(np.median(gaps_r)),
    )
    print(f"  [B] {out['n_sources']} sources: separation>0.01 bits in "
          f"{100*out['frac_sep_001']:.0f}%  (>0.05: {100*out['frac_sep_005']:.0f}%)"
          f"  median gap_work={out['gap_work_median']:.4f}  "
          f"max={out['gap_work_max']:.3f}  negative gaps={negs}", flush=True)
    return out

# =========================================================================
# [C] staleness Monte Carlo
# =========================================================================
def run_partC(rng, nchain=1_000_000):
    p = 0.05
    X = rng.integers(0, 2, size=nchain, dtype=np.int8)
    X0 = X.copy()
    worst_id = 0.0
    worst_comp = 0.0
    prevL = -1.0
    mono_ok = True
    for t in range(0, 41):
        if t > 0:
            X ^= (rng.random(nchain) < p).astype(np.int8)
        J = np.zeros((2, 2))
        np.add.at(J, (X0, X), 1.0)
        J /= nchain
        Lhat = Hb(J) - Hb(J.sum(0))
        Ihat = mi(J)
        qt = 0.5 * (1 - (1 - 2 * p) ** t)
        worst_id = max(worst_id, abs(Lhat - h2(qt)))
        worst_comp = max(worst_comp, abs(Ihat + Lhat - 1.0))
        if Lhat < prevL - 5e-3:
            mono_ok = False
        prevL = max(prevL, Lhat)
    # random 4-state chain vs exact
    k = 4
    Pt = rng.dirichlet(np.ones(k), size=k)
    w, V = np.linalg.eig(Pt.T)
    pi = np.abs(np.real(V[:, np.argmax(np.real(w))]))
    pi /= pi.sum()
    X = rng.choice(k, size=nchain, p=pi)
    X0 = X.copy()
    worst4 = 0.0
    Pk = np.eye(k)
    for t in range(0, 17):
        if t > 0:
            U = rng.random(nchain)
            C = np.cumsum(Pt, axis=1)
            Xn = (U[:, None] > C[X, :]).sum(axis=1)
            X = Xn.astype(np.int64)
            Pk = Pk @ Pt
        if t in (0, 1, 2, 4, 8, 16):
            J = np.zeros((k, k))
            np.add.at(J, (X0, X), 1.0)
            J /= nchain
            Lhat = Hb(J) - Hb(J.sum(0))
            Jex = pi[:, None] * Pk
            Lex = Hb(Jex) - Hb(Jex.sum(0))
            worst4 = max(worst4, abs(Lhat - Lex))
    out = dict(binary_worst_identity=worst_id, binary_worst_complement=worst_comp,
               binary_monotone=bool(mono_ok), chain4_worst_dev=worst4)
    print(f"  [C] binary: |L^-h2(q_t)| worst={worst_id:.4f}, |I+L-1| worst="
          f"{worst_comp:.4f}, monotone={mono_ok}; 4-state plug-in vs exact "
          f"worst={worst4:.4f}", flush=True)
    return out

# =========================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    args = ap.parse_args()
    rng = np.random.default_rng(SEED + (1 if args.pilot else 0))
    rbs = [0.03, 0.08, 0.13, 0.19, 0.26, 0.35, 0.50]
    if args.pilot:
        ngrid = [12, 16, 20, 24]
        trials = [60, 60, 60, 60]
        n_sources, nchain = 40, 200_000
    else:
        ngrid = [12, 16, 20, 24, 28, 32]
        trials = [200, 200, 200, 200, 120, 100]
        n_sources, nchain = 250, 1_000_000
    print(f"consumer-relative Landauer operational run "
          f"({'PILOT' if args.pilot else 'FULL'})  seed={SEED}")
    print(f"target channel: BSC({DA}) x BSC({DB})  R={R_AN:.4f}  L={L_AN:.4f}  "
          f"I(Xh;S)={R_AN-L_AN:.4f}  codebook rate={R_AN+RC_EXCESS:.4f}")
    t0 = time.time()
    print("[A] operational separation")
    rowsA = run_partA(ngrid, trials, rbs, rng)
    print("[B] genericity sweep")
    outB = run_partB(n_sources, rng)
    print("[C] staleness")
    outC = run_partC(rng, nchain)

    # -------- gated verdict (bars registered in GO-P-2026-043)
    iSEP = rbs.index(0.26)
    iLOW = rbs.index(0.03)
    err_sep = [r["err_si"][iSEP] for r in rowsA]
    err_low = [r["err_si"][iLOW] for r in rowsA]
    err_low_big = [r["err_si"][iLOW] for r in rowsA if r["n"] >= 16]
    ctrl_sep = [r["err_ctrl"][iSEP] for r in rowsA if r["n"] >= 20]
    half = len(err_sep) // 2
    last = rowsA[-1]
    verdict = dict(
        # bars robust to ceil() effects in codebook/bin sizes; calibrated by
        # the logged pilot, sealed in GO-P-2026-043 before the governed run
        A1_separation_decodes=bool(err_sep[-1] <= 0.05 and err_sep[-2] <= 0.12
                                   and np.mean(err_sep[half:]) <= np.mean(err_sep[:half])),
        A2_bin_rate_below_040R=bool(0.26 <= 0.40 * last["R_hat"]),
        A3_converse_low_rb_fails=bool(min(err_low_big) >= 0.30
                                      and err_low[-1] >= 0.50),
        A4_side_info_specific=bool(min(ctrl_sep) >= 0.90) if ctrl_sep else False,
        A5_channel_realized=bool(abs(last["D_hat"] - 0.20) <= 0.03
                                 and 0.06 <= last["L_hat"] <= 0.14
                                 and 0.62 <= last["R_hat"] <= 0.78),
        B_sanity_no_negative_gaps=bool(outB["negative_gaps"] == 0),
        C_staleness_identity=bool(outC["binary_worst_identity"] <= 0.005
                                  and outC["binary_worst_complement"] <= 0.005
                                  and outC["binary_monotone"]
                                  and outC["chain4_worst_dev"] <= 0.01),
    )
    result = dict(
        claim="GO-7 operational rate-work separation (consumer-relative Landauer)",
        prereg="GO-P-2026-043",
        mode="pilot" if args.pilot else "full",
        seed=SEED,
        target=dict(DA=DA, DB=DB, R=R_AN, L=L_AN, codebook_excess=RC_EXCESS),
        rb_grid=rbs,
        partA=rowsA,
        partB=outB,
        partC=outC,
        err_at_rb026=err_sep,
        err_at_rb003=err_low,
        spearman_err_vs_n=rho,
        verdict=verdict,
        GOL_operational_supported=bool(all(verdict.values())),
        seconds_total=round(time.time() - t0, 1),
    )
    print(f"\nverdict: {verdict}")
    print(f"GOL_operational_supported: {result['GOL_operational_supported']}")
    print("===GOLOP-JSON===")
    print(json.dumps(result, indent=1))
    print("===END===")

if __name__ == "__main__":
    sys.exit(main())
