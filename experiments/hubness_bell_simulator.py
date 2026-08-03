# Hubness-Bell simulator: is "contextual hubness" a mechanism for Bell-type
# correlations, or just a new vocabulary for the detection loophole?
#
# HONEST FRAMING (stated before any run).  Phase 1 is NOT an empirical
# question: for latent states sampled independently of the settings with
# locally factorizable responses, |K(lambda)| = 2 pointwise, so S <= 2 for ANY
# rho -- any dimension, any density skew, any hubness.  Phase 1 is therefore a
# FALSIFICATION NET on the simulator itself: if it ever reports S > 2 there,
# the code is wrong, not physics.  Phase 2 (setting-dependent retention) will
# exceed 2 easily; that is Pearle (1970) / Gisin-Gisin, i.e. the detection
# loophole.  Neither result is news.
#
# The research-worthy question is a DISSOCIATION:
#   does CHSH strength track CONTEXTUAL ensemble shift while being blind to
#   AGGREGATE hubness?
# If yes, hubness is not the primitive -- contextual shift is, and hubness
# matters only insofar as it induces it.
#
# Four diagnostics that can kill the idea outright:
#   D1 Tsirelson: if S can exceed 2*sqrt(2) (up to the algebraic 4), the model
#      is TOO PERMISSIVE to be an explanation of QM -- it does not reproduce
#      the quantum boundary, it just breaks the classical one.
#   D2 No-signalling: does Alice's conditioned marginal depend on Bob's
#      setting?  If it signals, it is not a viable causal model at all.
#   D3 Rejections-as-outcomes: re-score counting non-detections as physical
#      outcomes.  If the violation vanishes, it WAS postselection.
#   D4 Partial correlation of (S-2) with contextual shift controlling for hub
#      skew, and vice versa.  Also tests the loose bound S <= 2 + 8*delta.
#
# Latent space: unit vectors on S^{d-1} with tunable hubness via a
# concentration mixture (a dense core plus a uniform shell) and Zipf atom
# weights.  Hubness measured the standard way: skewness of the k-occurrence
# count N_k (Radovanovic et al. 2010).
#
# numpy only, CPU, deterministic.  Usage:
#   python experiments/hubness_bell_simulator.py [--n 200000] [--trials 24]
# Output: sentinel JSON ===HBELL-JSON===.  MIT.
import argparse
import json
import sys
import time

import numpy as np

TSIRELSON = 2.0 * np.sqrt(2.0)


# ------------------------------------------------------------ latent corpus
def make_latents(n, d, core_frac, core_kappa, zipf_a, rng):
    """Unit vectors with tunable density skew.  core_frac of the mass sits in a
    von Mises-Fisher-ish concentrated core (kappa), the rest is uniform.
    zipf_a > 0 additionally makes a few atoms dominate the sampling weight."""
    n_core = int(round(core_frac * n))
    X = rng.standard_normal((n, d))
    if n_core > 0:
        mu = rng.standard_normal(d)
        mu /= np.linalg.norm(mu)
        X[:n_core] = core_kappa * mu[None, :] + rng.standard_normal((n_core, d))
    X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-12
    if zipf_a > 0:
        w = 1.0 / np.power(np.arange(1, n + 1), zipf_a)
        rng.shuffle(w)
        w /= w.sum()
    else:
        w = np.full(n, 1.0 / n)
    return X, w


def hub_skew(X, k, rng, sample=4000):
    """Skewness of the k-occurrence count N_k -- the standard hubness measure."""
    n = X.shape[0]
    idx = rng.choice(n, min(sample, n), replace=False)
    S = X[idx]
    sims = S @ X[idx].T
    np.fill_diagonal(sims, -np.inf)
    nn = np.argpartition(-sims, kth=k, axis=1)[:, :k]
    Nk = np.bincount(nn.ravel(), minlength=len(idx)).astype(float)
    s = Nk.std()
    return float(((Nk - Nk.mean()) ** 3).mean() / (s ** 3 + 1e-12))


