"""OT-1 Arms S and R, constants per PREREG-OT1.md (sealed 2026-08-15).

Arm S: rank-1 synthetic consumers, the cos^2(theta) ratio curve (S1)
and the 45-degree codec-preference flip (S2).
Arm R: rank-4 operators, trace-ratio prediction with no refit (R1).

    .venv/Scripts/python crucible/ot1_arms_sr.py
"""

from __future__ import annotations

import json
import os

import numpy as np

SEED = 20260815
D = 64
EPS = 0.01
SIGMA_X = 0.125          # |pre-activation| <= 0.5 at 4 sigma
N = 10_000
THETAS = [0, 15, 30, 45, 60, 75, 90]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "OT1-arms-sr.json")


def consumer(a):
    return lambda x: np.tanh(x @ a)


def damage(c, xs, deltas):
    d0 = c(xs)
    return float(np.mean((c(xs + deltas) - d0) ** 2))


def arm_s(rng):
    e1 = np.zeros(D)
    e1[0] = 1.0
    e2 = np.zeros(D)
    e2[1] = 1.0
    xs = rng.normal(scale=SIGMA_X, size=(N, D))
    s_dirs = rng.normal(size=N)
    rows, s1_dev = [], 0.0
    flips = {}
    for th in THETAS:
        t = np.deg2rad(th)
        a1 = e1
        a2 = np.cos(t) * e1 + np.sin(t) * e2
        c1, c2 = consumer(a1), consumer(a2)
        # L1: directional perturbation along a1
        deltas = EPS * s_dirs[:, None] * a1[None, :]
        d1 = damage(c1, xs, deltas)
        d2 = damage(c2, xs, deltas)
        ratio = d2 / d1
        dev = abs(ratio - np.cos(t) ** 2)
        s1_dev = max(s1_dev, dev)
        # L2: codecs A (along a1) and B (along b, b perp a1 in the plane)
        b = e2  # for every theta, the in-plane direction orthogonal to a1
        deltas_b = EPS * s_dirs[:, None] * b[None, :]
        pref = {}
        for name, dd in (("A", deltas), ("B", deltas_b)):
            pref[name] = (damage(c1, xs, dd), damage(c2, xs, dd))
        c1_prefers = "A" if pref["A"][0] < pref["B"][0] else "B"
        c2_prefers = "A" if pref["A"][1] < pref["B"][1] else "B"
        flips[th] = {"c1": c1_prefers, "c2": c2_prefers,
                     "agree": c1_prefers == c2_prefers}
        rows.append({"theta": th, "ratio": round(ratio, 4),
                     "cos2": round(np.cos(t) ** 2, 4),
                     "dev": round(dev, 4)})
    s1 = s1_dev <= 0.05
    agree_low = all(flips[th]["agree"] for th in (0, 15, 30))
    disagree_high = all(not flips[th]["agree"] for th in (60, 75, 90))
    s2 = agree_low and disagree_high
    return rows, flips, s1, s2, s1_dev


def arm_r(rng):
    errs = []
    for _ in range(20):
        frames = []
        for _ in range(2):
            q, _r = np.linalg.qr(rng.normal(size=(D, 4)))
            frames.append(q[:, :4])
        lam = np.sort(10 ** rng.uniform(-1, 0, 4))[::-1]
        ps = [f @ np.diag(lam) @ f.T for f in frames]
        w = rng.normal(size=D)
        w /= np.linalg.norm(w)
        pred = np.trace(ps[1] @ np.outer(w, w)) / \
            np.trace(ps[0] @ np.outer(w, w))
        xs = rng.normal(scale=SIGMA_X, size=(N, D))
        s_dirs = rng.normal(size=N)
        deltas = EPS * s_dirs[:, None] * w[None, :]
        meas = []
        for f in frames:
            # vector-valued consumer: C(x)_j = sqrt(lam_j) tanh(u_j.x),
            # damage in its own (G = I) norm — this realizes exactly
            # P = f diag(lam) f.T as the read operator; a scalar sum
            # would realize a rank-1 operator instead (see OT1 notes).
            wts = np.sqrt(lam)
            d0 = np.tanh(xs @ f) * wts
            d1 = np.tanh((xs + deltas) @ f) * wts
            meas.append(float(np.mean(np.sum((d1 - d0) ** 2, axis=1))))
        errs.append(abs(meas[1] / meas[0] - pred) / pred)
    r1 = max(errs) <= 0.10
    return errs, r1


def main():
    rng = np.random.default_rng(SEED)
    rows, flips, s1, s2, s1_dev = arm_s(rng)
    print("Arm S — ratio curve (bar: max dev <= 0.05):")
    for r_ in rows:
        print(f"  theta={r_['theta']:>2}  measured={r_['ratio']:.4f}  "
              f"cos2={r_['cos2']:.4f}  dev={r_['dev']:.4f}")
    print(f"  S1 max dev = {s1_dev:.4f} -> {'PASS' if s1 else 'FAIL'}")
    print("  flip:", {t: f"{v['c1']}/{v['c2']}" for t, v in flips.items()},
          f"-> S2 {'PASS' if s2 else 'FAIL'}")
    errs, r1 = arm_r(rng)
    print(f"\nArm R — 20 constructions, max rel err = {max(errs):.4f} "
          f"(bar 0.10) -> {'PASS' if r1 else 'FAIL'}")
    json.dump({"claim": "OT-1-arms-SR", "seed": SEED, "S_curve": rows,
               "S_flips": {str(k): v for k, v in flips.items()},
               "S1": bool(s1), "S2": bool(s2),
               "R_errs": [round(float(e), 4) for e in errs],
               "R1": bool(r1)},
              open(OUT, "w"), indent=1)
    print(f"\nArms S/R: {'PASS' if (s1 and s2 and r1) else 'FAIL'} "
          f"-> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
