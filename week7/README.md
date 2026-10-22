# Hafta 7 · Ajanlar, MCP ve A2A

> **Lab:** kendi MCP sunucunuz + bütçeli bir ajan
> **Bu haftanın sorusu:** Model, dış dünyaya nasıl *güvenli* ve *sınırlı* dokunur?

Geçen hafta ajan sizin kodunuzu yazdı; bu hafta siz ajan yazıyorsunuz. Çerçeve yok: araç çağırma döngüsü ~150 satır Python. Üç fikir: **döngü** (model → araç → model), **bütçe** (adım/token/USD/süre tavanı ve durma koşulu), **protokol** (MCP: araçlarınızı her ajana açın; A2A: ajanlar birbirine). Hafta 1'deki beceri listesinden "ajan mühendisliği" ve "entegrasyon (MCP)"; başarısızlık listesinden "sınırsız maliyet".

## Ders akışı (90 dk)

| Süre | Bölüm |
|---|---|
| 35 dk | Teori: araç çağrısı nasıl çalışır (JSON şema → model → argümanlar), ReAct döngüsü, bütçe ve durma, MCP mimarisi (host/client/server, tools/resources/prompts, stdio vs HTTP), A2A |
| 15 dk | **Canlı demo** |
| 20 dk | **Lab** |
| 10 dk | Quiz + gelecek hafta |

## Klasördekiler

