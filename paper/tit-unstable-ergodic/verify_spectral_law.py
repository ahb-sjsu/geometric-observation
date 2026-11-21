"""Numerical checks for Theorem 13, Proposition 14 and Corollary 15 (sources with a
limiting eigenvalue distribution; sampled cyclostationary sources). Earlier drafts
numbered them Theorem 7, Proposition 8 and Corollary 9.

Source: X_c(t) = sigma(t) Z(t), sigma(t)^2 = 5 + (1/3) sin(2 pi t) (period T_c = 1, the
variance profile of the example in Tan, Dabora and Poor), Z stationary with the
triangular correlation kappa(lam) = max(0, 1 - |lam| / lam_c), which is positive
definite. Then c_c(t, lam) = sigma(t) sigma(t + lam) kappa(lam) is continuous, periodic
in t, and zero for |lam| > lam_c. Samples T_i = X_c(i T_s + phi), i = 1..N.
Holder S_i = H T_i + U_i, H = 1, U white with variance 1 (J = 1); weight Q = 1.

Checks (criteria fixed before the first run, except where marked below):
  phase_independence: T_s = 1/(3 + eps), eps = (sqrt 5 - 1)/2 (irrational). At four
    phases phi in {0, .25, .5, .75}, N in {500, 1000, 2000, 4000, 8000}, rate r_N and
    leakage l_N of Theorem 13's allocation (paper three, Lemma 24) at D = 0.2 Dmax and
    0.6 Dmax. Pass: the largest spread over phases at N = 8000 is below 1e-3 bits and
    at most a quarter of the spread at N = 500.
  moments: the first six moments of the eigenvalue distribution at N = 8000, phase 0,
    against the formula of Proposition 14, int g_k d(nu), computed on a grid of 4096
    phases. Pass: relative error below 1e-2 for k = 1..6.
  rational_contrast (recorded, no pass criterion): the same with eps = 1/2 (period 7
    samples); the theorem predicts that the phase can matter there. In the first run
    the spread decayed anyway: an orbit of 7 equally spaced phases averages the low
    harmonics of this sigma exactly. A second contrast, eps = 0 (period 3 samples),
    was added after seeing that run.
  strong_phase_independence (added 2026-11-20 after the R-IND-5 pass VI-26): with the weak
    modulation above, the rational runs also meet phase_independence's criteria, so that
    check cannot tell incommensurate from commensurate sampling. This check repeats it
    with sigma(t)^2 = 5 + 4 sin(2 pi t), the variance profile of the paper's own example
    (which samples at period 2; the control below samples at period 3), at
    eps = (sqrt 5 - 1)/2.
    Pass: spread at N = 8000 below 1e-3 bits and at most a quarter of the spread at N = 500.
  strong_rational_control (added with it): a power control for the comparison, not a
    statement of Corollary 15: the strong comparison at eps = 0 (period 3 samples), where
    the phase can matter. Pass: the control must NOT look phase-independent, i.e. its
    spread at N = 8000 is at least 1e-2 bits and at least half its spread at N = 500.
    Both criteria were set after the verifier's exploratory run of these two
    configurations (spreads 2.6e-3, 4.8e-4, 1.3e-4 at N = 500, 2000, 8000 for the
    irrational case; 0.0185, 0.0203, 0.0208 for period 3), disclosed in VI-26.
  rational_example_exact (added with them): the exact example after Corollary 15. Its
    predicted value is the paper's own derivation; but the first R-IND-5 verifier (VI-26)
    had already computed a similar configuration (triangular Z, length 2.5 samples) and
    reported agreement to 1e-14 before this check was written, so it is not a blind
    prediction. T_s = T_c/2, sigma(t)^2 = 5 + 4 sin(2 pi t), phases 0 (variances 5) and 1/4
    (variances 9 and 1). Z's sampled correlation is (1, 0.6, 0.2), with spectral density
    1 + 1.2 cos w + 0.4 cos 2w >= 0.15 (its minimum, at cos w = -0.75), so every eigenvalue
    is at least 0.15 * min sigma^2 = 0.15. At D = 0.1 every eigenvalue exceeds the water
    level D/Q, and the two rates differ by exactly (1/2) log2(5/3) bits for even N. Pass, at
    N = 1000 and 2000: every eigenvalue at least 0.15 and above the level, and
    |difference - (1/2) log2(5/3)| < 1e-9. Power: because
    log det(D Gamma D) = log det Gamma + sum log sigma^2, this tests the variances, the
    factor 1/2 and the eigenvalue floor, not anything about Z.

Note on Z: LAM_C_SAMPLES fixes Z's correlation length in samples of whichever step T_s is in
use, so the sampled correlation of Z is (1, 0.6, 0.2) in every check and only the samples of
sigma change between rates (Z's length in time is 0.691, 0.833 and 1.25 at the irrational,
period-3 and period-2 rates).

Usage: python verify_spectral_law.py [out.json]
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
from scipy.linalg import eigvals_banded

LN2 = np.log(2.0)
J = 1.0
Q = 1.0
LAM_C_SAMPLES = 2.5          # correlation length in units of T_s
OUT = {}


def sigma(t, amp=1.0 / 3.0):
    return np.sqrt(5.0 + amp * np.sin(2 * np.pi * t))


def kappa(lam, lam_c):
    return np.maximum(0.0, 1.0 - np.abs(lam) / lam_c)


def eigs(N, Ts, phi, amp=1.0 / 3.0):
    lam_c = LAM_C_SAMPLES * Ts
    m = int(np.floor(lam_c / Ts))
    t = np.arange(1, N + 1) * Ts + phi
    s = sigma(t, amp)
    ab = np.zeros((m + 1, N))          # lower banded form: ab[k, i] = A[i + k, i]
    for k in range(m + 1):
        ab[k, :N - k] = s[:N - k] * s[k:] * kappa(k * Ts, lam_c)
    return np.sort(eigvals_banded(ab, lower=True))


def allocation(lam, D):
    """Water level theta with Q mean(min(lam, theta)) = D; rate and leakage in bits."""
    lo, hi = 0.0, lam.max()
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if Q * np.mean(np.minimum(lam, mid)) > D:
            hi = mid
        else:
            lo = mid
    th = 0.5 * (lo + hi)
    big = lam > th
    r = np.sum(0.5 * np.log(lam[big] / th)) / len(lam) / LN2
    l = np.sum(0.5 * np.log((1 / th + J) / (1 / lam[big] + J))) / len(lam) / LN2
    return th, r, l


def g_moments(Ts, kmax, grid=4096):
    """int g_k d(nu): g_k(v) = (Gamma(v)^k)_{00} on a finite section centred at 0."""
    lam_c = LAM_C_SAMPLES * Ts
    m = int(np.floor(lam_c / Ts))
    w = kmax * m
    idx = np.arange(-w, w + 1)
    mom = np.zeros(kmax)
    for v in (np.arange(grid) + 0.5) / grid:
        t = idx * Ts + v
        s = sigma(t)
        G = np.outer(s, s) * kappa((idx[None, :] - idx[:, None]) * Ts, lam_c)
        P = np.eye(len(idx))
        for k in range(kmax):
            P = P @ G
            mom[k] += P[w, w]
    return mom / grid


def run(eps, Ns, phases, Dfracs, amp=1.0 / 3.0):
    Ts = 1.0 / (3.0 + eps)
    rows = []
    for N in Ns:
        for phi in phases:
            lam = eigs(N, Ts, phi, amp)
            dmax = Q * lam.mean()
            for fr in Dfracs:
                th, r, l = allocation(lam, fr * 5.0 * Q)   # D relative to the mean variance 5
                rows.append({"N": N, "phi": phi, "D_frac_of_5": fr, "theta": th, "rate": r,
                             "leak": l, "Dmax_N": dmax})
    spread = {}
    for N in Ns:
        sp = 0.0
        for fr in Dfracs:
            rs = [x["rate"] for x in rows if x["N"] == N and x["D_frac_of_5"] == fr]
            ls = [x["leak"] for x in rows if x["N"] == N and x["D_frac_of_5"] == fr]
            sp = max(sp, max(rs) - min(rs), max(ls) - min(ls))
        spread[N] = sp
    return rows, spread


def main(path=None):
    OUT.clear()
    t0 = time.time()
    fails = 0
    Ns = [500, 1000, 2000, 4000, 8000]
    phases = [0.0, 0.25, 0.5, 0.75]
    Dfracs = [0.2, 0.6]
    eps = (np.sqrt(5.0) - 1.0) / 2.0
    rows, spread = run(eps, Ns, phases, Dfracs)
    ok = spread[8000] < 1e-3 and spread[8000] <= spread[500] / 4
    OUT["phase_independence"] = {"eps": eps, "rows": rows, "spread_by_N": spread, "ok": bool(ok)}
    fails += not ok
    print("phase_independence", ok, {k: f"{v:.2e}" for k, v in spread.items()}, flush=True)
    last = [x for x in rows if x["N"] == 8000 and x["phi"] == 0.0]
    for x in last:
        print(f"  N=8000 D={x['D_frac_of_5']}*5: rate {x['rate']:.5f} leak {x['leak']:.5f} bits", flush=True)

    Ts = 1.0 / (3.0 + eps)
    lam = eigs(8000, Ts, 0.0)
    emp = np.array([np.mean(lam ** k) for k in range(1, 7)])
    th = g_moments(Ts, 6)
    rel = np.abs(emp - th) / np.abs(th)
    ok = bool(np.all(rel < 1e-2))
    OUT["moments"] = {"empirical_N8000": emp.tolist(), "formula": th.tolist(), "rel_err": rel.tolist(),
                      "ok": ok}
    fails += not ok
    print("moments", ok, [f"{x:.1e}" for x in rel], flush=True)

    rows_r, spread_r = run(0.5, Ns, phases, Dfracs)
    OUT["rational_contrast"] = {"eps": 0.5, "rows": rows_r, "spread_by_N": spread_r}
    print("rational_contrast (eps = 1/2)", {k: f"{v:.2e}" for k, v in spread_r.items()}, flush=True)
    rows_0, spread_0 = run(0.0, Ns, phases, Dfracs)
    OUT["rational_contrast_period3"] = {"eps": 0.0, "rows": rows_0, "spread_by_N": spread_0}
    print("rational_contrast (eps = 0)", {k: f"{v:.2e}" for k, v in spread_0.items()}, flush=True)

    # Strong modulation: a check with power to tell the two cases apart (VI-26).
    rows_s, spread_s = run(eps, Ns, phases, Dfracs, amp=4.0)
    ok = spread_s[8000] < 1e-3 and spread_s[8000] <= spread_s[500] / 4
    OUT["strong_phase_independence"] = {"eps": eps, "amp": 4.0, "rows": rows_s,
                                        "spread_by_N": spread_s, "ok": bool(ok)}
    fails += not ok
    print("strong_phase_independence", ok, {k: f"{v:.2e}" for k, v in spread_s.items()}, flush=True)
    rows_c, spread_c = run(0.0, Ns, phases, Dfracs, amp=4.0)
    ok = spread_c[8000] >= 1e-2 and spread_c[8000] >= spread_c[500] / 2
    OUT["strong_rational_control"] = {"eps": 0.0, "amp": 4.0, "rows": rows_c,
                                      "spread_by_N": spread_c, "ok": bool(ok)}
    fails += not ok
    print("strong_rational_control (must stay phase-dependent)", ok,
          {k: f"{v:.2e}" for k, v in spread_c.items()}, flush=True)

    # The paper's exact rational example, with its predicted value (VI-26 re-check).
    target = 0.5 * np.log2(5.0 / 3.0)
    exact = []
    for N in (1000, 2000):
        lam0, lam1 = eigs(N, 0.5, 0.0, 4.0), eigs(N, 0.5, 0.25, 4.0)
        th0, r0, _ = allocation(lam0, 0.1)
        th1, r1, _ = allocation(lam1, 0.1)
        above = bool(min(lam0.min(), lam1.min()) >= 0.15 and lam0.min() > th0 and lam1.min() > th1)
        exact.append({"N": N, "rate_phase0": r0, "rate_phase_quarter": r1, "difference": r0 - r1,
                      "target": target, "min_eig": float(min(lam0.min(), lam1.min())),
                      "theta": [th0, th1], "all_above_level": above})
    ok = all(x["all_above_level"] and abs(x["difference"] - target) < 1e-9 for x in exact)
    OUT["rational_example_exact"] = {"rows": exact, "ok": bool(ok)}
    fails += not ok
    print("rational_example_exact", ok,
          [f"N={x['N']}: {x['difference']:.14f} vs {target:.14f}" for x in exact], flush=True)

    OUT["_meta"] = {"failed": int(fails), "seconds": round(time.time() - t0, 1), "numpy": np.__version__}
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_spectral_law.json")
    with open(path, "w") as fh:
        json.dump(OUT, fh, indent=1)
    print("FAILED CHECKS:", fails)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
