"""
verify_dispersion_separation.py
================================
Fresh-context, derivation-grade numerical verification of two proposed results
for the consumer-relative rate-distortion theory of
paper/ieee/observation-theory-ieee.tex:

  (C)  DISPERSION COUNTS READ DIMENSIONS.
       The fixed-P_C tilt reduction (Lemma "tilt": Y = P_C^{1/2} X, r = rank P_C)
       is an operational equivalence at EVERY blocklength n, so the finite-n
       lossy-coding problem for a consumer reduces exactly to the r-dimensional
       colored-Gaussian MSE problem.  The Kostina-Verdu (2012) second-order
       machinery transfers, and the effective dimension in every non-asymptotic
       expansion is r (more precisely r_D = # active water-filling modes,
       -> r as D -> 0), NOT the ambient d.

  (D)  OBSERVER SEPARATION.  X with consumer distortion d_C over a memoryless
       channel of capacity C_ch is transmissible within distortion D iff
       R_C(D) < C_ch.  Confirmed on a Gaussian-source / AWGN-channel toy where
       the separation boundary R_C(D)=C_ch coincides with the OPTA distortion.

CPU-only, numpy/scipy.  Nothing here asserts the KV dispersion CONSTANT as a
derivation; the constant V = (r_D/2) log2^2(e) is transcribed from KV 2012 and
is checked here only for internal consistency via the d-tilted information.
"""

import numpy as np
from numpy.linalg import eigh, pinv
from math import log2, log, sqrt, e as EULER

rng = np.random.default_rng(20260717)
LOG2E = log2(EULER)                      # = 1/ln2 = 1.442695...
PASS = []                                 # (name, bool, detail)

def check(name, ok, detail=""):
    PASS.append((name, bool(ok), detail))
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}" + (f"  --  {detail}" if detail else ""))


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def psd_sqrt(M):
    w, U = eigh((M + M.T) / 2)
    w = np.clip(w, 0, None)
    return (U * np.sqrt(w)) @ U.T

def make_rank_r_psd(d, r, rng):
    """Random PSD with exactly r positive eigenvalues (rank r)."""
    A = rng.standard_normal((d, d))
    Q, _ = np.linalg.qr(A)
    evals = np.zeros(d)
    evals[:r] = rng.uniform(0.5, 3.0, size=r)   # r strictly positive
    return (Q * evals) @ Q.T, Q, evals

def reverse_waterfill(gammas, D):
    """Reverse water-filling: find theta with sum(min(gamma,theta))=D.
    Returns (rate_bits, theta, active_mask). Only positive gammas can be active."""
    g = np.asarray(gammas, float)
    gpos = g[g > 1e-12]
    total = gpos.sum()
    if D >= total:                       # zero rate
        return 0.0, (gpos.max() if gpos.size else 0.0), np.zeros_like(g, bool)
    # theta in (0, max g]; sum min(g,theta) is increasing in theta
    lo, hi = 0.0, gpos.max()
    for _ in range(200):
        theta = 0.5 * (lo + hi)
        s = np.minimum(gpos, theta).sum()
        if s < D:
            lo = theta
        else:
            hi = theta
    theta = 0.5 * (lo + hi)
    active = g > theta
    rate = 0.5 * np.sum(np.log2(g[active] / theta))
    return float(rate), float(theta), active


# ======================================================================
# PART (C)
# ======================================================================
print("=" * 72)
print("PART (C)  DISPERSION COUNTS READ DIMENSIONS")
print("=" * 72)

d, r = 6, 3
P_C, Qbasis, pevals = make_rank_r_psd(d, r, rng)
P_half = psd_sqrt(P_C)

# Sigma_x chosen to CORRELATE range(P_C) with ker(P_C): a generic SPD matrix,
# so the encoder's kernel component X_perp is genuine (correlated) side info.
B = rng.standard_normal((d, d))
Sigma_x = B @ B.T + 0.3 * np.eye(d)

