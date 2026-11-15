"""Steps of the proof of Theorem 23 (a holder with its whole observation
process) on instances.

For a window of N source symbols and holder observations on the window
extended by n times on each side, the script computes exactly

    kappa(N, n) = I(T^N; S_{1-n}^{N+n}) - I(T^N; S^N)   (bits),

checks that it is nondecreasing in n and at most s_N(Phi) / (2 ln 2), the
bound of the theorem, and checks the two intermediate bounds of the
proof.  A Gaussian vector Zd = C T^N + noise then stands in for the
message: h(Zd | S^N) - h(Zd | S_{1-n}^{N+n}) must be at most kappa.

Two instances: a moving-average source with a two-sided filter of three
taps and moving-average noise, and the same source with a causal filter
with taps A rho^k (cut at 60 taps) and white noise.  A check on
instances does not verify the theorem.  Run:  python verify_whole.py
"""
import json
import sys
import time

import numpy as np

SEED = 20261121
LN2 = np.log(2.0)
OUT = {}


def lndet(M):
    return np.linalg.slogdet(M)[1]


def cond_cov(S, a, b):
    Saa = S[np.ix_(a, a)]
    if len(b) == 0:
        return Saa
    Sab = S[np.ix_(a, b)]
    return Saa - Sab @ np.linalg.solve(S[np.ix_(b, b)], Sab.T)


def mi_bits(S, a, b):
    return 0.5 * (lndet(S[np.ix_(a, a)]) - lndet(cond_cov(S, a, b))) / LN2


class Instance:
    """Source T_t = e_t + B e_{t-1}; holder S_t = sum_k H_k T_{t-k} + U_t with
    U_t = v_t + Cn v_{t-1}; taps given as a dict {lag: matrix}."""

    def __init__(self, rng, taps, B, Cn, sig_v):
        self.taps, self.B, self.Cn, self.sig_v = taps, B, Cn, sig_v
        self.p = B.shape[0]
        self.r = Cn.shape[0]
        self.rng = rng

    def spectra(self, ngrid=8192):
        p, r = self.p, self.r
        ws = 2 * np.pi * np.arange(ngrid) / ngrid
        out = dict(Sigma=[], Phi=[], Err=[], SigS=[])
        self.err_grid = []
        self.ws = ws
        for w in ws:
            A = np.eye(p) + self.B * np.exp(-1j * w)
            Sig = A @ A.conj().T
            H = sum(Hk * np.exp(-1j * w * k) for k, Hk in self.taps.items())
            N_ = np.eye(r) + self.Cn * np.exp(-1j * w)
            SigU = self.sig_v * (N_ @ N_.conj().T)
            SigS = H @ Sig @ H.conj().T + SigU
            Phi = np.block([[Sig, Sig @ H.conj().T], [H @ Sig, SigS]])
            Err = Sig - Sig @ H.conj().T @ np.linalg.solve(SigS, H @ Sig)
            out['Sigma'].append(lndet(Sig))
            out['Phi'].append(lndet(Phi))
            out['Err'].append(lndet(Err))
            out['SigS'].append(lndet(SigS))
            self.err_grid.append(Err)
        self.err_grid = np.array(self.err_grid)
        return {k: float(np.mean(v)) for k, v in out.items()}

    def toeplitz_err(self, N):
        """T_N of the error spectrum, from its Fourier coefficients on the grid."""
        p = self.p
        coef = {}
        for tau in range(-(N - 1), N):
            ph = np.exp(1j * self.ws * tau)[:, None, None]
            coef[tau] = np.real(np.mean(self.err_grid * ph, axis=0))
        M = np.zeros((p * N, p * N))
        for a in range(N):
            for b in range(N):
                M[p * a:p * a + p, p * b:p * b + p] = coef[a - b]
        return M

    def joint(self, N, n):
        """Covariance of (T^N, S on times 1-n .. N+n, Zd) and index lists."""
        p, r = self.p, self.r
        kmin, kmax = min(self.taps), max(self.taps)
        t_lo, t_hi = 1 - n - kmax, N + n - kmin          # source times needed
        nt = t_hi - t_lo + 1
        ne = nt + 1                                      # innovations t_lo-1 .. t_hi
        G = np.zeros((p * nt, p * ne))
        for i in range(nt):
            G[p * i:p * i + p, p * (i + 1):p * (i + 2)] = np.eye(p)
            G[p * i:p * i + p, p * i:p * i + p] = self.B
        ns = N + 2 * n
        F = np.zeros((r * ns, p * nt))
        for j in range(ns):
            t = 1 - n + j
            for k, Hk in self.taps.items():
                col = t - k - t_lo
                F[r * j:r * j + r, p * col:p * col + p] = Hk
        nv = ns + 1
        Nz = np.zeros((r * ns, r * nv))
        for j in range(ns):
            Nz[r * j:r * j + r, r * (j + 1):r * (j + 2)] = np.eye(r)
            Nz[r * j:r * j + r, r * j:r * j + r] = self.Cn
        win = np.zeros((p * N, p * nt))
        o = 1 - t_lo
        win[:, p * o:p * o + p * N] = np.eye(p * N)
        C = np.random.default_rng(SEED + N).standard_normal((3, p * N)) / np.sqrt(N)
        d_e, d_v = p * ne, r * nv
        tot = d_e + d_v + 3

        def row(e=None, v=None, z=None, nrow=0):
            M = np.zeros((nrow, tot))
            if e is not None:
                M[:, :d_e] = e
            if v is not None:
                M[:, d_e:d_e + d_v] = v
            if z is not None:
                M[:, d_e + d_v:] = z
            return M

        L = np.vstack([row(e=win @ G, nrow=p * N),
                       row(e=F @ G, v=np.sqrt(self.sig_v) * Nz, nrow=r * ns),
                       row(e=C @ win @ G, z=0.3 * np.eye(3), nrow=3)])
        S = L @ L.T
        iT = list(range(p * N))
        iS = list(range(p * N, p * N + r * ns))
        iSwin = iS[r * n:r * n + r * N]
        iZ = list(range(p * N + r * ns, p * N + r * ns + 3))
        return S, iT, iS, iSwin, iZ


