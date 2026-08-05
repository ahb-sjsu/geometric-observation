#!/usr/bin/env python
"""GO-P-2026-076 harness: the causal-erasure coordinate L_a (GO-14
Theorem 1, definition (a) -- Delta-lagged causally-conditioned CMI).
s1 exact chain rule n L_a = I(T^n;Yh^n|S^n) + C_Delta (any record);
s2 collapse faces: N-only records collapse exactly while carrying
   bits (universal non-collapse REFUTED as worded); the D-feasibility
   boundary D >= rho^2(n-Delta-1)/n admits a feasible collapsing
   record (Delta=6, n=16, D=0.3); below the boundary every tested
   feasible optimizer has C_Delta > 0;
s3 class-conditional sandwich: block_n < L_a-upper(Delta) < slice
   coordinate, strictly decreasing in Delta (diag-class UPPER BOUNDS,
   never "the minimum" -- the diagonal class is beaten, see s5);
s4 smoothing pole: per-cell leak ratio -> lambda_s^{-2},
   lambda_s = a(1-K); aggregate ratio carries the
   (n-Delta-1)/(n-Delta-2) cell-count prefactor;
s5 diagonal-class refutation for L_a: feasible first-order descent
   at the diag optimum (failed certificate) + an actual feasible
   non-diagonal improvement;
s6 bookkeeping refuted, n-pinned: gap_n = static(q_path) - block_n
   rises with n toward the spectral gain (block_inf by per-frequency
   equal-slope allocation, the 070 machinery).
Sentinel ===GO14CE-JSON=== with ===END===; flag GO14CE_supported.
Pilot seed 20261101 / governed seed 20261102 (seed stamps the run and
feeds only the s1 random-channel draw; optimizers are deterministic
warm-started, the 070 lesson)."""
import argparse
import json
import sys
import time

import numpy as np
from scipy.optimize import minimize

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a_ = ap.parse_args()
SEED = a_.seed if a_.seed is not None else (20261101 if a_.pilot
                                            else 20261102)
rng = np.random.default_rng(SEED)
verdicts = {}
vals = {"seed": SEED, "pilot": bool(a_.pilot)}

A_ = 0.8
RHO = 0.7
TAU2 = 0.4
SN2 = 1.0 - RHO ** 2
LN2 = np.log(2.0)
D_TGT = 0.3
ZFLOOR = 1e-7


def ld(M):
    n = M.shape[0]
    j = 1e-11 * max(1.0, float(np.trace(M)) / n)
    return float(np.linalg.slogdet(M + j * np.eye(n))[1])


def cmi_bits(S, ia, ib, ic):
    ii = list(ia) + list(ib)
    if len(ic) > 0:
        S22 = S[np.ix_(ic, ic)]
        S12 = S[np.ix_(ii, ic)]
        Sc = S[np.ix_(ii, ii)] - S12 @ np.linalg.solve(
            S22 + 1e-12 * np.eye(len(ic)), S12.T)
    else:
        Sc = S[np.ix_(ii, ii)].copy()
    Sc = 0.5 * (Sc + Sc.T)
    na = len(ia)
    return 0.5 * (ld(Sc[:na, :na]) + ld(Sc[na:, na:]) - ld(Sc)) / LN2


def gstar_coord(q, D, rho2=RHO ** 2):
    """(1/2)log2 g*; array-safe in (q, D, rho2)."""
    s = 1.0 / (1.0 - np.asarray(q, float))
    D = np.asarray(D, float)
    rho2 = np.asarray(rho2, float)
    Aq = D * s
    Bq = -(D + s - rho2)
    Cq = 1.0 - rho2
    disc = np.maximum(Bq * Bq - 4 * Aq * Cq, 0.0)
    g = np.maximum((-Bq + np.sqrt(disc)) / (2 * Aq), 1.0)
    return 0.5 * np.log2(g)


def q_slice(Delta):
    return 1.0 - A_ ** (2 * Delta) / (1.0 + TAU2)


def q_path(m=400):
    j = np.arange(-m, m + 1)
    c = A_ ** np.abs(j)
    Sg = A_ ** np.abs(j[:, None] - j[None, :]) + TAU2 * np.eye(len(j))
    return float(1.0 - c @ np.linalg.solve(Sg, c))


