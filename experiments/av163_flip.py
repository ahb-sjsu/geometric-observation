# GO-P-2026-034 D2 -- second acoustic corpus (AV16.3), INDEPENDENT of LOCATA (different array,
# room, speakers, corpus). Within-domain robustness of the consumer-relative flip.
#
# Array   : AV16.3 array1 -- 8-mic UNIFORM CIRCULAR array (r=0.1 m), positions from the corpus README.
# Consumer: incoherent WIDEBAND MUSIC generalised to the 2D circular geometry (single source/window).
# GROUND TRUTH: the corpus's precise 3D-mouth location (camera-tracked, max err 1.2 cm) -> ABSOLUTE
#   azimuth at the array-1 centre. The 8-mic array's good resolution + precise GT support an absolute
#   reference here (unlike D1's tiny array) -- this is 034's sealed D2 protocol ("tracked source DOA").
# The speaker MOVES, so DOA is estimated per short time WINDOW, each synced to the GT azimuth at its
# centre time. Reuses compress3 from rehab033 (bit-identical matched-bit three-arm compressor).
#
#   --verify SEQ             : uncompressed MUSIC vs GT azimuth across windows (validity of the array/GT)
#   --develop                : config sweep on calibration sequences
#   --confirm WIN BAND BUD   : frozen config on held-out sequences
import json
import sys
import numpy as np
from scipy.signal import stft
import scipy.io.wavfile as wf
from rehab033 import compress3

C = 343.0
_ang = np.pi * (-1 + 2 * np.arange(8) / 8.0)        # array1 mic angles (README formula)
PX = 0.1 * np.cos(_ang); PY = 0.1 * np.sin(_ang)    # array1 mic (x,y), centre-relative
ACX, ACY = 0.0, 0.4                                 # array1 centre in the corpus 3D frame
_GRID = np.deg2rad(np.arange(-180, 180, 1.0))   # 1 deg grid (relative flip; keeps MUSIC cheap)
_PROJ = np.outer(PX, np.cos(_GRID)) + np.outer(PY, np.sin(_GRID))   # (M, G) far-field path term

DATA = "/home/claude/av163"
CAL = ["seq01-1p-0000", "seq02-1p-0000"]                        # calibration sequences
HELDOUT = ["seq03-1p-0000", "seq11-1p-0100", "seq15-1p-0100"]  # disjoint held-out sequences


def load_audio(seq):
    ch = []
    for m in range(1, 9):
        rate, a = wf.read(f"{DATA}/{seq}/a1_mic{m}.wav")
        ch.append(a.astype(float))
    L = min(len(c) for c in ch)
    return rate, np.stack([c[:L] for c in ch], 0)               # (8, L)


def load_gt(seq):
    g = np.loadtxt(f"{DATA}/{seq}/mouth.gt")                    # t, id, x, y, z
    return g[:, 0], np.arctan2(g[:, 3] - ACY, g[:, 2] - ACX)    # azimuth rel array1 centre


def wb_music_2d(X3, freqs):
    M, T, B = X3.shape
    Ps = np.zeros(len(_GRID))
    for b in range(B):
        Xb = X3[:, :, b]; _w, V = np.linalg.eigh((Xb @ Xb.conj().T) / T); Un = V[:, :M - 1]
        A = np.exp(1j * 2 * np.pi * freqs[b] * _PROJ / C)      # +j: source-lead convention (verified)
        Ps += 1.0 / (np.sum(np.abs(Un.conj().T @ A) ** 2, 0) + 1e-30)
    k = int(np.argmax(Ps))
    if 0 < k < len(_GRID) - 1:
        y0, y1, y2 = Ps[k - 1], Ps[k], Ps[k + 1]
        return _GRID[k] + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-30) * (_GRID[1] - _GRID[0])
    return _GRID[k]


