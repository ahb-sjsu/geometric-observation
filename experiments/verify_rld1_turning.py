#!/usr/bin/env python
"""C3 net for RLD-I Theorem 20 (thm:turning, paper/tit-rate-leakage): when the direction of
the best one-dimensional description turns with the budget.

Setting (paper one, Theorem 16(a)): A(Delta) = Sigma Q Sigma - Delta Sigma,
Kc = (Sigma^-1 + J)^-1, mu_max(Delta) the largest generalized eigenvalue of the pencil
(A(Delta), Kc) and b(Delta) its eigenvector, for 0 < Delta < lambda_max(Q^1/2 Sigma Q^1/2).
Here F = I and W = Q > 0. Delta is the paper's budget parameter, not the distortion.

Theorem 20: on an interval where mu_max is simple, b(Delta) spans one line throughout iff,
for some Delta0 in it, b0 = b(Delta0) satisfies Q Sigma b0 = lam b0 and J Sigma b0 = vs b0;
otherwise b(Delta) is constant on no open subinterval.

A fact the checks rely on (found by the R-IND-5 pass on this harness, VI-29): once
b0 = b(Delta0) is on the curve, EITHER equation implies the other. Q Sigma b0 = lam b0 gives
Sigma b0 = c Kc b0 with c = mu/(lam - Delta0), hence J Sigma b0 = (c - 1) b0; the converse
is the same computation. So "constancy requires only one equation" is not a false variant,
and an earlier version of this file wrongly claimed to refute it. The false variants that
matter drop the condition that b0 lies on the curve, or demand vs = 0.

Checks (revised 2026-11-20 after VI-29, which also found the earlier simplicity test blind
to crossings between grid points; the revision is disclosed, not hidden):
  t1_common_top_constant: b0 satisfies both equations with vs > 0, and lam is large enough
     that b0 is the top line on the whole interval. Pass: mu_max equals b0's branch
     (lam - Delta)(1 + vs) (relative 1e-9) at every grid point, mu_max is simple there
     (relative gap to the next eigenvalue > 1e-8), and b(Delta) is on b0's line
     (angle < 1e-11) throughout. Refutes "constancy requires vs = 0".
  t2_common_not_top_turns: b0 satisfies both equations but lam is so small that b0 is
     never the top line. Pass: b(Delta) turns at every grid step (atan2 angle > 1e-12) and
     in total by > 1e-3 rad. Refutes "constant iff Q Sigma and J Sigma share an
     eigenvector" (the variant that drops b0 = b(Delta0)).
  t3_crossing: b0 is common and top at small Delta, then overtaken by another branch. Pass:
     before the crossing, constancy and simplicity as in t1; at the first point after it,
     b0's branch is the SECOND eigenvalue (relative 1e-9), so the departure is a real
     crossing and not a simple eigenvalue leaving its branch; after it, turning at every
     step (> 1e-12) and in total > 1e-4 rad.
  t4_generic_turns: random Sigma, Q, J. Pass: turning at every step, total > 1e-3 rad.
  t5_perturbed_turns: t1's instances with J replaced by J + eps G (G random PSD, eps in
     1e-6, 1e-4, 1e-2). Pass: the unperturbed instance turns by < 1e-10 in total; the
     perturbed ones by > 1e-8 (eps = 1e-6) and > 1e-3 (eps = 1e-2); and the turn grows
     linearly, total(1e-4)/total(1e-6) in [30, 300]. So a loss of the common eigenvector as
     small as eps = 1e-6 already makes the line turn.
  Instance searches are capped (2000 tries); a family that cannot be filled FAILS. The
  rejection counts are recorded.

Scope (stated, not tested): Q > 0 only (F = I, W = Q), so the singular-Q case of
Corollary cor:context is not covered; vs = 0 is not exercised; p is 3, 4 or 5.

Provenance: the file was untracked when its first version ran, so there is no custody
evidence that criteria preceded runs. This version's criteria were written before its
first run, and the file is committed before CI runs it.

Usage: python experiments/verify_rld1_turning.py   (seed 20261120, CPU, seconds)
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np
from scipy.linalg import eigh

SEED = 20261120
GRID = 400


def spd(rng, p, lo=0.3, hi=3.0):
    U, _ = np.linalg.qr(rng.standard_normal((p, p)))
    return U @ np.diag(rng.uniform(lo, hi, p)) @ U.T


def psd_perp(rng, p, g, rank):
    """A random PSD matrix of the given rank that annihilates g."""
    R = np.eye(p) - np.outer(g, g) / (g @ g)
    B = R @ rng.standard_normal((p, rank))
    return B @ B.T


def angle(a, b):
    """Angle between the lines of a and b, resolved to ~1e-16 (atan2, not arccos)."""
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    d = abs(a @ b)
    return float(np.arctan2(np.linalg.norm(a - (a @ b) * b), d))


def top(Sigma, Q, Kc, Delta):
    """Top and second generalized eigenvalues of (A(Delta), Kc), and the top eigenvector."""
    w, V = eigh(Sigma @ Q @ Sigma - Delta * Sigma, Kc)
    return w[-1], w[-2], V[:, -1] / np.linalg.norm(V[:, -1])


def sweep(Sigma, Q, J):
    Kc = np.linalg.inv(np.linalg.inv(Sigma) + J)
    L = np.linalg.cholesky(Q)
    dmax = np.linalg.eigvalsh(L.T @ Sigma @ L).max()
    Deltas = np.linspace(dmax / (GRID + 1), dmax * GRID / (GRID + 1), GRID)
    out = [top(Sigma, Q, Kc, d) for d in Deltas]
    return (Deltas, np.array([o[0] for o in out]), np.array([o[1] for o in out]),
            [o[2] for o in out])


def step_angles(bs, idx):
    return [angle(bs[i], bs[j]) for i, j in zip(idx[:-1], idx[1:])]


def common(rng, p, vs, lam_scale):
    """Sigma, Q, J, b0, lam with Q Sigma b0 = lam b0 and J Sigma b0 = vs b0 exactly.

    Q = lam b0 b0'/s + Qp, J = vs b0 b0'/s + Jp, s = b0'Sigma b0, with Qp, Jp PSD and
    annihilating g = Sigma b0; Q > 0 because Qp has rank p - 1 on g's complement."""
    Sigma = spd(rng, p)
    b0 = rng.standard_normal(p)
    b0 /= np.linalg.norm(b0)
    g = Sigma @ b0
    s = b0 @ g
    Qp = 0.3 * psd_perp(rng, p, g, p - 1)
    J = vs * np.outer(b0, b0) / s + psd_perp(rng, p, g, max(1, p - 2))
    lam = lam_scale * np.linalg.eigvalsh(Sigma).max()
    Q = lam * np.outer(b0, b0) / s + Qp
    return Sigma, Q, J, b0, lam


