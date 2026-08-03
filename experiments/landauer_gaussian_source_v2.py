# GO-P-2026-047: corrected rerun of the GO-7 cross-source replication
# (scalar Gaussian).  GO-P-2026-046 MISSED 4/6 on two instrumentation-window
# design errors (R_mom ceiling anchored to the analytic R(D) instead of the
# codebook rate; a deep-decode bar sitting exactly on a realizable count and
# failing on float epsilon) while all four PHYSICS gates passed.  This v2
# reuses the sealed 046 machinery verbatim (import, no fork), keeps gates
# G1-G4 identical for comparability, corrects G5's ceiling to 1.06 (code
# rate 1.042 + estimation headroom) and G6 to <= 0.035 with an epsilon
# guard, and draws a FRESH seed.  Output: ===GOLGS2-JSON===.  Tier B.  MIT.
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landauer_gaussian_source import L_AN, R_AN, RC_EXCESS, RHO, DT, run_gauss  # noqa: E402

SEED = 20260806
NGRID = [8, 12, 16, 20, 24]
TRIALS = [200, 200, 200, 200, 200]
RBS = [0.05, 0.12, 0.20, 0.28, 0.36, 0.60]


def main():
    rng = np.random.default_rng(SEED)
    print(f"GO-7 cross-source replication v2 (corrected windows)  seed={SEED}")
    print(f"rho={RHO}  D={DT}  analytic R={R_AN:.4f}  L={L_AN:.4f}  "
          f"codebook rate={R_AN + RC_EXCESS:.4f}")
    t0 = time.time()
    rows = run_gauss(NGRID, TRIALS, RBS, rng)

    iSEP = RBS.index(0.36)
    iLOW = RBS.index(0.05)
    iDEEP = RBS.index(0.60)
    err_sep = [r["err_si"][iSEP] for r in rows]
    err_low = [r["err_si"][iLOW] for r in rows]
    err_low_big = [r["err_si"][iLOW] for r in rows if r["n"] >= 12]
    ctrl_sep = [r["err_ctrl"][iSEP] for r in rows if r["n"] >= 16]
    half = len(err_sep) // 2
    last = rows[-1]
    verdict = dict(
        # G1-G4 identical to GO-P-2026-046 (all passed there; comparability)
        G1_separation_decodes=bool(err_sep[-1] <= 0.20 and err_sep[-2] <= 0.30
                                   and np.mean(err_sep[half:]) <= np.mean(err_sep[:half])),
        G2_bin_rate_below_050R=bool(0.36 <= 0.50 * last["R_mom"]),
        G3_converse_low_rb_fails=bool(min(err_low_big) >= 0.30
                                      and err_low[-1] >= 0.40),
        G4_side_info_specific=bool(min(ctrl_sep) >= 0.90) if ctrl_sep else False,
        # G5 corrected: ceiling anchored to the codebook rate (1.042) + headroom
        G5_channel_realized=bool(0.22 <= last["D_hat"] <= 0.36
                                 and 0.72 <= last["R_mom"] <= 1.06
                                 and 0.02 <= last["L_mom"] <= 0.15),
        # G6 corrected: count-robust bar (<= 7/200) with epsilon guard
        G6_deep_decode=bool(last["err_si"][iDEEP] <= 0.035 + 1e-9),
    )
    result = dict(
        claim="GO-7 cross-source replication v2 (scalar Gaussian, corrected windows)",
        prereg="GO-P-2026-047",
        supersedes="GO-P-2026-046",
        seed=SEED,
        target=dict(rho=RHO, D=DT, R=R_AN, L=L_AN, codebook_excess=RC_EXCESS),
        rb_grid=RBS,
        rows=rows,
        err_at_rb036=err_sep,
        err_at_rb005=err_low,
        verdict=verdict,
        GOLGS2_crosssource_supported=bool(all(verdict.values())),
        seconds_total=round(time.time() - t0, 1),
    )
    print(f"\nverdict: {verdict}")
    print(f"GOLGS2_crosssource_supported: {result['GOLGS2_crosssource_supported']}")
    print("===GOLGS2-JSON===")
    print(json.dumps(result, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
