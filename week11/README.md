# Hafta 11 · Proje ve final hazırlığı

> **Bu hafta demo yok; bu hafta sizin projeniz var.**
> Ders saati atölye olarak işler: takımlar çalışır, hoca masa masa dolaşır, eval planları onaylanır.

Proje ödevinin tamamı tek belgede: [`proje/PROJE_ODEVI.md`](../proje/PROJE_ODEVI.md) (amaç, zorunlu bileşenler, teslim edilecekler, takvim, rubrik). Hafta 10'daki sunumlarla takımlar ve fikirler kesinleşti. Bu hafta üç şey netleşir: **ne teslim edeceksiniz** (şablon), **nasıl puanlanacak** (rubrik), **finalde ne sorulur** (konu haritası). Ürünün en küçük çalışan sürümü bu hafta sonunda yayında olmalı; RAG/ajan/MCP katmanları sonraki haftalarda eklenir.

## Ders akışı (90 dk)

| Süre | Bölüm |
|---|---|
| 15 dk | Teslim şablonu + rubrik üzerinden geçiş; sorular |
| 10 dk | Final konu haritası: hangi haftadan ne tür senaryo gelir |
| 55 dk | **Atölye**: takımlar `kullanim_senaryosu.md` + eval planı + en küçük çalışan sürüm; hoca onayı |
| 10 dk | Takvim: ara teslim + red team + prova (Hafta 12), sunum (Hafta 13), final sınavı (Hafta 14 tatil) |

## Klasördekiler

| Dosya | Ne işe yarar |
|---|---|
| `proje_teslim_sablonu.md` | `TESLIM.md` olarak repo köküne; takım, kanıt tablosu, eval sonuçları, maliyet, yönetişim, AI kullanımı |
| `degerlendirme_rubrigi.md` | 100 puanlık rubrik (kesin; [`proje/PROJE_ODEVI.md`](../proje/PROJE_ODEVI.md) §6 ile aynı) |
| `son_kontrol_listesi.md` | Teslimden 1 gün önce 15 dakikalık kontrol |
| `final_konu_haritasi.md` | Hafta 1-10 kavram/karar haritası + 10 örnek senaryo sorusu |
| `proje_fikirleri.md` | 10 fikir: veri · mimari · eval · risk; seçim kuralları |
| `sunum_gunu_akisi.md` | Hafta 13 akışı, akran değerlendirme |

## Atölye kontrol noktaları (hoca masaya geldiğinde hazır olsun)

1. **Kullanım senaryosu özeti** (Hafta 9 şablonu) — problem, kullanıcı, veri, risk sınıfı, insan onayı
2. **Eval planı** — kaç vaka, nereden, ilk 5 vaka yazılmış; metrik ve kabul eşiği
3. **En küçük çalışan sürüm** — tek model çağrısıyla uçtan uca akış, yerelde çalışıyor (yayın bu hafta sonu)
4. **Görev dağılımı** — kim ne yapıyor, commit'lerde görünecek
5. **Riskler** — veri yoksa, model Türkçe'de zayıfsa, zaman kalmazsa plan B

## Takvim (`PROJE_ODEVI.md` §5 ile aynı; sınıf kanalındaki tarih geçerlidir)

| Hafta | Kilometre taşı |
|---|---|
| 11 | Kapsam + eval planı onayı; en küçük sürüm yerelde |
| 12 | Ara teslim: yayında URL + ≥10 eval vakası + README iskeleti |
| 13 | Red team eşleşmesi (takımlar birbirini test eder) + sunum provası |
| 14 | Sunumlar (`sunum_gunu_akisi.md`) + `TESLIM.md` |
| 15 | Final sınavı (senaryo soruları; `final_konu_haritasi.md`) |

## Sık sorulan sorular

| Soru | Cevap |
|---|---|
| Önceki dönemin sahte haber projesini yapabilir miyiz? | Evet; `proje_fikirleri.md` #4. Eval, maliyet, güvenlik, yönetişim olmadan tam puan yok |
| Ücretli model gerekir mi? | Hayır. Gemini ücretsiz katman + hocanın OpenRouter anahtarı + Ollama yeter; maliyeti **ölçmeniz** yeter, ödemeniz değil |
| Tek kişi olabilir miyim? | Evet; kapsam küçülür, rubrik aynı |
| Kodun ne kadarını ajan yazabilir? | Hepsini bile; ama README "AI kullanımı" dürüst olmalı ve siz her satırı açıklayabilmelisiniz (soru-cevapta sorulur) |
| Verimiz kişisel veri içeriyor | Anonimleştirin (Faker ile sentetik), KVKK notunu yazın; gerçek TCKN/isim repoya girmez |

## Kaynaklar
[`proje/PROJE_ODEVI.md`](../proje/PROJE_ODEVI.md) · önceki haftaların README'leri (her birinin "Başarı kriterleri" bölümü) · [`week10/proje_readme_sablonu.md`](../week10/proje_readme_sablonu.md) · [`week9/kullanim_senaryosu_sablonu.md`](../week9/kullanim_senaryosu_sablonu.md) · [`week8/ci/eval.yml`](../week8/ci/eval.yml)
