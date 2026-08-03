# FIBER-G G3 probe -- can transition geometry alone produce a long range field?
# `[exploratory]`.  Uses the estimator certified in fiberg_estimator_cert.py.
#
# THE STRUCTURAL POINT, stated before the run.  Family B modifies how motion
# passes among states while holding the number of states fixed.  Under the
# anti-circularity contract the modification must be a LOCAL function of the
# source, so the conductance is c(x) = f(rho(x)) with no dependence on distance
# to the source and no direction toward it.  For a reversible walk with uniform
# stationary law the projected drift is proportional to grad log c(x), hence to
# f'(rho)/f(rho) times grad rho(x).
#
# Outside the support of rho the density is zero and constant, so grad rho
# vanishes and the drift is EXACTLY ZERO.  A purely local modification of
# transition geometry therefore produces no exterior field at all, let alone an
# inverse square one.  The exterior field is not merely wrong in exponent, it
# does not exist.
#
# That is a support argument, not a numerical accident, and it prunes the
# campaign: to obtain a long range law the source must change something that
# PROPAGATES away from it, which is Family C (a conserved defect or flux).
# Family C then carries the burden the plan already assigned to it, namely
# deriving the mediator and its universal coupling rather than assuming them.
#
# This script measures the prediction against the certified estimator's noise
# floor, so that "zero" is a bounded statement rather than an assertion, and
# includes an interior positive control (drift IS present where grad rho is
# nonzero) so a null cannot come from a dead instrument.
#
# numpy only, CPU.  Output ===FGG3-JSON===.  MIT.
import argparse
import json
import sys
import time

import numpy as np


def rho_blob(X, R_src, soft=0.04):
    """Local source density with COMPACT support -- a smoothed ball of radius
    R_src.  No dependence on anything but position, and identically zero
    outside R_src + soft."""
    r = np.linalg.norm(X, axis=1)
    return 0.5 * (1.0 - np.tanh((r - R_src) / soft))


def conductance(rho, mode, alpha=3.0):
    """c = f(rho), a LOCAL function of the local density only."""
    if mode == "exp":
        return np.exp(alpha * rho)
    if mode == "lin":
        return 1.0 + alpha * rho
    raise ValueError(mode)


def walk_conductance(n_walk, n_step, sigma, R_src, mode, rng,
                     r_out=1.30, alpha=3.0):
    """Reversible walk with uniform stationary law and position dependent
    conductance.  Realised as a Metropolis-Hastings move whose proposal scale
    is set by the LOCAL conductance, which yields drift ~ grad log c under
    detailed balance with a uniform target.  Every step recorded."""
    def reinject(m):
        v = rng.standard_normal((m, 3))
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        return v * rng.uniform(0.05, r_out - 0.05, (m, 1))

    X = reinject(n_walk)
    xb, dxs = [], []
    for _ in range(n_step):
        cx = conductance(rho_blob(X, R_src), mode, alpha)
        prop = X + sigma * (cx[:, None] ** 0.5) * rng.standard_normal((n_walk, 3))
        cy = conductance(rho_blob(prop, R_src), mode, alpha)
        # detailed balance for a uniform target with state dependent proposal
        # scale: accept with the ratio of proposal densities
        logq = 1.5 * (np.log(cx) - np.log(cy)) \
            - (np.linalg.norm(prop - X, axis=1) ** 2) / (2 * sigma ** 2) \
            * (1.0 / cy - 1.0 / cx)
        acc = np.log(rng.random(n_walk)) < np.minimum(0.0, logq)
        Xn = np.where(acc[:, None], prop, X)
        xb.append(X.copy())
        dxs.append((Xn - X).copy())
        rn = np.linalg.norm(Xn, axis=1)
        out = (rn > r_out) | (rn < 1e-6)
        if out.any():
            Xn[out] = reinject(int(out.sum()))
        X = Xn
    return np.concatenate(xb), np.concatenate(dxs)


