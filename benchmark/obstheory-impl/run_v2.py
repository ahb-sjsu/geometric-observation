#!/usr/bin/env python3
"""Run the v2 debug-loop harness on HF-router open-weight models, then grade the final impl on
the hidden held-out oracle. Usage: python run_v2.py [model_id ...]"""
import subprocess
import sys
from pathlib import Path

import requests

from harness import debug_loop

HERE = Path(__file__).resolve().parent
TOKEN = Path(r"C:\Users\abptl\.secrets\ahbond-hf-write.txt").read_text(encoding="utf-8").strip()
URL = "https://router.huggingface.co/v1/chat/completions"
MODELS = [
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "meta-llama/Llama-3.3-70B-Instruct",
    "deepseek-ai/DeepSeek-V3-0324",
]
MAX_ITERS = 4


def hf_generate(model):
    def gen(messages):
        r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"},
                          json={"model": model, "messages": messages,
                                "max_tokens": 4096, "temperature": 0.2}, timeout=300)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    return gen


def main():
    models = sys.argv[1:] or MODELS
    for model in models:
        name = model.split("/")[-1].lower().replace(".", "").replace("-instruct", "")
        out = HERE / "models_v2" / name
        try:
            hist = debug_loop(hf_generate(model), out, max_iters=MAX_ITERS)
            solved = next((h["iter"] for h in hist if h["ok"]), None)
            print(f"[loop] {name}: {len(hist)} iters, self-check {'solved@'+str(solved) if solved else 'unsolved'}")
        except Exception as e:
            print(f"[loop] {name}: FAILED {e}")
            continue
        # grade final impl on the hidden held-out oracle
        g = subprocess.run([sys.executable, str(HERE / "grade.py"), str(out)],
                           capture_output=True, text=True)
        print(g.stdout.strip().splitlines()[-1] if g.stdout else g.stderr[-300:])


if __name__ == "__main__":
    main()
