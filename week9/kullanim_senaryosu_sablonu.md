# Kullanım senaryosu özeti — <Senaryo adı>

> Tek sayfa. Bir yöneticinin 5 dakikada "evet / hayır / daha fazla bilgi" diyebilmesi için.
> Hafta 1'in dersi: pilotların %95'i şu altı nedenle ölür: eval yok, yanlış veri, sınırsız maliyet, güvenlik, sahibi yok, yanlış problem. Her bölüm bu altıdan birine cevap verir.

## 1. Problem (yanlış problem değil mi?)
- **Kim** bu işi **ne sıklıkla** yapıyor? (rol, kişi sayısı, günlük/haftalık adet)
- Bugün ne kadar sürüyor, ne kadar maliyeti var? (dakika × adet × saatlik maliyet)
- Neden şimdi? Hangi acı en büyük: süre, hata, tutarsızlık, ölçeklenemezlik?

## 2. Çözüm (bir cümle + akış)
- "Kullanıcı … yapar → sistem … üretir → insan … onaylar."
- Model nerede devreye giriyor, nerede girmiyor? (kural tabanlı yeten yere model koyma)
- Çıktı tipli mi (JSON şema)? Hangi alanlar?

## 3. Veri (yanlış veri değil mi?)
- Kaynak: hangi sistemler, ne kadar güncel, kim sahibi?
- Kişisel veri var mı? → KVKK bölümü (madde 7)
- Veri nerede duracak: kurum içi / bölge / sağlayıcı? Açık ağırlıklı mı kapalı model mi? (Hafta 1 ekseni)

## 4. Model ve mimari
- Model kademesi: kolay işler → ucuz; zor → amiral (Hafta 4 kaldıraçları). Önbellek oranı tahmini.
- Bileşenler: RAG (Hafta 5) · araçlar/MCP (Hafta 7) · bütçe ve durma koşulu
- Sağlayıcıdan bağımsız mı? Model bir günde değişebilir mi?

## 5. Maliyet ve getiri (sınırsız maliyet değil mi?)
`python roi_hesapla.py --senaryo senaryolar/benim.json` çıktısını yapıştır:
- Aylık token maliyeti · platform/altyapı · insan kontrol süresi · bakım
- Aylık tasarruf · net · geri ödeme süresi (ay)
- Duyarlılık: hata oranı iki katına çıkarsa ne olur?

## 6. Değerlendirme (eval yok değil mi?)
- Eval seti: kaç örnek, nereden (geçmiş kayıtlar), kim etiketledi?
- Metrikler: doğruluk / sadakat / güvenlik vakaları; **kabul eşiği** (örn. ≥ %90 ve 0 güvenlik hatası)
- Canlıda izleme: hangi iz (trace) alanları, hangi uyarılar (Hafta 8)

## 7. Risk, yönetişim ve hukuk (güvenlik yok değil mi?)
- EU AI Act risk sınıfı: yasak / yüksek / sınırlı (şeffaflık) / minimal — gerekçe
- KVKK: işleme amacı, hukuki dayanak, veri minimizasyonu, saklama süresi, yurt dışı aktarım, aydınlatma
- İnsan onayı noktası: hangi karar insan onayı olmadan uygulanmaz?
- Prompt injection / veri sızıntısı önlemleri (Hafta 8 `savunma.md` katmanları)
- Denetim izi: kim, ne zaman, hangi girdiyle, hangi sürüm (prompt/model) → nereye kaydediliyor?
- Model kartı var mı? (`model_karti_sablonu.md`)

## 8. Sahiplik ve yol haritası (sahibi yok değil mi?)
- Ürün sahibi (iş tarafı) · teknik sahip · bakım bütçesi (saat/ay)
- 3 haftalık pilot planı: hafta 1 eval seti, hafta 2 prototip, hafta 3 gölge modda (shadow) ölçüm
- Pilot başarı kriteri ve **durdurma kriteri** ("şu olursa kapatırız")

## 9. Prototip
- Copilot Studio ajanı / n8n akışı bağlantısı ve ekran görüntüsü (bu haftaki lab)
