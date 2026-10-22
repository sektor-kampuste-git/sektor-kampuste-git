# araclar/ — ortak yardımcılar

| Dosya | Ne işe yarar |
|---|---|
| `sahte_llm_sunucu.py` | Çevrimdışı, OpenAI uyumlu **sahte** model sunucusu. Ağ çökerse demolar aynı kodla çalışır; anahtar olmadan lab kodu denenir. Gerçek model değildir. |

## Sahte sunucuyu kullanmak

```bash
pip install fastapi "uvicorn[standard]"
python araclar/sahte_llm_sunucu.py          # http://127.0.0.1:8080/v1
```

`.env` içinde:

```
LLM_BASE_URL=http://localhost:8080/v1
LLM_API_KEY=sahte
LLM_MODEL=sahte-model
EMBED_MODEL=sahte-embedding
```

Desteklenenler: `chat.completions` (araç çağrısı, `response_format`, `stream`), `embeddings`, `models`.
Yanıtlar kural tabanlıdır: araç tanımı görürse kullanıcı metnine en yakın aracı çağırır, JSON şeması
görürse şemaya uygun örnek JSON döner, aksi halde "[SAHTE YANIT]" ile başlayan bir metin verir.
