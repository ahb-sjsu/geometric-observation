# Numerical falsification harness for the CONSUMER COMPLEMENTARITY TAX note
# (GO-P-2026-055; paper/complementarity-tax.tex v0.3). Claims netted:
#   T1 (rate floor, attributed to Gray 1973 / Xiao-Luo 2005 after reduction):
#       D_A * D_B >= kappa * 2^(-2 I(X;Xhat_A,Xhat_B)),
#       kappa = det(B' Sigma_x B), B = [u v]
#   P2 (exactness, attributed): R_AB = 1/2 log2(kappa/(D_A D_B)) iff
#       diag(D_A,D_B) <= B' Sigma_x B (PSD order); VI-10-corrected isotropic
#       form D <= sigma^2 (1 - |cos theta|)
#   T4 (work floor, no prior found): same with Sigma_{X|S} and I(X;Xhat|S)
#   C5 (discount identity, no prior found):
#       1/2 log2(kappa/kappa_S) = I(Y;S) exactly (jointly Gaussian)
#   Worked instance (Sec. 5): per-coordinate reduction; tax gap
#       CT_R - CT_W = 1/2 log2(1/(s^2+(1-s^2)D)) -> I(X1;S) as D->0;
#       mismatched reset context discounts nothing.
# Sections [1]-[7] implement prereg GO-P-2026-055 s1-s7 with the sealed bars.
# numpy + scipy only; Tier A (< ~5 min).
#   python verify_complementarity_tax.py           -> governed seed 20260810
#   python verify_complementarity_tax.py --pilot   -> logged pilot seed 20260809
# Solver non-convergence in [3]/[4] is a logged instrumentation miss per the
# sealed design note, not evidence against the theory. The conditional
# Blahut-Arimoto fixed point reuses the machinery validated under
# GO-P-2026-044 (verify_gaussian_sideinfo.py).
# MIT License.
import json
import math
import sys

import numpy as np
from scipy.optimize import minimize

PILOT = "--pilot" in sys.argv
SEED = 20260809 if PILOT else 20260810
rng = np.random.default_rng(SEED)
LOG2 = math.log(2.0)
fail = []
results = {"prereg": "GO-P-2026-055", "seed": SEED, "pilot": PILOT,
           "sections": {}}
print(f"GO-P-2026-055 harness — {'PILOT' if PILOT else 'GOVERNED'} run, "
      f"seed {SEED}")

# ----------------------------------------------------------------- helpers
def rand_psd(d, scale=1.0):
    A = rng.standard_normal((d, d))
    return scale * (A @ A.T) / d + 1e-3 * np.eye(d)

def rand_unit(d):
    w = rng.standard_normal(d)
    return w / np.linalg.norm(w)

def kappa_of(Sig, u, v):
    B = np.column_stack([u, v])
    return float(np.linalg.det(B.T @ Sig @ B))

def gauss_channel(Sx, C, Q, u, v, G=None, Rs=None):
    """Xhat = C X + N(0,Q); optional S = G X + N(0,Rs), noises independent
    (so Xhat - X - S is Markov). Consumers decode with E[X|Xhat] (Lemma 1
    equality), which only strengthens the floor test. Bits."""
    Sy = C @ Sx @ C.T + Q
    K = Sx @ C.T @ np.linalg.solve(Sy, np.eye(Sy.shape[0]))
    Se = Sx - K @ C @ Sx                       # E Cov(X|Xhat)
    out = dict(DA=float(u @ Se @ u), DB=float(v @ Se @ v),
               I=0.5 * (np.linalg.slogdet(Sy)[1]
                        - np.linalg.slogdet(Q)[1]) / LOG2)
    if G is not None:
        SxS = Sx - Sx @ G.T @ np.linalg.solve(G @ Sx @ G.T + Rs, G @ Sx)
        SyS = C @ SxS @ C.T + Q
        out["SxS"] = SxS
        out["Icond"] = 0.5 * (np.linalg.slogdet(SyS)[1]
                              - np.linalg.slogdet(Q)[1]) / LOG2
    return out

