# LOCATA wideband confirm — exploratory run logs (2026-11-13)

Raw stdout of `experiments/locata_gateb.py --confirm-wb "/archive/locata/dev/task1/recording*/dicit"`
(wideband 1200–3000 Hz black-box confirmatory path, 8 cm DICIT ULA), run on Atlas, CPU only,
on the three `dev/task1` recordings. **Exploratory and unsealed**: no prereg, no ledger row, no
`eval` recordings used. Context: PR #5 (merge `b4ead59`).

| File | Script state | Notes |
|---|---|---|
| `run_dev_task1.log` | sha256 `bfae1107…510fe` (not retained) | First run with the band-pooled analytic baseline. The baseline's complex phase was still arbitrary, so the `cos(rec,ĝ)` and `cos(ĝ,ĝmed)` columns in this log are **not meaningful**. Superseded. |
| `run_dev_task1_v2.log` | sha256 `3f871359…a729a` (not retained) | Final run: baseline phase pinned, phase-invariant overlap columns added. This is the table quoted in PR #5. |

Neither script state is a git commit. The committed script (`d183a68`) differs from the v2 state
only by the loader/fit dedup refactor, which was checked bit-identical (both recoveries on
synthetic data, both loaders on these three recordings); the full confirm was **not** rerun on
the committed script.

The only difference between the two runs' `ĝ` arm is the baseline's phase, and it moved
recording3 from 8/8 to 7/8 and the "recovered-same ≥ ĝ" tally from 1/3 to 2/3 — with three
recordings that tally is at noise level.

Log checksums (sha256):

    ab2edac5954de664e04047c5081eae0cc792084dc78f67789d8a64ccb2a6a3c3  run_dev_task1.log
    ca37ed65c806881b04b1e9709182ff29278720d99abdf7b403befea1e128af57  run_dev_task1_v2.log
