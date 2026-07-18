# DOA Gate-B, v2 (exploratory, NOT sealed) — corrected read operator.
#
# v1 failure (MATLAB MUSIC): splitting compression error between the signal subspace
# span(A) and its complement did NOT move the DOA estimate — MUSIC is scale-invariant
# within span(A), so RMSE was 0 for every arm. The read operator for an ANGLE consumer
# is not span(A); it is the array-manifold DERIVATIVE direction
#     ghat = normalize( P_a^perp a'(theta) ),   P_a^perp = I - a a^H / (a^H a),
# i.e. the component of da/dtheta orthogonal to the steering vector. A measurement
# perturbation moves the angle estimate ONLY through its projection on ghat.
#
# Consumer C = a continuous beamformer-ML estimator (matched filter, refined by Newton) —
# NOT a subspace method, so no scale-invariance degeneracy and no grid snapping.
#
# Three compressors at MATCHED bits (matched TOTAL log-precision => identical rate),
# allocated symmetrically about ghat (dR=1 informative real dim, dP=2M-1 others):
#   (a) invariant : var on ghat = s0^2/kappa   (precision ON the angle direction)
#   (b) recon     : var uniform  = s0^2         (minimizes ||x-xhat||)
#   (c) anti      : var on ghat = s0^2*kappa    (precision OFF the angle direction)
# Prediction: angle MSE ordering a<b<c (ratio ~kappa/step), while reconstruction energy
# is MINIMIZED by (b) — the flip. Plus OMISSION: leave ghat UNCODED => angle MSE floors.
#
# Pure numpy. This is the sealed-harness candidate; a MATLAB phased.RootMUSICEstimator
# reference will cross-check it (differential test, independent estimator).
import numpy as np

SEED = 20260718
M = 12                      # ULA sensors
DSP = 0.5                   # element spacing (wavelengths)
POS = np.arange(M)
MVEC = 2 * np.pi * DSP * POS
TH0 = np.deg2rad(12.0)      # true source DOA
KAPPA = 3.0                 # per-step precision ratio
FOV = np.deg2rad(60.0)      # +/- field of view for acquisition
ACQ = np.deg2rad(0.25)      # acquisition grid step


def steer(th):
    return np.exp(1j * MVEC * np.sin(th))


def dsteer(th):
    return steer(th) * (1j * MVEC * np.cos(th))


def c2r(z):
    return np.concatenate([z.real, z.imag])


def r2c(v):
    return v[:M] + 1j * v[M:]


# ---- continuous beamformer-ML angle estimator (full-FOV acquire + Newton refine) ----
_GRID = np.arange(-FOV, FOV + ACQ, ACQ)
_GSTEER = np.stack([steer(t) for t in _GRID], axis=1)      # M x Ngrid


def _power_derivs(th, x):
    a = steer(th)
    da = dsteer(th)
    dda = a * ((1j * MVEC * np.cos(th)) ** 2 - 1j * MVEC * np.sin(th))
    ax, dax, ddax = a.conj() @ x, da.conj() @ x, dda.conj() @ x
    P = abs(ax) ** 2
    dP = 2 * np.real(np.conj(ax) * dax)
    ddP = 2 * (abs(dax) ** 2 + np.real(np.conj(ax) * ddax))
    return P, dP, ddP


def estimate_theta(x):
    Pg = np.abs(_GSTEER.conj().T @ x) ** 2
    th = _GRID[int(np.argmax(Pg))]
    for _ in range(40):
        P, dP, ddP = _power_derivs(th, x)
        if ddP == 0:
            break
        step = dP / ddP                     # Newton toward the stationary point (ddP<0 at peak)
        th -= step
        if abs(step) < 1e-11:
            break
    return th


def read_direction(y):
    """Empirical read direction: unit R^{2M} vector along which measurement
    perturbations move the estimate (= range of the read operator P_C)."""
    base = estimate_theta(y)
    w = np.zeros(2 * M)
    eps = 1e-6
    for j in range(2 * M):
        e = np.zeros(2 * M)
        e[j] = eps
        w[j] = (estimate_theta(y + r2c(e)) - base) / eps
    return w / np.linalg.norm(w)


