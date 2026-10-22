"""
week7 · mcp_istemci.py — MCP sunucusuna programatik olarak bağlan: araçları listele, çağır, kaynağı oku.

Hem tek başına çalışır (demo), hem ajan_dongusu.py --mcp tarafından kullanılır.
  python mcp_istemci.py
"""
from __future__ import annotations

import asyncio
import json
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SUNUCU = Path(__file__).with_name("mcp_sunucu.py")


@asynccontextmanager
async def baglan(sunucu_yolu: Path = SUNUCU):
    """stdio üzerinden sunucu sürecini başlat ve oturum aç."""
    params = StdioServerParameters(command=sys.executable, args=[str(sunucu_yolu)])
    async with stdio_client(params) as (okuma, yazma):
        async with ClientSession(okuma, yazma) as oturum:
            await oturum.initialize()
            yield oturum


async def openai_araclari(oturum: ClientSession) -> list[dict]:
    """MCP araç listesini OpenAI 'tools' biçimine çevir. inputSchema zaten JSON Schema'dır."""
    sonuc = await oturum.list_tools()
    return [{"type": "function", "function": {"name": t.name, "description": t.description or "", "parameters": _sema(t)}}
            for t in sonuc.tools]


def _sema(arac) -> dict:
    """mcp 2.x: input_schema · mcp 1.x: inputSchema — ikisini de destekle."""
    return getattr(arac, "input_schema", None) or getattr(arac, "inputSchema", None) or {"type": "object", "properties": {}}


async def arac_cagir(oturum: ClientSession, ad: str, args: dict) -> str:
    sonuc = await oturum.call_tool(ad, args)
    parcalar = [getattr(c, "text", "") for c in (getattr(sonuc, "content", None) or [])]
    metin = "\n".join(p for p in parcalar if p)
    if getattr(sonuc, "is_error", None) or getattr(sonuc, "isError", False):
        return json.dumps({"hata": metin or "araç hatası"}, ensure_ascii=False)
    yapisal = getattr(sonuc, "structured_content", None) or getattr(sonuc, "structuredContent", None)
    return metin or json.dumps(yapisal or {}, ensure_ascii=False)


async def main() -> None:
    async with baglan() as oturum:
        araclar = await oturum.list_tools()
        print(f"Sunucudaki araçlar ({len(araclar.tools)}):")
        for t in araclar.tools:
            print(f"  • {t.name:18} {t.description}")
            print(f"    şema: {json.dumps(_sema(t).get('properties', {}), ensure_ascii=False)}")

        print("\nÇağrı: siparis_durumu(SIP-1001)")
        print("  →", await arac_cagir(oturum, "siparis_durumu", {"siparis_no": "SIP-1001"}))
        print("Çağrı: hesapla(1899*0.9)")
        print("  →", await arac_cagir(oturum, "hesapla", {"ifade": "1899*0.9"}))
        print("Çağrı: siparis_durumu(SIP-9999)  (hata yolu)")
        print("  →", await arac_cagir(oturum, "siparis_durumu", {"siparis_no": "SIP-9999"}))

        kaynaklar = await oturum.list_resources()
        print(f"\nKaynaklar ({len(kaynaklar.resources)}):")
        for r in kaynaklar.resources:
            icerik = await oturum.read_resource(r.uri)
            metin = next((getattr(c, "text", "") for c in icerik.contents), "")
            print(f"  • {r.uri}\n    {metin[:200].replace(chr(10), ' | ')}")

        print("\nOpenAI 'tools' biçimine çevrilmiş ilk araç:")
        print(json.dumps((await openai_araclari(oturum))[0], ensure_ascii=False, indent=2)[:400])


if __name__ == "__main__":
    asyncio.run(main())
