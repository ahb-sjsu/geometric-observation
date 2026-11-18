"""Audit VI-24, Corollary 3 (probes for a target price) of T1 note v4.

 (T) t = tanh(eta ln2 / p) >= (3/5) eta/p for 0 < eta <= p, and (p/2) log2((1+t)/(1-t)) = eta.
 (i)  m >= L max{200/9 nu+ nu- p^2/eta^2, 20/9 nu p/eta}  =>  (p/2) log2((1+e+)/(1-e-)) <= eta.
 (ii) m >= L max{50 nu+ nu- p^2/eta^2, 10/3 nu p/eta} and
      h^2 <= (6/M3) min{lam eta/(20 M1 p^{3/2}), (lam eta/(10 p^2))^{1/2}}
      => price with e+- + eps_h is <= eta, eps_h = (2 M1 sqrt(p) beta + p beta^2)/lam, beta = M3 h^2/6.
 Random instances at the thresholds (worst case m = ceil, h = the bound), plus how much slack
 the constants leave (smallest m that would do, by bisection).
"""
import numpy as np

rng = np.random.default_rng(3)
out = []
P = out.append
lg = np.log2

eta_p = np.linspace(1e-6, 1, 200001)
t = np.tanh(eta_p * np.log(2))
P(f"(T) min over eta/p in (0,1] of t / (0.6 eta/p) = {np.min(t / (0.6 * eta_p)):.6f} (>= 1 required)")
P(f"(T) tanh(ln 2) = {np.tanh(np.log(2)):.15f}; max |(p/2)log2((1+t)/(1-t)) - eta| / eta at p=1: "
  f"{np.max(np.abs(0.5 * lg((1 + t) / (1 - t)) - eta_p) / eta_p):.2e}")


def eps(nup, num, L, m):
    nu = max(nup, num)
    a = np.sqrt(2 * nup * num * L / m)
    return a + 2 * nup * L / (3 * m), a + 2 * num * L / (3 * m), a + 2 * nu * L / (3 * m)


fails_i = fails_ii = 0
slack_i, slack_ii = [], []
for trial in range(20000):
    p = int(rng.integers(1, 50))
    eta = rng.uniform(1e-3, 1) * p
    nup = 10 ** rng.uniform(-2, 1.5)
    num = 1.0 if trial % 2 else rng.uniform(0, 1)
    nu = max(nup, num)
    delta = 10 ** rng.uniform(-6, -0.3)
    L = np.log(2 * p / delta)
    # (i)
    m = int(np.ceil(L * max(200 / 9 * nup * num * p ** 2 / eta ** 2, 20 / 9 * nu * p / eta)))
    ep, em, _ = eps(nup, num, L, m)
    if em >= 1 or p / 2 * lg((1 + ep) / (1 - em)) > eta * (1 + 1e-12):
        fails_i += 1

    def ok(mm):
        a, b, _ = eps(nup, num, L, mm)
        return b < 1 and p / 2 * lg((1 + a) / (1 - b)) <= eta
    lo, hi = 1, m
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    slack_i.append(m / lo)
    # (ii)
    lam = 10 ** rng.uniform(-3, 1)
    M1 = np.sqrt(lam) * 10 ** rng.uniform(0, 1.5)   # M1^2 >= lmax(Q) >= lam
    M3 = 10 ** rng.uniform(-2, 2)
    m2 = int(np.ceil(L * max(50 * nup * num * p ** 2 / eta ** 2, 10 / 3 * nu * p / eta)))
    h2 = 6 / M3 * min(lam * eta / (20 * M1 * p ** 1.5), np.sqrt(lam * eta / (10 * p ** 2)))
    beta = M3 * h2 / 6
    eh = (2 * M1 * np.sqrt(p) * beta + p * beta ** 2) / lam
    ep, em, _ = eps(nup, num, L, m2)
    if em + eh >= 1 or p / 2 * lg((1 + ep + eh) / (1 - em - eh)) > eta * (1 + 1e-12):
        fails_ii += 1
    slack_ii.append(p / 2 * lg((1 + ep + eh) / (1 - em - eh)) / eta)
P(f"(i)  20000 random instances at the threshold m: failures {fails_i}; m_stated / m_needed: "
  f"median {np.median(slack_i):.2f}, max {np.max(slack_i):.2f}, min {np.min(slack_i):.2f}")
P(f"(ii) 20000 random instances at the threshold m and h: failures {fails_ii}; achieved price / eta: "
  f"median {np.median(slack_ii):.3f}, max {np.max(slack_ii):.3f}")

open(__file__.replace(".py", ".out.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
