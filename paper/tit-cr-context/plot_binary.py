"""Figure 3: the binary objective and the tilt residual.

At (p, q, D) = (0.25, 0.15, 0.15), plots along the constraint segment
(1-p) d0 + p d1 = D, parameterized by d0:
  top panel:    L(d0) = h2(u) - (1-p) h2(d0) - p h2(d1)   [bits]
  bottom panel: psi(d0) = l(d0) - l(d1) - 2(1-2q) l(u)    [nats]
with l(x) = ln((1-x)/x), u = a*q, a = 2(1-p) d0 + p - D.  The unique
interior zero of psi (Lemma: tilt root) is the unique minimizer of L
(Theorem: the binary function).  Output: binary.pdf (300 dpi, grayscale,
serif).  The caption quotes the numbers this script prints.
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
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6.2, 5.2))

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

fig.align_ylabels([ax1, ax2])
fig.tight_layout()
fig.savefig("binary.pdf", dpi=300)
print("wrote binary.pdf")
