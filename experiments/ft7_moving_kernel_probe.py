"""FT.7 probe (exploratory, disclosed): the price of a fixed weight for a consumer whose read
direction moves with the state.

Consumer C(x) = |x| on R^2, source X ~ N(0, I_2); p = 2, r = 1. P_C(x) = x x^T / |x|^2 has
rank 1 and its range rotates with x; Q = E P_C = I/2.

R_fix(D): least rate (nats) of a fixed-weight code, i.e. a Gaussian backward channel
X = Xhat + Z with Z ~ N(0, Delta) independent of Xhat ~ N(0, I - Delta), whose consumer loss
E(|Xhat + Z| - |Xhat|)^2 is at most D. Rate = (1/2) ln det(I Delta^{-1}).
R_C(D) = R_U(D) for U = |X| ~ Rayleigh(1) under squared error (data processing one way; the
decoder outputs (Uhat, 0) the other way). Bracketed: SLB h(U) - (1/2) ln(2 pi e D) <= R_U(D)
<= (1/2) ln(Var U / D) (the Gaussian upper bound).

Prediction (heuristic, FRONTIER FT.7): R_fix(D) - R_C(D) = ((p - r)/2) ln(1/D) + O(1).
Columns lo-hln and hi-hln are the excess brackets minus (1/2) ln(1/D).

Run: python experiments/ft7_moving_kernel_probe.py [results/FT7-moving-kernel-probe.json]
"""
import json
import math
import sys

import numpy as np
from scipy import integrate, optimize, special

EULER = 0.5772156649015329


def loss_iso(delta):
    """E(|Xhat + Z| - |Xhat|)^2 for Delta = delta I, by quadrature over a = |Xhat|."""
    s2 = 1.0 - delta

    def integrand(a):
        nu = a * a / (2.0 * delta)
        lhalf = (1.0 + nu) * special.ive(0, nu / 2.0) + nu * special.ive(1, nu / 2.0)
        er = math.sqrt(delta) * math.sqrt(math.pi / 2.0) * lhalf
        cond = 2.0 * a * a + 2.0 * delta - 2.0 * a * er
        dens = (a / s2) * math.exp(-a * a / (2.0 * s2))
        return cond * dens

    val, _ = integrate.quad(integrand, 0.0, 12.0, limit=400, epsabs=1e-14, epsrel=1e-11)
    return val


def loss_mc(d1, d2, n, rng):
    """Monte Carlo consumer loss for Delta = diag(d1, d2)."""
    xh = rng.standard_normal((n, 2)) * np.sqrt([1.0 - d1, 1.0 - d2])
    z = rng.standard_normal((n, 2)) * np.sqrt([d1, d2])
    l = (np.linalg.norm(xh + z, axis=1) - np.linalg.norm(xh, axis=1)) ** 2
    return float(l.mean()), float(l.std() / math.sqrt(n))


def main():
    seed = 20261130
    rng = np.random.default_rng(seed)
    h_u = 1.0 + EULER / 2.0 - 0.5 * math.log(2.0)  # differential entropy of Rayleigh(1), nats
    var_u = (4.0 - math.pi) / 2.0
    rows = []
    for D in [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5]:
        delta = optimize.brentq(lambda d: loss_iso(d) - D, D / 4.0, min(0.99, 4.0 * D), xtol=1e-18, rtol=1e-12)
        r_fix = math.log(1.0 / delta)
        slb = h_u - 0.5 * math.log(2.0 * math.pi * math.e * D)
        gub = 0.5 * math.log(var_u / D)
        rows.append({
            "D": D, "delta_iso": delta, "delta_over_D": delta / D, "R_fix": r_fix,
            "R_U_lower_SLB": slb, "R_U_upper_gauss": gub,
            "excess_lower": r_fix - gub, "excess_upper": r_fix - max(slb, 0.0),
            "excess_lower_minus_half_ln_1_over_D": r_fix - gub - 0.5 * math.log(1.0 / D),
            "excess_upper_minus_half_ln_1_over_D": r_fix - max(slb, 0.0) - 0.5 * math.log(1.0 / D),
        })
    # isotropy check: at fixed det Delta, does anisotropy lower the consumer loss?
    aniso = []
    for D in [1e-2, 1e-3]:
        delta = optimize.brentq(lambda d: loss_iso(d) - D, D / 4.0, min(0.99, 4.0 * D), xtol=1e-18, rtol=1e-12)
        for ratio in [1.0, 1.5, 3.0, 10.0]:
            d1, d2 = delta * math.sqrt(ratio), delta / math.sqrt(ratio)
            if d1 >= 1.0:
                continue
            m, se = loss_mc(d1, d2, 2_000_000, rng)
            aniso.append({"D": D, "det_root": delta, "ratio": ratio, "loss_mc": m, "se": se,
                          "loss_over_D": m / D})
    # quadrature cross-check by Monte Carlo at one point
    d_chk = 1e-3
    m_chk, se_chk = loss_mc(d_chk, d_chk, 4_000_000, rng)
    out = {
        "probe": "FT.7 fixed-weight price, consumer |x|, X ~ N(0, I_2)",
        "class": "exploratory probe (disclosed); not a registered test",
        "seed": seed, "h_U_nats": h_u, "var_U": var_u,
        "prediction": "excess = (1/2) ln(1/D) + O(1)",
        "rows": rows, "anisotropy_check": aniso,
        "quadrature_check": {"delta": d_chk, "loss_quad": loss_iso(d_chk), "loss_mc": m_chk,
                             "se": se_chk},
    }
    path = sys.argv[1] if len(sys.argv) > 1 else "results/FT7-moving-kernel-probe.json"
    json.dump(out, open(path, "w"), indent=1)
    print(f"{'D':>8} {'delta/D':>8} {'R_fix':>8} {'R_U lo':>8} {'R_U hi':>8} "
          f"{'exc lo':>8} {'exc hi':>8} {'lo-hln':>8} {'hi-hln':>8}")
    for r in rows:
        print(f"{r['D']:8.0e} {r['delta_over_D']:8.4f} {r['R_fix']:8.4f} {r['R_U_lower_SLB']:8.4f} "
              f"{r['R_U_upper_gauss']:8.4f} {r['excess_lower']:8.4f} {r['excess_upper']:8.4f} "
              f"{r['excess_lower_minus_half_ln_1_over_D']:8.4f} "
              f"{r['excess_upper_minus_half_ln_1_over_D']:8.4f}")
    print("anisotropy (fixed det):")
    for a in aniso:
        print(f"  D={a['D']:.0e} ratio={a['ratio']:5.1f} loss/D={a['loss_over_D']:.4f} (se {a['se']/a['D']:.4f})")
    q = out["quadrature_check"]
    print(f"quadrature {q['loss_quad']:.6e} vs MC {q['loss_mc']:.6e} +- {q['se']:.1e}")


if __name__ == "__main__":
    main()
