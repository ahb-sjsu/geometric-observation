#!/usr/bin/env python
"""C3 net for the corrected GO-16 Theorem 3 (thm:diagonal, paper/go16-adversarial-observer.tex):
the diagonal water level, with its blackout regime.

Written 2026-11-20 after VI-30 found the sealed statement (GO-P-2026-090: the water level
at a breakpoint mu_j, "tie iff contested") false on an open set (NEG-17). The corrected
statement adds the blackout regime t* = 0 and reads "tie iff t* = 0 or contested != empty".

The diagonal reduced program, min over rho in [0,1]^n of
    sum_i s_i^2 (1 - rho_i) + lam * (sum of the k largest mu_i rho_i),
is a linear program (top-k(g) = min_t [k t + sum_i (g_i - t)_+]), so scipy's HiGHS solves
it exactly and independently of the theorem. The theorem's closed form is
    J(t) = lam k t + sum_C lam (mu_i - t)_+ + sum_S s_i^2 (1 - t/mu_i)_+,  t >= 0,
minimized over {0} U {mu_i}, with rho_i = 1 on C (lam mu_i < s_i^2) and min(1, t*/mu_i) on S.

Checks (seed 20261122; criteria written before the first run):
  d1_value: on 600 random instances plus the NEG-17 witness, min_{t in {0} U {mu_i}} J(t)
     equals the LP optimum (relative 1e-9), and the closed-form rho(t*) attains it.
  d2_blackout: t* = 0 is a minimizer iff J'(0+) = lam(k - |C|) - sum_S s_i^2/mu_i >= 0, and
     in every blackout instance |C| < k, S is nonempty, and the attention range is feasible:
     sum_S s_i^2/(lam mu_i) <= k - |C| <= |S|.
  d3_tie: at every minimizing t* in {0} U {mu_i}, the tie lambda_k(G*) = lambda_{k+1}(G*)
     (relative 1e-12) holds iff (t* = 0 or some i in S has mu_i > t*).
  d4_power: the sealed statement "tie iff contested" (contested = S with mu_i > t* at a
     positive level, and nothing at t* = 0) is violated on at least one instance, the NEG-17
     witness included; and every instance class appears (blackout, positive level with and
     without contested coordinates), at least 20 times each. (The old and corrected
     predicates differ only at t* = 0, so this amounts to "blackout instances exist, the
     witness among them".)
  d5_attention_duals (added 2026-11-20 after the R-IND-5 re-check found no reader-side
     check): the LP's dual attention theta = -marginal/lam satisfies sum theta = k, theta in
     [0, 1], theta = 1 on conceded coordinates above the level, 0 on submerged ones,
     s^2/(lam mu) on contested ones, and >= s^2/(lam mu) on blacked-out ones.
  d6_lp_vertex_in_family (added with it): the LP's own optimal vertex (rho, t) has t a
     minimizer of J and rho = rho(t), one half of "the diagonal optima are exactly rho(t*)"
     at a vertex.

  d7_optimal_face_and_uniqueness (added 2026-11-21 after the confirming pass VI-35, with
     d8 and d9; criteria written before their first run): the LP's whole optimal face is the
     segment {rho(t) : t in [t1, t2]} of the minimizer interval (support functions in 3n
     directions, 1e-6, via a k-subset epigraph LP independent of the (t, z) LP above), and the
     optimum is unique iff rho(t) is constant there (no S coordinate above t1); coverage: at
     least 100 flat stretches, 50 of them non-unique and 10 flat but unique.
  d8_tie_on_the_interval: the tie lambda_k = lambda_{k+1}, and its value t, at t1, at the
     midpoint and at t2 (at least 50 cases with an interior point).
  d9_attention_ranges: the reader-side LP (max sum min(s_i^2, lam mu_i theta_i)) gives each
     theta_i's range over the reader's optimal face: 1 conceded, s^2/(lam mu) contested, 0
     submerged; a level coordinate exactly J'(mu_j+)/lam, interior at an isolated minimizer,
     0 at the left end of a stretch and min(1, s^2/(lam mu)) at the right end; blacked-out
     coordinates bounded below by s^2/(lam mu), with the range pinned when t2 = 0. Coverage:
     at least 50 stretches at t = 0, 10 level coordinates at isolated minimizers and 10 at
     each end of a stretch.
  The cases for d7-d9 come from their own random stream: three fixed cases (the witness,
  VI-33's E2 example and the paper's integral example), 300 random instances, and stretches
  of J made flat by construction at a positive level (200 attempts) and at t = 0 (100).
  First run: 603 cases, 317 flat stretches, 0 violations. Mutations, each run on a copy:
  putting back VI-33's E1 clause (non-unique on every flat stretch) fails d7; theta_j =
  J'(mu_j-)/lam fails d9; "tie iff contested" inside the interval fails d8.

Scope: the diagonal program only; its equivalence with the full reduced program (diagonality
by sign symmetrization) is proved in the theorem and checked by VI-30, not netted here. d2's
blackout sub-checks (|C| < k, S nonempty, the attention range) follow algebraically from
slope0 >= 0 and k < n, so only its iff can fail (VI-35). (This docstring said until
2026-11-21 that the random instances rarely land on a flat stretch; VI-35 counted 32 of the
601, every positive-level optimum with nothing contested being one, none of them with
contested coordinates.)

Usage: python experiments/verify_go16_diagonal.py   (CPU, seconds)
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np
from scipy.optimize import linprog

SEED = 20261122


def lp_solve(s2, mu, lam, k):
    """Exact optimum of the diagonal program by LP over (rho, t, z), with its primal
    (rho, t) and the reader's attention theta from the duals of mu rho - t - z <= 0."""
    n = len(s2)
    # variables: rho (n), t (1), z (n); objective sum s2 - s2.rho + lam k t + lam sum z
    c = np.concatenate([-s2, [lam * k], lam * np.ones(n)])
    A = np.hstack([np.diag(mu), -np.ones((n, 1)), -np.eye(n)])   # mu rho - t - z <= 0
    b = np.zeros(n)
    bounds = [(0, 1)] * n + [(None, None)] + [(0, None)] * n
    r = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")
    assert r.status == 0, r.message
    theta = -np.asarray(r.ineqlin.marginals) / lam
    return float(r.fun + s2.sum()), r.x[:n], float(r.x[n]), theta


