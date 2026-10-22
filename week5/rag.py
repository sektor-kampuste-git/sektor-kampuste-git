"""
week5 · rag.py — RAG'ın parçaları, tek dosyada ve okunabilir:

  tokenle()   → Türkçe'ye uygun kaba tokenleme (BM25 için)
  parcala()   → üç parçalama (chunking) yöntemi: sabit / paragraf / cümle
  gom()       → OpenAI uyumlu embeddings çağrısı (Gemini, Foundry, Ollama, sahte sunucu)
  Indeks      → Qdrant (bellek içi ya da sunucu) + BM25; vektör / bm25 / hibrit (RRF) getirme
  cevapla()   → bağlamla sınırlı, kaynak numaralı Türkçe cevap
  json_iste() → hakem (judge) çağrıları için şemalı JSON

Diğer dosyalar (gomme_demo, parcala, indeksle, sor, degerlendir) bu modülü kullanır.
"""
from __future__ import annotations

import json
import os
import pickle
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient, models
from rank_bm25 import BM25Okapi

load_dotenv(find_dotenv())

KOK = Path(__file__).parent
DERLEM = KOK / "derlem"
INDEKS_DOSYASI = KOK / "indeks.pkl"
KOLEKSIYON = "elkitabi"

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-6-luna")
EMBED_MODEL = os.getenv("EMBED_MODEL", "gemini-embedding-001")


# ----------------------------------------------------------------- istemciler
def llm_istemci() -> OpenAI:
    return OpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ["LLM_API_KEY"])


def embed_istemci() -> OpenAI:
    base = os.getenv("EMBED_BASE_URL") or os.environ["LLM_BASE_URL"]
    key = os.getenv("EMBED_API_KEY") or os.environ["LLM_API_KEY"]
    return OpenAI(base_url=base, api_key=key)


# ----------------------------------------------------------------- tokenleme
_TR = str.maketrans("IİÇĞÖŞÜ", "ıiçğöşü")


def tr_kucult(metin: str) -> str:
    """Python'ın lower()'ı 'I'→'i' yapar; Türkçe'de 'I'→'ı' olmalı."""
    return metin.translate(_TR).lower()


def tokenle(metin: str, kok_uzunlugu: int = 6) -> list[str]:
    """
    Kaba Türkçe tokenleme: küçült, kelimeleri al, uzun kelimeleri ilk 6 harfe kırp.
    'izinler', 'iznim', 'izinleri' → 'izinle', 'iznim', 'izinle'  (mükemmel değil, ama BM25'e çok yardım eder).
    Daha iyisi için: zeyrek, TurkishStemmer ya da snowball 'turkish'.
    """
    kelimeler = re.findall(r"\w+", tr_kucult(metin))
    return [k[:kok_uzunlugu] if len(k) > kok_uzunlugu else k for k in kelimeler]


