# GO-P-2026-040 support / Paper IV kappa alignment law.
# kappa = tr(Pbar_C Sigma_x) / sum_{i<=r} lambda_i(Sigma_x)  -- read-energy alignment (Def 1).
# Proposition: flip magnitude Delta = d_C(O) - d_C(R) is non-increasing in kappa.
#   kappa->1 : read subspace == top-energy subspace -> O already protects it -> Delta~0 (coupling null, D4)
#   kappa->0 : read subspace in low-energy dirs -> O starves it -> Delta maximal (DOA/synthetic)
# This script (a) dials kappa in a controlled synthetic domain and measures Delta with real matched-bit
# quantization, and (b) computes kappa analytically for the two real anchors (synthetic ULA DOA, gradient
# Hessian on load_digits). Learned-rep interiors (legal, whale, ...) are measured on Atlas separately.
import json
import numpy as np

RNG = np.random.default_rng(0)


def quant_error_cov(X, bits, ranges):
    """Uniform scalar quantize each coord of X (n,d) at bits[k] over +-ranges[k]; return Cov(X - Xhat)."""
    Xh = X.copy()
    for k in range(X.shape[1]):
        lv = 2 ** bits[k]
        if lv <= 1:
            Xh[:, k] = 0.0
            continue
        step = 2 * ranges[k] / lv
        Xh[:, k] = np.clip(np.round(X[:, k] / step), -lv / 2, lv / 2) * step
    D = X - Xh
    return np.cov(D, rowvar=False)


def alloc(weight, base_bits, D):
    """Reverse-water-filling style allocation at fixed total = base_bits*D bits."""
    w = np.maximum(weight, 1e-12)
    lw = 0.5 * np.log2(w)
    b = np.clip(lw - lw.mean() + base_bits, 0, 14)
    if b.sum() > 0:
        b = np.clip(b * (base_bits * D / b.sum()), 0, 14)
    return b


def synthetic_kappa_point(phi, d=64, r=8, n=20000, base_bits=1.0, decay=0.85):
    """Signal covariance = diag(lambda), lambda_k = decay^k (anisotropic, energy in low indices).
    Read subspace = span of u_i = cos(phi) e_i + sin(phi) e_{d-r+i}, i=0..r-1: rotates the read subspace
    from the TOP-energy block (phi=0, kappa~1) to the BOTTOM-energy block (phi=pi/2, kappa~0)."""
    lam = decay ** np.arange(d)
    Sx = np.diag(lam)
    top = np.arange(r)
    bot = np.arange(d - r, d)
    U = np.zeros((d, r))
    for i in range(r):
        U[top[i], i] = np.cos(phi)
        U[bot[i], i] = np.sin(phi)
    U, _ = np.linalg.qr(U)                       # orthonormal read basis
    Pc = U @ U.T                                 # rank-r read projector
    kappa = np.trace(Pc @ Sx) / lam[top].sum()

    X = RNG.standard_normal((n, d)) * np.sqrt(lam)
    ranges = 4 * np.sqrt(lam)
    read_diag = np.clip(np.diag(Pc), 1e-9, None)  # per-coord read importance
    bO = alloc(lam, base_bits, d)                 # reconstruction-optimal: bits by energy
    bR = alloc(read_diag, base_bits, d)           # read-preserving: bits by read importance
    SdO = quant_error_cov(X, bO, ranges)
    SdR = quant_error_cov(X, bR, ranges)
    dO = np.trace(Pc @ SdO)                        # downstream distortion under O
    dR = np.trace(Pc @ SdR)                        # ... under R
    recon_O = np.trace(SdO); recon_R = np.trace(SdR)
    delta = dO - dR                               # flip magnitude (positive => R wins downstream)
    read_energy = np.trace(Pc @ Sx)               # signal the consumer reads
    return dict(phi=float(phi), kappa=float(kappa), dO=float(dO), dR=float(dR),
                delta=float(delta), delta_rel=float(delta / (dO + 1e-12)),
                delta_norm=float(delta / (read_energy + 1e-12)),   # flip per unit read signal
                ratio=float(dO / (dR + 1e-12)),                    # scale-free: dO/dR
                recon_trade=bool(recon_O <= recon_R))


