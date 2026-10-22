# Yönetişim kontrol listesi: EU AI Act · KVKK · denetim izi · insan onayı

> Hukuki tavsiye değildir; mühendisin "neyi sormam gerektiğini bileyim" listesidir. Kesin yükümlülükler için hukuk/uyum ekibi.

## 1. EU AI Act — risk sınıfını belirle
AB Yapay Zeka Yasası (2024'te yürürlüğe girdi, yükümlülükler 2025-2027 arasında kademeli devreye giriyor). Türkiye'de kurulu bir şirket bile AB'de kullanıcıya/etkiye sahipse kapsamda olabilir; Türkiye'nin kendi düzenleme çalışmaları AB modeline yakın ilerliyor.

| Sınıf | Örnek | Sizin yükümlülüğünüz |
|---|---|---|
| **Yasak** | Duygu tanıma (iş yeri/okul), sosyal skorlama, manipülatif teknikler | Yapmayın |
| **Yüksek riskli** (Ek III) | İstihdam (CV eleme, terfi), kredi/sigorta skorlama, eğitimde değerlendirme, kritik altyapı, kolluk | Risk yönetimi, veri yönetişimi, teknik dokümantasyon, kayıt (log), **insan gözetimi**, doğruluk/sağlamlık, uygunluk değerlendirmesi |
| **Sınırlı** (şeffaflık) | Sohbet botları, üretilen içerik, deepfake | Kullanıcı bir yapay zekayla konuştuğunu bilmeli; üretilen içerik işaretlenmeli |
| **Minimal** | Spam filtresi, kod tamamlama, özetleme asistanı | Gönüllü davranış kodları |
| **Genel amaçlı model (GPAI)** | Model sağlayıcıları (siz değil, Anthropic/OpenAI/…) | Sağlayıcının dokümantasyonunu *sizin* dosyanıza ekleyin |

**Kontrol:** [ ] Sınıf belirlendi ve gerekçesi yazıldı · [ ] Yüksek riskliyse insan gözetimi tasarımda var · [ ] Sohbet botu ise "yapay zeka asistanı" açıklaması arayüzde

## 2. KVKK (6698) — kişisel veri varsa
- [ ] **İşleme amacı** ve **hukuki dayanak** yazıldı (açık rıza / sözleşme / meşru menfaat / kanuni yükümlülük)
- [ ] **Veri minimizasyonu:** prompta yalnızca gereken alanlar gidiyor; TCKN, telefon gibi alanlar maskeleniyor
- [ ] **Aydınlatma metni** güncellendi (yapay zeka ile işleme belirtildi)
- [ ] **Yurt dışı aktarım:** model sağlayıcısı yurt dışındaysa aktarım şartları (açık rıza, yeterlilik, taahhütname/BCR) kontrol edildi; Azure'da bölge seçimi (örn. Sweden Central / West Europe) belgelendi; mümkünse veri kurum içinde kalsın (açık ağırlıklı model seçeneği)
- [ ] **Saklama süresi:** iz (trace) kayıtlarında kişisel veri ne kadar tutuluyor, ne zaman siliniyor/anonimleştiriliyor
- [ ] **İlgili kişi hakları:** kararın gerekçesini açıklayabiliyor musunuz? (otomatik karara itiraz)
- [ ] **VERBİS** kaydı güncel mi (kurumun yükümlülüğü)
- [ ] **Özel nitelikli veri** (sağlık, biyometri, din, sendika…) varsa ekstra önlem ve dayanak

## 3. Denetim izi (audit trail) — Hafta 8 tracing'in kurumsal hali
Her çağrı için saklanacak asgari alanlar: zaman · kullanıcı/sistem kimliği · girdi (maskelenmiş) · çıktı · model adı+sürümü · prompt sürümü · getirilen kaynaklar (RAG) · araç çağrıları · maliyet · insan onayı (kim, ne zaman, karar). Saklama: KVKK süresiyle uyumlu, değiştirilemez (append-only), erişimi kısıtlı.

## 4. İnsan onayı (human-in-the-loop) tasarımı
- Hangi kararlar **asla** otomatik uygulanmaz? (para hareketi, istihdam, sağlık, hukuki sonuç)
- Onaylayan kişi neyi görüyor: modelin önerisi + gerekçe + kaynak + güven göstergesi
- "Lastik damga" riski: onaylayan her şeyi onaylıyorsa onay yoktur → örnekleme denetimi, zorunlu ret payı değil ama kalite kontrol

## 5. Olay yönetimi
- Yanlış/zararlı çıktı, veri sızıntısı, prompt injection tespit edildiğinde: kim bilgilendirilir, sistem nasıl durdurulur (kill switch), kullanıcılara ne söylenir, eval setine nasıl eklenir
- Model sağlayıcısı modeli kaldırırsa (Hafta 1: o3/o4-mini emekliliği) geçiş planı

## 6. Belgeler
- [ ] Kullanım senaryosu özeti (bu haftaki şablon) · [ ] Model kartı (`model_karti_sablonu.md`) · [ ] Eval raporu (Hafta 8) · [ ] KVKK etki değerlendirmesi (gerekirse) · [ ] Sahiplik ve bakım planı