def lp_optimum(s2, mu, lam, k):
    return lp_solve(s2, mu, lam, k)[0]


def J_t(t, s2, mu, lam, k):
    C = lam * mu < s2
    return float(lam * k * t + np.sum(np.where(C, lam * np.maximum(mu - t, 0), s2 * np.maximum(1 - t / mu, 0))))


def rho_t(t, s2, mu, lam):
    C = lam * mu < s2
    return np.where(C, 1.0, np.minimum(1.0, t / mu))


def objective(rho, s2, mu, lam, k):
    g = np.sort(mu * rho)[::-1]
    return float(np.sum(s2 * (1 - rho)) + lam * g[:k].sum())


# ---- d7-d9 (added 2026-11-21 after the confirming pass VI-35 found that nothing here checks
# the clauses VI-33 corrected: uniqueness, the level attention at the ends of a flat
# stretch, the tie inside a stretch). Ported from that pass's independent check, with its
# subset-epigraph LP for the optimal face and a reader-side LP for the attention ranges.
def subset_lp(s2, mu, lam, k):
    """The diagonal program as an LP over (rho, t) with one row per k-subset T:
    sum_{i in T} mu_i rho_i <= t; objective sum s2 (1 - rho) + lam t."""
    import itertools
    n = len(mu)
    subs = list(itertools.combinations(range(n), k))
    A = np.zeros((len(subs), n + 1))
    for r, T in enumerate(subs):
        A[r, list(T)] = mu[list(T)]
        A[r, n] = -1
    return A, np.concatenate([-s2, [lam]])


