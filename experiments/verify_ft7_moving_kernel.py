"""C3 net for the T1 addendum on consumers whose read kernel moves (FRONTIER FT.7).

Claims checked (paper/t1-moving-kernel/t1-moving-kernel.tex):
  Theorem A  For a consumer map g with bounded derivatives and Q = E P_C(T) positive definite,
             every fixed-covariance Gaussian test channel T = That + Z, Z ~ N(0, Delta)
             independent of That, with small Delta has tr(Delta) <= 2 E loss / lambda_min(Q);
             so its rate is at least (p/2) ln(1/D) - c at consumer loss D.
  Prop. B    R_C(D) = R_U(D) for U = g(T) when g has a section on a closed convex image, so
             R_C(D) = (r/2) ln(1/D) + O(1) for an r-dimensional output.
  Cor. C     The fixed-weight excess R_fix(D) - R_C(D) grows like ((rank Q - r)/2) ln(1/D);
             for a fixed kernel (rank Q = r) it stays bounded.

Instances (source N(0, I_p)):
  I1  p = 2, g(x) = sqrt(1 + |x|^2)                         r = 1, rank Q = 2 (moving)
  I2  p = 3, g(x) = sqrt(1 + |x|^2)                         r = 1, rank Q = 3 (moving)
  I3  p = 3, g(x) = (sqrt(1 + x1^2 + x2^2), x3)             r = 2, rank Q = 3 (moving)
  I4  p = 2, g(x) = x1 + 0.3 sin(x1)                        r = 1, rank Q = 1 (control: fixed)
  I5  p = 2, g(x) = x1 + sin(x2)                            r = 1, rank Q = 2 (moving)
      I5 is the theorem-faithful instance (the author's, 2026-11-21): three bounded
      derivatives, det Q = (1/2)(1 - 1/e)^2, section s(u) = (u, 0), image R. Its R_fix is
      computed over the family Delta = t Q^{-1} (first-order optimal), so it is an upper
      bound on the least fixed-weight rate; Theorem A (c1) is the matching lower bound.

Checks:
  c1  Theorem A's inequality tr(Delta) <= 2 L(Delta) / lambda_min(Q) on random small Delta
      (I1-I3).
  c2  The slope of the fixed-weight rate R_fix(D) in ln(1/D) over D in [1e-5, 1e-2] is
      rank(Q)/2 (within 0.03), for all four instances; equivalently the excess over R_C has
      slope (rank Q - r)/2: 1/2, 1, 1/2 for I1-I3, 1/2 for I5, and 0 for the control I4.
  c3  The section code: g(s(proj(u))) = proj(u) on the image, and its consumer loss equals the
      projected error, never above the unprojected error (I1-I4).
  c4  The excess bracket [R_fix - R_U upper, R_fix - R_U lower] at D = 1e-5, reported, with
      R_U bracketed by the Shannon lower bound and the Gaussian upper bound (always passes if
      finite; it carries the numbers the note quotes).

Fire test: `--fire` runs four mutants (Theorem A's factor 2 -> 0.5; slopes (rank Q - r)/2
halved; the control predicted to grow at slope 1/2; the moving kernels predicted bounded) and
exits 0 only if every mutant fails its check.

Output: results/FT7-moving-kernel-net.json (verdict, FT7NET_supported). Seed 20261131.
"""
import json
import math
import sys
import time

import numpy as np
from scipy import integrate, optimize, special

SEED = 20261131
N_MC = 1_000_000
DS = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5]
SLOPE_TOL = 0.03


# ---------- the consumers ----------
def g_rad(x):
    return np.sqrt(1.0 + np.sum(x * x, axis=-1))


def diff_rad(xh, z):
    """g(xh + z) - g(xh) for g = sqrt(1 + |x|^2), without cancellation."""
    a = 2.0 * np.sum(xh * z, axis=-1) + np.sum(z * z, axis=-1)
    return a / (g_rad(xh + z) + g_rad(xh))


def loss_I1I2(xh, z):
    return diff_rad(xh, z) ** 2


def loss_I3(xh, z):
    return diff_rad(xh[:, :2], z[:, :2]) ** 2 + z[:, 2] ** 2


