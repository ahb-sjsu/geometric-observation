# GO-P-2026-034 D3 -- seismic array backazimuth (PDAR IMS array), teleseismic P waves.
# GEOPHYSICS: elastic waves, natural earthquake sources -- a DIFFERENT physics again.
#
# Array   : PDAR (network IM), 13-element short-period array PD01..PD13, aperture ~3.2 km.
# Consumer: incoherent WIDEBAND MUSIC over BACKAZIMUTH at the theoretical teleseismic-P slowness
#           (single plane-wave source) -- the array's mature high-res backazimuth estimator.
# GROUND TRUTH: the event catalogue backazimuth (great-circle from the array to the USGS epicentre) --
#           an INDEPENDENT reference (the sealed D3 protocol, "catalogue backazimuth").
# Reuses compress3 from rehab033 (bit-identical matched-bit three-arm compressor).
#
#   --build MINMAG YEAR : fetch+process events, cache per-event snapshots, report baz recovery
#   --develop           : config sweep on calibration events (from cache)
#   --confirm BAND BITS : frozen config on held-out events (from cache)
import sys, os, glob, warnings
warnings.filterwarnings("ignore")
import numpy as np
from rehab033 import compress3

CACHE = "/home/claude/seismic_cache"
_GRID = np.deg2rad(np.arange(0, 360, 1.0))       # backazimuth grid (deg from North, to source)


def music_baz(X3, freqs, x, y, p):
    """X3 (M,T,B); x,y station coords (km, E/N); p slowness (s/km). Backazimuth of the plane wave."""
    M, T, B = X3.shape
    ux = -p * np.sin(_GRID); uy = -p * np.cos(_GRID)   # slowness vector = propagation dir (away from source)
    proj = np.outer(x, ux) + np.outer(y, uy)           # (M, G)
    Ps = np.zeros(len(_GRID))
    for b in range(B):
        Xb = X3[:, :, b]; _w, V = np.linalg.eigh((Xb @ Xb.conj().T) / T); Un = V[:, :M - 1]
        A = np.exp(-1j * 2 * np.pi * freqs[b] * proj)
        Ps += 1.0 / (np.sum(np.abs(Un.conj().T @ A) ** 2, 0) + 1e-30)
    k = int(np.argmax(Ps))
    sharp = Ps[k] / (np.median(Ps) + 1e-30)          # peak/median = GT-free resolution quality
    return np.rad2deg(_GRID[k]), sharp


# --------------------------- fetch + cache ---------------------------
def build(minmag, year):
    from obspy import UTCDateTime
    from obspy.clients.fdsn import Client
    from obspy.geodetics import gps2dist_azimuth, locations2degrees, kilometers2degrees
    from obspy.taup import TauPyModel
    from scipy.signal import stft
    os.makedirs(CACHE, exist_ok=True)
    iris = Client("IRIS", timeout=90); usgs = Client("USGS", timeout=90); MODEL = TauPyModel("iasp91")
    stas = ["PD%02d" % i for i in range(1, 14)]
    inv = iris.get_stations(network="IM", station=",".join(stas), channel="SHZ", level="station",
                            starttime=UTCDateTime("%d-01-01" % year))
    coord = {st.code: (st.latitude, st.longitude) for net in inv for st in net}
    use = sorted(coord)
    la = np.array([coord[s][0] for s in use]); lo = np.array([coord[s][1] for s in use])
    la0, lo0 = la.mean(), lo.mean()
    x = (lo - lo0) * 111.195 * np.cos(np.deg2rad(la0)); y = (la - la0) * 111.195   # km E/N
    cat = usgs.get_events(starttime=UTCDateTime("%d-01-01" % year), endtime=UTCDateTime("%d-12-31" % year),
                          minmagnitude=minmag)
    print(f"array PDAR: {len(use)} stations, aperture ~{max(x.max()-x.min(), y.max()-y.min()):.1f} km; "
          f"catalogue events M>={minmag} ({year}): {len(cat)}", flush=True)
    np.save(f"{CACHE}/_geom.npy", np.array([x, y]))
    kept = 0
    for ev in cat:
        o = ev.origins[0]; ot = o.time; elat, elon, edep = o.latitude, o.longitude, (o.depth or 0) / 1000.0
        dist_deg = locations2degrees(la0, lo0, elat, elon)
        if not (30 <= dist_deg <= 95):
            continue                                          # clean teleseismic P window
        baz = gps2dist_azimuth(la0, lo0, elat, elon)[1]       # array->event azimuth = backazimuth to source
        try:
            arr = MODEL.get_travel_times(source_depth_in_km=max(edep, 0), distance_in_degree=dist_deg,
                                         phase_list=["P"])
            if not arr:
                continue
            ptime = ot + arr[0].time; p_skm = arr[0].ray_param_sec_degree / 111.195     # s/km
            st = iris.get_waveforms("IM", ",".join(use), "*", "SHZ", ptime - 8, ptime + 32)
            st.detrend("demean"); st.taper(0.05); st.filter("bandpass", freqmin=0.7, freqmax=3.0)
            got = {tr.stats.station: tr for tr in st}
            if len(got) < 10:
                continue
            sr = got[list(got)[0]].stats.sampling_rate
            L = min(len(got[s].data) for s in got if s in use)
            chans = [s for s in use if s in got]
            xi = np.array([x[use.index(s)] for s in chans]); yi = np.array([y[use.index(s)] for s in chans])
            A = np.stack([got[s].data[:L].astype(float) for s in chans], 0)            # (M, L)
            f0, t0, _z = stft(A[0], fs=sr, nperseg=128, noverlap=96)
            Zf = np.stack([stft(A[m], fs=sr, nperseg=128, noverlap=96)[2] for m in range(len(chans))], 0)
            bins = np.where((f0 >= 0.8) & (f0 <= 2.8))[0]
            X3 = Zf[:, bins, :].transpose(0, 2, 1)                                       # (M, T, B)
            for b in range(X3.shape[2]):
                X3[:, :, b] /= (np.sqrt(np.mean(np.abs(X3[:, :, b]) ** 2)) + 1e-30)
            tag = str(ot)[:19].replace(":", "").replace("-", "")
            np.savez(f"{CACHE}/ev_{tag}.npz", X3=X3, freqs=f0[bins], x=xi, y=yi, p=p_skm,
                     baz=baz, dist=dist_deg, mag=ev.magnitudes[0].mag)
            rec, sharp = music_baz(X3, f0[bins], xi, yi, p_skm)
            err = abs(((rec - baz + 180) % 360) - 180)
            kept += 1
            print(f"  ev {tag} dist {dist_deg:4.0f} baz_GT {baz:5.1f} MUSIC {rec:5.1f} err {err:4.1f} "
                  f"sharp {sharp:5.1f} M{ev.magnitudes[0].mag} nsta {len(chans)}", flush=True)
        except Exception as e:
            print(f"  skip {str(ot)[:19]} {type(e).__name__} {str(e)[:60]}", flush=True)
    print(f"cached {kept} events", flush=True)


