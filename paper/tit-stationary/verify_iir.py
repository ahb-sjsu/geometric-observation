"""Steps of the proof of Theorem 22 (a holder whose filter has an infinite
impulse response) on Gaussian stand-ins.

A Gaussian vector Zd = C T^N + noise stands in for the message, and
conditional differential entropies stand in for the entropies of the
message.  This checks the direction of each inequality of the proof on
instances.  It does not verify the coding theorem.

Instance: a vector moving-average source of memory one (p = 2), a causal
filter with taps H_k = A rho^k (cut at K = 80 taps, where rho^K is below
1e-17), white holder noise.  Run:  python verify_iir.py
"""
import json
import sys
import time

import numpy as np

SEED = 20261120
LN2 = np.log(2.0)
OUT = {}


def logdet2(M):
    return np.linalg.slogdet(M)[1] / LN2


def cond_cov(S, a, b):
    """Covariance of block a given block b, from the joint covariance S."""
    Saa = S[np.ix_(a, a)]
    if len(b) == 0:
        return Saa
    Sab = S[np.ix_(a, b)]
    Sbb = S[np.ix_(b, b)]
    return Saa - Sab @ np.linalg.solve(Sbb, Sab.T)


def mi(S, a, b, c=()):
    """I(a; b | c) in bits for jointly Gaussian blocks of S."""
    a, b, c = list(a), list(b), list(c)
    return 0.5 * (logdet2(cond_cov(S, a, c)) - logdet2(cond_cov(S, a, b + c)))


def instance(rng, N, m, eps, rho, sig_u, K=80):
    p, r = 2, 2
    B = 0.5 * rng.standard_normal((p, p))
    A = rng.standard_normal((r, p))
    # source on times 1-K .. N, driven by innovations on times -K .. N
    nt = N + K
    ne = nt + 1
    G = np.zeros((p * nt, p * ne))
    for i in range(nt):
        G[p * i:p * i + p, p * (i + 1):p * (i + 1) + p] = np.eye(p)
        G[p * i:p * i + p, p * i:p * i + p] = B
    # filter matrices on the window times 1..N (index K .. K+N-1 in the source)
    F_all = np.zeros((r * N, p * nt))
    F_cut = np.zeros((r * N, p * nt))
    for t in range(N):
        for k in range(K):
            blk = A * rho ** k
            col = K + t - k
            F_all[r * t:r * t + r, p * col:p * col + p] = blk
            if k <= m:
                F_cut[r * t:r * t + r, p * col:p * col + p] = blk
    F_tail = F_all - F_cut
    win = np.zeros((p * N, p * nt))
    win[:, p * K:] = np.eye(p * N)
    C = rng.standard_normal((3, p * N)) / np.sqrt(N)
    # independent Gaussian inputs: innovations, U^-, W, W', description noise
    d_e, d_u = p * ne, r * N
    dims = [d_e, d_u, d_u, d_u, 3]
    off = np.concatenate([[0], np.cumsum(dims)])
    tot = off[-1]

    def row(e=None, um=None, w=None, wp=None, z=None, nrow=0):
        M = np.zeros((nrow, tot))
        for j, x in enumerate((e, um, w, wp, z)):
            if x is not None:
                M[:, off[j]:off[j + 1]] = x
        return M

    Iu = np.eye(d_u)
    su_minus = np.sqrt(sig_u - eps)
    se = np.sqrt(eps)
    rows = {
        'Zd': row(e=C @ win @ G, z=0.3 * np.eye(3), nrow=3),
        'S': row(e=F_all @ G, um=su_minus * Iu, w=se * Iu, nrow=d_u),
        'Sm': row(e=F_cut @ G, um=su_minus * Iu, nrow=d_u),
        'Sp': row(e=F_cut @ G, um=su_minus * Iu, w=se * Iu, wp=se * Iu, nrow=d_u),
        'Gam': row(e=F_tail @ G, nrow=d_u),
        'GamW': row(e=F_tail @ G, w=se * Iu, nrow=d_u),
        'WpGam': row(e=-F_tail @ G, wp=se * Iu, nrow=d_u),
        'T': row(e=win @ G, nrow=p * N),
    }
    names = list(rows)
    L = np.vstack([rows[k] for k in names])
    S = L @ L.T
    idx, pos = {}, 0
    for k in names:
        idx[k] = list(range(pos, pos + rows[k].shape[0]))
        pos += rows[k].shape[0]
    # constants of the proof
    tm = sum(np.linalg.norm(A * rho ** k, 'fro') ** 2 for k in range(m + 1, K))
    # b: largest eigenvalue of the spectral density of the source
    ws = np.linspace(-np.pi, np.pi, 2001)
    b = max(np.linalg.eigvalsh((np.eye(p) + B * np.exp(-1j * w)) @ (np.eye(p) + B * np.exp(-1j * w)).conj().T).max()
            for w in ws)
    c = b * tm / (2 * eps * LN2)
    return S, idx, dict(N=N, m=m, eps=eps, rho=rho, tm=tm, b=b, c=c)


