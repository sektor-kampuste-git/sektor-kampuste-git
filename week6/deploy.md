# Yayın: üç yol, hepsi ücretsiz katmanda

## 1. Streamlit Community Cloud (en kolay, 5 dk)
1. Uygulama GitHub'da **public** bir repoda (ya da Student Pack ile private)
2. share.streamlit.io → New app → repo, dal, `app.py`
3. **Advanced settings → Secrets**: `.streamlit/secrets.toml.example` içeriğini kendi anahtarınızla yapıştırın
4. Deploy → 1-2 dk sonra `https://<ad>.streamlit.app`
- Uyku modu: 7 gün kullanılmazsa uyur, ilk açılış 30 sn sürer. Sunumdan önce bir kez açın.
- `requirements.txt` repo kökünde ya da `app.py` ile aynı klasörde olmalı.

## 2. Azure Container Apps (Hafta 4'teki yol)
`week6/baslangic/Dockerfile` hazır; 8501 portu.
```bash
cd <uygulama klasörü>
az containerapp up --name <ad> --resource-group rg-ccai-week4 --location westeurope \
  --environment ccai-env --source . --ingress external --target-port 8501 \
  --env-vars LLM_BASE_URL=$LLM_BASE_URL LLM_MODEL=$LLM_MODEL
az containerapp secret set -n <ad> -g rg-ccai-week4 --secrets llm-key=$LLM_API_KEY
az containerapp update -n <ad> -g rg-ccai-week4 --set-env-vars LLM_API_KEY=secretref:llm-key --min-replicas 0
```

## 3. Hugging Face Spaces (Docker)
Space oluştur → SDK: **Docker** → dosyaları yükle → Settings → Variables and secrets'a `LLM_*` ekle. `Dockerfile` içindeki `${PORT:-8501}` HF'nin 7860 portuyla da çalışır (HF `PORT` değişkenini verir).

## Hangi yol?
| | Streamlit Cloud | Container Apps | HF Spaces |
|---|---|---|---|
| Kurulum | 5 dk | 10 dk + az CLI | 7 dk |
| Maliyet | ücretsiz | ücretsiz katman (sıfıra ölçeklenir) | ücretsiz |
| Öğrettiği şey | hızlı prototip | gerçek bulut dağıtımı, secret yönetimi | ML topluluğu, Docker |
| Sınırlar | sadece Streamlit, uyur | Azure hesabı gerekir | CPU yavaş |