def run_instance(name, inst, Ns, ns):
    sp = inst.spectra()
    p = inst.p
    rows, ok = [], True
    tol = 1e-8
    for N in Ns:
        S0, iT, iS, iSwin, iZ = inst.joint(N, 0)
        lnd_Sigma = lndet(S0[np.ix_(iT, iT)])
        lnd_Phi = lndet(S0[np.ix_(iT + iSwin, iT + iSwin)])
        lnd_SigS = lndet(S0[np.ix_(iSwin, iSwin)])
        s_Sigma = lnd_Sigma - N * sp['Sigma']
        s_Phi = lnd_Phi - N * sp['Phi']
        s_SigS = lnd_SigS - N * sp['SigS']
        bound = s_Phi / (2 * LN2)
        s_Err = lndet(inst.toeplitz_err(N)) - N * sp['Err']
        sharp = (s_Phi - s_SigS - s_Err) / (2 * LN2)
        i_win = mi_bits(S0, iT, iSwin)
        # lower bound of the proof on I(T^N; S^N)
        low = (N * (sp['Sigma'] + sp['SigS'] - sp['Phi']) + s_Sigma - s_Phi) / (2 * LN2)
        # upper bound of the proof on I(T^N; S_T)
        up = (N * (sp['Sigma'] - sp['Err']) + s_Sigma) / (2 * LN2)
        ident = abs(sp['Phi'] - sp['SigS'] - sp['Err'])
        prev, kap_list, stand = -1e-12, [], []
        good = (s_Sigma >= -tol and s_Phi >= -tol and s_SigS >= -tol and i_win >= low - tol and ident < 1e-9)
        for n in ns:
            S, iT, iS, iSwin, iZ = inst.joint(N, n)
            i_all = mi_bits(S, iT, iS)
            kap = i_all - mi_bits(S, iT, iSwin)
            hz_win = 0.5 * lndet(cond_cov(S, iZ, iSwin)) / LN2
            hz_all = 0.5 * lndet(cond_cov(S, iZ, iS)) / LN2
            good = good and (kap >= prev - tol) and (kap <= bound + tol) and (i_all <= up + tol)
            good = good and (hz_win - hz_all >= -tol) and (hz_win - hz_all <= kap + tol)
            prev = kap
            kap_list.append(kap)
            stand.append(hz_win - hz_all)
        # the sharper value: kappa never exceeds it and reaches it as n grows
        good = good and s_Err >= -tol and all(x <= sharp + 1e-7 for x in kap_list) and abs(kap_list[-1] - sharp) < 1e-4
        rows.append(dict(N=N, s_Sigma=s_Sigma, s_Phi=s_Phi, s_SigS=s_SigS, s_Err=s_Err, sharp_bits=sharp,
                         bound_bits=bound, kappa=kap_list,
                         standin_drop=stand, I_window=i_win, lower=low, upper=up, ok=bool(good)))
        ok = ok and good
        print(f"{name}  N={N:2d}  bound s_N(Phi)/(2 ln 2) = {bound:.4f} bits   sharper value = {sharp:.5f}   kappa at n={ns}: "
              + ' '.join(f'{x:.4f}' for x in kap_list) + f"   stand-in drop at largest n: {stand[-1]:.4f}"
              + ('  PASS' if good else '  FAIL'))
    return ok, dict(spectra=sp, table=rows, extensions=list(ns))


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    p = r = 2
    B = 0.5 * rng.standard_normal((p, p))
    Cn = 0.4 * rng.standard_normal((r, r))
    failed = []
    taps_fir = {k: rng.standard_normal((r, p)) for k in (-1, 0, 1)}
    inst1 = Instance(rng, taps_fir, B, Cn, sig_v=0.5)
    ok, rec = run_instance('finite filter, colored noise', inst1, Ns=(2, 4, 8, 16), ns=(0, 1, 2, 4, 8, 16, 32))
    OUT['finite_filter_colored_noise'] = dict(ok=ok, **rec)
    if not ok:
        failed.append('finite_filter_colored_noise')
    A = rng.standard_normal((r, p))
    taps_iir = {k: A * 0.6 ** k for k in range(60)}
    inst2 = Instance(rng, taps_iir, B, np.zeros((r, r)), sig_v=0.5)
    ok, rec = run_instance('geometric taps, white noise ', inst2, Ns=(2, 4, 8, 16), ns=(0, 1, 2, 4, 8, 16, 32))
    OUT['geometric_taps_white_noise'] = dict(ok=ok, **rec)
    if not ok:
        failed.append('geometric_taps_white_noise')
    for k in ('finite_filter_colored_noise', 'geometric_taps_white_noise'):
        print(('PASS' if OUT[k]['ok'] else 'FAIL'), k)
    OUT['_meta'] = dict(seed=SEED, failed=failed, seconds=round(time.time() - t0, 1), numpy=np.__version__)
    json.dump(OUT, open('verify_whole.json', 'w'), indent=1, default=float)
    print('failed:', failed, '| seconds:', OUT['_meta']['seconds'])
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
