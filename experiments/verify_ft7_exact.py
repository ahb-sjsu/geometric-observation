"""C3 net for the exact results of the T1 addendum on moving read kernels (FRONTIER FT.7).

Claims checked (paper/t1-moving-kernel/t1-moving-kernel.tex, by label):
  prop:exact(a)
               For g_a(x) = x1 + a sin x2 and Sigma = I, the consumer loss of the
               fixed-covariance channel with error covariance Delta = [[d11, d12], [d12, v]] is
               L = d11 + 2 a e^{-1/2} d12 + a^2 F(v), with
               F(v) = 1 - e^{-v/2} + e^{-2} (e^{3v/2} - (1 + e^{2v})/2).
  prop:exact(b), (c)
               F is concave on [0, 1], so L >= tr(H_a Delta) >= mu tr(Delta) with
               H_a = [[1, a e^{-1/2}], [a e^{-1/2}, a^2 (1 - e^{-2})/2]] and mu = lambda_min(H_a)
               (H_a is called Theta_a in the note);
               hence D_0 >= mu s_0.
  thm:sharp    For Q positive definite and small D,
               R_0(D) - (p/2) ln(1 + 4 K D / lambda^2) <= R_fixed(D)
                   <= R_0(D) - (p/2) ln(1 - B D / p^2),
               R_0(D) = (p/2) ln(p/D) + (1/2) ln det(Sigma Q), B = K (tr Q^{-1})^2.
  thm:reduce   For any Sigma and a consumer with rank Q = q < p, R_fixed of (T, g) equals
               R_fixed of the reduced pair (S, f) in dimension q: the loss depends on Delta only
               through the active block E of the whitened error covariance, the rate is at
               least -(1/2) ln det E, and the lift diag(E, I) attains it.

  prop:rate    For a = 1, Sigma = I and 0 < D <= 1e-2: R_fixed(D) = -(1/2) ln max phi_D(v)
               over 0 <= v <= D/eta, phi_D(v) = v (D - F(v) + v/e), eta = F(1) - 1/e; phi_D
               is strictly concave there; the minimizing covariance has d22 = v*,
               d12 = -e^{-1/2} v*, d11 = D - F(v*) + 2 v*/e. (phi_D is Phi_D in the note.)

Checks:
  e1  prop:exact against Monte Carlo (4 standard errors) at 3 covariances, for a = 1 and 0.7.
  e2  prop:exact(b), (c): F'' < 0 on a grid; F(v) >= v F(1); on 20,000 random admissible
      Delta, L >= tr(H_a Delta) and the ratio L / tr(Delta) is at least mu; a numerical
      estimate of D_0 lies in [mu s_0, 3 lambda^2 / (4K)].
  e3  thm:sharp for g_1: a numerical search for the least rate over all 2x2 Delta with the
      EXACT loss (not a certified minimum) lies inside the sandwich at D = 1e-4, 1e-5, 1e-6,
      which are below mu s_0 and so inside the proved range. The values at 1e-2 and 1e-3 are
      recorded and are not part of the verdict.
  e4  thm:reduce(b) on an instance with p = 3, q = 2 and a correlated Sigma for which
      ker Q is not invariant under Sigma: g(x) = g_1(Bx) with B Sigma B^T = I. The instance
      is checked first: rank Q = 2, the first two columns of O span the range of H, and
      B Delta B^T is the leading block of the whitened covariance. Then: the loss of the
      full 3-dimensional channel (Monte Carlo) equals the exact reduced loss at that block;
      the rate is at least -(1/2) ln det E on random Delta; the lift attains it. The
      consumer is g_1 composed with B, so part (a) of the theorem holds by construction
      here and is not tested; the rate inequality has a wide margin on these Delta and
      guards only against a wrong direction.
  e5  The numbers the note quotes for g_1: h(U) by quadrature at two resolutions
      (agreement to 1e-9), the variance of U by the same quadrature against its closed
      form, the exact rate of the family t Q^{-1} at D = 1e-5 against the search (1e-6),
      and the family's excess over the Shannon and Gaussian bounds on R_U against
      (1/2) ln(1/D) + c'_- and c'_+ of cor:gapq (within 1e-4, the O(D) term). h(U) and
      Var U cancel in those two comparisons: both say |family rate - R_0(D)| <= 1e-4, so
      they test the constant of thm:sharp, not h(U) and not c'_+ against c'_-. h(U) is
      tested separately: two resolutions of one quadrature, and a second method (adaptive
      quadrature over a trapezoid-rule density), agreement to 1e-9. Last, the entropy step
      of prop:gapex, 0 <= h(U + sqrt(D) N) - h(U) <= (1/2) ln(1 + D), at D = 0.1 and 0.01.
      By prop:gapex the constant of the gap is c'_+ (called C_* there).

  e6  prop:rate (a = 1): phi_D'' < 0 on a grid of [0, 0.16]; phi_D' changes sign on
      (0, D/eta), which is what lets the root-finder return v*; the stated covariance,
      with d11 from the proposition's own formula, has loss D to 1e-15, is positive
      definite and below I; its rate equals -(1/2) ln phi_D(v*); the search of e3 agrees
      with that rate to 1e-9; and of 40,000 random admissible Delta per value of D, each
      scaled along its ray to loss exactly D (the loss is concave along a ray, so that
      point is the best feasible one on it), none has a lower rate. The random comparison
      can only catch a claimed minimum that is too high; the search agreement catches one
      that is too low. D = 1e-2, 1e-3, 1e-4, 1e-5, 1e-6.

What the checks cannot fail on: e3's search is an upper estimate of the infimum, so its
comparison with the lower side of the sandwich is only as good as the search; at a = 1,
e6 shows the search's values are the minimum. The O(D)
remainder is checked through the sandwich, on one consumer.

Fire test: `--fire` exits 0 only if every mutant fails its check.
  m1  the cross term with e^{-1} in place of e^{-1/2}                     (e1 must fail)
  m2  mu replaced by lambda_min(Q)                                        (e2 must fail)
  m3  R_0 with ln(1/D) in place of ln(p/D)                                (e3 must fail)
  m4  the lift with 1/2 in place of 1 on the inactive coordinate          (e4 must fail)
  m5  the reduced covariance taken as the Schur complement, not the block (e4 must fail)
  m6  h(U) replaced by the Gaussian entropy of the same variance          (e5 must fail;
      it fails on the guard h(U) < Gaussian entropy, not on the excess comparisons)
  m7  the entropy step with the bound (1/2) ln(1 + D / Var U)             (e5 must fail)
  m8  h(U) shifted by 1e-6                                                (e5 must fail,
      on the agreement with the second quadrature method)
  m9  prop:rate with the term v^2/e dropped (a diagonal Delta)             (e6 must fail,
      by about 0.52 nats)
  m10 prop:rate with d12 = -0.99 e^{-1/2} v                               (e6 must fail,
      by a few 1e-6 nats: this one probes the tolerance)

Output: results/FT7-exact-net.json (verdict, FT7EXACT_supported). Seed 20261122.
"""
import json
import math
import sys
import time

