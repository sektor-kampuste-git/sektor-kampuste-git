"""
week8 · eval_calistir.py — 15 eval, saf Python, CI'da çalışır. promptfoo'nun yaptığı şeyin şeffaf hali.

Her vaka: 'icermeli' (hepsi geçmeli), 'icermemeli' (hiçbiri geçmemeli), isteğe bağlı 'rubrik' (LLM hakem, evet/hayır).
Çıkış kodu: geçen sayısı eşiğin altındaysa 1 → CI kırmızı. "v2 v1'den iyi mi?" sorusu böyle cevaplanır.

Kullanım:
  python eval_calistir.py                                   # v2, eşik 13/15
  python eval_calistir.py --prompt promptlar/v1.txt         # v1 ile karşılaştır
  python eval_calistir.py --esik 15 --hakem-yok             # yalnızca deterministik kontroller
  python eval_calistir.py --json > rapor_v2.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from openai import OpenAI

from asistan import KOK, cevapla


def hakem(soru: str, cevap: str, rubrik: str, model: str) -> bool:
    istemci = OpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ["LLM_API_KEY"])
    y = istemci.chat.completions.create(model=model, temperature=0, max_tokens=5, messages=[
        {"role": "system", "content": "Sen bir değerlendiricisin. Soruya yalnızca EVET ya da HAYIR diye cevap ver."},
        {"role": "user", "content": f"Kullanıcı sorusu: {soru}\nAsistan cevabı: {cevap}\n\nÖlçüt: {rubrik}\nCevap EVET mi HAYIR mı?"},
    ])
    return (y.choices[0].message.content or "").strip().upper().startswith("EVET")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", default="promptlar/v2.txt")
    p.add_argument("--evaller", default=str(KOK / "evaller.json"))
    p.add_argument("--esik", type=int, default=13)
    p.add_argument("--hakem-model", default=os.getenv("LLM_MODEL"))
    p.add_argument("--hakem-yok", action="store_true", help="Rubrik kontrollerini atla (sadece deterministik)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    vakalar = json.loads(Path(a.evaller).read_text(encoding="utf-8"))
    sonuclar, toplam_token = [], 0
    for v in vakalar:
        s = cevapla(v["soru"], a.prompt)
        cevap, kucuk = s["cevap"], s["cevap"].lower()
        toplam_token += s["girdi_token"] + s["cikti_token"]
        eksik = [x for x in v["icermeli"] if x.lower() not in kucuk]
        yasak = [x for x in v["icermemeli"] if x.lower() in kucuk]
        rubrik_sonuc = None
        if v.get("rubrik") and not a.hakem_yok:
            rubrik_sonuc = hakem(v["soru"], cevap, v["rubrik"], a.hakem_model)
        gecti = not eksik and not yasak and rubrik_sonuc is not False
        sonuclar.append({"id": v["id"], "gecti": gecti, "eksik": eksik, "yasak": yasak, "rubrik": rubrik_sonuc,
                         "cevap": cevap, "aciklama": v["aciklama"], "sure_ms": s["sure_ms"]})
        if not a.json:
            durum = "✓" if gecti else "✗"
            neden = (f" eksik={eksik}" if eksik else "") + (f" yasak={yasak}" if yasak else "") + (" rubrik=HAYIR" if rubrik_sonuc is False else "")
            print(f"{durum} {v['id']} {v['aciklama'][:48]:48}{neden}")

    gecen = sum(1 for r in sonuclar if r["gecti"])
    ozet = {"prompt": a.prompt, "gecen": gecen, "toplam": len(sonuclar), "esik": a.esik, "toplam_token": toplam_token,
            "basarili": gecen >= a.esik}
    if a.json:
        print(json.dumps({"ozet": ozet, "sonuclar": sonuclar}, ensure_ascii=False, indent=2))
    else:
        print(f"\n{gecen}/{len(sonuclar)} geçti · eşik {a.esik} · {toplam_token} token · prompt: {a.prompt}")
        print("SONUÇ:", "BAŞARILI ✅" if ozet["basarili"] else "BAŞARISIZ ❌ (CI kırmızı)")
    return 0 if ozet["basarili"] else 1


if __name__ == "__main__":
    sys.exit(main())
