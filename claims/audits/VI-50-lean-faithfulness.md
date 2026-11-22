# VI-50: faithfulness of Paper V's Lean statements (2026-11-21)

**Target.** The formal statements and definitions of Paper V's Lean layer, read against
`paper/consumer-relative-landauer.tex`. The question was whether each formal statement says what
the paper claims, not whether the proofs are right (Lean checks those). Versions read, by
sha256 prefix:

| File | sha256 |
|---|---|
| `lean/ObservationTheory/FiniteEntropy.lean` | `0860011b…` |
| `lean/ObservationTheory/EntropyTools.lean` | `9b5e726a…` |
| `lean/ObservationTheory/IidBlocks.lean` | `3d8d3a87…` |
| `lean/ObservationTheory/ConsumerLandauerIdentities.lean` | `0b74cfe7…` |
| `lean/ObservationTheory/ConsumerLandauerBlocks.lean` | `e8da232d…` |
| `paper/consumer-relative-landauer.tex` | `ad5ed7e8…` |

The EntropyTools and IidBlocks hashes are of the working files as read, which had Windows
line endings. The committed blobs, with LF endings, have the same content and hash
`e249b71d…` and `03423625…`.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. It did not compile
anything.

**What it checked and found sound:**
- **The definitions:** `H`, `push` and `condH`. The conditioning variable is always the second
  coordinate, and every use was checked against that.
- **Missing mass-one hypotheses don't change meaning.**
  - For a nonnegative law of mass t, `condH(tρ) = t·condH(ρ)`, and `condMI` scales the same way.
  - Where raw entropy matters, mass one is assumed.
  - Every inequality assumes nonnegativity.
- **The block constructions:** `iid`, `block` and `mask`.
- **The reset order** in `condH_chain` and `cor3m_coordinated`: it is the paper's.
- **`condMI` and `letterLaw`:** `work_converse` is exactly the outer ends of (eq:work-conv).
- **The `hex` hypotheses:**
  - decoding from the joint memory where the paper says so;
  - decoding from `M_j` alone where the paper says so.
- **The factor n,** and the conversion between nats and bits.
- **Deterministic codes:** they are the paper's codes.
- **`chainJoint` and `ageStep`:** they are the laws under `M − X_t − X_{t+1}`.

**Verdict.**
- **No (A) finding:** every formalized statement says what the paper claims, within its
  disclosed scope.
- **The verdict table:**
  - "faithful with listed gaps" for Thm 1's converse step, Thm 2, the exact-tax identity, Cor 3
    and Prop 6;
  - "faithful" for the model;
  - "not formalized (disclosed)" for Thm 1 as a whole.

## Findings and dispositions

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | C | Prop 6's process hypothesis is built into a definition (the iterate of `ageStep`), not proved | **Fixed by a proof.** `pathLaw K q₀ T` is the law `q₀(m, x₀) ∏ₛ K(xₛ, xₛ₊₁)` of `(M, X₀, …, X_T)`. `pathLaw_marginal` proves that its `(M, X_t)` marginal is `(ageStep K)^[t] q₀`, and `stale_monotone_path` states Prop 6 on that process |
| 2 | D | Time homogeneity not stated | Header and docstrings now say "one time-homogeneous kernel", and that `stale_step` covers an inhomogeneous step |
| 3 | B | The `cor3_joint_lower` docstring overstates ("any code") | Reworded: two memories with componentwise decoders. The joint-memory form is `cor3m_joint_lower` |
| 4 | D | Exactness is pointwise, not almost sure | Disclosed in the header and in `exact_lower`'s docstring; the almost-sure reading is listed as not formalized |
| 5 | D | The rate chain is claimed by instantiation only | Reworded: the one-point instantiation gives the rate chain in this encoding, and the reduction of `condH` and `condMI` to `H` and `I` is not stated as a lemma |
| 6 | D | Scope of `L_n ≤ R_n` | The header says that `content_le_log_card` is the first link of (eq:rate-conv) for finite source alphabets, and that the paper's Gaussian use lies outside this scope |
| 7 | D | Other reset orders; coordinated attainment not composed | `cor3m_coordinated_attained` added; the reset order is stated, and other orders are listed as a reindexing not stated |
| 8 | D | Thm 1's not-formalized list incomplete | The distortion coordinate, the region and the intermediate links have been added |
| 9 | D | README out of date; the new modules have no build record | `lean/README.md` rewritten; build record `paper/consumer-relative-landauer-lean-blocks-2026-11-21.txt` for all modules |
| 10 | D | FiniteEntropy header list incomplete | Completed |

**Paper problems exposed (none an error).** These are reported to the author; the paper is
unchanged.
- **P1.** Prop 6's "stationary" hypothesis is unused: any Markov chain suffices. For any
  Markov chain, M independent of the future given X₀ gives M − X_t − X_{t+1} at every t, and
  data processing does the rest. (The Lean statement uses one time-homogeneous kernel; that
  is a feature of the encoding, not of the paper's claim. Corrected after VI-51.)
- **P2.** The randomized-encoder remark (tex 247–248) needs the encoder's randomness to be
  independent of `(Xⁿ, Sⁿ)`.
- **P3.** (eq:exact-tax) does not restate Cor 2's hypothesis that zero distortion means exact
  recovery of `U`.
- **P4.** "Recovers exactly" is ambiguous between pointwise and almost sure. Either reading
  is harmless.

**After the fixes.**
- **Build:** all seven modules compile from scratch with zero `sorry`. They now include
  `BlockLLN.lean` and `Covering.lean`, the first two milestones of the achievability time
  box.
- **Axioms:** all 49 audited theorems depend only on `propext`, `Classical.choice` and
  `Quot.sound`.
- **Build record:** `paper/consumer-relative-landauer-lean-blocks-2026-11-21.txt`.
- **Confirming pass:** VI-51 confirmed the dispositions, the new `pathLaw` bridge included
  (`claims/audits/VI-51-lean-confirming.md`).