import numpy as np
from scipy import optimize

SEED = 20261122
N_MC = 2_000_000
EH = math.exp(-0.5)


def F(v):
    return -math.expm1(-v / 2) + math.exp(-2.0) * (math.expm1(1.5 * v) - 0.5 * math.expm1(2 * v))


def F2(v):
    return -0.25 * math.exp(-v / 2) + math.exp(-2.0) * (2.25 * math.exp(1.5 * v) - 2 * math.exp(2 * v))


def loss_exact(d, a=1.0, cross=EH):
    return d[0][0] + 2 * a * cross * d[0][1] + a * a * F(d[1][1])


def Q_of(a):
    return np.array([[1.0, a * EH], [a * EH, 0.5 * a * a * (1 + math.exp(-2.0))]])


def H_of(a):
    return np.array([[1.0, a * EH], [a * EH, 0.5 * a * a * (1 - math.exp(-2.0))]])


def consts(a=1.0):
    q = Q_of(a)
    lam = float(np.linalg.eigvalsh(q)[0])
    m1, m2 = math.sqrt(1 + a * a), abs(a)
    k = 1.75 * m2 ** 2 + 2 * m1 * m2 + (math.sqrt(5) / 2) * m2 * m2 * math.sqrt(2) + (5 / 12) * m2 * m2 * 2
    return q, lam, k, lam / (2 * k)


