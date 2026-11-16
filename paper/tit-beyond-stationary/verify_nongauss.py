"""Checks for the non-Gaussian bounds of "Rate and Leakage Beyond Stationary
Gaussian Sources".

The source T in R^2 is a Gaussian mixture, so it is not Gaussian, and every
vector formed from it by linear maps and independent mixture noises is again
a Gaussian mixture whose density is known in closed form.  Differential
entropies are computed by tensor Gauss-Hermite quadrature on each component.

  quadrature        entropies agree between two quadrature orders
  deficits          D(T) >= 0, delta >= 0, and delta <= D(T) for Gaussian
                    holder noise
  inner             the Gaussian test channel of the Gaussian problem with the
                    same second moments, applied to the mixture source, has
                    rate and leakage at most the Gaussian values (holder
                    noise Gaussian and not Gaussian)
  outer_gauss_ch    its weighted cost is at least V_G - a D(T) - (1-a) delta
  outer_other_ch    the same lower bound for a channel with mixture noise,
                    at the distortion of its conditional-mean decoder
  high_resolution   the gap between the Gaussian channel's cost and the lower
                    bound decreases to zero with the distortion
  mixing            V_G of an averaged covariance is at least the allocation
                    over the components (the mixing lemma)

Solver: spectral_core.py of the companion paper.  numpy only.
"""
import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tit-stationary"))
import spectral_core as sc  # noqa: E402

SEED = 20261115
LN2 = np.log(2.0)
OUT = {}
FAILED = []


def report(name, ok, **kv):
    OUT[name] = dict(ok=bool(ok), **kv)
    if not ok:
        FAILED.append(name)
    brief = ", ".join(f"{k}={v:.3e}" if isinstance(v, float) else f"{k}={v}" for k, v in kv.items() if k != "table")
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {brief}", flush=True)


# ------------------------------------------------------------ mixtures
class GM:
    """Gaussian mixture: weights (C,), means (C,d), covariances (C,d,d)."""

    def __init__(self, w, mu, cov):
        self.w = np.asarray(w, float)
        self.mu = np.asarray(mu, float)
        self.cov = np.asarray(cov, float)
        self.d = self.mu.shape[1]

    def mean(self):
        return self.w @ self.mu

    def covariance(self):
        m = self.mean()
        out = np.zeros((self.d, self.d))
        for w, mu, C in zip(self.w, self.mu, self.cov):
            out += w * (C + np.outer(mu - m, mu - m))
        return out

    def linear(self, L):
        L = np.atleast_2d(L)
        return GM(self.w, self.mu @ L.T, np.einsum("ij,cjk,lk->cil", L, self.cov, L))

    def logpdf(self, x):
        """Natural log density at points x (n,d)."""
        terms = []
        for w, mu, C in zip(self.w, self.mu, self.cov):
            Lc = np.linalg.cholesky(C)
            y = np.linalg.solve(Lc, (x - mu).T)
            terms.append(np.log(w) - 0.5 * np.sum(y * y, axis=0) - np.sum(np.log(np.diag(Lc)))
                         - 0.5 * self.d * np.log(2 * np.pi))
        t = np.array(terms)
        mx = t.max(axis=0)
        return mx + np.log(np.exp(t - mx).sum(axis=0))

    def nodes(self, order):
        """Quadrature nodes and weights for expectations under the mixture."""
        z, om = np.polynomial.hermite_e.hermegauss(order)
        om = om / om.sum()
        grids = np.array(list(itertools.product(z, repeat=self.d)))
        wts = np.prod(np.array(list(itertools.product(om, repeat=self.d))), axis=1)
        xs, ws = [], []
        for w, mu, C in zip(self.w, self.mu, self.cov):
            Lc = np.linalg.cholesky(C)
            xs.append(mu + grids @ Lc.T)
            ws.append(w * wts)
        return np.vstack(xs), np.concatenate(ws)

    def entropy(self, order=20):
        """Differential entropy in bits."""
        x, w = self.nodes(order)
        return float(-(w @ self.logpdf(x)) / LN2)


