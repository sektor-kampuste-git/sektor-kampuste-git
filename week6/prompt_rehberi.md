# Prompt rehberi — ajanla 40 dakikada spec'ten uygulamaya

Vibe coding "ne çıkarsa kabul et" değildir. Döngü şu: **plan → uygula → test → incele**. Her adımın promptu farklı.

## 0. Hazırlık (ders öncesi, 5 dk)
- `week6/baslangic/` klasörünü kendi reponuza kopyalayın, `SPEC.md` ve `AGENTS.md` ekleyin
- `.env` hazır, `streamlit run app.py` çalışıyor, `pytest -q` yeşil (6 test) — **sıfır noktası**
- Aracınız açık: VS Code + Copilot (agent modu) · Zed (Agent panel) · Cursor · Antigravity CLI · Claude Code

## 1. Plan promptu (ajan kod yazmaz)
```
SPEC.md ve AGENTS.md dosyalarını oku. Mevcut app.py, llm.py ve tests/ dosyalarını incele.
Kabul kriterlerini (K1..Kn) karşılamak için yapacağın değişiklikleri dosya dosya, 5-8 madde halinde listele.
Hangi kriter için hangi testi yazacağını belirt. Henüz kod yazma; planı onaylayacağım.
```
Planı okuyun. Kapsam dışına kaçan madde varsa silin. **Bu 2 dakika sonraki 30 dakikayı kurtarır.**

## 2. Uygulama promptu (küçük parçalar)
```
Plandaki 1-3. maddeleri uygula. llm.py'ye yeni görev eklerken GOREVLER sözlüğünü kullan, st.* ekleme.
Her değişiklik için ilgili testi tests/ altına yaz. Bitince pytest -q çalıştır ve çıktıyı göster.
```
Üçer madde ilerleyin. Ajan "hepsini yaptım" derse bile diff'i okuyun.

## 3. Test promptu
```
SPEC.md'deki K2 kriterini (özet en fazla 3 cümle) doğrulayan bir test yaz. Model çağrısını patch ile taklit et;
modelin 5 cümlelik yanıt verdiği durumda uygulamanın ne yaptığını da test et.
```
Ajanın ürettiği testlerin gerçekten bir şey test ettiğini kontrol edin: `assert True` tuzağı.

## 4. İnceleme promptu (başka bir oturumda / başka bir araçta)
```
Bu diff'i gözden geçir: güvenlik (anahtar sızıntısı, kullanıcı girdisini doğrudan prompt'a yapıştırma),
hata yönetimi (model 500 dönerse?), ve SPEC.md kapsam dışı ihlalleri. Sorunları önem sırasına göre listele; düzeltme yapma.
```
İnceleyen ajan ≠ yazan ajan daha iyi sonuç verir.

## 5. Yayın promptu
```
Bu Streamlit uygulamasını Streamlit Community Cloud'a yayınlamak için gereken adımları ve Secrets biçimini yaz.
requirements.txt'nin eksiksiz olduğunu kontrol et (pip freeze değil, yalnızca doğrudan bağımlılıklar).
```

## Ajan raydan çıkarsa
| Belirti | Müdahale |
|---|---|
| Yeni kütüphane kuruyor | "Bağımlılık ekleme, mevcut araçlarla çöz" — AGENTS.md'yi hatırlat |
| Testi geçiremeyince testi değiştiriyor | Diff'i geri al; "Testi değil kodu düzelt" |
| 300 satırlık tek dosya yazıyor | "app.py / llm.py ayrımını koru; st.* llm.py'de olmaz" |
| Anahtarı koda yazıyor | Anında geri al; anahtarı yenile (artık sızmış sayılır) |
| Kapsam dışı özellik ekliyor | "SPEC.md §4'e bak; bunu sil" |
| Aynı hatayı 3. kez deniyor | Durdur, hatayı siz okuyun, ipucunu siz verin |

## Araçlara göre notlar (Ekim 2026)
- **GitHub Copilot Free:** ayda 2.000 tamamlama + 50 sohbet. Agent modunu VS Code'da Copilot Chat → "Agent" ile açın. 50 sohbeti plan ve inceleme için saklayın; tamamlamayı küçük işlerde kullanın.
- **Zed Pro (öğrenci, 1 yıl ücretsiz):** Agent panel; `AGENTS.md`'yi otomatik okur. Hızlı ve hafif.
- **Cursor Hobby:** ücretsiz katman sınırlı; `.cursorrules` = AGENTS.md içeriği.
- **Antigravity CLI / Claude Code:** terminalde çalışır; repo kökünde başlatın, `AGENTS.md`/`CLAUDE.md` okur. Plan modunu kullanın.
- **Codespaces:** 180 çekirdek-saat/ay; Ollama çalışmaz, bulut modeli kullanın.
Araç pazarı hızlı değişiyor (Cursor artık SpaceX'in, Gemini CLI emekli). Araca değil **döngüye** alışın.
