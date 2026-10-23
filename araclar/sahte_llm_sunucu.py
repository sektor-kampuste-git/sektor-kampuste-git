"""
Sahte (çevrimdışı) OpenAI uyumlu LLM sunucusu.

Ne işe yarar?
  * Sınıfta ağ çökerse demolar yine çalışır: aynı istemci kodu, aynı endpoint biçimi.
  * Anahtar gerektirmeden lab kodunu uçtan uca denemek için.
  * Gerçek bir model DEĞİLDİR: yanıtları kurallarla üretir, "zeki" değildir.

Uçlar (OpenAI ile aynı biçim):
  GET  /v1/models
  POST /v1/chat/completions   (tools / tool_calls, response_format, stream desteklenir)
  POST /v1/embeddings          (deterministik, kelime örtüşmesine dayalı vektörler)

Çalıştırma:
  python araclar/sahte_llm_sunucu.py            # http://127.0.0.1:8080/v1
  PORT=9000 python araclar/sahte_llm_sunucu.py

.env:
  LLM_BASE_URL=http://localhost:8080/v1
  LLM_API_KEY=sahte
  LLM_MODEL=sahte-model
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import time
import uuid
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI(title="Sahte LLM Sunucusu", version="1.0")

GECIKME_MS = int(os.getenv("SAHTE_GECIKME_MS", "150"))
MODELLER = ["sahte-model", "sahte-ucuz", "sahte-amiral", "sahte-embedding"]


# ----------------------------------------------------------------- yardımcılar
def _metin(icerik: Any) -> str:
    """OpenAI mesaj içeriği string ya da parça listesi olabilir; düz metne indir."""
    if icerik is None:
        return ""
    if isinstance(icerik, str):
        return icerik
    if isinstance(icerik, list):
        return " ".join(p.get("text", "") for p in icerik if isinstance(p, dict))
    return str(icerik)


def _token_say(metin: str) -> int:
    # Kaba tahmin: ~4 karakter = 1 token (Türkçe için biraz daha fazla token çıkar)
    return max(1, math.ceil(len(metin) / 3.5))


def _ornek_deger(sema: dict[str, Any]) -> Any:
    """JSON şemasından örnek bir değer üret (tool argümanları / yapılandırılmış çıktı)."""
    if not isinstance(sema, dict):
        return None
    if "enum" in sema and sema["enum"]:
        return sema["enum"][0]
    tip = sema.get("type")
    if isinstance(tip, list):
        tip = [t for t in tip if t != "null"][0] if tip else "string"
    if tip == "object" or "properties" in sema:
        return {k: _ornek_deger({**v, "_ad": k}) if isinstance(v, dict) else None
                for k, v in (sema.get("properties") or {}).items()}
    if tip == "array":
        eleman = sema.get("items", {"type": "string"})
        return [_ornek_deger(eleman)]
    if tip == "integer":
        return 3
    if tip == "number":
        return 2.5
    if tip == "boolean":
        return True
    # string
    if sema.get("format") in ("date", "date-time"):
        return "2026-09-12" if sema.get("format") == "date" else "2026-09-12T10:00:00Z"
    aciklama = (sema.get("description") or "").lower()
    if "şehir" in aciklama or "sehir" in aciklama or "city" in aciklama:
        return "İstanbul"
    ad = (sema.get("_ad") or "").lower()
    if "tarih" in aciklama or "date" in aciklama or ad in ("date", "tarih"):
        return "2026-09-12"
    if ad in ("title", "baslik", "başlık"):
        return "Örnek başlık"
    if "id" in aciklama or "numara" in aciklama or "no" == aciklama.strip():
        return "SIP-1001"
    return "örnek"


def _mesajdan_sema(metin: str) -> dict[str, Any] | None:
    """Prompt metnine gömülü bir JSON şeması ("properties" içeren nesne) varsa onu döndür."""
    if not metin or '"properties"' not in metin:
        return None
    basla = metin.find("{")
    while basla != -1:
        derinlik = 0
        for i in range(basla, len(metin)):
            if metin[i] == "{":
                derinlik += 1
            elif metin[i] == "}":
                derinlik -= 1
                if derinlik == 0:
                    try:
                        aday = json.loads(metin[basla:i + 1])
                    except json.JSONDecodeError:
                        break
                    if isinstance(aday, dict) and "properties" in aday:
                        return aday
                    break
        basla = metin.find("{", basla + 1)
    return None


def _arac_sec(araclar: list[dict], kullanici_metni: str) -> dict:
    """Kullanıcı metnindeki kelimelere en çok benzeyen aracı seç; yoksa ilkini."""
    metin = kullanici_metni.lower()
    en_iyi, puan = araclar[0], -1
    for a in araclar:
        fn = a.get("function", a)
        ad = fn.get("name", "")
        kelimeler = set(re.split(r"[_\s]+", ad.lower())) | set(
            re.findall(r"\w+", (fn.get("description") or "").lower())
        )
        p = sum(1 for k in kelimeler if len(k) > 3 and k in metin)
        if p > puan:
            en_iyi, puan = a, p
    return en_iyi


def _sahte_cevap(model: str, kullanici: str, sistem: str, arac_ciktilari: list[str]) -> str:
    if arac_ciktilari:
        return (
            "Araçlardan gelen sonuçlara göre: "
            + " | ".join(c[:200] for c in arac_ciktilari)
            + ". (Sahte sunucu: araç çıktısını özetledim.)"
        )
    ilk_cumle = re.split(r"(?<=[.!?])\s+", kullanici.strip())[0][:160] if kullanici else ""
    return (
        f"[SAHTE YANIT · {model}] Sorunuzu aldım: \"{ilk_cumle}\". "
        "Bu çevrimdışı sahte sunucudur; gerçek bir model yerine örnek bir yanıt üretir. "
        "Gerçek modele geçmek için .env içindeki LLM_BASE_URL değerini değiştirin."
        + (" (Sistem promptu uygulandı.)" if sistem else "")
    )


# ------------------------------------------------------------------- uçlar
@app.get("/v1/models")
def modeller():
    return {"object": "list", "data": [{"id": m, "object": "model", "owned_by": "sahte"} for m in MODELLER]}


@app.post("/v1/chat/completions")
async def chat(req: Request):
    body = await req.json()
    msgs: list[dict] = body.get("messages", [])
    model = body.get("model", "sahte-model")
    araclar = body.get("tools") or []
    tool_choice = body.get("tool_choice", "auto")
    time.sleep(GECIKME_MS / 1000)

    sistem = " ".join(_metin(m.get("content")) for m in msgs if m.get("role") in ("system", "developer"))
    kullanici = ""
    arac_ciktilari: list[str] = []
    for m in reversed(msgs):
        if m.get("role") == "user":
            kullanici = _metin(m.get("content"))
            break
        if m.get("role") == "tool":
            arac_ciktilari.insert(0, _metin(m.get("content")))

    son_rol = msgs[-1].get("role") if msgs else None
    prompt_tokens = sum(_token_say(_metin(m.get("content"))) for m in msgs) + _token_say(json.dumps(araclar))

    # 1) Araç çağrısı: araç tanımı var ve son mesaj kullanıcıdan geldiyse bir araç çağır
    if araclar and son_rol == "user" and tool_choice != "none":
        secilen = _arac_sec(araclar, kullanici)
        fn = secilen.get("function", secilen)
        if isinstance(tool_choice, dict):  # belirli bir araç zorlanmış
            istenen = tool_choice.get("function", {}).get("name")
            for a in araclar:
                if a.get("function", {}).get("name") == istenen:
                    fn = a["function"]
        args = _ornek_deger(fn.get("parameters") or {"type": "object", "properties": {}})
        mesaj = {
            "role": "assistant",
            "content": None,
            "tool_calls": [{
                "id": "call_" + uuid.uuid4().hex[:8],
                "type": "function",
                "function": {"name": fn["name"], "arguments": json.dumps(args, ensure_ascii=False)},
            }],
        }
        bitis = "tool_calls"
        completion_tokens = _token_say(json.dumps(args))
    else:
        # 2) Yapılandırılmış çıktı istendiyse şemaya uygun JSON üret
        rf = body.get("response_format") or {}
        if rf.get("type") == "json_schema":
            sema = (rf.get("json_schema") or {}).get("schema") or {}
            icerik = json.dumps(_ornek_deger(sema) or {"cevap": "örnek"}, ensure_ascii=False)
        elif rf.get("type") == "json_object":
            # Instructor (Mode.JSON) şemayı sistem mesajına gömer; bulursak ona uy
            sema = _mesajdan_sema(sistem) or _mesajdan_sema(kullanici)
            if sema:
                icerik = json.dumps(_ornek_deger(sema) or {"cevap": "örnek"}, ensure_ascii=False)
            else:
                icerik = json.dumps({"cevap": _sahte_cevap(model, kullanici, sistem, arac_ciktilari)}, ensure_ascii=False)
        else:
            icerik = _sahte_cevap(model, kullanici, sistem, arac_ciktilari)
        mesaj = {"role": "assistant", "content": icerik}
        bitis = "stop"
        completion_tokens = _token_say(icerik)

    kimlik = "chatcmpl-" + uuid.uuid4().hex[:12]
    olusturma = int(time.time())
    usage = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
    }

    if body.get("stream"):
        def akis():
            def parca(delta: dict, finish: str | None = None, usage_: dict | None = None):
                veri = {
                    "id": kimlik, "object": "chat.completion.chunk", "created": olusturma, "model": model,
                    "choices": [{"index": 0, "delta": delta, "finish_reason": finish}],
                }
                if usage_ is not None:
                    veri["usage"] = usage_
                return f"data: {json.dumps(veri, ensure_ascii=False)}\n\n"

            yield parca({"role": "assistant"})
            if mesaj.get("tool_calls"):
                tc = mesaj["tool_calls"][0]
                yield parca({"tool_calls": [{"index": 0, **tc}]})
            else:
                # kelime kelime akıt ki "streaming" hissi olsun
                for kelime in mesaj["content"].split(" "):
                    yield parca({"content": kelime + " "})
            yield parca({}, bitis, usage if (body.get("stream_options") or {}).get("include_usage") else None)
            yield "data: [DONE]\n\n"

        return StreamingResponse(akis(), media_type="text/event-stream")

    return {
        "id": kimlik, "object": "chat.completion", "created": olusturma, "model": model,
        "choices": [{"index": 0, "message": mesaj, "finish_reason": bitis}],
        "usage": usage,
    }


@app.post("/v1/embeddings")
async def embeddings(req: Request):
    """Deterministik vektörler: aynı metin → aynı vektör; ortak kelime/3-gram → benzer vektör."""
    body = await req.json()
    girdi = body.get("input", "")
    metinler = girdi if isinstance(girdi, list) else [girdi]
    boyut = int(body.get("dimensions") or 256)

    def vektor(metin: str) -> list[float]:
        v = [0.0] * boyut
        for kelime in re.findall(r"\w+", metin.lower()):
            parcalar = [kelime] + [kelime[i:i + 3] for i in range(max(1, len(kelime) - 2))]
            for p in parcalar:
                h = int(hashlib.md5(p.encode("utf-8")).hexdigest(), 16)
                v[h % boyut] += 1.0 if (h >> 8) & 1 else -1.0
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / norm for x in v]

    veri = [{"object": "embedding", "index": i, "embedding": vektor(m)} for i, m in enumerate(metinler)]
    toplam = sum(_token_say(m) for m in metinler)
    return {"object": "list", "data": veri, "model": body.get("model", "sahte-embedding"),
            "usage": {"prompt_tokens": toplam, "total_tokens": toplam}}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8080"))
    print(f"Sahte LLM sunucusu: http://127.0.0.1:{port}/v1  (Ctrl+C ile durdurun)")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
