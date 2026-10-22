"""
week7 · araclar_yerel.py — ajanın kullandığı araçlar (saf Python, sahte veri).

Aynı fonksiyonlar iki yerden sunulur:
  * ajan_dongusu.py → doğrudan (yerel araç)
  * mcp_sunucu.py  → MCP üzerinden (herhangi bir istemci: VS Code, Claude Desktop, Cursor, kendi ajanınız)

Gerçek hayatta bu fonksiyonlar bir veritabanına / CRM'e / kargo API'sine bağlanır.
"""
from __future__ import annotations

import ast
import json
import operator

SIPARISLER: dict[str, dict] = {
    "SIP-1001": {"urun": "Kablosuz kulaklık", "kategori": "elektronik", "durum": "kargoda", "takip_no": "TK-77", "tarih": "2026-10-20", "tutar_tl": 1899.0},
    "SIP-1002": {"urun": "Yün kazak", "kategori": "giyim", "durum": "teslim edildi", "takip_no": "TK-41", "tarih": "2026-10-12", "tutar_tl": 749.0},
    "SIP-1003": {"urun": "Zeytinyağı 5L", "kategori": "gida", "durum": "hazırlanıyor", "takip_no": None, "tarih": "2026-10-22", "tutar_tl": 980.0},
}

KARGO: dict[str, list[str]] = {
    "TK-77": ["20.10 09:12 Depodan çıktı (İzmir)", "21.10 03:40 Transfer merkezi (İstanbul)", "22.10 07:55 Dağıtıma çıktı (Kadıköy)"],
    "TK-41": ["12.10 10:05 Depodan çıktı", "13.10 14:20 Teslim edildi (kapıcıya)"],
}

IADE_POLITIKASI: dict[str, str] = {
    "elektronik": "Teslimden itibaren 14 gün içinde, kutusu açılmamış ürünler iade edilir. Açılmış ürünlerde yalnızca arıza halinde değişim.",
    "giyim": "Teslimden itibaren 30 gün içinde, etiketi sökülmemiş ve yıkanmamış ürünler iade edilir.",
    "gida": "Gıda ürünlerinde iade kabul edilmez; hasarlı teslimatta 48 saat içinde fotoğrafla bildirim yapılırsa ücret iadesi yapılır.",
}


def siparis_durumu(siparis_no: str) -> str:
    """Sipariş numarasına göre ürün, durum, kargo takip numarası ve tutarı döndürür."""
    s = SIPARISLER.get(siparis_no.strip().upper())
    if not s:
        return json.dumps({"hata": f"{siparis_no} bulunamadı. Biçim: SIP-1001"}, ensure_ascii=False)
    return json.dumps({"siparis_no": siparis_no.upper(), **s}, ensure_ascii=False)


def kargo_takip(takip_no: str) -> str:
    """Kargo takip numarasının hareket geçmişini döndürür."""
    h = KARGO.get(takip_no.strip().upper())
    if not h:
        return json.dumps({"hata": f"{takip_no} için hareket yok."}, ensure_ascii=False)
    return json.dumps({"takip_no": takip_no.upper(), "hareketler": h, "son_durum": h[-1]}, ensure_ascii=False)


def iade_politikasi(kategori: str) -> str:
    """Ürün kategorisi (elektronik, giyim, gida) için iade kuralını döndürür."""
    k = kategori.strip().lower().replace("ı", "i")
    return IADE_POLITIKASI.get(k, "Bu kategori için tanımlı iade kuralı yok; müşteri hizmetlerine yönlendirin.")


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}


def hesapla(ifade: str) -> str:
    """Yalnızca dört işlem ve üs içeren aritmetik ifadeyi güvenle hesaplar (eval yok)."""
    def _d(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](_d(n.left), _d(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](_d(n.operand))
        raise ValueError("izin verilmeyen ifade")
    try:
        return str(_d(ast.parse(ifade, mode="eval").body))
    except Exception as hata:  # noqa: BLE001
        return f"hata: {hata}"


# OpenAI 'tools' biçimi. MCP sunucusu aynı bilgiyi fonksiyon imzasından kendisi üretir.
ARAC_TANIMLARI = [
    {"type": "function", "function": {"name": "siparis_durumu", "description": siparis_durumu.__doc__,
     "parameters": {"type": "object", "properties": {"siparis_no": {"type": "string", "description": "Sipariş numarası, örn. SIP-1001"}}, "required": ["siparis_no"]}}},
    {"type": "function", "function": {"name": "kargo_takip", "description": kargo_takip.__doc__,
     "parameters": {"type": "object", "properties": {"takip_no": {"type": "string", "description": "Kargo takip numarası, örn. TK-77"}}, "required": ["takip_no"]}}},
    {"type": "function", "function": {"name": "iade_politikasi", "description": iade_politikasi.__doc__,
     "parameters": {"type": "object", "properties": {"kategori": {"type": "string", "enum": ["elektronik", "giyim", "gida"]}}, "required": ["kategori"]}}},
    {"type": "function", "function": {"name": "hesapla", "description": hesapla.__doc__,
     "parameters": {"type": "object", "properties": {"ifade": {"type": "string", "description": "Örn. 1899*0.9"}}, "required": ["ifade"]}}},
]

ARAC_FONKSIYONLARI = {"siparis_durumu": siparis_durumu, "kargo_takip": kargo_takip, "iade_politikasi": iade_politikasi, "hesapla": hesapla}
