"""
week5 · sor.py — indekse soru sor: getirilen parçalar + kaynaklı cevap.

Kullanım:
  python sor.py "Yıllık izin kaç gün?"
  python sor.py "Şifre kuralı ne?" --yontem bm25 --goster        # anahtar kelime: 'şifre' geçmiyor → bulamaz
  python sor.py "Şifre kuralı ne?" --yontem vektor --goster      # anlam: 'parola' parçasını bulur
  python sor.py "Ciro ne kadar?" --sadece-getir                 # LLM'siz, yalnızca getirme
"""
from __future__ import annotations

import argparse

from rag import INDEKS_DOSYASI, Indeks, cevapla


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("soru")
    p.add_argument("--k", type=int, default=4)
    p.add_argument("--yontem", default="hibrit", choices=["hibrit", "vektor", "bm25"])
    p.add_argument("--indeks", default=str(INDEKS_DOSYASI))
    p.add_argument("--qdrant-url", default=None)
    p.add_argument("--goster", action="store_true", help="Getirilen parçaların metnini de yaz")
    p.add_argument("--sadece-getir", action="store_true", help="Model çağırma, yalnızca getirme")
    a = p.parse_args()

    indeks = Indeks.yukle(a.indeks, a.qdrant_url)
    if a.sadece_getir:
        baglamlar = indeks.getir(a.soru, a.k, a.yontem)
        sonuc = {"baglamlar": baglamlar}
    else:
        sonuc = cevapla(indeks, a.soru, a.k, a.yontem)

    print(f"\nSORU: {a.soru}   (yöntem: {a.yontem}, k={a.k})\n")
    print("Getirilen parçalar:")
    for i, b in enumerate(sonuc["baglamlar"], 1):
        print(f"  [{i}] {b['puan']:.4f}  {b['parca'].belge:32} {'+'.join(b['yontemler']):12} {b['parca'].metin[:70].replace(chr(10), ' ')!r}")
        if a.goster:
            print("      " + b["parca"].metin.replace("\n", "\n      ") + "\n")
    if not a.sadece_getir:
        print(f"\nCEVAP ({sonuc['sure_ms']} ms, {sonuc['girdi_token']} → {sonuc['cikti_token']} token):\n{sonuc['cevap']}")


if __name__ == "__main__":
    main()
