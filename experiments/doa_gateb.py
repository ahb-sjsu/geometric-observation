# GO-P-2026-031 governed harness — DOA Gate-B (simulated physical estimation).
#
# A physical-estimation Gate-B: direction-of-arrival on a uniform linear array. The
# consumer C reads a source angle; the angle-informative read operator is NOT the signal
# subspace span(A) (a subspace method is scale-invariant within it — the v1 MUSIC null) but
# the array-manifold DERIVATIVE orthogonalized against the steering vector:
#     ghat = normalize( P_a^perp a'(theta0) ),   P_a^perp = I - a a^H/(a^H a).
# A measurement perturbation moves the angle estimate ONLY through its projection on ghat.
#
# Three compressors at MATCHED bits (matched TOTAL log-precision = identical rate), allocated
# symmetrically about ghat (dR=1 informative real dim, dP=2M-1 others):
#   (a) invariant : var on ghat = s0^2/kappa   (precision ON the angle direction)
#   (b) recon     : var uniform  = s0^2         (minimizes ||x-xhat||)
#   (c) anti      : var on ghat = s0^2*kappa    (precision OFF the angle direction)
# Predict angle MSE a<b<c at every rate while reconstruction energy is minimized by (b) — the
# flip (GO-2 in a physical DOA domain). Consumer C = continuous beamformer-ML (matched filter,
# Newton-refined) — no subspace scale-invariance, no grid snapping. A MATLAB Phased Array
# root-MUSIC reference (doa_gateb_rootmusic.m, independent subspace estimator) cross-checks the
# same arms; its reconstruction-energy columns must match this harness's (shared shaping).
#
# HELD-OUT confirmatory params (M=16, theta0=-7 deg, kappa=4), distinct from the exploratory
# doa_gateb_v2 (M=12, +12 deg, kappa=3). Sealed BEFORE this run (GO-P-2026-031). Pure numpy.
import numpy as np

SEED = 20260718
M = 16                      # ULA sensors (held-out; exploratory used 12)
DSP = 0.5
POS = np.arange(M)
MVEC = 2 * np.pi * DSP * POS
TH0 = np.deg2rad(-7.0)      # true DOA (held-out; exploratory used +12)
KAPPA = 4.0                 # per-step precision ratio (held-out; exploratory used 3)
FOV = np.deg2rad(60.0)
ACQ = np.deg2rad(0.25)
S0SQS = np.geomspace(1e-1, 1e-4, 6)     # decreasing var = rising rate

# registered pass thresholds (fixed ex ante)
COS_MIN = 0.99
RATIO_LO, RATIO_HI = 2.4, 6.4           # beamformer-ML MSE step ratio band around kappa=4
OMIT_MIN = 100.0                        # omission floor multiple


def steer(th):
    return np.exp(1j * MVEC * np.sin(th))


def dsteer(th):
    return steer(th) * (1j * MVEC * np.cos(th))


def c2r(z):
    return np.concatenate([z.real, z.imag])


def r2c(v):
    return v[:M] + 1j * v[M:]


_GRID = np.arange(-FOV, FOV + ACQ, ACQ)
_GSTEER = np.stack([steer(t) for t in _GRID], axis=1)


def _power_derivs(th, x):
    a = steer(th)
    da = dsteer(th)
    dda = a * ((1j * MVEC * np.cos(th)) ** 2 - 1j * MVEC * np.sin(th))
    ax, dax, ddax = a.conj() @ x, da.conj() @ x, dda.conj() @ x
    return (2 * np.real(np.conj(ax) * dax),
            2 * (abs(dax) ** 2 + np.real(np.conj(ax) * ddax)))


def estimate_theta(x):
    th = _GRID[int(np.argmax(np.abs(_GSTEER.conj().T @ x) ** 2))]
    for _ in range(40):
        dP, ddP = _power_derivs(th, x)
        if ddP == 0:
            break
        step = dP / ddP
        th -= step
        if abs(step) < 1e-11:
            break
    return th


def read_direction(y):
    base = estimate_theta(y)
    w = np.zeros(2 * M)
    for j in range(2 * M):
        e = np.zeros(2 * M)
        e[j] = 1e-6
        w[j] = (estimate_theta(y + r2c(e)) - base) / 1e-6
    return w / np.linalg.norm(w)


def arm_vars(mode, s0sq, kappa, dP):
    if mode == "invariant":
        return s0sq / kappa, s0sq * kappa ** (1.0 / dP)
    if mode == "recon":
        return s0sq, s0sq
    if mode == "anti":
        return s0sq * kappa, s0sq * kappa ** (-1.0 / dP)


def basis_with(w):
    Q, _ = np.linalg.qr(np.column_stack([w, np.random.default_rng(1).standard_normal((2 * M, 2 * M))]))
    Q[:, 0] = w
    return Q