def f4(t):
    return t + 0.3 * np.sin(t)


def loss_I4(xh, z):
    return (f4(xh[:, 0] + z[:, 0]) - f4(xh[:, 0])) ** 2


def loss_I5(xh, z):
    return (z[:, 0] + np.sin(xh[:, 1] + z[:, 1]) - np.sin(xh[:, 1])) ** 2


def jac_rows(name, x):
    """Rows of J_g(x) (shape n x r x p)."""
    if name in ("I1", "I2"):
        return (x / g_rad(x)[:, None])[:, None, :]
    if name == "I3":
        n = x.shape[0]
        j = np.zeros((n, 2, 3))
        j[:, 0, :2] = x[:, :2] / g_rad(x[:, :2])[:, None]
        j[:, 1, 2] = 1.0
        return j
    if name == "I4":
        n = x.shape[0]
        j = np.zeros((n, 1, 2))
        j[:, 0, 0] = 1.0 + 0.3 * np.cos(x[:, 0])
        return j
    if name == "I5":
        n = x.shape[0]
        j = np.zeros((n, 1, 2))
        j[:, 0, 0] = 1.0
        j[:, 0, 1] = np.cos(x[:, 1])
        return j
    raise ValueError(name)


INST = {
    "I1": {"p": 2, "r": 1, "loss": loss_I1I2, "moving": True},
    "I2": {"p": 3, "r": 1, "loss": loss_I1I2, "moving": True},
    "I3": {"p": 3, "r": 2, "loss": loss_I3, "moving": True},
    "I4": {"p": 2, "r": 1, "loss": loss_I4, "moving": False},
    "I5": {"p": 2, "r": 1, "loss": loss_I5, "moving": True},
}
Q5 = np.array([[1.0, math.exp(-0.5)], [math.exp(-0.5), 0.5 * (1.0 + math.exp(-2.0))]])


# ---------- U = g(T): differential entropy and covariance (nats) ----------
def h_chi2(k):
    return k / 2.0 + math.log(2.0 * math.gamma(k / 2.0)) + (1.0 - k / 2.0) * special.digamma(k / 2.0)


def radial_u_stats(k):
    """U = sqrt(1 + V), V ~ chi^2_k: f_U(u) = 2u f_V(u^2 - 1), so h(U) = h(V) - E ln(2U); and Var U."""
    dens = lambda v: v ** (k / 2.0 - 1.0) * math.exp(-v / 2.0) / (2.0 ** (k / 2.0) * math.gamma(k / 2.0))
    e_ln2u = integrate.quad(lambda v: math.log(2.0 * math.sqrt(1.0 + v)) * dens(v), 0, np.inf, limit=200)[0]
    m1 = integrate.quad(lambda v: math.sqrt(1.0 + v) * dens(v), 0, np.inf, limit=200)[0]
    m2 = 1.0 + k
    return h_chi2(k) - e_ln2u, m2 - m1 * m1


def u_stats(name):
    h_gauss = 0.5 * math.log(2.0 * math.pi * math.e)
    if name == "I1":
        h, v = radial_u_stats(2)
        return h, [v]
    if name == "I2":
        h, v = radial_u_stats(3)
        return h, [v]
    if name == "I3":
        h, v = radial_u_stats(2)
        return h + h_gauss, [v, 1.0]
    if name == "I4":
        phi = lambda t: math.exp(-t * t / 2.0) / math.sqrt(2.0 * math.pi)
        e_lnf = integrate.quad(lambda t: math.log(1.0 + 0.3 * math.cos(t)) * phi(t), -12, 12, limit=200)[0]
        m2 = integrate.quad(lambda t: (t + 0.3 * math.sin(t)) ** 2 * phi(t), -12, 12, limit=200)[0]
        return h_gauss + e_lnf, [m2]  # E U = 0 by symmetry
    if name == "I5":
        # U = X1 + sin X2: density f(u) = E phi(u - sin X2), by quadrature
        phi = lambda t: math.exp(-t * t / 2.0) / math.sqrt(2.0 * math.pi)
        xs = np.linspace(-9.0, 9.0, 3601)
        wx = np.exp(-xs * xs / 2.0) / math.sqrt(2.0 * math.pi) * (xs[1] - xs[0])
        us = np.linspace(-10.0, 10.0, 4001)
        f = np.array([np.sum(wx * np.exp(-(u - np.sin(xs)) ** 2 / 2.0)) / math.sqrt(2.0 * math.pi) for u in us])
        du = us[1] - us[0]
        h = float(-np.sum(f * np.log(np.maximum(f, 1e-300))) * du)
        return h, [1.0 + 0.5 * (1.0 - math.exp(-2.0))]
    raise ValueError(name)


