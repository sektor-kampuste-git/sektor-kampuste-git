# Son kontrol listesi — teslimden 1 gün önce (15 dk)

## Repo
- [ ] Public; `python week10/portfolyo_kontrol.py <repo>` ≥ 8/10
- [ ] `git log -p | grep -iE "sk-|AIza|api_key\s*=" ` boş; `.env` yok, `.env.example` var
- [ ] `pip install -r requirements.txt && pytest -q` temiz bir sanal ortamda yeşil (arkadaşınızın makinesinde deneyin)
- [ ] README: demo URL, video, kurulum, mimari, eval tablosu, maliyet, güvenlik/yönetişim, AI kullanımı, lisans
- [ ] `TESLIM.md` (proje_teslim_sablonu) doldurulmuş; kanıt dosya yolları tıklanıyor
- [ ] `docs/kullanim_senaryosu.md` ve `docs/model_karti.md` var

## Ürün
- [ ] Canlı URL açılıyor (Streamlit Cloud uyuduysa bir kez açıp uyandırın)
- [ ] Boş girdi, çok uzun girdi, alakasız girdi → anlaşılır mesaj, çökme yok
- [ ] Anahtar yoksa / model 500 verirse kullanıcı dostu hata
- [ ] Token, süre ve maliyet ekranda (ya da logda)

## Ölçüm
- [ ] Eval koşucusu son commit'te çalıştırıldı, sonuç README'deki sayıyla aynı
- [ ] Red team tablosu güncel; kırılan saldırı eval'e eklenmiş
- [ ] "Ne bozuldu" bölümü yazılmış

## Yönetişim
- [ ] Risk sınıfı ve gerekçe · insan onayı noktası · KVKK notu · bilinen sınırlar
- [ ] Kişisel veri içeren örnekler anonimleştirilmiş (gerçek isim/TCKN/telefon yok)

## Sunum
- [ ] Demo videosu ≤45 sn, çalışıyor, ses gerekmiyor
- [ ] 6 slayt ya da sıfır slayt; sayılar büyük
- [ ] Kronometreyle 2 prova; soru-cevap hazır cevapları (`week10/sunum_sablonu.md`)
- [ ] Yedek: ağ yoksa ekran görüntüleri klasörü

## Bulut hijyeni
- [ ] Container Apps `--min-replicas 0`; kullanılmayan kaynak grupları silindi
- [ ] Azure for Students kredisi kontrol edildi; alarm kurulu (Cost Management → Budgets)
