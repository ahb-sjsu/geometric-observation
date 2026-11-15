"""Numerical check of the two constructions in the lemma on windows for a holder
with a filter (labelled lem:filterwindows in the manuscript).

Part (a) of the lemma bounds the interior cost from above by the cost of a
stationary test channel Z_t = T_t + W_t, where W has the spectral density
N = (Delta^{-1} - Sigma^{-1})^{-1} and Delta = (1 - eta) Delta* is the error
spectrum of the spectral frontier point scaled down.  Checked here, on two
instances with a two-sided filter and colored noise (the second with a
rank-one filter whose response vanishes at frequency pi):

  a1. the spectral density of the pair (S, Z) is at least min(a_U, delta) I,
      and at each frequency the information between S and Z computed from the
      three determinants equals (1/2) log det(H Sigma H* + Sigma_U)
      - (1/2) log det(H Delta H* + Sigma_U), which is rate minus leakage;
  a2. for a window of N symbols, the cost bound of the proof,
        [ I(T^N; Z^N) - (1 - alpha) I(S_int; Z_int) ] / N,
      exceeds the spectral cost of Delta by an amount that shrinks as N grows,
      and the exact interior cost of the channel is below that bound;
  a3. the spectral cost of Delta exceeds V by at most (p/2) log2(1 / (1 - eta));
  a4. the error of the finite smoother of half-width k decreases to
      (1 - eta) D.

Part (b) embeds a window in the source of period n = N + 2 m_H + max(m, m_U).
Checked:

  b1. the middle N symbols of a block of the periodic source, with the holder's
      observations at their times (circular filter, circular colored noise),
      have exactly the covariance of (T^N, S^N) for the stationary source;
  b2. with n - 1 in place of n the two covariances differ when all three taps
      are nonzero, so the stated n is needed for this construction in general.
      (In the second instance one tap is zero and n - 1 still works; that is
      reported, not required.)

The noise process W is represented by its autocovariances computed on a
frequency grid, and the spectral quantities are means over the same grid.
Nothing here proves the lemma.

Run:  python verify_filter_lemma.py     (about a minute; writes verify_filter_lemma.json)
"""
import json
import sys
import time

import numpy as np

import spectral_core as sc
from verify_spectral import random_source, dmax
from verify_filter_colored import FilteredSpectrum

SEED = 20261119
LN2 = np.log(2.0)
GRID = 1024
OUT = {}
FAILED = []


def report(name, ok, **kv):
    OUT[name] = dict(ok=bool(ok), **kv)
    if not ok:
        FAILED.append(name)
    brief = ", ".join(f"{k}={v:.3e}" if isinstance(v, float) else f"{k}={v}" for k, v in kv.items() if k != "table")
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {brief}", flush=True)


def ld2(A):
    return float(np.linalg.slogdet(sc.herm(A))[1]) / LN2


def coeffs(F, lags):
    """Real matrix coefficients R(tau) = mean_k F(w_k) e^{+i w_k tau}, tau = 0..lags-1."""
    n = len(F)
    w = 2 * np.pi * np.arange(n) / n
    return [np.real(np.tensordot(np.exp(1j * w * t), F, axes=(0, 0))) / n for t in range(lags)]


def acov_from(co):
    def f(tau):
        t = abs(tau)
        if t >= len(co):
            return np.zeros_like(co[0])
        return co[t] if tau >= 0 else co[t].T
    return f


def btoep(acov, N, d):
    S = np.zeros((N * d, N * d))
    for a in range(N):
        for b in range(N):
            S[a * d:(a + 1) * d, b * d:(b + 1) * d] = acov(a - b)
    return S


def filter_matrix(sp, N):
    """Rows: observation times 1..N; columns: source times 1-mH .. N+mH."""
    p, r, mH = sp.p, sp.r, sp.mH
    HE = np.zeros((N * r, (N + 2 * mH) * p))
    for t in range(N):
        for k, Hk in sp.taps.items():
            j = t + mH - k
            HE[t * r:(t + 1) * r, j * p:(j + 1) * p] = Hk
    return HE


def mi2(Caa, Cab, Cbb):
    """I(a; b) in bits for jointly Gaussian vectors."""
    J = np.block([[Caa, Cab], [Cab.T, Cbb]])
    return 0.5 * (ld2(Caa) + ld2(Cbb) - ld2(J))


