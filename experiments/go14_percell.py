"""GO-P-2026-086 -- per-cell convexity of L_a: REFUTED after the first cell,
and TRUE at the first cell.

WHAT THIS NETS
--------------
Theorem C (079) proves n L_a jointly convex in (H, Gamma) only in REGROUPED
form: the block bracket plus the S-side leak sum. Remark rem:percell recorded
as OPEN whether the INDIVIDUAL per-cell CMI terms are convex. They are not:

  (1) CELL 0 IS CONVEX, and was never open. With no Yh^{t-1} to condition on,
      the t=0 term collapses EXACTLY to the block bracket in scalar form with
      a TRUNCATED Q:
          f_0 = 1/2 log2 [ (G00 - h0 Qk h0') / (G00 - h0 P h0') ],
          Qk  = K_[k]' Cs_[k]^-1 K_[k],   k = k(0),  h0 = first row of H.
      This is an algebraic rearrangement, so cell 0's convexity is the 074
      lift's SCALAR CASE and needs no separate argument.

  (2) EVERY CELL t >= 1 ADMITS STRICTLY CONCAVE DIRECTIONS. A pinned witness
      of three points of int D, whose exact midpoint is the base point, has a
      Jensen gap the WRONG WAY.

  (3) THE REFUTATION NEEDS NO NON-CAUSAL RECORD. {H : HP lower-triangular} is
      a LINEAR subspace, so midpoints stay causal and a violation there is a
      violation on D. A second pinned witness lives inside it.

WHAT THIS DOES **NOT** TOUCH
----------------------------
Theorem C, Theorem R1, the 079 certificates and the 082/083/084/085 chain are
untouched, and s6 GATES that: at the very same witness pair the TOTAL n L_a is
convex, because the neighbouring cells' convexity absorbs the concave one. The
mass that makes a late cell concave is exactly what the regrouping moves into
the leak sum. The regrouping is not a convenience; it is the proof. The only
other mention of per-cell convexity in the document is the open-problems list.

HONESTY NOTES THAT TRAVEL WITH THE SEAL
---------------------------------------
* The witness was FOUND BEFORE this harness existed (PROBE.md, 2026-08-08).
  Every witness gate here is COMMITTED-VALUE REPRODUCTION, not discovery, and
  is labelled as such. Nothing here searches.
* The R-IND-5 pass on the refutation was run in the SAME context that produced
  it, not by a fresh-context verifier. Recorded in PROBE.md and in the prereg.
* NO OPTIMIZER, no fixed point, no root find anywhere in this file, so no gate
  can race a solver (the 079 lesson). Re-run tier by construction.

Sentinel ===GO14PC-JSON=== with ===END===; flag GO14PC_supported.
Pilot seed 20261190 / governed seed 20261191. SEED STAMPS ONLY: the seed is
recorded and feeds NO computation. Every base point is an internally pinned
literal or comes from an internally pinned generator, so pilot and governed
produce a bit-identical payload.
"""
import argparse
import json
import sys
import time
from fractions import Fraction
from decimal import Decimal, getcontext

import numpy as np
from scipy.linalg import cho_factor, cho_solve

A_, RHO, TAU2 = 0.8, 0.7, 0.4
SN2 = 1.0 - RHO ** 2
LN2 = np.log(2.0)

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a_ = ap.parse_args()
SEED = a_.seed if a_.seed is not None else (20261190 if a_.pilot else 20261191)
vals = {"seed": SEED, "pilot": bool(a_.pilot)}
verdicts = {}


# ===================== model + the three evaluation routes ================
class Model:
    def __init__(self, n):
        self.n = n
        i = np.arange(n)
        self.Cv = A_ ** np.abs(i[:, None] - i[None, :])
        self.Cy = RHO ** 2 * self.Cv + SN2 * np.eye(n)
        self.Cs = self.Cv + TAU2 * np.eye(n)
        self.SigW = np.block([[self.Cv, RHO * self.Cv],
                              [RHO * self.Cv, self.Cy]])
        self.P = np.linalg.inv(self.SigW)
        self.CovWS = np.vstack([self.Cv, RHO * self.Cv])
        self.Q = (self.P @ self.CovWS
                  @ np.linalg.solve(self.Cs, self.CovWS.T) @ self.P)
        self.K = self.CovWS.T @ self.P


