"""Week 2 lab, step 3: the same Turkish prompt at temperature 0, 0.7 and 1.5.

Uses Gemini Flash through its OpenAI-compatible endpoint (free tier).
Swap BASE_URL / MODEL to run the identical sweep on Ollama, Groq or Foundry.
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Ortak değişkenler (kök .env) öncelikli; yoksa Hafta 2 varsayılanı: Gemini 3.5 Flash ücretsiz katmanı.
BASE_URL = os.environ.get("LLM_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL = os.environ.get("LLM_MODEL") or os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
API_KEY = os.environ.get("LLM_API_KEY") or os.environ["GEMINI_API_KEY"]
# Local alternative (no key, slower):
# BASE_URL, MODEL, API_KEY = "http://localhost:11434/v1", "qwen3.5:4b", "ollama"

PROMPT = (
    "Ankara'daki bir öğrenciye, ilk stajı için üç cümlelik bir tavsiye yaz. "
    "Somut ol ve bir Türk şirketinden örnek ver."
)

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

for temperature in (0.0, 0.7, 1.5):
    print(f"\n===== temperature = {temperature} =====")
    for run in range(1, 4):
        r = client.chat.completions.create(
            model=MODEL,
            temperature=temperature,
            max_tokens=150,
            messages=[{"role": "user", "content": PROMPT}],
        )
        text = r.choices[0].message.content.strip().replace("\n", " ")
        print(f"[run {run}] {text}")

print(
    "\nYour verdict (write it in the class channel):\n"
    "  T=0   : identical? ______\n"
    "  T=0.7 : same meaning, different wording? ______\n"
    "  T=1.5 : wrong facts / other languages / nonsense? ______"
)
