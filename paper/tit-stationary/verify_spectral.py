"""Numerical checks for "Rate, Leakage, and Distortion for Stationary Gaussian Sources".

Run:  python verify_spectral.py            (prints a report, writes verify_spectral.json)
Deterministic: every random instance comes from numpy.random.default_rng(SEED).
Each check is labelled with the statement of the paper it supports.  No proof
depends on these numbers.
"""
import json
import sys
import time

import numpy as np

import spectral_core as sc

SEED = 20261113
OUT = {}
FAIL = []


T0 = time.time()


def report(name, ok, **kv):
    kv['seconds'] = round(time.time() - T0, 1)
    OUT[name] = dict(ok=bool(ok), **{k: (float(v) if isinstance(v, (int, float, np.floating, np.integer)) and not isinstance(v, bool) else v) for k, v in kv.items()})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: " + ", ".join(f"{k}={v:.3e}" if isinstance(v, float) else f"{k}={v}"
                                                                  for k, v in kv.items()))
    if not ok:
        FAIL.append(name)


def random_source(rng, p, m, r, taps=3, htaps=2):
    G = [rng.standard_normal((p, p)) * (0.7 ** k) for k in range(taps)]
    B = 0.3 * np.eye(p)
    F = rng.standard_normal((m, p))
    W = np.eye(m)
    Hk = [rng.standard_normal((r, p)) * (0.6 ** k) for k in range(htaps)]
    A = rng.standard_normal((r, r))
    SU = A @ A.T / r + 0.5 * np.eye(r)
    return sc.Spectrum(G, B, Hk, SU, F.T @ W @ F)


def dmax(sp, n=2048):
    return float(np.mean([np.real(np.trace(sp.Q @ sp.Sigma(2 * np.pi * k / n))) for k in range(n)]))


# ------------------------------------------------------------------ Theorem 1
def check_decoupling(rng):
    """Theorem 1: the n-periodic problem, solved as one real pn-dimensional
    program with no structure assumed, equals the per-frequency Hermitian
    programs with one common level."""
    worst = dict(cost=0.0, X=0.0, kkt=0.0, offdiag=0.0, nu=0.0, herm=0.0)
    cases = 0
    for (p, m, r, n) in [(2, 1, 1, 6), (2, 1, 1, 9), (3, 2, 1, 8), (3, 2, 2, 7), (2, 2, 2, 10), (4, 2, 3, 6)]:
        sp = random_source(rng, p, m, r)
        Qt, Ht, SUn, _ = sc.circulant_problem(sp, n)
        dm = float(np.trace(Qt)) / n
        for alpha in (0.0, 0.3, 0.7, 1.0):
            for frac in (0.25, 0.6):
                D = frac * dm
                full = sc.solve([(Qt, Ht, SUn)], [1.0 / n], alpha, D)
                spec = sc.spectral_solve(sp, n, alpha, D)
                Xa = sc.assemble_circulant(sp, n, spec["X"])
                worst["herm"] = max(worst["herm"], float(np.abs(Xa.imag).max()))
                Xa = Xa.real
                worst["cost"] = max(worst["cost"], abs(full["cost"] - spec["cost"]))
                worst["X"] = max(worst["X"], float(np.linalg.norm(full["X"][0] - Xa)))
                worst["nu"] = max(worst["nu"], abs(full["nu"] - spec["nu"]) / max(spec["nu"], 1e-12))
                # optimality of the assembled spectral solution in the FULL space [1, Thm. 7]
                A = 2 * spec["nu"] * Qt + sc.tilt(Xa, Ht, SUn, alpha)
                worst["kkt"] = max(worst["kkt"], float(np.linalg.norm(sc.Phi(A) - Xa)))
                # block-diagonality of the unstructured solution in the DFT basis
                w = 2 * np.pi * np.arange(n) / n
                U = np.kron(np.exp(1j * np.outer(np.arange(n), w)) / np.sqrt(n), np.eye(p))
                Xf = U.conj().T @ full["X"][0] @ U
                mask = np.kron(np.eye(n), np.ones((p, p))) == 0
                worst["offdiag"] = max(worst["offdiag"], float(np.abs(Xf[mask]).max()))
                cases += 1
    ok = worst["cost"] < 1e-9 and worst["X"] < 1e-6 and worst["kkt"] < 1e-8 and worst["offdiag"] < 1e-6
    report("thm1_decoupling", ok, cases=cases, **worst)


