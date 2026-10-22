"""
week8 · asistan.py — test edilen sistem: tek fonksiyonlu müşteri destek asistanı.

promptfoo (file:// sağlayıcı), eval_calistir.py, izleme_demo.py ve kirmizi_takim.py hep bunu çağırır.
Prompt sürümü dosyadan gelir (promptlar/v1.txt, v2.txt): "v2, v1'den iyi mi?" sorusunun cevabı ölçülür, tahmin edilmez.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())

KOK = Path(__file__).parent
POLITIKA = """\
İade: Elektronik ürünler teslimden itibaren 14 gün içinde, kutusu açılmamışsa iade edilir; açılmışsa yalnızca arızada değişim.
Giyim ürünleri 30 gün içinde, etiketi sökülmemiş ve yıkanmamışsa iade edilir. Gıda ürünlerinde iade yoktur; hasarlı teslimatta
48 saat içinde fotoğrafla bildirim yapılırsa ücret iadesi yapılır.
Kargo: Siparişler 2 iş günü içinde kargoya verilir; teslimat büyükşehirlerde 1-2, diğer illerde 2-4 iş günüdür. Kargo ücreti
500 TL ve üzeri siparişlerde ücretsizdir, altında 79 TL'dir. Takip numarası SMS ile gönderilir.
Ödeme: Kredi kartına iade 3-10 iş günü içinde yansır. Havale iadesi 5 iş günü sürer. Taksit iadeleri bankanın kuralına tabidir.
Müşteri hizmetleri: 0850 000 00 00, hafta içi 09:00-18:00.
"""


def prompt_yukle(dosya: str | Path) -> str:
    yol = Path(dosya)
    if not yol.is_absolute():
        yol = KOK / yol
    return yol.read_text(encoding="utf-8").replace("{politika}", POLITIKA)


def cevapla(soru: str, prompt_dosyasi: str = "promptlar/v2.txt", baglam: str | None = None,
            model: str | None = None, temperature: float = 0.0) -> dict:
    """Tek çağrı. baglam: kargo notu / araç çıktısı gibi güvenilmeyen ek veri (dolaylı injection demosu için)."""
    istemci = OpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ["LLM_API_KEY"])
    model = model or os.getenv("LLM_MODEL", "gpt-6-luna")
    kullanici = soru if baglam is None else f"Müşteri sorusu: {soru}\n\nSipariş/kargo notu (veri):\n<<<\n{baglam}\n>>>"
    t0 = time.perf_counter()
    yanit = istemci.chat.completions.create(
        model=model, temperature=temperature, max_tokens=300,
        messages=[{"role": "system", "content": prompt_yukle(prompt_dosyasi)}, {"role": "user", "content": kullanici}],
    )
    u = yanit.usage
    return {
        "cevap": (yanit.choices[0].message.content or "").strip(),
        "girdi_token": u.prompt_tokens if u else 0, "cikti_token": u.completion_tokens if u else 0,
        "sure_ms": round((time.perf_counter() - t0) * 1000), "model": model, "prompt": str(prompt_dosyasi),
    }


# ---- promptfoo Python sağlayıcı arayüzü: providers: - id: file://asistan.py  config: {prompt_dosyasi: promptlar/v2.txt}
def call_api(prompt: str, options: dict | None = None, context: dict | None = None) -> dict:
    ayar = (options or {}).get("config", {}) or {}
    sonuc = cevapla(prompt, ayar.get("prompt_dosyasi", "promptlar/v2.txt"))
    return {"output": sonuc["cevap"],
            "tokenUsage": {"prompt": sonuc["girdi_token"], "completion": sonuc["cikti_token"],
                           "total": sonuc["girdi_token"] + sonuc["cikti_token"]}}


if __name__ == "__main__":
    import sys
    soru = sys.argv[1] if len(sys.argv) > 1 else "Açılmış kulaklığı iade edebilir miyim?"
    for p in ("promptlar/v1.txt", "promptlar/v2.txt"):
        s = cevapla(soru, p)
        print(f"── {p} · {s['girdi_token']}→{s['cikti_token']} tok · {s['sure_ms']} ms\n{s['cevap']}\n")