def arm_vars(mode, s0sq, kappa, dR, dP):
    # symmetric matched-log-precision allocation about the informative subspace
    if mode == "invariant":
        return s0sq / kappa, s0sq * kappa ** (1.0 / dP)
    if mode == "recon":
        return s0sq, s0sq
    if mode == "anti":
        return s0sq * kappa, s0sq * kappa ** (-1.0 / dP)
    raise ValueError(mode)


def run(n=2000, omit=False):
    rng = np.random.default_rng(SEED)
    y = steer(TH0) * 1.0                                    # clean measurement, unit amplitude
    w = read_direction(y)
    # analytic direction, for a cross-check on the geometry
    a, da = steer(TH0), dsteer(TH0)
    Pperp_da = da - a * (np.vdot(a, da) / np.vdot(a, a))
    g_analytic = c2r(Pperp_da)
    g_analytic /= np.linalg.norm(g_analytic)
    cos_wa = abs(float(w @ g_analytic))
    # orthobasis with w first
    Q, _ = np.linalg.qr(np.column_stack([w, np.random.default_rng(1).standard_normal((2 * M, 2 * M))]))
    Q[:, 0] = w
    dR, dP = 1, 2 * M - 1
    s0sqs = np.geomspace(1e-1, 1e-4, 6)                     # decreasing var = rising rate
    modes = ["invariant", "recon", "anti"]
    MSE = np.zeros((len(s0sqs), 3))
    REC = np.zeros((len(s0sqs), 3))
    for ie, s0sq in enumerate(s0sqs):
        for im, mode in enumerate(modes):
            eR, eP = arm_vars(mode, s0sq, KAPPA, dR, dP)
            if omit and mode == "invariant":
                eR = 0.05                                  # ghat left UNCODED (fixed floor)
            sd = np.sqrt(np.concatenate([[eR], np.full(dP, eP)]))
            errs = np.empty(n)
            recs = np.empty(n)
            for t in range(n):
                coeff = sd * rng.standard_normal(2 * M)
                delta = Q @ coeff                          # R^{2M} error, shaped in Q basis
                th_hat = estimate_theta(y + r2c(delta))
                errs[t] = (np.rad2deg(th_hat - TH0)) ** 2
                recs[t] = float(delta @ delta)
            MSE[ie, im] = errs.mean()
            REC[ie, im] = recs.mean()
    return s0sqs, MSE, REC, cos_wa


if __name__ == "__main__":
    s0sqs, MSE, REC, cos_wa = run(n=2000)
    print("=" * 84)
    print(f"DOA Gate-B v2 | M={M} sensors, theta0={np.rad2deg(TH0):.0f} deg, kappa={KAPPA}, "
          f"beamformer-ML | cos(w, analytic ghat)={cos_wa:.4f}")
    print(f"{'rate':>4} | {'MSE_inv':>10} {'MSE_rec':>10} {'MSE_anti':>10} | "
          f"{'REC_inv':>8} {'REC_rec':>8} {'REC_anti':>8}")
    flip = 0
    for i in range(len(s0sqs)):
        mi, mr, mc = MSE[i]
        ri, rr, rc = REC[i]
        ok = (mi <= mr <= mc) and (rr <= ri) and (rr <= rc)
        flip += ok
        print(f"{i:>4} | {mi:>10.3e} {mr:>10.3e} {mc:>10.3e} | "
              f"{ri:>8.3f} {rr:>8.3f} {rc:>8.3f}  {'<' if ok else ' '}")
    print(f"\nFLIP (angle MSE inv<=rec<=anti AND recon-optimal is the recon arm): "
          f"{flip}/{len(s0sqs)} rate points")
    _, MSEo, _, _ = run(n=2000, omit=True)
    print(f"OMISSION (ghat left uncoded): invariant MSE at highest rate = {MSEo[-1,0]:.3e} deg^2 "
          f"vs coded {MSE[-1,0]:.3e} deg^2  -> {MSEo[-1,0]/max(MSE[-1,0],1e-12):.0f}x floor")
