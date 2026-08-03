# FIBER-G estimator certification -- the hard gate before any G-arm may claim a
# field law.  `[exploratory]` instrument work; no claim rides on it.
#
# The P0 pilot left the estimator UNCERTIFIED: an injected 1/r^2 drift came back
# as exponent -0.897 instead of -2.  Diagnosis was that the injection (0.2 per
# step) dwarfed the diffusion step (0.01), so walkers piled against the inner
# cutoff and the conditional moment measured boundary dynamics, not the law.
# This script fixes the injection to the LINEAR-RESPONSE regime and certifies
# three things:
#
#   C1  EXPONENT RECOVERY.  Inject b_r(r) = -c r^p for p in {-2,-1,+1} at an
#       amplitude ~5% of the diffusion step, fit only inside a window clear of
#       both boundaries, and require the recovered exponent to match p.  Until
#       this passes, the estimator cannot be trusted to detect an inverse-square
#       law and NO FIBER-G arm may claim one.
#
#   C2  THE JACOBIAN TRAP (a real trap, documented here).  Two radial
#       estimators are NOT the same thing:
#           E[ dx . u_hat ]  = b_r dt                      (clean)
#           E[ d|x| ]        = b_r dt + (n_obs-1) s^2 dt / (2r)   (contaminated)
#       The second carries a spurious OUTWARD 1/r term that is pure coordinate
#       Jacobian -- the same functional form as the "naive entropic force" the
#       gravity note derives.  Anyone measuring E[d|x|] and finding an outward
#       1/r drift may be measuring nothing but the radial coordinate change.
#       C2 measures both and checks the difference against the analytic term.
#
#   C3  SAMPLE FLOOR.  Standard error of the radial mean is s/sqrt(N) per bin,
#       so resolving a drift of size m at k sigma needs N >= (k s / m)^2.
#       Tabulated against the measured values so the eventual NRP manifest is
#       sized from arithmetic rather than optimism.
#
# Sampling note: walkers leaving the annulus have their step RECORDED (it is a
# real transition) and are then reinjected.  Conditional moments E[dx | x] are
# unbiased under any choice of starting-point distribution -- what would bias
# them is conditioning on the OUTCOME, which never happens here.
#
# numpy only, CPU.  Output ===FGCERT-JSON===.  MIT.
import argparse
import json
import sys
import time

import numpy as np


def walk(n_walk, n_step, sigma, law_p, amp_at_half, rng,
         r_in=0.15, r_out=1.20):
    """3-D walk with injected radial drift b_r = -c r^p, c set so that
    |b_r| at r=0.5 equals amp_at_half (kept far below sigma = linear response).
    Returns pooled (x_before, dx) over every step of every walker."""
    c = amp_at_half / (0.5 ** law_p)

    def reinject(m):
        v = rng.standard_normal((m, 3))
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        return v * rng.uniform(r_in + 0.05, r_out - 0.05, (m, 1))

    X = reinject(n_walk)
    xb, dxs = [], []
    for _ in range(n_step):
        r = np.linalg.norm(X, axis=1, keepdims=True)
        u = X / r
        b = -c * (r ** law_p) * u                     # injected drift
        step = b + sigma * rng.standard_normal((n_walk, 3))
        Xn = X + step
        xb.append(X.copy())
        dxs.append(step.copy())                       # the true transition
        rn = np.linalg.norm(Xn, axis=1)
        out = (rn < r_in) | (rn > r_out)
        if out.any():
            Xn[out] = reinject(int(out.sum()))        # resample START, not outcome
        X = Xn
    return np.concatenate(xb), np.concatenate(dxs)


def radial_moments(xb, dxs, lo, hi, n_bin=12):
    """Both estimators per bin: the clean projection and the contaminated |x|."""
    r = np.linalg.norm(xb, axis=1)
    u = xb / np.maximum(r, 1e-12)[:, None]
    proj = (dxs * u).sum(1)                            # E[dx . u]  -> b_r
    dnorm = np.linalg.norm(xb + dxs, axis=1) - r       # E[d|x|]    -> b_r + Jac
    edges = np.linspace(lo, hi, n_bin + 1)
    out = []
    for i in range(n_bin):
        m = (r >= edges[i]) & (r < edges[i + 1])
        if m.sum() < 2000:
            continue
        out.append(dict(r=float(0.5 * (edges[i] + edges[i + 1])),
                        b_proj=float(proj[m].mean()),
                        b_norm=float(dnorm[m].mean()),
                        se=float(proj[m].std() / np.sqrt(m.sum())),
                        n=int(m.sum())))
    return out