def face_support(s2, mu, lam, k, V, d):
    """max d.rho over the optimal face {rho : objective = V}."""
    n = len(mu)
    A, c = subset_lp(s2, mu, lam, k)
    A2 = np.vstack([A, c])
    b2 = np.concatenate([np.zeros(len(A)), [V - s2.sum() + 1e-12 * max(1.0, abs(V))]])
    r = linprog(np.concatenate([-d, [0.0]]), A_ub=A2, b_ub=b2,
                bounds=[(0, 1)] * n + [(None, None)], method="highs")
    assert r.status == 0, r.message
    return -r.fun


def theta_ranges(s2, mu, lam, k):
    """The reader's side: max sum_i min(s2_i, lam mu_i theta_i) over theta in [0,1]^n with
    sum theta = k, as an LP in (theta, u); returns its value and, per coordinate, the range
    of theta_i over the optimal face."""
    n = len(mu)
    Aub = np.hstack([-np.diag(lam * mu), np.eye(n)])
    Aeq = np.concatenate([np.ones(n), np.zeros(n)])[None]
    bnds = [(0, 1)] * n + [(None, s2[i]) for i in range(n)]
    r = linprog(np.concatenate([np.zeros(n), -np.ones(n)]), A_ub=Aub, b_ub=np.zeros(n),
                A_eq=Aeq, b_eq=[k], bounds=bnds, method="highs")
    assert r.status == 0, r.message
    Vd = -r.fun
    A2 = np.vstack([Aub, np.concatenate([np.zeros(n), -np.ones(n)])])
    b2 = np.concatenate([np.zeros(n), [-(Vd - 1e-12 * max(1.0, abs(Vd)))]])
    out = []
    for i in range(n):
        e = np.zeros(2 * n)
        e[i] = 1
        lo = linprog(e, A_ub=A2, b_ub=b2, A_eq=Aeq, b_eq=[k], bounds=bnds, method="highs").fun
        hi = -linprog(-e, A_ub=A2, b_ub=b2, A_eq=Aeq, b_eq=[k], bounds=bnds, method="highs").fun
        out.append((lo, hi))
    return Vd, np.array(out)


def slope_plus(t, s2, mu, lam, k):
    C = lam * mu < s2
    above = mu > t
    return lam * k - lam * np.sum(C & above) - np.sum((s2 / mu)[(~C) & above])


def flat_instance(rng, at_zero):
    """An instance whose J is flat on a whole stretch: one submerged-or-contested s_i^2 is
    moved so that J' vanishes on (mu_(j), mu_(j+1)) (or on (0, mu_(1)) when at_zero)."""
    for _ in range(200):
        s2, mu, lam, k = instance(rng)
        n = len(mu)
        C = lam * mu < s2
        order = np.sort(mu)
        if at_zero:
            lo_t, hi_t = 0.0, order[0]
        else:
            j = int(rng.integers(0, n - 1))
            lo_t, hi_t = order[j], order[j + 1]
        tm = 0.5 * (lo_t + hi_t)
        above = mu > tm
        Sa = np.where((~C) & above)[0]
        if len(Sa) == 0:
            continue
        i = int(rng.choice(Sa))
        need = lam * (k - np.sum(C & above)) - np.sum((s2 / mu)[(~C) & above]) + s2[i] / mu[i]
        new = need * mu[i]
        if 1e-3 < new < lam * mu[i] * (1 - 1e-3):
            s2 = s2.copy()
            s2[i] = new
            return s2, mu, lam, k
    return None


