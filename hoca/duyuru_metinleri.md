# Sınıf kanalı duyuru metinleri — Güz 2026

> Kopyala-yapıştır için hazır Türkçe duyurular. `<…>` alanlarını doldurun. Anahtarları **yalnızca** LMS'e ya da kanalda sabitlenmiş tek bir mesaja yazın; bu dosyaya ve slaytlara asla. Repo bağlantısı: `https://github.com/sektor-kampuste-git/sektor-kampuste-git` (dal: `<dal>`; `main` açarsanız bağlantıları güncelleyin).

---

## Repo açıldı (bir kez)

> 📂 **Ders deposu açıldı:** https://github.com/sektor-kampuste-git/sektor-kampuste-git
> Her haftanın klasöründe README (haftanın sorusu, demo, lab, başarı kriterleri, sık sorunlar), lab kodu ve `requirements.txt` var. Hafta 1-3 kodları da artık burada (`week1/`, `week2/`, `week3/`).
> Kurulum (bir kez): `git clone …` → `python -m venv .venv` → `cp .env.example .env` → anahtarınızı `LLM_API_KEY` satırına yazın. Ayrıntı kök README'de.
> Depo salt okunur: buraya push yapamazsınız; lab teslimleri **kendi reponuza** (`<ad>_<üniversite>_<no>`) ve bu kanala ekran görüntüsüyle. `.env` hiçbir zaman commit'lenmez; sızan anahtar yenilenir.

## Anahtar paylaşımı (LMS'te kişiye özel mesaj; şablon)

> 🔑 **Ders model anahtarınız (`<ogr-NN>`, yalnızca size özel, 1 $ harcama limitli)**
> `LLM_BASE_URL=https://openrouter.ai/api/v1`
> `LLM_API_KEY=<anahtar>`
> `LLM_MODEL=openai/gpt-6-luna` (diğerleri: `deepseek/deepseek-v4.1-flash`; hakem gerekirse `anthropic/claude-opus-5.5`)
> Bu değerleri `.env` dosyanıza yazın (`.env.example` (b) bloğu); ekran görüntüsüne, repoya, kanala koymayın, kimseyle paylaşmayın. Limit bütün lab'lara fazlasıyla yeter; `402` alırsanız bana yazın. Kendi ücretsiz anahtarınız (Gemini) her zaman yedeğiniz.

---

## Hafta 4 — Bulut, model erişimi, maliyet, Container Apps

> ☁️ **Hafta 4 (Cuma):** Yapay zeka için bulut: IaaS'tan "hizmet olarak model"e. API'den model kiralayacak (OpenRouter; Foundry'yi de göreceğiz), gerçek bir aylık fatura hesaplayacak ve Türkçe özetleyiciyi bir URL'de yayınlayacağız.
> **Dersten önce:** (1) Azure for Students aktif olsun (azure.microsoft.com/free/students; kart gerekmez) ve `az login` çalışsın; (2) `pip install -r week4/requirements.txt`; (3) LMS'te size özel gelen OpenRouter anahtarını `.env`'e yazın (`.env.example` (b) bloğu); (4) Ollama'da `qwen3.5:4b` inmiş olsun.
> **Lab teslimi:** üç ekran görüntüsü bu kanala: model karşılaştırma tablosu (`foundry_test.py`), maliyet tablosu (`maliyet_hesapla.py`), yayındaki `/saglik` yanıtı (ya da yerel çalıştırma). README: `week4/README.md`.
> Azure'unuz henüz onaylanmadıysa: yerelde `uvicorn` ya da HF Spaces alternatifleri README'de.

## Proje duyurusu (Hafta 4)

> 🧩 **Final projesi duyuruldu (%30):** `proje/PROJE_ODEVI.md` (PDF'i LMS'te). Türkçe bir kullanım senaryosu için bir yapay zeka uygulaması: tipli çıktılar + RAG **veya** araçlar/MCP + sıfır maliyetli deploy + ≥15 vakalık eval seti ve red team + maliyet ölçümü + yönetişim bölümü + sağlayıcıdan bağımsız kod + README "AI kullanımı".
> **Takım:** 1-3 kişi; her üye her dosyayı anlatabilmeli.
> **Takvim:** Hafta 9'a kadar senaryo + veri seçin (Hafta 9 lab'ında kullanım senaryosu özetini yazıyoruz) → Hafta 10: 3 dk fikir sunumu → Hafta 11: kapsam + eval planı onayı → Hafta 12: ara teslim (URL + ≥10 eval vakası) + red team eşleşmesi + prova → Hafta 13 (25 Aralık): sunumlar + `TESLIM.md` → son teslim: `<tarih/saat>`. Hafta 14 (1 Ocak) tatil.
> Fikir listesi: `week11/proje_fikirleri.md`. Rubrik: `week11/degerlendirme_rubrigi.md`. Ücretli model gerekmez; maliyeti **ölçmeniz** yeter.

