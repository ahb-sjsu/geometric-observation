"""Audit VI-24, Proposition 2 (finite differences) of T1 note v4.

Claims checked:
 (A) column error of central differences <= M2 h/2 (g C^2) and <= M3 h^2/6 (g C^3);
     both constants attained (tightness examples).
 (B) ||Phat(x) - P(x)|| <= 2 M1 sqrt(p) beta + p beta^2, beta = min{M2 h/2, M3 h^2/6},
     with Phat = Jhat^T G Jhat formed from queries of C (not g), G PSD and singular,
     and C not Lipschitz in the directions G does not see.
 (C) the relative statement: Qhat_h - Qhat between -eps_h Q and eps_h Q, eps_h = (..)/lambda.
 Also: how loose is ||B|| <= ||B||_F <= sqrt(p) beta (ratio observed).
M_j are computed as sups over many points/directions (lower estimates), so a pass is stringent.
"""
import numpy as np

rng = np.random.default_rng(24)
out = []
P = out.append

# ---------- (A) tightness of the column-error constants
P("=== (A) column-error constants ===")
for h in [0.5, 0.1, 0.01]:
    # g(x) = x^3: M3 = 6, central-difference error = h^2 exactly = M3 h^2/6
    x = rng.uniform(-3, 3, 7)
    err = np.abs(((x + h) ** 3 - (x - h) ** 3) / (2 * h) - 3 * x ** 2)
    P(f"g=x^3, h={h}: max column error {err.max():.6g}, M3 h^2/6 = {6 * h * h / 6:.6g}")
    # g(x) = x|x|/2 at x = 0: M2 = 1, error = h/2 = M2 h/2
    gg = lambda t: t * np.abs(t) / 2
    P(f"g=x|x|/2 at 0, h={h}: column error {abs((gg(h) - gg(-h)) / (2 * h) - 0):.6g}, M2 h/2 = {h / 2:.6g}")


# ---------- (B) random smooth consumers with singular G
def make(p, k, kz):
    """C(x) = (A tanh(W x + b) + B x, unseen polynomial part); G = blockdiag(G1 (PSD), 0)."""
    n = 6
    W = rng.normal(size=(n, p)) * rng.uniform(0.3, 1.5)
    b = rng.normal(size=n)
    A = rng.normal(size=(k, n)) / np.sqrt(n)
    B = rng.normal(size=(k, p)) * 0.5
    R = rng.normal(size=(k, k))
    G1 = R @ R.T
    if k > 1 and rng.random() < 0.5:   # make G1 singular too
        w, U = np.linalg.eigh(G1); w[0] = 0; G1 = U @ np.diag(w) @ U.T
    G = np.zeros((k + kz, k + kz)); G[:k, :k] = G1
    w, U = np.linalg.eigh(G); Gh = U @ np.diag(np.sqrt(np.clip(w, 0, None))) @ U.T

    def C(x):  # x (..., p)
        y = np.tanh(x @ W.T + b) @ A.T + x @ B.T
        z = np.stack([np.sum(x ** 2, -1) ** (j + 1) for j in range(kz)], -1)  # not Lipschitz, unseen
        return np.concatenate([y, z], -1)

    def Jg(x):  # Jacobian of g = Gh C at x (p,)
        s = 1 - np.tanh(W @ x + b) ** 2
        Jy = A @ (s[:, None] * W) + B
        Jz = np.stack([(j + 1) * np.sum(x ** 2) ** j * 2 * x for j in range(kz)], 0)
        return Gh @ np.concatenate([Jy, Jz], 0)

    def derivs_at(x, u, v, w):
        t = W @ x + b
        th = np.tanh(t); s = 1 - th ** 2
        d2 = -2 * th * s; d3 = -2 * s * s + 4 * th * th * s
        Wu, Wv, Ww = W @ u, W @ v, W @ w
        D2 = A @ (d2 * Wu * Wv); D3 = A @ (d3 * Wu * Wv * Ww)
        pad = np.zeros(kz)
        return Gh @ np.concatenate([D2, pad]), Gh @ np.concatenate([D3, pad])

    # sup estimates of M1, M2, M3 for g (unseen block has zero rows in Gh)
    M1 = M2 = M3 = 0.0
    for _ in range(4000):
        x = rng.normal(size=p) * 3
        M1 = max(M1, np.linalg.norm(Jg(x), 2))
        u, v, w = (rng.normal(size=p) for _ in range(3))
        u /= np.linalg.norm(u); v /= np.linalg.norm(v); w /= np.linalg.norm(w)
        d2, d3 = derivs_at(x, u, u, u)
        M2 = max(M2, np.linalg.norm(d2)); M3 = max(M3, np.linalg.norm(d3))
    return C, Jg, G, M1, M2, M3


