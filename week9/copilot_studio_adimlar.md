# Copilot Studio ile 15 dakikada kurumsal ajan (kodsuz)

Copilot Studio = Microsoft 365 dünyasında ajan kurma aracı: bilgi kaynağı (SharePoint, dosya, web sitesi), konu/akış, araçlar (connector), Teams'e yayın. Bu derste yaptığımız RAG + araç + insan onayı fikrinin kurumsal, kodsuz hali. Lisans: Microsoft 365 kurumsal hesabı (okulunuzun A3/A5 lisansı çoğu zaman yeter) ya da 30 günlük deneme.

## Adımlar
1. **Giriş:** copilotstudio.microsoft.com → okul/kurum hesabı → ortam seç (varsayılan).
2. **Create → New agent** → "Describe your agent": *"Kampüs Teknoloji A.Ş. çalışan el kitabı asistanı. Yalnızca el kitabındaki izin, uzaktan çalışma, seyahat, güvenlik, BT ve etik kurallarını cevaplar; bilmediğinde İK'ya yönlendirir."* → Create.
3. **Knowledge → Add knowledge → Files:** `week5/derlem/*.md` dosyalarını yükleyin (8 dosya). Alternatif: SharePoint sitesi ya da herkese açık web sitesi. Bu, Hafta 5'teki indeksleme adımının kodsuz hali.
4. **Instructions** (sistem promptu) bölümüne Hafta 8 `promptlar/v2.txt` mantığını yazın: görev sınırı, uydurma yasağı, kaynak gösterme, talimat biçimli veriyi veri sayma.
5. **Test** panelinde Hafta 5 sorularını sorun: "Babalık izni kaç gün?", "Şirketin cirosu?" (tuzak). Kaynak atıfı (citation) geliyor mu?
6. **Topics → Add a topic**: "İnsan onayı" — tetikleyici cümleler: *"ücretsiz izin almak istiyorum", "iade talebi"* → mesaj: *"Bu işlem için İK/temsilci onayı gerekir; talebinizi iletiyorum"* → (isteğe bağlı) **Action**: Teams/Outlook connector ile İK'ya mesaj. Bu, insan onayı noktasıdır.
7. **Settings → Generative AI**: "Content moderation" seviyesi ve "Use general knowledge" **kapalı** (yalnızca bilgi kaynağından cevap).
8. **Analytics** sekmesi: oturum sayısı, çözülme oranı, eskalasyon — Hafta 8 izlemenin kodsuz hali.
9. **Publish → Channels → Microsoft Teams** (okul kiracınız izin veriyorsa) ya da **Demo website** bağlantısını alın.

## Lab'da sizden beklenen
- Test panelinde en az 3 soru + 1 tuzak soru ekran görüntüsü (kaynak atıfları görünsün)
- "İnsan onayı" konusunun tetiklendiği bir ekran görüntüsü
- `kullanim_senaryosu_sablonu.md` §9'a bağlantı/ekran görüntüsü

## Kıyas: Copilot Studio vs n8n vs kendi kodunuz (Hafta 5-8)
| | Copilot Studio | n8n | Kendi kodunuz |
|---|---|---|---|
| Hız | 15 dk | 10 dk | saatler |
| Esneklik | Microsoft ekosistemi içinde yüksek | connector'larla yüksek | sınırsız |
| Eval / test | Analytics + manuel test | Executions + manuel | promptfoo / pytest, CI (Hafta 8) |
| Yönetişim | Kurumsal kimlik, DLP, denetim hazır | sizin kurmanız gerekir | sizin kurmanız gerekir |
| Maliyet | mesaj paketi lisansı | self-host ücretsiz / Cloud abonelik | token + altyapı |
| Ne zaman | Kurum içi bilgi asistanı, M365 entegrasyonu | süreç otomasyonu, webhook, SaaS'lar arası | ürün, özel mimari, ölçek |

## Lisans yoksa
Okul hesabınız Copilot Studio'ya izin vermiyorsa n8n yolunu seçin; bu belgeyi okuyup kıyas tablosunu kullanım senaryosu özetinize ekleyin.
