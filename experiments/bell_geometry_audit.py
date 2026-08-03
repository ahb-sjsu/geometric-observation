# GO-P-2026-057 -- Bell geometry audit: a constraint-first falsification harness
# for geometric hidden-variable conjectures.
#
# Built from the CONSTRAINTS, not from a desired violation.  In the baseline
# arm P0 every Bell premise is intact BY CONSTRUCTION:
#   * source sampling is setting-independent: lambda ~ rho, drawn once per
#     trial and reused across all four (x,y) contexts;
#   * responses are strictly local: A depends on (x,lambda) only, B on
#     (y,lambda) only, so P(A|x,y)=P(A|x) and P(B|x,y)=P(B|y) HOLD BY
#     CONSTRUCTION -- the measured no-signalling residual is a finite-sample
#     check on the code, not a property being hoped for;
#   * EVERY emitted trial is counted;
#   * non-detection is an explicit third outcome 0, never deleted.
# The pointwise bound needs only |A|,|B| <= 1, so {-1,0,+1} outcomes still give
# |K(lambda)| <= 2 and hence S <= 2 for ANY rho.  P0's null is therefore a
# theorem; the harness exists to show it is unmoved by geometry, and to be
# reusable.
#
# POSITIVE CONTROL (this is what makes the null meaningful).  Arms P1-P3 each
# break EXACTLY ONE premise and must exceed 2, proving the instrument can see a
# violation when one exists:
#   P1 outcome accounting : postselect on coincidence (delete non-detections)
#   P2 measurement dependence : sample lambda from rho_xy, responses still local
#   P3 locality : Alice's response reads Bob's setting
# Any future model exceeding the bound must land in one of these columns.
#
# FULL ANGULAR LAW, not one CHSH score: E(theta) is swept over [0,pi].  A local
# sign model on a sphere gives the SAWTOOTH  E(theta) = -(1 - 2*theta/pi),
# scaled by the mean detection product -- not the quantum -cos(theta).  The
# harness reports the gap to both, which is exactly why CHSH probes near pi/4.
#
# numpy only, CPU, deterministic.  Output: ===BGA-JSON===.  MIT.
import argparse
import json
import sys
import time

import numpy as np

TSIRELSON = 2.0 * np.sqrt(2.0)


def make_latents(n, d, core_frac, core_kappa, zipf_a, rng):
    n_core = int(round(core_frac * n))
    X = rng.standard_normal((n, d))
    if n_core > 0:
        mu = rng.standard_normal(d)
        mu /= np.linalg.norm(mu)
        X[:n_core] = core_kappa * mu[None, :] + rng.standard_normal((n_core, d))
    X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-12
    if zipf_a > 0:
        w = 1.0 / np.power(np.arange(1, n + 1), zipf_a)
        rng.shuffle(w)
        w /= w.sum()
    else:
        w = np.full(n, 1.0 / n)
    return X, w


def hub_skew(X, k, rng, sample=3000):
    n = X.shape[0]
    idx = rng.choice(n, min(sample, n), replace=False)
    S = X[idx]
    sims = S @ S.T
    np.fill_diagonal(sims, -np.inf)
    nn = np.argpartition(-sims, kth=k, axis=1)[:, :k]
    Nk = np.bincount(nn.ravel(), minlength=len(idx)).astype(float)
    return float(((Nk - Nk.mean()) ** 3).mean() / (Nk.std() ** 3 + 1e-12))


def plane(d, rng):
    e1 = rng.standard_normal(d)
    e1 /= np.linalg.norm(e1)
    e2 = rng.standard_normal(d)
    e2 -= (e2 @ e1) * e1
    e2 /= np.linalg.norm(e2)
    return e1, e2


def dirn(e1, e2, t):
    return np.cos(t) * e1 + np.sin(t) * e2


def chsh(E):
    return abs(E[(0, 0)] + E[(0, 1)] + E[(1, 0)] - E[(1, 1)])


def trial_outcomes(L, qa, qb, eta, rng, arm, qa_other=None):
    """Local outcomes in {-1,0,+1}; 0 == explicit non-detection, never deleted.
    arm='P3' breaks locality by letting Alice read Bob's setting."""
    sa = L @ qa
    if arm == "P3" and qa_other is not None:            # locality broken
        sa = sa + 0.9 * (L @ qa_other)
    A = np.where(sa >= 0, 1.0, -1.0)
    B = np.where((L @ qb) >= 0, -1.0, 1.0)
    if eta is not None:
        dA = rng.random(len(L)) < eta(L, qa)
        dB = rng.random(len(L)) < eta(L, qb)
        A = np.where(dA, A, 0.0)
        B = np.where(dB, B, 0.0)
    return A, B


def eta_align(sharp):
    """Detection probability depends on lambda and the LOCAL setting only."""
    def f(L, q):
        return 1.0 / (1.0 + np.exp(-sharp * (L @ q)))
    return f