def interval_checks(s2, mu, lam, k, rng, stats):
    """d7-d9 on one instance; returns a list of violations (empty if all hold)."""
    bad = []
    n = len(mu)
    C = lam * mu < s2
    S = ~C
    cands = np.sort(np.concatenate([[0.0], mu]))
    Js = np.array([J_t(t, s2, mu, lam, k) for t in cands])
    Jm = Js.min()
    on = cands[np.abs(Js - Jm) <= 1e-10 * max(1.0, abs(Jm))]
    t1, t2 = float(on.min()), float(on.max())
    V = lp_optimum(s2, mu, lam, k)
    r1, r2 = rho_t(t1, s2, mu, lam), rho_t(t2, s2, mu, lam)
    flat = t2 > t1
    stats["flat"] += flat
    stats["flat_at_zero"] += flat and t1 == 0.0
    # d7: the optimal face is the segment {rho(t) : t in [t1, t2]}, and the uniqueness clause
    dirs = list(np.eye(n)) + list(-np.eye(n)) + list(rng.standard_normal((n, n)))
    for d in dirs:
        if abs(face_support(s2, mu, lam, k, V, d) - max(d @ r1, d @ r2)) > 1e-6:
            bad.append(("d7", "face"))
            break
    unique_pred = (not flat) or not np.any(S & (mu > t1))
    if unique_pred != bool(np.max(np.abs(r1 - r2)) < 1e-12):
        bad.append(("d7", "uniqueness clause"))
    stats["flat_nonunique"] += flat and not unique_pred
    stats["flat_but_unique"] += flat and unique_pred
    # d8: the tie and its value at both ends of the minimizer interval and inside it
    for t in sorted({t1, 0.5 * (t1 + t2), t2}):
        g = np.sort(mu * rho_t(t, s2, mu, lam))[::-1]
        tie = abs(g[k - 1] - g[k]) <= 1e-10 * max(1.0, g[0])
        if tie != ((t == 0.0) or bool(np.any(S & (mu > t)))):
            bad.append(("d8", "tie", t))
        if tie and abs(g[k - 1] - t) > 1e-10 * max(1.0, g[0]):
            bad.append(("d8", "tie value", t))
    stats["interior_t"] += flat
    # d9: the reader's attention ranges, coordinate by coordinate
    Vd, th = theta_ranges(s2, mu, lam, k)
    if abs(Vd - V) > 1e-8 * max(1.0, V):
        bad.append(("d9", "dual value"))
    tol = 1e-6
    for t in sorted({t1, t2}):
        for i in range(n):
            lo, hi = th[i]
            cap = s2[i] / (lam * mu[i])
            if t == 0.0 and S[i]:
                if lo < cap - tol:
                    bad.append(("d9", "blackout lower bound", i))
                if t2 == 0.0:
                    others = np.sum((s2 / (lam * mu))[S]) - cap
                    if abs(hi - min(1.0, k - C.sum() - others)) > tol or abs(lo - cap) > tol:
                        bad.append(("d9", "blackout range", i))
                continue
            if mu[i] > t and C[i]:
                ok = abs(lo - 1) < tol and abs(hi - 1) < tol
            elif mu[i] > t and S[i]:
                ok = abs(lo - cap) < tol and abs(hi - cap) < tol
            elif mu[i] < t:
                ok = abs(lo) < tol and abs(hi) < tol
            else:   # a level coordinate, mu_i = t
                pred = slope_plus(t, s2, mu, lam, k) / lam
                ok = abs(lo - pred) < tol and abs(hi - pred) < tol and -tol <= pred <= min(1.0, cap) + tol
                if not flat:
                    ok = ok and tol < pred < min(1.0, cap) - tol
                    stats["level_isolated"] += 1
                elif t == t1:
                    ok = ok and abs(pred) < tol
                    stats["level_left_end"] += 1
                else:
                    ok = ok and abs(pred - min(1.0, cap)) < tol
                    stats["level_right_end"] += 1
            if not ok:
                bad.append(("d9", "attention", i, t))
    return bad