def check_chains(rng):
    rows, ok = [], True
    for (N, m, eps, rho) in [(6, 2, 0.10, 0.5), (8, 3, 0.05, 0.6), (8, 6, 0.02, 0.5), (10, 1, 0.20, 0.7)]:
        S, ix, par = instance(rng, N, m, eps, rho, sig_u=0.6)
        Nc = N * par['c']
        hS = 0.5 * logdet2(cond_cov(S, ix['Zd'], ix['S']))
        hSm = 0.5 * logdet2(cond_cov(S, ix['Zd'], ix['Sm']))
        hSp = 0.5 * logdet2(cond_cov(S, ix['Zd'], ix['Sp']))
        # the power bound and (tailinfo)
        trG = np.trace(S[np.ix_(ix['Gam'], ix['Gam'])])
        i_tail = mi(S, ix['Gam'], ix['GamW'])
        i_tail2 = mi(S, ix['Gam'], ix['WpGam'])
        # the conditional informations that the proof bounds by the tail information
        i_dn = mi(S, ix['Zd'], ix['GamW'], ix['Sm'])
        i_up = mi(S, ix['Zd'], ix['WpGam'], ix['S'])
        # the identities S = S^- + Gam + W and S^+ = S - Gam + W'
        L1 = S[np.ix_(ix['S'], ix['S'])]
        e1 = np.abs(cond_cov(S, ix['S'], ix['Sm'] + ix['GamW'])).max()
        e2 = np.abs(cond_cov(S, ix['Sp'], ix['S'] + ix['WpGam'])).max()
        tol = 1e-9
        row = dict(par, power=trG, power_bound=N * par['b'] * par['tm'], tail_info=i_tail, tail_info_2=i_tail2,
                   Nc=Nc, cond_info_down=i_dn, cond_info_up=i_up, h_given_S=hS, h_given_Sminus=hSm,
                   h_given_Splus=hSp, identity_err=max(e1, e2) / np.abs(L1).max())
        good = (trG <= N * par['b'] * par['tm'] + tol and i_tail <= Nc + tol and i_tail2 <= Nc + tol
                and i_dn <= i_tail + tol and i_up <= i_tail2 + tol
                and hSm <= hS + i_dn + tol and hS <= hSp + i_up + tol
                and hSm <= hS + Nc + tol and hS <= hSp + Nc + tol
                and row['identity_err'] < 1e-10)
        row['ok'] = bool(good)
        ok = ok and good
        rows.append(row)
    return ok, rows


def check_lipschitz(rng, trials=20000):
    worst = 0.0
    for _ in range(trials):
        p = int(rng.integers(1, 5))

        def psd(scale):
            X = rng.standard_normal((p, p)) + 1j * rng.standard_normal((p, p))
            return scale * (X @ X.conj().T) / p

        Sig = psd(1.0) + 0.05 * np.eye(p)
        b = np.linalg.eigvalsh(Sig).max()
        Wm = psd(1.0) + 0.05 * np.eye(p)
        Dl = np.linalg.inv(np.linalg.inv(Sig) + Wm)          # 0 < Delta <= Sigma
        J = psd(rng.uniform(0, 3))
        Jp = J + rng.uniform(0, 1) * (psd(1.0) - psd(1.0))
        w, Q = np.linalg.eigh(Jp)
        Jp = (Q * np.clip(w, 0, None)) @ Q.conj().T          # positive semidefinite

        def phi(Jm):
            I = np.eye(p)
            return 0.5 * (logdet2(I + Sig @ Jm) - logdet2(I + Dl @ Jm))

        lhs = abs(phi(J) - phi(Jp))
        rhs = p * b / (2 * LN2) * np.linalg.norm(J - Jp, 2)
        worst = max(worst, lhs / rhs if rhs > 0 else 0.0)
    return worst <= 1 + 1e-9, worst


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    failed = []
    ok, rows = check_chains(rng)
    OUT['leakage_comparisons'] = dict(ok=ok, table=rows)
    for r in rows:
        print(f"N={r['N']:2d} m={r['m']} eps={r['eps']:.2f} rho={r['rho']:.1f}  tail info={r['tail_info']:.4f}"
              f" <= Nc={r['Nc']:.4f}   h(Z|S-)={r['h_given_Sminus']:.4f}  h(Z|S)={r['h_given_S']:.4f}"
              f"  h(Z|S+)={r['h_given_Splus']:.4f}  (checked: each is at most the next plus Nc)"
              f"  {'PASS' if r['ok'] else 'FAIL'}")
    print(('PASS' if ok else 'FAIL'), 'leakage comparisons (eqs. for the two holders) and the tail bound')
    if not ok:
        failed.append('leakage_comparisons')
    ok2, worst = check_lipschitz(rng)
    OUT['lipschitz_in_J'] = dict(ok=ok2, worst_ratio=worst)
    print(('PASS' if ok2 else 'FAIL'), f'Lipschitz bound in J: largest ratio of change to bound {worst:.4f} (must be <= 1)')
    if not ok2:
        failed.append('lipschitz_in_J')
    OUT['_meta'] = dict(seed=SEED, failed=failed, seconds=round(time.time() - t0, 1), numpy=np.__version__)
    json.dump(OUT, open('verify_iir.json', 'w'), indent=1, default=float)
    print('failed:', failed, '| seconds:', OUT['_meta']['seconds'])
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