# ---------------------------------------------------------------- Bell core
def chsh(E):
    """E is a dict {(x,y): corr}; CHSH with the standard sign pattern."""
    return abs(E[(0, 0)] + E[(0, 1)] + E[(1, 0)] - E[(1, 1)])


def outcomes(X, qA, qB, x, y):
    A = np.sign(X @ qA[x])
    B = -np.sign(X @ qB[y])
    A[A == 0] = 1.0
    B[B == 0] = 1.0
    return A, B


def retention(X, q, sharp, mode):
    """Setting-dependent accessibility eta(setting, lambda) in [0,1].
    'rank'  : hubness-flavoured -- closeness to the query direction, so states
              near the query become retrieval hubs FOR THAT CONTEXT.
    'none'  : constant (no contextual dependence).
    """
    if mode == "none":
        return np.ones(X.shape[0])
    s = X @ q
    return 1.0 / (1.0 + np.exp(-sharp * s))          # logistic in query alignment


def exact_contextual_shift(X, w, qA, qB, sharp, mode):
    """EXACT contextual ensemble shift, not a projection proxy.

    rho_xy(lambda) ∝ w(lambda) * etaA(x,lambda) * etaB(y,lambda) over the
    latent atoms, so total variation and I(Lambda;X,Y) are computable in closed
    form.  The earlier 1-D histogram proxy was hopeless in d up to 128 -- it
    underestimates the shift and injects noise, which is exactly the kind of
    bad instrument that would fake a null in D4."""
    if mode == "none":
        return 0.0, 0.0
    P = {}
    for x in (0, 1):
        eA = retention(X, qA[x], sharp, mode)
        for y in (0, 1):
            p = w * eA * retention(X, qB[y], sharp, mode)
            P[(x, y)] = p / p.sum()
    keys = list(P)
    dtv = max(0.5 * np.abs(P[i] - P[j]).sum() for i in keys for j in keys)
    # I(Lambda; X,Y) with a uniform prior over the four contexts
    mix = sum(P.values()) / 4.0
    H = lambda p: float(-(p[p > 0] * np.log2(p[p > 0])).sum())
    mi = H(mix) - float(np.mean([H(P[k]) for k in keys]))
    return float(dtv), float(max(mi, 0.0))


def run_phase(X, w, qA, qB, sharp, mode, rng, n_draw):
    """Returns correlations, efficiency, contextual shift, no-signalling,
    and the rejections-as-outcomes re-score."""
    n = X.shape[0]
    draw = rng.choice(n, n_draw, p=w)
    E, E_all, eff, marg = {}, {}, {}, {}
    rho_ctx = {}
    dtv_exact, mi_exact = exact_contextual_shift(X, w, qA, qB, sharp, mode)
    for x in (0, 1):
        for y in (0, 1):
            A, B = outcomes(X, qA, qB, x, y)
            a, b = A[draw], B[draw]
            if mode == "none":
                keep = np.ones(n_draw, dtype=bool)
            else:
                etaA = retention(X, qA[x], sharp, mode)[draw]
                etaB = retention(X, qB[y], sharp, mode)[draw]
                keep = (rng.random(n_draw) < etaA) & (rng.random(n_draw) < etaB)
            eff[(x, y)] = float(keep.mean())
            # D3: rejections counted as physical outcomes (assign +1 -- any
            # fixed local rule works; the point is that no data is discarded)
            a_all = np.where(keep, a, 1.0)
            b_all = np.where(keep, b, 1.0)
            E_all[(x, y)] = float((a_all * b_all).mean())
            if keep.sum() < 50:
                E[(x, y)] = 0.0
                marg[(x, y)] = (0.0, 0.0)
                rho_ctx[(x, y)] = np.zeros(64)
                continue
            E[(x, y)] = float((a[keep] * b[keep]).mean())
            marg[(x, y)] = (float(a[keep].mean()), float(b[keep].mean()))
            # contextual latent distribution, binned by a fixed random direction
            proj = X[draw][keep] @ rho_ctx.setdefault("_axis",
                                                      _axis(X.shape[1], rng))
            h, _ = np.histogram(proj, bins=64, range=(-1, 1), density=False)
            rho_ctx[(x, y)] = h / max(h.sum(), 1)
    keys = [(0, 0), (0, 1), (1, 0), (1, 1)]
    dtv = max(0.5 * np.abs(rho_ctx[i] - rho_ctx[j]).sum()
              for i in keys for j in keys)
    # D2: no-signalling residual -- Alice's marginal must not depend on y
    ns = max(abs(marg[(x, 0)][0] - marg[(x, 1)][0]) for x in (0, 1))
    ns = max(ns, max(abs(marg[(0, y)][1] - marg[(1, y)][1]) for y in (0, 1)))
    return dict(S=chsh(E), S_all_counted=chsh(E_all), E={str(k): v for k, v in E.items()},
                eff_min=min(eff.values()), eff_mean=float(np.mean(list(eff.values()))),
                dtv_proj_proxy=float(dtv),          # kept only to show it is bad
                dtv_contextual=dtv_exact, mi_lambda_xy=mi_exact,
                no_signalling_residual=float(ns))


