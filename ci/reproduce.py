#!/usr/bin/env python
"""CI reproduction gate for Geometric Observation (Tier-A: CPU-only, no GPU/Atlas).

Enforces PROTOCOL.md's "CI green" requirement for the [demonstrated]/[replicated]
rows by RE-RUNNING each CPU-only harness and asserting it reproduces the exact
`verdict` dict and `*_supported` flag committed in results/. Verdicts are booleans
with margin, so this is robust across platforms/BLAS. It also:
  * runs the Appendix-B numerical verification (verify_appendixB.py) and asserts PASS;
  * validates that every committed results/*.json parses and its summary flag is
    self-consistent with its verdict dict (tamper check), including the harnesses CI
    cannot re-run (Gate-B needs Atlas+Llama; GO-4/GO-5-ADC need external corpora).

Run from repo root:  python ci/reproduce.py
Exit 0 iff everything green."""
from __future__ import annotations
import json, subprocess, sys, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

# (harness, stdout sentinel, committed json, summary-flag key)
# NOTE: the go2_kv_keys* and go2_embed_retrieval harnesses import `turboquant_pro`
# (a separate research package, not on PyPI), so they are NOT Tier-A self-contained
# and are carried as committed artifacts, re-derived for self-consistency in step [3].
# The GO-2 mechanism is still CI-reproduced here by two independent instances that
# depend only on numpy: retrieval ranking and gradient curvature.
REPRODUCIBLE = [
    ("go1_blinded_probe.py",        "GO1-JSON",   "GO1-blinded-probe.json",        "GO1_supported"),
    ("go2_retrieval_matched_v2.py", "GO2RM2-JSON","GO2-retrieval-matched-v2.json", "GO2_mechanism_replicates"),
    ("go2_gradient_curvature.py",   "GO2GB-JSON", "GO2-gradient-curvature.json",   "GO2_mechanism_generalizes"),
    ("go3_certificate_vacuity_v3.py","GO3-JSON",  "GO3-certificate-vacuity-v3.json","GO3_supported"),
    ("go5_diffusion_distance.py",   "GO5-JSON",   "GO5-diffusion-distance.json",   "GO5_supported"),
    # GO-10 operational face (GO-P-2026-058): pure numpy, deterministic at the
    # governed seed 20260820; default (no-arg) invocation IS the governed mode.
    ("go10_operational_tax.py",     "GO10OP-JSON","GO10-operational-tax.json",     "GO10OP_supported"),
    # GO-10 second source family (GO-P-2026-059), same conventions, seed 20260822.
    ("go10_operational_tax_binary.py","GO10OPB-JSON","GO10-operational-tax-binary.json","GO10OPB_supported"),
    # GO-11 region theorems (GO-P-2026-060): deterministic at governed seed
    # 20260826 (default invocation); ~6 min, keeps the job under its 20-min cap.
    ("verify_go11_region.py",       "GO11-JSON",  "GO11-region.json",              "GO11_supported"),
    # GO-11 encoder-tilt face (GO-P-2026-061), governed seed 20260830, ~1 min.
    ("go11_encoder_tilt.py",        "GO11ET-JSON","GO11-encoder-tilt.json",        "GO11ET_supported"),
    # GO-11 binary tilt family (GO-P-2026-062), governed seed 20260902, ~2 min.
    ("go11_encoder_tilt_binary.py", "GO11ETB-JSON","GO11-encoder-tilt-binary.json","GO11ETB_supported"),
    # GO-11 v0.9 closing theorems (GO-P-2026-063), governed seed 20260906, ~1 min.
    ("verify_go11_rungs.py",        "GO11R-JSON", "GO11-rungs.json",               "GO11R_supported"),
]

failures: list[str] = []


def run(rel_path: str, timeout: int = 600) -> str:
    p = subprocess.run([PY, os.path.join(ROOT, rel_path)], capture_output=True,
                       text=True, timeout=timeout, cwd=ROOT)
    if p.returncode != 0:
        raise RuntimeError(f"{rel_path} exited {p.returncode}\nSTDERR tail:\n{p.stderr[-1500:]}")
    return p.stdout


def extract_json(stdout: str, sentinel: str) -> dict:
    lines = stdout.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == f"==={sentinel}===")
        end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "===END===")
    except StopIteration:
        raise RuntimeError(f"sentinel {sentinel} / ===END=== not found in stdout")
    return json.loads("\n".join(lines[start + 1:end]))


print("=" * 68)
print("[1/3] Appendix-B numerical verification (verify_appendixB.py)")
print("=" * 68)
try:
    out = run("experiments/verify_appendixB.py", timeout=300)
    need = ["B2/B2a VERDICT: PASS", "B3(ii) VERDICT: PASS"]
    missing = [s for s in need if s not in out]
    # B3(i): confirm the last high-res diff is tiny (exact once modes active)
    if missing:
        failures.append(f"verify_appendixB: missing {missing}")
        print("  FAIL:", missing)
    else:
        print("  PASS: B2, B2a, B3(ii) verdicts green")