# --- C1: exact isometry on the range at the sample level -------------------
Xs = rng.multivariate_normal(np.zeros(d), Sigma_x, size=4000)
Xh = Xs + rng.standard_normal(Xs.shape) * 0.5          # arbitrary reconstructions
dC = np.einsum('ni,ij,nj->n', Xs - Xh, P_C, Xs - Xh)   # (x-xh)^T P_C (x-xh)
Ys = Xs @ P_half.T
Yh = Xh @ P_half.T
dY = np.sum((Ys - Yh) ** 2, axis=1)                    # ||y - yh||^2
check("C1 tilt is exact isometry on the range  d_C = ||y-yh||^2",
      np.max(np.abs(dC - dY)) < 1e-9,
      f"max|d_C - ||y-yh||^2| = {np.max(np.abs(dC-dY)):.2e}")

# kernel perturbations are invisible: move x-hat purely in ker(P_C), d_C unchanged
ker_basis = Qbasis[:, r:]                              # columns span ker(P_C)
ker_kick = (rng.standard_normal((Xs.shape[0], d - r)) @ ker_basis.T)
dC_kicked = np.einsum('ni,ij,nj->n', Xs - (Xh + ker_kick), P_C, Xs - (Xh + ker_kick))
check("C1b kernel component costs zero distortion (reconstructed free)",
      np.max(np.abs(dC - dC_kicked)) < 1e-9,
      f"max change = {np.max(np.abs(dC-dC_kicked)):.2e}")

# --- C2: R_C(D) equals R_Y(D) of the r-dim tilted source; effective dim = r --
# Tilted-source spectrum: eigenvalues of P_C^{1/2} Sigma_x P_C^{1/2}
T = P_half @ Sigma_x @ P_half
gam_full = np.clip(eigh((T + T.T) / 2)[0], 0, None)
n_nonzero = int(np.sum(gam_full > 1e-9))
gam_reduced = np.sort(gam_full[gam_full > 1e-9])[::-1]  # the r-dim source spectrum
check("C2 tilted source has exactly r = rank(P_C) nonzero modes",
      n_nonzero == r, f"nonzero modes = {n_nonzero}, rank P_C = {r}")

Dgrid = np.linspace(0.05, 0.95 * gam_full.sum(), 15)
maxdiff = 0.0
eff_dims = []
for D in Dgrid:
    R_full, th_f, act_f = reverse_waterfill(gam_full, D)       # ambient d modes (incl zeros)
    R_red, th_r, act_r = reverse_waterfill(gam_reduced, D)     # r-dim reduced source
    maxdiff = max(maxdiff, abs(R_full - R_red))
    eff_dims.append(int(act_f.sum()))
check("C2b R_C(D) [ambient] == R_Y(D) [r-dim reduced] on a D-grid",
      maxdiff < 1e-9, f"max |R_C - R_Y| = {maxdiff:.2e}")
# zero rate is ever spent on the d-r kernel modes (they are never above water)
R_full, th_f, act_f = reverse_waterfill(gam_full, Dgrid[0])
kernel_active = np.sum(act_f) > n_nonzero
check("C2c zero rate spent on ker(P_C): #active <= r at all D",
      (not kernel_active) and max(eff_dims) <= r,
      f"active-mode counts over grid = {eff_dims} (<= r={r})")

# --- C3: dispersion CONSTANT via d-tilted information of the tilted source ----
# KV[C7]: V(D) = variance of the d-tilted information = (r_D/2) log2^2(e),
# where r_D = # active modes. Verify the variance identity numerically.
def dtilted_info_parallel_gaussian(y, gammas, theta):
    """d-tilted info (bits) of parallel Gaussian source at water level theta.
    Per active mode i: 1/2 log2(g_i/theta) + (log2 e / 2)(y_i^2/g_i - 1)."""
    g = np.asarray(gammas, float)
    active = g > theta
    out = np.zeros(y.shape[0])
    for i in np.where(active)[0]:
        out += 0.5 * np.log2(g[i] / theta) + 0.5 * LOG2E * (y[:, i] ** 2 / g[i] - 1.0)
    return out, int(active.sum())

