# Hafta 5 · RAG ve vektör veritabanları

> **Lab:** Türkçe bir derlem üzerinde RAG kurmak ve RAGAS tarzı ölçmek
> **Vize haftası:** vize 1-4. haftaları kapsar (token/bağlam, prompt ve tipli çıktı, bulut katmanları, maliyet kaldıraçları).
> **Bu haftanın sorusu:** Model kendi verinizi nasıl "bilir" ve bunu *ölçülebilir* biçimde nasıl yaparsınız?

Hafta 1'deki başarısızlık listesinin ikinci maddesi: *"Yanlış veri: bayat ya da indekslenmemiş belgeler üzerinde RAG."* Bilgi yönetimi asistanları şirketlerde en çok ölçeklenen ajan kullanım senaryosu. Bu hafta bir çalışan el kitabını (kurgusal **Kampüs Teknoloji A.Ş.**, 8 belge) indeksleyip soru cevaplıyoruz ve en önemlisi: **ölçüyoruz.**

## Ders akışı (90 dk)

| Süre | Bölüm |
|---|---|
| 35 dk | Teori: gömme, parçalama, vektör DB'ler (Qdrant, pgvector, Azure AI Search), hibrit arama, RAG hattı, RAGAS metrikleri |
| 15 dk | **Canlı demo** |
| 20 dk | **Lab** |
| 10 dk | Quiz + vize hatırlatması |

## Kavramlar (5 dakikada)

```
 belgeler ──parçala──▶ parçalar ──göm──▶ vektörler ──▶ Qdrant (vektör indeksi)
                         │                                  ▲
                         └──tokenle──▶ BM25 (anahtar kelime) │
 soru ──göm──▶ vektör ───────────── benzerlik araması ───────┘
 soru ──tokenle──▶ BM25 araması
                        ▼  RRF ile birleştir (hibrit)
                  en iyi k parça ──▶ prompt (bağlam + soru) ──▶ model ──▶ kaynak numaralı cevap
                                                                              │
                                              RAGAS tarzı hakem: sadakat · ilgililik · bağlam kalitesi
```

- **Gömme (embedding):** metni anlam taşıyan bir vektöre çevirir; benzer anlam → yakın vektör. `parola` ≈ `şifre`.
- **Parçalama (chunking):** sabit pencere / paragraf / cümle. Küçük parça kesin ama bağlamsız, büyük parça bağlamlı ama gürültülü.
- **Vektör veritabanı:** milyonlarca vektörde yaklaşık en yakın komşu (ANN, HNSW). Burada Qdrant bellek içi; Docker ile aynı kodla sunucuya geçer.
- **Hibrit arama:** vektör anlamı, BM25 tam kelimeyi/sayıyı yakalar ("14 gün", "SLA"). Reciprocal Rank Fusion ile birleşir.
- **Türkçe:** sondan eklemeli dil → tokenleme ve gömme modeli seçimi önemli. Çok dilli modeller (gemini-embedding, bge-m3, multilingual-e5) Türkçe'de iyi; İngilizce-only modeller kötü.
- **RAGAS metrikleri:** *faithfulness* (cevap bağlama sadık mı), *answer relevancy* (soruya odaklı mı), *context precision/recall* (doğru parçalar geldi mi). Hakem = başka bir LLM çağrısı.

## Klasördekiler

| Dosya | Ne işe yarar |
|---|---|
| `derlem/*.md` | 8 belgelik kurgusal çalışan el kitabı (izin, uzaktan çalışma, seyahat, güvenlik, işe alım, eğitim, BT, etik) |
| `sorular.json` | 13 soru + gerçek cevap + kaynak belge; sonuncusu tuzak (el kitabında olmayan bilgi) |
| `rag.py` | Tüm RAG parçaları: tokenleme, parçalama, gömme, Qdrant+BM25 indeks, hibrit getirme, cevaplama, hakem JSON |
| `gomme_demo.py` | 8 cümlenin benzerlik matrisi — gömme sezgisi |
| `parcala.py` | Üç parçalama yöntemini derlem üzerinde karşılaştır |
| `indeksle.py` | Derlemi parçala, göm, `indeks.pkl` olarak kaydet (Qdrant sunucu seçeneğiyle) |
| `sor.py` | Soru sor: getirilen parçalar + kaynak numaralı cevap; yöntem seçilebilir |
| `degerlendir.py` | 13 soru üzerinde RAGAS tarzı metrik tablosu |

Kurulum:

```bash
pip install -r week5/requirements.txt
# .env: LLM_* (Hafta 4) + EMBED_MODEL. Gemini: gemini-embedding-001 · Ollama: ollama pull bge-m3 ve EMBED_BASE_URL=http://localhost:11434/v1
cd week5
```

## Canlı demo (hoca · 15 dk)

1. **Gömme sezgisi (3 dk).** `python gomme_demo.py` → c3 (parola) ile c4 (şifre) ortak kelime içermiyor ama benzerlik yüksek. BM25 bunu bulamaz. Docker cümlesi herkesten uzak.
2. **Parçalama (2 dk).** `python parcala.py` → aynı derlem, üç farklı parça sayısı. `python parcala.py --yontem sabit --belge 01_izin_politikasi.md` ile cümlenin ortadan bölündüğünü göster.
3. **İndeksle ve sor (5 dk).**
   ```bash
   python indeksle.py
   python sor.py "Şifre kuralı ne?" --yontem bm25 --goster     # 'şifre' kelimesi derlemde yok → zayıf
   python sor.py "Şifre kuralı ne?" --yontem vektor --goster   # 'parola' parçasını bulur
   python sor.py "Laptopum açılmıyor, kaç saatte çözülür?" --yontem hibrit
   python sor.py "Şirketin cirosu ne kadar?"                   # doğru davranış: 'Bu bilgi el kitabında yok.'
   ```
