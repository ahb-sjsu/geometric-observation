"""Numerical checks of the inequalities in the proof of the achievability theorem
(Theorem 16 and Lemma 17 of the manuscript; the two instances are in the affine
class, which the general decomposition of the proof contains).

The theorem is a coding theorem and is not something a computation can verify.
What is checked here, on Gaussian stand-ins for the message, are the steps of
the proof that are statements about covariances:

  1. decomposition  Sigma = Sigma' + e A  with Sigma' a trigonometric polynomial
     density, 0 <= e <= eps, both cases of the proof (min f > 0, and min f = 0);
  2. blocks of the finite-memory process separated by guard intervals of m
     symbols are exactly uncorrelated;
  3. the coupling: drawing T' from its conditional law given T = T' + E returns
     the product law (checked on covariances); Cov(T', E) = 0 is also what makes
     the distortion cross term vanish;
  4. the leakage perturbation: for a Gaussian description Z of T',
        I(T'; Z | S)  <=  I(T'; Z | S')  +  I(E; HE + U),
     and I(E; HE + U) <= N eps tr(J A) / (2 ln 2);
  5. dropping the guard observations cannot lower the leakage bound:
        I(T'; Z | S'_all) <= I(T'; Z | S'_blocks).

The first two instances have a spectrum affine in one scalar spectrum (the
class an earlier draft treated).  The third, added 2026-11-14, runs the
decomposition as the proof now states it for a general spectrum: a random
vector moving average whose spectrum is not affine, Sigma' a Fejer mean of
Sigma minus (eps/2) I, the remainder between 0 and eps I, the encoder's draw
built as it is performed, the leakage steps with the constant eps tr J, and
the exact split of the distortion with the bound eps tr Q.

Run:  python verify_achievability.py     (a few seconds; writes verify_achievability.json)
"""
import json
import sys

import numpy as np

SEED = 20261114
LOG2 = np.log(2.0)


def ld(A):
    return np.linalg.slogdet((A + A.T) / 2)[1] / LOG2


def psd_sqrt(A):
    w, V = np.linalg.eigh((A + A.T) / 2)
    return (V * np.sqrt(np.clip(w, 0, None))) @ V.T


def toeplitz(r, N):
    """Scalar Toeplitz matrix from autocovariances r[0..]."""
    return np.array([[r[abs(i - j)] if abs(i - j) < len(r) else 0.0 for j in range(N)] for i in range(N)])


def autocov(spec, lags, grid=4096):
    w = 2 * np.pi * np.arange(grid) / grid
    s = spec(w)
    return np.array([np.mean(s * np.cos(w * k)) for k in range(lags)])


def trig_poly(spec, m, grid=4096):
    """Fourier partial sum of degree m, as cosine coefficients c[0..m] with
    p(w) = c0 + 2 sum_k c_k cos(k w).  For the smooth spectra used here the tail is far
    below eps / 2, which the check of the range of e confirms."""
    return autocov(spec, m + 1, grid)


def eval_poly(c, w):
    return c[0] + 2 * sum(c[k] * np.cos(k * w) for k in range(1, len(c)))


def cond_mi(C, a, b, c):
    """I(a; b | c) in bits for a jointly Gaussian vector with covariance C; a, b, c index lists."""
    def h(idx):
        return 0.5 * ld(C[np.ix_(idx, idx)]) if len(idx) else 0.0
    return h(a + c) + h(b + c) - h(a + b + c) - h(c)


