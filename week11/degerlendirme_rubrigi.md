# Final projesi değerlendirme rubriği — 100 puan (taslak; hoca onayıyla kesinleşir)

Önceki dönem rubriği (fonksiyonellik 40 / kod 20 / arayüz 20 / dokümantasyon 10 / teslim 10) bu dönemin beş becerisine göre yeniden ağırlıklandırıldı. Arayüz güzelliği değil, **ölçülebilirlik ve canlıya hazırlık** puan getirir.

| # | Ölçüt | Puan | Tam puan için | Yarı puan | Sıfır |
|---|---|---:|---|---|---|
| 1 | **Çalışan ürün ve yayın** | 25 | Canlı URL çalışıyor; temel akış hatasız; hatalı girdide anlaşılır mesaj; `.env.example` ile 5 dakikada yerelde kurulur | Yerelde çalışıyor, yayında değil ya da akışın bir kısmı kırık | Çalışmıyor |
| 2 | **Değerlendirme (eval)** | 20 | ≥15 vakalık eval seti (gerçek/anonim veriden), otomatik koşucu, sonuçlar README'de sayıyla; RAG varsa sadakat/isabet; "ne bozuldu" anlatılmış | Eval var ama <10 vaka ya da elle | Eval yok |
| 3 | **Mimari ve maliyet kararları** | 15 | Model kademesi gerekçeli; sağlayıcıdan bağımsız; istek başına maliyet ölçülmüş; önbellek/kademe kaldıraçları değerlendirilmiş; ajan varsa bütçe ve durma koşulu | Mimari var, maliyet tahmini kaba | Model adı koda gömülü, maliyet bilinmiyor |
| 4 | **Güvenlik ve yönetişim** | 15 | Red team yapılmış (≥8 saldırı), injection savunması katmanlı, yetki kısıtı, risk sınıfı + insan onayı noktası + KVKK notu, model kartı | Prompt'ta birkaç kural, risk sınıfı yazılmış | Yok |
| 5 | **Kod kalitesi ve testler** | 10 | Arayüz/model katmanı ayrımı, ≥8 ağsız test, CI yeşil, anlamlı commit'ler, sır sızıntısı yok | Testler var ama az / CI yok | Test yok ya da `.env` commit'li (−10 ek ceza) |
| 6 | **Dokümantasyon ve AI kullanımı şeffaflığı** | 10 | README şablonun tüm bölümleri; AI kullanımı dürüst ve ayrıntılı; kullanım senaryosu özeti | README var, AI kullanımı yüzeysel | README yok ya da AI kullanımı gizlenmiş |
| 7 | **Sunum** | 5 | `week10/sunum_rubrigi.md` ile 3 dk + soru-cevap | | |

## Ek kurallar
- **Takım katkısı:** commit geçmişi ve `TESLIM.md` sorumluluk tablosu uyumsuzsa bireysel not ayrışır.
- **Dürüstlük bonusu (+5):** eval'de düşen vakaları ve çözemediğiniz sorunu açıkça yazanlar; "her şey mükemmel" raporu şüpheyle okunur.
- **Yüksek riskli alan (İK, kredi, sağlık) seçenler:** 4. ölçütte insan onayı ve yükümlülükler ayrıntılı değilse tam puan alamaz.
- **Sır sızıntısı:** repoda anahtar/token → anahtar sızmış sayılır; −10 ve yenileme zorunlu.

## Önceki dönem projesinden ne değişti?
Sahte haber tespit projesi (TF-IDF/BERT + Streamlit) hâlâ geçerli bir fikirdir; ama bu dönem **eval seti, maliyet, güvenlik ve yönetişim** olmadan tam puan almaz. `proje_fikirleri.md`'de güncellenmiş sürümü var.