def rand_instance(with_S):
    d = int(rng.integers(2, 5))
    Sx = rand_psd(d)
    m = int(rng.integers(1, d + 1))
    C = rng.standard_normal((m, d))
    Q = rand_psd(m, scale=float(rng.uniform(0.01, 2.0)))
    u, v = rand_unit(d), rand_unit(d)
    if abs(u @ v) > 0.999:
        return None
    if not with_S:
        return Sx, C, Q, u, v, None, None
    k = int(rng.integers(1, d + 1))
    G = rng.standard_normal((k, d))
    Rs = rand_psd(k, scale=float(rng.uniform(0.01, 2.0)))
    return Sx, C, Q, u, v, G, Rs

# =============================================================== section 1
print("=" * 78)
print("[1] s1 rate net: 4000 random Gaussian channels, d in {2,3,4}")
worst1 = np.inf
n1 = 0
while n1 < 4000:
    inst = rand_instance(False)
    if inst is None:
        continue
    Sx, C, Q, u, v, _, _ = inst
    q = gauss_channel(Sx, C, Q, u, v)
    floor = kappa_of(Sx, u, v) * 2.0 ** (-2 * q["I"])
    worst1 = min(worst1, (q["DA"] * q["DB"] - floor) / max(floor, 1e-300))
    n1 += 1
ok1 = worst1 > -1e-9
print(f"  worst relative slack = {worst1:.3e}  (bar: never < -1e-9)  "
      f"pass={ok1}")
results["sections"]["s1"] = {"worst_rel_slack": worst1, "pass": bool(ok1)}
if not ok1:
    fail.append("s1-rate-net")

# =============================================================== section 2
print("=" * 78)
print("[2] s2 work net: 4000 random channels + Gaussian side information")
worst2 = np.inf
n2 = 0
while n2 < 4000:
    inst = rand_instance(True)
    if inst is None:
        continue
    Sx, C, Q, u, v, G, Rs = inst
    q = gauss_channel(Sx, C, Q, u, v, G=G, Rs=Rs)
    floor = kappa_of(q["SxS"], u, v) * 2.0 ** (-2 * q["Icond"])
    worst2 = min(worst2, (q["DA"] * q["DB"] - floor) / max(floor, 1e-300))
    n2 += 1
ok2 = worst2 > -1e-9
print(f"  worst relative slack = {worst2:.3e}  (bar: never < -1e-9)  "
      f"pass={ok2}")
results["sections"]["s2"] = {"worst_rel_slack": worst2, "pass": bool(ok2)}
if not ok2:
    fail.append("s2-work-net")

# =============================================================== section 3
print("=" * 78)
print("[3] s3 exactness on/off the regime (max-det, multi-start SLSQP)")

def R_joint(Sx, u, v, DA, DB, restarts=12):
    """1/2 log2(det Sx / max det Sigma) s.t. Sigma<=Sx, u'Su<=DA, v'Sv<=DB.
    Bits, or None on solver non-convergence (instrumentation miss)."""
    def mat(p):
        return np.array([[p[0], p[2]], [p[2], p[1]]])
    def negobj(p):
        sign, ld = np.linalg.slogdet(mat(p))
        return 1e6 if sign <= 0 else -ld
    cons = [
        {"type": "ineq", "fun": lambda p: np.linalg.eigvalsh(mat(p))[0]},
        {"type": "ineq", "fun": lambda p: np.linalg.eigvalsh(Sx - mat(p))[0]},
        {"type": "ineq", "fun": lambda p: DA - u @ mat(p) @ u},
        {"type": "ineq", "fun": lambda p: DB - v @ mat(p) @ v},
    ]
    best = None
    for _ in range(restarts):
        x0 = np.array([rng.uniform(0.01, 0.5), rng.uniform(0.01, 0.5),
                       rng.uniform(-0.1, 0.1)])
        r = minimize(negobj, x0, constraints=cons, method="SLSQP",
                     options={"maxiter": 600, "ftol": 1e-12})
        if r.success and (best is None or r.fun < best):
            best = r.fun
    if best is None:
        return None
    return 0.5 * (np.linalg.slogdet(Sx)[1] + best) / LOG2

