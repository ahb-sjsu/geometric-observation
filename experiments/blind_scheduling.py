"""GO-P-2026-087 (DRAFT) -- blind recovery -> sensor scheduling (OT-EC Campaign 3 flagship).

Query-only recovery of a downstream consumer's read operator, composed with the
Kalman covariance as tr(P_C Sigma), driving greedy sensor scheduling, judged on
the HELD-OUT actual consumer at matched budgets WITH PROBE COST CHARGED.

Two consumer arms:
  P (positive control, analytic)  z = Lx, rank-3: the optimal scheduling weight
                                  is known exactly (P_C = L'L). The blind
                                  pipeline must RECOVER/MATCH it, not beat it.
  N (non-analytic, black-box)     frozen low-rank tanh MLP + a smoothed-threshold
                                  scalar consumer. No analytic weight exists;
                                  the blind pipeline must WIN over
                                  consumer-agnostic policies.

Policies (matched sensor-use budget; OT arms are charged lambda_p per probe
query, implemented as prediction-only steps at the start of each rollout):
  ot-blind    greedy V_C with probed P_hat        oracle   greedy with true P_C
  iso-trace   greedy tr(dSigma)                   logdet   greedy information
  random      uniform                             anti     eigen-complement of P_hat
  shuffled    P_hat probed from a permuted-input consumer (control)

Phases:
  --calibrate       internal calibration split; prints the candidate floors to
                    freeze in the prereg seal. No governed claims.
  --governed SEED   single governed run on FRESH systems; evaluates the sealed
                    gates; writes results/GO87-blind-scheduling.json.

DRAFT status: gates below read module-level FROZEN_* constants that are
placeholders until the prereg is sealed; the sealed values must match the
committed prereg YAML byte-for-byte.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")

# ---------------------------------------------------------------- experiment size
D = 12            # state dimension
M_POOL = 30       # candidate sensors
K_BUDGET = 3      # sensor-uses per step
T_STEPS = 60      # rollout length
N_TEST = 24       # held-out rollouts per system per policy
N_SYS_CAL = 8     # calibration systems
N_SYS_GOV = 20    # governed systems
N_PROBE = 40      # probe sample points (each costs 2*D queries, central diff)
LAMBDA_P = 0.002  # sensor-uses charged per consumer query
FD_EPS = 1e-3

# ------------------------------------------- SEALED GATES (frozen 2026-08-18
# from the five disclosed calibration pilots; must match the prereg YAML)
FROZEN_EPS_MATCH = 0.25   # P1 gate: pooled match fraction >= 0.75 (cal: 0.874)
FROZEN_DELTA_N = 0.08     # P2 gate: rel. improvement >= 0.08 (cal: 0.166-0.265)
FROZEN_TR_TOL = 0.05      # P3: relative trace-matching band
FROZEN_Q_ORDER = 0.65     # P3 gate: ordering fraction >= 0.65 (cal: 0.773-0.923,
                          # n_pairs 11-22, prop. SE ~0.09 at n=22)


# ------------------------------------------------------------------------ plant
def make_system(rng):
    A = rng.standard_normal((D, D)) / np.sqrt(D)
    A *= 0.95 / max(abs(np.linalg.eigvals(A)))
    Mq = rng.standard_normal((D, D)) / np.sqrt(D)
    Q = Mq @ Mq.T / D + 0.02 * np.eye(D)
    H = rng.standard_normal((M_POOL, D))
    H /= np.linalg.norm(H, axis=1, keepdims=True)
    r = 10.0 ** rng.uniform(-2, 0, size=M_POOL)
    return A, Q, H, r


def steady_prior(A, Q, iters=400):
    S = Q.copy()
    for _ in range(iters):
        S = A @ S @ A.T + Q
        S = 0.5 * (S + S.T)
        if np.trace(S) > 1e6:
            break
    return S


# -------------------------------------------------------------------- consumers
class LinearConsumer:
    """Arm P: z = Lx. Analytic read operator P_C = L'L (rank 3)."""

    def __init__(self, rng):
        self.L = rng.standard_normal((3, D)) / np.sqrt(D)

    def query(self, x):
        return self.L @ x

    def loss(self, xhat, x):
        d = self.L @ (xhat - x)
        return float(d @ d)

    def true_pc(self):
        return self.L.T @ self.L


