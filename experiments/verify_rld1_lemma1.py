#!/usr/bin/env python
"""C3 net for RLD-I Lemma 1 (lem:gauss, the Gaussian exhaustion lemma) and the identity of
Proposition 2 (prop:posterior), paper/tit-rate-leakage: the ingredients of Theorem 3's
converse, which had no numerical net (R-IND-5 pass VI-27, 2026-11-20).

Lemma 1: for a description Yh with finite second moments, regression residual N' = Yh - AT,
Cov(N', S) = 0 and Cov N' > 0,
    I(T;Yh)   >= (1/2) log(det Sigma_T / det Se0),
    I(T;Yh|S) >= (1/2) log(det Kc / det Se),
with Se0, Se the error covariances of the best affine estimates of T from Yh and from
(Yh, S), and Kc = (Sigma_T^-1 + J)^-1. Proposition 2's proof also uses
Se^-1 = Se0^-1 + J, which holds for such a description because its second moments with
(T, S) are those of a Gaussian channel AT + N.

The net uses deliberately non-Gaussian descriptions: T ~ N(0, s2) scalar, S = H T + U in
R^2 with U ~ N(0, SU), and Yh = the index of the bin of X = T + Z, Z ~ N(0, tau^2), among
k bins with random thresholds. Then every quantity is exact up to 1-D quadrature:
    p(j | t) = Phi((c_j - t)/tau) - Phi((c_{j-1} - t)/tau),
    p(j | S) depends on S only through m = E[T|S] ~ N(0, s2 - Kc), and
    p(j | m) = Phi((c_j - m)/r) - Phi((c_{j-1} - m)/r), r^2 = tau^2 + Kc,
    I(T;Yh) = H(Yh) - E H(Yh|T), I(T;Yh|S) = E H(Yh|S) - E H(Yh|T) (Markov Yh - T - S).
The affine estimates use the k bin indicators (so Se0 is the MMSE given Yh), with exact
second moments E[T 1_j] by quadrature and E[1_j S] = H E[T 1_j].

Checks (seed 20261121; revised 2026-11-20 after the R-IND-5 pass VI-29 found the earlier
equality check tautological and the hypothesis Cov(N', S) = 0 never exercised):
  l1_bounds: over 60 random instances (k in {2, 3, 5, 8}, tau in [0.05, 1.5] sd), both
     inequalities hold with slack >= -1e-9 nats.
  l2_identity: Se^-1 = Se0^-1 + J to relative 1e-9 on those instances.
  l2b_hypothesis_power: on 20 descriptions that VIOLATE Cov(N', S) = 0 (the bin of
     T + gamma U_1 + Z, so the description sees the holder's noise), the identity must FAIL,
     by a relative error above 1e-3 on at least 15 of them. (The two bounds themselves do not
     need the hypothesis: the proof's divergence and Jensen steps do not use it, and VI-29
     found they still hold there. The identity, the determinant identity and the equality
     clause do use it, as the paper's appendix says; l2b and l5b test the first two.)
  l3_quadrature: doubling the grid moves both informations, Se0 and Se by < 1e-9.
  l4_power: false variants violated on at least one instance, so the net can fail:
     (a) "I(T;Yh|S) >= (1/2) log(Sigma_T / Se)", wrong reference (gross: false even for
     Gaussian descriptions); (b) "I(T;Yh) <= (1/2) log(Sigma_T / Se0)" and
     (c) "I(T;Yh|S) <= (1/2) log(Kc / Se)", the reverse inequalities, which are the variants
     that show power against non-Gaussian descriptions.
  l5_gaussian_replacement: for each instance, its Gaussian replacement A T + N
     (A = E[T 1]/s2 over the k-1 bin indicators, Sigma_N = Cov(1) - s2 A A', asserted
     positive definite) meets both bounds with equality, computed from determinants
     (relative 1e-9), and satisfies the paper's identity
     Se = Kc det(Sigma_N) / det(A Kc A' + Sigma_N) against the description's own Se. Given
     l1-l2 this mostly re-checks the algebra by another code path, so it has two power arms:
     l5a, a wrong replacement (A scaled by 1.01) must FAIL it (relative error > 1e-6) on every
     instance; l5b, on the hypothesis-violating family of l2b, the determinant identity
     must FAIL (relative error > 1e-3) on at least 15 of 20.

Scope (stated, not tested): T is scalar (p = 1), so the scalar Jensen step is exercised but
the matrix log-det Jensen step and the matrix Schur step are not; the descriptions are noisy
scalar quantizers; the holder has dimension 2. Proposition 2's other steps (the singular
Cov N' reduction, the LMMSE distortion bound, the converse construction) are not netted.

Provenance: the first version ran while the file was untracked; this version's criteria were
written before its first run, and the file is committed before CI runs it.

Usage: python experiments/verify_rld1_lemma1.py   (CPU, seconds)
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np
from scipy.special import ndtr

SEED = 20261121


def grid(n, sd):
    """Uniform grid on [-12 sd, 12 sd] with Gaussian N(0, sd^2) weights summing to 1."""
    x = np.linspace(-12 * sd, 12 * sd, n)
    w = np.exp(-0.5 * (x / sd) ** 2)
    return x, w / w.sum()


def entropy_rows(P):
    P = np.clip(P, 1e-300, 1.0)
    return -(P * np.log(P)).sum(axis=-1)


def bin_probs(x, c, scale):
    edges = np.concatenate([[-np.inf], c, [np.inf]])
    F = ndtr((edges[None, :] - x[:, None]) / scale)
    return np.diff(F, axis=1)


def instance_values(s2, H, SU, c, tau, n):
    J = float(H @ np.linalg.solve(SU, H))
    Kc = 1.0 / (1.0 / s2 + J)
    t, wt = grid(n, np.sqrt(s2))
    Pt = bin_probs(t, c, tau)                      # p(j | t)
    pj = wt @ Pt                                    # p(j)
    I0 = entropy_rows(pj[None, :])[0] - wt @ entropy_rows(Pt)
    m, wm = grid(n, np.sqrt(s2 - Kc))
    Pm = bin_probs(m, c, np.sqrt(tau ** 2 + Kc))   # p(j | S) through m = E[T|S]
    IS = wm @ entropy_rows(Pm) - wt @ entropy_rows(Pt)
    ET1 = (wt * t) @ Pt                             # E[T 1_j]
    Se0 = s2 - np.sum(ET1 ** 2 / pj)                # MMSE given Yh = best affine via indicators
    # Best affine estimate of T from (indicators 1..k-1, S): exact second moments.
    k = len(pj)
    cov_ind = np.diag(pj[:-1]) - np.outer(pj[:-1], pj[:-1])
    cov_ind_S = np.outer(ET1[:-1], H)               # Cov(1_j, S) = H E[T 1_j] (centred: E[T] = 0)
    cov_S = s2 * np.outer(H, H) + SU
    C = np.block([[cov_ind, cov_ind_S], [cov_ind_S.T, cov_S]])
    cT = np.concatenate([ET1[:-1], s2 * H])
    Se = s2 - cT @ np.linalg.solve(C, cT)
    # The Gaussian replacement A T + N over the k-1 indicators (same second moments with T, S).
    A = ET1[:-1] / s2
    SN = cov_ind - s2 * np.outer(A, A)
    sign, ldSN = np.linalg.slogdet(SN)
    IG0 = 0.5 * (np.linalg.slogdet(s2 * np.outer(A, A) + SN)[1] - ldSN)
    IGS = 0.5 * (np.linalg.slogdet(Kc * np.outer(A, A) + SN)[1] - ldSN)
    Se_formula = Kc * np.exp(ldSN - np.linalg.slogdet(Kc * np.outer(A, A) + SN)[1])
    # Power arm l5a: a wrong replacement (A scaled by 1.01) must not reproduce the bounds.
    A2 = 1.01 * A
    SN2 = cov_ind - s2 * np.outer(A2, A2)
    ld2 = np.linalg.slogdet(SN2)[1]
    wrong = 0.5 * (np.linalg.slogdet(s2 * np.outer(A2, A2) + SN2)[1] - ld2)
    return dict(J=J, Kc=Kc, I0=float(I0), IS=float(IS), Se0=float(Se0), Se=float(Se), k=k,
                IG0=float(IG0), IGS=float(IGS), Se_formula=float(Se_formula),
                SN_posdef=bool(sign > 0 and np.linalg.eigvalsh(SN).min() > 0),
                SN_min_eig=float(np.linalg.eigvalsh(SN).min()), IG0_wrong=float(wrong))


def violating_identity_error(s2, H, SU, c, tau, gamma):
    """Second moments of the bin of X = T + gamma U_1 + Z, which sees the holder's noise, so
    Cov(N', S) != 0. Returns the relative error of Se^-1 = Se0^-1 + J (exact, closed form)."""
    J = float(H @ np.linalg.solve(SU, H))
    vx = s2 + gamma ** 2 * SU[0, 0] + tau ** 2
    sx = np.sqrt(vx)
    edges = np.concatenate([[-np.inf], c, [np.inf]])
    pj = np.diff(ndtr(edges / sx))
    dens = np.where(np.isfinite(edges), np.exp(-0.5 * (edges / sx) ** 2) / (sx * np.sqrt(2 * np.pi)), 0.0)
    EX1 = vx * (dens[:-1] - dens[1:])              # E[X 1_j] for a centred Gaussian X
    ET1 = s2 / vx * EX1
    EU1 = np.outer(gamma * SU[:, 0] / vx, EX1)     # E[U 1_j], shape (2, k)
    Se0 = s2 - np.sum(ET1 ** 2 / pj)
    cov_ind = np.diag(pj[:-1]) - np.outer(pj[:-1], pj[:-1])
    cov_ind_S = np.outer(ET1[:-1], H) + EU1[:, :-1].T
    C = np.block([[cov_ind, cov_ind_S], [cov_ind_S.T, s2 * np.outer(H, H) + SU]])
    cT = np.concatenate([ET1[:-1], s2 * H])
    Se = s2 - cT @ np.linalg.solve(C, cT)
    Kc = 1.0 / (1.0 / s2 + J)
    A = ET1[:-1] / s2
    SN = cov_ind - s2 * np.outer(A, A)
    Se_formula = Kc * np.exp(np.linalg.slogdet(SN)[1] - np.linalg.slogdet(Kc * np.outer(A, A) + SN)[1])
    return abs(1 / Se - (1 / Se0 + J)) / (1 / Se), abs(Se_formula - Se) / Se


def main():
    rng = np.random.default_rng(SEED)
    t0 = time.time()
    rows, slack_min, ident_max, quad_max = [], np.inf, 0.0, 0.0
    viol_a = viol_b = viol_c = 0
    repl_max = 0.0
    posdef_all, sn_min, wrong_min = True, np.inf, np.inf
    for i in range(60):
        s2 = float(rng.uniform(0.5, 3.0))
        H = rng.standard_normal(2)
        A = rng.standard_normal((2, 2))
        SU = A @ A.T + 0.2 * np.eye(2)
        k = (2, 3, 5, 8)[i % 4]
        tau = float(rng.uniform(0.05, 1.5)) * np.sqrt(s2)
        c = np.sort(rng.standard_normal(k - 1) * np.sqrt(s2 + tau ** 2))
        v = instance_values(s2, H, SU, c, tau, 6001)
        v2 = instance_values(s2, H, SU, c, tau, 12001)
        quad_max = max(quad_max, *(abs(v[x] - v2[x]) for x in ("I0", "IS", "Se0", "Se")))
        b0 = 0.5 * np.log(s2 / v["Se0"])
        bS = 0.5 * np.log(v["Kc"] / v["Se"])
        sl = min(v["I0"] - b0, v["IS"] - bS)
        slack_min = min(slack_min, sl)
        ident_max = max(ident_max, abs(1 / v["Se"] - (1 / v["Se0"] + v["J"])) / (1 / v["Se"]))
        viol_a += v["IS"] < 0.5 * np.log(s2 / v["Se"]) - 1e-9
        viol_b += v["I0"] > b0 + 1e-9
        viol_c += v["IS"] > bS + 1e-9
        repl_max = max(repl_max, abs(v["IG0"] - b0) / max(b0, 1e-300), abs(v["IGS"] - bS) / max(bS, 1e-300),
                       abs(v["Se_formula"] - v["Se"]) / v["Se"])
        posdef_all = posdef_all and v["SN_posdef"]
        sn_min = min(sn_min, v["SN_min_eig"])
        wrong_min = min(wrong_min, abs(v["IG0_wrong"] - b0) / max(b0, 1e-300))
        rows.append({"k": k, "tau_over_sd": tau / np.sqrt(s2), "I_TY": v["I0"], "bound_TY": b0,
                     "I_TY_given_S": v["IS"], "bound_TY_given_S": bS, "slack": sl})
    # The hypothesis Cov(N', S) = 0 matters for the identity: break it and the identity must fail.
    viol_errs, viol_det = [], []
    for i in range(20):
        s2 = float(rng.uniform(0.5, 3.0))
        H = rng.standard_normal(2)
        A_ = rng.standard_normal((2, 2))
        SU = A_ @ A_.T + 0.2 * np.eye(2)
        k = (2, 3, 5, 8)[i % 4]
        tau = float(rng.uniform(0.05, 1.5)) * np.sqrt(s2)
        gamma = float(rng.uniform(0.5, 2.0))
        c = np.sort(rng.standard_normal(k - 1) * np.sqrt(s2 + gamma ** 2 * SU[0, 0] + tau ** 2))
        e_id, e_det = violating_identity_error(s2, H, SU, c, tau, gamma)
        viol_errs.append(float(e_id))
        viol_det.append(float(e_det))
    verdict = {
        "l1_bounds": bool(slack_min >= -1e-9),
        "l2_identity": bool(ident_max < 1e-9),
        "l2b_hypothesis_power": bool(sum(e > 1e-3 for e in viol_errs) >= 15),
        "l3_quadrature": bool(quad_max < 1e-9),
        "l4_power": bool(viol_a >= 1 and viol_b >= 1 and viol_c >= 1),
        "l5_gaussian_replacement": bool(repl_max < 1e-9 and posdef_all),
        "l5a_wrong_replacement_fails": bool(wrong_min > 1e-6),
        "l5b_hypothesis_power": bool(sum(e > 1e-3 for e in viol_det) >= 15),
    }
    res = {"seed": SEED, "lemma": "RLD-I Lemma 1 (lem:gauss) and Proposition 2's identity",
           "instances": rows, "min_slack_nats": float(slack_min), "identity_max_rel": float(ident_max),
           "hypothesis_violation_identity_errors": viol_errs,
           "quadrature_max_change": float(quad_max), "variant_a_violations": int(viol_a),
           "variant_b_violations": int(viol_b), "variant_c_violations": int(viol_c),
           "replacement_max_rel": float(repl_max), "SN_min_eig": float(sn_min),
           "wrong_replacement_min_rel_error": float(wrong_min),
           "hypothesis_violation_determinant_errors": viol_det,
           "verdict": verdict, "RLD1L1_supported": all(verdict.values()),
           "seconds": round(time.time() - t0, 1)}
    for k, val in verdict.items():
        print(f"{k}: {'PASS' if val else 'FAIL'}")
    print("===RLD1L1-JSON===")
    print(json.dumps(res, indent=1, default=float))
    print("===END===")
    return 0 if res["RLD1L1_supported"] else 1


if __name__ == "__main__":
    sys.exit(main())
