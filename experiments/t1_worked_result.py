#!/usr/bin/env python
"""T1 worked result: learn a consumer's read operator, pay for the probing, serve it,
and bound the downstream loss against the rate-leakage-distortion (RLD) frontier.

Instrument for the registration drafted in drafts/T1-WORKED-RESULT-REGISTRATION-DRAFT.md
(to be sealed as GO-P-2026-NNN). Theory: paper/t1-learn-then-serve (Lemma 1, Theorem 2).
Solver: paper/tit-stationary/spectral_core.py, one block, which is the memoryless Gaussian
vector setting of RLD I: whitened error covariance 0 < X <= I, rate -1/2 log2 det X,
leakage I(T; Xhat | S), distortion tr(Qt X) = tr(Q Delta).

MODES
  --smoke
      Runs the smoke instance the registration names (p = 3, Sigma = I, beta = 0.1, with
      its own seeds). It is a different instance from the registered one and produces no
      governed number. This is the only mode that may run before the seal.
  --governed --prereg prereg/GO-P-2026-NNN-....md [--verify-only]
      Runs the registered instance. It refuses unless all of these hold:
        - the prereg file is tracked by git and unmodified against HEAD;
        - it says `status: SEALED`;
        - its sha256 verifies by the rule of scripts/seal.py;
        - its `governs:` line names this script;
        - this script is tracked by git and unmodified against HEAD.
      --verify-only runs these checks and exits without measuring.

WHAT IS MEASURED (per arm, probe count m, seed)
  Probing. m points x_i ~ pi = N(0, Sigma). The Jacobian at each point is taken by central
  differences, which costs 2p consumer queries. Then Qhat = mean_i J^T G J.
  H1. Relative error ||Q^{-1/2} Qhat Q^{-1/2} - I||_2 against eps_m = nu (sqrt(2L/m) +
      2L/(3m)), with L = ln(2p/delta) and nu = max(nu-, nu+) known in advance. For arm L,
      nu = 0, so the bar is exact recovery to tol_L.
  H2. On the seeds where the H1 event holds, the Gaussian test channel built for Qhat at
      Dhat = D (1 - eps_m) / (1 + nu+), at weight alpha. Its Monte Carlo consumer loss
      must be at most D (1 + h2_rel) + h2_se * SE.
  H3. On the same seeds, its weighted cost alpha R + (1 - alpha) L must be at most
      V_Q(alpha, D / (1 - nu-)) + tau + h3_tol, with
      tau = (p/2) log2[(1 + nu+)(1 + eps_m) / ((1 - nu-)(1 - eps_m))].
  H4. At alpha = 1 and matched rate R_h4, compare the consumer quadratic distortion
      tr(Q Delta) of the design for Qhat against the reconstruction design (water-filling
      on Sigma). The reduction must be at least half the closed-form reduction for the
      true Q, in at least h4_min seeds per cell.
  Control (shuffled consumer). The design for P Qhat P^T, with P reversing the coordinates,
      must FAIL the H4 criterion in every cell.
  Arm B (softmax read-out). It fails (A1), so there are no bars. The arm applies the
      recipe with plug-in Dhat = D and reports.
  Arm R (the real Llama attention-score consumer) is NOT implemented here. It is optional
      in the registration, needs the owner's GPU go-ahead, and would be a separate
      instrument.

SELF-CHECKS (instrument errors, not bars). They run in both modes:
  SC1. The rate-R water-filling matches the series' solver at alpha = 1.
  SC2. The held-out sandwich ratios lie inside the a priori (nu-, nu+) for arms L and S.
  SC3. The closed form of Q for arm S matches a Monte Carlo average of the analytic
      J^T G J.

Deterministic: every random draw comes from numpy default_rng seeded by
[base_seed, arm code, round(1e4 beta), m, seed index, purpose, ...]. Numpy only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "paper" / "tit-stationary"))
import spectral_core as sc  # noqa: E402

SCRIPT_REL = "experiments/t1_worked_result.py"
VERSION = "1.0"

# ----------------------------------------------------------------------------- instances
GOVERNED = dict(
    name="governed",
    p=2, Sigma=[2.0, 0.5],              # T ~ N(0, diag(Sigma))
    G=[4.0, 1.0],                       # output metric of arms L and S (diagonal)
    betas=[0.05, 0.2],                  # arm S: C(x) = x + beta sin x componentwise
    H=[[1.0, 0.5]], SU=[[1.0]],         # holder S = H T + U, U ~ N(0, SU)
    alphas=[0.0, 0.5, 1.0],
    D_frac=0.3,                         # D = D_frac * tr(Q Sigma)
    delta=0.1,
    ms=[8, 32, 128, 512], h4_ms=[32, 128, 512],
    n_seeds=20, h1_min=14, h4_min=18,
    n_mc=200_000, h2_rel=0.005, h2_se=4.0, h3_tol=1e-6, tol_L=1e-6,
    R_h4=2.0, fd_step=1e-4, n_pairs=10_000, n_Qmc=1_000_000,
    base_seed=20261117,
    B_k=3, B_W_seed=20261117,           # arm B: softmax(W x), W k x p, unit spectral norm, G = I_k
    K_serve=1_000_000,
)

SMOKE = dict(
    name="smoke",
    p=3, Sigma=[1.0, 1.0, 1.0],
    G=[3.0, 2.0, 1.0],
    betas=[0.1],
    H=[[1.0, 0.5, 0.25]], SU=[[1.0]],
    alphas=[0.0, 0.5, 1.0],
    D_frac=0.3,
    delta=0.1,
    ms=[8, 32], h4_ms=[32],
    n_seeds=5, h1_min=4, h4_min=4,
    n_mc=20_000, h2_rel=0.005, h2_se=4.0, h3_tol=1e-6, tol_L=1e-6,
    R_h4=2.0, fd_step=1e-4, n_pairs=2_000, n_Qmc=200_000,
    base_seed=7,
    B_k=4, B_W_seed=7,
    K_serve=1_000_000,
)

ARM_CODE = {"L": 1, "S": 2, "B": 3}


# ----------------------------------------------------------------------------- linear algebra
def sym(A):
    return (A + A.T) / 2


def msqrt(A):
    w, V = np.linalg.eigh(sym(A))
    return (V * np.sqrt(np.clip(w, 0, None))) @ V.T


def minv_sqrt(A):
    w, V = np.linalg.eigh(sym(A))
    return (V / np.sqrt(w)) @ V.T


def rel_err(Qh, Q):
    Mi = minv_sqrt(Q)
    return float(np.linalg.norm(sym(Mi @ Qh @ Mi) - np.eye(len(Q)), 2))


def rng_for(inst, arm, beta, *rest):
    return np.random.default_rng([inst["base_seed"], ARM_CODE[arm], int(round(1e4 * beta)), *rest])


# ----------------------------------------------------------------------------- consumers
def q_sin(s2, beta):
    """E (1 + beta cos X)^2 for X ~ N(0, s2)."""
    return 1 + 2 * beta * np.exp(-s2 / 2) + (beta ** 2 / 2) * (1 + np.exp(-2 * s2))


def softmax(Z):
    Z = Z - Z.max(axis=1, keepdims=True)
    E = np.exp(Z)
    return E / E.sum(axis=1, keepdims=True)


class Arm:
    """kind 'L' or 'S': C(x) = x + beta sin x (beta = 0 for L), G diagonal, Q in closed form,
    (nu-, nu+) exact a priori. kind 'B': C(x) = softmax(W x), G = I, Q by Monte Carlo, no nu."""

    def __init__(self, kind, beta, inst):
        self.kind, self.beta, self.inst = kind, beta, inst
        p = inst["p"]
        s2 = np.array(inst["Sigma"], float)
        self.label = "L" if kind == "L" else (f"S(beta={beta})" if kind == "S" else "B")
        if kind in ("L", "S"):
            b = beta
            self.G = np.diag(np.array(inst["G"], float))
            self.f = lambda X, b=b: X + b * np.sin(X)
            qs = q_sin(s2, b)
            # G and Sigma diagonal: E[J^T G J] = G diag(E (1 + b cos X_i)^2)
            self.Q = self.G @ np.diag(qs)
            # mean value theorem: each coordinate's difference quotient lies in [1 - b, 1 + b]
            self.nu_minus = float(1 - np.min((1 - b) ** 2 / qs))
            self.nu_plus = float(np.max((1 + b) ** 2 / qs) - 1)
            self.Q_se = 0.0
        else:
            k = inst["B_k"]
            W = np.random.default_rng(inst["B_W_seed"]).standard_normal((k, p))
            self.W = W / np.linalg.norm(W, 2)
            self.G = np.eye(k)
            self.f = lambda X: softmax(X @ self.W.T)
            self.Q, self.Q_se = self._mc_Q_softmax(np.random.default_rng([inst["base_seed"], 3, 0, 0, 0, 6]))
            self.nu_minus = self.nu_plus = None

    def jac_analytic(self, X):
        if self.kind in ("L", "S"):
            d = 1 + self.beta * np.cos(X)                       # n x p
            return np.einsum("ni,ij->nij", d, np.eye(X.shape[1]))
        s = self.f(X)                                           # n x k
        A = np.einsum("ni,ij->nij", s, np.eye(s.shape[1])) - np.einsum("ni,nj->nij", s, s)
        return A @ self.W                                       # n x k x p

    def read_metrics(self, J):
        return np.einsum("nkp,kl,nlq->npq", J, self.G, J)

    def _mc_Q_softmax(self, rng):
        n, p = self.inst["n_Qmc"], self.inst["p"]
        S12 = np.diag(np.sqrt(self.inst["Sigma"]))
        acc, acc2, done = np.zeros((p, p)), np.zeros((p, p)), 0
        while done < n:
            b = min(100_000, n - done)
            P = self.read_metrics(self.jac_analytic(rng.standard_normal((b, p)) @ S12))
            acc += P.sum(0)
            acc2 += (P ** 2).sum(0)
            done += b
        mean = acc / n
        se = np.sqrt(np.maximum(acc2 / n - mean ** 2, 0) / n)
        return sym(mean), float(np.max(se))

    def loss(self, Xa, Xb):
        d = self.f(Xa) - self.f(Xb)
        return np.einsum("nk,kl,nl->n", d, self.G, d)


def fd_Qhat(arm, X, h):
    """Mean of J^T G J over the probe points, Jacobians by central differences (2p queries each)."""
    n, p = X.shape
    k = arm.G.shape[0]
    J = np.empty((n, k, p))
    for j in range(p):
        E = np.zeros(p)
        E[j] = h
        J[:, :, j] = (arm.f(X + E) - arm.f(X - E)) / (2 * h)
    return sym(arm.read_metrics(J).mean(0))


# ----------------------------------------------------------------------------- coding side
class Coder:
    def __init__(self, inst):
        self.Sig = np.diag(np.array(inst["Sigma"], float))
        self.S12 = msqrt(self.Sig)
        self.Ht = np.array(inst["H"], float) @ self.S12
        self.SU = np.array(inst["SU"], float)
        self.p = inst["p"]

    def design(self, W, alpha, D):
        """Frontier point of the series' solver for weight W at distortion D (one block)."""
        Qt = sym(self.S12 @ W @ self.S12)
        r = sc.solve([(Qt, self.Ht, self.SU)], [1.0], alpha, D)
        X = sym(r["X"][0])
        return dict(Delta=sym(self.S12 @ X @ self.S12), X=X, R=r["R"], L=r["L"], cost=r["cost"])

    def wf_rate(self, W, R):
        """Rate-only design (alpha = 1) for weight W at exactly R bits: reverse water-filling
        on the whitened weight. Returns the error covariance Delta and the whitened X."""
        Qt = sym(self.S12 @ W @ self.S12)
        w, U = np.linalg.eigh(Qt)
        o = np.argsort(w)[::-1]
        w, U = w[o], U[:, o]
        for k in range(1, self.p + 1):
            th = 2.0 ** ((np.sum(np.log2(w[:k])) - 2 * R) / k)
            if w[k - 1] > th and (k == self.p or w[k] <= th):
                break
        X = sym((U * np.minimum(1.0, th / w)) @ U.T)
        return sym(self.S12 @ X @ self.S12), X

    def sample_N(self, rng, n, C):
        return rng.standard_normal((n, self.p)) @ msqrt(C)

    def mc_loss(self, arm, Delta, n, rng):
        """Gaussian test channel (backward form): Xhat ~ N(0, Sigma - Delta), T = Xhat + Z,
        Z ~ N(0, Delta) independent. Returns the mean consumer loss and its standard error."""
        Xh = self.sample_N(rng, n, self.Sig - Delta)
        T = Xh + self.sample_N(rng, n, Delta)
        vals = arm.loss(Xh, T)
        return float(vals.mean()), float(vals.std(ddof=1) / np.sqrt(n))