# ------------------------------------------------------------------ Theorem 2
def check_limit(rng):
    """Theorem 2: the n-periodic values converge to the spectral integral
    (reference: n = 2048 grid) and the common level converges."""
    sp = random_source(rng, 2, 1, 1)
    D = 0.4 * dmax(sp)
    rows = []
    ok = True
    for alpha in (0.0, 0.5, 1.0):
        ref = sc.spectral_solve(sp, 2048, alpha, D, half=True)
        prev = None
        for n in (8, 16, 32, 64, 128, 256, 512):
            s = sc.spectral_solve(sp, n, alpha, D, half=True)
            err = abs(s["cost"] - ref["cost"])
            rows.append(dict(alpha=alpha, n=n, cost=s["cost"], err=err, nu=s["nu"], nu_ref=ref["nu"]))
            prev = err
        ok = ok and prev < 1e-6
    report("thm2_limit", ok, last_err=float(max(r["err"] for r in rows if r["n"] == 512)), table=rows)


# ------------------------------------------------------------------ anchors
def check_kolmogorov(rng):
    """alpha = 1, scalar described process: the spectral program is
    Kolmogorov's reverse water-filling of S_Y."""
    sp = random_source(rng, 2, 1, 1)
    n = 2048
    w = 2 * np.pi * np.arange(n) / n
    f = sp.Q[0, 0]  # not used: Q = F^T F is rank one; S_Y(w) = F Sigma F^T up to the weight
    SY = np.array([np.real(np.trace(sp.Q @ sp.Sigma(x))) for x in w])
    D = 0.35 * SY.mean()
    lo, hi = 0.0, SY.max()
    for _ in range(200):
        th = 0.5 * (lo + hi)
        if np.minimum(th, SY).mean() > D:
            hi = th
        else:
            lo = th
    Rk = np.mean(np.maximum(0.0, 0.5 * np.log2(SY / th)))
    s = sc.spectral_solve(sp, n, 1.0, D, half=True)
    report("anchor_kolmogorov", abs(s["R"] - Rk) < 1e-9, R_spectral=s["R"], R_waterfill=float(Rk),
           diff=abs(s["R"] - Rk))


def pair_source(rho, a, tau2, n_taps=40):
    """Scalar pair: V an AR(1) process with pole a and unit variance (truncated
    moving-average form), Y_t = rho V_t + N_t with N white, Var Y = 1;
    holder S_t = V_t + U_t, Var U = tau2.  T = (Y, V)."""
    c = np.sqrt(1 - a * a)
    G = [np.array([[0.0, rho * c * a ** k], [0.0, c * a ** k]]) for k in range(n_taps)]
    B = np.array([[1 - rho ** 2, 0.0], [0.0, 1e-12]])
    return sc.Spectrum(G, B, [np.array([[0.0, 1.0]])], np.array([[tau2]]), np.diag([1.0, 0.0]))


def general_pair(rng):
    """Scalar pair with a frequency-dependent complex cross-spectrum."""
    G = [rng.standard_normal((2, 2)) * (0.6 ** k) for k in range(4)]
    return sc.Spectrum(G, 0.2 * np.eye(2), [np.array([[0.0, 1.0]])], np.array([[0.7]]), np.diag([1.0, 0.0]))


