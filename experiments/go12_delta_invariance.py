#!/usr/bin/env python
"""GO-P-2026-065 harness: the noncausal Delta-invariance control (GO-12).

Claim under test: the staleness tax is an ACCESS-WIDTH phenomenon, not a
delay phenomenon.

  s1  PATH ACCESS, circulant embedding: Sigma_{Y|S} is EXACTLY
      Delta-invariant (cyclic shift commutes with circulant
      covariances) -- the analytic-zero control, two instances,
      Delta in {1, 4, 16} vs 0.
  s2  PATH ACCESS, finite Toeplitz window: the per-symbol information
      functional M_n = (1/n) I(Y^n; S^n) deviates from Delta=0 only
      through edge terms O(Delta/n): small at n=128 and halving at
      n=256.
  s3  SLICE ACCESS, both encoder scopes (verifier-corrected pairing):
      (B) single-letter records from (Y_t, V_t) -- GO-8's situation --
      pay the static quadratic at rho UNCHANGED, s -> s/a^{2 Delta}
      (tau2_eff = (tau2 + 1 - a^{2 Delta})/a^{2 Delta});
      (A) records granted the context-epoch latent V_{t +/- Delta}
      (path-encoder benchmark, by pair sufficiency) pay the static
      quadratic at rho_eff = rho a^Delta, tau2 unchanged.
      Each is checked against its own direct multi-start channel
      program; L_B >= L_A always with a strict gap at the probe point
      (encoder access width matters too); both strictly increasing in
      Delta with the common limit 1/2 log2(1/D).
  s4  ORDERING: per-symbol path information exceeds slice information
      (more context can only help the eraser).

Model: V_t AR(1) pole a, Var 1; Y_t = rho V_t + N_t, Var 1;
S_t = V_{t-Delta} + U_t, Var U = tau2. Single governed run.
Sentinel ===GO12DI-JSON===; summary flag GO12DI_supported.
"""
import argparse
import json
import math
import sys
import time

import numpy as np
from scipy.linalg import cholesky, solve
from scipy.optimize import minimize

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a = ap.parse_args()
SEED = a.seed if a.seed is not None else (20260914 if a.pilot else 20260915)
rng = np.random.default_rng(SEED)

verdicts = {}
vals = {}


def ar1_circ_cov(n, aa):
    k = np.arange(n)
    S = 1.0 / np.abs(1 - aa * np.exp(-2j * np.pi * k / n)) ** 2
    c = np.real(np.fft.ifft(S))
    C = c[(k[:, None] - k[None, :]) % n]
    return C / C[0, 0]


# s1: circulant exact invariance
worst_s1 = 0.0
for (aa, rho, tau2, n) in [(0.8, 0.7, 0.4, 96), (0.55, 0.45, 1.1, 128)]:
    CV = ar1_circ_cov(n, aa)
    CY = rho ** 2 * CV + (1 - rho ** 2) * np.eye(n)
    CS = CV + tau2 * np.eye(n)

    def cc(Delta):
        P = np.roll(np.eye(n), Delta, axis=1)
        CYS = rho * CV @ P
        return CY - CYS @ solve(CS, CYS.T, assume_a="pos")

    ref = cc(0)
    for Delta in (1, 4, 16):
        worst_s1 = max(worst_s1, float(np.max(np.abs(cc(Delta) - ref))))
vals["s1_max_dev"] = worst_s1
verdicts["s1_circ_invariance"] = bool(worst_s1 <= 1e-12)


# s2: finite-window edge leakage
def M_n(n, aa, rho, tau2, Delta):
    k = np.arange(n)
    CV = aa ** np.abs(k[:, None] - k[None, :])
    CY = rho ** 2 * CV + (1 - rho ** 2) * np.eye(n)
    CYS = rho * aa ** np.abs(k[:, None] - k[None, :] + Delta)
    CS = CV + tau2 * np.eye(n)
    Cc = CY - CYS @ solve(CS, CYS.T, assume_a="pos")
    return (np.linalg.slogdet(CY)[1]
            - np.linalg.slogdet(Cc)[1]) / (2 * math.log(2) * n)


aa, rho, tau2, D = 0.8, 0.7, 0.4, 0.3
d128 = abs(M_n(128, aa, rho, tau2, 8) - M_n(128, aa, rho, tau2, 0))
d256 = abs(M_n(256, aa, rho, tau2, 8) - M_n(256, aa, rho, tau2, 0))
vals["s2_leak_128"] = d128
vals["s2_leak_256"] = d256
vals["s2_ratio"] = d256 / d128
verdicts["s2_edge_leakage"] = bool(d128 <= 0.05
                                   and 0.35 <= d256 / d128 <= 0.65)


# s3: slice access static tax
def gstar(rho2, tau2v, Dv):
    s = 1 + tau2v
    A, B, C = Dv * s, -(Dv + s - rho2), (1 - rho2)
    return (-B + math.sqrt(B * B - 4 * A * C)) / (2 * A)


