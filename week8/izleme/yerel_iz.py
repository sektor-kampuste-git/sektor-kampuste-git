"""
week8 · izleme/yerel_iz.py — Langfuse yoksa da iz (trace) tutmak için 60 satırlık yerel izleyici.

Kavramlar Langfuse/OpenTelemetry ile aynı: trace (bir kullanıcı isteği) → span'ler (model çağrısı, araç, getirme) → her
span'de girdi, çıktı, süre, token, maliyet. Kayıt: izler/*.jsonl (satır başına bir trace).
Kullanım: `with Iz("destek") as iz:` ve `with iz.span("model", girdi=...) as s: ... s.bitir(cikti=..., token=...)`
"""
from __future__ import annotations

import json
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

IZ_KLASORU = Path(__file__).parent / "izler"


class Span:
    def __init__(self, ad: str, girdi=None, ust: str | None = None):
        self.id, self.ad, self.ust, self.girdi = uuid.uuid4().hex[:8], ad, ust, girdi
        self.cikti, self.token, self.maliyet_usd, self.hata = None, None, None, None
        self.baslangic, self.sure_ms = time.perf_counter(), None

    def bitir(self, cikti=None, token: int | None = None, maliyet_usd: float | None = None, hata: str | None = None):
        self.cikti, self.token, self.maliyet_usd, self.hata = cikti, token, maliyet_usd, hata
        self.sure_ms = round((time.perf_counter() - self.baslangic) * 1000)

    def kayit(self) -> dict:
        return {"id": self.id, "ust": self.ust, "ad": self.ad, "girdi": self.girdi, "cikti": self.cikti,
                "token": self.token, "maliyet_usd": self.maliyet_usd, "sure_ms": self.sure_ms, "hata": self.hata}


class Iz:
    def __init__(self, ad: str, kullanici: str | None = None, etiketler: dict | None = None, klasor: Path = IZ_KLASORU):
        self.id, self.ad, self.kullanici, self.etiketler = uuid.uuid4().hex[:12], ad, kullanici, etiketler or {}
        self.spanler: list[Span] = []
        self._yigin: list[str] = []
        self.klasor = klasor
        self.baslangic = time.perf_counter()

    @contextmanager
    def span(self, ad: str, girdi=None):
        s = Span(ad, girdi, self._yigin[-1] if self._yigin else None)
        self.spanler.append(s)
        self._yigin.append(s.id)
        try:
            yield s
        except Exception as hata:  # noqa: BLE001
            s.bitir(hata=repr(hata))
            raise
        finally:
            if s.sure_ms is None:
                s.bitir()
            self._yigin.pop()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.klasor.mkdir(parents=True, exist_ok=True)
        kayit = {"trace_id": self.id, "ad": self.ad, "kullanici": self.kullanici, "etiketler": self.etiketler,
                 "zaman": time.strftime("%Y-%m-%dT%H:%M:%S"), "toplam_ms": round((time.perf_counter() - self.baslangic) * 1000),
                 "toplam_token": sum(s.token or 0 for s in self.spanler),
                 "toplam_usd": round(sum(s.maliyet_usd or 0 for s in self.spanler), 6),
                 "spanler": [s.kayit() for s in self.spanler]}
        with (self.klasor / f"{time.strftime('%Y-%m-%d')}.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
        return False
