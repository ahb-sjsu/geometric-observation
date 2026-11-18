"""Audit VI-24, Proposition 4 (the calibration message) of T1 note v4.

 (G) grid range: on the event every entry of Qhat lies in [-N_q s, N_q s];
     rounding error <= s/2; Qtilde satisfies (1-e-)(1-eq) Q <= Qtilde <= (1+e+)(1+eq) Q.
     Worst cases: Qhat on the event's boundary, adversarial rounding (every entry at +-s/2).
 (B) bit count B = p(p+1)/2 ceil(log2(2N_q+1)) and its growth as e- -> 1 (hidden by the O()).
 (L) the leakage measure: exact entropies on a toy with a random calibration message.
     I(T;Qt,M|S) (the note's measure) vs H(Qt,M|S) (the series' H(M|S^N) definition,
     which part2 Sec. 'The Stationary Source' uses for encoders with private randomness),
     and vs the per-realisation reading H(M|S, Qt=q).
"""
import numpy as np
from itertools import product

rng = np.random.default_rng(4)
out = []
P = out.append
lg = np.log2

P("=== (G) grid, rounding, sandwich ===")
viol = 0; tot = 0; maxratio_lo = maxratio_hi = 0.0
for trial in range(6000):
    p = int(rng.integers(1, 9))
    A = rng.normal(size=(p, p)); Q = A @ A.T + 10 ** rng.uniform(-3, 0) * np.eye(p)
    w = np.linalg.eigvalsh(Q)
    lam = w[0] * rng.uniform(0.3, 1.0); Lam = w[-1] * rng.uniform(1.0, 2.0)
    kappa = Lam / lam
    ep = rng.uniform(0, 2); em = rng.uniform(0, 0.95); eq = 10 ** rng.uniform(-3, -0.05)
    Qh_half = np.linalg.cholesky(Q)
    U, _ = np.linalg.qr(rng.normal(size=(p, p)))
    ev = rng.choice([1 - em, 1 + ep], p) if trial % 2 == 0 else rng.uniform(1 - em, 1 + ep, p)
    Qhat = Qh_half @ U @ np.diag(ev) @ U.T @ Qh_half.T
    s = 2 * (1 - em) * lam * eq / p
    Nq = int(np.ceil(p * kappa * (1 + ep) / (2 * (1 - em) * eq)))
    assert np.max(np.abs(Qhat)) <= Nq * s * (1 + 1e-12)
    iu = np.triu_indices(p)
    j = np.round(Qhat[iu] / s)
    assert np.all(np.abs(j) <= Nq)
    Qt = np.zeros((p, p)); Qt[iu] = j * s; Qt = Qt + Qt.T - np.diag(np.diag(Qt))
    # adversarial variant: every rounding error at +- s/2 with the sign pattern that maximises ||E||
    E = np.zeros((p, p)); E[iu] = s / 2 * rng.choice([-1, 1], len(iu[0])); E = E + E.T - np.diag(np.diag(E))
    for Qtil in (Qt, Qhat + E, Qhat + s / 2 * np.ones((p, p)), Qhat - s / 2 * np.ones((p, p))):
        Li = np.linalg.inv(Qh_half)
        r = np.linalg.eigvalsh(Li @ Qtil @ Li.T)
        tot += 1
        lo, hi = (1 - em) * (1 - eq), (1 + ep) * (1 + eq)
        if r[0] < lo * (1 - 1e-12) or r[-1] > hi * (1 + 1e-12):
            viol += 1
        maxratio_lo = max(maxratio_lo, (1 - r[0]) / (1 - lo))
        maxratio_hi = max(maxratio_hi, (r[-1] - 1) / (hi - 1))
P(f"{tot} (instance, rounding) cases incl. all-(+s/2) and all-(-s/2) errors: violations {viol}; "
  f"max (1-rmin)/(1-lo) = {maxratio_lo:.4f}, max (rmax-1)/(hi-1) = {maxratio_hi:.4f}")

P("")
P("=== (B) bits ===")
for p, kappa, eq in [(2, 10, 0.05), (10, 100, 0.01), (50, 1000, 0.01)]:
    for ep, em in [(0.2, 0.2), (0.2, 0.9), (0.2, 0.999)]:
        Nq = int(np.ceil(p * kappa * (1 + ep) / (2 * (1 - em) * eq)))
        B = p * (p + 1) // 2 * int(np.ceil(lg(2 * Nq + 1)))
        P(f"p={p:3d} kappa={kappa:5d} eq={eq}: e+={ep}, e-={em}: N_q={Nq}, B={B} bits "
          f"(p(p+1)/2 log2(p kappa/eq) = {p * (p + 1) / 2 * lg(p * kappa / eq):.0f})")

P("")
P("=== (L) the leakage measure, exact on a toy ===")
# T uniform on {0,1,2,3}; holder S = T // 2 seen through a BSC(0.1); calibration Qt uniform on {0,1}
# independent of (T, S) (it comes from the probes); code for weight q: M = f_q(T).
# Two code families: (i) the code does not depend on q; (ii) the code for q relabels the messages.
pT = np.full(4, 0.25)


def pS_given_T(s, t):
    return 0.9 if s == (t // 2) else 0.1


def H(pmf):
    v = np.array([x for x in pmf.values() if x > 0])
    return -np.sum(v * lg(v))


def joint(f):
    J = {}
    for t, s, q in product(range(4), range(2), range(2)):
        pr = pT[t] * pS_given_T(s, t) * 0.5
        key = (t, s, q, f(q, t))
        J[key] = J.get(key, 0) + pr
    return J


def marg(J, idx):
    m = {}
    for k, v in J.items():
        kk = tuple(k[i] for i in idx)
        m[kk] = m.get(kk, 0) + v
    return m


def Hc(J, A, B):  # H(A | B)
    return H(marg(J, A + B)) - H(marg(J, B))


for label, f in [("code independent of q: M = T // 2", lambda q, t: t // 2),
                 ("code for q relabels: M = (T // 2) xor q", lambda q, t: (t // 2) ^ q)]:
    J = joint(f)   # indices: 0 T, 1 S, 2 Qt, 3 M
    I_note = Hc(J, [0], [1]) - Hc(J, [0], [1, 2, 3])          # I(T; Qt, M | S)
    H_series = Hc(J, [2, 3], [1])                              # H(Qt, M | S)
    H_M_only = Hc(J, [3], [1])                                 # H(M | S), holder not told Qt
    H_given_q = Hc(J, [3], [1, 2])                             # H(M | S, Qt): per-realisation reading
    P(f"{label}:  I(T;Qt,M|S)={I_note:.4f}  H(M|S,Qt)={H_given_q:.4f}  H(Qt,M|S)={H_series:.4f}  H(M|S)={H_M_only:.4f}")

open(__file__.replace(".py", ".out.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
