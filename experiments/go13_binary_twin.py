#!/usr/bin/env python
"""GO-P-2026-072 harness: the binary twin (GO-13 Theorem 3).
s1 slice collapse q_eff = q*delta; s2 closed form + generalized tilt
vs direct channel optimization (two-sample class, 3 distortions);
s3 exact non-collapse of single-q universality (gap >> precision;
envelope REPORTED, near-universality stays a numerical observation);
s4 anchors (Delta=0 slice; useless context).
Sentinel ===GO13BT-JSON=== with ===END===; flag GO13BT_supported.
Pilot seed 20261006 / governed seed 20261007."""
import argparse
import json
import sys
import time

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a_ = ap.parse_args()
SEED = a_.seed if a_.seed is not None else (20261006 if a_.pilot
                                            else 20261007)
verdicts = {}
vals = {}
import math
import numpy as np
from scipy.optimize import minimize, minimize_scalar, brentq

p, f, q = 0.25, 0.15, 0.1
rng = np.random.default_rng(SEED)


def h2(x):
    return 0.0 if x <= 0 or x >= 1 else -(x * math.log2(x)
                                          + (1 - x) * math.log2(1 - x))


def ell(x):
    return math.log((1 - x) / x)


def conv(a_, b_):
    return a_ * (1 - b_) + (1 - a_) * b_


def delta(D_):
    return 0.5 * (1 - (1 - 2 * f) ** D_)


def thm10(D, qv):
    lo = max(0.0, (D - p) / (1 - p)) + 1e-12
    hi = min(1.0, D / (1 - p)) - 1e-12

    def L(d0):
        d1 = (D - (1 - p) * d0) / p
        a_ = (1 - p) * d0 + p * (1 - d1)
        return h2(conv(a_, qv)) - (1 - p) * h2(d0) - p * h2(d1)

    r = minimize_scalar(L, bounds=(lo, hi), method="bounded",
                        options={"xatol": 1e-13})
    return L(r.x)



def chain_prob(sites, vs, vt):
    """P(V at sites = vs | V_t = vt) * 1/2: each side chains
    independently from t (Markov, conditional independence given V_t);
    parent of a site = nearest already-placed site on the SAME side."""
    pr = 0.5
    state = {0: vt}
    for off, val in sorted(zip(sites, vs), key=lambda z: abs(z[0])):
        cand = [o for o in state if o == 0 or (o > 0) == (off > 0)]
        par = max(cand, key=abs) if any(o != 0 for o in cand) else 0
        d_ = delta(abs(off - par))
        pr *= (1 - d_) if val == state[par] else d_
        state[off] = val
    return pr

def rel_dist(idx):
    """Posterior reliability distribution of V_t given S at offsets
    idx (exact enumeration over V-values at the needed sites + t)."""
    sites = sorted(set(idx))
    m = len(sites)
    atoms = {}
    for vt in (0, 1):
        for vv in range(1 << m):
            vs = [(vv >> i) & 1 for i in range(m)]
            pr = chain_prob(sites, vs, vt)
            for sv in range(1 << m):
                ss = [(sv >> i) & 1 for i in range(m)]
                ps = pr
                for k in range(m):
                    ps *= (1 - q) if ss[k] == vs[k] else q
                key = tuple(ss)
                d0_, d1_ = atoms.get(key, (0.0, 0.0))
                if vt == 0:
                    atoms[key] = (d0_ + ps, d1_)
                else:
                    atoms[key] = (d0_, d1_ + ps)
    out = []
    for key, (a0, a1) in atoms.items():
        tot = a0 + a1
        out.append((tot, min(a0, a1) / tot))
    return out                                   # [(P(g), r_g)]


def L_closed(D, rd):
    lo = max(0.0, (D - p) / (1 - p)) + 1e-12
    hi = min(1.0, D / (1 - p)) - 1e-12

    def L(d0):
        d1 = (D - (1 - p) * d0) / p
        a_ = (1 - p) * d0 + p * (1 - d1)
        return (sum(pg * h2(conv(a_, rg)) for pg, rg in rd)
                - (1 - p) * h2(d0) - p * h2(d1))

    r = minimize_scalar(L, bounds=(lo, hi), method="bounded",
                        options={"xatol": 1e-13})
    return L(r.x), r.x


