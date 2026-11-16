"""Numerical checks for the section on unstable autoregressive sources.

Source: T_t = sum_k a_k T_{t-k} + W_t, t >= 1, zero initial state, W_t iid
N(0, s2). Holder S_t = h T_t + U_t, U_t iid N(0, su2); weight q on T itself.
With a(z) = 1 - sum a_k z^k = prod_k (1 - rho_k z), f(w) = s2/|a(e^{iw})|^2
and rbar = sum_{|rho_k|>1} log2 |rho_k|.

Checks, for each of the four sources in CASES, at N = 40, 80, 160, 320
(Gamma_N = s2 (A^T A)^{-1}, Lemma 25):
  eigen_split: the eigenvalues of A^T A with index > p lie in [min|a|^2, max|a|^2],
     and all lie below max|a|^2.
  exploding_count: for N >= 80, the m smallest eigenvalues of A^T A, one per
     unstable pole, are below 1e-3 times the next one.
  outlier_logsum: (1/2N) log2 of the product of the m exploding eigenvalues of
     Gamma_N -> rbar.
  bulk_law: the averages of log(lambda) and 1/lambda over the N - p bulk
     eigenvalues -> the same averages of f.
  cost_limit: the window cost of the separable program (Lemma 24), computed by
     duality, -> alpha*rbar + (1-alpha)*rbar*[h=0] + V_f(alpha, D) (Theorem 26).
  The criterion for the last three is the O(1/N) rate of the proofs: N times the
  error at N = 320 is at most twice N times the error at N = 40, or the error is
  below 1e-6.
And once:
  feasible_spectra_dominated: sampled error covariances in the feasible set have
     sorted eigenvalues below those of Gamma_8 (the fact behind Lemma 24).
  common_optimizer: for every alpha the dual optimum equals the cost of
     delta = min(lambda, theta), in the window and in the spectral program
     (Lemma 24, Corollary 27); tolerance 1e-6 bits.
  mp_check: the log-sum of the exploding eigenvalues from the det identity, in
     double precision, against an 80-digit computation.

Numerics: see spectrum(). The bulk comes from A^T A; the exploding eigenvalues
enter only through their log-sum, taken from det Gamma_N = s2^N.

Usage: python verify_unstable.py [out.json]   (default: verify_unstable.json
next to this file). From Python: main() fills OUT and returns 0 when all pass.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize_scalar

LN2 = np.log(2.0)


def ar_coeffs(poles):
    c = np.real(np.poly(poles))          # z^p - a1 z^{p-1} - ... - ap
    return -c[1:]                          # a_1..a_p


def a_on_circle(a, w):
    z = np.exp(1j * w)
    return 1 - sum(a[k] * z ** (k + 1) for k in range(len(a)))


def matrices(a, N):
    A = np.eye(N)
    for k, ak in enumerate(a, start=1):
        A -= ak * np.eye(N, k=-k)
    return A


def spectrum(a, s2, N, m):
    """Eigenvalues of Gamma_N = s2 (A^T A)^{-1}. The N - m eigenvalues of A^T A that stay
    of order one are computed directly (absolute accuracy ~1e-15). The m exploding
    eigenvalues of Gamma_N, one per unstable pole, can differ from one another by more
    than double precision resolves, so their log-sum is taken from det Gamma_N = s2^N,
    which is the identity the proof uses, and each is set to exp(logsum/m). The cost of
    the separable program depends on exploding eigenvalues only through their log-sum,
    up to O(1/lambda), so this loses nothing; the identity itself is checked in high
    precision by mp_check."""
    A = matrices(a, N)
    mu = np.sort(np.linalg.eigvalsh(A.T @ A))           # ascending
    bounded = s2 / mu[m:]                                # N - m eigenvalues of Gamma_N
    L = N * np.log(s2) - np.sum(np.log(bounded))         # log-sum of the m exploding ones
    top = np.full(m, np.exp(L / m)) if m else np.zeros(0)
    return top, bounded, mu, L


def mp_check(poles, s2, N, dps):
    """High precision: the m smallest eigenvalues of A^T A, their log-sum, against the
    det identity computed in double precision."""
    import mpmath as mp
    mp.mp.dps = dps
    a = ar_coeffs(poles)
    m = sum(abs(r) > 1 for r in poles)
    A = mp.eye(N)
    for k, ak in enumerate(a, start=1):
        for i in range(k, N):
            A[i, i - k] = -mp.mpf(repr(float(ak)))
    E, _ = mp.eigsy(A.T * A)
    ev = sorted([E[i] for i in range(N)])
    L_mp = float(N * mp.log(s2) - sum(mp.log(s2 / e) for e in ev[m:]) )
    L_direct = float(sum(mp.log(s2 / e) for e in ev[:m]))
    _, _, _, L_double = spectrum(a, s2, N, m)
    return {"N": N, "m": m, "logsum_direct_mp": L_direct, "logsum_det_mp": L_mp,
            "logsum_det_double": L_double, "rel_diff": abs(L_direct - L_double) / abs(L_direct)}


def m_nu(lam, nu, alpha, q, j):
    """min over 0<d<=lam of 1/2 ln(lam/d) + (1-alpha)/2 ln((1+j d)/(1+j lam)) + nu q d (nats)."""
    lam = np.asarray(lam, float)
    if j > 0:
        b = 2 * nu * q - alpha * j
        d = (-b + np.sqrt(b * b + 8 * nu * q * j)) / (4 * nu * q * j)
    else:
        d = np.full_like(lam, 1 / (2 * nu * q))
    d = np.minimum(d, lam)
    return (0.5 * np.log(lam / d) + 0.5 * (1 - alpha) * np.log((1 + j * d) / (1 + j * lam))
            + nu * q * d)


def dual_cost(weights_lams, alpha, q, j, D):
    """sup_nu [ sum_i w_i m_nu(lam_i) - nu D ], in bits. weights_lams = list of (w, lam arrays)."""
    def neg(lognu):
        nu = np.exp(lognu)
        return -(sum(np.sum(w * m_nu(l, nu, alpha, q, j)) for w, l in weights_lams) - nu * D)
    res = minimize_scalar(neg, bounds=(-30, 30), method="bounded",
                          options={"xatol": 1e-12, "maxiter": 2000})
    return -res.fun / LN2


def spectral_cost(f_grid, alpha, q, j, D):
    w = np.full(f_grid.shape, 1.0 / len(f_grid))
    return dual_cost([(w, f_grid)], alpha, q, j, D)


def water_level_cost(lams, w, alpha, q, j, D):
    """Closed form of Lemma 24 / Corollary 27: delta = min(lambda, theta) with
    q * sum w min(lambda, theta) = D, for every alpha. Returns alpha*rbar + (1-alpha)*lbar in bits."""
    lams = np.concatenate([np.asarray(l, float) for l in lams])
    w = np.concatenate([np.asarray(x, float) for x in w])
    lo, hi = np.log(lams.min()) - 40, np.log(lams.max())
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if q * np.sum(w * np.minimum(lams, np.exp(mid))) > D:
            hi = mid
        else:
            lo = mid
    d = np.minimum(lams, np.exp(0.5 * (lo + hi)))
    r = np.sum(w * 0.5 * np.log(lams / d))
    l = np.sum(w * 0.5 * np.log((1 / d + j) / (1 / lams + j)))
    return (alpha * r + (1 - alpha) * l) / LN2


def window_cost(top, bulk, N, alpha, q, j, D):
    return dual_cost([(np.full(top.shape, 1.0 / N), top), (np.full(bulk.shape, 1.0 / N), bulk)],
                     alpha, q, j, D)


def feasible_spectra(G, rng, samples=2000):
    """The reduction to the separable program rests on one fact: if 0 < Delta <= G then
    the sorted eigenvalues of Delta are at most those of G (and the cost of Delta depends
    only on its eigenvalues). Sample feasible Delta = G^{1/2} X G^{1/2}, 0 < X <= I, and
    return the largest violation of delta_[k] <= lambda_[k] (should be <= 0 up to rounding)."""
    w, V = np.linalg.eigh(G)
    Gh = V @ np.diag(np.sqrt(w)) @ V.T
    lam = np.sort(w)[::-1]
    worst = -np.inf
    for _ in range(samples):
        Z = rng.standard_normal(G.shape)
        U, _ = np.linalg.qr(Z)
        X = U @ np.diag(rng.uniform(1e-6, 1.0, G.shape[0])) @ U.T
        d = np.sort(np.linalg.eigvalsh(Gh @ X @ Gh))[::-1]
        worst = max(worst, np.max((d - lam) / lam))
    return worst


CASES = {
    "AR1_rho1.5": [1.5],
    "AR2_rho1.3_0.5": [1.3, 0.5],
    "AR2_rho1.2_-1.4": [1.2, -1.4],
    "AR2_complex_1.15": [1.15 * np.exp(0.7j), 1.15 * np.exp(-0.7j)],
}


OUT = {}


def main(path=None):
    OUT.clear()
    out = OUT
    out.update({"cases": {}, "_meta": {}})
    t0 = time.time()
    s2, q, su2 = 1.0, 1.0, 0.5
    wgrid = (np.arange(20000) + 0.5) / 20000 * 2 * np.pi - np.pi
    fails = 0
    for name, poles in CASES.items():
        a = ar_coeffs(poles)
        p = len(a)
        aw2 = np.abs(a_on_circle(a, wgrid)) ** 2
        m_a, M_a = aw2.min(), aw2.max()
        f = s2 / aw2
        rbar = sum(np.log2(abs(r)) for r in poles if abs(r) > 1)
        m = sum(abs(r) > 1 for r in poles)
        rec = {"poles": [str(complex(r)) for r in poles], "rbar_bits": rbar, "m_unstable": int(m),
               "bulk_interval": [s2 / M_a, s2 / m_a], "rows": []}
        Dmax = q * f.mean()
        for N in (40, 80, 160, 320):
            top, bounded, mu, L = spectrum(a, s2, N, m)
            lo, hi = s2 / M_a, s2 / m_a
            # Lemma: the eigenvalues of A^T A with index > p lie in [m_a, M_a], all lie
            # below M_a, and the m smallest vanish exponentially
            bulk = s2 / mu[p:]
            split_ok = bool(mu[p:].min() >= m_a * (1 - 1e-9) and mu.max() <= M_a * (1 + 1e-9))
            outlier = L / (2 * N * LN2)
            row = {"N": N, "eigen_split_ok": split_ok,
                   "smallest_m_of_AtA": [float(x) for x in mu[:m]],
                   "next_of_AtA": float(mu[m]) if m < N else None,
                   "outlier_logsum_over_2N": outlier, "outlier_err": outlier - rbar,
                   "bulk_mean_log_err": float(np.sum(np.log(bulk)) / (N - p) - np.mean(np.log(f))),
                   "bulk_mean_inv_err": float(np.sum(1 / bulk) / (N - p) - np.mean(1 / f))}
            costs = {}
            for h in (1.0, 0.0):
                j = h * h / su2
                for alpha in (0.0, 0.5, 1.0):
                    for frac in (0.2, 0.6):
                        D = frac * Dmax
                        VN = window_cost(top, bounded, N, alpha, q, j, D)
                        Vf = spectral_cost(f, alpha, q, j, D)
                        pred = alpha * rbar + (1 - alpha) * rbar * (h == 0) + Vf
                        costs[f"h{h:g}_a{alpha:g}_D{frac:g}"] = {"VN": VN, "pred": pred, "gap": VN - pred}
            row["costs"] = costs
            rec["rows"].append(row)
        # convergence verdicts. The errors are O(1/N) in theory (a fixed number of
        # eigenvalues out of N), so the criterion is that N times the error stays bounded:
        # N*|err| at N = 320 is at most twice N*|err| at N = 40, or the error is below 1e-6.
        last = rec["rows"][-1]
        first = rec["rows"][0]

        def rate_ok(e_last, e_first):
            return abs(e_last) < 1e-6 or 320 * abs(e_last) <= 2 * 40 * abs(e_first) + 1e-9

        gap_last = max(abs(c["gap"]) for c in last["costs"].values())
        gap_first = max(abs(c["gap"]) for c in first["costs"].values())
        verdict = {
            "eigen_split": all(r["eigen_split_ok"] for r in rec["rows"]),
            "exploding_count": all((m == 0 or (max(r["smallest_m_of_AtA"]) < 1e-3 * r["next_of_AtA"]))
                                   for r in rec["rows"][1:]),
            "outlier_logsum": rate_ok(last["outlier_err"], first["outlier_err"]),
            "bulk_law": rate_ok(last["bulk_mean_log_err"], first["bulk_mean_log_err"])
            and rate_ok(last["bulk_mean_inv_err"], first["bulk_mean_inv_err"]),
            "cost_limit": rate_ok(gap_last, gap_first),
        }
        verdict = {k: bool(v) for k, v in verdict.items()}
        rec["N_times_err_last"] = {"outlier": 320 * last["outlier_err"], "cost_gap": 320 * gap_last}
        rec["verdict"] = verdict
        fails += sum(not v for v in verdict.values())
        out["cases"][name] = rec
        print(name, verdict, "last-row max cost gap %.4f" % max(abs(c["gap"]) for c in last["costs"].values()),
              flush=True)

    # 5. the fact behind the separable program: feasible spectra are dominated
    rng = np.random.default_rng(20261116)
    sep = []
    for name in ("AR1_rho1.5", "AR2_rho1.3_0.5", "AR2_complex_1.15"):
        a = ar_coeffs(CASES[name])
        A = matrices(a, 8)
        Ainv = np.linalg.solve(A, np.eye(8))
        G = s2 * Ainv @ Ainv.T
        sep.append({"case": name, "N": 8, "worst_relative_violation": feasible_spectra(G, rng)})
    sep_ok = all(s["worst_relative_violation"] <= 1e-9 for s in sep)
    for s in sep:
        s["worst_relative_violation"] = float(s["worst_relative_violation"])
    out["feasible_spectra_dominated"] = {"rows": sep, "ok": bool(sep_ok)}
    fails += (not sep_ok)
    print("feasible_spectra_dominated", sep_ok, [s["worst_relative_violation"] for s in sep], flush=True)

    # 7. common optimizer (Lemma 24, Corollary 27): for every alpha the dual
    # optimum equals the cost of delta = min(lambda, theta), in the window and in
    # the spectral program
    co = []
    for name, poles in CASES.items():
        a = ar_coeffs(poles)
        m = sum(abs(r) > 1 for r in poles)
        f = s2 / np.abs(a_on_circle(a, wgrid)) ** 2
        Dmax = q * f.mean()
        N = 160
        top, bounded, _, _ = spectrum(a, s2, N, m)
        for h in (1.0, 0.0):
            j = h * h / su2
            for alpha in (0.0, 0.3, 0.7, 1.0):
                for frac in (0.2, 0.6):
                    D = frac * Dmax
                    Vw = window_cost(top, bounded, N, alpha, q, j, D)
                    Cw = water_level_cost([top, bounded], [np.full(m, 1 / N), np.full(N - m, 1 / N)],
                                          alpha, q, j, D)
                    Vs = spectral_cost(f, alpha, q, j, D)
                    Cs = water_level_cost([f], [np.full(f.shape, 1 / len(f))], alpha, q, j, D)
                    co.append({"case": name, "h": h, "alpha": alpha, "D_frac": frac,
                               "window_dual": Vw, "window_closed": Cw, "spectral_dual": Vs,
                               "spectral_closed": Cs, "diff": max(abs(Vw - Cw), abs(Vs - Cs))})
    co_ok = max(c["diff"] for c in co) < 1e-6
    out["common_optimizer"] = {"rows": co, "max_diff": max(c["diff"] for c in co), "ok": bool(co_ok)}
    fails += (not co_ok)
    print("common_optimizer", co_ok, "max diff %.2e" % max(c["diff"] for c in co), flush=True)

    # 6. the det identity for the exploding log-sum, against high precision
    mpc = [mp_check(CASES[name], s2, 60, 80) for name in ("AR2_rho1.2_-1.4", "AR2_rho1.3_0.5")]
    mp_ok = all(c["rel_diff"] < 1e-8 for c in mpc)
    out["mp_check"] = {"rows": mpc, "ok": bool(mp_ok)}
    fails += (not mp_ok)
    print("mp_check", mp_ok, [c["rel_diff"] for c in mpc], flush=True)

    out["_meta"] = {"failed": int(fails), "seconds": round(time.time() - t0, 1),
                    "numpy": np.__version__}
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_unstable.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print("FAILED CHECKS:", fails)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
