"""Fig. 2: water-filling on a tilted spectrum, for a scalar process observed by the
holder through a filter in white noise (the commuting case of Section IV).

For a scalar source with spectrum S(w), Q = 1, and holder information
j(w) = |H(w)|^2 S(w) / S_U, the frontier field of Theorem 6 is
x(w) = min{1, xi(w)}, xi the positive root of  t S j x^2 + (t S - alpha j) x - 1 = 0
with t = 2 nu, and the error spectrum D(w) = S(w) x(w).  Since Phi(a) = min{1, 1/a}
for a scalar, the fixed point gives

    D(w) = min{ S(w), lambda(w) },   lambda(w) = 1 / (2 nu + (1-alpha) j / (S (1 + j x))),

reverse water-filling of S under a surface lambda that is flat (= 1/(2 nu)) at
alpha = 1 and is lowered where the holder's information j is large.  The level nu
is set by the distortion budget.  The script checks the closed form against the
general solver of spectral_core.py and writes fig_waterfill.pdf / .png to the
working directory (run it from this folder).
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import spectral_core as sc  # noqa: E402

plt.rcParams.update({"font.family": "serif", "font.size": 10, "mathtext.fontset": "cm"})

# the instance (illustrative): AR(1) source, holder behind a band-pass filter
A_AR, S_U, FRAC = 0.5, 0.02, 0.6


def spectra(w):
    S = (1 - A_AR ** 2) / np.abs(1 - A_AR * np.exp(-1j * w)) ** 2      # unit variance
    H = (1 - np.exp(-2j * w)) / 2                                        # |H|^2 = sin^2 w
    j = np.abs(H) ** 2 * S / S_U
    return S, H, j


def x_field(S, j, alpha, t):
    A, B = t * S * j, t * S - alpha * j
    root = np.sqrt(B ** 2 + 4 * A)
    with np.errstate(divide="ignore", invalid="ignore"):
        # the positive root of A x^2 + B x - 1, in the form without cancellation
        xi = np.where(B >= 0, 2 / (B + root), (root - B) / (2 * A))
    return np.minimum(1.0, xi)


def level(S, j, alpha, D):
    lo, hi = 1e-8, 1e8
    for _ in range(300):
        t = np.sqrt(lo * hi)
        lo, hi = (t, hi) if np.mean(S * x_field(S, j, alpha, t)) > D else (lo, t)
    return np.sqrt(lo * hi)


def check_against_solver(n=64):
    wk = 2 * np.pi * np.arange(n) / n
    S, H, j = spectra(wk)
    D = FRAC * np.mean(S)
    worst = 0.0
    for alpha in (1.0, 0.5, 0.0):
        blocks = [(np.array([[s]], complex), np.array([[h * np.sqrt(s)]], complex),
                   np.array([[S_U]], complex)) for s, h in zip(S, H)]
        r = sc.solve(blocks, [1 / n] * n, alpha, D)
        xs = np.array([np.real(X[0, 0]) for X in r["X"]])
        xc = x_field(S, j, alpha, level(S, j, alpha, D))
        worst = max(worst, float(np.abs(xs - xc).max()))
    assert worst < 1e-9, worst
    return worst


def main():
    worst = check_against_solver()
    w = np.linspace(0, np.pi, 2001)
    S, H, j = spectra(w)
    wf = np.linspace(-np.pi, np.pi, 4096, endpoint=False)          # the budget uses the full circle
    Sf, _, jf = spectra(wf)
    D = FRAC * np.mean(Sf)
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.1), sharey=True)
    rows = []
    for ax, alpha, tag in zip(axes, (1.0, 0.0), ("(a)", "(b)")):
        t = level(Sf, jf, alpha, D)
        x = x_field(S, j, alpha, t)
        Dw = S * x
        lam = 1 / (t + (1 - alpha) * j / (S * (1 + j * x)))
        R = np.mean(-0.5 * np.log2(x_field(Sf, jf, alpha, t)))
        xf = x_field(Sf, jf, alpha, t)
        L = np.mean(0.5 * np.log2((1 / xf + jf) / (1 + jf)))
        rows.append((alpha, 1 / t, R, L))
        ax.fill_between(w, 0, Dw, color="C0", alpha=0.22, lw=0)
        ax.plot(w, S, color="0.2", lw=1.5, label=r"spectrum $S(\omega)$")
        ax.plot(w, lam, color="C0", lw=1.2, ls="--",
                label=r"surface $\lambda(\omega)$, flat at the level $1/(2\nu)$ in (a)")
        ax.plot(w, Dw, color="C0", lw=1.2, label=r"error spectrum $D(\omega)$")
        ax.set_xlim(0, np.pi)
        ax.set_xticks([0, np.pi / 2, np.pi])
        ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$"])
        ax.set_xlabel(r"frequency $\omega$")
        ax.set_title(f"{tag} " + (r"$\alpha=1$: rate" if alpha == 1 else r"$\alpha=0$: leakage"),
                     fontsize=9.5)
        if alpha == 0.0:
            ax2 = ax.twinx()
            ax2.plot(w, j, color="0.55", lw=0.9, ls=":",
                     label=r"holder's information $j(\omega)$, right axis of (b)")
            ax2.set_ylabel(r"$j(\omega)$", color="0.4", fontsize=9)
            ax2.tick_params(axis="y", colors="0.4", labelsize=8)
            ax2.set_ylim(0, 1.15 * j.max())
    axes[0].set_ylabel("spectral density")
    axes[0].set_ylim(0, 1.15 * S.max())
    h, l = axes[0].get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    fig.legend(h + h2, l + l2, frameon=False, fontsize=8, loc="lower center", ncol=2)
    fig.tight_layout(rect=(0, 0.14, 1, 1))
    fig.savefig("fig_waterfill.pdf")          # in the working directory, as plot_bands.py does
    fig.savefig("fig_waterfill.png", dpi=300)
    print(f"closed form vs spectral_core.solve, max |dx| = {worst:.1e}")
    for alpha, lv, R, L in rows:
        print(f"alpha={alpha}: 1/(2nu)={lv:.4f}  R={R:.4f}  L={L:.4f} bits/symbol")


if __name__ == "__main__":
    main()