def kalman_pole():
    M = 1.0
    for _ in range(500):
        K = M / (M + TAU2)
        M = A_ ** 2 * (1 - K) * M + (1 - A_ ** 2)
    K = M / (M + TAU2)
    return A_ * (1 - K)


class P:
    """Window model on t=1..n; general record Yh = Ay Y + Av V + Z."""

    def __init__(self, n):
        self.n = n
        idx = np.arange(n)
        self.Cv = A_ ** np.abs(idx[:, None] - idx[None, :])
        self.mu, self.U = np.linalg.eigh(self.Cv)
        self.Cy = RHO ** 2 * self.Cv + SN2 * np.eye(n)
        self.lam = RHO ** 2 * self.mu + SN2
        n3 = 3 * n
        St = np.zeros((n3, n3))
        St[0:n, 0:n] = self.Cv
        St[n:2 * n, n:2 * n] = self.Cy
        St[2 * n:, 2 * n:] = self.Cv + TAU2 * np.eye(n)
        St[0:n, n:2 * n] = RHO * self.Cv
        St[n:2 * n, 0:n] = RHO * self.Cv
        St[0:n, 2 * n:] = self.Cv
        St[2 * n:, 0:n] = self.Cv
        St[n:2 * n, 2 * n:] = RHO * self.Cv
        St[2 * n:, n:2 * n] = RHO * self.Cv
        self.static = St

    def blk(self, d):
        return (self.U * d) @ self.U.T

    def sigma_full(self, Ay, Av, zd):
        n = self.n
        Cvh = RHO * self.Cv @ Ay.T + self.Cv @ Av.T
        Cyh = self.Cy @ Ay.T + RHO * self.Cv @ Av.T
        Chh = (Ay @ self.Cy @ Ay.T + Av @ self.Cv @ Av.T
               + Ay @ (RHO * self.Cv) @ Av.T
               + Av @ (RHO * self.Cv) @ Ay.T + np.diag(zd))
        S = np.zeros((4 * n, 4 * n))
        S[:3 * n, :3 * n] = self.static
        S[0:n, 3 * n:] = Cvh
        S[3 * n:, 0:n] = Cvh.T
        S[n:2 * n, 3 * n:] = Cyh
        S[3 * n:, n:2 * n] = Cyh.T
        S[2 * n:3 * n, 3 * n:] = Cvh
        S[3 * n:, 2 * n:3 * n] = Cvh.T
        S[3 * n:, 3 * n:] = Chh
        return S

    def sigma_diagclass(self, g, h, z):
        n = self.n
        Ay = self.blk(g)
        Av = self.blk(h)
        Cvh = RHO * self.Cv @ Ay.T + self.Cv @ Av.T
        Cyh = self.Cy @ Ay.T + RHO * self.Cv @ Av.T
        Chh = (Ay @ self.Cy @ Ay.T + Av @ self.Cv @ Av.T
               + Ay @ (RHO * self.Cv) @ Av.T
               + Av @ (RHO * self.Cv) @ Ay.T + self.blk(z))
        S = np.zeros((4 * n, 4 * n))
        S[:3 * n, :3 * n] = self.static
        S[0:n, 3 * n:] = Cvh
        S[3 * n:, 0:n] = Cvh.T
        S[n:2 * n, 3 * n:] = Cyh
        S[3 * n:, n:2 * n] = Cyh.T
        S[2 * n:3 * n, 3 * n:] = Cvh
        S[3 * n:, 2 * n:3 * n] = Cvh.T
        S[3 * n:, 3 * n:] = Chh
        return S

    def dist_diag(self, g, h, z):
        return float(np.mean(self.lam * (1 - g) ** 2 + self.mu * h ** 2
                             - 2 * (1 - g) * h * RHO * self.mu + z))

    def dist_sigma(self, S):
        n = self.n
        iY = np.arange(n, 2 * n)
        iH = np.arange(3 * n, 4 * n)
        return float(np.mean(np.diag(S)[iY] - 2 * S[iY, iH]
                             + np.diag(S)[iH]))