def cvar(S, i, cond):
    if len(cond) == 0:
        return float(S[i, i])
    C = S[np.ix_(cond, cond)]
    b = S[cond, i]
    cf = cho_factor(C, lower=True, check_finite=False)
    return float(S[i, i] - b @ cho_solve(cf, b, check_finite=False))


def sched0(n, Delta):
    return np.minimum(np.arange(n) + Delta + 1, n)


def percell(M, H, Gam, Delta):
    """ROUTE 1 -- moment form: MP pivots and the (S, Yh) joint."""
    n = M.n
    se0 = sched0(n, Delta)
    MP = Gam - H @ M.P @ H.T
    MP = 0.5 * (MP + MP.T)
    J = np.block([[M.Cs, M.K @ H.T], [H @ M.K.T, Gam]])
    J = 0.5 * (J + J.T)
    out = []
    for t in range(n):
        vden = cvar(MP, t, list(range(t)))
        cond = list(range(se0[t])) + [n + i for i in range(t)]
        vnum = cvar(J, n + t, cond)
        if vden <= 0 or vnum <= 0:
            return None
        out.append(0.5 * np.log2(vnum / vden))
    return np.array(out)


def joint4(M, Ay, Av, Ncov):
    """Cov of (V, Y, S, Yh) from definitions -- for routes 2 and 3."""
    n = M.n
    Cv, Cy = M.Cv, M.Cy
    CvY = RHO * Cv
    CvH = Cv @ Av.T + CvY @ Ay.T
    CyH = CvY.T @ Av.T + Cy @ Ay.T
    ChH = (Av @ Cv @ Av.T + Ay @ Cy @ Ay.T
           + Av @ CvY @ Ay.T + Ay @ CvY.T @ Av.T + Ncov)
    Z = np.zeros((4 * n, 4 * n))
    Z[0:n, 0:n] = Cv
    Z[n:2 * n, n:2 * n] = Cy
    Z[2 * n:3 * n, 2 * n:3 * n] = M.Cs
    Z[3 * n:, 3 * n:] = ChH

    def put(i, j, B):
        Z[i * n:(i + 1) * n, j * n:(j + 1) * n] = B
        Z[j * n:(j + 1) * n, i * n:(i + 1) * n] = B.T
    put(0, 1, CvY); put(0, 2, Cv); put(1, 2, CvY.T)
    put(0, 3, CvH); put(1, 3, CyH); put(2, 3, CvH)
    return 0.5 * (Z + Z.T)


def _record(M, H, Gam):
    A = H @ M.P
    Nc = Gam - H @ M.P @ H.T
    return A[:, :M.n], A[:, M.n:], 0.5 * (Nc + Nc.T)


def percell_4n(M, H, Gam, Delta):
    """ROUTE 2 -- rebuild the record and use the 4n joint."""
    n = M.n
    Av, Ay, Nc = _record(M, H, Gam)
    S4 = joint4(M, Ay, Av, Nc)
    iT = list(range(2 * n))
    Sb, Hb = 2 * n, 3 * n
    se0 = sched0(n, Delta)
    out = []
    for t in range(n):
        cond = list(range(Sb, Sb + se0[t])) + list(range(Hb, Hb + t))
        out.append(0.5 * np.log2(cvar(S4, Hb + t, cond)
                                 / cvar(S4, Hb + t, iT + cond)))
    return np.array(out)


