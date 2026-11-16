"""Numerical checks for Section III (unstable vector autoregressive sources).

Source T_t = sum_k A_k T_{t-k} + xi_t, T_t = 0 for t <= 0, xi ~ N(0, Sig); holder
S_t = sum_j H_j T_{t-j} + U_t, U ~ N(0, s2u I) with s2u = 1; weight Q = I. In the code the
dimension is n and the order p (the paper writes p and d). Units: nats inside, bits in
the printed and recorded rho values and costs.

Checks and pass criteria. The criteria were written after exploratory runs of the same
computations on the same cases (2026-11-16), not before; the appendix says so.
  bridge (Lemma 2): Gamma_N^{-1} - T_N(f^{-1}) vanishes outside the last p blocks
    (<= 1e-12), has rank <= np there, and T_N(f^{-1}) is block Toeplitz (<= 1e-12). N = 12.
  stationary (the banded precision of a stationary window, used in Lemma 3; this was
    Lemma 3(a) of the draft when the run was made): T_N(f)^{-1} = T_N(f^{-1}) - E_N with
    E_N >= 0 (smallest eigenvalue >= -1e-8), supported on the first and last p blocks
    (<= 1e-8), of numerical rank <= 2np (tolerance 1e-8 times its norm). N = 16; T_N(f)
    from the Fourier coefficients of f on 16384 points.
  posterior_floor (Lemma 5(c)): the smallest eigenvalue of Cov(x_N | S^N) is at least
    c = min{(1/m_f + Jbar)^{-1}, 1/M_f}, Jbar = (sum_j ||H_j||)^2 / s2u, at
    N = 25, 50, 100, 200, 400.
  prior_growth (Lemma 5(a)) and posterior_growth (Lemma 5(b)): (1/2N) log det Cov(x_N)
    -> rho_star and (1/2N) log det Cov(x_N | S^N) -> rho_hid. Pass:
    400 |err(400)| <= 2 max(50 |err(50)|, 100 |err(100)|) + 1e-6, allowing O(log N / N).
  innovations (Lemma 4): |ln det R_400 - [int ln det(Sigma_U + G f G^*) + 2(rho* - rho_hid)]|
    <= 1e-9, the integral on 4096 points.
  window_cost (Theorem 1): sources C1, C2, C8 at alpha = 0, 0.5, 1, D = 0.3 Dmax,
    N = 40, 80, 160, 320. Pass: |gap(320)| <= |gap(40)| / 4 and the cost changes by at
    most 1e-6 between the caps M = 1e3 and 1e5 (see window_cost below).
Recorded without a criterion: C6 (a mode hidden only to about 6e-17, which the holder
eventually sees), and the window cost of C7 (holder with memory, outside Theorem 1).
The posterior and Kalman computations use 320 digits (mpmath).

Usage: python verify_unstable_vector.py [out.json]
       python verify_unstable_vector.py --caps     (follow-up, see cap_followup)

Record of the first run (2026-11-16, Atlas, numpy 2.4.4, 515 s): verify_unstable_vector.json,
FAILED CHECKS: 1, the cap criterion for C8 at N = 40 and 80 (changes up to 1.9e-6 bits).
Every other check passed. The follow-up, verify_unstable_vector_caps.json, shows the
costs change by at most 2e-8 bits between M = 1e5 and 1e7. After that run only this
docstring and the function cap_followup were changed.
"""
from __future__ import annotations

import os
import time

import json
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tit-stationary"))
import spectral_core as sc  # noqa: E402

LN2 = np.log(2.0)

mp.mp.dps = 320          # the covariances span more than 160 decimal orders at N = 400


def companion(As):
    p = len(As)
    n = As[0].shape[0]
    C = np.zeros((n * p, n * p))
    for k, A in enumerate(As):
        C[:n, k * n:(k + 1) * n] = A
    if p > 1:
        C[n:, :-n] = np.eye(n * (p - 1))
    return C


