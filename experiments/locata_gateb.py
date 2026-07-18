# Real-data DOA Gate-B on the LOCATA corpus (empirical companion to GO-P-2026-031).
#
# GO-P-2026-031 showed the reconstruction flip + omission floor on a SIMULATED ULA. LOCATA
# (Open Data Commons Attribution v1.0; Zenodo 3630471) provides REAL microphone-array
# recordings with OptiTrack ground-truth source DOA. The DICIT array contains four nested
# uniform linear sub-arrays (4/8/16/32 cm), so we can pull a real ULA out of real recordings
# and reuse the exact steering-vector / MUSIC machinery.
#
# On real data this tests MORE than the simulation:
#   GO-2 (flip): at matched bits, angle error invariant < recon < anti, recon min. reconstruction.
#   GO-1 (identifiability): does the analytic read operator ghat = P_a^perp a'(theta0), computed
#         from the ideal manifold, match the REAL estimator's finite-difference sensitivity once
#         reverberation / coupling / miscalibration bend the manifold? (cos < 1 is the story.)
#
# Runs on Atlas (data lives at /archive/locata). `python locata_gateb.py --selftest` runs the
# geometry-agnostic core on synthetic ULA data with NO LOCATA dependency, and must reproduce the
# GO-P-2026-031 flip — the gate before trusting the loader on real recordings.
import argparse
import sys

import numpy as np

C = 343.0  # speed of sound, m/s


# ── geometry-agnostic narrowband ULA Gate-B core ─────────────────────────────
def steer(theta, p, f):
    """Narrowband far-field steering vector; p = mic positions along the array axis (m),
    theta = azimuth from broadside (rad), f = Hz."""
    return np.exp(-1j * 2 * np.pi * f * p * np.sin(theta) / C)


def dsteer(theta, p, f):
    return steer(theta, p, f) * (-1j * 2 * np.pi * f * p * np.cos(theta) / C)


def c2r(z):
    return np.concatenate([z.real, z.imag])


def r2c(v):
    m = len(v) // 2
    return v[:m] + 1j * v[m:]


def read_dir_analytic(theta0, p, f):
    """The angle-informative real direction ghat in R^{2M} at theta0."""
    a, da = steer(theta0, p, f), dsteer(theta0, p, f)
    g = da - a * (np.vdot(a, da) / np.vdot(a, a))       # P_a^perp a'
    w = c2r(g)
    return w / np.linalg.norm(w)


def basis_with(w, rng):
    M2 = len(w)
    Q, _ = np.linalg.qr(np.column_stack([w, rng.standard_normal((M2, M2))]))
    Q[:, 0] = w
    return Q


def arm_vars(mode, s0sq, kappa, dP):
    if mode == "invariant":
        return s0sq / kappa, s0sq * kappa ** (1.0 / dP)
    if mode == "recon":
        return s0sq, s0sq
    if mode == "anti":
        return s0sq * kappa, s0sq * kappa ** (-1.0 / dP)


def _grid(halfspan_deg=80, step_deg=0.25):
    return np.deg2rad(np.arange(-halfspan_deg, halfspan_deg + step_deg, step_deg))


def beamform_ml(x, p, f, grid):
    """Single-snapshot matched-filter / beamformer-ML angle estimate (continuous via parabolic
    interpolation) — the consumer whose sensitivity is exactly ghat (GO-P-2026-031)."""
    A = np.exp(-1j * 2 * np.pi * f * np.outer(p, np.sin(grid)) / C)      # M x G
    P = np.abs(A.conj().T @ x) ** 2
    k = int(np.argmax(P))
    if 0 < k < len(grid) - 1:
        y0, y1, y2 = P[k - 1], P[k], P[k + 1]
        d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-30)
        return grid[k] + d * (grid[1] - grid[0])
    return grid[k]


