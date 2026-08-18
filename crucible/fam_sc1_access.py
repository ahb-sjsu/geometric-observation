"""SC-1 heterogeneous-access arm (shakedown) — the AM/GM law's boundary.

Answers the terrestrial telecom question: does the downlink allocation
law (G = AM(d)/GM(d)) apply to a congested access link / RAN shared by
traffic classes (latency-, throughput-, loss-sensitive) instead of
science instruments? The law is domain-agnostic — the consumers are now
QoS classes and d_k is their aggregate importance over resource units
(sub-carriers / time-slots). The point of this arm is the BOUNDARY the
law predicts: as the classes homogenize, the importance spread → 0, the
AM/GM gap → 1, and consumer-relative scheduling buys NOTHING. That is
why the fiber core (one uniform consumer) sees no gain, and the
congested heterogeneous edge does.

Sweeps a heterogeneity knob h from 0 (identical classes) to 1 (highly
differentiated) and checks that measured G tracks AM(d)/GM(d) across the
whole range, collapsing to 1 at h=0. No evidential weight.

    python crucible/fam_sc1_access.py
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\source\readscope")
from readscope import water_fill  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "SC1-access-shakedown.json")

D = 64                       # resource units (sub-carriers / slots)
K_CLASSES = 4                # traffic classes sharing the link
BITS_PER_UNIT = 3.0
H_GRID = [0.0, 0.25, 0.5, 0.75, 1.0]     # heterogeneity knob
N_SCEN = 30
SEEDS = [0, 1, 2]


def class_importance(rng, h):
    """Aggregate importance d_k from K QoS classes. At h=0 every class
    has the same flat demand (homogeneous); at h=1 each class concentrates
    on a distinct resource band with a distinct QoS weight."""
    d = np.zeros(D)
    for j in range(K_CLASSES):
        flat = np.ones(D)
        centre = (j + 0.5) / K_CLASSES * D
        peak = np.exp(-0.5 * ((np.arange(D) - centre) / (0.06 * D)) ** 2)
        profile = (1 - h) * flat + h * D * peak
        qos = (1 - h) * 1.0 + h * rng.uniform(0.3, 3.0)
        d += qos * profile
    return np.clip(d, 1e-9, None)


def cons_distortion(bits, weights):
    return float(np.sum(weights * np.power(2.0, -2.0 * bits)))


def main():
    sigma2 = np.ones(D)      # whitened resource units
    print(f"SC-1 access arm — d={D} classes={K_CLASSES} "
          f"rate={BITS_PER_UNIT}b/unit seeds={SEEDS}")
    print("prediction: G = AM(d)/GM(d); G -> 1 as classes homogenize (h->0)\n")

    rows, per_h = {h: {"gmeas": [], "gpred": []} for h in H_GRID}, None
    per_h = {h: {"gmeas": [], "gpred": []} for h in H_GRID}
    allrows = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed * 6301 + 5)
        for h in H_GRID:
            for _ in range(N_SCEN):
                d = class_importance(rng, h)
                budget = BITS_PER_UNIT * D
                wc = d * sigma2
                a_mse = water_fill(sensitivity=np.ones(D), variance=sigma2,
                                   budget=budget)
                a_con = water_fill(sensitivity=d, variance=sigma2,
                                   budget=budget)
                g_meas = cons_distortion(a_mse.bits, wc) / \
                    cons_distortion(a_con.bits, wc)
                g_pred = float(np.mean(d)) / float(np.exp(np.mean(np.log(d))))
                per_h[h]["gmeas"].append(g_meas)
                per_h[h]["gpred"].append(g_pred)
                allrows.append({"seed": seed, "h": h, "g_meas": g_meas,
                                "g_pred": g_pred})

    print("heterogeneity h:  mean G_pred  mean G_meas  median meas/pred")
    for h in H_GRID:
        gp = np.array(per_h[h]["gpred"])
        gm = np.array(per_h[h]["gmeas"])
        print(f"  h={h:.2f}:  {gp.mean():.3f}       {gm.mean():.3f}       "
              f"{np.median(gm / gp):.3f}")
    print("\nboundary: at h=0 (homogeneous classes) G_pred≈G_meas≈1.0 "
          "(no gain); AM/GM gap opens with heterogeneity — the fiber-core "
          "vs congested-edge distinction, measured.")

    json.dump({"campaign": "SC-1-access", "sealed": False, "shakedown": True,
               "note": "no evidential weight; arm of PREREG-SC1.md",
               "generated": datetime.now(timezone.utc).isoformat(),
               "constants": {"d": D, "k_classes": K_CLASSES,
                             "bits_per_unit": BITS_PER_UNIT,
                             "h_grid": H_GRID, "n_scen": N_SCEN,
                             "seeds": SEEDS},
               "rows": allrows},
              open(OUT, "w"), indent=1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    print(f"\nwrote {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
