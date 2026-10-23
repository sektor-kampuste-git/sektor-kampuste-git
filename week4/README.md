# Hafta 4 · Yapay zeka için bulut: IaaS'tan "hizmet olarak model"e

> **Lab:** API'den model kiralamak (OpenRouter) · maliyet tablosu · Azure'a deploy
> **Bu haftanın sorusu:** Bir modeli *nereden* kiralarsınız, size *kaça* gelir ve ürününüzü *nerede* çalıştırırsınız?

İlk üç hafta modelin nasıl çalıştığını ve onunla nasıl konuşulduğunu gördük. Bu hafta modeli çalıştırdığınız **bulut katmanını** anlıyoruz: sanal makineden "hizmet olarak model"e (MaaS) uzanan merdiven, token ekonomisi ve bir Türkçe özetleyiciyi gerçek bir URL'de yayınlamak.

## Ders akışı (90 dk)

| Süre | Bölüm |
|---|---|
| 35 dk | Teori: bulut katmanları, Foundry/Bedrock/Vertex ve OpenRouter gibi model yönlendiricileri, token ekonomisi, dört fiyat kaldıracı |
| 15 dk | **Canlı demo** (aşağıda) |
| 20 dk | **Lab** (aşağıda) |
| 10 dk | Quiz + gelecek hafta (RAG, vize) |

## Kavram: bulut merdiveni

