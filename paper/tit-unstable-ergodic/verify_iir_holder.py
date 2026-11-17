"""Numerical checks for unstable vector autoregressive sources observed through a filter
with an infinite impulse response (Theorem 10 of the draft: the extension of Theorem 1 to stable rational holder
filters, paper-four draft).

Source T_t = sum_k A_k T_{t-k} + xi_t, T_t = 0 for t <= 0, xi ~ N(0, Sig); holder
S_t = sum_{j >= 0} H_j T_{t-j} + U_t with a stable rational transfer function
G(z) = sum_j H_j z^j = Dg + Cg z (I - z F)^{-1} Bg (spectral radius of F below one),
U ~ N(0, s2u I), s2u = 1; weight Q = I. Within a window the holder's observations are
exact: T_t = 0 for t <= 0, so S_t involves only H_0, ..., H_{t-1}.

The joint state chi_t = (x_t, w_t), with x_t = (T_t, ..., T_{t-p+1}) the companion state and
w_t the filter state (w_{t+1} = F w_t + Bg T_t, w_1 = 0), follows
  chi_{t+1} = [[A, 0], [Bg E^T, F]] chi_t + [E; 0] xi_{t+1},  S_t = [Dg E^T, Cg] chi_t + U_t.
rho_hid is the sum of log|lambda| over the unstable eigenvalues of the joint matrix
restricted to its unobservable subspace. A pole rho with eigenvector v (of the
polynomial Phi) is hidden when G(1/rho) v = 0.

Cases (n = dimension, p = order):
  A1 scalar pole 1.5, G = (1 - 1.5 z) / (1 - 0.5 z): the filter's zero cancels the pole.
  A2 scalar pole 1.5, G = 1 / (1 - 0.5 z): the pole is visible.
  A3 A = diag(1.5, 0.5), G = (Ha + z Hb) / (1 - 0.625 z), Ha = (1, 1), Hb = (-1.5, 0.25):
     G(2/3) e1 = 0, the unstable mode is hidden.
  A4 as A3 with Hb = (-1, 0.25): visible.
  A5 A = [[1, -0.75], [0.75, 1]] (poles 1 +- 0.75 i, modulus 1.25),
     G = (1, 0) / (1 - 0.5 z + 0.25 z^2): visible.
  A6 as A5 with G = (1, 0) (1 - 2 z + 1.5625 z^2) / (1 - 0.5 z + 0.25 z^2); the numerator is
     det(I - z A), whose zeros 1/rho, 1/conj(rho) hide both poles.
  All coefficients are dyadic, so the hidden modes are hidden exactly in binary (a mode
  hidden only to rounding error becomes visible as it grows; see C6 of
  verify_unstable_vector.py). This choice was made before the first run.
Checks and pass criteria, written before the first run (2026-11-16):
  innovations (Lemma 4 with the joint realization):
    |ln det R_400 - [int ln det(s2u I + G f G^*) + 2 (rho* - rho_hid)]| <= 1e-9 (nats),
    the integral on 4096 points.
  prior_growth, posterior_growth (Lemma 5(a), (b)): (1/2N) ln det Cov(x_N) -> rho* and
    (1/2N) ln det Cov(x_N | S^N) -> rho_hid, with
    400 |err(400)| <= 2 max(50 |err(50)|, 100 |err(100)|) + 1e-6.
  posterior_floor (Lemma 5(c)): the smallest eigenvalue of Cov(x_N | S^N) is at least
    c = min{(1/m_f + Jbar)^{-1}, 1/M_f}, Jbar = (sum_j ||H_j||)^2 / s2u (sum to j = 4000),
    at N = 25, 50, 100, 200, 400.
  window_cost (the window-cost limit of the extended theorem): cases A1, A2, A3, A6 at
    alpha = 0, 0.5, 1, D = 0.3 Dmax^f, N = 40, 80, 160, 320. Pass: |gap(320)| <= |gap(40)| / 4
    at each alpha, and the cost changes by at most 1e-6 bits between the caps M = 1e5 and
    1e7 (the cap of the exploding part, as in verify_unstable_vector.py).
The posterior and Kalman computations use 320 digits (mpmath).

Usage: python verify_iir_holder.py [out.json]
"""
from __future__ import annotations

