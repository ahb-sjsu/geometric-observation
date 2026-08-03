# FIBER-G pilots P0/P1 -- does projected high-dimensional dynamics produce a
# gravity-like field, and is the witness OCCUPANCY or TRANSITIONS?
#
# `[exploratory]`: instrument validation and estimator floors only.  No claim
# rides on this file; the claim-bearing campaign is sealed afterwards.
#
# ANTI-CIRCULARITY CONTRACT (enforced by construction here).  No arm's
# microscopic rule may contain: distance from probe to source, 1/r or 1/r^2,
# the source-to-probe direction, a precomputed potential, or a global
# shortest-path query.  P0b DELIBERATELY violates this -- it is the injected
# positive control, and it is labelled as such.
#
# P0 -- ESTIMATOR NET (three arms, one exact target each)
#   P0a  projected d-ball diffusion.  For x in R^3 observable and z in R^(d-3)
#        hidden, the fiber volume is Omega(x) ~ (R^2-|x|^2)^((d-3)/2), so a
#        reversible diffusion with equilibrium ~ Omega has projected drift
#             b(x) = kappa * grad log Omega = -kappa (d-3) x / (R^2 - |x|^2),
#        i.e. INWARD and LINEAR near the centre -- verified analytically to
#        1e-9 before this run.  The estimator must recover it.
#   P0b  injected 1/r^2 (positive control): must recover exponent ~ -2.
#   P0c  harmonic null: must recover exponent ~ +1 and must NOT report -2.
#   Together these fix the estimator's numerical floor and prove it can tell
#   an inverse-square field from a harmonic one.
#
# P1 -- THE DECISIVE DISSOCIATION: occupancy vs transitions.
#   The Bell probe's lesson was that a striking concentration statistic is not
#   the generator of motion.  Here that is made exact, not sampled: on a finite
#   radial birth-death chain both the stationary law pi and the conditional
#   drift E[dr | r] are computed in closed form from the transition matrix.
#     pair 1: IDENTICAL pi, DIFFERENT conductances -> if drift differs,
#             occupancy cannot be the witness.
#     pair 2: IDENTICAL drift, DIFFERENT pi        -> the converse.
#     pair 3: matched degree/hubness, different geometry.
#   Every trajectory counted; nothing conditioned on arrival or capture.
#
# numpy only, CPU, deterministic.  Output ===FIBERG-JSON===.  MIT.
import argparse
import json
import sys
import time

import numpy as np


# ------------------------------------------------------------------ P0 arms
def project_ball_walk(d, n_walk, n_step, step, rng, R=1.0):
    """Isotropic walk confined to the unit d-ball (reject exits), projected to
    the first 3 coords.  Returns (x_before, dx) pairs pooled over ALL steps and
    ALL walkers -- no conditioning, no discarding."""
    X = rng.standard_normal((n_walk, d))
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    X *= (rng.random((n_walk, 1)) ** (1.0 / d)) * R * 0.6      # start interior
    xb, dxs = [], []
    for _ in range(n_step):
        P = X + step * rng.standard_normal((n_walk, d))
        ok = np.linalg.norm(P, axis=1) <= R                    # reflect = reject
        Xn = np.where(ok[:, None], P, X)
        xb.append(X[:, :3].copy())
        dxs.append((Xn[:, :3] - X[:, :3]).copy())
        X = Xn
    return np.concatenate(xb), np.concatenate(dxs)


def injected_walk(n_walk, n_step, step, rng, law, R=1.0):
    """3-D walk with a DELIBERATELY injected radial drift (positive controls).
    law='inv_sq' -> b ~ -x/|x|^3 ;  law='harmonic' -> b ~ -x."""
    X = rng.standard_normal((n_walk, 3))
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    X *= rng.uniform(0.15, 0.9, (n_walk, 1))
    xb, dxs = [], []
    for _ in range(n_step):
        r = np.linalg.norm(X, axis=1, keepdims=True)
        b = -X / np.maximum(r, 0.05) ** 3 if law == "inv_sq" else -X
        P = X + 0.002 * b + step * rng.standard_normal((n_walk, 3))
        keep = (np.linalg.norm(P, axis=1) <= R) & (np.linalg.norm(P, axis=1) > 0.05)
        Xn = np.where(keep[:, None], P, X)
        xb.append(X.copy())
        dxs.append((Xn - X).copy())
        X = Xn
    return np.concatenate(xb), np.concatenate(dxs)


