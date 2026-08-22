"""GO-16 discrete twin -- opening probe (EXPLORATORY, disclosed).

The discrete disclosure game, mirroring the diagonal LQG theorem
(go16-adversarial-observer.tex v0.2, Theorem 3):

  n coordinates ("spots"); private bits X_i ~ Bern(1/2) iid.
  Encoder's per-coordinate policy: binary action A_i with
  q0 = P(A=1|X=0) (the bluff frequency), q1 = P(A=1|X=1) (the value
  frequency).  Value loss: s_i^2 * P(A_i != X_i).
  Reader: watches k of n coordinates (mixed subset choice = marginal
  attention theta, 0<=theta<=1, sum = k); a watched coordinate leaks
  g_i = mu_i * rho_i where rho_i = resolved-variance ratio
  (1 - 4 E[Var(X_i|A_i)]) -- the discrete SNR.
  Encoder commits; reader best-responds:  J = sum_i s_i^2 err_i
  + lambda * (sum of top-k g_i).

Predictions under test (the twin conjecture, reading fixed by v0.2):
  P1  The per-coordinate frontier e(rho) = min err at resolved ratio
      rho is convex decreasing and NOT linear (the LQG linearity is a
      Gaussian privilege); deterministic policies give rho in {0,1}
      only -- the exact discrete carrier of "noiseless records are
      idempotent revelators": fractional revelation REQUIRES mixing.
  P2  Main instance (the LQG hand instance transplanted): the
      optimum's KKT structure survives with the GENERALIZED pricing
      theta_i = -c_i'(rho_i)/(lambda mu_i) on fractional-attention
      coordinates; attention budget sums to k; the tie among
      fractional-attention coordinates survives (it is reader-side,
      curvature-independent).
  P3  The new class LQG forbids: with convex cost, a coordinate can
      be shielded to an INTERIOR FOC strictly above the water level
      with theta = 1 and NO tie ("partial balancing without
      indifference").  Hand-derived instance mu=(4,1,0.5),
      s2=(12,5,1), lambda=1, k=1: rho_1 = 0.5625, g_1 = 2.25 vs
      g_2 = 1 (strict gap), J* = 3.75.
  P4  Every shielded coordinate at the optimum uses a strictly
      randomized policy (interior q0 or q1) -- bluffing frequencies
      reported.

Deterministic, numpy only.  Seed-free (grid computations).
Exploratory: no prereg governs this run.
"""

import json
import numpy as np

GRID = 2001  # q-grid and rho-grid resolution
SADDLE_SEED = 20260821  # dev default; the governed run overrides via argv


# ---------------------------------------------------------------- frontier
def channel_stats(q0, q1):
    """err = P(A != X); rho = 1 - 4 E[Var(X|A)] for X ~ Bern(1/2)."""
    err = 0.5 * (q0 + (1.0 - q1))
    sa = q0 + q1
    sb = 2.0 - q0 - q1
    t1 = np.where(sa > 0, q0 * q1 / (2.0 * np.maximum(sa, 1e-300)), 0.0)
    t2 = np.where(sb > 0, (1 - q0) * (1 - q1) / (2.0 * np.maximum(sb, 1e-300)), 0.0)
    rho = 1.0 - 4.0 * (t1 + t2)
    return err, rho


