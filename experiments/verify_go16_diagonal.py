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

Scope: the diagonal program only; its equivalence with the full reduced program (diagonality
by sign symmetrization) is proved in the theorem and checked by VI-30, not netted here. The
random instances rarely land on a flat stretch of J, so the flat-stretch clauses (non-unique
optima, a level slack at 0 or at its cap) are checked by the R-IND-5 re-check's own 3000-
instance primal-dual run (517 constructed flat stretches, 0 violations), not here.

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
    verdict = {
        "d1_value": bool(worst_val < 1e-9),
        "d2_blackout": bool(d2_ok),
        "d3_tie": bool(d3_ok),
        "d4_power": bool(old_violations >= 1 and witness_old_violated and min(counts.values()) >= 20),
        "d5_attention_duals": bool(d5_ok),
        "d6_lp_vertex_in_family": bool(d6_ok),
    }
    res = {"seed": SEED, "theorem": "GO-16 Theorem 3 (thm:diagonal), corrected 2026-11-20",
           "instances": len(cases), "worst_value_rel": worst_val, "old_statement_violations": old_violations,
           "witness_old_statement_violated": witness_old_violated, "regime_counts": counts, "sample": rows,
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