# --------------------------- flip ---------------------------
def _events():
    return sorted(glob.glob(f"{CACHE}/ev_*.npz"))


def flip_on(files, f_lo, f_hi, budget, sharp_min=0.0, tol=1.0):
    # Flip scored vs the ABSOLUTE catalogue backazimuth (sealed D3 protocol). Events are gated by the
    # uncompressed MUSIC peak SHARPNESS (GT-free): only events where the array actually resolves the
    # source plane wave are valid tests -- the seismic analog of the acoustic energy / radar sharpness gate.
    holds = anti = recon = n = 0; fails = []; recs = []; gts = []
    for f in files:
        d = np.load(f); X3 = d["X3"]; freqs = d["freqs"]; x = d["x"]; y = d["y"]; p = float(d["p"]); baz = float(d["baz"])
        bsel = (freqs >= f_lo) & (freqs <= f_hi)
        if bsel.sum() < 2:
            continue
        Xs = X3[:, :, bsel]; fs = freqs[bsel]
        ref, sharp = music_baz(Xs, fs, x, y, p)                            # uncompressed estimate + quality
        if sharp < sharp_min:
            continue
        cx = compress3(Xs, budget)
        dg = {a: abs(((music_baz(cx[a][0], fs, x, y, p)[0] - baz + 180) % 360) - 180) for a in cx}
        pqr, lqr = cx["pq"][1], cx["lloyd"][1]
        holds += (dg["pq"] <= dg["lloyd"] + tol) and (lqr <= pqr)
        anti += dg["phase_destroy"] >= max(dg["pq"], dg["lloyd"])
        recon += lqr <= pqr
        fails.append(max(0.0, dg["pq"] - dg["lloyd"])); n += 1
        recs.append(ref); gts.append(baz)
    recs = np.array(recs); gts = np.array(gts)
    gterr = float(np.median(np.abs(((recs - gts + 180) % 360) - 180))) if n else 9.9
    return dict(n=n, holds=holds, anti=anti, recon=recon,
                med=float(np.median(fails)) if fails else 9.9, gterr=gterr)


def main():
    if "--build" in sys.argv:
        i = sys.argv.index("--build"); build(float(sys.argv[i + 1]), int(sys.argv[i + 2])); return
    ev = _events()
    half = len(ev) // 2
    CAL, HELD = ev[:half], ev[half:]                    # deterministic split (chronological)
    if "--develop" in sys.argv:
        print(f"DEVELOP (calibration events: {len(CAL)} of {len(ev)})", flush=True)
        for band in ((0.8, 2.8), (1.0, 2.8)):
            for bud in (48, 64):
                for sm in (0, 3, 6):
                    r = flip_on(CAL, band[0], band[1], bud, sm)
                    print(f"  band={band[0]}-{band[1]} bits={bud} sharp>={sm}: flip {r['holds']:2d}/{r['n']:2d} | "
                          f"anti {r['anti']:2d}/{r['n']:2d} | recon {r['recon']:2d}/{r['n']:2d} | "
                          f"med {r['med']:.2f} | uncompressed-GT err {r['gterr']:.1f}", flush=True)
        return
    if "--confirm" in sys.argv:
        i = sys.argv.index("--confirm"); band = sys.argv[i + 1]; bud = int(sys.argv[i + 2]); sm = float(sys.argv[i + 3])
        f_lo, f_hi = [float(v) for v in band.split("-")]
        r = flip_on(HELD, f_lo, f_hi, bud, sm)
        print(f"CONFIRM (held-out {len(HELD)} events): band={band} bits={bud} sharp>={sm}, n={r['n']}")
        print(f"  clean flip {r['holds']}/{r['n']} | median flip_fail {r['med']:.2f}deg | "
              f"anti worst {r['anti']}/{r['n']} | recon(lloyd<=pq) {r['recon']}/{r['n']} | "
              f"uncompressed-GT err {r['gterr']:.1f}deg")
        frac = lambda a, b: a / b if b else 0
        checks = {"clean flip >= 55%": frac(r["holds"], r["n"]) >= 0.55,
                  "recon-trade >= 60%": frac(r["recon"], r["n"]) >= 0.60,
                  "anti worst >= 70%": frac(r["anti"], r["n"]) >= 0.70}
        for k, v in checks.items():
            print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        print(f"\nVERDICT: {'CONFIRMED' if all(checks.values()) else 'NOT CONFIRMED (honest negative)'}")


if __name__ == "__main__":
    main()
