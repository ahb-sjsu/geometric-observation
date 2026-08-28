"""Figure 4 (fig:binary): the binary objective, the tilt residual, and the
frontier.

Panels 1-2, at (p, q, D) = (0.25, 0.15, 0.15), along the constraint
segment (1-p) d0 + p d1 = D, parameterized by d0:
  panel 1: L(d0) = h2(u) - (1-p) h2(d0) - p h2(d1)   [bits]
  panel 2: psi(d0) = l(d0) - l(d1) - 2(1-2q) l(u)    [nats]
with l(x) = ln((1-x)/x), u = a*q, a = 2(1-p) d0 + p - D.  The unique
interior zero of psi (Lemma: tilt root) is the unique minimizer of L
(Theorem: the binary function).

Panel 3, at (p, q, D) = (0.1, 0.1, 0.05): the binary rate--content
frontier (Remark: the binary rate--content frontier), R(d0) =
1 - (1-p) h2(d0) - p h2(d1) against L(d0) along the segment; the Pareto
arc runs from the tilt root (the L-minimizer) to d0 = D (the
R-minimizer, R_min = 1 - h2(D)).  The script prints the two endpoint
excesses; the caption quotes them.

Output: binary.pdf and binary.png (300 dpi, grayscale, serif).
"""

import numpy as np
from scipy.optimize import brentq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

P, Q, D = 0.25, 0.15, 0.15

lo = max(0.0, (D - P) / (1 - P))
hi = D / (1 - P)


def h2(x):
    x = np.clip(x, 1e-15, 1 - 1e-15)
    return -(x * np.log2(x) + (1 - x) * np.log2(1 - x))


def ell(x):
    x = np.clip(x, 1e-15, 1 - 1e-15)
    return np.log((1 - x) / x)


def parts(d0):
    d1 = (D - (1 - P) * d0) / P
    a = 2 * (1 - P) * d0 + P - D
    u = a * (1 - Q) + (1 - a) * Q
    return d1, a, u


def L(d0):
    d1, _, u = parts(d0)
    return h2(u) - (1 - P) * h2(d0) - P * h2(d1)


def psi(d0):
    d1, _, u = parts(d0)
    return ell(d0) - ell(d1) - 2 * (1 - 2 * Q) * ell(u)


eps = 1e-9
d0s = np.linspace(lo + 1e-4, hi - 1e-4, 800)
root = brentq(psi, lo + eps, hi - eps, xtol=1e-14)
d1r, ar, ur = parts(root)
Lmin = L(root)

print(f"segment: d0 in ({lo:.4f}, {hi:.4f})")
print(f"tilt root d0* = {root:.4f}  (d1* = {d1r:.4f}, u* = {ur:.4f})")
print(f"L(d0*) = {Lmin:.4f} bits")
print(f"psi(d0*) = {psi(root):.2e}")
print(f"sign changes of psi on grid: "
      f"{int(np.sum(np.diff(np.sign(psi(d0s))) != 0))}")

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 12,
})
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6.2, 8.0))

ax1.plot(d0s, L(d0s), color="0.2", lw=1.6)
ax1.plot(root, Lmin, marker="o", color="0.2", ms=7)
ax1.annotate(rf"$(d_0^\star,\,L^\star)=({root:.4f},\,{Lmin:.4f})$",
             (root, Lmin), textcoords="offset points", xytext=(10, 10))
ax1.set_ylabel(r"$L(d_0)$ (bits)")
ax1.grid(True, color="0.85", lw=0.5)

ax2.plot(d0s, psi(d0s), color="0.2", lw=1.6)
ax2.axhline(0.0, color="0.6", lw=0.8)
ax2.plot(root, 0.0, marker="o", color="0.2", ms=7)
ax2.annotate(rf"$d_0^\star={root:.4f}$", (root, 0.0),
             textcoords="offset points", xytext=(10, 10))
ax2.set_xlabel(r"$d_0$ along the constraint segment $(1-p)d_0+pd_1=D$")
ax2.set_ylabel(r"$\psi(d_0)$ (nats)")
ax2.grid(True, color="0.85", lw=0.5)

# ---- panel 3: the binary rate--content frontier at (p, q, D) = (0.1, 0.1, 0.05)
P2, Q2, D2 = 0.1, 0.1, 0.05
lo2 = max(0.0, (D2 - P2) / (1 - P2))
hi2 = D2 / (1 - P2)


def parts2(d0):
    d1 = (D2 - (1 - P2) * d0) / P2
    a = 2 * (1 - P2) * d0 + P2 - D2
    u = a * (1 - Q2) + (1 - a) * Q2
    return d1, a, u


def L2(d0):
    d1, _, u = parts2(d0)
    return h2(u) - (1 - P2) * h2(d0) - P2 * h2(d1)


def R2(d0):
    d1, _, _ = parts2(d0)
    return 1 - (1 - P2) * h2(d0) - P2 * h2(d1)


def psi2(d0):
    d1, _, u = parts2(d0)
    return ell(d0) - ell(d1) - 2 * (1 - 2 * Q2) * ell(u)


root2 = brentq(psi2, lo2 + eps, hi2 - eps, xtol=1e-14)
Lmin2 = L2(root2)
Rmin2 = 1 - h2(D2)                       # R-minimizer at d0 = d1 = D
dR = R2(root2) - Rmin2                   # rate excess of the L-optimal point
dL = L2(D2) - Lmin2                      # content excess of the R-optimal point

print()
print(f"frontier instance (p,q,D) = ({P2}, {Q2}, {D2})")
print(f"segment: d0 in ({lo2:.4f}, {hi2:.4f})")
print(f"tilt root d0* = {root2:.4f}  (L-minimizer)")
print(f"L_min = L(d0*)          = {Lmin2:.4f} bits")
print(f"R_min = 1 - h2(D)       = {Rmin2:.4f} bits  (at d0 = D = {D2})")
print(f"R(d0*) - R_min          = {dR:.4f} bits  (rate excess of L-optimum)")
print(f"L(D) - L_min            = {dL:.4f} bits  (content excess of R-optimum)")

d0f = np.linspace(lo2 + 1e-6, hi2 - 1e-6, 1200)
Rf, Lf = R2(d0f), L2(d0f)
arc = np.linspace(root2, D2, 400)        # the Pareto arc
ax3.plot(Rf, Lf, color="0.7", lw=1.0)
ax3.plot(R2(arc), L2(arc), color="0.2", lw=1.8)
ax3.plot(Rmin2, L2(D2), marker="s", color="0.2", ms=7)
ax3.plot(R2(root2), Lmin2, marker="o", color="0.2", ms=7)
ax3.annotate(rf"$(R_{{\min}},\,{L2(D2):.4f})$", (Rmin2, L2(D2)),
             textcoords="offset points", xytext=(10, 8))
ax3.annotate(rf"$({R2(root2):.4f},\,L_{{\min}})$", (R2(root2), Lmin2),
             textcoords="offset points", xytext=(10, -14))
ax3.margins(x=0.08, y=0.12)
ax3.set_xlabel(r"rate $R$ (bits)")
ax3.set_ylabel(r"conditional content $L$ (bits)")
ax3.grid(True, color="0.85", lw=0.5)

fig.align_ylabels([ax1, ax2, ax3])
fig.tight_layout()
fig.savefig("binary.pdf", dpi=300)
fig.savefig("binary.png", dpi=300)
print("wrote binary.pdf and binary.png")