def output_map(Hs, n, p):
    m = len(Hs)
    assert m <= p
    r = Hs[0].shape[0]
    C = np.zeros((r, n * p))
    for j, H in enumerate(Hs):
        C[:, j * n:(j + 1) * n] = H
    return C


def rho_star(M):
    ev = np.linalg.eigvals(M)
    return float(sum(np.log(abs(x)) for x in ev if abs(x) > 1 + 1e-12))


def unobservable_rho(Acomp, C):
    d = Acomp.shape[0]
    O = np.vstack([C @ np.linalg.matrix_power(Acomp, k) for k in range(d)])
    u, s, vt = np.linalg.svd(O)
    tol = 1e-9 * max(1.0, s.max())
    null = vt[(s > tol).sum():].T if (s > tol).sum() < d else np.zeros((d, 0))
    if null.shape[1] == 0:
        return 0.0, 0
    Ar = null.T @ Acomp @ null
    return rho_star(Ar), null.shape[1]


def mpm(a):
    return mp.matrix([[mp.mpf(repr(float(x))) for x in row] for row in np.atleast_2d(a)])


def mp_logdet(M):
    return mp.log(mp.det(M))


def growth(As, Sig, Hs, s2u, Ns):
    """Prior and posterior ln det of the companion state x_N, and innovation covariances."""
    n = As[0].shape[0]
    p = len(As)
    A = mpm(companion(As))
    C = mpm(output_map(Hs, n, p))
    d = n * p
    B = mp.zeros(d, n)
    for i in range(n):
        B[i, i] = 1
    Q = B * mpm(Sig) * B.T
    R = mpm(s2u * np.eye(C.rows))
    P_prior = Q.copy()          # Cov(x_1)
    P_post_pred = Q.copy()      # Cov(x_1 | nothing)
    out = []
    Re_last = None
    for t in range(1, max(Ns) + 1):
        # update with S_t
        Re = C * P_post_pred * C.T + R
        K = P_post_pred * C.T * mp.inverse(Re)
        P_filt = P_post_pred - K * C * P_post_pred
        P_filt = (P_filt + P_filt.T) / 2
        Re_last = Re
        if t in Ns:
            out.append({"N": t, "prior_logdet_over_2N": float(mp_logdet(P_prior) / (2 * t)),
                        "post_logdet_over_2N": float(mp_logdet(P_filt) / (2 * t)),
                        "min_eig_post": float(min(mp.eigsy(P_filt, eigvals_only=True))),
                        "ln_det_Re": float(mp_logdet(Re))})
        # predict
        P_prior = A * P_prior * A.T + Q
        P_post_pred = A * P_filt * A.T + Q
    return out


def bode_rhs(As, Sig, Hs, s2u, W=4096):
    n = As[0].shape[0]
    w = (np.arange(W) + 0.5) / W * 2 * np.pi
    tot = 0.0
    for om in w:
        z = np.exp(-1j * om)
        Phi = np.eye(n, dtype=complex) - sum(A * z ** (k + 1) for k, A in enumerate(As))
        Pinv = np.linalg.inv(Phi)
        f = Pinv @ Sig @ Pinv.conj().T
        G = sum(H * z ** j for j, H in enumerate(Hs))
        PhiS = s2u * np.eye(G.shape[0]) + G @ f @ G.conj().T
        tot += np.log(np.linalg.det(PhiS).real)
    return tot / W


