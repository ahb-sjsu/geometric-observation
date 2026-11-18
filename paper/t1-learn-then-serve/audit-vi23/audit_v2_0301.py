"""Exact (quadrature) consumer loss for x+0.05 sin x, design for exact Q at D=0.3 (Sigma=diag(2,.5), G=diag(4,1),
holder H=[1,.5], SU=1 as in the author's checks; the VI-22 audit's own setup is not known to the auditor)."""
import itertools, sys
import numpy as np
sys.path.insert(0, r"C:\source\worktrees\geometric-observation-t1-v3\paper\tit-stationary")
import spectral_core as sc
def msqrt(A):
    w, V = np.linalg.eigh((A+A.T)/2); return (V*np.sqrt(np.clip(w, 0, None))) @ V.T
x, w = np.polynomial.hermite_e.hermegauss(60); w = w/w.sum()
idx = np.array(list(itertools.product(range(60), repeat=2))); z, wz = x[idx], np.prod(w[idx], 1)
Sig = np.diag([2.0, 0.5]); G = np.diag([4.0, 1.0]); H = np.array([[1.0, 0.5]]); SU = np.array([[1.0]])
b = 0.05; f = lambda X: X + b*np.sin(X)
q = 1 + 2*b*np.exp(-np.diag(Sig)/2) + b**2/2*(1 + np.exp(-2*np.diag(Sig))); Q = G @ np.diag(q)
S12 = msqrt(Sig)
for alpha in (0.0, 0.5, 1.0):
    Dl = S12 @ sc.solve([(S12 @ Q @ S12, H @ S12, SU)], [1.0], alpha, 0.3)["X"][0] @ S12; Dl = (Dl+Dl.T)/2
    Th = z @ msqrt(Sig - Dl).T; Z = z @ msqrt(Dl).T
    d = f(Th[:, None, :] + Z[None]) - f(Th)[:, None, :]
    print(alpha, "tr(Q Delta)=%.6f  E loss=%.6f" % (np.trace(Q @ Dl), np.einsum("i,j,ijk,kl,ijl->", wz, wz, d, G, d)))
