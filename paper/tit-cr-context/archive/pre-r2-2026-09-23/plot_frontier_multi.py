"""Figure: the rate--content frontier at three correlations, fixed (tau^2, D).

Overlays the Pareto frontier (R(alpha), L(alpha)) for rho^2 = 0.2, 0.5, 0.8 at
tau^2 = 0.5, D = 0.3, by the same weighted-objective minimization as
plot_frontier.py / verifier_num_checks.py. It shows how the endpoint gap
between (R_min, L_R^star) and (R_L^star, L_min) -- i.e. how two-dimensional the
region is -- grows with correlation, the intuition behind the misalignment
dichotomy. Marker SHAPE (not colour alone) distinguishes the curves. The
caption quotes the printed endpoint gaps.

Output: frontier_multi.pdf and frontier_multi.png (300 dpi, grayscale, serif).
"""

import numpy as np
from numpy import log2, sqrt
from scipy.optimize import minimize
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

TAU2, D = 0.5, 0.3
RHO2S = [0.2, 0.5, 0.8]
MARKERS = ["o", "s", "^"]
GREYS = ["0.15", "0.4", "0.6"]


def gstar(rho2, tau2, D):
    s = 1.0 + tau2
    b_ = D + s - rho2
    return (b_ + sqrt(b_ * b_ - 4 * D * s * (1 - rho2))) / (2 * D * s)


def coords(a, b, rho2, tau2, D):
    rho, s = sqrt(rho2), 1.0 + tau2
    h = (1 - a) ** 2 - 2 * (1 - a) * b * rho + b * b
    n = D - h
    if n <= 0:
        return None
    Q0 = a * a + b * b + 2 * a * b * rho
    Q1 = Q0 - (a * rho + b) ** 2 / s
    return 0.5 * log2((Q0 + n) / n), 0.5 * log2((Q1 + n) / n)


def phi(al, x, rho2):
    out = coords(x[0], x[1], rho2, TAU2, D)
    if out is None:
        return 1e6
    return al * out[0] + (1 - al) * out[1]


def brute(al, rho2, starts=30, seed=0):
    rng = np.random.default_rng(seed)
    best, bx = np.inf, None
    for _ in range(starts):
        x0 = np.array([1 - D, 0.0]) + 0.25 * rng.standard_normal(2)
        r = minimize(lambda x: phi(al, x, rho2), x0, method="Nelder-Mead",
                     options=dict(xatol=1e-12, fatol=1e-14, maxiter=6000))
        if r.fun < best:
            best, bx = r.fun, r.x
    return bx


plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 13})
fig, ax = plt.subplots(figsize=(6.4, 4.4))
alphas = np.linspace(0.0, 1.0, 31)
Rmin = 0.5 * log2(1 / D)

for rho2, mk, gy in zip(RHO2S, MARKERS, GREYS):
    R, L = [], []
    for al in alphas:
        x = brute(al, rho2)
        r, l = coords(x[0], x[1], rho2, TAU2, D)
        R.append(r); L.append(l)
    R, L = np.array(R), np.array(L)
    Lmin = 0.5 * log2(gstar(rho2, TAU2, D))
    dR = R[0] - Rmin
    dL = L[-1] - Lmin
    print(f"rho^2={rho2}: R_min={Rmin:.4f} R_L*={R[0]:.4f} L_min={Lmin:.4f} "
          f"L_R*={L[-1]:.4f} | rate gap dR={dR:.4f}  content gap dL={dL:.4f}")
    ax.plot(R, L, color=gy, lw=1.4, marker=mk, ms=4, markevery=5,
            label=rf"$\rho^2={rho2}$  ($\Delta R={dR:.3f},\ \Delta L={dL:.3f}$)")

ax.set_xlabel(r"rate $R$ (bits)")
ax.set_ylabel(r"conditional content $L$ (bits)")
ax.grid(True, color="0.88", lw=0.5)
ax.legend(frameon=False, fontsize=10, loc="upper right")
fig.tight_layout()
fig.savefig("frontier_multi.pdf", dpi=300)
fig.savefig("frontier_multi.png", dpi=300)
print("wrote frontier_multi.pdf and frontier_multi.png")
