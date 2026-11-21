#!/usr/bin/env python
"""C3 net for the rate identity of Paper III's Lemma `lem:maxdet` (paper/observation-theory.tex).

Target. For X ~ N(0, Sx), Sx > 0, P >= 0 and the weighted squared error
d(x, xh) = (x - xh)^T P (x - xh),

    R_P(D) = min { I(X; Xh) : E d(X, Xh) <= D } = 1/2 logdet Sx - 1/2 logdet Sigma*(P, D)
           = 1/2 sum_{pt_k > theta} log(pt_k / theta)   (nats),

where pt_k are the eigenvalues of Sx^{1/2} P Sx^{1/2} and sum_k min(pt_k, theta) = D. The proof
in the paper has a converse (Lemma `lem:cm`, then Lemma `lem:info`, whose step
h(X | Xh) <= 1/2 logdet(2 pi e Sigma(Xh)) is Gaussian maximum entropy, then the max-det
program) and an achievability half (the Gaussian backward channel). The max-det program and its
closed form are netted separately (verify_paper3_nets.py, m1-m4). This file nets what those do
not: that no test channel beats the formula, including non-Gaussian channels, for which
`lem:info` is a strict inequality; and that the backward channel realizes the source at the
stated distortion. It is a net, not a proof (CHARTER T-CUST-2). Written 2026-11-21, after VI-46
found that row PAPER-III.b (the dispersion formula) rests on this identity and nothing netted it.

Channel families. Every quantity below is computed from the joint law, independently of the
formula under test.
- Product quantizers. W = Sx^{-1/2} X ~ N(0, I). Pick an orthogonal U, set V = U^T W (i.i.d.
  N(0,1) coordinates) and quantize each coordinate with its own thresholds; the channel output is
  the cell's centroid. I(X; Xh) = H(cell) exactly (distinct cells have distinct centroids), and
  Sigma(Xh) = Sx^{1/2} U diag(mse_k) U^T Sx^{1/2} exactly, from closed-form truncated-normal
  moments. Half of them use a random U, half the eigenbasis of Sx^{1/2} P Sx^{1/2}. For these,
  `lem:info` reduces to the scalar Gaussian bound coordinate by coordinate.
- Skew-rectangle quantizers (d = 2). Y = M W with M invertible and not orthogonal, cells are
  rectangles in Y, so the coordinates are correlated and the cells are parallelograms in W:
  `lem:info` is tested as a genuinely two-dimensional inequality. Cell probabilities and first
  and second moments are one-dimensional quadratures of closed-form inner truncated moments,
  checked by guards (the cell probabilities and moments must sum to 1, 0 and Cov Y).
- Gaussian channels. Sigma(Xh) = (Sx^{-1} + Lam)^{-1} for PSD Lam: random ones, and near-optimal
  ones Lam = Lam* + eps E around the optimum Lam* = Sigma*^{-1} - Sx^{-1}. For these `lem:info`
  holds with equality, so they test the formula's water-filling part, at high resolution.

Checks (seed 20261128; every criterion below was written before this file first ran):
  r1_lemma_info   every quantizer channel has slack H(cell) - 1/2 log det Sx / det Sigma(Xh)
                  >= -1e-9 (product) or >= -1e-7 (skew, quadrature); the skew quadrature guards
                  hold (|sum p - 1| <= 1e-9, |sum E[Y; c]| <= 1e-8, |sum E[YY^T; c] - Cov Y|
                  <= 1e-8); the skew cells' centroids are pairwise >= 1e-9 apart (product cells'
                  centroids are distinct by construction).
  r2_converse     every channel (all three families) has I(X; Xh) - R_P(E d) >= -1e-9 max(1, R)
                  (product, Gaussian) or >= -1e-7 (skew).
  r3_attained     at the optimum Lam*, I - R_P(D) is within 1e-9 of 0, and the eigenvalue form
                  of R_P equals 1/2 logdet Sx - 1/2 logdet Sigma* to 1e-9; every near-optimal
                  channel has gap >= -1e-9, and those with eps = 1e-3 have gap <= 1e-3.
  r4_backward     the backward channel exists (min eig(Sx - Sigma*) >= -1e-10 ||Sx||) and meets
                  the budget (|tr(P Sigma*) - D| <= 1e-9 D); on 10 instances a Monte Carlo
                  realization (Xh ~ N(0, Sx - Sigma*), Z ~ N(0, Sigma*), X = Xh + Z, 200000
                  samples) has mean distortion within 5 standard errors of D and every entry of
                  the sample covariance of X within 5 standard errors of Sx. This is a
                  consistency check of the construction; it can fail only if the construction
                  or Sigma* is wrong.
  r5_power        known-wrong versions must be caught by some channel:
                  (a) the formula raised by 1e-2 nats (counts also recorded at 1e-3 and 1e-1,
                      per family);
                  (b) `lem:info` raised by 0.05 nats, caught by a product quantizer (counts
                      recorded at 0.01 and 0.05 per quantizer family);
                  (c) the formula evaluated in P's own eigenbasis with Sx replaced by its
                      diagonal there (the "commuting" shortcut), on some instance;
                  (d) VI-4's bug, Sigma = (Sx^{-1} + lam P)^{-1} with tr(P Sigma) = D, on some
                      instance;
                  (e) the formula in bits instead of nats.
Verdict: all five pass. The run records the harness sha256 (of the file with line endings
normalized to LF), the git commit and whether this file was modified, the start time, and the
versions of Python, numpy and scipy.

Before this file was committed, its helper functions were smoke-tested on hand-made inputs only
(the scalar moments against direct numerical integration; the skew quadrature with M = I against
the product closed form). No instance at the seed was evaluated before the commit.

History.
- Attempt 1 (commit 3073453, 2026-11-21) crashed after 2 s, while building the product channels
  and before any check was computed or any output written: `scalar_quantizer` raised "empty
  cell". A dead-zone quantizer with a threshold near +-12 has an upper-tail cell whose
  probability Phi(inf) - Phi(12) cancels to 0 in double precision (the true value is about
  1e-33). The fix (`tail_stable_diff`) computes upper-tail differences as Phi(-a) - Phi(-b). The
  criteria, the seed and the instance generator are unchanged; the fix was committed before
  attempt 2.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys

import numpy as np
import scipy
from scipy import integrate
from scipy.special import ndtr

SEED = 20261128
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "PAPER3-rate-identity.json")
LN2 = float(np.log(2.0))


# ---------------------------------------------------------------- linear algebra
def sym(A):
    return 0.5 * (A + A.T)


def sqrtm_psd(S):
    w, V = np.linalg.eigh(sym(S))
    return sym((V * np.sqrt(np.clip(w, 0.0, None))) @ V.T)


def logdet(S):
    sign, ld = np.linalg.slogdet(sym(S))
    if sign <= 0:
        raise ValueError("matrix not positive definite")
    return float(ld)


def haar(rng, d):
    Q, R = np.linalg.qr(rng.standard_normal((d, d)))
    return Q * np.sign(np.diag(R))


def rand_spd(rng, d):
    A = rng.standard_normal((d, d))
    return sym(A @ A.T / d + 0.2 * np.eye(d))


def rand_psd_rank(rng, d, k):
    B = rng.standard_normal((d, k))
    return sym(B @ B.T)


# ---------------------------------------------------------------- the formula under test
def whitened_eigs(P, Sx):
    Sh = sqrtm_psd(Sx)
    pt, V = np.linalg.eigh(sym(Sh @ P @ Sh))
    return np.clip(pt, 0.0, None), V, Sh


def water_level(pt, D):
    """theta with sum_k min(pt_k, theta) = D, for 0 < D < sum pt."""
    lo, hi = 0.0, float(pt.max())
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if float(np.minimum(pt, mid).sum()) < D:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def rate_from_eigs(pt, D):
    if D >= float(pt.sum()):
        return 0.0
    th = water_level(pt, D)
    act = pt > th
    return 0.5 * float(np.sum(np.log(pt[act] / th)))


def rate_formula(P, D, Sx):
    """R_P(D) in nats, by the eigenvalue form of the closed form."""
    pt, _, _ = whitened_eigs(P, Sx)
    return rate_from_eigs(pt, D)


def sigma_star(P, D, Sx):
    """The closed form of lem:maxdet with cap Sx."""
    pt, V, Sh = whitened_eigs(P, Sx)
    if D >= float(pt.sum()):
        return sym(Sx.copy())
    th = water_level(pt, D)
    w = np.where(pt > th, th / np.where(pt > 0, pt, 1.0), 1.0)
    return sym(Sh @ (V * w) @ V.T @ Sh)


# wrong versions (r5)
def rate_commuting_shortcut(P, D, Sx):
    p, Q = np.linalg.eigh(sym(P))
    s2 = np.diag(Q.T @ Sx @ Q)
    return rate_from_eigs(np.clip(p, 0.0, None) * s2, D)


def rate_vi4_bug(P, D, Sx):
    Sxi = np.linalg.inv(Sx)
    if D >= float(np.trace(P @ Sx)):
        return 0.0
    lo, hi = 0.0, 1.0
    while float(np.trace(P @ np.linalg.inv(Sxi + hi * P))) > D:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if float(np.trace(P @ np.linalg.inv(Sxi + mid * P))) > D:
            lo = mid
        else:
            hi = mid
    S = np.linalg.inv(Sxi + 0.5 * (lo + hi) * P)
    return 0.5 * (logdet(Sx) - logdet(S))


# ---------------------------------------------------------------- scalar truncated-normal moments
def _phi(x):
    return np.exp(-0.5 * x * x) / np.sqrt(2.0 * np.pi)


def tail_stable_diff(a, b):
    """Phi(b) - Phi(a) for a < b, computed as Phi(-a) - Phi(-b) when a >= 0, so that a cell far in
    the upper tail keeps its (tiny, positive) probability instead of cancelling to 0 (attempt 1)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    return np.where(a >= 0, ndtr(-a) - ndtr(-b), ndtr(b) - ndtr(a))