def part_a(tag, sp, alpha, eta, Ns):
    p, r, mH = sp.p, sp.r, sp.mH
    Dm = dmax(sp)
    D = 0.4 * Dm
    ws = 2 * np.pi * np.arange(GRID) / GRID
    sol = sc.spectral_solve(sp, GRID, alpha, D, half=True)
    Xh = sol["X"]
    Xs = [Xh[k] if k <= GRID // 2 else Xh[GRID - k].conj() for k in range(GRID)]
    V = sol["cost"]
    Sig = [sp.Sigma(w) for w in ws]
    Rs = [sc.psd_sqrt(S_) for S_ in Sig]
    Hw = [sp.H(w) for w in ws]
    SU = [sp.SUw(w) for w in ws]
    Del = [(1 - eta) * sc.herm(R_ @ X_ @ R_) for R_, X_ in zip(Rs, Xs)]
    Nn = [sc.herm(np.linalg.inv(np.linalg.inv(D_) - np.linalg.inv(S_))) for D_, S_ in zip(Del, Sig)]
    a_U = min(np.linalg.eigvalsh(u).min() for u in SU)
    dlt = min(np.linalg.eigvalsh(d).min() for d in Del)

    # a1: density of the pair and the per-frequency identity
    min_eig, ident = np.inf, 0.0
    cost_Delta = 0.0
    for k in range(GRID):
        A = np.vstack([Hw[k], np.eye(p)])
        F = sc.herm(A @ Sig[k] @ A.conj().T + np.block([[SU[k], np.zeros((r, p))], [np.zeros((p, r)), Nn[k]]]))
        min_eig = min(min_eig, float(np.linalg.eigvalsh(F).min()))
        FS = sc.herm(Hw[k] @ Sig[k] @ Hw[k].conj().T + SU[k])
        FZ = sc.herm(Sig[k] + Nn[k])
        i_det = 0.5 * (ld2(FS) + ld2(FZ) - ld2(F))
        i_schur = 0.5 * (ld2(FS) - ld2(Hw[k] @ Del[k] @ Hw[k].conj().T + SU[k]))
        Xk = (1 - eta) * Xs[k]
        Ht = Hw[k] @ Rs[k]
        rate_k = sc.rate(Xk)
        leak_k = sc.leak(Xk, Ht, SU[k])
        ident = max(ident, abs(i_det - i_schur), abs(i_schur - (rate_k - leak_k)))
        cost_Delta += (alpha * rate_k + (1 - alpha) * leak_k) / GRID
    ok1 = min_eig >= min(a_U, dlt) - 1e-9 and ident < 1e-9
    report(f"{tag}_a1_pair_density_and_identity", ok1, min_eig_pair=min_eig, lower_bound=float(min(a_U, dlt)), identity_err=ident)

    # a3: spectral cost of Delta against V
    exc = cost_Delta - V
    cap = 0.5 * p * np.log2(1 / (1 - eta))
    report(f"{tag}_a3_cost_of_scaled_spectrum", -1e-9 <= exc <= cap + 1e-9, excess=float(exc), cap=float(cap))

    # a2: finite windows
    Nmax = max(Ns)
    coS = [sp.autocov(t) for t in range(Nmax + 2 * mH + 1)]
    coN = coeffs(np.array(Nn), Nmax + 1)
    rows = []
    for N in Ns:
        L = N + 2 * mH
        SigE = btoep(acov_from(coS), L, p)
        win = np.arange(mH * p, (mH + N) * p)
        SigN = SigE[np.ix_(win, win)]
        NN = btoep(acov_from(coN), N, p)
        CU = btoep(sp.noise_autocov, N, r)
        HE = filter_matrix(sp, N)
        rate = 0.5 * (ld2(SigN + NN) - ld2(NN))                       # I(T^N; Z^N)
        ir = np.arange(mH * r, (N - mH) * r)                           # interior observation rows
        iz = np.arange(mH * p, (N - mH) * p)                           # Z at the interior times
        CSS = (HE @ SigE @ HE.T + CU)[np.ix_(ir, ir)]
        CSZ = (HE @ SigE[:, win])[ir]                                  # Cov(S_int, Z^N) = Cov(S_int, T^N)
        CZZ = SigN + NN
        i_int = mi2(CSS, CSZ[:, iz], CZZ[np.ix_(iz, iz)])              # I(S_int; Z_int)
        i_full = mi2(CSS, CSZ, CZZ)                                    # I(S_int; Z^N)
        bound = (rate - (1 - alpha) * i_int) / N
        exact = (rate - (1 - alpha) * i_full) / N
        rows.append(dict(N=N, bound=bound, exact=exact, excess=bound - cost_Delta, N_excess=N * (bound - cost_Delta)))
    ex = [x["excess"] for x in rows]
    ok2 = (all(x["exact"] <= x["bound"] + 1e-9 for x in rows) and all(e > -1e-6 for e in ex)
           and all(ex[i + 1] < ex[i] for i in range(len(ex) - 1)) and ex[-1] < 0.35 * ex[0])
    report(f"{tag}_a2_window_bound", ok2, cost_Delta=float(cost_Delta), V=float(V), first_excess=float(ex[0]),
           last_excess=float(ex[-1]), table=rows)

    # a4: finite smoother
    Qs = sp.Q
    target = float(np.mean([np.real(np.trace(Qs @ d)) for d in Del]))
    ds = []
    coT = coS
    for k in (0, 1, 2, 4, 8, 16):
        M = 2 * k + 1
        ST = btoep(acov_from(coT), M, p)
        NNk = btoep(acov_from(coN), M, p)
        c = slice(k * p, (k + 1) * p)
        Cty = ST[c, :]                                                 # Cov(T_t, Z window) = Cov(T_t, T window)
        err = ST[c, c] - Cty @ np.linalg.solve(ST + NNk, Cty.T)
        ds.append(float(np.trace(Qs @ err)))
    ok4 = all(ds[i + 1] <= ds[i] + 1e-10 for i in range(len(ds) - 1)) and ds[-1] >= target - 1e-6 and ds[-1] - target < 1e-3
    report(f"{tag}_a4_finite_smoother", ok4, limit=target, d_k=[round(x, 6) for x in ds], D=float(D), one_minus_eta_D=float((1 - eta) * D))


def circ_cov(acov, n, d, reach):
    """Block-circulant covariance with blocks sum_j R(a - b + j n)."""
    S = np.zeros((n * d, n * d))
    for a in range(n):
        for b in range(n):
            blk = np.zeros((d, d))
            for j in range(-reach, reach + 1):
                blk = blk + acov(a - b + j * n)
            S[a * d:(a + 1) * d, b * d:(b + 1) * d] = blk
    return S


def part_b(tag, sp, Ns, shorter_must_fail):
    p, r, mH = sp.p, sp.r, sp.mH
    m, mU = len(sp.G) - 1, len(sp.C) - 1

    def laws(N, n):
        # stationary: (T^N, S^N)
        L = N + 2 * mH
        SigE = btoep(sp.autocov, L, p)
        win = np.arange(mH * p, (mH + N) * p)
        HE = filter_matrix(sp, N)
        st_TT = SigE[np.ix_(win, win)]
        st_ST = HE @ SigE[:, win]
        st_SS = HE @ SigE @ HE.T + btoep(sp.noise_autocov, N, r)
        # periodic: block of n symbols, circular filter, circular noise; middle N are positions mH .. mH+N-1
        SigC = circ_cov(sp.autocov, n, p, 2)
        CUc = circ_cov(sp.noise_autocov, n, r, 2)
        Hc = np.zeros((n * r, n * p))
        for t in range(n):
            for k, Hk in sp.taps.items():
                j = (t - k) % n
                Hc[t * r:(t + 1) * r, j * p:(j + 1) * p] += Hk
        mt = np.arange(mH * p, (mH + N) * p)
        ms = np.arange(mH * r, (mH + N) * r)
        pe_TT = SigC[np.ix_(mt, mt)]
        pe_ST = (Hc @ SigC)[np.ix_(ms, mt)]
        pe_SS = (Hc @ SigC @ Hc.T + CUc)[np.ix_(ms, ms)]
        return max(float(np.abs(st_TT - pe_TT).max()), float(np.abs(st_ST - pe_ST).max()), float(np.abs(st_SS - pe_SS).max()))

    good, bad = 0.0, np.inf
    for N in Ns:
        n = N + 2 * mH + max(m, mU)
        good = max(good, laws(N, n))
        bad = min(bad, laws(N, n - 1))
    # the lemma claims only that the stated n suffices; that a shorter period fails is checked where it is
    # expected (all taps nonzero) and merely reported otherwise
    ok = good < 1e-12 and (bad > 1e-6 or not shorter_must_fail)
    report(f"{tag}_b_equality_of_laws", ok, max_err_with_stated_n=good, min_err_with_n_minus_1=float(bad),
           source_memory=m, noise_memory=mU, filter_half_length=mH)


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    base = random_source(rng, 2, 1, 1, taps=3, htaps=1)
    p, r = 2, 2
    taps = {-1: 0.5 * rng.standard_normal((r, p)), 0: rng.standard_normal((r, p)), 1: 0.6 * rng.standard_normal((r, p))}
    C = [0.8 * rng.standard_normal((r, r)), 0.5 * rng.standard_normal((r, r))]
    floor = 0.4 * np.eye(r)
    sp1 = FilteredSpectrum(base.G, base.B, taps, C, floor, base.Q)
    # second instance: rank-one filter whose response vanishes at frequency pi (taps h at 0 and at 1)
    h = np.outer(rng.standard_normal(r), rng.standard_normal(p))
    sp2 = FilteredSpectrum(base.G, base.B, {-1: np.zeros((r, p)), 0: h, 1: h}, C, floor, base.Q)
    assert np.abs(sp2.H(np.pi)).max() < 1e-12

    Ns = (6, 12, 24, 48)
    part_a("generic_alpha0", sp1, 0.0, 0.1, Ns)
    part_a("generic_alpha05", sp1, 0.5, 0.05, Ns)
    part_a("vanishing_filter_alpha0", sp2, 0.0, 0.1, Ns)
    part_b("generic", sp1, (1, 2, 3, 5, 9), shorter_must_fail=True)
    # here the tap at -1 is zero, so the filter reaches one symbol less and a period shorter by one still works
    part_b("vanishing_filter", sp2, (1, 2, 3, 5, 9), shorter_must_fail=False)

    OUT["_meta"] = dict(seed=SEED, numpy=np.__version__, failed=FAILED, seconds=round(time.time() - t0, 1), grid=GRID)
    json.dump(OUT, open("verify_filter_lemma.json", "w"), indent=1)
    print(f"{len(OUT) - 1 - len(FAILED)} passed, {len(FAILED)} failed, {OUT['_meta']['seconds']} s")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
