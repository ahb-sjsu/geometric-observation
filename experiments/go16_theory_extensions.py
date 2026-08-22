"""GO-16 theory extensions -- exact binary identities (S3, hard gates),
the commuting-alignment scan (S1, exploratory measurement), and the
fixed-instrument commitment-gap probe (S2, exploratory measurement).

S3 nets the algebra that upgrades the discrete twin to theorem grade
(statement v0.5, Theorem 4):
  (i)  EVar(q0,q1) = 1/4 - (q1-q0)^2 / (4(q0+q1)(2-q0-q1))  exactly,
       hence rho = (q1-q0)^2 / ((q0+q1)(2-q0-q1))  -- closed form; the
       symmetric-channel frontier is then a two-line THEOREM:
       v^2 = rho * u(2-u) <= rho  (since u(2-u) <= 1), so
       err = (1-v)/2 >= (1-sqrt(rho))/2, equality iff q0+q1 = 1.
       (Supersedes the 091 SLSQP instrument validation.)
  (ii) the per-coordinate FOC completion of squares:
       s^2(1-x)/2 + c x^2 = s^2/2 - s^4/(16c) + c(x - s^2/(4c))^2,
       x = sqrt(rho), c = lam*theta*mu -- the fifth-class FOC algebra.
Mirrored in Lean: lean/ObservationTheory/AdversarialObserverDiscrete.lean.

S1 measures the V10 commuting-alignment hypothesis: contested
(fractional-revelation) mass vs commutator norm ||[Sigma_S, M]||_F
along random non-commuting perturbations of a commuting pair.

S2 probes the fixed-instrument Theta-mixture game at the exact m=2
instance (V* = 7/4): the encoder best-responds (full matrix policy) to
committed read mixtures; sanity gate inf_E <= V* (minimax direction);
the measured shortfall estimates the commitment gap.

Deterministic, seed 20260821 (dev, disclosed).  Exploratory except the
S3 identity gates; a governed seal for S3 may follow.
"""

import json
import numpy as np
from scipy.optimize import minimize

SEED = 20260821


def channel_stats(q0, q1):
    err = 0.5 * (q0 + (1.0 - q1))
    sa = q0 + q1
    sb = 2.0 - q0 - q1
    t1 = np.where(sa > 0, q0 * q1 / (2.0 * np.maximum(sa, 1e-300)), 0.0)
    t2 = np.where(sb > 0, (1 - q0) * (1 - q1) / (2.0 * np.maximum(sb, 1e-300)), 0.0)
    rho = 1.0 - 4.0 * (t1 + t2)
    return err, rho


# ---------------------------------------------------------------- S3
def s3():
    q = np.linspace(0.0025, 0.9975, 399)
    Q0, Q1 = np.meshgrid(q, q, indexing="ij")
    err, rho = channel_stats(Q0, Q1)
    u = Q0 + Q1
    v = Q1 - Q0
    ok_dom = (u > 1e-9) & (2 - u > 1e-9)
    rho_cf = v ** 2 / (u * (2 - u))
    evar_cf = 0.25 - v ** 2 / (4 * u * (2 - u))
    evar = (1 - rho) / 4.0
    e1 = float(np.max(np.abs((rho - rho_cf))[ok_dom]))
    e2 = float(np.max(np.abs(evar - evar_cf)[ok_dom]))
    # frontier bound and attainment
    bound_viol = float(np.max(((1 - np.sqrt(np.clip(rho, 0, None))) / 2 - err)[ok_dom]))
    eps = np.linspace(0, 0.5, 201)
    err_s, rho_s = channel_stats(eps, 1 - eps)
    attain = float(np.max(np.abs(err_s - (1 - np.sqrt(np.clip(rho_s, 0, None))) / 2)))
    # FOC completion of squares on random triples
    rng = np.random.default_rng(SEED)
    worst_foc = 0.0
    for _ in range(2000):
        s2v, c, x = rng.uniform(0.1, 5), rng.uniform(0.05, 5), rng.uniform(0, 1)
        lhs = s2v * (1 - x) / 2 + c * x ** 2
        rhs = s2v / 2 - s2v ** 2 / (16 * c) + c * (x - s2v / (4 * c)) ** 2
        worst_foc = max(worst_foc, abs(lhs - rhs))
    return {
        "rho_closed_form_err": e1,
        "evar_closed_form_err": e2,
        "frontier_bound_violation": bound_viol,
        "symmetric_attainment_err": attain,
        "foc_identity_worst": worst_foc,
        "pass": bool(e1 < 1e-12 and e2 < 1e-13 and bound_viol < 1e-12
                     and attain < 1e-12 and worst_foc < 1e-10),
    }