def iso(theta_deg):
    th = math.radians(theta_deg)
    return np.array([1.0, 0.0]), np.array([math.cos(th), math.sin(th)])

ok3, miss3 = True, False
D = 0.10
s3 = {}
for deg in (30, 45, 60, 75, 90):
    u, v = iso(deg)
    R = R_joint(np.eye(2), u, v, D, D)
    if R is None:
        miss3 = True
        continue
    floor = 0.5 * math.log2(math.sin(math.radians(deg)) ** 2 / D ** 2)
    ok = abs(R - floor) <= 1e-3
    ok3 &= ok
    s3[f"on_{deg}"] = {"R": R, "floor": floor, "pass": bool(ok)}
    print(f"  ON  theta={deg:3d}: R_AB={R:.5f} b, floor={floor:.5f} b, "
          f"|diff|<=1e-3: {ok}")
u, v = iso(15)
R15 = R_joint(np.eye(2), u, v, D, D)
if R15 is None:
    miss3 = True
else:
    floor15 = 0.5 * math.log2(math.sin(math.radians(15)) ** 2 / D ** 2)
    ok = (R15 - floor15) >= 0.05
    ok3 &= ok
    s3["off_15"] = {"excess": R15 - floor15, "pass": bool(ok)}
    print(f"  OFF theta= 15: excess over floor = {R15 - floor15:.4f} b "
          f"(bar >= 0.05): {ok}")
Dstar = 1 - math.cos(math.radians(45))
for tag, Db, mode in (("D_minus", Dstar - 0.02, "tight"),
                      ("D_plus", Dstar + 0.02, "slack")):
    u, v = iso(45)
    R = R_joint(np.eye(2), u, v, Db, Db)
    if R is None:
        miss3 = True
        continue
    floor = 0.5 * math.log2(math.sin(math.radians(45)) ** 2 / Db ** 2)
    # slack bar 1.5e-3: corrected from the drafted 5e-3 after the LOGGED
    # pilot (seed 20260809) measured the deterministic gap at D*+0.02 as
    # +2.95e-3 -- a net-design artifact in the drafted bar, fixed pre-seal
    # and disclosed in the prereg PILOT NOTE. No other bar was touched.
    gap = R - floor
    ok = (abs(gap) <= 1e-3) if mode == "tight" else (gap >= 1.5e-3)
    ok3 &= ok
    s3[f"bracket_{tag}"] = {"D": Db, "gap": gap, "pass": bool(ok)}
    print(f"  BRACKET {tag}: D={Db:.4f}, R-floor={gap:+.5f} b ({mode}): {ok}")
u, v = iso(120)
Bm = np.column_stack([u, v])
lam_min = float(np.linalg.eigvalsh(Bm.T @ Bm - 0.7 * np.eye(2))[0])
R120 = R_joint(np.eye(2), u, v, 0.7, 0.7)
if R120 is None:
    miss3 = True
else:
    floor120 = 0.5 * math.log2(math.sin(math.radians(120)) ** 2 / 0.49)
    ok = (lam_min < 0) and (abs(lam_min + 0.2) < 1e-9) \
        and (R120 - floor120 >= 0.03)
    ok3 &= ok
    s3["obtuse_120"] = {"lam_min": lam_min, "excess": R120 - floor120,
                        "pass": bool(ok)}
    print(f"  OBTUSE theta=120, D=0.7: lam_min={lam_min:.6f} (want -0.2), "
          f"R-floor={R120 - floor120:.4f} b (bar >= 0.03): {ok}")
results["sections"]["s3"] = s3
if miss3:
    fail.append("s3-INSTRUMENTATION-MISS(solver-nonconvergence)")
elif not ok3:
    fail.append("s3-exactness")

# =============================================================== section 4
print("=" * 78)
print("[4] s4 tax closed form on the regime grid")
ok4 = True
prev = -np.inf
s4 = {}
for deg in (30, 45, 60, 75, 90):
    key = f"on_{deg}"
    if key not in s3:
        ok4 = False
        break
    CT = s3[key]["R"] - 0.5 * math.log2(1 / D)
    pred = 0.5 * math.log2(math.sin(math.radians(deg)) ** 2 / D)
    ok = abs(CT - pred) <= 1e-3 and CT > prev
    ok4 &= ok
    prev = CT
    s4[str(deg)] = {"CT_R": CT, "pred": pred, "pass": bool(ok)}
    print(f"  theta={deg:3d}: CT_R={CT:.5f} b vs pred {pred:.5f} b, "
          f"monotone+match: {ok}")