def r_u_bracket(name, D):
    """SLB <= R_U(D) <= Gaussian upper bound, for D <= k * min variance (nats)."""
    h, var = u_stats(name)
    k = len(var)
    slb = h - 0.5 * k * math.log(2.0 * math.pi * math.e * D / k)
    gub = 0.5 * sum(math.log(v * k / D) for v in var)
    return max(slb, 0.0), gub


# ---------- the fixed-weight rate R_fix(D), by common random numbers ----------
class Fixed:
    def __init__(self, name, rng):
        self.name, self.p = name, INST[name]["p"]
        self.w1 = rng.standard_normal((N_MC, self.p))
        self.w2 = rng.standard_normal((N_MC, self.p))
        self.loss = INST[name]["loss"]

    def L(self, d):
        """Consumer loss of the backward channel with Delta = diag(d), Sigma = I."""
        d = np.asarray(d, dtype=float)
        xh = self.w1 * np.sqrt(1.0 - d)
        z = self.w2 * np.sqrt(d)
        return float(np.mean(self.loss(xh, z)))

    def rate_fix(self, D):
        """Least rate (1/2) sum ln(1/d_i) over the family that is optimal by symmetry:
        I1, I2 isotropic; I3 diag(a, a, b) with b = D - L_a(a); I4 diag(d, 1)."""
        nm = self.name
        if nm in ("I1", "I2"):
            d = optimize.brentq(lambda t: self.L([t] * self.p) - D, D / 20, min(0.99, 20 * D), xtol=1e-14 * D)
            return 0.5 * self.p * math.log(1.0 / d), [d] * self.p
        if nm == "I4":
            d = optimize.brentq(lambda t: self.L([t, 1.0 - 1e-12]) - D, D / 20, min(0.99, 20 * D), xtol=1e-14 * D)
            return 0.5 * math.log(1.0 / d), [d, 1.0]
        if nm == "I5":
            qi = np.linalg.inv(Q5)

            def lt(t):
                delta = t * qi
                ch = np.linalg.cholesky(np.eye(2) - delta)
                cz = np.linalg.cholesky(delta)
                return float(np.mean(self.loss(self.w1 @ ch.T, self.w2 @ cz.T)))
            t = optimize.brentq(lambda t: lt(t) - D, D / 40, min(0.05, 20 * D), xtol=1e-14 * D)
            return 0.5 * math.log(np.linalg.det(Q5) / (t * t)), (t * qi).tolist()
        if nm == "I3":
            la = lambda a: self.L([a, a, 1e-300]) if a > 0 else 0.0

            def neg(lna):
                a = math.exp(lna)
                b = D - la(a)
                if b <= 0:
                    return 1e9
                return -(math.log(a) + 0.5 * math.log(b))
            res = optimize.minimize_scalar(neg, bounds=(math.log(D / 50), math.log(min(0.99, 2 * D))),
                                           method="bounded", options={"xatol": 1e-6})
            a = math.exp(res.x)
            b = D - la(a)
            return 0.5 * (2 * math.log(1.0 / a) + math.log(1.0 / b)), [a, a, b]
        raise ValueError(nm)


def lambda_min_Q(name, rng):
    x = rng.standard_normal((N_MC, INST[name]["p"]))
    j = jac_rows(name, x)
    q = np.einsum("nki,nkj->ij", j, j) / x.shape[0]
    return float(np.linalg.eigvalsh(q)[0]), q


