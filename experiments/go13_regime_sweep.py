# GO-13 EXPLORATORY (unregistered, disclosed): global regime map of
# sign(dCT_W/dq) via the 068-netted envelope sign law. Grid: 6
# correlation triples x 3 distortion pairs at q=0.5, w=0.5, seed
# 20260925. Findings (full table in the commit / tex remark):
#   - dCT/dq > 0 at 16/18 non-degenerate grid points: the dynamic tax
#     GENERICALLY RISES with staleness.
#   - Decreases are shallow slivers (|dCT/dq| < 1e-3) and occur only
#     when the binding consumer is the context-RICH one.
#   - When the binding consumer is context-poor the rise is strong,
#     10/10 points, up to +0.286 bits/unit-q at r=(0.0,0.8,0.3),
#     D=(0.2,0.2).
#   - The candidate iff-law ("rises iff binding is context-poor")
#     FAILS at 6/18 points and is recorded as refuted-as-iff; the
#     surviving statement is the asymmetry above.
# Exploratory grade: no claim beyond [exploratory]; the 069 face
# gates the rising regime operationally.
# (Script body identical to scratchpad/regime_sweep.py, seed 20260925.)
import itertools
import math
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(20260925)
L2 = 2 * math.log(2)


def prog2(SigT, cvec, q, DA, DB, W, starts=25):
    SigTc = SigT - (1 - q) * np.outer(cvec, cvec)

    def unpack(p):
        A = p[:6].reshape(2, 3)
        Lc = np.array([[math.exp(min(p[6], 20)), 0],
                       [p[7], math.exp(min(p[8], 20))]])
        return A, Lc @ Lc.T

    def obj(p):
        A, SN = unpack(p)
        dn = np.linalg.det(SN)
        return (W * math.log(np.linalg.det(A @ SigT @ A.T + SN) / dn)
                + (1 - W) * math.log(
                    np.linalg.det(A @ SigTc @ A.T + SN) / dn))

    cons = []
    for i, Dv in ((0, DA), (1, DB)):
        def c(p, i=i, Dv=Dv):
            A, SN = unpack(p)
            d = np.eye(3)[i] - A[i]
            return Dv - (float(d @ SigT @ d) + SN[i, i])
        cons.append({"type": "ineq", "fun": c})
    best, bp = None, None
    for _ in range(starts):
        p0 = np.concatenate([
            (np.eye(2, 3) * rng.uniform(0.3, 0.9)).ravel()
            + rng.normal(0, 0.05, 6),
            [math.log(rng.uniform(5e-3, 0.3)), rng.uniform(-0.1, 0.1),
             math.log(rng.uniform(5e-3, 0.3))]])
        r = minimize(obj, p0, constraints=cons, method="SLSQP",
                     options={"maxiter": 2000, "ftol": 1e-13})
        if r.success and (best is None or r.fun < best):
            best, bp = r.fun, r.x
    A = bp[:6].reshape(2, 3)
    Lc = np.array([[math.exp(min(bp[6], 20)), 0],
                   [bp[7], math.exp(min(bp[8], 20))]])
    SN = Lc @ Lc.T
    M1 = A @ SigTc @ A.T + SN
    Ac = A @ cvec
    return best / L2, float(Ac @ np.linalg.solve(M1, Ac))


def prog1(SigT, cvec, q, i, Dv, W, starts=20):
    SigTc = SigT - (1 - q) * np.outer(cvec, cvec)
    y0 = np.eye(3)[i]

    def obj(p):
        u, nv = p[:3], math.exp(min(p[3], 20))
        return (W * math.log((u @ SigT @ u + nv) / nv)
                + (1 - W) * math.log((u @ SigTc @ u + nv) / nv))

    def c(p):
        u, nv = p[:3], math.exp(min(p[3], 20))
        d = y0 - u
        return Dv - (float(d @ SigT @ d) + nv)

    best, bp = None, None
    for _ in range(starts):
        p0 = np.concatenate([y0 * rng.uniform(0.3, 0.9)
                             + rng.normal(0, 0.05, 3),
                             [math.log(rng.uniform(1e-3, 0.3))]])
        r = minimize(obj, p0, constraints=[{"type": "ineq", "fun": c}],
                     method="SLSQP",
                     options={"maxiter": 2000, "ftol": 1e-13})
        if r.success and (best is None or r.fun < best):
            best, bp = r.fun, r.x
    u, nv = bp[:3], math.exp(min(bp[3], 20))
    Q1 = float(u @ (SigTc @ u))
    return best / L2, float((u @ cvec) ** 2 / (Q1 + nv))


rows = []
law_ok, law_n = 0, 0
grid_r = [(0.3, 0.7, 0.2), (-0.2, 0.5, 0.6), (0.1, 0.6, -0.4),
          (0.5, 0.4, 0.4), (0.0, 0.8, 0.3), (0.4, 0.3, 0.75)]
grid_D = [(0.2, 0.2), (0.15, 0.4), (0.4, 0.15)]
q, W = 0.5, 0.5
for rv, (DA, DB) in itertools.product(grid_r, grid_D):
    try:
        SigT = np.array([[1, rv[0], rv[1]], [rv[0], 1, rv[2]],
                         [rv[1], rv[2], 1.0]])
        if np.linalg.eigvalsh(SigT)[0] <= 1e-6:
            continue
        cvec = SigT[:, 2].copy()
        J, sJ = prog2(SigT, cvec, q, DA, DB, W)
        LA, sA = prog1(SigT, cvec, q, 0, DA, W)
        LB, sB = prog1(SigT, cvec, q, 1, DB, W)
        bind = 0 if LA >= LB else 1
        sbind = sA if bind == 0 else sB
        dCT = (1 - W) * (sJ - sbind) / L2
        # candidate law: rises iff binding consumer's own coupling
        # is the SMALLER of the two consumers' couplings
        poor = 0 if sA < sB else 1
        law_pred = (bind == poor)
        obs_rise = dCT > 1e-4
        flat = abs(dCT) <= 1e-4
        if not flat:
            law_n += 1
            law_ok += int(law_pred == obs_rise)
        rows.append((rv, DA, DB, "AB"[bind], dCT, "AB"[poor], flat))
        print(f"r={rv} D=({DA},{DB}): bind={'AB'[bind]} "
              f"poor={'AB'[poor]} dCT={dCT:+.5f}"
              f"{' FLAT' if flat else ''}")
    except Exception as e:
        print(f"r={rv} D=({DA},{DB}): SKIP {e}")
print(f"\ncandidate law (rises iff binding is context-poor): "
      f"{law_ok}/{law_n} non-flat points")