class MLPConsumer:
    """Arm N: frozen 2-layer tanh MLP with a planted rank-4 first layer."""

    def __init__(self, rng):
        U = rng.standard_normal((8, 4)) / 2.0
        V = rng.standard_normal((4, D)) / np.sqrt(D)
        self.W1, self.b1 = U @ V, rng.standard_normal(8) * 0.1
        self.W2, self.b2 = rng.standard_normal((2, 8)) / np.sqrt(8), np.zeros(2)

    def query(self, x):
        return self.W2 @ np.tanh(self.W1 @ x + self.b1) + self.b2

    def loss(self, xhat, x):
        d = self.query(xhat) - self.query(x)
        return float(d @ d)

    def true_pc(self):
        return None  # non-analytic by construction (probed oracle used instead)


class ThresholdConsumer:
    """Arm N variant: smoothed scalar threshold (sigmoid link)."""

    def __init__(self, rng, steep=4.0):
        g = rng.standard_normal(D)
        self.g = g / np.linalg.norm(g)
        self.s, self.tau = steep, 0.0

    def query(self, x):
        return np.array([1.0 / (1.0 + np.exp(-self.s * (self.g @ x - self.tau)))])

    def loss(self, xhat, x):
        d = self.query(xhat) - self.query(x)
        return float(d @ d)

    def true_pc(self):
        return None


# -------------------------------------------------------- query-only FD recovery
def probe_read_operator(consumer, S_probe, rng, n_probe=N_PROBE, perm=None):
    """Central-difference Jacobian probing under x ~ N(0, S_probe).
    Returns (P_hat, n_queries). `perm` permutes the consumer's input
    (the shuffled-consumer control)."""
    Lc = np.linalg.cholesky(S_probe + 1e-9 * np.eye(D))
    P = np.zeros((D, D))
    n_queries = 0
    for _ in range(n_probe):
        x0 = Lc @ rng.standard_normal(D)
        J = []
        for i in range(D):
            e = np.zeros(D)
            e[i] = FD_EPS
            xp, xm = x0 + e, x0 - e
            if perm is not None:
                xp, xm = xp[perm], xm[perm]
            J.append((consumer.query(xp) - consumer.query(xm)) / (2 * FD_EPS))
            n_queries += 2
        J = np.array(J).T          # (m_out, D)
        P += J.T @ J
    P /= n_probe
    return 0.5 * (P + P.T), n_queries


# ---------------------------------------------------------------------- policies
def greedy_weighted(P, S, H, r, k):
    """Greedy top-k sensors by V_C = tr(P dSigma) with sequential updates."""
    picks = []
    S = S.copy()
    for _ in range(k):
        num = np.einsum("md,de,me->m", H @ S, P, H @ S)   # h'S P S h per sensor
        den = np.einsum("md,md->m", H @ S, H) + r
        best = int(np.argmax(num / den))
        picks.append(best)
        h = H[best]
        Sh = S @ h
        S = S - np.outer(Sh, Sh) / (h @ Sh + r[best])
        S = 0.5 * (S + S.T)
    return picks


def greedy_logdet(S, H, r, k):
    picks = []
    S = S.copy()
    for _ in range(k):
        gain = np.log1p(np.einsum("md,md->m", H @ S, H) / r)
        best = int(np.argmax(gain))
        picks.append(best)
        h = H[best]
        Sh = S @ h
        S = S - np.outer(Sh, Sh) / (h @ Sh + r[best])
        S = 0.5 * (S + S.T)
    return picks


def anti_operator(P):
    ev, V = np.linalg.eigh(P)
    w = ev.max() - ev + 1e-9 * ev.max()
    return V @ np.diag(w) @ V.T


# ----------------------------------------------------------------------- rollout
def make_noise_bundles(rng, n_test):
    """Common random numbers: every policy replays the SAME realizations, so
    cross-policy gains are policy differences, not noise variance."""
    return [{"x0": rng.standard_normal(D),
             "w": rng.standard_normal((T_STEPS, D)),
             "v": rng.standard_normal((T_STEPS, M_POOL))} for _ in range(n_test)]


