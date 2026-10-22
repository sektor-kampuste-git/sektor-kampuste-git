# 3 dakikalık sunum şablonu (final projesi ön sunumu)

3 dakika = 6 slayt ya da hiç slayt. Kronometre çalışır; 3:00'da kesilir. Demo video önceden kaydedilmiş olsun (canlı demo şans işidir).

| Dakika | Bölüm | İçerik | Sık hata |
|---|---|---|---|
| 0:00-0:30 | **Problem** | Kim, ne sıklıkla, bugün ne kadar sürüyor/kaça mal oluyor | Teknolojiyle başlamak |
| 0:30-1:00 | **Çözüm + mimari** | Tek cümle + tek şema; model/sağlayıcı seçimi ve neden | 5 kutulu mimari resmi okumak |
| 1:00-1:45 | **Demo** | 45 saniyelik kayıt: girdi → çıktı → ölçümler (token, süre, maliyet) | Canlı demo, uzun yükleme |
| 1:45-2:20 | **Ölçüm** | Eval sonucu (x/15), RAG metrikleri, red team, maliyet/istek; **ne bozuldu ve nasıl düzelttiniz** | Yalnızca iyi sayıları göstermek |
| 2:20-2:45 | **Risk ve yönetişim** | Risk sınıfı, insan onayı noktası, bilinen sınırlar | "Güvenlik önemli" demekle geçmek |
| 2:45-3:00 | **Sonraki adım + istek** | Bir sonraki iterasyon; dinleyiciden ne istiyorsunuz (test kullanıcısı, veri, geri bildirim) | Teşekkür slaytında 20 saniye |

## Hazırlık kontrolü
- [ ] Demo videosu (≤45 sn, ses gerekmez, altyazı/ok işareti var)
- [ ] Sayılar slaytta büyük: 14/15 · 0.93 · $0.0004 · 2.1 sn
- [ ] "Ne bozuldu" cümlesi hazır (bu cümle güvenilirlik kazandırır)
- [ ] Repo bağlantısı QR ya da kısa URL
- [ ] Prova: 2 kez, kronometreyle

## Soru-cevap (2 dk) için hazır cevaplar
- "Neden bu model?" → kademe + maliyet + eval sonucu
- "Model yanılırsa?" → insan onayı noktası + eval'deki hata oranı + hata maliyeti
- "Verim nerede duruyor?" → bölge / sağlayıcı / açık ağırlıklı seçenek
- "Bunu kim kullanacak?" → rol + sahiplik
