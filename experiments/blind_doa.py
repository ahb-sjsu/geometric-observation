"""GO-P-2026-041 -- blind, NON-ORACLE, prospective DOA flip with magnitude prediction.

The reviewer's decisive test: recover the read operator by finite-difference PROBING of the
ACTUAL MUSIC estimator (no ground-truth theta0 anywhere in the compressor), commit the
winning code, the sign of the downstream/reconstruction reversal, AND a magnitude interval
for the downstream gap from CALIBRATION, then evaluate ONCE on a held-out realization.

Domain: narrowband ULA, single source. Consumer = spectral MUSIC (its own peak-picker).
Compressor sees only the array snapshots and the estimator's output sensitivity -- never the
true angle. The read operator is P_C = <g g^T>, g = d(theta_hat)/d(snapshot coord) by finite
difference; this is the estimator's actual read direction, recovered non-oracle.

  --calibrate   : recover P_C (non-oracle), fit R/O/A codes, compute Delta_pred, print the
                  predictions to be SEALED.
  --confirm     : score the FROZEN codes once on the held-out realization; check sign +
                  magnitude against the sealed predictions.
"""
import argparse
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
M = 12                    # ULA elements
THETA0 = 21.3             # true source DOA (deg) -- UNKNOWN to the compressor
SNR_DB = 8.0
T = 200                   # snapshots
GRID = np.arange(-60, 60.01, 0.1)   # MUSIC search grid (deg)
BASE_BITS = 2.0
R_RANK = 3                # read-subspace rank kept
EPS = 1e-3               # finite-difference step for the blind probe


def steer(theta_deg, M=M):
    return np.exp(-1j * np.pi * np.sin(np.deg2rad(theta_deg)) * np.arange(M))


def snapshots(rng, theta=THETA0, snr_db=SNR_DB, T=T, M=M):
    a = steer(theta, M)
    s = (rng.standard_normal(T) + 1j * rng.standard_normal(T)) / np.sqrt(2)
    sig = np.sqrt(10 ** (snr_db / 10)) * np.outer(a, s)
    noise = (rng.standard_normal((M, T)) + 1j * rng.standard_normal((M, T))) / np.sqrt(2)
    return sig + noise                 # (M, T) complex


def music_doa(X):
    """root-MUSIC on the array snapshots X (M,T): a CONTINUOUS DOA estimate (deg), so the
    finite-difference probe of the estimator is well-defined. Consumer output = theta_hat."""
    R = (X @ X.conj().T) / X.shape[1]
    R = R + 1e-9 * np.eye(M)
    try:
        w, V = np.linalg.eigh(R)
    except np.linalg.LinAlgError:
        return 0.0
    En = V[:, :-1]                      # noise subspace (1 source)
    C = En @ En.conj().T
    coeffs = np.array([np.trace(C, offset=d) for d in range(M - 1, -M, -1)])  # deg 2(M-1)
    roots = np.roots(coeffs)
    roots = roots[np.abs(roots) < 1 - 1e-9]
    if len(roots) == 0:
        return 0.0
    z = roots[np.argmin(1 - np.abs(roots))]          # root closest to the unit circle
    s = np.clip(-np.angle(z) / np.pi, -1, 1)          # a_m = exp(-j pi sin(theta) m)
    return float(np.rad2deg(np.arcsin(s)))


def blind_probe(Xc):
    """NON-ORACLE read operator: g_i = d theta_hat / d (coherent coord-i perturbation) by
    finite difference; probe the REAL MUSIC estimator, no theta0. Coords = [Re; Im] (2M)."""
    base = music_doa(Xc)
    g = np.zeros(2 * M)
    for i in range(2 * M):
        d = np.zeros(M, complex)
        if i < M:
            d[i] = EPS
        else:
            d[i - M] = 1j * EPS
        g[i] = (music_doa(Xc + d[:, None]) - base) / EPS
    return g                            # sensitivity of theta_hat to each input coord


def _realify(X):
    return np.vstack([X.real, X.imag])  # (2M, T)


def alloc(weight, base_bits, D):
    lw = 0.5 * np.log2(np.maximum(weight, 1e-12))
    b = np.clip(lw - lw.mean() + base_bits, 0, 14)
    if b.sum() > 0:
        b = np.clip(b * (base_bits * D / b.sum()), 0, 14)
    return b


def quant(C, bits, ranges):
    Cq = C.copy()
    for k in range(C.shape[0]):
        lv = 2 ** bits[k]
        if lv <= 1:
            Cq[k] = C[k].mean(); continue
        step = 2 * ranges[k] / lv
        Cq[k] = np.clip(np.round(C[k] / step), -lv / 2, lv / 2) * step
    return Cq


def fit_codes(Xc, g):
    """Codes in the real snapshot-covariance eigenbasis. O = reverse water-filling by
    variance; R = bits to the read subspace (top-r of P_C in this basis); A = anti."""
    Xr = _realify(Xc)                                  # (2M, T)
    Sx = np.cov(Xr)                                    # (2M, 2M)
    wv, V = np.linalg.eigh(Sx)                         # eigenbasis
    Cc = V.T @ Xr                                      # coeffs (2M, T)
    var = np.maximum((Cc ** 2).mean(1), 1e-12)
    # read importance per basis vector = squared projection of g onto each eigenvector
    gproj = (V.T @ g) ** 2
    keep = np.zeros(len(gproj), bool); keep[np.argsort(gproj)[::-1][:R_RANK]] = True
    read_w = np.where(keep, np.maximum(gproj, 1e-12), gproj.max() * 1e-4)
    D = len(var); ranges = 4 * np.sqrt(var)
    bO, bR, bA = alloc(var, BASE_BITS, D), alloc(read_w, BASE_BITS, D), alloc(var / read_w, BASE_BITS, D)
    return dict(V=V, var=var, ranges=ranges, bO=bO, bR=bR, bA=bA,
                read_diag=np.diag(V @ np.diag(keep.astype(float)) @ V.T))


