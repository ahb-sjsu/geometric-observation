"""Numerical checks of the inequalities in the proof of the achievability theorem
(Theorem 11 and Lemma 12 of the manuscript).

The theorem is a coding theorem and is not something a computation can verify.
What is checked here, on Gaussian stand-ins for the message, are the steps of
the proof that are statements about covariances:

  1. decomposition  Sigma = Sigma' + e A  with Sigma' a trigonometric polynomial
     density, 0 <= e <= eps, both cases of the proof (min f > 0, and min f = 0);
  2. blocks of the finite-memory process separated by guard intervals of m
     symbols are exactly uncorrelated;
  3. the coupling: drawing T' from its conditional law given T = T' + E returns
     the product law (checked on covariances);
  4. the leakage perturbation: for a Gaussian description Z of T',
        I(T'; Z | S)  <=  I(T'; Z | S')  +  I(E; HE + U),
     and I(E; HE + U) <= N eps tr(J A) / (2 ln 2);
  5. dropping the guard observations cannot lower the leakage bound:
        I(T'; Z | S'_all) <= I(T'; Z | S'_blocks).

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
    out["_meta"] = dict(seed=SEED, numpy=np.__version__, all_ok=bool(ok))
    json.dump(out, open("verify_achievability.json", "w"), indent=1)
    print("all passed" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
