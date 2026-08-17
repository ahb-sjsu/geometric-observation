"""FP3N shakedown — the noisy-cliff measurement family (P3's owed
prediction, theorem half in OT3-NOISY-THEOREM.md). No bars, no
evidential weight: this run exists to show the family's interior.

The family instantiates the theorem's oracle model exactly:
noisy symmetric blocks Y = V^T P V + Xi with Xi_ij ~ N(0, sigma^2)
symmetrized, planted rank-r spectra, oblivious designs.

Two faces to exhibit:
- k = d: eigenspace error linear in sigma with slope ~ sqrt(d)/gamma
  (N2a), graded later on the slope's (d, gamma) scaling;
- k = d-1 with the adversarial T1b plant (leading eigenvector half
  inside the hidden direction): error flat in sigma at ~1/sqrt(2)
  (N1a's face; typical-position plants would hide the cliff, so the
  family plants the worst case on purpose).

Interior requirements (committed before any seal may cite this
family): a sigma grid with >= 2 points on each side of gamma/sqrt(d)
and >= 2 interior points (error in (0.05, 0.7)) at k = d; linearity
ratio within 20% across the sub-saturation decade; the k = d-1 face
flat within 10% across the DECISIVE BAND x <= 0.3 (above it noise
exceeds the spectrum and both faces saturate -- physics, not
family); trial IQR under a third of the face separation in-band.

    .venv/Scripts/python crucible/fam_p3n_shakedown.py
"""

from __future__ import annotations

import json
import os

import numpy as np

SEED = 20260817
DIMS = [16, 32, 64]
SPECTRA = {"gapA": [1.0, 0.8, 0.5, 0.2], "gapB": [1.0, 0.95, 0.9, 0.8]}
X_GRID = [0.03, 0.1, 0.3, 1.0, 3.0]      # sigma = x * gamma / sqrt(d)
TRIALS = 20
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "FP3N-shakedown.json")


def sym_noise(rng, d, sigma):
    a = rng.normal(0.0, sigma, (d, d))
    return np.triu(a) + np.triu(a, 1).T


def sin_theta(u_hat, u_true):
    """Largest principal angle's sine between equal-rank frames."""
    q = u_true.T @ u_hat
    s = np.linalg.svd(q, compute_uv=False)
    return float(np.sqrt(max(0.0, 1.0 - s.min() ** 2)))


def cell_full(rng, d, lam, sigma):
    """k = d: observe the full noisy block in a random basis."""
    r = len(lam)
    basis = np.linalg.qr(rng.standard_normal((d, d)))[0]
    u = basis[:, :r]
    p = u @ np.diag(lam) @ u.T
    v = np.linalg.qr(rng.standard_normal((d, d)))[0]
    y = v.T @ p @ v + sym_noise(rng, d, sigma)
    p_hat = v @ ((y + y.T) / 2) @ v.T
    w, vec = np.linalg.eigh(p_hat)
    return sin_theta(vec[:, ::-1][:, :r], u)


def cell_confined(rng, d, lam, sigma):
    """k = d-1, adversarial plant: leading eigenvector = (e+w)/sqrt2
    with w orthogonal to the observed subspace V."""
    r = len(lam)
    basis = np.linalg.qr(rng.standard_normal((d, d)))[0]
    w_hid = basis[:, 0]
    e = basis[:, 1]
    rest = basis[:, 2:r + 1]
    u1 = (e + w_hid) / np.sqrt(2.0)
    u = np.column_stack([u1, rest])
    p = u @ np.diag(lam) @ u.T
    v = basis[:, 1:]                     # spans w_hid's complement
    y = v.T @ p @ v + sym_noise(rng, d - 1, sigma)
    w_eig, vec = np.linalg.eigh((y + y.T) / 2)
    u_hat = v @ vec[:, ::-1][:, :r]
    return sin_theta(u_hat, u)


def cell_sideinfo(rng, d, k0, lam, sigma, confined):
    """N4 arm: promise range(P) in W, dim W = d - k0. Full coverage
    of W (k = d-k0) should behave as the upper face with d_eff = d-k0;
    one-short-of-W with the adversarial plant inside W as the lower."""
    r = len(lam)
    basis = np.linalg.qr(rng.standard_normal((d, d)))[0]
    w_basis = basis[:, :d - k0]
    if confined:
        w_hid = w_basis[:, 0]
        e = w_basis[:, 1]
        rest = w_basis[:, 2:r + 1]
        u = np.column_stack([(e + w_hid) / np.sqrt(2.0), rest])
        v = w_basis[:, 1:]
    else:
        u = w_basis[:, :r]
        v = w_basis
    p = u @ np.diag(lam) @ u.T
    kdim = v.shape[1]
    y = v.T @ p @ v + sym_noise(rng, kdim, sigma)
    w_eig, vec = np.linalg.eigh((y + y.T) / 2)
    u_hat = v @ vec[:, ::-1][:, :r]
    return sin_theta(u_hat, u)


