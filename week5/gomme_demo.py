"""
week5 · gomme_demo.py — gömme (embedding) sezgisi: anlam benzerliği sayıya dönüşür.

Sekiz Türkçe cümleyi vektöre çevirir, kosinüs benzerliği matrisini ve en yakın çiftleri yazar.
Gözlenecekler:
  * 'parola' ↔ 'şifre' : kelime örtüşmesi yok, anlam benzer → vektörler yakın (BM25 bunu kaçırır)
  * 'izin' ↔ 'iznim' ↔ 'tatil' : Türkçe ekler ve eş anlamlılar
  * 'Docker' cümlesi herkesten uzak

Kullanım:  python gomme_demo.py            (EMBED_MODEL .env'den; Ollama için bge-m3 önerilir)
"""
from __future__ import annotations

import numpy as np

from rag import EMBED_MODEL, gom

CUMLELER = [
    "Yıllık izin kaç gün?",
    "İznim ne kadar, kaç gün tatil yapabilirim?",
    "Parolam en az kaç karakter olmalı?",
    "Şifre uzunluğu kuralı nedir?",
    "Kafede çalışırken VPN açmam gerekir mi?",
    "Halka açık Wi-Fi'de şirket ağına nasıl güvenli bağlanırım?",
    "Docker imajı nasıl oluşturulur?",
    "Yurt dışı seyahatte günlük harcırah ne kadar?",
]


def main() -> None:
    print(f"Gömme modeli: {EMBED_MODEL}")
    v = np.array(gom(CUMLELER))
    v = v / np.linalg.norm(v, axis=1, keepdims=True)
    benzerlik = v @ v.T
    print(f"Vektör boyutu: {v.shape[1]}\n")

    print("Kosinüs benzerliği (1.00 = aynı anlam):")
    print("      " + " ".join(f"  c{i + 1}" for i in range(len(CUMLELER))))
    for i, satir in enumerate(benzerlik):
        print(f"c{i + 1:<4} " + " ".join(f"{x:5.2f}" for x in satir))
    print()
    for i, c in enumerate(CUMLELER):
        print(f"c{i + 1}: {c}")

    ciftler = sorted(((benzerlik[i, j], i, j) for i in range(len(CUMLELER)) for j in range(i + 1, len(CUMLELER))), reverse=True)
    print("\nEn yakın 4 çift:")
    for puan, i, j in ciftler[:4]:
        print(f"  {puan:.2f}  c{i + 1} ↔ c{j + 1}")
    print("\nEn uzak çift:")
    puan, i, j = ciftler[-1]
    print(f"  {puan:.2f}  c{i + 1} ↔ c{j + 1}")
    print("\nSoru: c3 ↔ c4 ortak kelime içermiyor. BM25 bu çifti bulabilir miydi? Hibrit arama bu yüzden var.")


if __name__ == "__main__":
    main()