def run_case(name, f, B, A, H, SU, Q, eps, m, n, K, rng, out):
    p = B.shape[0]
    r_ = H.shape[0]
    w = 2 * np.pi * np.arange(4096) / 4096
    fmin = f(w).min()
    # --- 1. decomposition
    if fmin > 1e-9:                                 # q <= f, B_eps = B, e = f - q
        target = lambda x: f(x) - eps / 2
        c = trig_poly(target, m)
        Be = B.copy()
        e = f(w) - eval_poly(c, w)
    else:                                           # q >= f, B_eps = B - eps A, e = f + eps - q
        target = lambda x: f(x) + eps / 2
        c = trig_poly(target, m)
        Be = B - eps * A
        e = f(w) + eps - eval_poly(c, w)
    q = eval_poly(c, w)
    ok1 = (e.min() >= -1e-12 and e.max() <= eps + 1e-12 and q.min() >= 0
           and np.linalg.eigvalsh(Be).min() >= -1e-12
           and min(np.linalg.eigvalsh(Be + l * A).min() for l in (q.min(), q.max())) > 0)
    # --- window covariances, N = K (n + m)
    N = K * (n + m)
    rq = np.concatenate([c, np.zeros(max(0, N - len(c)))])          # autocovariance of the q-process
    re = autocov(lambda x: (f(x) - eval_poly(c, x)) if fmin > 1e-9 else (f(x) + eps - eval_poly(c, x)), N)
    Cq, Ce = toeplitz(rq, N), toeplitz(re, N)
    Sp = np.kron(Cq, A) + np.kron(np.eye(N), Be)                    # Cov T'
    SE = np.kron(Ce, A)                                             # Cov E
    rf = autocov(f, N)
    ST = np.kron(toeplitz(rf, N), A) + np.kron(np.eye(N), B)
    dec_err = float(np.abs(Sp + SE - ST).max())
    # --- 2. block independence
    blk = [list(range(k * (n + m) * p, (k * (n + m) + n) * p)) for k in range(K)]
    cross = max(float(np.abs(Sp[np.ix_(blk[i], blk[j])]).max()) for i in range(K) for j in range(K) if i != j)
    # --- 3. coupling: T' | T has mean G T with G = Sp ST^{-1}; drawn T' = G T + noise(Sp - G ST G^T)
    G = Sp @ np.linalg.inv(ST)
    cross_TE = float(np.abs(G @ ST - Sp).max())                     # Cov(T', T) = Sp  <=>  Cov(T', E) = 0
    # --- 4./5. joint Gaussian of (T', E, U, noise): description Z = Gz T'_blocks + W
    allblk = sum(blk, [])
    dz = 3
    Gz = rng.standard_normal((dz, len(allblk)))
    HN = np.kron(np.eye(N), H)
    d = N * p
    # variables: T' (d), E (d), Z (dz), S (N r), S' (N r)
    L_T = psd_sqrt(Sp)
    L_E = psd_sqrt(SE)                              # singular when A is rank one
    L_U = np.kron(np.eye(N), np.linalg.cholesky(SU))
    nz = d + d + N * r_ + dz                                        # independent standard normals: xT, xE, xU, xW
    def lin(MT=None, ME=None, MU=None, MW=None, rows=0):
        M = np.zeros((rows, nz))
        if MT is not None: M[:, :d] = MT @ L_T
        if ME is not None: M[:, d:2 * d] = ME @ L_E
        if MU is not None: M[:, 2 * d:2 * d + N * r_] = MU @ L_U
        if MW is not None: M[:, 2 * d + N * r_:] = MW
        return M
    Tsel = np.zeros((dz, d)); Tsel[:, allblk] = Gz
    rows = [lin(MT=np.eye(d), rows=d), lin(ME=np.eye(d), rows=d), lin(MT=Tsel, MW=0.7 * np.eye(dz), rows=dz),
            lin(MT=HN, ME=HN, MU=np.eye(N * r_), rows=N * r_), lin(MT=HN, MU=np.eye(N * r_), rows=N * r_)]
    M = np.vstack(rows)
    Cj = M @ M.T + 1e-11 * np.eye(M.shape[0])
    o = np.cumsum([0] + [x.shape[0] for x in rows])
    iT, iE, iZ, iS, iSp = (list(range(o[k], o[k + 1])) for k in range(5))
    blk_obs = [iSp[t * r_ + j] for k in range(K) for t in range(k * (n + m), k * (n + m) + n) for j in range(r_)]
    leak_real = cond_mi(Cj, iT, iZ, iS)                             # I(T'; Z | S)
    leak_clean = cond_mi(Cj, iT, iZ, iSp)                           # I(T'; Z | S')
    leak_blocks = cond_mi(Cj, iT, iZ, blk_obs)                      # I(T'; Z | S'_blocks)
    J = H.T @ np.linalg.inv(SU) @ H
    info_E = 0.5 * ld(np.eye(N * r_) + np.linalg.inv(np.kron(np.eye(N), SU)) @ HN @ SE @ HN.T)
    bound_E = N * eps * np.trace(J @ A) / (2 * LOG2)
    ok = (ok1 and dec_err < 1e-9 and cross < 1e-12 and cross_TE < 1e-9
          and leak_real <= leak_clean + info_E + 1e-7 and info_E <= bound_E + 1e-9
          and leak_clean <= leak_blocks + 1e-7)
    out[name] = dict(ok=bool(ok), eps=eps, m=m, n=n, K=K, N=N, e_min=float(e.min()), e_max=float(e.max()), q_min=float(q.min()),
                     decomposition_err=dec_err, block_cross_cov=cross, coupling_cross_cov=cross_TE,
                     leak_real=float(leak_real), leak_clean=float(leak_clean), leak_blocks=float(leak_blocks),
                     info_E=float(info_E), bound_E=float(bound_E))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: e in [{e.min():.2e}, {e.max():.2e}] (eps={eps}), q_min={q.min():.3f}, "
          f"decomp={dec_err:.1e}, block cross-cov={cross:.1e}, Cov(T',E)={cross_TE:.1e}\n"
          f"        I(T';Z|S)={leak_real:.6f} <= I(T';Z|S')={leak_clean:.6f} + I(E;HE+U)={info_E:.6f} "
          f"<= bound {bound_E:.6f};  I(T';Z|S')<= I(T';Z|S'_blocks)={leak_blocks:.6f}")
    return ok


