"""Numerical check of the two leakage chains in the proof of the coding
theorem for a holder with a filter (achievability and converse), on Gaussian
stand-ins for the message.

The message of a code is discrete.  Here it is replaced by a Gaussian vector
Z = (linear function of what the encoder codes) + independent noise, and
every conditional entropy H(M | .) in the proof by the conditional
differential entropy h(Z | .).  Each step of the two chains is an inequality
between such entropies that holds for the same reason (conditioning, a
Markov chain, or independence), so it can be tested exactly on covariances.
This does not verify the coding theorem.

Instance: moving-average source of memory 2 (p = 2), two-sided filter with
taps at -1, 0, 1 (r = 2), moving-average noise of memory 1.  The couplings
are built as the encoder performs them: the drawn vector is a linear
function of the WINDOW of the observed source plus private randomness, and
the source outside the window is whatever the true process makes it.

Achievability chain (source T = T' + E, Sigma' = Sigma - eps I; artificial
noise V with spectrum delta I; K blocks of length n with guards g):
   h(Z | S^N) <= h(Z | S_int) <= h(Z | S'_int) + I(E; filtered E + U_int)
             <= h(Z | S'_int + V_int) + I  <= h(Z | block interiors of S' + V) + I,
   I <= N eps c_H / (2 a_U ln 2),  and the blocks are i.i.d.

Converse chain (source T'' = T + E', Sigma'' = Sigma + eps I; noise
U = U^- + V'):
   h(Z | S''^N) <= h(Z | S''_int) <= h(Z | S^-_int) + I'      (system '')
   h(Z | S^-_int) <= h(Z | S^{-N}) + e_H <= h(Z | S^N) + e_H   (given system)
   I' <= N eps c_H / (a_U ln 2).

Run:  python verify_filter_chains.py    (a few seconds; writes verify_filter_chains.json)
"""
import json
import sys
import time

import numpy as np

import spectral_core as sc
from verify_spectral import random_source
from verify_filter_colored import FilteredSpectrum

SEED = 20261118
LN2 = np.log(2.0)
TOL = 1e-8
OUT = {}
FAILED = []


def report(name, ok, **kv):
    OUT[name] = dict(ok=bool(ok), **kv)
    if not ok:
        FAILED.append(name)
    brief = ", ".join(f"{k}={v:.4e}" if isinstance(v, float) else f"{k}={v}" for k, v in kv.items())
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {brief}", flush=True)


def ld2(A):
    return float(np.linalg.slogdet(sc.herm(A))[1]) / LN2


def psd_factor(A):
    """A real matrix L with L L^T = A, for A positive semidefinite."""
    w, V = np.linalg.eigh(sc.herm(A))
    assert w.min() > -1e-9 * max(1.0, w.max()), w.min()
    return np.real(V * np.sqrt(np.clip(w, 0, None)))


class Joint:
    """A jointly Gaussian family given as linear maps of independent standard normals."""

    def __init__(self, dims):
        self.off = np.cumsum([0] + list(dims))
        self.n = int(self.off[-1])
        self.rows = {}

    def driver(self, i, L):
        """Rows L applied to the i-th block of drivers."""
        M = np.zeros((L.shape[0], self.n))
        M[:, self.off[i]:self.off[i + 1]] = L
        return M

    def set(self, name, M):
        self.rows[name] = M

    def cov(self, a, b):
        return self.rows[a] @ self.rows[b].T

    def h_cond(self, z, given):
        """h(z | given) in bits, up to the constant (d/2) log2(2 pi e)."""
        Z = self.rows[z]
        if not given:
            return 0.5 * ld2(Z @ Z.T)
        Gm = np.vstack([self.rows[g] for g in given])
        Czz, Czg, Cgg = Z @ Z.T, Z @ Gm.T, Gm @ Gm.T
        return 0.5 * ld2(Czz - Czg @ np.linalg.solve(Cgg + 1e-13 * np.eye(len(Cgg)), Czg.T))


