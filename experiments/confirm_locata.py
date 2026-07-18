# GO-P-2026-032 confirmatory: PolarQuant DOA Gate-B on HELD-OUT LOCATA eval/task1.
#
# Config was SELECTED on dev/task1 calibration (fuzz_doa_technique.py): 8 cm DICIT ULA at exactly
# lambda/2 (2144 Hz, single bin -> ESPRIT/root-MUSIC exact), matched-bit budgets {48, 64}. This
# script runs that FIXED config on the 13 unseen eval/task1 recordings and scores the sealed bars.
# Reuses the compressors + loader from polarquant_doa_gateb.py and the MATLAB estimator pq_doa.m.
#
# Clean flip (both halves) per recording: PolarQuant (angle-favoring) DOA error <= scalar
# (reconstruction-optimal) DOA error + 0.5 deg  AND  scalar reconstruction MSE <= PolarQuant's.
import glob
import subprocess
import sys

import numpy as np
from scipy.io import loadmat, savemat

sys.path.insert(0, "/tmp")
from polarquant_doa_gateb import load_snap, compress, MATLAB  # noqa: E402

BUDGETS = [48, 64]
ARMS = ["polarquant", "scalar", "phase_destroy"]
TOL = 0.5  # deg tolerance on the DOA half


def main():
    recs = sorted(glob.glob("/archive/locata/eval/task1/recording*/dicit"),
                  key=lambda s: int(s.split("recording")[1].split("/")[0]))
    covs, meta, recon = [], [], {}
    for rd in recs:
        X, p, f, th0 = load_snap(rd, f_target=2144.0)
        covs.append((X @ X.conj().T) / X.shape[1]); meta.append((rd, -1, "clean", np.rad2deg(th0)))
        for B in BUDGETS:
            cx = compress(X, B)
            for arm in ARMS:
                Xh, mse, bits = cx[arm]
                covs.append((Xh @ Xh.conj().T) / Xh.shape[1])
                meta.append((rd, B, arm, np.rad2deg(th0)))
                recon.setdefault((rd, B), {})[arm] = mse
    savemat("/tmp/pq_covs.mat", {"R": np.stack(covs, 0), "nsig": 1})
    subprocess.run([MATLAB, "-batch", "run('/tmp/pq_doa.m')"], check=True,
                   capture_output=True, text=True, timeout=300)
    doa = loadmat("/tmp/pq_doas.mat")
    est = {"esprit": doa["esprit"].ravel(), "rmu": doa["rootmusic"].ravel()}
    idx = {}
    for i, m in enumerate(meta):
        idx[(m[0], m[1], m[2])] = i

    print(f"HELD-OUT confirmatory: {len(recs)} eval/task1 recordings, 8cm ULA @2144Hz, budgets {BUDGETS}")
    for B in BUDGETS:
        print(f"\n=== budget {B} bits ===")
        for ename, arr in est.items():
            holds = anti_worst = recon_ok = 0
            fails = []
            for rd in recs:
                gt = meta[idx[(rd, -1, "clean")]][3]
                de = {a: abs(arr[idx[(rd, B, a)]] - gt) for a in ARMS}
                pq_r, sc_r = recon[(rd, B)]["polarquant"], recon[(rd, B)]["scalar"]
                doa_half = de["polarquant"] <= de["scalar"] + TOL
                recon_half = sc_r <= pq_r
                holds += doa_half and recon_half
                anti_worst += de["phase_destroy"] >= max(de["polarquant"], de["scalar"])
                recon_ok += recon_half
                fails.append(max(0.0, de["polarquant"] - de["scalar"]))
            n = len(recs)
            print(f"  [{ename:>6}] clean flip holds {holds}/{n} | median flip_fail {np.median(fails):.2f}° "
                  f"| anti worst {anti_worst}/{n} | recon(scalar<=pq) {recon_ok}/{n}")

    # sealed bars (GO-P-2026-032), evaluated at budget 48
    print("\n=== sealed bars (budget 48) ===")
    B = 48
    res = {}
    for ename, arr in est.items():
        holds = anti = recon_ok = 0
        fails = []
        for rd in recs:
            gt = meta[idx[(rd, -1, "clean")]][3]
            de = {a: abs(arr[idx[(rd, B, a)]] - gt) for a in ARMS}
            pq_r, sc_r = recon[(rd, B)]["polarquant"], recon[(rd, B)]["scalar"]
            holds += (de["polarquant"] <= de["scalar"] + TOL) and (sc_r <= pq_r)
            anti += de["phase_destroy"] >= max(de["polarquant"], de["scalar"])
            recon_ok += sc_r <= pq_r
            fails.append(max(0.0, de["polarquant"] - de["scalar"]))
        res[ename] = dict(holds=holds, anti=anti, recon=recon_ok, med=float(np.median(fails)))
    n = len(recs)
    best = max(res.values(), key=lambda r: r["holds"])
    checks = {
        "flip holds >= 8/13 (either estimator)": max(r["holds"] for r in res.values()) >= 8,
        "median flip_fail <= 1.5deg (either)": min(r["med"] for r in res.values()) <= 1.5,
        "anti worst >= 10/13 (either)": max(r["anti"] for r in res.values()) >= 10,
        "recon scalar<=pq >= 10/13 (either)": max(r["recon"] for r in res.values()) >= 10,
    }
    for k, v in checks.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nVERDICT: {'CONFIRMED' if all(checks.values()) else 'NOT CONFIRMED (honest negative)'}")


if __name__ == "__main__":
    main()