# ---------------------------------------------------------------- S1
def kyfan(A, k):
    w = np.sort(np.linalg.eigvalsh(A))[::-1]
    return float(np.sum(w[:k]))


def sdp_solve(SigS, Ms, lam, k, n, iters=15000):
    K = 0.5 * np.eye(n)
    K_avg = np.zeros((n, n)); wsum = 0.0
    for t in range(1, iters + 1):
        w, V = np.linalg.eigh(Ms @ K @ Ms)
        idx = np.argsort(w)[::-1][:k]
        W = V[:, idx] @ V[:, idx].T
        K = K - (0.5 / np.sqrt(t)) * (-SigS + lam * Ms @ W @ Ms)
        K = 0.5 * (K + K.T)
        wk, Vk = np.linalg.eigh(K)
        K = Vk @ np.diag(np.clip(wk, 0, 1)) @ Vk.T
        if t > iters // 2:
            K_avg += K; wsum += 1
    return K_avg / wsum


def s1():
    rng = np.random.default_rng(SEED + 1)
    n, lam, k = 4, 1.0, 2
    s2 = np.array([0.5, 3.0, 0.4, 2.0])
    mu = np.array([4.0, 2.5, 1.8, 1.0])
    Q, _ = np.linalg.qr(rng.standard_normal((n, n)))
    SigS = Q @ np.diag(s2) @ Q.T
    M0 = Q @ np.diag(mu) @ Q.T
    rows = []
    frac0 = None
    for eps in [0.0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6]:
        for rep in range(3 if eps > 0 else 1):
            R = rng.standard_normal((n, n))
            P = 0.5 * (R + R.T)
            P *= np.sqrt(n) / np.linalg.norm(P)
            M = M0 + eps * P
            wmin = np.min(np.linalg.eigvalsh(M))
            if wmin < 0.05:           # keep M comfortably PD
                M = M + (0.05 - wmin) * np.eye(n)
            comm = float(np.linalg.norm(SigS @ M - M @ SigS))
            Ms = np.linalg.cholesky(M) if False else None
            w, V = np.linalg.eigh(M)
            Msq = V @ np.diag(np.sqrt(w)) @ V.T
            K = sdp_solve(SigS, Msq, lam, k, n)
            kap = np.linalg.eigvalsh(K)
            frac = float(np.sum(np.minimum(kap, 1 - kap)))
            rows.append({"eps": eps, "rep": rep, "commutator_fro": comm,
                         "fractional_mass": frac})
            if eps == 0.0:
                frac0 = frac
    return {"rows": rows, "fractional_mass_at_commuting": frac0,
            "pass": bool(frac0 is not None and frac0 > 0.05)}


# ---------------------------------------------------------------- S2
def encoder_best_response(S, H, lam, atoms, weights, rng, restarts=6):
    """min over full (F, Sigma_w=LL') of ||F-S||^2 + tr(Sw)
       + lam * sum_j w_j * ||H F' u_j||^2 / (u_j' N u_j)."""
    m, n = S.shape
    tril = np.tril_indices(m)

    def unpack(z):
        F = z[: m * n].reshape(m, n)
        L = np.zeros((m, m))
        L[tril] = z[m * n:]
        return F, L @ L.T

    def obj(z):
        F, Sw = unpack(z)
        N = F @ F.T + Sw + 1e-12 * np.eye(m)
        leak = 0.0
        for u, w in zip(atoms, weights):
            leak += w * float(u @ F @ H.T @ H @ F.T @ u) / float(u @ N @ u)
        return float(np.sum((F - S) ** 2) + np.trace(Sw) + lam * leak)

    best = None
    for r in range(restarts):
        F0 = S + 0.25 * r * rng.standard_normal((m, n)) / max(1, r)
        z0 = np.concatenate([F0.ravel(), 0.15 * rng.standard_normal(len(tril[0]))])
        res = minimize(obj, z0, method="L-BFGS-B",
                       options=dict(maxiter=4000, maxfun=200000))
        if best is None or res.fun < best.fun:
            best = res
    return float(best.fun)