def check_scalar_closed_form(rng):
    """Theorem 3: for a scalar pair, per frequency the minimum leakage at
    distortion d is (1/2) log g*(kappa, s, d / S_Y), the slope is that of
    [1, Lemma 26], and a band is described iff the level exceeds
    tau2 / (2 ln2 S_Y (kappa S_V... )) in the form stated in the paper."""
    worst = dict(val=0.0, alloc=0.0, thr=0.0)
    for sp in (general_pair(rng), pair_source(0.8, 0.7, 0.5)):
        n = 256
        w = 2 * np.pi * np.arange(n) / n
        Sg = [sp.Sigma(x) for x in w]
        SY = np.array([S[0, 0].real for S in Sg])
        SV = np.array([S[1, 1].real for S in Sg])
        kap = np.array([abs(S[0, 1]) ** 2 for S in Sg]) / (SY * SV)
        tau2 = float(sp.SU[0, 0])
        s_w = 1 + tau2 / SV
        D = 0.45 * SY.mean()
        num = sc.spectral_solve(sp, n, 0.0, D)
        # value per frequency at the numerically optimal distortion
        val = sc.ell_scalar(kap, s_w, num["Db"] / SY)
        worst["val"] = max(worst["val"], float(np.abs(val - num["Lb"]).max()))
        # allocation from the closed-form slope: equalise -dL/dD = theta
        thr = tau2 / (2 * sc.LOG2 * SY * (kap * SV + tau2))          # activation level per band

        def alloc(theta):
            d = SY.copy()
            for k in range(n):
                if theta > thr[k]:
                    lo, hi = 1e-14, 1 - 1e-14
                    for _ in range(200):
                        mid = 0.5 * (lo + hi)
                        if -sc.ell_slope(kap[k], s_w[k], mid) / SY[k] > theta:
                            lo = mid
                        else:
                            hi = mid
                    d[k] = SY[k] * 0.5 * (lo + hi)
            return d

        lo, hi = 0.0, 1e6
        for _ in range(200):
            th = 0.5 * (lo + hi)
            if alloc(th).mean() > D:
                lo = th
            else:
                hi = th
        d_cf = alloc(th)
        worst["alloc"] = max(worst["alloc"], float(np.abs(d_cf - num["Db"]).max()))
        active_num = num["Db"] < SY * (1 - 1e-7)
        active_cf = th > thr
        worst["thr"] = max(worst["thr"], float(np.sum(active_num != active_cf)))
    ok = worst["val"] < 1e-8 and worst["alloc"] < 1e-6 and worst["thr"] == 0
    report("thm3_scalar_closed_form", ok, **worst)


def check_disjoint_bands():
    """Corollary: the rate-optimal and leakage-optimal descriptions of one
    scalar pair process can occupy disjoint frequency bands."""
    # two-band spectrum: band 1 (low w) strong Y, context nearly useless to the holder;
    # band 2 (high w) weaker Y, context coherent.  Built as a moving average pair.
    n = 512
    w = 2 * np.pi * np.arange(n) / n
    low = np.cos(w / 2) ** 2
    high = 1 - low
    # T = (Y, V): independent "low" and "high" components added
    SY = 1.6 * low + 1.0 * high
    SV = np.ones(n)
    kap = 0.02 * low + 0.90 * high
    tau2 = 0.25
    blocks = []
    for k in range(n):
        c = np.sqrt(kap[k] * SY[k] * SV[k])
        S = np.array([[SY[k], c], [c, SV[k]]], dtype=complex)
        Rt = sc.psd_sqrt(S)
        blocks.append((sc.herm(Rt @ np.diag([1.0, 0.0]) @ Rt), np.array([[0.0, 1.0]], dtype=complex) @ Rt,
                       np.array([[tau2]], dtype=complex)))
    D = 0.97 * SY.mean()
    wts = np.full(n, 1.0 / n)
    rt = sc.solve(blocks, wts, 1.0, D)
    lk = sc.solve(blocks, wts, 0.0, D)
    act_r = rt["Db"] < SY * (1 - 1e-7)
    act_l = lk["Db"] < SY * (1 - 1e-7)
    overlap = int(np.sum(act_r & act_l))
    report("cor_disjoint_bands", overlap == 0 and act_r.sum() > 0 and act_l.sum() > 0,
           bands_rate=int(act_r.sum()), bands_leak=int(act_l.sum()), overlap=overlap,
           L_of_rate_opt=rt["L"], L_min=lk["L"], R_of_leak_opt=lk["R"], R_min=rt["R"])
    return dict(w=w.tolist(), SY=SY.tolist(), kap=kap.tolist(), Dr=rt["Db"].tolist(), Dl=lk["Db"].tolist(),
                tau2=tau2, D=D)