def gateb(X, p, f, theta0, *, kappa=4.0, s0sqs=None, n_frames=40, n_reps=12, rng=None):
    """Three-arm Gate-B applied PER FRAME (each column of X is a single snapshot at bin f),
    using the beamformer-ML consumer — a direct per-frame application of GO-P-2026-031.
    theta0 = ground-truth azimuth (rad). Returns per-arm MSE(deg^2), reconstruction energy, the
    flip count, MSE step ratios, and GO-1 cos(empirical read dir, analytic ghat)."""
    rng = rng or np.random.default_rng(0)
    M, T = X.shape
    if s0sqs is None:
        s0sqs = np.geomspace(1e-1, 1e-4, 6)
    w = read_dir_analytic(theta0, p, f)
    Q = basis_with(w, np.random.default_rng(1))
    dP = 2 * M - 1
    grid = _grid()
    idx = np.unique(np.linspace(0, T - 1, min(n_frames, T)).astype(int))
    Xs = X[:, idx]                                                       # M x nf

    # GO-1: empirical read direction = finite-diff sensitivity of the estimator at the clean
    # manifold point a(theta0). For the beamformer-ML consumer this equals the analytic ghat.
    y = steer(theta0, p, f)
    base = beamform_ml(y, p, f, grid)
    w_emp = np.zeros(2 * M)
    for j in range(2 * M):
        e = np.zeros(2 * M); e[j] = 1e-4
        w_emp[j] = beamform_ml(y + r2c(e), p, f, grid) - base
    nrm = np.linalg.norm(w_emp)
    cos_go1 = abs(float((w_emp / nrm) @ w)) if nrm > 0 else 0.0

    modes = ["invariant", "recon", "anti"]
    MSE = np.zeros((len(s0sqs), 3)); REC = np.zeros((len(s0sqs), 3))
    for ie, s0sq in enumerate(s0sqs):
        for im, mode in enumerate(modes):
            eR, eP = arm_vars(mode, s0sq, kappa, dP)
            sd = np.sqrt(np.concatenate([[eR], np.full(dP, eP)]))
            errs = []; recs = []
            for t in range(Xs.shape[1]):
                x = Xs[:, t]
                for _ in range(n_reps):
                    d = Q @ (sd * rng.standard_normal(2 * M))
                    errs.append(np.rad2deg(beamform_ml(x + r2c(d), p, f, grid) - theta0) ** 2)
                    recs.append(float(d @ d))
            MSE[ie, im] = float(np.mean(errs)); REC[ie, im] = float(np.mean(recs))
    flip = int(sum((MSE[i, 0] <= MSE[i, 1] <= MSE[i, 2]) and (REC[i, 1] <= min(REC[i, 0], REC[i, 2]))
                   for i in range(len(s0sqs))))
    r1 = float(np.median([MSE[i, 1] / max(MSE[i, 0], 1e-30) for i in range(len(s0sqs))]))
    r2 = float(np.median([MSE[i, 2] / max(MSE[i, 1], 1e-30) for i in range(len(s0sqs))]))
    return {"MSE": MSE, "REC": REC, "flip": flip, "n_rates": len(s0sqs),
            "ratios": (r1, r2), "cos_go1": cos_go1, "theta0_deg": float(np.rad2deg(theta0))}


def srp_doa(X, p, f, grid):
    """SRP / Bartlett beamformer on the sample covariance — averages reverb down over frames.
    theta_hat = argmax_theta a(theta)^H R a(theta), continuous via parabolic interpolation."""
    R = (X @ X.conj().T) / X.shape[1]
    A = np.exp(-1j * 2 * np.pi * f * np.outer(p, np.sin(grid)) / C)      # M x G
    P = np.real(np.einsum("mg,mn,ng->g", A.conj(), R, A))
    k = int(np.argmax(P))
    if 0 < k < len(grid) - 1:
        y0, y1, y2 = P[k - 1], P[k], P[k + 1]
        d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-30)
        return grid[k] + d * (grid[1] - grid[0])
    return grid[k]


