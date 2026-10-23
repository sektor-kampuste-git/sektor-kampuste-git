# Hoca hazırlık listesi — Güz 2026

> Bu klasör eğitmen içindir; repoya girer ama **anahtar, endpoint URL'si ya da öğrenci bilgisi içermez**. Üç dosya: bu liste (ne zaman ne yapılacak), [`duyuru_metinleri.md`](duyuru_metinleri.md) (sınıf kanalına kopyala-yapıştır), [`ders_oncesi_kontrol.md`](ders_oncesi_kontrol.md) (her ders günü 10 dakikalık prova). Öğrencilere kalan tek iş: anahtarları dağıtmak, hesapları açmak, kanala yazmak.

**Takvim varsayımı:** dersler Cuma; Hafta 1 = 2 Ekim 2026 (Hafta 3 lab'ının ekran görüntüleri 16 Ekim). Buna göre Hafta 4 = 23 Ekim, Hafta 5 (vize) = 30 Ekim, Hafta 6 = 6 Kasım, Hafta 7 = 13 Kasım, Hafta 8 = 20 Kasım, Hafta 9 = 27 Kasım, Hafta 10 = 4 Aralık, Hafta 11 = 11 Aralık, Hafta 12 = 18 Aralık, Hafta 13 = 25 Aralık, **Hafta 14 = 1 Ocak 2027 (resmî tatil!)**, Hafta 15 = 8 Ocak. Sunum gününü ve final tarihini okul takvimine göre siz kesinleştirip duyurun; öğrenci belgeleri (`proje/PROJE_ODEVI.md`, `week11/README.md`) bilerek yalnızca hafta numarası kullanır.

## 0. Hemen (Hafta 4'ten önce, tek seferlik)

- [ ] **Repoyu public yap:** GitHub → `sektor-kampuste-git/sektor-kampuste-git` → Settings → General → Danger Zone → *Change visibility* → Public. (Bu oturumdan yapılamadı; proxy repo ayarlarını engelliyor.)
- [ ] **Dal kararı:** şu an tek dal `claude/modest-fermat-14wqlj` ve varsayılan dal bu. Öğrencilere verdiğiniz bütün bağlantılar `tree/<dal>` içerir; `main` oluşturup varsayılan yapmak isterseniz: Settings → Branches → *Default branch* (önce `git branch main && git push -u origin main`). Bu karar sizin; README'deki `git clone` komutu her iki durumda çalışır.
- [ ] **Sınıf kanalına repo bağlantısı** ([`duyuru_metinleri.md`](duyuru_metinleri.md) §"Repo açıldı").
- [ ] **LMS'e `proje/PROJE_ODEVI.pdf`** yükle; son teslim tarihini LMS'e ve kanala yaz.
- [ ] **Foundry deployment'ları** (§1) ve **anahtar dağıtım planı** (§2).
- [ ] **Kendi hesaplarınız** (§3): Google AI Studio anahtarı, Groq, OpenRouter (yedek sağlayıcılar), Langfuse, Streamlit Community Cloud, Azure aboneliği (Container Apps demosu), n8n (Docker), Copilot Studio tenant kontrolü.
- [ ] **Microsoft Learn for Educators:** bölümü kaydettirin → AI-901 / AZ-900 sınav kuponları (Hafta 1 ve 10 slaytlarında söz ediliyor).
- [ ] **Eğitim laptopu:** `ollama pull qwen3.5:4b`, `ollama pull bge-m3`, `ollama pull vngrs-ai/Kumru-2B`; `python -m venv .venv` + her haftanın `requirements.txt`; Node 18+ (`npx promptfoo`), Docker (n8n, Qdrant), Azure CLI (`az login`).
- [ ] **Demo yedekleri yok:** slaytlar `build/demo-wN/` ekran görüntülerine ve kayıtlı çalıştırmalara gönderme yapıyor ama Drive'da yoklar (`HANDOFF.md`: "None are created yet"). Her hafta provada (`ders_oncesi_kontrol.md`) gerçek modelle aldığınız çıktıların ekran görüntüsünü bir klasöre koyun; sahte sunucu akışı kurtarır, sayıları kurtarmaz.
- [ ] **Slayt lab sayfaları:** her TR deste lab slaytında `github.com/<course-org>/ccai-2026/tree/main/labs/weekNN` yazıyor; §5'teki tabloya göre repo yolu ve dosya adlarını düzeltin (deste başına 1-2 slayt).
- [ ] **Drive'daki `sinavlar/`, `ogrenciler/`, `Değerlendirilecek_Projeler/` klasörleri repoya girmedi** ve girmemeli; `bulut-bilisim-yz-katilimcilar.csv` öğrenci verisidir.

## 1. Azure AI Foundry deployment planı

Öğrenci abonelikleri Foundry'de model deploy edemez; endpoint'leri siz sağlarsınız (slaytlar ve `HANDOFF.md` bunu varsayar). Önerilen set; adlar repodaki varsayılanlarla uyumludur:

| Deployment adı (= `LLM_MODEL`) | Model | Kademe | Tür / bölge önerisi | Nerede kullanılıyor |
|---|---|---|---|---|
| `gpt-6-luna` | GPT-6 Luna | ucuz | Global Standard (en bol kota) ya da Sweden Central **Data Zone EU** (demo'da veri yerleşimini göstermek için; daha pahalı) | `.env.example` (b) bloğu varsayılanı; `week4/maliyet_hesapla.py --ucuz-model`; `week7/ajan_dongusu.py` fiyat varsayılanı ($0.10/$0.50); tüm lab'ların varsayılan modeli |
| `deepseek-v4.1-flash` | DeepSeek V4.1 Flash | ucuz / açık ağırlık | Global | Hafta 1 ve 4 demosu: `foundry_test.py --model gpt-6-luna --model deepseek-v4.1-flash`; "açık vs kapalı" karşılaştırması |
| `gpt-6-sol` **ya da** `claude-opus-5-5` | GPT-6 Sol / Claude Opus 5.5 | amiral | Global, düşük TPM yeter | Hakem (judge): `week5/degerlendir.py --hakem-model`, `week8/eval_calistir.py --hakem-model`, promptfoo `llm-rubric`; Hafta 4 "en pahalısı her zaman en iyisi değil" satırı |
| *(isteğe bağlı)* bir gömme modeli | Foundry kataloğundan çok dilli bir embedding modeli | — | Global | `EMBED_BASE_URL` / `EMBED_MODEL` (Hafta 5). Zorunlu değil: öğrenciler ücretsiz `gemini-embedding-001` (Gemini) ya da `bge-m3` (Ollama) kullanabilir |

**Kota:** 40-50 öğrenci aynı anda lab yaparken tek deployment 429 verir (`HANDOFF.md` uyarısı). Her deployment'ın TPM'ini aboneliğin izin verdiği en üste çekin; yetmezse `gpt-6-luna` için ikinci bir deployment (`gpt-6-luna-b`) açıp sınıfı ikiye bölün. Lab'larda `max_tokens` küçük (README'lerde zaten 300-400).
**Maliyet koruması:** Cost Management → Budgets: aylık bütçe ve %80 / %120 alarmı (Hafta 4 slaytındaki tavsiyenin aynısı). Dönem başına beklenen tüketim: lab başına öğrenci başına < $0.05; projelerde takım başına birkaç dolar.
**Endpoint biçimi:** `https://<kaynak-adı>.openai.azure.com/openai/v1/` (sonunda `/openai/v1/`; `api-version` gerekmez). Model adı = **deployment adı**. `week4/README.md` sık sorunlar tablosu bunu anlatıyor.

## 2. Anahtar dağıtımı

| Kime | Ne | Nasıl | Ne zaman yenilenir |
|---|---|---|---|
| Bütün sınıf (lab'lar) | Tek Foundry kaynağının **Key 1** + endpoint + deployment adları | LMS duyurusu ya da sınıf kanalında sabitlenmiş mesaj; **slaytlara yazmayın**, ekran görüntüsüne girmesin | Hafta 11'de (proje anahtarları verilince) ve dönem sonunda; sızıntı şüphesinde hemen (Key 2'ye geçin, sonra Key 1'i yenileyin) |
| Her proje takımı (Hafta 11'den itibaren) | Ayrı Foundry projesi/kaynağı ya da en azından ayrı deployment + bütçe alarmı | Takım liderine özel mesaj; takım `.env`'e yazar, repoya asla girmez | Dönem sonunda; takım üyesi ayrılırsa |
| Öğrenci (kendi) | Gemini (AI Studio), Groq, OpenRouter, Streamlit Cloud, Langfuse, GitHub token | Öğrenci kendi açar (Hafta 1 lab'ı) | — |
| Hoca (kendi) | Gemini, Groq, OpenRouter yedekleri; Langfuse; Azure | Yalnızca `.env` (gitignore'da) | — |

Sızan anahtar kuralı (README'de): anahtar repoda görülürse sızmış sayılır, yenilenir, projede −10.

## 3. Hesap ve servis listesi

| Servis | Kim | Ne için | Not |
|---|---|---|---|
| Azure AI Foundry (ai.azure.com) | Hoca | Deployment'lar (§1), kullanım panosu demosu (Hafta 4) | Kurumsal/PEAKUP aboneliği |
| Azure for Students | Öğrenci | Container Apps (Hafta 4, 6), Key Vault, AI Search Free | $100 / 12 ay, kart yok; Foundry deploy edemez |
| Azure aboneliği (hoca) | Hoca | `week4/ozetleyici/deploy_aca.sh` canlı demosu; Container Apps | Dersten önce bir kez deploy (3-5 dk), ders sonunda `az group delete -n rg-ccai-week4 --yes` |
| Google AI Studio | Öğrenci + hoca | Gemini ücretsiz anahtarı; `gemini-embedding-001` | Ücretsiz katman verisi eğitimde kullanılabilir → özel veri yok |
| Google AI Plus (gemini.google/tr/students) | Öğrenci | 1 yıl ücretsiz (18+, SheerID) | **31 Aralık 2026'ya kadar** başvuru; Hafta 4-5 duyurusunda hatırlatın |
| GitHub Student Developer Pack | Öğrenci | Codespaces 180 saat/ay, Pro | Onay günler-haftalar; Hafta 1'de başvurdular, takip edin |
| GitHub org `sektor-kampuste-git` | Hoca (owner) | Öğrenci repoları `<ad>_<üniversite>_<no>` (42 repo, 53 üye, 16 Ekim) | Adlandırma dışı repoları düzelttirin; proje repoları **public** olacak (org dışında da olabilir) |
| Zed Pro (zed.dev/education) | Öğrenci | Hafta 6 ajan aracı | 1 yıl ücretsiz |
| GitHub Copilot Free | Öğrenci | Hafta 6-7 (VS Code agent modu, MCP) | Öğrenci kayıtları durdu; Free yeter |
| Streamlit Community Cloud | Öğrenci + hoca | Hafta 6 yayın, proje demo URL'si | Hoca: `week6/baslangic` bir kez yayınlanmış olsun (Secrets'a `.env` içeriği TOML olarak) |
| Langfuse (cloud.langfuse.com) | Öğrenci + hoca | Hafta 8 tracing | Ücretsiz proje; `LANGFUSE_PUBLIC_KEY/SECRET_KEY/HOST` `.env`'e; AB bölgesi `cloud.langfuse.com` |
| promptfoo (`npx promptfoo@latest`) | Hoca + öğrenci | Hafta 8 eval tablosu | Node 18+; hakem için `OPENAI_API_KEY=$LLM_API_KEY OPENAI_BASE_URL=$LLM_BASE_URL` |
| n8n (Docker) | Hoca | Hafta 9 prototip | `cd week9/n8n && docker compose up -d` dersten önce; `.env` n8n klasöründe |
| Copilot Studio | Hoca (varsa M365 tenant) | Hafta 9 Plan A | Lisans yoksa n8n yolu (README'de kıyas tablosu) |
| Ollama | Hoca + öğrenci | Hafta 1, 2, 4, 5 yerel model | `qwen3.5:4b`, `bge-m3`, `vngrs-ai/Kumru-2B`; Codespaces'te çalışmaz |
| Groq, OpenRouter | Yedek | Foundry 429 verirse ikinci sağlayıcı | Ücretsiz katman limitleri `week1/ogrenci_kaynaklari_2026.md` |

## 4. Hafta hafta

Her satır: **önceki gün** hazırlık → **ders günü** ısıtma (komutlar `ders_oncesi_kontrol.md`'de) → **duyuru** (`duyuru_metinleri.md`).

### Hafta 4 — Bulut, Foundry, maliyet, Container Apps (23 Ekim)
- Önceki gün: §0 ve §1 bitmiş; `week4/fiyatlar.json` içindeki `tarih` alanını ve fiyatları sağlayıcı sayfalarından kontrol edin (22 Eylül 2026 liste fiyatları); `week4/ozetleyici/deploy_aca.sh` bir kez çalıştırılmış (ACR + ortam kurulumu 3-5 dk); Foundry anahtarını LMS'e koyun.
- Ders günü: `foundry_test.py` iki deployment + Ollama ile; `maliyet_hesapla.py` iki senaryo; Container Apps URL'si açılıyor; sahte sunucu yedeği hazır.
- Duyuru: Hafta 4 ön koşullar + proje duyurusu + vize hatırlatması (üçü aynı gün).

### Hafta 5 — Vize (30 dk) + RAG (30 Ekim)
- Önceki gün: vize kâğıtları (Drive `sinavlar/TR/`; repoya girmez); `EMBED_MODEL` kararı (Gemini `gemini-embedding-001` ücretsiz → öğrencilere bu; Foundry gömme deployment'ı açtıysanız adını duyurun); `pip install -r week5/requirements.txt`; `indeksle.py` → `sor.py` → `degerlendir.py` gerçek anahtarla bir kez; isteğe bağlı `docker run -p 6333:6333 qdrant/qdrant`.
- Ders günü: `gomme_demo.py`, `parcala.py`, dört `sor.py` sorusu, `degerlendir.py --sinir 6`. Hakem modeli amiral deployment (`--hakem-model gpt-6-sol`).
- Duyuru: vize hatırlatması (bir hafta önce, Hafta 4'te), Hafta 5 ön koşullar.

### Hafta 6 — Vibe coding (6 Kasım)
- Önceki gün: `week6/baslangic` kopyası + `.env` + `pytest -q` yeşil + `streamlit run app.py`; Streamlit Cloud'a bir kez yayınlanmış (Secrets); ajan aracı (Copilot agent modu / Zed / Claude Code) açık ve `AGENTS.md` okutulmuş; yedek ekran görüntüleri/video.
- Duyuru: Copilot Free'yi VS Code'da açtırın, Zed Pro aldırın, Streamlit Cloud hesabı açtırın; lab 40 dk.

### Hafta 7 — Ajanlar, MCP, A2A (13 Kasım)
- Önceki gün: `pip install "mcp>=2,<3"`; `mcp_istemci.py`, `ajan_dongusu.py --mcp`, `a2a_mini.py` gerçek modelle; `week7/ide_ayarlari/vscode_mcp.json` içindeki python yolunu kendi sanal ortamınıza çevirip VS Code Copilot Agent modunda "SIP-1001 nerede?" denemesi.
- Not: küçük yerel modellerin araç çağrısı zayıf; demoda Foundry/Gemini.
- Duyuru: `mcp` paketi 2.x, Copilot agent modu.

### Hafta 8 — Tracing, eval, güvenlik (20 Kasım)
- Önceki gün: Langfuse projesi + anahtarlar `.env`'de; `izleme_demo.py` iz gönderiyor; `eval_calistir.py --prompt promptlar/v1.txt` ve `v2.txt` gerçek modelle (sayıları not edin); `npx promptfoo@latest eval` + `view`; `kirmizi_takim.py`; `ci/eval.yml` örnek repoda yeşil (GitHub Secrets).
- Red team kuralı: `week8/guvenlik/kirmizi_takim_kontrol_listesi.md` — yalnızca izinle, yalnızca ders sistemleri.
- Duyuru: Langfuse hesabı, Node 18+, eşleşme için takım arkadaşı.

### Hafta 9 — İş yeri, ROI, yönetişim (27 Kasım)
- Önceki gün: `cd week9/n8n && docker compose up -d`, akış içe aktarılmış, iki `curl` çalışıyor; Copilot Studio hesabı varsa el kitabı ajanı hazır; `roi_hesapla.py` üç senaryo (ağ gerektirmez).
- Duyuru: öğrenciler bu hafta `docs/kullanim_senaryosu.md`'ye başlıyor (proje fikri burada doğar).

### Hafta 10 — Kariyer, portfolyo, 3 dk fikir sunumları (4 Aralık)
- Önceki gün: `portfolyo_kontrol.py` bir örnek repoda (`GITHUB_TOKEN` rate limit için); kronometre; sunum sırası listesi; her takıma 2 satır yazılı not için şablon.
- Duyuru: 3 dk sunum formatı (`week10/sunum_sablonu.md`), portfolyo reposu public.

### Hafta 11 — Proje atölyesi, kapsam onayı (11 Aralık)
- Önceki gün: takım listesi; masa masa onay için `week11/README.md` kontrol noktaları; proje anahtarları (§2) hazır.
- Duyuru: kapsam onayı + eval planı; ara teslim tarihi (Hafta 12).

### Hafta 12 — Ara teslim (18 Aralık)
- Kanalda link toplama; `portfolyo_kontrol.py` ile hızlı tarama; eksik URL/eval'e geri bildirim.

### Hafta 13 — Red team eşleşmesi + prova (25 Aralık)
- Önceki gün: eşleşme listesi (takım A ↔ takım B, kimse kendi sistemini test etmez); rapor şablonu `week8/guvenlik/kirmizi_takim_kontrol_listesi.md`; prova için kronometre.
- Duyuru: red team eşleşme duyurusu (kurallar + rapor teslimi).

### Hafta 14 — Sunumlar (tarih: 1 Ocak tatil → okul takvimine göre belirleyin)
- `week11/sunum_gunu_akisi.md`; akran değerlendirme formu (anonim, 3 soru); sunum sırası bir gün önce kanalda; HDMI/USB-C adaptörü.

### Hafta 15 — Final sınavı
- Drive `sinavlar/TR/` (repoya girmez); `week11/final_konu_haritasi.md` öğrencinin elinde.

## 5. Slaytlar ↔ repo farkları (lab slaytlarını düzeltirken)

TR desteler (`Drive: 2026-Guz-Yeni-Seri/TR/Hafta-NN-*.pptx`) Eylül 2026 tasarımındaki `labs/weekNN` dosya adlarını kullanır; repo `weekN` klasörleri ve Türkçe dosya adlarıyla kuruldu. Hafta 1-3 kodları birebir alındı, 4-10 yeniden yazıldı. Her deste için lab slaytında düzeltilecekler:

| Hafta | Slaytta | Repoda |
|---|---|---|
| Hepsi | `github.com/<course-org>/ccai-2026/tree/main/labs/weekNN` | `github.com/sektor-kampuste-git/sektor-kampuste-git/tree/<dal>/weekN` |
| 1 | `labs/week01/hello.py`, `.env` içinde `GEMINI_API_KEY` | `week1/hello.py`; kök `.env`'de `LLM_API_KEY` (eski ad da çalışır) |
| 2 | `labs/week02/{tokens,temperature,bakeoff,similarity}.py` | `week2/` aynı dosyalar |
| 3 | `labs/week03/extract.py`, `BASE_URL/API_KEY/MODEL`, `demo.ipynb` | `week3/extract.py` (Pydantic `date` alanı çakışması düzeltildi), `LLM_*`; notebook yok, demo `extract.py` ile |
| 4 | `call_two.py`, `cost-sheet.csv`, `api/main.py`, `deploy.sh` (`w04-<ad>`, `rg-ccai-w04`), `FOUNDRY_*` | `foundry_test.py`, `maliyet_hesapla.py` + `senaryolar/*.json`, `ozetleyici/app.py`, `ozetleyici/deploy_aca.sh` (`APP=ozet-<ad>`, `rg-ccai-week4`), `LLM_*` |
| 5 | `rag.py index --chunk 200/800`, Chroma + yerel `turkish-e5-large`, `eval_ragas.py`, `gold.json` (10 soru), 15 belge | `indeksle.py --yontem/--boyut`, Qdrant bellek içi + BM25 hibrit, `degerlendir.py` (RAGAS tarzı hakem), `sorular.json` (13 soru), `derlem/` (8 belge), gömme API ile (`EMBED_MODEL`) |
| 6 | `SPEC.md`, FastAPI haber sınıflandırıcı demosu | `SPEC_SABLONU.md` + `spec_ornekleri/`, Streamlit `baslangic/` (6 test), `AGENTS.md`, `deploy.md` |
| 7 | `seed.py` → `products.db`, `mcp_server.py` (`search_products`, `low_stock`), Pydantic AI `agent.py --limit`, `tool_calls.log` | `araclar_yerel.py` (sipariş/kargo/iade/hesapla), `mcp_sunucu.py`, `mcp_istemci.py`, `ajan_dongusu.py --max-adim/--max-usd --mcp --trace`, `a2a_mini.py`; alan e-ticaret siparişi |
| 8 | `trace_langfuse.py`, `prompts/system.txt` (`CANARY-7f3a`), `promptfooconfig.yaml`, `.github/workflows/evals.yml`, `injections.md` | `izleme/izleme_demo.py`, `promptlar/v1.txt` `v2.txt`, `evaller.json` + `eval_calistir.py`, `promptfooconfig.yaml`, `ci/eval.yml`, `guvenlik/saldiri_seti.json` + `kirmizi_takim.py` |
| 9 | `TEMPLATE.md` (8 bölüm), `eu-ai-act-checklist.md`, `n8n-workflow.json`, `classify.py` + `emails.txt` | `kullanim_senaryosu_sablonu.md` (9 bölüm), `yonetisim_kontrol_listesi.md`, `n8n/destek_triyaj_workflow.json`, `roi_hesapla.py` + `senaryolar/` |
| 10 | `README-TEMPLATE.md`, 6 maddelik liste, `cv-bullets-TR-EN.md`, 90 sn video | `proje_readme_sablonu.md`, `portfolyo_kontrol.py` (10 madde), `cv_maddeleri.md`, `profil_kontrol_listesi.md`; proje videosu ≤ 2 dk |
| Proje | "10. haftada proje sunumları", "≥ 30 örnekli altın set" | Hafta 10 fikir sunumu, Hafta 14 final sunumu; ≥ 15 vaka zorunlu, 30 + kalibre hakem tam puan (`proje/PROJE_ODEVI.md`) |

## 6. Bilinen tuzaklar

- `week2/tokens.py` ilk çalıştırmada `o200k_base` sözlüğünü ve HF tokenizer dosyalarını indirir; kampüs Wi-Fi'ı engellerse HF satırları atlanır, tiktoken dosyası inmezse betik durur → eğitim laptopunda evden bir kez çalıştırın (önbelleğe alınır).
- Codespaces'te Ollama çalışmaz; yerel lab adımları laptopta.
- Foundry'de `404 model`: `LLM_MODEL` deployment adı değil model adı yazılmış.
- Streamlit Cloud uyuyan uygulama: sunum/notlandırma öncesi bir kez açın.
- promptfoo python sağlayıcısı: `PROMPTFOO_PYTHON=.venv/bin/python`.
- Sahte sunucu (`araclar/sahte_llm_sunucu.py`) her haftanın akışını çalıştırır ama sayılar anlamsızdır; eval'ler "başarısız" görünür.
- Hafta 14 = 1 Ocak: resmî tatil. Sunumları Hafta 13'e çekmek ya da ek güne almak gerekir.