def branch(Deltas, lam, vs):
    return (lam - Deltas) * (1 + vs)


def close(x, y, rel=1e-9):
    return np.abs(x - y) <= rel * np.abs(y)


TRIES = 2000


def main():
    rng = np.random.default_rng(SEED)
    t0 = time.time()
    res = {"seed": SEED, "grid": GRID, "theorem": "RLD-I Theorem 20 (thm:turning)", "sections": {},
           "rejections": {}}
    verdict = {}

    # t1: common, and top on the whole interval -> constant and simple throughout.
    rows, ok_all, t1_inst, tries = [], True, [], 0
    while len(rows) < 12 and tries < TRIES:
        tries += 1
        p = 3 + len(rows) % 3
        vs = float(rng.uniform(0.5, 4.0))
        Sigma, Q, J, b0, lam = common(rng, p, vs, 8.0)
        Deltas, mus, mu2, bs = sweep(Sigma, Q, J)
        br = close(mus, branch(Deltas, lam, vs))
        if not br[0]:            # design: b0 must be top at the smallest budget
            continue
        gap = float(np.min((mus - mu2) / np.abs(mus)))
        worst = max(angle(b, b0) for b in bs)
        ok = bool(br.all() and gap > 1e-8 and worst < 1e-11)
        ok_all &= ok
        t1_inst.append((Sigma, Q, J))
        rows.append({"p": p, "vs": vs, "lam": lam, "on_branch_points": int(br.sum()),
                     "min_rel_gap": gap, "worst_angle_rad": worst, "ok": ok})
    res["rejections"]["t1"] = tries - len(rows)
    res["sections"]["t1_common_top_constant"] = rows
    verdict["t1_common_top_constant"] = bool(ok_all and len(rows) == 12)

    # t2: common but never top -> must turn.
    rows, ok_all, tries = [], True, 0
    while len(rows) < 12 and tries < TRIES:
        tries += 1
        p = 3 + len(rows) % 3
        vs = float(rng.uniform(0.5, 4.0))
        Sigma, Q, J, b0, lam = common(rng, p, vs, 0.02)
        Deltas, mus, mu2, bs = sweep(Sigma, Q, J)
        if close(mus, branch(Deltas, lam, vs)).any():   # design: b0 never the top line
            continue
        steps = step_angles(bs, list(range(GRID)))
        ok = bool(min(steps) > 1e-12 and sum(steps) > 1e-3)
        ok_all &= ok
        rows.append({"p": p, "vs": vs, "lam": lam, "smallest_step_rad": min(steps),
                     "total_turn_rad": sum(steps), "closest_to_b0_rad": min(angle(b, b0) for b in bs),
                     "ok": ok})
    res["rejections"]["t2"] = tries - len(rows)
    res["sections"]["t2_common_not_top_turns"] = rows
    verdict["t2_common_not_top_turns"] = bool(ok_all and len(rows) == 12)

    # t3: common, top at small Delta, then overtaken -> constant before, a real crossing, turning after.
    rows, ok_all, tries = [], True, 0
    while len(rows) < 6 and tries < TRIES:
        tries += 1
        p = 3 + len(rows) % 3
        vs = float(rng.uniform(0.5, 4.0))
        Sigma, Q, J, b0, lam = common(rng, p, vs, float(rng.uniform(0.3, 2.0)))
        Deltas, mus, mu2, bs = sweep(Sigma, Q, J)
        bra = branch(Deltas, lam, vs)
        br = close(mus, bra)
        if not br[0] or br.all():
            continue
        k = int(np.argmin(br))                      # first point off b0's branch
        if br[k:].any() or k < 5 or GRID - k < 20:  # design: one clean crossing, room both sides
            continue
        gap_before = float(np.min((mus[:k] - mu2[:k]) / np.abs(mus[:k])))
        before = max(angle(bs[i], b0) for i in range(k))
        second_is_branch = bool(close(mu2[k], bra[k]))
        steps = step_angles(bs, list(range(k + 1, GRID)))
        ok = bool(before < 1e-11 and gap_before > 1e-8 and second_is_branch
                  and min(steps) > 1e-12 and sum(steps) > 1e-4)
        ok_all &= ok
        rows.append({"p": p, "vs": vs, "crossing_index": k, "worst_angle_before_rad": before,
                     "min_rel_gap_before": gap_before, "branch_is_second_after": second_is_branch,
                     "smallest_step_after_rad": min(steps), "total_turn_after_rad": sum(steps), "ok": ok})
    res["rejections"]["t3"] = tries - len(rows)
    res["sections"]["t3_crossing"] = rows
    verdict["t3_crossing"] = bool(ok_all and len(rows) == 6)

    # t4: generic.
    rows, ok_all = [], True
    for k in range(12):
        p = 3 + k % 3
        Sigma, Q = spd(rng, p), spd(rng, p)
        H = rng.standard_normal((2, p))
        _, _, _, bs = sweep(Sigma, Q, H.T @ H)
        steps = step_angles(bs, list(range(GRID)))
        ok = bool(min(steps) > 1e-12 and sum(steps) > 1e-3)
        ok_all &= ok
        rows.append({"p": p, "smallest_step_rad": min(steps), "total_turn_rad": sum(steps), "ok": ok})
    res["sections"]["t4_generic_turns"] = rows
    verdict["t4_generic_turns"] = bool(ok_all)

    # t5: perturb t1's J off the common structure; the line must turn, linearly in eps.
    rows, ok_all = [], True
    for Sigma, Q, J in t1_inst[:6]:
        p = len(Sigma)
        G = rng.standard_normal((p, p))
        G = G @ G.T
        base = sum(step_angles(sweep(Sigma, Q, J)[3], list(range(GRID))))
        tot = {eps: sum(step_angles(sweep(Sigma, Q, J + eps * G)[3], list(range(GRID))))
               for eps in (1e-6, 1e-4, 1e-2)}
        ratio = tot[1e-4] / tot[1e-6]
        ok = bool(base < 1e-10 and tot[1e-6] > 1e-8 and tot[1e-2] > 1e-3 and 30 <= ratio <= 300)
        ok_all &= ok
        rows.append({"p": p, "unperturbed_total_rad": base, "total_eps_1e-6": tot[1e-6],
                     "total_eps_1e-4": tot[1e-4], "total_eps_1e-2": tot[1e-2],
                     "ratio_1e-4_over_1e-6": ratio, "ok": ok})
    res["sections"]["t5_perturbed_turns"] = rows
    verdict["t5_perturbed_turns"] = bool(ok_all and len(rows) == 6)

    res["verdict"] = verdict
    res["RLD1T20_supported"] = all(verdict.values())
    res["seconds"] = round(time.time() - t0, 1)
    for k, v in verdict.items():
        print(f"{k}: {'PASS' if v else 'FAIL'}")
    print("===RLD1T20-JSON===")
    print(json.dumps(res, indent=1, default=float))
    print("===END===")
    return 0 if res["RLD1T20_supported"] else 1


if __name__ == "__main__":
    sys.exit(main())