def build_frontier():
    """e(rho): min err over all (q0, q1) at resolved ratio rho (binned),
    plus the symmetric-channel curve for comparison."""
    q = np.linspace(0, 1, GRID)
    Q0, Q1 = np.meshgrid(q, q, indexing="ij")
    err, rho = channel_stats(Q0, Q1)
    rho = np.clip(rho, 0.0, 1.0)
    bins = np.linspace(0, 1, GRID)
    idx = np.minimum((rho * (GRID - 1)).astype(int), GRID - 1)
    e = np.full(GRID, np.inf)
    np.minimum.at(e, idx.ravel(), err.ravel())
    # enforce the frontier is attainable at-or-above each rho
    # (shielding less is always allowed): running min from the right
    for i in range(GRID - 2, -1, -1):
        e[i] = min(e[i], e[i + 1] + 0.0)  # e is decreasing in rho? no:
    # err decreases as rho -> 1; frontier e(rho) is DEcreasing in rho.
    # A record achieving rho' > rho can be degraded to rho by mixing
    # with an uninformative record only at extra err cost -- so no
    # monotonization from the right is valid; undo (keep raw bins).
    e2 = np.full(GRID, np.inf)
    np.minimum.at(e2, idx.ravel(), err.ravel())
    e = e2
    # fill any empty bins by neighbor interpolation
    bad = ~np.isfinite(e)
    if bad.any():
        good = np.where(~bad)[0]
        e[bad] = np.interp(np.where(bad)[0], good, e[good])
    e_sym = 0.5 * (1.0 - np.sqrt(bins))  # symmetric channel candidate
    return bins, e, e_sym


def deterministic_rhos():
    out = []
    for q0 in (0.0, 1.0):
        for q1 in (0.0, 1.0):
            _, rho = channel_stats(np.array(q0), np.array(q1))
            out.append(float(rho))
    return out


# ---------------------------------------------------------------- solver
def solve_game(mu, s2, lam, k, bins, e):
    """Minimize sum_i s2_i e(rho_i) + lam * top-k(mu*rho) via the
    variational t-representation; exact on the grid."""
    mu = np.asarray(mu, float)
    s2 = np.asarray(s2, float)
    n = len(mu)
    tgrid = np.linspace(0, float(mu.max()), GRID)
    # per-coordinate cost matrix over (t, rho) minimized over rho
    best_rho = np.zeros((GRID, n))
    best_val = np.zeros((GRID, n))
    for i in range(n):
        c = s2[i] * e  # cost over rho-grid
        g = mu[i] * bins
        # value(t, rho) = c(rho) + lam * max(g - t, 0)
        # vectorized over t via broadcasting
        V = c[None, :] + lam * np.maximum(g[None, :] - tgrid[:, None], 0.0)
        j = np.argmin(V, axis=1)
        best_rho[:, i] = bins[j]
        best_val[:, i] = V[np.arange(GRID), j]
    Jt = best_val.sum(axis=1) + lam * k * tgrid
    it = int(np.argmin(Jt))
    t_star = float(tgrid[it])
    rho = best_rho[it]
    g = mu * rho
    # exact objective at the reconstructed point
    cost = float(np.sum(s2 * np.interp(rho, bins, e)))
    leak = float(np.sum(np.sort(g)[::-1][:k]))
    return {"t": t_star, "J": cost + lam * leak, "rho": rho, "g": g,
            "cost": cost, "leak": leak}


def encoder_response(s2i, mui, lam, theta_i, bins, e):
    """R(theta): the encoder's best-response rho given attention theta_i
    (derivative-free: argmin over the binned frontier)."""
    vals = s2i * e + lam * theta_i * mui * bins
    return float(bins[int(np.argmin(vals))])


