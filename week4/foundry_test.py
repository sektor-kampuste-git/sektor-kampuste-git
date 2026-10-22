"""
week4 · foundry_test.py — aynı Türkçe prompt, birden çok model / arka uç.

Ne gösterir?
  Her model için: yanıt, girdi/çıktı token sayısı, gecikme ve fiyat tablosuna göre maliyet.
  "Hizmet olarak model" (MaaS) fikrinin somut hali: tek OpenAI uyumlu istemci, farklı endpoint'ler.

Kullanım:
  python foundry_test.py                              # .env'deki LLM_MODEL ile tek çalıştırma
  python foundry_test.py --model gpt-6-luna --model deepseek-v4.1-flash   # aynı endpoint'teki birden çok deployment
  python foundry_test.py --ollama qwen3.5:4b          # yerel modeli de tabloya ekle
  python foundry_test.py --ekstra "https://generativelanguage.googleapis.com/v1beta/openai/|GEMINI_API_KEY|gemini-3.5-flash-lite"

.env (repo kökünde):  LLM_BASE_URL, LLM_API_KEY, LLM_MODEL
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())

MADDE = (
    "Madde 7 — Gizlilik. Taraflar, bu sözleşme kapsamında birbirlerine ilettikleri her türlü ticari, teknik ve "
    "finansal bilgiyi gizli tutmayı, üçüncü kişilerle paylaşmamayı ve yalnızca sözleşmenin ifası amacıyla "
    "kullanmayı kabul eder. Bu yükümlülük sözleşmenin sona ermesinden itibaren üç (3) yıl boyunca devam eder. "
    "Kamuya mal olmuş bilgiler, yasal bir zorunluluk nedeniyle açıklanması gereken bilgiler ve alıcı tarafın "
    "bağımsız olarak geliştirdiğini belgeleyebildiği bilgiler bu kapsamın dışındadır. Gizlilik yükümlülüğünün "
    "ihlali halinde ihlal eden taraf, diğer tarafın uğradığı doğrudan zararları tazmin eder."
)
PROMPT = (
    "Aşağıdaki sözleşme maddesini en fazla iki cümlede Türkçe özetle. "
    "Metinde olmayan hiçbir süre, tutar veya koşul EKLEME.\n\n" + MADDE
)


def fiyat_tablosu() -> dict[str, dict]:
    yol = Path(__file__).with_name("fiyatlar.json")
    veri = json.loads(yol.read_text(encoding="utf-8"))
    return {m["id"].lower(): m for m in veri["modeller"]}


def fiyat_bul(model: str, tablo: dict[str, dict]) -> dict | None:
    m = model.lower()
    if m in tablo:
        return tablo[m]
    for kimlik, satir in tablo.items():        # deployment adı fiyat kimliğini içeriyorsa (gpt-6-luna-eu gibi)
        kisa = kimlik.split("/")[-1]
        if kisa in m or m in kisa:
            return satir
    return None


def sor(base_url: str, api_key: str, model: str, tablo: dict[str, dict]) -> dict:
    istemci = OpenAI(base_url=base_url, api_key=api_key)
    t0 = time.perf_counter()
    yanit = istemci.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": PROMPT}],
        temperature=0.2,
    )
    sure = time.perf_counter() - t0
    u = yanit.usage
    girdi, cikti = (u.prompt_tokens, u.completion_tokens) if u else (0, 0)
    fiyat = fiyat_bul(model, tablo)
    maliyet = (girdi * fiyat["girdi"] + cikti * fiyat["cikti"]) / 1e6 if fiyat else None
    return {
        "model": model, "endpoint": base_url.split("/")[2], "cevap": (yanit.choices[0].message.content or "").strip(),
        "girdi": girdi, "cikti": cikti, "sure_ms": round(sure * 1000), "maliyet_usd": maliyet,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", action="append", help="Aynı endpoint'te denenecek model/deployment adı (tekrarlanabilir)")
    p.add_argument("--ollama", metavar="MODEL", help="Yerel Ollama modelini de ekle (örn. qwen3.5:4b)")
    p.add_argument("--ekstra", action="append", default=[],
                   help='Ek arka uç: "base_url|API_KEY_ENV_ADI|model" biçiminde (tekrarlanabilir)')
    p.add_argument("--json", action="store_true", help="Tabloyu JSON olarak yaz")
    a = p.parse_args()

    base = os.getenv("LLM_BASE_URL")
    key = os.getenv("LLM_API_KEY")
    if not base or not key:
        raise SystemExit("LLM_BASE_URL ve LLM_API_KEY tanımlı değil. Repo kökündeki .env.example dosyasını .env olarak kopyalayın.")

    hedefler: list[tuple[str, str, str]] = []
    for m in a.model or [os.getenv("LLM_MODEL", "gpt-6-luna")]:
        hedefler.append((base, key, m))
    if a.ollama:
        hedefler.append(("http://localhost:11434/v1", "ollama", a.ollama))
    for e in a.ekstra:
        url, key_env, model = e.split("|")
        anahtar = os.getenv(key_env)
        if not anahtar:
            print(f"UYARI: {key_env} ortam değişkeni boş; {model} atlanıyor.")
            continue
        hedefler.append((url, anahtar, model))

    tablo = fiyat_tablosu()
    sonuclar = []
    for url, k, m in hedefler:
        try:
            sonuclar.append(sor(url, k, m, tablo))
        except Exception as hata:  # noqa: BLE001 — derste hatayı tabloda görmek istiyoruz
            sonuclar.append({"model": m, "endpoint": url.split("/")[2], "hata": str(hata)[:140]})

    if a.json:
        print(json.dumps(sonuclar, ensure_ascii=False, indent=2))
        return

    print("\nPROMPT:", PROMPT[:90].replace("\n", " "), "...\n")
    print(f"{'model':28} {'endpoint':34} {'girdi':>6} {'çıktı':>6} {'ms':>6} {'maliyet/istek':>14}")
    print("-" * 100)
    for s in sonuclar:
        if "hata" in s:
            print(f"{s['model']:28} {s['endpoint']:34} HATA: {s['hata']}")
            continue
        m = f"${s['maliyet_usd']:.6f}" if s["maliyet_usd"] is not None else "fiyat yok"
        print(f"{s['model']:28} {s['endpoint']:34} {s['girdi']:>6} {s['cikti']:>6} {s['sure_ms']:>6} {m:>14}")
    print()
    for s in sonuclar:
        if "cevap" in s:
            print(f"── {s['model']} ──\n{s['cevap']}\n")
    print("Kontrol: metinde OLMAYAN bir süre/tutar/koşul uyduran model var mı? (3 yıl ve 'doğrudan zarar' metinde var.)")


if __name__ == "__main__":
    main()
