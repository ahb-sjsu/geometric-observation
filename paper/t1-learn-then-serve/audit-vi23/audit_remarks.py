"""Auditor's independent re-computation of the 0.998 ratio (arm S, beta=0.2, D=0.3 tr(Q Sigma)),
using spectral_core only for the frontier design and an own backward-channel quadrature for the
loss; plus lambda_min(Q) for the softmax read-out of arm B; plus the backward-bound rhobar of
Corollary 8 versus the note's rhobar on the arm-S consumers."""
import itertools, sys
import numpy as np
sys.path.insert(0, r"C:\source\worktrees\geometric-observation-t1-v3\paper\tit-stationary")
import spectral_core as sc

def msqrt(A):
    w, V = np.linalg.eigh((A+A.T)/2); return (V*np.sqrt(np.clip(w, 0, None))) @ V.T
x, w = np.polynomial.hermite_e.hermegauss(60); w = w/w.sum()
Sig = np.diag([2.0, 0.5]); G = np.diag([4.0, 1.0]); H = np.array([[1.0, 0.5]]); SU = np.array([[1.0]])
beta = 0.2
f = lambda X: X + beta*np.sin(X)
q = 1 + 2*beta*np.exp(-np.diag(Sig)/2) + beta**2/2*(1 + np.exp(-2*np.diag(Sig)))
Q = G @ np.diag(q)
D = 0.3*np.trace(Q @ Sig)
S12 = msqrt(Sig)
for alpha in (0.0, 0.5, 1.0):
    r = sc.solve([(S12 @ Q @ S12, H @ S12, SU)], [1.0], alpha, D)
    Dl = S12 @ r["X"][0] @ S12; Dl = (Dl+Dl.T)/2
    # backward channel: That ~ N(0, Sig - Dl), Z ~ N(0, Dl), independent
    idx = np.array(list(itertools.product(range(60), repeat=2))); z, wz = x[idx], np.prod(w[idx], 1)
    Th = z @ msqrt(Sig - Dl).T; Z = z @ msqrt(Dl).T
    d = f(Th[:, None, :] + Z[None]) - f(Th)[:, None, :]
    El = np.einsum("i,j,ijk,kl,ijl->", wz, wz, d, G, d)
    print(f"alpha={alpha}: tr(Q Delta)={np.trace(Q @ Dl):.5f}  E loss={El:.5f}  ratio={El/np.trace(Q @ Dl):.5f}  (D={D:.4f}, tr Delta={np.trace(Dl):.4f})")

# softmax arm B: lambda_min(Q) under Sigma = diag(2, 0.5)
Wb = np.random.default_rng(20261117).standard_normal((3, 2)); Wb /= np.linalg.norm(Wb, 2)
idx = np.array(list(itertools.product(range(60), repeat=2))); z, wz = x[idx], np.prod(w[idx], 1)
T = z @ S12
Zl = T @ Wb.T; e = np.exp(Zl - Zl.max(1, keepdims=True)); s = e/e.sum(1, keepdims=True)
A = np.einsum("ni,ij->nij", s, np.eye(3)) - np.einsum("ni,nj->nij", s, s)
P = np.einsum("ip,nij,njk,kq->npq", Wb, A, A, Wb)
Qs = np.einsum("n,npq->pq", wz, P)
print("softmax arm B: eig(Q) =", np.linalg.eigvalsh(Qs), " singular values of W:", np.linalg.svd(Wb, compute_uv=False))

# Corollary 8: note's rhobar vs backward rhobar (no omega, no Sigma) on arm S, as a fraction of D
for beta in (0.05, 0.2):
    g = np.diag(G); M1 = np.sqrt(g.max())*(1+beta); M2 = M3 = np.sqrt(g.max())*beta
    q = 1 + 2*beta*np.exp(-np.diag(Sig)/2) + beta**2/2*(1 + np.exp(-2*np.diag(Sig)))
    lq = (G @ np.diag(q)).diagonal().min(); ls = 0.5
    for frac in (0.002, 0.0005):
        D = frac*np.trace(G @ np.diag(q) @ Sig); sb = D/lq; th = sb**2/ls
        rn = (M1**2*th + M1*M2*(3*th**0.5*sb + 3**0.75*th**1.5) + (0.75*M2**2 + M1*M3)*sb**2
              + np.sqrt(5)/2*M2*M3*sb**2.5 + 5/12*M3**2*sb**3)
        rb = (1.75*M2**2 + 2*M1*M3)*sb**2 + np.sqrt(5)/2*M2*M3*sb**2.5 + 5/12*M3**2*sb**3
        print(f"Cor8 arm S beta={beta} frac={frac}: rhobar_note/D={rn/D:.4f}  rhobar_back/D={rb/D:.4f}  (lambda_min(Q) used in place of lambda_min(Qhat))")