def rollout(A, Q, H, r, consumer, select_fn, charged_uses, noise):
    """One rollout: KF with per-step greedy selection; returns (mean consumer
    loss over steps, time-average tr Sigma). Probe charge is taken in SENSOR
    USES: `charged_uses` single sensor-uses are removed (k-1 instead of k) at
    evenly spread steps — never a whole blacked-out step, which would charge
    1 use at the price of many. All randomness comes from the `noise` bundle
    (common random numbers across policies)."""
    S0 = steady_prior(A, Q)
    L0 = np.linalg.cholesky(S0 + 1e-9 * np.eye(D))
    x = L0 @ noise["x0"]                 # x0 ~ prior, belief-consistent
    xhat = np.zeros(D)
    S = S0.copy()
    Lq = np.linalg.cholesky(Q + 1e-12 * np.eye(D))
    reduced = set(np.linspace(0, T_STEPS - 1, min(charged_uses, T_STEPS)).astype(int)) \
        if charged_uses else set()
    loss_sum, tr_sum = 0.0, 0.0
    for t in range(T_STEPS):
        x = A @ x + Lq @ noise["w"][t]
        xhat = A @ xhat
        S = A @ S @ A.T + Q
        S = 0.5 * (S + S.T)
        k_t = K_BUDGET - (1 if t in reduced else 0)
        if k_t > 0:
            for i in select_fn(S)[:k_t]:
                h = H[i]
                y = h @ x + np.sqrt(r[i]) * noise["v"][t, i]
                Sh = S @ h
                kal = Sh / (h @ Sh + r[i])
                xhat = xhat + kal * (y - h @ xhat)
                S = S - np.outer(kal, Sh)
                S = 0.5 * (S + S.T)
        loss_sum += consumer.loss(xhat, x)
        tr_sum += np.trace(S)
    return loss_sum / T_STEPS, tr_sum / T_STEPS


def evaluate_system(sysdef, consumer, rng, probed_pc, oracle_pc, n_queries, noise):
    """All policies on one (system, consumer), all replaying the SAME noise
    bundles (common random numbers). Probe charge -> skip_steps for arms that
    used the probed operator."""
    A, Q, H, r = sysdef
    charge_uses = int(np.ceil(LAMBDA_P * n_queries))   # charge in sensor USES
    P_anti = anti_operator(probed_pc)
    rand_rng = np.random.default_rng(rng.integers(2**31))
    rand_picks = [list(rand_rng.integers(0, M_POOL, size=K_BUDGET)) for _ in range(T_STEPS)]
    policies = {
        "ot-blind": (lambda S: greedy_weighted(probed_pc, S, H, r, K_BUDGET), charge_uses),
        "ot-blind-uncharged": (lambda S: greedy_weighted(probed_pc, S, H, r, K_BUDGET), 0),
        "oracle":   (lambda S: greedy_weighted(oracle_pc, S, H, r, K_BUDGET), 0),
        "iso-trace": (lambda S: greedy_weighted(np.eye(D), S, H, r, K_BUDGET), 0),
        "logdet":   (lambda S: greedy_logdet(S, H, r, K_BUDGET), 0),
        "random":   (lambda S, _c=iter(rand_picks * (N_TEST + 1)): next(_c), 0),
        "anti":     (lambda S: greedy_weighted(P_anti, S, H, r, K_BUDGET), charge_uses),
    }
    out = {}
    for name, (fn, charged) in policies.items():
        losses, traces = [], []
        for nb in noise:
            l, tr = rollout(A, Q, H, r, consumer, fn, charged, nb)
            losses.append(l)
            traces.append(tr)
        out[name] = {"loss": float(np.mean(losses)), "loss_se": float(np.std(losses) / np.sqrt(N_TEST)),
                     "tr": float(np.mean(traces))}
    out["_meta"] = {"n_queries": n_queries, "probe_charge_uses": charge_uses}
    return out