def bridge_check(As, Sig, N):
    n = As[0].shape[0]
    p = len(As)
    Si = np.linalg.inv(Sig)
    # full convolution, rows t = 1..N+p, columns 1..N
    Cf = np.zeros(((N + p) * n, N * n))
    for t in range(N + p):
        for s in range(N):
            k = t - s
            if k == 0:
                Cf[t * n:(t + 1) * n, s * n:(s + 1) * n] = np.eye(n)
            elif 1 <= k <= p:
                Cf[t * n:(t + 1) * n, s * n:(s + 1) * n] = -As[k - 1]
    Wi = np.kron(np.eye(N + p), Si)
    Tsym = Cf.T @ Wi @ Cf                 # T_N(f^{-1}), block Toeplitz
    AN = Cf[:N * n]
    Gi = AN.T @ np.kron(np.eye(N), Si) @ AN   # Gamma_N^{-1}
    Dm = Tsym - Gi
    k0 = (N - p) * n
    outside = np.abs(Dm[:k0, :]).max() + np.abs(Dm[:, :k0]).max()
    rank = np.linalg.matrix_rank(Dm[k0:, k0:], tol=1e-10)
    # block-Toeplitz check of Tsym
    toe = max(np.abs(Tsym[i * n:(i + 1) * n, j * n:(j + 1) * n]
                     - Tsym[(i + 1) * n:(i + 2) * n, (j + 1) * n:(j + 2) * n]).max()
              for i in range(N - 1) for j in range(N - 1))
    return {"N": N, "max_outside_last_p": float(outside), "rank_of_difference": int(rank),
            "np": n * p, "toeplitz_defect": float(toe)}


def cases():
    I2 = np.eye(2)
    rng = np.random.default_rng(20261116)
    cs = {}
    cs["C1_diag_obs"] = ([np.diag([1.5, 0.5])], I2, [np.array([[1.0, 0.0]])])
    cs["C2_diag_unobs"] = ([np.diag([1.5, 0.5])], I2, [np.array([[0.0, 1.0]])])
    cs["C3_triangular_e1_invariant"] = ([np.array([[1.4, 0.3], [0.0, 1.2]])], I2, [np.array([[0.0, 1.0]])])
    th = 0.7
    Rot = 1.2 * np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    cs["C4_complex_obs"] = ([Rot], I2, [np.array([[1.0, 0.0]])])
    cs["C4b_complex_H0"] = ([Rot], I2, [np.array([[0.0, 0.0]])])
    cs["C5_jordan_obs"] = ([np.array([[1.3, 1.0], [0.0, 1.3]])], I2, [np.array([[1.0, 0.0]])])
    cs["C5b_jordan_unobs"] = ([np.array([[1.3, 1.0], [0.0, 1.3]])], I2, [np.array([[0.0, 1.0]])])
    # C6: VAR(2) with an unstable mode (lam=1.6, eigvec (e2, e2/lam)) invisible to H=[1,0]
    lam = 1.6
    A2 = 0.3 * rng.standard_normal((2, 2))
    A1 = 0.4 * rng.standard_normal((2, 2))
    e2 = np.array([0.0, 1.0])
    A1[:, 1] = lam * (e2 - A2 @ e2 / lam ** 2)
    Sig = np.array([[1.0, 0.4], [0.4, 0.8]])
    # C6 (kept as found): built in double precision, the mode 1.6 is unobservable only to
    # ~6e-17, so for large N the holder sees it. Shows that the leakage shift is not
    # continuous in the holder gain.
    cs["C6_var2_nearly_hidden_mode"] = ([A1, A2], Sig, [np.array([[1.0, 0.0]])])
    # C8: exact construction. lam = 2 and dyadic entries, so A1 e2 + A2 e2 / 2 = 2 e2 holds
    # exactly in binary and the mode (e2, e2/2) is exactly in the kernel of [H 0], H = [1, 0].
    # Search a dyadic grid for one more unstable eigenvalue, of modulus in (1.1, 1.6),
    # observable, so that the hidden mode and a visible unstable mode share the noise.
    g = np.random.default_rng(7)
    found = None
    for _ in range(20000):
        B2 = g.integers(-8, 9, size=(2, 2)) / 16.0
        x, y = g.integers(-24, 25, size=2) / 16.0
        B1 = np.array([[x, -B2[0, 1] / 2.0], [y, 2.0 - B2[1, 1] / 2.0]])
        ev = np.linalg.eigvals(companion([B1, B2]))
        mods = sorted(abs(ev))
        if abs(mods[-1] - 2.0) < 1e-12 and 1.1 < mods[-2] < 1.6 and mods[-3] < 0.9:
            Cmap = output_map([np.array([[1.0, 0.0]])], 2, 2)
            if abs(unobservable_rho(companion([B1, B2]), Cmap)[0] - np.log(2.0)) < 1e-9:
                found = (B1, B2)
                break
    assert found is not None
    cs["C8_var2_hidden_mode_exact"] = ([found[0], found[1]], np.array([[1.0, 0.5], [0.5, 1.0]]),
                                       [np.array([[1.0, 0.0]])])
    # C9: same source, holder sees the second coordinate as well: hidden mode becomes visible
    cs["C9_var2_mode_visible"] = ([found[0], found[1]], np.array([[1.0, 0.5], [0.5, 1.0]]),
                                  [np.array([[1.0, 0.0], [0.0, 1.0]])])
    # C7: scalar AR(1) rho=1.5 with holder S_t = T_t - 1.5 T_{t-1} + U_t (sees innovations)
    cs["C7_scalar_innovation_holder"] = ([np.array([[1.5]]), np.array([[0.0]])], np.eye(1),
                                         [np.array([[1.0]]), np.array([[-1.5]])])
    cs["C7b_scalar_other_filter"] = ([np.array([[1.5]]), np.array([[0.0]])], np.eye(1),
                                     [np.array([[1.0]]), np.array([[-0.5]])])
    return cs