import json
import os
import sys
import time

import mpmath as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify_unstable_vector as vu  # noqa: E402  (sets the solver tolerances and mp.dps)

sc = vu.sc
LN2 = np.log(2.0)


def rational(b, a):
    """Direct-form realization of the scalar b(z)/a(z), a[0] = 1, in the delay variable z:
    returns (F, Bs, Cs, Ds) with g(z) = Ds + Cs z (I - z F)^{-1} Bs."""
    k = len(a) - 1
    b = list(b) + [0.0] * (k + 1 - len(b))
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    F = np.zeros((k, k))
    F[0, :] = -a[1:]
    if k > 1:
        F[1:, :-1] = np.eye(k - 1)
    Bs = np.zeros((k, 1))
    Bs[0, 0] = 1.0
    Cs = (b[1:] - b[0] * a[1:]).reshape(1, k)
    return F, Bs, Cs, np.array([[b[0]]])


def scalar_times_row(b, a, h):
    """Realization of the 1 x n transfer function (b(z)/a(z)) h."""
    F, Bs, Cs, Ds = rational(b, a)
    h = np.atleast_2d(h)
    return F, Bs @ h, Cs, Ds @ h


def cases():
    I2 = np.eye(2)
    cs = {}
    one = np.array([[1.0]])
    cs["A1_scalar_iir_hides"] = ([np.array([[1.5]])], one, rational([1.0, -1.5], [1.0, -0.5]))
    cs["A2_scalar_iir_sees"] = ([np.array([[1.5]])], one, rational([1.0, 0.0], [1.0, -0.5]))
    Ha = np.array([[1.0, 1.0]])
    for name, Hb in (("A3_diag_iir_hides", np.array([[-1.5, 0.25]])),
                     ("A4_diag_iir_sees", np.array([[-1.0, 0.25]]))):
        # G = Ha + z (Hb + 0.625 Ha) / (1 - 0.625 z) = (Ha + z Hb) / (1 - 0.625 z)
        cs[name] = ([np.diag([1.5, 0.5])], I2, (np.array([[0.625]]), Hb + 0.625 * Ha, np.array([[1.0]]), Ha))
    Rot = np.array([[1.0, -0.75], [0.75, 1.0]])
    den = [1.0, -0.5, 0.25]
    cs["A5_complex_iir_sees"] = ([Rot], I2, scalar_times_row([1.0, 0.0, 0.0], den, [1.0, 0.0]))
    cs["A6_complex_iir_hides"] = ([Rot], I2, scalar_times_row([1.0, -2.0, 1.5625], den, [1.0, 0.0]))
    return cs


def joint(As, real):
    F, Bg, Cg, Dg = real
    n, p = As[0].shape[0], len(As)
    Ac = vu.companion(As)
    E = np.zeros((n * p, n))
    E[:n, :] = np.eye(n)
    k = F.shape[0]
    Aj = np.zeros((n * p + k, n * p + k))
    Aj[:n * p, :n * p] = Ac
    Aj[n * p:, :n * p] = Bg @ E.T
    Aj[n * p:, n * p:] = F
    Cj = np.hstack([Dg @ E.T, Cg])
    Ej = np.vstack([E, np.zeros((k, n))])
    return Aj, Cj, Ej


def impulse(real, N):
    F, Bg, Cg, Dg = real
    Hs = [Dg]
    Fp = np.eye(F.shape[0])
    for _ in range(1, N):
        Hs.append(Cg @ Fp @ Bg)
        Fp = Fp @ F
    return Hs