# ----------------------------------------------------------------------------- the run
def eps_m(nu, m, p, delta):
    L = np.log(2 * p / delta)
    return float(nu * (np.sqrt(2 * L / m) + 2 * L / (3 * m)))


def run_arm(arm, inst, coder):
    p, alphas = inst["p"], inst["alphas"]
    Q = arm.Q
    Dmax = float(np.trace(Q @ coder.Sig))
    D = inst["D_frac"] * Dmax
    bar = arm.kind in ("L", "S")
    rec = dict(arm=arm.label, Q=Q.tolist(), Q_mc_se=arm.Q_se, D_max=Dmax, D=D,
               nu_minus=arm.nu_minus, nu_plus=arm.nu_plus)
    P = np.eye(p)[::-1]

    # held-out sandwich ratios: 'pairs' of independent draws from pi (reported, never a bar)
    rng = rng_for(inst, arm.kind, arm.beta, 0, 0, 4)
    xa = coder.sample_N(rng, inst["n_pairs"], coder.Sig)
    xb = coder.sample_N(rng, inst["n_pairs"], coder.Sig)
    d = xb - xa
    r = arm.loss(xb, xa) / np.einsum("ni,ij,nj->n", d, Q, d)
    rec["nu_hat_minus"], rec["nu_hat_plus"] = float(1 - r.min()), float(r.max() - 1)

    # reference designs for the true Q (no bars): outer bound of Thm 2(a) and the full-budget design
    nu = max(arm.nu_minus, arm.nu_plus) if bar else None
    ref = {}
    for ai, a in enumerate(alphas):
        full = coder.design(Q, a, D)
        mcl, mcse = coder.mc_loss(arm, full["Delta"], inst["n_mc"], rng_for(inst, arm.kind, arm.beta, 0, 0, 5, ai))
        ref[a] = dict(V_full=full["cost"], full_design_loss=mcl, full_design_loss_se=mcse)
        if bar:
            ref[a]["V_outer"] = coder.design(Q, a, D / (1 - arm.nu_minus))["cost"]
    rec["reference"] = {str(a): v for a, v in ref.items()}

    # H4 closed forms for the true Q
    Delta_rec, _ = coder.wf_rate(np.eye(p), inst["R_h4"])
    Delta_Q, _ = coder.wf_rate(Q, inst["R_h4"])
    d_rec, d_Q = float(np.trace(Q @ Delta_rec)), float(np.trace(Q @ Delta_Q))
    red_true = 1 - d_Q / d_rec
    rec["h4_closed_form"] = dict(R=inst["R_h4"], d_rec=d_rec, d_trueQ=d_Q, reduction=red_true,
                                 floor=red_true / 2 if bar else None)
    if not bar:  # arm B: true consumer loss at the matched rate, by Monte Carlo
        mrec = coder.mc_loss(arm, Delta_rec, inst["n_mc"], rng_for(inst, "B", 0, 0, 0, 7, 0))
        mQ = coder.mc_loss(arm, Delta_Q, inst["n_mc"], rng_for(inst, "B", 0, 0, 0, 7, 1))
        rec["h4_closed_form"].update(loss_rec_mc=mrec, loss_trueQ_mc=mQ)

    cells = {}
    for m in inst["ms"]:
        e = eps_m(nu, m, p, inst["delta"]) if bar else None
        tau = (p / 2) * np.log2((1 + arm.nu_plus) * (1 + e) / ((1 - arm.nu_minus) * (1 - e))) if bar else None
        Dhat = D * (1 - e) / (1 + arm.nu_plus) if bar else D
        cell = dict(m=m, eps_m=e, tau=tau, tau_looseness=(p / 2) * np.log2((1 + arm.nu_plus) / (1 - arm.nu_minus)) if bar else None,
                    D_hat=Dhat, queries=2 * p * m, probe_overhead_per_symbol=2 * p * m / inst["K_serve"],
                    rel_err=[], h1_event=[], per_alpha={str(a): dict(loss=[], se=[], loss_over_D=[], h2_ok=[], cost=[],
                                                                       h3_bound=None, h3_ok=[], gap_to_full_design=[])
                                                         for a in alphas},
                    h4=dict(reduction=[], ok=[], shuffled_reduction=[], shuffled_ok=[], loss_Qhat_mc=[], loss_rec_mc=[])
                    if m in inst["h4_ms"] else None)
        if bar:
            for a in alphas:
                cell["per_alpha"][str(a)]["h3_bound"] = ref[a]["V_outer"] + tau
        for s in range(inst["n_seeds"]):
            X = coder.sample_N(rng_for(inst, arm.kind, arm.beta, m, s, 1), m, coder.Sig)
            Qh = fd_Qhat(arm, X, inst["fd_step"])
            err = rel_err(Qh, Q)
            ev = (err <= (e if nu > 0 else inst["tol_L"])) if bar else None
            cell["rel_err"].append(err)
            cell["h1_event"].append(ev)
            for ai, a in enumerate(alphas):
                pa = cell["per_alpha"][str(a)]
                if bar and not ev:
                    for key in ("loss", "se", "loss_over_D", "h2_ok", "cost", "h3_ok", "gap_to_full_design"):
                        pa[key].append(None)
                    continue
                des = coder.design(Qh, a, Dhat)
                ml, se = coder.mc_loss(arm, des["Delta"], inst["n_mc"], rng_for(inst, arm.kind, arm.beta, m, s, 2, ai))
                pa["loss"].append(ml)
                pa["se"].append(se)
                pa["loss_over_D"].append(ml / D)
                pa["cost"].append(des["cost"])
                pa["gap_to_full_design"].append(des["cost"] - ref[a]["V_full"])
                pa["h2_ok"].append(bool(ml <= D * (1 + inst["h2_rel"]) + inst["h2_se"] * se) if bar else None)
                pa["h3_ok"].append(bool(des["cost"] <= pa["h3_bound"] + inst["h3_tol"]) if bar else None)
            if cell["h4"] is not None:
                h4 = cell["h4"]
                Dl, _ = coder.wf_rate(Qh, inst["R_h4"])
                Ds, _ = coder.wf_rate(sym(P @ Qh @ P.T), inst["R_h4"])
                red = 1 - float(np.trace(Q @ Dl)) / d_rec
                red_s = 1 - float(np.trace(Q @ Ds)) / d_rec
                h4["reduction"].append(red)
                h4["shuffled_reduction"].append(red_s)
                h4["ok"].append(bool(red >= red_true / 2) if bar else None)
                h4["shuffled_ok"].append(bool(red_s >= red_true / 2) if bar else None)
                if not bar:
                    h4["loss_Qhat_mc"].append(coder.mc_loss(arm, Dl, inst["n_mc"], rng_for(inst, "B", 0, m, s, 3, 0)))
                    h4["loss_rec_mc"].append(coder.mc_loss(arm, Delta_rec, inst["n_mc"], rng_for(inst, "B", 0, m, s, 3, 1)))
        if bar:
            cell["h1_count"] = int(sum(cell["h1_event"]))
            cell["h1_pass"] = cell["h1_count"] >= inst["h1_min"]
            if cell["h4"] is not None:
                cell["h4"]["count"] = int(sum(cell["h4"]["ok"]))
                cell["h4"]["pass"] = cell["h4"]["count"] >= inst["h4_min"]
                cell["h4"]["shuffled_count"] = int(sum(cell["h4"]["shuffled_ok"]))
                cell["h4"]["shuffled_fails_as_required"] = cell["h4"]["shuffled_count"] < inst["h4_min"]
        cells[str(m)] = cell
    rec["cells"] = cells
    return rec