## Vize hatırlatması (Hafta 4'te gönderin)

> 📝 **Vize: Hafta 5 (Cuma), dersin ilk 30 dakikası.** Kapsam Hafta 1-4: model manzarası ve açık/kapalı ekseni, token ve bağlam penceresi, temperature, dikkat ve gömme, prompt anatomisi, tipli çıktı ve doğrulayıcılar, bulut katmanları (IaaS→MaaS), dört fiyat kaldıracı, bölge/KVKK. Senaryo soruları; ezber değil karar. Çalışma rehberi: her haftanın README'sindeki "Bu haftanın sorusu" ve quiz soruları; `week11/final_konu_haritasi.md` ilk dört satır.
> Vizeden sonra ders normal devam eder (RAG); `pip install -r week5/requirements.txt` yapılmış gelin.

## Hafta 5 — RAG ve vektör veritabanları

> 🔎 **Hafta 5:** Vize (30 dk) + RAG: Türkçe bir çalışan el kitabını indeksleyip soru cevaplayacak ve **ölçeceğiz** (RAGAS tarzı sadakat/isabet).
> **Dersten önce:** `pip install -r week5/requirements.txt`; `.env`'de `EMBED_MODEL=gemini-embedding-001` (Gemini anahtarınızla) ya da Ollama için `ollama pull bge-m3` + `EMBED_BASE_URL=http://localhost:11434/v1`, `EMBED_MODEL=bge-m3`.
> **Lab teslimi:** iki değerlendirme tablosunun ekran görüntüsü + bir cümle "hangi kurulum, neden?". README: `week5/README.md`.
> Google AI Plus (1 yıl ücretsiz, gemini.google/tr/students) başvurusu **31 Aralık**'ta kapanıyor; almadıysanız alın.

## Hafta 6 — Vibe coding

> 🤖 **Hafta 6:** Ajan tabanlı kodlama araçlarıyla spec'ten testli ve yayınlanmış bir uygulamaya; lab bu hafta **40 dakika**.
> **Dersten önce:** VS Code'da GitHub Copilot Free açık (agent modu) **ya da** Zed Pro (zed.dev/education, 1 yıl ücretsiz) **ya da** başka bir ajan aracı; Streamlit Community Cloud hesabı (GitHub ile giriş); `pip install -r week6/baslangic/requirements.txt` ve `cd week6/baslangic && pytest -q` yeşil.
> **Lab teslimi:** repo linki + yayın URL'i + `pytest -q` ekran görüntüsü. Kural: ajanın yazdığı kodu README "AI kullanımı" bölümünde anlatıyorsunuz. README: `week6/README.md`.

## Hafta 7 — Ajanlar, MCP, A2A

> 🛠️ **Hafta 7:** Bu kez siz ajan yazıyorsunuz: araç çağrısı döngüsü, bütçe ve durma koşulu, kendi MCP sunucunuz.
> **Dersten önce:** `pip install -r week7/requirements.txt` (`mcp` 2.x); VS Code Copilot agent modu çalışıyor olsun (MCP istemcisi olarak). Araç çağrısı için OpenRouter (`openai/gpt-6-luna`) ya da Gemini; küçük yerel modeller araç çağırmakta zayıf.
> **Lab teslimi:** `mcp_istemci.py` çıktısında yeni aracınızın göründüğü + ajanın onu çağırdığı iz satırı ekran görüntüsü. README: `week7/README.md`.

## Hafta 8 — Tracing, eval, güvenlik

> 🧪 **Hafta 8:** "v2, v1'den iyi mi?" sorusuna sayıyla cevap: tracing, CI'da 15 eval, red team.
> **Dersten önce:** cloud.langfuse.com'da ücretsiz proje açıp anahtarları `.env`'e yazın; Node 18+ (`npx promptfoo@latest --version`); `pip install -r week8/requirements.txt`. Red team için bir eş seçin; **yalnızca izinle, yalnızca ders sistemlerine** (`week8/guvenlik/kirmizi_takim_kontrol_listesi.md`).
> **Lab teslimi:** v3 eval tablosu (≥13/15) + red team tablosu + eşinizden aldığınız rapor. Bonus: `ci/eval.yml` kendi reponuzda yeşil. README: `week8/README.md`.