def direct_L_pair(SigT, cvec, varS, Dv, starts=40):
    """min I(T;Yhat|S) over scalar records Yhat = u'T + noise, MSE(Y)<=Dv.
    T 2-dim with covariance SigT (read = first coordinate);
    cvec = Cov(T, S), varS = Var S."""
    SigTcS = SigT - np.outer(cvec, cvec) / varS
    Cw = cholesky(SigT, lower=True)
    Wm = solve(Cw, solve(Cw, SigTcS).T).T
    lam, Q = np.linalg.eigh((Wm + Wm.T) / 2)
    y0 = (Q.T @ Cw.T[:, 0])

    def obj(p):
        u, nv = p[:2], math.exp(min(p[2], 20))
        return math.log((float(u @ (lam * u)) + nv) / nv)

    def con(p):
        u, nv = p[:2], math.exp(min(p[2], 20))
        return Dv - (float((y0 - u) @ (y0 - u)) + nv)

    best = None
    for _ in range(starts):
        p0 = np.concatenate([y0 * rng.uniform(0.3, 0.95),
                             [math.log(rng.uniform(1e-3, 0.5))]])
        r = minimize(obj, p0, constraints=[{"type": "ineq", "fun": con}],
                     method="SLSQP",
                     options={"maxiter": 2000, "ftol": 1e-14})
        if r.success and (best is None or r.fun < best):
            best = r.fun
    return None if best is None else best / (2 * math.log(2))


worst_A, worst_B, mono_all, lim_dev = 0.0, 0.0, True, 0.0
order_ok, probe_gap = True, 0.0
for (aa2, rho2c, tau2c, Dc) in [(0.8, 0.7, 0.4, 0.3),
                                (0.55, 0.45, 1.1, 0.35)]:
    LA, LB = [], []
    for Delta in (0, 1, 2, 4, 8):
        ad = aa2 ** Delta
        # (A) context-epoch latent: T = (Y_t, V_{t+/-Delta})
        re = rho2c * ad
        LqA = 0.5 * math.log2(gstar(re * re, tau2c, Dc))
        SigA = np.array([[1.0, re], [re, 1.0]])
        LdA = direct_L_pair(SigA, np.array([re, 1.0]), 1 + tau2c, Dc)
        # (B) single-letter records: T = (Y_t, V_t), S reads a^D V_t
        t2B = (tau2c + 1 - ad * ad) / (ad * ad) if ad > 1e-12 else None
        LqB = (0.5 * math.log2(gstar(rho2c * rho2c, t2B, Dc))
               if t2B is not None else 0.5 * math.log2(1 / Dc))
        SigB = np.array([[1.0, rho2c], [rho2c, 1.0]])
        LdB = direct_L_pair(SigB, np.array([rho2c * ad, ad]),
                            1 + tau2c, Dc)
        if LdA is None or LdB is None:
            worst_A = worst_B = 1.0
            continue
        worst_A = max(worst_A, abs(LqA - LdA))
        worst_B = max(worst_B, abs(LqB - LdB))
        order_ok &= LqB >= LqA - 1e-12
        LA.append(LqA)
        LB.append(LqB)
    mono_all &= all(LA[i] < LA[i + 1] for i in range(len(LA) - 1))
    mono_all &= all(LB[i] < LB[i + 1] for i in range(len(LB) - 1))
    lim_dev = max(lim_dev, abs(0.5 * math.log2(gstar(1e-18, tau2c, Dc))
                               - 0.5 * math.log2(1 / Dc)))
# strict encoder-access gap at the verifier's max-gap probe point
pg_a, pg_r, pg_t, pg_D, pg_Del = 0.9, 0.95, 0.25, 0.25, 1
ad = pg_a ** pg_Del
probe_gap = (0.5 * math.log2(gstar(
    pg_r ** 2, (pg_t + 1 - ad * ad) / (ad * ad), pg_D))
    - 0.5 * math.log2(gstar((pg_r * ad) ** 2, pg_t, pg_D)))
vals["s3_gap_A"] = worst_A
vals["s3_gap_B"] = worst_B
vals["s3_monotone"] = bool(mono_all)
vals["s3_limit_dev"] = lim_dev
vals["s3_probe_gap_BA"] = probe_gap
verdicts["s3_slice_tax"] = bool(worst_A <= 1e-6 and worst_B <= 1e-6
                                and mono_all and order_ok
                                and lim_dev <= 1e-9
                                and probe_gap >= 0.01)

# s4: path >= slice information, with margin
Mpath = M_n(256, aa, rho, tau2, 4)
re = rho * aa ** 4
Islice = -0.5 * math.log2(1 - re * re / (1 + tau2))
vals["s4_path"] = Mpath
vals["s4_slice"] = Islice
verdicts["s4_ordering"] = bool(Mpath - Islice >= 0.05)

allpass = all(verdicts.values())
out = dict(seed=SEED, pilot=bool(a.pilot),
           runtime_s=round(time.time() - t0, 1),
           values={k: (float(v) if isinstance(v, (int, float, np.floating))
                       else v) for k, v in vals.items()},
           verdicts=verdicts, GO12DI_supported=bool(allpass))
print("===GO12DI-JSON===")
print(json.dumps(out, indent=1))
print("===END===")
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")
sys.exit(0 if allpass else 1)