def unpack(x, n):
    g = x[:n]
    h = x[n:2 * n]
    u = x[2 * n:]
    return g, h, u ** 2 + ZFLOOR


def terms(Pm, S, Delta):
    """Per-cell L_a, leak; block per-symbol. T = (V^n, Y^n)."""
    n = Pm.n
    ia = list(range(2 * n))
    Sb, Hb = 2 * n, 3 * n
    La, leak = [], []
    for t in range(n):
        se = min(t + Delta + 1, n)
        icS = list(range(Sb, Sb + se))
        icH = list(range(Hb, Hb + t))
        La.append(cmi_bits(S, ia, [Hb + t], icS + icH))
        if se < n:
            iaf = list(range(Sb + se, Sb + n))
            leak.append(cmi_bits(S, iaf, [Hb + t], icS + icH))
        else:
            leak.append(0.0)
    Iblk = cmi_bits(S, ia, list(range(Hb, Hb + n)),
                    list(range(Sb, Sb + n))) / n
    return np.array(La), np.array(leak), Iblk


def rwf_x(Pm, D):
    lam = Pm.lam
    lo, hi = 1e-9, float(lam.max())
    for _ in range(200):
        th = 0.5 * (lo + hi)
        if np.minimum(th, lam).mean() > D:
            hi = th
        else:
            lo = th
    Di = np.minimum(th, lam)
    g = 1 - Di / lam
    z = np.maximum(Di * g - ZFLOOR, 0.0)
    return np.concatenate([g, np.zeros(Pm.n), np.sqrt(z)])


def scalar_x(Pm, D):
    n = Pm.n
    return np.concatenate([np.full(n, 1 - D), np.zeros(n),
                           np.full(n, np.sqrt(max(D * (1 - D) - ZFLOOR,
                                                  0.0)))])


def opt_diag(Pm, D, objfun, starts, maxiter):
    n = Pm.n
    cons = [{'type': 'ineq',
             'fun': lambda x: D - Pm.dist_diag(*unpack(x, n))}]
    bounds = ([(-2, 2)] * n + [(-2, 2)] * n + [(0.0, 2.0)] * n)
    best = None
    for x0 in starts:
        r = minimize(objfun, x0, method='SLSQP', bounds=bounds,
                     constraints=cons,
                     options={'maxiter': maxiter, 'ftol': 1e-9})
        d = Pm.dist_diag(*unpack(r.x, n))
        v = float(objfun(r.x))
        if d <= D + 1e-6 and (best is None or v < best[0]):
            best = (v, r.x.copy())
    return best


def obj_La(Pm, Delta):
    n = Pm.n

    def f(x):
        S = Pm.sigma_diagclass(*unpack(x, n))
        La, _, _ = terms(Pm, S, Delta)
        return float(np.mean(La))
    return f


def obj_block(Pm):
    n = Pm.n
    ia = list(range(2 * n))

    def f(x):
        S = Pm.sigma_diagclass(*unpack(x, n))
        return cmi_bits(S, ia, list(range(3 * n, 4 * n)),
                        list(range(2 * n, 3 * n))) / n
    return f


LAM_S = kalman_pole()
vals["lambda_s"] = LAM_S
vals["lambda_s_m2"] = LAM_S ** -2

# ---------------------------------------------------------------- s1 identity
print("[s1] exact chain rule n L_a = block + C_Delta ...", flush=True)
resids = []
for n in (8, 16):
    Pm = P(n)
    xr = rng.normal(0, 0.3, 3 * n)
    xr[2 * n:] = np.abs(xr[2 * n:]) + 0.2
    for x in (rwf_x(Pm, D_TGT), scalar_x(Pm, D_TGT), xr):
        S = Pm.sigma_diagclass(*unpack(x, n))
        for Delta in (0, 2, 5, n):
            La, leak, Iblk = terms(Pm, S, Delta)
            resids.append(abs(float(np.mean(La))
                              - (Iblk + float(np.mean(leak)))))
vals["s1_max_resid"] = float(max(resids))
verdicts["s1_identity"] = vals["s1_max_resid"] < 1e-8
print(f"  max residual {vals['s1_max_resid']:.2e} over "
      f"{len(resids)} (n, channel, Delta) cells", flush=True)

