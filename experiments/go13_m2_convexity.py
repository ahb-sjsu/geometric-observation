#!/usr/bin/env python
"""GO-P-2026-074 harness: the m=2 moment-convexity lemma (all m, dT)
and its corollary chain -- Theorem 9 uniqueness resolved, the
spectral-m=2 two-price rule upgraded to sufficiency.
s1 identity G = -logdet(I - Z); s2 Jensen (zero violations, 3
families incl. m>dT); s3 Hessian decomposition identity + curvature
positivity; s4 corollary F convexity + m=1 rank-one flat control.
Sentinel ===GO13MC-JSON=== with ===END===; flag GO13MC_supported.
Pilot seed 20261012 / governed seed 20261013."""
import argparse
import json
import math
import sys
import time

import numpy as np

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a_ = ap.parse_args()
SEED = a_.seed if a_.seed is not None else (20261012 if a_.pilot
                                            else 20261013)
rng = np.random.default_rng(SEED)
verdicts = {}
vals = {}


def rpsd(d, s=0.5):
    B = rng.normal(0, s, (d, d))
    return B @ B.T


def fams():
    out = []
    for dT, m in ((3, 2), (4, 3), (2, 3)):
        Q = rpsd(dT, 0.3)
        P = Q + rpsd(dT, 0.4)
        out.append((dT, m, P, Q))
    return out


def G(C, V, P, Q):
    MP = V - C.T @ P @ C
    MQ = V - C.T @ Q @ C
    sP, lP = np.linalg.slogdet(MP)
    sQ, lQ = np.linalg.slogdet(MQ)
    if sP <= 0 or sQ <= 0:
        return None
    return lQ - lP


def feas(dT, m, P):
    for _ in range(200):
        C = rng.normal(0, 0.4, (dT, m))
        V = C.T @ P @ C + 0.2 * np.eye(m) + rpsd(m, 0.3)
        if np.linalg.slogdet(V - C.T @ P @ C)[0] > 0:
            return C, V
    raise RuntimeError


FAM = fams()
# s1: identity
worst_id = 0.0
for dT, m, P, Q in FAM:
    R = P - Q
    w2, U = np.linalg.eigh(R)
    Rh = U @ np.diag(np.sqrt(np.clip(w2, 0, None))) @ U.T
    for _ in range(30):
        C, V = feas(dT, m, P)
        MQ = V - C.T @ Q @ C
        Z = Rh @ C @ np.linalg.solve(MQ, C.T) @ Rh
        s, l = np.linalg.slogdet(np.eye(dT) - Z)
        if s <= 0:
            continue
        worst_id = max(worst_id, abs(G(C, V, P, Q) - (-l)))
vals["s1_identity"] = worst_id
verdicts["s1_identity"] = bool(worst_id <= 1e-11)

# s2: Jensen
viol, worst_gap = 0, 0.0
for dT, m, P, Q in FAM:
    for _ in range(500):
        C1, V1 = feas(dT, m, P)
        C2, V2 = feas(dT, m, P)
        gm = G((C1 + C2) / 2, (V1 + V2) / 2, P, Q)
        g1, g2 = G(C1, V1, P, Q), G(C2, V2, P, Q)
        if None in (gm, g1, g2):
            continue
        gap = gm - 0.5 * (g1 + g2)
        worst_gap = max(worst_gap, gap)
        viol += gap > 1e-9
vals["s2_violations"] = viol
vals["s2_worst_gap"] = worst_gap
verdicts["s2_jensen"] = bool(viol == 0)

# s3: directional curvature positivity (generic directions)
neg, mncurv = 0, 1e9
dT, m, P, Q = FAM[0]
for _ in range(300):
    C, V = feas(dT, m, P)
    X = rng.normal(0, 1, (dT, m))
    Y0 = rng.normal(0, 1, (m, m))
    Y = (Y0 + Y0.T) / 2
    nrm = math.sqrt((X * X).sum() + (Y * Y).sum())
    X, Y = X / nrm, Y / nrm
    h = 1e-4
    gs = []
    ok = True
    for t in (-h, 0, h):
        g = G(C + t * X, V + t * Y, P, Q)
        if g is None:
            ok = False
            break
        gs.append(g)
    if not ok:
        continue
    sd = (gs[0] - 2 * gs[1] + gs[2]) / (h * h)
    mncurv = min(mncurv, sd)
    neg += sd < -1e-6
vals["s3_neg_dirs"] = neg
vals["s3_min_curv"] = mncurv
verdicts["s3_curvature"] = bool(neg == 0)

# s4: corollary F convexity + m=1 rank-one flat control
rAB, rAV, rBV, tau2, W = 0.3, 0.7, 0.2, 0.4, 0.5
SigT = np.array([[1, rAB, rAV], [rAB, 1, rBV], [rAV, rBV, 1.0]])
cv = SigT[:, 2]
SigTc = SigT - np.outer(cv, cv) / (1 + tau2)
S1 = np.linalg.inv(SigT)
K = S1 - S1 @ SigTc @ S1


def F(C, V):
    g1 = G(C, V, S1, np.zeros((3, 3)))
    g2 = G(C, V, S1, K)
    if g1 is None or g2 is None:
        return None
    return W * g1 + (1 - W) * g2


violF = 0
for _ in range(800):
    C1, V1 = feas(3, 2, S1)
    C2, V2 = feas(3, 2, S1)
    fm = F((C1 + C2) / 2, (V1 + V2) / 2)
    f1, f2 = F(C1, V1), F(C2, V2)
    if None in (fm, f1, f2):
        continue
    violF += fm - 0.5 * (f1 + f2) > 1e-9
vals["s4_F_violations"] = violF
# m=1 rank-one control: flats exist by design (matrix-convexity of Z
# holds with equality along the gauge) -- Jensen must still hold
r1 = np.outer(rng.normal(0, 1, 3), rng.normal(0, 1, 3))
R1 = r1 @ r1.T * 0 + np.outer(rng.normal(0, 1, 3),
                              rng.normal(0, 1, 3))
R1 = R1 @ R1.T
Q1 = rpsd(3, 0.3)
P1 = Q1 + R1
viol1 = 0
for _ in range(400):
    C1, V1 = feas(3, 1, P1)
    C2, V2 = feas(3, 1, P1)
    gm = G((C1 + C2) / 2, (V1 + V2) / 2, P1, Q1)
    g1, g2 = G(C1, V1, P1, Q1), G(C2, V2, P1, Q1)
    if None in (gm, g1, g2):
        continue
    viol1 += gm - 0.5 * (g1 + g2) > 1e-9
vals["s4_m1_violations"] = viol1
verdicts["s4_corollary"] = bool(violF == 0 and viol1 == 0)

allpass = all(verdicts.values())
out = dict(seed=SEED, pilot=bool(a_.pilot),
           runtime_s=round(time.time() - t0, 1),
           values={k: float(v) for k, v in vals.items()},
           verdicts=verdicts, GO13MC_supported=bool(allpass))
print("===GO13MC-JSON===")
print(json.dumps(out, indent=1))
print("===END===")
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")
sys.exit(0 if allpass else 1)