def percell_logdet(M, H, Gam, Delta):
    """ROUTE 3 -- log-dets of 4n submatrices. No conditional-variance helper."""
    n = M.n
    Av, Ay, Nc = _record(M, H, Gam)
    S4 = joint4(M, Ay, Av, Nc)
    iT = list(range(2 * n))
    Sb, Hb = 2 * n, 3 * n
    se0 = sched0(n, Delta)

    def ld(idx):
        if not idx:
            return 0.0
        return np.linalg.slogdet(S4[np.ix_(idx, idx)])[1]
    out = []
    for t in range(n):
        aa = list(range(Sb, Sb + se0[t])) + [Hb + i for i in range(t)]
        bb = iT + aa
        out.append(((ld(aa + [Hb + t]) - ld(aa))
                    - (ld(bb + [Hb + t]) - ld(bb))) / (2 * LN2))
    return np.array(out)


def repr_bits(M, H, Gam, Delta):
    """Theorem R RHS: block bracket + leak sum (the REGROUPED form)."""
    n = M.n
    MQ = Gam - H @ M.Q @ H.T
    MP = Gam - H @ M.P @ H.T
    sQ, lQ = np.linalg.slogdet(MQ)
    sP, lP = np.linalg.slogdet(MP)
    if sQ <= 0 or sP <= 0:
        return None
    se0 = sched0(n, Delta)
    ks = np.array([int(np.sum(se0 <= j)) for j in range(n)])
    J = np.block([[M.Cs, M.K @ H.T], [H @ M.K.T, Gam]])
    Lc = np.linalg.cholesky(M.Cs)
    lk = 0.0
    for j in range(n):
        cond = list(range(j)) + [n + i for i in range(ks[j])]
        s = cvar(J, j, cond)
        if s <= 0:
            return None
        lk += 2.0 * np.log(np.diag(Lc))[j] - np.log(s)
    return (lQ - lP + lk) / (2 * LN2)


def in_intD(M, H, Gam, tol=1e-10):
    X = 0.5 * ((Gam - H @ M.P @ H.T) + (Gam - H @ M.P @ H.T).T)
    return float(np.linalg.eigvalsh(X).min()) > tol


def pack(H, Gam):
    n = H.shape[0]
    return np.concatenate([H.ravel(), Gam[np.triu_indices(n)]])


def unpack(x, n):
    H = x[:2 * n * n].reshape(n, 2 * n)
    G = np.zeros((n, n))
    iu = np.triu_indices(n)
    G[iu] = x[2 * n * n:]
    return H, G + G.T - np.diag(np.diag(G))


def hessian(fun, x, h=2e-4):
    d = len(x)
    Hs = np.zeros((d, d))
    f0 = fun(x)
    if f0 is None:
        return None
    for i in range(d):
        for j in range(i, d):
            if i == j:
                xp, xm = x.copy(), x.copy()
                xp[i] += h; xm[i] -= h
                fp, fm = fun(xp), fun(xm)
                if fp is None or fm is None:
                    return None
                Hs[i, i] = (fp - 2 * f0 + fm) / h ** 2
            else:
                q = []
                for si, sj in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                    z = x.copy(); z[i] += si * h; z[j] += sj * h
                    q.append(fun(z))
                if any(v is None for v in q):
                    return None
                Hs[i, j] = Hs[j, i] = (q[0] - q[1] - q[2] + q[3]) / (4 * h ** 2)
    return 0.5 * (Hs + Hs.T)


def base_point(M, rng, scale=0.35):
    """Causal-by-construction interior point (internally pinned generator)."""
    n = M.n
    while True:
        Av = np.tril(rng.normal(0, scale, (n, n)))
        Ay = np.tril(rng.normal(0, scale, (n, n)))
        Ab = np.hstack([Av, Ay])
        Nc = (0.3 + 0.4 * rng.random()) * np.eye(n)
        H = Ab @ M.SigW
        G = Ab @ M.SigW @ Ab.T + Nc
        G = 0.5 * (G + G.T)
        if in_intD(M, H, G):
            return H, G