def mc_loss2(d, a, rng, n=N_MC):
    d = np.asarray(d, dtype=float)
    xh = rng.standard_normal((n, 2)) @ np.linalg.cholesky(np.eye(2) - d).T
    z = rng.standard_normal((n, 2)) @ np.linalg.cholesky(d).T
    l = (z[:, 0] + a * (np.sin(xh[:, 1] + z[:, 1]) - np.sin(xh[:, 1]))) ** 2
    return float(l.mean()), float(l.std() / math.sqrt(n))


E1_CASES = [[[0.02, -0.01], [-0.01, 0.03]], [[0.2, -0.06], [-0.06, 0.1]], [[0.3, 0.1], [0.1, 0.5]]]


def check_e1(rng, cross=EH):
    rows, ok = [], True
    for a in (1.0, 0.7):
        for d in E1_CASES:
            m, se = mc_loss2(d, a, rng)
            c = loss_exact(d, a, cross)
            z = (c - m) / se
            rows.append({"a": a, "Delta": d, "exact": c, "mc": m, "se": se, "z": z})
            ok = ok and abs(z) <= 4.0
    return ok, rows


def random_admissible(rng, n):
    out = []
    for _ in range(n):
        th = rng.uniform(0, math.pi)
        ev = np.exp(rng.uniform(math.log(1e-6), 0.0, size=2))
        r = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        out.append(r @ np.diag(ev) @ r.T)
    return out


def d0_estimate(s0):
    """Numerical inf of the exact loss over admissible Delta with trace >= s0 (a = 1)."""
    best = math.inf

    def obj(p):
        x, y, t = abs(p[0]), min(abs(p[1]), 1.0), math.tanh(p[2])
        d12 = t * math.sqrt(x * y)
        pen = 1e9 * max(0.0, s0 - (x + y)) ** 2
        return loss_exact([[x, d12], [d12, y]]) + pen
    for x0 in (1e-4, 3e-3, 7e-3, 1e-2):
        for t0 in (-3.0, -1.0, 0.0):
            r = optimize.minimize(obj, [x0, max(s0 - x0, 1e-5) + 1e-5, t0], method="Nelder-Mead",
                                  options={"xatol": 1e-13, "fatol": 1e-16, "maxiter": 40000})
            best = min(best, float(r.fun))
    return best


def check_e2(rng, mu=None):
    q, lam, k, s0 = consts(1.0)
    h = H_of(1.0)
    mu_true = float(np.linalg.eigvalsh(h)[0])
    mu = mu_true if mu is None else mu
    vs = np.linspace(0.0, 1.0, 4001)
    concave = all(F2(v) < 0 for v in vs)
    chord = all(F(v) >= v * F(1.0) - 1e-15 for v in vs)
    ds = random_admissible(rng, 20000)
    worst = min(loss_exact(d) / float(np.trace(d)) for d in ds)
    worst_h = min(loss_exact(d) - float(np.trace(h @ d)) for d in ds)
    d0 = d0_estimate(s0)
    up = 3 * lam * lam / (4 * k)
    info = {"mu": mu_true, "lambda_min_Q": lam, "K": k, "s0": s0, "mu_s0": mu_true * s0,
            "D0_upper_bound": up, "D0_numerical_estimate": d0, "worst_ratio_L_over_trace": worst,
            "F_concave_on_grid": concave, "F_above_chord": chord, "F_at_1": F(1.0),
            "least_L_minus_trace_H_Delta": worst_h}
    ok = concave and chord and worst >= mu and worst_h >= -1e-15 and mu * s0 <= d0 <= up
    return ok, info


def min_rate_exact(D):
    """Search for the least rate -(1/2) ln det Delta with exact loss <= D (a = 1, Sigma = I)."""
    q = Q_of(1.0)
    qi = np.linalg.inv(q)

    def delta(p):
        th, la, lb = p
        r = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        return r @ np.diag([math.exp(la), math.exp(lb)]) @ r.T

    def rate(p):
        return -0.5 * (p[1] + p[2])

    def slack(p):
        return (D - loss_exact(delta(p))) / D

    best = math.inf
    t = D / 2.0
    w, v = np.linalg.eigh(t * qi)
    th0 = math.atan2(v[1, 0], v[0, 0])
    starts = [[th0, math.log(w[0]), math.log(w[1])]]
    for dth in (-0.4, 0.4, 1.0):
        for sc in (-0.7, 0.0, 0.7):
            starts.append([th0 + dth, math.log(w[0]) + sc, math.log(w[1]) - sc])
    for s in starts:
        r = optimize.minimize(rate, s, method="SLSQP", constraints=[{"type": "ineq", "fun": slack}],
                              bounds=[(None, None), (-40.0, -1e-9), (-40.0, -1e-9)],
                              options={"ftol": 1e-14, "maxiter": 500})
        if r.success and slack(r.x) >= -1e-9:
            best = min(best, float(r.fun))
    return best


