# Kontrol listesi — teslim öncesi 10 madde

Ajanla yazılan her uygulama için. Birini bile atlarsanız, ürün "çalışıyor gibi" görünür ama canlıda patlar.

## Güvenlik
- [ ] 1. `git log -p | grep -i "api_key\|sk-\|AIza"` boş dönüyor; anahtar hiçbir commit'te yok (`.env` gitignore'da)
- [ ] 2. Kullanıcı metni prompt'a **içerik** olarak giriyor, talimat olarak değil (sistem mesajı ayrı; Hafta 8'de prompt injection)
- [ ] 3. Hata mesajlarında traceback, endpoint ya da anahtar parçası görünmüyor

## Doğruluk
- [ ] 4. `pytest -q` yeşil ve testler gerçekten bir şey ölçüyor (`assert True` yok)
- [ ] 5. SPEC'teki her kabul kriterinin karşısında bir test ya da elle doğrulama notu var
- [ ] 6. 5 örnek girdiyle elle denendi; en az biri "kötü" girdi (boş, çok uzun, alakasız)

## Kapsam ve kalite
- [ ] 7. SPEC §4 kapsam dışı maddelerden hiçbiri "bonus" olarak eklenmedi
- [ ] 8. `app.py` içinde model çağrısı yok, `llm.py` içinde `st.*` yok
- [ ] 9. `requirements.txt` yalnızca doğrudan bağımlılıkları içeriyor ve sürümlü

## Şeffaflık
- [ ] 10. README "AI kullanımı" bölümü dolu: araç, promptlar, ajanın hatası ve sizin düzeltmeniz

## Yayın kontrolü
- [ ] URL açılıyor, bir örnek çalışıyor, Secrets doğru (ekran görüntüsünde anahtar yok)
- [ ] Kullanılmayan kaynaklar kapatıldı (Container Apps'te `--min-replicas 0`; Azure'da kaynak grubu silindi)
