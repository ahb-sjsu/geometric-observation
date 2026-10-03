"""check_sign_flips.py (diagnostic, 2026-10-02): in the replicate designs (registrations 4 and 5, phase B), b_R is
recomputed by an eigensolver on each split while b_aware is frozen from split 0. The eigenvector's sign is arbitrary, and
the mix views S = cos(phi) Z_R + sin(phi) X_j depend on it. This lists, for every dataset used by those designs, the
seeds on which b_R's sign differs from split 0 (sign of b_R(seed)' Sigma0 b_R(0))."""
import numpy as np
import ot_boundary as ob
import ot_gaussianity as og
import ot_scope as sc
import ot_nearboundary as nb
from scipy.linalg import eigh

def bR(d, seed):
    P = ob.prepare(d, seed=seed); Sig = P["Sig"]; m = d["m"]; p = Sig.shape[0]
    F = np.zeros((m, p)); F[:, :m] = np.eye(m); B = Sig @ F.T @ F @ Sig
    return eigh(B, Sig)[1][:, -1], Sig

sets = ob.DATA + ob.synthetic_sets() + [f() for f in og.FRESH_LOADERS] + [f() for f in sc.LOADERS] + sc.controls() \
       + [f() for f in nb.LOADERS] + nb.controls()
for d in sets:
    b0, S0 = bR(d, 0); flips = []
    for s in range(1, 21):
        b, _ = bR(d, s)
        if float(b @ S0 @ b0) < 0: flips.append(s)
    print(f"{d['name']:18s} flipped seeds (1..20): {flips}")