def self_checks(arms, inst, coder):
    out = {}
    # SC1: rate-R water-filling == series solver at alpha = 1
    worst_R, worst_X = 0.0, 0.0
    for arm in arms:
        Delta, X = coder.wf_rate(arm.Q, inst["R_h4"])
        r = coder.design(arm.Q, 1.0, float(np.trace(arm.Q @ Delta)))
        worst_R = max(worst_R, abs(r["R"] - inst["R_h4"]))
        worst_X = max(worst_X, float(np.linalg.norm(r["X"] - X)))
    out["SC1_waterfilling_vs_solver"] = dict(max_rate_diff=worst_R, max_X_diff=worst_X, ok=worst_R < 1e-6 and worst_X < 1e-5)
    # SC2 is filled from the arm records (held-out ratios inside the a priori bounds)
    # SC3: closed-form Q (arm S) vs Monte Carlo of the analytic J^T G J
    rows = []
    for arm in arms:
        if arm.kind != "S":
            continue
        rng = rng_for(inst, "S", arm.beta, 0, 0, 8)
        P = arm.read_metrics(arm.jac_analytic(coder.sample_N(rng, inst["n_Qmc"], coder.Sig)))
        mean, se = P.mean(0), P.std(0, ddof=1) / np.sqrt(len(P))
        z = float(np.max(np.abs(mean - arm.Q) / np.maximum(se, 1e-300) * (se > 0)))
        rows.append(dict(arm=arm.label, max_abs_z=z))
    # generic: q_sin at variances away from any instance's
    gen = []
    rng = np.random.default_rng([inst["base_seed"], 99])
    for s2 in (0.7, 3.0):
        x = rng.standard_normal(400_000) * np.sqrt(s2)
        v = (1 + 0.1 * np.cos(x)) ** 2
        gen.append(abs(v.mean() - q_sin(s2, 0.1)) / (v.std(ddof=1) / np.sqrt(len(v))))
    out["SC3_closed_form_Q"] = dict(instance=rows, generic_max_abs_z=float(max(gen)),
                                   ok=bool(all(r["max_abs_z"] < 5 for r in rows) and max(gen) < 5))
    return out