def instance(rng):
    n = int(rng.integers(3, 7))
    k = int(rng.integers(1, n))
    lam = float(rng.uniform(0.3, 3.0))
    mu = rng.permutation(np.sort(rng.uniform(0.2, 5.0, n)))
    s2 = rng.uniform(0.01, 6.0, n) * (rng.random(n) < 0.5) + rng.uniform(0.01, 0.4, n)
    # (G2): keep lam mu_i away from s_i^2
    s2 = np.where(np.abs(lam * mu - s2) < 1e-3, s2 + 0.01, s2)
    return s2, mu, lam, k


def main():
    rng = np.random.default_rng(SEED)
    t0 = time.time()
    cases = [("witness", (np.array([10.0, 0.1, 0.1, 0.1]), np.array([5.0, 3.0, 2.0, 1.0]), 1.0, 2))]
    cases += [(f"r{i}", instance(rng)) for i in range(600)]
    worst_val = 0.0
    d2_ok = d3_ok = d5_ok = d6_ok = True
    old_violations, witness_old_violated = 0, False
    counts = {"blackout": 0, "positive_contested": 0, "positive_integral": 0}
    rows = []
    for name, (s2, mu, lam, k) in cases:
        C = lam * mu < s2
        S = ~C
        cands = np.concatenate([[0.0], mu])
        Js = np.array([J_t(t, s2, mu, lam, k) for t in cands])
        Jmin = Js.min()
        lp = lp_optimum(s2, mu, lam, k)
        attained = objective(rho_t(cands[np.argmin(Js)], s2, mu, lam), s2, mu, lam, k)
        worst_val = max(worst_val, abs(Jmin - lp) / max(1.0, abs(lp)), abs(attained - lp) / max(1.0, abs(lp)))
        slope0 = lam * (k - C.sum()) - np.sum(s2[S] / mu[S])
        black = bool(Js[0] <= Jmin * (1 + 1e-12) + 1e-12)
        if black != (slope0 >= -1e-12):
            d2_ok = False
        if black:
            lo = np.sum(s2[S] / (lam * mu[S]))
            if not (C.sum() < k and S.any() and lo <= k - C.sum() + 1e-12 and k - C.sum() <= S.sum()):
                d2_ok = False
        for t in cands[np.abs(Js - Jmin) <= 1e-12 * max(1.0, abs(Jmin))]:
            g = np.sort(mu * rho_t(t, s2, mu, lam))[::-1]
            tie = bool(abs(g[k - 1] - g[k]) <= 1e-12 * max(1.0, abs(g[0])))
            contested = bool(np.any(S & (mu > t)))
            corrected = (t == 0.0) or contested
            old = contested and t > 0.0
            if tie != corrected:
                d3_ok = False
            if tie != old:
                old_violations += 1
                if name == "witness":
                    witness_old_violated = True
            key = "blackout" if t == 0.0 else ("positive_contested" if contested else "positive_integral")
            counts[key] += 1
        # d5/d6 (added 2026-11-20 after the R-IND-5 re-check found no reader-side check):
        # the LP's own vertex optimum and its dual attention.
        _, rlp, tlp, th = lp_solve(s2, mu, lam, k)
        tol = 1e-7
        if not (abs(J_t(tlp, s2, mu, lam, k) - Jmin) <= 1e-9 * max(1.0, abs(Jmin))
                and np.max(np.abs(rlp - rho_t(tlp, s2, mu, lam))) <= tol):
            d6_ok = False
        if not (abs(th.sum() - k) <= 1e-7 and th.min() >= -tol and th.max() <= 1 + tol):
            d5_ok = False
        for i in range(len(s2)):
            if C[i] and mu[i] > tlp + tol and abs(th[i] - 1) > tol:            # conceded above: read in full
                d5_ok = False
            if mu[i] < tlp - tol and abs(th[i]) > tol:                          # submerged: unread
                d5_ok = False
            if S[i] and tol < rlp[i] < 1 - tol and abs(th[i] - s2[i] / (lam * mu[i])) > 1e-6:  # contested
                d5_ok = False
            if S[i] and tlp <= tol and th[i] < s2[i] / (lam * mu[i]) - 1e-6:    # blacked out
                d5_ok = False
        if name == "witness" or len(rows) < 20:
            rows.append({"case": name, "n": int(len(s2)), "k": k, "Jmin_closed_form": Jmin, "LP": lp,
                         "blackout": black, "slope0": float(slope0)})
    # d7-d9 on their own random stream (so d1-d6 reproduce unchanged): three fixed cases, 300
    # random instances, and constructed flat stretches at a positive level and at t = 0.
    rng2 = np.random.default_rng([SEED, 7])
    stats = {k_: 0 for k_ in ("cases", "flat", "flat_at_zero", "flat_nonunique", "flat_but_unique",
                              "interior_t", "level_isolated", "level_left_end", "level_right_end")}
    fixed = [("witness", (np.array([10.0, 0.1, 0.1, 0.1]), np.array([5.0, 3.0, 2.0, 1.0]), 1.0, 2)),
             ("E2_example", (np.array([2.0, 1.0, 0.5]), np.array([4.0, 2.0, 1.0]), 1.0, 1)),
             ("integral_example", (np.array([5.0, 5.0, 5.0]), np.array([4.0, 2.5, 1.8]), 1.0, 2))]
    more = fixed + [(f"q{i}", instance(rng2)) for i in range(300)]
    for i in range(200):
        x = flat_instance(rng2, at_zero=False)
        if x is not None:
            more.append((f"f{i}", x))
    for i in range(100):
        x = flat_instance(rng2, at_zero=True)
        if x is not None:
            more.append((f"z{i}", x))
    violations = []
    for name, (s2, mu, lam, k) in more:
        stats["cases"] += 1
        violations += [(name,) + v for v in interval_checks(s2, mu, lam, k, rng2, stats)]
    kinds = {v[1] for v in violations}
    verdict = {
        "d1_value": bool(worst_val < 1e-9),
        "d2_blackout": bool(d2_ok),
        "d3_tie": bool(d3_ok),
        "d4_power": bool(old_violations >= 1 and witness_old_violated and min(counts.values()) >= 20),
        "d5_attention_duals": bool(d5_ok),
        "d6_lp_vertex_in_family": bool(d6_ok),
        "d7_optimal_face_and_uniqueness": bool("d7" not in kinds and stats["flat"] >= 100
                                               and stats["flat_nonunique"] >= 50
                                               and stats["flat_but_unique"] >= 10),
        "d8_tie_on_the_interval": bool("d8" not in kinds and stats["interior_t"] >= 50),
        "d9_attention_ranges": bool("d9" not in kinds and stats["flat_at_zero"] >= 50
                                    and stats["level_isolated"] >= 10
                                    and stats["level_left_end"] >= 10 and stats["level_right_end"] >= 10),
    }
    res = {"seed": SEED, "theorem": "GO-16 Theorem 3 (thm:diagonal), corrected 2026-11-20",
           "instances": len(cases), "worst_value_rel": worst_val, "old_statement_violations": old_violations,
           "witness_old_statement_violated": witness_old_violated, "regime_counts": counts, "sample": rows,
           "interval_checks": {"stats": stats, "violations": len(violations),
                               "first_violations": [list(map(str, v)) for v in violations[:10]]},
           "verdict": verdict, "GO16DIAG_supported": all(verdict.values()),
           "seconds": round(time.time() - t0, 1)}
    for k_, v in verdict.items():
        print(f"{k_}: {'PASS' if v else 'FAIL'}")
    print("===GO16DIAG-JSON===")
    print(json.dumps(res, indent=1, default=float))
    print("===END===")
    return 0 if res["GO16DIAG_supported"] else 1


if __name__ == "__main__":
    sys.exit(main())