def run_general(name, p, r, taps, decay, mprime, n, K, rng, out):
    """The decomposition of the proof as written for a general spectrum: Sigma is a matrix spectral density
    that is NOT affine in a scalar spectrum (a random vector moving average), Sigma' is a Fejer mean of Sigma
    minus (eps/2) I, of degree mprime, and the remainder Sigma^E = Sigma - Sigma' satisfies 0 <= Sigma^E <= eps I.
    The encoder's draw is built as it is performed: T' = G T + xi with private xi."""
    Gk = [rng.standard_normal((p, p)) * (decay ** k) for k in range(taps)]
    B0 = 0.3 * np.eye(p)
    H = rng.standard_normal((r, p))
    A0 = rng.standard_normal((r, r))
    SU = A0 @ A0.T / r + 0.5 * np.eye(r)
    F = rng.standard_normal((1, p))
    Q = F.T @ F
    J = H.T @ np.linalg.inv(SU) @ H

    def R(tau):                                    # E[T_{t+tau} T_t^T]
        t = abs(tau)
        M = sum(Gk[k] @ Gk[k - t].T for k in range(t, taps)) if t < taps else np.zeros((p, p))
        if t == 0:
            M = M + B0
        return M if tau >= 0 else M.T

    def spec(Rf, deg, w):
        return sum(Rf(t) * np.exp(-1j * w * t) for t in range(-deg, deg + 1))

    fej = lambda tau: (1 - abs(tau) / (mprime + 1)) * R(tau) if abs(tau) <= mprime else np.zeros((p, p))
    ws = 2 * np.pi * np.arange(2048) / 2048
    dev = max(np.linalg.norm(spec(R, taps - 1, w) - spec(fej, mprime, w), 2) for w in ws)
    eps = 2 * dev * (1 + 1e-9)                     # the Fejer mean is within eps / 2 of Sigma

    def Rp(tau):                                   # autocovariance of Sigma' = Fejer mean - (eps / 2) I
        M = fej(tau)
        return M - 0.5 * eps * np.eye(p) if tau == 0 else M

    eE = np.array([np.linalg.eigvalsh(spec(R, taps - 1, w) - spec(Rp, mprime, w)) for w in ws])
    eP = np.array([np.linalg.eigvalsh(spec(Rp, mprime, w)) for w in ws])
    a_S = min(np.linalg.eigvalsh(spec(R, taps - 1, w)).min() for w in ws)
    # is the spectrum outside the affine class?  Sigma(w) - Sigma(0) would then be multiples of one matrix
    D1 = np.real(spec(R, taps - 1, 1.0) - spec(R, taps - 1, 0.0)).ravel()
    D2 = np.real(spec(R, taps - 1, 2.0) - spec(R, taps - 1, 0.0)).ravel()
    non_affine = 1 - abs(D1 @ D2) / (np.linalg.norm(D1) * np.linalg.norm(D2))
    ok1 = eE.min() >= -1e-10 and eE.max() <= eps + 1e-10 and eP.min() >= a_S - eps - 1e-10 > 0 and non_affine > 1e-3

    N = K * (n + mprime)

    def btoep(Rf):
        S = np.zeros((N * p, N * p))
        for a in range(N):
            for b in range(N):
                S[a * p:(a + 1) * p, b * p:(b + 1) * p] = Rf(a - b)
        return S

    ST, SP = btoep(R), btoep(Rp)
    SE = ST - SP
    lamE = np.linalg.eigvalsh((SE + SE.T) / 2)
    blkT = [list(range(k * (n + mprime) * p, (k * (n + mprime) + n) * p)) for k in range(K)]
    cross = max(float(np.abs(SP[np.ix_(blkT[i], blkT[j])]).max()) for i in range(K) for j in range(K) if i != j)

    # the draw: T' = G T + xi, E = T - T'.  Drivers: xT (N p), xxi (N p), xU (N r), xW (dz)
    G = SP @ np.linalg.inv(ST)
    Cxi = SP - G @ ST @ G.T
    dz = 3
    d, dr = N * p, N * r
    nz = d + d + dr + dz

    def lin(MT=None, Mxi=None, MU=None, MW=None, rows=0):
        M = np.zeros((rows, nz))
        if MT is not None: M[:, :d] = MT @ psd_sqrt(ST)
        if Mxi is not None: M[:, d:2 * d] = Mxi @ psd_sqrt(Cxi)
        if MU is not None: M[:, 2 * d:2 * d + dr] = MU @ np.kron(np.eye(N), np.linalg.cholesky(SU))
        if MW is not None: M[:, 2 * d + dr:] = MW
        return M

    T = lin(MT=np.eye(d), rows=d)
    Tp = lin(MT=G, Mxi=np.eye(d), rows=d)
    E = T - Tp
    HN = np.kron(np.eye(N), H)
    U = lin(MU=np.eye(dr), rows=dr)
    S, Sp = HN @ T + U, HN @ Tp + U
    allblk = sum(blkT, [])
    Zsel = np.zeros((dz, d)); Zsel[:, allblk] = rng.standard_normal((dz, len(allblk)))
    Z = Zsel @ Tp + lin(MW=0.7 * np.eye(dz), rows=dz)
    blkS = [t * r + j for k in range(K) for t in range(k * (n + mprime), k * (n + mprime) + n) for j in range(r)]
    coup = max(float(np.abs(Tp @ E.T).max()), float(np.abs(Tp @ Tp.T - SP).max()), float(np.abs(E @ E.T - SE).max()))

    def h(Zm, Gm):                                  # h(Z | G) in bits, up to a constant
        Czz, Czg, Cgg = Zm @ Zm.T, Zm @ Gm.T, Gm @ Gm.T
        return 0.5 * ld(Czz - Czg @ np.linalg.solve(Cgg, Czg.T))

    h_S, h_Sp, h_blk = h(Z, S), h(Z, Sp), h(Z, Sp[blkS])
    I_E = 0.5 * ld(np.eye(dr) + np.linalg.inv(np.kron(np.eye(N), SU)) @ HN @ SE @ HN.T)
    bound_E = N * eps * np.trace(J) / (2 * LOG2)
    # distortion: for any linear reproduction B Z of the source, the weighted error splits exactly
    QN = np.kron(np.eye(N), Q)
    Bm = (Tp @ Z.T) @ np.linalg.inv(Z @ Z.T)       # the best linear reproduction of T' from Z
    errT, errTp = T - Bm @ Z, Tp - Bm @ Z
    dist_split = abs(np.trace(QN @ errT @ errT.T) - np.trace(QN @ errTp @ errTp.T) - np.trace(QN @ SE)) / N
    dist_E = float(np.trace(QN @ SE)) / N
    ok = (ok1 and lamE.min() >= -1e-9 and lamE.max() <= eps + 1e-9 and cross < 1e-12 and coup < 1e-9
          and h_S <= h_Sp + I_E + 1e-8 and I_E <= bound_E + 1e-9 and h_Sp <= h_blk + 1e-8
          and dist_split < 1e-9 and dist_E <= eps * np.trace(Q) + 1e-10)
    out[name] = dict(ok=bool(ok), p=p, r=r, source_memory=taps - 1, m=mprime, n=n, K=K, N=N, eps=float(eps),
                     min_eig_Sigma=float(a_S), non_affine_measure=float(non_affine),
                     remainder_eig_min=float(eE.min()), remainder_eig_max=float(eE.max()), min_eig_Sigma_prime=float(eP.min()),
                     window_remainder_eig_max=float(lamE.max()), block_cross_cov=cross, coupling_err=coup,
                     h_Z_given_S=float(h_S), h_Z_given_Sprime=float(h_Sp), h_Z_given_Sprime_blocks=float(h_blk),
                     info_E=float(I_E), bound_E=float(bound_E), distortion_split_err=float(dist_split),
                     distortion_from_E=dist_E, bound_distortion_from_E=float(eps * np.trace(Q)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: eps={eps:.4f} (min eig Sigma {a_S:.3f}), remainder spectrum in "
          f"[{eE.min():.2e}, {eE.max():.2e}], non-affine measure {non_affine:.3f}, block cross-cov={cross:.1e}, "
          f"coupling={coup:.1e}\n"
          f"        h(Z|S)={h_S:.6f} <= h(Z|S')={h_Sp:.6f} + I(E;HE+U)={I_E:.6f} <= bound {bound_E:.6f};  "
          f"h(Z|S') <= h(Z|S'_blocks)={h_blk:.6f}\n"
          f"        distortion: exact split error {dist_split:.1e}; from E {dist_E:.6f} <= eps tr Q = {eps * np.trace(Q):.6f}")
    return ok


def main():
    rng = np.random.default_rng(SEED)
    out = {}
    rho, a, tau2 = 0.8, 0.7, 0.5
    A = np.array([[rho ** 2, rho], [rho, 1.0]])
    Hm = np.array([[0.0, 1.0]])
    SU = np.array([[tau2]])
    Q = np.diag([1.0, 0.0])
    ar1 = lambda w: (1 - a * a) / (1 - 2 * a * np.cos(w) + a * a)          # min f > 0
    ok = run_case("pair_ar1_minf_positive", ar1, np.diag([1 - rho ** 2, 1e-9]), A, Hm, SU, Q,
                  eps=0.05, m=40, n=6, K=3, rng=rng, out=out)
    zero = lambda w: 2 * np.cos(w / 2) ** 2                                # f(pi) = 0, so B must be > 0
    ok &= run_case("zero_in_spectrum_minf_zero", zero, np.diag([0.5, 0.4]), A, Hm, SU, Q,
                   eps=0.05, m=12, n=5, K=3, rng=rng, out=out)
    # the general decomposition of the proof (a spectrum outside the affine class, Fejer mean)
    # the Fejer mean converges slowly, so the degree (and the guard) must be large for eps to be below min eig Sigma
    ok &= run_general("general_spectrum_fejer", p=2, r=2, taps=4, decay=0.4, mprime=14, n=6, K=2, rng=rng, out=out)
    out["_meta"] = dict(seed=SEED, numpy=np.__version__, all_ok=bool(ok))
    json.dump(out, open("verify_achievability.json", "w"), indent=1)
    print("all passed" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