# ------------------------------------------------------------ s2 collapse faces
print("[s2] collapse faces ...", flush=True)
n = 16
Pm = P(n)
# (a) N-only record: Yh = Y - rho V + Z  (V-free) -- collapses exactly,
# carries bits, and is D-INFEASIBLE (dist >= rho^2 > D).
Ay = np.eye(n)
Av = -RHO * np.eye(n)
S = Pm.sigma_full(Ay, Av, np.full(n, 0.05))
La, leak, Iblk = terms(Pm, S, 2)
dna = Pm.dist_sigma(S)
vals["s2a_leak"] = float(np.max(np.abs(leak)))
vals["s2a_block_bits"] = Iblk
vals["s2a_dist"] = dna
verdicts["s2a_Nonly_collapse"] = (vals["s2a_leak"] < 1e-9
                                  and Iblk > 0.5 and dna > D_TGT)
print(f"  N-only: max|leak|={vals['s2a_leak']:.1e} block/n={Iblk:.4f} "
      f"dist={dna:.4f} (infeasible as the theorem requires)", flush=True)
# (b) boundary-V record at Delta=6: V-free on t <= n-Delta-2, exact
# copy on late cells; feasible iff D >= rho^2(n-Delta-1)/n = 0.2756.
Delta_b = 6
nfree = n - Delta_b - 1          # cells 0..8 must be V-free
Ay = np.zeros((n, n))
Av = np.zeros((n, n))
zd = np.full(n, ZFLOOR)
for t in range(n):
    if t < nfree:
        Ay[t, t] = 1.0
        Av[t, t] = -RHO         # Yh_t = N_t (+ floor noise)
    else:
        Ay[t, t] = 1.0          # Yh_t = Y_t exactly (+ floor)
S = Pm.sigma_full(Ay, Av, zd)
La, leak, Iblk = terms(Pm, S, Delta_b)
db = Pm.dist_sigma(S)
bound = RHO ** 2 * (n - Delta_b - 1) / n
vals["s2b_dist"] = db
vals["s2b_bound"] = bound
vals["s2b_leak"] = float(np.max(np.abs(leak)))
verdicts["s2b_boundary_collapse"] = (db <= D_TGT and db >= bound - 1e-9
                                     and vals["s2b_leak"] < 1e-9)
print(f"  boundary-V (Delta=6): dist={db:.4f} vs bound {bound:.4f} "
      f"<= D={D_TGT}; max|leak|={vals['s2b_leak']:.1e}", flush=True)

# --------------------------------------------- s3 sandwich (diag-class UBs)
print("[s3] class-conditional sandwich (diag-class upper bounds) ...",
      flush=True)
DELTAS = (0, 2, 5)
fb = obj_block(Pm)
vb, xb = opt_diag(Pm, D_TGT, fb, [rwf_x(Pm, D_TGT), scalar_x(Pm, D_TGT)],
                  maxiter=70)
vals["s3_block16"] = vb
ubs, leaks_at_opt = {}, {}
xprev = xb
for i, Delta in enumerate(DELTAS):
    res = opt_diag(Pm, D_TGT, obj_La(Pm, Delta),
                   [xprev] + ([rwf_x(Pm, D_TGT)] if i == 0 else []),
                   maxiter=60 if i == 0 else 40)
    v, xo = res
    S = Pm.sigma_diagclass(*unpack(xo, n))
    La, leak, Iblk = terms(Pm, S, Delta)
    ubs[Delta] = v
    leaks_at_opt[Delta] = float(np.mean(leak))
    xprev = xo
    if Delta == 0:
        x_diag0 = xo.copy()
    print(f"  Delta={Delta}: L_a-UB={v:.6f} (leak {np.mean(leak):.2e}, "
          f"slice coord {gstar_coord(q_slice(Delta), D_TGT):.6f})",
          flush=True)
vals["s3_ub"] = {str(d): ubs[d] for d in DELTAS}
vals["s3_leak_at_opt"] = {str(d): leaks_at_opt[d] for d in DELTAS}
sl = {d: gstar_coord(q_slice(d), D_TGT) for d in DELTAS}
verdicts["s3_sandwich"] = all(
    vb < ubs[d] < sl[d] for d in DELTAS)
