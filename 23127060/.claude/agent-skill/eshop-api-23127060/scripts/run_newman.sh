#!/usr/bin/env bash
# run_newman.sh - Chạy Newman cho 1 API trên một CSDL sạch, sinh báo cáo HTML + JSON.
#
#   bash run_newman.sh API-1            # chay day du (co case @bug -> se FAIL, dung y do)
#   bash run_newman.sh API-1 contract    # chi chay collection @contract (moc hoi quy)
#   bash run_newman.sh all               # chay ca 3 API
#
# Chạy từ thư mục 23127060/.
#
# VÌ SAO PHẢI KHỞI ĐỘNG LẠI BACKEND TRƯỚC MỖI LẦN CHẠY
#   backend/database.js gọi initDatabase() ngay khi module được require, và hàm đó bắt đầu
#   bang mot loat DROP TABLE. Khoi dong lai backend = CSDL ve dung trang thai seed goc.
#   Đây không phải tùy chọn: SUT có bug A-09 (mỗi lần đăng nhập sai cộng +2, khóa ở 3), nên
#   sau một lần chạy thì tài khoản test đã bị khóa 180 giây. Chạy lần hai trên cùng CSDL đó
#   sẽ cho ra hàng loạt thất bại GIẢ không liên quan gì đến chất lượng API.
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
# của nó), tự giết phiên làm việc. Đặt một ký tự vào ngoặc vuông làm mẫu không còn khớp chính nó.
pkill -f "[n]ode server\.js" >/dev/null 2>&1 || true
sleep 1
# setsid --fork tách hẳn tiến trình backend ra khỏi phiên làm việc của script này.
# Nếu dùng "node server.js &" thì backend vẫn là con của script, và script sẽ treo ở bước
# thoát vì chờ một tiến trình không bao giờ kết thúc.
( cd "$SUT_DIR" && setsid --fork node server.js ) > /tmp/eshop_${SID}.log 2>&1 < /dev/null || true

echo "[2/4] Cho SUT san sang tai $BASE_URL ..."
up=0
for i in $(seq 1 30); do
  if curl -sf "$BASE_URL/api/products" >/dev/null 2>&1; then up=1; echo "      SUT san sang sau ${i}s"; break; fi
  sleep 1
done
[ "$up" = "1" ] || { echo "[LOI] SUT khong khoi dong duoc. Log:"; cat /tmp/eshop_${SID}.log; exit 1; }

# ---- 2) Kiểm tra nhanh trạng thái SUT ----
echo "[3/4] Kiem tra trang thai SUT..."
node agent-skill/eshop-api-23127060/scripts/seed_sut.js check 2>/dev/null || true

# ---- 3) Chạy Newman ----
# Tài khoản test được tạo bởi folder _setup ngay trong collection, không dùng seed_sut.js
# reset, để tránh đăng ký trùng email (SUT không có ràng buộc UNIQUE trên cột email).
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

# Báo cáo JSON của Newman chứa toàn bộ body request/response nên rất lớn (8-24 MB).
# Nén lại ngay để repo không phình; mọi script phân tích đều đọc được cả .json và .json.gz.
[ -f "$JSON" ] && gzip -9 -f "$JSON" && JSON="${JSON}.gz"

echo
echo "Bao cao JSON : $JSON"
echo "Bao cao HTML : $HTML"
echo "--reporter-htmlextra-logs giu lai dong console.log '[HW06][${SID}] ...' trong file HTML,"
echo "day chinh la bang chung header X-Student-Id ma de bai muc 11 yeu cau."
exit $rc
