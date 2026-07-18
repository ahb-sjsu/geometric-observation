import os
from vllm import LLM, SamplingParams

SYS = ("You are an expert in array signal processing and numerical Python. Implement the task "
       "from the specification alone. Output ONLY one Python code block containing the complete "
       "impl.py with a solve(...) function exactly as specified. Pure numpy + stdlib, "
       "deterministic, no file/network access.")

spec = open("/work/spec_doa.md").read()
model = os.environ.get("MODEL", "Qwen/Qwen2.5-Coder-7B-Instruct")
llm = LLM(model=model, dtype="float16", gpu_memory_utilization=0.90, max_model_len=8192)
out = llm.chat(
    [{"role": "system", "content": SYS}, {"role": "user", "content": spec}],
    SamplingParams(temperature=0.2, max_tokens=4096),
)
print("__CODE_START__")
print(out[0].outputs[0].text)
print("__CODE_END__")
