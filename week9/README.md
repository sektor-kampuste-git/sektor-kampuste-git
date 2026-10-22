# Hafta 9 · İş yerinde yapay zeka: roller, ROI, yönetişim, hukuk

> **Lab:** kullanım senaryosu özeti + Copilot Studio / n8n prototipi
> **Bu haftanın sorusu:** Teknik olarak çalışan bir sistem şirkette neden yine de ölür ve bunu kim engeller?

Hafta 1'deki tablo: kurumların %88'i yapay zeka kullanıyor, %23'ü ajanları ölçeklemiş, pilotların %95'i kâr-zarara etki etmiyor. 88 ile 23 arasındaki boşluk sizin işleriniz. Bu hafta mühendisliğin "iş" tarafı: hangi rol hangi senaryoyu ister, ROI nasıl hesaplanır (ve nasıl çöker), EU AI Act / KVKK neyi zorunlu kılar, insan onayı nereye konur. Sonra iki kodsuz araçla 15 dakikada prototip. Beş beceriden "yönetişim".

## Ders akışı (90 dk)

| Süre | Bölüm |
|---|---|
| 35 dk | Teori: fonksiyonlara göre benimseme, pilotlar neden ölür, ROI anatomisi, EU AI Act risk sınıfları, KVKK ve yurt dışı aktarım, insan onayı tasarımı, denetim izi, Mythos/Fable erişim katmanı örneği |
| 15 dk | **Canlı demo** |
| 20 dk | **Lab** |
| 10 dk | Quiz + gelecek hafta |

## Klasördekiler

| Dosya | Ne işe yarar |
|---|---|
| `roller.md` | 7 fonksiyon × işe yarayan / batan senaryo × risk sınıfı tablosu |
| `kullanim_senaryosu_sablonu.md` | Tek sayfalık kullanım senaryosu özeti; 6 ölüm nedenine karşı 9 bölüm |
| `roi_hesapla.py` + `senaryolar/` | Aylık getiri/maliyet, geri ödeme, hata oranı duyarlılığı; 3 örnek (biri yüksek riskli) |
| `yonetisim_kontrol_listesi.md` | EU AI Act sınıfları, KVKK maddeleri, denetim izi, insan onayı, olay yönetimi |
| `model_karti_sablonu.md` | Sistemin "prospektüsü" |
| `n8n/` | Docker compose + içe aktarılabilir triyaj akışı + adım adım kurulum |
| `copilot_studio_adimlar.md` | 9 adımda kurumsal bilgi asistanı; n8n/Copilot/kod kıyası |
| `fiyatlar.json` | Hafta 4 fiyat tablosunun kopyası (ROI için) |

## Canlı demo (hoca · 15 dk)

1. **ROI'nin anatomisi (6 dk).**
   ```bash
   cd week9
   python roi_hesapla.py --senaryo senaryolar/hasar_triyaj.json
   python roi_hesapla.py --senaryo senaryolar/hasar_triyaj.json --hata-orani 0.2
   python roi_hesapla.py --senaryo senaryolar/cv_eleme_yanlis_ornek.json
   ```
   Üç mesaj: (1) token maliyeti en küçük kalem; (2) hata oranı ROI'yi belirler → eval seti = para; (3) yüksek riskli alanda model öneri üretir, insan karar verir; tasarruf bu yüzden sınırlı.
2. **Yönetişim 5 dakikada (4 dk).** `yonetisim_kontrol_listesi.md`: hasar triyajı hangi sınıf? (sigorta fiyatlaması yüksek riskli; *triyaj + eksper onayı* ise insan gözetimli). KVKK: PDF'lerde TCKN var → maskeleme + bölge. Mythos/Fable: erişim katmanı artık ürünün parçası.
3. **Prototip (5 dk).** Dersten önce n8n ayağa kalkmış olsun: iki `curl` → biri insana, biri otomatiğe gidiyor. Executions sekmesi = denetim izi. Copilot Studio hesabı varsa Test panelinde el kitabı sorusu + kaynak atıfı.

> **Ağ çökerse:** `roi_hesapla.py` ağ gerektirmez. n8n yerine `n8n/README.md`'deki akış tablosunu tahtada çizin.

## Lab (öğrenci · 20 dk)

**Hedef:** bir rolün gözünden bir senaryo seçip tek sayfalık özet + kodsuz prototip.

1. **Rol ve senaryo (3 dk).** `roller.md`'den bir fonksiyon seç; "sık yapılan, hatası ucuz ya da onayla yakalanabilir, verisi var, sahibi var" kuralına uyan bir senaryo yaz.
2. **ROI (5 dk).** `senaryolar/destek_botu.json`'u kopyala, sayıları senaryona göre değiştir (tahmin et, ama **gerekçele**). Çalıştır; duyarlılık tablosunu özete yapıştır. Soru: hata oranı kaçı geçerse net negatif?
3. **Yönetişim (4 dk).** Risk sınıfı + KVKK maddeleri + insan onayı noktasını özetin §7'sine yaz. Yüksek riskli seçtiysen yükümlülükleri say.
4. **Prototip (8 dk).** **Yol A:** `n8n/` akışını içe aktar, çalıştır, bir iyileştirme ekle. **Yol B:** Copilot Studio'da el kitabı ajanı + "insan onayı" konusu. Ekran görüntüsünü §9'a ekle.
5. **Teslim.** Doldurulmuş `kullanim_senaryosu_sablonu.md` (kendi repona) + prototip ekran görüntüsü. Final projesine bu özetle başlayacaksın.

**Başarı kriterleri**
- [ ] Özet tek sayfa; 9 bölümün hepsi dolu, rakamlar gerekçeli
- [ ] ROI tablosu var ve "hata oranı eşiği" cümlesi yazılmış
- [ ] Risk sınıfı gerekçesiyle belirlenmiş; insan onayı noktası akışta işaretli
- [ ] Prototip çalışıyor (n8n iki curl / Copilot Studio test paneli) ve kaynak/denetim izi görünüyor

## Sık karşılaşılan sorunlar

| Belirti | Çözüm |
|---|---|
| n8n akışı içe aktarılmıyor | Sürüm farkı; `n8n/README.md`'deki 5 node'u elle kurun |
| HTTP Request 401 | `LLM_API_KEY` compose'a geçmemiş; `.env` n8n klasöründe mi? Cloud'da Credential kullanın |
| `$env` boş | `N8N_BLOCK_ENV_ACCESS_IN_NODE=false` compose'da var mı; container'ı yeniden başlatın |
| Copilot Studio "no license" | Okul kiracısı kapatmış; n8n yolunu seçin, kıyas tablosunu özete ekleyin |
| ROI çok iyi çıkıyor | Hata maliyeti ve bakım saatini düşük tuttunuz; `--hata-orani` ile iki katını deneyin |

## Gelecek hafta

**Hafta 10 — Kariyer, portfolyo ve final sunumları:** bu özet, portfolyonuzun "iş etkisi" sayfası olur. 3 dakikalık sunum için hazırlanın.

## Kaynaklar

- Stanford AI Index 2026 · McKinsey State of AI 2026 · MIT "State of AI in Business" (Hafta 1 kaynakları)
- EU AI Act resmî metni ve Komisyon'un uygulama takvimi · KVKK rehberleri (kvkk.gov.tr) · Türkiye Ulusal Yapay Zeka Stratejisi
- Microsoft Learn: *Copilot Studio — Create and publish an agent* · n8n docs: *HTTP Request node*, *Webhook node*
