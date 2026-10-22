"""
week7 · ajan_dongusu.py — sıfırdan, bütçeli bir araç çağırma (tool calling) ajanı. ~150 satır, çerçeve yok.

Döngü:
  kullanıcı mesajı → model → (araç çağrısı → çalıştır → sonucu modele ver)* → nihai cevap
Her turdan önce BÜTÇE kontrol edilir: adım, token, USD, süre. Aşılırsa ajan durur ve bunu söyler.
Hafta 1'deki başarısızlık maddesi: "Sınırsız maliyet: ajan döngüye giriyor, fatura patlıyor."

Kullanım:
  python ajan_dongusu.py "SIP-1001 siparişim nerede? İade edebilir miyim?"
  python ajan_dongusu.py "SIP-1002 için iade var mı, %10 indirimli fiyatı ne olurdu?" --max-adim 3 --max-usd 0.002
  python ajan_dongusu.py "..." --mcp            # araçları yerel fonksiyon yerine MCP sunucusundan al
  python ajan_dongusu.py "..." --trace izler/deneme.jsonl
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Awaitable, Callable

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

import araclar_yerel

load_dotenv(find_dotenv())

SISTEM = (
    "Sen bir e-ticaret müşteri destek ajanısın. Türkçe, kısa ve net yanıt ver. "
    "Bilgiyi uydurma; sipariş, kargo, iade ve hesaplama için araçları kullan. "
    "Araç sonucu hata dönerse kullanıcıya bunu söyle, tekrar tekrar aynı aracı çağırma."
)


# ----------------------------------------------------------------- bütçe
@dataclass
class Butce:
    max_adim: int = 6
    max_token: int = 20_000
    max_usd: float = 0.05
    max_sure_sn: float = 60.0
    girdi_fiyat: float = 0.10      # $/1M token (gpt-6-luna varsayılanı; week4/fiyatlar.json)
    cikti_fiyat: float = 0.50
    adim: int = 0
    token: int = 0
    usd: float = 0.0
    baslangic: float = field(default_factory=time.perf_counter)

    def kaydet(self, girdi: int, cikti: int) -> None:
        self.token += girdi + cikti
        self.usd += (girdi * self.girdi_fiyat + cikti * self.cikti_fiyat) / 1e6

    def asildi(self) -> str | None:
        if self.adim >= self.max_adim:
            return f"adım sınırı ({self.max_adim})"
        if self.token >= self.max_token:
            return f"token sınırı ({self.max_token})"
        if self.usd >= self.max_usd:
            return f"maliyet sınırı (${self.max_usd})"
        if time.perf_counter() - self.baslangic >= self.max_sure_sn:
            return f"süre sınırı ({self.max_sure_sn} sn)"
        return None

    def ozet(self) -> str:
        return f"{self.adim} adım · {self.token} token · ${self.usd:.5f} · {time.perf_counter() - self.baslangic:.1f} sn"


# ----------------------------------------------------------------- araç köprüsü
AracCalistirici = Callable[[str, dict[str, Any]], Awaitable[str]]


async def yerel_calistir(ad: str, args: dict[str, Any]) -> str:
    fn = araclar_yerel.ARAC_FONKSIYONLARI.get(ad)
    if fn is None:
        return json.dumps({"hata": f"bilinmeyen araç: {ad}"}, ensure_ascii=False)
    try:
        return fn(**args)
    except TypeError as hata:
        return json.dumps({"hata": f"argüman hatası: {hata}"}, ensure_ascii=False)


# ----------------------------------------------------------------- döngü
async def ajan(soru: str, araclar: list[dict], calistir: AracCalistirici, butce: Butce,
               model: str | None = None, trace: list[dict] | None = None, sessiz: bool = False,
               sistem: str = SISTEM) -> str:
    istemci = OpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ["LLM_API_KEY"])
    model = model or os.getenv("LLM_MODEL", "gpt-6-luna")
    mesajlar: list[dict] = [{"role": "system", "content": sistem}, {"role": "user", "content": soru}]

    def log(**kayit):
        kayit["t"] = round(time.perf_counter() - butce.baslangic, 3)
        if trace is not None:
            trace.append(kayit)
        if not sessiz:
            print(f"  [{kayit['t']:5.1f}s] {kayit['olay']:<10} {kayit.get('detay', '')}")

    while True:
        sebep = butce.asildi()
        if sebep:
            log(olay="DURDU", detay=f"bütçe aşıldı: {sebep} · {butce.ozet()}")
            return f"(Ajan durduruldu: {sebep}. Şimdiye kadar: {butce.ozet()})"

        butce.adim += 1
        yanit = istemci.chat.completions.create(model=model, messages=mesajlar, tools=araclar, tool_choice="auto", temperature=0)
        u = yanit.usage
        if u:
            butce.kaydet(u.prompt_tokens, u.completion_tokens)
        mesaj = yanit.choices[0].message
        log(olay="MODEL", detay=f"adım {butce.adim} · {u.prompt_tokens if u else '?'}→{u.completion_tokens if u else '?'} tok · toplam ${butce.usd:.5f}")

        if not mesaj.tool_calls:
            log(olay="CEVAP", detay=(mesaj.content or "")[:120].replace("\n", " "))
            return mesaj.content or ""

        # Modelin araç çağrısını geçmişe ekle, her aracı çalıştır, sonuçları geri ver
        mesajlar.append({"role": "assistant", "content": mesaj.content, "tool_calls": [
            {"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
            for tc in mesaj.tool_calls]})
        for tc in mesaj.tool_calls:
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            log(olay="ARAÇ", detay=f"{tc.function.name}({json.dumps(args, ensure_ascii=False)})")
            sonuc = await calistir(tc.function.name, args)
            log(olay="SONUÇ", detay=sonuc[:120].replace("\n", " "))
            mesajlar.append({"role": "tool", "tool_call_id": tc.id, "content": sonuc})


# ----------------------------------------------------------------- CLI
async def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("soru")
    p.add_argument("--max-adim", type=int, default=6)
    p.add_argument("--max-token", type=int, default=20_000)
    p.add_argument("--max-usd", type=float, default=0.05)
    p.add_argument("--max-sure", type=float, default=60.0)
    p.add_argument("--girdi-fiyat", type=float, default=float(os.getenv("GIRDI_FIYAT", 0.10)))
    p.add_argument("--cikti-fiyat", type=float, default=float(os.getenv("CIKTI_FIYAT", 0.50)))
    p.add_argument("--mcp", action="store_true", help="Araçları mcp_sunucu.py üzerinden kullan")
    p.add_argument("--trace", help="İzi JSONL olarak bu dosyaya yaz (örn. izler/deneme.jsonl)")
    a = p.parse_args()

    butce = Butce(a.max_adim, a.max_token, a.max_usd, a.max_sure, a.girdi_fiyat, a.cikti_fiyat)
    iz: list[dict] = []
    print(f"SORU: {a.soru}\nBÜTÇE: {a.max_adim} adım · {a.max_token} token · ${a.max_usd} · {a.max_sure} sn · araçlar: {'MCP' if a.mcp else 'yerel'}\n")

    if a.mcp:
        import mcp_istemci
        async with mcp_istemci.baglan() as oturum:
            araclar = await mcp_istemci.openai_araclari(oturum)

            async def calistir(ad: str, args: dict) -> str:
                return await mcp_istemci.arac_cagir(oturum, ad, args)

            cevap = await ajan(a.soru, araclar, calistir, butce, trace=iz)
    else:
        cevap = await ajan(a.soru, araclar_yerel.ARAC_TANIMLARI, yerel_calistir, butce, trace=iz)

    print(f"\nCEVAP:\n{cevap}\n\nÖZET: {butce.ozet()}")
    if a.trace:
        yol = Path(a.trace)
        yol.parent.mkdir(parents=True, exist_ok=True)
        with yol.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"soru": a.soru, "cevap": cevap, "butce": butce.ozet(), "iz": iz}, ensure_ascii=False) + "\n")
        print(f"İz eklendi: {yol}")


if __name__ == "__main__":
    asyncio.run(main())