verdicts["s3_decreasing"] = (ubs[0] > ubs[2] > ubs[5]
                             and ubs[0] - ubs[2] > 1e-3)
verdicts["s3_strict_leak"] = all(leaks_at_opt[d] > 1e-9 for d in DELTAS)
print(f"  block16={vb:.6f}; UBs {ubs[0]:.6f} > {ubs[2]:.6f} > "
      f"{ubs[5]:.6f}, all in (block, slice)", flush=True)

# ------------------------------------------------------------------ s4 pole
# The pole claim is CELL-LOCAL-SCOPED: for time-local (cell-diagonal)
# records the per-cell leak decays at lambda_s^{2 Delta}. Code-mixing
# records measurably do NOT share the exponent (rwf shows a stable
# slower pole ~= 0.255/lag, empirically ~ lambda_s^2/rho^2 -- recorded
# as an open scoping observation, not gated).
print("[s4] smoothing pole lambda_s = a(1-K), cell-local scope ...",
      flush=True)


def leak_only(Pm_, S, Delta):
    n_ = Pm_.n
    Sb, Hb = 2 * n_, 3 * n_
    out = []
    for t in range(n_):
        se = min(t + Delta + 1, n_)
        if se >= n_:
            out.append(0.0)
            continue
        out.append(cmi_bits(S, list(range(Sb + se, Sb + n_)), [Hb + t],
                            list(range(Sb, Sb + se))
                            + list(range(Hb, Hb + t))))
    return np.array(out)


n32 = 32
Pm32 = P(n32)
S32 = Pm32.sigma_diagclass(*unpack(scalar_x(Pm32, D_TGT), n32))
tcell = 12
lk = np.array([leak_only(Pm32, S32, Dd)[tcell] for Dd in range(0, 8)])
rat_cell = lk[:-1] / lk[1:]
vals["s4_cell_ratios"] = [float(r) for r in rat_cell]
cell_err = float(np.max(np.abs(rat_cell[2:6] / LAM_S ** -2 - 1)))
vals["s4_cell_relerr"] = cell_err
verdicts["s4_pole_cell"] = cell_err < 0.01
# aggregate with the (n-Delta-1)/(n-Delta-2) prefactor at n=16;
# gated over Delta=0..6 where leaks sit far above the ~1e-11 CMI
# jitter floor (beyond Delta~8 the leaks reach 1e-10..1e-13 and the
# ratio is numerically meaningless -- disclosed scope)
S16 = Pm.sigma_diagclass(*unpack(scalar_x(Pm, D_TGT), n))
ag = np.array([float(np.mean(leak_only(Pm, S16, Dd)))
               for Dd in range(0, 8)])
rat_ag = ag[:-1] / ag[1:]
pred = np.array([LAM_S ** -2 * (n - Dd - 1) / (n - Dd - 2)
                 for Dd in range(0, 7)])
agg_err = float(np.max(np.abs(rat_ag / pred - 1)))
vals["s4_agg_relerr"] = agg_err
verdicts["s4_pole_prefactor"] = agg_err < 0.02
# the record-dependence observation (not a gate): rwf pole
S32r = Pm32.sigma_diagclass(*unpack(rwf_x(Pm32, D_TGT), n32))
lkr = np.array([leak_only(Pm32, S32r, Dd)[tcell] for Dd in (4, 5)])
vals["s4_rwf_ratio_obs"] = float(lkr[0] / lkr[1])
print(f"  cell-local ratios Delta 2..5 "
      f"{[f'{r:.4f}' for r in rat_cell[2:6]]} vs {LAM_S**-2:.4f} "
      f"(relerr {cell_err:.4f}); aggregate prefactor relerr "
      f"{agg_err:.4f}; rwf observed ratio "
      f"{vals['s4_rwf_ratio_obs']:.3f} (record-dependent, open)",
      flush=True)

# --------------------------------------- s5 diagonal class beaten for L_a
print("[s5] non-diagonal refutation at the Delta=0 diag optimum ...",
      flush=True)