def product(*gms):
    """Joint mixture of independent mixtures (block-diagonal covariances)."""
    w, mu, cov = [1.0], [np.zeros(0)], [np.zeros((0, 0))]
    for g in gms:
        w2, mu2, cov2 = [], [], []
        for a, m, C in zip(w, mu, cov):
            for b, m_, C_ in zip(g.w, g.mu, g.cov):
                w2.append(a * b)
                mu2.append(np.concatenate([m, m_]))
                d0 = C.shape[0]
                Cn = np.zeros((d0 + g.d, d0 + g.d))
                Cn[:d0, :d0] = C
                Cn[d0:, d0:] = C_
                cov2.append(Cn)
        w, mu, cov = w2, mu2, cov2
    return GM(w, mu, cov)


def bimodal(sep, s):
    """Zero-mean scalar mixture 1/2 N(-sep, s^2) + 1/2 N(sep, s^2)."""
    return GM([0.5, 0.5], [[-sep], [sep]], [[[s * s]], [[s * s]]])


def gauss(C):
    C = np.atleast_2d(C)
    return GM([1.0], [np.zeros(C.shape[0])], [C])


def hgauss(C):
    """Entropy in bits of a Gaussian with covariance C."""
    C = np.atleast_2d(C)
    return 0.5 * (C.shape[0] * np.log(2 * np.pi * np.e) + np.linalg.slogdet(C)[1]) / LN2


# ------------------------------------------------------------ the instance
class Instance:
    def __init__(self, rng, noise="gauss"):
        mixT = product(bimodal(1.0, 0.45), bimodal(0.8, 0.6))
        A = np.array([[1.0, 0.6], [-0.3, 1.0]])
        self.T = mixT.linear(A)                      # T in R^2, zero mean, not Gaussian
        self.K = self.T.covariance()
        self.Q = np.array([[1.0, 0.2], [0.2, 0.6]])  # positive definite
        self.H = np.array([[0.7, 0.9]])
        if noise == "gauss":
            self.U = gauss([[0.5]])
        else:
            self.U = bimodal(0.6, 0.38)
        self.SU = self.U.covariance()
        self.J = self.H.T @ np.linalg.solve(self.SU, self.H)
        self.Kc = np.linalg.inv(np.linalg.inv(self.K) + self.J)
        self.base_TU = product(self.T, self.U)
        # (T, S) as a linear image of (T, U)
        L = np.block([[np.eye(2), np.zeros((2, 1))], [self.H, np.eye(1)]])
        self.TS = self.base_TU.linear(L)
        self.S = self.base_TU.linear(np.hstack([self.H, np.eye(1)]))
        self.hT = self.T.entropy(28)
        self.hS = self.S.entropy(40)
        self.hTS = self.TS.entropy(28)
        self.DT = hgauss(self.K) - self.hT                       # D(T || Gaussian), bits
        self.delta = hgauss(self.Kc) - (self.hTS - self.hS)      # h_G(T|S) - h(T|S), bits
        self.Dmax = float(np.trace(self.Q @ self.K))

    def gauss_solution(self, alpha, D):
        R = np.real(sc.psd_sqrt(self.K))
        sol = sc.solve([(sc.herm(R @ self.Q @ R), self.H @ R, self.SU)], [1.0], alpha, D)
        X = np.real(sol["X"][0])
        Delta = R @ X @ R
        return sol, Delta

    def gauss_cost(self, alpha, D):
        if D >= self.Dmax:
            return 0.0
        return self.gauss_solution(alpha, D)[0]["cost"]

    def channel_costs(self, G, Ngm, order=26):
        """Z = G T + N, N ~ Ngm independent.  Returns I(T;Z), I(T;Z|S) in bits
        and the (Z), (Z,S) mixtures."""
        base = product(self.T, self.U, Ngm)
        Lz = np.hstack([G, np.zeros((2, 1)), np.eye(2)])
        Ls = np.hstack([self.H, np.eye(1), np.zeros((1, 2))])
        Z = base.linear(Lz)
        ZS = base.linear(np.vstack([Lz, Ls]))
        hN = Ngm.entropy(28)
        IZ = Z.entropy(28) - hN
        IZS = ZS.entropy(order) - self.hS - hN
        return IZ, IZS, base, Lz

    def mmse_error(self, base, Lz, order=28):
        """E Cov(T | Z) for Z = Lz base, by quadrature over Z."""
        Lt = np.hstack([np.eye(2), np.zeros((2, base.d - 2))])
        Z = base.linear(Lz)
        x, w = Z.nodes(order)
        logs, cond = [], []
        for wc, mu, C in zip(base.w, base.mu, base.cov):
            mz, mt = Lz @ mu, Lt @ mu
            Czz = Lz @ C @ Lz.T
            Ctz = Lt @ C @ Lz.T
            Lc = np.linalg.cholesky(Czz)
            y = np.linalg.solve(Lc, (x - mz).T)
            logs.append(np.log(wc) - 0.5 * np.sum(y * y, axis=0) - np.sum(np.log(np.diag(Lc))))
            cond.append(mt + (x - mz) @ np.linalg.solve(Czz, Ctz.T))
        logs = np.array(logs)
        post = np.exp(logs - logs.max(axis=0))
        post = post / post.sum(axis=0)
        m = np.einsum("cn,cnd->nd", post, np.array(cond))
        second = np.einsum("n,ni,nj->ij", w, m, m)
        return self.K - second


