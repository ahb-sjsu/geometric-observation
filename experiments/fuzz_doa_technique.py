# Structural-fuzzing search for a real-data DOA technique that shows the consumer-relative flip.
#
# DISCIPLINE (a light in dark places, honestly): the config space is SEARCHED on CALIBRATION
# recordings only; the whole robustness map is reported (not one cherry-picked point); any selected
# region is then pre-registered and validated on HELD-OUT recordings (separate step). Uses the
# user's structural-fuzzing package for sensitivity + adversarial-threshold analysis.
#
# Config axes: bandwidth (# pooled STFT bins), aperture (which DICIT ULA), total bits/snapshot,
# energy-selection %. Objective: the matched-bit flip = angle-favoring PolarQuant beats
# reconstruction-optimal scalar on DOA (flip_fail = max(0, doa_err_polarquant - doa_err_scalar)).
# Consumer for the SEARCH = numpy MUSIC (fast); held-out confirmation uses mature MATLAB ESPRIT.
import sys
import numpy as np
from scipy.signal import stft
import scipy.io.wavfile as wf

import structural_fuzzing as sf

C = 343.0
# aperture -> (mic channels, frequency for exactly lambda/2)
APERTURE = {0: ([4, 5, 6, 8, 9], 343.0 / (2 * 0.04)),      # 4 cm ULA, 4287 Hz
            1: ([3, 4, 6, 9, 10], 343.0 / (2 * 0.08)),     # 8 cm ULA, 2144 Hz
            2: ([2, 3, 6, 10, 11], 343.0 / (2 * 0.16))}    # 16 cm ULA, 1072 Hz
CAL = [f"/archive/locata/dev/task1/recording{r}/dicit" for r in (1, 2, 3)]


def polar_encode(X):
    angles = []; v = X
    while v.shape[1] > 1:
        a, b = v[:, 0::2], v[:, 1::2]; angles.append(np.arctan2(b, a)); v = np.sqrt(a * a + b * b)
    return v[:, 0], angles


def polar_decode(radius, angles):
    v = radius[:, None]
    for th in reversed(angles):
        a, b = v * np.cos(th), v * np.sin(th)
        nv = np.empty((v.shape[0], 2 * v.shape[1])); nv[:, 0::2], nv[:, 1::2] = a, b; v = nv
    return v


def _qu(x, lo, hi, bits):
    lv = 2 ** bits; step = (hi - lo) / max(lv, 1)
    return lo + (np.clip(np.floor((x - lo) / (step + 1e-30)), 0, lv - 1) + 0.5) * step


def _pad(V):
    d = V.shape[1]; p = 1
    while p < d:
        p *= 2
    if p == d:
        return V, d
    o = np.zeros((V.shape[0], p)); o[:, :d] = V; return o, d


def compress(X, budget):
    M, T = X.shape
    Xr = np.concatenate([X.real, X.imag], 0).T
    Xp, d = _pad(Xr); D = Xp.shape[1]
    out = {}
    ab = max(1, round((budget - 4) / (D - 1)))
    r, ang = polar_encode(Xp); lr = np.log(np.maximum(r, 1e-20))
    rec = polar_decode(np.exp(_qu(lr, lr.min(), lr.max(), 4)), [_qu(t, -np.pi, np.pi, ab) for t in ang])[:, :2 * M]
    out["pq"] = rec[:, :M].T + 1j * rec[:, M:].T
    qb = max(1, round(budget / D)); sc = np.empty_like(Xp)
    for j in range(D):
        sc[:, j] = _qu(Xp[:, j], Xp[:, j].min(), Xp[:, j].max(), qb)
    sc = sc[:, :2 * M]; out["scalar"] = sc[:, :M].T + 1j * sc[:, M:].T
    res = {}
    for k, Xh in out.items():
        res[k] = (Xh, float(np.mean(np.sum(np.abs(X - Xh) ** 2, 0))))
    return res


_GRID = np.deg2rad(np.arange(-80, 80.25, 0.25))


def music(R, p, f):
    M = R.shape[0]; _w, V = np.linalg.eigh(R); Un = V[:, :M - 1]
    A = np.exp(-1j * 2 * np.pi * f * np.outer(p, np.sin(_GRID)) / C)
    Pm = 1.0 / (np.sum(np.abs(Un.conj().T @ A) ** 2, 0) + 1e-30)
    k = int(np.argmax(Pm))
    if 0 < k < len(_GRID) - 1:
        y0, y1, y2 = Pm[k - 1], Pm[k], Pm[k + 1]
        return _GRID[k] + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-30) * (_GRID[1] - _GRID[0])
    return _GRID[k]


