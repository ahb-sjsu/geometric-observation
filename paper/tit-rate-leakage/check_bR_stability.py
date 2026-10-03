"""check_bR_stability.py (diagnostic, 2026-10-02): the replicate designs recompute b_R on every split, although
registrations 4 and 5 describe b_R as frozen. For each dataset: the smallest |b_R(seed)' Sigma0 b_R(0)| over seeds
1..20 (1 = same direction, 0 = an orthogonal swap), and the seeds on which the mix view's context column (the one least
correlated with Z_R) differs from split 0."""
import math
import numpy as np
import ot_boundary as ob
import ot_gaussianity as og
import ot_scope as sc
import ot_nearboundary as nb
from scipy.linalg import eigh

def info(d, seed):
    P = ob.prepare(d, seed=seed); Sig = P["Sig"]; m = d["m"]; p = Sig.shape[0]
    F = np.zeros((m, p)); F[:, :m] = np.eye(m); B = Sig @ F.T @ F @ Sig
    w, V = eigh(B, Sig); b = V[:, -1]; zR = b / math.sqrt(b @ Sig @ b); ctx = list(range(m, p))
    j = ctx[int(np.argmin([abs(float(zR @ Sig[:, k]) / math.sqrt(Sig[k, k])) for k in ctx]))]
    gap = (w[-1] - w[-2]) / w[-1] if len(w) > 1 else 1.0
    return b, Sig, j, gap

sets = ob.DATA + ob.synthetic_sets() + [f() for f in og.FRESH_LOADERS] + [f() for f in sc.LOADERS] + sc.controls() \
       + [f() for f in nb.LOADERS] + nb.controls()
for d in sets:
    b0, S0, j0, g0 = info(d, 0); mins, jch = 1.0, []
    for s in range(1, 21):
        b, _, j, _ = info(d, s); mins = min(mins, abs(float(b @ S0 @ b0))); jch += [s] if j != j0 else []
    print(f"{d['name']:18s} min |align| {mins:.3f}  relative eigengap at split 0 {g0:.3f}  context column changes on seeds {jch}")