def scalar_cells(th):
    """Thresholds of a scalar quantizer of N(0,1) -> per-cell (p, E[Z; c], E[Z^2; c])."""
    e = np.concatenate([[-np.inf], np.sort(np.asarray(th, float)), [np.inf]])
    a, b = e[:-1], e[1:]
    fa = np.where(np.isfinite(a), _phi(np.where(np.isfinite(a), a, 0.0)), 0.0)
    fb = np.where(np.isfinite(b), _phi(np.where(np.isfinite(b), b, 0.0)), 0.0)
    af, bf = np.where(np.isfinite(a), a, 0.0), np.where(np.isfinite(b), b, 0.0)
    p = tail_stable_diff(a, b)
    m1 = fa - fb
    m2 = p + af * fa - bf * fb
    return p, m1, m2


def scalar_quantizer(th):
    """-> (entropy in nats, mse with centroid reconstruction, centroids)."""
    p, m1, m2 = scalar_cells(th)
    if np.any(p <= 0):
        raise ValueError("empty cell")
    H = float(-np.sum(p * np.log(p)))
    mse = float(np.sum(m2 - m1 * m1 / p))
    return H, mse, m1 / p


# ---------------------------------------------------------------- skew-rectangle cells (d = 2)
def skew_cell_moments(G, a1, b1, a2, b2):
    """For Y ~ N(0, G) in R^2 and the cell (a1,b1) x (a2,b2): (p, E[Y; c], E[Y Y^T; c])."""
    g11, g12, g22 = G[0, 0], G[0, 1], G[1, 1]
    beta = g12 / g11
    s = np.sqrt(g22 - g12 * g12 / g11)
    sd1 = np.sqrt(g11)

    def inner(y1):
        mu = beta * y1
        ua = (a2 - mu) / s if np.isfinite(a2) else -np.inf
        ub = (b2 - mu) / s if np.isfinite(b2) else np.inf
        q0 = float(tail_stable_diff(ua, ub))
        fa = _phi(ua) if np.isfinite(ua) else 0.0
        fb = _phi(ub) if np.isfinite(ub) else 0.0
        ta = ua * fa if np.isfinite(ua) else 0.0
        tb = ub * fb if np.isfinite(ub) else 0.0
        e1 = mu * q0 + s * (fa - fb)
        e2 = mu * mu * q0 + 2.0 * mu * s * (fa - fb) + s * s * (q0 + ta - tb)
        return q0, e1, e2

    def dens(y1):
        return np.exp(-0.5 * y1 * y1 / g11) / (np.sqrt(2.0 * np.pi) * sd1)

    def quad(f):
        v, _ = integrate.quad(f, a1, b1, epsabs=1e-14, epsrel=1e-12, limit=400)
        return v

    p = quad(lambda y: dens(y) * inner(y)[0])
    m1 = quad(lambda y: dens(y) * y * inner(y)[0])
    m2 = quad(lambda y: dens(y) * inner(y)[1])
    s11 = quad(lambda y: dens(y) * y * y * inner(y)[0])
    s12 = quad(lambda y: dens(y) * y * inner(y)[1])
    s22 = quad(lambda y: dens(y) * inner(y)[2])
    return p, np.array([m1, m2]), np.array([[s11, s12], [s12, s22]])


