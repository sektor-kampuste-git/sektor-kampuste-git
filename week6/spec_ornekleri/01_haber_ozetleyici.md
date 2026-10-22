# SPEC — Türkçe Haber Özetleyici

## 1. Amaç
Bir öğrenci, uzun bir Türkçe haber metnini yapıştırıp **3 cümlelik tarafsız özet**, **5 anahtar kelime** ve **"metinde olmayan iddia" uyarısı** alabilsin.

## 2. Kullanıcı ve bağlam
Gazetecilik/iletişim öğrencileri; tarayıcı (Streamlit); metin yapıştırılır (URL yok).

## 3. Kabul kriterleri
- [ ] K1. 200 karakterden kısa metinde uyarı; model çağrılmaz.
- [ ] K2. Özet en fazla 3 cümle; cümle sayısı arayüzde gösterilir.
- [ ] K3. Anahtar kelimeler 5 adet, virgülle ayrılmış, metinde geçen kelimelerden.
- [ ] K4. "Doğrulama" bölümü: özetteki her cümle için metinde dayanağı olan bir alıntı gösterilir; dayanak bulunamayan cümle kırmızı işaretlenir.
- [ ] K5. Token/maliyet/süre gösterilir.
- [ ] K6. `pytest -q` yeşil, ≥5 test, ağsız.
- [ ] K7. Anahtar `.env` / Secrets'tan okunur.

## 4. Kapsam dışı
URL'den haber çekme, çoklu dil, kullanıcı hesabı, geçmiş saklama.

## 5. Teknik kısıtlar
`app.py` + `llm.py` + `tests/`; tek model çağrısıyla JSON (özet, anahtar_kelimeler, dayanaklar) alınır; `response_format` kullanılır, bozuk JSON'da bir kez yeniden denenir.

## 6. Arayüz taslağı
Metin alanı → "Özetle" → üç sütun: Özet | Anahtar kelimeler | Doğrulama tablosu.

## 7. Değerlendirme
`ornekler/` içinde 5 haber (biri içinde özetin uyduracağı tuzak bilgi barındıran). Uydurma oranı sayılır.

## 8. Yayın
Streamlit Community Cloud.