def run_arm(X, w, qA, qB, rng, n_draw, arm, sharp):
    """One arm; returns S over ALL emitted trials plus diagnostics."""
    eta = None if sharp is None else eta_align(sharp)
    E_all, E_ps, marg, eff = {}, {}, {}, {}
    # setting-independent source: ONE draw reused across contexts (P0/P1/P3)
    base = rng.choice(len(X), n_draw, p=w)
    for x in (0, 1):
        for y in (0, 1):
            if arm == "P2":
                # measurement dependence: the source law itself depends on (x,y)
                tilt = w * np.exp(1.2 * (X @ qA[x]) * (X @ qB[y]))
                tilt /= tilt.sum()
                idx = rng.choice(len(X), n_draw, p=tilt)
            else:
                idx = base
            L = X[idx]
            A, B = trial_outcomes(L, qA[x], qB[y], eta, rng, arm,
                                  qa_other=qB[y] if arm == "P3" else None)
            E_all[(x, y)] = float((A * B).mean())          # EVERY trial counted
            both = (A != 0) & (B != 0)
            eff[(x, y)] = float(both.mean())
            E_ps[(x, y)] = float((A[both] * B[both]).mean()) if both.sum() > 50 else 0.0
            # no-signalling check: Alice's marginal must not move with y
            marg[(x, y)] = (float(A.mean()), float(B.mean()))
    ns = max(max(abs(marg[(x, 0)][0] - marg[(x, 1)][0]) for x in (0, 1)),
             max(abs(marg[(0, y)][1] - marg[(1, y)][1]) for y in (0, 1)))
    return dict(arm=arm, S_all_counted=chsh(E_all), S_postselected=chsh(E_ps),
                no_signalling_residual=float(ns),
                eff_mean=float(np.mean(list(eff.values()))))