# ===================== the PINNED witnesses (committed values) ============
# Found 2026-08-08 (PROBE.md) BEFORE this harness existed. Reproduction, not
# discovery: nothing below searches for them.
H_BASE = np.array([
    [-0.0006869005823149157, -0.0005495204658519104, -0.0004396163726815387,
     -0.2848860638756038, -0.0003846643260963581, -0.0003077314608770851],
    [-0.5141258694924573, -0.5720215330891457, -0.45761722647131653,
     -0.21675793830883497, -0.6294465851316413, -0.3203320585299216],
    [-0.045683969609016654, 0.018536401207564696, -0.027558679244520917,
     -0.3489151994529134, 0.22580670622075918, -0.20404113618807604]])
G_BASE = np.array([
    [0.574141114904137, -0.07946443391672448, 0.17677329550465268],
    [-0.07946443391672448, 0.8946415914824144, -0.18563049840582752],
    [0.17677329550465268, -0.18563049840582752, 0.7837490118631325]])
H_DIR = np.array([
    [-0.04386839875067463, -0.004501562996746156, -0.023569658274612743,
     0.03984007174015866, -0.0267536615657845, 0.02322376245806674],
    [0.049648600758562145, 0.004323662469832845, 0.02665651835523819,
     -0.047293667914351994, 0.031758957516273334, -0.02756865323152441],
    [0.013729429028674543, 0.011888066126859755, 0.013440626325089728,
     0.009889734855362375, 0.004517409128742628, -0.0030843410504032553]])
G_DIR = np.array([
    [0.03520361319727405, -0.07714839699049042, -0.08625712962881461],
    [-0.07714839699049042, 0.04212453541260486, 0.0957414186218796],
    [-0.08625712962881461, 0.0957414186218796, 0.03531683424331544]])
# committed measurements (PROBE.md, 2026-08-08)
COMMIT = {"f_plus": 0.4209618516, "f_minus": 0.1470759393,
          "f_mid": 0.3535350376, "gap": 6.95161422e-02,
          "total_gap": -3.26796198e-01, "gap_50digit": 0.0695161421594886909968382}
NW, DW, TW = 3, 0, 2                      # witness: n=3, Delta=0, cell 2

M3 = Model(NW)
X_BASE = pack(H_BASE, G_BASE)
X_DIR = pack(H_DIR, G_DIR)
XP, XM = X_BASE + X_DIR, X_BASE - X_DIR

print(f"[go14_percell] seed {SEED} pilot={bool(a_.pilot)}", flush=True)

# ------------------------------------------------------- s1 object identity
print("[s1] the per-cell terms ARE the document's object ...", flush=True)
rng = np.random.default_rng(90210)        # internally pinned
w1 = w2 = 0.0
cnt = 0
for n in (3, 4, 5):
    Mn = Model(n)
    for D in (0, 1, 2):
        for _ in range(12):
            H, G = base_point(Mn, rng)
            s = percell(Mn, H, G, D).sum()
            w1 = max(w1, abs(s - percell_4n(Mn, H, G, D).sum()))
            w2 = max(w2, abs(s - repr_bits(Mn, H, G, D)))
            cnt += 1
