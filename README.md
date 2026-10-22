# Bulut Bilişim ve Yapay Zeka Teknolojileri — Güz 2026

**Sektör Kampüste** programı kapsamında, Baha Kırbaşoğlu tarafından verilen dersin **demo ve lab deposu**. Bu ders sinir ağlarının matematiğini değil, **bulut altyapısı üzerinde yapay zeka ile ürün geliştirmeyi** anlatır. Her hafta: tarihli kaynaklarla teori (35 dk) · canlı demo (15 dk) · kendi laptopunuzda lab (20 dk) · quiz (10 dk).

> Bu depo **herkese açık ve salt okunurdur**: klonlayın, çalıştırın, kendi reponuza kopyalayın. Buraya push yapamazsınız; lab teslimleri org'daki **kendi reponuza** (`<ad>_<üniversite>_<no>`) ve sınıf kanalına ekran görüntüsüyle yapılır.

## Haftalık plan

| Hafta | Konu | Lab | Klasör |
|---|---|---|---|
| 1 | 2026'da yapay zeka: manzara, ekonomi, araç çantası | Hesaplar + `hello.py` (bulut vs yerel model) | *derste paylaşıldı* |
| 2 | LLM'ler nasıl çalışır: token, bağlam, dikkat, gömme | Türkçe vs İngilizce token, temperature, yerel model yarışı | *derste paylaşıldı* |
| 3 | Prompt yazımı ve tip güvenli çıktılar; GitHub org'u | Instructor + Pydantic ile veri çıkarma; kendi reponuz | *derste paylaşıldı* |
| 4 | **Yapay zeka için bulut: IaaS'tan hizmet olarak modele** | Foundry endpoint'i · maliyet tablosu · Azure Container Apps'e deploy | [`week4/`](week4/) |
| 5 | **RAG ve vektör veritabanları** *(vize haftası)* | Türkçe derlem üzerinde hibrit RAG + RAGAS tarzı değerlendirme | [`week5/`](week5/) |
| 6 | **Vibe coding I: ajan tabanlı kodlama araçları** | 40 dk: spec'ten testli uygulamaya ve yayına | [`week6/`](week6/) |
| 7 | **Ajanlar, MCP ve A2A** | Bütçeli ajan döngüsü + kendi MCP sunucunuz | [`week7/`](week7/) |
| 8 | **Canlı ortam: DevOps, değerlendirme, güvenlik** | Tracing · CI'da 15 eval · arkadaşınızın sistemine red team | [`week8/`](week8/) |
| 9 | **İş yerinde yapay zeka: roller, ROI, yönetişim, hukuk** | Kullanım senaryosu özeti + Copilot Studio / n8n prototipi | [`week9/`](week9/) |
| 10 | **Kariyer, portfolyo ve final sunumları** | Portfolyo rötuşu + 3 dakikalık sunumlar | [`week10/`](week10/) |
| 11 | **Proje ve final hazırlığı** | Atölye: teslim şablonu, rubrik, konu haritası | [`week11/`](week11/) |

Her klasörde bir `README.md` var: haftanın sorusu, demo adımları (hoca), lab adımları (öğrenci), başarı kriterleri, sık karşılaşılan sorunlar.

**Notlandırma:** Proje %30 · Vize %30 (Hafta 5, 1-4. haftaları kapsar) · Final %40 (senaryo ağırlıklı).

## Kurulum (bir kez)

```bash
git clone https://github.com/sektor-kampuste-git/sektor-kampuste-git.git
cd sektor-kampuste-git
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r week4/requirements.txt                  # her haftanın kendi requirements.txt'si var
cp .env.example .env                                   # anahtarlarınızı .env'e yazın; .env asla commit'lenmez
```

Python 3.12+ önerilir. [uv](https://docs.astral.sh/uv/) kullananlar: `uv venv && uv pip install -r week4/requirements.txt`.

### Model erişimi: tek OpenAI uyumlu istemci, çok arka uç

Tüm lab kodu üç ortam değişkeni okur: `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`. Aynı kod şunlarla çalışır:

| Arka uç | Nereden | Ücret |
|---|---|---|
| **Azure AI Foundry** | Hocanın paylaştığı endpoint ve anahtar (Claude, GPT, DeepSeek, Qwen tek katalogda) | Ders karşılar |
| **Google AI Studio (Gemini)** | Kendi ücretsiz anahtarınız — aistudio.google.com | Ücretsiz katman |
| **Ollama** | Kendi laptopunuz — `ollama pull qwen3.5:4b` | $0, çevrimdışı |
| Groq · OpenRouter · DeepSeek | Ücretsiz katmanlar | `.env.example`'da |
| **Sahte sunucu** | `python araclar/sahte_llm_sunucu.py` | Ağ yokken; gerçek model değildir |

Ayrıntı ve hazır bloklar: [`.env.example`](.env.example). Hafta 5 gömme modeli için `EMBED_MODEL` (Gemini: `gemini-embedding-001`, Ollama: `bge-m3`).

### Ücretsiz öğrenci kaynakları
GitHub Student Developer Pack (Codespaces 180 saat/ay) · Azure for Students ($100, kart gerekmez) · Google AI Plus (TR öğrencilerine 1 yıl) · Zed Pro (1 yıl) · Copilot Free · Streamlit Community Cloud · Azure Container Apps ücretsiz katman. Doğrulanmış liste Hafta 1 notlarında.

## Depo düzeni

```
.env.example        ← ortak ortam değişkenleri şablonu
araclar/            ← sahte_llm_sunucu.py (çevrimdışı yedek ve test)
week4/ … week11/    ← her hafta: README.md + demo/lab kodu + requirements.txt
```

Her haftanın kodu **kendi başına çalışır** (haftalar arası import yok); bir klasörü kopyalayıp kendi projenize başlayabilirsiniz.

## Ders kuralları

- **Yapay zeka araçlarını kullanmanız beklenir**; nasıl kullandığınızı README'nizde "AI kullanımı" bölümünde belirtirsiniz.
- **Lab'lar katılım sayılır**: ekran görüntünüzü sınıf kanalına atın.
- **Sırlar**: API anahtarı hiçbir dosyaya, ekran görüntüsüne, commit'e girmez. `.env` gitignore'dadır. Sızan anahtar yenilenir.
- **Red team** yalnızca sınıf arkadaşının izniyle, yalnızca bu dersin lab sistemlerine (`week8/guvenlik/kirmizi_takim_kontrol_listesi.md`).

## Sorun giderme (ortak)

| Belirti | Çözüm |
|---|---|
| `LLM_BASE_URL ve LLM_API_KEY tanımlı değil` | `.env` repo kökünde mi? `cp .env.example .env` sonra düzenleyin |
| `401` | Anahtar yanlış/eksik ya da başka kaynağın anahtarı |
| `404 model` | `LLM_MODEL` Foundry'de **deployment adı** olmalı |
| Ağ yok | `python araclar/sahte_llm_sunucu.py` + `.env`'de (d) bloğu |
| Windows'ta `source` çalışmıyor | `.venv\Scripts\activate`; `export` yerine `set` ya da `.env` dosyası (otomatik okunur) |

Haftaya özel sorunlar ilgili klasörün README'sinde.

## Lisans

Kod ve belgeler [MIT](LICENSE) lisansıyla paylaşılır; kendi projelerinizde serbestçe kullanın, kaynak gösterin. Fiyat tabloları ve araç listeleri tarihlidir (Eylül-Ekim 2026); kullanmadan önce güncelliğini kontrol edin.