def gateb_srp(X, p, f, theta0, *, kappa=4.0, s0sqs=None, n_reps=30, rng=None):
    """Three-arm Gate-B with the SRP/Bartlett consumer: per-frame ghat-shaped compression, then
    a covariance beamformer over all frames (reverb-averaged). One stable estimate per rep."""
    rng = rng or np.random.default_rng(0)
    M, T = X.shape
    if s0sqs is None:
        s0sqs = np.geomspace(3e-2, 1e-4, 6)
    w = read_dir_analytic(theta0, p, f)
    Q = basis_with(w, np.random.default_rng(1))
    dP = 2 * M - 1
    grid = _grid()
    modes = ["invariant", "recon", "anti"]
    MSE = np.zeros((len(s0sqs), 3)); REC = np.zeros((len(s0sqs), 3))
    for ie, s0sq in enumerate(s0sqs):
        for im, mode in enumerate(modes):
            eR, eP = arm_vars(mode, s0sq, kappa, dP)
            sd = np.sqrt(np.concatenate([[eR], np.full(dP, eP)]))
            errs = np.empty(n_reps); recs = np.empty(n_reps)
            for r in range(n_reps):
                D = Q @ (sd[:, None] * rng.standard_normal((2 * M, T)))   # 2M x T
                Xd = X + (D[:M] + 1j * D[M:])                             # per-frame r2c
                errs[r] = np.rad2deg(srp_doa(Xd, p, f, grid) - theta0) ** 2
                recs[r] = float(np.mean(np.sum(D ** 2, axis=0)))
            MSE[ie, im] = errs.mean(); REC[ie, im] = recs.mean()
    flip = int(sum((MSE[i, 0] <= MSE[i, 1] <= MSE[i, 2]) and (REC[i, 1] <= min(REC[i, 0], REC[i, 2]))
                   for i in range(len(s0sqs))))
    r1 = float(np.median([MSE[i, 1] / max(MSE[i, 0], 1e-30) for i in range(len(s0sqs))]))
    r2 = float(np.median([MSE[i, 2] / max(MSE[i, 1], 1e-30) for i in range(len(s0sqs))]))
    return {"MSE": MSE, "REC": REC, "flip": flip, "n_rates": len(s0sqs), "ratios": (r1, r2)}


# ── autotune-to-the-scale: manifold denoising + recovered read operator ──────
def manifold_denoise(X, rank=1):
    """Project snapshots onto the top-`rank` signal subspace of the sample covariance. Uses only
    the data's own structure (the dominant eigenvector = estimated source direction), NOT the
    ground-truth angle — 'autotune to the scale (array manifold), not to the known note'."""
    R = (X @ X.conj().T) / X.shape[1]
    _w, V = np.linalg.eigh(R)
    U = V[:, -rank:]
    return U @ (U.conj().T @ X)


def _consumer(X, p, f, grid, rank=1):
    """The cleaned consumer: manifold-denoise, then SRP/Bartlett DOA."""
    return srp_doa(manifold_denoise(X, rank), p, f, grid)


def _read_subspace(theta0, p, f):
    """Orthonormal basis of span{a, i a, a', i a'} in R^{2M} — where the DOA read operator lives."""
    a, da = steer(theta0, p, f), dsteer(theta0, p, f)
    B = np.stack([c2r(a), c2r(1j * a), c2r(da), c2r(1j * da)], axis=1)
    Q, R = np.linalg.qr(B)
    return Q[:, np.abs(np.diag(R)) > 1e-9]


def _mse_dir(X, p, f, theta0, w, var, grid, n_reps, rng, rank):
    """DOA MSE of the cleaned consumer when per-snapshot error of variance `var` is placed on the
    unit real direction w."""
    M, T = X.shape
    errs = np.empty(n_reps)
    for r in range(n_reps):
        D = np.outer(w, np.sqrt(var) * rng.standard_normal(T))
        Xd = X + (D[:M] + 1j * D[M:])
        errs[r] = np.rad2deg(_consumer(Xd, p, f, grid, rank) - theta0) ** 2
    return errs.mean()


