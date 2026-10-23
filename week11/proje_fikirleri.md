# 10 proje fikri (hepsi beş beceriyle uyumlu)

Her fikir için: veri · model/mimari · eval fikri · risk notu. Kendi fikriniz de olur; [`week9/kullanim_senaryosu_sablonu.md`](../week9/kullanim_senaryosu_sablonu.md) ile başlayın. Zorunlu bileşenler ve rubrik: [`proje/PROJE_ODEVI.md`](../proje/PROJE_ODEVI.md).

| # | Fikir | Veri | Mimari | Eval | Risk / yönetişim |
|---|---|---|---|---|---|
| 1 | **Çalışan el kitabı asistanı (kurumsal RAG)** | week5 derlemi + kendi okulunuzun yönergeleri (public PDF) | Hibrit RAG + kaynak atıfı + "bilmiyorum" | 20 soru, sadakat/isabet, tuzak sorular | Minimal; kişisel veri yok |
| 2 | **Fiş/fatura → muhasebe kaydı** | Kendi fişleriniz (anonim) | Tipli çıktı (Pydantic), toplam kontrolü, CSV | 30 fiş, alan doğruluğu | Finans verisi; KVKK (gerçek fişte isim var) |
| 3 | **Destek ajanı + MCP** | week7 sahte sipariş verisi genişletilmiş | Araçlar + bütçe + MCP sunucu; insan onayı kuyruğu | 15 eval + 12 saldırı | Para etkisi → insan onayı |
| 4 | **Sahte haber tespiti 2026 sürümü** | Kaggle Fake/Real News + Türkçe haber seti | Klasik sınıflandırıcı (TF-IDF+LR) **ve** LLM hakem; ikisini karşılaştır | accuracy/F1 + LLM sadakat; maliyet/istek karşılaştırması | Yanlış pozitif = sansür riski; şeffaf gerekçe |
| 5 | **Ders notundan quiz + zayıf konu raporu** | Kendi ders notlarınız | Tipli quiz üretimi + doğrulama çağrısı + session state | 10 üretimde şüpheli soru oranı | Minimal |
| 6 | **Sözleşme maddesi risk tarayıcı** | Public örnek sözleşmeler (kira, hizmet) | RAG (mevzuat özetleri) + tipli risk şeması + kaynak | 20 madde, uzman etiketli | Hukuki tavsiye değil uyarısı; insan onayı |
| 7 | **BT ticket triyaj akışı** | Sentetik ticket seti (Faker ile) | n8n/kendi kod: sınıfla → yönlendir → kayıt (denetim izi) | 100 ticket, kategori doğruluğu | Minimal; iz saklama süresi |
| 8 | **Toplantı notu → aksiyon maddeleri + takvim** | Kendi toplantı transkriptleriniz (izinli) | Tipli çıktı + MCP araçları (takvim) | 15 transkript, aksiyon yakalama oranı | Kişisel veri; katılımcı rızası |
| 9 | **Türkçe gömme modeli karşılaştırması** | week5 derlemi + 50 soru | 3 gömme modeli × 2 parçalama; aynı eval | Kaynak isabeti tablosu, maliyet/süre | Minimal; araştırma projesi |
| 10 | **Yapay zeka kullanım politikası danışmanı (yönetişim)** | EU AI Act özeti, KVKK rehberleri (public) | RAG + senaryo → risk sınıfı + kontrol listesi üretimi | 20 senaryo, uzman etiketli sınıf | "Hukuki tavsiye değil"; kaynak zorunlu |

## Seçim kuralları
- **Veri elinizde olsun** (ilk hafta veri bulmaya çalışan proje gecikir). 100-200 örnek eval için yeter.
- **Bir çağrı ile çalışan en küçük sürümü** ilk hafta yayınlayın; RAG/ajan/MCP sonra.
- Yüksek riskli alan (6, 10 kısmen) seçerseniz "öneri üretir, insan karar verir" tasarımı zorunlu.
- Takım 3 kişiyse: biri ürün+eval, biri mimari+maliyet+güvenlik, biri yönetişim+doküman+sunum; hepsi kod yazar.