def inverse_pricing(s2i, mui, lam, rho_i, bins, e, iters=50):
    """theta_i such that the encoder's best response reproduces rho_i
    (bisection; R is nonincreasing in theta)."""
    lo, hi = 0.0, 1.0
    if encoder_response(s2i, mui, lam, 1.0, bins, e) > rho_i:
        return 1.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if encoder_response(s2i, mui, lam, mid, bins, e) > rho_i:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def classify(mu, s2, lam, k, sol, bins, e, tol=5e-3):
    mu = np.asarray(mu, float)
    s2 = np.asarray(s2, float)
    t, rho, g = sol["t"], sol["rho"], sol["g"]
    n = len(mu)
    scale = max(g.max(), 1e-12)
    above = g > t + tol * scale
    level = np.abs(g - t) <= tol * scale
    shielded = rho < 1 - tol
    theta = np.zeros(n)
    theta[above] = 1.0
    # derivative-free generalized pricing on the fractional (level) group:
    # theta_i inverts the encoder's best-response map at rho_i
    for i in range(n):
        if level[i] and shielded[i]:
            theta[i] = inverse_pricing(s2[i], mu[i], lam, rho[i], bins, e)
    slack_idx = [i for i in range(n) if level[i] and not shielded[i]]
    slack = k - theta.sum()
    if slack_idx:
        theta[slack_idx[0]] += slack
    classes = {
        "conceded_above": [i for i in range(n) if above[i] and not shielded[i]],
        "interior_contested_above": [i for i in range(n) if above[i] and shielded[i]],
        "tied_contested": [i for i in range(n) if level[i] and shielded[i]],
        "level_unshielded": slack_idx,
        "submerged": [i for i in range(n) if g[i] < t - tol * scale],
    }
    return theta, classes


def encoder_saddle_check(mu, s2, lam, sol, theta, bins, e):
    """Encoder-side saddle verification, derivative-free: given theta,
    each coordinate's played rho must be best-response optimal (compare
    objective values, robust to grid staircase)."""
    worst = 0.0
    for i in range(len(mu)):
        vals = s2[i] * e + lam * theta[i] * mu[i] * bins
        played = s2[i] * float(np.interp(sol["rho"][i], bins, e)) \
            + lam * theta[i] * mu[i] * sol["rho"][i]
        worst = max(worst, played - float(vals.min()))
    return worst


# ---------------------------------------------------------------- parts
def refine_frontier_point(rho_target):
    """Exact local check at fixed rho: minimize err over (q0, q1) with
    rho pinned, via SLSQP from several starts (analytic formulas, no
    binning)."""
    from scipy.optimize import minimize as smin
    best = np.inf
    arg = None
    eps_t = (1 - np.sqrt(rho_target)) / 2      # symmetric start
    beta = (1 - rho_target) / (1 + rho_target)  # bluff-only start
    for x0 in ([eps_t, 1 - eps_t], [beta, 1.0], [0.0, 1 - beta],
               [eps_t / 2, 1 - 2 * eps_t]):
        r = smin(lambda x: 0.5 * (x[0] + 1 - x[1]), x0=np.array(x0),
                 method="SLSQP", bounds=[(0, 1), (0, 1)],
                 constraints=[{"type": "eq",
                               "fun": lambda x: channel_stats(
                                   np.array(x[0]), np.array(x[1]))[1]
                               - rho_target}],
                 options=dict(maxiter=400, ftol=1e-14))
        if r.success and r.fun < best:
            best = r.fun
            arg = [float(r.x[0]), float(r.x[1])]
    return float(best), arg


def part1():
    bins, e, e_sym = build_frontier()
    d = np.diff(e)
    dec_viol = float(np.max(np.maximum(d, 0)))          # should be ~<= 0
    d2 = np.diff(e, 2)
    conv_viol = float(np.max(np.maximum(-d2, 0)))        # grid-noise scale
    lqg_line = 0.5 * (1 - bins)  # LQG shape at matched endpoints
    lqg_dev = float(np.max(np.abs(e - lqg_line)))
    det = deterministic_rhos()
    det_ok = all(min(abs(r - 0), abs(r - 1)) < 1e-12 for r in det)
    # exact refinement at interior rho: is the symmetric channel the
    # frontier, or do asymmetric (bluff-weighted) channels beat it?
    refined = []
    asym_wins = 0
    frontier_ok = True
    for rt in (0.1, 0.3, 0.5, 0.7, 0.9):
        err_full, argq = refine_frontier_point(rt)
        err_sym = 0.5 * (1 - np.sqrt(rt))
        beats = err_full < err_sym - 1e-9
        asym_wins += int(beats)
        frontier_ok &= err_full <= err_sym + 1e-9
        refined.append({"rho": rt, "err_full": err_full,
                        "err_sym": float(err_sym),
                        "asym_beats_sym": bool(beats), "q_opt": argq})
    return bins, e, {
        "monotone_violation": dec_viol,
        "convexity_violation_gridscale": conv_viol,
        "max_dev_from_LQG_line": lqg_dev,
        "deterministic_rhos": det,
        "refined_points": refined,
        "asym_beats_sym_count": asym_wins,
        "pass": bool(dec_viol < 1e-6 and conv_viol < 2e-3
                     and det_ok and frontier_ok),
    }