def recover_read_dir(X, p, f, theta0, *, var=0.3, n_reps=30, rank=1, rng=None):
    """Empirically recover the cleaned consumer's read operator: probe the quadratic MSE response
    within the manifold read-subspace, return its top eigendirection (the direction whose
    per-snapshot error most degrades this consumer's DOA). Does NOT use theta0 to steer — only to
    score the resulting error (as any downstream metric would)."""
    rng = rng or np.random.default_rng(0)
    grid = _grid()
    S = _read_subspace(theta0, p, f)
    d = S.shape[1]
    base = _mse_dir(X, p, f, theta0, np.zeros(2 * X.shape[0]), 0.0, grid, n_reps, rng, rank)
    diag = np.array([(_mse_dir(X, p, f, theta0, S[:, i], var, grid, n_reps, rng, rank) - base) / var
                     for i in range(d)])
    P = np.diag(diag)
    for i in range(d):
        for j in range(i + 1, d):
            w = (S[:, i] + S[:, j]) / np.sqrt(2)
            m = (_mse_dir(X, p, f, theta0, w, var, grid, n_reps, rng, rank) - base) / var
            P[i, j] = P[j, i] = m - 0.5 * (diag[i] + diag[j])
    _ew, ev = np.linalg.eigh(P)
    w_rec = S @ ev[:, -1]
    return w_rec / np.linalg.norm(w_rec)


def gateb_consumer(X, p, f, theta0, w_read, *, kappa=4.0, s0sqs=None, n_reps=30, rank=1, rng=None):
    """Three-arm Gate-B for the cleaned (manifold-denoised SRP) consumer, arms shaped about the
    given read direction w_read."""
    rng = rng or np.random.default_rng(0)
    M, T = X.shape
    if s0sqs is None:
        s0sqs = np.geomspace(1.0, 5e-3, 8)      # top trimmed to stay below estimator saturation
    Q = basis_with(w_read, np.random.default_rng(1))
    dP = 2 * M - 1
    grid = _grid()
    modes = ["invariant", "recon", "anti"]
    MSE = np.zeros((len(s0sqs), 3)); REC = np.zeros((len(s0sqs), 3))
    for ie, s0sq in enumerate(s0sqs):
        for im, mode in enumerate(modes):
            eR, eP = arm_vars(mode, s0sq, kappa, dP)
            sd = np.sqrt(np.concatenate([[eR], np.full(dP, eP)]))
            errs = np.empty(n_reps); recs = np.empty(n_reps)
            for r in range(n_reps):
                D = Q @ (sd[:, None] * rng.standard_normal((2 * M, T)))
                Xd = X + (D[:M] + 1j * D[M:])
                errs[r] = np.rad2deg(_consumer(Xd, p, f, grid, rank) - theta0) ** 2
                recs[r] = float(np.mean(np.sum(D ** 2, axis=0)))
            MSE[ie, im] = errs.mean(); REC[ie, im] = recs.mean()
    flip = int(sum((MSE[i, 0] <= MSE[i, 1] <= MSE[i, 2]) and (REC[i, 1] <= min(REC[i, 0], REC[i, 2]))
                   for i in range(len(s0sqs))))
    r1 = float(np.median([MSE[i, 1] / max(MSE[i, 0], 1e-30) for i in range(len(s0sqs))]))
    r2 = float(np.median([MSE[i, 2] / max(MSE[i, 1], 1e-30) for i in range(len(s0sqs))]))
    return {"MSE": MSE, "REC": REC, "flip": flip, "n_rates": len(s0sqs), "ratios": (r1, r2)}


def flip_significance(X, p, f, theta0, w_read, s0sq, *, kappa=4.0, n=400, rank=1, rng=None):
    """Within-recording significance at a fixed rate: draw n independent compression realizations
    per arm, return each arm's mean squared angle error +- standard error and the z-scores
    (sigmas) of the pairwise gaps recon>inv, anti>inv, anti>recon. Randomness = the compression
    draws (the controlled intervention); the signal and consumer are fixed."""
    rng = rng or np.random.default_rng(1)
    M, T = X.shape
    grid = _grid()
    Q = basis_with(w_read, np.random.default_rng(1))
    dP = 2 * M - 1
    stats = {}
    for mode in ["invariant", "recon", "anti"]:
        eR, eP = arm_vars(mode, s0sq, kappa, dP)
        sd = np.sqrt(np.concatenate([[eR], np.full(dP, eP)]))
        e = np.empty(n)
        for i in range(n):
            D = Q @ (sd[:, None] * rng.standard_normal((2 * M, T)))
            Xd = X + (D[:M] + 1j * D[M:])
            e[i] = np.rad2deg(_consumer(Xd, p, f, grid, rank) - theta0) ** 2
        stats[mode] = (float(e.mean()), float(e.std(ddof=1) / np.sqrt(n)))

    def z(hi, lo):
        mh, sh = stats[hi]; ml, sl = stats[lo]
        return (mh - ml) / np.sqrt(sh ** 2 + sl ** 2 + 1e-30)
    return stats, z("recon", "invariant"), z("anti", "invariant"), z("anti", "recon")