# ------------------------------------------------------------------ delay
def check_delay(rng):
    """Proposition (all-pass invariance): delaying the holder's observation by
    Delta symbols leaves the n-periodic region unchanged.  Solved in the full
    real space, where the delay is a cyclic shift and nothing is assumed."""
    sp = random_source(rng, 2, 1, 1)
    n = 8
    worst = 0.0
    base = None
    for delay in range(0, 5):
        Qt, Ht, SUn, _ = sc.circulant_problem(sp, n, delay=delay)
        D = 0.4 * float(np.trace(Qt)) / n
        vals = [sc.solve([(Qt, Ht, SUn)], [1.0 / n], al, D) for al in (0.0, 0.5)]
        v = np.array([[x["R"], x["L"]] for x in vals])
        if base is None:
            base = v
        worst = max(worst, float(np.abs(v - base).max()))
    report("prop_delay_invariance", worst < 1e-9, max_change_bits=worst, delays="0..4", n=n)


# ------------------------------------------------------------------ Toeplitz
def check_affine_toeplitz(rng):
    """Theorem 4: when Sigma(w) = B + f(w) A the window (Toeplitz) problem
    decouples exactly in the eigenbasis of T_n(f), at every n, and its value
    converges to the spectral value."""
    rho, a, tau2 = 0.8, 0.7, 0.5
    sp = pair_source(rho, a, tau2, n_taps=80)
    A = np.array([[rho ** 2, rho], [rho, 1.0]])
    B = np.array([[1 - rho ** 2, 0.0], [0.0, 1e-12]])
    Q = np.diag([1.0, 0.0])
    Hrow = np.array([[0.0, 1.0]])
    SU = np.array([[tau2]])
    D = 0.5
    ref = {al: sc.spectral_solve(sp, 2048, al, D, half=True) for al in (0.0, 0.5)}
    rows = []
    worst_dec = 0.0
    for n in (4, 8, 16, 32, 64):
        C = np.array([[a ** abs(i - j) for j in range(n)] for i in range(n)])   # T_n(f_V), exact
        lam = np.linalg.eigvalsh(C)
        blocks = []
        for l in lam:
            S = l * A + B
            Rt = np.real(sc.psd_sqrt(S))
            blocks.append((sc.herm(Rt @ Q @ Rt), Hrow @ Rt, SU))
        for al in (0.0, 0.5):
            eig = sc.solve(blocks, np.full(n, 1.0 / n), al, D)
            row = dict(n=n, alpha=al, cost_eig=eig["cost"], gap=eig["cost"] - ref[al]["cost"],
                       n_gap=n * (eig["cost"] - ref[al]["cost"]))
            if n <= 32:
                Sig = np.kron(C, A) + np.kron(np.eye(n), B)
                Rt = np.real(sc.psd_sqrt(Sig))
                full = sc.solve([(sc.herm(Rt @ np.kron(np.eye(n), Q) @ Rt), np.kron(np.eye(n), Hrow) @ Rt,
                                  np.kron(np.eye(n), SU))], [1.0 / n], al, D)
                row["cost_full"] = full["cost"]
                worst_dec = max(worst_dec, abs(full["cost"] - eig["cost"]))
            rows.append(row)
    last = [r for r in rows if r["n"] == 64]
    ok = worst_dec < 1e-9 and all(abs(r["gap"]) < 2e-2 for r in last)
    report("thm4_affine_toeplitz", ok, decoupling_err=worst_dec,
           gap_n64=float(max(abs(r["gap"]) for r in last)), table=rows)


def check_general_toeplitz(rng):
    """Conjecture 1 (evidence only): for a general spectrum the window value
    approaches the spectral value; n * gap is recorded."""
    sp = random_source(rng, 2, 1, 1, taps=3, htaps=1)
    D = 0.4 * dmax(sp)
    rows = []
    for al in (0.0, 0.5, 1.0):
        ref = sc.spectral_solve(sp, 2048, al, D, half=True)["cost"]
        for n in (4, 8, 16, 32, 48):
            Qt, Ht, SUn, _ = sc.toeplitz_problem(sp, n)
            v = sc.solve([(Qt, Ht, SUn)], [1.0 / n], al, D)["cost"]
            rows.append(dict(alpha=al, n=n, cost=v, gap=v - ref, n_gap=n * (v - ref)))
    g48 = max(abs(r["gap"]) for r in rows if r["n"] == 48)
    g8 = max(abs(r["gap"]) for r in rows if r["n"] == 8)
    report("conj1_general_toeplitz_evidence", g48 < g8, gap_n8=float(g8), gap_n48=float(g48), table=rows)


