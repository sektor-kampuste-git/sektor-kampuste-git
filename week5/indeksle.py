"""
week5 · indeksle.py — derlemi parçala, vektöre çevir, indeksi diske kaydet.

Kullanım:
  python indeksle.py                                   # paragraf, 600 karakter
  python indeksle.py --yontem sabit --boyut 400 --cikti indeks_sabit.pkl
  python indeksle.py --qdrant-url http://localhost:6333   # Docker'daki Qdrant'a yaz (docker run -p 6333:6333 qdrant/qdrant)
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from rag import EMBED_MODEL, INDEKS_DOSYASI, Indeks, gom, parcalari_olustur


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--yontem", default="paragraf", choices=["sabit", "paragraf", "cumle"])
    p.add_argument("--boyut", type=int, default=600)
    p.add_argument("--ortusme", type=int, default=100)
    p.add_argument("--cikti", default=str(INDEKS_DOSYASI))
    p.add_argument("--qdrant-url", default=None)
    a = p.parse_args()

    parcalar = parcalari_olustur(a.yontem, a.boyut, a.ortusme)
    print(f"{len(parcalar)} parça ({a.yontem}, {a.boyut} karakter) → gömme modeli: {EMBED_MODEL}")
    t0 = time.perf_counter()
    vektorler = gom([x.metin for x in parcalar])
    sure = time.perf_counter() - t0
    print(f"{len(vektorler)} vektör, boyut {len(vektorler[0])}, {sure:.1f} sn")

    indeks = Indeks(parcalar, vektorler, a.qdrant_url)
    indeks.kaydet(Path(a.cikti))
    print(f"Kaydedildi: {a.cikti}  (Qdrant: {'sunucu ' + a.qdrant_url if a.qdrant_url else 'bellek içi, yeniden yüklemede kurulur'})")
    print("Sıradaki: python sor.py \"Yıllık izin kaç gün?\" --goster")


if __name__ == "__main__":
    main()
