# SPEC — Fiş / Fatura Bilgi Çıkarıcı

## 1. Amaç
Kullanıcı bir fiş ya da faturanın **metnini** (OCR çıktısı ya da elle yazılmış) yapıştırsın; uygulama **tipli bir şema** (satıcı, tarih, toplam, KDV, kalemler) üretsin ve CSV olarak indirilebilsin.

## 2. Kullanıcı ve bağlam
Küçük işletme sahibi / muhasebe stajyeri; Streamlit; metin yapıştırma (görsel yükleme kapsam dışı — isteğe bağlı bonus).

## 3. Kabul kriterleri
- [ ] K1. Çıktı Pydantic modeliyle doğrulanır: `satici: str`, `tarih: date`, `toplam: Decimal`, `kdv: Decimal | None`, `kalemler: list[Kalem]`.
- [ ] K2. Toplam ≠ kalemler toplamı ise arayüzde sarı uyarı (hesap tutmuyor).
- [ ] K3. Tarih biçimi `GG.AA.YYYY` olarak gösterilir; model farklı biçim verirse normalize edilir.
- [ ] K4. "CSV indir" düğmesi kalemleri indirir.
- [ ] K5. Şemaya uymayan model çıktısında bir kez yeniden deneme, sonra anlaşılır hata.
- [ ] K6. `pytest -q` yeşil; şema doğrulama ve toplam kontrolü testleri ağsız.
- [ ] K7. Anahtar `.env` / Secrets'tan.

## 4. Kapsam dışı
Görsel OCR (bonus), çoklu para birimi, muhasebe entegrasyonu.

## 5. Teknik kısıtlar
Hafta 3'teki yapılandırılmış çıktı yaklaşımı (Pydantic + `response_format`); `llm.py` içinde `fis_cikar(metin) -> Fis`.

## 6. Arayüz taslağı
Metin alanı → "Çıkar" → sol: alanlar (satıcı, tarih, toplam, KDV) · sağ: kalemler tablosu · altta CSV indir.

## 7. Değerlendirme
`ornekler/` içinde 5 fiş metni; 2'sinde toplam kalemlerle tutmaz, 1'inde tarih farklı biçimde.

## 8. Yayın
Streamlit Community Cloud.
