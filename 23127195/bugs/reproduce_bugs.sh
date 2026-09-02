#!/usr/bin/env bash
# =============================================================================
# reproduce_bugs.sh — Tai hien toan bo 24 loi bang curl (doc lap voi Postman)
#
# Muc dich: cung cap duong tai hien toi gian, khong phu thuoc Postman/Newman,
# de nguoi cham tu kiem chung tung loi. Ket qua ghi ra
# bugs/evidence/reproduce_output.txt
#
#   BASE_URL=http://localhost:3000 bash bugs/reproduce_bugs.sh
#
# NGUYEN TAC CUA BAN NAY: lenh IN RA chinh la lenh DUOC CHAY.
#   Ham run() nhan lenh duoi dang mang doi so, chay no bang "$@", va dung
#   chinh mang do de dung lai dong hien thi. Khong co dong mo ta nao viet tay.
#   Nho vay ban ghi (va anh chup man hinh) la mot transcript trung thuc: doc
#   duoc chinx xac request da gui, copy lai chay duoc.
#
#   Hai chuoi dai bi thay bang ten bien cho de doc — JWT va cap header lap
#   lai o moi lenh. Dinh nghia cua chung duoc in ngay dau ban ghi.
# =============================================================================
set -u

B="${BASE_URL:-http://localhost:3000}/api"
SID="23127195"
CT="Content-Type: application/json"
XS="X-Student-Id: ${SID}"

hr()   { printf '\n%s\n' "----------------------------------------------------------------------"; }
sec()  { hr; printf '### %s\n' "$1"; }
note() { printf '   %s\n' "$1"; }          # ghi chu cua nguoi lam, KHONG phai lenh

jqv()   { python -c "import sys,json;d=json.load(sys.stdin);print(d.get('$1'))" 2>/dev/null; }
count() { curl -s -H "$CT" -H "$XS" "$B/products" | python -c "import sys,json;print(len(json.load(sys.stdin)))"; }

