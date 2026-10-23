# Hafta 2 · LLM'ler gerçekte nasıl çalışır: token, bağlam, dikkat, gömme

> **Lab:** Türkçe vs İngilizce token sayımı · temperature taraması · yerelde Türkçe model yarışı
> **Bu haftanın sorusu:** Neye para ödüyorsunuz, model neyi görebiliyor, neden "unutuyor" ve anlam nasıl sayıya dönüşüyor?

Dersin tek "kaputun altı" haftası. Amaç matematik değil, sonraki her kararda işinize yarayacak zihinsel model: Türkçe neden 1.5-2× daha pahalı, uzun prompt neden masraflı, temperature gerçekte ne yapıyor, 1.6T parametreli bir model nasıl ucuza çalışıyor (MoE), akıl yürütme modları neden bir *maliyet ayarı* ve gömme (embedding) nedir (Hafta 5 buna dayanıyor). Lab'da söylenenleri ölçüyorsunuz: inanmak yerine sayın.

## Ders akışı (90 dk)

| Süre | Bölüm |
|---|---|
| 0-5 dk | Giriş: aynı cümle Türkçede iki kat pahalı |
| 5-30 dk | Teori 1: token (BPE), bağlam penceresi (8K → 1M), sonraki token tahmini, temperature / top-p, öz-dikkat (Q/K/V), ölçekleme ve MoE, akıl yürütme modları |
| 30-45 dk | **Canlı demo**: Transformer Explainer, Tiktokenizer'da TR/EN, temperature taraması |
| 45-50 dk | Ara (`ollama pull` başlatılmadıysa şimdi) |
| 50-62 dk | Teori 2: gömme ve kosinüs benzerliği, yerel vs bulut çıkarım, nicemleme (Q4_K_M), telefona sığan modeller; bankanın çağrı merkezi vakası (−%91 token maliyeti) |
| 62-80 dk | **Lab** |
| 80-90 dk | Üç quiz sorusu + gelecek hafta |

## Klasördekiler

| Dosya | Ne işe yarar |
|---|---|
| `tokens.py` | Aynı kira sözleşmesi paragrafını Türkçe ve İngilizce olarak üç tokenizer ile sayar: tiktoken `o200k_base` (GPT-4o/5/6), Qwen, Kumru; TR/EN oranı ve `evlerimizdekilerden` kelimesinin parçalanışı |
| `temperature.py` | Tek Türkçe prompt, temperature 0 / 0.7 / 1.5, her birinde üç çalıştırma; sonunda sizin yorumunuz |
| `bakeoff.py` + `questions.json` | Ollama'daki `vngrs-ai/Kumru-2B` ve `qwen3.5:4b`'ye 10 Türkçe soru; doğruluk (anahtar kelime) ve token/sn; `results.csv` yazar |
| `similarity.py` | Bonus: 5 Türkçe cümlenin kosinüs benzerlik matrisi (`ytu-ce-cosmos/turkish-e5-large`) |
| `requirements.txt` | `openai`, `python-dotenv`, `tiktoken`, `transformers` (bonus için `sentence-transformers`) |
| `README.en.md` | Eğitmenin özgün İngilizce lab metni (arşiv) |

Kurulum: `pip install -r week2/requirements.txt`. `.env` Hafta 1'deki gibi (`LLM_*`; eski `GEMINI_API_KEY` de çalışır). Yerel modeller için kendi laptopunuzda: `ollama pull qwen3.5:4b` ve `ollama pull vngrs-ai/Kumru-2B` — **indirmeyi dersin başında başlatın**.

## Canlı demo (hoca · 15 dk)

1. **Transformer Explainer (5 dk).** https://poloclub.github.io/transformer-explainer → "Banka nehir kenarında" yazın, dikkat görünümünü açın: `banka` hangi token'lara bakıyor? `nehir` yerine `faiz` yazınca değişiyor mu? Temperature kaydırıcısını oynatın. (Statik site; bir kez yüklenince çevrimdışı da çalışır.)
2. **Tiktokenizer (4 dk).** https://tiktokenizer.vercel.app → 120 kelimelik aynı paragrafı Türkçe ve İngilizce yapıştırın, gpt-4o ve Qwen sekmelerinde sayıları karşılaştırın. Renkli özel token'ları gösterin: sohbet şablonu bedava değil. Bölünmeler nereye düşüyor (ekler, ş/ğ/ı)?
3. **Temperature taraması (5 dk).** AI Studio'da (Gemini 3.5 Flash) tek bir Türkçe prompt, T = 0 / 0.7 / 1.5, her birinde üç çalıştırma. Beklenti: T=0 neredeyse aynı; 0.7 aynı anlam farklı ifade; 1.5 yanlış bilgi, araya giren İngilizce. Aynı tarama bu depoda:
   ```bash
   python week2/temperature.py
   ```

