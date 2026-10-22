"""
week8 · izleme/izleme_demo.py — aynı asistan çağrısı, iki izleme yolu:

  1) LANGFUSE_* anahtarları varsa → Langfuse (cloud.langfuse.com, ücretsiz katman): @observe + OpenAI drop-in
  2) yoksa → yerel_iz.py ile izler/*.jsonl; `python iz_goster.py` ile ağaç olarak oku

Neden? Hafta 1'deki "Değerlendirme yok" ve "Sahibi yok" maddeleri: canlıda hangi prompt sürümü, kaç token, kaç ms,
hangi kullanıcı sorusu hata verdi — bunları görmeden ne iyileştirme ne de maliyet kontrolü yapılabilir.

Kullanım:  python izleme_demo.py "Açılmış kulaklığı iade edebilir miyim?"
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # week8/ → asistan.py
from dotenv import find_dotenv, load_dotenv  # noqa: E402

load_dotenv(find_dotenv())

import asistan  # noqa: E402
from yerel_iz import Iz  # noqa: E402

GIRDI_FIYAT = float(os.getenv("GIRDI_FIYAT", 0.10))   # $/1M, gpt-6-luna varsayılanı
CIKTI_FIYAT = float(os.getenv("CIKTI_FIYAT", 0.50))

LANGFUSE_VAR = bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


def maliyet(girdi: int, cikti: int) -> float:
    return (girdi * GIRDI_FIYAT + cikti * CIKTI_FIYAT) / 1e6


def yerel_izle(soru: str, prompt: str) -> dict:
    with Iz("destek-asistani", kullanici="ogrenci-demo", etiketler={"prompt": prompt, "ortam": "lab"}) as iz:
        with iz.span("girdi-kontrol", girdi=soru) as s:
            if len(soru) > 2000:
                raise ValueError("soru çok uzun")
            s.bitir(cikti="ok")
        with iz.span("model-cagrisi", girdi={"soru": soru, "prompt": prompt}) as s:
            sonuc = asistan.cevapla(soru, prompt)
            s.bitir(cikti=sonuc["cevap"], token=sonuc["girdi_token"] + sonuc["cikti_token"],
                    maliyet_usd=maliyet(sonuc["girdi_token"], sonuc["cikti_token"]))
        with iz.span("cikti-kontrol", girdi=sonuc["cevap"][:80]) as s:
            sizinti = "CANARY-8F2A" in sonuc["cevap"]
            s.bitir(cikti={"canary_sizdi": sizinti})
        sonuc["trace_id"] = iz.id
    return sonuc


def langfuse_izle(soru: str, prompt: str) -> dict:
    """Langfuse v3: @observe dekoratörü trace/span açar; langfuse.openai drop-in model çağrısını otomatik kaydeder."""
    from langfuse import get_client, observe
    from langfuse.openai import OpenAI as IzlenenOpenAI

    @observe(name="destek-asistani")
    def calistir(soru: str, prompt: str) -> dict:
        istemci = IzlenenOpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ["LLM_API_KEY"])
        yanit = istemci.chat.completions.create(
            model=os.getenv("LLM_MODEL", "gpt-6-luna"), temperature=0, max_tokens=300,
            messages=[{"role": "system", "content": asistan.prompt_yukle(prompt)}, {"role": "user", "content": soru}],
            name="model-cagrisi",                      # Langfuse'ta span adı
            metadata={"prompt": prompt, "ortam": "lab"},
        )
        u = yanit.usage
        return {"cevap": yanit.choices[0].message.content, "girdi_token": u.prompt_tokens, "cikti_token": u.completion_tokens}

    sonuc = calistir(soru, prompt)
    get_client().flush()
    sonuc["trace_id"] = "Langfuse arayüzünde (Traces sekmesi)"
    return sonuc


if __name__ == "__main__":
    soru = sys.argv[1] if len(sys.argv) > 1 else "Açılmış kulaklığı iade edebilir miyim?"
    prompt = sys.argv[2] if len(sys.argv) > 2 else "promptlar/v2.txt"
    yol = "Langfuse" if LANGFUSE_VAR else "yerel (izler/*.jsonl)"
    print(f"İzleme: {yol}\n")
    sonuc = langfuse_izle(soru, prompt) if LANGFUSE_VAR else yerel_izle(soru, prompt)
    print(f"CEVAP: {sonuc['cevap']}\n")
    print(f"token: {sonuc['girdi_token']}→{sonuc['cikti_token']} · maliyet ${maliyet(sonuc['girdi_token'], sonuc['cikti_token']):.6f} · trace: {sonuc['trace_id']}")
    if not LANGFUSE_VAR:
        print("Ağacı gör: python iz_goster.py")
