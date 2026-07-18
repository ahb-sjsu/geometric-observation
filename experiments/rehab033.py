# GO-P-2026-033 honest rehabilitation of the real-data DOA flip.
#
# Fixes the two genuine weaknesses of the GO-P-2026-032 miss:
#   (1) single-bin under-powering  -> incoherent WIDEBAND MUSIC (many bins, correct per-bin steering)
#   (2) a non-optimal recon baseline -> LLOYD-MAX (fixed-rate reconstruction-optimal) instead of uniform
# Method + config are developed on SEEN data (dev/task1 + eval/task1), then FROZEN + sealed, then
# confirmed on FRESH held-out eval/task2 (unused). Multi-source there is handled by fixing the
# reference to the dominant source identified on the CLEAN data (both arms scored vs the same source).
#
#   --develop                 : config sweep on seen data (method selection; prints the map)
#   --confirm AP BITS FLO FHI : fixed config on eval/task2 (governed held-out run)
import sys
import numpy as np
from scipy.signal import stft
import scipy.io.wavfile as wf


# ---- PolarQuant transform (turboquant-pro; Han et al. 2502.02617) ----
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
    o = np.zeros((V.shape[0], p)); o[:, :d] = V
    return o, d


C = 343.0
APERTURE = {0: ([4, 5, 6, 8, 9], 0.04), 1: ([3, 4, 6, 9, 10], 0.08), 2: ([2, 3, 6, 10, 11], 0.16)}
SEEN = ([f"/archive/locata/dev/task1/recording{r}/dicit" for r in (1, 2, 3)]
        + [f"/archive/locata/eval/task1/recording{r}/dicit" for r in range(1, 14)])
HELDOUT = sorted(__import__("glob").glob("/archive/locata/eval/task2/recording*/dicit"),
                 key=lambda s: int(s.split("recording")[1].split("/")[0]))
_GRID = np.deg2rad(np.arange(-85, 85.25, 0.25))


def lloyd1d(x, bits, iters=12):
    lv = np.quantile(x, (np.arange(2 ** bits) + 0.5) / 2 ** bits)
    for _ in range(iters):
        bnd = (lv[:-1] + lv[1:]) / 2
        idx = np.searchsorted(bnd, x)
        for k in range(len(lv)):
            m = idx == k
            if m.any():
                lv[k] = x[m].mean()
    return lv[np.searchsorted((lv[:-1] + lv[1:]) / 2, x)]


def _row(path):
    L = open(path).read().splitlines()
    return dict(zip(L[0].split("\t"), np.array(L[1].split("\t"), float)))


def load_wb3(array_dir, mic_idx, f_lo, f_hi, energy_pct=50):
    d = _row(array_dir + "/position_array_dicit.txt")
    ref = np.array([d["x"], d["y"], d["z"]])
    Rot = np.array([[d["rotation_%d%d" % (i, j)] for j in (1, 2, 3)] for i in (1, 2, 3)])
    mics = np.array([[d["mic%d_%s" % (i, ax)] for ax in "xyz"] for i in range(1, 16)])
    p = ((mics - ref) @ Rot)[mic_idx, 0]
    import glob
    ths = []
    for sf_ in sorted(glob.glob(array_dir + "/position_source_*.txt")):
        sd = _row(sf_)
        ls = (np.array([sd["x"], sd["y"], sd["z"]]) - ref) @ Rot
        ths.append(np.arctan2(ls[1], ls[0]) - np.pi / 2)
    rate, a = wf.read(array_dir + "/audio_array_dicit.wav")
    a = a[:, mic_idx].astype(float)
    Z = np.stack([stft(a[:, m], fs=rate, nperseg=1024, noverlap=512)[2] for m in range(len(mic_idx))], 0)
    fb = stft(a[:, 0], fs=rate, nperseg=1024, noverlap=512)[0]
    bins = np.where((fb >= f_lo) & (fb <= f_hi))[0]
    en = np.sum(np.abs(Z[:, bins, :]) ** 2, axis=(0, 1))
    act = en >= np.percentile(en, energy_pct)
    X3 = Z[:, bins, :][:, :, act].transpose(0, 2, 1)
    for b in range(X3.shape[2]):
        X3[:, :, b] /= (np.sqrt(np.mean(np.abs(X3[:, :, b]) ** 2)) + 1e-30)
    return X3, p, fb[bins], np.array(ths)


def wb_music(X3, p, freqs):
    M, T, B = X3.shape
    Ps = np.zeros(len(_GRID))
    for b in range(B):
        Xb = X3[:, :, b]; _w, V = np.linalg.eigh((Xb @ Xb.conj().T) / T); Un = V[:, :M - 1]
        A = np.exp(-1j * 2 * np.pi * freqs[b] * np.outer(p, np.sin(_GRID)) / C)
        Ps += 1.0 / (np.sum(np.abs(Un.conj().T @ A) ** 2, 0) + 1e-30)
    k = int(np.argmax(Ps))
    if 0 < k < len(_GRID) - 1:
        y0, y1, y2 = Ps[k - 1], Ps[k], Ps[k + 1]
        return _GRID[k] + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-30) * (_GRID[1] - _GRID[0])
    return _GRID[k]


