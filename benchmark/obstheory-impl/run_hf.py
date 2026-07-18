#!/usr/bin/env python3
"""Query open-weight LLMs via the HuggingFace Inference router (OpenAI-compatible)
with the DOA spec, save each model's impl.py. Usage: python run_hf.py [model_id ...]"""
import re
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
TOKEN = Path(r"C:\Users\abptl\.secrets\ahbond-hf-write.txt").read_text(encoding="utf-8").strip()
SPEC = (HERE / "spec_doa.md").read_text(encoding="utf-8")
URL = "https://router.huggingface.co/v1/chat/completions"

DEFAULT_MODELS = [
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "meta-llama/Llama-3.3-70B-Instruct",
    "deepseek-ai/DeepSeek-V3-0324",
]
SYS = ("You are an expert in array signal processing and numerical Python. Implement the "
       "task from the specification alone. Output ONLY one Python code block (```python ...```) "
       "containing the complete impl.py with a solve(...) function exactly as specified. "
       "Pure numpy + stdlib, deterministic, no file/network access.")


def slug(model):
    return model.split("/")[-1].lower().replace(".", "").replace("-instruct", "")


def extract_code(text):
    blocks = re.findall(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    if blocks:
        return max(blocks, key=len).strip()
    return text.strip()


def query(model):
    r = requests.post(
        URL,
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"model": model,
              "messages": [{"role": "system", "content": SYS},
                           {"role": "user", "content": SPEC}],
              "max_tokens": 4096, "temperature": 0.2},
        timeout=300,
    )
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:400]}")
    return r.json()["choices"][0]["message"]["content"]


def main():
    models = sys.argv[1:] or DEFAULT_MODELS
    for model in models:
        name = slug(model)
        try:
            content = query(model)
            code = extract_code(content)
            d = HERE / "models" / name
            d.mkdir(parents=True, exist_ok=True)
            (d / "impl.py").write_text(code, encoding="utf-8")
            (d / "raw.md").write_text(content, encoding="utf-8")
            print(f"[ok]   {model} -> models/{name}/impl.py ({len(code)} chars)")
        except Exception as e:
            print(f"[FAIL] {model}: {e}")


if __name__ == "__main__":
    main()
