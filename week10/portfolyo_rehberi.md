# Portfolyo rehberi: beş beceri, beş kanıt, beş CV maddesi

Hafta 1'deki tez: *"İşverenlerin aradığı beş beceri 2023'te bir iş unvanı değildi."* Aralık ayına kadar her birini **bir GitHub bağlantısıyla** kanıtlayabilmelisiniz. Portfolyo = iddia değil, kanıt.

| Beceri | Hangi hafta | Repoda ne olmalı (kanıt) | CV'de nasıl görünür |
|---|---|---|---|
| **Ajan mühendisliği** | 6-7 | `ajan_dongusu.py` türevi: araç çağrısı, **bütçe ve durma koşulu**, iz çıktısı; AGENTS.md + spec ile ajanla geliştirilmiş uygulama | "Bütçe ve durma koşullu, araç çağıran bir destek ajanı tasarladım (4 araç, adım/USD tavanı, JSONL iz)" |
| **Değerlendirme** | 5, 8 | `evaller.json` (≥15 vaka), `eval_calistir.py` / promptfoo raporu, CI'da eval, RAG için RAGAS tarzı tablo | "15 vakalık eval setiyle prompt v1→v3 geçişini CI'da ölçtüm: 6/15 → 14/15; RAG'da sadakat 0.71→0.93" |
| **Entegrasyon (MCP)** | 7 | `mcp_sunucu.py`: en az 3 araç + 1 kaynak; VS Code/Claude Desktop ekran görüntüsü; A2A notu | "Şirket içi sipariş/kargo API'lerini MCP sunucusu olarak ajanlara açtım (stdio, 4 araç)" |
| **Yapay zeka güvenliği** | 8 | `saldiri_seti.json` (kendi saldırılarınız dahil), red team raporu, v2/v3 prompt, `savunma.md` eşlemesi, canary | "10+2 saldırılık red team setiyle prompt injection testi; dolaylı injection'a karşı yetki kısıtı ve çıktı filtresi" |
| **Yönetişim** | 4, 9 | Kullanım senaryosu özeti (ROI + risk sınıfı + KVKK + insan onayı), model kartı, maliyet tablosu | "EU AI Act risk sınıflandırması ve KVKK kontrol listesiyle bir kullanım senaryosu özeti; ROI'de hata oranı duyarlılığı" |

## Portfolyo reposu nasıl görünmeli?
```
<ad>-ai-portfolio/
├── README.md              ← 1 paragraf kimsiniz + 5 beceri tablosu (yukarıdaki) + her satırda bağlantı
├── 01-ajan/               ← week7 türevi + kendi aracınız
├── 02-eval/               ← week8 eval seti, CI badge
├── 03-mcp/                ← MCP sunucusu + IDE ekran görüntüsü
├── 04-guvenlik/           ← red team raporu (tablo), savunma notu
├── 05-yonetisim/          ← kullanım senaryosu özeti, model kartı, ROI
└── proje/                 ← final projesi (ya da ayrı repo bağlantısı)
```
Tek bir final projesi beş beceriyi birden içerebilir; o zaman README'de her beceri için **dosya bağlantısı** verin. Okuyan kişi (işe alımcı, 90 saniye) tıklayıp kanıtı görmeli.

## Üç kural
1. **Her iddia bir dosyaya bağlanır.** "Eval yaptım" → `evaller.json` + rapor ekran görüntüsü.
2. **Sayı varsa yazılır.** 15 vaka, 14/15, $0.0004/istek, 2 adım bütçe. Sayısız madde iddia, sayılı madde kanıttır.
3. **AI kullanımı şeffaf.** README'de "AI kullanımı" bölümü (ders kuralı). İşe alımcılar bunu artık **olumlu** okur: aracı yönetebildiğinizi gösterir.

## 20 dakikalık rötuş (lab)
- `python portfolyo_kontrol.py <repo-url>` → 10 kontrol, puan ve öneriler
- Eksikleri kapat: README bölümleri, `.env.example`, testler, LICENSE, açıklama + topics
- `cv_maddeleri.md` ile 5 maddeyi yaz; `profil_kontrol_listesi.md` ile GitHub/LinkedIn'i düzelt
