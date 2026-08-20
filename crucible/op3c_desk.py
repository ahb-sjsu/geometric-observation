"""OP3-C desk analysis (2026-08-20): reproduce the dynamic-law
re-diagnosis from committed data only (no new measurement, no seal).
See OP3C-DESK.md for the reading.

    python crucible/op3c_desk.py
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.join(r"C:\source\readscope", "calibration", "records",
                   "op3-frontlaw.json")
W = 0.75
P = 4.0


def fit_A(points, gamma):
    s = np.array([q["m"] ** gamma * W ** (P * q["i"]) for q in points])
    y = np.array([q["cos2"] for q in points])
    best = None
    for logA in np.linspace(-12, 6, 400):
        A = np.exp(logA)
        rms = float(np.sqrt(np.mean((s / (s + A) - y) ** 2)))
        if best is None or rms < best[0]:
            best = (rms, A)
    return best


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    d = json.load(open(REC, encoding="utf-8"))
    pts = d["points"]
    seeds = sorted({q["seed"] for q in pts})
    ms = sorted({q["m"] for q in pts})

    print("recovered mass M(m) = sum_i cos2_i, per family seed:")
    for seed in seeds:
        Ms = [sum(q["cos2"] for q in pts
                  if q["seed"] == seed and q["m"] == m) for m in ms]
        rate = float(np.polyfit(np.log(ms), Ms, 1)[0])
        print(f"  seed {seed}: " +
              " ".join(f"M({m})={v:.2f}" for m, v in zip(ms, Ms)) +
              f"  dM={Ms[-1]-Ms[0]:+.2f} rate={rate:.3f}/lnm")

    print("\nsingle-A (gamma=1) law vs two-parameter collapse:")
    for gamma in (1.0, 0.5, 0.4, 0.3, 0.2):
        rms, A = fit_A(pts, gamma)
        def M(m, g=gamma, A=A):
            return sum(m ** g * W ** (P * i) / (m ** g * W ** (P * i) + A)
                       for i in range(16))
        print(f"  gamma={gamma:.1f}: rms={rms:.4f} A={A:.3g} "
              f"M(4)={M(4):.2f} M(1000)={M(1000):.2f} "
              f"dM={M(1000)-M(4):.2f} rate={gamma/np.log(W**-P):.3f}")

    fine = [(g,) + fit_A(pts, g) for g in np.arange(0.15, 1.01, 0.05)]
    g, rms, A = min(fine, key=lambda r: r[1])
    print(f"\npooled best: gamma={g:.2f} (rms {rms:.4f}); "
          f"the budget enters as m^{g:.2f}, not m — the gamma "
          f"derivation is the owed desk item (OP3C-DESK.md).")


if __name__ == "__main__":
    main()