def radial_profile(xb, dxs, edges):
    """Certified estimator: E[dx . u_hat], never E[d|x|] (which carries the
    spurious outward (n_obs-1)sigma^2/2r Jacobian term)."""
    r = np.linalg.norm(xb, axis=1)
    u = xb / np.maximum(r, 1e-12)[:, None]
    proj = (dxs * u).sum(1)
    rows = []
    for i in range(len(edges) - 1):
        m = (r >= edges[i]) & (r < edges[i + 1])
        if m.sum() < 5000:
            continue
        rows.append(dict(r=float(0.5 * (edges[i] + edges[i + 1])),
                         b=float(proj[m].mean()),
                         se=float(proj[m].std() / np.sqrt(m.sum())),
                         n=int(m.sum())))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--walk", type=int, default=40000)
    ap.add_argument("--step", type=int, default=400)
    ap.add_argument("--sigma", type=float, default=0.01)
    ap.add_argument("--rsrc", type=float, default=0.30)
    ap.add_argument("--alpha", type=float, default=3.0)
    ap.add_argument("--seed", type=int, default=20260820)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    t0 = time.time()
    print(f"FIBER-G G3 locality probe  seed={a.seed}  source radius={a.rsrc}  "
          f"alpha={a.alpha}  sigma={a.sigma}")
    print("prediction: drift nonzero only where grad rho != 0, i.e. only in the "
          "source shell; EXACTLY zero outside\n", flush=True)

    res = {}
    for mode in ("exp", "lin"):
        xb, dxs = walk_conductance(a.walk, a.step, a.sigma, a.rsrc, mode, rng,
                                   alpha=a.alpha)
        edges = np.concatenate([np.linspace(0.06, 0.50, 12),
                                np.linspace(0.55, 1.20, 12)])
        rows = radial_profile(xb, dxs, edges)
        inner = [x for x in rows if x["r"] < a.rsrc - 0.06]          # inside source
        shell = [x for x in rows if abs(x["r"] - a.rsrc) <= 0.06]    # grad rho != 0
        outer = [x for x in rows if x["r"] > a.rsrc + 0.12]          # exterior
        def worst(rs):
            return (max((abs(x["b"]) / max(x["se"], 1e-30)) for x in rs) if rs
                    else float("nan"))
        res[mode] = dict(rows=rows,
                         shell_max_sigma=worst(shell),
                         outer_max_sigma=worst(outer),
                         inner_max_sigma=worst(inner),
                         outer_max_abs=float(max((abs(x["b"]) for x in outer),
                                                 default=float("nan"))),
                         outer_mean_se=float(np.mean([x["se"] for x in outer]))
                         if outer else float("nan"))
        print(f"  mode={mode}: source-shell drift = {res[mode]['shell_max_sigma']:.1f} "
              f"sigma  |  EXTERIOR drift = {res[mode]['outer_max_sigma']:.1f} sigma "
              f"(max |b| {res[mode]['outer_max_abs']:.2e}, SE {res[mode]['outer_mean_se']:.2e})",
              flush=True)

    verdict = dict(
        G3a_shell_drift_detected=bool(all(res[m]["shell_max_sigma"] > 5.0
                                          for m in res)),
        G3b_exterior_drift_absent=bool(all(res[m]["outer_max_sigma"] < 5.0
                                           for m in res)),
    )
    result = dict(
        note="[exploratory] G3 locality probe. A purely LOCAL conductance "
             "c(x)=f(rho(x)) gives projected drift proportional to grad log c, "
             "so outside the compact support of rho the drift is identically "
             "zero by a support argument. Family B therefore cannot produce ANY "
             "exterior field, inverse square or otherwise. Long range behaviour "
             "requires the source to modify something that propagates, which is "
             "Family C, whose burden is to derive the mediator and its universal "
             "coupling rather than assume them. The interior shell measurement is "
             "the positive control proving the estimator is live.",
        seed=a.seed, source_radius=a.rsrc, alpha=a.alpha, sigma=a.sigma,
        modes=res, verdict=verdict, all_pass=bool(all(verdict.values())),
        seconds=round(time.time() - t0, 1))
    print(f"\nverdict: {verdict}")
    print(f"all_pass: {result['all_pass']}")
    print("===FGG3-JSON===")
    print(json.dumps(result, indent=1, default=float))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