results["sections"]["s4"] = s4
if not ok4:
    fail.append("s4-tax-closed-form")

# =============================================================== section 5
print("=" * 78)
print("[5] s5 discount identity 1/2 log2(kappa/kappa_S) = I(Y;S)")
worst5, mono5, n5 = 0.0, True, 0
while n5 < 2000:
    d = int(rng.integers(2, 5))
    Sx = rand_psd(d)
    u, v = rand_unit(d), rand_unit(d)
    if abs(u @ v) > 0.999:
        continue
    k = int(rng.integers(1, d + 1))
    G = rng.standard_normal((k, d))
    Rs = rand_psd(k, scale=float(rng.uniform(0.01, 2.0)))
    B = np.column_stack([u, v])
    SxS = Sx - Sx @ G.T @ np.linalg.solve(G @ Sx @ G.T + Rs, G @ Sx)
    kap = float(np.linalg.det(B.T @ Sx @ B))
    kapS = float(np.linalg.det(B.T @ SxS @ B))
    mono5 &= kapS <= kap + 1e-12
    disc = 0.5 * math.log2(kap / kapS)
    SY = B.T @ Sx @ B
    SS = G @ Sx @ G.T + Rs
    CYS = B.T @ Sx @ G.T
    Jt = np.block([[SY, CYS], [CYS.T, SS]])
    IYS = 0.5 * (np.linalg.slogdet(SY)[1] + np.linalg.slogdet(SS)[1]
                 - np.linalg.slogdet(Jt)[1]) / LOG2
    worst5 = max(worst5, abs(disc - IYS))
    n5 += 1
# geometric null: d=3, reads in span{e1,e2}, S reads e3 only
Sx3 = np.eye(3)
u3 = np.array([1.0, 0.0, 0.0])
v3 = np.array([math.cos(1.0), math.sin(1.0), 0.0])
G3 = np.array([[0.0, 0.0, 1.0]])
SxS3 = Sx3 - Sx3 @ G3.T @ np.linalg.solve(
    G3 @ Sx3 @ G3.T + np.array([[0.5]]), G3 @ Sx3)
disc_null = 0.5 * math.log2(kappa_of(Sx3, u3, v3) / kappa_of(SxS3, u3, v3))
# exact u-read: kappa_S -> 0
Sx2 = rand_psd(2)
u2, v2 = rand_unit(2), np.array([0.0, 1.0])
SxS2 = Sx2 - np.outer(Sx2 @ u2, u2 @ Sx2) / float(u2 @ Sx2 @ u2)
kapS_exact = abs(kappa_of(SxS2, u2, v2))
ok5 = (worst5 <= 1e-10) and mono5 and (abs(disc_null) <= 1e-10) \
    and (kapS_exact <= 1e-12)
print(f"  2000 instances: max|discount - I(Y;S)| = {worst5:.2e} (bar 1e-10); "
      f"kappa_S <= kappa always: {mono5}")
print(f"  independent-S null discount = {disc_null:.2e} (bar 1e-10); "
      f"exact-u-read kappa_S = {kapS_exact:.2e} (bar 1e-12)  pass={ok5}")
results["sections"]["s5"] = {"max_dev": worst5, "null": disc_null,
                             "kappaS_exact_read": kapS_exact,
                             "pass": bool(ok5)}
if not ok5:
    fail.append("s5-discount-identity")

# =============================================================== section 6
print("=" * 78)
print("[6] s6 worked instance, discretized (per-coordinate vs full channel)")

def Hb(p):
    p = np.asarray(p, dtype=float).ravel()
    p = p[p > 1e-300]
    return float(-(p * np.log2(p)).sum())

def mi_joint(J):
    return Hb(J.sum(1)) + Hb(J.sum(0)) - Hb(J)