def L_direct(D, idx, starts=40):
    """Direct optimization over ALL 4-param binary channels of
    I(Y,V;Yh|S_idx), exact joint enumeration."""
    sites = sorted(set(idx))
    m = len(sites)
    # joint P(y, v_t, s-vector) via the same enumeration
    joint = {}
    for vt in (0, 1):
        for vv in range(1 << m):
            vs = [(vv >> i) & 1 for i in range(m)]
            pr = chain_prob(sites, vs, vt)
            for sv in range(1 << m):
                ss = [(sv >> i) & 1 for i in range(m)]
                ps = pr
                for k in range(m):
                    ps *= (1 - q) if ss[k] == vs[k] else q
                for y in (0, 1):
                    py = (1 - p) if y == vt else p
                    key = (y, vt, tuple(ss))
                    joint[key] = joint.get(key, 0.0) + ps * py

    keys = list(joint)

    def val(cp):
        C = {(0, 0): cp[0], (0, 1): cp[1], (1, 0): cp[2], (1, 1): cp[3]}
        HcT = 0.0
        psy = {}
        dist = 0.0
        for (y, v, ss), pj in joint.items():
            c1 = min(max(C[(y, v)], 1e-12), 1 - 1e-12)
            HcT += pj * h2(c1)
            psy[ss] = psy.get(ss, [0.0, 0.0])
            psy[ss][0] += pj * (1 - c1)
            psy[ss][1] += pj * c1
            dist += pj * (c1 if y == 0 else 1 - c1)
        HcS = 0.0
        for ss, (a0, a1) in psy.items():
            tot = a0 + a1
            if tot > 0 and a0 > 0 and a1 > 0:
                HcS += tot * h2(a1 / tot)
        return HcS - HcT, dist

    best = None
    for _ in range(starts):
        cp0 = rng.uniform(0.02, 0.6, 4)
        r = minimize(lambda cp: val(cp)[0], cp0,
                     constraints=[{"type": "ineq",
                                   "fun": lambda cp: D - val(cp)[1]}],
                     bounds=[(1e-6, 1 - 1e-6)] * 4,
                     method="SLSQP",
                     options={"maxiter": 2000, "ftol": 1e-14})
        if r.success:
            L_, d_ = val(r.x)
            if d_ <= D + 1e-8 and (best is None or L_ < best):
                best = L_
    return best


ok = True
qe = conv(q, delta(2))
vals["s1_gap"] = abs(thm10(0.1, qe) - L_direct(0.1, [2]))
verdicts["s1_slice"] = bool(vals["s1_gap"] <= 1e-8)

rd = rel_dist([-1, 1])
worst_cf, worst_tilt = 0.0, 0.0
for D in (0.05, 0.10, 0.15):
    Lc, d0s = L_closed(D, rd)
    worst_cf = max(worst_cf, abs(Lc - L_direct(D, [-1, 1])))
    d1s = (D - (1 - p) * d0s) / p
    a_v = (1 - p) * d0s + p * (1 - d1s)
    rhs = 2 * sum(pg * (1 - 2 * rg) * ell(conv(a_v, rg))
                  for pg, rg in rd)
    worst_tilt = max(worst_tilt, abs(ell(d0s) - ell(d1s) - rhs))
vals["s2_worst_cf"] = worst_cf
vals["s2_worst_tilt"] = worst_tilt
verdicts["s2_family"] = bool(worst_cf <= 1e-7 and worst_tilt <= 1e-4)

from scipy.optimize import brentq as _bq
L10, _ = L_closed(0.10, rd)
qfit = _bq(lambda qv: thm10(0.10, qv) - L10, 1e-4, 0.5 - 1e-4)
g05 = thm10(0.05, qfit) - L_closed(0.05, rd)[0]
g15 = thm10(0.15, qfit) - L_closed(0.15, rd)[0]
vals["s3_gap_D005"] = g05
vals["s3_gap_D015"] = g15
vals["s3_max_abs"] = max(abs(g05), abs(g15))
verdicts["s3_noncollapse"] = bool(vals["s3_max_abs"] > 1e-11
                                  and vals["s3_max_abs"] < 5e-4)

vals["s4_slice0"] = abs(thm10(0.1, q) - L_direct(0.1, [0]))
vals["s4_useless"] = abs(L_closed(0.1, [(1.0, 0.5)])[0]
                         - (1 - h2(0.1)))
verdicts["s4_anchors"] = bool(vals["s4_slice0"] <= 1e-8
                              and vals["s4_useless"] <= 1e-9)

allpass = all(verdicts.values())
out = dict(seed=SEED, pilot=bool(a_.pilot),
           runtime_s=round(time.time() - t0, 1),
           values={k: float(v) for k, v in vals.items()},
           verdicts=verdicts, GO13BT_supported=bool(allpass))
print("===GO13BT-JSON===")
print(json.dumps(out, indent=1))
print("===END===")
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")
sys.exit(0 if allpass else 1)
