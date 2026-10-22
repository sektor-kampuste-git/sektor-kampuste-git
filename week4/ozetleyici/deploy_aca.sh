#!/usr/bin/env bash
# week4 · Azure Container Apps'e dağıtım (az CLI gerekir: https://aka.ms/installazurecli)
#
# Kullanım:
#   export LLM_BASE_URL=... LLM_API_KEY=... LLM_MODEL=...      # ya da repo kökündeki .env'i source edin
#   ./deploy_aca.sh                        # varsayılan isimlerle
#   APP=ozet-ahmet RG=rg-ccai LOC=swedencentral ./deploy_aca.sh
#
# Ne yapar?
#   1) Kaynak grubu + Container Apps ortamı oluşturur (yoksa)
#   2) Bu klasörü Azure'da imaja çevirir ve yayınlar (az containerapp up --source .)
#   3) API anahtarını SECRET olarak saklar, env var'a secretref ile bağlar (anahtar imaja girmez)
#   4) Sıfıra ölçeklenir (min 0 replika) → boştayken ücret yok; URL'i yazdırır
# Temizlik:  az group delete -n "$RG" --yes --no-wait
set -euo pipefail

RG="${RG:-rg-ccai-week4}"
LOC="${LOC:-westeurope}"
ENV_NAME="${ENV_NAME:-ccai-env}"
APP="${APP:-ozetleyici-$(whoami | tr -cd 'a-z0-9' | cut -c1-8)}"

: "${LLM_BASE_URL:?LLM_BASE_URL gerekli}"
: "${LLM_API_KEY:?LLM_API_KEY gerekli}"
: "${LLM_MODEL:?LLM_MODEL gerekli}"

echo "▶ Kaynak grubu: $RG ($LOC)  · ortam: $ENV_NAME · uygulama: $APP"
az group create -n "$RG" -l "$LOC" -o none
az extension add --name containerapp --upgrade -o none 2>/dev/null || true
az provider register -n Microsoft.App --wait -o none
az provider register -n Microsoft.OperationalInsights --wait -o none

echo "▶ İmaj oluşturuluyor ve yayınlanıyor (ilk seferde 3-5 dk)..."
az containerapp up \
  --name "$APP" --resource-group "$RG" --location "$LOC" \
  --environment "$ENV_NAME" --source . \
  --ingress external --target-port 8000 \
  --env-vars "LLM_BASE_URL=$LLM_BASE_URL" "LLM_MODEL=$LLM_MODEL" \
  -o none

echo "▶ Anahtar secret olarak ekleniyor..."
az containerapp secret set -n "$APP" -g "$RG" --secrets "llm-key=$LLM_API_KEY" -o none
az containerapp update -n "$APP" -g "$RG" \
  --set-env-vars "LLM_API_KEY=secretref:llm-key" \
  --min-replicas 0 --max-replicas 2 -o none

FQDN=$(az containerapp show -n "$APP" -g "$RG" --query properties.configuration.ingress.fqdn -o tsv)
echo
echo "✅ Yayında: https://$FQDN"
echo "   Sağlık:  curl https://$FQDN/saglik"
echo "   Loglar:  az containerapp logs show -n $APP -g $RG --follow"
echo "   Sil:     az group delete -n $RG --yes --no-wait"