# ── confirmatory protocol: black-box recovery, cal/eval split, cross-recording ──
def _split_frames(X, frac_cal=0.5):
    """Temporal split into calibration | evaluation frame sets (disjoint)."""
    c = int(X.shape[1] * frac_cal)
    return X[:, :c], X[:, c:]


def recover_operator(Xcal, p, f, *, var=0.3, n_probes=180, n_reps=12, rank=1, rng, mode="ambient"):
    """FULLY BLACK-BOX read-operator recovery on calibration snapshots. Probes random directions
    in R^{2M}, measures mean-squared DISPLACEMENT of the consumer's DOA from its OWN clean estimate
    (NO ground truth anywhere), fits the quadratic response y = w^T P w by least squares, returns
    P's top eigenvector. mode='ambient' = full R^{2M} random probes + LS low-rank fit (no manifold,
    no truth). mode='subspace' = probes restricted to span{a,ia,a',ia'} at the consumer's OWN clean
    angle estimate (still truth-free). Returns (w_rec, th_ref, eigengap)."""
    grid = _grid()
    M = Xcal.shape[0]; M2 = 2 * M
    th_ref = _consumer(Xcal, p, f, grid, rank)                 # own clean DOA — the only reference
    if mode == "ambient":
        W = rng.standard_normal((n_probes, M2))
    else:
        S = _read_subspace(th_ref, p, f)
        W = rng.standard_normal((n_probes, S.shape[1])) @ S.T
    W = W / np.linalg.norm(W, axis=1, keepdims=True)
    y = np.empty(n_probes)
    for k in range(n_probes):
        w = W[k]; d = 0.0
        for _ in range(n_reps):
            D = np.outer(w, np.sqrt(var) * rng.standard_normal(Xcal.shape[1]))
            d += (_consumer(Xcal + (D[:M] + 1j * D[M:]), p, f, grid, rank) - th_ref) ** 2
        y[k] = d / n_reps / var
    idx = [(i, j) for i in range(M2) for j in range(i, M2)]
    Phi = np.array([[(2.0 if i != j else 1.0) * W[k, i] * W[k, j] for (i, j) in idx]
                    for k in range(n_probes)])
    coef = np.linalg.lstsq(Phi, y, rcond=None)[0]
    P = np.zeros((M2, M2))
    for c, (i, j) in zip(coef, idx):
        P[i, j] = P[j, i] = c
    ew, ev = np.linalg.eigh(P)
    w_rec = ev[:, -1]
    gap = float(ew[-1] / (abs(ew[-2]) + 1e-12))                # eigen-gap: rank-1-ness of P
    return w_rec / np.linalg.norm(w_rec), th_ref, gap


def bootstrap_stability(Xcal, p, f, *, B=6, rng, **kw):
    """Median pairwise |cos| between operators recovered on bootstrap resamples of the cal frames."""
    ws = []
    for _ in range(B):
        idx = rng.integers(0, Xcal.shape[1], Xcal.shape[1])
        w, _t, _g = recover_operator(Xcal[:, idx], p, f, rng=rng, n_probes=120, n_reps=8, **kw)
        ws.append(w)
    cs = [abs(float(ws[i] @ ws[j])) for i in range(B) for j in range(i + 1, B)]
    return float(np.median(cs))


