#!/usr/bin/env python
"""Anchor a sealed prereg to a third-party timestamp (PE-CLS-1.0 s7.1.2).

Git ancestry proves ORDER: the seal commit precedes the result commit in the
DAG, verifiable by anyone at any later snapshot.  It does not prove WALL-CLOCK
TIME to a party who does not already trust the repository owner, because the
owner controls the whole history.  Closing that gap needs a timestamp issued
by someone with no stake in the results.

This does NOT require running a blockchain.  Two standard mechanisms, in
increasing order of independence:

  rfc3161   A Time-Stamp Authority signs (hash, time) under RFC 3161.  One
            HTTP round trip, a ~2 KB .tsr token committed beside the prereg,
            verifiable with openssl.  Trust model: the TSA's key.

  ots       OpenTimestamps aggregates your hash into a Merkle tree whose root
            is committed to the Bitcoin blockchain.  You do not run a chain,
            hold coins, or pay fees -- an existing chain is used as a public
            clock.  Trust model: no authority at all.  Proof (~1 KB .ots)
            upgrades to full independence once the block confirms.

Both anchor the SEAL HASH (the content commitment from scripts/seal.py), not
the file, so an anchor survives rebases, renames, and re-serialization.

    python scripts/anchor_seal.py prereg/GO-P-2026-092-foo.md
    python scripts/anchor_seal.py --method ots prereg/...
    python scripts/anchor_seal.py --verify prereg/...
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys

FREE_TSA = "https://freetsa.org/tsr"


def seal_digest(path: str) -> str:
    text = open(path, encoding="utf-8").read()
    m = re.search(r"hash:\s*sha256:([0-9a-f]{64})", text)
    if not m:
        raise SystemExit(f"{path}: not sealed (no full sha256). "
                         f"Run scripts/seal.py first.")
    return m.group(1)


def anchor_rfc3161(digest: str, out: str) -> int:
    if not shutil.which("openssl"):
        print("openssl not found; cannot build an RFC 3161 request", file=sys.stderr)
        return 2
    try:
        import urllib.request
    except ImportError:
        return 2
    tmp_q = out + ".tsq"
    # A request over the ALREADY-COMPUTED digest: the prereg text never leaves
    # the machine, only its hash.
    subprocess.run(["openssl", "ts", "-query", "-digest", digest,
                    "-sha256", "-cert", "-out", tmp_q], check=True)
    req = open(tmp_q, "rb").read()
    rq = urllib.request.Request(FREE_TSA, data=req,
                                headers={"Content-Type": "application/timestamp-query"})
    try:
        with urllib.request.urlopen(rq, timeout=60) as resp:
            open(out, "wb").write(resp.read())
    except Exception as e:                                    # offline is fine
        os.remove(tmp_q)
        print(f"timestamp request failed ({e}). Seal stands; anchor deferred.",
              file=sys.stderr)
        return 1
    os.remove(tmp_q)
    print(f"anchored: {out}  (verify: openssl ts -reply -in {out} -text)")
    return 0


def anchor_ots(digest: str, out: str) -> int:
    if not shutil.which("ots"):
        print("opentimestamps-client not installed "
              "(pip install opentimestamps-client)", file=sys.stderr)
        return 2
    tmp = out + ".digest"
    open(tmp, "wb").write(bytes.fromhex(digest))
    r = subprocess.run(["ots", "stamp", tmp])
    os.remove(tmp) if os.path.exists(tmp) else None
    if os.path.exists(tmp + ".ots"):
        shutil.move(tmp + ".ots", out)
        print(f"anchored: {out}  (upgrade later: ots upgrade {out})")
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("prereg")
    ap.add_argument("--method", choices=["rfc3161", "ots"], default="rfc3161")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()

    digest = seal_digest(a.prereg)
    ext = ".tsr" if a.method == "rfc3161" else ".ots"
    out = os.path.splitext(a.prereg)[0] + ext

    if a.verify:
        if not os.path.exists(out):
            print(f"NO ANCHOR: {out} absent (P1 rests on git ancestry alone)")
            return 1
        print(f"anchor present: {out}")
        if a.method == "rfc3161" and shutil.which("openssl"):
            subprocess.run(["openssl", "ts", "-reply", "-in", out, "-text"])
        elif a.method == "ots" and shutil.which("ots"):
            subprocess.run(["ots", "info", out])
        return 0

    print(f"seal digest: sha256:{digest}")
    return (anchor_rfc3161 if a.method == "rfc3161" else anchor_ots)(digest, out)


if __name__ == "__main__":
    sys.exit(main())