# ------------------------------------------------------------------------ arms
def run_arm(arm, n_sys, seed, with_controls):
    rng = np.random.default_rng(seed)
    per_sys = []
    for s in range(n_sys):
        sysdef = make_system(rng)
        A, Q, H, r = sysdef
        S_probe = steady_prior(A, Q)
        if arm == "P":
            consumer = LinearConsumer(rng)
            oracle_pc = consumer.true_pc()
        else:
            consumer = MLPConsumer(rng) if s % 2 == 0 else ThresholdConsumer(rng)
            # non-analytic: "oracle" = a lavish uncharged probe (upper reference)
            oracle_pc, _ = probe_read_operator(consumer, S_probe, rng, n_probe=8 * N_PROBE)
        probed_pc, n_q = probe_read_operator(consumer, S_probe, rng)
        noise = make_noise_bundles(rng, N_TEST)
        res = evaluate_system(sysdef, consumer, rng, probed_pc, oracle_pc, n_q, noise)
        if with_controls:
            perm = rng.permutation(D)
            shuf_pc, n_qs = probe_read_operator(consumer, S_probe, rng, perm=perm)
            charge = int(np.ceil(LAMBDA_P * n_qs))
            losses = [rollout(A, Q, H, r, consumer,
                              lambda S: greedy_weighted(shuf_pc, S, H, r, K_BUDGET),
                              charge, nb)[0] for nb in noise]
            res["shuffled"] = {"loss": float(np.mean(losses))}
        per_sys.append(res)
    return per_sys


# ------------------------------------------------------------------------ gates
def summarize(per_sys):
    pol = [k for k in per_sys[0] if not k.startswith("_")]
    return {p: float(np.mean([s[p]["loss"] for s in per_sys])) for p in pol}


def p1_match_fraction(per_sys):
    """Arm P: fraction of oracle's improvement over iso-trace captured by
    ot-blind. POOLED ratio (sum of gains / sum of gains) — the per-system
    ratio is reported descriptively but is unstable when a system's oracle
    gain is small."""
    g_ot = sum(s["iso-trace"]["loss"] - s["ot-blind"]["loss"] for s in per_sys)
    g_or = sum(s["iso-trace"]["loss"] - s["oracle"]["loss"] for s in per_sys)
    per = [(s["iso-trace"]["loss"] - s["ot-blind"]["loss"]) /
           max(s["iso-trace"]["loss"] - s["oracle"]["loss"], 1e-12) for s in per_sys]
    return float(g_ot / max(g_or, 1e-12)), [float(f) for f in per]


def p2_improvement(per_sys):
    """Arm N: relative improvement of ot-blind over the best consumer-agnostic
    policy, per system."""
    rel = []
    for s in per_sys:
        agnostic = min(s["iso-trace"]["loss"], s["logdet"]["loss"])
        rel.append((agnostic - s["ot-blind"]["loss"]) / max(agnostic, 1e-12))
    return float(np.mean(rel)), [float(x) for x in rel]


def p3_ordering(per_sys_all):
    """Trace-matched pairs across {iso-trace, logdet, ot-blind, anti}: is the
    consumer-loss ordering predicted by having used P_hat (i.e. ot-blind lower
    than agnostic/anti in matched pairs)?"""
    names = ["iso-trace", "logdet", "ot-blind", "anti"]
    checked = correct = 0
    for s in per_sys_all:
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = s[names[i]], s[names[j]]
                if abs(a["tr"] - b["tr"]) / max(a["tr"], b["tr"]) < FROZEN_TR_TOL:
                    checked += 1
                    # prediction: the arm aligned with P_hat (ot-blind) wins;
                    # anti loses to everything; iso vs logdet -> no prediction
                    pair = {names[i], names[j]}
                    if "ot-blind" in pair:
                        pred_winner = "ot-blind"
                    elif "anti" in pair:
                        pred_winner = names[i] if names[j] == "anti" else names[j]
                    else:
                        checked -= 1
                        continue
                    actual = names[i] if a["loss"] < b["loss"] else names[j]
                    correct += int(actual == pred_winner)
    return (correct / checked if checked else float("nan")), checked


