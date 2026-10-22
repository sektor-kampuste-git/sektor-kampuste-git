"""
week6 · baslangic/llm.py — uygulamanın model katmanı. Arayüzden bağımsız, test edilebilir.

Kural: st.* burada YOK. Böylece pytest ağ olmadan saf fonksiyonları test eder,
ajan (Copilot/Zed/Cursor) yeni bir görev eklerken yalnızca GOREVLER'e dokunur.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())

# Görev adı → sistem talimatı. Yeni görev eklemek = buraya bir satır eklemek.
GOREVLER: dict[str, str] = {
    "Özetle": "Metni en fazla üç cümlede, metinde olmayan bilgi eklemeden Türkçe özetle.",
    "Anahtar kelimeler": "Metinden en fazla 8 anahtar kelime çıkar; virgülle ayır, başka bir şey yazma.",
    "Soru üret": "Metinden 3 adet çoktan seçmeli soru üret. Her soru için 4 şık ve doğru şıkkı belirt.",
    "Sadeleştir": "Metni 12 yaşındaki bir öğrencinin anlayacağı sadelikte, anlamı bozmadan yeniden yaz.",
}

SISTEM_TEMEL = "Sen dikkatli bir Türkçe metin asistanısın. Yalnızca verilen metinle çalış, uydurma."


@dataclass
class Sonuc:
    icerik: str
    girdi_token: int
    cikti_token: int
    sure_ms: int
    model: str


def prompt_olustur(gorev: str, metin: str) -> list[dict]:
    """Saf fonksiyon: test edilir. Bilinmeyen görev → ValueError."""
    if gorev not in GOREVLER:
        raise ValueError(f"Bilinmeyen görev: {gorev}")
    metin = metin.strip()
    if len(metin) < 20:
        raise ValueError("Metin çok kısa (en az 20 karakter).")
    return [
        {"role": "system", "content": f"{SISTEM_TEMEL} Görev: {GOREVLER[gorev]}"},
        {"role": "user", "content": metin},
    ]


def maliyet_usd(girdi_token: int, cikti_token: int, girdi_fiyat: float, cikti_fiyat: float) -> float:
    """Fiyatlar 1M token başına USD. Saf fonksiyon: test edilir."""
    if min(girdi_token, cikti_token, girdi_fiyat, cikti_fiyat) < 0:
        raise ValueError("Negatif değer olamaz.")
    return (girdi_token * girdi_fiyat + cikti_token * cikti_fiyat) / 1_000_000


def istemci() -> OpenAI:
    base, key = os.getenv("LLM_BASE_URL"), os.getenv("LLM_API_KEY")
    if not base or not key:
        raise RuntimeError("LLM_BASE_URL / LLM_API_KEY tanımlı değil. .env ya da Streamlit secrets kontrol edin.")
    return OpenAI(base_url=base, api_key=key)


def calistir(gorev: str, metin: str, temperature: float = 0.3, max_tokens: int = 600,
             model: str | None = None) -> Sonuc:
    """Tek model çağrısı. Ağ gerektirir; testlerde taklit (mock) edilir."""
    model = model or os.getenv("LLM_MODEL", "gpt-6-luna")
    mesajlar = prompt_olustur(gorev, metin)
    t0 = time.perf_counter()
    yanit = istemci().chat.completions.create(model=model, messages=mesajlar, temperature=temperature, max_tokens=max_tokens)
    u = yanit.usage
    return Sonuc(
        icerik=(yanit.choices[0].message.content or "").strip(),
        girdi_token=u.prompt_tokens if u else 0,
        cikti_token=u.completion_tokens if u else 0,
        sure_ms=round((time.perf_counter() - t0) * 1000),
        model=model,
    )