except Exception as e:
    failures.append(f"verify_appendixB crashed: {e}")
    print("  FAIL:", e)

print()
print("=" * 68)
print("[1b] Two-observer theorem harness (verify_two_observer.py)")
print("=" * 68)
try:
    out = run("experiments/verify_two_observer.py", timeout=180)
    need = ["construction reproduces both optima", "all nested = True",
            "L=R1(D1): OK", "VERDICT: ALL PASS"]
    missing = [s for s in need if s not in out]
    if missing:
        failures.append(f"verify_two_observer: missing {missing}")
        print("  FAIL:", missing)
    else:
        print("  PASS: max-det sufficiency construction, Equitz-Cover recovery, "
              "orthogonal loss L=R1(D1)")
except Exception as e:
    failures.append(f"verify_two_observer crashed: {e}")
    print("  FAIL:", e)

print()
print("=" * 68)
print("[1c] New analytic-result harnesses (region, mismatch, dispersion/separation)")
print("=" * 68)
for h in ("verify_rate_region.py", "verify_observer_mismatch.py",
          "verify_dispersion_separation.py", "verify_go6.py",
          "verify_consumer_landauer.py", "verify_gaussian_sideinfo.py"):
    try:
        out = run(f"experiments/{h}", timeout=900)
        if "VERDICT: ALL PASS" in out:
            print(f"  PASS {h}")
        else:
            failures.append(f"{h}: VERDICT not ALL PASS")
            print(f"  FAIL {h}: VERDICT not ALL PASS")
    except Exception as e:
        failures.append(f"{h} crashed: {e}")
        print(f"  FAIL {h}: {e}")

print()
print("=" * 68)
print("[2/3] Re-run CPU-only harnesses; assert committed verdict reproduces")
print("=" * 68)
for harness, sentinel, jname, flag in REPRODUCIBLE:
    try:
        committed = json.load(open(os.path.join(ROOT, "results", jname)))
        fresh = extract_json(run(f"experiments/{harness}"), sentinel)
        bad = []
        if fresh.get("verdict") != committed.get("verdict"):
            bad.append(f"verdict {fresh.get('verdict')} != committed {committed.get('verdict')}")
        if fresh.get(flag) != committed.get(flag):
            bad.append(f"{flag} {fresh.get(flag)} != committed {committed.get(flag)}")
        if bad:
            failures.append(f"{harness}: " + "; ".join(bad))
            print(f"  FAIL {harness}: {'; '.join(bad)}")
        else:
            print(f"  PASS {harness:32s} verdict + {flag}={committed.get(flag)} reproduced")
    except Exception as e:
        failures.append(f"{harness} crashed: {e}")
        print(f"  FAIL {harness}: {e}")

print()
print("=" * 68)
print("[3/3] Integrity: every results/*.json parses; summary flag == all(verdict)")
print("=" * 68)
for path in sorted(glob.glob(os.path.join(ROOT, "results", "*.json"))):
    name = os.path.basename(path)
    try:
        d = json.load(open(path))
    except Exception as e:
        failures.append(f"{name} does not parse: {e}")
        print(f"  FAIL {name}: parse error {e}")
        continue
    verdict = d.get("verdict")
    flags = [k for k, v in d.items() if isinstance(v, bool)]
    # The summary flag is the boolean named *_supported (house convention).
    # Fall back to a lone boolean only when no *_supported key exists --
    # auxiliary booleans (audit gates like recon_matched_audit_ok, mode flags
    # like pilot) must not be mistaken for the run summary (the GO-P-2026-056
    # lesson: an honest MISS verdict next to a passing audit flag is
    # consistent, not tampered).
    supp = [k for k in flags if k.endswith("_supported")]
    key = supp[0] if len(supp) == 1 else (flags[0] if len(flags) == 1 else None)
    if isinstance(verdict, dict) and verdict and key is not None:
        summary = d[key]
        expect = all(bool(v) for v in verdict.values())
        if summary != expect:
            failures.append(f"{name}: {key}={summary} but all(verdict)={expect}")
            print(f"  FAIL {name}: {key}={summary} inconsistent with verdict")
        else:
            print(f"  ok   {name:34s} {key}={summary}")
    else:
        print(f"  ok   {name:34s} (parsed; no single-flag/verdict pair to cross-check)")

print()
print("=" * 68)
if failures:
    print(f"CI RESULT: FAIL ({len(failures)} problem(s))")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("CI RESULT: GREEN -- Appendix-B verified, all CPU-only claims reproduced, "
      "results self-consistent.")
sys.exit(0)
