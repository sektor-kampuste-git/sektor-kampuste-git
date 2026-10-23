"""Week 1 lab: one function, two providers, same interface.

Runs the same Turkish prompt against a cloud model (Gemini Flash-Lite via its
OpenAI-compatible endpoint) and a local model (Ollama). Prints tokens, latency, cost.
Set GEMINI_API_KEY in .env or your shell. Ollama must be running locally.

Ders deposu notu: kod önce ortak LLM_BASE_URL / LLM_API_KEY / LLM_MODEL değişkenlerini okur
(kök .env.example); bunlar yoksa Hafta 1'deki gibi GEMINI_API_KEY ile Gemini Flash-Lite kullanır.
"""
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Ortak değişkenler (kök .env) öncelikli; yoksa Hafta 1 varsayılanı: Gemini ücretsiz katmanı.
BASE_URL = os.environ.get("LLM_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
API_KEY = os.environ.get("LLM_API_KEY") or os.environ["GEMINI_API_KEY"]
MODEL = os.environ.get("LLM_MODEL") or "gemini-3.5-flash-lite"
OLLAMA_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")

PROMPT = (
    "Aşağıdaki sözleşme maddesini iki cümlede özetle:\n"
    "Kiracı, kira bedelini her ayın en geç 5'inci gününe kadar kiraya verenin "
    "bildirdiği banka hesabına yatırmakla yükümlüdür. Geç ödeme hâlinde aylık %2 "
    "gecikme faizi uygulanır; üç ay üst üste geç ödeme, kiraya verene sözleşmeyi "
    "tek taraflı fesih hakkı verir."
)

# USD per 1M tokens (input, output). Update from the provider pricing page.
PRICES = {
    "gemini-3.5-flash-lite": (0.30, 2.50),
    "qwen3.5:4b": (0.0, 0.0),
}


def ask(base_url: str, api_key: str, model: str):
    client = OpenAI(base_url=base_url, api_key=api_key)
    t0 = time.perf_counter()
    r = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": PROMPT}]
    )
    dt = time.perf_counter() - t0
    u = r.usage
    pin, pout = PRICES.get(model, (0.0, 0.0))
    cost = (u.prompt_tokens * pin + u.completion_tokens * pout) / 1_000_000
    print(f"\n=== {model} ===")
    print(r.choices[0].message.content.strip())
    print(f"tokens in/out: {u.prompt_tokens}/{u.completion_tokens}  "
          f"latency: {dt:.2f}s  cost: ${cost:.6f}")


if __name__ == "__main__":
    # Cloud: Gemini via OpenAI-compatible endpoint (free tier, Flash/Flash-Lite only)
    ask(BASE_URL, API_KEY, MODEL)
    # Local: Ollama exposes the same API shape on localhost
    try:
        ask(OLLAMA_URL, "ollama", "qwen3.5:4b")
    except Exception as e:  # Ollama kurulu/çalışıyor değilse bulut yarısı yine görülsün
        print(f"\n=== qwen3.5:4b (Ollama) ===\natlandı: {type(e).__name__}: {e}\n"
              "ipucu: 'ollama serve' çalışıyor mu, 'ollama pull qwen3.5:4b' yapıldı mı?")
    # Other OpenAI-compatible options (uncomment and set the key):
    # ask("https://api.groq.com/openai/v1", os.environ["GROQ_API_KEY"], "openai/gpt-oss-20b")
    # ask("https://openrouter.ai/api/v1", os.environ["OPENROUTER_API_KEY"], "qwen/qwen3.5-9b:free")
    # ask(os.environ["FOUNDRY_BASE_URL"], os.environ["FOUNDRY_API_KEY"], os.environ["FOUNDRY_MODEL"])
