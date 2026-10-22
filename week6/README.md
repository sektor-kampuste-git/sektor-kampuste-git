# Hafta 6 · Vibe coding I: ajan tabanlı kodlama araçları

> **Lab (40 dk):** bir spec'ten çalışan ve yayınlanmış bir uygulamaya
> **Bu haftanın sorusu:** Kodu ajan yazıyorsa mühendisin işi ne? (Cevap: spec, kısıt, test, inceleme.)

Hafta 1'deki beş beceriden "ajan mühendisliği"nin ilk yarısı. Harcamaya göre en büyük kurumsal yapay zeka kategorisi kodlama; piyasa "Python biliyor"a değil, ajanla **doğrulanabilir** iş çıkarabilene ödüyor. Bu hafta araçları değil **döngüyü** öğreniyoruz: *plan → uygula → test → incele*. Araç pazarı altı ayda bir değişiyor (Cursor artık SpaceX'in, Gemini CLI emekli, Copilot öğrenci kayıtları durdu); döngü değişmiyor.

## Ders akışı (90 dk)

| Süre | Bölüm |
|---|---|
| 25 dk | Teori: ajan tabanlı IDE'ler nasıl çalışır (bağlam, araç çağrısı, diff), spec'in gücü, "çalışıyor" ≠ "doğru" |
| 15 dk | **Canlı demo**: hoca spec'ten uygulamaya |
| 40 dk | **Lab**: siz spec'ten uygulamaya |
| 10 dk | Üç quiz sorusu + gelecek hafta |

## Klasördekiler

| Dosya | Ne işe yarar |
|---|---|
| `SPEC_SABLONU.md` | Ajana "bitti" ne demek onu söyleyen tek sayfa: amaç, kabul kriterleri, kapsam dışı |
| `spec_ornekleri/` | Üç hazır spec: haber özetleyici · fiş bilgi çıkarıcı · ders notundan quiz |
| `AGENTS.md` | Ajan kuralları; projenizin köküne koyun (`.cursorrules` / `copilot-instructions.md` eşdeğeri) |
| `prompt_rehberi.md` | Plan / uygula / test / incele promptları + ajan raydan çıkınca ne yapmalı |
| `baslangic/` | Çalışan Streamlit iskeleti: `app.py` (arayüz) + `llm.py` (model katmanı) + 6 ağsız test + Dockerfile |
| `kontrol_listesi.md` | Teslim öncesi 10 madde (anahtar sızıntısı, sahte testler, kapsam kayması) |
| `deploy.md` | Streamlit Cloud · Container Apps · HF Spaces |

## Canlı demo (hoca · 15 dk)

Hazırlık (ders öncesi): `baslangic/` kopyalanmış, `.env` dolu, `streamlit run app.py` çalışıyor, `pytest -q` 6 test yeşil, ajan aracı açık.

1. **Sıfır noktası (2 dk).** Uygulamayı göster: 4 görev, token/maliyet metrikleri. "Bu kadarı 60 satır; spec'imiz bundan fazlasını istiyor."
2. **Spec'i oku (2 dk).** `spec_ornekleri/01_haber_ozetleyici.md` → K4 "doğrulama tablosu" maddesine dikkat: ajan bunu kendiliğinden yapmaz.
3. **Plan promptu (3 dk).** `prompt_rehberi.md` §1'deki promptu yapıştır. Planı sınıfla birlikte oku; kapsam dışına taşan bir madde varsa sil. "Bu iki dakika, sonraki otuzu kurtarır."
4. **Uygula + test (5 dk).** İlk 3 maddeyi uygulat. Diff'i ekranda oku: `llm.py`'de `st.*` var mı? Test gerçekten bir şey ölçüyor mu? `pytest -q`.
5. **İncele + yayınla (3 dk).** İnceleme promptunu *başka* bir sohbette çalıştır; bir bulguyu düzelt. Streamlit Cloud'a push → URL. (Dersten önce bir kez yayınlanmış olsun; canlıda yalnızca yeniden deploy.)

> **Ağ çökerse:** sahte sunucu ile uygulama aynen çalışır; ajan aracı ise bulut gerektirir. Yedek: önceden kaydedilmiş ekran görüntüleri / video.