# ---------- c1: Theorem A's inequality on random small Delta ----------
def check_c1(name, lam, rng, factor=2.0, n_delta=60, n_mc=400_000):
    p = INST[name]["p"]
    loss = INST[name]["loss"]
    worst = -np.inf
    ok = True
    for _ in range(n_delta):
        a = rng.standard_normal((p, p))
        delta = a @ a.T
        delta *= rng.uniform(1e-4, 0.03) / np.trace(delta)  # tr Delta in [1e-4, 0.03]
        # backward channel with Sigma = I: That ~ N(0, I - Delta), Z ~ N(0, Delta)
        ch = np.linalg.cholesky(np.eye(p) - delta)
        cz = np.linalg.cholesky(delta + 1e-18 * np.eye(p))
        w1 = rng.standard_normal((n_mc, p))
        w2 = rng.standard_normal((n_mc, p))
        xh, z = w1 @ ch.T, w2 @ cz.T
        L = float(np.mean(loss(xh, z)))
        ratio = np.trace(delta) / (factor * L / lam)  # must be <= 1
        worst = max(worst, ratio)
        ok = ok and ratio <= 1.0
    return ok, float(worst)


# ---------- c3: the section code ----------
def check_c3(name, rng, n=200_000):
    p = INST[name]["p"]
    x = rng.standard_normal((n, p))
    if name in ("I1", "I2"):
        u = g_rad(x)
        uh = u + 0.3 * rng.standard_normal(n)
        up = np.maximum(uh, 1.0)  # projection onto the image [1, inf)
        s = np.zeros((n, p))
        s[:, 0] = np.sqrt(up * up - 1.0)
        gu = g_rad(s)
        lc, lu = (gu - u) ** 2, (uh - u) ** 2
        exact = np.max(np.abs(gu - up))
    elif name == "I3":
        u1 = g_rad(x[:, :2])
        uh1 = u1 + 0.3 * rng.standard_normal(n)
        uh3 = x[:, 2] + 0.3 * rng.standard_normal(n)
        up1 = np.maximum(uh1, 1.0)
        s = np.zeros((n, 3))
        s[:, 0] = np.sqrt(up1 * up1 - 1.0)
        s[:, 2] = uh3
        g1, g3 = g_rad(s[:, :2]), s[:, 2]
        lc = (g1 - u1) ** 2 + (g3 - x[:, 2]) ** 2
        lu = (uh1 - u1) ** 2 + (uh3 - x[:, 2]) ** 2
        exact = max(np.max(np.abs(g1 - up1)), np.max(np.abs(g3 - uh3)))
    elif name == "I5":
        u = x[:, 0] + np.sin(x[:, 1])
        uh = u + 0.3 * rng.standard_normal(n)
        gu = uh + np.sin(np.zeros(n))  # g(s(uh)) with s(u) = (u, 0)
        lc, lu = (gu - u) ** 2, (uh - u) ** 2
        exact = np.max(np.abs(gu - uh))
    elif name == "I4":
        u = f4(x[:, 0])
        uh = u + 0.3 * rng.standard_normal(n)
        # the image is R; the section inverts f by bisection (f' >= 0.7)
        lo, hi = uh - 0.4, uh + 0.4  # |f(t) - t| <= 0.3
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            big = f4(mid) > uh
            hi = np.where(big, mid, hi)
            lo = np.where(big, lo, mid)
        s1 = 0.5 * (lo + hi)
        gu = f4(s1)
        lc, lu = (gu - u) ** 2, (uh - u) ** 2
        exact = np.max(np.abs(gu - uh))
    ok = bool(exact < 1e-9 and np.all(lc <= lu + 1e-12))
    return ok, float(exact), float(np.mean(lc)), float(np.mean(lu))


def slope(ds, rates):
    xs = np.log(1.0 / np.asarray(ds))
    return float(np.polyfit(xs, np.asarray(rates), 1)[0])