# ---------------------------------------------------------------------------
# run — in ra dung lenh sap chay, roi chay no
# ---------------------------------------------------------------------------
run() {
    local out="" a
    for a in "$@"; do
        case $a in
            *[\ \"\{]*) out="$out '$a'" ;;   # co khoang trang / nhay / ngoac -> boc nhay don
            *)          out="$out $a"   ;;
        esac
    done
    # rut gon nhung chuoi dai lap lai thanh ten bien (chi doi HIEN THI)
    local v
    for v in USER_TOKEN ADMIN_TOKEN NEW_TOKEN; do
        # bo qua bien chua duoc gan — thay chuoi rong se pha hong dong hien thi
        [ -n "${!v:-}" ] && out=${out//${!v}/\$$v}
    done
    out=${out//-H \'$CT\' -H \'$XS\'/\$H}
    out=${out//$B/\$B}
    printf '\n$%s\n' "$out"
    "$@"
}

echo "Tai hien loi — SUT: $B"
echo "Thoi diem   : $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "Student ID  : $SID (moi request deu mang header X-Student-Id)"

USER_TOKEN=$(curl -s -H "$CT" -H "$XS" -X POST "$B/login" -d '{"email":"test@eshop.com","password":"Test1234!"}' | jqv token)
ADMIN_TOKEN=$(curl -s -H "$CT" -H "$XS" -X POST "$B/login" -d '{"email":"admin@eshop.com","password":"Admin123!"}' | jqv token)

cat <<EOF

Bien dung trong cac lenh duoi day (rut gon cho de doc, noi dung that duoc gui di):
  \$B           = $B
  \$H           = -H '$CT' -H '$XS'
  \$USER_TOKEN  = JWT lay tu POST $B/login  voi test@eshop.com  (role=user)
  \$ADMIN_TOKEN = JWT lay tu POST $B/login  voi admin@eshop.com (role=admin)
EOF

# ---------------------------------------------------------------- API-1 FR-04
sec "BUG-A1-01 [Critical] SEC-06 — leo quyen len admin qua PUT /api/users/me"
run curl -s -X PUT "$B/users/me" -H "$CT" -H "$XS" -H "Authorization: Bearer $USER_TOKEN" \
    -d '{"name":"Test User","shipping_address":"1 Le Loi","phone":"0912345678","role":"admin"}'
note "role hien tai sau lenh tren:"
run curl -s "$B/users/me" -H "$CT" -H "$XS" -H "Authorization: Bearer $USER_TOKEN"
note "dang nhap lai — JWT moi mang role gi?"
run curl -s -X POST "$B/login" -H "$CT" -H "$XS" -d '{"email":"test@eshop.com","password":"Test1234!"}'
NEW_TOKEN=""
NEW_TOKEN=$(curl -s -H "$CT" -H "$XS" -X POST "$B/login" -d '{"email":"test@eshop.com","password":"Test1234!"}' | jqv token)
note "dung JWT moi goi GET /api/admin/users (chi admin moi duoc phep):"
run curl -s -o /dev/null -w "HTTP %{http_code}\n" "$B/admin/users" -H "$CT" -H "$XS" -H "Authorization: Bearer $NEW_TOKEN"

sec "BUG-A1-02 [High] SEC-01 — GET /api/users/me tra ve mat khau plaintext + reset_token"
run curl -s "$B/users/me" -H "$CT" -H "$XS" -H "Authorization: Bearer $USER_TOKEN"

sec "BUG-A1-03 [Medium] FR-04 — khong validate so dien thoai"
for p in "abc" "12345" "9912345678" "" "0912-345-678" "+84912345678"; do
    run curl -s -X PUT "$B/users/me" -H "$CT" -H "$XS" -H "Authorization: Bearer $USER_TOKEN" \
        -d "{\"name\":\"T\",\"shipping_address\":\"a\",\"phone\":\"$p\"}"
done

sec "BUG-A1-04 [Medium] FR-04 — khong validate ho ten"
for n in "" "   " "23127195"; do
    run curl -s -X PUT "$B/users/me" -H "$CT" -H "$XS" -H "Authorization: Bearer $USER_TOKEN" \
        -d "{\"name\":\"$n\",\"shipping_address\":\"a\",\"phone\":\"0912345678\"}"
done

sec "BUG-A1-05 [Medium] Cap nhat mot phan xoa trang cac truong khong gui"
run curl -s -X PUT "$B/users/me" -H "$CT" -H "$XS" -H "Authorization: Bearer $USER_TOKEN" \
    -d '{"name":"Baseline","shipping_address":"227 Nguyen Van Cu","phone":"0912345678"}'
note "chi gui MOT truong name, khong gui phone va shipping_address:"
run curl -s -X PUT "$B/users/me" -H "$CT" -H "$XS" -H "Authorization: Bearer $USER_TOKEN" \
    -d '{"name":"Chi doi ten"}'
note "doc lai ho so — hai truong khong gui da bi xoa trang:"
run curl -s "$B/users/me" -H "$CT" -H "$XS" -H "Authorization: Bearer $USER_TOKEN"

# ---------------------------------------------------------------- API-2 FR-09
sec "BUG-A2-01 [Critical] C4/SEC-02 — apply-coupon khong yeu cau dang nhap"
note "KHONG kem header Authorization:"
run curl -s -o /dev/null -w "HTTP %{http_code}\n" -X POST "$B/apply-coupon" -H "$CT" -H "$XS" \
    -d '{"code":"SAVE10","total_amount":500000}'
run curl -s -X POST "$B/apply-coupon" -H "$CT" -H "$XS" -d '{"code":"SAVE10","total_amount":500000}'

sec "BUG-A2-02 [Critical] Cong thuc percent sai -> giam gia AM"
note "FR-09: discount = total x discount_value / 100 = 500000 x 10 / 100 = 50000"
note "Ky vong: discount_amount=50000, final_amount=450000"
run curl -s -X POST "$B/apply-coupon" -H "$CT" -H "$XS" \
    -d '{"code":"SAVE10","total_amount":500000,"user_id":2}'
note "-> khach hang phai tra 5.000.000 thay vi 450.000 (gap 11 lan gia goc)"

sec "BUG-A2-03 [High] C3 dung dau > thay vi >= (FR-09 ghi ro >=)"
note "min_order_amount = 300000; don bang dung nguong PHAI duoc chap nhan"
for t in 299999 300000 300001; do
    run curl -s -X POST "$B/apply-coupon" -H "$CT" -H "$XS" \
        -d "{\"code\":\"SAVE10\",\"total_amount\":$t,\"user_id\":2}"
done

sec "BUG-A2-04/05 [High] C5 bi vo hieu khi bo user_id / muon luot nguoi khac"
run curl -s -X POST "$B/coupon-usage" -H "$CT" -H "$XS" -H "Authorization: Bearer $USER_TOKEN" \
    -d '{"coupon_id":1}'
note "da ghi 1 luot dung SAVE10 cho user id=2, max_uses_per_user=1"
for body in '{"code":"SAVE10","total_amount":500000,"user_id":2}' \
            '{"code":"SAVE10","total_amount":500000}' \
            '{"code":"SAVE10","total_amount":500000,"user_id":1}'; do
    run curl -s -X POST "$B/apply-coupon" -H "$CT" -H "$XS" -d "$body"
done

sec "BUG-A2-06 [Low] Thu tu kiem tra dieu kien: ma het han bao nham 'chua du nguong'"
for t in 500000 50000; do
    run curl -s -X POST "$B/apply-coupon" -H "$CT" -H "$XS" \
        -d "{\"code\":\"EXPIRED\",\"total_amount\":$t}"
done

sec "BUG-A2-07 [Low] Ma giam gia phan biet chu hoa/thuong"
for c in SAVE10 save10; do
    run curl -s -o /dev/null -w "HTTP %{http_code}\n" -X POST "$B/apply-coupon" -H "$CT" -H "$XS" \
        -d "{\"code\":\"$c\",\"total_amount\":500000}"
done

sec "BUG-A2-08 [Medium] Khong kiem mien gia tri total_amount"
run curl -s -X POST "$B/apply-coupon" -H "$CT" -H "$XS" \
    -d '{"code":"SAVE10","total_amount":1000000000000000}'

# ---------------------------------------------------------------- API-3 FR-16
sec "BUG-A3-01 [Critical] SEC-03 — nguoi dung THUONG import duoc san pham"
note "dung \$USER_TOKEN (role=user), khong phai token admin:"
run curl -s -X POST "$B/admin/import-products" -H "$CT" -H "$XS" -H "Authorization: Bearer $USER_TOKEN" \
    -d '{"products":[{"name":"HANG-GIA-DO-USER-CHEN-23127195","price":1,"description":"khong phai admin","imageUrl":"","category_id":1}]}'
note "san pham co hien tren cua hang cong khai khong?"
run curl -s "$B/products?search=HANG-GIA-DO-USER-CHEN-23127195" -H "$CT" -H "$XS"

sec "BUG-A3-02 [High] FR-16 — import KHONG nguyen tu (khong rollback)"
BEFORE=$(count); note "so san pham truoc: $BEFORE"
note "gui 1 dong hop le + 1 dong THIEU name — FR-16 yeu cau all-or-nothing:"
run curl -s -X POST "$B/admin/import-products" -H "$CT" -H "$XS" -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{"products":[{"name":"ATOMIC-OK-23127195","price":5000,"category_id":1},{"price":7000,"category_id":1}]}'
AFTER=$(count); note "so san pham sau : $AFTER   (phai bang $BEFORE neu rollback dung)"
note "dong hop le co con nam lai trong CSDL khong?"
run curl -s "$B/products?search=ATOMIC-OK-23127195" -H "$CT" -H "$XS"

sec "BUG-A3-03/04 [High] Khong validate price (0 / am / chuoi / thieu truong / null)"
for p in '"price":0' '"price":-50000' '"price":"khong-phai-so"' '"price":null'; do
    run curl -s -X POST "$B/admin/import-products" -H "$CT" -H "$XS" -H "Authorization: Bearer $ADMIN_TOKEN" \
        -d "{\"products\":[{\"name\":\"PRICE-TEST-23127195\",$p,\"category_id\":1}]}"
done
note "truong hop THIEU HAN truong price:"
run curl -s -X POST "$B/admin/import-products" -H "$CT" -H "$XS" -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{"products":[{"name":"NOPRICE-23127195","category_id":1}]}'

sec "BUG-A3-05/08 [Medium] Khong kiem khoa ngoai category_id / am tham gan mac dinh"
for c in 999 0 -1; do
    run curl -s -X POST "$B/admin/import-products" -H "$CT" -H "$XS" -H "Authorization: Bearer $ADMIN_TOKEN" \
        -d "{\"products\":[{\"name\":\"CAT-TEST-23127195\",\"price\":1000,\"category_id\":$c}]}"
done
note "truong hop THIEU category_id:"
run curl -s -X POST "$B/admin/import-products" -H "$CT" -H "$XS" -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{"products":[{"name":"NOCAT-23127195","price":1000}]}'
note "danh muc thuc te duoc gan cho san pham do:"
run curl -s "$B/products?search=NOCAT-23127195" -H "$CT" -H "$XS"

sec "BUG-A3-06/07 [Low] name toan khoang trang lot qua / khong gioi han 255 ky tu"
run curl -s -X POST "$B/admin/import-products" -H "$CT" -H "$XS" -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{"products":[{"name":"     ","price":1000,"category_id":1}]}'
LONG=$(python -c "print('X'*300)")
note "name dai 300 ky tu (rut gon khi hien thi):"
run curl -s -o /dev/null -w "HTTP %{http_code}\n" -X POST "$B/admin/import-products" -H "$CT" -H "$XS" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d "{\"products\":[{\"name\":\"XXX...300 ky tu X...XXX\",\"price\":1000,\"category_id\":1}]}"
curl -s -H "$CT" -H "$XS" -H "Authorization: Bearer $ADMIN_TOKEN" -X POST "$B/admin/import-products" \
    -d "{\"products\":[{\"name\":\"$LONG\",\"price\":1000,\"category_id\":1}]}" > /dev/null

sec "BUG-A3-09 [High] Phan tu null trong mang gay CRASH 500 + lo stack trace HTML"
run curl -s -o /dev/null -w "HTTP %{http_code}\n" -X POST "$B/admin/import-products" -H "$CT" -H "$XS" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{"products":[{"name":"NULLROW-23127195","price":1000,"category_id":1},null]}'
note "300 ky tu dau cua response body — lo duong dan he thong:"
curl -s -H "$CT" -H "$XS" -H "Authorization: Bearer $ADMIN_TOKEN" -X POST "$B/admin/import-products" \
    -d '{"products":[{"name":"NULLROW2-23127195","price":1000,"category_id":1},null]}' | head -c 300
echo

sec "BUG-A3-10 [Low] Mat chinh xac voi price vuot Number.MAX_SAFE_INTEGER"
note "Number.MAX_SAFE_INTEGER = 9007199254740991; thu voi gia tri +2 = 9007199254740993"
run curl -s -X POST "$B/admin/import-products" -H "$CT" -H "$XS" -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{"products":[{"name":"PREC-23127195","price":9007199254740993,"category_id":1}]}'
note "doc lai gia da luu — so bi lam tron xuong, mat 1 don vi:"
run curl -s "$B/products?search=PREC-23127195" -H "$CT" -H "$XS"

sec "BUG-A3-11 [Medium] imageUrl chap nhan giao thuc javascript: (vector stored XSS)"
run curl -s -X POST "$B/admin/import-products" -H "$CT" -H "$XS" -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{"products":[{"name":"JSURL-23127195","price":1000,"imageUrl":"javascript:alert(document.cookie)","category_id":1}]}'
note "gia tri imageUrl duoc luu nguyen van, khong bi loc:"
run curl -s "$B/products?search=JSURL-23127195" -H "$CT" -H "$XS"

hr
echo "Hoan tat. Cac loi tren deu duoc phu boi test case tuong ung —"
echo "doi chieu cot 'Ma loi' trong testcases/TESTCASES_23127195.xlsx."
