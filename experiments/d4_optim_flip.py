# GO-P-2026-034 D4 (optional stretch) -- OPTIMIZATION: gradient compression, curvature (Hessian)
# read operator, on a REAL model + task. Extends the confirmed SYNTHETIC Gate-B (GO-P-2026-010) to
# real training steps: logistic regression on real handwritten-digit data (sklearn `load_digits`,
# self-contained). The read operator P_C = the real loss HESSIAN at the step.
#
# Three matched-bit arms compress the real gradient in the Hessian's eigenbasis, differing ONLY in
# which coordinates get more bits (identical bit MULTISET -> exactly matched total bits):
#   (R) read-preserving  -- protect high-curvature (high lambda*energy) directions
#   (O) reconstruction-optimal -- protect high-energy directions (minimise raw gradient MSE)
#   (A) anti             -- protect LOW-curvature directions (starve the read directions)
# Downstream = update-direction distortion under the H-metric  (ghat-g)'H(ghat-g)/g'Hg.
# Flip (per step): dH(R) <= dH(O)  AND  recon(O) <= recon(R);  anti: dH(A) >= max(dH(R),dH(O)).
# Split: CALIBRATION = one-vs-rest tasks for digits 0-4; HELD-OUT = DISJOINT tasks digits 5-9.
import sys
import numpy as np
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler

_D = load_digits()
_X = StandardScaler().fit_transform(_D.data.astype(float))
_X = np.hstack([_X, np.ones((_X.shape[0], 1))])          # + bias -> d = 65
_TARGET = _D.target


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -40, 40)))


def _grad_hess(w, X, y):
    p = _sigmoid(X @ w)
    g = X.T @ (p - y) / len(y)
    W = p * (1 - p)
    H = (X * W[:, None]).T @ X / len(y) + 1e-4 * np.eye(X.shape[1])   # tiny ridge -> PD
    return g, H


def compress_arms(g, H, base_bits):
    """Three arms quantize the gradient in the H-eigenbasis over a GLOBAL range, at the SAME total
    bits, differing only in bit ALLOCATION: O=uniform (min ||delta||^2), R=bits to high curvature,
    A=bits to low curvature. A global range makes reconstruction genuinely trade against curvature."""
    lam, U = np.linalg.eigh(H); lam = np.maximum(lam, 1e-10)
    c = U.T @ g; d = len(c)
    G = 4 * np.std(c) + 1e-12                    # global quantization range (equal precision baseline)
    total = base_bits * d

    def alloc(weight):
        if weight is None:
            return np.full(d, float(base_bits))  # uniform bits = reconstruction-optimal for equal range
        lw = 0.5 * np.log2(weight)
        b = np.clip(lw - lw.mean() + base_bits, 0, 14)
        if b.sum() > 0:
            b = np.clip(b * (total / b.sum()), 0, 14)   # rescale to exact matched total
        return b

    def quant(b):
        cq = c.copy()
        for k in range(d):
            lv = 2 ** b[k]
            if lv <= 1:
                cq[k] = 0.0; continue
            step = G / lv
            cq[k] = np.clip(np.round(c[k] / step), -lv / 2, lv / 2) * step
        return U @ cq, float(b.sum())

    R, bR = quant(alloc(lam))           # read-preserving: bits to high curvature
    O, bO = quant(alloc(None))          # reconstruction-optimal: uniform bits
    A, bA = quant(alloc(1.0 / lam))     # anti: bits to LOW curvature (starve the read directions)
    return {"R": R, "O": O, "A": A}, (bR, bO, bA)


def _dH(gh, g, H):
    e = gh - g
    return float(e @ H @ e) / float(g @ H @ g + 1e-30)


def _recon(gh, g):
    return float(np.sum((gh - g) ** 2)) / float(np.sum(g ** 2) + 1e-30)