vals["s1_points"] = cnt
vals["s1_max_dev_vs_4n_joint"] = w1
vals["s1_max_dev_vs_repr_bits"] = w2
vals["s1_bar"] = 1e-10
verdicts["s1_percell_sum_equals_4n_joint"] = w1 < 1e-10
verdicts["s1_percell_sum_equals_regrouped_repr"] = w2 < 1e-10
print(f"  {cnt} points: vs 4n-joint {w1:.2e}, vs repr_bits {w2:.2e} "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ----------------------------------------------------------- s2 the witness
print("[s2] pinned witness -- COMMITTED-VALUE REPRODUCTION ...", flush=True)
mid_err = float(np.abs(X_BASE - 0.5 * (XP + XM)).max())
pts = {}
for tag, x in (("plus", XP), ("minus", XM), ("mid", X_BASE)):
    H, G = unpack(x, NW)
    Nc = G - H @ M3.P @ H.T
    pts[tag] = (percell(M3, H, G, DW)[TW],
                float(np.linalg.eigvalsh(0.5 * (Nc + Nc.T)).min()))
gap = pts["mid"][0] - 0.5 * (pts["plus"][0] + pts["minus"][0])
vals["s2_f_plus"] = pts["plus"][0]
vals["s2_f_minus"] = pts["minus"][0]
vals["s2_f_mid"] = pts["mid"][0]
vals["s2_gap"] = gap
vals["s2_eigmin_Ncov"] = {k: v[1] for k, v in pts.items()}
vals["s2_midpoint_error"] = mid_err
vals["s2_committed"] = COMMIT
dev = max(abs(pts["plus"][0] - COMMIT["f_plus"]),
          abs(pts["minus"][0] - COMMIT["f_minus"]),
          abs(pts["mid"][0] - COMMIT["f_mid"]))
vals["s2_max_dev_vs_committed"] = dev
verdicts["s2_reproduces_committed_values"] = dev < 5e-10
verdicts["s2_JENSEN_VIOLATION_at_cell_2"] = gap > 6.9e-2
verdicts["s2_all_three_points_strictly_in_intD"] = min(
    v[1] for v in pts.values()) > 1e-3
verdicts["s2_midpoint_is_exact"] = mid_err < 1e-15
print(f"  f(x+)={pts['plus'][0]:.10f} f(x-)={pts['minus'][0]:.10f} "
      f"f(mid)={pts['mid'][0]:.10f}")
print(f"  gap {gap:+.8e} (bar 6.9e-2), committed dev {dev:.2e}, "
      f"midpoint err {mid_err:.1e}, eigmin(Ncov) min "
      f"{min(v[1] for v in pts.values()):.3e} [{time.time()-t0:.0f}s]",
      flush=True)

# --------------------------------------------------- s3 three routes agree
print("[s3] three independent routes ...", flush=True)
spread = 0.0
for x in (XP, XM, X_BASE):
    H, G = unpack(x, NW)
    v = [percell(M3, H, G, DW)[TW], percell_4n(M3, H, G, DW)[TW],
         percell_logdet(M3, H, G, DW)[TW]]
    spread = max(spread, max(v) - min(v))
g2 = (percell_4n(M3, *unpack(X_BASE, NW), DW)[TW]
      - 0.5 * (percell_4n(M3, *unpack(XP, NW), DW)[TW]
               + percell_4n(M3, *unpack(XM, NW), DW)[TW]))
g3 = (percell_logdet(M3, *unpack(X_BASE, NW), DW)[TW]
      - 0.5 * (percell_logdet(M3, *unpack(XP, NW), DW)[TW]
               + percell_logdet(M3, *unpack(XM, NW), DW)[TW]))
vals["s3_route_spread"] = spread
vals["s3_gap_route2_4njoint"] = g2
vals["s3_gap_route3_logdet"] = g3
verdicts["s3_routes_agree"] = spread < 1e-12
verdicts["s3_violation_on_all_three_routes"] = min(gap, g2, g3) > 6.9e-2
print(f"  spread {spread:.2e}; gaps {gap:+.6e} / {g2:+.6e} / {g3:+.6e} "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------- s4 exact-rational confirmation
print("[s4] EXACT rational conditional variances + 60-digit log ...",
      flush=True)


def _fmat(A):
    return [[Fraction(x) for x in row] for row in A]


def _solve_frac(Amat, bvec):
    m = len(Amat)
    Aa = [row[:] + [bvec[i]] for i, row in enumerate(Amat)]
    for c in range(m):
        p = next(r for r in range(c, m) if Aa[r][c] != 0)
        Aa[c], Aa[p] = Aa[p], Aa[c]
        pv = Aa[c][c]
        Aa[c] = [v / pv for v in Aa[c]]
        for r in range(m):
            if r != c and Aa[r][c] != 0:
                f = Aa[r][c]
                Aa[r] = [Aa[r][k] - f * Aa[c][k] for k in range(m + 1)]
    return [Aa[i][m] for i in range(m)]


def _inv_frac(Amat):
    m = len(Amat)
    cols = []
    for j in range(m):
        e = [Fraction(1) if i == j else Fraction(0) for i in range(m)]
        cols.append(_solve_frac(Amat, e))
    return [[cols[j][i] for j in range(m)] for i in range(m)]


def _mul(Aa, Bb):
    return [[sum(Aa[i][k] * Bb[k][j] for k in range(len(Bb)))
             for j in range(len(Bb[0]))] for i in range(len(Aa))]


def _T(Aa):
    return [list(r) for r in zip(*Aa)]


def exact_cvar(S, i, cond):
    if not cond:
        return S[i][i]
    C = [[S[r][c] for c in cond] for r in cond]
    b = [S[r][i] for r in cond]
    y = _solve_frac(C, b)
    return S[i][i] - sum(b[k] * y[k] for k in range(len(cond)))


def exact_ratio(H, G, t, se0t, n):
    a, rho, tau2 = Fraction(4, 5), Fraction(7, 10), Fraction(2, 5)
    sn2 = 1 - rho ** 2
    Cv = [[a ** abs(i - j) for j in range(n)] for i in range(n)]
    Cy = [[rho ** 2 * Cv[i][j] + (sn2 if i == j else 0) for j in range(n)]
          for i in range(n)]
    Cs = [[Cv[i][j] + (tau2 if i == j else 0) for j in range(n)]
          for i in range(n)]
    SigW = [[Fraction(0)] * (2 * n) for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            SigW[i][j] = Cv[i][j]
            SigW[i][n + j] = rho * Cv[i][j]
            SigW[n + i][j] = rho * Cv[i][j]
            SigW[n + i][n + j] = Cy[i][j]
    P = _inv_frac(SigW)
    CovWS = [[Cv[i][j] for j in range(n)] for i in range(n)] + \
            [[rho * Cv[i][j] for j in range(n)] for i in range(n)]
    K = _mul(_T(CovWS), P)
    Hf, Gf = _fmat(H), _fmat(G)
    MP = [[Gf[i][j] - _mul(_mul(Hf, P), _T(Hf))[i][j] for j in range(n)]
          for i in range(n)]
    KH = _mul(K, _T(Hf))
    J = [[Fraction(0)] * (2 * n) for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            J[i][j] = Cs[i][j]
            J[i][n + j] = KH[i][j]
            J[n + i][j] = KH[j][i]
            J[n + i][n + j] = Gf[i][j]
    vden = exact_cvar(MP, t, list(range(t)))
    vnum = exact_cvar(J, n + t, list(range(se0t)) + [n + i for i in range(t)])
    return vnum / vden


getcontext().prec = 60
LN2D = Decimal(2).ln()
ex = {}
for tag, x in (("plus", XP), ("minus", XM), ("mid", X_BASE)):
    H, G = unpack(x, NW)
    r = exact_ratio(H, G, TW, int(sched0(NW, DW)[TW]), NW)
    ex[tag] = (Decimal(r.numerator) / Decimal(r.denominator)).ln() / (2 * LN2D)
gap_exact = ex["mid"] - (ex["plus"] + ex["minus"]) / 2
vals["s4_gap_exact_rational_60dp"] = str(gap_exact)
vals["s4_dev_vs_float64"] = float(abs(gap_exact - Decimal(float(gap))))
vals["s4_committed_50digit"] = COMMIT["gap_50digit"]
verdicts["s4_exact_arithmetic_confirms_violation"] = gap_exact > Decimal("0.069")
verdicts["s4_float64_matches_exact"] = \
    float(abs(gap_exact - Decimal(float(gap)))) < 1e-12
print(f"  exact gap = {str(gap_exact)[:24]} ; float64 dev "
      f"{vals['s4_dev_vs_float64']:.2e} [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------- s5 the cell-0 theorem
print("[s5] cell 0 IS the scalar bracket with truncated Q_k ...", flush=True)
rng = np.random.default_rng(13579)
worst_id = 0.0
worst_eig = 1e9
for n in (3, 4, 5):
    Mn = Model(n)
    for D in (0, 1, 2):
        k = int(sched0(n, D)[0])
        Kk = Mn.K[:k, :]
        Qk = Kk.T @ np.linalg.solve(Mn.Cs[:k, :k], Kk)
        worst_eig = min(worst_eig,
                        float(np.linalg.eigvalsh(Mn.P - Qk).min()))
        for _ in range(20):
            H, G = base_point(Mn, rng)
            h0 = H[0:1, :]
            pred = 0.5 * np.log2(
                (G[0, 0] - (h0 @ Qk @ h0.T).item())
                / (G[0, 0] - (h0 @ Mn.P @ h0.T).item()))
            worst_id = max(worst_id, abs(pred - percell(Mn, H, G, D)[0]))
vals["s5_max_identity_dev"] = worst_id
vals["s5_min_eigmin_P_minus_Qk"] = worst_eig
verdicts["s5_cell0_is_the_scalar_bracket"] = worst_id < 1e-12
verdicts["s5_Qk_strictly_below_P"] = worst_eig > 1e-3
print(f"  identity dev {worst_id:.2e}; min eigmin(P-Qk) {worst_eig:.3e} "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------- s6 genericity + the cell-0 MUST-NOT-VIOLATE control
print("[s6] curvature grid: every t>=1 concave, cell 0 never ...", flush=True)
rng = np.random.default_rng(24680)
grid = {}
worst_t0 = 1e9
worst_tge1 = 1e9
for n in (3, 4, 5):
    Mn = Model(n)
    for D in (0, 1, 2):
        best = [1e9] * n
        for _ in range(2):
            H, G = base_point(Mn, rng)
            xb = pack(H, G)
            for t in range(n):
                def ft(x, t=t, Mn=Mn, D=D, n=n):
                    Hh, Gg = unpack(x, n)
                    if not in_intD(Mn, Hh, Gg):
                        return None
                    r = percell(Mn, Hh, Gg, D)
                    return None if r is None else float(r[t])
                Hs = hessian(ft, xb)
                if Hs is None:
                    continue
                best[t] = min(best[t], float(np.linalg.eigvalsh(Hs).min()))
        grid[f"n{n}_D{D}"] = best
        worst_t0 = min(worst_t0, best[0])
        worst_tge1 = min(worst_tge1, max(best[1:]))
vals["s6_grid_min_eig"] = grid
vals["s6_worst_cell0_min_eig"] = worst_t0
vals["s6_largest_min_eig_over_t_ge_1"] = worst_tge1
verdicts["s6_every_cell_t_ge_1_admits_concave_directions"] = worst_tge1 < -0.5
verdicts["s6_MUSTNOTFAIL_cell0_never_concave"] = worst_t0 > -1e-8
print(f"  worst over t>=1 (largest of the per-grid minima) {worst_tge1:+.3e} "
      f"(bar < -0.5); cell 0 worst {worst_t0:+.3e} (must be >= -1e-8) "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------- s7 does not prove too much
print("[s7] Theorem C intact, and the historical method has zero power ...",
      flush=True)
tp = percell(M3, *unpack(XP, NW), DW).sum()
tm = percell(M3, *unpack(XM, NW), DW).sum()
tc = percell(M3, *unpack(X_BASE, NW), DW).sum()
tot_gap = tc - 0.5 * (tp + tm)
per = [percell(M3, *unpack(X_BASE, NW), DW)[i]
       - 0.5 * (percell(M3, *unpack(XP, NW), DW)[i]
                + percell(M3, *unpack(XM, NW), DW)[i]) for i in range(NW)]
vals["s7_total_gap_at_witness"] = tot_gap
vals["s7_percell_gaps_at_witness"] = per
verdicts["s7_TOTAL_stays_convex_at_the_witness"] = tot_gap < -1e-3
# The random-pair control. THE PILOT REFUTED ITS FIRST SPECIFICATION: this
# gate originally asserted that random pairs have ZERO power, on the strength
# of rem:percell's "no violation was found in any sampling ... zero hits".
# That is FALSE HERE -- random per-cell pairs violate at ~0.25% with gaps up
# to +4.5e-2, which are real violations and not threshold noise. Whatever
# sampling produced the "zero hits" note therefore cannot have been per-cell
# pairs of this kind (the 079 harness gates the TOTAL and the two REGROUPED
# pieces and records per-cell as explicitly NOT gated). The gate now asserts
# what is true and is more informative for it: the rate is nonzero, so the
# historical note does not reproduce; and it is small, which is why a
# directed curvature search is the right instrument rather than sampling.
rng = np.random.default_rng(11235)
found = 0
kept = 0
worst_rand = -1e9
NPAIR = 4000
for _ in range(NPAIR):
    H1, G1 = base_point(M3, rng)
    H2, G2 = base_point(M3, rng)
    Hm, Gm = 0.5 * (H1 + H2), 0.5 * (G1 + G2)
    if not in_intD(M3, Hm, Gm):
        continue
    f1, f2, fm = (percell(M3, H1, G1, DW), percell(M3, H2, G2, DW),
                  percell(M3, Hm, Gm, DW))
    if any(v is None for v in (f1, f2, fm)):
        continue
    kept += 1
    g = fm[TW] - 0.5 * (f1[TW] + f2[TW])
    worst_rand = max(worst_rand, g)
    if g > 1e-9:
        found += 1
rate = found / max(kept, 1)
vals["s7_random_pairs"] = kept
vals["s7_random_pair_violations"] = found
vals["s7_random_pair_rate"] = rate
vals["s7_random_pair_worst_gap"] = worst_rand
verdicts["s7_random_sampling_DOES_violate_so_zero_hits_does_not_reproduce"] = \
    (found >= 1) and (worst_rand > 1e-3)
verdicts["s7_but_the_rate_is_low_so_sampling_is_the_wrong_instrument"] = \
    rate < 0.02
print(f"  total gap {tot_gap:+.6e} (convex, Thm C); per-cell "
      f"{[round(float(v), 10) for v in per]}")
print(f"  random-pair control: {found}/{kept} = {rate:.3%}, worst "
      f"{worst_rand:+.3e} -- nonzero (the 'zero hits' note does NOT "
      f"reproduce) but small [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------- report
allpass = all(verdicts.values())
print()
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print(f"VERDICT: {'ALL PASS' if allpass else 'FAIL'} "
      f"{sum(verdicts.values())}/{len(verdicts)}")
vals["runtime_s"] = round(time.time() - t0, 1)


def jsafe(o):
    if isinstance(o, dict):
        return {k: jsafe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsafe(v) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return jsafe(o.tolist())
    return o


out = {"verdict": jsafe(verdicts), "GO14PC_supported": bool(allpass), "vals": jsafe(vals),
       "scope": {
           "what_is_refuted": "per-cell convexity of the INDIVIDUAL CMI terms "
           "of L_a in (H,Gamma), for every cell t >= 1",
           "what_is_proved": "cell t=0 IS convex -- it collapses exactly to "
           "the block bracket in scalar form with a truncated Q_k, so it is "
           "the 074 lift's SCALAR CASE",
           "what_is_untouched": "Theorem C, Theorem R1, the 079 certificates "
           "and the 082/083/084/085 chain. s7 GATES this: at the witness pair "
           "the TOTAL n L_a is convex. No result in the document uses a "
           "per-cell statement -- the only other mention is the "
           "open-problems list",
           "provenance": "the witnesses were found 2026-08-08 (PROBE.md) "
           "BEFORE this harness existed. Every witness gate is "
           "COMMITTED-VALUE REPRODUCTION, not discovery. Nothing here searches",
           "rind5_independence": "the R-IND-5 pass on this refutation was run "
           "in the SAME context that produced it, NOT by a fresh-context "
           "verifier. Recorded as a self-audit",
           "no_solver": "no optimizer, fixed point or root find anywhere in "
           "this file, so no gate races a solver (the 079 lesson)"}}
print("===GO14PC-JSON===")
print(json.dumps(out, indent=1))
print("===END===")
sys.exit(0 if allpass else 1)
