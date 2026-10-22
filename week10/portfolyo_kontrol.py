"""
week10 · portfolyo_kontrol.py — bir GitHub reposunu işe alımcı gözüyle 10 maddede kontrol et.

Yalnızca standart kütüphane (urllib) + GitHub REST API. Public repolar için anahtar gerekmez;
saatte 60 istek sınırına takılırsanız .env'e GITHUB_TOKEN ekleyin (ya da export edin).

Kullanım:
  python portfolyo_kontrol.py https://github.com/<kullanici>/<repo>
  python portfolyo_kontrol.py <kullanici>/<repo> --json
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

try:
    from dotenv import find_dotenv, load_dotenv
    load_dotenv(find_dotenv())
except ImportError:
    pass

API = "https://api.github.com"


def istek(yol: str) -> dict | None:
    basliklar = {"Accept": "application/vnd.github+json", "User-Agent": "portfolyo-kontrol"}
    if os.getenv("GITHUB_TOKEN"):
        basliklar["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    try:
        with urllib.request.urlopen(urllib.request.Request(API + yol, headers=basliklar), timeout=20) as y:
            return json.load(y)
    except urllib.error.HTTPError as h:
        if h.code == 404:
            return None
        if h.code == 409:
            raise SystemExit("Repo boş görünüyor (hiç commit yok). Önce README ile ilk commit'i atın.") from h
        if h.code in (403, 429):
            raise SystemExit("GitHub API sınırı (403/429). .env'e GITHUB_TOKEN ekleyin ya da bir saat bekleyin.") from h
        raise SystemExit(f"GitHub API hatası {h.code}: {h.reason} ({yol})") from h
    except urllib.error.URLError as u:
        raise SystemExit(f"Ağ hatası: {u.reason}. İnternet / proxy ayarlarını kontrol edin.") from u


def repo_adi(girdi: str) -> tuple[str, str]:
    e = re.search(r"github\.com[/:]([^/]+)/([^/.\s]+)", girdi)
    if e:
        return e.group(1), e.group(2)
    if "/" in girdi:
        o, r = girdi.split("/", 1)
        return o, r.strip("/")
    raise SystemExit("Repo biçimi: https://github.com/kullanici/repo ya da kullanici/repo")


def kontrol(owner: str, repo: str) -> dict:
    meta = istek(f"/repos/{owner}/{repo}")
    if meta is None:
        raise SystemExit(f"Repo bulunamadı ya da private: {owner}/{repo} (portfolyo public olmalı)")
    dal = meta.get("default_branch") or "main"
    agac_yaniti = istek(f"/repos/{owner}/{repo}/git/trees/{dal}?recursive=1") or {}
    yollar = [e["path"] for e in agac_yaniti.get("tree", [])]
    readme_yaniti = istek(f"/repos/{owner}/{repo}/readme")
    readme = base64.b64decode(readme_yaniti["content"]).decode("utf-8", "replace") if readme_yaniti else ""
    rk = readme.lower()

    def var(desen: str) -> bool:
        return any(re.search(desen, y, re.I) for y in yollar)

    son_push = meta.get("pushed_at")
    gun = (datetime.now(timezone.utc) - datetime.fromisoformat(son_push.replace("Z", "+00:00"))).days if son_push else 9999
    demo = bool(meta.get("homepage")) or bool(re.search(r"https?://\S+\.(streamlit\.app|azurecontainerapps\.io|hf\.space|vercel\.app|azurewebsites\.net)", readme))

    maddeler = [
        ("README var ve dolu (≥400 karakter)", len(readme) >= 400, "README'yi proje_readme_sablonu.md ile doldurun"),
        ("README: kurulum / çalıştırma bölümü", bool(re.search(r"kurulum|çalıştır|calistir|install|getting started|usage|how to run", rk)), "Kopyala-yapıştır çalışan kurulum komutları ekleyin"),
        ("README: 'AI kullanımı' bölümü (ders kuralı)", bool(re.search(r"ai kullan|yapay zeka kullan|ai usage|ai-assisted|ai disclosure", rk)), "Hangi araç, ajanın hatası, sizin düzeltmeniz"),
        ("README: değerlendirme / eval sonuçları", bool(re.search(r"eval|değerlendirme|degerlendirme|metrik|benchmark|test sonu", rk)), "Sayı verin: x/15, sadakat 0.9, red team 10/12"),
        ("README: maliyet ya da mimari", bool(re.search(r"maliyet|cost|mimari|architecture|token", rk)), "İstek başına maliyet + tek şema"),
        (".env.example var, .env YOK", var(r"(^|/)\.env\.example$") and not var(r"(^|/)\.env$"), "`.env` commit'lenmişse anahtarı HEMEN yenileyin ve geçmişten temizleyin"),
        ("Testler var (tests/ ya da test_*.py)", var(r"(^|/)tests?/") or var(r"(^|/)test_[^/]+\.py$") or var(r"[^/]+_test\.py$") or var(r"\.(test|spec)\.[jt]sx?$"), "En az 5 ağsız test; CI'da çalıştırın"),
        ("Bağımlılık dosyası (requirements.txt / pyproject / package.json)", var(r"(^|/)(requirements[^/]*\.txt|pyproject\.toml|package\.json|uv\.lock)$"), "Sürümlü bağımlılık listesi"),
        ("LICENSE var", var(r"(^|/)LICENSE") or bool(meta.get("license")), "MIT ekleyin (GitHub → Add file → License)"),
        ("Açıklama + topics + son 90 günde push", bool(meta.get("description")) and len(meta.get("topics") or []) >= 1 and gun <= 90, "Repo → About → açıklama ve en az 3 topic; aktif tutun"),
    ]
    bonus = [
        ("CI iş akışı (.github/workflows)", var(r"^\.github/workflows/.+\.ya?ml$")),
        ("Dockerfile", var(r"(^|/)Dockerfile$")),
        ("Canlı demo bağlantısı", demo),
        ("Ekran görüntüsü / görsel", var(r"\.(png|gif|jpe?g|webp)$") or "![" in readme),
    ]
    puan = sum(1 for _, ok, _ in maddeler if ok)
    return {"repo": f"{owner}/{repo}", "dal": dal, "dosya_sayisi": len(yollar), "agac_kesik": bool(agac_yaniti.get("truncated")),
            "son_push_gun": gun, "puan": puan, "maddeler": [{"madde": m, "ok": ok, "oneri": o} for m, ok, o in maddeler],
            "bonus": [{"madde": m, "ok": ok} for m, ok in bonus], "env_sizintisi": var(r"(^|/)\.env$")}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("repo")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    s = kontrol(*repo_adi(a.repo))
    if a.json:
        print(json.dumps(s, ensure_ascii=False, indent=2))
        return
    print(f"\n# {s['repo']}  ·  dal: {s['dal']}  ·  {s['dosya_sayisi']} dosya  ·  son push {s['son_push_gun']} gün önce\n")
    for m in s["maddeler"]:
        print(f"{'✓' if m['ok'] else '✗'} {m['madde']}" + ("" if m["ok"] else f"\n    → {m['oneri']}"))
    print("\nBonus: " + " · ".join(f"{'✓' if b['ok'] else '–'} {b['madde']}" for b in s["bonus"]))
    print(f"\nPUAN: {s['puan']}/10" + ("  🎉 işe alımcıya hazır" if s["puan"] >= 9 else "  → eksikleri kapatın, tekrar çalıştırın" if s["puan"] >= 6 else "  → önce README ve .env.example"))
    if s["env_sizintisi"]:
        print("\n⚠️  .env repoda! Anahtarı hemen yenileyin (sızmış sayılır) ve dosyayı geçmişten silin (git filter-repo).")
    if s["agac_kesik"]:
        print("Not: repo çok büyük, dosya listesi kesildi; bazı kontroller eksik olabilir.")


if __name__ == "__main__":
    sys.exit(main())
