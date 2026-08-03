# Multi-codebook replication of GO-7 (GO-P-2026-045): rerun the sealed
# GO-P-2026-043 Part-A design with FIVE independent codebooks per blocklength
# and a fresh seed, resolving the registered few-cluster caveat (one codebook
# per n).  The physics claim being hardened: the operational rate-work
# separation is a property of the random-coding ensemble, not of one lucky
# codebook draw.  Reuses the sealed Part-A machinery from
# landauer_operational.py verbatim (import, no copy).  Tier B (Atlas CPU,
# single process, ~45 min).  Output: sentinel JSON ===GOLMC-JSON===.  MIT.
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landauer_operational import R_AN, L_AN, RC_EXCESS, run_partA  # noqa: E402

SEED = 20260804          # fresh; distinct from the 043 governed seed
NCB = 5
NGRID = [12, 16, 20, 24, 28, 32]
TRIALS = [200, 200, 200, 200, 120, 100]
RBS = [0.03, 0.08, 0.13, 0.19, 0.26, 0.35, 0.50]


def main():
    print(f"GO-7 multi-codebook replication  seed={SEED}  codebooks={NCB}")
    print(f"target channel: BSC(0.08) x BSC(0.32)  R={R_AN:.4f}  L={L_AN:.4f}  "
          f"codebook rate={R_AN + RC_EXCESS:.4f}")
    t0 = time.time()
    books = []
    for cb in range(NCB):
        print(f"--- codebook {cb + 1}/{NCB} ---", flush=True)
        rng = np.random.default_rng([SEED, cb])
        books.append(run_partA(NGRID, TRIALS, RBS, rng))

    iSEP = RBS.index(0.26)
    iLOW = RBS.index(0.03)
    err_sep32 = [b[-1]["err_si"][iSEP] for b in books]
    err_low32 = [b[-1]["err_si"][iLOW] for b in books]
    err_low_big = [r["err_si"][iLOW] for b in books for r in b if r["n"] >= 16]
    ctrl = [r["err_ctrl"][iSEP] for b in books for r in b if r["n"] >= 20]
    R32 = [b[-1]["R_hat"] for b in books]
    L32 = [b[-1]["L_hat"] for b in books]
    D32 = [b[-1]["D_hat"] for b in books]

    verdict = dict(
        A1r_separation_every_codebook=bool(
            all(e <= 0.12 for e in err_sep32)
            and float(np.median(err_sep32)) <= 0.05),
        A2r_bin_rate_below_045R=bool(0.26 <= 0.45 * float(np.median(R32))),
        A3r_converse_every_codebook=bool(
            all(e >= 0.40 for e in err_low32) and min(err_low_big) >= 0.30),
        A4r_side_info_specific=bool(min(ctrl) >= 0.90),
        A5r_channel_realized_every_codebook=bool(
            all(abs(d - 0.20) <= 0.04 for d in D32)
            and all(0.03 <= l_ <= 0.14 for l_ in L32)
            and all(0.62 <= r_ <= 0.78 for r_ in R32)),
        A6r_cross_codebook_stability=bool(
            max(err_sep32) - min(err_sep32) <= 0.10),
    )
    result = dict(
        claim="GO-7 replication across independent codebooks",
        prereg="GO-P-2026-045",
        seed=SEED,
        n_codebooks=NCB,
        rb_grid=RBS,
        err_sep_n32_per_codebook=err_sep32,
        err_low_n32_per_codebook=err_low32,
        R_hat_n32_per_codebook=R32,
        L_hat_n32_per_codebook=L32,
        D_hat_n32_per_codebook=D32,
        books=books,
        verdict=verdict,
        GOLMC_replication_supported=bool(all(verdict.values())),
        seconds_total=round(time.time() - t0, 1),
    )
    print(f"\nerr(rb=0.26, n=32) per codebook: {err_sep32}")
    print(f"err(rb=0.03, n=32) per codebook: {err_low32}")
    print(f"verdict: {verdict}")
    print(f"GOLMC_replication_supported: {result['GOLMC_replication_supported']}")
    print("===GOLMC-JSON===")
    print(json.dumps(result, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
