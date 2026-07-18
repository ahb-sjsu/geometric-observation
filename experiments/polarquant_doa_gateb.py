# PolarQuant DOA Gate-B on real LOCATA data (per reviewer + PolarQuant redesign).
#
# Replaces the ad-hoc additive-Gaussian compression with the REAL PolarQuant quantizer
# (turboquant-pro foundation; Han et al. arXiv:2502.02617) — decompose each array snapshot into
# radius (magnitude) + angles (direction) and quantize separately, because the direction carries
# the geometry (the angular-observer thesis). Consumer = a MATURE MATLAB DOA estimator
# (Phased Array ESPRIT + root-MUSIC), independent of the compressor.
#
# Three quantizers at MATCHED bits/snapshot on the real-embedded snapshot:
#   (a) PolarQuant     — angle-favoring (the thesis's compressor)          [invariant]
#   (b) scalar-uniform — reconstruction-optimal per-coord uniform          [recon, neutral baseline]
#   (c) phase-destroy  — per-complex-coord magnitude-fine / phase-coarse   [anti]
# Falsifiable prediction (GO-2, physical): DOA error a < b < c, while reconstruction MSE is
# minimized by (b) — angle-preserving beats reconstruction-optimal for the angle-reading consumer.
#
# 8 cm DICIT ULA at 2144 Hz (exactly lambda/2 -> ESPRIT/root-MUSIC exact). Runs on Atlas:
#   /home/claude/env/bin/python polarquant_doa_gateb.py <rec1/dicit> [rec2/dicit ...]
import subprocess
import sys

import numpy as np
from scipy.io import loadmat, savemat
from scipy.signal import stft
import scipy.io.wavfile as wf

C = 343.0
MIC = [3, 4, 6, 9, 10]                 # 8 cm DICIT ULA
MATLAB = "/home/claude/MATLAB/bin/matlab"


# ---- PolarQuant transform (verbatim from turboquant-pro / erisml polar_encoding.py) ----
def polar_encode(X):
    angles = []
    v = X
    while v.shape[1] > 1:
        a, b = v[:, 0::2], v[:, 1::2]
        angles.append(np.arctan2(b, a))
        v = np.sqrt(a * a + b * b)
    return v[:, 0], angles


def polar_decode(radius, angles):
    v = radius[:, None]
    for th in reversed(angles):
        a, b = v * np.cos(th), v * np.sin(th)
        nv = np.empty((v.shape[0], 2 * v.shape[1]))
        nv[:, 0::2], nv[:, 1::2] = a, b
        v = nv
    return v


def _quant_uniform(x, lo, hi, bits):
    levels = 2 ** bits
    step = (hi - lo) / max(levels, 1)
    q = np.clip(np.floor((x - lo) / (step + 1e-30)), 0, levels - 1)
    return lo + (q + 0.5) * step


def polar_quantize(Xr, abits, rbits):
    radius, angles = polar_encode(Xr)
    lr = np.log(np.maximum(radius, 1e-20))
    radius_q = np.exp(_quant_uniform(lr, lr.min(), lr.max(), rbits))
    angles_q = [_quant_uniform(th, -np.pi, np.pi, abits) for th in angles]
    return polar_decode(radius_q, angles_q)


def _pad_pow2(V):
    d = V.shape[1]; p = 1
    while p < d:
        p *= 2
    if p == d:
        return V, d
    out = np.zeros((V.shape[0], p)); out[:, :d] = V
    return out, d


# ---- neutral + anti quantizers ----
def scalar_uniform(Xr, qbits):
    out = np.empty_like(Xr)
    for j in range(Xr.shape[1]):
        out[:, j] = _quant_uniform(Xr[:, j], Xr[:, j].min(), Xr[:, j].max(), qbits)
    return out


def phase_destroy(Xc, mbits, pbits):
    r = np.abs(Xc); ph = np.angle(Xc)
    lr = np.log(np.maximum(r, 1e-20))
    rq = np.exp(_quant_uniform(lr, lr.min(), lr.max(), mbits))
    pq = _quant_uniform(ph, -np.pi, np.pi, pbits)
    return rq * np.exp(1j * pq)


# ---- LOCATA single-bin snapshots (8 cm ULA, exact lambda/2 bin) ----
def load_snap(array_dir, f_target=2144.0, energy_pct=60):
    def row(path):
        L = open(path).read().splitlines()
        return dict(zip(L[0].split("\t"), np.array(L[1].split("\t"), float)))
    d = row(array_dir + "/position_array_dicit.txt")
    ref = np.array([d["x"], d["y"], d["z"]])
    Rot = np.array([[d["rotation_%d%d" % (i, j)] for j in (1, 2, 3)] for i in (1, 2, 3)])
    mics = np.array([[d["mic%d_%s" % (i, ax)] for ax in "xyz"] for i in range(1, 16)])
    p = ((mics - ref) @ Rot)[MIC, 0]
    import glob
    sd = row(glob.glob(array_dir + "/position_source_*.txt")[0])
    ls = (np.array([sd["x"], sd["y"], sd["z"]]) - ref) @ Rot
    theta0 = np.arctan2(ls[1], ls[0]) - np.pi / 2
    rate, a = wf.read(array_dir + "/audio_array_dicit.wav")
    a = a[:, MIC].astype(float)
    Z = np.stack([stft(a[:, m], fs=rate, nperseg=1024, noverlap=512)[2] for m in range(len(MIC))], 0)
    fb = stft(a[:, 0], fs=rate, nperseg=1024, noverlap=512)[0]
    b = int(np.argmin(np.abs(fb - f_target)))
    Xf = Z[:, b, :]
    X = Xf[:, np.sum(np.abs(Xf) ** 2, 0) >= np.percentile(np.sum(np.abs(Xf) ** 2, 0), energy_pct)]
    X = X / (np.sqrt(np.mean(np.abs(X) ** 2)) + 1e-30)
    return X, p, float(fb[b]), theta0