def run_confirm(rec_dirs, freq=2000.0, mode="ambient"):
    """Full confirmatory protocol over a set of held-out recordings: black-box recover on each
    recording's CALIBRATION frames, then three-way flip on its EVALUATION frames using
    (analytic tangent, recovered-same-recording, recovered-TRANSFER-from-another-recording)."""
    rng = np.random.default_rng(31)
    D = []
    for d in rec_dirs:
        X, p, f, theta0 = load_recording(d, f_target=freq)
        if X.shape[1] < 24:
            print(f"  skip {d}: too few frames ({X.shape[1]})"); continue
        Xc, Xe = _split_frames(X)
        w_rec, th_ref, gap = recover_operator(Xc, p, f, rng=rng, mode=mode)
        w_an = read_dir_analytic(th_ref, p, f)                 # tangent at OWN estimate (truth-free)
        stab = bootstrap_stability(Xc, p, f, rng=rng, mode=mode)
        D.append(dict(name=d.split("/dev/")[-1].split("/eval/")[-1], p=p, f=f, theta0=theta0,
                      Xe=Xe, w_rec=w_rec, w_an=w_an, th_ref=th_ref, gap=gap, stab=stab,
                      cos=abs(float(w_rec @ w_an))))
    print(f"\n{'recording':<26} {'th_est':>7} {'GTΔ':>5} {'cos(rec,ĝ)':>10} {'stab':>5} {'gap':>5} "
          f"| {'flip: ĝ':>7} {'rec-same':>8} {'rec-xfer':>8}")
    agg = {"an": [], "same": [], "xfer": []}
    for i, di in enumerate(D):
        j = (i + 1) % len(D)                                   # transfer donor (different recording)
        fa = gateb_consumer(di["Xe"], di["p"], di["f"], di["theta0"], di["w_an"], n_reps=30)["flip"]
        fs = gateb_consumer(di["Xe"], di["p"], di["f"], di["theta0"], di["w_rec"], n_reps=30)["flip"]
        ft = gateb_consumer(di["Xe"], di["p"], di["f"], di["theta0"], D[j]["w_rec"], n_reps=30)["flip"]
        agg["an"].append(fa); agg["same"].append(fs); agg["xfer"].append(ft)
        gd = abs(np.rad2deg(di["th_ref"] - di["theta0"]))
        print(f"{di['name']:<26} {np.rad2deg(di['th_ref']):>6.1f}° {gd:>4.1f}° {di['cos']:>10.3f} "
              f"{di['stab']:>5.2f} {di['gap']:>5.1f} | {fa:>5}/8 {fs:>6}/8 {ft:>6}/8")
    n8 = 8
    print(f"\naggregate median flip /{n8}:  analytic ĝ = {int(np.median(agg['an']))}  "
          f"recovered-same = {int(np.median(agg['same']))}  recovered-transfer = {int(np.median(agg['xfer']))}")
    print(f"recordings where recovered-same >= analytic: {sum(s>=a for s,a in zip(agg['same'],agg['an']))}/{len(D)}")
    print(f"recordings where recovered-transfer >= analytic: {sum(t>=a for t,a in zip(agg['xfer'],agg['an']))}/{len(D)}")
    return D, agg


# ── self-test: synthetic ULA, must reproduce the GO-P-2026-031 flip ──────────
def selftest():
    rng = np.random.default_rng(20260718)
    M, d, f = 8, 0.04, 3000.0           # 8-mic ULA, 4 cm spacing, 3 kHz (< lambda/2 -> unambiguous)
    p = np.arange(M) * d
    theta0 = np.deg2rad(20.0)
    T = 200
    a = steer(theta0, p, f)
    s = np.exp(1j * rng.uniform(0, 2 * np.pi, T))       # unit-modulus source (constant SNR/frame)
    X = np.outer(a, s) + 0.02 * (rng.standard_normal((M, T)) + 1j * rng.standard_normal((M, T)))
    res = gateb(X, p, f, theta0, kappa=4.0, s0sqs=np.geomspace(3e-2, 1e-4, 6),
                n_frames=40, n_reps=40, rng=rng)
    print("=" * 78)
    print(f"SELFTEST (synthetic ULA M={M}, d={d*100:.0f}cm, f={f:.0f}Hz, theta0=20deg)")
    print(f"  cos(empirical read dir, analytic ghat) = {res['cos_go1']:.4f}")
    print(f"  flip = {res['flip']}/{res['n_rates']}   MSE step ratios = "
          f"{res['ratios'][0]:.2f}, {res['ratios'][1]:.2f} (expect ~kappa=4)")
    ok = res["flip"] == res["n_rates"] and res["cos_go1"] > 0.99
    print(f"  VERDICT: {'PASS' if ok else 'FAIL'} — core reproduces the flip on clean ULA data")
    return ok