def main():
    rng = np.random.default_rng(SEED)
    out = {"family": "FP3N", "seed": SEED, "x_grid": X_GRID,
           "trials": TRIALS, "cells": []}
    for d in DIMS:
        for name, lam in SPECTRA.items():
            gamma = lam[-1]
            for x in X_GRID:
                sigma = x * gamma / np.sqrt(d)
                full = [cell_full(rng, d, lam, sigma)
                        for _ in range(TRIALS)]
                conf = [cell_confined(rng, d, lam, sigma)
                        for _ in range(TRIALS)]
                cell = {
                    "d": d, "spectrum": name, "gamma": gamma, "x": x,
                    "sigma": round(sigma, 6),
                    "full_median": round(float(np.median(full)), 4),
                    "full_iqr": round(float(np.subtract(
                        *np.percentile(full, [75, 25]))), 4),
                    "confined_median": round(
                        float(np.median(conf)), 4),
                    "confined_iqr": round(float(np.subtract(
                        *np.percentile(conf, [75, 25]))), 4),
                }
                out["cells"].append(cell)
                print(f"d={d:>3} {name} x={x:<5} sigma={sigma:.4f}  "
                      f"k=d {cell['full_median']:.3f} "
                      f"(iqr {cell['full_iqr']:.3f})   "
                      f"k=d-1 {cell['confined_median']:.3f} "
                      f"(iqr {cell['confined_iqr']:.3f})")

    # interior evidence, printed (graded by eye here, by bars later)
    print("\nINTERIOR EVIDENCE")
    for d in DIMS:
        for name in SPECTRA:
            cs = [c for c in out["cells"]
                  if c["d"] == d and c["spectrum"] == name]
            interior = [c for c in cs
                        if 0.05 < c["full_median"] < 0.7]
            sub = [c for c in cs if c["x"] in (0.03, 0.1, 0.3)]
            lin = (sub[1]["full_median"] / max(sub[0]["full_median"],
                                               1e-9) / (0.1 / 0.03),
                   sub[2]["full_median"] / max(sub[1]["full_median"],
                                               1e-9) / (0.3 / 0.1))
            # decisive band: x <= 0.3 -- above it noise exceeds the
            # spectrum and BOTH faces saturate at ~1 (no design can
            # distinguish anything there; that is physics, not family)
            band = [c for c in cs if c["x"] <= 0.3]
            conf_band = [c["confined_median"] for c in band]
            flat = (max(conf_band) - min(conf_band)) / max(conf_band)
            sep = min(c["confined_median"] - c["full_median"]
                      for c in band)
            print(f"  d={d:>3} {name}: interior pts "
                  f"{len(interior)} (need >=2); linearity ratios "
                  f"{lin[0]:.2f}, {lin[1]:.2f} (want ~1); decisive "
                  f"band x<=0.3: confined face flat to {flat:.1%} at "
                  f"{np.median(conf_band):.3f}, min face separation "
                  f"{sep:.3f}")
    # N4 arm: the cliff relocates to d - k0
    print("\nN4 ARM (side information, d=32)")
    d = 32
    for k0 in (8, 16):
        for name, lam in SPECTRA.items():
            gamma = lam[-1]
            deff = d - k0
            for x in X_GRID:
                sigma = x * gamma / np.sqrt(deff)
                full = [cell_sideinfo(rng, d, k0, lam, sigma, False)
                        for _ in range(TRIALS)]
                conf = [cell_sideinfo(rng, d, k0, lam, sigma, True)
                        for _ in range(TRIALS)]
                cell = {"arm": "N4", "d": d, "k0": k0,
                        "spectrum": name, "gamma": gamma, "x": x,
                        "sigma": round(sigma, 6),
                        "full_median": round(float(np.median(full)), 4),
                        "confined_median": round(
                            float(np.median(conf)), 4)}
                out["cells"].append(cell)
                if x <= 0.3:
                    print(f"  k0={k0:>2} {name} x={x:<5} "
                          f"W-full {cell['full_median']:.3f}  "
                          f"W-minus-one {cell['confined_median']:.3f}")

    json.dump(out, open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}  (shakedown, no verdict)")


if __name__ == "__main__":
    main()