# Solver tolerances: the defaults (1e-13 fixed point, 1e-12 level) take minutes per
# window solve; at 1e-9 the window cost agrees with the default to 1e-6 bits (timed on
# Atlas, C1, N = 40 and 80) and takes under a second.
_pb = sc.penalised_block
_solve = sc.solve
sc.penalised_block = lambda Qt, Ht, SU, alpha, nu, X0=None, tol=1e-13, itmax=2000: \
    _pb(Qt, Ht, SU, alpha, nu, X0=X0, tol=1e-9, itmax=400)
sc.solve = lambda b, w, a, D, tol=1e-12, warm=None: _solve(b, w, a, D, tol=1e-9, warm=warm)


def window_mats(As, Sig, N):
    n = As[0].shape[0]
    p = len(As)
    Si = np.linalg.inv(Sig)
    Cf = np.zeros(((N + p) * n, N * n))
    for t in range(N + p):
        for s in range(N):
            k = t - s
            if k == 0:
                Cf[t * n:(t + 1) * n, s * n:(s + 1) * n] = np.eye(n)
            elif 1 <= k <= p:
                Cf[t * n:(t + 1) * n, s * n:(s + 1) * n] = -As[k - 1]
    P0 = Cf.T @ np.kron(np.eye(N + p), Si) @ Cf          # T_N(f^{-1})
    Rb = Cf[N * n:]                                       # boundary rows
    w, V = np.linalg.eigh(Si)
    F = Rb.T @ np.kron(np.eye(p), (V * np.sqrt(w)) @ V.T)  # B = F F^T = Rb^T (I_d (x) Si) Rb
    return P0, F


def holder_matrix(Hs, n, N):
    r = Hs[0].shape[0]
    G = np.zeros((N * r, N * n))
    for t in range(N):
        for j, H in enumerate(Hs):
            if t - j >= 0:
                G[t * r:(t + 1) * r, (t - j) * n:(t - j + 1) * n] = H
    return G


def spectral_cost(As, Sig, Hs, s2u, alpha, D, W=512):
    n = As[0].shape[0]
    blocks = []
    for k in range(W):
        om = 2 * np.pi * (k + 0.5) / W
        z = np.exp(-1j * om)
        Phi = np.eye(n, dtype=complex) - sum(A * z ** (j + 1) for j, A in enumerate(As))
        Pi = np.linalg.inv(Phi)
        f = sc.herm(Pi @ Sig @ Pi.conj().T)
        R = sc.psd_sqrt(f)
        G = sum(H * z ** j for j, H in enumerate(Hs))
        blocks.append((sc.herm(R @ R), G @ R, s2u * np.eye(G.shape[0], dtype=complex)))
    return sc.solve(blocks, np.full(W, 1.0 / W), alpha, D)


