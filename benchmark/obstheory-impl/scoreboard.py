#!/usr/bin/env python3
"""Aggregate models/*/score.json into a ranked scoreboard (prints + writes scoreboard.md/json)."""
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
ORIGIN = {  # provenance of each candidate
    "claude": "API / frontier (Claude, isolated spec-only subagent)",
    "qwen25-coder-32b": "API / open-weight (HF router)",
    "llama-33-70b": "API / open-weight (HF router)",
    "deepseek-v3-0324": "API / open-weight (HF router)",
    "nrp-qwen25-coder-7b": "NRP / open-weight (A10 burst Job, vLLM)",
}


def main():
    rows = []
    for sj in sorted(HERE.glob("models/*/score.json")):
        d = json.loads(sj.read_text(encoding="utf-8"))
        rows.append(d)
    rows.sort(key=lambda d: (-d.get("passed", 0), d.get("candidate", "")))

    lines = ["# ObsTheory-Impl / DOA — scoreboard", "",
             "Task: derive the read operator and reproduce the DOA Gate-B flip + omission floor",
             "from spec alone. Graded on the sealed held-out instance (M=16, θ0=-7°, κ=4).", "",
             "| Rank | Model | Source | Score | Verdict | cos | flip | ratios | shuf | omit× |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for i, d in enumerate(rows, 1):
        det = d.get("detail", {})
        src = ORIGIN.get(d["candidate"], "?")
        if "error" in d:
            lines.append(f"| {i} | `{d['candidate']}` | {src} | {d['passed']}/{d['total']} | "
                         f"**{d['verdict']}** | — | — | — | — | — |")
        else:
            lines.append(
                f"| {i} | `{d['candidate']}` | {src} | {d['passed']}/{d['total']} | "
                f"{d['verdict']} | {det.get('cos_read_ghat','?')} | {det.get('flip','?')} | "
                f"{det.get('mse_step_ratios','?')} | {det.get('shuffled_flip','?')} | "
                f"{det.get('omission_floor_mult','?')} |")
    md = "\n".join(lines) + "\n"
    (HERE / "scoreboard.md").write_text(md, encoding="utf-8")
    (HERE / "scoreboard.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
