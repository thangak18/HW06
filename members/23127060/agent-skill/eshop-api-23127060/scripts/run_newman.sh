#!/usr/bin/env bash
# run_newman.sh - Chay Newman cho 1 API tren mot CSDL sach, sinh bao cao HTML + JSON.
#
#   bash run_newman.sh API-1            # chay day du (co case @bug -> se FAIL, dung y do)
#   bash run_newman.sh API-1 contract    # chi chay collection @contract (moc hoi quy)
#   bash run_newman.sh all               # chay ca 3 API
#
# Chay tu thu muc members/23127060/.
#
# VI SAO PHAI KHOI DONG LAI BACKEND TRUOC MOI LAN CHAY
#   backend/database.js goi initDatabase() ngay khi module duoc require, va ham do bat dau
#   bang mot loat DROP TABLE. Khoi dong lai backend = CSDL ve dung trang thai seed goc.
#   Day khong phai tuy chon: SUT co bug A-09 (moi lan dang nhap sai cong +2, khoa o 3), nen
#   sau mot lan chay thi tai khoan test da bi khoa 180 giay. Chay lan hai tren cung CSDL do
#   se cho ra hang loat that bai GIA khong lien quan gi den chat luong API.
set -uo pipefail

API="${1:-API-1}"
MODE="${2:-full}"
SID="23127060"
BASE_URL="${BASE_URL:-http://localhost:3000}"
# Tu do duong dan SUT: no nam ngang hang voi thu muc repo, nhung do cay thu muc co the
# long nhieu cap khac nhau tren tung may, o day do len tren toi da 5 cap thay vi hardcode.
if [ -z "${SUT_DIR:-}" ]; then
  for up in ".." "../.." "../../.." "../../../.." "../../../../.."; do
    if [ -d "$up/eshop-sut/backend" ]; then SUT_DIR="$up/eshop-sut/backend"; break; fi
  done
fi
SUT_DIR="${SUT_DIR:-../../../../eshop-sut/backend}"
OUTDIR="newman"
TS="$(date +%Y%m%d-%H%M%S)"

if [ "$API" = "all" ]; then
  rc=0
  for a in API-1 API-2 API-3; do
    bash "$0" "$a" "$MODE" || rc=$?
  done
  exit $rc
fi

command -v newman >/dev/null 2>&1 || {
  echo "[LOI] chua co newman. Chay: npm i -g newman newman-reporter-htmlextra"; exit 1; }

SUF=""
[ "$MODE" = "contract" ] && SUF="_contract"
COL="postman/collections/${SID}_HW06_${API}${SUF}.postman_collection.json"
ENV="postman/environments/${SID}_local.postman_environment.json"
[ -f "$COL" ] || { echo "[LOI] khong thay collection: $COL"; exit 1; }
[ -f "$ENV" ] || { echo "[LOI] khong thay environment: $ENV"; exit 1; }
mkdir -p "$OUTDIR"

# ---- 1) Dua CSDL ve trang thai goc bang cach khoi dong lai backend ----
echo "[1/4] Khoi dong lai SUT de CSDL ve trang thai seed goc..."
# Dung mau "[n]ode" thay vi "node": pkill -f so khop tren TOAN BO dong lenh, nen mot mau
# chua nguyen van "node server.js" se khop luon chinh dong lenh dang goi pkill (va shell cha
# cua no), tu giet phien lam viec. Dat mot ky tu vao ngoac vuong lam mau khong con khop chinh no.
pkill -f "[n]ode server\.js" >/dev/null 2>&1 || true
sleep 1
# setsid --fork tach han tien trinh backend ra khoi phien lam viec cua script nay.
# Neu dung "node server.js &" thi backend van la con cua script, va script se treo o buoc
# thoat vi cho mot tien trinh khong bao gio ket thuc.
( cd "$SUT_DIR" && setsid --fork node server.js ) > /tmp/eshop_${SID}.log 2>&1 < /dev/null || true

echo "[2/4] Cho SUT san sang tai $BASE_URL ..."
up=0
for i in $(seq 1 30); do
  if curl -sf "$BASE_URL/api/products" >/dev/null 2>&1; then up=1; echo "      SUT san sang sau ${i}s"; break; fi
  sleep 1
done
[ "$up" = "1" ] || { echo "[LOI] SUT khong khoi dong duoc. Log:"; cat /tmp/eshop_${SID}.log; exit 1; }

# ---- 2) Kiem tra nhanh trang thai SUT ----
echo "[3/4] Kiem tra trang thai SUT..."
node agent-skill/eshop-api-23127060/scripts/seed_sut.js check 2>/dev/null || true

# ---- 3) Chay Newman ----
# Tai khoan test duoc tao boi folder _setup ngay trong collection, khong dung seed_sut.js
# reset, de tranh dang ky trung email (SUT khong co rang buoc UNIQUE tren cot email).
JSON="${OUTDIR}/${SID}_${API}${SUF}_${TS}.json"
HTML="${OUTDIR}/${SID}_${API}${SUF}_${TS}.html"
echo "[4/4] Chay Newman: $COL"
newman run "$COL" \
  -e "$ENV" \
  --env-var "baseUrl=$BASE_URL" \
  --env-var "studentId=$SID" \
  --reporters cli,json,htmlextra \
  --reporter-cli-no-assertions --reporter-cli-no-console \
  --reporter-json-export "$JSON" \
  --reporter-htmlextra-export "$HTML" \
  --reporter-htmlextra-title "HW06 ${API} - SV ${SID} Ninh Van Khai" \
  --reporter-htmlextra-logs \
  --reporter-htmlextra-browserTitle "HW06 ${API} ${SID}" \
  --timeout-request 10000 \
  --suppress-exit-code
rc=$?

# Bao cao JSON cua Newman chua toan bo body request/response nen rat lon (8-24 MB).
# Nen lai ngay de repo khong phinh; moi script phan tich deu doc duoc ca .json va .json.gz.
[ -f "$JSON" ] && gzip -9 -f "$JSON" && JSON="${JSON}.gz"

echo
echo "Bao cao JSON : $JSON"
echo "Bao cao HTML : $HTML"
echo "--reporter-htmlextra-logs giu lai dong console.log '[HW06][${SID}] ...' trong file HTML,"
echo "day chinh la bang chung header X-Student-Id ma de bai muc 11 yeu cau."
exit $rc