def angular_law(X, w, rng, d, n_draw, sharp, n_ang=25):
    """E(theta) over ALL trials; compare to the local sawtooth and to -cos."""
    e1, e2 = plane(d, rng)
    eta = None if sharp is None else eta_align(sharp)
    idx = rng.choice(len(X), n_draw, p=w)
    L = X[idx]
    qa = dirn(e1, e2, 0.0)
    ths = np.linspace(0.0, np.pi, n_ang)
    E, saw, qm = [], [], []
    for t in ths:
        A, B = trial_outcomes(L, qa, dirn(e1, e2, t), eta, rng, "P0")
        E.append(float((A * B).mean()))
        saw.append(-(1.0 - 2.0 * t / np.pi))
        qm.append(-float(np.cos(t)))
    E, saw, qm = np.array(E), np.array(saw), np.array(qm)
    scale = float(np.dot(E, saw) / max(np.dot(saw, saw), 1e-12))   # detection scaling
    return dict(thetas=ths.tolist(), E=E.tolist(), sawtooth=saw.tolist(),
                quantum=qm.tolist(), fitted_scale=scale,
                rms_vs_scaled_sawtooth=float(np.sqrt(np.mean((E - scale * saw) ** 2))),
                rms_vs_quantum=float(np.sqrt(np.mean((E - qm) ** 2))),
                max_gap_vs_quantum=float(np.abs(E - qm).max()),
                argmax_gap_theta=float(ths[int(np.abs(E - qm).argmax())]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=60000)
    ap.add_argument("--draw", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=20260817)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    t0 = time.time()
    print(f"Bell geometry audit  seed={a.seed} n_latent={a.n} n_draw={a.draw}")
    print("P0 = all premises intact (S<=2 is a THEOREM here); P1-P3 = positive "
          "controls, one broken premise each.\n", flush=True)

    grid = []
    for d in (3, 8, 32, 128):
        for cf, ck in ((0.0, 0.0), (0.02, 8.0), (0.25, 3.0)):
            for za in (0.0, 1.5):
                grid.append(dict(d=d, core_frac=cf, core_kappa=ck, zipf_a=za))

    p0, ctrl, ang = [], [], []
    for g in grid:
        X, w = make_latents(a.n, g["d"], g["core_frac"], g["core_kappa"],
                            g["zipf_a"], rng)
        hs = hub_skew(X, 10, rng)
        e1, e2 = plane(g["d"], rng)
        # CHSH-optimal-ish settings in a shared plane
        qA = {0: dirn(e1, e2, 0.0), 1: dirn(e1, e2, np.pi / 2)}
        qB = {0: dirn(e1, e2, np.pi / 4), 1: dirn(e1, e2, -np.pi / 4)}
        for sharp in (None, 4.0, 15.0):          # None = perfect detection
            r = run_arm(X, w, qA, qB, rng, a.draw, "P0", sharp)
            r.update(g, hub_skew=hs, sharp=(sharp or 0.0))
            p0.append(r)
        for arm in ("P1", "P2", "P3"):
            r = run_arm(X, w, qA, qB, rng, a.draw, arm, 15.0 if arm == "P1" else None)
            r.update(g, hub_skew=hs, sharp=15.0 if arm == "P1" else 0.0)
            ctrl.append(r)
        ang.append(dict(**g, **angular_law(X, w, rng, g["d"], a.draw // 4, 15.0)))
        print(f"  d={g['d']:3d} core={g['core_frac']:.2f} zipf={g['zipf_a']:.1f} "
              f"hub={hs:6.2f} | P0 S={[round(x['S_all_counted'],4) for x in p0[-3:]]} "
              f"| P1={ctrl[-3]['S_all_counted']:.3f} P2={ctrl[-2]['S_all_counted']:.3f} "
              f"P3={ctrl[-1]['S_all_counted']:.3f}", flush=True)

    s0 = np.array([r["S_all_counted"] for r in p0])
    ns0 = np.array([r["no_signalling_residual"] for r in p0])
    hub0 = np.array([r["hub_skew"] for r in p0])
    tol = 4.0 / np.sqrt(a.draw)                     # finite-sample tolerance
    byarm = {k: np.array([r["S_all_counted"] for r in ctrl if r["arm"] == k])
             for k in ("P1", "P2", "P3")}
    ns_by = {k: np.array([r["no_signalling_residual"] for r in ctrl if r["arm"] == k])
             for k in ("P1", "P2", "P3")}
    ps0 = np.array([r["S_postselected"] for r in p0])

    verdict = dict(
        T1_P0_respects_bound=bool(s0.max() <= 2.0 + tol),
        T2_P0_no_signalling=bool(ns0.max() <= tol),
        T3_angular_law_is_sawtooth_not_cosine=bool(
            all(x["rms_vs_scaled_sawtooth"] < x["rms_vs_quantum"] for x in ang)),
        T4_positive_controls_fire=bool(all(byarm[k].max() > 2.0 + tol
                                           for k in ("P1", "P2", "P3"))),
        T5_geometry_irrelevant_in_P0=bool(abs(np.corrcoef(s0, hub0)[0, 1]) < 0.35
                                          and s0.max() <= 2.0 + tol),
        T6_postselection_alone_breaks_it=bool(ps0.max() > 2.0 + tol),
    )
    result = dict(
        note="P0's null is a theorem (|A|,|B|<=1 gives |K|<=2 pointwise); the "
             "harness shows it is unmoved by dimension, density skew, Zipf "
             "concentration or hubness, and the P1-P3 positive controls prove "
             "the instrument can detect a violation when a premise breaks.",
        seed=a.seed, n_latent=a.n, n_draw=a.draw, finite_sample_tol=float(tol),
        tsirelson=TSIRELSON, P0=p0, controls=ctrl, angular=ang,
        P0_max_S=float(s0.max()), P0_max_ns=float(ns0.max()),
        P0_max_S_postselected=float(ps0.max()),
        P0_corr_S_vs_hubskew=float(np.corrcoef(s0, hub0)[0, 1]),
        controls_max_S={k: float(v.max()) for k, v in byarm.items()},
        controls_max_ns={k: float(v.max()) for k, v in ns_by.items()},
        verdict=verdict, all_pass=bool(all(verdict.values())),
        seconds=round(time.time() - t0, 1))

    print(f"\nP0 (all premises intact, every trial counted):")
    print(f"  max S = {s0.max():.5f}   bound 2 + tol({tol:.4f}) = {2+tol:.4f}   "
          f"-> respects bound: {verdict['T1_P0_respects_bound']}")
    print(f"  max no-signalling residual = {ns0.max():.5f} (by construction; "
          f"tol {tol:.4f}) -> {verdict['T2_P0_no_signalling']}")
    print(f"  corr(S, hub skew) = {result['P0_corr_S_vs_hubskew']:+.3f}  "
          f"-> geometry irrelevant: {verdict['T5_geometry_irrelevant_in_P0']}")
    print(f"  same data, POSTSELECTED instead of fully counted: max S = "
          f"{ps0.max():.4f} -> {verdict['T6_postselection_alone_breaks_it']}")
    print(f"\nPositive controls (one broken premise each):")
    for k, lbl in (("P1", "outcome accounting (postselection)"),
                   ("P2", "measurement independence"),
                   ("P3", "locality")):
        print(f"  {k} {lbl:38s} max S = {byarm[k].max():.4f}   "
              f"max NS residual = {ns_by[k].max():.4f}")
    print(f"\nAngular law (E(theta) over ALL trials):")
    for x in ang[:4]:
        print(f"  d={x['d']:3d} core={x['core_frac']:.2f}: rms vs scaled sawtooth "
              f"{x['rms_vs_scaled_sawtooth']:.4f}  vs -cos(theta) "
              f"{x['rms_vs_quantum']:.4f}  max gap {x['max_gap_vs_quantum']:.3f} "
              f"at theta={x['argmax_gap_theta']:.2f}")
    print(f"\nverdict: {verdict}\nall_pass: {result['all_pass']}")
    print("===BGA-JSON===")
    print(json.dumps(result, indent=1, default=float))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
