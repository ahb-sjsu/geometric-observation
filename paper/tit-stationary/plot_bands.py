"""Fig. 3: distortion allocations of the rate-optimal and leakage-optimal
descriptions for the disjoint-bands instance.  Reads verify_spectral.json
(written by verify_spectral.py); writes fig_bands.pdf and fig_bands.png."""
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.family": "serif", "font.size": 10, "mathtext.fontset": "cm"})


def main(path="verify_spectral.json"):
    f = json.load(open(path))["_figure_disjoint"]
    w = np.array(f["w"])
    half = w <= np.pi + 1e-12                      # the spectra are even: plot [0, pi]
    SY, Dr, Dl = (np.array(f[k])[half] for k in ("SY", "Dr", "Dl"))
    w = w[half]
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.plot(w, SY, color="0.25", lw=1.6, label=r"spectrum $S_Y(\omega)$")
    ax.plot(w, Dr, color="C0", lw=1.4, ls="--", label="rate-optimal allocation")
    ax.plot(w, Dl, color="C3", lw=1.4, ls=":", label="leakage-optimal allocation")
    ax.fill_between(w, Dr, SY, where=Dr < SY * (1 - 1e-7), color="C0", alpha=0.18, lw=0)
    ax.fill_between(w, Dl, SY, where=Dl < SY * (1 - 1e-7), color="C3", alpha=0.18, lw=0, hatch="///")
    ax.set_xlabel(r"frequency $\omega$")
    ax.set_ylabel("distortion per frequency")
    ax.set_xlim(0, np.pi)
    ax.set_xticks([0, np.pi / 2, np.pi])
    ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$"])
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.tight_layout()
    fig.savefig("fig_bands.pdf")
    fig.savefig("fig_bands.png", dpi=300)
    return fig


if __name__ == "__main__":
    main()