def s2():
    rng = np.random.default_rng(SEED + 2)
    # exact m=2 instance: V* = 7/4, saddle attention (1/4, 3/4)
    S = np.diag([1.0, np.sqrt(2.0)])
    H = np.diag([2.0, 1.0])
    lam, Vstar = 1.0, 1.75
    e1, e2 = np.eye(2)

    out = {}
    # (a) the natural axis mixture at the saddle weights
    J_axis = encoder_best_response(S, H, lam, [e1, e2], [0.25, 0.75], rng)
    out["axis_saddle_mixture_inf"] = J_axis
    # (b) best axis mixture over a weight grid
    best_w, best_val = None, -np.inf
    for w in np.linspace(0.02, 0.98, 25):
        val = encoder_best_response(S, H, lam, [e1, e2], [w, 1 - w], rng,
                                    restarts=4)
        if val > best_val:
            best_val, best_w = val, float(w)
    out["best_axis_mixture"] = {"w1": best_w, "inf": best_val}
    # (c) three-atom mixture on the circle, outer Nelder-Mead
    def outer_neg(p):
        angles = p[:3]
        wraw = np.exp(p[3:5]); w3 = np.append(wraw, 1.0); w3 /= w3.sum()
        atoms = [np.array([np.cos(a), np.sin(a)]) for a in angles]
        return -encoder_best_response(S, H, lam, atoms, w3, rng, restarts=3)
    res = minimize(outer_neg, np.array([0.0, np.pi / 2, np.pi / 4, 0.0, 0.5]),
                   method="Nelder-Mead",
                   options=dict(maxiter=80, xatol=1e-3, fatol=1e-5))
    out["three_atom_best_inf"] = float(-res.fun)
    sup_found = max(J_axis, best_val, float(-res.fun))
    out["V_star"] = Vstar
    out["V_Theta_lower_bound_found"] = sup_found
    out["gap_estimate_at_m2"] = float(Vstar - sup_found)
    # sanity (minimax direction): every inner inf must be <= V* + tol
    sane = (J_axis <= Vstar + 1e-4 and best_val <= Vstar + 1e-4
            and -res.fun <= Vstar + 1e-4)
    # (d) the 6-coordinate governed instance, axis mixture at theta*
    mu6 = np.array([4.0, 2.5, 1.8, 1.0, 0.55, 0.3])
    s26 = np.array([0.5, 3.0, 0.4, 2.0, 0.3, 0.25])
    S6 = np.diag(np.sqrt(s26))
    H6 = np.diag(np.sqrt(mu6))
    th6 = np.array([0.125, 1.0, 0.4 / 1.8, 2 - 1 - 0.125 - 0.4 / 1.8, 0.0, 0.0])
    atoms6 = [np.eye(6)[i] for i in range(6)]
    J6 = encoder_best_response(S6, H6, 1.0, atoms6, th6, rng, restarts=5)
    out["six_coord_axis_mixture_inf"] = J6
    out["six_coord_V_star"] = 4.052777777777778
    out["gap_estimate_at_6coord"] = float(4.052777777777778 - J6)
    sane = sane and (J6 <= 4.052777777777778 + 1e-3)
    out["pass"] = bool(sane)
    return out


def main():
    out = {"seed": SEED}
    out["S3_exact_identities"] = s3()
    out["S1_commuting_alignment_scan"] = s1()
    out["S2_fixed_instrument_gap"] = s2()
    gates = [out["S3_exact_identities"]["pass"],
             out["S1_commuting_alignment_scan"]["pass"],
             out["S2_fixed_instrument_gap"]["pass"]]
    out["ALL_PASS"] = bool(all(gates))
    out["gates_passed"] = f"{sum(gates)}/{len(gates)}"
    return out


if __name__ == "__main__":
    res = main()
    print("GO16_THEORY_EXT_BEGIN")
    print(json.dumps(res, indent=1))
    print("GO16_THEORY_EXT_END")
