#!/usr/bin/env bash
# run_datadriven.sh - Chay collection data-driven: moi folder voi dung data file cua no.
#
#   bash agent-skill/eshop-api-23127060/scripts/run_datadriven.sh
#
# Tuong duong voi thao tac tren GUI: Collection Runner -> chon folder -> Select File -> Run.
# Newman dung co -d de nap data file, va chay lai request mot lan cho MOI DONG trong file.
set -uo pipefail
SID="23127060"
BASE_URL="${BASE_URL:-http://localhost:3000}"
COL="postman/collections/${SID}_HW06_DataDriven.postman_collection.json"
ENV="postman/environments/${SID}_local.postman_environment.json"
ENV_RUN="/tmp/${SID}_dd_env.json"
OUT="newman"
TS="$(date +%Y%m%d-%H%M%S)"

if [ -z "${SUT_DIR:-}" ]; then
  for up in ".." "../.." "../../.." "../../../.." "../../../../.."; do
    [ -d "$up/eshop-sut/backend" ] && { SUT_DIR="$up/eshop-sut/backend"; break; }
  done
fi

echo "[1/3] Khoi dong lai SUT (CSDL ve trang thai seed goc)..."
# Dung mau "[n]ode" thay vi "node": pkill -f so khop tren TOAN BO dong lenh, nen mot mau
# chua nguyen van "node server.js" se khop luon chinh dong lenh dang goi pkill (va shell cha
# cua no), tu giet phien lam viec. Dat mot ky tu vao ngoac vuong lam mau khong con khop chinh no.
pkill -f "[n]ode server\.js" >/dev/null 2>&1 || true
sleep 1
( cd "$SUT_DIR" && setsid --fork node server.js ) > /tmp/eshop_${SID}.log 2>&1 < /dev/null || true
for i in $(seq 1 30); do curl -sf "$BASE_URL/api/products" >/dev/null 2>&1 && break; sleep 1; done

# Collection data-driven khong tu tao tai khoan. Chay folder _setup cua collection API-2 truoc
# va xuat environment ra file, de lay token_user / token_admin / userId.
echo "[2/3] Chay _setup de lay token, xuat environment ra $ENV_RUN ..."
newman run "postman/collections/${SID}_HW06_API-2.postman_collection.json" \
  -e "$ENV" --folder "_setup - chuan bi du lieu va token" \
  --env-var "baseUrl=$BASE_URL" --env-var "studentId=$SID" \
  --export-environment "$ENV_RUN" \
  --reporters cli --reporter-cli-no-assertions --reporter-cli-no-console >/dev/null 2>&1

echo "[3/3] Chay tung folder voi data file tuong ung..."
run_folder () {  # $1 = ten folder, $2 = data file, $3 = nhan ngan
  echo "  -> $3  (data: $2)"
  newman run "$COL" -e "$ENV_RUN" \
    --folder "$1" -d "$2" \
    --env-var "baseUrl=$BASE_URL" --env-var "studentId=$SID" \
    --reporters cli,json,htmlextra \
    --reporter-cli-no-assertions --reporter-cli-no-console \
    --reporter-json-export "${OUT}/${SID}_DD-$3_${TS}.json" \
    --reporter-htmlextra-export "${OUT}/${SID}_DD-$3_${TS}.html" \
    --reporter-htmlextra-title "HW06 data-driven $3 - SV ${SID}" \
    --reporter-htmlextra-logs \
    --suppress-exit-code 2>&1 | grep -a -E "iterations|assertions|requests" | head -4
}
run_folder "DD1 - Brute force OTP (data: brute_force_tokens.csv)"            postman/data/brute_force_tokens.csv  DD1
run_folder "DD2 - Bang chuyen trang thai FR-10 (data: state_transitions.csv)" postman/data/state_transitions.csv  DD2
run_folder "DD3 - Lam dung han muc coupon (data: coupon_abuse.csv)"          postman/data/coupon_abuse.csv       DD3
run_folder "DD4 - Dau vao khong hop le cho POST /api/products (data: product_invalid.csv)" postman/data/product_invalid.csv DD4
gzip -9 -f ${OUT}/${SID}_DD-*_${TS}.json 2>/dev/null || true

echo
echo "Bao cao: ${OUT}/${SID}_DD-*_${TS}.html"