4. **Ölç (5 dk).** `python degerlendir.py --sinir 6` → tabloyu oku: kaynak isabeti düşükse getirme sorunu, sadakat düşükse üretim sorunu. Vurgu: Hafta 1'deki sigorta vakasında 200 dosyalık eval seti tam olarak buydu.

> **Ağ çökerse:** sahte sunucu gömme de üretir (`EMBED_MODEL=sahte-embedding`); kelime örtüşmesine dayalıdır, demo akışı aynen çalışır ama hakem puanları anlamsızdır.

## Lab (öğrenci · 20 dk)

**Hedef:** Aynı derlem, iki farklı kurulum; hangisi daha iyi ölçüyor?

1. **Kur ve sor (5 dk).** `python indeksle.py` → `python sor.py "Babalık izni kaç gün?" --goster`. Cevaptaki kaynak numaraları doğru parçaya işaret ediyor mu?
2. **Yöntem karşılaştır (5 dk).** Aynı soruyu `--yontem bm25`, `--yontem vektor`, `--yontem hibrit` ile sor. Hangi sorularda BM25 kazanıyor (sayılar, özel adlar), hangilerinde vektör (eş anlamlılar)?
3. **İki indeks, iki tablo (8 dk).**
   ```bash
   python indeksle.py --yontem sabit --boyut 300 --cikti indeks_sabit.pkl
   python degerlendir.py --indeks indeks.pkl       --yontem hibrit
   python degerlendir.py --indeks indeks_sabit.pkl --yontem hibrit
   ```
   Hangi parçalama daha yüksek kaynak isabeti ve sadakat veriyor? Girdi token farkı ne (maliyet!)?
4. **Tuzak soruyu kontrol et (2 dk).** "Ciro" sorusunda model "el kitabında yok" dedi mi, yoksa uydurdu mu? Uydurduysa `rag.py` içindeki `CEVAP_SISTEM` metnini sertleştir ve tekrar dene.
5. **Teslim.** İki değerlendirme tablosunun ekran görüntüsü + bir cümle: "Hangi kurulum, neden?"

**Başarı kriterleri**
- [ ] `sor.py` kaynak numaralı cevap veriyor ve numaralar doğru parçayı gösteriyor
- [ ] İki farklı indeks için `degerlendir.py` tablosu alındı ve fark bir cümleyle açıklandı
- [ ] Tuzak soruda model uydurmuyor
- [ ] Hangi metrik getirme, hangisi üretim sorununu gösterir söyleyebiliyorsun

## Daha ileri (isteğe bağlı)

- **Gerçek RAGAS:** `pip install ragas` → `faithfulness`, `answer_relevancy`, `context_precision` metriklerini aynı `sorular.json` ile çalıştırın; `degerlendir.py --json` çıktısı RAGAS'ın beklediği `question / answer / contexts / ground_truth` alanlarına kolayca eşlenir. Belgeler: docs.ragas.io
- **Qdrant sunucu:** `docker run -p 6333:6333 qdrant/qdrant` → `python indeksle.py --qdrant-url http://localhost:6333`; panel: http://localhost:6333/dashboard
- **Türkçe kök bulma:** `rag.tokenle` içindeki 6 harf kırpmayı `zeyrek` ya da `snowballstemmer` ("turkish") ile değiştirip BM25 farkını ölçün.
- **Yeniden sıralama (re-ranking):** hibrit sonrası bir cross-encoder (bge-reranker-v2-m3) ekleyin; kaynak isabeti nasıl değişiyor?

## Sık karşılaşılan sorunlar

| Belirti | Çözüm |
|---|---|
| `embeddings` çağrısı 404 | `EMBED_MODEL` sağlayıcıda yok. Gemini: `gemini-embedding-001`; Ollama: `ollama pull bge-m3` ve `EMBED_BASE_URL=http://localhost:11434/v1` |
| `indeks.pkl yok` | Önce `python indeksle.py` |
| Hakem JSON hatası / boş tablo | Bazı modeller `response_format` desteklemez; `json_iste` düz metinden JSON çeker. Küçük yerel modeller şemayı bozabilir → `--hakem-model` olarak daha güçlü bir model verin |
| Hepsi 'el kitabında yok' | Getirme boş dönüyor: `--sadece-getir --goster` ile parçaları kontrol et; gömme modeli Türkçe'yi anlamıyor olabilir |
| Vektör boyutu uyuşmazlığı | İndeks başka bir gömme modeliyle kurulmuş; `indeksle.py` ile yeniden kur |

## Gelecek hafta

**Hafta 6 — Vibe coding I:** ajan tabanlı kodlama araçlarıyla spec'ten uygulamaya 40 dakikada. Dersten önce: Copilot Free'nin VS Code'da açık olduğundan emin olun, Zed Pro öğrenci lisansınızı alın.

## Kaynaklar

- RAGAS belgeleri (metrik tanımları) · Qdrant "Hybrid search" rehberi · Anthropic "Contextual Retrieval" yazısı
- MTEB liderlik tablosu (çok dilli gömme modelleri; Türkçe sütunu)
- Microsoft Learn: *Azure AI Search — hybrid search* (kurumsal RAG'da Qdrant'ın karşılığı)