def window_cost(As, Sig, Hs, s2u, N, alpha, D, Ms, post_logdet_nats):
    n = As[0].shape[0]
    p = len(As)
    P0, F = window_mats(As, Sig, N)
    C0 = np.linalg.inv(P0)
    C0 = (C0 + C0.T) / 2
    E = F.T @ C0 @ F
    e, U = np.linalg.eigh((E + E.T) / 2)
    expl = (1 - e) < 1e-7
    Wm = C0 @ F
    G = holder_matrix(Hs, n, N)
    J = G.T @ G / s2u
    # exact constants (nats)
    ld_Gamma = N * np.linalg.slogdet(Sig)[1]
    k0 = (N - p) * n
    ld_GiJ = np.linalg.slogdet((P0 + J)[:k0, :k0])[1] - post_logdet_nats
    out = []
    for M in Ms:
        k = np.full(e.shape, float(M))
        k[~expl] = 1.0 / (1 - e[~expl])
        GM = Wm @ (U * k) @ U.T @ Wm.T
        GamM = C0 + (GM + GM.T) / 2
        R = np.real(sc.psd_sqrt(GamM))
        blk = (sc.herm(R @ R), G @ R, s2u * np.eye(G.shape[0]))
        sol = sc.solve([blk], [1.0 / N], alpha, D)   # weight 1/N: D is per symbol
        X = sol["X"][0]
        Delta = R @ X @ R
        Delta = (Delta + Delta.T) / 2
        ld_Delta = np.linalg.slogdet(Delta)[1]
        Pd = np.linalg.inv(Delta)
        ld_PJ = np.linalg.slogdet((Pd + Pd.T) / 2 + J)[1]
        r = 0.5 * (ld_Gamma - ld_Delta) / N / LN2
        l = 0.5 * (ld_PJ - ld_GiJ) / N / LN2
        out.append({"M": M, "rate": r, "leak": l, "cost": alpha * r + (1 - alpha) * l,
                    "dist": float(np.trace(Delta)) / N, "n_exploding": int(expl.sum())})
    return out




def toeplitz_of(fun, n, N, W=16384):
    """Block Toeplitz matrix whose (s, t) block is the coefficient of e^{i(s-t)w} in fun(w)."""
    w = 2 * np.pi * np.arange(W) / W
    vals = np.array([fun(om) for om in w])            # W x n x n
    T = np.zeros((N * n, N * n))
    for k in range(-(N - 1), N):
        ck = np.real(np.tensordot(np.exp(-1j * k * w), vals, axes=(0, 0)) / W)
        for s in range(N):
            t = s - k
            if 0 <= t < N:
                T[s * n:(s + 1) * n, t * n:(t + 1) * n] = ck
    return T


def f_of(As, Sig):
    n = As[0].shape[0]

    def fun(om):
        z = np.exp(1j * om)
        Phi = np.eye(n, dtype=complex) - sum(A * z ** (k + 1) for k, A in enumerate(As))
        Pi = np.linalg.inv(Phi)
        return Pi @ Sig @ Pi.conj().T
    return fun


def stationary_check(As, Sig, N=16):
    n, p = As[0].shape[0], len(As)
    P0, _ = window_mats(As, Sig, N)
    Tf = toeplitz_of(f_of(As, Sig), n, N)
    E = P0 - np.linalg.inv(Tf)
    E = (E + E.T) / 2
    k0, k1 = p * n, (N - p) * n
    mid = np.abs(E[k0:k1, :]).max() if k1 > k0 else 0.0
    mid = max(mid, np.abs(E[:, k0:k1]).max() if k1 > k0 else 0.0)
    ev = np.linalg.eigvalsh(E)
    rank = int(np.sum(np.abs(ev) > 1e-8 * max(1e-300, np.abs(ev).max())))
    return {"N": N, "max_outside_first_last_p": float(mid), "min_eig": float(ev.min()),
            "rank": rank, "2np": 2 * n * p, "norm": float(np.abs(ev).max())}