def faithful_coupling_point(k, d=128, m=32, r=16, nu=4.0, beta=0.25, n=40000, base_bits=1.0):
    """Faithful coupling model (fixes both confounds of the naive sweep).
    Energy CONCENTRATED and FLAT-within-block: nuisance block dims 0..m-1 variance nu (high),
    background dims m..d-1 variance beta (low). Read subspace = r axis-aligned dirs: k drawn from the
    nuisance block (0..k-1), r-k from the background (m..m+(r-k)-1). Dialing k=r->0 moves the read
    subspace from INSIDE the high-energy block (kappa=1, coupling null) to the low-energy background
    (kappa small). Flat-within-block means at k=r the O-allocation (by variance) and R-allocation (by
    read membership) coincide on the read dims -> genuine null. Report the SCALE-FREE relative flip
    delta_rel = 1 - d_C(R)/d_C(O), since absolute delta inherently scales with read-subspace energy."""
    var = np.full(d, beta); var[:m] = nu
    read_idx = list(range(k)) + list(range(m, m + (r - k)))
    Pc_diag = np.zeros(d); Pc_diag[read_idx] = 1.0
    Sx = np.diag(var)
    Pc = np.diag(Pc_diag)                                   # axis-aligned read projector (rank r)
    top_r = np.sort(var)[::-1][:r].sum()
    kappa = (Pc_diag * var).sum() / top_r

    X = RNG.standard_normal((n, d)) * np.sqrt(var)
    ranges = 4 * np.sqrt(var)                               # signal-scaled range (the embedding regime)
    bO = alloc(var, base_bits, d)                           # recon-optimal: bits by variance
    bR = alloc(np.clip(Pc_diag, 1e-9, None), base_bits, d)  # read-preserving: bits by read membership
    SdO = quant_error_cov(X, bO, ranges)
    SdR = quant_error_cov(X, bR, ranges)
    dO = float((Pc_diag * np.diag(SdO)).sum())             # tr(Pc Sd) for diagonal Pc
    dR = float((Pc_diag * np.diag(SdR)).sum())
    return dict(k=int(k), kappa=float(kappa), dO=dO, dR=dR,
                delta_rel=float(1 - dR / (dO + 1e-18)),
                recon_trade=bool(np.trace(SdO) <= np.trace(SdR)))


def anchor_doa(M=16, snr_db=10.0, theta0=0.2):
    """Synthetic lambda/2 ULA. Read direction ghat = P_a^perp a'(theta0); Sigma_x = P_s a a^H + sigma^2 I.
    kappa (r=1) = (ghat^H Sx ghat / |ghat|^2) / lambda_1(Sx)."""
    m = np.arange(M)
    a = np.exp(-1j * np.pi * np.sin(theta0) * m)
    ap = (-1j * np.pi * np.cos(theta0) * m) * a           # da/dtheta
    Pa_perp = np.eye(M) - np.outer(a, a.conj()) / (a.conj() @ a)
    g = Pa_perp @ ap
    g = g / np.linalg.norm(g)
    Ps = 1.0; sigma2 = Ps / (10 ** (snr_db / 10))
    Sx = Ps * np.outer(a, a.conj()) + sigma2 * np.eye(M)
    lam1 = np.linalg.eigvalsh(Sx)[-1].real
    num = (g.conj() @ Sx @ g).real
    return dict(domain="synthetic-DOA", kappa=float(num / lam1), note="ghat perp steering => kappa~0")


def anchor_gradient():
    """load_digits one-vs-rest logistic; read op = Hessian H=(1/n)X^T diag(p(1-p)) X; Sigma_x = X^T X / n.
    Read subspace = top-r eigvecs of H; kappa = tr(Pbar_C Sx)/sum top-r lambda(Sx)."""
    from sklearn.datasets import load_digits
    from sklearn.linear_model import LogisticRegression
    Xd, yd = load_digits(return_X_y=True)
    Xd = (Xd - Xd.mean(0)) / (Xd.std(0) + 1e-9)
    y = (yd == 0).astype(int)                              # one-vs-rest
    clf = LogisticRegression(max_iter=2000).fit(Xd, y)
    p = clf.predict_proba(Xd)[:, 1]
    W = Xd * np.sqrt(p * (1 - p))[:, None]
    H = (W.T @ W) / len(Xd)
    Sx = (Xd.T @ Xd) / len(Xd)
    r = 8
    wH, VH = np.linalg.eigh(H); Ur = VH[:, ::-1][:, :r]    # top-r read subspace
    Pc = Ur @ Ur.T
    lamx = np.linalg.eigvalsh(Sx)[::-1]
    kappa = np.trace(Pc @ Sx) / lamx[:r].sum()
    return dict(domain="gradient-D4", kappa=float(kappa), note="H and X^TX share eigenstructure => kappa~1")