def G_of(real, z):
    F, Bg, Cg, Dg = real
    return Dg + Cg @ (z * np.linalg.inv(np.eye(F.shape[0]) - z * F)) @ Bg


def growth_joint(As, Sig, real, s2u, Ns):
    """Prior and posterior ln det of x_N (the last p symbols) and innovation covariances,
    from the Kalman filter of the joint state, in 320-digit arithmetic."""
    n, p = As[0].shape[0], len(As)
    Aj, Cj, Ej = joint(As, real)
    A = vu.mpm(Aj)
    C = vu.mpm(Cj)
    Eh = vu.mpm(Ej)
    Q = Eh * vu.mpm(Sig) * Eh.T
    R = vu.mpm(s2u * np.eye(Cj.shape[0]))
    k0 = n * p
    P_prior = Q.copy()
    P_pred = Q.copy()
    out = []
    for t in range(1, max(Ns) + 1):
        Re = C * P_pred * C.T + R
        K = P_pred * C.T * mp.inverse(Re)
        P_filt = P_pred - K * C * P_pred
        P_filt = (P_filt + P_filt.T) / 2
        if t in Ns:
            Px = P_prior[0:k0, 0:k0]
            Pf = P_filt[0:k0, 0:k0]
            out.append({"N": t, "prior_logdet_over_2N": float(vu.mp_logdet(Px) / (2 * t)),
                        "post_logdet_over_2N": float(vu.mp_logdet(Pf) / (2 * t)),
                        "min_eig_post": float(min(mp.eigsy(Pf, eigvals_only=True))),
                        "ln_det_Re": float(vu.mp_logdet(Re))})
        P_prior = A * P_prior * A.T + Q
        P_pred = A * P_filt * A.T + Q
    return out


def f_at(As, Sig, z):
    n = As[0].shape[0]
    Phi = np.eye(n, dtype=complex) - sum(A * z ** (k + 1) for k, A in enumerate(As))
    Pi = np.linalg.inv(Phi)
    return Pi @ Sig @ Pi.conj().T


def bode_rhs(As, Sig, real, s2u, W=4096):
    tot = 0.0
    for k in range(W):
        z = np.exp(-1j * 2 * np.pi * (k + 0.5) / W)
        G = G_of(real, z)
        tot += np.log(np.linalg.det(s2u * np.eye(G.shape[0]) + G @ f_at(As, Sig, z) @ G.conj().T).real)
    return tot / W


def spectral_cost(As, Sig, real, s2u, alpha, D, W=512):
    blocks = []
    for k in range(W):
        z = np.exp(-1j * 2 * np.pi * (k + 0.5) / W)
        f = sc.herm(f_at(As, Sig, z))
        R = sc.psd_sqrt(f)
        G = G_of(real, z)
        blocks.append((sc.herm(R @ R), G @ R, s2u * np.eye(G.shape[0], dtype=complex)))
    return sc.solve(blocks, np.full(W, 1.0 / W), alpha, D)


def floor_constant(As, Sig, real, s2u, W=4096, jmax=4000):
    eig = np.array([np.linalg.eigvalsh(f_at(As, Sig, np.exp(1j * 2 * np.pi * (k + 0.5) / W)))
                    for k in range(W)])
    m_f, M_f = eig.min(), eig.max()
    Jn = sum(np.linalg.norm(H, 2) for H in impulse(real, jmax)) ** 2 / s2u
    return min(1.0 / (1.0 / m_f + Jn), 1.0 / M_f), float(Jn)


WINDOW = ["A1_scalar_iir_hides", "A2_scalar_iir_sees", "A3_diag_iir_hides", "A6_complex_iir_hides"]