> **Ağ çökerse:** `python araclar/sahte_llm_sunucu.py` + `.env`'de (d) bloğu ile `temperature.py` çalışır; `tokens.py` ağ istemez ama tiktoken sözlüğü ve HF tokenizer dosyaları **ilk** çalıştırmada iner (dersten önce bir kez çalıştırın, sonrası önbellekten). Transformer Explainer bir kez yüklenince çevrimdışı da çalışır; Tiktokenizer için ekran görüntüsü alın.

## Lab (öğrenci · 20 dk)

**Hedef:** Derste söylenen üç şeyi kendiniz ölçmek: Türkçe daha çok token tutar, temperature determinizmi değiştirir, 2B'lik bir Türkçe model kendi laptopunuzda 4B'lik genel modelle yarışabilir.

1. **Kurulum (2 dk).** `pip install -r week2/requirements.txt`; `.env` Hafta 1'deki gibi. Laptopunuzda (Codespaces değil): `ollama pull qwen3.5:4b` ve `ollama pull vngrs-ai/Kumru-2B` — en uzun süren adım, hemen başlatın.
2. **tokens.py (5 dk).** `cd week2 && python tokens.py` → üç tokenizer için TR ve EN sayıları ve TR/EN oranı. Oranı not edin (o200k'da 1.3-2.0, Kumru'da daha düşük bekleyin). `evlerimizdekilerden` kaç parçaya bölünüyor?
3. **temperature.py (4 dk).** `python temperature.py` → dokuz çıktı. Her temperature için tek satırlık yorum: aynı mı? aynı anlam mı? bozuldu mu?
4. **bakeoff.py (8 dk).** `python bakeoff.py` → iki yerel model, 10 Türkçe soru; model başına doğruluk ve token/sn, `results.csv`. Hatalara bakın: Kumru yanlış mı, yoksa doğru ama farklı kelimelerle mi? (Hafta 8'de bu kaba metriğin yerini gerçek eval alır.)
5. **Bonus — similarity.py.** `pip install sentence-transformers` (ilk çalıştırmada ~1 GB model iner; RAM darsa Colab), `python similarity.py` → hangi çiftler 1'e, hangileri 0'a yakın? Bu geometri, Hafta 5'te RAG'in aradığı şeydir.
6. **Teslim.** Token tablosu + temperature yorumlarınız + `results.csv` (ya da ekran görüntüsü) sınıf kanalına.

**Başarı kriterleri**
- [ ] 3 tokenizer için TR ve EN token sayıları ve oranı içeren bir tablo
- [ ] Dokuz temperature çıktısı ve her temperature için tek satırlık yorumunuz
- [ ] İki yerel modelin doğruluk ve token/sn değerlerini içeren `results.csv`
- [ ] Türkçe prompt'un neden pahalı olduğunu ve temperature'ın ne zaman 0 olması gerektiğini söyleyebiliyorsunuz

## Sık karşılaşılan sorunlar

| Belirti | Çözüm |
|---|---|
| `ModuleNotFoundError: tiktoken` | `pip install -r week2/requirements.txt` (sanal ortam aktif mi?) |
| Hugging Face indirmesi kampüs Wi-Fi'ında engelli | `tokens.py` HF tokenizer'larını atlar, tiktoken satırını yine yazar; evde tekrar çalıştırın |
| `Connection refused :11434` | `ollama serve` çalışmıyor; etiketler `ollama list` ile uyuşmuyorsa `bakeoff.py` içindeki `MODELS` listesini düzenleyin |
| Codespaces'te Ollama yok | 1. ve 4. adımlar laptopunuzda; 2. ve 3. adımlar her yerde |
| Gemini `429` | `.env`'de `LLM_MODEL=gemini-3.5-flash-lite` ya da `temperature.py`'yi Ollama'ya yönlendirin (dosyadaki yorumlu satır) |
| Kumru çok yavaş | CPU'da 5-15 token/sn normal; `max_tokens=120` zaten sınırlı; sonuçları bekleyin, hızı kaydedin |

## Gelecek hafta

**Hafta 3 — Prompt mühendisliği ve tip güvenli çıktılar:** rol + bağlam + format + kısıt prompt'ları, few-shot, Instructor + Pydantic ile JSON Schema kısıtlı üretim. Lab: 20 Türkçe haber parçası üzerinde `extract.py` ve GitHub org'unda kendi reponuz. Dersten önce: GitHub hesabınız org davetini kabul etmiş olsun.

## Kaynaklar

- 3Blue1Brown, *But what is a GPT?* ve *Attention in transformers* (~50 dk) · Karpathy, *Let's build the GPT tokenizer*
- Vaswani ve ark., *Attention Is All You Need* (2017), Bölüm 1-3 · DeepSeek V4 sürüm notu (24 Nisan 2026)
- poloclub.github.io/transformer-explainer · tiktokenizer.vercel.app · github.com/openai/tiktoken
- huggingface.co/vngrs/Kumru-2B · huggingface.co/ytu-ce-cosmos/turkish-e5-large · ollama.com/library · lmstudio.ai
- Derinleşmek için: Stanford CS25 V6 (2026) · HF LLM kursu, tokenizer bölümü · sbert.net · Anthropic/OpenAI prompt caching ve reasoning effort belgeleri
