#!/usr/bin/env bash
# run_newman.sh - Chay Newman cho 1 API, sinh bao cao HTML + JSON.
#
#   bash run_newman.sh API-1              # chay full (co case @bug -> se fail, dung y do)
#   bash run_newman.sh API-1 contract     # chi chay collection @contract (phai 100% pass)
#
# Chay tu thu muc members/23127060/
set -uo pipefail

API="${1:-API-1}"
MODE="${2:-full}"
SID="23127060"
TS="$(date +%Y%m%d-%H%M)"

COL="postman/collections/${SID}_HW06_${API}.postman_collection.json"
COL_CONTRACT="postman/collections/${SID}_HW06_${API}_contract.postman_collection.json"
ENV="postman/environments/${SID}_local.postman_environment.json"
OUTDIR="newman"

mkdir -p "$OUTDIR"

if ! command -v newman >/dev/null 2>&1; then
  echo "[LOI] chua co newman. Chay: npm i -g newman newman-reporter-htmlextra"
  exit 1
fi

if [ "$MODE" = "contract" ]; then
  TARGET="$COL_CONTRACT"
  LABEL="contract"
else
  TARGET="$COL"
  LABEL="full"
fi

if [ ! -f "$TARGET" ]; then
  echo "[LOI] khong thay collection: $TARGET"
  echo "      chay build_collection.py truoc (them --only-tag @contract cho ban contract)"
  exit 1
fi
if [ ! -f "$ENV" ]; then
  echo "[LOI] khong thay environment: $ENV"
  exit 1
fi

# kiem tra SUT dang song
if ! curl -sf http://localhost:3000/api/products >/dev/null 2>&1; then
  echo "[LOI] SUT chua chay tai http://localhost:3000"
  echo "      (cd <duong-dan>/eshop-sut/backend && nohup node server.js > /tmp/eshop.log 2>&1 &)"
  exit 1
fi

BASE="${OUTDIR}/${SID}_${API}_${LABEL}_${TS}"
echo "[INFO] chay $API ($LABEL) -> ${BASE}.html"

newman run "$TARGET" \
  -e "$ENV" \
  --reporters cli,json,htmlextra \
  --reporter-json-export "${BASE}.json" \
  --reporter-htmlextra-export "${BASE}.html" \
  --reporter-htmlextra-title "HW06 ${API} - SV ${SID} - Ninh Van Khai" \
  --reporter-htmlextra-logs \
  --reporter-htmlextra-browserTitle "HW06 ${API} ${SID}" \
  --timeout-request 10000 \
  --insecure
RC=$?

echo ""
echo "[INFO] newman exit code = $RC"
if [ "$LABEL" = "contract" ] && [ "$RC" -ne 0 ]; then
  echo "[CANH BAO] ban @contract PHAI pass 100% de dung cho CI run all-pass."
  echo "           Kiem tra lai: case do co dang bi gan nham tag @contract khong?"
fi
if [ "$LABEL" = "full" ] && [ "$RC" -eq 0 ]; then
  echo "[CANH BAO] ban full pass 100% => co the cac case @bug chua duoc viet assertion dung."
fi

echo "[OK] JSON: ${BASE}.json"
echo "[OK] HTML: ${BASE}.html"
exit 0
