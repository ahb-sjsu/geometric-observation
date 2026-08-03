# Shared instruments for the GO-P-2026-053/054 second attempts.
#
# (1) exact_binom_ok -- replaces the normal-approximation control gate that
#     invalidly failed GO-P-2026-051 at r_b = 0.35: chance error there is
#     0.99994, so N*p*(1-p) = 0.05 << 5 and the normal SE is meaningless.
#     This is an EXACT two-sided binomial tail test in log space (no scipy).
#     It is the only gate changed between the 051/052 attempt and this one;
#     every physics bar is carried over byte-identical.
# (2) strided_members -- performance only, semantics identical: the in-bin
#     member set {b, b+nbins, ...} is a strided VIEW of the codebook rather
#     than a fancy-indexed COPY, which is what made the 051/052 designs
#     compute-bound and forced small n.
# MIT License.
from math import exp, lgamma, log, log1p

import numpy as np


def binom_sf(k, N, p):
    """P(X >= k) for X ~ Binom(N, p), exact, summed in log space."""
    if k <= 0:
        return 1.0
    if p <= 0.0:
        return 0.0
    if p >= 1.0:
        return 1.0
    tot = 0.0
    lc = lgamma(N + 1)
    for i in range(int(k), int(N) + 1):
        lp = (lc - lgamma(i + 1) - lgamma(N - i + 1)
              + i * log(p) + (N - i) * log1p(-p))
        t = exp(lp)
        tot += t
        if t < 1e-18 and i > k:
            break
    return min(1.0, tot)


def binom_cdf(k, N, p):
    """P(X <= k), exact."""
    return 1.0 - binom_sf(k + 1, N, p)


def exact_binom_ok(ctrl_err_pooled, chance_err_pooled, N, alpha=5e-4):
    """True iff the pooled control's success count is consistent with chance
    under an EXACT two-sided binomial test at level alpha."""
    p = max(min(1.0 - chance_err_pooled, 1.0), 0.0)
    k = int(round(N * (1.0 - ctrl_err_pooled)))
    if p <= 0.0:
        return k == 0
    return binom_sf(k, N, p) >= alpha and binom_cdf(k, N, p) >= alpha


def strided_argmin(scores_view, base, step, rng):
    """argmin over a strided member view -> absolute codebook index,
    with uniform tie-breaking (identical semantics to the 051/052 loops)."""
    mn = scores_view.min()
    loc = np.flatnonzero(scores_view == mn)
    return int(base + step * int(loc[rng.integers(0, loc.size)]))


def thr_interp(errs, rbs, bar=0.25):
    """Continuous threshold: linear interpolation of the error curve's crossing
    of `bar` (carried over unchanged from the 051/052 harnesses)."""
    for i, e in enumerate(errs):
        if e <= bar:
            if i == 0:
                return float(rbs[0])
            e0, e1 = errs[i - 1], e
            if e0 <= e1:
                return float(rbs[i])
            f = (e0 - bar) / (e0 - e1)
            return float(rbs[i - 1] + f * (rbs[i] - rbs[i - 1]))
    return float("nan")
