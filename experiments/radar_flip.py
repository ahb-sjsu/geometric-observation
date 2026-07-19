# GO-P-2026-034 D1 -- radar DOA consumer-relative flip (RaDICaL; ELECTROMAGNETIC physics).
#
# Reuses the EXACT matched-bit three-arm compressor from GO-P-2026-033 (compress3: pq / lloyd /
# phase_destroy) -- bit-identical to the confirmed LOCATA run; only the domain front-end changes.
#
# Array   : RaDICaL indoor -- 4 RX x 2 TX (TX0,TX2) = 8 virtual elements, lambda/2 ULA (from cfg).
# Consumer: narrowband MUSIC (single source) on the 8-element covariance -- the mature high-res
#           estimator, matching the LOCATA consumer choice.
# Reference: the consumer's OWN uncompressed estimate (score the compression-induced displacement).
#           WHY (amendment to 034 D1, reasoned from the sample BEFORE any held-out flip is scored):
#           the 8-element array has ~15 deg azimuth resolution, so an absolute camera/lidar GT is
#           dominated by the array's own resolution noise and would swamp the compression flip. The
#           reviewer-endorsed corrected-LOCATA protocol (GO-P-2026-033 correction) scores displacement
#           from the consumer's own clean estimate -- the common resolution noise cancels across arms.
#           Camera depth-azimuth is retained as an independent VALIDITY cross-check (the uncompressed
#           MUSIC must correlate with the depth-derived source azimuth).
#
#   --develop H5              : config sweep (budget x sharpness) on calibration frames; prints the map
#   --confirm H5 BITS SHARP   : frozen config on held-out frames (governed run)
import sys
import numpy as np
import h5py
from rehab033 import compress3          # identical matched-bit compressor (pq / lloyd / phase_destroy)

M = 8                                    # 4 RX x 2 TX virtual elements
_ULA = np.arange(M)                      # lambda/2 spacing -> steering exp(-j pi m sin th)
_GRID = np.deg2rad(np.arange(-60, 60.05, 0.1))
_A = np.exp(-1j * np.pi * np.outer(_ULA, np.sin(_GRID)))
RES = 0.047                              # metres per range bin (indoor_human_rcs.cfg)
HFOV = 87.0                              # depth camera horizontal FoV (deg) -- cross-check only


def music(X):
    """X: (M, T) narrowband snapshots -> azimuth (deg), single dominant source, parabolic-refined."""
    T = X.shape[1]
    R = (X @ X.conj().T) / T
    _w, V = np.linalg.eigh(R)
    Un = V[:, :M - 1]                    # noise subspace (single source)
    Ps = 1.0 / (np.sum(np.abs(Un.conj().T @ _A) ** 2, 0) + 1e-30)
    k = int(np.argmax(Ps))
    if 0 < k < len(_GRID) - 1:
        y0, y1, y2 = Ps[k - 1], Ps[k], Ps[k + 1]
        return np.rad2deg(_GRID[k] + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-30) * (_GRID[1] - _GRID[0]))
    return np.rad2deg(_GRID[k])


def _sharpness(X):
    R = (X @ X.conj().T) / X.shape[1]
    _w, V = np.linalg.eigh(R); Un = V[:, :M - 1]
    Ps = 1.0 / (np.sum(np.abs(Un.conj().T @ _A) ** 2, 0) + 1e-30)
    return Ps.max() / np.median(Ps)


def load_frame(R, D, fr):
    """Range-FFT, pick the dominant range bin (CFAR-style), return unit-power 8xT snapshots,
    the MUSIC sharpness, and the depth-derived source azimuth (cross-check)."""
    cube = np.asarray(R[fr])                              # (T=32, M=8, fast=304)
    rng = np.fft.fft(cube, axis=2)
    pw = np.mean(np.abs(rng[:, :, 8:200]) ** 2, axis=(0, 1))
    rb = 8 + int(np.argmax(pw))
    X = rng[:, :, rb].T                                   # (M, T)
    X = X / (np.sqrt(np.mean(np.abs(X) ** 2)) + 1e-30)    # unit power (LOCATA discipline)
    az_c = np.nan
    d = np.asarray(D[fr]).astype(float); dv = d[d > 300]
    if dv.size > 500:
        near = np.percentile(dv, 3); mask = (d > 300) & (d < near + 700); s = mask.sum()
        if s > 0:
            az_c = (((np.arange(1280)[None, :] * mask).sum() / s) - 640) / 640 * (HFOV / 2)
    return X, _sharpness(X), az_c