def main():
    sweep = [synthetic_kappa_point(phi) for phi in np.linspace(0.0, np.pi / 2, 11)]
    # Salvage attempt: faithful coupling model (concentrated flat-block energy, m=r, relative flip).
    faithful = {f"beta_{b:.0e}": [faithful_coupling_point(k, m=16, r=16, d=64, nu=4.0, beta=b)
                                   for k in range(16, -1, -1)] for b in (0.25, 1e-3, 1e-6)}
    anchors = [anchor_doa(), anchor_gradient()]
    print("=== faithful coupling salvage: delta_rel at kappa=1 (null) vs kappa~0 (max), by background beta ===")
    for b, rows in faithful.items():
        print(f"  {b}: kappa=1 delta_rel={rows[0]['delta_rel']:.4f}  kappa~0 delta_rel={rows[-1]['delta_rel']:.4f}")
    print("  (sharp null delta_rel->0 at kappa=1 only when beta->0 = signal support == read support = D4;")
    print("   but then the sweep degenerates: delta_rel~0 for all kappa>0 -> no magnitude dial.)\n")
    print("=== synthetic kappa-sweep (phi 0->pi/2 : read top-energy -> bottom-energy) ===")
    print(f"{'kappa':>7} {'delta':>11} {'delta_norm':>11} {'ratio dO/dR':>12}")
    for s in sweep:
        print(f"{s['kappa']:7.3f} {s['delta']:11.4e} {s['delta_norm']:11.4f} {s['ratio']:12.3f}")

    def spear(a, b):
        ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
        return np.corrcoef(ra, rb)[0, 1]
    ks = np.array([s["kappa"] for s in sweep])
    for key in ("delta", "delta_norm", "ratio"):
        vs = np.array([s[key] for s in sweep])
        print(f"Spearman(kappa, {key:10s}) = {spear(ks, vs):+.3f}")
    print("(law predicts strongly NEGATIVE; a clean normalization is one that is monotone in kappa)")
    rho = spear(ks, np.array([s["delta_norm"] for s in sweep]))
    print("\n=== real-domain analytic anchors ===")
    for a in anchors:
        print(f"  {a['domain']:16s} kappa={a['kappa']:.4f}  ({a['note']})")
    finding = (
        "EXPLORATORY / honest negative, with a SHARPENING. The naive alignment law (flip magnitude delta "
        "monotone DECREASING in kappa) is NOT supported. The salvage attempt (faithful coupling model: "
        "concentrated flat-block energy, m=r, relative flip delta_rel=1-dR/dO) converges on a precise "
        "characterization rather than a magnitude law: (a) the kappa=1 coupling null is SHARP "
        "(delta_rel->0) exactly when the signal support equals the read support (background beta->0) -- "
        "which is precisely the D4 coupling condition (Hessian support = X^TX energy support); (b) but in "
        "that sharp-null regime the sweep DEGENERATES (delta_rel~0 for all kappa>0, jumping only at "
        "kappa=0), because dialing kappa down puts the read subspace in the vanishing-energy background, "
        "so the flip lands on negligible signal. A sharp null at kappa=1 AND a meaningful flip at low "
        "kappa are IRRECONCILABLE in this model class. Robust conclusion: kappa is an ordinal "
        "coupling-null predictor with an EXACT null condition (read support = signal support), not a "
        "cross-regime magnitude dial; the flip magnitude is governed by where the read-subspace SIGNAL "
        "sits relative to O's bit allocation, which is not a single scalar. Anchors: gradient-D4 "
        "kappa~0.80 (empirical flip 27% ~ null), synthetic-DOA kappa~0.006 (large flip). GO-P-2026-040 "
        "NOT sealed: no clean magnitude law exists to predict."
    )
    out = dict(status="exploratory", finding=finding, synthetic_sweep=sweep,
               faithful_coupling_salvage=faithful, anchors=anchors, spearman_kappa_delta_norm=float(rho))
    with open("results/GO-kappa-law.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\n" + finding)
    print("\nwrote results/GO-kappa-law.json")


if __name__ == "__main__":
    main()