def analytic_solve(mu, s2, lam, k):
    """Exact water-level solution on the VALIDATED analytic frontier
    e(rho) = (1 - sqrt(rho))/2 (P1: symmetric channel is the frontier,
    SLSQP-refined to 1e-12).  Per coordinate given level t:
      interior FOC rho_int = (s^2/(4 lam mu))^2 (clipped at 1);
      mu <= t              -> submerged (rho=1, theta=0);
      rho_int > t/mu       -> above water: rho = min(rho_int, 1),
                              theta = 1 (interior-contested if rho<1,
                              conceded if rho=1);
      else                 -> tied: rho = t/mu, g = t,
                              theta = s^2/(4 lam sqrt(mu t)).
    Water level t* pinned by attention budget D(t*) = k (bisection)."""
    mu = np.asarray(mu, float)
    s2 = np.asarray(s2, float)
    n = len(mu)

    def coord(t):
        rho = np.ones(n)
        theta = np.zeros(n)
        rho_int = np.minimum(1.0, (s2 / (4 * lam * mu)) ** 2)
        for i in range(n):
            if mu[i] <= t:
                rho[i], theta[i] = 1.0, 0.0
            elif rho_int[i] > t / mu[i]:
                rho[i], theta[i] = rho_int[i], 1.0
            else:
                rho[i] = t / mu[i]
                theta[i] = s2[i] / (4 * lam * np.sqrt(mu[i] * t))
        return rho, theta

    def D(t):
        return float(coord(t)[1].sum())

    lo, hi = 1e-12, float(mu.max())
    if D(hi) >= k:
        t_star = hi
    elif D(lo) <= k:
        t_star = lo
    else:
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if D(mid) > k:
                lo = mid
            else:
                hi = mid
        t_star = 0.5 * (lo + hi)
    rho, theta = coord(t_star)
    g = mu * rho
    cost = float(np.sum(s2 * 0.5 * (1 - np.sqrt(rho))))
    above = g > t_star * (1 + 1e-9)
    a = int(above.sum())
    leak = float(g[above].sum() + max(0, k - a) * t_star)
    return {"t": float(t_star), "J": cost + lam * leak, "rho": rho,
            "g": g, "theta": theta, "cost": cost, "leak": leak}


def analytic_classify(mu, s2, lam, sol, tol=1e-7):
    mu = np.asarray(mu, float)
    s2 = np.asarray(s2, float)
    t, rho, g, theta = sol["t"], sol["rho"], sol["g"], sol["theta"]
    n = len(mu)
    scale = max(g.max(), 1e-12)
    above = g > t + tol * scale
    level = np.abs(g - t) <= tol * scale
    shielded = rho < 1 - tol
    return {
        "conceded_above": [i for i in range(n) if above[i] and not shielded[i]],
        "interior_contested_above": [i for i in range(n) if above[i] and shielded[i]],
        "tied_contested": [i for i in range(n) if level[i] and shielded[i]],
        "level_unshielded": [i for i in range(n) if level[i] and not shielded[i]],
        "submerged": [i for i in range(n) if g[i] < t - tol * scale],
    }


