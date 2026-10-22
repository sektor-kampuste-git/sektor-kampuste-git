"""
week7 · a2a_mini.py — iki ajan, iki "Agent Card", bir el değiştirme (handoff). A2A fikrinin en küçük hali.

Gerçek A2A (Agent2Agent) protokolünde her ajan /.well-known/agent-card.json yayınlar, görevler (task)
JSON-RPC/HTTP ile gönderilir, sonuçlar artifact olarak döner. Burada aynı fikir süreç içinde:
  planlayıcı ajan → gorev_ver(ajan="destek-uzmani", gorev=...) → uzman ajan kendi araçları ve KENDİ BÜTÇESİYLE çalışır → cevap planlayıcıya döner

MCP ile fark: MCP ajan ↔ ARAÇ, A2A ajan ↔ AJAN. Uzman ajanın hangi aracı kullandığı planlayıcıyı ilgilendirmez.

Kullanım:  python a2a_mini.py "SIP-1001 nerede ve iade edersem %10 kesinti sonrası ne kadar alırım?"
"""
from __future__ import annotations

import asyncio
import json
import sys

import araclar_yerel
from ajan_dongusu import Butce, ajan, yerel_calistir

AJAN_KARTLARI = {
    "destek-uzmani": {
        "name": "destek-uzmani",
        "description": "Sipariş, kargo, iade ve basit hesaplama sorularını kendi araçlarıyla yanıtlar.",
        "url": "local://destek-uzmani",
        "skills": [{"id": "siparis-kargo-iade", "description": "SIP-xxxx ve TK-xx numaralarıyla durum ve iade bilgisi"}],
        "capabilities": {"streaming": False},
    },
    "planlayici": {
        "name": "planlayici",
        "description": "Kullanıcı isteğini alt görevlere böler, uzman ajanlara devreder, cevapları birleştirir.",
        "url": "local://planlayici",
        "skills": [{"id": "devret", "description": "gorev_ver(ajan, gorev)"}],
        "capabilities": {"streaming": False},
    },
}

PLANLAYICI_SISTEM = (
    "Sen bir planlayıcı ajansın. Kendin araç kullanamazsın; sipariş/kargo/iade/hesap gerektiren her şeyi "
    "gorev_ver aracıyla 'destek-uzmani' ajanına devret. Gelen cevapları birleştirip kullanıcıya kısa Türkçe yanıt ver."
)
PLANLAYICI_ARACLARI = [{
    "type": "function",
    "function": {
        "name": "gorev_ver",
        "description": "Bir alt görevi uzman ajana devret. Mevcut uzman: destek-uzmani (sipariş, kargo, iade, hesaplama).",
        "parameters": {"type": "object", "properties": {
            "ajan": {"type": "string", "enum": list(k for k in AJAN_KARTLARI if k != "planlayici")},
            "gorev": {"type": "string", "description": "Uzmana verilecek, kendi başına anlaşılır görev cümlesi"},
        }, "required": ["ajan", "gorev"]},
    },
}]

UZMAN_BUTCELERI: list[Butce] = []


async def planlayici_calistir(ad: str, args: dict) -> str:
    if ad != "gorev_ver":
        return json.dumps({"hata": f"planlayıcının böyle bir aracı yok: {ad}"}, ensure_ascii=False)
    hedef, gorev = args.get("ajan"), args.get("gorev", "")
    if hedef not in AJAN_KARTLARI or hedef == "planlayici":
        return json.dumps({"hata": f"bilinmeyen ajan: {hedef}"}, ensure_ascii=False)
    print(f"    ↳ HANDOFF → {hedef}: {gorev!r}")
    butce = Butce(max_adim=4, max_usd=0.01)          # uzmanın KENDİ bütçesi
    UZMAN_BUTCELERI.append(butce)
    cevap = await ajan(gorev, araclar_yerel.ARAC_TANIMLARI, yerel_calistir, butce, sessiz=True)
    print(f"    ↲ {hedef} bitti ({butce.ozet()})")
    return cevap


async def main() -> None:
    soru = sys.argv[1] if len(sys.argv) > 1 else "SIP-1001 nerede ve iade edersem %10 kesinti sonrası ne kadar alırım?"
    print("Agent Card'lar:")
    for kart in AJAN_KARTLARI.values():
        print(f"  • {kart['name']:15} {kart['description']}")
    print(f"\nSORU: {soru}\n")
    butce = Butce(max_adim=5, max_usd=0.02)
    cevap = await ajan(soru, PLANLAYICI_ARACLARI, planlayici_calistir, butce, sistem=PLANLAYICI_SISTEM)
    print(f"\nCEVAP:\n{cevap}")
    print(f"\nPlanlayıcı: {butce.ozet()}")
    for i, b in enumerate(UZMAN_BUTCELERI, 1):
        print(f"Uzman #{i}:   {b.ozet()}")
    print(f"Toplam maliyet: ${butce.usd + sum(b.usd for b in UZMAN_BUTCELERI):.5f}")


if __name__ == "__main__":
    asyncio.run(main())
