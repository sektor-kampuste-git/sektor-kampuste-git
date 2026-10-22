"""
week4 · maliyet_hesapla.py — bir iş yükü için aylık LLM faturası ve dört fiyat kaldıracı.

Kaldıraçlar (Hafta 1'den):
  1. Girdi ve çıktı tokenları   → çıktı 4-5× pahalı
  2. İstem önbellekleme        → tekrar eden girdi %60-90 ucuz
  3. Model kademeleri          → kolay işi ucuz modele yönlendir
  4. Hızlı mod                 → aynı model, 2× fiyat (yalnızca gecikme kritikse)

Kullanım:
  python maliyet_hesapla.py --senaryo senaryolar/destek_botu.json
  python maliyet_hesapla.py --senaryo senaryolar/kod_ajani.json --ucuz-model deepseek-v4.1-flash
  python maliyet_hesapla.py --senaryo senaryolar/sozlesme_ozet.json --model claude-opus-5.5 --model gpt-6-sol
  python maliyet_hesapla.py --senaryo senaryolar/destek_botu.json --onbellek 0 --kolay 0   # kaldıraçları kapat
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def yukle(yol: str | Path) -> dict:
    return json.loads(Path(yol).read_text(encoding="utf-8"))


def aylik(model: dict, s: dict, onbellek: float, hizli: bool = False) -> float:
    """Tek modelin aylık maliyeti (USD). onbellek: 0-1 arası, girdinin önbellekten gelen payı."""
    istek = s["gunluk_istek"] * s["ay_gun"]
    girdi_tok = istek * s["girdi_token_ort"]
    cikti_tok = istek * s["cikti_token_ort"]
    girdi_f, cikti_f = model["girdi"], model["cikti"]
    if hizli:
        hm = model.get("hizli_mod")
        if not hm:
            return float("nan")
        girdi_f, cikti_f = hm["girdi"], hm["cikti"]
    onbellek_f = model.get("onbellek_okuma", girdi_f)
    return (
        girdi_tok * (1 - onbellek) / 1e6 * girdi_f
        + girdi_tok * onbellek / 1e6 * onbellek_f
        + cikti_tok / 1e6 * cikti_f
    )


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--senaryo", default="senaryolar/destek_botu.json")
    p.add_argument("--fiyatlar", default=str(Path(__file__).with_name("fiyatlar.json")))
    p.add_argument("--model", action="append", help="Yalnızca bu modelleri göster (tekrarlanabilir)")
    p.add_argument("--ucuz-model", default="gpt-6-luna", help="Kolay işlerin yönlendirileceği ucuz model")
    p.add_argument("--onbellek", type=float, help="Senaryodaki önbellek oranını ez (0-1)")
    p.add_argument("--kolay", type=float, help="Senaryodaki kolay iş oranını ez (0-1)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    s = yukle(a.senaryo)
    fiyat = yukle(a.fiyatlar)
    modeller = [m for m in fiyat["modeller"] if m["kademe"] != "yerel"]
    if a.model:
        istenen = {x.lower() for x in a.model}
        modeller = [m for m in modeller if m["id"].lower() in istenen]
    onbellek = s["onbellek_orani"] if a.onbellek is None else a.onbellek
    kolay = s["kolay_is_orani"] if a.kolay is None else a.kolay
    ucuz = next((m for m in fiyat["modeller"] if m["id"].lower() == a.ucuz_model.lower()), None)
    if ucuz is None:
        raise SystemExit(f"Ucuz model bulunamadı: {a.ucuz_model}")

    istek_ay = s["gunluk_istek"] * s["ay_gun"]
    satirlar = []
    for m in modeller:
        temel = aylik(m, s, 0.0)
        onbellekli = aylik(m, s, onbellek)
        kademeli = onbellekli * (1 - kolay) + aylik(ucuz, s, onbellek) * kolay
        hizli = aylik(m, s, onbellek, hizli=True)
        satirlar.append({
            "model": m["id"], "kademe": m["kademe"], "temel": temel, "onbellekli": onbellekli,
            "kademeli": kademeli, "hizli": hizli, "istek_basi_cent": kademeli / istek_ay * 100,
            "cikti_payi": (istek_ay * s["cikti_token_ort"] / 1e6 * m["cikti"]) / temel if temel else 0,
        })
    satirlar.sort(key=lambda r: r["kademeli"])

    insan = s.get("insan_karsiligi")
    insan_aylik = istek_ay * insan["dakika_per_istek"] / 60 * insan["saatlik_maliyet_usd"] if insan else None

    if a.json:
        print(json.dumps({"senaryo": s["ad"], "onbellek": onbellek, "kolay": kolay, "ucuz_model": ucuz["id"],
                          "insan_aylik_usd": insan_aylik, "modeller": satirlar}, ensure_ascii=False, indent=2))
        return

    print(f"\n# {s['ad']}")
    print(f"{s['aciklama']}\n")
    print(f"- İstek/ay: {istek_ay:,}  · girdi {s['girdi_token_ort']:,} tok · çıktı {s['cikti_token_ort']:,} tok")
    print(f"- Önbellek oranı: {onbellek:.0%} · kolay iş oranı: {kolay:.0%} → ucuz model: {ucuz['id']}")
    if insan_aylik:
        print(f"- Aynı işi insan yapsaydı: ~${insan_aylik:,.0f}/ay ({insan['dakika_per_istek']} dk × ${insan['saatlik_maliyet_usd']}/saat)")
    print()
    print("| Model | Kademe | Temel $/ay | +Önbellek | +Kademeli | Tasarruf | ¢/istek | Çıktı payı | Hızlı mod |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in satirlar:
        tasarruf = 1 - r["kademeli"] / r["temel"] if r["temel"] else 0
        hizli = f"${r['hizli']:,.0f}" if r["hizli"] == r["hizli"] else "—"  # NaN kontrolü
        print(f"| {r['model']} | {r['kademe']} | ${r['temel']:,.0f} | ${r['onbellekli']:,.0f} | ${r['kademeli']:,.0f} "
              f"| {tasarruf:.0%} | {r['istek_basi_cent']:.3f} | {r['cikti_payi']:.0%} | {hizli} |")
    print()
    print("Okuma rehberi:")
    print("  • 'Temel' = liste fiyatı, kaldıraç yok.  '+Önbellek' = tekrar eden girdi önbellekten.  '+Kademeli' = kolay işler ucuz modelde.")
    print("  • 'Çıktı payı' yüksekse cevapları kısaltmak (max_tokens, 'iki cümlede') faturayı doğrudan düşürür.")
    print("  • Fiyatlar fiyatlar.json'daki tarihe aittir; sağlayıcı sayfasından doğrulayın. Yerel modeller tabloda yok: token başına $0, ama donanım + operasyon sizin.")


if __name__ == "__main__":
    main()
