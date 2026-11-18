"""Audit VI-24, Remark 13 (how restrictive (A1) is) and the g = G^{1/2} C statements after (A1).

 (R1) 'A bi-Lipschitz g excludes a ReLU without leak': counterexamples. An expanding ReLU layer
      g(x) = ReLU([I; -I] x) (2p outputs) is bi-Lipschitz, satisfies (A1a) under a Gaussian source,
      and has finite tau_nu. Also g(x) = (x, ReLU(x)).
 (R2) C(x) = (x, x^2), G = diag(1,0): loss (xh-x)^2, Q = 1, nu = 0, C not Lipschitz.
 (R3) leaky ReLU slope a, symmetric pi: nu+- = (1-a^2)/(1+a^2), tau_nu = p log2(1/a);
      the pairwise sandwich (A1a) holds with the same constants.
 (R4) Lipschitz constant from the upper half of (A1a): ((1+nu+) lmax(Q))^{1/2}.
"""
import numpy as np

rng = np.random.default_rng(13)
out = []
P = out.append
relu = lambda z: np.maximum(z, 0)

P("=== (R1) ReLU without leak, expanding: bi-Lipschitz and (A1a) ===")
for p in [1, 2, 4]:
    Wt = np.vstack([np.eye(p), -np.eye(p)])
    g = lambda x: relu(x @ Wt.T)
    # read metric: J = diag(1{x_i>0}) rows for +, diag(1{x_i<0}) for -, so J^T J = I a.e.  => Q = I
    X = rng.normal(size=(400000, p)) * 2
    Y = X + rng.normal(size=X.shape) * 10 ** rng.uniform(-3, 1, (len(X), 1))
    d = Y - X
    ratio = np.sum((g(Y) - g(X)) ** 2, 1) / np.sum(d ** 2, 1)
    lo, hi = ratio.min(), ratio.max()
    nu_m, nu_p = 1 - lo, hi - 1
    tau = p / 2 * np.log2((1 + max(nu_p, 0)) / (1 - nu_m))
    P(f"p={p}: g=ReLU([I;-I]x), Q=I; loss/(d^T Q d) over 4e5 pairs in [{lo:.4f}, {hi:.4f}] "
      f"(theory [1/2, 1]); so (A1a) with nu-={nu_m:.3f}, nu+={max(nu_p, 0):.3f}; tau_nu = {tau:.3f} bits (theory p/2)")
gx = lambda x: np.stack([x, relu(x)], -1)
x = rng.normal(size=400000) * 2; y = x + rng.normal(size=x.size)
r = np.sum((gx(y) - gx(x)) ** 2, -1) / (y - x) ** 2
P(f"g(x)=(x, ReLU x): ratio loss/(xh-x)^2 in [{r.min():.4f}, {r.max():.4f}] -> bi-Lipschitz (Q = E P = 1.5 under symmetric pi)")

P("")
P("=== (R2) C=(x, x^2), G=diag(1,0) ===")
x = rng.normal(size=10) * 5; y = rng.normal(size=10) * 5
C = lambda t: np.stack([t, t ** 2], -1)
G = np.diag([1.0, 0.0])
loss = np.einsum("ni,ij,nj->n", C(y) - C(x), G, C(y) - C(x))
P(f"max |loss - (y-x)^2| = {np.max(np.abs(loss - (y - x) ** 2)):.2e}; Lip(x^2) on [-L,L] = 2L unbounded")

P("")
P("=== (R3) leaky ReLU ===")
for a in [0.01, 0.2, 0.5]:
    p = 3
    X = rng.normal(size=(400000, p)); Y = X + rng.normal(size=X.shape) * 10 ** rng.uniform(-2, 1, (len(X), 1))
    lr = lambda z: np.where(z > 0, z, a * z)
    Q = (1 + a * a) / 2
    ratio = np.sum((lr(Y) - lr(X)) ** 2, 1) / (Q * np.sum((Y - X) ** 2, 1))
    nu_th = (1 - a * a) / (1 + a * a)
    P(f"a={a}: pairwise ratio in [{ratio.min():.4f}, {ratio.max():.4f}] vs theory [{1 - nu_th:.4f}, {1 + nu_th:.4f}]; "
      f"tau_nu/p = {0.5 * np.log2((1 + nu_th) / (1 - nu_th)):.4f} = log2(1/a) = {np.log2(1 / a):.4f}")

P("")
P("=== (R4) Lipschitz constant from the upper half of (A1a) ===")
for trial in range(3):
    p = 3
    A = rng.normal(size=(p, p)); Q = A @ A.T + np.eye(p)
    nup = 0.3
    # any loss with l <= (1+nup) d^T Q d: e.g. g(x) = (1+nup)^{1/2} Q^{1/2} x  (extremal)
    w, U = np.linalg.eigh(Q); Qh = U @ np.diag(np.sqrt(w)) @ U.T
    g = lambda x: np.sqrt(1 + nup) * x @ Qh
    X = rng.normal(size=(200000, p)); Y = rng.normal(size=(200000, p))
    lip = np.max(np.linalg.norm(g(Y) - g(X), axis=1) / np.linalg.norm(Y - X, axis=1))
    P(f"extremal g: observed Lipschitz {lip:.4f} <= ((1+nu+) lmax Q)^1/2 = {np.sqrt((1 + nup) * w[-1]):.4f}")

open(__file__.replace(".py", ".out.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