def main(path=None):
    t0 = time.time()
    fails = 0
    allc = cases()
    Ns = [25, 50, 100, 200, 400]
    out = {"cases": {}, "window_cost": {}}
    for name, (As, Sig, real) in allc.items():
        Aj, Cj, _ = joint(As, real)
        rs = vu.rho_star(vu.companion(As))
        rs_joint = vu.rho_star(Aj)
        ru, dim_u = vu.unobservable_rho(Aj, Cj)
        g = growth_joint(As, Sig, real, 1.0, Ns)
        c_floor, Jbar = floor_constant(As, Sig, real, 1.0)
        rhs = bode_rhs(As, Sig, real, 1.0) + 2 * (rs - ru)
        pri_ok, pri_e = vu.growth_ok(g, "prior_logdet_over_2N", rs)
        post_ok, post_e = vu.growth_ok(g, "post_logdet_over_2N", ru)
        diff = g[-1]["ln_det_Re"] - rhs
        checks = {"innovations": abs(diff) <= 1e-9, "prior_growth": pri_ok, "posterior_growth": post_ok,
                  "posterior_floor": all(r["min_eig_post"] >= c_floor * (1 - 1e-9) for r in g)}
        fails += sum(not v for v in checks.values())
        out["cases"][name] = {"rho_star_bits": rs / LN2, "rho_star_joint_bits": rs_joint / LN2,
                              "rho_hid_bits": ru / LN2, "unobs_dim": dim_u, "Jbar": Jbar, "c_floor": c_floor,
                              "filter_poles": [str(complex(x)) for x in np.linalg.eigvals(real[0])],
                              "growth": g, "innovations": {"lnDetRe_400": g[-1]["ln_det_Re"], "rhs": rhs,
                                                           "diff": diff},
                              "prior_err": pri_e, "post_err": post_e,
                              "checks": {k: bool(v) for k, v in checks.items()}}
        print(f"{name:24s} rho*={rs / LN2:.4f} rho_hid={ru / LN2:.4f} bits | 400*err prior "
              f"{400 * pri_e[400]:+.3f} post {400 * post_e[400]:+.3f} | innov {diff:+.1e} | "
              f"{out['cases'][name]['checks']}", flush=True)

    WN = [40, 80, 160, 320]
    for name in WINDOW:
        As, Sig, real = allc[name]
        Aj, Cj, _ = joint(As, real)
        rs = vu.rho_star(vu.companion(As)) / LN2
        ru = vu.unobservable_rho(Aj, Cj)[0] / LN2
        g = growth_joint(As, Sig, real, 1.0, WN)
        post = {r["N"]: 2 * r["N"] * r["post_logdet_over_2N"] for r in g}
        Dmax = spectral_cost(As, Sig, real, 1.0, 1.0, 1e9)["D"]
        rows, ok = [], True
        for alpha in (0.0, 0.5, 1.0):
            D = 0.3 * Dmax
            Vf = spectral_cost(As, Sig, real, 1.0, alpha, D)["cost"]
            pred = alpha * rs + (1 - alpha) * ru + Vf
            gaps = {}
            for N in WN:
                wc = vu.window_cost(As, Sig, impulse(real, N), 1.0, N, alpha, D, [1e5, 1e7], post[N])
                cap = abs(wc[0]["cost"] - wc[1]["cost"])
                gaps[N] = wc[-1]["cost"] - pred
                rows.append({"alpha": alpha, "N": N, "pred": pred, "Vf": Vf, "window": wc,
                             "gap": gaps[N], "cap_change": cap})
                ok = ok and cap <= 1e-6
            ok = ok and abs(gaps[320]) <= abs(gaps[40]) / 4
            print(f"  window {name:22s} a={alpha:.1f} pred={pred:.4f} gaps "
                  f"{[f'{gaps[N]:+.5f}' for N in WN]}", flush=True)
        out["window_cost"][name] = {"rows": rows, "ok": bool(ok)}
        fails += not ok
    out["_meta"] = {"failed": int(fails), "seconds": round(time.time() - t0, 1), "numpy": np.__version__,
                    "mp_dps": mp.mp.dps}
    if path is None:
        path = os.path.join(HERE, "verify_iir_holder.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print("FAILED CHECKS:", fails)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