# ------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--governed", type=int, metavar="SEED")
    args = ap.parse_args()

    if args.calibrate:
        seed, n_sys, tag = 20260818, N_SYS_CAL, "CALIBRATION"
    elif args.governed is not None:
        seed, n_sys, tag = args.governed, N_SYS_GOV, "GOVERNED"
    else:
        ap.error("choose --calibrate or --governed SEED")

    print(f"[{tag}] seed={seed} n_sys={n_sys} D={D} pool={M_POOL} k={K_BUDGET} "
          f"T={T_STEPS} n_test={N_TEST} n_probe={N_PROBE} lambda_p={LAMBDA_P}")

    armP = run_arm("P", n_sys, seed, with_controls=True)
    armN = run_arm("N", n_sys, seed + 1, with_controls=True)

    sumP, sumN = summarize(armP), summarize(armN)
    print("\nArm P (positive control) mean losses:", json.dumps(sumP, indent=2))
    print("Arm N (non-analytic) mean losses:", json.dumps(sumN, indent=2))

    m1, fr1 = p1_match_fraction(armP)
    m2, fr2 = p2_improvement(armN)
    q3, n3 = p3_ordering(armP + armN)
    shuf_gap = float(np.mean(
        [s["shuffled"]["loss"] - s["iso-trace"]["loss"] for s in armP + armN if "shuffled" in s]))
    # anti control: pooled per-arm — anti must be the worst informed policy
    anti_worst = all(
        smry["anti"] >= max(smry["iso-trace"], smry["logdet"], smry["ot-blind"]) - 1e-12
        for smry in (sumP, sumN))

    print(f"\nP1 match fraction (arm P, probe-charged): {m1:.3f}  "
          f"(gate: >= {1 - FROZEN_EPS_MATCH:.2f})")
    print(f"P2 relative improvement (arm N, probe-charged): {m2:.3f}  "
          f"(gate: >= {FROZEN_DELTA_N:.2f})")
    print(f"P3 trace-matched ordering: {q3 if q3 == q3 else float('nan'):.3f} "
          f"over {n3} pairs  (gate: >= {FROZEN_Q_ORDER:.2f})")
    p4_charge_cost = float(np.mean(
        [s["ot-blind"]["loss"] - s["ot-blind-uncharged"]["loss"] for s in armP + armN]))
    print(f"controls: shuffled-vs-iso gap {shuf_gap:+.4f} (want ~>= 0); "
          f"anti worst (pooled per arm): {anti_worst}")
    print(f"P4 probe-charge cost (charged minus uncharged ot-blind): {p4_charge_cost:+.4f}")

    if args.calibrate:
        print("\n[CALIBRATION] candidate floors to freeze at seal time:")
        print(f"  eps_match <= {1 - m1:.3f} observed; delta_N <= {m2:.3f} observed; "
              f"q_order <= {q3:.3f} observed")
        print("  Freeze conservative values in the prereg, then run --governed once.")
        return

    gates = {
        "P1_match": m1 >= 1 - FROZEN_EPS_MATCH,
        "P2_improve": m2 >= FROZEN_DELTA_N,
        "P3_ordering": (q3 == q3) and q3 >= FROZEN_Q_ORDER,
        "C_shuffled_no_free_lunch": shuf_gap >= -0.02,
        "C_anti_worst": anti_worst,
    }
    verdict = "ALL PASS" if all(gates.values()) else "FAIL"
    out = {
        "id": "GO-P-2026-087", "seed": seed, "n_sys": n_sys,
        "config": {"D": D, "M_POOL": M_POOL, "K_BUDGET": K_BUDGET, "T_STEPS": T_STEPS,
                   "N_TEST": N_TEST, "N_PROBE": N_PROBE, "LAMBDA_P": LAMBDA_P,
                   "eps_match": FROZEN_EPS_MATCH, "delta_N": FROZEN_DELTA_N,
                   "tr_tol": FROZEN_TR_TOL, "q_order": FROZEN_Q_ORDER},
        "armP": armP, "armN": armN,
        "metrics": {"P1_match_fraction": m1, "P1_per_system": fr1,
                    "P2_rel_improvement": m2, "P2_per_system": fr2,
                    "P3_ordering": q3, "P3_pairs": n3,
                    "P4_charge_cost": p4_charge_cost,
                    "shuffled_gap": shuf_gap, "anti_worst": anti_worst},
        "gates": gates, "verdict": verdict,
    }
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "GO87-blind-scheduling.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n[GOVERNED] verdict: {verdict}  gates: {gates}\nwrote {path}")


if __name__ == "__main__":
    main()
