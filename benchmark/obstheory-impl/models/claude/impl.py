"""Direction-of-arrival compression benchmark.

Single narrowband source on an M-element half-wavelength ULA:

    x = a(theta0) * s + delta,   a_m(theta) = exp(1j*pi*m*sin(theta)),  |s| = 1

A consumer C estimates the continuous source angle by matched-filter ML
(maximize |a(theta)^H x|^2 over theta).  We shape the compression error
`delta` in an orthonormal basis of the real embedding R^{2M} whose first
axis is the informative direction w_hat -- the unit real vector along which
a measurement perturbation most changes the angle estimate.

Everything is pure numpy + stdlib and deterministic given `seed`.
"""

import numpy as np


# --------------------------------------------------------------------------
# Informative direction w_hat (derived from consumer/array geometry)
# --------------------------------------------------------------------------
#
# The consumer maximizes  J(theta, x) = |a(theta)^H x|^2 .  The estimate
# theta_hat(x) solves the stationarity condition  g := dJ/dtheta = 0 .  By
# the implicit function theorem,  d theta_hat / dx = -(dg/dtheta)^{-1} dg/dx ,
# and since dg/dtheta is a scalar at the operating point, the direction in
# x-space that most changes theta_hat is parallel to the x-gradient of g.
#
# Write J = (a^H x)(x^H a).  Then
#     g = dJ/dtheta = 2 Re[ (a^H x) (x^H a') ]           (a' = da/dtheta)
# and its Wirtinger derivative is
#     dg/d(x bar) = (a^H x) a' + (a'^H x) a .
# For a real scalar g, the R^{2M} gradient is the embedding of 2 dg/d(x bar),
# so w_hat is the (normalized) real embedding of that complex vector.
#
# Evaluated noiselessly at x = a(theta0)*s with |s|=1 (take s = 1):
#     a^H x = M,  and
#     w_c = M a'(theta0) + (a'(theta0)^H a0) a0 .
# with a'_m = 1j*pi*m*cos(theta0) * a_m.
def informative_direction(M, theta0):
    m = np.arange(M)
    a0 = np.exp(1j * np.pi * m * np.sin(theta0))
    ap = 1j * np.pi * m * np.cos(theta0) * a0            # da/dtheta at theta0
    wc = M * ap + np.vdot(ap, a0) * a0                   # vdot(ap,a0) = ap^H a0
    w = np.concatenate([wc.real, wc.imag])
    n = np.linalg.norm(w)
    if n == 0.0:
        w = np.zeros(2 * M)
        w[0] = 1.0
        return w
    return w / n


# --------------------------------------------------------------------------
# Continuous ML angle estimator
# --------------------------------------------------------------------------
_GR = (np.sqrt(5.0) - 1.0) / 2.0


def _make_grid(M, n_grid=3601):
    th = np.linspace(-np.pi / 2 + 1e-4, np.pi / 2 - 1e-4, n_grid)
    m = np.arange(M)
    A = np.exp(1j * np.pi * np.outer(np.sin(th), m))     # (n_grid, M)
    return th, A


def _golden_max(f, a, b, tol=1e-8, itmax=200):
    c = b - _GR * (b - a)
    d = a + _GR * (b - a)
    fc, fd = f(c), f(d)
    for _ in range(itmax):
        if (b - a) < tol:
            break
        if fc < fd:
            a, c, fc = c, d, fd
            d = a + _GR * (b - a)
            fd = f(d)
        else:
            b, d, fd = d, c, fc
            c = b - _GR * (b - a)
            fc = f(c)
    return 0.5 * (a + b)


def estimate_theta(x, grid_th, A, M):
    """Return the continuous ML angle estimate (radians)."""
    m = np.arange(M)
    p = np.abs(A.conj() @ x) ** 2                         # |a(theta)^H x|^2
    gi = int(np.argmax(p))
    lo = grid_th[max(gi - 1, 0)]
    hi = grid_th[min(gi + 1, len(grid_th) - 1)]

    def f(th):
        a = np.exp(1j * np.pi * m * np.sin(th))
        v = np.vdot(a, x)                                 # a^H x
        return (v.real * v.real + v.imag * v.imag)

    return _golden_max(f, lo, hi, tol=1e-9)


