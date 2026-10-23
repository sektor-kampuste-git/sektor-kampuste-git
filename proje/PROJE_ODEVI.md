# Final projesi — Bulut Bilişim ve Yapay Zeka Teknolojileri, Güz 2026

> **Ağırlık:** ders notunun **%30**'u (vize %30, final sınavı %40). Hafta 4'te duyurulur; takımlar ve fikirler Hafta 10'daki 3 dakikalık sunumlarla, kapsam Hafta 11 atölyesinde kesinleşir; sunumlar Hafta 14'te; son teslim ders sayfasındaki tarihe kadardır (tarih sınıf kanalında duyurulur).
> Bu belge projenin **tek kaynağıdır**; `week11/degerlendirme_rubrigi.md` buradaki rubriğin kopyasıdır, `week11/proje_teslim_sablonu.md` teslim dosyasının şablonudur.

## 1. Amaç

Bu dersin on haftası tek bir cümleye çıkar: *çalışan, ölçülen, maliyeti bilinen ve yönetilebilir bir yapay zeka ürünü canlıya çıkarabiliyor musunuz?* Proje bunun kanıtıdır. **Türkçe bir kullanım senaryosu** için bir yapay zeka uygulaması geliştirin, deploy edin ve değerlendirin. Teknoloji vitrini değil, işe yarayan ve sınırlarını dürüstçe söyleyen bir ürün bekliyoruz.