E3_PROVED = [1e-4, 1e-5, 1e-6]
E3_OTHER = [1e-2, 1e-3]


def check_e3(with_p=True):
    q, lam, k, s0 = consts(1.0)
    p = 2
    b = k * float(np.trace(np.linalg.inv(q))) ** 2
    rows, ok = [], True
    for D in E3_OTHER + E3_PROVED:
        r0 = 0.5 * p * math.log((p if with_p else 1.0) / D) + 0.5 * math.log(np.linalg.det(q))
        lo = r0 - 0.5 * p * math.log(1 + 4 * k * D / lam ** 2)
        hi = r0 - 0.5 * p * math.log(1 - b * D / p ** 2) if b * D < p * p else math.inf
        rm = min_rate_exact(D)
        inside = lo - 1e-9 <= rm <= hi + 1e-9
        rows.append({"D": D, "R0": r0, "lower": lo,
                     "upper": hi if math.isfinite(hi) else None, "min_rate_exact_loss": rm,
                     "min_minus_R0": rm - r0, "inside": bool(inside), "in_verdict": D in E3_PROVED})
        if D in E3_PROVED:
            ok = ok and inside
    return ok, rows


# ---- e4: the reduction, p = 3, q = 2, correlated Sigma ----
SIG3 = np.array([[2.0, 0.6, 0.3], [0.6, 1.0, -0.2], [0.3, -0.2, 1.5]])


def sqrtm_sym(m):
    w, v = np.linalg.eigh(m)
    return v @ np.diag(np.sqrt(w)) @ v.T


def instance3():
    """g(x) = g_1(Bx) with B Sigma B^T = I_2; returns B, Sigma^{1/2}, the orthogonal O."""
    sh = sqrtm_sym(SIG3)
    a0 = np.array([[1.0, 0.5, 0.0], [0.0, 1.0, 1.0]])
    m = a0 @ sh                      # rows to orthonormalise
    qm, _ = np.linalg.qr(m.T)        # 3x2, orthonormal columns
    rows = qm.T                      # orthonormal rows = B Sigma^{1/2}
    b = rows @ np.linalg.inv(sh)
    n = np.cross(rows[0], rows[1])
    o = np.vstack([rows[0], rows[1], n / np.linalg.norm(n)]).T
    return b, sh, o


def mc_loss3(delta, b, rng, n=N_MC):
    xh = rng.standard_normal((n, 3)) @ np.linalg.cholesky(SIG3 - delta + 1e-14 * np.eye(3)).T
    z = rng.standard_normal((n, 3)) @ np.linalg.cholesky(delta).T
    uh, u = xh @ b.T, (xh + z) @ b.T
    l = (u[:, 0] + np.sin(u[:, 1]) - uh[:, 0] - np.sin(uh[:, 1])) ** 2
    return float(l.mean()), float(l.std() / math.sqrt(n))


