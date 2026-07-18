# PILOT (exploratory, NOT sealed) — a physical-estimation Gate-B candidate to replace the
# de-gated swell radar: DOA (direction-of-arrival) estimation on a uniform linear array.
#
# Instance: snapshot x = sum_k a(theta_k) s_k + noise on an M-sensor ULA; consumer C = a
# beamformer that estimates the source angles theta. The estimator READS only the
# angle-informative subspace R = span{ a(theta_k), i a(theta_k), a'(theta_k), i a'(theta_k) }
# (signal + steering-derivative directions); everything orthogonal is noise it ignores, so
# ker of the read operator has dimension 2M - dim R > 0.
#
# Three compressors at MATCHED bits (matched as total log-precision, so identical rate):
#   (a) invariant  -- precision concentrated on R (angle-aware);
#   (b) recon      -- uniform precision (minimizes ||x - xhat||, isotropic);
#   (c) anti       -- precision concentrated on R^perp (the wrong quotient).
# Prediction (GO-2 in a physical domain): DOA MSE ordering a < b < c, while the RECONSTRUCTION
# energy ordering is b < a,c -- reconstruction-optimal is downstream-worst (the flip).
# Bonus: OMISSION -- deny bits to one source's derivative direction => that angle floors.
# Pure numpy. This is the reference the MATLAB (Phased Array Toolbox) prototype will cross-check.
import numpy as np
rng = np.random.default_rng(31)

M, K = 16, 2                      # sensors, sources
m = np.arange(M)

def steer(th):   return np.exp(1j * np.pi * np.sin(th) * m)                     # a(theta)
def dsteer(th):  return (1j * np.pi * np.cos(th) * m) * np.exp(1j * np.pi * np.sin(th) * m)  # da/dtheta
def c2r(z):      return np.concatenate([z.real, z.imag])                        # C^M -> R^{2M}
def r2c(v):      return v[:M] + 1j * v[M:]

GRID = np.linspace(-np.pi/2, np.pi/2, 1441)
GSTEER = np.stack([steer(t) for t in GRID], axis=1)                             # M x G

def beamform_doa(x, K):
    P = np.abs(GSTEER.conj().T @ x) ** 2
    loc = np.where((P[1:-1] > P[:-2]) & (P[1:-1] > P[2:]))[0] + 1
    if len(loc) < K: loc = np.argsort(P)[-K:]
    top = loc[np.argsort(P[loc])[-K:]]
    return np.sort(GRID[top])

def read_basis(thetas):
    cols = []
    for th in thetas:
        a, da = steer(th), dsteer(th)
        cols += [c2r(a), c2r(1j * a), c2r(da), c2r(1j * da)]
    Braw = np.stack(cols, axis=1)
    U, s, _ = np.linalg.svd(Braw, full_matrices=False)
    UR = U[:, s > 1e-9 * s.max()]                                              # orthonormal basis of R
    # complement
    Q, _ = np.linalg.qr(np.hstack([UR, rng.standard_normal((2*M, 2*M))]))
    Uperp = Q[:, UR.shape[1]:2*M]
    return UR, Uperp

def arm_variances(dR, dP, e0, kappa, mode):
    # matched log-precision: dR*log(eR)+dP*log(eP) = (dR+dP)*log(e0) for all arms
    if mode == "recon":     eR, eP = e0, e0
    elif mode == "invariant": eR, eP = e0 / kappa, e0 * kappa ** (dR / dP)
    elif mode == "anti":      eR, eP = e0 * kappa ** (dP / dR), e0 / kappa
    return eR, eP

def trial(e0, kappa, mode, omit=False):
    th0 = np.sort(rng.uniform(-0.35, 0.35, K))                                 # true angles (rad)
    thetas = th0 if (th0[1]-th0[0]) > 0.18 else np.array([th0[0], th0[0]+0.22])# ensure ~beamwidth separation
    s = (rng.standard_normal(K) + 1j * rng.standard_normal(K)) / np.sqrt(2)
    x = sum(s[k] * steer(thetas[k]) for k in range(K)) + \
        0.03 * (rng.standard_normal(M) + 1j * rng.standard_normal(M))          # low base noise: compression dominates
    UR, Uperp = read_basis(thetas); dR, dP = UR.shape[1], Uperp.shape[1]
    eR, eP = arm_variances(dR, dP, e0, kappa, mode)
    vR = np.sqrt(eR) * rng.standard_normal(dR)
    if omit and mode == "invariant":
        vR[-1] = np.sqrt(0.30) * rng.standard_normal()                         # one angle-informative dir left UNCODED
    vP = np.sqrt(eP) * rng.standard_normal(dP)
    delta = UR @ vR + Uperp @ vP                                               # real error, R^{2M}
    xhat = x + r2c(delta)
    th_hat = beamform_doa(xhat, K)
    doa_mse = float(np.mean((th_hat - thetas) ** 2))
    recon = float(np.sum(delta ** 2))
    return doa_mse, recon

def sweep(mode, e0s, kappa, n=400, omit=False):
    out = []
    for e0 in e0s:
        mses, recs = zip(*[trial(e0, kappa, mode, omit) for _ in range(n)])
        out.append((float(np.median(mses)), float(np.mean(recs))))
    return np.array(out)

e0s = np.geomspace(0.2, 2e-3, 5)                                               # decreasing base error = rising rate
kappa = 25.0
A = sweep("invariant", e0s, kappa); B = sweep("recon", e0s, kappa); C = sweep("anti", e0s, kappa)
print("="*80); print("DOA Gate-B pilot: MSE (median rad^2) and reconstruction energy at matched bits")
print(f"{'rate idx':>8} | {'MSE(a inv)':>11} {'MSE(b rec)':>11} {'MSE(c anti)':>11} | "
      f"{'rec(a)':>8} {'rec(b)':>8} {'rec(c)':>8}")
flip = 0
for i in range(len(e0s)):
    ma, mb, mc = A[i,0], B[i,0], C[i,0]; ra, rb, rc = A[i,1], B[i,1], C[i,1]
    flip += (ma <= mb <= mc) and (rb <= ra + 1e-9) and (rb <= rc + 1e-9)
    print(f"{i:>8} | {ma:>11.2e} {mb:>11.2e} {mc:>11.2e} | {ra:>8.2f} {rb:>8.2f} {rc:>8.2f}")
print(f"\nDOA-MSE ordering a<=b<=c AND recon-optimal is arm b: {flip}/{len(e0s)} rate points "
      f"-> the flip (recon-optimal is downstream-worst-but-one)")
Om = sweep("invariant", e0s, kappa, omit=True)
print(f"OMISSION (deny bits to one source's derivative): MSE floors at {Om[-1,0]:.2e} "
      f"vs no-omit {A[-1,0]:.2e} at the highest rate (>{Om[-1,0]/max(A[-1,0],1e-12):.0f}x)")