def verdict(recs, checks, inst):
    bar = [r for r in recs if r["nu_minus"] is not None]
    h1 = all(c["h1_pass"] for r in bar for c in r["cells"].values())
    h2v = [ok for r in bar for c in r["cells"].values() for pa in c["per_alpha"].values() for ok in pa["h2_ok"] if ok is not None]
    h3v = [ok for r in bar for c in r["cells"].values() for pa in c["per_alpha"].values() for ok in pa["h3_ok"] if ok is not None]
    h4c = [c["h4"] for r in bar for c in r["cells"].values() if c["h4"] is not None]
    sc2 = all(r["nu_hat_minus"] <= r["nu_minus"] + 1e-9 and r["nu_hat_plus"] <= r["nu_plus"] + 1e-9 for r in bar)
    checks["SC2_sandwich_contains_heldout"] = dict(ok=sc2, rows=[dict(arm=r["arm"], nu_hat_minus=r["nu_hat_minus"],
                                                                     nu_hat_plus=r["nu_hat_plus"]) for r in bar])
    instrument_ok = all(v["ok"] for v in checks.values())
    v = dict(
        H1=h1,
        H2=all(h2v), H2_tests=len(h2v), H2_failures=int(len(h2v) - sum(h2v)),
        H3=all(h3v), H3_tests=len(h3v), H3_failures=int(len(h3v) - sum(h3v)),
        H4=all(c["pass"] for c in h4c),
        control_shuffled=all(c["shuffled_fails_as_required"] for c in h4c),
        control_armL_exact=all(all(c["h1_event"]) for r in bar if r["arm"] == "L" for c in r["cells"].values()),
        instrument_self_checks=instrument_ok,
    )
    keys = ("H1", "H2", "H3", "H4", "control_shuffled", "control_armL_exact")
    v["all_pass"] = instrument_ok and all(v[k] for k in keys)
    v["summary"] = "INSTRUMENT ERROR (self-check failed)" if not instrument_ok else (
        "ALL PASS" if v["all_pass"] else "MISS: " + ", ".join(k for k in keys if not v[k]))
    return v