def check_e4(rng, lift_inactive=1.0, schur=False):
    b, sh, o = instance3()
    shi = np.linalg.inv(sh)
    # the unread direction and whether Sigma leaves it invariant
    nq = np.linalg.svd(b)[2][2]
    sn = SIG3 @ nq
    sin_angle = float(np.linalg.norm(np.cross(sn, nq)) / np.linalg.norm(sn))
    ok, rows, worst_rate_gap, block_err = True, [], math.inf, 0.0
    # the instance: Q = B^T Q_1 B, H = Sigma^{1/2} Q Sigma^{1/2}
    qfull = b.T @ Q_of(1.0) @ b
    hh = sh @ qfull @ sh
    rank_q = int(np.sum(np.linalg.eigvalsh(qfull) > 1e-10))
    range_err = float(np.abs(hh @ o[:, 2]).max())          # last column of O in ker H
    eig_err = float(np.abs(np.sort(np.linalg.eigvalsh(hh))[1:] - np.linalg.eigvalsh(Q_of(1.0))).max())
    bsb_err = float(np.abs(b @ SIG3 @ b.T - np.eye(2)).max())
    for _ in range(4):
        ev = np.exp(rng.uniform(math.log(0.02), math.log(0.9), size=3))
        g, _ = np.linalg.qr(rng.standard_normal((3, 3)))
        dp = g @ np.diag(ev) @ g.T                      # whitened error covariance, 0 < dp <= I
        delta = sh @ o @ dp @ o.T @ sh
        if schur:
            e = np.linalg.inv(np.linalg.inv(dp)[:2, :2])
        else:
            e = b @ delta @ b.T                         # = dp[:2, :2]
        block_err = max(block_err, float(np.abs(b @ delta @ b.T - dp[:2, :2]).max()))
        m, se = mc_loss3(delta, b, rng)
        c = loss_exact(e)
        z = (c - m) / se
        rate_full = 0.5 * math.log(np.linalg.det(SIG3) / np.linalg.det(delta))
        rate_red = -0.5 * math.log(np.linalg.det(dp[:2, :2]))
        worst_rate_gap = min(worst_rate_gap, rate_full - rate_red)
        rows.append({"exact_reduced": c, "mc_full": m, "se": se, "z": z,
                     "rate_full": rate_full, "rate_reduced": rate_red})
        ok = ok and abs(z) <= 4.0 and rate_full >= rate_red - 1e-10
    # the lift attains the reduced rate
    e = np.array([[0.03, -0.01], [-0.01, 0.05]])
    dp = np.zeros((3, 3)); dp[:2, :2] = e; dp[2, 2] = lift_inactive
    delta = sh @ o @ dp @ o.T @ sh
    lift_gap = abs(0.5 * math.log(np.linalg.det(SIG3) / np.linalg.det(delta)) + 0.5 * math.log(np.linalg.det(e)))
    below = float(np.linalg.eigvalsh(SIG3 - delta)[0])
    ok = ok and lift_gap <= 1e-10 and below >= -1e-12 and sin_angle > 0.05
    ok = ok and rank_q == 2 and max(range_err, eig_err, bsb_err, block_err) <= 1e-10
    info = {"rows": rows, "worst_rate_full_minus_reduced": worst_rate_gap, "lift_rate_gap": lift_gap,
            "lift_min_eig_Sigma_minus_Delta": below, "sin_angle_Sigma_n_to_n": sin_angle,
            "B_Sigma_Bt_error": bsb_err, "rank_Q": rank_q, "O_last_column_in_ker_H": range_err,
            "nonzero_eig_H_vs_Q1": eig_err, "block_vs_B_Delta_Bt": block_err}
    return ok, info


def h_and_var(n, m, lim, noise=0.0):
    """h and variance of X1 + sin X2 + sqrt(noise) N, by Gauss-Hermite (n) and Simpson (m)."""
    from scipy import integrate
    t, w = np.polynomial.hermite_e.hermegauss(n)
    w = w / math.sqrt(2 * math.pi)
    u = np.linspace(-lim, lim, m)
    v = 1.0 + noise
    f = (np.exp(-0.5 * (u[:, None] - np.sin(t)[None, :]) ** 2 / v) / math.sqrt(2 * math.pi * v)) @ w
    ent = np.where(f > 0, -f * np.log(np.where(f > 0, f, 1.0)), 0.0)
    return float(integrate.simpson(ent, x=u)), float(integrate.simpson(f * u * u, x=u))


def family_rate_exact(D):
    """Rate of Delta = t Q^{-1} with exact loss D (a = 1)."""
    q = Q_of(1.0)
    qi = np.linalg.inv(q)
    t = optimize.brentq(lambda x: loss_exact(x * qi) - D, D / 20, D, xtol=1e-18, rtol=1e-14)
    return 0.5 * math.log(np.linalg.det(q)) - math.log(t)