Örnekler: kaynak gösteren KAP bildirimi özetleyici; üniversite yönetmelik asistanı; fatura / KYC belgelerinden veri çıkarıcı; ürün kataloğu üzerinde çalışan müşteri destek yönlendirme ajanı; Türk mahkeme kararlarında arama; belge düzeyinde erişim kontrolü olan İK politikaları soru-cevap sistemi. On hazır fikir ve seçim kuralları: [`week11/proje_fikirleri.md`](../week11/proje_fikirleri.md). Önceki dönemin sahte haber tespiti projesi hâlâ geçerli bir fikirdir (#4), ama bu dönemin zorunlu bileşenleri olmadan tam puan almaz.

## 2. Takım kuralı

- **1-3 kişi.** Tek kişi olabilir; kapsam küçülür, rubrik aynıdır. Üç kişilik takımda kapsam büyür.
- **Her üye her dosyayı anlatabilmelidir.** Soru-cevapta rastgele bir üyeye rastgele bir dosya sorulur.
- Katkı commit geçmişinden ve `TESLIM.md` sorumluluk tablosundan okunur; uyumsuzsa bireysel not ayrışır.
- Önerilen iş bölümü (3 kişi): biri ürün + eval, biri mimari + maliyet + güvenlik, biri yönetişim + doküman + sunum; **hepsi kod yazar**.

## 3. Zorunlu bileşenler

Her satır bir haftaya karşılık gelir ve `TESLIM.md`'de kanıt dosyasıyla gösterilir.

| # | Gereksinim | Hafta | Kanıt |
|---|---|---|---|
| 1 | **Tipli ve doğrulanmış çıktılar** (Pydantic / Instructor / `response_format`) | 3 | Şema dosyası + en az 3 doğrulayıcı |
| 2 | **Türkçe bir derlem üzerinde RAG** *veya* **araçlar / bir MCP sunucusu** (ya da ikisi birden) | 5 / 7 | Getirme kodu + kaynak atıfı **veya** MCP sunucusu + araç çağrıları loglanan, adım/USD bütçesi ve durma koşulu olan ajan |
| 3 | **Sıfır maliyetli yığına deploy**, gizli bilgiler ortam değişkenlerinde | 4 / 6 | Gizli tarayıcı penceresinden açılan herkese açık URL (Streamlit Cloud, Render, Vercel, Cloudflare, Azure Container Apps / App Service / Functions, HF Spaces) |
| 4 | **İzlenmiş ve değerlendirilmiş**: en az **15 vakalık eval seti** (gerçek/anonim veriden; en az 5'i zorlayıcı/adversarial), otomatik koşucu, sonuçlar sayı ve tarihle; **red team** (≥8 saldırı); izler (trace) görünür | 8 | `evaller.json` + koşucu çıktısı, Langfuse projesi ya da yerel iz, promptfoo / RAGAS raporu, red team tablosu; CI'da çalışan eval ve yeşil GitHub Actions rozeti (tam puan için) |
| 5 | **Maliyet ölçümü**: istek başına ve aylık tahmin; model kademesi gerekçeli; önbellek / kademe kaldıraçları değerlendirilmiş | 4 | `maliyet_hesapla.py` / `roi_hesapla.py` çıktısı, README maliyet tablosu |
| 6 | **Güvenlik ve yönetişim bölümü**: EU AI Act risk seviyesi (Omnibus sonrası tarihlerle), KVKK kontrolü, injection savunmaları ve yetki kısıtı, insan onayı noktası, yapay zeka kullanım beyanı | 8 / 9 | README bölümü + `docs/kullanim_senaryosu.md` + `docs/model_karti.md` |
| 7 | **Sağlayıcıdan bağımsız kod**: `base_url` + `api_key` + `model` ortam değişkenlerinden; en az iki sağlayıcıda çalışır (hocanın Foundry endpoint'i + Gemini ücretsiz katmanı / Groq / OpenRouter / Ollama) | hepsi | `.env.example`, README |
| 8 | **README "AI kullanımı" bölümü** (ders kuralı): hangi araçlar, hangi işler; ajanın en az bir hatası ve sizin düzeltmeniz | 6 | README |

## 4. Teslim edilecekler

1. **Herkese açık GitHub reposu**; `python week10/portfolyo_kontrol.py <repo>` ≥ 8/10. README [`week10/proje_readme_sablonu.md`](../week10/proje_readme_sablonu.md) yapısında: demo URL, video, kurulum, mimari diyagramı, eval tablosu (N vaka, geçme oranı, hakem, **tarih**), maliyet tablosu, güvenlik/yönetişim, AI kullanımı, sınırlar, lisans.
2. **`TESLIM.md`** repo kökünde ([`week11/proje_teslim_sablonu.md`](../week11/proje_teslim_sablonu.md) doldurulmuş hali). LMS'e aynı dosyanın **PDF çıktısı** (≤ 6 sayfa) yüklenir.
3. **Canlı URL**: gizli tarayıcı penceresinden, giriş yapmadan açılır; uyuyan barındırıcıda (Render) soğuk başlangıç süresi README "Sınırlar" bölümünde yazılı.
4. **Demo videosu (≤ 2 dk)**: problem 15 sn → demo 45 sn → eval + maliyet 20 sn → sınırlar 10 sn (YouTube unlisted / Drive). Ağ yoksa sunum bu videoyla yapılır.
5. **Kullanım senaryosu özeti** `docs/kullanim_senaryosu.md` ([`week9/kullanim_senaryosu_sablonu.md`](../week9/kullanim_senaryosu_sablonu.md), Hafta 9 lab'ında başladığınız belge).
6. **Model kartı** `docs/model_karti.md` ([`week9/model_karti_sablonu.md`](../week9/model_karti_sablonu.md)).
7. **3 dakikalık sunum** Hafta 14'te ([`week10/sunum_sablonu.md`](../week10/sunum_sablonu.md), [`week11/sunum_gunu_akisi.md`](../week11/sunum_gunu_akisi.md)); uzaktan katılan takım 3 dakikalık video gönderir.

## 5. Takvim

| Hafta | Kilometre taşı | Ne teslim edilir / ne olur |
|---|---|---|
| 4 | Proje duyurusu | Bu belge; Hafta 9'a kadar bir kullanım senaryosu ve bir derlem/veri seçin |
| 5 | Vize | 1-4. haftalar; projeyle ilgisi yok ama takvime dikkat |
| 9 | Kullanım senaryosu özeti | Hafta 9 lab'ı: `docs/kullanim_senaryosu.md` ilk sürüm (proje fikri burada doğar) |
| 10 | 3 dakikalık fikir sunumları | Problem → çözüm → ölçüm → risk; hoca her takıma yazılı 2 satır not verir; takımlar kesinleşir |
| 11 | **Kapsam + eval planı onayı** | Atölye: kullanım senaryosu, eval planı (kaç vaka, nereden, ilk 5 vaka yazılmış), en küçük çalışan sürüm yerelde, görev dağılımı, plan B ([`week11/README.md`](../week11/README.md)) |
| 12 | **Ara teslim** (notlandırılmaz, zorunlu) | Yayında URL + ≥10 eval vakası + README iskeleti + `.env.example`; sınıf kanalına link |
| 13 | **Red team eşleşmesi + prova** | Takımlar birbirinin sistemini `week8/guvenlik/kirmizi_takim_kontrol_listesi.md` kurallarıyla test eder, rapor teslim eder; kronometreli sunum provası |
| 14 | **Sunumlar** | 3 dk + 2 dk soru-cevap; `TESLIM.md` son hali; akran değerlendirmesi |
| 15 | Final sınavı | Senaryo soruları ([`week11/final_konu_haritasi.md`](../week11/final_konu_haritasi.md)) |

Kesin tarihler ve son teslim saati sınıf kanalında duyurulur. Sunumdan sonra 48 saat içinde soru-cevapta çıkan düzeltmelerle `TESLIM.md` güncellenebilir (son commit sayılır).

## 6. Notlandırma (%30) ve rubrik — 100 puan

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

## 7. Sıfır maliyetli yığın hatırlatması (Eylül 2026)

Modeller: hocanın Azure AI Foundry endpoint'i + Gemini API ücretsiz katmanı (Flash / Flash-Lite) + Groq + OpenRouter `:free` + yerelde Ollama. Hesaplama: Codespaces (Student Pack, ayda 180 çekirdek-saat), Kaggle / Colab GPU, Modal kredileri. Deploy: Streamlit Community Cloud, Render, Vercel Hobby, Cloudflare, Azure Static Web Apps + Functions, Container Apps her zaman ücretsiz katmanı. Vektör veritabanı: Qdrant bellek içi (Hafta 5) → Supabase pgvector → Azure AI Search Free. Türkçe gömme: `gemini-embedding-001`, `bge-m3`, `ytu-ce-cosmos/turkish-e5-large`. Tam liste: [`week1/ogrenci_kaynaklari_2026.md`](../week1/ogrenci_kaynaklari_2026.md). Ücretli model **gerekmez**: maliyeti ölçmeniz yeter, ödemeniz değil.

## 8. Öğretim elemanının sağlayacakları

- Son teslim tarihi, saati ve LMS bağlantısı (sınıf kanalında).
- Her takım için Azure AI Foundry endpoint'i + anahtarı (dönem sonunda yenilenir; sızarsa hemen yenilenir).
- Ders reposunda örnek Türkçe derlemler: `week5/derlem/` (çalışan el kitabı), `week3/news.json` (haber parçaları), `week7/araclar_yerel.py` (sipariş/kargo verisi), `week9/senaryolar/`.
- Hafta 11 atölyesinde kapsam onayı; Hafta 13'te red team eşleştirmesi.

## 9. Teslimden önce

[`week11/son_kontrol_listesi.md`](../week11/son_kontrol_listesi.md) — 15 dakikalık kontrol. En sık kaybedilen puanlar: eval tablosunda tarih ve N yok; `.env` commit'li; URL yalnızca localhost'ta çalışıyor; "ne bozuldu" bölümü boş.
