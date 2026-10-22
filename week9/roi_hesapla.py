"""
week9 · roi_hesapla.py — bir yapay zeka kullanım senaryosunun aylık getirisi, maliyeti, geri ödeme süresi ve duyarlılığı.

Formül (şeffaf, tartışılabilir):
  tasarruf      = istek × (dakika_önce − dakika_sonra)/60 × saatlik_maliyet
  token_maliyet = Hafta 4 fiyat tablosu + önbellek oranı
  hata_maliyet  = istek × hata_oranı × hata_maliyeti      (eval'ınız bu oranı verir — Hafta 8)
  bakım         = saat × saatlik ücret ; platform = sabit
  net           = tasarruf − (token + hata + bakım + platform)
  geri ödeme    = kurulum / net   (ay)

Kullanım:
  python roi_hesapla.py --senaryo senaryolar/hasar_triyaj.json
  python roi_hesapla.py --senaryo senaryolar/destek_botu.json --hata-orani 0.15     # eval kötüyse?
  python roi_hesapla.py --senaryo senaryolar/cv_eleme_yanlis_ornek.json             # yüksek riskli örnek
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

KOK = Path(__file__).parent


def fiyat(model: str) -> dict:
    tablo = json.loads((KOK / "fiyatlar.json").read_text(encoding="utf-8"))["modeller"]
    for m in tablo:
        if m["id"].lower() == model.lower():
            return m
    raise SystemExit(f"Model fiyat tablosunda yok: {model} (fiyatlar.json)")


def hesapla(s: dict, hata_orani: float | None = None, onbellek: float | None = None) -> dict:
    istek = s["gunluk_istek"] * s["ay_gun"]
    ins = s["insan"]
    hata_orani = s["hata_orani"] if hata_orani is None else hata_orani
    onbellek = s["onbellek_orani"] if onbellek is None else onbellek
    f = fiyat(s["model"])

    tasarruf = istek * (ins["dakika_per_istek_once"] - ins["dakika_per_istek_sonra"]) / 60 * ins["saatlik_maliyet_usd"]
    girdi_tok, cikti_tok = istek * s["girdi_token_ort"], istek * s["cikti_token_ort"]
    token = (girdi_tok * (1 - onbellek) * f["girdi"] + girdi_tok * onbellek * f.get("onbellek_okuma", f["girdi"]) + cikti_tok * f["cikti"]) / 1e6
    hata = istek * hata_orani * s["hata_maliyeti_usd"]
    bakim = s["aylik_bakim_saat"] * s["bakim_saatlik_usd"]
    platform = s["aylik_platform_usd"]
    maliyet = token + hata + bakim + platform
    net = tasarruf - maliyet
    return {
        "istek_ay": istek, "tasarruf": tasarruf, "token": token, "hata": hata, "bakim": bakim, "platform": platform,
        "maliyet": maliyet, "net": net, "roi_yuzde": (net / maliyet * 100) if maliyet else float("inf"),
        "geri_odeme_ay": (s["kurulum_maliyeti_usd"] / net) if net > 0 else None,
        "hata_orani": hata_orani, "onbellek": onbellek, "insan_saat_tasarrufu": istek * (ins["dakika_per_istek_once"] - ins["dakika_per_istek_sonra"]) / 60,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--senaryo", default=str(KOK / "senaryolar/hasar_triyaj.json"))
    p.add_argument("--hata-orani", type=float, help="Senaryodaki hata oranını ez (eval sonucunuz)")
    p.add_argument("--onbellek", type=float, help="Önbellek oranını ez")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    s = json.loads(Path(a.senaryo).read_text(encoding="utf-8"))
    r = hesapla(s, a.hata_orani, a.onbellek)
    if a.json:
        print(json.dumps({"senaryo": s["ad"], **r}, ensure_ascii=False, indent=2))
        return

    def usd(x: float) -> str:
        return f"${x:,.0f}"

    print(f"\n# {s['ad']}\n{s['aciklama']}\n")
    print(f"İstek/ay: {r['istek_ay']:,} · model: {s['model']} · önbellek {r['onbellek']:.0%} · hata oranı {r['hata_orani']:.0%}\n")
    print("| Kalem | Aylık USD |")
    print("|---|---:|")
    print(f"| **Tasarruf** (insan süresi: {r['insan_saat_tasarrufu']:,.0f} saat) | **{usd(r['tasarruf'])}** |")
    print(f"| Token (model) | −{usd(r['token'])} |")
    print(f"| Hata maliyeti ({r['hata_orani']:.0%} × ${s['hata_maliyeti_usd']}) | −{usd(r['hata'])} |")
    print(f"| Bakım ({s['aylik_bakim_saat']} saat) | −{usd(r['bakim'])} |")
    print(f"| Platform / altyapı | −{usd(r['platform'])} |")
    print(f"| **Net** | **{usd(r['net'])}** |")
    print(f"| ROI (net / maliyet) | {r['roi_yuzde']:.0f}% |")
    geri = f"{r['geri_odeme_ay']:.1f} ay" if r["geri_odeme_ay"] else "— (net negatif)"
    print(f"| Kurulum {usd(s['kurulum_maliyeti_usd'])} → geri ödeme | {geri} |")

    print("\nDuyarlılık — hata oranı değişirse net ne olur?")
    print("| Hata oranı | Net/ay | Geri ödeme |")
    print("|---:|---:|---:|")
    for h in sorted({r["hata_orani"] / 2, r["hata_orani"], r["hata_orani"] * 2, r["hata_orani"] * 4}):
        rr = hesapla(s, h, a.onbellek)
        g = f"{rr['geri_odeme_ay']:.1f} ay" if rr["geri_odeme_ay"] else "—"
        print(f"| {h:.1%} | {usd(rr['net'])} | {g} |")
    print("\nOkuma: token maliyeti çoğu senaryoda en küçük kalem; faturayı HATA ve BAKIM belirler. Eval seti (Hafta 8) hata oranını verir; eval'siz ROI tahmindir.")
    print("Yüksek riskli alanlarda (İK, kredi) hata maliyeti büyüktür: model yalnızca öneri üretir, insan karar verir; 'dakika_sonra' bu yüzden fazla düşmez.")


if __name__ == "__main__":
    main()