def windows(seq, win, f_lo, f_hi, energy_pct=70):
    """Yield (X3 (M,T,Bbins), freqs, gt_azimuth) for high-energy windows synced to GT time.
    STFT the whole sequence once, then slice windows in the STFT-frame domain (robust)."""
    rate, A = load_audio(seq); tg, azg = load_gt(seq)
    nper = 512; hop = 256
    f0, t0, _z = stft(A[0], fs=rate, nperseg=nper, noverlap=nper - hop)
    Zf = np.stack([stft(A[m], fs=rate, nperseg=nper, noverlap=nper - hop)[2] for m in range(8)], 0)
    bins = np.where((f0 >= f_lo) & (f0 <= f_hi))[0]
    Zb = Zf[:, bins, :]; fq = f0[bins]                         # (8, Bbins, Tframes)
    half = win / 2
    centers = np.arange(tg[0] + half, min(tg[-1], t0[-1]) - half, half)
    e_list = []; packs = []
    for tc in centers:
        idx = np.where((t0 >= tc - half) & (t0 < tc + half))[0]
        if len(idx) < 8:
            continue
        Zw = Zb[:, :, idx]                                     # (8, Bbins, Tw)
        e_list.append(np.sum(np.abs(Zw) ** 2))
        packs.append((float(np.interp(tc, tg, azg)), Zw))
    if not e_list:
        return
    thr = np.percentile(e_list, energy_pct)
    for e, (az, Zw) in zip(e_list, packs):
        if e < thr:
            continue
        X3 = Zw.transpose(0, 2, 1).copy()                     # (M, Tw, B)
        for b in range(X3.shape[2]):
            X3[:, :, b] /= (np.sqrt(np.mean(np.abs(X3[:, :, b]) ** 2)) + 1e-30)
        yield X3, fq, az


def flip_on(seqs, win, f_lo, f_hi, budget, tol=1.0):
    # Flip is scored vs the consumer's OWN uncompressed estimate (isolates the compression effect;
    # the ~20deg absolute array/reverb noise cancels across arms). The precise tracked mouth GT is the
    # VALIDITY cross-check (does the uncompressed consumer read the true direction?).
    # Score the flip TWO ways: (rel) vs the consumer's own uncompressed estimate, and (abs) vs the
    # precise tracked mouth GT (the sealed D2 protocol). recon-trade is identical (raw-signal MSE).
    holds = anti = recon = n = 0; fails = []; refs = []; gts = []
    holds_abs = anti_abs = 0; dump = []
    for seq in seqs:
        for X3, fq, az_true in windows(seq, win, f_lo, f_hi):
            ref = np.rad2deg(wb_music_2d(X3, fq)); gtd = np.rad2deg(az_true)
            cx = compress3(X3, budget)
            mus = {a: np.rad2deg(wb_music_2d(cx[a][0], fq)) for a in cx}
            de = {a: abs(((mus[a] - ref + 180) % 360) - 180) for a in cx}          # vs uncompressed
            dg = {a: abs(((mus[a] - gtd + 180) % 360) - 180) for a in cx}          # vs tracked GT
            pqr, lqr = cx["pq"][1], cx["lloyd"][1]
            holds += (de["pq"] <= de["lloyd"] + tol) and (lqr <= pqr)
            anti += de["phase_destroy"] >= max(de["pq"], de["lloyd"])
            holds_abs += (dg["pq"] <= dg["lloyd"] + tol) and (lqr <= pqr)
            anti_abs += dg["phase_destroy"] >= max(dg["pq"], dg["lloyd"])
            recon += lqr <= pqr
            fails.append(max(0.0, de["pq"] - de["lloyd"])); n += 1
            refs.append(ref); gts.append(gtd)
            # per-window paired errors + recording label, for the clustered bootstrap:
            dump.append([seq, float(de["pq"]), float(de["lloyd"]), float(de["phase_destroy"])])
    refs = np.array(refs); gts = np.array(gts)
    gterr = float(np.median(np.abs(((refs - gts + 180) % 360) - 180))) if n else 9.9
    gtcorr = float(np.corrcoef(refs, gts)[0, 1]) if n > 3 else float("nan")
    return dict(n=n, holds=holds, anti=anti, recon=recon, holds_abs=holds_abs, anti_abs=anti_abs,
                med=float(np.median(fails)) if fails else 9.9, gterr=gterr, gtcorr=gtcorr, dump=dump)