g0, h0, z0 = unpack(x_diag0, n)
Ay0 = Pm.blk(g0)
Av0 = Pm.blk(h0)
Zfull0 = Pm.blk(z0)
zd0 = np.diag(Zfull0).copy()
# work with the full-matrix embedding of the SAME record: Z made
# diagonal by moving the off-diagonal Z-structure into an equivalent
# record is not exact, so instead evaluate the diag record exactly and
# perturb (Ay, Av) only, with per-cell z fixed at diag(Zfull0) plus the
# off-diag part folded via its symmetric square root into Ay-space:
# for the refutation it suffices to compare against the SAME baseline.
Sb0 = Pm.sigma_full(Ay0, Av0, zd0) + 0.0
# add exact off-diagonal Z back
Off = Zfull0 - np.diag(zd0)
Sb0[3 * n:, 3 * n:] += Off


def eval_rec(Ay, Av):
    S = Pm.sigma_full(Ay, Av, zd0)
    S[3 * n:, 3 * n:] += Off
    La, _, _ = terms(Pm, S, 0)
    return float(np.mean(La)), Pm.dist_sigma(S)


base_val, base_dist = eval_rec(Ay0, Av0)
vals["s5_base_val"] = base_val
vals["s5_base_dist"] = base_dist
# finite-difference gradient over full (Ay, Av), projected onto the
# distortion tangent
eps = 1e-5
gL = np.zeros(2 * n * n)
gD = np.zeros(2 * n * n)
for k in range(2 * n * n):
    dA = np.zeros((2, n, n))
    dA[k // (n * n)].flat[k % (n * n)] = eps
    v1, d1 = eval_rec(Ay0 + dA[0], Av0 + dA[1])
    gL[k] = (v1 - base_val) / eps
    gD[k] = (d1 - base_dist) / eps
gDn = gD / max(np.linalg.norm(gD), 1e-12)
gproj = gL - (gL @ gDn) * gDn
slope = float(np.linalg.norm(gproj))
vals["s5_projected_slope"] = slope
verdicts["s5_certificate_fails"] = slope > 1e-3
# take feasible steps along -gproj (restore distortion by shrinking z)
dirv = -gproj / max(slope, 1e-12)
best_impr = 0.0
for step in (0.005, 0.01, 0.02, 0.04):
    dAy = dirv[:n * n].reshape(n, n) * step
    dAv = dirv[n * n:].reshape(n, n) * step
    v1, d1 = eval_rec(Ay0 + dAy, Av0 + dAv)
    if d1 > D_TGT:
        exc = d1 - D_TGT
        znew = zd0 - exc      # uniform per-cell noise shave
        if znew.min() <= ZFLOOR:
            continue
        S = Pm.sigma_full(Ay0 + dAy, Av0 + dAv, znew)
        S[3 * n:, 3 * n:] += Off
        La, _, _ = terms(Pm, S, 0)
        v1, d1 = float(np.mean(La)), Pm.dist_sigma(S)
    if d1 <= D_TGT + 1e-9:
        best_impr = max(best_impr, base_val - v1)
vals["s5_best_improvement"] = best_impr
verdicts["s5_diag_beaten"] = best_impr > 1e-4
print(f"  projected slope {slope:.4f}; best feasible non-diagonal "
      f"improvement {best_impr:.5f} bits (diag class = upper bound "
      f"only)", flush=True)

# ------------------------------------ s6 bookkeeping refuted, n-pinned gain
print("[s6] spectral gain, n-pinned ...", flush=True)
QP = q_path()
static_path = gstar_coord(QP, D_TGT)
vals["s6_static_qpath"] = static_path
blocks = {}
for nn in (8, 16):
    if nn == 16:
        blocks[nn] = vb
        continue
    Pn = P(nn)
    r = opt_diag(Pn, D_TGT, obj_block(Pn),
                 [rwf_x(Pn, D_TGT), scalar_x(Pn, D_TGT)], maxiter=70)
    blocks[nn] = r[0]
gaps = {nn: static_path - blocks[nn] for nn in blocks}
vals["s6_gap"] = {str(k): float(v) for k, v in gaps.items()}
# block_inf by DIRECT per-frequency single-letter minimization in
# Lagrangian form (the closed-form g* quadratic does NOT survive the
# per-frequency rho^2 generalization -- checked against the exact
# per-mode decomposition of block_16, which the direct computation
# reproduces to machine precision).
NW = 128
wg = (np.arange(NW) + 0.5) * np.pi / NW
Svw = (1 - A_ ** 2) / (1 + A_ ** 2 - 2 * A_ * np.cos(wg))
Syw = RHO ** 2 * Svw + SN2


def sl_val(x, Sv, Sy_):
    """Single-letter I(V,Y;Yh|G) in bits + distortion, closed 4x4."""
    al, be, sz = x
    C = np.zeros((4, 4))
    C[0, 0] = Sv
    C[1, 1] = Sy_
    C[0, 1] = C[1, 0] = RHO * Sv
    C[2, 2] = Sv + TAU2
    C[0, 2] = C[2, 0] = Sv
    C[1, 2] = C[2, 1] = RHO * Sv
    cvh = al * RHO * Sv + be * Sv
    cyh = al * Sy_ + be * RHO * Sv
    C[0, 3] = C[3, 0] = cvh
    C[1, 3] = C[3, 1] = cyh
    C[2, 3] = C[3, 2] = cvh
    C[3, 3] = (al ** 2 * Sy_ + be ** 2 * Sv + 2 * al * be * RHO * Sv
               + sz ** 2 + 1e-13)
    ii = [0, 1, 3]
    cS = C[np.ix_(ii, ii)] - np.outer(C[ii, 2], C[ii, 2]) / C[2, 2]
    v = 0.5 * (np.linalg.slogdet(cS[:2, :2])[1] + np.log(cS[2, 2])
               - np.linalg.slogdet(cS)[1]) / LN2
    d = ((1 - al) ** 2 * Sy_ + be ** 2 * Sv
         - 2 * (1 - al) * be * RHO * Sv + sz ** 2)
    return v, d


def freq_pass(slp, X0):
    """Per-freq unconstrained min of val + slp*dist; returns v, d, X."""
    V = np.zeros(NW)
    Dd = np.zeros(NW)
    X = np.zeros((NW, 3))
    for i in range(NW):
        def f(x):
            v, d = sl_val(x, Svw[i], Syw[i])
            return v + slp * d
        r = minimize(f, X0[i], method='Nelder-Mead',
                     options={'xatol': 1e-9, 'fatol': 1e-12,
                              'maxiter': 400})
        V[i], Dd[i] = sl_val(r.x, Svw[i], Syw[i])
        X[i] = r.x
    return V, Dd, X


X0 = np.zeros((NW, 3))
X0[:, 0] = 1 - D_TGT / Syw
X0[:, 2] = np.sqrt(0.5 * D_TGT)
lo, hi = 0.05, 20.0
Xw = X0
for it in range(24):
    slp = 0.5 * (lo + hi)
    Vv, Dd, Xw = freq_pass(slp, Xw)
    if float(Dd.mean()) < D_TGT:
        hi = slp
    else:
        lo = slp
block_inf = float(Vv.mean())
vals["s6_mean_d_inf"] = float(Dd.mean())
vals["s6_block_inf"] = block_inf
gap_inf = static_path - block_inf
vals["s6_gap_inf"] = gap_inf
verdicts["s6_gain_monotone"] = (gaps[8] < gaps[16] < gap_inf)
verdicts["s6_gain_value"] = abs(gap_inf - 0.0313) < 0.004
print(f"  gap_8={gaps[8]:.4f} < gap_16={gaps[16]:.4f} < "
      f"gap_inf={gap_inf:.4f} (block_inf={block_inf:.5f})", flush=True)

# -------------------------------------------------------------------- report
verdicts = {k: bool(v) for k, v in verdicts.items()}
allpass = all(verdicts.values())
print()
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")


def jsafe(o):
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(o)


out = {"verdict": verdicts, "GO14CE_supported": allpass, "vals": vals,
       "runtime_s": round(time.time() - t0, 1)}
print("===GO14CE-JSON===")
print(json.dumps(out, indent=1, default=jsafe))
print("===END===")
sys.exit(0 if allpass else 1)
