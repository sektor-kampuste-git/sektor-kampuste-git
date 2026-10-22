"""
week4 · ozetleyici — Türkçe metin özetleyen küçük bir API + tek sayfalık arayüz.

Amaç: "modeli kiraladık, şimdi onu bir ürün gibi bulutta yayınlayalım" adımını göstermek.
Aynı kod yerelde (uvicorn), Docker'da ve Azure Container Apps'te değişmeden çalışır.

Çalıştırma (yerel):
  pip install -r requirements.txt
  uvicorn app:app --reload --port 8000      # http://127.0.0.1:8000
Ortam değişkenleri: LLM_BASE_URL, LLM_API_KEY, LLM_MODEL  (repo kökündeki .env okunur)
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv(find_dotenv())

app = FastAPI(title="Özetleyici", version="1.0", description="Bulut Bilişim ve Yapay Zeka · week4 demo")

MODEL = os.getenv("LLM_MODEL", "gpt-6-luna")


def istemci() -> OpenAI:
    base, key = os.getenv("LLM_BASE_URL"), os.getenv("LLM_API_KEY")
    if not base or not key:
        raise HTTPException(500, "LLM_BASE_URL / LLM_API_KEY ayarlı değil (ortam değişkeni veya .env).")
    return OpenAI(base_url=base, api_key=key)


def fiyat(model: str) -> dict | None:
    """fiyatlar.json bir üst klasörde (week4/) durur; konteynerde kopyası yanımızda."""
    for yol in (Path(__file__).with_name("fiyatlar.json"), Path(__file__).parent.parent / "fiyatlar.json"):
        if yol.exists():
            for m in json.loads(yol.read_text(encoding="utf-8"))["modeller"]:
                kisa = m["id"].split("/")[-1].lower()
                if kisa in model.lower() or model.lower() in kisa:
                    return m
    return None


class Istek(BaseModel):
    metin: str = Field(min_length=20, max_length=20000, description="Özetlenecek Türkçe metin")
    cumle: int = Field(default=2, ge=1, le=6, description="Özet kaç cümle olsun")


class Yanit(BaseModel):
    ozet: str
    model: str
    girdi_token: int
    cikti_token: int
    sure_ms: int
    maliyet_usd: float | None


@app.get("/saglik")
def saglik():
    base = os.getenv("LLM_BASE_URL", "")
    return {"durum": "ok", "model": MODEL, "endpoint": base.split("/")[2] if "//" in base else base}


@app.post("/ozetle", response_model=Yanit)
def ozetle(istek: Istek):
    t0 = time.perf_counter()
    try:
        yanit = istemci().chat.completions.create(
            model=MODEL,
            temperature=0.2,
            max_tokens=300,
            messages=[
                {"role": "system", "content": "Sen dikkatli bir Türkçe özetleyicisin. Metinde olmayan bilgi ekleme."},
                {"role": "user", "content": f"Aşağıdaki metni en fazla {istek.cumle} cümlede özetle:\n\n{istek.metin}"},
            ],
        )
    except Exception as hata:  # noqa: BLE001
        raise HTTPException(502, f"Model çağrısı başarısız: {hata}") from hata
    sure = round((time.perf_counter() - t0) * 1000)
    u = yanit.usage
    girdi, cikti = (u.prompt_tokens, u.completion_tokens) if u else (0, 0)
    f = fiyat(MODEL)
    maliyet = (girdi * f["girdi"] + cikti * f["cikti"]) / 1e6 if f else None
    return Yanit(ozet=(yanit.choices[0].message.content or "").strip(), model=MODEL,
                 girdi_token=girdi, cikti_token=cikti, sure_ms=sure, maliyet_usd=maliyet)


SAYFA = """<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Özetleyici</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:system-ui,sans-serif;max-width:720px;margin:40px auto;padding:0 16px;color:#1f2933}
textarea{width:100%;height:180px;font:inherit;padding:10px;border:1px solid #cbd2d9;border-radius:8px}
button{background:#0f62fe;color:#fff;border:0;padding:10px 18px;border-radius:8px;font:inherit;cursor:pointer}
pre{background:#f5f7fa;padding:12px;border-radius:8px;white-space:pre-wrap}.meta{color:#52606d;font-size:.9em}</style></head>
<body><h1>Özetleyici</h1><p class="meta">week4 demo · model: <b>__MODEL__</b> · aynı kod: yerel → Docker → Azure Container Apps</p>
<textarea id="m" placeholder="Türkçe bir metin yapıştırın (en az 20 karakter)..."></textarea><br><br>
<label>Cümle: <input id="c" type="number" value="2" min="1" max="6" style="width:60px"></label>
<button onclick="git()">Özetle</button>
<h3>Sonuç</h3><pre id="o">—</pre><p class="meta" id="meta"></p>
<script>async function git(){const o=document.getElementById('o');o.textContent='...';
const r=await fetch('/ozetle',{method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({metin:document.getElementById('m').value,cumle:+document.getElementById('c').value})});
const d=await r.json(); if(!r.ok){o.textContent='Hata: '+(d.detail||r.status);return;}
o.textContent=d.ozet; document.getElementById('meta').textContent=
`${d.model} · girdi ${d.girdi_token} tok · çıktı ${d.cikti_token} tok · ${d.sure_ms} ms · `+(d.maliyet_usd==null?'fiyat yok':'$'+d.maliyet_usd.toFixed(6));}</script>
</body></html>"""


@app.get("/", response_class=HTMLResponse)
def anasayfa():
    return SAYFA.replace("__MODEL__", MODEL)
