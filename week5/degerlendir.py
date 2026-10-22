"""
week5 · degerlendir.py — RAG'ı ölçmek: RAGAS'ın yaptığı şeyi şeffaf biçimde, ~100 satırda.

Her soru için:
  1) kaynak_isabeti   (deterministik) getirilen parçaların kaçı doğru belgeden? → context precision
  2) baglam_kapsami   (deterministik) gerçek cevabın anahtar kelimeleri bağlamda var mı? → context recall
  3) sadakat          (LLM hakem)     cevaptaki iddiaların kaçı bağlamla destekleniyor? → faithfulness
  4) ilgililik        (LLM hakem)     cevap soruya ne kadar odaklı? 0-5 → answer relevancy
  5) dogruluk         (LLM hakem)     cevap gerçek cevapla örtüşüyor mu? → answer correctness

Kullanım:
  python degerlendir.py                                 # hibrit, k=4, tüm sorular
  python degerlendir.py --yontem vektor --k 3           # getirme yöntemini değiştir, karşılaştır
  python degerlendir.py --indeks indeks_sabit.pkl       # başka bir parçalama ile kurulan indeks
  python degerlendir.py --sinir 3 --json                # hızlı deneme / makine okunur çıktı

Gerçek RAGAS kütüphanesi (ragas.io) aynı metrikleri daha rafine hesaplar; README'de bağlantısı var.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from rag import INDEKS_DOSYASI, KOK, LLM_MODEL, Indeks, baglam_metni, cevapla, json_iste, tokenle

SADAKAT_SEMA = {
    "type": "object",
    "properties": {
        "iddialar": {
            "type": "array",
            "items": {"type": "object", "properties": {"iddia": {"type": "string"}, "destekleniyor": {"type": "boolean"}},
                      "required": ["iddia", "destekleniyor"]},
        }
    },
    "required": ["iddialar"],
}
ILGILILIK_SEMA = {"type": "object", "properties": {"puan": {"type": "integer", "description": "0-5"}, "gerekce": {"type": "string"}},
                  "required": ["puan", "gerekce"]}
DOGRULUK_SEMA = {"type": "object", "properties": {"dogru": {"type": "boolean"}, "aciklama": {"type": "string"}},
                 "required": ["dogru", "aciklama"]}

DURAK = {"nedir", "kadar", "hangi", "nasıl", "için", "olan", "veya", "gerekir", "günü", "gün", "iş"}


def anahtarlar(metin: str) -> set[str]:
    return {t for t in tokenle(metin) if (len(t) > 3 or t.isdigit()) and t not in DURAK}


def hakem_sadakat(cevap: str, baglam: str, model: str) -> float | None:
    if "el kitabında yok" in cevap.lower():
        return None                                   # iddia yok, sadakat ölçülmez
    veri = json_iste([
        {"role": "system", "content": "Sen titiz bir denetçisin. Cevabı atomik iddialara böl; her iddia yalnızca verilen bağlamdan çıkarılabiliyorsa destekleniyor=true, aksi halde false."},
        {"role": "user", "content": f"Bağlam:\n{baglam}\n\nCevap:\n{cevap}"},
    ], SADAKAT_SEMA, model, "sadakat")
    iddialar = veri.get("iddialar") or []
    return sum(1 for i in iddialar if i.get("destekleniyor")) / len(iddialar) if iddialar else None


def hakem_ilgililik(soru: str, cevap: str, model: str) -> float:
    veri = json_iste([
        {"role": "system", "content": "Cevabın soruya ne kadar odaklı ve eksiksiz olduğunu 0 (alakasız) ile 5 (tam ve odaklı) arasında puanla. Doğruluğu değil, odaklanmayı ölç."},
        {"role": "user", "content": f"Soru: {soru}\nCevap: {cevap}"},
    ], ILGILILIK_SEMA, model, "ilgililik")
    return max(0, min(5, int(veri.get("puan", 0)))) / 5


def hakem_dogruluk(soru: str, cevap: str, gercek: str, model: str) -> bool:
    veri = json_iste([
        {"role": "system", "content": "Verilen cevap, gerçek cevapla anlamca örtüşüyorsa dogru=true. Sayılar ve koşullar farklıysa false. Fazladan doğru bilgi hata değildir."},
        {"role": "user", "content": f"Soru: {soru}\nGerçek cevap: {gercek}\nVerilen cevap: {cevap}"},
    ], DOGRULUK_SEMA, model, "dogruluk")
    return bool(veri.get("dogru", False))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sorular", default=str(KOK / "sorular.json"))
    p.add_argument("--indeks", default=str(INDEKS_DOSYASI))
    p.add_argument("--qdrant-url", default=None)
    p.add_argument("--k", type=int, default=4)
    p.add_argument("--yontem", default="hibrit", choices=["hibrit", "vektor", "bm25"])
    p.add_argument("--hakem-model", default=LLM_MODEL)
    p.add_argument("--sinir", type=int, help="İlk N soruyla sınırla")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    sorular = json.loads(Path(a.sorular).read_text(encoding="utf-8"))[: a.sinir]
    indeks = Indeks.yukle(a.indeks, a.qdrant_url)
    satirlar = []
    for s in sorular:
        sonuc = cevapla(indeks, s["soru"], a.k, a.yontem)
        baglam = baglam_metni(sonuc["baglamlar"])
        getirilen_belgeler = [b["parca"].belge for b in sonuc["baglamlar"]]
        if s["kaynak"]:
            isabet = sum(1 for b in getirilen_belgeler if b == s["kaynak"]) / len(getirilen_belgeler)
            anahtar = anahtarlar(s["gercek_cevap"])
            baglam_tok = set(tokenle(baglam))
            kapsam = len(anahtar & baglam_tok) / len(anahtar) if anahtar else None
        else:
            isabet, kapsam = None, None
        satirlar.append({
            "soru": s["soru"], "cevap": sonuc["cevap"], "kaynak": s["kaynak"], "getirilen": getirilen_belgeler,
            "kaynak_isabeti": isabet, "baglam_kapsami": kapsam,
            "sadakat": hakem_sadakat(sonuc["cevap"], baglam, a.hakem_model),
            "ilgililik": hakem_ilgililik(s["soru"], sonuc["cevap"], a.hakem_model),
            "dogru": hakem_dogruluk(s["soru"], sonuc["cevap"], s["gercek_cevap"], a.hakem_model),
            "girdi_token": sonuc["girdi_token"], "sure_ms": sonuc["sure_ms"],
        })
        if not a.json:
            print(f"✓ {s['soru'][:60]}")

    def ort(alan: str) -> float | None:
        degerler = [r[alan] for r in satirlar if r[alan] is not None]
        return sum(degerler) / len(degerler) if degerler else None

    ozet = {"yontem": a.yontem, "k": a.k, "indeks": a.indeks, "soru_sayisi": len(satirlar),
            "ort_kaynak_isabeti": ort("kaynak_isabeti"), "ort_baglam_kapsami": ort("baglam_kapsami"),
            "ort_sadakat": ort("sadakat"), "ort_ilgililik": ort("ilgililik"),
            "dogruluk_orani": sum(1 for r in satirlar if r["dogru"]) / len(satirlar),
            "ort_girdi_token": ort("girdi_token")}
    if a.json:
        print(json.dumps({"ozet": ozet, "satirlar": satirlar}, ensure_ascii=False, indent=2))
        return

    def f(x):
        return "—" if x is None else f"{x:.2f}"

    print(f"\n## Değerlendirme · yöntem={a.yontem} k={a.k} indeks={Path(a.indeks).name} hakem={a.hakem_model}\n")
    print("| Soru | Kaynak isabeti | Bağlam kapsamı | Sadakat | İlgililik | Doğru | Girdi tok |")
    print("|---|---:|---:|---:|---:|:-:|---:|")
    for r in satirlar:
        print(f"| {r['soru'][:48]} | {f(r['kaynak_isabeti'])} | {f(r['baglam_kapsami'])} | {f(r['sadakat'])} | {f(r['ilgililik'])} | {'✓' if r['dogru'] else '✗'} | {r['girdi_token']} |")
    print(f"| **Ortalama** | **{f(ozet['ort_kaynak_isabeti'])}** | **{f(ozet['ort_baglam_kapsami'])}** | **{f(ozet['ort_sadakat'])}** | **{f(ozet['ort_ilgililik'])}** | **{ozet['dogruluk_orani']:.0%}** | {ozet['ort_girdi_token']:.0f} |")
    print("\nOkuma: kaynak isabeti/bağlam kapsamı düşükse sorun GETİRME'de (parçalama, k, yöntem); sadakat düşükse sorun ÜRETİM'de (prompt, model).")
    print("Son soru ('ciro') tuzaktır: doğru davranış 'Bu bilgi el kitabında yok.' demektir.")


if __name__ == "__main__":
    main()
