# SPEC — Ders Notundan Quiz Üretici

## 1. Amaç
Öğrenci ders notunu yapıştırsın; uygulama **5 çoktan seçmeli soru** üretsin, öğrenci cevaplasın, **puan ve açıklama** görsün.

## 2. Kullanıcı ve bağlam
Üniversite öğrencileri; Streamlit; sınav öncesi tekrar.

## 3. Kabul kriterleri
- [ ] K1. Sorular JSON şemasıyla gelir: `soru`, `siklar` (4), `dogru` (0-3), `aciklama`; şema bozuksa bir kez yeniden dene.
- [ ] K2. Şıklar karıştırılır; doğru cevap her zaman A olmaz (test edilir).
- [ ] K3. Öğrenci şıkları seçip "Kontrol et" dediğinde puan ve her soru için açıklama görünür.
- [ ] K4. Aynı notla "Yeni sorular" denince farklı sorular gelir (temperature ≥ 0.7).
- [ ] K5. Sorular yalnızca nottaki bilgiden üretilir; notta olmayan bilgi içeren soru "şüpheli" işaretlenir (ikinci bir doğrulama çağrısı).
- [ ] K6. `pytest -q` yeşil; karıştırma, puanlama ve şema testleri ağsız.
- [ ] K7. Anahtar `.env` / Secrets'tan.

## 4. Kapsam dışı
PDF yükleme, kullanıcı hesabı, geçmiş puan takibi, açık uçlu sorular.

## 5. Teknik kısıtlar
`st.session_state` ile sorular ve cevaplar saklanır; `llm.py` içinde `quiz_uret(not_metni, n=5) -> list[Soru]` ve saf `puanla(sorular, cevaplar) -> int`.

## 6. Arayüz taslağı
Not alanı → "Quiz üret" → 5 soru radyo düğmeleriyle → "Kontrol et" → puan + açıklamalar → "Yeni sorular".

## 7. Değerlendirme
`ornekler/` içinde 3 ders notu (biri bu dersin week4 README'si); 10 üretimde şüpheli soru oranı sayılır.

## 8. Yayın
Streamlit Community Cloud.