def h_second_method():
    """h(U) by adaptive quadrature in u over a trapezoid-rule density in t."""
    from scipy import integrate
    tt = np.linspace(-10.0, 10.0, 20001)
    wt = np.exp(-0.5 * tt * tt) / (2 * math.pi) * (tt[1] - tt[0])
    st = np.sin(tt)

    def ent(u):
        f = float(np.sum(wt * np.exp(-0.5 * (u - st) ** 2)))
        return -f * math.log(f) if f > 0 else 0.0
    val, err = integrate.quad(ent, -12.0, 12.0, limit=400, epsabs=1e-13, epsrel=1e-13)
    return float(val), float(err)


def check_e5(gaussian_h=False, weak_bound=False, h_shift=0.0):
    D = 1e-5
    h1, v1 = h_and_var(80, 4001, 12.0)
    h2, v2 = h_and_var(240, 32001, 16.0)
    h3, h3_err = h_second_method()
    var = 1 + 0.5 * (1 - math.exp(-2.0))
    h = 0.5 * math.log(2 * math.pi * math.e * var) if gaussian_h else h2 + h_shift
    q = Q_of(1.0)
    fam = family_rate_exact(D)
    srch = min_rate_exact(D)
    slb = h - 0.5 * math.log(2 * math.pi * math.e * D)      # Shannon lower bound on R_U, k = 1
    gub = 0.5 * math.log(var / D)                           # Gaussian upper bound on R_U
    half = 0.5 * math.log(1 / D)
    cm = math.log(2.0) + 0.5 * math.log(np.linalg.det(q)) - 0.5 * math.log(var)
    cp = math.log(2.0) + 0.5 * math.log(np.linalg.det(q)) + 0.5 * math.log(2 * math.pi * math.e) - h
    # prop:gapex: 0 <= h(U + sqrt(D) N) - h(U) <= (1/2) ln(1 + D)
    steps = []
    for dd in (0.1, 0.01):
        inc = h_and_var(240, 32001, 16.0, noise=dd)[0] - h2
        bound = 0.5 * math.log(1 + (dd / var if weak_bound else dd))
        steps.append({"D": dd, "entropy_increase": inc, "half_log_1_plus_D": bound})
    step_ok = all(0.0 <= r["entropy_increase"] <= r["half_log_1_plus_D"] for r in steps)
    info = {"h_U": h2, "h_U_coarse": h1, "h_U_resolution_difference": abs(h1 - h2),
            "h_U_second_method": h3, "h_U_second_method_quad_error_estimate": h3_err,
            "h_U_method_difference": abs(h3 - h2),
            "entropy_step": steps,
            "var_U_quadrature": v2, "var_U_closed_form": var,
            "family_rate_exact_1e-5": fam, "search_min_1e-5": srch,
            "R_U_shannon_lower_1e-5": slb, "R_U_gaussian_upper_1e-5": gub,
            "family_minus_gaussian_upper": fam - gub, "family_minus_shannon_lower": fam - slb,
            "c_minus_prime": cm, "c_plus_prime": cp,
            "half_log_plus_c_minus": half + cm, "half_log_plus_c_plus": half + cp}
    ok = (abs(h1 - h2) <= 1e-9 and abs(v2 - var) <= 1e-9 and abs(fam - srch) <= 1e-6
          and h < 0.5 * math.log(2 * math.pi * math.e * var)
          and abs((fam - gub) - (half + cm)) <= 1e-4 and abs((fam - slb) - (half + cp)) <= 1e-4
          and cp - cm > 1e-5 and step_ok and abs(h - h3) <= 1e-9)
    return ok, info


def F1(v):
    return 0.5 * math.exp(-v / 2) + math.exp(-2.0) * (1.5 * math.exp(1.5 * v) - math.exp(2 * v))


E6_DS = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]