def toeplitz(acov, N, d):
    S = np.zeros((N * d, N * d))
    for a in range(N):
        for b in range(N):
            S[a * d:(a + 1) * d, b * d:(b + 1) * d] = acov(a - b)
    return S


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    base = random_source(rng, 2, 1, 1, taps=3, htaps=1)
    p, r = 2, 2
    taps = {-1: 0.5 * rng.standard_normal((r, p)), 0: rng.standard_normal((r, p)), 1: 0.6 * rng.standard_normal((r, p))}
    C = [0.8 * rng.standard_normal((r, r)), 0.5 * rng.standard_normal((r, r))]
    floor = 0.4 * np.eye(r)
    sp = FilteredSpectrum(base.G, base.B, taps, C, floor, base.Q)
    m, mH, mU = len(sp.G) - 1, sp.mH, len(sp.C) - 1

    n, g, K = 5, max(m, mU), 2
    N = K * (n + g)
    L = N + 2 * mH
    eps, delta = 0.05, 0.1
    ws = np.linspace(0, np.pi, 600)
    a_S = float(min(np.linalg.eigvalsh(sp.Sigma(w)).min() for w in ws))
    a_U = float(min(np.linalg.eigvalsh(sp.SUw(w)).min() for w in ws))
    b_S = float(max(np.linalg.eigvalsh(sp.H(w) @ sp.Sigma(w) @ sp.H(w).conj().T + sp.SUw(w)).max() for w in ws))
    c_H = float(sum(np.linalg.norm(h, "fro") ** 2 for h in taps.values()))
    e_H = mH * r * np.log2(2 * b_S / a_U)
    assert eps < a_S and delta < a_U / 2

    SigE = toeplitz(sp.autocov, L, p)                       # source on the extended window
    win = np.arange(mH * p, (mH + N) * p)
    Pw = np.eye(L * p)[win]                                 # selects T^N from T_ext
    SigN = SigE[np.ix_(win, win)]
    HE = np.zeros((N * r, L * p))
    for t in range(N):
        for k, Hk in taps.items():
            j = t + mH - k
            HE[t * r:(t + 1) * r, j * p:(j + 1) * p] = Hk
    int_rows = np.arange(mH * r, (N - mH) * r)              # interior observations
    Hint = HE[np.ix_(int_rows, win)]                        # they involve T^N only
    assert np.abs(np.delete(HE[int_rows], win, axis=1)).max() == 0
    CU = toeplitz(sp.noise_autocov, N, r)
    Ir = np.eye(N * r)
    blk_T = [np.arange(k * (n + g) * p, (k * (n + g) + n) * p) for k in range(K)]
    blk_Sint = [np.arange((k * (n + g) + mH) * r, (k * (n + g) + n - mH) * r) for k in range(K)]
    allblk = np.concatenate(blk_T)
    dz = 4
    Gz = rng.standard_normal((dz, len(allblk)))
    Zsel = np.zeros((dz, N * p))
    Zsel[:, allblk] = Gz

    # ---------------------------------------------------------------- achievability
    SigP = SigN - eps * np.eye(N * p)                       # window covariance of T'
    G = SigP @ np.linalg.inv(SigN)                          # T' = G T + xi
    Cxi = SigP - G @ SigN @ G.T
    J = Joint([L * p, N * p, N * r, N * r, dz])             # drivers: T_ext, xi, U, V, W
    T_ext = J.driver(0, psd_factor(SigE))
    T = Pw @ T_ext
    Tp = G @ T + J.driver(1, psd_factor(Cxi))
    E = T - Tp
    U = J.driver(2, psd_factor(CU))
    V = J.driver(3, np.sqrt(delta) * Ir)
    for name, M in (("T", T), ("Tp", Tp), ("E", E), ("S", HE @ T_ext + U),
                    ("S_int", (HE @ T_ext + U)[int_rows]),
                    ("Sp_int", Hint @ Tp + U[int_rows]),
                    ("SpV_int", Hint @ Tp + (U + V)[int_rows]),
                    ("Z", Zsel @ Tp + 0.7 * J.driver(4, np.eye(dz)))):
        J.set(name, M)
    full_int = np.arange(N * r)
    SpV_full = np.zeros((N * r, J.n))
    SpV_full[int_rows] = J.rows["SpV_int"]
    J.set("SpV_blk", np.vstack([SpV_full[b] for b in blk_Sint]))

    coupling = max(float(np.abs(J.cov("Tp", "E")).max()), float(np.abs(J.cov("Tp", "Tp") - SigP).max()),
                   float(np.abs(J.cov("E", "E") - eps * np.eye(N * p)).max()))
    report("ach_coupling", coupling < 1e-9, max_err=coupling)

    h1, h2 = J.h_cond("Z", ["S"]), J.h_cond("Z", ["S_int"])
    h3, h4, h5 = J.h_cond("Z", ["Sp_int"]), J.h_cond("Z", ["SpV_int"]), J.h_cond("Z", ["SpV_blk"])
    CUi = CU[np.ix_(int_rows, int_rows)]
    I_E = 0.5 * ld2(np.eye(len(int_rows)) + np.linalg.solve(CUi, Hint @ (eps * np.eye(N * p)) @ Hint.T))
    bound_E = N * eps * c_H / (2 * a_U * LN2)
    ok = h1 <= h2 + TOL and h2 <= h3 + I_E + TOL and h3 <= h4 + TOL and h4 <= h5 + TOL and I_E <= bound_E + TOL
    report("ach_leakage_chain", ok, h_S=h1, h_S_int=h2, h_Sp_int=h3, h_SpV_int=h4, h_SpV_blocks=h5,
           I_E=float(I_E), bound_I_E=float(bound_E), end_to_end_slack=float(h5 + I_E - h1))

    # the chain in the order displayed in the paper (eq. achchain): degrade to the block interiors with the
    # added noise first, then remove E:   h(Z | S^N) <= h(Z | S'_B + A_B E) <= h(Z | S'_B) + I(E; A_B E + U'_B)
    Brows = np.concatenate(blk_Sint)
    A_B = HE[np.ix_(Brows, win)]
    assert np.abs(np.delete(HE[Brows], win, axis=1)).max() == 0
    J.set("SV_blk", (HE @ T_ext + U + V)[Brows])            # = S'_B + A_B E
    same = float(np.abs(J.rows["SV_blk"] - (J.rows["SpV_blk"] + A_B @ E)).max())
    CUB = (CU + delta * Ir)[np.ix_(Brows, Brows)]
    I_B = 0.5 * ld2(np.eye(len(Brows)) + np.linalg.solve(CUB, A_B @ (eps * np.eye(N * p)) @ A_B.T))
    hB = J.h_cond("Z", ["SV_blk"])
    ok = same < 1e-12 and h1 <= hB + TOL and hB <= h5 + I_B + TOL and I_B <= bound_E + TOL
    report("ach_chain_as_displayed", ok, h_S=h1, h_SpB_plus_AE=hB, h_SpB=h5, I_E_B=float(I_B),
           bound_I_E=float(bound_E), identity_err=same, end_to_end_slack=float(h5 + I_B - h1))

    # blocks: pairs (block of T', block-interior observations of S' + V) are independent and identically distributed
    pair = [np.vstack([Tp[b_t], SpV_full[b_s]]) for b_t, b_s in zip(blk_T, blk_Sint)]
    cross = float(np.abs(pair[0] @ pair[1].T).max())
    same = float(np.abs(pair[0] @ pair[0].T - pair[1] @ pair[1].T).max())
    report("ach_blocks_iid", cross < 1e-9 and same < 1e-9, cross_cov=cross, law_difference=same)

    # ---------------------------------------------------------------- converse
    # given system: source T, noise U = U^- + V'  (V' white of power delta);  system '': source T'' = T + E'
    CUm = CU - delta * Ir                                    # covariance of U^-
    assert np.linalg.eigvalsh(CUm).min() >= a_U / 2 - 1e-9
    # the given system
    Jg = Joint([L * p, N * r, N * r, dz])                    # drivers: T_ext, U^-, V', W
    T_ext = Jg.driver(0, psd_factor(SigE))
    T = Pw @ T_ext
    Um = Jg.driver(1, psd_factor(CUm))
    Vp = Jg.driver(2, np.sqrt(delta) * Ir)
    Zg = Zsel @ T + 0.7 * Jg.driver(3, np.eye(dz))
    for name, M in (("Z", Zg), ("S", HE @ T_ext + Um + Vp), ("Sm", HE @ T_ext + Um),
                    ("Sm_int", (HE @ T_ext + Um)[int_rows])):
        Jg.set(name, M)
    g_full, g_minus, g_int = Jg.h_cond("Z", ["S"]), Jg.h_cond("Z", ["Sm"]), Jg.h_cond("Z", ["Sm_int"])

    # system '': the encoder sees T''^N and draws T^N = G2 T''^N + xi2
    SigE2 = SigE + eps * np.eye(L * p)
    SigN2 = SigN + eps * np.eye(N * p)
    G2 = SigN @ np.linalg.inv(SigN2)
    Cxi2 = SigN - G2 @ SigN2 @ G2.T
    J2 = Joint([L * p, N * p, N * r, dz])                    # drivers: T''_ext, xi2, U^-, W
    T2_ext = J2.driver(0, psd_factor(SigE2))
    T2 = Pw @ T2_ext
    Td = G2 @ T2 + J2.driver(1, psd_factor(Cxi2))            # the drawn T^N
    E2 = T2 - Td
    Um2 = J2.driver(2, psd_factor(CUm))
    for name, M in (("Td", Td), ("E2", E2), ("Z", Zsel @ Td + 0.7 * J2.driver(3, np.eye(dz))),
                    ("S2", HE @ T2_ext + Um2), ("S2_int", (HE @ T2_ext + Um2)[int_rows]),
                    ("Sm_int", Hint @ Td + Um2[int_rows])):
        J2.set(name, M)
    coupling = max(float(np.abs(J2.cov("Td", "E2")).max()), float(np.abs(J2.cov("Td", "Td") - SigN).max()),
                   float(np.abs(J2.cov("E2", "E2") - eps * np.eye(N * p)).max()))
    report("conv_coupling", coupling < 1e-9, max_err=coupling)

    k1, k2, k3 = J2.h_cond("Z", ["S2"]), J2.h_cond("Z", ["S2_int"]), J2.h_cond("Z", ["Sm_int"])
    CUmi = CUm[np.ix_(int_rows, int_rows)]
    I_E2 = 0.5 * ld2(np.eye(len(int_rows)) + np.linalg.solve(CUmi, Hint @ (eps * np.eye(N * p)) @ Hint.T))
    bound_E2 = N * eps * c_H / (a_U * LN2)
    same_law = abs(k3 - g_int)                               # (T^N, Z, S^-_int) has the same law in both systems
    edge = g_int - g_minus
    ok = (k1 <= k2 + TOL and k2 <= k3 + I_E2 + TOL and same_law < 1e-7 and -TOL <= edge <= e_H + TOL
          and g_minus <= g_full + TOL and I_E2 <= bound_E2 + TOL
          and k1 <= g_full + e_H + bound_E2 + TOL)
    report("conv_leakage_chain", ok, h_S2=k1, h_S2_int=k2, h_Sm_int=k3, same_law_err=float(same_law),
           h_Sm_given=g_minus, h_S_given=g_full, edge_bits=float(edge), e_H=float(e_H),
           I_E=float(I_E2), bound_I_E=float(bound_E2), end_to_end_slack=float(g_full + e_H + bound_E2 - k1),
           measured_increase=float(k1 - g_full))

    OUT["_meta"] = dict(seed=SEED, numpy=np.__version__, failed=FAILED, seconds=round(time.time() - t0, 1),
                        N=N, n=n, guard=g, K=K, eps=eps, delta=delta, a_S=a_S, a_U=a_U, b_S=b_S, c_H=c_H,
                        source_memory=m, filter_half_length=mH, noise_memory=mU)
    json.dump(OUT, open("verify_filter_chains.json", "w"), indent=1)
    print(f"{len(OUT) - 1 - len(FAILED)} passed, {len(FAILED)} failed, {OUT['_meta']['seconds']} s")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