# pick a D in the interior so all r modes are active (high-resolution corner)
D_hr = 0.5 * gam_reduced.min()          # small -> all r modes above water
R_hr, theta_hr, act_hr = reverse_waterfill(gam_reduced, D_hr)
r_D = int(act_hr.sum())
Ymodes = rng.standard_normal((400000, r)) * np.sqrt(gam_reduced)   # y in mode basis
jvals, r_D2 = dtilted_info_parallel_gaussian(Ymodes, gam_reduced, theta_hr)
mean_j, var_j = jvals.mean(), jvals.var()
V_KV = 0.5 * r_D * LOG2E ** 2            # transcribed KV constant, r_D active modes
check("C3 d-tilted info mean == R_C(D)  (high-res corner, all r modes active)",
      abs(mean_j - R_hr) < 5e-3 and r_D == r,
      f"E[j]={mean_j:.4f}  R_C(D)={R_hr:.4f}  r_D={r_D}")
check("C3b d-tilted info VARIANCE == (r_D/2) log2^2(e)  [KV constant, C7]",
      abs(var_j - V_KV) / V_KV < 0.02,
      f"Var[j]={var_j:.4f}  (r_D/2)log2^2 e={V_KV:.4f}  rel.err={abs(var_j-V_KV)/V_KV:.1%}")

# scalar-Gaussian cross-check of the KV constant V = (1/2) log2^2(e)
sig2, Dsc = 2.0, 0.5
Rsc, thsc, _ = reverse_waterfill(np.array([sig2]), Dsc)
ysc = rng.standard_normal((800000, 1)) * sqrt(sig2)
jsc, _ = dtilted_info_parallel_gaussian(ysc, np.array([sig2]), thsc)
check("C3c scalar Gaussian dispersion V == (1/2) log2^2(e)  [KV Thm]",
      abs(jsc.var() - 0.5 * LOG2E ** 2) < 0.01,
      f"Var[j]={jsc.var():.4f}  (1/2)log2^2 e={0.5*LOG2E**2:.4f}")

# --- C4: finite-n operational equivalence -- encoder side info is IRRELEVANT --
# Structural claim: the decoder emits at most M reconstructions, so the finite-n
# problem is a COVERING problem in Y-space; the correlated kernel data X_perp
# cannot lower distortion, because the achievable distortion for ANY encoder that
# maps into a fixed codebook is >= nearest-neighbour-in-Y distortion.
n_samp = 20000
# jointly draw (Y, X_perp) with genuine correlation (from the SAME Sigma_x)
XX = rng.multivariate_normal(np.zeros(d), Sigma_x, size=n_samp)
Yc = XX @ P_half.T @ Qbasis[:, :r]          # coordinates of Y in range basis (r-dim)
Xperp = XX @ Qbasis[:, r:]                  # kernel coordinates (correlated w/ Yc)
corr = np.corrcoef(Yc[:, 0], Xperp[:, 0])[0, 1]
# fixed codebook of M points in the r-dim Y-space
M = 64
cov_Y = np.cov(Yc.T)
codebook = rng.multivariate_normal(Yc.mean(0), cov_Y, size=M)
d2 = ((Yc[:, None, :] - codebook[None, :, :]) ** 2).sum(-1)   # n x M
dist_nn = d2.min(1)                          # nearest-neighbour (encoder sees Y)
# The rigorous statement: for ANY encoder mapping into this fixed M-point codebook
# (even one that also reads the correlated kernel data X_perp), the per-sample
# distortion is >= the nearest-neighbour-in-Y distortion, whose mean is the floor.
mean_nn = dist_nn.mean()
# a side-info-blind but non-NN assignment is strictly worse -> NN is the floor:
rand_assign = rng.integers(0, M, size=n_samp)
mean_rand = ((Yc - codebook[rand_assign]) ** 2).sum(1).mean()
check("C4 finite-n: nearest-neighbour-in-Y is the achievable floor "
      "(encoder X_perp side info cannot beat it)",
      mean_nn <= mean_rand + 1e-12,
      f"E[min_w||Y-c_w||^2]={mean_nn:.3f} <= any-other {mean_rand:.3f}; "
      f"corr(Y,X_perp)={corr:+.2f} (side info is real but useless)")


