# VI-45: Paper III's net, version 4, its run and its CI wiring (2026-11-21)

**Target.**
- **Version 4** of `experiments/verify_paper3_nets.py`, committed as 57bccec before its
  first run.
- **Its output** `results/PAPER3-nets.json` and the run account `results/PAPER3-nets-RUNS.md`.
- **The CI wiring**, which adds the net to `ci/reproduce.py`'s re-run tier. The output, the
  account and the wiring were all uncommitted at the time of the review.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. Its checks:
- read the 5375b7b..57bccec diff;
- checked the recorded hash against `git show 57bccec:…`;
- recomputed every number in the run account from the JSON's `pairs_detail`;
- regenerated the instances, the closed forms, m5 and m6 from the committed blob and its
  seed on Windows with numpy 2.5.2. It had no cvxpy, so the solver outputs were not
  reproduced.

**Verdict.** Version 4 does what VI-38 asked (#10, an absolute m4 tolerance on a fresh seed;
#17, m1's trace check). The run account's numbers match the JSON exactly, every verdict
follows from the recorded values, and the CI wiring is correct. **0 errors**, 5 gaps,
2 overclaims (minor) and 5 exposition items. The main risk for CI is m4's solver-status
clauses.

## Findings and dispositions (2026-11-21)

The harness is left byte-identical to the file that ran, so that its recorded sha256 still
matches. Findings about the harness are therefore disclosed in the run account and owed to a
version 5; none is applied to the harness itself.

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | OVERCLAIM (minor) | m1's two-sided trace clause is an identity of the closed form and can fail only on a bug. It does not test that the max-det optimum binds the trace. | Disclosed in the run account. Version 5: apply the check to the solver's solution. |
| 2 | OVERCLAIM (minor) | m4's intercepts (up to 3.6e-6) are the bias of the a + c√δ fit, not corner error. A quadratic through the same gaps gives at most 2.1e-7. m4's resolution is asymmetric: about 6.4e-6 nats for a corner too high, 1.36e-5 for one too low. | Disclosed in the run account. Version 5: a quadratic fit on four δ. |
| 3 | GAP | The JSON has no start time, commit, Clarabel version or thread count. That the harness was committed before it ran rests on git's order (commit 08:28:44, push 08:28:48, JSON 08:33). | Disclosed, with Clarabel 0.11.1 on Atlas as queried after the run. Version 5 records all four. |
| 4 | GAP (CI fragility) | m4's verdict includes two discrete solver-status clauses. One solver failure in 574 solves flips it. Clarabel is not pinned. | Accepted and disclosed. The `ci/reproduce.py` comment names the risk, and if it fires the fix is forward, with disclosure. The shard was run in full on an Atlas clean clone before the push. |
| 5 | GAP (procedural) | Committing the CI wiring without the new JSON would crash shard 1. FRONTIER G11 and the LEDGER still called version 4 owed. | The wiring, the JSON, the run account and the rename are committed together, and G11 is updated. |
| 6 | GAP (minor, since version 2) | After 50 draws the redraw loop keeps its last draw, unrecorded. On this seed every pair met the floor within 4 draws. | Disclosed. Version 5: record the draws, and fail when the floor is not met. |
| 7 | GAP (minor) | `cap_binds` is not recorded per row. Regenerated, the 28 informative pairs are exactly the pairs that are independent, have a binding cap and are not nested. | Disclosed. Version 5: record it. |
| 8 | exposition | The docstring's output-file name and "version 4 … owed" are stale. | Named in the `ci/reproduce.py` comment and the run account. Version 5 fixes the docstring. |
| 9 | exposition | The run account's last line said "this file's verdict". | Now names `PAPER3-nets.json`. |
| 10 | exposition | "Crashed before any check printed" would be true of any crash. | "Crashed at m1's first solver call; no check completed". |
| 11 | exposition (older text) | m3's docstring counts differ slightly from the code: the code gates all nested pairs, and only the cap-binding non-nested ones. No effect here. | Version 5. |
| 12 | exposition (low) | "On the others gap = 0 by construction" holds for one named pair by that instance's structure, not by the general argument. | Version 5. |

**Confirmed right by the verifier:**
- **The hash.** The blob of 57bccec hashes to the recorded 6dfa9e68…; the Windows CRLF
  checkout hashes differently, as the account says.
- **The version 4 code against VI-38 and the docstring.**
- **The attempt-1 account and the environment-only rerun.** No outcome was seen and
  discarded.
- **Every number in the run account.** The informative count, the worst intercept, the
  status counts, m3's counts and the iff all recompute.
- **Regeneration.** The instances, the closed-form checks, m5 and m6 reproduce. The
  Monte Carlo is bit-identical across numpy 2.4.6 on Linux and 2.5.2 on Windows.
- **Margins.** All of them are comfortable apart from #4.
- **The CI wiring.** The sentinel, the JSON, the flag and the timeout match, and the net falls
  in shard 1 of 3.

**Not checked:**
- the solver outputs (no cvxpy);
- facts about Atlas;
- the net's behaviour on the GitHub runner;
- the paper's proofs.

## What this does and does not establish

The net is a consistency net for three Gaussian statements of Paper III. It is a C3 harness,
built to fail on known wrong versions (m7), and from this commit it is CI-run. It is not a
proof (CHARTER T-CUST-2). No Paper III result's class changes here. A `[proved]` row would
also need a custody table and a ledger row scoped to what is proved, and both are still
owed.
