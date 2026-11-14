"""Distortion sweep for the disjoint-bands instance of Section IX.

For each budget D / D_max it solves the rate-optimal and the leakage-optimal
allocation on a grid of 512 frequencies and records how many frequencies each
describes, how many both describe, and the two cost penalties.  It then
bisects for the budget at which the two described sets first overlap.

Run:  python sweep_bands.py      (writes sweep_bands.json, about one minute)
"""
import json

import numpy as np

import spectral_core as sc

N = 512
TAU2 = 0.25


def instance(n=N):
    w = 2 * np.pi * np.arange(n) / n
    low = np.cos(w / 2) ** 2
    SY = 1.6 * low + 1.0 * (1 - low)
    kap = 0.02 * low + 0.90 * (1 - low)
    blocks = []
    for k in range(n):
        c = np.sqrt(kap[k] * SY[k])
        Rt = sc.psd_sqrt(np.array([[SY[k], c], [c, 1.0]], dtype=complex))
        blocks.append((sc.herm(Rt @ np.diag([1.0, 0.0]) @ Rt), np.array([[0.0, 1.0]], dtype=complex) @ Rt,
                       np.array([[TAU2]], dtype=complex)))
    return w, SY, kap, blocks


def at(frac, SY, blocks):
    wts = np.full(len(blocks), 1.0 / len(blocks))
    D = frac * SY.mean()
    rt = sc.solve(blocks, wts, 1.0, D)
    lk = sc.solve(blocks, wts, 0.0, D)
    ar = rt["Db"] < SY * (1 - 1e-7)
    al = lk["Db"] < SY * (1 - 1e-7)
    return dict(frac=frac, D=D, bands_rate=int(ar.sum()), bands_leak=int(al.sum()), overlap=int((ar & al).sum()),
                R_min=rt["R"], L_of_rate_opt=rt["L"], L_min=lk["L"], R_of_leak_opt=lk["R"],
                leak_factor=rt["L"] / lk["L"], rate_factor=lk["R"] / rt["R"])


def main():
    w, SY, kap, blocks = instance()
    rows = [at(f, SY, blocks) for f in (0.50, 0.70, 0.80, 0.90, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99)]
    lo, hi = 0.90, 0.97                       # overlap at lo, none at hi
    assert at(lo, SY, blocks)["overlap"] > 0 and at(hi, SY, blocks)["overlap"] == 0
    for _ in range(14):
        mid = 0.5 * (lo + hi)
        if at(mid, SY, blocks)["overlap"] > 0:
            lo = mid
        else:
            hi = mid
    out = dict(grid=N, tau2=TAU2, rows=rows, onset_lo=lo, onset_hi=hi)
    json.dump(out, open("sweep_bands.json", "w"), indent=1)
    print(" D/Dmax  rate-bands leak-bands overlap   R_min    L(rate-opt)  L_min    R(leak-opt)  L-factor R-factor")
    for r in rows:
        print(f"{r['frac']:7.2f} {r['bands_rate']:10d} {r['bands_leak']:10d} {r['overlap']:7d}  {r['R_min']:.5f}   {r['L_of_rate_opt']:.5f}   "
              f"{r['L_min']:.5f}   {r['R_of_leak_opt']:.5f}    {r['leak_factor']:.2f}    {r['rate_factor']:.2f}")
    print(f"described sets are disjoint on this grid for D/Dmax >= {hi:.4f} and overlap at {lo:.4f}")
    return out


if __name__ == "__main__":
    main()