P("")
P("=== (B) operator-norm bound with queries of C and Phat = Jhat^T G Jhat ===")
worst = 0.0; ratioF = []; nchk = 0
for trial in range(60):
    p = int(rng.integers(1, 6)); k = int(rng.integers(1, 4)); kz = int(rng.integers(1, 3))
    C, Jg, G, M1, M2, M3 = make(p, k, kz)
    for _ in range(30):
        x = rng.normal(size=p) * 2
        h = 10 ** rng.uniform(-3, -0.3)
        I = np.eye(p)
        Jhat = np.stack([(C(x + h * I[j]) - C(x - h * I[j])) / (2 * h) for j in range(p)], 1)
        Phat = Jhat.T @ G @ Jhat
        Jx = Jg(x)
        Pt = Jx.T @ Jx
        beta = min(M2 * h / 2, M3 * h * h / 6)
        bound = 2 * M1 * np.sqrt(p) * beta + p * beta ** 2
        lhs = np.linalg.norm(Phat - Pt, 2)
        if lhs > 1e-11:  # avoid pure round-off cases
            worst = max(worst, lhs / bound)
            nchk += 1
        # how loose is ||B|| vs sqrt(p) beta
        w, U = np.linalg.eigh(G); Gh = U @ np.diag(np.sqrt(np.clip(w, 0, None))) @ U.T
        Bm = Gh @ Jhat - Jx
        if beta > 0:
            ratioF.append(np.linalg.norm(Bm, 2) / (np.sqrt(p) * beta))
P(f"{nchk} (consumer, x, h) cases: max ||Phat-P|| / bound = {worst:.4f} (must be <= 1, up to round-off at tiny h)")
P(f"||B|| / (sqrt(p) beta): max {max(ratioF):.3f}, median {np.median(ratioF):.3f}")

# ---------- (C) relative statement
P("")
P("=== (C) Qhat_h - Qhat between -eps_h Q and +eps_h Q ===")
viol = 0; tot = 0; tight = 0.0
for trial in range(40):
    p = int(rng.integers(1, 5)); k = int(rng.integers(p, p + 3)); kz = 1
    C, Jg, G, M1, M2, M3 = make(p, k, kz)
    xs = rng.normal(size=(20000, p))
    Q = np.mean([Jg(x).T @ Jg(x) for x in xs[:4000]], 0)  # a probe-law average (lambda only needs <= lmin Q)
    lam = np.linalg.eigvalsh(Q)[0]
    if lam < 1e-6:
        continue
    for h in [0.3, 0.05, 0.01]:
        m = 16
        pts = xs[4000:4000 + m]
        I = np.eye(p)
        Qh = np.zeros((p, p)); Qe = np.zeros((p, p))
        for x in pts:
            Jhat = np.stack([(C(x + h * I[j]) - C(x - h * I[j])) / (2 * h) for j in range(p)], 1)
            Qh += Jhat.T @ G @ Jhat / m
            Qe += Jg(x).T @ Jg(x) / m
        beta = min(M2 * h / 2, M3 * h * h / 6)
        eh = (2 * M1 * np.sqrt(p) * beta + p * beta ** 2) / lam
        Li = np.linalg.inv(np.linalg.cholesky(Q))
        ev = np.linalg.eigvalsh(Li @ (Qh - Qe) @ Li.T)
        tot += 1
        if np.max(np.abs(ev)) > eh * (1 + 1e-9) + 1e-12:
            viol += 1
        tight = max(tight, np.max(np.abs(ev)) / eh if eh > 0 else 0)
P(f"{tot} cases: violations {viol}; max observed |eig(Q^-1/2 (Qhat_h-Qhat) Q^-1/2)| / eps_h = {tight:.4f}")

open(__file__.replace(".py", ".out.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