def skew_channel(M, t1, t2):
    """Cells = rectangles in Y = M W, W ~ N(0, I_2). -> (H, Sigma_W(cell), guards, centroid gap)."""
    G = sym(M @ M.T)
    e1 = np.concatenate([[-np.inf], np.sort(t1), [np.inf]])
    e2 = np.concatenate([[-np.inf], np.sort(t2), [np.inf]])
    ps, means, SY = [], [], np.zeros((2, 2))
    sum_m, sum_s = np.zeros(2), np.zeros((2, 2))
    for i in range(len(e1) - 1):
        for j in range(len(e2) - 1):
            p, m, S = skew_cell_moments(G, e1[i], e1[i + 1], e2[j], e2[j + 1])
            if p <= 1e-300:
                raise ValueError("empty skew cell")
            ps.append(p)
            means.append(m / p)
            SY += S - np.outer(m, m) / p
            sum_m += m
            sum_s += S
    ps = np.array(ps)
    H = float(-np.sum(ps * np.log(ps)))
    Mi = np.linalg.inv(M)
    SW = sym(Mi @ SY @ Mi.T)
    cents = np.array(means)
    gaps = [np.linalg.norm(cents[u] - cents[v]) for u in range(len(cents)) for v in range(u + 1, len(cents))]
    guards = {
        "p_sum": abs(float(ps.sum()) - 1.0),
        "mean_sum": float(np.abs(sum_m).max()),
        "second_sum": float(np.abs(sum_s - G).max()),
    }
    return H, SW, guards, (min(gaps) if gaps else float("inf"))