## Lab (öğrenci · 40 dk)

**Hedef:** Üç spec'ten birini seçip, ajanla, testli ve yayınlanmış bir uygulama çıkarmak.

| Dakika | Adım |
|---|---|
| 0-5 | `baslangic/` klasörünü kendi reponuza kopyalayın. Seçtiğiniz spec'i `SPEC.md`, `AGENTS.md`'yi olduğu gibi köke koyun. `pytest -q` yeşil, `streamlit run app.py` açılıyor → **sıfır noktası commit'i**. |
| 5-10 | **Plan promptu.** Planı okuyun, kapsam dışına kaçanı silin. Onay verin. |
| 10-25 | **Uygula.** Üçer madde. Her turda diff okuyun, `pytest -q`. Testleri silen/`skip` eden ajanı durdurun. |
| 25-30 | **İnceleme promptu** (başka oturum). En az bir bulguyu düzeltin. |
| 30-37 | **Yayın.** `deploy.md` → Streamlit Cloud (Secrets!). URL'i açın, bir örnek çalıştırın. |
| 37-40 | **README "AI kullanımı"** bölümünü doldurun. `kontrol_listesi.md`'yi işaretleyin. Commit + push. |

**Teslim:** repo linki + yayın URL'i + `pytest -q` ekran görüntüsü sınıf kanalına.

**Başarı kriterleri**
- [ ] SPEC'teki kabul kriterlerinin en az %70'i karşılandı ve her biri için test ya da elle doğrulama notu var
- [ ] `pytest -q` yeşil; en az 8 test; hiçbiri ağ gerektirmiyor
- [ ] Uygulama bir URL'de çalışıyor; anahtar hiçbir dosyada/ekran görüntüsünde yok
- [ ] README "AI kullanımı": araç, promptlar, ajanın en az bir hatası ve sizin düzeltmeniz
- [ ] Kapsam dışı hiçbir özellik eklenmedi

## Araç seçimi (Ekim 2026, hepsi öğrenciye ücretsiz)

| Araç | Durum | Not |
|---|---|---|
| GitHub Copilot Free (VS Code, agent modu) | 2.000 tamamlama + 50 sohbet/ay | Öğrenci kayıtları durdu; Free yeterli. 50 sohbeti plan/inceleme için saklayın |
| Zed Pro | Öğrencilere 1 yıl ücretsiz | Hafif, hızlı; `AGENTS.md` okur |
| Cursor Hobby | Ücretsiz katman sınırlı | `.cursorrules` = AGENTS.md |
| Antigravity CLI / Claude Code | Terminal ajanları | Plan modu; repo kökünde başlatın |
| Codespaces | 180 çekirdek-saat/ay | Tarayıcıda VS Code + Copilot; Ollama çalışmaz |

Kural: aynı spec'i iki araçla deneyen öğrenci bonus alır — farkı 3 cümleyle yazın.

## Sık karşılaşılan sorunlar

| Belirti | Çözüm |
|---|---|
| Ajan `requirements.txt`'ye 15 paket ekledi | Geri alın; "mevcut bağımlılıklarla çöz". Streamlit Cloud ağır paketlerde zaman aşımına düşer |
| `ModuleNotFoundError: llm` testlerde | Testleri `baslangic/` (uygulama) klasöründen çalıştırın: `cd baslangic && pytest -q` |
| Streamlit Cloud'da "secrets" hatası | Settings → Secrets'a TOML biçiminde yapıştırın; tırnaklar şart |
| Ajan modeli koda sabitledi | `LLM_MODEL` ortam değişkeni; AGENTS.md'yi hatırlatın |
| Uygulama çalışıyor ama testler yok | "Çalışıyor" değil "doğrulandı" teslim edilir; her kabul kriterine test |

## Gelecek hafta

**Hafta 7 — Ajanlar, MCP ve A2A:** bu hafta ajan *sizin* kodunuzu yazdı; gelecek hafta *siz* ajan yazacaksınız: araç çağrısı döngüsü, bütçe ve durma koşulları, kendi MCP sunucunuz.
