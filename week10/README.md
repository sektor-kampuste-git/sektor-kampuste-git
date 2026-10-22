# Hafta 10 · Kariyer, portfolyo ve final sunumları

> **Lab:** portfolyo rötuşu + 3 dakikalık sunumlar
> **Bu haftanın sorusu:** Dokuz haftada yaptıklarınızı bir işe alımcı 90 saniyede görebilir mi?

Hafta 1'deki iki zıt sinyal: genel junior ilanları daralıyor, yapay zeka rolleri patlıyor. Piyasa "Python biliyor"a değil, **belirli ve kanıtlanabilir** becerilere ödüyor: ajan mühendisliği, değerlendirme, MCP entegrasyonu, yapay zeka güvenliği, yönetişim. Bu hafta o kanıtı toparlıyoruz: repo düzeni, README, CV maddeleri, profil; sonra herkes 3 dakikada final projesi fikrini sunuyor.

## Ders akışı (90 dk)

| Süre | Bölüm |
|---|---|
| 20 dk | Teori: iş piyasası 2026, beş beceri → kanıt, portfolyo anatomisi, mülakat formatları (take-home, sistem tasarımı), İK perspektifi |
| 10 dk | **Canlı demo**: bir repoyu işe alımcı gözüyle 10 maddede kontrol |
| 20 dk | **Lab 1**: portfolyo rötuşu |
| 35 dk | **Lab 2**: 3 dakikalık sunumlar (kronometreli) + akran geri bildirimi |
| 5 dk | Kapanış: Hafta 11 ve proje takvimi |

## Klasördekiler

| Dosya | Ne işe yarar |
|---|---|
| `portfolyo_rehberi.md` | Beş beceri × hafta × repoda kanıt × CV maddesi; portfolyo repo düzeni |
| `portfolyo_kontrol.py` | GitHub reposunu 10 maddede puanlar (README bölümleri, `.env` sızıntısı, testler, LICENSE, topics…) |
| `cv_maddeleri.md` | Zayıf → güçlü maddeler (TR + EN); yapılmayacaklar |
| `proje_readme_sablonu.md` | Final projesi README iskeleti (eval, maliyet, güvenlik, AI kullanımı bölümleriyle) |
| `sunum_sablonu.md` | 3 dk sunum yapısı, dakika dakika; soru-cevap hazır cevapları |
| `sunum_rubrigi.md` | 20 puanlık sunum rubriği (finalde de kullanılır) |
| `mulakat_sorulari.md` | 25 soru, her biri haftaya bağlı; mülakat formatları |
| `profil_kontrol_listesi.md` | GitHub + LinkedIn 10 dakikalık düzen |

## Canlı demo (hoca · 10 dk)

```bash
python week10/portfolyo_kontrol.py https://github.com/<bir öğrenci reposu>      # izinle
python week10/portfolyo_kontrol.py https://github.com/<hocanın örnek reposu>
```
Çıktıyı birlikte okuyun: hangi madde neden işe alımcıyı ilgilendirir? `.env` sızıntısı uyarısını gösterin (varsa anahtar yenilenir). Sonra `cv_maddeleri.md`'den bir zayıf maddeyi sınıfla güçlüye çevirin.

## Lab 1 · Portfolyo rötuşu (20 dk)

1. **Ölç (3 dk).** `python week10/portfolyo_kontrol.py <kendi repon>` — puanı not al.
2. **Kapat (12 dk).** Eksik maddeleri sırayla: README bölümleri (`proje_readme_sablonu.md`), `.env.example`, LICENSE, açıklama + 3 topic, testler. Tekrar ölç; hedef ≥ 8/10.
3. **Beş madde (5 dk).** `portfolyo_rehberi.md` tablosundan beş CV maddesini kendi sayılarınla yaz (TR + EN), README'nin üstüne koy.
4. **Teslim.** Önce/sonra puan ekran görüntüsü + 5 madde.

## Lab 2 · 3 dakikalık sunumlar (35 dk)

Final projesi **fikri** için (ürün bitmiş olmak zorunda değil): problem, çözüm, ne ölçeceksiniz, risk. `sunum_sablonu.md` yapısı, kronometre 3:00. Her sunumdan sonra 1 dk akran geri bildirimi (`sunum_rubrigi.md` ölçütleriyle, bir güçlü yön + bir öneri). Hoca her takıma yazılı 2 satır not verir; proje kapsamı bu notlarla kesinleşir.

**Başarı kriterleri**
- [ ] Portfolyo reposu public ve ≥ 8/10
- [ ] Beş beceri için beş kanıt bağlantısı ve beş sayılı CV maddesi
- [ ] 3 dakikada problem → çözüm → ölçüm → risk anlatıldı, süre aşılmadı
- [ ] Akran geri bildirimi verildi ve alındı

## Hafta 1 ↔ Hafta 10 köprüsü
Hafta 1'de "Aralık'a kadar her beceriyi bir GitHub linkiyle CV'nize yazabilmelisiniz" demiştik. Bugün o linkler yazıldı. Hoca referansı için portfolyo bağlantınızı e-posta ile gönderin.

## Gelecek hafta

**Hafta 11 — Proje ve final hazırlığı:** teslim şablonu, rubrik, son kontrol listesi, final konu haritası. Proje takımları ve fikirleri bu haftaki sunumlarla kesinleşti; gelecek hafta kapsam ve eval planı netleşir.
