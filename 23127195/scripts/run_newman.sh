#!/usr/bin/env bash
# =============================================================================
# run_newman.sh — chay toan bo API test cua 23127195 (HW06)
#
#   ./scripts/run_newman.sh              # chay ca 3 API
#   ./scripts/run_newman.sh api1         # chay 1 collection
#   ./scripts/run_newman.sh api1 api3    # chay nhieu collection
#   SUT_DIR=/duong/dan ./scripts/run_newman.sh
#   NO_RESTART=1 ./scripts/run_newman.sh # khong restart SUT (dung khi chay trong CI)
#
# LUU Y VE TINH TAI LAP:
#   Backend cua SUT DROP + seed lai toan bo bang moi lan khoi dong
#   (xem backend/database.js). Vi vay script LUON restart SUT truoc khi chay,
#   de moi lan run deu xuat phat tu cung mot trang thai du lieu.
#
# LUU Y VE BIEN MOI TRUONG:
#   Cac bien runtime (adminToken, userToken, formulaToken, couponToken, otp,
#   countBefore...) duoc test script ghi vao COLLECTION scope. KHONG khai bao
#   chung trong file environment: bien Environment co do uu tien CAO HON
#   Collection nen mot gia tri rong se de len gia tri that va gay 401 hang loat.
# =============================================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SUT_DIR="${SUT_DIR:-$HERE/../../.sut/eshop-sut}"
BASE_URL="${BASE_URL:-http://localhost:3000}"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="$HERE/newman"
mkdir -p "$OUT"

restart_sut() {
    if [ "${NO_RESTART:-0}" = "1" ]; then
        echo ">> NO_RESTART=1 — dung SUT dang chay san"
        return 0
    fi
    echo ">> Restart SUT de reset du lieu ve trang thai seed..."
    powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Where-Object { \$_.CommandLine -like '*server.js*' } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force -ErrorAction SilentlyContinue }" 2>/dev/null || true
    sleep 1
    ( cd "$SUT_DIR/backend" && node server.js > "$OUT/sut-server.log" 2>&1 & )
    for _ in $(seq 1 40); do
        if curl -s -o /dev/null "$BASE_URL/api/products"; then
            echo ">> SUT san sang tai $BASE_URL"
            return 0
        fi
        sleep 0.25
    done
    echo "!! SUT khong khoi dong duoc — xem $OUT/sut-server.log" >&2
    return 1
}

run_one() {
    local key="$1"
    local col="$2"
    local log="$OUT/${key}_${STAMP}.console.log"
    echo ""
    echo "================================================================"
    echo ">> Newman run: $key  ($col)"
    echo "================================================================"
    npx newman run "$HERE/postman/collections/$col" --environment "$HERE/postman/environments/eshop-local.postman_environment.json" --env-var "baseUrl=$BASE_URL" --reporters cli,htmlextra,json,junit --reporter-cli-no-banner --reporter-htmlextra-export "$OUT/${key}_${STAMP}.html" --reporter-htmlextra-title "HW06 - 23127195 - ${key}" --reporter-htmlextra-browserTitle "HW06 23127195 ${key}" --reporter-htmlextra-logs --reporter-htmlextra-displayProgressBar --reporter-json-export "$OUT/${key}_${STAMP}.json" --reporter-junit-export "$OUT/${key}_${STAMP}.xml" > "$log" 2>&1
    local rc=$?
    sed -n '/^.*│.*│/p' "$log" | tail -12
    echo "   (log day du: $log)"
    return "$rc"
}

collection_for() {
    case "$1" in
        api1) echo "api1_fr04_user_profile.postman_collection.json" ;;
        api2) echo "api2_fr09_apply_coupon.postman_collection.json" ;;
        api3) echo "api3_fr16_import_products.postman_collection.json" ;;
        *)    echo "" ;;
    esac
}

if [ "$#" -gt 0 ]; then
    TARGETS=("$@")
else
    TARGETS=(api1 api2 api3)
fi

restart_sut || exit 1

FAILED=0
for t in "${TARGETS[@]}"; do
    col="$(collection_for "$t")"
    if [ -z "$col" ]; then
        echo "!! Khong biet target '$t' (hop le: api1 api2 api3)"
        continue
    fi
    if [ ! -f "$HERE/postman/collections/$col" ]; then
        echo ">> Bo qua $t — chua co $col"
        continue
    fi
    run_one "$t" "$col" || FAILED=1
done

echo ""
echo ">> Bao cao da xuat vao: $OUT"
ls -1t "$OUT" | head -14
echo ""
if [ "$FAILED" -ne 0 ]; then
    echo ">> Ket qua: CO test FAIL (exit 1). Day la ket qua MONG DOI khi SUT con khiem khuyet —"
    echo "   xem bugs/BUG_REPORTS.md de doi chieu tung FAIL voi ma loi tuong ung."
fi
exit "$FAILED"
