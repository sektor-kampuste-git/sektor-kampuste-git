"""
week7 · mcp_sunucu.py — kendi MCP (Model Context Protocol) sunucunuz, 30 satır.

MCP = araçlarınızı (ve kaynaklarınızı) HERHANGİ bir ajana açmanın standart yolu:
VS Code Copilot, Claude Desktop, Cursor, kendi ajan_dongusu.py'niz... hepsi aynı sunucuya bağlanır.

Çalıştırma (stdio; istemci bu süreci kendisi başlatır):
  python mcp_sunucu.py
Deneme: python mcp_istemci.py        ·  IDE bağlantıları: ide_ayarlari/
"""
from __future__ import annotations

from mcp.server.mcpserver import MCPServer

import araclar_yerel

sunucu = MCPServer("kampus-destek")


@sunucu.tool()
def siparis_durumu(siparis_no: str) -> str:
    """Sipariş numarasına göre ürün, durum, kargo takip numarası ve tutarı döndürür (örn. SIP-1001)."""
    return araclar_yerel.siparis_durumu(siparis_no)


@sunucu.tool()
def kargo_takip(takip_no: str) -> str:
    """Kargo takip numarasının (örn. TK-77) hareket geçmişini döndürür."""
    return araclar_yerel.kargo_takip(takip_no)


@sunucu.tool()
def iade_politikasi(kategori: str) -> str:
    """Ürün kategorisi (elektronik, giyim, gida) için iade kuralını döndürür."""
    return araclar_yerel.iade_politikasi(kategori)


@sunucu.tool()
def hesapla(ifade: str) -> str:
    """Dört işlem ve üs içeren aritmetik ifadeyi hesaplar, örn. 1899*0.9."""
    return araclar_yerel.hesapla(ifade)


@sunucu.resource("kampus://iade-politikasi")
def iade_politikasi_belgesi() -> str:
    """Tüm kategorilerin iade kuralları, tek belge halinde."""
    return "\n".join(f"- {k}: {v}" for k, v in araclar_yerel.IADE_POLITIKASI.items())


if __name__ == "__main__":
    sunucu.run(transport="stdio")