def compress3(X3, budget):
    M, T, B = X3.shape
    Xc = X3.transpose(1, 2, 0).reshape(T * B, M)
    Xr = np.concatenate([Xc.real, Xc.imag], 1)
    Xp, d = _pad(Xr); D = Xp.shape[1]
    def back(real2m):
        cc = real2m[:, :M] + 1j * real2m[:, M:]
        return cc.reshape(T, B, M).transpose(2, 0, 1)
    out = {}
    ab = max(1, round((budget - 4) / (D - 1)))
    r, ang = polar_encode(Xp); lr = np.log(np.maximum(r, 1e-20))
    out["pq"] = back(polar_decode(np.exp(_qu(lr, lr.min(), lr.max(), 4)),
                                  [_qu(t, -np.pi, np.pi, ab) for t in ang])[:, :2 * M])
    qb = max(1, round(budget / D)); rl = np.empty_like(Xp)
    for j in range(D):
        rl[:, j] = lloyd1d(Xp[:, j], qb)
    out["lloyd"] = back(rl[:, :2 * M])
    mb = max(1, round(budget / M - 1))
    lrr = np.log(np.maximum(np.abs(Xc), 1e-20))
    pdc = np.exp(_qu(lrr, lrr.min(), lrr.max(), mb)) * np.exp(1j * _qu(np.angle(Xc), -np.pi, np.pi, 1))
    out["phase_destroy"] = pdc.reshape(T, B, M).transpose(2, 0, 1)
    res = {}
    for k, Xh in out.items():
        res[k] = (Xh, float(np.mean(np.sum(np.abs(X3 - Xh) ** 2, 0))))
    return res


def flip_on(recs, ap, budget, f_lo, f_hi):
    mic_idx, dsp = APERTURE[ap]
    holds = anti = recon = 0; fails = []; n = 0
    for rd in recs:
        try:
            X3, p, freqs, ths = load_wb3(rd, mic_idx, f_lo, f_hi)
            if X3.shape[1] < 15:
                continue
            th_ref = ths[int(np.argmin(np.abs(ths - wb_music(X3, p, freqs))))]   # dominant src (clean)
            cx = compress3(X3, budget)
            de = {a: abs(np.rad2deg(wb_music(cx[a][0], p, freqs) - th_ref)) for a in cx}
            pqr, lqr = cx["pq"][1], cx["lloyd"][1]
            holds += (de["pq"] <= de["lloyd"] + 0.5) and (lqr <= pqr)
            anti += de["phase_destroy"] >= max(de["pq"], de["lloyd"])
            recon += lqr <= pqr
            fails.append(max(0.0, de["pq"] - de["lloyd"])); n += 1
        except Exception as e:
            print("  skip", rd.split("/")[-2], type(e).__name__, e)
    return dict(n=n, holds=holds, anti=anti, recon=recon, med=float(np.median(fails)) if fails else 9.9)


def main():
    if "--develop" in sys.argv:
        print("DEVELOP (method selection on SEEN data: dev/task1 + eval/task1)")
        for ap in (0, 1, 2):
            _mi, dsp = APERTURE[ap]; fh = C / (2 * dsp)
            for bits in (48, 64):
                r = flip_on(SEEN, ap, bits, 0.35 * fh, 0.98 * fh)
                print(f"  aperture={ap}({dsp*100:.0f}cm) band={0.35*fh:.0f}-{0.98*fh:.0f}Hz bits={bits}: "
                      f"flip {r['holds']}/{r['n']} | anti {r['anti']}/{r['n']} | recon {r['recon']}/{r['n']} "
                      f"| median flip_fail {r['med']:.2f}")
        return
    if "--confirm" in sys.argv:
        i = sys.argv.index("--confirm")
        ap, bits, flo, fhi = int(sys.argv[i+1]), int(sys.argv[i+2]), float(sys.argv[i+3]), float(sys.argv[i+4])
        print(f"CONFIRM (held-out eval/task2, n={len(HELDOUT)}): aperture={ap} bits={bits} band={flo:.0f}-{fhi:.0f}Hz")
        r = flip_on(HELDOUT, ap, bits, flo, fhi)
        print(f"  clean flip holds {r['holds']}/{r['n']} | median flip_fail {r['med']:.2f}° "
              f"| anti worst {r['anti']}/{r['n']} | recon(lloyd<=pq) {r['recon']}/{r['n']}")
        checks = {"flip >= 8/13": r["holds"] >= 8, "median <= 1.5deg": r["med"] <= 1.5,
                  "anti worst >= 10/13": r["anti"] >= 10, "recon lloyd<=pq >= 10/13": r["recon"] >= 10}
        for k, v in checks.items():
            print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        print(f"\nVERDICT: {'CONFIRMED' if all(checks.values()) else 'NOT CONFIRMED (honest negative)'}")


if __name__ == "__main__":
    main()
