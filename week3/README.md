# Hafta 3 · Prompt mühendisliği ve tip güvenli çıktılar

> **Lab:** 20 Türkçe haber parçası üzerinde Instructor + Pydantic ile tipli çıkarım · GitHub org'unda kendi reponuz
> **Bu haftanın sorusu:** Bir sohbet modelini kodunuzun *güvenebileceği* bir bileşene ne çevirir? (Cevap: şema + doğrulayıcı + yeniden deneme.)

Bugün iki yarı var. İlk yarı bir zanaat olarak prompt yazımı: rol + bağlam + format + kısıtlar, few-shot ne zaman işe yarar, akıl yürüten modellerde "adım adım düşün" neden zarar verir, prompt'lar neden git'te durur. İkinci yarı haftanın özü: **yapılandırılmış çıktılar**. Şema, "sohbet"ten "yazılım"a geçişin köprüsüdür: biçimi sağlayıcı garanti eder (kısıtlı çözümleme), anlamı sizin doğrulayıcılarınız; Instructor doğrulama hatalarını yeniden denemeye çevirir. Haziran 2026'ya kadar 1.598 avukat uydurulmuş atıf yüzünden yaptırım aldı: hepsi doğrulanmamış serbest metin.

## Ders akışı (90 dk)

| Süre | Bölüm |
|---|---|
| 0-5 dk | Giriş: doğrulanmamış çıktının bedeli |
| 5-30 dk | Teori 1: prompt anatomisi (rol, bağlam, format, kısıt), system vs user, few-shot, CoT vs yerleşik akıl yürütme, prompt = kod (sürümleme, CLAUDE.md/AGENTS.md), injection'a ilk bakış (OWASP LLM01) |
| 30-45 dk | **Canlı demo**: bir haber, bir Pydantic şeması, iki sağlayıcı, bilerek tetiklenen doğrulama hatası |
| 45-50 dk | Ara |
| 50-62 dk | Teori 2: kısıtlı çözümleme (OpenAI `response_format`, Anthropic structured output, Gemini `response_schema`), Instructor / Pydantic AI / Zod, araç çağırma aynı mekanizma, taşınabilirlik uyarıları, lojistik şirketinde fatura/KYC vakası (%94 insansız) |
| 62-80 dk | **Lab** |
| 80-90 dk | Üç quiz sorusu + gelecek hafta |

## Klasördekiler

| Dosya | Ne işe yarar |
|---|---|
| `extract.py` | Instructor + Pydantic çıkarıcı: `news.json`'daki 20 parçayı `NewsRecord` (title, entities[], sentiment, date) kayıtlarına çevirir; 3 doğrulayıcı; `parse:error` hook'u ile yeniden deneme sayar; `results.csv` + `failed.csv` |
| `news.json` | 20 kısa Türkçe haber parçası (**sentetik**; şirketler ve olaylar kurgusal). 20. parça bir prompt injection satırı içerir |
| `extract.ts` + `package.json` | Bonus: aynı çıkarıcı TypeScript'te, Zod + `zodResponseFormat` + elle yazılmış yeniden deneme döngüsü (Node 20+) |
| `requirements.txt` | `openai`, `instructor`, `pydantic`, `python-dotenv` |
| `README.en.md` | Eğitmenin özgün İngilizce lab metni (arşiv) |

Kurulum: `pip install -r week3/requirements.txt`. `.env` ortak (`LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL`; kod eski `BASE_URL` / `API_KEY` / `MODEL` adlarını da okur). Sahte sunucu şemaya uygun örnek JSON döndürür: akış anahtarsız da denenir.

## Canlı demo (hoca · 15 dk)

1. **Şemayı göster (3 dk).** `extract.py` içindeki `NewsRecord`; `python -c "from extract import NewsRecord; print(NewsRecord.model_json_schema())"` ile ham JSON Schema. Model Python sınıfını görmez, bu şemayı görür. `Field` kısıtları şemaya girer, `field_validator` sizin kodunuzda çalışır.
2. **İki sağlayıcı, aynı kod (6 dk).**
   ```bash
   cd week3
   python extract.py                          # .env: Gemini Flash-Lite
   # .env'de LLM_BASE_URL/LLM_API_KEY/LLM_MODEL → hocanın Foundry deployment'ı, tekrar:
   python extract.py
   ```
   Değişen yalnızca `base_url`, `api_key`, `model`. Özet satırını okuyun: `model=... records=20 failed=0 total retries=...`.
3. **Bozalım (4 dk).** Bir parçanın tarihini gelecek haftaya çekin ya da `not_future` doğrulayıcısına bakın: Pydantic reddeder, Instructor hata metnini yeniden deneme prompt'una koyar, ikinci cevap tam o alanı düzeltir. 20. parça: şema biçimi korur ama başlığa `HACKED` yazılmasını yalnızca sizin doğrulayıcınız yakalar (lab alıştırması).
4. **Mode.JSON vs Mode.TOOLS (2 dk).** `instructor.Mode.JSON` ücretsiz sağlayıcılarda en taşınabilir olanı; Gemini ve Foundry'de `Mode.TOOLS` deneyip yeniden deneme sayısını karşılaştırın.

> **Ağ çökerse:** sahte sunucu `response_format` görünce şemaya uygun örnek JSON döndürür; akış aynen çalışır, değerler anlamsızdır. Terminal kaydı Drive'daki `build/demo-w3/` içinde.

## Lab (öğrenci · 20 dk)

**Hedef:** 20 tipli kayıt, iki sağlayıcı, arkasında durabileceğiniz bir yeniden deneme sayısı; artı sınıf org'unda kendi reponuz.

