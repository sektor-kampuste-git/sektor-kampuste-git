# n8n ile 10 dakikada prototip: destek talebi triyajı

n8n = görsel otomasyon (low-code). Webhook → LLM → karar → yönlendirme akışını kod yazmadan kurarsınız; Hafta 7'deki ajanın "iş süreci" hali. Kurumlarda Power Automate / Logic Apps / Zapier'in açık kaynak karşılığı.

## Kurulum
```bash
cd week9/n8n
cp ../../.env .env            # LLM_BASE_URL, LLM_API_KEY, LLM_MODEL (compose bunları okur)
docker compose up -d           # http://localhost:5678 → hesap oluştur
```
Docker yoksa: n8n Cloud 14 gün ücretsiz deneme; ortam değişkenleri yerine HTTP Request node'una anahtarı **Credential** olarak girin (asla düz metin).

## Akışı yükle
Workflows → **Import from file** → `destek_triyaj_workflow.json` → **Save** → sağ üstte **Inactive → Active**.
İçe aktarma sürüm uyumsuzluğu verirse (n8n hızlı güncellenir), aynı akışı elle kurun — 5 node:

| # | Node | Ayar |
|---|---|---|
| 1 | **Webhook** | POST, path `destek`, Respond: *Using Respond to Webhook node* |
| 2 | **HTTP Request** | POST `{{$env.LLM_BASE_URL}}/chat/completions`, header `Authorization: Bearer {{$env.LLM_API_KEY}}`, JSON body: model + `response_format: json_object` + sistem promptu (triyaj şeması) + `$json.body.mesaj` |
| 3 | **Code** | `choices[0].message.content` → `JSON.parse`; hata olursa `insan_gerekli=true` |
| 4 | **IF** | `{{$json.insan_gerekli}}` is true |
| 5a/5b | **Respond to Webhook** | true → `insana_yonlendirildi` · false → `otomatik` |

## Dene
```bash
curl -s -X POST http://localhost:5678/webhook/destek -H 'Content-Type: application/json' \
  -d '{"musteri":"m-1","mesaj":"Siparişim 10 gündür gelmedi, paramı geri istiyorum yoksa şikayet edeceğim"}'
# → {"durum":"insana_yonlendirildi","kuyruk":"temsilci-kargo","oncelik":"yuksek",...}
curl -s -X POST http://localhost:5678/webhook/destek -H 'Content-Type: application/json' \
  -d '{"musteri":"m-2","mesaj":"Kargo takip numaramı nereden görebilirim?"}'
# → {"durum":"otomatik","kategori":"kargo","oncelik":"dusuk",...}
```
Test modunda (Active değilken) URL `/webhook-test/destek` olur ve her çağrı için "Listen for test event"e basmanız gerekir.

## Lab'da sizden beklenen
- Akışı çalıştırıp iki curl çıktısının ekran görüntüsü
- Bir **iyileştirme**: (a) 5a dalına e-posta/Slack/Teams bildirimi, (b) Google Sheet / Airtable'a kayıt (denetim izi!), (c) `oncelik=yuksek` için ikinci bir LLM çağrısıyla yanıt taslağı
- `kullanim_senaryosu_sablonu.md` §9'a ekran görüntüsü ve "bu akışta insan onayı nerede?" cümlesi

## Yönetişim notu
Bu akış **karar vermez**, **yönlendirir**. Para iadesi, hesap kapatma gibi işlemler 5a dalında insana gider. Her çağrı n8n Executions sekmesinde kalır (denetim izi); kişisel veri varsa saklama süresini ayarlayın (Settings → Executions → Prune).