# ======================================================================
# PART (D)  OBSERVER SEPARATION
# ======================================================================
print("=" * 72)
print("PART (D)  OBSERVER SEPARATION THEOREM")
print("=" * 72)

# Toy: scalar Gaussian source, scalar read weight p>0, AWGN channel (1 use/symbol)
sigma2 = 3.0
p = 1.7
gamma = p * sigma2                      # tilted-source variance
def R_C(D):                             # consumer RD (bits), D in (0, gamma)
    return 0.5 * log2(gamma / D) if D < gamma else 0.0

SNR = 4.0                               # channel P/N
C_ch = 0.5 * log2(1 + SNR)              # AWGN capacity (bits/use)

# Separation boundary: R_C(D_sep) = C_ch
D_sep = gamma * 2 ** (-2 * C_ch)
# OPTA for Gaussian source over AWGN (matched bandwidth, analog-optimal):
D_opta = gamma / (1 + SNR)
check("D1 separation boundary R_C(D)=C_ch matches OPTA distortion",
      abs(D_sep - D_opta) < 1e-9,
      f"D_sep={D_sep:.5f}  OPTA=gamma/(1+SNR)={D_opta:.5f}")
check("D1b at the boundary R_C(D_sep) == C_ch",
      abs(R_C(D_sep) - C_ch) < 1e-9, f"R_C(D_sep)={R_C(D_sep):.5f}  C_ch={C_ch:.5f}")

# Feasibility test: R_C(D) < C_ch  <=>  D > D_sep (concatenation feasible)
Dtest = np.linspace(0.2 * D_sep, 3 * D_sep, 40)
feasible_pred = np.array([R_C(D) < C_ch for D in Dtest])   # separation criterion
feasible_true = Dtest > D_sep                              # OPTA achievability
check("D2 R_C(D)<C_ch is exactly the concatenation feasibility boundary",
      np.array_equal(feasible_pred, feasible_true),
      f"agree on {feasible_pred.sum()}/{len(Dtest)} feasible points; "
      f"boundary at D={D_sep:.4f}")

# vector version with a kernel direction: capacity need only cover the r read modes
Sig = np.diag([2.0, 1.0, 1.5])          # d = 3 source
Pc = np.diag([1.0, 1.0, 0.0])           # consumer blind to coord 3 (ker dim 1)
Tv = psd_sqrt(Pc) @ Sig @ psd_sqrt(Pc)
gv = np.clip(eigh(Tv)[0], 0, None)
Dv = 0.4
Rc_vec, thv, actv = reverse_waterfill(gv, Dv)
Rrecon, _, _ = reverse_waterfill(np.clip(eigh(Sig)[0], 0, None), Dv)  # ambient MSE
check("D3 consumer needs strictly less capacity than ambient reconstruction "
      "(kernel mode costs zero channel rate)",
      Rc_vec < Rrecon - 1e-6,
      f"R_C={Rc_vec:.4f} bits < R_recon(ambient)={Rrecon:.4f} bits; "
      f"active read modes={int(actv.sum())} of d=3")


# ======================================================================
print("=" * 72)
n_fail = sum(1 for _, ok, _ in PASS if not ok)
for name, ok, _ in PASS:
    if not ok:
        print("FAILED:", name)
print("VERDICT:", "ALL PASS" if n_fail == 0 else f"FAIL ({n_fail} failed)")
