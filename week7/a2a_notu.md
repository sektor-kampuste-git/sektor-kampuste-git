# MCP ve A2A — iki protokol, iki farklı soru

| | **MCP** (Model Context Protocol) | **A2A** (Agent2Agent) |
|---|---|---|
| Soru | Ajan, **araçlara ve verilere** nasıl erişir? | Ajanlar **birbirleriyle** nasıl konuşur? |
| Taraflar | Host (IDE/uygulama) → Client → **Server** (sizin araçlarınız) | Client ajan → **Remote ajan** |
| Birimler | `tools`, `resources`, `prompts` | `Agent Card`, `task`, `message`, `artifact` |
| Taşıma | stdio (yerel) · Streamable HTTP (uzak) | HTTP + JSON-RPC, SSE ile akış |
| Keşif | İstemci sunucuya bağlanır, `list_tools` | `/.well-known/agent-card.json` |
| Kim tanımladı | Anthropic (2024), açık standart | Google (2025), Linux Foundation'a devredildi |
| Bu haftaki dosya | `mcp_sunucu.py`, `mcp_istemci.py` | `a2a_mini.py` (süreç içi taklit) |

**Tek cümle:** MCP ajanın *elleri*, A2A ajanın *meslektaşları*.

## Ne zaman hangisi?
- Veritabanı, CRM, dosya sistemi, kargo API'si → **MCP sunucusu** yazın. Bir kez yazılır, her IDE/ajan kullanır.
- Başka ekibin / başka şirketin ajanıyla iş bölümü (sizin destek ajanınız, onların lojistik ajanıyla) → **A2A**. Karşı tarafın araçlarını bilmeniz gerekmez; yalnızca yeteneklerini (Agent Card) bilirsiniz.
- İkisi birlikte: her ajan kendi araçlarına MCP ile, diğer ajanlara A2A ile bağlanır.

## Agent Card örneği (gerçek A2A biçimine yakın)
```json
{
  "name": "destek-uzmani",
  "description": "Sipariş, kargo ve iade sorularını yanıtlar",
  "url": "https://destek.kampusteknoloji.example/a2a",
  "version": "1.0.0",
  "capabilities": {"streaming": true, "pushNotifications": false},
  "skills": [
    {"id": "siparis-durumu", "name": "Sipariş durumu", "description": "SIP-xxxx için durum ve kargo", "tags": ["siparis", "kargo"]},
    {"id": "iade", "name": "İade", "description": "Kategoriye göre iade kuralı ve tutar", "tags": ["iade"]}
  ],
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain", "application/json"]
}
```

## Bütçe neden her ajana ayrı?
`a2a_mini.py`'de planlayıcı ve uzman ayrı `Butce` nesneleri taşır. Tek bütçe olsaydı uzmanın döngüye girmesi planlayıcıyı da bitirirdi; ayrı bütçe hatayı **yerelleştirir**. Gerçek sistemlerde bu, görev başına token/maliyet tavanı ve zaman aşımı olarak uygulanır (Hafta 8'de tracing ile izleyeceğiz).

## Güvenlik notu (Hafta 8'e köprü)
- MCP sunucusu **sizin kodunuz**: araç yalnızca yapması gerekeni yapsın (hesapla → `eval` değil `ast`).
- Araç çıktıları **güvenilmeyen girdidir**: bir kargo notunda "önceki talimatları yoksay" yazabilir (prompt injection). Çıktıyı veri olarak işleyin, talimat olarak değil.
- Uzak MCP/A2A sunucularında kimlik doğrulama (OAuth) ve en az yetki.

## Daha ileri
- Resmî A2A Python SDK: `pip install a2a-sdk` → `a2a_mini.py`'deki iki ajanı gerçek HTTP sunucularına çevirin.
- MCP'yi Streamable HTTP ile uzaktan sunun: `sunucu.run(transport="streamable-http")`; Azure Container Apps'e Hafta 4 betiğiyle dağıtın.
- MCP `prompts`: kullanıcıya hazır prompt şablonları sunmak için (`@sunucu.prompt()`).