# ----------------------------------------------------------------------------- seal guard
def _git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)


def check_governed(prereg):
    pr = Path(prereg).resolve()
    if not pr.is_file() or ROOT not in pr.parents:
        raise SystemExit(f"refusing the governed run: {prereg} is not a file inside {ROOT}")
    rel = pr.relative_to(ROOT).as_posix()
    text = pr.read_text(encoding="utf-8")          # same normalization as scripts/seal.py
    problems = []
    if not re.search(r"^status:\s*SEALED", text, re.M):
        problems.append("status is not SEALED")
    if not re.search(r"^governs:.*" + re.escape(SCRIPT_REL), text, re.M):
        problems.append(f"`governs:` does not name {SCRIPT_REL}")
    mh = re.search(r"hash:\s*sha256:(\S*)", text)
    digest = hashlib.sha256(re.sub(r"hash:\s*sha256:\S*", "hash: sha256:", text).encode("utf-8")).hexdigest()
    if not mh or mh.group(1) != digest:
        problems.append("sha256 does not verify")
    for path in (rel, SCRIPT_REL):
        if _git("ls-files", "--error-unmatch", path).returncode != 0:
            problems.append(f"{path} is not tracked by git")
        elif _git("diff", "--quiet", "HEAD", "--", path).returncode != 0:
            problems.append(f"{path} differs from HEAD")
    if problems:
        raise SystemExit("refusing the governed run: " + "; ".join(problems))
    return dict(path=rel, sha256=digest)


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--smoke", action="store_true", help="run the smoke instance (not governed)")
    g.add_argument("--governed", action="store_true", help="run the registered instance (needs --prereg)")
    ap.add_argument("--prereg", help="the sealed prereg file that governs this run")
    ap.add_argument("--out", help="also write the JSON record here")
    ap.add_argument("--verify-only", action="store_true",
                    help="with --governed: check the seal and exit without measuring")
    a = ap.parse_args()

    if a.governed:
        if not a.prereg:
            raise SystemExit("--governed needs --prereg")
        seal = check_governed(a.prereg)
        if a.verify_only:
            print(f"seal verified, nothing measured: {seal}")
            return
        inst = GOVERNED
    else:
        seal, inst = None, SMOKE

    t0 = time.time()
    coder = Coder(inst)
    arms = [Arm("L", 0.0, inst)] + [Arm("S", b, inst) for b in inst["betas"]] + [Arm("B", 0.0, inst)]
    checks = self_checks(arms, inst, coder)
    recs = [run_arm(arm, inst, coder) for arm in arms]
    v = verdict(recs, checks, inst)
    head = _git("rev-parse", "HEAD").stdout.strip()
    dirty = _git("diff", "--quiet", "HEAD", "--", SCRIPT_REL).returncode != 0
    out = dict(instrument=SCRIPT_REL, version=VERSION, mode=inst["name"],
               note=None if a.governed else "SMOKE: instance differs from the registration; not a governed result",
               git_head=head, script_differs_from_head=dirty, prereg=seal,
               arm_R="not implemented (optional in the registration; needs the owner's GPU go-ahead)",
               instance=inst, self_checks=checks, arms=recs, verdict=v,
               wall_seconds=round(time.time() - t0, 1))

    for r in recs:
        print(f"[{inst['name']}] arm {r['arm']}: D={r['D']:.4f} nu-={r['nu_minus']} nu+={r['nu_plus']} "
              f"nu_hat=({r['nu_hat_minus']:.3f},{r['nu_hat_plus']:.3f})", file=sys.stderr)
        for c in r["cells"].values():
            line = f"   m={c['m']:4d} rel_err median {np.median(c['rel_err']):.3g}"
            if "h1_count" in c:
                line += f"  H1 {c['h1_count']}/{inst['n_seeds']}"
            if c["h4"] is not None and "count" in c["h4"]:
                line += f"  H4 {c['h4']['count']}/{inst['n_seeds']} (shuffled {c['h4']['shuffled_count']})"
            print(line, file=sys.stderr)
    print(f"[{inst['name']}] verdict: {v['summary']}  ({out['wall_seconds']} s)", file=sys.stderr)

    payload = json.dumps(out, indent=1, default=float)
    if a.out:
        Path(a.out).write_text(payload, encoding="utf-8")
    print("===T1-JSON===")
    print(payload)
    print("===END===")


if __name__ == "__main__":
    main()