# ---------------------------------------------------------------- random quantizer thresholds
def random_thresholds(rng):
    kind = rng.integers(0, 4)
    if kind == 0:                      # no thresholds: one cell
        return np.array([])
    if kind == 1:                      # random thresholds
        k = int(rng.integers(1, 6))
        return np.sort(rng.normal(0.0, 1.5, size=k))
    t = float(rng.uniform(0.3, 3.0))   # dead zone, uniform steps outside it
    step = float(rng.uniform(0.3, 3.0))
    L = int(rng.integers(1, 5))
    right = t + step * np.arange(L)
    return np.concatenate([-right[::-1], right])


# ---------------------------------------------------------------- environment and custody
def harness_sha256():
    raw = open(os.path.abspath(__file__), "rb").read().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def git_info():
    def run(*args):
        try:
            r = subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True, timeout=30)
            return r.stdout.strip() if r.returncode == 0 else None
        except Exception:
            return None
    commit = run("rev-parse", "HEAD")
    dirty = run("status", "--porcelain", "--", os.path.basename(__file__))
    return {"commit": commit, "harness_modified": None if dirty is None else bool(dirty)}


# ---------------------------------------------------------------- main
def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    rng = np.random.default_rng(SEED)
    out = {"seed": SEED, "started_utc": started, "harness_sha256": harness_sha256(),
           "git": git_info(),
           "environment": {"python": platform.python_version(), "numpy": np.__version__,
                           "scipy": scipy.__version__, "system": platform.system(),
                           "machine": platform.machine()},
           "targets": "Paper III lem:maxdet rate identity: R_P(D) = 1/2 logdet Sx - 1/2 logdet Sigma*(P,D)"}

    # base instances
    base = []
    for _ in range(120):
        d = int(rng.integers(2, 5))
        k = int(rng.integers(1, d + 1))
        Sx, P = rand_spd(rng, d), rand_psd_rank(rng, d, k)
        D = float(rng.uniform(0.05, 0.95) * np.trace(P @ Sx))
        base.append((Sx, P, D))

    channels = []  # (family, instance index, I, Ed, slack or None)

    # product quantizers, random U and aligned U
    prod_slacks = []
    for idx, (Sx, P, _) in enumerate(base):
        d = Sx.shape[0]
        pt, V, Sh = whitened_eigs(P, Sx)
        for fam, U in (("product_random", haar(rng, d)), ("product_aligned", V)):
            H, mses = 0.0, []
            for _ in range(d):
                h, m, _ = scalar_quantizer(random_thresholds(rng))
                H += h
                mses.append(m)
            SW = sym(U @ np.diag(mses) @ U.T)
            Sig = sym(Sh @ SW @ Sh)
            Ed = float(np.trace(P @ Sig))
            slack = H + 0.5 * logdet(SW)          # H - 1/2 log det Sx / det Sigma(Xh)
            channels.append((fam, idx, H, Ed, slack))
            prod_slacks.append(slack)

    # skew-rectangle quantizers (d = 2, own instances)
    skew_guard_worst = {"p_sum": 0.0, "mean_sum": 0.0, "second_sum": 0.0}
    skew_min_centroid_gap = float("inf")
    skew_inst = []
    for _ in range(40):
        Sx, P = rand_spd(rng, 2), rand_psd_rank(rng, 2, int(rng.integers(1, 3)))
        while True:
            M = rng.standard_normal((2, 2))
            G = M @ M.T
            if np.linalg.cond(M) <= 10.0 and abs(float(G[0, 1])) / np.sqrt(G[0, 0] * G[1, 1]) > 0.2:
                break
        sd = np.sqrt(np.diag(M @ M.T))
        t1 = np.sort(rng.normal(0.0, 1.0, size=int(rng.integers(1, 4)))) * sd[0]
        t2 = np.sort(rng.normal(0.0, 1.0, size=int(rng.integers(1, 4)))) * sd[1]
        H, SW, guards, cgap = skew_channel(M, t1, t2)
        for kk in skew_guard_worst:
            skew_guard_worst[kk] = max(skew_guard_worst[kk], guards[kk])
        skew_min_centroid_gap = min(skew_min_centroid_gap, cgap)
        Sh = sqrtm_psd(Sx)
        Sig = sym(Sh @ SW @ Sh)
        Ed = float(np.trace(P @ Sig))
        skew_inst.append((Sx, P))
        channels.append(("skew", len(base) + len(skew_inst) - 1, H, Ed, H + 0.5 * logdet(SW)))

    # Gaussian channels: random, and near-optimal around Lam*
    gauss_exact_gap, ident_gap, near = [], [], {1e-1: [], 1e-2: [], 1e-3: []}
    for idx, (Sx, P, D) in enumerate(base):
        d = Sx.shape[0]
        Sxi = np.linalg.inv(Sx)
        k = int(rng.integers(1, d + 1))
        Lam = rand_psd_rank(rng, d, k) * float(rng.uniform(0.1, 10.0))
        Sig = np.linalg.inv(Sxi + Lam)
        channels.append(("gauss_random", idx, 0.5 * (logdet(Sx) - logdet(Sig)), float(np.trace(P @ Sig)), None))
        Ss = sigma_star(P, D, Sx)
        Lstar = sym(np.linalg.inv(Ss) - Sxi)
        I0 = 0.5 * (logdet(Sx) - logdet(Ss))
        Ed0 = float(np.trace(P @ Ss))
        gauss_exact_gap.append(I0 - rate_formula(P, Ed0, Sx))     # the optimum attains R at its own E d
        ident_gap.append(abs(I0 - rate_formula(P, D, Sx)))        # det form = eigenvalue form at D
        channels.append(("gauss_optimum", idx, I0, Ed0, None))
        scale = max(float(np.linalg.norm(Lstar, 2)), 1e-12)
        E = rand_psd_rank(rng, d, d)
        E /= float(np.linalg.norm(E, 2))
        for eps in near:
            Sig = np.linalg.inv(Sxi + Lstar + eps * scale * E)
            I = 0.5 * (logdet(Sx) - logdet(Sig))
            Ed = float(np.trace(P @ Sig))
            channels.append((f"gauss_near_eps{int(round(-np.log10(eps)))}", idx, I, Ed, None))
            near[eps].append(I - rate_formula(P, Ed, Sx))

    # r1, r2
    def inst(idx):
        return base[idx][:2] if idx < len(base) else skew_inst[idx - len(base)]

    worst = {}
    r1_ok, r2_ok = True, True
    gaps_by_family = {}
    for fam, idx, I, Ed, slack in channels:
        Sx, P = inst(idx)
        R = rate_formula(P, Ed, Sx)
        gap = I - R
        gaps_by_family.setdefault(fam, []).append(gap)
        tol2 = 1e-7 if fam == "skew" else 1e-9 * max(1.0, R)
        if gap < -tol2:
            r2_ok = False
        if slack is not None:
            tol1 = 1e-7 if fam == "skew" else 1e-9
            if slack < -tol1:
                r1_ok = False
            worst.setdefault(fam, []).append(slack)
    guards_ok = (skew_guard_worst["p_sum"] <= 1e-9 and skew_guard_worst["mean_sum"] <= 1e-8
                 and skew_guard_worst["second_sum"] <= 1e-8 and skew_min_centroid_gap >= 1e-9)
    r1_ok = r1_ok and guards_ok

    # r3
    r3_ok = (max(abs(g) for g in gauss_exact_gap) <= 1e-9 and max(ident_gap) <= 1e-9
             and all(g >= -1e-9 for e in near for g in near[e]) and max(near[1e-3]) <= 1e-3)

    # r4
    r4_eig, r4_tr = [], []
    for Sx, P, D in base:
        Ss = sigma_star(P, D, Sx)
        r4_eig.append(float(np.linalg.eigvalsh(sym(Sx - Ss)).min() / np.linalg.norm(Sx, 2)))
        r4_tr.append(abs(float(np.trace(P @ Ss)) - D) / D)
    mc_rows, mc_ok = [], True
    for Sx, P, D in base[:10]:
        Ss = sigma_star(P, D, Sx)
        n, d = 200000, Sx.shape[0]
        Xh = rng.multivariate_normal(np.zeros(d), sym(Sx - Ss), size=n, method="eigh")
        Z = rng.multivariate_normal(np.zeros(d), Ss, size=n, method="eigh")
        X = Xh + Z
        dist = np.einsum("ni,ij,nj->n", Z, P, Z)
        z_d = (float(dist.mean()) - D) / (float(dist.std(ddof=1)) / np.sqrt(n))
        prods = np.einsum("ni,nj->nij", X, X)
        se = prods.std(axis=0, ddof=1) / np.sqrt(n)
        z_c = float(np.max(np.abs((prods.mean(axis=0) - Sx) / se)))
        mc_rows.append({"z_distortion": z_d, "z_cov_max": z_c})
        mc_ok = mc_ok and abs(z_d) <= 5.0 and z_c <= 5.0
    r4_ok = min(r4_eig) >= -1e-10 and max(r4_tr) <= 1e-9 and mc_ok

    # r5 power
    levels = {"s_1e-3": 1e-3, "s_1e-2": 1e-2, "s_1e-1": 1e-1}
    counts_a = {key: {} for key in levels}
    caught_c, caught_d, caught_e = set(), set(), 0
    for fam, idx, I, Ed, slack in channels:
        Sx, P = inst(idx)
        R = rate_formula(P, Ed, Sx)
        for key, s in levels.items():
            if I < R + s:
                counts_a[key][fam] = counts_a[key].get(fam, 0) + 1
        if I < rate_commuting_shortcut(P, Ed, Sx) - 1e-9:
            caught_c.add(idx)
        if I < rate_vi4_bug(P, Ed, Sx) - 1e-9:
            caught_d.add(idx)
        if I < R / LN2 - 1e-9:
            caught_e += 1
    counts_b = {}
    for fam, sl in worst.items():
        counts_b[fam] = {"s_1e-2": int(sum(x < 0.01 for x in sl)), "s_5e-2": int(sum(x < 0.05 for x in sl))}
    prod_b = counts_b.get("product_random", {}).get("s_5e-2", 0) + counts_b.get("product_aligned", {}).get("s_5e-2", 0)
    r5 = {"a_raised_1e-2": sum(counts_a["s_1e-2"].values()) >= 1,
          "b_lemma_info_raised_5e-2_product": prod_b >= 1,
          "c_commuting_shortcut": len(caught_c) >= 1,
          "d_vi4_bug": len(caught_d) >= 1,
          "e_bits_for_nats": caught_e >= 1}
    r5_ok = all(r5.values())

    out["counts"] = {"base_instances": len(base), "skew_instances": len(skew_inst),
                     "channels": len(channels),
                     "by_family": {f: len(g) for f, g in gaps_by_family.items()}}
    out["lemma_info"] = {"min_slack": {f: float(min(v)) for f, v in worst.items()},
                         "skew_guard_worst": skew_guard_worst,
                         "skew_min_centroid_gap": float(skew_min_centroid_gap)}
    out["converse"] = {"min_gap": {f: float(min(v)) for f, v in gaps_by_family.items()}}
    out["attained"] = {"worst_abs_gap_at_optimum": float(max(abs(g) for g in gauss_exact_gap)),
                       "worst_identity_gap": float(max(ident_gap)),
                       "near_optimum_max_gap": {f"eps{int(round(-np.log10(e)))}": float(max(v)) for e, v in near.items()},
                       "near_optimum_min_gap": {f"eps{int(round(-np.log10(e)))}": float(min(v)) for e, v in near.items()}}
    out["backward"] = {"worst_min_eig_rel": float(min(r4_eig)), "worst_trace_rel": float(max(r4_tr)),
                       "monte_carlo": mc_rows}
    out["power"] = {"a_raised_counts": counts_a, "b_lemma_info_raised_counts": counts_b,
                    "c_commuting_shortcut_instances_caught": len(caught_c),
                    "d_vi4_bug_instances_caught": len(caught_d),
                    "e_bits_channels_caught": caught_e, "gates": r5}
    out["verdict"] = {"r1_lemma_info": bool(r1_ok), "r2_converse": bool(r2_ok), "r3_attained": bool(r3_ok),
                      "r4_backward": bool(r4_ok), "r5_power": bool(r5_ok)}
    out["PAPER3RATE_supported"] = all(out["verdict"].values())
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print("PAPER3RATE-JSON", os.path.relpath(OUT))
    for kk, v in out["verdict"].items():
        print(f"  {kk}: {'PASS' if v else 'FAIL'}")
    print("VERDICT:", "ALL PASS" if out["PAPER3RATE_supported"] else "FAIL")
    return 0 if out["PAPER3RATE_supported"] else 1


if __name__ == "__main__":
    sys.exit(main())
