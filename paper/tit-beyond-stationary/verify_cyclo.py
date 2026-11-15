"""Checks for the cyclostationary results of "Rate and Leakage Beyond
Stationary Gaussian Sources".

A cyclostationary source of period q is stacked, one period at a time, into
a stationary vector source in R^{pq}.  The checks are

  harmonic_form      the stacked spectral density is unitarily equivalent, by
                     a matrix that does not depend on the source, to the
                     matrix of cyclic spectra  [f_{k-l}((w + 2 pi k)/q)]
  blocking           for a stationary source, the stacked spectral cost per
                     symbol equals the spectral cost of the companion paper
                     (memoryless holder map and a filter)
  phase_shift        stacking from a different starting phase gives the same
                     cost
  window_converse    window costs of a cyclostationary source at N = kq are
                     at least the stacked spectral cost and decrease to it
  window_any_N       for N not a multiple of q the window cost is at least
                     the spectral cost at distortion D + q dbar / N
  regimes            a source made of independent stationary segments: the
                     joint window problem equals the allocation over the
                     segments under one level
  averaged_spectrum  with time-invariant parties, the stationary source with
                     the time-averaged spectrum costs at least as much

The solver is spectral_core.py of the companion paper, imported from
../tit-stationary.  numpy only.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tit-stationary"))
import spectral_core as sc  # noqa: E402
from verify_spectral import random_source  # noqa: E402

SEED = 20261115
OUT = {}
FAILED = []


def report(name, ok, **kv):
    OUT[name] = dict(ok=bool(ok), **kv)
    if not ok:
        FAILED.append(name)
    brief = ", ".join(f"{k}={v:.3e}" if isinstance(v, float) else f"{k}={v}" for k, v in kv.items() if k != "table")
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {brief}", flush=True)


# ------------------------------------------------------------ the source
class PMA:
    """Periodic moving average of period q in R^p:
        T_t = sum_{k=0}^{m} A[t mod q][k] xi_{t-k} + B[t mod q]^{1/2} eta_t,
    xi, eta white N(0, I).  Phase a = t mod q, a = 0..q-1.
    Decoder weight Q[a], memoryless holder S_t = H[a] T_t + U_t, Cov U_t = SU[a]."""

    def __init__(self, A, B, Q, H, SU):
        self.A, self.B, self.Q, self.H, self.SU = A, B, Q, H, SU
        self.q = len(A)
        self.m = len(A[0]) - 1
        self.p = B[0].shape[0]
        self.r = H[0].shape[0]

    def cov(self, s, t):
        """E[T_s T_t^T]."""
        a, b = s % self.q, t % self.q
        out = np.zeros((self.p, self.p))
        for k in range(self.m + 1):
            l = k + (t - s)
            if 0 <= l <= self.m:
                out = out + self.A[a][k] @ self.A[b][l].T
        if s == t:
            out = out + self.B[a]
        return out

    def window_cov(self, N, start=0):
        p = self.p
        S = np.zeros((N * p, N * p))
        for i in range(N):
            for j in range(N):
                S[i * p:(i + 1) * p, j * p:(j + 1) * p] = self.cov(start + i, start + j)
        return S

    def stacked_acov(self, j, start=0):
        """Cov(stacked_{j0+j}, stacked_{j0}), stacked_j = (T_{start+jq+a})_a."""
        q, p = self.q, self.p
        Rj = np.zeros((q * p, q * p))
        for a in range(q):
            for b in range(q):
                Rj[a * p:(a + 1) * p, b * p:(b + 1) * p] = self.cov(start + j * q + a, start + b)
        return Rj

    def stacked_sigma(self, w, start=0):
        J = self.m // self.q + 2
        return sc.herm(sum(self.stacked_acov(j, start) * np.exp(-1j * w * j) for j in range(-J, J + 1)))

    def diag(self, mats, start=0, reps=1):
        q = self.q
        blocks = [mats[(start + i) % q] for i in range(q * reps)] if reps else []
        return blocks

    def stacked_block(self, w, start=0):
        q = self.q
        Qs = block_diag([self.Q[(start + a) % q] for a in range(q)])
        Hs = block_diag([self.H[(start + a) % q] for a in range(q)])
        SUs = block_diag([self.SU[(start + a) % q] for a in range(q)])
        R = sc.psd_sqrt(self.stacked_sigma(w, start))
        return sc.herm(R @ Qs @ R), Hs @ R, SUs.astype(complex)

    def dbar(self):
        """Largest per-symbol maximal distortion over the phases."""
        return max(float(np.trace(self.Q[a] @ self.cov(a, a))) for a in range(self.q))

    def dmax(self):
        return float(np.mean([np.trace(self.Q[a] @ self.cov(a, a)) for a in range(self.q)]))


def block_diag(mats):
    rows = sum(M.shape[0] for M in mats)
    cols = sum(M.shape[1] for M in mats)
    out = np.zeros((rows, cols), dtype=np.result_type(*mats))
    i = j = 0
    for M in mats:
        out[i:i + M.shape[0], j:j + M.shape[1]] = M
        i += M.shape[0]
        j += M.shape[1]
    return out


def random_pma(rng, q, p, r, m=2, same_parties=False):
    A = [[rng.standard_normal((p, p)) * (0.7 ** k) for k in range(m + 1)] for _ in range(q)]
    B = [0.3 * np.eye(p) + 0.1 * a * np.eye(p) for a in range(q)]
    if same_parties:
        F = rng.standard_normal((1, p))
        Q = [F.T @ F + 0.2 * np.eye(p)] * q
        H0 = rng.standard_normal((r, p))
        H = [H0] * q
        SU = [0.6 * np.eye(r)] * q
    else:
        Q, H, SU = [], [], []
        for a in range(q):
            F = rng.standard_normal((1, p))
            Q.append(F.T @ F + 0.2 * np.eye(p))
            H.append(rng.standard_normal((r, p)))
            SU.append((0.5 + 0.2 * a) * np.eye(r))
    return PMA(A, B, Q, H, SU)


def stacked_spectral(src, alpha, D, n=128, start=0):
    """Per-symbol stacked spectral cost: (1/q) V~(alpha, q D)."""
    q = src.q
    blocks = [src.stacked_block(2 * np.pi * j / n, start) for j in range(n)]
    sol = sc.solve(blocks, np.full(n, 1.0 / n), alpha, q * D)
    return sol["cost"] / q, sol


def window_cost(src, N, alpha, D, start=0):
    q = src.q
    S = src.window_cov(N, start)
    R = np.real(sc.psd_sqrt(S))
    Qn = block_diag([src.Q[(start + i) % q] for i in range(N)])
    Hn = block_diag([src.H[(start + i) % q] for i in range(N)])
    SUn = block_diag([src.SU[(start + i) % q] for i in range(N)])
    sol = sc.solve([(sc.herm(R @ Qn @ R), Hn @ R, SUn)], [1.0 / N], alpha, D)
    return sol["cost"]


# ------------------------------------------------------------ checks
def check_harmonic(rng):
    worst = 0.0
    worst_herm = 0.0
    cases = 0
    for (q, p) in [(2, 1), (3, 1), (2, 2), (4, 2), (5, 1)]:
        src = random_pma(rng, q, p, 1, m=3)
        m = src.m

        def R_t(t, tau):
            return src.cov(t + tau, t)

        def f(k, lam):
            out = np.zeros((p, p), dtype=complex)
            for tau in range(-m, m + 1):
                Bk = sum(R_t(t, tau) * np.exp(-2j * np.pi * k * t / q) for t in range(q)) / q
                out = out + Bk * np.exp(-1j * lam * tau)
            return out

        for w in rng.uniform(-np.pi, np.pi, 5):
            lam = [(w + 2 * np.pi * k) / q for k in range(q)]
            V = np.zeros((q * p, q * p), dtype=complex)
            Fm = np.zeros((q * p, q * p), dtype=complex)
            for a in range(q):
                for k in range(q):
                    V[a * p:(a + 1) * p, k * p:(k + 1) * p] = np.exp(1j * a * lam[k]) / np.sqrt(q) * np.eye(p)
            for k in range(q):
                for l in range(q):
                    Fm[k * p:(k + 1) * p, l * p:(l + 1) * p] = f((k - l) % q, lam[k])
            lhs = V.conj().T @ src.stacked_sigma(w) @ V
            worst = max(worst, float(np.abs(lhs - Fm).max()))
            worst_herm = max(worst_herm, float(np.abs(V.conj().T @ V - np.eye(q * p)).max()))
            cases += 1
    report("harmonic_form", worst < 1e-10 and worst_herm < 1e-12, max_err=worst, unitary_err=worst_herm, cases=cases)


class StackedStationary:
    """A stationary sc.Spectrum viewed as cyclostationary of period q."""

    def __init__(self, sp, q):
        self.sp, self.q, self.p = sp, q, sp.p
        self.r = sp.Hk[0].shape[0]

    def sigma(self, w):
        q, p = self.q, self.p
        K = len(self.sp.G)
        J = K // q + 2
        out = np.zeros((q * p, q * p), dtype=complex)
        for j in range(-J, J + 1):
            Rj = np.zeros((q * p, q * p))
            for a in range(q):
                for b in range(q):
                    Rj[a * p:(a + 1) * p, b * p:(b + 1) * p] = self.sp.autocov(j * q + a - b)
            out = out + Rj * np.exp(-1j * w * j)
        return sc.herm(out)

    def Hs(self, w):
        """Stacked filter response: tap l has block (a,b) = H_{a-b+lq}."""
        q, p, r = self.q, self.p, self.r
        K = len(self.sp.Hk)
        J = K // q + 2
        out = np.zeros((q * r, q * p), dtype=complex)
        for l in range(-J, J + 1):
            for a in range(q):
                for b in range(q):
                    k = a - b + l * q
                    if 0 <= k < K:
                        out[a * r:(a + 1) * r, b * p:(b + 1) * p] += self.sp.Hk[k] * np.exp(-1j * w * l)
        return out

    def block(self, w):
        R = sc.psd_sqrt(self.sigma(w))
        Qs = np.kron(np.eye(self.q), self.sp.Q)
        SUs = np.kron(np.eye(self.q), self.sp.SU).astype(complex)
        return sc.herm(R @ Qs @ R), self.Hs(w) @ R, SUs


def check_blocking(rng):
    worst = 0.0
    cases = 0
    for (p, m, r, q, htaps) in [(1, 1, 1, 2, 1), (2, 1, 1, 3, 1), (2, 1, 1, 2, 2), (1, 1, 1, 4, 3), (2, 2, 2, 2, 2)]:
        sp = random_source(rng, p, m, r, htaps=htaps)
        st = StackedStationary(sp, q)
        nprime = 24
        n = nprime * q
        dm = float(np.mean([np.real(np.trace(sp.Q @ sp.Sigma(2 * np.pi * k / n))) for k in range(n)]))
        for alpha in (0.0, 0.4, 1.0):
            for frac in (0.3, 0.7):
                D = frac * dm
                ref = sc.spectral_solve(sp, n, alpha, D)
                sol = sc.solve([st.block(2 * np.pi * j / nprime) for j in range(nprime)],
                               np.full(nprime, 1.0 / nprime), alpha, q * D)
                worst = max(worst, abs(sol["cost"] / q - ref["cost"]),
                            abs(sol["R"] / q - ref["R"]), abs(sol["L"] / q - ref["L"]))
                cases += 1
    report("blocking", worst < 1e-8, max_err=worst, cases=cases)


def check_phase(rng):
    worst = 0.0
    cases = 0
    for (q, p) in [(2, 1), (3, 2), (4, 1)]:
        src = random_pma(rng, q, p, 1)
        dm = src.dmax()
        for alpha in (0.0, 0.5, 1.0):
            D = 0.4 * dm
            base, _ = stacked_spectral(src, alpha, D, n=48)
            for c in range(1, q):
                v, _ = stacked_spectral(src, alpha, D, n=48, start=c)
                worst = max(worst, abs(v - base))
                cases += 1
    report("phase_shift", worst < 1e-8, max_err=worst, cases=cases)


def check_windows(rng):
    src = random_pma(rng, 3, 1, 1, m=2)
    q = src.q
    dm = src.dmax()
    table = []
    ok = True
    for alpha in (0.0, 0.5, 1.0):
        D = 0.4 * dm
        v, _ = stacked_spectral(src, alpha, D, n=256)
        gaps = []
        for k in (2, 4, 8, 16, 32):
            N = k * q
            gaps.append(window_cost(src, N, alpha, D) - v)
        table.append(dict(alpha=alpha, spectral=v, gaps=gaps, N_times_gap=[g * k * q for g, k in zip(gaps, (2, 4, 8, 16, 32))]))
        ok = ok and all(g > -1e-9 for g in gaps) and all(gaps[i + 1] < gaps[i] for i in range(len(gaps) - 1))
        ok = ok and gaps[-1] < 0.02
    report("window_converse", ok, last_gap=max(t["gaps"][-1] for t in table),
           first_gap=max(t["gaps"][0] for t in table), table=table)

    # N not a multiple of q
    ok = True
    worst = np.inf
    dbar = src.dbar()
    for alpha in (0.0, 0.5, 1.0):
        D = 0.4 * dm
        for N in (4, 5, 7, 10, 13, 20, 31):
            vw = window_cost(src, N, alpha, D)
            vs, _ = stacked_spectral(src, alpha, D + q * dbar / N, n=96)
            worst = min(worst, vw - vs)
            ok = ok and vw >= vs - 1e-9
    report("window_any_N", ok, min_margin=float(worst))


def check_regimes(rng):
    """Independent segments of two stationary sources: the joint window problem
    (block-diagonal covariance) equals the two window problems under one level."""
    worst = 0.0
    cases = 0
    for (N1, N2) in [(4, 6), (5, 5), (3, 9)]:
        sp1 = random_source(rng, 2, 1, 1, htaps=1)
        sp2 = random_source(rng, 2, 1, 1, htaps=1)
        b1 = sc.toeplitz_problem(sp1, N1)
        b2 = sc.toeplitz_problem(sp2, N2)
        N = N1 + N2
        S = block_diag([b1[3], b2[3]])
        R = np.real(sc.psd_sqrt(S))
        Qn = block_diag([np.kron(np.eye(N1), sp1.Q), np.kron(np.eye(N2), sp2.Q)])
        Hn = block_diag([np.kron(np.eye(N1), sp1.Hk[0]), np.kron(np.eye(N2), sp2.Hk[0])])
        SUn = block_diag([np.kron(np.eye(N1), sp1.SU), np.kron(np.eye(N2), sp2.SU)])
        dm = float(np.trace(Qn @ S)) / N
        for alpha in (0.0, 0.5, 1.0):
            D = 0.45 * dm
            joint = sc.solve([(sc.herm(R @ Qn @ R), Hn @ R, SUn)], [1.0 / N], alpha, D)
            split = sc.solve([b1[:3], b2[:3]], [1.0 / N, 1.0 / N], alpha, D)
            worst = max(worst, abs(joint["cost"] - split["cost"]))
            cases += 1
    report("regimes", worst < 1e-8, max_err=worst, cases=cases)


def averaged_cost(src, alpha, D, n):
    """Spectral cost of the stationary source whose spectrum is the time
    average f_0 of the cyclostationary one (time-invariant parties)."""
    q, p, m = src.q, src.p, src.m

    def f0(lam):
        out = np.zeros((p, p), dtype=complex)
        for tau in range(-m, m + 1):
            out = out + sum(src.cov(t + tau, t) for t in range(q)) / q * np.exp(-1j * lam * tau)
        return sc.herm(out)

    blocks = []
    for k in range(n):
        R = sc.psd_sqrt(f0(2 * np.pi * k / n))
        blocks.append((sc.herm(R @ src.Q[0] @ R), src.H[0] @ R, src.SU[0].astype(complex)))
    return sc.solve(blocks, np.full(n, 1.0 / n), alpha, D)["cost"]


def check_averaged(rng):
    """Theorem: with time-invariant parties, the stationary source with the
    time-averaged spectrum costs at least as much, at every weight."""
    worst = np.inf
    cases = 0
    for (q, p, r) in [(2, 1, 1), (3, 1, 1), (2, 2, 1), (4, 1, 1), (3, 2, 2)]:
        src = random_pma(rng, q, p, r, m=2, same_parties=True)
        dm = src.dmax()
        nprime = 32
        for alpha in (0.0, 0.3, 0.7, 1.0):
            for frac in (0.1, 0.4, 0.8):
                D = frac * dm
                v, _ = stacked_spectral(src, alpha, D, n=nprime)
                v0 = averaged_cost(src, alpha, D, nprime * q)
                worst = min(worst, v0 - v)
                cases += 1
    report("averaged_spectrum", worst > -1e-9, min_saving=float(worst), cases=cases)


def report_stationarized(rng):
    """Numbers for the text: one instance of the comparison above."""
    src = random_pma(rng, 2, 1, 1, m=2, same_parties=True)
    q, p, m = src.q, src.p, src.m
    dm = src.dmax()

    def f0(lam):
        out = np.zeros((p, p), dtype=complex)
        for tau in range(-m, m + 1):
            out = out + sum(src.cov(t + tau, t) for t in range(q)) / q * np.exp(-1j * lam * tau)
        return sc.herm(out)

    n = 256
    rows = []
    for alpha in (0.0, 1.0):
        for frac in (0.1, 0.4, 0.8):
            D = frac * dm
            v, _ = stacked_spectral(src, alpha, D, n=n // q)
            blocks = []
            for k in range(n):
                R = sc.psd_sqrt(f0(2 * np.pi * k / n))
                blocks.append((sc.herm(R @ src.Q[0] @ R), src.H[0] @ R, src.SU[0].astype(complex)))
            v0 = sc.solve(blocks, np.full(n, 1.0 / n), alpha, D)["cost"]
            rows.append(dict(alpha=alpha, D_over_Dmax=frac, cyclostationary=v, stationarized=v0, saving=v0 - v))
            print(f"    alpha={alpha} D/Dmax={frac}: cyclostationary {v:.5f}  stationarized {v0:.5f}  saving {v0 - v:+.5f}")
    OUT["stationarized_report"] = dict(ok=True, table=rows)


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    check_harmonic(rng)
    check_blocking(rng)
    check_phase(rng)
    check_windows(rng)
    check_regimes(rng)
    check_averaged(rng)
    report_stationarized(rng)
    OUT["_meta"] = dict(seed=SEED, numpy=np.__version__, failed=FAILED, seconds=round(time.time() - t0, 1))
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(OUT, open(os.path.join(here, "verify_cyclo.json"), "w"), indent=1)
    n_checks = len(OUT) - 2
    print(f"{n_checks - len(FAILED)} passed, {len(FAILED)} failed, {OUT['_meta']['seconds']} s")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