def check_e6(rng, cross=1.0):
    """cross = 1 is the proposition; d12 = -cross e^{-1/2} v is the mutated minimizer."""
    ie = (2 * cross - cross * cross) * math.exp(-1.0)
    kappa = F(1.0) - math.exp(-1.0)
    grid = np.linspace(0.0, 0.16, 1601)
    worst_curv = max(-2 * F1(v) - v * F2(v) + 2 * math.exp(-1.0) for v in grid)
    ok, rows = worst_curv < 0, []
    for D in E6_DS:
        phi = lambda v: v * (D - F(v) + v * ie)
        dphi = lambda v: D - F(v) + 2 * v * ie - v * F1(v)
        vmax = D / kappa
        v = optimize.brentq(dphi, 1e-300, vmax, xtol=1e-300, rtol=8.9e-16)
        rate = -0.5 * math.log(phi(v))
        d12 = -cross * EH * v
        # the proposition's own formula for d11 at cross = 1: D - F(v*) + 2 v*/e
        d11 = D - F(v) + 2 * cross * v * math.exp(-1.0)
        delta = np.array([[d11, d12], [d12, v]])
        loss = loss_exact(delta)
        lo = float(np.linalg.eigvalsh(delta)[0])
        hi = float(np.linalg.eigvalsh(np.eye(2) - delta)[0])
        rate_direct = -0.5 * math.log(np.linalg.det(delta))
        srch = min_rate_exact(D)
        # random admissible Delta scaled to loss exactly D: none may beat the rate
        best = math.inf
        for d in random_admissible(rng, 40000):
            sc = optimize.brentq(lambda x: loss_exact(x * d) - D, 1e-12, 1.0, xtol=1e-300, rtol=1e-12) \
                if loss_exact(d) > D else 1.0
            best = min(best, -0.5 * math.log(np.linalg.det(sc * d)))
        rows.append({"D": D, "v_star": v, "v_star_over_bound": v / vmax, "rate": rate,
                     "rate_from_det": rate_direct, "loss_of_minimizer": loss,
                     "min_eig_Delta": lo, "min_eig_I_minus_Delta": hi,
                     "search_min": srch, "rate_minus_search": rate - srch,
                     "best_random_rate_minus_rate": best - rate})
        ok = (ok and 0 < v < vmax and abs(loss - D) <= 1e-15
              and lo > 0 and hi > 0 and abs(rate - rate_direct) <= 1e-9
              and abs(rate - srch) <= 1e-9 and best >= rate - 1e-12)
    return ok, {"max_phi_second_derivative_on_grid": worst_curv, "kappa": kappa, "rows": rows}


def run():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    out = {"net": "FT.7 exact net", "seed": SEED, "n_mc": N_MC}
    ok1, r1 = check_e1(rng)
    ok2, r2 = check_e2(rng)
    ok3, r3 = check_e3()
    ok4, r4 = check_e4(rng)
    ok5, r5 = check_e5()
    ok6, r6 = check_e6(rng)
    out.update({"e1": r1, "e2": r2, "e3": r3, "e4": r4, "e5": r5, "e6": r6})
    out["verdict"] = {"e1_exact_loss": bool(ok1), "e2_d0_lower_bound": bool(ok2),
                      "e3_sharp_expansion": bool(ok3), "e4_reduction": bool(ok4),
                      "e5_quoted_numbers": bool(ok5), "e6_exact_rate": bool(ok6)}
    out["FT7EXACT_supported"] = all(out["verdict"].values())
    out["seconds"] = round(time.time() - t0, 1)
    return out


def fire():
    rng = np.random.default_rng(SEED + 1)
    q, lam, k, s0 = consts(1.0)
    caught = {
        "m1_cross_term": not check_e1(rng, cross=math.exp(-1.0))[0],
        "m2_mu_is_lambda_min_Q": not check_e2(rng, mu=lam)[0],
        "m3_R0_without_log_p": not check_e3(with_p=False)[0],
        "m4_lift_half": not check_e4(rng, lift_inactive=0.5)[0],
        "m5_schur_complement": not check_e4(rng, schur=True)[0],
        "m6_gaussian_entropy": not check_e5(gaussian_h=True)[0],
        "m7_entropy_step_weak_bound": not check_e5(weak_bound=True)[0],
        "m8_h_shifted": not check_e5(h_shift=1e-6)[0],
        "m9_no_cross_term": not check_e6(rng, cross=0.0)[0],
        "m10_cross_term_0.99": not check_e6(rng, cross=0.99)[0],
    }
    print("fire:", caught)
    return all(caught.values())


if __name__ == "__main__":
    if "--fire" in sys.argv:
        sys.exit(0 if fire() else 1)
    o = run()
    path = sys.argv[1] if len(sys.argv) > 1 else "results/FT7-exact-net.json"
    json.dump(o, open(path, "w"), indent=1)
    print("verdict:", o["verdict"])
    print("FT7EXACT_supported:", o["FT7EXACT_supported"])
    sys.exit(0 if o["FT7EXACT_supported"] else 1)