def sweep(Q, y, rng, n, omit=False):
    dP = 2 * M - 1
    MSE = np.zeros((len(S0SQS), 3))
    REC = np.zeros((len(S0SQS), 3))
    for ie, s0sq in enumerate(S0SQS):
        for im, mode in enumerate(["invariant", "recon", "anti"]):
            eR, eP = arm_vars(mode, s0sq, KAPPA, dP)
            if omit and mode == "invariant":
                eR = 0.05                              # ghat left UNCODED -> floor
            sd = np.sqrt(np.concatenate([[eR], np.full(dP, eP)]))
            errs = np.empty(n)
            recs = np.empty(n)
            for t in range(n):
                delta = Q @ (sd * rng.standard_normal(2 * M))
                errs[t] = np.rad2deg(estimate_theta(y + r2c(delta)) - TH0) ** 2
                recs[t] = float(delta @ delta)
            MSE[ie, im] = errs.mean()
            REC[ie, im] = recs.mean()
    return MSE, REC


def flip_count(MSE, REC):
    return int(sum((MSE[i, 0] <= MSE[i, 1] <= MSE[i, 2]) and (REC[i, 1] <= REC[i, 0]) and (REC[i, 1] <= REC[i, 2])
                   for i in range(len(S0SQS))))


def main():
    rng = np.random.default_rng(SEED)
    y = steer(TH0) * 1.0
    w = read_direction(y)
    a, da = steer(TH0), dsteer(TH0)
    g = da - a * (np.vdot(a, da) / np.vdot(a, a))
    g_an = c2r(g); g_an /= np.linalg.norm(g_an)
    cos_wa = abs(float(w @ g_an))

    MSE, REC = sweep(basis_with(w), y, np.random.default_rng(SEED), n=2500)
    flip = flip_count(MSE, REC)
    r1 = np.median([MSE[i, 1] / MSE[i, 0] for i in range(len(S0SQS))])
    r2 = np.median([MSE[i, 2] / MSE[i, 1] for i in range(len(S0SQS))])

    w_rand = np.random.default_rng(99).standard_normal(2 * M)
    w_rand /= np.linalg.norm(w_rand)
    MSEs, RECs = sweep(basis_with(w_rand), y, np.random.default_rng(SEED + 1), n=1500)
    flip_shuf = flip_count(MSEs, RECs)
    spread_shuf = np.median([(MSEs[i].max() - MSEs[i].min()) / MSEs[i].mean() for i in range(len(S0SQS))])

    MSEo, _ = sweep(basis_with(w), y, np.random.default_rng(SEED + 2), n=1500, omit=True)
    omit_mult = MSEo[-1, 0] / max(MSE[-1, 0], 1e-15)

    print("=" * 88)
    print(f"GO-P-2026-031 DOA Gate-B | M={M}, theta0={np.rad2deg(TH0):.0f} deg, kappa={KAPPA} "
          f"(HELD-OUT) | beamformer-ML")
    print(f"cos(w, analytic ghat) = {cos_wa:.4f}   (>{COS_MIN} required)")
    print(f"{'rate':>4} | {'MSE_inv':>10} {'MSE_rec':>10} {'MSE_anti':>10} | "
          f"{'REC_inv':>8} {'REC_rec':>8} {'REC_anti':>8}")
    for i in range(len(S0SQS)):
        ok = (MSE[i, 0] <= MSE[i, 1] <= MSE[i, 2]) and (REC[i, 1] <= min(REC[i, 0], REC[i, 2]))
        print(f"{i:>4} | {MSE[i,0]:>10.3e} {MSE[i,1]:>10.3e} {MSE[i,2]:>10.3e} | "
              f"{REC[i,0]:>8.3f} {REC[i,1]:>8.3f} {REC[i,2]:>8.3f}  {'<' if ok else '!'}")
    print(f"flip (real ghat): {flip}/6   MSE step ratios: rec/inv={r1:.2f}, anti/rec={r2:.2f} "
          f"(band [{RATIO_LO},{RATIO_HI}])")
    print(f"shuffled-consumer control (random dir): flip {flip_shuf}/6, median arm-spread "
          f"{spread_shuf:.3f} (expect ~0, no ordering)")
    print(f"omission (ghat uncoded): MSE {MSEo[-1,0]:.3e} vs coded {MSE[-1,0]:.3e} deg^2 "
          f"-> {omit_mult:.0f}x floor (>{OMIT_MIN:.0f} required)")

    checks = {
        "geometry cos>0.99": cos_wa > COS_MIN,
        "flip 6/6": flip == 6,
        "MSE ratio band": (RATIO_LO <= r1 <= RATIO_HI) and (RATIO_LO <= r2 <= RATIO_HI),
        "shuffled collapses (flip<=1)": flip_shuf <= 1,
        "omission floor>=100x": omit_mult >= OMIT_MIN,
    }
    print("-" * 88)
    for k, v in checks.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nVERDICT: {'ALL PASS' if all(checks.values()) else 'FAIL'}")


if __name__ == "__main__":
    main()