def fit_exp(rows, key="b_proj"):
    r = np.array([x["r"] for x in rows])
    b = np.array([x[key] for x in rows])
    m = b < 0
    if m.sum() < 4:
        return float("nan")
    return float(np.polyfit(np.log(r[m]), np.log(-b[m]), 1)[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--walk", type=int, default=40000)
    ap.add_argument("--step", type=int, default=300)
    ap.add_argument("--sigma", type=float, default=0.01)
    ap.add_argument("--amp", type=float, default=5e-4)   # 5% of sigma at r=0.5
    ap.add_argument("--seed", type=int, default=20260819)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    t0 = time.time()
    print(f"FIBER-G estimator certification  seed={a.seed}  walkers={a.walk} "
          f"steps={a.step} sigma={a.sigma} amp@0.5={a.amp} "
          f"(= {a.amp/a.sigma:.0%} of sigma -> linear response)\n", flush=True)

    LO, HI = 0.30, 0.90                                 # clear of both boundaries
    cert = {}
    for p, name in ((-2.0, "inverse_square"), (-1.0, "inverse_r"), (1.0, "harmonic")):
        xb, dxs = walk(a.walk, a.step, a.sigma, p, a.amp, rng)
        rows = radial_moments(xb, dxs, LO, HI)
        e_proj, e_norm = fit_exp(rows, "b_proj"), fit_exp(rows, "b_norm")
        # analytic Jacobian term (n_obs = 3): (n-1) s^2 / (2r) = s^2 / r
        jac_pred = [a.sigma ** 2 / x["r"] for x in rows]
        jac_meas = [x["b_norm"] - x["b_proj"] for x in rows]
        jac_err = float(np.abs(np.array(jac_meas) - np.array(jac_pred)).max()
                        / max(np.abs(jac_pred).max(), 1e-30))
        cert[name] = dict(p_true=p, exp_proj=e_proj, exp_norm=e_norm,
                          jac_rel_err=jac_err, rows=rows,
                          mean_se=float(np.mean([x["se"] for x in rows])),
                          signal_at_mid=float(abs(rows[len(rows)//2]["b_proj"])))
        print(f"  {name:15s} p={p:+.0f}: clean estimator exponent = {e_proj:+.3f}"
              f"   |x|-estimator exponent = {e_norm:+.3f}"
              f"   Jacobian term matched to {jac_err:.1%}", flush=True)

    print(f"\n  C3 sample floor (SE = sigma/sqrt(N) per bin):")
    for name, v in cert.items():
        m, se = v["signal_at_mid"], v["mean_se"]
        need10 = (10.0 * a.sigma / max(m, 1e-30)) ** 2
        print(f"    {name:15s} signal {m:.3e}  SE {se:.3e}  "
              f"signal/SE = {m/max(se,1e-30):5.1f}x   "
              f"N/bin for 10-sigma = {need10:.3e}")

    verdict = dict(
        C1_recovers_inverse_square=bool(abs(cert["inverse_square"]["exp_proj"] + 2.0) < 0.25),
        C1_recovers_inverse_r=bool(abs(cert["inverse_r"]["exp_proj"] + 1.0) < 0.25),
        C1_recovers_harmonic=bool(abs(cert["harmonic"]["exp_proj"] - 1.0) < 0.25),
        C1_separates_the_three=bool(
            cert["inverse_square"]["exp_proj"] < cert["inverse_r"]["exp_proj"] - 0.5
            < cert["harmonic"]["exp_proj"] - 1.0),
        C2_jacobian_trap_quantified=bool(
            all(v["jac_rel_err"] < 0.20 for v in cert.values())),
    )
    result = dict(
        note="[exploratory] estimator certification. C1 is the HARD GATE: until "
             "the clean projection estimator recovers -2 for an injected "
             "inverse-square drift, no FIBER-G arm may claim a Newtonian field. "
             "C2 documents that E[d|x|] carries a spurious outward (n_obs-1)s^2/2r "
             "term -- the same 1/r form as the 'naive entropic force' -- which is "
             "pure coordinate Jacobian, not a force.",
        seed=a.seed, sigma=a.sigma, amp_at_half=a.amp,
        fit_window=[LO, HI], cert=cert, verdict=verdict,
        estimator_certified=bool(all(verdict.values())),
        seconds=round(time.time() - t0, 1))
    print(f"\nverdict: {verdict}")
    print(f"ESTIMATOR CERTIFIED: {result['estimator_certified']}")
    print("===FGCERT-JSON===")
    print(json.dumps(result, indent=1, default=float))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