def floor_constant(As, Sig, Hs, s2u, W=4096):
    fun = f_of(As, Sig)
    eig = np.array([np.linalg.eigvalsh(fun(2 * np.pi * (k + 0.5) / W)) for k in range(W)])
    m_f, M_f = eig.min(), eig.max()
    Jn = sum(np.linalg.norm(H, 2) for H in Hs) ** 2 / s2u
    return min(1.0 / (1.0 / m_f + Jn), 1.0 / M_f)


EXACT = ["C1_diag_obs", "C2_diag_unobs", "C3_triangular_e1_invariant", "C4_complex_obs",
         "C4b_complex_H0", "C5_jordan_obs", "C5b_jordan_unobs", "C8_var2_hidden_mode_exact",
         "C9_var2_mode_visible", "C7_scalar_innovation_holder"]
WINDOW = ["C1_diag_obs", "C2_diag_unobs", "C8_var2_hidden_mode_exact"]
OUT = {}


def growth_ok(rows, key, target):
    e = {r["N"]: r[key] - target for r in rows}
    return bool(400 * abs(e[400]) <= 2 * max(50 * abs(e[50]), 100 * abs(e[100])) + 1e-6), e


def main(path=None):
    OUT.clear()
    t0 = time.time()
    fails = 0
    allc = cases()
    Ns = [25, 50, 100, 200, 400]
    res = {}
    for name, (As, Sig, Hs) in allc.items():
        n, p = As[0].shape[0], len(As)
        Ac = companion(As)
        C = output_map(Hs, n, p)
        rs = rho_star(Ac)
        ru, dim_u = unobservable_rho(Ac, C)
        g = growth(As, Sig, Hs, 1.0, Ns)
        br = bridge_check(As, Sig, 12)
        st = stationary_check(As, Sig, 16)
        c_floor = floor_constant(As, Sig, Hs, 1.0)
        rhs = bode_rhs(As, Sig, Hs, 1.0) + 2 * (rs - ru)
        pri_ok, pri_e = growth_ok(g, "prior_logdet_over_2N", rs)
        post_ok, post_e = growth_ok(g, "post_logdet_over_2N", ru)
        rec = {"rho_star_bits": rs / LN2, "rho_hid_bits": ru / LN2, "unobs_dim": dim_u,
               "eig": [str(complex(x)) for x in np.linalg.eigvals(Ac)], "growth": g,
               "bridge": br, "stationary": st, "c_floor": c_floor,
               "innovations": {"lnDetRe_400": g[-1]["ln_det_Re"], "rhs": rhs,
                               "diff": g[-1]["ln_det_Re"] - rhs},
               "prior_err": pri_e, "post_err": post_e}
        checks = {
            "bridge": br["max_outside_last_p"] <= 1e-12 and br["rank_of_difference"] <= br["np"]
            and br["toeplitz_defect"] <= 1e-12,
            "stationary": st["max_outside_first_last_p"] <= 1e-8 and st["min_eig"] >= -1e-8
            and st["rank"] <= st["2np"],
            "posterior_floor": all(r["min_eig_post"] >= c_floor * (1 - 1e-9) for r in g),
        }
        if name in EXACT:
            checks.update({"prior_growth": pri_ok, "posterior_growth": post_ok,
                           "innovations": abs(rec["innovations"]["diff"]) <= 1e-9})
        rec["checks"] = {k: bool(v) for k, v in checks.items()}
        fails += sum(not v for v in checks.values())
        res[name] = rec
        print(f"{name:30s} rho*={rs / LN2:.4f} rho_hid={ru / LN2:.4f} bits | 400*err prior "
              f"{400 * pri_e[400]:+.3f} post {400 * post_e[400]:+.3f} | innov {rec['innovations']['diff']:+.1e}"
              f" | {rec['checks']}", flush=True)
    OUT["cases"] = res

    wres = {}
    for name in WINDOW + ["C7_scalar_innovation_holder"]:
        As, Sig, Hs = allc[name]
        n, p = As[0].shape[0], len(As)
        Ac = companion(As)
        C = output_map(Hs, n, p)
        rs = rho_star(Ac) / LN2
        ru = unobservable_rho(Ac, C)[0] / LN2
        WN = [40, 80, 160, 320]
        g = growth(As, Sig, Hs, 1.0, WN)
        post = {r["N"]: 2 * r["N"] * r["post_logdet_over_2N"] for r in g}
        Dmax = spectral_cost(As, Sig, Hs, 1.0, 1.0, 1e9)["D"]
        rows = []
        ok = True
        for alpha in (0.0, 0.5, 1.0):
            D = 0.3 * Dmax
            Vf = spectral_cost(As, Sig, Hs, 1.0, alpha, D)["cost"]
            pred = alpha * rs + (1 - alpha) * ru + Vf
            gaps = {}
            for N in WN:
                wc = window_cost(As, Sig, Hs, 1.0, N, alpha, D, [1e3, 1e5], post[N])
                cap = abs(wc[0]["cost"] - wc[1]["cost"])
                gaps[N] = wc[-1]["cost"] - pred
                rows.append({"alpha": alpha, "N": N, "pred": pred, "Vf": Vf, "window": wc,
                             "gap": gaps[N], "cap_change": cap})
                ok = ok and cap <= 1e-6
            ok = ok and abs(gaps[320]) <= abs(gaps[40]) / 4
            print(f"  window {name:28s} a={alpha:.1f} pred={pred:.4f} gaps "
                  f"{[f'{gaps[N]:+.4f}' for N in WN]}", flush=True)
        wres[name] = {"rows": rows, "ok": bool(ok) if name in WINDOW else None}
        if name in WINDOW:
            fails += not ok
    OUT["window_cost"] = wres
    OUT["_meta"] = {"failed": int(fails), "seconds": round(time.time() - t0, 1),
                    "numpy": np.__version__, "mp_dps": mp.mp.dps}
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_unstable_vector.json")
    with open(path, "w") as fh:
        json.dump(OUT, fh, indent=1)
    print("FAILED CHECKS:", fails)
    return 0 if fails == 0 else 1