# ── LOCATA DICIT loader (real recordings) ────────────────────────────────────
# The DICIT array's 8 cm nested ULA (channels below; x = +-16/+-8/0 cm, y~0) is ~lambda/2 at 2 kHz.
DICIT_ULA_8CM = [3, 4, 6, 9, 10]      # 0-indexed channels, mics {4,5,7,10,11}


def _pos_row(path):
    L = open(path).read().splitlines()
    return dict(zip(L[0].split("\t"), np.array(L[1].split("\t"), float)))


def load_recording(array_dir, mic_idx=DICIT_ULA_8CM, f_target=2000.0, energy_pct=60):
    """Load a LOCATA DICIT recording as narrowband ULA snapshots. Returns (X, p, f, theta0):
    X = M x T complex snapshots at the STFT bin nearest f_target during high-energy frames;
    p = mic positions along the array axis (m); theta0 = GT azimuth from broadside (rad)."""
    import scipy.io.wavfile as wf
    from scipy.signal import stft

    d = _pos_row(array_dir + "/position_array_dicit.txt")
    ref = np.array([d["x"], d["y"], d["z"]])
    Rot = np.array([[d["rotation_%d%d" % (i, j)] for j in (1, 2, 3)] for i in (1, 2, 3)])
    mics = np.array([[d["mic%d_%s" % (i, ax)] for ax in "xyz"] for i in range(1, 16)])
    p = ((mics - ref) @ Rot)[mic_idx, 0]                         # local x-positions (m)

    import glob
    sd = _pos_row(glob.glob(array_dir + "/position_source_*.txt")[0])
    ls = (np.array([sd["x"], sd["y"], sd["z"]]) - ref) @ Rot
    theta0 = np.arctan2(ls[1], ls[0]) - np.pi / 2                # azimuth -> from broadside

    rate, a = wf.read(array_dir + "/audio_array_dicit.wav")
    a = a[:, mic_idx].astype(float)
    Z = []
    for m in range(len(mic_idx)):
        fb, _t, z = stft(a[:, m], fs=rate, nperseg=1024, noverlap=512)
        Z.append(z)
    Z = np.stack(Z, axis=0)                                      # (M, nfreq, nframes)
    b = int(np.argmin(np.abs(fb - f_target)))
    Xf = Z[:, b, :]
    en = np.sum(np.abs(Xf) ** 2, axis=0)
    X = Xf[:, en >= np.percentile(en, energy_pct)]              # keep active (high-energy) frames
    X = X / (np.sqrt(np.mean(np.abs(X) ** 2)) + 1e-30)          # unit avg power (calibrate noise scale)
    return X, p, float(fb[b]), theta0


