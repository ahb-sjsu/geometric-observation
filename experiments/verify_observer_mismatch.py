# Numerical falsification harness for "The price of a misidentified observer."
# Governed by the same max-det / reverse-water-filling machinery as
# verify_two_observer.py (Lemma "Gaussian optimum", Sec. successive refinement).
# Pure numpy, CPU only.  MIT License.
#
#   X ~ N(0, Sx).  True read operator P >= 0, distortion d_P(x,xh)=(x-xh)^T P (x-xh),
#   downstream cost governed by tr(P Sigma_delta).  Single-observer optimum:
#     R_P(D) = 1/2 logdet Sx - 1/2 logdet Sigma*(P,D),
#     Sigma*(P,D) = argmax{ logdet S : 0<=S<=Sx, tr(P S)<=D }.
#   Whiten Pt = Sx^{1/2} P Sx^{1/2} = V diag(p_k) V^T; then in whitened coords the
#   error S_w = min(1, theta/p_k) per mode, sum_k min(p_k,theta)=D, and
#     Sigma* = Sx^{1/2} V diag(min(1,theta/p_k)) V^T Sx^{1/2}.
#   The cap S<=Sx binds on ker P (p_k=0 -> S_w=1 -> Sigma=Sx there, zero rate).
#
# Two claims under test:
#   COMMISSION.  If m P_hat <= P <= M P_hat on a shared range of rank r (0<m<=M),
#     designing for P_hat but guaranteeing the TRUE distortion D costs excess rate
#     Delta R <= (r/2) log(M/m).  (Tight when P = m P_hat, coder knows only loose M.)
#   OMISSION.  If range(P) is NOT subset range(P_hat), every P_hat-allocation has true
#     distortion >= D_floor = tr( Pt * Pi ), Pi = orth. proj. onto ker(Sx^{1/2} P_hat
#     Sx^{1/2}).  Distortion is FLOORED (never below D_floor) but never unbounded
#     (<= tr(P Sx) at zero rate); the rate to reach any D < D_floor is +infinity.
import numpy as np
rng = np.random.default_rng(20260717)

# ----------------------------------------------------------------------- helpers
def spd(n, jitter=0.5):
    A = rng.standard_normal((n, n)); return A @ A.T + jitter*np.eye(n)

def sqrtm_sym(M):
    w, U = np.linalg.eigh((M+M.T)/2); return U @ np.diag(np.sqrt(np.maximum(w,0))) @ U.T

def _waterlevel(p, D):
    """theta solving sum_k min(p_k, theta) = D  (p_k>=0)."""
    Dmax = float(np.sum(p))
    if D >= Dmax:
        return np.inf
    lo, hi = 0.0, max(float(p.max()), 1e-12)
    for _ in range(300):
        mid = 0.5*(lo+hi)
        if float(np.sum(np.minimum(p, mid))) < D: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)

def sigma_star(P, D, Sx):
    """max-det optimal error covariance (reverse water-filling; cap binds on ker P)."""
    Sh = sqrtm_sym(Sx)
    p, V = np.linalg.eigh(Sh @ P @ Sh); p = np.maximum(p, 0.0)
    theta = _waterlevel(p, D)
    if not np.isfinite(theta):
        e = np.ones_like(p)
    else:
        with np.errstate(divide="ignore", invalid="ignore"):
            e = np.where(p > 0, np.minimum(1.0, theta/np.where(p>0, p, 1.0)), 1.0)
    return Sh @ (V @ np.diag(e) @ V.T) @ Sh

