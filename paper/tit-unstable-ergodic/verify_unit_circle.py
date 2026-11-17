"""Numerical checks for scalar autoregressive sources with poles on the unit circle
(paper-four draft, Theorem 11 and Lemma 12): the region of [part3, Theorem 26] without its assumption that no pole
lies on the circle.

Source T_t = sum_i phi_i T_{t-i} + xi_t, T_t = 0 for t <= 0, xi ~ N(0, 1); holder
S_t = H T_t + U_t, U ~ N(0, 1); weight Q = 1. phi(z) = 1 - sum_i phi_i z^i.
f(w) = 1 / |phi(e^{iw})|^2 is unbounded when phi has a zero on the circle, and
int f = infinity, so D_max = infinity.
Cases:
  U1  phi = 1 - z (random walk), H = 1;   U1b the same with H = 0 (no holder);
  U2  phi = (1 - z)(1 - 0.5 z), H = 1;    U3  phi = 1 + z^2 (poles +-i), H = 1;
  U4  phi = (1 - z)(1 - 1.5 z), H = 1 (a unit pole and an unstable pole 1.5);
  U5  phi = (1 - z)^2 (a double unit pole), H = 1.
The covariance Gamma_N has precision A_N^T A_N (A_N lower triangular Toeplitz of phi),
with eigenvalues s_1 <= ... <= s_N and sum_k ln s_k = 0. In U4 the smallest is about
1.5^{-2N} and is not resolved in double precision; its logarithm is taken from that
identity, and its component is costed with 1/lambda = 0 (its error lies far below
anything that is printed). Every other eigenvalue is at least c N^{-4} (see
smallest_toeplitz) and is resolved.
Window quantities (Lemma 24 of [part3]: the allocation min{lambda_k, theta_N} with
(1/N) sum_k min{lambda_k, theta_N} = D minimizes every weighted cost):
  r_N = (1/N) sum_k (1/2) log2^+(lambda_k / theta_N),
  l_N = (1/N) sum_{lambda_k > theta_N} (1/2) log2((1/theta_N + J)/(1/lambda_k + J)), J = H^2.
Predicted limits: (rho* + r_f(D), rho* 1{H = 0} + l_f(D)), with r_f and l_f the same
integrals over the law of f(w), w uniform, computed on 2^22 midpoints.
Checks and pass criteria, written before the first run (2026-11-16); N in
{200, 400, 800, 1600, 3200}:
  window: for D in {0.5, 2}, |gap_r(3200)| <= max(|gap_r(200)| / 4, 1e-4) and the same for
    the leakage, where gap = window value minus predicted limit.
  bulk_logmean: e_N = (1/N) sum_{k > d} ln lambda_k - int ln f (d the order, k counted from
    the largest lambda); |e_3200| <= max(|e_200| / 4, 1e-4). (This is what makes log^+ of
    the eigenvalues uniformly integrable.)
  exceptional: (1/2N) sum_{k <= d} log2 lambda_k -> rho*; |err(3200)| <= max(|err(200)| / 4, 1e-4).
  smallest_toeplitz: with r the largest multiplicity of a zero of phi on the circle,
    N^{2r} times the smallest eigenvalue of T_N(|phi|^2) at N = 3200 is at least half its
    value at N = 200.

Usage: python verify_unit_circle.py [out.json]

Record of the first run (2026-11-16, local Windows machine, python 3.12.2, numpy 2.5.2,
261 s): verify_unit_circle.json, all 30 checks passed. After that run only this docstring
changed (this record, and the theorem numbers in its first lines).
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = np.log(2.0)
WGRID = 2 ** 22


def poly_mul(a, b):
    return list(np.convolve(a, b))


CASES = {
    # coefficients of phi(z) in increasing powers, H, multiplicity of the zero on the circle
    "U1_random_walk": ([1.0, -1.0], 1.0, 1),
    "U1b_random_walk_no_holder": ([1.0, -1.0], 0.0, 1),
    "U2_unit_and_stable": (poly_mul([1.0, -1.0], [1.0, -0.5]), 1.0, 1),
    "U3_poles_plus_minus_i": ([1.0, 0.0, 1.0], 1.0, 1),
    "U4_unit_and_unstable": (poly_mul([1.0, -1.0], [1.0, -1.5]), 1.0, 1),
    "U5_double_unit_pole": (poly_mul([1.0, -1.0], [1.0, -1.0]), 1.0, 2),
}


def rho_star_bits(c):
    # poles are reciprocals of the zeros of phi; unstable poles <-> zeros inside the disk
    zeros = np.roots(c[::-1])
    return float(sum(-np.log2(abs(z)) for z in zeros if abs(z) < 1 - 1e-9)), \
        int(sum(abs(z) < 1 - 1e-9 for z in zeros))


def precision_eigs(c, N):
    A = np.zeros((N, N))
    for i, ci in enumerate(c):
        A += ci * np.eye(N, k=-i)
    return np.linalg.eigvalsh(A.T @ A)


def toeplitz_min(c, N):
    d = len(c) - 1
    Cf = np.zeros((N + d, N))
    for i, ci in enumerate(c):
        Cf += ci * np.eye(N + d, N, k=-i)
    return float(np.linalg.eigvalsh(Cf.T @ Cf)[0])


def spectral_law(c):
    w = 2 * np.pi * (np.arange(WGRID) + 0.5) / WGRID
    z = np.exp(1j * w)
    phi = sum(ci * z ** i for i, ci in enumerate(c))
    return 1.0 / np.abs(phi) ** 2


def theta_for(vals, D, weights=None, extra=0):
    """Solve mean(min(vals, theta)) + extra * theta / len = D by bisection (extra counts
    components with infinite variance, weight 1/N each)."""
    n = len(vals) + extra

    def g(th):
        return (np.minimum(vals, th).sum() + extra * th) / n
    lo, hi = 0.0, 1.0
    while g(hi) < D:
        hi *= 2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if g(mid) < D:
            lo = mid
        else:
            hi = mid
    return hi


def window_values(c, H, N, D):
    J = H * H
    s = precision_eigs(c, N)
    _, du = rho_star_bits(c)
    if du:
        exc_lnsum = -np.log(s[du:]).sum()          # sum of ln s over the unresolved ones
        s_res = s[du:]
    else:
        exc_lnsum, s_res = 0.0, s
    lam = 1.0 / s_res                               # resolved eigenvalues of Gamma_N
    th = theta_for(lam, D, extra=du)
    big = lam > th
    r = 0.5 * np.log2(lam[big] / th).sum()
    l_terms = (0.5 * np.log2((1 / th + J) / (1 / lam[big] + J))).sum() if J > 0 else r
    if du:
        # unresolved components: ln lambda = -ln s; each has lambda >> theta
        r += 0.5 * (-exc_lnsum) / LN2 - 0.5 * du * np.log2(th)
        l_terms += (0.5 * du * np.log2(1 + 1 / (J * th))) if J > 0 else (0.5 * (-exc_lnsum) / LN2
                                                                           - 0.5 * du * np.log2(th))
    order = len(c) - 1
    # the d largest eigenvalues: the du unresolved ones (ln lambda summed via the identity)
    # and the largest resolved ones
    top_res = np.sort(np.log(lam))[::-1][:order - du]
    top_ln_sum = (-exc_lnsum if du else 0.0) + top_res.sum()
    bulk = np.sort(np.log(lam))[::-1][order - du:]
    return {"r": r / N, "l": l_terms / N, "theta": th,
            "bulk_logmean": float(bulk.sum() / N), "exceptional_bits": float(top_ln_sum / (2 * N) / LN2)}


def predicted(c, H, D):
    J = H * H
    f = spectral_law(c)
    th = theta_for(f, D)
    big = f > th
    r = 0.5 * np.log2(f[big] / th).sum() / len(f)
    l = (0.5 * np.log2((1 / th + J) / (1 / f[big] + J))).sum() / len(f) if J > 0 else r
    return r, l, float(np.log(f).mean())


def main(path=None):
    t0 = time.time()
    Ns = [200, 400, 800, 1600, 3200]
    Ds = [0.5, 2.0]
    out, fails = {}, 0
    for name, (c, H, mult) in CASES.items():
        rs, du = rho_star_bits(c)
        rec = {"phi": c, "H": H, "rho_star_bits": rs, "n_unstable": du, "D": {}}
        checks = {}
        int_lnf = None
        for D in Ds:
            rf, lf, int_lnf = predicted(c, H, D)
            pr = (rs + rf, (rs if H == 0 else 0.0) + lf)
            rows = {N: window_values(c, H, N, D) for N in Ns}
            gr = {N: rows[N]["r"] - pr[0] for N in Ns}
            gl = {N: rows[N]["l"] - pr[1] for N in Ns}
            okr = abs(gr[3200]) <= max(abs(gr[200]) / 4, 1e-4)
            okl = abs(gl[3200]) <= max(abs(gl[200]) / 4, 1e-4)
            checks[f"window_D{D}"] = bool(okr and okl)
            rec["D"][str(D)] = {"pred_rate": pr[0], "pred_leak": pr[1], "r_f": rf, "l_f": lf,
                                "rows": {str(N): rows[N] for N in Ns},
                                "gap_rate": {str(N): gr[N] for N in Ns}, "gap_leak": {str(N): gl[N] for N in Ns}}
            print(f"{name:26s} D={D} pred ({pr[0]:.5f}, {pr[1]:.5f}) gaps rate "
                  f"{[f'{gr[N]:+.1e}' for N in Ns]} leak {[f'{gl[N]:+.1e}' for N in Ns]}", flush=True)
        rows = rec["D"][str(Ds[0])]["rows"]
        eb = {N: rows[str(N)]["bulk_logmean"] - int_lnf for N in Ns}
        ee = {N: rows[str(N)]["exceptional_bits"] - rs for N in Ns}
        checks["bulk_logmean"] = bool(abs(eb[3200]) <= max(abs(eb[200]) / 4, 1e-4))
        checks["exceptional"] = bool(abs(ee[3200]) <= max(abs(ee[200]) / 4, 1e-4))
        tm = {N: toeplitz_min(c, N) * N ** (2 * mult) for N in (200, 3200)}
        checks["smallest_toeplitz"] = bool(tm[3200] >= 0.5 * tm[200])
        rec.update({"int_ln_f": int_lnf, "bulk_logmean_err": {str(N): eb[N] for N in Ns},
                    "exceptional_err": {str(N): ee[N] for N in Ns},
                    "N2r_times_smallest_toeplitz": {str(N): v for N, v in tm.items()}, "checks": checks})
        fails += sum(not v for v in checks.values())
        out[name] = rec
        print(f"{name:26s} rho*={rs:.4f} bulk err {[f'{eb[N]:+.1e}' for N in Ns]} exc err "
              f"{[f'{ee[N]:+.1e}' for N in Ns]} N^2r s_min {tm} | {checks}", flush=True)
    out["_meta"] = {"failed": int(fails), "seconds": round(time.time() - t0, 1), "numpy": np.__version__}
    if path is None:
        path = os.path.join(HERE, "verify_unit_circle.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print("FAILED CHECKS:", fails)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