def run_recording(array_dir, **kw):
    X, p, f, theta0 = load_recording(array_dir, **kw)
    grid = _grid()
    th_hat = np.median([beamform_ml(X[:, t], p, f, grid) for t in range(X.shape[1])])
    print(f"  loaded {X.shape[1]} active frames, M={X.shape[0]}, bin={f:.0f} Hz")
    print(f"  GT azimuth (broadside) = {np.rad2deg(theta0):+.1f} deg ; "
          f"clean beamformer-ML median = {np.rad2deg(th_hat):+.1f} deg  "
          f"(|Δ| = {abs(np.rad2deg(th_hat - theta0)):.1f} deg)")
    th_srp = srp_doa(X, p, f, grid)
    print(f"  SRP/covariance beamformer (clean) = {np.rad2deg(th_srp):+.1f} deg  "
          f"(|Δ| = {abs(np.rad2deg(th_srp - theta0)):.1f} deg)")
    sweep = np.geomspace(2.0, 5e-3, 8)                          # span the reverb floor -> compression-dominated
    res = gateb(X, p, f, theta0, kappa=4.0, s0sqs=sweep,
                n_frames=min(60, X.shape[1]), n_reps=20)
    print(f"  [single-snapshot beamformer-ML]  GO-1 cos = {res['cos_go1']:.4f}   "
          f"GO-2 flip = {res['flip']}/{res['n_rates']}  ratios {res['ratios'][0]:.2f},{res['ratios'][1]:.2f}")
    # autotune-to-the-scale: manifold-denoised consumer + recover ITS read operator
    th_clean = _consumer(X, p, f, grid, rank=1)
    print(f"  manifold-denoised SRP (clean) = {np.rad2deg(th_clean):+.1f} deg  "
          f"(|Δ| = {abs(np.rad2deg(th_clean - theta0)):.1f} deg)")
    w_hat = read_dir_analytic(theta0, p, f)
    w_rec = recover_read_dir(X, p, f, theta0, var=0.3, n_reps=30, rank=1)
    print(f"  recovered read operator vs analytic ghat: cos = {abs(float(w_rec @ w_hat)):.3f}  "
          f"(GO-1: distance of the cleaned consumer's operator from the manifold tangent)")
    rc = gateb_consumer(X, p, f, theta0, w_rec, kappa=4.0, n_reps=30, rank=1)
    rg = gateb_consumer(X, p, f, theta0, w_hat, kappa=4.0, n_reps=30, rank=1)
    print(f"  [cleaned consumer, shaped by RECOVERED op ] GO-2 flip = {rc['flip']}/{rc['n_rates']}  "
          f"ratios {rc['ratios'][0]:.2f},{rc['ratios'][1]:.2f}")
    print(f"  [cleaned consumer, shaped by analytic ghat] GO-2 flip = {rg['flip']}/{rg['n_rates']}  "
          f"ratios {rg['ratios'][0]:.2f},{rg['ratios'][1]:.2f}  (wrong operator for this consumer)")
    for i in range(rc["n_rates"]):
        m = rc["MSE"][i]
        print(f"    rate {i}: recovered MSE inv/rec/anti = {m[0]:.3e} {m[1]:.3e} {m[2]:.3e} deg^2"
              + ("  <" if (m[0] <= m[1] <= m[2]) else "  !"))
    return res, rc, rg


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="run the synthetic-ULA core check")
    ap.add_argument("--recording", help="path to a LOCATA .../dicit array directory")
    ap.add_argument("--freq", type=float, default=2000.0)
    ap.add_argument("--sig", action="store_true", help="within-recording significance (sigmas)")
    ap.add_argument("--confirm", help="glob of .../dicit dirs for the black-box confirmatory protocol")
    ap.add_argument("--mode", default="ambient", choices=["ambient", "subspace"])
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    if a.confirm:
        import glob
        recs = sorted(glob.glob(a.confirm))
        print(f"confirmatory ({a.mode}) over {len(recs)} recordings, freq {a.freq} Hz")
        run_confirm(recs, freq=a.freq, mode=a.mode)
        sys.exit(0)
    if a.recording and a.sig:
        X, p, f, theta0 = load_recording(a.recording, f_target=a.freq)
        w_rec = recover_read_dir(X, p, f, theta0, var=0.3, n_reps=30, rank=1)
        print(f"within-recording significance (recovered operator), n=400 draws/arm\n  {a.recording}")
        for s0sq in [0.3, 0.1, 0.03, 0.01]:
            st, zri, zai, zar = flip_significance(X, p, f, theta0, w_rec, s0sq, n=400)
            print(f"  s0sq={s0sq:<5.3g} inv={st['invariant'][0]:7.2f}±{st['invariant'][1]:.2f} "
                  f"rec={st['recon'][0]:7.2f}±{st['recon'][1]:.2f} anti={st['anti'][0]:8.2f}±{st['anti'][1]:.2f} "
                  f"| z(rec>inv)={zri:5.1f}σ  z(anti>inv)={zai:5.1f}σ")
    elif a.recording:
        run_recording(a.recording, f_target=a.freq)
    else:
        print("give --selftest or --recording <.../dicit>")