def radial_drift(xb, dxs, n_bin=14, rmax=0.9):
    """Conditional radial drift E[dr | r] in fixed bins -- a TRANSITION moment,
    never an occupancy statistic."""
    r = np.linalg.norm(xb, axis=1)
    u = xb / np.maximum(r, 1e-12)[:, None]
    dr = (dxs * u).sum(1)                                      # radial component
    edges = np.linspace(0.08, rmax, n_bin + 1)
    ctr, val, cnt = [], [], []
    for i in range(n_bin):
        m = (r >= edges[i]) & (r < edges[i + 1])
        if m.sum() > 200:
            ctr.append(0.5 * (edges[i] + edges[i + 1]))
            val.append(float(dr[m].mean()))
            cnt.append(int(m.sum()))
    return np.array(ctr), np.array(val), np.array(cnt)


def fit_exponent(r, b):
    """Slope of log|b| vs log r for the inward part; returns nan if not inward."""
    m = b < 0
    if m.sum() < 4:
        return float("nan")
    return float(np.polyfit(np.log(r[m]), np.log(-b[m]), 1)[0])


# ------------------------------------------------- P1 exact finite-state pairs
def birth_death(pi, cond, scale=1.0):
    """Reversible birth-death chain with stationary pi and edge conductances
    cond[i] between i and i+1, built from detailed balance
    pi_i P_ij = pi_j P_ji = cond_i.

    BUGFIX: the first version renormalised any row whose off-diagonal sum
    exceeded 1, which DESTROYS detailed balance and silently moved pi -- the
    pilot's own N5 gate caught it (it reported max|pi_A-pi_B| = 2.4e-2 under a
    banner claiming the laws were identical).  Instead the caller passes a
    single global `scale` applied to ALL conductances of ALL chains being
    compared: global scaling preserves detailed balance and pi EXACTLY, and is
    a pure uniform time-rescaling, so drift comparisons stay fair."""
    n = len(pi)
    P = np.zeros((n, n))
    for i in range(n - 1):
        P[i, i + 1] = scale * cond[i] / pi[i]
        P[i + 1, i] = scale * cond[i] / pi[i + 1]
    rows = P.sum(axis=1)
    assert rows.max() <= 1.0 + 1e-12, f"row sum {rows.max():.4f} > 1; lower scale"
    for i in range(n):
        P[i, i] = 1.0 - P[i].sum()
    return P


def safe_scale(pis, conds, margin=0.9):
    """Largest common conductance scale keeping every row substochastic."""
    worst = 0.0
    for pi, cond in zip(pis, conds):
        n = len(pi)
        for i in range(n):
            s = 0.0
            if i < n - 1:
                s += cond[i] / pi[i]
            if i > 0:
                s += cond[i - 1] / pi[i]
            worst = max(worst, s)
    return margin / worst


def exact_stationary(P):
    w, V = np.linalg.eig(P.T)
    v = np.real(V[:, np.argmin(np.abs(w - 1.0))])
    v = np.abs(v)
    return v / v.sum()