# --------------------------------------------------------------------------
# Variance shaping (matched total log-precision across arms)
# --------------------------------------------------------------------------
def _arm_vars(arm, s0sq, kappa, twoM):
    dP = twoM - 1
    v = np.empty(twoM)
    if arm == "invariant":
        v[0] = s0sq / kappa
        v[1:] = s0sq * kappa ** (1.0 / dP)
    elif arm == "recon":
        v[:] = s0sq
    elif arm == "anti":
        v[0] = s0sq * kappa
        v[1:] = s0sq * kappa ** (-1.0 / dP)
    elif arm == "omission":                              # w_hat uncoded
        v[0] = 0.05
        v[1:] = s0sq * kappa ** (1.0 / dP)
    else:
        raise ValueError(arm)
    return v


def _basis_from_direction(w):
    """Orthonormal basis Q of R^{2M} with first column parallel to w."""
    twoM = w.shape[0]
    Q, _ = np.linalg.qr(np.column_stack([w, np.eye(twoM)]))
    return Q[:, :twoM]


# --------------------------------------------------------------------------
# Main entry point
# --------------------------------------------------------------------------
def solve(M, theta0_deg, kappa, s0sq_list, n_trials, seed):
    rng = np.random.default_rng(seed)
    theta0 = np.radians(theta0_deg)
    twoM = 2 * M

    w = informative_direction(M, theta0)
    Qw = _basis_from_direction(w)

    m = np.arange(M)
    x0 = np.exp(1j * np.pi * m * np.sin(theta0))          # source, s = 1
    grid_th, A = _make_grid(M)

    def arm_mc(arm, s0sq, Q):
        v = _arm_vars(arm, s0sq, kappa, twoM)
        z = rng.standard_normal((n_trials, twoM))
        delta_v = (z * np.sqrt(v)) @ Q.T
        energy = float(np.mean(np.sum(delta_v * delta_v, axis=1)))
        delta_c = delta_v[:, :M] + 1j * delta_v[:, M:]
        se = 0.0
        for t in range(n_trials):
            th = estimate_theta(x0 + delta_c[t], grid_th, A, M)
            e = np.degrees(th) - theta0_deg
            se += e * e
        return se / n_trials, energy

    arms = ["invariant", "recon", "anti"]
    mse = {a: [] for a in arms}
    recon_energy = {a: [] for a in arms}

    for s0sq in s0sq_list:
        for a in arms:
            mm, ee = arm_mc(a, s0sq, Qw)
            mse[a].append(mm)
            recon_energy[a].append(ee)

    # ---- omission arm: floor multiplier at the highest-rate point --------
    hi_idx = int(np.argmin(s0sq_list))          # smallest var -> highest rate
    s0_hi = s0sq_list[hi_idx]
    om_mse, _ = arm_mc("omission", s0_hi, Qw)
    inv_hi = mse["invariant"][hi_idx]
    omission_floor_mult = float(om_mse / inv_hi) if inv_hi > 0 else 0.0

    # ---- shuffled control: shape around a random direction ---------------
    r = rng.standard_normal(twoM)
    r = r / np.linalg.norm(r)
    Qr = _basis_from_direction(r)
    shuffled_flip = 0
    for s0sq in s0sq_list:
        vals = {a: arm_mc(a, s0sq, Qr)[0] for a in arms}
        if vals["invariant"] <= vals["recon"] <= vals["anti"]:
            shuffled_flip += 1

    return {
        "read_dir": w.tolist(),
        "mse": {a: mse[a] for a in arms},
        "recon_energy": {a: recon_energy[a] for a in arms},
        "omission_floor_mult": omission_floor_mult,
        "shuffled_flip": int(shuffled_flip),
    }


if __name__ == "__main__":
    out = solve(M=16, theta0_deg=-7.0, kappa=4.0,
                s0sq_list=[0.02, 0.05, 0.1, 0.2],
                n_trials=200, seed=0)
    inv = out["mse"]["invariant"]
    rec = out["mse"]["recon"]
    ant = out["mse"]["anti"]
    en = out["recon_energy"]
    print("s0sq      invariant     recon         anti")
    for i, s in enumerate([0.02, 0.05, 0.1, 0.2]):
        print(f"{s:<8} {inv[i]:.6e}  {rec[i]:.6e}  {ant[i]:.6e}")
    mse_ok = all(inv[i] <= rec[i] <= ant[i] for i in range(len(inv)))
    en_ok = all(en["recon"][i] <= min(en["invariant"][i], en["anti"][i])
                for i in range(len(inv)))
    print("angle MSE flip (inv<=recon<=anti):", mse_ok)
    print("recon smallest energy:", en_ok)
    print("FLIP:", mse_ok and en_ok)
    print("omission_floor_mult:", out["omission_floor_mult"])
    print("shuffled_flip:", out["shuffled_flip"])