def cap_followup(path=None):
    """Follow-up added after the first run, in which the cap criterion failed for C8 at
    N = 40 and 80 (changes up to 1.9e-6 bits between M = 1e3 and 1e5). Records the cost
    of C8 at N = 40 and 80 for M = 1e3, 1e5, 1e7. No pass criterion."""
    As, Sig, Hs = cases()["C8_var2_hidden_mode_exact"]
    rs = rho_star(companion(As)) / LN2
    ru = unobservable_rho(companion(As), output_map(Hs, As[0].shape[0], len(As)))[0] / LN2
    g = growth(As, Sig, Hs, 1.0, [40, 80])
    post = {r["N"]: 2 * r["N"] * r["post_logdet_over_2N"] for r in g}
    Dmax = spectral_cost(As, Sig, Hs, 1.0, 1.0, 1e9)["D"]
    rows = []
    for alpha in (0.0, 0.5, 1.0):
        D = 0.3 * Dmax
        pred = alpha * rs + (1 - alpha) * ru + spectral_cost(As, Sig, Hs, 1.0, alpha, D)["cost"]
        for N in (40, 80):
            wc = window_cost(As, Sig, Hs, 1.0, N, alpha, D, [1e3, 1e5, 1e7], post[N])
            rows.append({"alpha": alpha, "N": N, "pred": pred, "costs": [w["cost"] for w in wc]})
            print(f"  C8 a={alpha:.1f} N={N}: cost at M=1e3,1e5,1e7 "
                  f"{[f'{w['cost']:.8f}' for w in wc]}", flush=True)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_unstable_vector_caps.json")
    with open(path, "w") as fh:
        json.dump({"rows": rows, "numpy": np.__version__}, fh, indent=1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--caps":
        cap_followup()
        sys.exit(0)
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
