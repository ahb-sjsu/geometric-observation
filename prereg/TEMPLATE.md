# Prediction-registry entry — TEMPLATE

Copy to `prereg/GO-<id>-<slug>.md`, fill every field, commit **before** the first
measurement it governs. The git commit timestamp is the binding registration
time; `hash` is the sha256 of this file's body with the `hash:` line blanked.
Amendments only dated-and-logged **before** unblinding (§1.17, §5). Append amendments
and outcomes *after* the sealed text: never edit a sealed line, never re-seal (CHARTER
REG-2), and disclose the change in the registry row and `prereg/SEAL-DISCLOSURES.json`.
Keep exactly one seal line, the `hash:` field in the block below. `scripts/seal.py`
refuses a file in which its pattern matches twice, because it would overwrite the other
match: name other hashes `code_sha256:`, or list them under `instruments_sha256:`.
Check with `python scripts/verify_seals.py`.

```yaml
id: GO-P-2026-###
date: YYYY-MM-DD          # must predate first governed measurement
retrospective: false      # true if the instance's data was already seen (known instance);
                          # then class is at most [replicated]/[demonstrated], never [predicted]
instance:
  representation: ...
  consumer: ...            # functional + how d_O is measured
  q_family: [...]
probe_output:
  invariant: ...
  nuisance: ...
  predicted_failure_class: radial-displacement | direction-concentration | dc-offset | margin-flip | other(amend)
prediction:
  arm_ordering: a > b > c on <downstream metric>
  effect_floor: ...        # registered minimum effect size (not just sign)
design:
  n: ...
  clusters: ...            # independent unit for the clustered CI
  stopping: fixed-n
  bits_matched_via: ...    # external harness where available
controls: [shuffled-consumer, noise-floor]
amendments: []             # dated, pre-unblinding only
hash: sha256:...
```
