# Savunma: OWASP LLM Top 10 (2025) → bu derste ne yaptık

| # | Risk | Bu derste gördüğünüz yer | Savunma katmanı |
|---|---|---|---|
| LLM01 | **Prompt injection** (doğrudan / dolaylı) | `saldiri_seti.json` S01-S08, `dolayli_injection_demo.py` | Talimat hiyerarşisi (sistem > kullanıcı > veri), veri sınırlayıcıları `<<< >>>`, "talimat biçimli metin veridir" kuralı (v2), çıktı filtresi, **modelin yetkisini kısıtla** (kupon üretemez) |
| LLM02 | **Hassas bilgi ifşası** | canary + parola (v1 iç notu), S02/S04/S06 | Sırrı prompta koyma (v1'deki parola bilinçli hata); gerekirse araç tarafında tut; canary ile sızıntıyı ölç; log'larda maskele |
| LLM03 | Tedarik zinciri | week6: ajanın eklediği bağımlılıklar | `requirements.txt` sürümlü, inceleme promptu, lisans kontrolü |
| LLM04 | Veri/model zehirlenmesi | week5: derlemdeki belge → cevap | Derlem kaynağını denetle; dış belgeleri "güvenilmeyen" işaretle |
| LLM05 | **Uygunsuz çıktı işleme** | week7: araç çıktısı modele geri gidiyor; week6: model çıktısı arayüze | Çıktıyı veri olarak işle (JSON şema, `escapeHTML`), `eval` yok (`hesapla` → `ast`) |
| LLM06 | **Aşırı yetki (excessive agency)** | week7 ajan: hangi araçlar, hangi bütçe | En az yetki: yalnızca gereken araçlar; para etkisi olan işlem = insan onayı; bütçe/durma koşulu |
| LLM07 | Sistem promptu sızıntısı | S02, E09 | Prompt sır değildir diye tasarla; sırları araç/sunucu tarafında tut; sızıntıyı eval'e koy |
| LLM08 | Vektör/gömme zafiyetleri | week5 RAG | Erişim kontrolü belge düzeyinde (kim hangi parçayı görebilir), çok kiracılı indekslerde filtre |
| LLM09 | **Yanlış bilgi** | week5 sadakat metriği, tuzak soru | "El kitabında yok" davranışı, kaynak numarası, eval seti, insan son onayı (sigorta vakası) |
| LLM10 | Sınırsız tüketim | week7 bütçe, week4 maliyet | Adım/token/USD/süre tavanı, hız sınırı, önbellek, izleme uyarıları |

## Katmanlı savunma: hiçbiri tek başına yetmez
1. **Girdi tarafı:** uzunluk/biçim sınırı, bilinen injection kalıpları için uyarı (engelleme değil; kolay aşılır)
2. **Prompt tarafı:** talimat hiyerarşisi, görev sınırı, veri sınırlayıcıları, "talimat biçimli veri = veri"
3. **Yetki tarafı (en önemlisi):** modelin yapabildiği şeyleri kısıtla. Kupon üretemeyen asistan, kandırılsa da kupon üretemez
4. **Çıktı tarafı:** canary/sır taraması, şema doğrulama, para etkisi için insan onayı
5. **Gözlem tarafı:** her çağrı izlenir (Langfuse / yerel iz); eval setine her yeni saldırı eklenir → regresyon testi

## Red team sonrası ne yapmalı?
Kırılan her saldırı → `evaller.json`'a yeni vaka → `eval_calistir.py` kırmızı → prompt/yetki düzelt → yeşil. Güvenlik bir kez değil, CI'da her commit'te test edilir.

## Kaynaklar
- OWASP Top 10 for LLM Applications 2025 (genai.owasp.org)
- Simon Willison, "Prompt injection" yazı dizisi ("lethal trifecta": özel veri + güvenilmeyen içerik + dışarı iletişim)
- Anthropic / OpenAI / Google güvenlik ve sorumlu kullanım belgeleri