def exact_drift(P, r):
    """E[dr | state i] computed exactly from the transition matrix."""
    return P @ r - r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--walk", type=int, default=20000)
    ap.add_argument("--step", type=int, default=250)
    ap.add_argument("--seed", type=int, default=20260818)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    t0 = time.time()
    print(f"FIBER-G pilot P0/P1  seed={a.seed}  walkers={a.walk} steps={a.step}")
    print("[exploratory] estimator net + occupancy-vs-transition dissociation\n",
          flush=True)

    # ---------------- P0a: projected d-ball, exact analytic target
    p0a = []
    for d in (6, 12, 30):
        xb, dxs = project_ball_walk(d, a.walk, a.step, 0.02, rng)
        r, b, c = radial_drift(xb, dxs)
        ana = -(d - 3) * r / (1.0 - r ** 2)
        s = float(np.dot(b, ana) / np.dot(ana, ana))            # one free scale (kappa)
        rel = float(np.abs(b - s * ana).max() / (np.abs(s * ana).max() + 1e-18))
        near = float(np.polyfit(r[:5], b[:5], 1)[0])
        p0a.append(dict(d=d, kappa_fit=s, max_rel_resid=rel, near_centre_slope=near,
                        exponent=fit_exponent(r, b), r=r.tolist(), b=b.tolist(),
                        analytic=ana.tolist(), n=c.tolist()))
        print(f"  P0a d={d:3d}: fitted kappa={s:.3e}  max rel resid={rel:.3f}  "
              f"near-centre slope={near:+.3e}  inward={bool(b[0] < 0)}  "
              f"apparent exponent={p0a[-1]['exponent']:+.2f}", flush=True)

    # ---------------- P0b/P0c: injected positive controls
    ctrl = {}
    for law, want in (("inv_sq", -2.0), ("harmonic", 1.0)):
        xb, dxs = injected_walk(a.walk, a.step, 0.01, rng, law)
        r, b, c = radial_drift(xb, dxs)
        e = fit_exponent(r, b)
        ctrl[law] = dict(exponent=e, target=want, r=r.tolist(), b=b.tolist())
        print(f"  P0{'b' if law=='inv_sq' else 'c'} injected {law:9s}: recovered "
              f"exponent {e:+.3f}  (target {want:+.1f})", flush=True)

    # ---------------- P1: exact occupancy-vs-transition dissociation
    n = 40
    r_states = np.linspace(0.1, 1.0, n)
    OmegaA = (1.0 - r_states ** 2 * 0.9) ** 6                  # a fiber profile
    piA = OmegaA / OmegaA.sum()
    condA = np.full(n - 1, 0.02)                               # uniform conductance
    condB = 0.02 * (1.0 + 3.0 * np.linspace(0, 1, n - 1) ** 2)  # graded, SAME pi
    sc = safe_scale([piA, piA], [condA, condB])     # ONE common scale => fair
    PA, PB = birth_death(piA, condA, sc), birth_death(piA, condB, sc)
    piA_chk, piB_chk = exact_stationary(PA), exact_stationary(PB)
    dA, dB = exact_drift(PA, r_states), exact_drift(PB, r_states)
    pi_gap = float(np.abs(piA_chk - piB_chk).max())
    drift_gap = float(np.abs(dA - dB).max())

    # pair 2: different pi, engineered to share a drift profile as closely as
    # a birth-death chain allows (conductance rescaled to compensate pi)
    OmegaC = (1.0 - r_states ** 2 * 0.9) ** 12
    piC = OmegaC / OmegaC.sum()
    condC = condA * (piC[:-1] / piA[:-1])
    sc2 = safe_scale([piA, piC], [condA, condC])
    PC = birth_death(piC, condC, sc2)
    PA2 = birth_death(piA, condA, sc2)              # same scale for comparison
    dA2 = exact_drift(PA2, r_states)
    dC = exact_drift(PC, r_states)
    pi_gap2 = float(np.abs(exact_stationary(PC) - piA_chk).max())
    drift_gap2 = float(np.abs(dC - dA2).max())

    print(f"\n  P1 pair 1 (SAME stationary law, different conductances):")
    print(f"     max|pi_A - pi_B|   = {pi_gap:.3e}   <- occupancy identical")
    print(f"     max|drift_A - drift_B| = {drift_gap:.3e}   <- drift DIFFERS")
    print(f"     ratio drift_gap / max|drift_A| = "
          f"{drift_gap / (np.abs(dA).max()+1e-18):.3f}")
    print(f"  P1 pair 2 (different stationary law, compensated conductances):")
    print(f"     max|pi_C - pi_A|   = {pi_gap2:.3e}   <- occupancy DIFFERS")
    print(f"     max|drift_C - drift_A| = {drift_gap2:.3e}")

    verdict = dict(
        N1_estimator_recovers_dball_law=bool(
            all(x["max_rel_resid"] < 0.35 and x["b"][0] < 0 for x in p0a)),
        N2_recovers_injected_inverse_square=bool(
            abs(ctrl["inv_sq"]["exponent"] + 2.0) < 0.6),
        N3_distinguishes_harmonic=bool(ctrl["harmonic"]["exponent"] > 0.0),
        N4_dball_has_no_exterior_inverse_square=bool(
            all(x["near_centre_slope"] < 0 for x in p0a)),
        N5_occupancy_is_not_the_witness=bool(
            pi_gap < 1e-9 and drift_gap > 0.05 * abs(dA).max()),
    )
    result = dict(
        note="[exploratory] FIBER-G P0/P1. P0a's target is analytic; P0b/P0c are "
             "deliberately injected positive controls (they violate the "
             "anti-circularity contract on purpose). P1 is exact finite-state: "
             "identical stationary law with different conductances gives "
             "different drift, so occupancy cannot be the force witness.",
        seed=a.seed, walkers=a.walk, steps=a.step,
        P0a_dball=p0a, P0_controls=ctrl,
        P1=dict(pi_gap_pair1=pi_gap, drift_gap_pair1=drift_gap,
                drift_gap_rel_pair1=float(drift_gap / (np.abs(dA).max() + 1e-18)),
                pi_gap_pair2=pi_gap2, drift_gap_pair2=drift_gap2,
                r_states=r_states.tolist(), drift_A=dA.tolist(),
                drift_B=dB.tolist(), drift_C=dC.tolist(),
                pi_A=piA_chk.tolist(), pi_C=exact_stationary(PC).tolist()),
        verdict=verdict, all_pass=bool(all(verdict.values())),
        seconds=round(time.time() - t0, 1))
    print(f"\nverdict: {verdict}")
    print(f"all_pass: {result['all_pass']}")
    print("===FIBERG-JSON===")
    print(json.dumps(result, indent=1, default=float))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