def run(fire=False):
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    out = {"net": "FT.7 moving-kernel net", "seed": SEED, "n_mc": N_MC, "D_grid": DS,
           "instances": {}}
    verdict = {}
    for name in ["I1", "I2", "I3", "I4", "I5"]:
        info = INST[name]
        lam, q = lambda_min_Q(name, rng)
        rank_q = int(np.sum(np.linalg.eigvalsh(q) > 1e-6))
        fx = Fixed(name, rng)
        rows = []
        for D in DS:
            rf, dvec = fx.rate_fix(D)
            lo, hi = r_u_bracket(name, D)
            rows.append({"D": D, "R_fix": rf, "Delta_diag": dvec, "R_U_lower": lo, "R_U_upper": hi,
                         "excess_lower": rf - hi, "excess_upper": rf - lo})
        s_fix = slope(DS, [r["R_fix"] for r in rows])
        pred = rank_q / 2.0
        inst = {"p": info["p"], "r": info["r"], "rank_Q": rank_q, "lambda_min_Q": lam,
                "Q": q.tolist(), "rows": rows, "slope_R_fix": s_fix, "predicted_slope_R_fix": pred,
                "slope_excess": s_fix - info["r"] / 2.0,
                "predicted_slope_excess": (rank_q - info["r"]) / 2.0}
        verdict[f"c2_{name}_slope"] = abs(s_fix - pred) <= SLOPE_TOL
        if info["moving"]:
            ok1, worst = check_c1(name, lam, rng)
            inst["c1_worst_ratio"] = worst
            verdict[f"c1_{name}_thmA"] = ok1
        ok3, exact, lc, lu = check_c3(name, rng)
        inst["c3"] = {"section_max_error": exact, "loss_section_code": lc, "loss_unprojected": lu}
        verdict[f"c3_{name}_section"] = ok3
        last = rows[-1]
        inst["c4_excess_bracket_at_1e-5"] = [last["excess_lower"], last["excess_upper"]]
        verdict[f"c4_{name}_finite"] = bool(np.isfinite(last["excess_lower"]) and np.isfinite(last["excess_upper"]))
        out["instances"][name] = inst
        print(f"{name}: rank Q {rank_q}, lam_min {lam:.4f}, slope R_fix {s_fix:.4f} (pred {pred}), "
              f"excess at 1e-5 in [{last['excess_lower']:.4f}, {last['excess_upper']:.4f}]", flush=True)
    verdict = {k: bool(v) for k, v in verdict.items()}
    out["verdict"] = verdict
    out["FT7NET_supported"] = all(verdict.values())
    out["seconds"] = round(time.time() - t0, 1)
    if fire:
        return out
    path = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "results/FT7-moving-kernel-net.json"
    json.dump(out, open(path, "w"), indent=1)
    print("verdict:", {k: bool(v) for k, v in verdict.items()})
    print("FT7NET_supported:", out["FT7NET_supported"])
    return out


def fire():
    """Each mutant must fail its check."""
    out = run(fire=True)
    rng = np.random.default_rng(SEED + 1)
    caught = {}
    # m1: Theorem A with factor 0.5 instead of 2
    caught["m1_thmA_factor_half"] = not all(
        check_c1(nm, out["instances"][nm]["lambda_min_Q"], rng, factor=0.5)[0] for nm in ["I1", "I2", "I3", "I5"])
    # m2: excess slopes halved, (rank Q - r)/4
    caught["m2_slopes_halved"] = any(
        abs(out["instances"][nm]["slope_excess"] - (out["instances"][nm]["rank_Q"] - INST[nm]["r"]) / 4.0) > SLOPE_TOL
        for nm in ["I1", "I2", "I3", "I5"])
    # m3: the fixed-kernel control predicted to grow at slope 1/2
    caught["m3_control_grows"] = abs(out["instances"]["I4"]["slope_excess"] - 0.5) > SLOPE_TOL
    # m4: the moving kernels predicted bounded (rank Q = r)
    caught["m4_moving_bounded"] = all(abs(out["instances"][nm]["slope_excess"]) > SLOPE_TOL for nm in ["I1", "I2", "I3", "I5"])
    print("fire:", caught)
    return all(caught.values())


if __name__ == "__main__":
    if "--fire" in sys.argv:
        sys.exit(0 if fire() else 1)
    o = run()
    sys.exit(0 if o["FT7NET_supported"] else 1)
