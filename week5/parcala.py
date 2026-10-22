"""
week5 · parcala.py — parçalama (chunking) yöntemlerini derlem üzerinde karşılaştır.

Kullanım:
  python parcala.py                         # üç yöntemin istatistikleri
  python parcala.py --yontem paragraf --belge 01_izin_politikasi.md   # bir belgenin tüm parçalarını göster
  python parcala.py --boyut 300 --ortusme 50
"""
from __future__ import annotations

import argparse

from rag import DERLEM, derlemi_yukle, parcala


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--yontem", choices=["sabit", "paragraf", "cumle"])
    p.add_argument("--belge", help="Tek bir belgenin parçalarını yazdır (dosya adı)")
    p.add_argument("--boyut", type=int, default=600)
    p.add_argument("--ortusme", type=int, default=100)
    a = p.parse_args()

    belgeler = derlemi_yukle(DERLEM)
    print(f"Derlem: {len(belgeler)} belge, {sum(len(m) for _, _, m in belgeler):,} karakter\n")

    if a.belge:
        metin = next(m for d, _, m in belgeler if d == a.belge)
        for i, parca in enumerate(parcala(metin, a.yontem or "paragraf", a.boyut, a.ortusme), 1):
            print(f"── parça {i} · {len(parca)} karakter ──\n{parca}\n")
        return

    print(f"{'yöntem':10} {'parça':>6} {'ort. kar.':>10} {'min':>6} {'maks':>6}   örnek (ilk parça, ilk 90 karakter)")
    for yontem in ([a.yontem] if a.yontem else ["sabit", "paragraf", "cumle"]):
        tum = [parca for _, _, m in belgeler for parca in parcala(m, yontem, a.boyut, a.ortusme)]
        uz = [len(x) for x in tum]
        print(f"{yontem:10} {len(tum):>6} {sum(uz) / len(uz):>10.0f} {min(uz):>6} {max(uz):>6}   {tum[0][:90].replace(chr(10), ' ')!r}")
    print("\nSorular: Hangi yöntem başlığı içeriğinden ayırıyor? Hangisi cümleyi ortadan bölüyor? Küçük parça = kesin ama bağlamsız; büyük parça = bağlamlı ama gürültülü.")


if __name__ == "__main__":
    main()