def gauss_forward(K, Delta):
    """G with Delta^{-1} - K^{-1} = G^T G, so that Z = G T + N(0, I) has
    linear-estimation error covariance Delta."""
    M = sc.herm(np.linalg.inv(Delta) - np.linalg.inv(K))
    w, V = np.linalg.eigh(M)
    return (V * np.sqrt(np.clip(w, 0, None))) @ V.T


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    inst = {"gauss": Instance(rng, "gauss"), "mixture": Instance(rng, "mixture")}

    # quadrature orders
    g = inst["mixture"]
    e1 = abs(g.TS.entropy(26) - g.TS.entropy(32))
    e2 = abs(g.T.entropy(20) - g.T.entropy(32))
    e3 = abs(g.S.entropy(30) - g.S.entropy(48))
    report("quadrature", max(e1, e2, e3) < 1e-5, joint=e1, source=e2, holder=e3)

    ok = True
    vals = {}
    for name, I in inst.items():
        vals[name] = dict(D_T=I.DT, delta=I.delta)
        ok = ok and I.DT > 1e-3 and I.delta > -1e-7
    ok = ok and inst["gauss"].delta <= inst["gauss"].DT + 1e-7
    report("deficits", ok, D_T=inst["gauss"].DT, delta_gauss_noise=inst["gauss"].delta,
           delta_mixture_noise=inst["mixture"].delta)

    # inner bound and outer bound on the Gaussian channel
    N0 = gauss(np.eye(2))
    worst_r = worst_l = -np.inf
    worst_lb = np.inf
    rows = []
    for name, I in inst.items():
        for alpha in (0.0, 0.3, 0.7, 1.0):
            for frac in (0.6, 0.3, 0.1):
                D = frac * I.Dmax
                sol, Delta = I.gauss_solution(alpha, D)
                G = gauss_forward(I.K, Delta)
                IZ, IZS, _, _ = I.channel_costs(G, N0)
                cost = alpha * IZ + (1 - alpha) * IZS
                lb = sol["cost"] - alpha * I.DT - (1 - alpha) * I.delta
                worst_r = max(worst_r, IZ - sol["R"])
                worst_l = max(worst_l, IZS - sol["L"])
                worst_lb = min(worst_lb, cost - lb)
                rows.append(dict(noise=name, alpha=alpha, D_over_Dmax=frac, rate=IZ, rate_gauss=sol["R"],
                                 leak=IZS, leak_gauss=sol["L"], lower=lb, cost=cost, upper=sol["cost"]))
    report("inner", worst_r < 1e-6 and worst_l < 1e-6, max_rate_excess=float(worst_r),
           max_leak_excess=float(worst_l), cases=len(rows), table=rows)
    report("outer_gauss_ch", worst_lb > -1e-6, min_margin=float(worst_lb), cases=len(rows))

    # outer bound on a channel that is not Gaussian
    worst = np.inf
    cases = 0
    rows2 = []
    for name, I in inst.items():
        for scale in (0.6, 1.5, 4.0):
            Gm = scale * np.array([[1.0, 0.3], [0.0, 0.8]])
            Nm = product(bimodal(0.9, 0.45), bimodal(0.7, 0.7))
            IZ, IZS, base, Lz = I.channel_costs(Gm, Nm, order=16)
            Dch = float(np.trace(I.Q @ I.mmse_error(base, Lz)))
            for alpha in (0.0, 0.5, 1.0):
                cost = alpha * IZ + (1 - alpha) * IZS
                lb = I.gauss_cost(alpha, Dch) - alpha * I.DT - (1 - alpha) * I.delta
                worst = min(worst, cost - lb)
                rows2.append(dict(noise=name, scale=scale, alpha=alpha, D_over_Dmax=Dch / I.Dmax, cost=cost, lower=lb))
                cases += 1
    report("outer_other_ch", worst > -1e-6, min_margin=float(worst), cases=cases, table=rows2)

    # high resolution
    I = inst["gauss"]
    rows3 = []
    ok = True
    for alpha in (0.0, 0.5, 1.0):
        gaps = []
        for frac in (0.5, 0.2, 0.05, 0.01, 0.002, 0.0004):
            D = frac * I.Dmax
            sol, Delta = I.gauss_solution(alpha, D)
            IZ, IZS, _, _ = I.channel_costs(gauss_forward(I.K, Delta), N0)
            lb = sol["cost"] - alpha * I.DT - (1 - alpha) * I.delta
            gaps.append(alpha * IZ + (1 - alpha) * IZS - lb)
        rows3.append(dict(alpha=alpha, gaps=gaps))
        ok = ok and all(gaps[i + 1] < gaps[i] for i in range(len(gaps) - 1)) and gaps[-1] < 5e-3 and gaps[-1] > -1e-5
    report("high_resolution", ok, last_gap=max(r["gaps"][-1] for r in rows3),
           first_gap=max(r["gaps"][0] for r in rows3), table=rows3)

    # mixing lemma, purely Gaussian
    worst = np.inf
    cases = 0
    for _ in range(40):
        p, r, C = 3, 2, 3
        F = rng.standard_normal((2, p))
        Q = F.T @ F
        H = rng.standard_normal((r, p))
        SU = 0.5 * np.eye(r)
        lam = rng.dirichlet(np.ones(C))
        Ss = []
        for _c in range(C):
            A = rng.standard_normal((p, p))
            Ss.append(A @ A.T + 0.2 * np.eye(p))
        Sbar = sum(l * S for l, S in zip(lam, Ss))
        dm = float(np.trace(Q @ Sbar))
        for alpha in (0.0, 0.5, 1.0):
            D = rng.uniform(0.15, 0.8) * dm
            Rb = np.real(sc.psd_sqrt(Sbar))
            vbar = sc.solve([(sc.herm(Rb @ Q @ Rb), H @ Rb, SU)], [1.0], alpha, D)["cost"]
            blocks = []
            for S in Ss:
                Rc = np.real(sc.psd_sqrt(S))
                blocks.append((sc.herm(Rc @ Q @ Rc), H @ Rc, SU))
            vmix = sc.solve(blocks, lam, alpha, D)["cost"]
            worst = min(worst, vbar - vmix)
            cases += 1
    report("mixing", worst > -1e-8, min_margin=float(worst), cases=cases)

    OUT["_meta"] = dict(seed=SEED, numpy=np.__version__, failed=FAILED, seconds=round(time.time() - t0, 1))
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(OUT, open(os.path.join(here, "verify_nongauss.json"), "w"), indent=1)
    print(f"{len(OUT) - 1 - len(FAILED)} passed, {len(FAILED)} failed, {OUT['_meta']['seconds']} s")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