# ----------------------------------------------------------------- parçalama
def parcala(metin: str, yontem: str = "paragraf", boyut: int = 600, ortusme: int = 100) -> list[str]:
    """Metni parçalara böl. boyut/ortusme karakter cinsindendir."""
    metin = metin.strip()
    if yontem == "sabit":
        parcalar, i = [], 0
        while i < len(metin):
            son = min(len(metin), i + boyut)
            if son < len(metin):                       # kelimeyi ortadan kesme
                bosluk = metin.rfind(" ", i, son)
                if bosluk > i + boyut // 2:
                    son = bosluk
            parcalar.append(metin[i:son].strip())
            if son >= len(metin):
                break
            i = max(son - ortusme, i + 1)
        return [p for p in parcalar if p]

    if yontem == "paragraf":
        bloklar = [b.strip() for b in re.split(r"\n\s*\n", metin) if b.strip()]
        parcalar, mevcut = [], ""
        for b in bloklar:
            aday = (mevcut + "\n\n" + b).strip() if mevcut else b
            if b.startswith("#"):
                # Başlık: önceki parça kısaysa (örn. yalnızca üst başlık) ona ekle,
                # değilse önceki parçayı kapat; başlık bir sonraki paragrafla aynı parçada kalsın.
                if mevcut and len(mevcut) < boyut // 3:
                    mevcut = aday
                else:
                    if mevcut:
                        parcalar.append(mevcut)
                    mevcut = b
                continue
            if len(aday) <= boyut or not mevcut:
                mevcut = aday
            else:
                parcalar.append(mevcut)
                mevcut = b
        if mevcut:
            parcalar.append(mevcut)
        return parcalar

    if yontem == "cumle":
        cumleler = [c.strip() for c in re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9#])", metin.replace("\n", " ")) if c.strip()]
        parcalar, pencere = [], []
        for c in cumleler:
            pencere.append(c)
            if sum(len(x) for x in pencere) >= boyut:
                parcalar.append(" ".join(pencere))
                pencere = pencere[-1:]                 # 1 cümle örtüşme
        if pencere and (not parcalar or " ".join(pencere) != parcalar[-1]):
            parcalar.append(" ".join(pencere))
        return parcalar

    raise ValueError(f"Bilinmeyen yöntem: {yontem} (sabit | paragraf | cumle)")


@dataclass
class Parca:
    id: int
    belge: str
    baslik: str
    metin: str


def derlemi_yukle(klasor: Path = DERLEM) -> list[tuple[str, str, str]]:
    """[(dosya_adi, baslik, metin), ...]"""
    belgeler = []
    for yol in sorted(klasor.glob("*.md")):
        metin = yol.read_text(encoding="utf-8")
        baslik = next((s.lstrip("# ").strip() for s in metin.splitlines() if s.startswith("# ")), yol.stem)
        belgeler.append((yol.name, baslik, metin))
    return belgeler


def parcalari_olustur(yontem: str = "paragraf", boyut: int = 600, ortusme: int = 100, klasor: Path = DERLEM) -> list[Parca]:
    parcalar: list[Parca] = []
    for dosya, baslik, metin in derlemi_yukle(klasor):
        for p in parcala(metin, yontem, boyut, ortusme):
            parcalar.append(Parca(len(parcalar), dosya, baslik, p))
    return parcalar


# ----------------------------------------------------------------- gömme
def gom(metinler: list[str], model: str = EMBED_MODEL, parti: int = 32) -> list[list[float]]:
    """Metinleri vektöre çevir. Her sağlayıcı aynı OpenAI 'embeddings' biçimini konuşur."""
    istemci = embed_istemci()
    vektorler: list[list[float]] = []
    for i in range(0, len(metinler), parti):
        yanit = istemci.embeddings.create(model=model, input=metinler[i:i + parti])
        vektorler.extend(d.embedding for d in sorted(yanit.data, key=lambda d: d.index))
    return vektorler


# ----------------------------------------------------------------- indeks
class Indeks:
    """Vektör (Qdrant) + anahtar kelime (BM25) indeksi."""

    def __init__(self, parcalar: list[Parca], vektorler: list[list[float]], qdrant_url: str | None = None,
                 embed_model: str = EMBED_MODEL):
        if len(parcalar) != len(vektorler):
            raise ValueError("parça ve vektör sayısı eşleşmiyor")
        self.parcalar = parcalar
        self.vektorler = vektorler
        self.embed_model = embed_model
        self.qdrant = QdrantClient(url=qdrant_url) if qdrant_url else QdrantClient(":memory:")
        boyut = len(vektorler[0])
        if self.qdrant.collection_exists(KOLEKSIYON):
            self.qdrant.delete_collection(KOLEKSIYON)
        self.qdrant.create_collection(
            KOLEKSIYON, vectors_config=models.VectorParams(size=boyut, distance=models.Distance.COSINE)
        )
        self.qdrant.upsert(
            KOLEKSIYON,
            points=[
                models.PointStruct(id=p.id, vector=v, payload={"belge": p.belge, "baslik": p.baslik})
                for p, v in zip(parcalar, vektorler)
            ],
        )
        self.bm25 = BM25Okapi([tokenle(p.metin) for p in parcalar])

    # --- kalıcılık: vektörleri yeniden hesaplamamak için pickle
    def kaydet(self, yol: Path = INDEKS_DOSYASI) -> None:
        yol.write_bytes(pickle.dumps({
            "parcalar": [asdict(p) for p in self.parcalar], "vektorler": self.vektorler, "embed_model": self.embed_model,
        }))

    @classmethod
    def yukle(cls, yol: Path = INDEKS_DOSYASI, qdrant_url: str | None = None) -> "Indeks":
        if not Path(yol).exists():
            raise SystemExit(f"{yol} yok. Önce: python indeksle.py")
        veri = pickle.loads(Path(yol).read_bytes())
        return cls([Parca(**p) for p in veri["parcalar"]], veri["vektorler"], qdrant_url, veri.get("embed_model", EMBED_MODEL))

    # --- arama
    def vektor_ara(self, soru: str, k: int) -> list[tuple[int, float]]:
        sorgu = gom([soru], self.embed_model)[0]
        sonuc = self.qdrant.query_points(KOLEKSIYON, query=sorgu, limit=k).points
        return [(int(n.id), float(n.score)) for n in sonuc]

    def bm25_ara(self, soru: str, k: int) -> list[tuple[int, float]]:
        puanlar = self.bm25.get_scores(tokenle(soru))
        sirali = sorted(range(len(puanlar)), key=lambda i: puanlar[i], reverse=True)
        return [(i, float(puanlar[i])) for i in sirali[:k] if puanlar[i] > 0]

    def getir(self, soru: str, k: int = 4, yontem: str = "hibrit") -> list[dict]:
        """[{parca, puan, yontemler}] — hibrit: Reciprocal Rank Fusion (RRF), k=60."""
        if yontem == "vektor":
            adaylar = {i: {"puan": s, "yontemler": ["vektor"]} for i, s in self.vektor_ara(soru, k)}
        elif yontem == "bm25":
            adaylar = {i: {"puan": s, "yontemler": ["bm25"]} for i, s in self.bm25_ara(soru, k)}
        elif yontem == "hibrit":
            adaylar: dict[int, dict] = {}
            for ad, liste in (("vektor", self.vektor_ara(soru, 2 * k)), ("bm25", self.bm25_ara(soru, 2 * k))):
                for sira, (i, _) in enumerate(liste):
                    a = adaylar.setdefault(i, {"puan": 0.0, "yontemler": []})
                    a["puan"] += 1.0 / (60 + sira + 1)
                    a["yontemler"].append(ad)
        else:
            raise ValueError("yontem: vektor | bm25 | hibrit")
        sirali = sorted(adaylar.items(), key=lambda kv: kv[1]["puan"], reverse=True)[:k]
        return [{"parca": self.parcalar[i], **bilgi} for i, bilgi in sirali]


# ----------------------------------------------------------------- cevaplama
CEVAP_SISTEM = (
    "Sen Kampüs Teknoloji A.Ş. çalışan el kitabı asistanısın. YALNIZCA verilen bağlam parçalarını kullan. "
    "Bağlamda olmayan hiçbir bilgiyi uydurma; cevap bağlamda yoksa tam olarak şunu yaz: 'Bu bilgi el kitabında yok.' "
    "Kullandığın her bilginin sonuna parça numarasını [1], [2] biçiminde ekle. Kısa ve net Türkçe yaz."
)


def baglam_metni(baglamlar: list[dict]) -> str:
    return "\n\n".join(
        f"[{i + 1}] ({b['parca'].belge} · {b['parca'].baslik})\n{b['parca'].metin}" for i, b in enumerate(baglamlar)
    )


def cevapla(indeks: Indeks, soru: str, k: int = 4, yontem: str = "hibrit", model: str = LLM_MODEL) -> dict:
    baglamlar = indeks.getir(soru, k, yontem)
    t0 = time.perf_counter()
    yanit = llm_istemci().chat.completions.create(
        model=model, temperature=0.0, max_tokens=400,
        messages=[
            {"role": "system", "content": CEVAP_SISTEM},
            {"role": "user", "content": f"Bağlam:\n{baglam_metni(baglamlar)}\n\nSoru: {soru}"},
        ],
    )
    u = yanit.usage
    return {
        "soru": soru, "cevap": (yanit.choices[0].message.content or "").strip(), "baglamlar": baglamlar,
        "sure_ms": round((time.perf_counter() - t0) * 1000),
        "girdi_token": u.prompt_tokens if u else None, "cikti_token": u.completion_tokens if u else None,
    }


# ----------------------------------------------------------------- hakem için JSON
def json_iste(messages: list[dict], sema: dict, model: str = LLM_MODEL, ad: str = "sonuc") -> dict:
    """Şemalı JSON iste; sağlayıcı json_schema desteklemiyorsa düz metinden JSON'u çek."""
    istemci = llm_istemci()
    try:
        yanit = istemci.chat.completions.create(
            model=model, temperature=0.0, messages=messages,
            response_format={"type": "json_schema", "json_schema": {"name": ad, "schema": sema}},
        )
        return json.loads(yanit.choices[0].message.content or "{}")
    except Exception:  # noqa: BLE001 — bazı arka uçlar response_format'ı reddeder
        yedek = messages + [{"role": "user", "content": f"Yalnızca şu JSON şemasına uyan bir JSON döndür, başka hiçbir şey yazma:\n{json.dumps(sema, ensure_ascii=False)}"}]
        yanit = istemci.chat.completions.create(model=model, temperature=0.0, messages=yedek)
        metin = yanit.choices[0].message.content or ""
        eslesme = re.search(r"\{.*\}", metin, re.S)
        return json.loads(eslesme.group(0)) if eslesme else {}
