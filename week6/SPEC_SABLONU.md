# SPEC — <Uygulama adı>

> Bir spec, ajana (ve size) "bitti" ne demek onu söyler. Ajan spec'siz çalışırsa sizin yerinize karar verir.
> Bu dosyayı projenizin köküne `SPEC.md` olarak koyun; ajan ilk promptta bunu okusun.

## 1. Amaç (bir cümle)
<Kim>, <neyi>, <neden> yapabilsin. Örn: "Öğrenci, uzun bir Türkçe haber metnini yapıştırıp 3 cümlelik özet ve 5 anahtar kelime alabilsin."

## 2. Kullanıcı ve bağlam
- Kim kullanacak: …
- Nerede çalışacak: tarayıcı (Streamlit) / terminal / API
- Veri nereden geliyor: kullanıcı yapıştırır / dosya yükler / URL

## 3. Kabul kriterleri (test edilebilir, numaralı)
Her madde "evet/hayır" ile cevaplanabilmeli. Ajan bunları test haline getirir.
- [ ] K1. Kullanıcı 20 karakterden kısa metin girerse uyarı görür, model çağrılmaz.
- [ ] K2. "Özetle" seçilince çıktı en fazla 3 cümledir.
- [ ] K3. Her sonucun altında girdi/çıktı token ve tahmini maliyet görünür.
- [ ] K4. API anahtarı koda yazılmaz; `.env` ya da Streamlit Secrets'tan okunur.
- [ ] K5. `pytest -q` yeşil; en az 5 test, hiçbiri ağ gerektirmez.
- [ ] K6. …

## 4. Kapsam dışı (ajan bunları YAPMAZ)
- Kullanıcı girişi / hesap sistemi
- Veritabanı
- Birden çok dil desteği
- …

## 5. Teknik kısıtlar
- Python 3.12, Streamlit, `openai` istemcisi (OpenAI uyumlu, sağlayıcıdan bağımsız)
- Model: `.env` içindeki `LLM_MODEL`; kodda model adı sabitlenmez
- Dosya yapısı: `app.py` (arayüz), `llm.py` (model katmanı, st.* yok), `tests/`
- Bağımlılık eklemek için önce sor

## 6. Arayüz taslağı
```
[Başlık]
Görev: ( ) Özetle  ( ) Anahtar kelimeler  ( ) Soru üret
[ metin alanı ..................... ]
[ Çalıştır ]
Sonuç: ...
girdi 812 tok · çıktı 96 tok · 1.2 sn · $0.00013
```

## 7. Değerlendirme (nasıl "iyi" olduğunu bileceğiz?)
- 5 örnek metinle elle deneme: `ornekler/` klasörü
- Çıktı uzunluğu ve uydurma kontrolü (metinde olmayan bilgi var mı?)

## 8. Yayın
- Streamlit Community Cloud (ücretsiz) · alternatif: Azure Container Apps (week4 betiği)

## 9. AI kullanımı (README'ye taşınacak)
- Hangi araç, hangi prompt'lar, ajanın hatası ve düzeltmesi