def saddle_check_discrete(mu, s2, lam, k, sol, trials=500, seed=None):
    """Two-sided saddle verification on the reduced game
    J~(rho, theta) = sum s2 e(rho) + lam sum theta mu rho:
    reader side: no feasible theta beats theta* against rho*;
    encoder side: each rho_i is best-response to theta* (1D exact)."""
    rng = np.random.default_rng(SADDLE_SEED if seed is None else seed)
    mu = np.asarray(mu, float)
    s2 = np.asarray(s2, float)
    n = len(mu)
    g, theta = sol["g"], sol["theta"]
    base_read = float(np.sum(theta * g))
    worst_reader = 0.0
    for _ in range(trials):
        v = rng.uniform(0, 1, n)
        lo, hi = 0.0, 1e3
        for _ in range(60):
            a = 0.5 * (lo + hi)
            if np.sum(np.minimum(1.0, a * v)) < k:
                lo = a
            else:
                hi = a
        th = np.minimum(1.0, 0.5 * (lo + hi) * v)
        worst_reader = max(worst_reader, float(np.sum(th * g)) - base_read)
    # encoder side: exact 1D best response on the analytic frontier
    worst_enc = 0.0
    for i in range(n):
        th = theta[i]
        # min over rho of s2*(1-sqrt(rho))/2 + lam*th*mu*rho:
        # FOC sqrt(rho) = s2/(4 lam th mu) (or boundary rho=1 / rho->0)
        cands = [1.0, 1e-16]
        if th > 1e-15:
            r = (s2[i] / (4 * lam * th * mu[i])) ** 2
            if r < 1:
                cands.append(r)
        vals = [s2[i] * 0.5 * (1 - np.sqrt(r)) + lam * th * mu[i] * r
                for r in cands]
        played = s2[i] * 0.5 * (1 - np.sqrt(sol["rho"][i])) \
            + lam * th * mu[i] * sol["rho"][i]
        worst_enc = max(worst_enc, played - min(vals))
    return worst_reader, worst_enc


def part2(bins, e):
    mu = [4.0, 2.5, 1.8, 1.0, 0.55, 0.3]
    s2 = [0.5, 3.0, 0.4, 2.0, 0.3, 0.25]
    lam, k = 1.0, 2
    sol = analytic_solve(mu, s2, lam, k)
    classes = analytic_classify(mu, s2, lam, sol)
    theta = sol["theta"]
    grid_sol = solve_game(mu, s2, lam, k, bins, e)   # independent solver
    grid_gap = abs(grid_sol["J"] - sol["J"])
    tie_frac_group = 0.0
    frac_ids = classes["tied_contested"] + classes["level_unshielded"]
    if len(frac_ids) >= 2:
        gv = [sol["g"][i] for i in frac_ids]
        tie_frac_group = float(max(gv) - min(gv))
    budget_err = abs(float(theta.sum()) - k)
    theta_ok = bool(np.all(theta > -1e-9) and np.all(theta < 1 + 1e-9))
    worst_reader, worst_enc = saddle_check_discrete(mu, s2, lam, k, sol)
    return {
        "instance": {"mu": mu, "s2": s2, "lambda": lam, "k": k},
        "t": sol["t"], "J": sol["J"], "J_grid_independent": grid_sol["J"],
        "grid_vs_analytic_gap": float(grid_gap),
        "rho": [float(x) for x in sol["rho"]],
        "g": [float(x) for x in sol["g"]],
        "theta": [float(x) for x in theta],
        "classes": classes,
        "tie_within_fractional_group": tie_frac_group,
        "budget_err": float(budget_err),
        "saddle_worst_reader": float(worst_reader),
        "saddle_worst_encoder": float(worst_enc),
        "pass": bool(budget_err < 1e-6 and theta_ok
                     and tie_frac_group < 1e-9
                     and grid_gap < 2.5e-3
                     and worst_reader < 1e-9 and worst_enc < 1e-9),
    }


