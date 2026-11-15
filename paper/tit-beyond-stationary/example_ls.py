"""Worked example for the time-frequency water-filling theorem.

The source is the two-dimensional time-varying moving average of
verify_ls.py (Proposition "tvma").  The decoder wants one linear
combination of the two components, and the holder sees another one in
noise.  The script solves the time-frequency program at the rate-only
weight and at the leakage-only weight, at one distortion, and writes

  fig_ls.pdf / fig_ls.png   three maps over (time, frequency): the power of
                            the described part, and the rate spent at each
                            point by the two optimal descriptions
  example_ls.json           the numbers quoted in the text

numpy and matplotlib only.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tit-stationary"))
import spectral_core as sc  # noqa: E402
from verify_ls import source_vector, vec_cost  # noqa: E402

G, W = 40, 64          # time and frequency grid (frequency over [0, pi] is shown)
FRAC = 0.35


def solve_ls(src, alpha, D):
    us = [(j + 0.5) / G for j in range(G)]
    ws = [2 * np.pi * k / W for k in range(W)]
    blocks = [src.block(u, w) for u in us for w in ws]
    sol = sc.solve(blocks, np.full(G * W, 1.0 / (G * W)), alpha, D)
    return sol, np.array(sol["Rb"]).reshape(G, W), np.array(sol["Lb"]).reshape(G, W), \
        np.array(sol["Db"]).reshape(G, W)


def main():
    src = source_vector()
    dm = src.dmax(G, W)
    D = FRAC * dm
    power = np.array([[np.real(np.trace(src.Q @ src.sigma((j + 0.5) / G, 2 * np.pi * k / W)))
                       for k in range(W)] for j in range(G)])
    out = dict(D_over_Dmax=FRAC, Dmax=dm, grid=[G, W])
    maps = {}
    for name, alpha in (("rate_optimal", 1.0), ("leakage_optimal", 0.0)):
        sol, Rb, Lb, Db = solve_ls(src, alpha, D)
        maps[name] = Rb
        active = Rb > 1e-9
        out[name] = dict(rate=sol["R"], leakage=sol["L"], level=sol["nu"],
                         fraction_of_plane_described=float(active.mean()),
                         rate_first_half_of_time=float(Rb[:G // 2].mean() / 2),
                         rate_second_half_of_time=float(Rb[G // 2:].mean() / 2))
    both = (maps["rate_optimal"] > 1e-9) & (maps["leakage_optimal"] > 1e-9)
    either = (maps["rate_optimal"] > 1e-9) | (maps["leakage_optimal"] > 1e-9)
    out["described_by_both_over_either"] = float(both.sum() / max(1, either.sum()))

    # the stationary source with the time-averaged spectrum
    blocks = []
    for k in range(W):
        w = 2 * np.pi * k / W
        Sbar = sum(src.sigma((j + 0.5) / G, w) for j in range(G)) / G
        Rb_ = sc.psd_sqrt(Sbar)
        blocks.append((sc.herm(Rb_ @ src.Q @ Rb_), src.H @ Rb_, src.SU.astype(complex)))
    for name, alpha in (("rate_optimal", 1.0), ("leakage_optimal", 0.0)):
        sol = sc.solve(blocks, np.full(W, 1.0 / W), alpha, D)
        out[name]["averaged_spectrum_cost"] = sol["cost"]
        out[name]["cost"] = out[name]["rate"] if alpha == 1.0 else out[name]["leakage"]

    # finite windows
    out["window"] = {}
    for name, alpha in (("rate_optimal", 1.0), ("leakage_optimal", 0.0)):
        out["window"][name] = {str(N): vec_cost(src.cov(N), src.Q, src.H, src.SU, alpha, D) for N in (16, 32, 64)}

    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(out, open(os.path.join(here, "example_ls.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "serif", "font.size": 9})
    half = W // 2 + 1
    ext = [0, 1, 0, np.pi]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.5), sharey=True)
    panels = [(power, "(a) power of the described part"),
              (maps["rate_optimal"], "(b) rate spent, least rate"),
              (maps["leakage_optimal"], "(c) rate spent, least leakage")]
    for ax, (M, title) in zip(axes, panels):
        im = ax.imshow(M[:, :half].T, origin="lower", aspect="auto", extent=ext, cmap="Greys")
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("time $u$")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    axes[0].set_ylabel(r"frequency $\omega$")
    axes[0].set_yticks([0, np.pi / 2, np.pi])
    axes[0].set_yticklabels(["0", r"$\pi/2$", r"$\pi$"])
    fig.tight_layout()
    fig.savefig(os.path.join(here, "fig_ls.pdf"))
    fig.savefig(os.path.join(here, "fig_ls.png"), dpi=300)
    return 0


if __name__ == "__main__":
    sys.exit(main())
