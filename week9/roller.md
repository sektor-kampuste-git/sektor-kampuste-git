# Roller: iş yerinde yapay zeka nerede gerçekten ölçeklendi?

McKinsey State of AI 2026: kurumların %23'ü en az bir fonksiyonda ajan tabanlı sistemi ölçeklemiş; hiçbir fonksiyon %10'u geçmiyor. Sıralama (yaklaşık): BT > bilgi yönetimi > yazılım mühendisliği > müşteri hizmetleri > pazarlama-satış > İK > finans. Her satır bir kariyer yolu; her satırın kendi "iyi senaryo" kalıbı var.

| Fonksiyon | Tipik, işe yarayan senaryo | Genellikle batan senaryo | Veri hassasiyeti | EU AI Act (tipik) | Bu dersteki karşılığı |
|---|---|---|---|---|---|
| **BT / operasyon** | Ticket triyajı ve yönlendirme, log özetleme, runbook asistanı | "Sunucuyu kendisi yeniden başlatan ajan" (yetki fazla) | Orta | Minimal/sınırlı | Hafta 7 bütçe + yetki kısıtı, Hafta 8 iz |
| **Bilgi yönetimi** | Politika/prosedür RAG asistanı (bu dersin el kitabı), sözleşme arama | Bayat belgelerle RAG; kaynaksız cevap | Orta-yüksek | Sınırlı | Hafta 5 RAG + değerlendirme |
| **Yazılım mühendisliği** | Kod inceleme asistanı, test üretimi, dokümantasyon, kodlama ajanı | Spec'siz ajan; testleri silen ajan | Düşük-orta (kaynak kod gizli olabilir) | Minimal | Hafta 6 spec + AGENTS.md |
| **Müşteri hizmetleri** | Araç kullanan destek ajanı (sipariş/kargo/iade), yanıt taslağı + insan onayı | Para etkisi olan işlemi ajana bırakmak | Yüksek (kişisel veri) | Sınırlı (şeffaflık: kullanıcı bot olduğunu bilmeli) | Hafta 7 ajan, Hafta 8 red team |
| **Pazarlama / satış** | İçerik taslağı, segment özeti, CRM notu özetleme | Kişiselleştirilmiş manipülatif içerik | Yüksek | Sınırlı; bazı profilleme yüksek riskli | Hafta 3 tipli çıktı, Hafta 9 yönetişim |
| **İK** | Mülakat soru hazırlığı, politika asistanı, iş ilanı taslağı | **Özgeçmiş eleme / işe alım kararı** (yüksek riskli, insan onayı zorunlu) | Çok yüksek | **Yüksek riskli** (Ek III: istihdam) | Hafta 9 KVKK + insan onayı |
| **Finans** | Fatura/fiş bilgi çıkarma, mutabakat özeti, rapor taslağı | **Kredi skorlama / sigorta fiyatlama** otomasyonu | Çok yüksek | **Yüksek riskli** (kredi, sigorta) | Hafta 1 sigorta vakası: eval seti + eksper onayı |

## Senaryo seçme kuralı (Hafta 1'den)
1. **Sık yapılan** bir iş olsun (günde 10 değil 1000 kez). Nadiren yapılan işi otomatikleştirmek yanlış problem.
2. **Hatası ucuz** ya da **insan onayıyla yakalanabilir** olsun. Hata pahalıysa (kredi, sağlık, istihdam) model yalnızca *öneri* üretir.
3. **Verisi var** olsun: en az 100-200 geçmiş örnek → eval seti. Yoksa önce veri topla.
4. **Sahibi** olsun: iş tarafında bir isim, teknik tarafta bir isim.

## Lab için rol seçimi
Beş rolden birini seçin, o rolün bir çalışanı gibi düşünün ve `kullanim_senaryosu_sablonu.md`'yi doldurun. Yüksek riskli bir alan seçtiyseniz (İK, finans kararı) insan onayı noktasını ve EU AI Act yükümlülüklerini ayrıntılı yazmanız beklenir.