def main():
    if "--verify" in sys.argv:
        seq = sys.argv[sys.argv.index("--verify") + 1]
        mus = []; gt = []
        for X3, fq, az in windows(seq, 0.75, 500, 2500):
            mus.append(np.rad2deg(wb_music_2d(X3, fq))); gt.append(np.rad2deg(az))
        mus = np.array(mus); gt = np.array(gt)
        err = ((mus - gt + 180) % 360) - 180
        print(f"{seq}: n={len(mus)} windows | median|MUSIC-GT|={np.median(np.abs(err)):.1f} deg | "
              f"corr={np.corrcoef(mus, gt)[0,1]:+.3f} | GT az range [{gt.min():.0f},{gt.max():.0f}]")
        return
    if "--develop" in sys.argv:
        print("DEVELOP (calibration sequences: " + ", ".join(CAL) + ")", flush=True)
        for win in (0.75,):
            for band in ((500, 2500), (700, 3500)):
                for bud in (48, 64):
                    r = flip_on(CAL, win, band[0], band[1], bud)
                    print(f"  win={win} band={band[0]}-{band[1]} bits={bud}: "
                          f"flip_rel {r['holds']:3d}/{r['n']:3d} flip_abs {r['holds_abs']:3d}/{r['n']:3d} "
                          f"| anti_rel {r['anti']:3d} anti_abs {r['anti_abs']:3d} | recon {r['recon']:3d}/{r['n']:3d} "
                          f"| GT corr {r['gtcorr']:+.2f} err {r['gterr']:.0f}", flush=True)
        return
    if "--dump" in sys.argv:
        # per-window paired errors + recording label on the frozen held-out config,
        # for a recording-clustered bootstrap (win=0.75 band=500-2500 bits=64).
        r = flip_on(HELDOUT, 0.75, 500.0, 2500.0, 64)
        print("###DUMP_JSON_START###")
        print(json.dumps(r["dump"]))
        print("###DUMP_JSON_END###")
        return
    if "--confirm" in sys.argv:
        i = sys.argv.index("--confirm")
        win = float(sys.argv[i + 1]); band = sys.argv[i + 2]; bud = int(sys.argv[i + 3])
        f_lo, f_hi = [float(x) for x in band.split("-")]
        r = flip_on(HELDOUT, win, f_lo, f_hi, bud)
        print(f"CONFIRM (held-out {HELDOUT}): win={win} band={band} bits={bud}, n={r['n']}")
        print(f"  flip_abs(vs tracked GT) {r['holds_abs']}/{r['n']} | flip_rel(vs uncompressed) {r['holds']}/{r['n']} | "
              f"median flip_fail {r['med']:.2f}deg")
        print(f"  anti_abs {r['anti_abs']}/{r['n']} | anti_rel {r['anti']}/{r['n']} | recon(lloyd<=pq) {r['recon']}/{r['n']} | "
              f"GT xcheck corr {r['gtcorr']:+.2f} err {r['gterr']:.0f}deg")
        frac = lambda a, b: a / b if b else 0
        checks = {"clean flip (vs tracked GT) >= 60%": frac(r["holds_abs"], r["n"]) >= 0.60,
                  "recon-trade >= 60%": frac(r["recon"], r["n"]) >= 0.60,
                  "anti worst (vs GT) >= 70%": frac(r["anti_abs"], r["n"]) >= 0.70}
        for k, v in checks.items():
            print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        print(f"\nVERDICT (sealed absolute-GT protocol): "
              f"{'CONFIRMED' if all(checks.values()) else 'NOT CONFIRMED (honest negative)'}")


if __name__ == "__main__":
    main()