def sigma_from_theta(P, theta, Sx):
    """error covariance of the P-water-filling family at an explicit water level theta."""
    Sh = sqrtm_sym(Sx)
    p, V = np.linalg.eigh(Sh @ P @ Sh); p = np.maximum(p, 0.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        e = np.where(p > 0, np.minimum(1.0, theta/np.where(p>0, p, 1.0)), 1.0)
    return Sh @ (V @ np.diag(e) @ V.T) @ Sh

def rate(Sig, Sx):
    return 0.5*(np.linalg.slogdet(Sx)[1] - np.linalg.slogdet(Sig)[1])

def R_P(P, D, Sx):
    return rate(sigma_star(P, D, Sx), Sx)

def mineig(M): return float(np.linalg.eigvalsh((M+M.T)/2).min())

fail = []

# ============================================================ [1] COMMISSION TAX
print("="*72)
print("[1] COMMISSION: excess rate of the safe P_hat-plan <= (r/2) log(M/m)")
for d in (2, 3):
    r = d  # full shared range
    for tag, at_lower_edge in (("tight (P=m*P_hat)", True), ("random G in [m,M]", False)):
        Sx  = spd(d)
        Ph  = spd(d)                                  # estimated operator P_hat > 0
        m, M = 0.5, 4.0                               # sandwich constants the coder knows
        Phh = sqrtm_sym(Ph)
        if at_lower_edge:
            G = m*np.eye(d)                           # P = m P_hat exactly (worst case)
        else:
            evs = rng.uniform(m, M, size=d); evs[0]=m; evs[-1]=M   # eigs pinned to [m,M]
            Q,_ = np.linalg.qr(rng.standard_normal((d,d)))
            G = Q @ np.diag(evs) @ Q.T
        P = Phh @ G @ Phh                              # m*Ph <= P <= M*Ph by construction
        # verify the sandwich actually holds
        sw_lo = mineig(P - m*Ph) >= -1e-9
        sw_hi = mineig(M*Ph - P) >= -1e-9
        # pick a TRUE target distortion D in the coding regime, small enough all modes active
        D = 0.05*np.trace(P@Sx)
        # oracle (knows P):
        Rora = R_P(P, D, Sx)
        # safe mismatched plan: design for P_hat at D/M  ->  guarantees tr(P Sig) <= D
        Sig_mm = sigma_star(Ph, D/M, Sx)
        Rmm    = rate(Sig_mm, Sx)
        true_D = float(np.trace(P @ Sig_mm))
        dR     = Rmm - Rora
        bound  = 0.5*r*np.log(M/m)
        ratio  = dR/bound
        ok = (sw_lo and sw_hi and true_D <= D + 1e-8 and dR >= -1e-8
              and dR <= bound + 1e-8)
        print(f"  d={d} {tag:22s} sandwich[{sw_lo}&{sw_hi}] trueD={true_D:.4f}<=D={D:.4f} "
              f"dR={dR:.4f} bound={bound:.4f} ratio={ratio:.3f} {'OK' if ok else 'FAIL'}")
        if not ok: fail.append(f"commission d={d} {tag}")

# ============================================================ [2] OMISSION FLOOR
print("="*72)
print("[2] OMISSION: distortion floored at D_floor=tr(Pt*Pi), never unbounded, rate->inf")
for d in (2, 3):
    Sx = spd(d)
    # Build P_hat that MISSES a direction: rank d-1 (kernel = one random direction).
    Q,_ = np.linalg.qr(rng.standard_normal((d,d)))
    read_dirs = Q[:, :d-1]                            # P_hat reads these
    weights   = rng.uniform(0.5, 3.0, size=d-1)
    Ph = read_dirs @ np.diag(weights) @ read_dirs.T   # rank d-1, misses Q[:,d-1]
    # True P reads full space (so it reads the missed direction too):
    P = spd(d)
    # --- floor via the whitened-kernel projector ---
    Sh = sqrtm_sym(Sx); Pt = Sh @ P @ Sh
    pw, Vw = np.linalg.eigh(Sh @ Ph @ Sh)
    kmask = pw <= 1e-9                                # whitened kernel of P_hat
    Pi = Vw[:, kmask] @ Vw[:, kmask].T
    D_floor = float(np.trace(Pt @ Pi))
    # --- independent floor: limiting covariance Sx^{1/2} Pi Sx^{1/2}, its P-energy ---
    Sig_limit = Sh @ Pi @ Sh
    D_floor_alt = float(np.trace(P @ Sig_limit))
    # --- sweep water levels down; watch true distortion approach floor from ABOVE ---
    thetas = np.array([1e0, 1e-1, 1e-2, 1e-4, 1e-8])
    Ds, Rs = [], []
    for th in thetas:
        Sig = sigma_from_theta(Ph, th, Sx)
        Ds.append(float(np.trace(P @ Sig)))
        Rs.append(rate(Sig, Sx))
    Ds = np.array(Ds); Rs = np.array(Rs)
    D_zero_rate = float(np.trace(P @ Sx))            # zero-rate distortion (finite!)
    above  = bool(np.all(Ds >= D_floor - 1e-6))      # never below floor
    approach = abs(Ds[-1] - D_floor) < 1e-3          # reaches floor as theta->0
    diverge  = Rs[-1] > Rs[0] + 5                     # rate blows up
    finite   = np.isfinite(D_zero_rate) and D_zero_rate < 1e6
    match    = abs(D_floor - D_floor_alt) < 1e-9
    ok = above and approach and diverge and finite and match and D_floor > 1e-6
    print(f"  d={d} D_floor={D_floor:.5f} (alt={D_floor_alt:.5f}) "
          f"zero-rate D={D_zero_rate:.4f}(finite)")
    print(f"       theta-sweep true D: {np.array2string(Ds, precision=5)}")
    print(f"       theta-sweep rate  : {np.array2string(Rs, precision=3)}  "
          f"(rate->inf as D->floor+)")
    print(f"       floored={above} reaches-floor={approach} rate-diverges={diverge} "
          f"{'OK' if ok else 'FAIL'}")
    if not ok: fail.append(f"omission d={d}")

# ================================================ [3] PROBE OVERLAP -> FLOOR/BOUND
print("="*72)
print("[3] PROBE: principal-angle overlap o -> certified floor  (Sx=I: D_floor=r(1-o))")
for d, r in ((3, 2), (3, 1)):
    Sx = np.eye(d)
    # true read subspace R (rank r): first r columns of a random orthobasis
    Qt,_ = np.linalg.qr(rng.standard_normal((d,d)))
    U  = Qt[:, :r]
    P  = U @ U.T                                      # projector read operator on R
    # recovered subspace R_hat: rotate U toward a partial miss by angle phi in one plane
    phi = rng.uniform(0.3, 1.0)                       # principal angle (radians)
    Uh = U.copy().astype(float)
    outside = Qt[:, r]                                # a direction orthogonal to R
    Uh[:, 0] = np.cos(phi)*U[:, 0] + np.sin(phi)*outside  # tilt one basis vector out of R
    Uh, _ = np.linalg.qr(Uh)                          # re-orthonormalize -> R_hat basis
    Uh = Uh[:, :r]
    Ph = Uh @ Uh.T                                    # recovered projector (misses part of R)
    # overlap metric o = (1/r) tr(Pi_R Pi_Rhat) = (1/r) sum cos^2(theta_i)
    o = float(np.trace(P @ Ph))/r
    # measured floor via general formula
    Sh = sqrtm_sym(Sx); Pt = Sh @ P @ Sh
    pw, Vw = np.linalg.eigh(Sh @ Ph @ Sh); kmask = pw <= 1e-9
    Pi = Vw[:, kmask] @ Vw[:, kmask].T
    D_floor = float(np.trace(Pt @ Pi))
    predicted = r*(1.0 - o)                           # Sx=I closed form
    read_energy = float(np.trace(P @ Sx))             # = r
    frac = D_floor/read_energy
    ok = abs(D_floor - predicted) < 1e-6 and abs(frac - (1-o)) < 1e-6
    print(f"  d={d} r={r} overlap o={o:.4f}  D_floor={D_floor:.5f}  r(1-o)={predicted:.5f}  "
          f"floor/read-energy={frac:.4f}  {'OK' if ok else 'FAIL'}")
    if not ok: fail.append(f"probe d={d} r={r}")

# map the measured Llama overlap 0.647 (Sx=I, projector model) to a certified floor
o_meas = 0.647
print(f"  --> measured overlap {o_meas}: certified irreducible distortion floor = "
      f"{1-o_meas:.3f} of read energy (no rate removes it) IF the recovery OMITS "
      f"(does not contain) the true read subspace.")

# also: general Sx != I -- the naive r(1-o) is NOT the floor; whitened projector is.
print("="*72)
print("[3b] Sx != I: naive r(1-o) MISSES; correct floor uses whitened kernel projector")
d, r = 3, 2
Sx = spd(d)
Qt,_ = np.linalg.qr(rng.standard_normal((d,d)))
U = Qt[:, :r]; P = U@U.T
phi = 0.7
Uh = U.copy().astype(float); Uh[:,0] = np.cos(phi)*U[:,0] + np.sin(phi)*Qt[:,r]
Uh,_ = np.linalg.qr(Uh); Uh = Uh[:, :r]; Ph = Uh@Uh.T
o = float(np.trace(P@Ph))/r
Sh = sqrtm_sym(Sx); Pt = Sh@P@Sh
pw, Vw = np.linalg.eigh(Sh@Ph@Sh); kmask = pw <= 1e-9
Pi = Vw[:, kmask]@Vw[:, kmask].T
D_floor = float(np.trace(Pt@Pi))
naive = r*(1-o)
# independent check: floor equals limiting P-energy
D_floor_alt = float(np.trace(P @ (Sh@Pi@Sh)))
ok = abs(D_floor - D_floor_alt) < 1e-9 and D_floor > 1e-6
print(f"  d={d} r={r} overlap o={o:.4f}  correct D_floor={D_floor:.5f}  "
      f"(alt={D_floor_alt:.5f})  naive r(1-o)={naive:.5f}  differ={abs(D_floor-naive):.4f}  "
      f"{'OK' if ok else 'FAIL'}")
if not ok: fail.append("probe Sx!=I")

print("="*72)
print("VERDICT:", "ALL PASS" if not fail else f"FAIL: {fail}")