def apply_code(Xc, code, bits):
    Xr = _realify(Xc); V, ranges = code["V"], code["ranges"]
    Cc = V.T @ Xr
    Cq = quant(Cc, bits, ranges)
    Xrq = V @ Cq
    return Xrq[:M] + 1j * Xrq[M:]                       # back to complex (M, T)


def downstream_and_recon(Xc, code, bits, theta_true):
    Xq = apply_code(Xc, code, bits)
    err = (music_doa(Xq) - theta_true) ** 2            # downstream: squared DOA error (deg^2)
    recon = float(((_realify(Xq) - _realify(Xc)) ** 2).sum() / (_realify(Xc) ** 2).sum())
    return err, recon


def delta_pred(Xc, code):
    """Delta_pred = tr[P_C (Sigma_delta^O - Sigma_delta^R)] on calibration, in the read
    metric -- the theory's predicted downstream gap (deg^2), sign + magnitude."""
    g = code["_g"]; Pc = np.outer(g, g)                # rank-1 read operator (2M,2M)
    def Sdelta(bits):
        Xq = apply_code(Xc, code, bits); Dr = _realify(Xc) - _realify(Xq)
        return np.cov(Dr)
    return float(np.trace(Pc @ (Sdelta(code["bO"]) - Sdelta(code["bR"]))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--confirm", action="store_true")
    args = ap.parse_args()

    rng_cal = np.random.default_rng(11)
    Xc = snapshots(rng_cal)
    g = blind_probe(Xc)                                # NON-ORACLE read operator
    code = fit_codes(Xc, g); code["_g"] = g
    dpred = delta_pred(Xc, code)

    if args.calibrate:
        # calibration downstream/recon (many SNR realizations, same config)
        errO = errR = errA = recO = recR = 0.0; K = 40
        rng = np.random.default_rng(101)
        for _ in range(K):
            X = snapshots(rng)
            eO, rO = downstream_and_recon(X, code, code["bO"], THETA0)
            eR, rR = downstream_and_recon(X, code, code["bR"], THETA0)
            eA, _ = downstream_and_recon(X, code, code["bA"], THETA0)
            errO += eO; errR += eR; errA += eA; recO += rO; recR += rR
        errO/=K; errR/=K; errA/=K; recO/=K; recR/=K
        print("=== CALIBRATION (non-oracle read operator from probing MUSIC) ===")
        print(f"read op recovered by finite-diff probe; ||g||={np.linalg.norm(g):.3f} (no theta0 used)")
        print(f"downstream DOA MSE (deg^2): R={errR:.4f}  O={errO:.4f}  A={errA:.4f}")
        print(f"reconstruction rel-MSE:     R={recR:.4f}  O={recO:.4f}")
        print(f"Delta_measured = MSE(O)-MSE(R) = {errO-errR:+.4f} deg^2")
        print(f"Delta_pred = tr[P_C(Sd_O - Sd_R)] = {dpred:+.4e}  (theory, from calibration)")
        print("\n--- SEALED PREDICTIONS (commit before held-out) ---")
        print(f"  (1) winning code: R (read-preserving) downstream")
        print(f"  (2) sign: MSE(R) < MSE(O)  AND  recon(O) < recon(R)")
        print(f"  (3) magnitude: Delta = MSE(O)-MSE(R) in [{0.5*(errO-errR):.4f}, {1.5*(errO-errR):.4f}] deg^2")
        return

    if args.confirm:
        # HELD-OUT: fresh seed, single evaluation over held-out realizations
        errs = {"R": [], "O": [], "A": []}; recs = {"R": [], "O": []}
        rng = np.random.default_rng(9999)
        for _ in range(40):
            X = snapshots(rng)
            for arm, bits in (("R", code["bR"]), ("O", code["bO"]), ("A", code["bA"])):
                e, r = downstream_and_recon(X, code, bits, THETA0)
                errs[arm].append(e)
                if arm in recs: recs[arm].append(r)
        mR, mO, mA = np.mean(errs["R"]), np.mean(errs["O"]), np.mean(errs["A"])
        rR, rO = np.mean(recs["R"]), np.mean(recs["O"])
        dmeas = mO - mR
        checks = {
            "R wins downstream (MSE_R<MSE_O)": mR < mO,
            "recon-trade (recon_O<recon_R)": rO < rR,
            "anti worst": mA >= max(mR, mO),
            "magnitude in sealed band [0.006,0.018]": 0.006 <= dmeas <= 0.018,
        }
        out = dict(id="GO-P-2026-041", oracle_free=True,
                   downstream_mse=dict(R=mR, O=mO, A=mA), recon=dict(R=rR, O=rO),
                   delta_measured=dmeas, delta_pred=dpred, checks=checks,
                   verdict="CONFIRMED" if all(checks.values()) else "NOT CONFIRMED")
        print("=== HELD-OUT CONFIRM (single evaluation) ===")
        print(f"downstream DOA MSE: R={mR:.4f} O={mO:.4f} A={mA:.4f}  recon: O={rO:.4f} R={rR:.4f}")
        print(f"Delta_measured={dmeas:+.4f} deg^2   Delta_pred(theory)={dpred:+.4e}")
        for k, v in checks.items():
            print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        print(f"VERDICT: {out['verdict']}")
        with open(os.path.join(HERE, "..", "results", "GO-blind-doa.json"), "w") as f:
            json.dump(out, f, indent=1)
        return


if __name__ == "__main__":
    main()