## Hafta 9 — İş yerinde yapay zeka

> 🏢 **Hafta 9:** Roller, ROI, EU AI Act / KVKK, insan onayı; sonra n8n ya da Copilot Studio ile 15 dakikada prototip. **Proje fikriniz bu hafta kâğıda dökülüyor.**
> **Dersten önce:** Docker Desktop (n8n için) **ya da** M365 hesabınızda Copilot Studio erişimi; `week9/kullanim_senaryosu_sablonu.md`'yi okuyun; takımınızı kurun (1-3 kişi).
> **Lab teslimi:** doldurulmuş kullanım senaryosu özeti (kendi reponuza `docs/kullanim_senaryosu.md`) + prototip ekran görüntüsü. README: `week9/README.md`.

## Hafta 10 — Kariyer, portfolyo, 3 dakikalık sunumlar

> 🎤 **Hafta 10:** Portfolyo rötuşu + her takım final projesi **fikrini** 3 dakikada sunuyor (problem → çözüm → ölçüm → risk; `week10/sunum_sablonu.md`). Kronometre 3:00.
> **Dersten önce:** portfolyo/proje reponuz **public**; `python week10/portfolyo_kontrol.py <repo>` ile puanınızı ölçün; sunum için slayt zorunlu değil.
> **Teslim:** önce/sonra puan ekran görüntüsü + 5 CV maddesi; sunum. Hoca her takıma 2 satır yazılı not verecek; kapsam Hafta 11'de kesinleşir.

## Hafta 11 — Proje atölyesi

> 🧭 **Hafta 11 atölye:** demo yok; takımlar çalışır, masa masa onay. Masaya geldiğimde hazır olsun: kullanım senaryosu özeti, eval planı (kaç vaka, nereden, ilk 5 vaka yazılı), tek model çağrısıyla uçtan uca çalışan en küçük sürüm (yerelde), görev dağılımı, plan B. Liste: `week11/README.md`.
> Proje anahtarlarınız (takım başına) bu hafta özel mesajla.
> **Ara teslim Hafta 12:** yayında URL + ≥10 eval vakası + README iskeleti + `.env.example`; linki bu kanala.

## Hafta 12 — Ara teslim + red team + prova

> ⏱️ **Ara teslim bugün:** repo linki + canlı URL'yi bu mesajın altına yazın. Notlandırılmaz ama zorunlu; geri bildirim 3 gün içinde. `.env` repoda **olmasın**; `python week10/portfolyo_kontrol.py <repo>` ≥ 6/10 hedef.

### Aynı hafta: red team eşleşmesi + prova

> 🛡️ **Red team eşleşmesi:** `<Takım A ↔ Takım B, …>`. Kurallar: `week8/guvenlik/kirmizi_takim_kontrol_listesi.md` — yalnızca eşinizin sistemine, yalnızca ders kapsamındaki saldırı seti + kendi 2 saldırınız, veri silme/dolum yok, bulgular **tablo** olarak (cevap metinleri değil). Rapor: sunumdan önceki çarşamba (23 Aralık) akşamına kadar eşinize ve bu kanala (gizli bilgi yoksa). Kırılan her saldırı eval setinize vaka olur.
> **Prova:** derste kronometreyle 3 dk; `week10/sunum_rubrigi.md` ile akran geri bildirimi.

## Hafta 13 — Sunum günü

> 🎓 **Sunum günü 25 Aralık:** sıra `<liste>`; takım başına 3 dk sunum + 2 dk soru-cevap + 1 dk geçiş. Repo + demo URL'sini sabah bu kanala atın; demo videosu yerelde olsun (ağ bağımsız). `TESLIM.md` son hali repoda; soru-cevaptan sonra 48 saat düzeltme hakkı. Akran değerlendirme formu derste. Akış: `week11/sunum_gunu_akisi.md`.

## Final hatırlatması

> 📚 **Final `<tarih>`:** %40, senaryo ağırlıklı, Hafta 1-10'un tamamı. Çalışma haritası ve 10 örnek senaryo: `week11/final_konu_haritasi.md`. Her haftanın "Bu haftanın sorusu" ve "Başarı kriterleri" bölümlerini cevaplayabiliyor musunuz? Lab çıktılarınıza bakın: tablolar ne diyordu, siz ne değiştirdiniz?
