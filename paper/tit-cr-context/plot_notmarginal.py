"""Figure: non-determination by the reduced marginal (cor:notmarginal).

Plots L(D) against D for the two instances of the corollary, which share
the reduced (Y, S) joint law up to bijective scaling
(Corr(Y,S) = rho/sqrt(s) = 1/sqrt(2) in both):

  instance 1: (rho^2, tau^2) = (1/2, 0)    -- clean context;
              L(D) = max(0, 0.5*log2(1/(2D)))   (Proposition prop:marg(ii))
  instance 2: (rho^2, tau^2) = (3/4, 1/2)  -- noisy context;
              L(D) = 0.5*log2(g*)               (Theorem thm:function)

The two distortion levels tabulated in Table tab:notmarginal (D = 0.1,
0.3) are marked.  The script prints the values at the marked levels and
the two gaps; the figure caption quotes those printed numbers.

Output: notmarginal.pdf and notmarginal.png (300 dpi, grayscale, serif).
"""

import numpy as np
from numpy import log2, sqrt
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RHO2_2, TAU2_2 = 0.75, 0.5  # instance 2


def gstar(rho2, tau2, D):
    s = 1.0 + tau2
    b_ = D + s - rho2
    return (b_ + sqrt(b_ * b_ - 4 * D * s * (1 - rho2))) / (2 * D * s)


def L1(D):
    """Instance (1/2, 0): clean context, L = (1/2)log2^+(1/(2D))."""
    return np.maximum(0.0, 0.5 * log2(1.0 / (2.0 * D)))


def L2(D):
    """Instance (3/4, 1/2): closed form (1/2)log2 g*."""
    return 0.5 * log2(gstar(RHO2_2, TAU2_2, D))


D = np.linspace(0.02, 0.6, 800)
Dmarks = np.array([0.1, 0.3])

corr = sqrt(0.5)
print(f"common reduced correlation Corr(Y,S) = 1/sqrt(2) = {corr:.4f}")
for Dm in Dmarks:
    l1, l2 = L1(Dm), L2(Dm)
    print(f"D = {Dm}:  L1 = {l1:.4f}  L2 = {l2:.4f}  gap = {l2 - l1:.4f} bits")

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 13,
})
fig, ax = plt.subplots(figsize=(6.4, 4.4))
ax.plot(D, L1(D), color="0.45", lw=1.6, ls="--",
        label=r"$(\rho^2,\tau^2)=(\frac{1}{2},\,0)$")
ax.plot(D, L2(D), color="0.2", lw=1.6, ls="-",
        label=r"$(\rho^2,\tau^2)=(\frac{3}{4},\,\frac{1}{2})$")
ax.plot(Dmarks, L1(Dmarks), marker="s", color="0.45", ms=7, ls="none")
ax.plot(Dmarks, L2(Dmarks), marker="o", color="0.2", ms=7, ls="none")
for Dm in Dmarks:
    ax.plot([Dm, Dm], [L1(Dm), L2(Dm)], color="0.7", lw=0.9, zorder=0)
ax.annotate(rf"gap ${L2(0.1) - L1(0.1):.4f}$", (0.1, L2(0.1)),
            textcoords="offset points", xytext=(10, 8))
ax.annotate(rf"gap ${L2(0.3) - L1(0.3):.4f}$", (0.3, L2(0.3)),
            textcoords="offset points", xytext=(10, 8))
ax.set_xlabel(r"distortion $D$")
ax.set_ylabel(r"conditional content $L(D)$ (bits)")
ax.legend(frameon=False)
ax.grid(True, color="0.85", lw=0.5)
fig.tight_layout()
fig.savefig("notmarginal.pdf", dpi=300)
fig.savefig("notmarginal.png", dpi=300)
print("wrote notmarginal.pdf and notmarginal.png")