def cond_mi(pXS, q):
    L = 0.0
    for s in range(pXS.shape[1]):
        ps = pXS[:, s].sum()
        if ps > 1e-15:
            pxg = pXS[:, s] / ps
            L += ps * mi_joint(pxg[:, None] * q)
    return float(L)

def ba_min(pXS, d, beta, conditional, iters=3000, tol=1e-11):
    """Fixed point minimizing [I(X;Xhat) or I(X;Xhat|S)] + beta*E d over
    q(xhat|x). Conditional update: q propto prod_s r(xhat|s)^{p(s|x)}
    * 2^{-beta d}; the objective is convex in q (VI-8), so the alternating
    minimization converges to the global optimum (044-validated machinery)."""
    nx, nxh = d.shape
    pX = pXS.sum(1)
    psx = pXS / np.maximum(pX, 1e-300)[:, None]
    pS = pXS.sum(0)
    pxg = pXS / np.maximum(pS, 1e-300)[None, :]
    q = np.full((nx, nxh), 1.0 / nxh)
    for _ in range(iters):
        if conditional:
            qs = pxg.T @ q
            lq = psx @ np.log(np.maximum(qs, 1e-300)) - beta * LOG2 * d
        else:
            qm = pX @ q
            lq = np.log(np.maximum(qm, 1e-300))[None, :] - beta * LOG2 * d
        lq -= lq.max(axis=1, keepdims=True)
        qn = np.exp(lq)
        qn /= qn.sum(axis=1, keepdims=True)
        if np.abs(qn - q).max() < tol:
            q = qn
            break
        q = qn
    return q

def solve_at_D(pXS, d, Dtar, conditional, blo=1e-3, bhi=4000.0, steps=42):
    """Bisect beta so achieved distortion ~= Dtar from below; return
    (objective value in bits, achieved distortion)."""
    pX = pXS.sum(1)
    for _ in range(steps):
        bm = math.sqrt(blo * bhi)
        q = ba_min(pXS, d, bm, conditional)
        dd = float((pX[:, None] * q * d).sum())
        if dd > Dtar:
            blo = bm
        else:
            bhi = bm
    q = ba_min(pXS, d, bhi, conditional)
    val = cond_mi(pXS, q) if conditional else mi_joint(pX[:, None] * q)
    return val, float((pX[:, None] * q * d).sum())

def gauss_grid(n, lo=-4.0, hi=4.0):
    x = np.linspace(lo, hi, n)
    w = np.exp(-x ** 2 / 2)
    return x, w / w.sum()

# fine per-coordinate grids: 61 source, 41 reproduction, 21 side-info values
xg, px = gauss_grid(61)
xh = np.linspace(-4, 4, 41)
d1 = (xg[:, None] - xh[None, :]) ** 2
pX_unc = px[:, None]                          # trivial one-value "S" column
ok6 = True
s6 = {}
for s2v in (0.2, 0.5):
    tau2 = s2v / (1 - s2v)                    # Var(X1|S) = tau2/(1+tau2)
    sg = np.linspace(-4 * math.sqrt(1 + tau2), 4 * math.sqrt(1 + tau2), 21)
    pXS = px[:, None] * np.exp(-(sg[None, :] - xg[:, None]) ** 2 / (2 * tau2))
    pXS /= pXS.sum()
    for Dv in (0.25, 0.05):
        LA, dA = solve_at_D(pXS, d1, Dv, conditional=True)
        RB, dB = solve_at_D(pX_unc, d1, Dv, conditional=False)
        LA_pred = 0.5 * math.log2((s2v + (1 - s2v) * Dv) / Dv)
        R_pred = 0.5 * math.log2(1 / Dv)
        LAB, LAB_pred = LA + RB, LA_pred + R_pred
        gap = RB - LA                          # CT_R_disc - CT_W_disc
        gap_pred = 0.5 * math.log2(1 / (s2v + (1 - s2v) * Dv))
        ok = (abs(LA - LA_pred) <= 0.06 and abs(LAB - LAB_pred) <= 0.06
              and abs(gap - gap_pred) <= 0.06)
        ok6 &= ok
        s6[f"s2={s2v}_D={Dv}"] = {
            "L_A": LA, "L_A_pred": LA_pred, "L_AB": LAB,
            "L_AB_pred": LAB_pred, "taxgap": gap, "taxgap_pred": gap_pred,
            "pass": bool(ok)}
        print(f"  s^2={s2v} D={Dv}: L_A={LA:.4f} (pred {LA_pred:.4f}), "
              f"L_AB={LAB:.4f} (pred {LAB_pred:.4f}), "
              f"gap={gap:.4f} (pred {gap_pred:.4f})  pass={ok}")