# ------------------------------------------------------------------ retention
def check_retention():
    """Proposition (what the holder retains): for the pair source and a
    description of one epoch, the leakage depends on the retained observations
    only through q = Var(V_t | retained), and the fixed-lag gap is geometric."""
    rho, a, tau2 = 0.8, 0.7, 0.5
    Dn = 0.4
    N = 160                      # long window standing in for the infinite path (a^80 ~ 4e-13)
    t = N // 2
    C = np.array([[a ** abs(i - j) for j in range(N)] for i in range(N)])

    def q_of(idx):
        idx = np.asarray(idx)
        K = C[np.ix_(idx, idx)] + tau2 * np.eye(len(idx))
        c = C[t, idx]
        return float(1 - c @ np.linalg.solve(K, c))

    def leak_direct(idx):
        # the one-epoch problem with the holder observing S_idx, by the general solver
        idx = np.asarray(idx)
        Sig = np.array([[1.0, rho], [rho, 1.0]])
        Hm = np.outer(C[idx, t], [0.0, 1.0])                    # E[V_s | T_t] = a^{|s-t|} V_t
        SU = C[np.ix_(idx, idx)] - np.outer(C[idx, t], C[idx, t]) + tau2 * np.eye(len(idx))
        Rt = np.real(sc.psd_sqrt(Sig))
        return sc.solve([(sc.herm(Rt @ np.diag([1.0, 0.0]) @ Rt), Hm @ Rt, SU)], [1.0], 0.0, Dn)["L"]

    worst = 0.0
    qs = {}
    for name, idx in [("slice_lag3", [t - 3]), ("prefix_lag0", list(range(0, t + 1))),
                      ("prefix_lag3", list(range(0, t + 4))), ("path", list(range(N)))]:
        q = q_of(idx)
        qs[name] = q
        worst = max(worst, abs(leak_direct(idx) - float(sc.ell_scalar(rho ** 2, 1 / (1 - q), Dn))))
    # closed forms
    q_slice = 1 - a ** 6 / (1 + tau2)
    # Riccati: filtering variance P_f, prediction P_p = a^2 P_f + 1 - a^2
    Pp = 1.0
    for _ in range(10000):
        Pf = Pp * tau2 / (Pp + tau2)
        Pp = a * a * Pf + 1 - a * a
    Cg = a * Pf / Pp
    # noncausal Wiener error: integral of S_V tau2 / (S_V + tau2)
    w = 2 * np.pi * (np.arange(200000) + 0.5) / 200000
    SV = (1 - a * a) / (1 - 2 * a * np.cos(w) + a * a)
    q_path = float(np.mean(SV * tau2 / (SV + tau2)))
    gaps = []
    for lag in (0, 1, 2, 3, 5):
        q_pre = q_of(list(range(0, t + lag + 1)))
        gaps.append(abs((q_pre - q_path) - Cg ** (2 * lag) * (Pf - q_path)))
    ok = (worst < 1e-9 and abs(qs["slice_lag3"] - q_slice) < 1e-12 and abs(qs["prefix_lag0"] - Pf) < 1e-9
          and abs(qs["path"] - q_path) < 1e-8 and max(gaps) < 1e-9
          and qs["slice_lag3"] > qs["prefix_lag3"] > qs["path"])
    report("prop_retention", ok, leak_vs_closed_form=worst, q_slice=qs["slice_lag3"], q_prefix0=qs["prefix_lag0"],
           q_prefix3=qs["prefix_lag3"], q_path=qs["path"], P_f=float(Pf), C=float(Cg), geometric_gap_err=float(max(gaps)))


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    check_decoupling(rng)
    check_limit(rng)
    check_kolmogorov(rng)
    check_scalar_closed_form(rng)
    fig = check_disjoint_bands()
    check_delay(rng)
    check_affine_toeplitz(rng)
    check_general_toeplitz(rng)
    check_retention()
    OUT["_figure_disjoint"] = fig
    OUT["_meta"] = dict(seed=SEED, numpy=np.__version__, seconds=round(time.time() - t0, 1),
                        failed=FAIL)
    with open("verify_spectral.json", "w") as f:
        json.dump(OUT, f, indent=1)
    print(f"\n{len(OUT) - 2 - len(FAIL)} passed, {len(FAIL)} failed, {time.time() - t0:.1f} s")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