def flip_on(frames, R, D, budget, sharp_min, tol=0.5):
    holds = anti = recon = n = 0; fails = []; azr = []; azc = []
    for fr in frames:
        X, sharp, az_c = load_frame(R, D, fr)
        if sharp < sharp_min:
            continue
        ref = music(X)                                   # consumer's own uncompressed estimate
        cx = compress3(X[:, :, None], budget)            # (M, T, 1) narrowband -> 3 arms
        de = {a: abs(music(cx[a][0][:, :, 0]) - ref) for a in cx}
        pqr, lqr = cx["pq"][1], cx["lloyd"][1]           # reconstruction MSE
        holds += (de["pq"] <= de["lloyd"] + tol) and (lqr <= pqr)
        anti += de["phase_destroy"] >= max(de["pq"], de["lloyd"])
        recon += lqr <= pqr
        fails.append(max(0.0, de["pq"] - de["lloyd"])); n += 1
        azr.append(ref); azc.append(az_c)
    azr = np.array(azr); azc = np.array(azc); mfin = np.isfinite(azc)
    xcorr = float(np.corrcoef(azr[mfin], azc[mfin])[0, 1]) if mfin.sum() > 3 else float("nan")
    return dict(n=n, holds=holds, anti=anti, recon=recon,
                med=float(np.median(fails)) if fails else 9.9, xcorr=xcorr)


def main():
    h5 = sys.argv[sys.argv.index("--develop" if "--develop" in sys.argv else "--confirm") + 1]
    f = h5py.File(h5, "r"); R, D = f["radar"], f["depth"]
    N = R.shape[0]
    cal = list(range(0, N // 2))          # calibration = first half; held-out = second half
    hld = list(range(N // 2, N))
    if "--develop" in sys.argv:
        print(f"DEVELOP (calibration frames 0..{N//2-1} of {h5.split('/')[-1]})")
        for budget in (24, 32, 48, 64):
            for sm in (6, 10, 15):
                r = flip_on(cal, R, D, budget, sm)
                print(f"  bits={budget:2d} sharp>={sm:2d}: flip {r['holds']:2d}/{r['n']:2d} | "
                      f"anti {r['anti']:2d}/{r['n']:2d} | recon {r['recon']:2d}/{r['n']:2d} | "
                      f"med {r['med']:.2f} | xcorr(cam) {r['xcorr']:+.2f}")
        return
    if "--confirm" in sys.argv:
        i = sys.argv.index("--confirm")
        budget, sharp = int(sys.argv[i + 2]), float(sys.argv[i + 3])
        r = flip_on(hld, R, D, budget, sharp)
        print(f"CONFIRM (held-out frames {N//2}..{N-1}): bits={budget} sharp>={sharp}")
        print(f"  clean flip {r['holds']}/{r['n']} | median flip_fail {r['med']:.2f}deg | "
              f"anti worst {r['anti']}/{r['n']} | recon(lloyd<=pq) {r['recon']}/{r['n']} | "
              f"cam xcorr {r['xcorr']:+.2f}")
        frac = (lambda a, b: a / b if b else 0)
        checks = {"clean flip >= 60%": frac(r["holds"], r["n"]) >= 0.60,
                  "recon-trade >= 60%": frac(r["recon"], r["n"]) >= 0.60,
                  "anti worst >= 70%": frac(r["anti"], r["n"]) >= 0.70,
                  "cam cross-check |xcorr|>=0.4": abs(r["xcorr"]) >= 0.4}
        for k, v in checks.items():
            print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        print(f"\nVERDICT: {'CONFIRMED' if all(checks.values()) else 'NOT CONFIRMED (honest negative)'}")


if __name__ == "__main__":
    main()