def _row(path):
    L = open(path).read().splitlines()
    return dict(zip(L[0].split("\t"), np.array(L[1].split("\t"), float)))


def load_wb(array_dir, mic_idx, f_center, n_bins, energy_pct):
    d = _row(array_dir + "/position_array_dicit.txt")
    ref = np.array([d["x"], d["y"], d["z"]])
    Rot = np.array([[d["rotation_%d%d" % (i, j)] for j in (1, 2, 3)] for i in (1, 2, 3)])
    mics = np.array([[d["mic%d_%s" % (i, ax)] for ax in "xyz"] for i in range(1, 16)])
    p = ((mics - ref) @ Rot)[mic_idx, 0]
    import glob
    sd = _row(glob.glob(array_dir + "/position_source_*.txt")[0])
    ls = (np.array([sd["x"], sd["y"], sd["z"]]) - ref) @ Rot
    theta0 = np.arctan2(ls[1], ls[0]) - np.pi / 2
    rate, a = wf.read(array_dir + "/audio_array_dicit.wav"); a = a[:, mic_idx].astype(float)
    Z = np.stack([stft(a[:, m], fs=rate, nperseg=1024, noverlap=512)[2] for m in range(len(mic_idx))], 0)
    fb = stft(a[:, 0], fs=rate, nperseg=1024, noverlap=512)[0]
    b0 = int(np.argmin(np.abs(fb - f_center))); h = n_bins // 2
    bins = range(max(0, b0 - h), min(len(fb), b0 + h + 1))
    en = np.sum(np.abs(Z[:, b0, :]) ** 2, 0); act = en >= np.percentile(en, energy_pct)
    X = np.concatenate([Z[:, bb, act] for bb in bins], 1)
    X = X / (np.sqrt(np.mean(np.abs(X) ** 2)) + 1e-30)
    return X, p, f_center, theta0


def flip_score(n_bins, aperture, total_bits, energy_pct, recs=CAL):
    mic_idx, f = APERTURE[int(np.clip(round(aperture), 0, 2))]
    errs = {}
    for rd in recs:
        try:
            X, p, fc, th0 = load_wb(rd, mic_idx, f, int(max(1, round(n_bins))), float(np.clip(energy_pct, 0, 90)))
            if X.shape[1] < 20:
                errs[rd] = 5.0; continue
            cx = compress(X, int(np.clip(round(total_bits), 12, 96)))
            de = {}
            for arm in ("pq", "scalar"):
                Xh, _mse = cx[arm]
                de[arm] = abs(np.rad2deg(music((Xh @ Xh.conj().T) / Xh.shape[1], p, fc) - th0))
            errs[rd.split("/dev/")[-1][:20]] = max(0.0, de["pq"] - de["scalar"])   # 0 when flip holds
        except Exception:
            errs[rd.split("/dev/")[-1][:20]] = 5.0
    mae = float(np.mean(list(errs.values())))
    return mae, errs


def evaluate_fn(params):
    return flip_score(params[0], params[1], params[2], params[3])


def main():
    dim_names = ["bandwidth", "aperture", "total_bits", "energy_pct"]
    grid = [(nb, ap, tb, ep) for nb in (1, 3, 7, 15, 25) for ap in (0, 1, 2)
            for tb in (32, 48, 64, 80) for ep in (0, 40, 70)]
    print(f"searching {len(grid)} configs on {len(CAL)} calibration recordings ...")
    rows = []
    for cfg in grid:
        mae, _ = flip_score(*cfg)
        rows.append((mae, cfg))
    rows.sort()
    print("\n=== robustness map (flip_fail = deg by which PolarQuant loses to scalar on DOA; 0 = flip holds) ===")
    print("best configs (flip holds most robustly across calibration):")
    for mae, cfg in rows[:8]:
        print(f"  flip_fail={mae:5.2f}  bandwidth={cfg[0]:>2} aperture={cfg[1]} bits={cfg[2]:>2} energy%={cfg[3]:>2}")
    print("worst configs (flip fails):")
    for mae, cfg in rows[-4:]:
        print(f"  flip_fail={mae:5.2f}  bandwidth={cfg[0]:>2} aperture={cfg[1]} bits={cfg[2]:>2} energy%={cfg[3]:>2}")
    holds = sum(1 for m, _ in rows if m <= 0.5)
    print(f"\nconfigs where the flip holds (flip_fail<=0.5): {holds}/{len(rows)}")

    best = np.array(rows[0][1], float)
    print(f"\n=== structural-fuzzing sensitivity around best config {rows[0][1]} ===")
    for s in sf.sensitivity_profile(best, dim_names, evaluate_fn):
        print(f"  {s}")


if __name__ == "__main__":
    main()
