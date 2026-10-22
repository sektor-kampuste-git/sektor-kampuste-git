"""week8 · izleme/iz_goster.py — izler/*.jsonl dosyalarını ağaç olarak yazdır; en pahalı / en yavaş trace'leri bul.

Kullanım:  python iz_goster.py            # bugünün dosyası
           python iz_goster.py --hepsi    # tüm günler
           python iz_goster.py --en-pahali 3
"""
from __future__ import annotations

import argparse
import json
import time

from yerel_iz import IZ_KLASORU


def yukle(hepsi: bool) -> list[dict]:
    dosyalar = sorted(IZ_KLASORU.glob("*.jsonl")) if hepsi else [IZ_KLASORU / f"{time.strftime('%Y-%m-%d')}.jsonl"]
    izler = []
    for d in dosyalar:
        if d.exists():
            izler += [json.loads(s) for s in d.read_text(encoding="utf-8").splitlines() if s.strip()]
    return izler


def agac(iz: dict) -> None:
    print(f"▣ {iz['trace_id']} · {iz['ad']} · {iz['zaman']} · {iz['toplam_ms']} ms · {iz['toplam_token']} tok · ${iz['toplam_usd']:.6f} · {iz['etiketler']}")
    cocuklar: dict[str | None, list[dict]] = {}
    for s in iz["spanler"]:
        cocuklar.setdefault(s["ust"], []).append(s)

    def yaz(ust: str | None, derinlik: int):
        for s in cocuklar.get(ust, []):
            hata = f" ✗ {s['hata']}" if s.get("hata") else ""
            tok = f" · {s['token']} tok" if s.get("token") else ""
            print("  " * derinlik + f"└─ {s['ad']} · {s['sure_ms']} ms{tok}{hata}")
            if s.get("cikti") is not None:
                print("  " * derinlik + f"     ↳ {str(s['cikti'])[:100]!r}")
            yaz(s["id"], derinlik + 1)

    yaz(None, 1)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--hepsi", action="store_true")
    p.add_argument("--en-pahali", type=int, metavar="N", help="Maliyete göre ilk N trace")
    a = p.parse_args()
    izler = yukle(a.hepsi)
    if not izler:
        print("İz yok. Önce: python izleme_demo.py \"...\"")
        return
    if a.en_pahali:
        izler = sorted(izler, key=lambda i: i["toplam_usd"], reverse=True)[: a.en_pahali]
    for iz in izler:
        agac(iz)
        print()
    print(f"{len(izler)} trace · toplam ${sum(i['toplam_usd'] for i in izler):.6f} · ortalama {sum(i['toplam_ms'] for i in izler) / len(izler):.0f} ms")


if __name__ == "__main__":
    main()
