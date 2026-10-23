"""Week 2 lab, step 4: local bake-off of two small models on 10 Turkish questions.

Both models run on Ollama, which exposes the same OpenAI-compatible API on
localhost. Records accuracy (keyword match) and tokens per second, writes
results.csv. Requires: ollama serve, ollama pull qwen3.5:4b, ollama pull vngrs-ai/Kumru-2B
"""
import csv
import json
import os
import time

from openai import OpenAI

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
MODELS = ["vngrs-ai/Kumru-2B", "qwen3.5:4b"]  # edit to match `ollama list`

client = OpenAI(base_url=BASE_URL, api_key="ollama")
with open("questions.json", encoding="utf-8") as f:
    QS = json.load(f)


def ask(model: str, question: str):
    t0 = time.perf_counter()
    r = client.chat.completions.create(
        model=model,
        temperature=0,
        max_tokens=120,
        messages=[{"role": "user", "content": question}],
    )
    dt = time.perf_counter() - t0
    text = r.choices[0].message.content or ""
    return text, r.usage.completion_tokens / dt if dt else 0.0


rows = []
for model in MODELS:
    hits, speeds = 0, []
    print(f"\n===== {model} =====")
    for q in QS:
        text, tps = ask(model, q["q"])
        ok = any(k.lower() in text.lower() for k in q["keywords"])
        hits += ok
        speeds.append(tps)
        rows.append([model, q["id"], ok, round(tps, 1), text.strip()[:120]])
        print(f"{'OK ' if ok else 'MISS'} q{q['id']:02d} {tps:5.1f} tok/s | {text.strip()[:90]!r}")
    print(f"--> {model}: accuracy {hits}/{len(QS)}  avg {sum(speeds) / len(speeds):.1f} tok/s")

with open("results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["model", "question_id", "correct", "tokens_per_s", "answer"])
    w.writerows(rows)
print("\nwrote results.csv")