def compress(X, budget):
    """Return {arm: (Xhat complex M x T, recon_MSE, bits)} at ~matched total bits/snapshot."""
    M, T = X.shape
    Xr = np.concatenate([X.real, X.imag], 0).T          # T x 2M
    Xp, d = _pad_pow2(Xr)                                 # T x D (pow2)
    D = Xp.shape[1]
    out = {}
    # PolarQuant (angle-favoring): rbits=4, abits from budget
    ab = max(1, round((budget - 4) / (D - 1)))
    rec = polar_quantize(Xp, ab, 4)[:, :2 * M]
    out["polarquant"] = (rec[:, :M].T + 1j * rec[:, M:].T, ab * (D - 1) + 4)
    # scalar-uniform (reconstruction-optimal neutral baseline)
    qb = max(1, round(budget / D))
    rec = scalar_uniform(Xp, qb)[:, :2 * M]
    out["scalar"] = (rec[:, :M].T + 1j * rec[:, M:].T, qb * D)
    # phase-destroy (anti): per complex coord, magnitude fine / phase coarse (1 bit)
    Xc = X.T                                             # T x M
    mb = max(1, round((budget / M) - 1))
    rec = phase_destroy(Xc, mb, 1)
    out["phase_destroy"] = (rec.T, (mb + 1) * M)
    res = {}
    for k, (Xh, bits) in out.items():
        res[k] = (Xh, float(np.mean(np.sum(np.abs(X - Xh) ** 2, 0))), bits)
    return res


def main():
    recs = sys.argv[1:]
    budgets = [24, 36, 48, 64, 84]
    arms = ["polarquant", "scalar", "phase_destroy"]
    covs, meta, recon = [], [], {}
    for rd in recs:
        X, p, f, th0 = load_snap(rd)
        Rc = (X @ X.conj().T) / X.shape[1]
        covs.append(Rc); meta.append((rd, -1, "clean", np.rad2deg(th0)))
        for B in budgets:
            cx = compress(X, B)
            for arm in arms:
                Xh, mse, bits = cx[arm]
                covs.append((Xh @ Xh.conj().T) / Xh.shape[1])
                meta.append((rd, B, arm, np.rad2deg(th0)))
                recon.setdefault((rd, B), {})[arm] = (mse, bits)
    savemat("/tmp/pq_covs.mat", {"R": np.stack(covs, 0), "nsig": 1})
    subprocess.run([MATLAB, "-batch", "run('/tmp/pq_doa.m')"], check=True,
                   capture_output=True, text=True, timeout=280)
    doa = loadmat("/tmp/pq_doas.mat")
    esp = doa["esprit"].ravel(); rmu = doa["rootmusic"].ravel()

    print(f"{'recording':<22} {'GT':>6} | clean(esp/rmu)")
    idx = 0
    per = {}
    for m in meta:
        rd, B, arm, gt = m
        per.setdefault(rd, {})[(B, arm)] = (esp[idx], rmu[idx], gt)
        idx += 1
    for rd in recs:
        d = per[rd]; gt = d[(-1, "clean")][2]
        ce, cr, _ = d[(-1, "clean")]
        print(f"\n{rd.split('/dev/')[-1]:<28} GT={gt:+.1f}°  clean esprit={ce:+.1f}° rootmusic={cr:+.1f}°")
        print(f"  {'budget':>6} {'arm':<14} {'bits':>5} {'reconMSE':>9} {'|DOAerr| esp':>12} {'rmu':>7}")
        for B in budgets:
            for arm in arms:
                e, r, _ = d[(B, arm)]
                mse, bits = recon[(rd, B)][arm]
                print(f"  {B:>6} {arm:<14} {bits:>5} {mse:>9.3f} {abs(e-gt):>12.1f} {abs(r-gt):>7.1f}")
            # flip check at this budget (esprit)
            de = {arm: abs(d[(B, arm)][0] - gt) for arm in arms}
            rc = {arm: recon[(rd, B)][arm][0] for arm in arms}
            flip = de["polarquant"] <= de["scalar"] <= de["phase_destroy"] and rc["scalar"] <= rc["polarquant"]
            print(f"         -> flip(esprit): {'YES' if flip else 'no '}  "
                  f"(DOA pq<scal<pd, reconMSE scal<pq)")


if __name__ == "__main__":
    main()