| Katman | Siz neyi yönetirsiniz? | Azure örneği | Ne zaman |
|---|---|---|---|
| **IaaS** | İşletim sistemi, yamalar, ölçekleme, GPU sürücüsü | Virtual Machines (GPU'lu NC/ND serisi) | Açık ağırlıklı model kendi GPU'nuzda çalışacak, veri dışarı çıkmayacak |
| **CaaS / PaaS** | Yalnızca kodunuz ve konteyneriniz | Container Apps, App Service | Uygulamanız (API, Streamlit) bulutta çalışacak; sunucu yönetmek istemiyorsunuz |
| **FaaS** | Tek fonksiyon, olay tetikler | Azure Functions | Dosya gelince / saatte bir çalışan küçük işler |
| **MaaS** (hizmet olarak model) | Hiçbir altyapı; token başına ödersiniz | **Azure AI Foundry**, AWS Bedrock, Google Vertex, OpenAI/Anthropic API; **OpenRouter** (birçok sağlayıcının önünde tek API) | Öncü modele ihtiyaç var, altyapı istemiyorsunuz |

> **Bu derste model erişimi:** hoca her öğrenciye harcama limitli bir **OpenRouter** anahtarı verir. OpenRouter bir *yönlendirici*dir: tek endpoint ve tek anahtarla OpenAI, Anthropic, DeepSeek, Qwen modellerine gider, faturayı tek yerde keser. Foundry ise aynı işi kendi Azure aboneliğinizin içinde yapar (veri yerleşimi, kurumsal sözleşme, Azure güvenlik/ağ kontrolleri). Kod ikisinde de aynıdır; değişen yalnızca `.env`'deki üç satırdır.

Hafta 1'deki para akışı: *Çipler → Bulut → Model laboratuvarları → Platformlar (Foundry) → Sizin uygulamanız.* Bu hafta **platform** ve **uygulama** kutularını kiralıyoruz.

## Klasördekiler

| Dosya | Ne işe yarar |
|---|---|
| `foundry_test.py` | Aynı Türkçe prompt'u birden çok model/arka uca gönderir (OpenRouter, Foundry, Gemini, Ollama); token, gecikme, maliyet tablosu |
| `maliyet_hesapla.py` | Bir iş yükü senaryosu için aylık fatura; önbellek, kademe ve hızlı mod kaldıraçlarının etkisi |
| `fiyatlar.json` | Tarihli liste fiyatları (1M token başına USD). **Dersten önce güncelleyin.** |
| `senaryolar/*.json` | Dört gerçekçi iş yükü: destek botu, sözleşme özeti, kodlama ajanı, hasar triyajı |
| `ozetleyici/` | FastAPI özetleyici: `app.py`, `Dockerfile`, `deploy_aca.sh` (Azure Container Apps) |

Kurulum (repo kökünde bir kez):

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r week4/requirements.txt
cp .env.example .env                                   # sonra .env içine anahtarınızı yazın
```

## Canlı demo (hoca · 15 dk)

1. **Merdiveni portalda göster (3 dk).** Azure Portal'da bir VM fiyatı (GPU'lu), bir Container Apps ortamı ve Foundry'yi yan yana aç. Soru: "Qwen'i kendimiz mi çalıştıralım, Foundry'den mi kiralayalım?" Veri nerede durmalı, kim yamalar, kaça gelir.
2. **Tek API, birçok model (3 dk).** openrouter.ai → Models sayfasında bir modelin sağlayıcılarını ve fiyatını göster; sonra Activity sayfasında öğrenci anahtarlarının harcamasını (kimse limitini aşamaz). İsteğe bağlı: ai.azure.com'da Foundry *Model catalog → Deploy* akışını göster ("aynı şeyi kendi aboneliğimizde yapsaydık"). Aynı istemci koduyla konuşuyoruz:
   ```bash
   python week4/foundry_test.py --model openai/gpt-6-luna --model deepseek/deepseek-v4.1-flash --ollama qwen3.5:4b
   ```
   Tabloyu oku: en ucuz model en kötüsü değil; yerel model $0 ama yavaş. Metinde olmayan bir madde uyduran var mı?
3. **Faturayı hesapla (5 dk).**
   ```bash
   python week4/maliyet_hesapla.py --senaryo week4/senaryolar/destek_botu.json
   python week4/maliyet_hesapla.py --senaryo week4/senaryolar/kod_ajani.json --ucuz-model deepseek-v4.1-flash
   ```
   Önce `--onbellek 0 --kolay 0` ile kaldıraçları kapatıp farkı göster. Kodlama ajanı senaryosunda önbellek neden her şeyi değiştiriyor? (Aynı 40K token her adımda yeniden gidiyor.)
4. **Ürünü yayınla (4 dk).** Dersten önce `ozetleyici/deploy_aca.sh` bir kez çalıştırılmış olsun (ilk dağıtım 3-5 dk sürer). Derste URL'i aç, bir metin özetle, `/saglik`'i göster; sonra `az containerapp logs show --follow` ile isteğin logunu göster. "Sıfıra ölçeklenir: kimse kullanmıyorsa ödemiyoruz."

> **Ağ çökerse:** `python araclar/sahte_llm_sunucu.py` çalıştırın ve `.env`'de `LLM_BASE_URL=http://localhost:8080/v1` yapın. Tüm demolar aynı kodla çalışır (yanıtlar sahte ama akış gerçek).

## Lab (öğrenci · 20 dk)

**Hedef:** API'den bir model kiralamak, faturasını hesaplamak ve özetleyiciyi bir URL'de yayınlamak.

1. **Endpoint'i bağla (4 dk).** Hocanın LMS'ten sana özel gönderdiği OpenRouter anahtarını `.env`'e yaz: `.env.example`'daki (b) bloğu (`LLM_BASE_URL=https://openrouter.ai/api/v1`, `LLM_MODEL=openai/gpt-6-luna`). Doğrula:
   ```bash
   python week4/foundry_test.py
   ```
   Anahtarın henüz yoksa Gemini anahtarınla (Hafta 1) aynı komutu çalıştır; `.env.example`'daki (a) bloğu.
2. **Üç model karşılaştır (4 dk).** OpenRouter'da en az iki model + yerel modelin:
   ```bash
   python week4/foundry_test.py --model openai/gpt-6-luna --model deepseek/deepseek-v4.1-flash --ollama qwen3.5:4b
   ```
   Tabloyu kaydet. Hangisi en ucuz, hangisi en hızlı, hangisi uydurdu?
3. **Kendi senaryonun faturası (5 dk).** `senaryolar/destek_botu.json` dosyasını kopyala, sayıları **kendi proje fikrine** göre değiştir (günlük istek, token uzunlukları, önbellek oranı). Çalıştır:
   ```bash
   python week4/maliyet_hesapla.py --senaryo week4/senaryolar/benim.json
   ```
   Soru: Faturayı yarıya indiren ilk kaldıraç hangisi? Çıktı payı kaç?
4. **Yayınla (7 dk).** Azure for Students hesabınla:
   ```bash
   cd week4/ozetleyici
   export $(grep -v '^#' ../../.env | xargs)     # .env'i ortam değişkeni yap (Windows: set komutları)
   APP=ozet-<adin> ./deploy_aca.sh
   ```
   Azure'un yoksa alternatifler: (a) yerelde `uvicorn app:app --port 8000`; (b) `docker build -t ozet . && docker run -p 8000:8000 --env-file ../../.env ozet`; (c) Hugging Face Spaces'te *Docker* tipinde Space açıp bu klasörü yükle (ücretsiz).
5. **Teslim.** Üç şeyin ekran görüntüsü sınıf kanalına: model karşılaştırma tablosu, maliyet tablosu, yayındaki `/saglik` yanıtı (veya yerel çalıştırma).

**Başarı kriterleri**
- [ ] `foundry_test.py` en az iki model için token, gecikme ve maliyet yazdırıyor
- [ ] Kendi senaryonda önbellek ve kademe kaldıraçlarının etkisini yüzde olarak söyleyebiliyorsun
- [ ] Özetleyici bir URL'de (veya yerelde) çalışıyor ve `/saglik` `"durum": "ok"` dönüyor
- [ ] API anahtarın hiçbir dosyada, imajda ya da ekran görüntüsünde görünmüyor

## Sık karşılaşılan sorunlar

| Belirti | Sebep / çözüm |
|---|---|
| `401 Unauthorized` | Anahtar eksik kopyalanmış (`sk-or-v1-` ile başlar) ya da başka sağlayıcının anahtarı `LLM_BASE_URL`'le eşleşmiyor. |
| `404 model not found` | OpenRouter'da model adı önekli: `openai/gpt-6-luna`, `deepseek/deepseek-v4.1-flash`. Gemini/Ollama'da önek yok. |
| `402` / `insufficient credits` | Anahtarının harcama limiti doldu (lab'lar için fazlasıyla yeter; döngüde kalmış bir betik olabilir). Hocaya yaz, bu arada Gemini'ye geç. |
| `429 rate limit` | Kısa bekleyip tekrar dene; `:free` modellerde günlük istek sınırı var, ücretli modellerde yok. |
| Foundry kullanıyorsan base URL `/openai/v1/` ile bitmiyor | Foundry'nin OpenAI uyumlu endpoint'i bu yolla biter; `api-version` gerekmez; model adı = deployment adı. |
| `Connection refused :11434` | Ollama çalışmıyor: `ollama serve` sonra `ollama pull qwen3.5:4b`. |
| `az containerapp up` çok uzun sürüyor | İlk seferde ACR + ortam kurulur (3-5 dk). İkinci dağıtım 1 dk. |
| Container Apps'te 502 | `az containerapp logs show -n APP -g RG --follow`; büyük ihtimalle env var eksik → `/saglik` endpoint'ine bak. |
| Fatura korkusu | `--min-replicas 0` ile boşta ücret yok; ders sonunda `az group delete -n rg-ccai-week4 --yes`. |

## Fiyatları güncelleme

`fiyatlar.json` içindeki değerler **22 Eylül 2026** liste fiyatlarıdır (Hafta 1 slaytı). Dersten önce `kaynaklar` listesindeki sayfalardan kontrol edip `tarih` alanını güncelleyin. `varsayim` alanı dolu satırlar slaytta yoktu; oranla tahmin edildi.

## Gelecek hafta

**Hafta 5 — RAG ve vektör veritabanları (vize haftası).** Vize 1-4. haftaları kapsar: token/bağlam, prompt ve tipli çıktı, bulut katmanları ve bu haftaki maliyet kaldıraçları. Lab: Türkçe bir derlem üzerinde RAG kurup RAGAS tarzı ölçmek.

## Kaynaklar

- Microsoft Learn: *Azure Fundamentals — Describe cloud service types* · *Deploy to Azure Container Apps from source* · *Azure AI Foundry — Deploy models*
- OpenRouter: openrouter.ai/docs (OpenAI uyumlu API, model listesi ve fiyatlar), openrouter.ai/models
- Hafta 1 slaytı: fiyat kaldıraçları, para akışı
- epoch.ai → *LLM inference price trends* (fiyat düşüşü eğrisi)
- artificialanalysis.ai → zeka / hız / görev başına maliyet grafikleri
