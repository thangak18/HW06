#!/usr/bin/env bash
# =============================================================================
# reproduce_bugs.sh — Tai hien toan bo loi bang curl (doc lap voi Postman)
#
# Muc dich: cung cap duong tai hien toi gian, khong phu thuoc Postman/Newman,
# de nguoi cham co the tu kiem chung tung loi. Ket qua duoc ghi ra
# bugs/evidence/reproduce_output.txt
#
#   BASE_URL=http://localhost:3000 bash bugs/reproduce_bugs.sh
# =============================================================================
set -u

B="${BASE_URL:-http://localhost:3000}/api"
SID="23127195"
H=(-H "Content-Type: application/json" -H "X-Student-Id: ${SID}")

hr()  { printf '\n%s\n' "----------------------------------------------------------------------"; }
sec() { hr; printf '### %s\n' "$1"; }

jqv() { python -c "import sys,json;d=json.load(sys.stdin);print(d.get('$1'))" 2>/dev/null; }

echo "Tai hien loi — SUT: $B"
echo "Thoi diem   : $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "Student ID  : $SID (moi request deu mang header X-Student-Id)"

USER_TOKEN=$(curl -s "${H[@]}" -X POST "$B/login" -d '{"email":"test@eshop.com","password":"Test1234!"}' | jqv token)
ADMIN_TOKEN=$(curl -s "${H[@]}" -X POST "$B/login" -d '{"email":"admin@eshop.com","password":"Admin123!"}' | jqv token)
AU=(-H "Authorization: Bearer $USER_TOKEN")
AA=(-H "Authorization: Bearer $ADMIN_TOKEN")
count() { curl -s "${H[@]}" "$B/products" | python -c "import sys,json;print(len(json.load(sys.stdin)))"; }

# ---------------------------------------------------------------- API-1 FR-04
sec "BUG-A1-01 [Critical] SEC-06 — leo quyen len admin qua PUT /api/users/me"
echo '$ curl -X PUT /api/users/me -d {"name":...,"role":"admin"}'
curl -s "${H[@]}" "${AU[@]}" -X PUT "$B/users/me" \
  -d '{"name":"Test User","shipping_address":"1 Le Loi","phone":"0912345678","role":"admin"}'
echo; echo '$ curl /api/users/me   -> role hien tai:'
curl -s "${H[@]}" "${AU[@]}" "$B/users/me" | jqv role
echo '$ dang nhap lai -> JWT moi mang role gi?'
NEW_TOKEN=$(curl -s "${H[@]}" -X POST "$B/login" -d '{"email":"test@eshop.com","password":"Test1234!"}' | jqv token)
curl -s "${H[@]}" -X POST "$B/login" -d '{"email":"test@eshop.com","password":"Test1234!"}' | python -c "import sys,json;print('role trong JWT:',json.load(sys.stdin)['user']['role'])"
echo '$ dung JWT do goi GET /api/admin/users (chi admin moi duoc phep):'
curl -s -o /dev/null -w "   HTTP %{http_code}\n" "${H[@]}" -H "Authorization: Bearer $NEW_TOKEN" "$B/admin/users"
curl -s "${H[@]}" -H "Authorization: Bearer $NEW_TOKEN" "$B/admin/users" | head -c 200; echo

sec "BUG-A1-02 [High] SEC-01 — GET /api/users/me tra ve mat khau plaintext + reset_token"
curl -s "${H[@]}" "${AU[@]}" "$B/users/me"; echo

sec "BUG-A1-03 [Medium] FR-04 — khong validate so dien thoai"
for p in "abc" "12345" "9912345678" "" "0912-345-678" "+84912345678"; do
  printf '   phone=%-14s -> ' "\"$p\""
  curl -s "${H[@]}" "${AU[@]}" -X PUT "$B/users/me" \
    -d "{\"name\":\"T\",\"shipping_address\":\"a\",\"phone\":\"$p\"}"
  echo
done

sec "BUG-A1-04 [Medium] FR-04 — khong validate ho ten"
for n in "" "   " "23127195"; do
  printf '   name=%-12s -> ' "\"$n\""
  curl -s "${H[@]}" "${AU[@]}" -X PUT "$B/users/me" \
    -d "{\"name\":\"$n\",\"shipping_address\":\"a\",\"phone\":\"0912345678\"}"
  echo
done

sec "BUG-A1-05 [Medium] Cap nhat mot phan xoa trang cac truong khong gui"
curl -s "${H[@]}" "${AU[@]}" -X PUT "$B/users/me" \
  -d '{"name":"Baseline","shipping_address":"227 Nguyen Van Cu","phone":"0912345678"}' > /dev/null
