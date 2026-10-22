# Mülakat soruları: junior yapay zeka mühendisi / yapay zeka uygulama geliştirici (2026)

Her sorunun yanında bu dersteki karşılığı. Cevap verirken **kendi reponuzdaki örneğe** bağlayın: "Hafta 8'de şunu yaptım…" değil, "destek asistanımda şöyle oldu…".

## Teknik (15)
1. OpenAI uyumlu API ne demek, neden sağlayıcıdan bağımsız kod yazarsınız? *(Hafta 1, 4)*
2. Girdi ve çıktı tokenı fiyatı neden farklı; faturayı düşüren dört kaldıraç nedir? *(Hafta 4)*
3. Prompt caching ne zaman işe yarar, ne zaman yaramaz? *(Hafta 4)*
4. RAG'da parça boyutunu nasıl seçersiniz; küçük/büyük parçanın bedeli nedir? *(Hafta 5)*
5. Hibrit arama neden gerekir; BM25'in vektör aramaya göre güçlü olduğu bir örnek verin. *(Hafta 5)*
6. RAG'ı nasıl ölçersiniz; sadakat ile ilgililik farkı nedir; hangi metrik "getirme" sorununu gösterir? *(Hafta 5)*
7. Türkçe için gömme modeli seçerken neye bakarsınız? *(Hafta 5)*
8. Ajan döngüsü nasıl çalışır; durma koşulları ne olmalı; sonsuz döngüyü nasıl engellersiniz? *(Hafta 7)*
9. MCP nedir, hangi problemi çözer; A2A'dan farkı? *(Hafta 7)*
10. `eval` kullanan bir "hesapla" aracını neden kabul etmezsiniz? *(Hafta 7, 8)*
11. Prompt injection türleri; dolaylı injection'a karşı en etkili savunma hangi katmandadır? *(Hafta 8)*
12. "v2 promptu v1'den iyi" iddiasını nasıl kanıtlarsınız? CI'da eval ne demek? *(Hafta 8)*
13. LLM uygulamasında tracing neyi kaydeder; hangi alan maliyet denetimi için şart? *(Hafta 8)*
14. Yapılandırılmış çıktı (JSON şema) neden serbest metinden iyidir; model şemayı bozarsa? *(Hafta 3, 6)*
15. Açık ağırlıklı model ne zaman tercih edilir? Bir hastane örneği verin. *(Hafta 1)*

## Ürün ve iş (6)
16. Bir yapay zeka pilotunun ölmesinin en sık altı nedeni? Hangisini en çok gördünüz? *(Hafta 1, 9)*
17. ROI hesabında token maliyeti neden genelde en küçük kalemdir; asıl kalemler ne? *(Hafta 9)*
18. İnsan onayı noktasını nereye koyarsınız; "lastik damga" riski nedir? *(Hafta 9)*
19. EU AI Act'te yüksek riskli sayılan bir senaryo verin; yükümlülükler ne? *(Hafta 9)*
20. KVKK açısından bir LLM uygulamasında ilk üç kontrolünüz? *(Hafta 9)*
21. Kullanım senaryosu seçme kuralınız? *(Hafta 9)*

## Davranışsal (4)
22. Ajanın yazdığı kodda yakaladığınız bir hatayı anlatın; nasıl fark ettiniz? *(Hafta 6, README "AI kullanımı")*
23. Bir arkadaşınızın sistemini kırdığınız red team deneyimi; nasıl raporladınız? *(Hafta 8)*
24. Spec'i olmayan bir istekle ne yaparsınız? *(Hafta 6)*
25. Bu alan ayda bir değişiyor; neyi takip ediyorsunuz, nasıl öğreniyorsunuz? *(Hafta 1: artificialanalysis.ai, kaynak listeleri)*

## Mülakat formatları (Hafta 1 ve İK perspektifi)
- **Take-home (2-4 saat):** spec okuma, testli teslim, README "AI kullanımı" — Hafta 6 döngüsünün aynısı
- **Sistem tasarımı (45 dk):** "müşteri destek ajanı tasarla" → Hafta 7-9 çizimi: araçlar, bütçe, eval, insan onayı, iz
- **Canlı kodlama:** ajanla kodlamaya izin veren şirketler artıyor; döngüyü (plan→uygula→test→incele) sesli yürütün
- **Davranışsal:** STAR (durum, görev, eylem, sonuç) + sayı
