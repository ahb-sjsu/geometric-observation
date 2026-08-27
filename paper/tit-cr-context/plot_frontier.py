"""Figure 2: the Gaussian Pareto frontier of the rate--content region.

Traces (R(alpha), L(alpha)) for alpha in [0,1] at (rho^2, tau^2, D) =
(0.75, 0.5, 0.3) by direct minimization of the weighted objective
phi_alpha = alpha*B0 + (1-alpha)*B1 over (a, b) with n = D - h(a, b),
the same routine that verifier_num_checks.py uses.  Endpoints are
checked against the closed forms: alpha=1 gives the classical reverse
channel (R_min = 0.5*log2(1/D), content L(1)); alpha=0 gives the channel
of Theorem 2 (rate R(0), content L_min = L(D) = 0.5*log2(g*)).

Output: frontier.pdf (300 dpi, grayscale, serif).  The script prints the
endpoint excesses R(0)-R_min and L(1)-L_min; the figure caption quotes
those printed numbers.
"""

import numpy as np
from numpy import log2, sqrt
from scipy.optimize import minimize
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RHO2, TAU2, D = 0.75, 0.5, 0.3


def gstar(rho2, tau2, D):
    s = 1.0 + tau2
    b_ = D + s - rho2
    return (b_ + sqrt(b_ * b_ - 4 * D * s * (1 - rho2))) / (2 * D * s)


def coords(a, b, rho2, tau2, D):
    """(R, L) of the channel with regression (a, b) and active n = D - h."""
    rho, s = sqrt(rho2), 1.0 + tau2
    h = (1 - a) ** 2 - 2 * (1 - a) * b * rho + b * b
    n = D - h
    if n <= 0:
        return None
    Q0 = a * a + b * b + 2 * a * b * rho
    Q1 = Q0 - (a * rho + b) ** 2 / s
    return 0.5 * log2((Q0 + n) / n), 0.5 * log2((Q1 + n) / n)


def phi(al, x):
    out = coords(x[0], x[1], RHO2, TAU2, D)
    if out is None:
        return 1e6
    return al * out[0] + (1 - al) * out[1]


def brute(al, starts=40, seed=0):
    rng = np.random.default_rng(seed)
    best, bx = np.inf, None
    for _ in range(starts):
        x0 = np.array([1 - D, 0.0]) + 0.25 * rng.standard_normal(2)
        r = minimize(lambda x: phi(al, x), x0, method="Nelder-Mead",
                     options=dict(xatol=1e-12, fatol=1e-14, maxiter=6000))
        if r.fun < best:
            best, bx = r.fun, r.x
    return bx


alphas = np.linspace(0.0, 1.0, 41)
R, L = [], []
for al in alphas:
    x = brute(al)
    r, l = coords(x[0], x[1], RHO2, TAU2, D)
    R.append(r)
    L.append(l)
R, L = np.array(R), np.array(L)

# closed-form anchors
Rmin = 0.5 * log2(1 / D)                      # alpha = 1 endpoint rate
g = gstar(RHO2, TAU2, D)
Lmin = 0.5 * log2(g)                          # alpha = 0 endpoint content
s = 1 + TAU2
L1 = 0.5 * log2(((1 - D) * (1 - RHO2 / s) + D) / D)   # content of reverse channel

print(f"R_min          = {Rmin:.6f} bits (closed form 0.5*log2(1/D))")
print(f"L_min = L(D)   = {Lmin:.6f} bits (closed form 0.5*log2(g*))")
print(f"R(0)           = {R[0]:.6f} bits  (traced endpoint, alpha=0)")
print(f"L(1)           = {L[-1]:.6f} bits  (traced endpoint, alpha=1)")
print(f"closed-form L(1) = {L1:.6f}")
print(f"excess rate    R(0)-R_min = {R[0]-Rmin:.4f} bits")
print(f"excess content L(1)-L_min = {L[-1]-Lmin:.4f} bits")
print(f"endpoint residuals: dR(1)={abs(R[-1]-Rmin):.2e}  dL(0)={abs(L[0]-Lmin):.2e}"
      f"  dL(1) vs closed form={abs(L[-1]-L1):.2e}")

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 13,
})
fig, ax = plt.subplots(figsize=(6.4, 4.4))
ax.plot(R, L, color="0.2", lw=1.6)
ax.plot(Rmin, L[-1], marker="s", color="0.2", ms=7)
ax.plot(R[0], Lmin, marker="o", color="0.2", ms=7)
ax.annotate(r"$(R_{\min},\,L(1))$", (Rmin, L[-1]),
            textcoords="offset points", xytext=(14, -6))
ax.annotate(r"$(R(0),\,L_{\min})$", (R[0], Lmin),
            textcoords="offset points", xytext=(-10, 12), ha="right")
ax.margins(x=0.08, y=0.10)
ax.set_xlabel(r"rate $R$ (bits)")
ax.set_ylabel(r"conditional content $L$ (bits)")
ax.grid(True, color="0.85", lw=0.5)
fig.tight_layout()
fig.savefig("frontier.pdf", dpi=300)
print("wrote frontier.pdf")
