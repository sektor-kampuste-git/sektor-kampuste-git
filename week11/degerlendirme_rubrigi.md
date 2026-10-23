# Final projesi değerlendirme rubriği — 100 puan (kesin)

> Bu rubrik [`proje/PROJE_ODEVI.md`](../proje/PROJE_ODEVI.md) §6 ile **birebir aynıdır**; iki dosya ayrışırsa proje belgesi geçerlidir. Proje notu dersin %30'udur.

Önceki dönem rubriği (fonksiyonellik 40 / kod 20 / arayüz 20 / dokümantasyon 10 / teslim 10) bu dönemin beş becerisine göre yeniden ağırlıklandırıldı. Arayüz güzelliği değil, **ölçülebilirlik ve canlıya hazırlık** puan getirir.

| Ölçüt | Puan | Tam puan | Kısmi puan | Sıfır |
|---|---:|---|---|---|
| **İşlevsellik** | **30** | Kullanım senaryosunu önceden belirlenmiş 5 girdide uçtan uca çözüyor; tipli çıktılar; RAG kaynak göstererek / araçlar çağrıları loglayarak çalışıyor; hatalı girdide anlaşılır mesaj; `.env.example` ile 5 dakikada yerelde kurulur | Girdilerin çoğunda çalışıyor; zorunlu bileşenlerden biri zayıf ya da akışın bir kısmı kırık | Demo çalışmıyor veya Türkçe kullanım senaryosu yok |
| **Mühendislik kalitesi** | **20** | Sağlayıcıdan bağımsız istemci, iki sağlayıcıda çalışıyor; arayüz/model katmanı ayrımı; ≥ 8 ağsız test, CI yeşil; gizli bilgiler ortam değişkenlerinde; ajan varsa bütçe ve durma koşulu; spec'le başlayan anlamlı commit geçmişi; ölü kod yok | Testler zayıf veya yapı dağınık; yine de iki sağlayıcıda çalışıyor | Anahtarlar kodun içinde, tek sağlayıcı koda gömülü veya ekibin açıklayamadığı kod |
| **Değerlendirme** | **20** | ≥ 30 vakalık eval seti (en az 5'i zorlayıcı), insan etiketleriyle kalibre edilmiş hakem model, sonuçlar tarihli ve CI'da; red team ≥ 8 saldırı, kırılan saldırı eval'e vaka olarak eklenmiş; izler görünür; "ne bozuldu, nasıl düzelttik" yazılmış | ≥ 15 vaka var, otomatik koşuluyor, sonuçlar mevcut; hakem kalibre edilmemiş ya da red team eksik | Eval seti yok, < 15 vaka ya da yöntemi belirtilmemiş sayılar |
| **Deploy** | **10** | Herkese açık URL, sıfır maliyetli yığın, soğuk başlangıç sorunsuz; istek başına ve 1.000 kullanıcı/ay için maliyet tablosu; kaldıraçlar (önbellek, kademe, `max_tokens`) değerlendirilmiş | URL çalışıyor ama maliyet tablosu yok, ya da uygulama uykuya geçiyor ve bu belirtilmemiş | Herkese açık URL yok |
| **Dokümantasyon** | **10** | README şablonun tüm bölümleriyle; mimari diyagramı; yönetişim bölümü (EU AI Act sınıfı gerekçeli, KVKK, insan onayı noktası); kullanım senaryosu özeti + model kartı; AI kullanımı dürüst ve ayrıntılı | 4-5 bölüm; yönetişim ya da AI kullanımı yüzeysel | README'de temel bölümler eksik ya da AI kullanımı gizlenmiş |
| **Sunum** | **10** | 3 dakika: problem, demo, eval sayıları, maliyet, sınırlar; soruya iyi cevap ([`week10/sunum_rubrigi.md`](../week10/sunum_rubrigi.md)) | Süre aşılmış veya eval / sınırlar atlanmış | Sunum yok |

**Ek kurallar**
- **Geç teslim:** gün başına −10 puan, en fazla 3 gün; sonrası 0.
- **Dürüstlük bonusu (+5):** eval'de düşen vakaları ve çözemediğiniz sorunu açıkça yazanlar; "her şey mükemmel" raporu şüpheyle okunur. Toplam 100'ü geçmez.
- **Yüksek riskli alan** (İK, kredi, sağlık, hukuk) seçenler: "öneri üretir, insan karar verir" tasarımı zorunlu; insan onayı ve yükümlülükler ayrıntılı değilse Dokümantasyon ve İşlevsellik'ten tam puan alamaz.
- **Sır sızıntısı:** repoda anahtar/token → anahtar sızmış sayılır; −10 ve yenileme zorunlu.
- **İntihal veya beyan edilmemiş kopya:** 0. Yapay zeka araçlarını kullanmanız **beklenir**; README'deki AI kullanım beyanı zorunludur.
- **Kişisel veri:** gerçek isim, TCKN, telefon, IBAN repoya girmez; anonimleştirin (Faker ile sentetik) ve KVKK notunu yazın.

## Önceki dönem projesinden ne değişti?
Sahte haber tespit projesi (TF-IDF/BERT + Streamlit) hâlâ geçerli bir fikirdir; ama bu dönem **eval seti, maliyet, güvenlik ve yönetişim** olmadan tam puan almaz. [`proje_fikirleri.md`](proje_fikirleri.md) #4'te güncellenmiş sürümü var.