# full-channel separability net on coarse product grids (13^2 x 7^2, 7 s)
xgc, pxc = gauss_grid(13)
xhc = np.linspace(-3.2, 3.2, 7)
d1c = (xgc[:, None] - xhc[None, :]) ** 2
s2v, Dv = 0.2, 0.25
tau2 = s2v / (1 - s2v)
sgc = np.linspace(-4 * math.sqrt(1 + tau2), 4 * math.sqrt(1 + tau2), 7)
pXSc = pxc[:, None] * np.exp(-(sgc[None, :] - xgc[:, None]) ** 2 / (2 * tau2))
pXSc /= pXSc.sum()
pJ = (pXSc[:, None, :] * pxc[None, :, None]).reshape(13 * 13, 7)
dJ1 = np.kron(d1c, np.ones((13, 7)))          # (169,49): d on coordinate 1
dJ2 = np.kron(np.ones((13, 7)), d1c)          # (169,49): d on coordinate 2
Lfull, dfull = solve_at_D(pJ, dJ1 + dJ2, 2 * Dv, conditional=True)
env = np.inf
for dsplit in np.linspace(0.35 * Dv, 1.65 * Dv, 9):
    L1, _ = solve_at_D(pXSc, d1c, dsplit, conditional=True)
    L2, _ = solve_at_D(pxc[:, None], d1c, 2 * Dv - dsplit, conditional=False)
    env = min(env, L1 + L2)
sep_ok = Lfull >= env - 5e-3
ok6 &= sep_ok
s6["full_channel"] = {"L_full": Lfull, "envelope": env,
                      "achieved_d_total": dfull, "pass": bool(sep_ok)}
print(f"  full-channel (13^2 x 7^2): L_full={Lfull:.4f} vs per-coordinate "
      f"envelope {env:.4f}  (bar: never below env - 5e-3)  pass={sep_ok}")
results["sections"]["s6"] = s6
if not ok6:
    fail.append("s6-instance-reduction")

# =============================================================== section 7
print("=" * 78)
print("[7] s7 mismatched reset context saves nothing")
s2v, Dv = 0.2, 0.25
tau2 = s2v / (1 - s2v)
sg = np.linspace(-4 * math.sqrt(1 + tau2), 4 * math.sqrt(1 + tau2), 21)
pXS_true = px[:, None] * np.exp(-(sg[None, :] - xg[:, None]) ** 2 / (2 * tau2))
pXS_true /= pXS_true.sum()
pXS_shuf = np.outer(px, pXS_true.sum(0))      # same marginals, independent
L_shuf, _ = solve_at_D(pXS_shuf, d1, Dv, conditional=True)
R_unc, _ = solve_at_D(pX_unc, d1, Dv, conditional=False)
discount_shuf = R_unc - L_shuf
ok7 = abs(discount_shuf) <= 5e-3
print(f"  shuffled-S' discount = {discount_shuf:.2e} b (bar |.| <= 5e-3); "
      f"hence CT_R - CT_W(S') <= 5e-3 as well  pass={ok7}")
results["sections"]["s7"] = {"discount_shuffled": discount_shuf,
                             "pass": bool(ok7)}
if not ok7:
    fail.append("s7-null-context")

# =====================================================================
print("=" * 78)
verdict = "ALL PASS" if not fail else f"FAIL: {fail}"
print("VERDICT:", verdict)
results["verdict"] = verdict
print("===GO-P-2026-055-RESULT-BEGIN===")
print(json.dumps(results, indent=1, default=float))
print("===GO-P-2026-055-RESULT-END===")
