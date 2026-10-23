# Hafta 1 · 2026'da yapay zeka: manzara, ekonomi ve araç çantanız

> **Lab:** hesaplar + `hello.py` (bulut modeli vs yerel model)
> **Bu haftanın sorusu:** Modelleri kim üretiyor, kaça satılıyor ve bu dönem boyunca hangi *ücretsiz* araçlarla çalışacaksınız?

Bu ders sinir ağlarının matematiğini değil, bulut altyapısı üzerinde yapay zeka ile ürün geliştirmeyi anlatır. İlk hafta üç şey yapıyoruz: Eylül 2026 itibarıyla model pazarının fotoğrafını çekiyoruz (kapalı ABD laboratuvarları, Çin'in açık ağırlıklı ekosistemi, yılda ~50× düşen fiyatlar), şirketlerin yapay zekayı gerçekte nasıl kullandığına ve pilotların neden battığına bakıyoruz, sonra dönem boyunca kullanacağınız **sıfır maliyetli araç çantasını** birlikte kuruyoruz. Slaytlar ve konuşmacı notları PDF olarak sınıf kanalında.

## Ders akışı (90 dk)

| Süre | Bölüm |
|---|---|
| 0-5 dk | Giriş: siz yaz tatilindeyken neler değişti (22 Eylül 2026 fiyat savaşı) |
| 5-30 dk | Teori 1: 2026 model manzarası, açık vs kapalı, dört fiyat kaldıracı, Fable/Mythos erişim katmanı, para akışı (çip → bulut → laboratuvar → platform → sizin uygulamanız) |
| 30-45 dk | **Canlı demo**: aynı prompt, beş model, beş fiyat |
| 45-50 dk | Ara |
| 50-62 dk | Teori 2: şirketler yapay zekayı nasıl kullanıyor (%88 / %23 / %95), pilotlar neden ölüyor, sigorta hasar triyajı vakası, iş piyasası ve beş beceri |
| 62-80 dk | **Lab**: hesaplar + `hello.py` |
| 80-90 dk | Üç quiz sorusu + gelecek hafta |

## Klasördekiler

| Dosya | Ne işe yarar |
|---|---|
| `hello.py` | Tek fonksiyon, iki sağlayıcı: aynı Türkçe sözleşme maddesini bulut modeline ve yerel Ollama modeline gönderir; token, gecikme ve maliyet yazdırır |
| `requirements.txt` | `openai`, `python-dotenv` |
| `ogrenci_kaynaklari_2026.md` | Doğrulanmış ücretsiz öğrenci kaynakları listesi (Eylül 2026): hangi kapılar kapandı, hangileri açıldı |
| `README.en.md` | Eğitmenin özgün İngilizce lab metni (arşiv) |

Kurulum (repo kökünde bir kez):

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r week1/requirements.txt
cp .env.example .env                                   # Gemini anahtarınızı LLM_API_KEY satırına yazın
python week1/hello.py
```

> **Ortam değişkenleri:** `hello.py` önce ortak `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL` değişkenlerini okur (bu depodaki bütün haftalar aynı üçlüyü kullanır). Derste gösterilen `GEMINI_API_KEY` adı da hâlâ çalışır: yalnızca o varsa Gemini Flash-Lite'a gider. Yerel model için `OLLAMA_BASE_URL` (varsayılan `http://localhost:11434/v1`).

## Canlı demo (hoca · 15 dk)

1. **Aynı Türkçe sözleşme maddesi, beş model (8 dk).** 400 kelimelik bir kira sözleşmesi maddesini Gemini Flash-Lite, DeepSeek V4-Flash, Claude Haiku 4.5, GPT-6 Luna ve yerel Qwen3.5 4B'ye gönderin; her biri için girdi/çıktı token, gecikme ve fatura. Bu depoda aynı tabloyu `week4/foundry_test.py` üretir:
   ```bash
   python week4/foundry_test.py --model gpt-6-luna --model deepseek-v4.1-flash --ollama qwen3.5:4b
   ```
   Sorular: Türkçe neden İngilizceden 1.5-2× fazla token harcıyor? En ucuz model en kötüsü mü? Metinde olmayan bir maddeyi hangisi uydurdu? Yerel model: $0.00 ama neden?
2. **Her hafta açılacak iki konsol (4 dk).** ai.azure.com'da bir modeli 30 saniyede deploy edin (endpoint + anahtar); aistudio.google.com'da 30 saniyede ücretsiz Gemini anahtarı oluşturun. Aynı OpenAI uyumlu istemci ikisiyle de konuşur.
3. **artificialanalysis.ai (3 dk).** Zeka / hız / görev başına maliyet grafiklerini açın, sıralamayı maliyete göre değiştirin. Alışkanlık: modeli basın bülteninden değil bağımsız sıralamadan seçin, bir ay sonra tekrar bakın.

> **Ağ çökerse:** `python araclar/sahte_llm_sunucu.py` + `.env`'de (d) bloğu; tablo sahte yanıtlarla da çıkar. Beş model demosunun ekran görüntüleri Drive'daki `build/demo-w1/` klasöründe.

## Lab (öğrenci · 20 dk)

**Hedef:** Dönem boyunca kullanacağınız her hesap açık; aynı prompt'u hem bulutta hem kendi laptopunuzda çalıştırdınız.

1. **GitHub Student Developer Pack (3 dk).** https://education.github.com/pack → üniversite e-postası ya da öğrenci kimlik fotoğrafı. Onay günler sürebilir; **bugün başvurun**. Kazanım: GitHub Pro, Codespaces 180 çekirdek-saat/ay, JetBrains, DigitalOcean ve Heroku kredisi.
2. **Azure for Students (2 dk).** https://azure.microsoft.com/free/students → $100 kredi, 12 ay, kart gerekmez (Student Pack üzerinden de bağlanır). Hafta 4'te Container Apps için lazım.
3. **Google AI Plus + Gemini anahtarı (3 dk).** https://gemini.google/tr/students → Türkiye'deki üniversite öğrencilerine 1 yıl ücretsiz (18+, SheerID, 31 Aralık 2026'ya kadar). Sonra https://aistudio.google.com → *Get API key*. Ücretsiz katman yalnızca Flash / Flash-Lite; **özel veri göndermeyin**, ücretsiz katman verisi eğitimde kullanılabilir.
4. **Zed Pro (1 dk).** https://zed.dev/education → öğrencilere 1 yıl ücretsiz (üniversite e-postası + 30 günden eski GitHub hesabı). Hafta 6'da kullanacağız.
5. **Ollama (5 dk, kendi laptopunuzda).** https://ollama.com/download → `ollama pull qwen3.5:4b` (8 GB RAM) ya da Türkçe için `ollama pull vngrs-ai/Kumru-2B`; 16 GB RAM'de `qwen3.5:9b` / `gemma4:e4b`. İndirmeyi hemen başlatın, lab'ın en yavaş kısmı budur.
6. **hello.py (5 dk).** Depoyu klonlayın, `.env.example` → `.env`, Gemini anahtarınızı `LLM_API_KEY`'e yazın, `python week1/hello.py`. İki cevap, iki gecikme, bir sıfırdan farklı maliyet görmelisiniz.
7. **Teslim.** `hello.py` çıktısının ekran görüntüsü sınıf kanalına (anahtar görünmesin!).

İsteğe bağlı ücretsiz API'ler (aynı kod, farklı `base_url`): Groq (https://console.groq.com, ~30 istek/dk), OpenRouter `:free` modeller (https://openrouter.ai, günde 50 istek; bir kerelik $10 yükleme ile 1.000/gün). Hazır bloklar `.env.example`'da.

**Başarı kriterleri**
- [ ] `hello.py` iki cevap, iki gecikme değeri ve sıfırdan farklı bir maliyet yazdırıyor
- [ ] Yerel modelin neden $0.00 gösterdiğini (ve asıl maliyetin ne olduğunu: CPU süreniz, elektrik) açıklayabiliyorsunuz
- [ ] GitHub Student Pack ve Azure for Students başvuruları yapıldı; Gemini anahtarı `.env`'de, hiçbir ekran görüntüsünde değil
- [ ] Ekran görüntüsü sınıf kanalına atıldı

## Sık karşılaşılan sorunlar

| Belirti | Çözüm |
|---|---|
| GitHub doğrulaması takılıyor | Üniversite e-postası yoksa öğrenci kimlik kartı fotoğrafı da kabul ediliyor; onay haftalar sürebilir, lab için gerekmez |
| `KeyError: 'GEMINI_API_KEY'` | `.env` repo kökünde mi? `LLM_API_KEY` ya da `GEMINI_API_KEY` satırlarından biri dolu olmalı |
| `429` Gemini | Ücretsiz katman dakika/gün sınırı; birkaç saniye bekleyip tekrar deneyin, `LLM_MODEL=gemini-3.5-flash-lite` kullanın |
| `Connection refused :11434` | `ollama serve` çalışmıyor ya da model inmedi (`ollama list`); `hello.py` bulut yarısını yine gösterir |
| Codespaces'te Ollama yok | Codespaces GPU'suz ve kısıtlı RAM'li: yerel yarıyı kendi laptopunuzda çalıştırın |
| Kampüs Wi-Fi yavaş | Ollama indirmesini derste başlatın, 5. adımı evde tamamlayın |

## Gelecek hafta

**Hafta 2 — LLM'ler gerçekte nasıl çalışır:** token, bağlam penceresi, temperature, dikkat (attention), gömme (embedding). Lab: Türkçe ve İngilizce tokenizasyon karşılaştırması, temperature taraması ve yerel model yarışı. Dersten önce: Ollama'da `qwen3.5:4b` ve `vngrs-ai/Kumru-2B` inmiş olsun.

## Kaynaklar

- Stanford AI Index 2026 ("12 takeaways") · McKinsey State of AI 2026 · MIT "State of AI in Business" · a16z CIO anketi (Şubat 2026)
- Epoch AI, LLM inference price trends (epoch.ai/data-insights/llm-inference-price-trends)
- Anthropic, Fable 5.1 / Mythos 5.1 duyurusu · Dario Amodei, "We Must Pace the Frontier" (12 Eylül 2026) · Semafor, açık ağırlıklı modeller (9 Ağustos 2026)
- artificialanalysis.ai (bağımsız sıralama) · LMArena · SWE-bench
- Derinleşmek için: Karpathy, *Neural Networks: Zero to Hero* · Anthropic Academy, *AI Fluency* · MIT 6.S191 (2026) · BTK Akademi üretken yapay zeka kursları
- Öğrenci kaynakları, doğrulanmış liste: [`ogrenci_kaynaklari_2026.md`](ogrenci_kaynaklari_2026.md)