1. **Kendi reponuz (3 dk).** github.com/sektor-kampuste-git org'unda *New repository* → ad: `<ad>_<üniversite>_<no>` (örn. `aysegul_kostu_230501001`), **Private**, *Add README* işaretli. Klonlayın; bu dönemki lab çıktılarınız buraya gidecek. `.gitignore`'a ilk commit'te `.env` ekleyin.
2. **Kurulum (2 dk).** `pip install -r week3/requirements.txt`; `.env` kökte, Gemini anahtarınızla.
3. **extract.py'yi okuyun ve tamamlayın (5 dk).** `NewsRecord` ve üç doğrulayıcı hazır (title boş değil ve ≤120 karakter; entities tekilleştirilmiş ve ≥1; date ≤ bugün). Dördüncüsünü siz ekleyin: `HACKED` başlığını reddeden bir `field_validator` (20. parçaya bakın).
4. **Çalıştırın (4 dk).** `cd week3 && python extract.py` → satır başına `retries=`, sonunda özet; `results.csv` ve `failed.csv`.
5. **Sağlayıcı değiştirin (4 dk).** `.env`'de yalnızca üç değeri değiştirip tekrar çalıştırın (Groq, OpenRouter, Ollama `qwen3.5:4b` ya da hocanın Foundry endpoint'i). İki CSV'yi karşılaştırın: yeniden denemeler, hatalar, token'lar. Hangi doğrulayıcı en çok tetiklendi?
6. **Teslim (2 dk).** `results.csv` dosyalarını (anahtarsız!) kendi reponuza `week3/` altına push'layın; yeniden deneme özet satırının ekran görüntüsü sınıf kanalına. Bonus: `npm install && npm run extract` ile Zod sürümü (`results-ts.csv`).

| Sağlayıcı | `LLM_BASE_URL` | `LLM_MODEL` (örnek) | Not |
|---|---|---|---|
| Gemini API (ücretsiz) | `https://generativelanguage.googleapis.com/v1beta/openai/` | `gemini-3.5-flash-lite` | Flash / Flash-Lite; özel veri yok |
| Groq (ücretsiz) | `https://api.groq.com/openai/v1` | `openai/gpt-oss-20b` | ~30 istek/dk, günde 1.000 |
| OpenRouter (ücretsiz) | `https://openrouter.ai/api/v1` | `qwen/qwen3.5-9b:free` | günde 50 istek |
| Ollama (yerel) | `http://localhost:11434/v1` | `qwen3.5:4b` | `LLM_API_KEY=ollama`; JSON şema çıktısını destekler |
| Azure AI Foundry | hocadan | hocadan (deployment adı) | sınıf kanalında |

**Başarı kriterleri**
- [ ] `results.csv` iki sağlayıcıda da geçerli ISO tarih ve sentiment içeren 20 satırdan oluşuyor
- [ ] Her sağlayıcının kaç yeniden deneme gerektirdiğini ve en çok hangi doğrulayıcının tetiklendiğini söyleyebiliyorsunuz
- [ ] Dördüncü doğrulayıcı 20. parçayı yakalıyor
- [ ] Org'daki reponuz açık, `.env` gitignore'da, `week3/results.csv` push'lanmış

## Sık karşılaşılan sorunlar

| Belirti | Çözüm |
|---|---|
| `KeyError: 'LLM_BASE_URL'` / `'BASE_URL'` | `.env` repo kökünde ve üç değişken dolu mu? `cp .env.example .env` |
| Model `entities`'i tek bir virgüllü string döndürüyor | Virgülden bölen bir doğrulayıcı ekleyin (`v.split(",")`) |
| OpenAI dışı sağlayıcıda JSON hatası | `instructor.Mode.JSON` kullanın (dosyadaki varsayılan); `Mode.TOOLS` her yerde yok |
| `429` | Betik çağrılar arasında 1 sn bekler; artırın. Gemini'de Flash-Lite'a geçin |
| `12 Eylül 2026` → tarih doğrulaması düşüyor | System prompt ISO ister; model uymazsa yeniden deneme mesajı alanı ve kuralı söyler, çoğu ilk denemede düzeltir |
| `npm run extract` çalışmıyor | Node 20+; `node --env-file=.env node_modules/.bin/tsx extract.ts` |
| Repo adı yanlış | `<ad>_<üniversite>_<no>` kalıbı; büyük/küçük harf ve Türkçe karakter kullanmayın |

## Gelecek hafta

**Hafta 4 — Yapay zeka için bulut: IaaS'tan "hizmet olarak model"e.** Azure AI Foundry'den model kiralamak, gerçek bir fatura hesaplamak ve Türkçe özetleyiciyi Azure Container Apps'te yayınlamak. Dersten önce: Azure for Students'ı etkinleştirin (Hafta 1 lab adım 2), `pip install -r week4/requirements.txt`.

## Kaynaklar

- Anthropic ve OpenAI prompt engineering rehberleri (Eylül 2026) · OpenAI, *Structured model outputs* · Gemini API, structured output (`response_schema`) · Anthropic, structured outputs ve tool use belgeleri
- python.useinstructor.com (Concepts → Validation, Retrying, Hooks) · docs.pydantic.dev (validators, `model_json_schema`) · zod.dev · promptfoo.dev (Hafta 8)
- OWASP GenAI Top 10, LLM01 prompt injection (genai.owasp.org) · Stanford RegLab hukuk araçları çalışması · AI Hallucination Cases veritabanı
- Derinleşmek için: Anthropic Academy, Claude API kursu · Google Prompting Essentials (TR) · Pydantic AI belgeleri (`output_type`; Hafta 7 ön bakışı)