def steps_for_class(cls, T=60, bs=96, seed=0):
    """Real training trajectory: one-vs-rest logistic regression, mini-batch (g,H) per step."""
    y = (_TARGET == cls).astype(float); rng = np.random.default_rng(seed + cls)
    w = np.zeros(_X.shape[1]); insts = []
    for _t in range(T):
        idx = rng.choice(len(y), bs, replace=False)
        g, H = _grad_hess(w, _X[idx], y[idx])
        insts.append((g.copy(), H.copy()))
        gf, _ = _grad_hess(w, _X, y)
        w = w - 0.5 * gf
    return insts


def flip_on(classes, base_bits, tol=1e-3):
    holds = anti = recon = n = 0; fails = []; bitspread = []
    dH_ratio = []; rec_ratio = []; anisotropy = []
    for cls in classes:
        for g, H in steps_for_class(cls):
            arms, bits = compress_arms(g, H, base_bits)
            dr, do, da = _dH(arms["R"], g, H), _dH(arms["O"], g, H), _dH(arms["A"], g, H)
            rr, ro = _recon(arms["R"], g), _recon(arms["O"], g)
            holds += (dr <= do * (1 + tol)) and (ro <= rr)
            anti += da >= max(dr, do)
            recon += ro <= rr
            fails.append(max(0.0, dr - do)); n += 1
            bitspread.append(max(bits) - min(bits))
            dH_ratio.append(do / (dr + 1e-30))            # how much worse recon-optimal is downstream
            rec_ratio.append(rr / (ro + 1e-30))           # how much worse read-preserving is on recon
            lam = np.linalg.eigvalsh(H); anisotropy.append(lam.max() / (lam.min() + 1e-30))
    return dict(n=n, holds=holds, anti=anti, recon=recon,
                med=float(np.median(fails)) if fails else 9.9,
                maxbitgap=float(np.max(bitspread)) if bitspread else 0.0,
                dH_ratio=float(np.median(dH_ratio)) if dH_ratio else 1.0,
                rec_ratio=float(np.median(rec_ratio)) if rec_ratio else 1.0,
                aniso=float(np.median(anisotropy)) if anisotropy else 1.0)


CAL = [0, 1, 2, 3, 4]; HELD = [5, 6, 7, 8, 9]


def main():
    if "--develop" in sys.argv:
        print(f"DEVELOP (calibration one-vs-rest tasks digits {CAL})")
        for bb in (3, 4, 5):
            r = flip_on(CAL, bb)
            print(f"  base_bits={bb}: flip {r['holds']:3d}/{r['n']:3d} | anti {r['anti']:3d}/{r['n']:3d} | "
                  f"recon {r['recon']:3d}/{r['n']:3d} | bitgap {r['maxbitgap']:.0e} | "
                  f"EFFECT: recon-opt {r['dH_ratio']:.1f}x worse downstream, read-pres {r['rec_ratio']:.1f}x worse recon "
                  f"(H anisotropy {r['aniso']:.0e})")
        return
    if "--confirm" in sys.argv:
        bb = int(sys.argv[sys.argv.index("--confirm") + 1])
        r = flip_on(HELD, bb)
        frac = lambda a, b: a / b if b else 0
        print(f"CONFIRM (held-out DISJOINT tasks digits {HELD}): base_bits={bb}, n={r['n']}")
        print(f"  clean flip {r['holds']}/{r['n']} ({100*frac(r['holds'],r['n']):.0f}%) | "
              f"anti worst {r['anti']}/{r['n']} | recon(O<=R) {r['recon']}/{r['n']} | matched bits (max gap {r['maxbitgap']:.0e})")
        print(f"  EFFECT SIZE on real Hessians: recon-optimal is {r['dH_ratio']:.1f}x worse on the curvature "
              f"metric; read-preserving is {r['rec_ratio']:.1f}x worse on reconstruction; median H anisotropy {r['aniso']:.0e}")
        checks = {"clean flip >= 60%": frac(r["holds"], r["n"]) >= 0.60,
                  "recon-trade >= 60%": frac(r["recon"], r["n"]) >= 0.60,
                  "anti worst >= 70%": frac(r["anti"], r["n"]) >= 0.70}
        for k, v in checks.items():
            print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        print(f"\nVERDICT: {'CONFIRMED' if all(checks.values()) else 'NOT CONFIRMED (honest negative)'}")


if __name__ == "__main__":
    main()