echo '   truoc:  ' && curl -s "${H[@]}" "${AU[@]}" "$B/users/me" | python -c "import sys,json;d=json.load(sys.stdin);print('           name=%r phone=%r addr=%r'%(d['name'],d['phone'],d['shipping_address']))"
curl -s "${H[@]}" "${AU[@]}" -X PUT "$B/users/me" -d '{"name":"Chi doi ten"}' > /dev/null
echo '   sau khi PUT chi gui {"name":"Chi doi ten"}:'
curl -s "${H[@]}" "${AU[@]}" "$B/users/me" | python -c "import sys,json;d=json.load(sys.stdin);print('           name=%r phone=%r addr=%r'%(d['name'],d['phone'],d['shipping_address']))"

# ---------------------------------------------------------------- API-2 FR-09
sec "BUG-A2-01 [Critical] C4/SEC-02 — apply-coupon khong yeu cau dang nhap"
echo '$ curl -X POST /api/apply-coupon  (KHONG kem Authorization)'
curl -s -o /dev/null -w "   HTTP %{http_code}\n" "${H[@]}" -X POST "$B/apply-coupon" -d '{"code":"SAVE10","total_amount":500000}'
curl -s "${H[@]}" -X POST "$B/apply-coupon" -d '{"code":"SAVE10","total_amount":500000}'; echo

sec "BUG-A2-02 [Critical] Cong thuc percent sai -> giam gia AM"
echo '   FR-09: discount = total x discount_value / 100 = 500000 x 10 / 100 = 50000'
echo '   Ky vong: discount_amount=50000, final_amount=450000'
echo '   Thuc te:'
curl -s "${H[@]}" -X POST "$B/apply-coupon" -d '{"code":"SAVE10","total_amount":500000,"user_id":2}'; echo
echo '   -> khach hang phai tra 5.000.000 thay vi 450.000 (gap 11 lan gia goc)'

sec "BUG-A2-03 [High] C3 dung dau > thay vi >= (FR-09 ghi ro >=)"
for t in 299999 300000 300001; do
  printf '   SAVE10 total=%-8s (min=300000) -> ' "$t"
  curl -s "${H[@]}" -X POST "$B/apply-coupon" -d "{\"code\":\"SAVE10\",\"total_amount\":$t,\"user_id\":2}" | head -c 120
  echo
done

sec "BUG-A2-04/05 [High] C5 bi vo hieu khi bo user_id / muon luot nguoi khac"
curl -s "${H[@]}" "${AU[@]}" -X POST "$B/coupon-usage" -d '{"coupon_id":1}' > /dev/null
echo '   (da ghi 1 luot dung SAVE10 cho user id=2, max_uses_per_user=1)'
printf '   co user_id=2      -> '; curl -s "${H[@]}" -X POST "$B/apply-coupon" -d '{"code":"SAVE10","total_amount":500000,"user_id":2}' | head -c 110; echo
printf '   BO user_id        -> '; curl -s "${H[@]}" -X POST "$B/apply-coupon" -d '{"code":"SAVE10","total_amount":500000}' | head -c 110; echo
printf '   user_id=1 (nguoi khac) -> '; curl -s "${H[@]}" -X POST "$B/apply-coupon" -d '{"code":"SAVE10","total_amount":500000,"user_id":1}' | head -c 110; echo

sec "BUG-A2-06 [Low] Thu tu kiem tra dieu kien: ma het han bao nham 'chua du nguong'"
printf '   EXPIRED total=500000 (>= min 100000) -> '; curl -s "${H[@]}" -X POST "$B/apply-coupon" -d '{"code":"EXPIRED","total_amount":500000}'; echo
printf '   EXPIRED total=50000  (<  min 100000) -> '; curl -s "${H[@]}" -X POST "$B/apply-coupon" -d '{"code":"EXPIRED","total_amount":50000}'; echo

sec "BUG-A2-07 [Low] Ma giam gia phan biet chu hoa/thuong"
printf '   code=SAVE10 -> '; curl -s -o /dev/null -w "HTTP %{http_code}\n" "${H[@]}" -X POST "$B/apply-coupon" -d '{"code":"SAVE10","total_amount":500000}'
printf '   code=save10 -> '; curl -s -o /dev/null -w "HTTP %{http_code}\n" "${H[@]}" -X POST "$B/apply-coupon" -d '{"code":"save10","total_amount":500000}'

sec "BUG-A2-08 [Medium] Tran so voi total_amount lon"
curl -s "${H[@]}" -X POST "$B/apply-coupon" -d '{"code":"SAVE10","total_amount":1000000000000000}'; echo

# ---------------------------------------------------------------- API-3 FR-16
sec "BUG-A3-01 [Critical] SEC-03 — nguoi dung THUONG import duoc san pham"
echo '$ POST /api/admin/import-products voi JWT cua tai khoan role=user'
curl -s "${H[@]}" "${AU[@]}" -X POST "$B/admin/import-products" \
  -d '{"products":[{"name":"HANG-GIA-DO-USER-CHEN-23127195","price":1,"description":"khong phai admin","imageUrl":"","category_id":1}]}'
echo; echo '   -> san pham co hien tren cua hang cong khai khong?'
curl -s "${H[@]}" "$B/products?search=HANG-GIA-DO-USER-CHEN-23127195"; echo