| Dosya | Ne işe yarar |
|---|---|
| `araclar_yerel.py` | Dört araç (sipariş, kargo, iade, hesapla) + sahte veri + OpenAI `tools` şeması |
| `ajan_dongusu.py` | Bütçeli ajan döngüsü; iz (trace) yazar; `--mcp` ile araçları MCP'den alır |
| `mcp_sunucu.py` | Aynı dört aracı + bir kaynağı MCP ile sunar (30 satır) |
| `mcp_istemci.py` | Sunucuya bağlan, araçları listele/çağır, kaynağı oku; ajan için köprü fonksiyonları |
| `ide_ayarlari/` | VS Code · Claude Desktop · Cursor için MCP yapılandırma örnekleri |
| `a2a_mini.py` | Planlayıcı + uzman ajan, Agent Card'lar, ayrı bütçelerle el değiştirme |
| `a2a_notu.md` | MCP ve A2A karşılaştırması, ne zaman hangisi, güvenlik notu |
| `izler/` | `--trace` çıktıları (JSONL, gitignore'da) |

Kurulum: `pip install -r week7/requirements.txt` (`mcp` 2.x). `.env` Hafta 4'teki gibi.

## Canlı demo (hoca · 15 dk)

1. **Döngüyü izle (4 dk).**
   ```bash
   python ajan_dongusu.py "SIP-1001 siparişim nerede? İade edebilir miyim?"
   ```
   İz satırlarını oku: MODEL → ARAÇ → SONUÇ → MODEL → CEVAP. Modelin araç *seçtiğini*, kodun araç *çalıştırdığını* vurgula. Soru: "hesapla aracı neden `eval` kullanmıyor?"
2. **Bütçeyi patlat (3 dk).**
   ```bash
   python ajan_dongusu.py "SIP-1002 iade var mı, %10 kesintiyle ne alırım?" --max-adim 1
   python ajan_dongusu.py "SIP-9999 nerede?" --max-usd 0.0001
   ```
   Ajan durur ve *neden* durduğunu söyler. "Canlıdaki ajanın en önemli özelliği durmayı bilmesidir."
3. **MCP: aynı araçlar, standart kapı (5 dk).**
   ```bash
   python mcp_istemci.py                          # araç listesi, şema, çağrı, kaynak
   python ajan_dongusu.py "TK-77 kargom nerede?" --mcp
   ```
   Sonra VS Code'da `.vscode/mcp.json` (bkz. `ide_ayarlari/`) → Copilot Agent modunda "SIP-1001 nerede?" sor: *aynı sunucu*, farklı istemci. (Dersten önce yolu düzenleyin.)
4. **A2A fikri (3 dk).** `python a2a_mini.py` → planlayıcı görevi uzmana devrediyor; iki ayrı bütçe. `a2a_notu.md` tablosunu göster: MCP = eller, A2A = meslektaşlar.

> **Ağ çökerse:** sahte sunucu araç çağrısını taklit eder (kullanıcı metnine en yakın aracı seçer, sonra cevap üretir). Döngü ve MCP akışı aynen çalışır; cevaplar anlamsızdır.

## Lab (öğrenci · 20 dk)

**Hedef:** MCP sunucunuza yeni bir araç ekleyip, bütçeli ajanın onu kullandığını izlemek.

1. **Çalıştır (3 dk).** `python mcp_istemci.py` ve `python ajan_dongusu.py "SIP-1003 ne zaman gelir?"`. İz çıktısını oku.
2. **Yeni araç (8 dk).** `araclar_yerel.py`'ye bir fonksiyon ekle — öneriler: `stok_sorgula(urun)`, `kupon_dogrula(kod)`, `teslimat_tahmini(il)`. Sahte veri yeter. Ardından:
   - `ARAC_TANIMLARI`'na şemasını ekle, `ARAC_FONKSIYONLARI`'na fonksiyonu ekle
   - `mcp_sunucu.py`'ye `@sunucu.tool()` ile aynı aracı ekle (docstring = modelin okuduğu açıklama; iyi yaz!)
   - `python mcp_istemci.py` → yeni araç listede mi?
3. **Ajanla dene (4 dk).** Yeni aracı gerektiren bir soru sor; hem yerel hem `--mcp` ile. `--trace izler/benim.jsonl` ile izi kaydet.
4. **Bütçe deneyi (3 dk).** Aynı soruyu `--max-adim 2` ve `--max-usd 0.0005` ile çalıştır. Hangi sınır önce vuruyor? Ajan düzgün durup açıkladı mı?
5. **Teslim.** `mcp_istemci.py` çıktısında yeni aracın göründüğü + ajanın yeni aracı çağırdığı iz satırının ekran görüntüsü. Bonus: VS Code / Claude Desktop'ta sunucunuzun çalıştığı ekran görüntüsü.

**Başarı kriterleri**
- [ ] Yeni araç hem yerel ajan hem MCP istemcisi tarafından görülüyor ve çağrılıyor
- [ ] Araç açıklaması (docstring) modelin doğru aracı seçmesine yetiyor
- [ ] Bütçe aşımında ajan duruyor ve sebebini söylüyor
- [ ] `hesapla` gibi "tehlikeli" bir aracın neden sınırlı yazıldığını açıklayabiliyorsun

## Sık karşılaşılan sorunlar

| Belirti | Çözüm |
|---|---|
| `ModuleNotFoundError: mcp.server.mcpserver` | `mcp` 1.x kurulu; `pip install "mcp>=2,<3"`. (1.x'te sınıf adı `FastMCP` idi.) |
| Model araç çağırmıyor, düz cevap veriyor | Küçük yerel modellerin araç desteği zayıf; Foundry/Gemini kullanın. Araç açıklamasını netleştirin |
| Araç argümanları yanlış (`siparis_no` yerine `order_id`) | Şemadaki `description`'a örnek ekleyin; `required` listesini kontrol edin |
| `--mcp` takılıyor | Sunucu stdout'a `print` yapıyorsa protokol bozulur; MCP sunucusunda log için `stderr` kullanın |
| VS Code sunucuyu görmüyor | `mcp.json` içindeki `command` sanal ortamdaki python'a işaret etsin; VS Code'u yeniden başlatın |
| Ajan aynı aracı tekrar tekrar çağırıyor | Sistem promptundaki "tekrar çağırma" kuralı + `--max-adim`. Canlıda: aynı (araç, argüman) çiftini ikinci kez görünce dur |

## Gelecek hafta

**Hafta 8 — Canlı ortam:** bu ajanı izlemek (tracing), 15 eval ile CI'da test etmek ve arkadaşınızın ajanına saldırmak (prompt injection). `--trace` ile bugün kaydettiğiniz izleri saklayın.

## Kaynaklar

- modelcontextprotocol.io — spesifikasyon, Python SDK (`mcp`), örnek sunucular
- a2a-protocol.org — Agent Card ve task yaşam döngüsü
- OpenAI / Anthropic / Gemini "function calling" belgeleri (aynı JSON şema fikri)
- Anthropic, *Building effective agents* (döngü ve durma koşulları üzerine)