def _axis(d, rng):
    v = rng.standard_normal(d)
    return v / np.linalg.norm(v)


def chsh_queries(d, rng, theta=np.pi / 4):
    """Two settings per side in a shared plane at the CHSH-optimal-ish angles."""
    e1 = rng.standard_normal(d)
    e1 /= np.linalg.norm(e1)
    e2 = rng.standard_normal(d)
    e2 -= (e2 @ e1) * e1
    e2 /= np.linalg.norm(e2)
    ang = lambda t: np.cos(t) * e1 + np.sin(t) * e2
    qA = {0: ang(0.0), 1: ang(np.pi / 2)}
    qB = {0: ang(theta), 1: ang(-theta)}
    return qA, qB


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=120000)
    ap.add_argument("--draw", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=20260816)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    t0 = time.time()
    print("Hubness-Bell simulator  seed=%d  n_latent=%d  n_draw=%d"
          % (a.seed, a.n, a.draw), flush=True)
    print("PHASE 1 is a falsification net: S<=2 is a theorem, not a finding.\n",
          flush=True)

    grid = []
    for d in (3, 8, 32, 128):
        for core_frac, core_kappa in ((0.0, 0.0), (0.02, 6.0), (0.20, 3.0)):
            for zipf_a in (0.0, 1.2):
                grid.append(dict(d=d, core_frac=core_frac, core_kappa=core_kappa,
                                 zipf_a=zipf_a))

    p1, p2 = [], []
    for g in grid:
        X, w = make_latents(a.n, g["d"], g["core_frac"], g["core_kappa"],
                            g["zipf_a"], rng)
        hs = hub_skew(X, 10, rng)
        qA, qB = chsh_queries(g["d"], rng)
        r1 = run_phase(X, w, qA, qB, 0.0, "none", rng, a.draw)
        r1.update(g, hub_skew=hs, phase=1)
        p1.append(r1)
        # sharpness swept well past the point of diminishing efficiency: if the
        # model is not structurally Tsirelson-bounded, extreme retention
        # contrast is where it should break through 2*sqrt(2).
        for sharp in (2.0, 6.0, 12.0, 25.0, 60.0, 150.0, 400.0):
            r2 = run_phase(X, w, qA, qB, sharp, "rank", rng, a.draw)
            r2.update(g, hub_skew=hs, phase=2, sharp=sharp)
            p2.append(r2)
        print(f"  d={g['d']:3d} core={g['core_frac']:.2f} zipf={g['zipf_a']:.1f} "
              f"hub_skew={hs:6.2f} | P1 S={r1['S']:.4f} | "
              f"P2 S={[round(x['S'],3) for x in p2[-4:]]}", flush=True)

    s1 = np.array([r["S"] for r in p1])
    viol1 = int((s1 > 2.0 + 5e-3).sum())
    s2 = np.array([r["S"] for r in p2])
    dtv2 = np.array([r["dtv_contextual"] for r in p2])
    hub2 = np.array([r["hub_skew"] for r in p2])
    sall = np.array([r["S_all_counted"] for r in p2])
    nsr = np.array([r["no_signalling_residual"] for r in p2])

    def pcorr(u, v, z):
        """partial correlation of u,v controlling for z"""
        def resid(y, x):
            A = np.vstack([x, np.ones_like(x)]).T
            return y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
        ru, rv = resid(u, z), resid(v, z)
        return float(np.corrcoef(ru, rv)[0, 1])

    excess = s2 - 2.0
    r_dtv = float(np.corrcoef(excess, dtv2)[0, 1])
    r_hub = float(np.corrcoef(excess, hub2)[0, 1])
    pr_dtv = pcorr(excess, dtv2, hub2)     # shift, controlling for hubness
    pr_hub = pcorr(excess, hub2, dtv2)     # hubness, controlling for shift
    bound_ok = int((s2 <= 2.0 + 8.0 * dtv2 + 1e-6).sum())

    verdict = dict(
        P1_net_holds=bool(viol1 == 0),                       # must be True or code is wrong
        P2_exceeds_two=bool((s2 > 2.0 + 5e-3).any()),
        D1_exceeds_tsirelson=bool((s2 > TSIRELSON + 5e-3).any()),
        D2_signals=bool((nsr > 0.02).any()),
        D3_violation_survives_counting_rejections=bool((sall > 2.0 + 5e-3).any()),
        D4_shift_beats_hubness=bool(abs(pr_dtv) > abs(pr_hub)),
        bound_S_le_2_plus_8dtv_holds=bool(bound_ok == len(s2)),
    )
    result = dict(
        note="Phase 1 is a falsification net (S<=2 is a theorem). The finding, if "
             "any, is the dissociation in D4 plus the diagnostics D1-D3.",
        seed=a.seed, n_latent=a.n, n_draw=a.draw, tsirelson=TSIRELSON,
        phase1=p1, phase2=p2,
        phase1_max_S=float(s1.max()), phase1_violations=viol1,
        phase2_max_S=float(s2.max()), phase2_max_S_all_counted=float(sall.max()),
        max_no_signalling_residual=float(nsr.max()),
        corr_excess_vs_dtv=r_dtv, corr_excess_vs_hubskew=r_hub,
        partial_excess_dtv_given_hub=pr_dtv, partial_excess_hub_given_dtv=pr_hub,
        loose_bound_satisfied_frac=bound_ok / len(s2),
        verdict=verdict, seconds=round(time.time() - t0, 1))

    print(f"\nPHASE 1 (net): max S = {s1.max():.5f}  violations = {viol1}  "
          f"(any violation here means the SIMULATOR is broken)")
    print(f"PHASE 2: max S = {s2.max():.4f}   Tsirelson = {TSIRELSON:.4f}   "
          f"algebraic max = 4")
    print(f"  exceeds Tsirelson: {verdict['D1_exceeds_tsirelson']}  "
          f"-> model {'is NOT' if verdict['D1_exceeds_tsirelson'] else 'is'} "
          f"quantum-bounded")
    print(f"  max no-signalling residual = {nsr.max():.4f}  "
          f"signals: {verdict['D2_signals']}")
    print(f"  counting rejections as outcomes: max S = {sall.max():.4f}  "
          f"survives: {verdict['D3_violation_survives_counting_rejections']}")
    print(f"  corr(S-2, contextual DTV) = {r_dtv:+.3f}   "
          f"corr(S-2, hub skew) = {r_hub:+.3f}")
    print(f"  PARTIAL: DTV|hub = {pr_dtv:+.3f}   hub|DTV = {pr_hub:+.3f}  "
          f"-> primitive is {'CONTEXTUAL SHIFT' if verdict['D4_shift_beats_hubness'] else 'HUBNESS'}")
    print(f"  loose bound S<=2+8*DTV held in {bound_ok}/{len(s2)} configs")
    print("===HBELL-JSON===")
    print(json.dumps(result, indent=1, default=float))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
