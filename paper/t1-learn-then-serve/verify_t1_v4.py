#!/usr/bin/env python3
"""Numerical checks for v4 of the T1 note (paper/t1-learn-then-serve).

Every criterion is fixed in this file before it runs. The checks are not a
registration under PE-CLS-1.0 and cannot net a ledger row; they guard the note's
algebra and constants.

  C1  Matrix Bhatia-Davis: E X^2 <= nu+ nu- I for centred symmetric X with spectrum
      in [-nu-, nu+]; equality for the two-point law.
  C2  Lemma 1 (one-sided Bernstein): coverage of (1-eps-)Q <= Qhat <= (1+eps+)Q is at
      least 1 - delta, on the smooth consumers of the registration draft and on the
      two-point law where the variance bound is tight; eps+- <= the v2 eps_m.
  C3  Corollary 3(i) (probe count): the explicit m makes the learning price <= eta.
  C4  Proposition 12 (sharpness): V_W(alpha, D/b) - V_W(alpha, D/a) lies in
      [(p/2)log2(b/a) - bound(D), (p/2)log2(b/a)], bound = (1-alpha) lmax(J) D (1/a - 1/b)
      / (2 ln2 lmin(W)), and tends to (p/2)log2(b/a).
  C5  Theorem 5 (second order): |E loss - tr(Q Delta)| <= rho_f and <= rho_b for the Gaussian
      test channel, on four smooth consumers, by Gauss-Hermite quadrature; exact
      for a linear consumer; excess / (tr Delta)^2 stays bounded as Delta -> 0.
  C6  Corollary 8(a): with nu- = 1, rhobar = rho_b at s = D / lmin(Qhat), and the budget
      Dhat = (1-eps-)(D - rhobar(D)),
      the frontier designs for Qhat have loss <= D on the event of Lemma 1.
  C7  Remark 15 (softmax): the registration draft's arm-B matrix W has the all-ones vector
      outside its range, so every read metric W^T A(x)^2 W is nonsingular and Q > 0
      (algebraic; no measurement of the registered arm).
  C8  Proposition 2 (finite differences): for the four smooth consumers, at 64 points and
      h in {0.3, 0.1, 0.03, 0.01}, ||Phat - P|| <= 2 M1 sqrt(p) beta + p beta^2 with
      beta = min(M2 h/2, M3 h^2/6), and the mean's error relative to Q is <= eps_h with
      lambda = lmin(Q); the error at h = 0.01 is below 1/50 of that at h = 0.1 (order h^2).
  C9  Proposition 4 (calibration message): for p in {2, 4, 8}, kappa in {2, 30},
      eps_q in {0.1, 0.01}, 50 random Q and Qhat on the event (e+ = 0.2, e- = 0.3): no entry
      leaves the grid, (1 - eps_q) Qhat <= Qtilde <= (1 + eps_q) Qhat, the composite
      sandwich holds, and B equals p(p+1)/2 * ceil(log2(2 N_q + 1)).
  C10 Remark 13: C(x) = (x, x^2), G = diag(1, 0) has loss exactly (xhat - x)^2 (so (A1a)
      holds with Q = 1, nu = 0), its weighted map is 1-Lipschitz, and C is not Lipschitz
      (difference quotients of x^2 exceed 1000 on [500, 501]).
  C11 Theorem 7, step (3): in one dimension (T ~ N(0, 2), test channel Delta = 0.3), for
      x + 0.2 sin x and the circle consumer, the surrogate distortion of the quantized
      channel, E[ d_k(T_k, That_k) ], minus the channel's consumer loss, on common samples
      (N = 2e6), is below 0.2% of the loss at k = 6 and below 1/10 of its value at k = 1.
  C12 Corollary 3(ii): the explicit m and h make the price with eps+- + eps_h <= eta.
  C13 Remark 13 (added for v4.1, after audit VI-24): the expanding ReLU layer
      g(x) = (ReLU(x), ReLU(-x)) componentwise has loss between 1/2 and 1 times
      |xhat - x|^2, both ends attained, so (A1a) holds with Q = I, nu- = 1/2, nu+ = 0.

Run: python paper/t1-learn-then-serve/verify_t1_v4.py   (writes verify_t1_v4.json)
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "paper" / "tit-stationary"))
import spectral_core as sc  # noqa: E402

LN2 = np.log(2.0)
OUT = {}
FAIL = []


def check(name, ok, **info):
    OUT[name] = dict(ok=bool(ok), **info)
    print(f"{'PASS' if ok else 'FAIL'}  {name}  " + ", ".join(f"{k}={v}" for k, v in info.items()
                                                       if not isinstance(v, (list, dict))))
    if not ok:
        FAIL.append(name)


def sym(A):
    return (A + A.T) / 2


def msqrt(A):
    w, V = np.linalg.eigh(sym(A))
    return (V * np.sqrt(np.clip(w, 0, None))) @ V.T


def minv_sqrt(A):
    w, V = np.linalg.eigh(sym(A))
    return (V / np.sqrt(w)) @ V.T


def eps_pm(nup, num, m, p, delta):
    L = np.log(2 * p / delta)
    root = np.sqrt(2 * nup * num * L / m)
    return root + 2 * nup * L / (3 * m), root + 2 * num * L / (3 * m)


def eps_v2(nu, m, p, delta):
    L = np.log(2 * p / delta)
    return nu * (np.sqrt(2 * L / m) + 2 * L / (3 * m))


# ----------------------------------------------------------------------------- C1
def c1():
    rng = np.random.default_rng(20261117)
    worst = -np.inf
    for trial in range(2000):
        p = int(rng.integers(1, 5))
        nup, num = rng.uniform(0.01, 1.5), rng.uniform(0.01, 1.0)
        k = int(rng.integers(2, 6))
        mats = []
        for _ in range(k):
            U, _ = np.linalg.qr(rng.standard_normal((p, p)))
            mats.append((U * rng.uniform(-num, nup, p)) @ U.T)
        w = rng.dirichlet(np.ones(k))
        mu = sum(wi * M for wi, M in zip(w, mats))
        # one more atom, -mu/s, scaled into the spectral range; weight 1/(1+s) on the
        # first k atoms makes the mixture's mean exactly zero
        lam = np.linalg.eigvalsh(mu)
        s = max(-lam.min() / nup, lam.max() / num, 1e-12)
        atoms = mats + [-mu / s]
        wts = np.r_[w / (1 + s), s / (1 + s)]
        assert np.abs(sum(wi * M for wi, M in zip(wts, atoms))).max() < 1e-12
        for M in atoms:
            ev = np.linalg.eigvalsh(M)
            assert ev.min() >= -num - 1e-12 and ev.max() <= nup + 1e-12
        EX2 = sum(wi * M @ M for wi, M in zip(wts, atoms))
        worst = max(worst, np.linalg.eigvalsh(EX2).max() / (nup * num) - 1)
    two_pt = []
    for nup, num in [(0.062, 0.164), (0.233, 0.522), (1.0, 1.0), (3.0, 1.0)]:
        pr = num / (nup + num)            # P(X = nup)
        EX2 = pr * nup ** 2 + (1 - pr) * num ** 2
        two_pt.append(EX2 / (nup * num))
    check("C1 matrix Bhatia-Davis", worst <= 1e-12 and np.allclose(two_pt, 1.0),
          max_ratio_minus_1=float(worst), two_point_ratios=[float(x) for x in two_pt])


# ----------------------------------------------------------------------------- consumers
def q_sin(s2, beta):
    return 1 + 2 * beta * np.exp(-s2 / 2) + (beta ** 2 / 2) * (1 + np.exp(-2 * s2))


SIG = np.diag([2.0, 0.5])
G = np.diag([4.0, 1.0])


def sin_arm(beta):
    q = q_sin(np.diag(SIG), beta)
    Q = G @ np.diag(q)
    num = 1 - min((1 - beta) ** 2 / q)
    nup = max((1 + beta) ** 2 / q) - 1
    return Q, nup, num


def c2():
    rng = np.random.default_rng([20261117, 2])
    delta, p, reps = 0.1, 2, 4000
    rows = []
    ok = True
    for beta in (0.05, 0.2):
        Q, nup, num = sin_arm(beta)
        Mi = minv_sqrt(Q)
        for m in (8, 32, 128, 512):
            ep, em = eps_pm(nup, num, m, p, delta)
            ev2 = eps_v2(max(nup, num), m, p, delta)
            X = rng.standard_normal((reps, m, p)) * np.sqrt(np.diag(SIG))
            d = 1 + beta * np.cos(X)                      # diagonal Jacobian entries
            Qh = np.einsum("rmi,ij->rij", d ** 2, G) / m   # diag(G) * mean d^2 (diagonal)
            Qh = Qh * np.eye(p)
            lam = np.array([np.linalg.eigvalsh(sym(Mi @ A @ Mi)) for A in Qh])
            cov = np.mean((lam.max(1) <= 1 + ep) & (lam.min(1) >= 1 - em))
            rows.append(dict(beta=beta, m=m, eps_plus=float(ep), eps_minus=float(em),
                             eps_v2=float(ev2), coverage=float(cov)))
            ok &= cov >= 1 - delta and ep <= ev2 + 1e-15 and em <= ev2 + 1e-15
    # the two-point law where the variance bound is attained: scalar per coordinate,
    # independent coordinates, P = Q^{1/2}(I + X)Q^{1/2}
    for nup, num in [(0.25, 0.5), (0.9, 0.9), (2.0, 0.3)]:
        for m in (8, 32, 128):
            ep, em = eps_pm(nup, num, m, p, delta)
            pr = num / (nup + num)
            Z = np.where(rng.random((reps, m, p)) < pr, nup, -num)
            mean = Z.mean(1)
            cov = np.mean((mean.max(1) <= ep) & (mean.min(1) >= -em))
            rows.append(dict(two_point=(nup, num), m=m, eps_plus=float(ep), eps_minus=float(em),
                             coverage=float(cov)))
            ok &= cov >= 1 - delta
    check("C2 Lemma 1 coverage and eps+- <= eps_v2", ok,
          min_coverage=min(r["coverage"] for r in rows), rows=rows)


# ----------------------------------------------------------------------------- C3
def c3():
    worst = -np.inf
    n = 0
    for p, nup, num, eta, delta in itertools.product((1, 2, 8, 64), (0.01, 0.2, 1.0, 3.0),
                                                    (0.01, 0.3, 1.0), (0.01, 0.1, 1.0),
                                                    (1e-6, 0.1)):
        if eta > p:
            continue
        L = np.log(2 * p / delta)
        nu = max(nup, num)
        m = int(np.ceil(L * max(200 / 9 * nup * num * p ** 2 / eta ** 2, 20 / 9 * nu * p / eta)))
        ep, em = eps_pm(nup, num, m, p, delta)
        if em >= 1:
            worst = np.inf
            break
        price = p / 2 * np.log2((1 + ep) / (1 - em))
        worst = max(worst, price / eta)
        n += 1
    check("C3 Corollary 3(i) probe count", worst <= 1 + 1e-12, cases=n, max_price_over_eta=float(worst))


# ----------------------------------------------------------------------------- C4
class Coder:
    def __init__(self, Sig, H, SU):
        self.Sig, self.S12 = Sig, msqrt(Sig)
        self.Ht = np.array(H, float) @ self.S12
        self.SU = np.array(SU, float)
        self.J = np.array(H, float).T @ np.linalg.solve(self.SU, np.array(H, float))

    def design(self, W, alpha, D):
        Qt = sym(self.S12 @ W @ self.S12)
        r = sc.solve([(Qt, self.Ht, self.SU)], [1.0], alpha, D)
        X = sym(r["X"][0])
        return dict(Delta=sym(self.S12 @ X @ self.S12), cost=r["cost"], R=r["R"], L=r["L"])


def c4():
    coder = Coder(SIG, [[1.0, 0.5]], [[1.0]])
    W = G
    p = 2
    lw, ls = np.linalg.eigvalsh(W).min(), np.linalg.eigvalsh(SIG).min()
    rows, ok = [], True
    for a, b in [(0.8, 1.25), (0.5, 1.0), (0.9, 3.0)]:
        target = p / 2 * np.log2(b / a)
        for alpha in (0.0, 0.5, 1.0):
            gaps = []
            for D in (1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001):
                gap = coder.design(W, alpha, D / b)["cost"] - coder.design(W, alpha, D / a)["cost"]
                bound = (1 - alpha) * np.linalg.eigvalsh(coder.J).max() * D * (1 / a - 1 / b) / (2 * LN2 * lw)
                valid = D <= a * lw * ls
                inside = gap <= target + 1e-8 and (not valid or gap >= target - bound - 1e-8)
                ok &= inside
                gaps.append(dict(D=D, gap=float(gap), target=float(target), bound=float(bound),
                                 bound_applies=bool(valid), inside=bool(inside)))
            ok &= target - gaps[-1]["gap"] <= 3e-3     # the limit D -> 0
            rows.append(dict(a=a, b=b, alpha=alpha, gaps=gaps))
    check("C4 Proposition 12 sharpness", ok,
          final_gap_errors=[float(r["gaps"][-1]["gap"] - r["gaps"][-1]["target"]) for r in rows],
          rows=rows)


# ----------------------------------------------------------------------------- C5
GH_X, GH_W = np.polynomial.hermite_e.hermegauss(40)
GH_W = GH_W / GH_W.sum()


class Consumer:
    """C: R^p -> R^k with analytic Jacobian, sup-norm derivative bounds in the G geometry."""

    def __init__(self, name, f, jac, M1, M2, M3, Gout):
        self.name, self.f, self.jac = name, f, jac
        self.M1, self.M2, self.M3, self.G = M1, M2, M3, Gout

    def loss(self, X, Xh):
        d = self.f(Xh) - self.f(X)
        return np.einsum("ni,ij,nj->n", d, self.G, d)

    def P(self, X):
        Jx = self.jac(X)
        return np.einsum("nki,kl,nlj->nij", Jx, self.G, Jx)


def gauss_grid(dim):
    pts = np.array(list(itertools.product(range(len(GH_X)), repeat=dim)))
    return GH_X[pts], np.prod(GH_W[pts], axis=1)


GRID2 = gauss_grid(2)
GRID4 = gauss_grid(4)


def Q_of(cons, Sig):
    z, w = GRID2
    X = z @ msqrt(Sig)
    return np.einsum("n,nij->ij", w, cons.P(X))


def test_channel_loss(cons, Sig, Delta):
    """E loss for T ~ N(0,Sig), That = (I - Delta Sig^-1) T + V, V ~ N(0, Delta - Delta Sig^-1 Delta)."""
    z, w = GRID4
    p = Sig.shape[0]
    T = z[:, :p] @ msqrt(Sig)
    B = Delta @ np.linalg.inv(Sig)
    CV = sym(Delta - B @ Delta)
    V = z[:, p:] @ msqrt(CV)
    Th = T - T @ B.T + V
    return float(w @ cons.loss(T, Th))


def rho_b(cons, Delta):
    s = float(np.trace(Delta))
    M1, M2, M3 = cons.M1, cons.M2, cons.M3
    return ((1.75 * M2 ** 2 + 2 * M1 * M3) * s ** 2 + np.sqrt(5) / 2 * M2 * M3 * s ** 2.5
            + 5 / 12 * M3 ** 2 * s ** 3)


def rho(cons, Sig, Delta, Q, omega=None):
    s = float(np.trace(Delta))
    th = float(np.trace(Delta @ np.linalg.solve(Sig, Delta)))
    lq = np.linalg.eigvalsh(Q)
    if omega is None:
        omega = max(cons.M1 ** 2 - lq.min(), lq.max())
    M1, M2, M3 = cons.M1, cons.M2, cons.M3
    return (omega * th + M1 * M2 * (3 ** 0.75 * th ** 1.5 + 3 * th ** 0.5 * s)
            + (0.75 * M2 ** 2 + M1 * M3) * s ** 2 + np.sqrt(5) / 2 * M2 * M3 * s ** 2.5
            + 5 / 12 * M3 ** 2 * s ** 3)


def consumers():
    out = []
    g = np.diag(G)
    for beta in (0.05, 0.2):
        out.append(Consumer(f"sin beta={beta}",
                            lambda X, b=beta: X + b * np.sin(X),
                            lambda X, b=beta: np.einsum("ni,ij->nij", 1 + b * np.cos(X), np.eye(2)),
                            np.sqrt(g.max()) * (1 + beta), np.sqrt(g.max()) * beta,
                            np.sqrt(g.max()) * beta, G))
    # a coupled consumer: x + beta A tanh(B x), G = I
    A = np.array([[1.0, 0.6], [-0.4, 1.0]])
    Bm = np.array([[0.8, -0.5], [0.3, 1.1]])
    beta = 0.3
    nA, nB = np.linalg.norm(A, 2), np.linalg.norm(Bm, 2)

    def f_t(X):
        return X + beta * np.tanh(X @ Bm.T) @ A.T

    def j_t(X):
        s = 1 - np.tanh(X @ Bm.T) ** 2
        return np.eye(2)[None] + beta * np.einsum("ij,nj,jk->nik", A, s, Bm)

    out.append(Consumer("x + 0.3 A tanh(Bx)", f_t, j_t, 1 + beta * nA * nB,
                        beta * nA * nB ** 2 * 4 / (3 * np.sqrt(3)), 2 * beta * nA * nB ** 3, np.eye(2)))
    # the circle consumer (fails (A1)): (cos x1, sin x1, cos x2, sin x2), G = I
    def f_c(X):
        return np.column_stack([np.cos(X[:, 0]), np.sin(X[:, 0]), np.cos(X[:, 1]), np.sin(X[:, 1])])

    def j_c(X):
        n = len(X)
        Jx = np.zeros((n, 4, 2))
        Jx[:, 0, 0], Jx[:, 1, 0] = -np.sin(X[:, 0]), np.cos(X[:, 0])
        Jx[:, 2, 1], Jx[:, 3, 1] = -np.sin(X[:, 1]), np.cos(X[:, 1])
        return Jx
    out.append(Consumer("circle (cos, sin) per coordinate", f_c, j_c, 1.0, 1.0, 1.0, np.eye(4)))
    return out


def c5():
    coder = Coder(SIG, [[1.0, 0.5]], [[1.0]])
    rows, ok = [], True
    lin = Consumer("linear", lambda X: X @ np.array([[1.0, 0.3], [0.0, 0.7]]).T,
                   lambda X: np.broadcast_to(np.array([[1.0, 0.3], [0.0, 0.7]]), (len(X), 2, 2)),
                   np.linalg.norm([[1.0, 0.3], [0.0, 0.7]], 2), 0.0, 0.0, G)
    lin_err = 0.0
    for cons in [lin] + consumers():
        Q = Q_of(cons, SIG)
        ratios = []
        for alpha in (0.0, 0.5, 1.0):
            for frac in (0.3, 0.1, 0.03, 0.01, 0.003):
                D = frac * float(np.trace(Q @ SIG))
                Delta = coder.design(Q, alpha, D)["Delta"]
                El = test_channel_loss(cons, SIG, Delta)
                exc = El - float(np.trace(Q @ Delta))
                rf = rho(cons, SIG, Delta, Q)
                rb = rho_b(cons, Delta)
                r = min(rf, rb)
                s = float(np.trace(Delta))
                inside = (abs(exc) <= rf + 1e-12 * max(1.0, El)) and (abs(exc) <= rb + 1e-12 * max(1.0, El))
                ok &= inside
                ratios.append(dict(alpha=alpha, frac=frac, s=s, loss=El, excess=exc, rho=r,
                                   rho_f=rf, rho_b=rb,
                                   excess_over_s2=exc / s ** 2, rho_over_s2=r / s ** 2,
                                   inside=bool(inside)))
                if cons.name == "linear":
                    lin_err = max(lin_err, abs(exc) / El)
        rows.append(dict(consumer=cons.name, Q=Q.tolist(), cases=ratios))
    ok &= lin_err < 1e-12
    # boundedness of excess / s^2 as s -> 0 (the second-order claim): the last two
    # fractions differ by at most a factor 2 in excess/s^2 for each consumer and alpha
    for r in rows:
        for alpha in (0.0, 0.5, 1.0):
            e = [c["excess_over_s2"] for c in r["cases"] if c["alpha"] == alpha]
            if r["consumer"] != "linear":
                ok &= abs(e[-1]) <= 2 * abs(e[-2]) + 1e-6
    check("C5 Theorem 5 second-order bound", ok, linear_rel_err=float(lin_err),
          worst_excess_over_rho=float(max(abs(c["excess"]) / c["rho"] for r in rows
                                           for c in r["cases"] if c["rho"] > 0)),
          rows=rows)


# ----------------------------------------------------------------------------- C6
def c6():
    """Learn without the lower sandwich (nu- = 1), certify by the closed form, serve."""
    coder = Coder(SIG, [[1.0, 0.5]], [[1.0]])
    rng = np.random.default_rng([20261117, 6])
    delta, p = 0.1, 2
    rows, ok = [], True
    for cons in consumers()[:3]:
        Q = Q_of(cons, SIG)
        # an a priori nu+ (here M1^2 / lambda_min(Q) - 1, standing in for prior knowledge)
        nup = cons.M1 ** 2 / np.linalg.eigvalsh(Q).min() - 1
        for m in (128, 512):
            ep, em = eps_pm(nup, 1.0, m, p, delta)
            X = rng.standard_normal((m, p)) @ msqrt(SIG)
            Qh = cons.P(X).mean(0)
            Mi = minv_sqrt(Q)
            lam = np.linalg.eigvalsh(sym(Mi @ Qh @ Mi))
            event = bool(lam.max() <= 1 + ep and lam.min() >= 1 - em)
            for frac in (0.002, 0.0005):
                D = frac * float(np.trace(Q @ SIG))
                sb = D / np.linalg.eigvalsh(Qh).min()
                M1, M2, M3 = cons.M1, cons.M2, cons.M3
                rb = ((1.75 * M2 ** 2 + 2 * M1 * M3) * sb ** 2 + np.sqrt(5) / 2 * M2 * M3 * sb ** 2.5
                      + 5 / 12 * M3 ** 2 * sb ** 3)     # rho_b at s = D / lmin(Qhat)
                if rb >= D or em >= 1:
                    ok = False
                    continue
                Dh = (1 - em) * (D - rb)
                for alpha in (0.0, 0.5, 1.0):
                    des = coder.design(Qh, alpha, Dh)
                    El = test_channel_loss(cons, SIG, des["Delta"])
                    good = (not event) or El <= D
                    # the cost statement: V_Qhat(alpha, Dhat) <= V_Q(alpha, D) + taubar
                    taubar = p / 2 * np.log2((1 + ep) / ((1 - em) * (1 - rb / D)))
                    vq = coder.design(Q, alpha, D)["cost"]
                    cost_ok = (not event) or des["cost"] <= vq + taubar + 1e-9
                    ok &= good and cost_ok
                    rows.append(dict(consumer=cons.name, m=m, frac=frac, alpha=alpha, D=D,
                                     rhobar_over_D=rb / D, Dhat=Dh, loss=El, loss_over_D=El / D,
                                     event=event, cost=des["cost"], VQ_plus_taubar=vq + taubar,
                                     taubar=taubar, eps_plus=ep, eps_minus=em))
    check("C6 Corollary 8(a) certified design", ok,
          loss_over_D_range=[float(min(r["loss_over_D"] for r in rows)),
                             float(max(r["loss_over_D"] for r in rows))], rows=rows)


def c7():
    W = np.random.default_rng(20261117).standard_normal((3, 2))
    W = W / np.linalg.norm(W, 2)
    one = np.ones(3) / np.sqrt(3)
    Pw = W @ np.linalg.pinv(W)
    dist = float(np.linalg.norm(one - Pw @ one))
    rank = int(np.linalg.matrix_rank(W))
    check("C7 arm-B softmax weight is nonsingular", dist > 1e-6 and rank == 2,
          distance_of_ones_from_range=dist, rank_W=rank)


# ----------------------------------------------------------------------------- C8
def c8():
    rng = np.random.default_rng([20261117, 8])
    rows, ok, p = [], True, 2
    for cons in consumers():
        Q = Q_of(cons, SIG)
        lam = float(np.linalg.eigvalsh(Q).min())
        Mi = minv_sqrt(Q)
        X = rng.standard_normal((64, p)) @ msqrt(SIG)
        P = cons.P(X)
        errs = {}
        for h in (0.3, 0.1, 0.03, 0.01):
            cols = []
            for j in range(p):
                e = np.zeros(p)
                e[j] = h
                cols.append((cons.f(X + e) - cons.f(X - e)) / (2 * h))
            Jh = np.stack(cols, axis=2)                                  # (n, k, p)
            Ph = np.einsum("nki,kl,nlj->nij", Jh, cons.G, Jh)
            err = max(float(np.linalg.norm(Ph[i] - P[i], 2)) for i in range(len(X)))
            beta = min(cons.M2 * h / 2, cons.M3 * h ** 2 / 6)
            bound = 2 * cons.M1 * np.sqrt(p) * beta + p * beta ** 2
            eps_h = bound / lam
            rel = float(np.abs(np.linalg.eigvalsh(sym(Mi @ (Ph.mean(0) - P.mean(0)) @ Mi))).max())
            inside = err <= bound * (1 + 1e-9) + 1e-14 and rel <= eps_h * (1 + 1e-9) + 1e-14
            ok &= inside
            errs[h] = err
            rows.append(dict(consumer=cons.name, h=h, max_err=err, bound=float(bound),
                             err_over_bound=err / bound, rel_mean_err=rel, eps_h=float(eps_h),
                             inside=bool(inside)))
        ok &= errs[0.01] <= errs[0.1] / 50 + 1e-13
    check("C8 Proposition 2 finite differences", ok,
          max_err_over_bound=max(r["err_over_bound"] for r in rows), rows=rows)


# ----------------------------------------------------------------------------- C9
def c9():
    rng = np.random.default_rng([20261117, 9])
    rows, ok = [], True
    e_p, e_m = 0.2, 0.3
    for p in (2, 4, 8):
        for kappa in (2.0, 30.0):
            for eq in (0.1, 0.01):
                worst_rel, clipped = 0.0, 0
                for _ in range(50):
                    U, _r = np.linalg.qr(rng.standard_normal((p, p)))
                    ev = np.exp(rng.uniform(0, np.log(kappa), p))
                    ev[0], ev[-1] = 1.0, kappa
                    scale = rng.uniform(0.1, 10)
                    Q = sym((U * (scale * ev)) @ U.T)
                    lam, Lam = scale, scale * kappa
                    V, _r = np.linalg.qr(rng.standard_normal((p, p)))
                    Xm = (V * rng.uniform(-e_m, e_p, p)) @ V.T
                    R12 = msqrt(Q)
                    Qh = sym(R12 @ (np.eye(p) + Xm) @ R12)
                    s = 2 * (1 - e_m) * lam * eq / p
                    Nq = int(np.ceil(p * kappa * (1 + e_p) / (2 * (1 - e_m) * eq)))
                    iu = np.triu_indices(p)
                    j_raw = np.rint(Qh[iu] / s)
                    clipped += int(np.any(np.abs(j_raw) > Nq))
                    j = np.clip(j_raw, -Nq, Nq)
                    Qt = np.zeros((p, p))
                    Qt[iu] = j * s
                    Qt = Qt + np.triu(Qt, 1).T
                    Hi = minv_sqrt(Qh)
                    rel = float(np.abs(np.linalg.eigvalsh(sym(Hi @ (Qt - Qh) @ Hi))).max())
                    worst_rel = max(worst_rel, rel / eq)
                    Mi = minv_sqrt(Q)
                    lq = np.linalg.eigvalsh(sym(Mi @ Qt @ Mi))
                    ok &= (lq.min() >= (1 - e_m) * (1 - eq) - 1e-12
                           and lq.max() <= (1 + e_p) * (1 + eq) + 1e-12)
                B = p * (p + 1) // 2 * int(np.ceil(np.log2(2 * Nq + 1)))
                ok &= worst_rel <= 1 + 1e-9 and clipped == 0
                rows.append(dict(p=p, kappa=kappa, eps_q=eq, N_q=Nq, bits=B,
                                 max_rel_err_over_eps_q=worst_rel, clipped=clipped))
    check("C9 Proposition 4 calibration message", ok,
          max_rel_err_over_eps_q=max(r["max_rel_err_over_eps_q"] for r in rows), rows=rows)


# ----------------------------------------------------------------------------- C10
def c10():
    rng = np.random.default_rng([20261117, 10])
    x, xh = rng.normal(0, 30, 10 ** 5), rng.normal(0, 30, 10 ** 5)
    Gm = np.diag([1.0, 0.0])
    d = np.column_stack([xh - x, xh ** 2 - x ** 2])
    loss = np.einsum("ni,ij,nj->n", d, Gm, d)
    exact = float(np.max(np.abs(loss - (xh - x) ** 2)))
    g_lip = float(np.max(np.abs((np.sqrt(Gm) @ d.T)[0]) / np.abs(xh - x)))
    a = np.linspace(500, 501, 101)
    quot = float(np.min(np.abs(a[1:] ** 2 - a[:-1] ** 2) / np.abs(a[1:] - a[:-1])))
    check("C10 Remark 13 semidefinite G example", exact == 0.0 and g_lip <= 1 + 1e-12 and quot > 1000,
          max_loss_minus_quadratic=exact, weighted_map_lipschitz=g_lip,
          min_difference_quotient_of_x2_on_500_501=quot)


# ----------------------------------------------------------------------------- C11
def q_k(x, k):
    return np.clip(np.floor(x * 2.0 ** k) / 2.0 ** k, -2.0 ** k, 2.0 ** k)


def cell_moments(gfun, sigma, k, dim):
    """E[g(T) | T_k = c] and E[|g(T)|^2 | T_k = c] for the cells of q_k, T ~ N(0, sigma^2)."""
    from math import erf, sqrt
    w = 2.0 ** -k
    lo = -(2.0 ** k)
    edges = lo + w * np.arange(2 * 4 ** k + 1)          # -2^k, ..., 2^k
    # cell 0 is (-inf, lo + w): merged lower tail; the last is [2^k, inf)
    left = np.r_[-12 * sigma, edges[1:-1], edges[-1]]
    right = np.r_[edges[1:-1], edges[-1], 12 * sigma]
    m1 = np.zeros((len(left), dim))
    m2 = np.zeros(len(left))
    for i, (a, b) in enumerate(zip(left, right)):
        if b <= a:
            continue
        n = 40 if b - a < 1 else 400
        z, wt = np.polynomial.legendre.leggauss(n)
        xs = (a + b) / 2 + (b - a) / 2 * z
        dens = np.exp(-xs ** 2 / (2 * sigma ** 2)) * wt * (b - a) / 2
        mass = dens.sum()
        if mass <= 0:
            continue
        gv = gfun(xs)
        m1[i] = dens @ gv / mass
        m2[i] = dens @ np.sum(gv ** 2, axis=1) / mass
    # q_k(x) = left endpoint; index of a value v = q_k(x) among the cells
    return m1, m2, lo, w


def c11():
    rng = np.random.default_rng([20261117, 11])
    sig2, Dl, N = 2.0, 0.3, 2 * 10 ** 6
    sigma = np.sqrt(sig2)
    a = 1 - Dl / sig2
    T = rng.normal(0, sigma, N)
    Th = a * T + rng.normal(0, np.sqrt(a * Dl), N)
    cons = {"x + 0.2 sin x": lambda x: (x + 0.2 * np.sin(x))[:, None],
            "circle (cos x, sin x)": lambda x: np.column_stack([np.cos(x), np.sin(x)])}
    rows, ok = [], True
    for name, gf in cons.items():
        truth = float(np.mean(np.sum((gf(T) - gf(Th)) ** 2, axis=1)))
        gaps = []
        for k in range(1, 7):
            m1, m2, lo, w = cell_moments(gf, sigma, k, gf(np.zeros(1)).shape[1])
            idx = np.clip(np.floor((T - lo) / w).astype(np.int64), 0, len(m2) - 1)
            idx[T >= 2.0 ** k] = len(m2) - 1
            gk = gf(q_k(Th, k))
            sur = float(np.mean(m2[idx] - 2 * np.sum(m1[idx] * gk, axis=1) + np.sum(gk ** 2, axis=1)))
            gaps.append(sur - truth)
        rel = [abs(x) / truth for x in gaps]
        good = rel[-1] < 2e-3 and abs(gaps[-1]) < abs(gaps[0]) / 10
        ok &= good
        rows.append(dict(consumer=name, loss=truth, gap_by_k=[float(x) for x in gaps],
                         rel_gap_by_k=[float(x) for x in rel], ok=bool(good)))
    check("C11 Theorem 7 surrogate distortion converges", ok,
          final_rel_gaps=[r["rel_gap_by_k"][-1] for r in rows], rows=rows)


# ----------------------------------------------------------------------------- C12
def c12():
    worst, n = -np.inf, 0
    for p, nup, num, eta, delta, M1, M3, lam in itertools.product(
            (1, 2, 8, 64), (0.01, 0.2, 1.0, 3.0), (0.01, 0.3, 1.0), (0.01, 0.1, 1.0),
            (1e-6, 0.1), (1.0, 5.0), (0.1, 10.0), (0.01, 1.0)):
        if eta > p:
            continue
        L = np.log(2 * p / delta)
        nu = max(nup, num)
        m = int(np.ceil(L * max(50 * nup * num * p ** 2 / eta ** 2, 10 / 3 * nu * p / eta)))
        h = np.sqrt(6 / M3 * min(lam * eta / (20 * M1 * p ** 1.5), np.sqrt(lam * eta / (10 * p ** 2))))
        beta = M3 * h ** 2 / 6
        eh = (2 * M1 * np.sqrt(p) * beta + p * beta ** 2) / lam
        ep, em = eps_pm(nup, num, m, p, delta)
        if em + eh >= 1:
            worst = np.inf
            break
        price = p / 2 * np.log2((1 + ep + eh) / (1 - em - eh))
        worst = max(worst, price / eta)
        n += 1
    check("C12 Corollary 3(ii) probe count with finite differences", worst <= 1 + 1e-12,
          cases=n, max_price_over_eta=float(worst))


# ----------------------------------------------------------------------------- C13
def c13():
    rng = np.random.default_rng([20261118, 13])
    lo, hi = np.inf, -np.inf
    for p in (1, 2, 4):
        x, xh = rng.normal(0, 2, (20000, p)), rng.normal(0, 2, (20000, p))
        g = lambda z: np.concatenate([np.maximum(z, 0), np.maximum(-z, 0)], axis=1)  # noqa: E731
        r = np.sum((g(xh) - g(x)) ** 2, 1) / np.sum((xh - x) ** 2, 1)
        lo, hi = min(lo, r.min()), max(hi, r.max())
    # the two ends, attained: same signs (ratio 1) and opposite points (ratio 1/2)
    one = float(np.sum((g(np.array([[2.0]])) - g(np.array([[1.0]]))) ** 2))
    half = float(np.sum((g(np.array([[1.0]])) - g(np.array([[-1.0]]))) ** 2) / 4.0)
    ok = lo >= 0.5 - 1e-12 and hi <= 1 + 1e-12 and abs(one - 1) < 1e-15 and abs(half - 0.5) < 1e-15
    check("C13 Remark 13 expanding ReLU satisfies (A1a)", ok, min_ratio=float(lo), max_ratio=float(hi),
          same_sign_ratio=one, opposite_ratio=half)


if __name__ == "__main__":
    for f in (c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13):
        f()
    OUT["verdict"] = "ALL PASS" if not FAIL else "FAIL: " + ", ".join(FAIL)
    print(OUT["verdict"])
    (HERE / "verify_t1_v4.json").write_text(json.dumps(OUT, indent=1, default=float))
