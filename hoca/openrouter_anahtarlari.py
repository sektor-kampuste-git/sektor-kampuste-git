"""
hoca · openrouter_anahtarlari.py — öğrenci / takım başına harcama limitli OpenRouter anahtarları.

Neden? Tek bir anahtarı sınıfa dağıtmak yerine herkese ayrı, dolar limitli bir anahtar verirsiniz:
biri sızarsa yalnızca o kapatılır, kimse bütçenin tamamını harcayamaz, kullanım kişi başına görünür.

Ön koşul (bir kez, tarayıcıda):
  1. openrouter.ai → Settings → Credits: bakiye yükleyin (hesap başına ≥ 10 $ olunca ücretsiz
     `:free` modellerin günlük limiti de yükselir).
  2. openrouter.ai → Settings → Management API Keys → "Create New Key". Bu anahtar model çağıramaz,
     yalnızca anahtar üretir. Terminalde ortam değişkeni yapın, dosyaya yazmayın:
        export OPENROUTER_MANAGEMENT_KEY=sk-or-v1-...

Kullanım:
  python hoca/openrouter_anahtarlari.py olustur --onek ogr --adet 45 --limit 1
  python hoca/openrouter_anahtarlari.py olustur --onek takim --adet 15 --limit 3 --cikti takim_anahtarlari.csv
  python hoca/openrouter_anahtarlari.py listele              # ad, limit, harcanan, durum
  python hoca/openrouter_anahtarlari.py kapat --onek ogr      # dönem sonu: hepsini devre dışı bırak

Çıktı CSV'si (`anahtarlar.csv`) .gitignore'dadır; anahtarları LMS'te kişiye özel mesajla dağıtın.
Etiketlerde öğrenci adı yerine sıra numarası kullanın (ogr-01 ↔ öğrenci eşleşmesi sizin yerel listenizde kalsın).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request

API = os.environ.get("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")


def istek(yontem: str, yol: str, govde: dict | None = None) -> dict:
    anahtar = os.environ.get("OPENROUTER_MANAGEMENT_KEY")
    if not anahtar:
        sys.exit("OPENROUTER_MANAGEMENT_KEY ortam değişkeni yok (openrouter.ai → Settings → Management API Keys).")
    veri = json.dumps(govde).encode() if govde is not None else None
    req = urllib.request.Request(
        API + yol, data=veri, method=yontem,
        headers={"Authorization": f"Bearer {anahtar}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as yanit:
            return json.loads(yanit.read() or b"{}")
    except urllib.error.HTTPError as hata:
        sys.exit(f"{yontem} {yol} → HTTP {hata.code}: {hata.read().decode(errors='replace')[:300]}")


def tum_anahtarlar() -> list[dict]:
    sonuc, ofset = [], 0
    while True:
        sayfa = istek("GET", f"/keys?offset={ofset}").get("data", [])
        sonuc += sayfa
        if len(sayfa) < 100:
            return sonuc
        ofset += len(sayfa)


def olustur(a: argparse.Namespace) -> None:
    if os.path.exists(a.cikti) and not a.uzerine_yaz:
        sys.exit(f"{a.cikti} zaten var; önceki anahtarları kaybetmemek için başka --cikti verin ya da --uzerine-yaz.")
    mevcut = {k.get("name") for k in tum_anahtarlar()}
    satirlar = []
    for i in range(a.baslangic, a.baslangic + a.adet):
        ad = f"{a.onek}-{i:02d}"
        if ad in mevcut:
            print(f"atlandı: {ad} zaten var")
            continue
        govde = {"name": ad, "limit": a.limit}
        if a.sifirlama:
            govde["limit_reset"] = a.sifirlama
        yanit = istek("POST", "/keys", govde)
        satirlar.append({"ad": ad, "limit_usd": a.limit, "anahtar": yanit["key"]})
        print(f"oluşturuldu: {ad} (limit {a.limit} $)")
    with open(a.cikti, "w", newline="", encoding="utf-8") as f:
        yazici = csv.DictWriter(f, fieldnames=["ad", "limit_usd", "anahtar"])
        yazici.writeheader()
        yazici.writerows(satirlar)
    print(f"\n{len(satirlar)} anahtar → {a.cikti} (repoya girmez; dağıttıktan sonra silin)")


def listele(a: argparse.Namespace) -> None:
    anahtarlar = [k for k in tum_anahtarlar() if not a.onek or str(k.get("name", "")).startswith(a.onek)]
    print(f"{'ad':<14} {'limit $':>8} {'harcanan $':>11}  durum")
    toplam = 0.0
    for k in sorted(anahtarlar, key=lambda k: str(k.get("name"))):
        kullanim = float(k.get("usage") or 0)
        toplam += kullanim
        limit = "-" if k.get("limit") is None else f"{float(k['limit']):.2f}"
        print(f"{str(k.get('name')):<14} {limit:>8} {kullanim:>11.4f}  {'kapalı' if k.get('disabled') else 'açık'}")
    print(f"\n{len(anahtarlar)} anahtar, toplam harcama {toplam:.4f} $")


def kapat(a: argparse.Namespace) -> None:
    hedef = [k for k in tum_anahtarlar() if str(k.get("name", "")).startswith(a.onek) and not k.get("disabled")]
    for k in hedef:
        istek("PATCH", f"/keys/{k['hash']}", {"disabled": True})
        print(f"kapatıldı: {k.get('name')}")
    print(f"{len(hedef)} anahtar devre dışı.")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    alt = p.add_subparsers(dest="komut", required=True)
    o = alt.add_parser("olustur", help="limitli anahtarlar üret")
    o.add_argument("--onek", default="ogr", help="anahtar adı öneki (ogr-01, ogr-02 …)")
    o.add_argument("--adet", type=int, required=True)
    o.add_argument("--baslangic", type=int, default=1, help="ilk sıra numarası (sonradan ekleme için)")
    o.add_argument("--limit", type=float, default=1.0, help="anahtar başına USD harcama limiti")
    o.add_argument("--sifirlama", choices=["daily", "weekly", "monthly"], help="limit periyodik sıfırlansın")
    o.add_argument("--cikti", default="anahtarlar.csv")
    o.add_argument("--uzerine-yaz", action="store_true")
    o.set_defaults(f=olustur)
    l = alt.add_parser("listele", help="ad, limit, harcama")
    l.add_argument("--onek", default="")
    l.set_defaults(f=listele)
    k = alt.add_parser("kapat", help="öneke uyan anahtarları devre dışı bırak")
    k.add_argument("--onek", required=True)
    k.set_defaults(f=kapat)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