def part3(bins, e):
    mu = [4.0, 1.0, 0.5]
    s2 = [12.0, 5.0, 1.0]
    lam, k = 1.0, 1
    sol = analytic_solve(mu, s2, lam, k)
    classes = analytic_classify(mu, s2, lam, sol)
    theta = sol["theta"]
    grid_sol = solve_game(mu, s2, lam, k, bins, e)   # independent solver
    grid_gap = abs(grid_sol["J"] - sol["J"])
    rho1 = float(sol["rho"][0])
    g = sol["g"]
    gap = float(g[0] - g[1])
    worst_reader, worst_enc = saddle_check_discrete(mu, s2, lam, k, sol)
    ok = (abs(rho1 - 0.5625) < 1e-9          # exact hand prediction
          and abs(sol["J"] - 3.75) < 1e-9
          and abs(gap - 1.25) < 1e-9         # strict, far from tie
          and 0 in classes["interior_contested_above"]
          and abs(theta[0] - 1.0) < 1e-9
          and grid_gap < 2.5e-3
          and worst_reader < 1e-9 and worst_enc < 1e-9)
    return {
        "instance": {"mu": mu, "s2": s2, "lambda": lam, "k": k},
        "predicted": {"rho1": 0.5625, "J": 3.75, "g1_minus_g2": 1.25},
        "t": sol["t"], "J": sol["J"], "J_grid_independent": grid_sol["J"],
        "grid_vs_analytic_gap": float(grid_gap),
        "rho": [float(x) for x in sol["rho"]],
        "g": [float(x) for x in g],
        "theta": [float(x) for x in theta],
        "classes": classes,
        "strict_gap_g1_g2": gap,
        "saddle_worst_reader": float(worst_reader),
        "saddle_worst_encoder": float(worst_enc),
        "pass": bool(ok),
    }


def part4(bins, e, p2, p3):
    """Recover the bluffing frequencies (q0, q1) implementing each
    shielded coordinate's rho at frontier cost."""
    q = np.linspace(0, 1, GRID)
    Q0, Q1 = np.meshgrid(q, q, indexing="ij")
    err, rho = channel_stats(Q0, Q1)
    rows = []
    interior_all = True
    for tag, res in (("main", p2), ("interior", p3)):
        for i, r in enumerate(res["rho"]):
            if r < 1 - 5e-3:
                mask = np.abs(rho - r) < 2e-3
                if not mask.any():
                    continue
                errs = np.where(mask, err, np.inf)
                j = np.unravel_index(np.argmin(errs), errs.shape)
                q0, q1 = float(q[j[0]]), float(q[j[1]])
                interior = (1e-6 < q0 < 1 - 1e-6) or (1e-6 < q1 < 1 - 1e-6)
                interior_all &= interior
                rows.append({"instance": tag, "coord": i, "rho": float(r),
                             "q0_bluff": q0, "q1_value": q1,
                             "randomized": bool(interior)})
    return {"shielded_policies": rows, "pass": bool(interior_all and rows)}


def main(seed=20260821):
    global SADDLE_SEED
    SADDLE_SEED = seed
    bins, e, p1 = part1()
    p2 = part2(bins, e)
    p3 = part3(bins, e)
    p4 = part4(bins, e, p2, p3)
    gates = [p1["pass"], p2["pass"], p3["pass"], p4["pass"]]
    return {
        "grid": GRID,
        "saddle_seed": SADDLE_SEED,
        "P1_frontier": p1,
        "P2_main_instance": p2,
        "P3_interior_contested": p3,
        "P4_mixing_carrier": p4,
        "ALL_PASS": bool(all(gates)),
        "gates_passed": f"{sum(gates)}/{len(gates)}",
    }


if __name__ == "__main__":
    import sys
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20260821
    res = main(seed)
    print("GO16_DISCRETE_TWIN_BEGIN")
    print(json.dumps(res, indent=1))
    print("GO16_DISCRETE_TWIN_END")