sec "BUG-A3-02 [High] FR-16 — import KHONG nguyen tu (khong rollback)"
BEFORE=$(count); echo "   so san pham truoc : $BEFORE"
echo '   gui 1 dong hop le + 1 dong THIEU name:'
curl -s "${H[@]}" "${AA[@]}" -X POST "$B/admin/import-products" \
  -d '{"products":[{"name":"ATOMIC-OK-23127195","price":5000,"category_id":1},{"price":7000,"category_id":1}]}'
AFTER=$(count); echo; echo "   so san pham sau   : $AFTER   (FR-16 yeu cau all-or-nothing -> phai bang $BEFORE)"
echo '   dong hop le co con nam lai trong CSDL khong?'
curl -s "${H[@]}" "$B/products?search=ATOMIC-OK-23127195" | head -c 200; echo

sec "BUG-A3-03/04 [High] Khong validate price (0 / am / chuoi / thieu / null)"
for p in '0' '-50000' '"khong-phai-so"' 'null'; do
  printf '   price=%-16s -> ' "$p"
  curl -s "${H[@]}" "${AA[@]}" -X POST "$B/admin/import-products" \
    -d "{\"products\":[{\"name\":\"PRICE-TEST-23127195\",\"price\":$p,\"category_id\":1}]}"
  echo
done

sec "BUG-A3-05/08 [Medium] Khong kiem khoa ngoai category_id / am tham gan mac dinh"
for c in '999' '0' '-1'; do
  printf '   category_id=%-5s -> ' "$c"
  curl -s "${H[@]}" "${AA[@]}" -X POST "$B/admin/import-products" \
    -d "{\"products\":[{\"name\":\"CAT-TEST-23127195\",\"price\":1000,\"category_id\":$c}]}"
  echo
done
printf '   THIEU category_id  -> '
curl -s "${H[@]}" "${AA[@]}" -X POST "$B/admin/import-products" \
  -d '{"products":[{"name":"NOCAT-23127195","price":1000}]}'
echo
echo '   -> danh muc thuc te duoc gan:'
curl -s "${H[@]}" "$B/products?search=NOCAT-23127195" | python -c "import sys,json;d=json.load(sys.stdin);print('     category_id =',d[0]['category_id'] if d else 'khong tim thay')"

sec "BUG-A3-06/07 [Low] name toan khoang trang lot qua / khong gioi han 255 ky tu"
printf '   name=\"     \" -> '
curl -s "${H[@]}" "${AA[@]}" -X POST "$B/admin/import-products" \
  -d '{"products":[{"name":"     ","price":1000,"category_id":1}]}'
echo
printf '   name dai 300 ky tu -> '
LONG=$(python -c "print('X'*300)")
curl -s "${H[@]}" "${AA[@]}" -X POST "$B/admin/import-products" \
  -d "{\"products\":[{\"name\":\"$LONG\",\"price\":1000,\"category_id\":1}]}"
echo

sec "BUG-A3-09 [High] Phan tu null trong mang gay CRASH 500 + lo stack trace HTML"
curl -s -o /dev/null -w "   HTTP %{http_code}\n" "${H[@]}" "${AA[@]}" -X POST "$B/admin/import-products" \
  -d '{"products":[{"name":"NULLROW-23127195","price":1000,"category_id":1},null]}'
echo '   30 dong dau cua response body:'
curl -s "${H[@]}" "${AA[@]}" -X POST "$B/admin/import-products" \
  -d '{"products":[{"name":"NULLROW2-23127195","price":1000,"category_id":1},null]}' | head -c 600
echo

sec "BUG-A3-10 [Low] Tran so voi price cuc lon"
curl -s "${H[@]}" "${AA[@]}" -X POST "$B/admin/import-products" \
  -d '{"products":[{"name":"HUGE-PRICE-23127195","price":1000000000000000000,"category_id":1}]}' > /dev/null
curl -s "${H[@]}" "$B/products?search=HUGE-PRICE-23127195" | python -c "import sys,json;d=json.load(sys.stdin);print('   gia gui len : 1000000000000000000');print('   gia luu lai :',d[0]['price'] if d else 'n/a')"

sec "BUG-A3-11 [Medium] imageUrl chap nhan giao thuc javascript: (vector stored XSS)"
curl -s "${H[@]}" "${AA[@]}" -X POST "$B/admin/import-products" \
  -d '{"products":[{"name":"JSURL-23127195","price":1000,"imageUrl":"javascript:alert(document.cookie)","category_id":1}]}' > /dev/null
curl -s "${H[@]}" "$B/products?search=JSURL-23127195" | python -c "import sys,json;d=json.load(sys.stdin);print('   imageUrl luu lai:',repr(d[0]['imageUrl']) if d else 'n/a')"

hr
echo "Hoan tat. Luu y: cac loi tren deu duoc phu boi test case tuong ung —"
echo "doi chieu cot 'Ma loi' trong testcases/TESTCASES_23127195.xlsx."
