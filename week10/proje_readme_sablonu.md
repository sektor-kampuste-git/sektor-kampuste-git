# <Proje adı>

> Bir cümle: kim için, neyi, nasıl. Örn: "Küçük işletmeler için fiş metninden tipli muhasebe kaydı çıkaran, Streamlit arayüzlü, eval'li bir asistan."

**Canlı demo:** <URL> · **Video (2 dk):** <URL> · **Durum:** prototip / pilot

## Problem ve kullanıcı
Kim bu işi ne sıklıkla yapıyor; bugün ne kadar sürüyor; neden yapay zeka (ve neden kural tabanlı değil).

## Mimari
```
kullanıcı → Streamlit → llm.py (OpenAI uyumlu istemci) → <model/sağlayıcı>
                      ↘ RAG (Qdrant) / araçlar (MCP) / bütçe
```
- Model kademesi ve neden; sağlayıcıdan bağımsızlık; önbellek kullanımı
- Bütçe ve durma koşulları (ajan varsa)

## Kurulum ve çalıştırma
```bash
pip install -r requirements.txt
cp .env.example .env    # anahtarlar
streamlit run app.py
pytest -q
```

## Değerlendirme
| Metrik | Değer | Nasıl ölçüldü |
|---|---|---|
| Eval geçme oranı | 14/15 | `eval_calistir.py`, CI'da |
| Sadakat (RAG) | 0.93 | `degerlendir.py`, 13 soru |
| Red team | 10/12 dayandı | `kirmizi_takim.py` |
Neyi ölçmediğinizi de yazın.

## Maliyet
İstek başına ve aylık tahmin (`maliyet_hesapla.py` / `roi_hesapla.py` çıktısı); hangi kaldıraçlar kullanıldı.

## Güvenlik ve yönetişim
Injection önlemleri, yetki kısıtları, insan onayı noktası, risk sınıfı, kişisel veri varsa KVKK notu. Bilinen sınırlar.

## AI kullanımı
Hangi araçlar, hangi işler için; ajanın en az bir hatası ve düzeltmeniz; hangi testler elle yazıldı. (Ders kuralı; şeffaflık olumlu puandır.)

## Yol haritası / bilinen eksikler
3 madde.

## Lisans
MIT (ya da seçtiğiniz).
