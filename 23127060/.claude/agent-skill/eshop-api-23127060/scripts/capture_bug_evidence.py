#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""capture_bug_evidence.py - Chạy lại kịch bản tái hiện của từng bug và ghi lại
request + response THẬT.

  python3 capture_bug_evidence.py --base http://localhost:3000 --out bugs/evidence

Mục đích: `CLAUDE.md` mục 4 và đề bài mục 11 đều cấm báo cáo bug mà không có bằng chứng tái
hiện được. Script này chạy từng kịch bản rồi ghi nguyên văn cặp request/response ra file, để
báo cáo bug trích thẳng từ đó thay vì chép lại từ trí nhớ.

Mỗi bug khai báo một danh sách bước. Bước cuối là bước PHƠI BÀY bug; các bước trước chỉ
chuẩn bị trạng thái. Biến `$ten` trong bước sau lấy từ kết quả bước trước.
"""
import argparse
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.request

SID = "23127060"


def goi(base, method, path, body=None, token=None, ctx=None):
    ctx = ctx or {}
    def sub(x):
        if isinstance(x, str):
            return re.sub(r"\$(\w+)", lambda m: str(ctx.get(m.group(1), m.group(0))), x)
        if isinstance(x, dict):
            return {k: sub(v) for k, v in x.items()}
        if isinstance(x, list):
            return [sub(v) for v in x]
        return x

    path = sub(path)
    body = sub(body) if body is not None else None
    data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Student-Id", SID)
    if token:
        req.add_header("Authorization", "Bearer " + str(sub(token)))
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode("utf-8", "replace")
            code, ct = r.status, r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        code, ct = e.code, e.headers.get("Content-Type", "")
    except Exception as e:
        raw, code, ct = str(e), 0, ""
    try:
        js = json.loads(raw)
    except Exception:
        js = None
    return {"method": method, "path": path, "body": body, "token": bool(token),
            "code": code, "content_type": ct, "raw": raw, "json": js}


def curl(base, r):
    s = "curl -i -X %s '%s%s' \\\n     -H 'Content-Type: application/json' \\\n     -H 'X-Student-Id: %s'" % (
        r["method"], base, r["path"], SID)
    if r["token"]:
        s += " \\\n     -H 'Authorization: Bearer <token>'"
    if r["body"] is not None:
        s += " \\\n     -d '%s'" % json.dumps(r["body"], ensure_ascii=False)
    return s


# ---------------------------------------------------------------------------
# Khai báo kịch bản tái hiện. "set" lấy giá trị từ response của bước đó đưa vào ctx.
# ---------------------------------------------------------------------------
def kich_ban():
    # Mỗi bug dùng MỘT cặp tài khoản riêng. Lý do: bug A-09 khóa tài khoản 180 giây sau
    # hai lần đăng nhập sai, nên nếu dùng chung một tài khoản thì mọi kịch bản chạy sau A-09
    # đều không lấy được token và "tái hiện" ra một bug hoàn toàn khác. Biến $U và $A được
    # hàm main() gán giá trị riêng trước khi chạy từng kịch bản.
    U = "$U"
    A = "$A"
    dk_u = ("POST", "/api/register", {"name": "Victim", "email": U, "password": "Api1234!"}, None, {})
    dk_a = ("POST", "/api/register", {"name": "Attacker", "email": A, "password": "Api1234!"}, None, {})
    li_u = ("POST", "/api/login", {"email": U, "password": "Api1234!"}, None, {"tokenU": "token", "uid": "user.id"})
    li_a = ("POST", "/api/login", {"email": A, "password": "Api1234!"}, None, {"tokenA": "token", "aid": "user.id"})
    return {
    "A-01": ("Response cua forgot-password tra thang ma OTP ra ngoai", [
        dk_u, ("POST", "/api/forgot-password", {"email": U}, None, {})]),
    "A-02": ("OTP chi co 4 chu so trong khi SEC-07 doi toi thieu 6", [
        dk_u, ("POST", "/api/forgot-password", {"email": U}, None, {})]),
    "A-03": ("User enumeration: email khong ton tai tra 404, email ton tai tra 200", [
        dk_u,
        ("POST", "/api/forgot-password", {"email": U}, None, {}),
        ("POST", "/api/forgot-password", {"email": "khongtontai." + SID + "@test.local"}, None, {})]),
    "A-05": ("reset-password khong kiem tra do manh mat khau", [
        dk_u,
        ("POST", "/api/forgot-password", {"email": U}, None, {"otp": "resetToken"}),
        ("POST", "/api/reset-password", {"email": U, "resetToken": "$otp", "newPassword": "1"}, None, {}),
        ("POST", "/api/login", {"email": U, "password": "1"}, None, {})]),
    "A-07": ("login tra ve nguyen ban ghi user gom ca password plaintext va reset_token", [
        dk_u, li_u, ("GET", "/api/users/me", None, "$tokenU", {})]),
    "A-08": ("forgot-password bo qua bien err cua db.get nen loi CSDL bi bao thanh 404", [
        ("POST", "/api/forgot-password", {"email": None}, None, {})]),
    "A-09": ("Bo dem dang nhap sai cong +2 moi lan nen khoa ngay o lan sai thu HAI", [
        dk_u,
        ("POST", "/api/login", {"email": U, "password": "SaiRoi1!"}, None, {}),
        ("POST", "/api/login", {"email": U, "password": "SaiRoi2!"}, None, {}),
        ("POST", "/api/login", {"email": U, "password": "Api1234!"}, None, {})]),
    "X-01": ("PUT /api/users/me cho phep user thuong tu nang role len admin", [
        dk_a, li_a,
        ("PUT", "/api/users/me", {"name": "Attacker", "phone": "0900000000",
                                  "shipping_address": "Q5", "role": "admin"}, "$tokenA", {}),
        ("GET", "/api/users/me", None, "$tokenA", {})]),
    "B-01": ("checkout tin tuyet doi total_amount tu client", [
        dk_u, li_u,
        ("POST", "/api/checkout", {"total_amount": 1, "shipping_address": "1 Le Loi"}, "$tokenU", {"oid": "orderId"}),
        ("GET", "/api/orders/$oid", None, "$tokenU", {})]),
    "B-01b": ("checkout chap nhan total_amount am", [
        dk_u, li_u,
        ("POST", "/api/checkout", {"total_amount": -500000, "shipping_address": "1 Le Loi"}, "$tokenU", {})]),
    "B-02": ("GET /api/orders/:id thieu xac thuc - IDOR doc don hang cua bat ky ai", [
        dk_u, li_u,
        ("POST", "/api/checkout", {"total_amount": 500000, "shipping_address": "1 Le Loi"}, "$tokenU", {"oid": "orderId"}),
        ("GET", "/api/orders/$oid", None, None, {})]),
    "B-03": ("PUT /api/admin/orders/:id/status khong kiem role - user thuong doi don nguoi khac", [
        dk_u, li_u, dk_a, li_a,
        ("POST", "/api/checkout", {"total_amount": 500000, "shipping_address": "1 Le Loi"}, "$tokenU", {"oid": "orderId"}),
        ("PUT", "/api/admin/orders/$oid/status", {"status": "confirmed"}, "$tokenA", {})]),
    "B-05": ("Cong thuc coupon percent sai: discount = total*(1-value) cho ra so AM", [
        ("POST", "/api/apply-coupon", {"code": "SAVE10", "total_amount": 500000, "user_id": 1}, None, {})]),
    "B-06": ("Nguong don toi thieu dung > thay vi >=: don bang dung min_order_amount bi tu choi", [
        ("POST", "/api/apply-coupon", {"code": "SAVE10", "total_amount": 300000, "user_id": 1}, None, {}),
        ("POST", "/api/apply-coupon", {"code": "SAVE10", "total_amount": 300001, "user_id": 1}, None, {})]),
    "B-07": ("apply-coupon khong xac thuc; bo user_id di la bo qua toan bo kiem tra han muc", [
        ("POST", "/api/apply-coupon", {"code": "VIP100", "total_amount": 500000}, None, {})]),
    "B-08": ("Kiem tra han su dung nam trong nhanh total > min nen thong bao loi sai nguyen nhan", [
        ("POST", "/api/apply-coupon", {"code": "EXPIRED", "total_amount": 50000, "user_id": 1}, None, {})]),
    "B-09": ("PUT /api/orders/:id/cancel cho phep huy don dang shipping", [
        dk_u, li_u,
        ("POST", "/api/checkout", {"total_amount": 500000, "shipping_address": "1 Le Loi"}, "$tokenU", {"oid": "orderId"}),
        ("PUT", "/api/admin/orders/$oid/status", {"status": "confirmed"}, "$tokenU", {}),
        ("PUT", "/api/admin/orders/$oid/status", {"status": "shipping"}, "$tokenU", {}),
        ("PUT", "/api/orders/$oid/cancel", {}, "$tokenU", {}),
        ("GET", "/api/orders/$oid", None, None, {})]),
    "B-10": ("admin/orders/:id/status cho phep canceled -> delivered", [
        dk_u, li_u,
        ("POST", "/api/checkout", {"total_amount": 500000, "shipping_address": "1 Le Loi"}, "$tokenU", {"oid": "orderId"}),
        ("PUT", "/api/orders/$oid/cancel", {}, "$tokenU", {}),
        ("PUT", "/api/admin/orders/$oid/status", {"status": "delivered"}, "$tokenU", {}),
        ("GET", "/api/orders/$oid", None, None, {})]),
    "B-11": ("POST /api/coupon-usage ghi nhan luot dung cho coupon_id khong ton tai", [
        dk_u, li_u, ("POST", "/api/coupon-usage", {"coupon_id": 999999}, "$tokenU", {})]),
    "B-12": ("checkout tao duoc don hang khi thieu han shipping_address", [
        dk_u, li_u,
        ("POST", "/api/checkout", {"total_amount": 100}, "$tokenU", {"oid": "orderId"}),
        ("GET", "/api/orders/$oid", None, None, {})]),
    "B-14": ("checkout tra 200 thay vi 201 Created cho thao tac tao tai nguyen", [
        dk_u, li_u,
        ("POST", "/api/checkout", {"total_amount": 500000, "shipping_address": "1 Le Loi"}, "$tokenU", {})]),
    "C-01": ("POST/PUT/DELETE /api/products hoan toan khong xac thuc", [
        ("POST", "/api/products", {"name": "Khach vang lai " + SID, "price": 1,
                                   "description": "x", "imageUrl": "", "category_id": 1}, None, {"pid": "id"}),
        ("PUT", "/api/products/$pid", {"name": "Bi sua khong can token", "price": 2,
                                       "description": "x", "imageUrl": "", "category_id": 1}, None, {}),
        ("DELETE", "/api/products/$pid", None, None, {})]),
    "C-02": ("GET /api/products?search= noi chuoi SQL truc tiep - SQL Injection", [
        ("GET", "/api/products?search=%25%27%20OR%20%271%27%3D%271", None, None, {}),
        ("GET", "/api/products?search=%25%27%20UNION%20SELECT%20id%2Cemail%2Cpassword%2Crole%2C1%2C1%20FROM%20users--%20",
         None, None, {})]),
    "C-03": ("Loi SQL tra ve HTML kem thong diep cua tang CSDL thay vi JSON", [
        ("GET", "/api/products?search=%27", None, None, {})]),
    "C-04": ("GET /api/products/:id voi id khong ton tai tra 200 {} thay vi 404", [
        ("GET", "/api/products/999999", None, None, {})]),
    "C-05": ("price la number voi id le nhung la string voi id chan", [
        ("GET", "/api/products/1", None, None, {}),
        ("GET", "/api/products/2", None, None, {})]),
    "C-06": ("POST /api/products khong validate gi: gia am, gia la chuoi, ten null deu duoc chap nhan", [
        ("POST", "/api/products", {"name": "Gia am " + SID, "price": -100,
                                   "description": "x", "imageUrl": "", "category_id": 1}, None, {}),
        ("POST", "/api/products", {"name": None, "price": "abc",
                                   "description": "x", "imageUrl": "", "category_id": 1}, None, {})]),
    "C-07": ("PUT /api/products/:id voi id khong ton tai van tra 200 Product updated", [
        ("PUT", "/api/products/999999", {"name": "Khong ton tai", "price": 1,
                                         "description": "x", "imageUrl": "", "category_id": 1}, None, {})]),
    "C-08": ("DELETE /api/products/:id voi id khong ton tai van tra 200 Product deleted", [
        ("DELETE", "/api/products/999999", None, None, {})]),
    "C-09": ("PUT khong ho tro cap nhat mot phan: truong khong gui bi ghi de thanh null", [
        ("POST", "/api/products", {"name": "Day du " + SID, "price": 150000,
                                   "description": "Mo ta day du", "imageUrl": "https://e.com/a.png",
                                   "category_id": 2}, None, {"pid": "id"}),
        ("PUT", "/api/products/$pid", {"name": "Chi doi ten " + SID}, None, {}),
        ("GET", "/api/products/$pid", None, None, {})]),
    "C-10": ("category_id khong duoc kiem khoa ngoai: tao duoc san pham thuoc danh muc khong ton tai", [
        ("POST", "/api/products", {"name": "Danh muc la " + SID, "price": 1000,
                                   "description": "x", "imageUrl": "", "category_id": 9999}, None, {"pid": "id"}),
        ("GET", "/api/categories", None, None, {})]),
    "C-11": ("name va description khong duoc sanitize: payload script duoc luu nguyen van", [
        ("POST", "/api/products", {"name": "<script>alert('" + SID + "')</script>", "price": 1000,
                                   "description": "<img src=x onerror=alert(1)>", "imageUrl": "",
                                   "category_id": 1}, None, {"pid": "id"}),
        ("GET", "/api/products/$pid", None, None, {})]),
    "C-13": ("Mot san pham co price = null lam SAP HAN backend khi doc lai (tu choi dich vu)", [
        # Dùng sản phẩm id = 2 có sẵn từ seed. Phải là id CHẴN: nhánh gây sập chỉ chạy khi
        # row.id % 2 === 0. Nếu tạo sản phẩm mới thì id là ngẫu nhiên chẵn/lẻ và bug sẽ không
        # tái hiện được một cách ổn định.
        ("GET", "/api/products/2", None, None, {}),
        # PUT thieu truong -> price bi ghi de thanh null (day la bug C-09)
        ("PUT", "/api/products/2", {"name": "Chi con ten " + SID}, None, {}),
        # Đọc lại sản phẩm id chẵn: server chạy row.price.toString() trên null -> TypeError
        # không ai bắt -> tiến trình Node thoát hẳn.
        ("GET", "/api/products/2", None, None, {}),
        # Bat ky request nao sau do cung Connection refused: toan bo API da chet.
        ("GET", "/api/products", None, None, {})]),
    "C-12": ("POST /api/products tra 200 thay vi 201 Created", [
        ("POST", "/api/products", {"name": "Ma trang thai " + SID, "price": 1000,
                                   "description": "x", "imageUrl": "", "category_id": 1}, None, {})]),
    }


def con_song(base):
    try:
        urllib.request.urlopen(base + "/api/products", timeout=5).read()
        return True
    except Exception:
        return False


def khoi_dong_lai(base, sut_dir):
    """Khoi dong lai SUT sau khi no bi sap.

    Can thiet vi chinh mot trong cac bug (C-13) lam tien trinh Node thoat han: mot san pham
    co price = null se khien GET /api/products/:id goi null.toString() va nem TypeError khong
    ai bat. Neu khong khoi dong lai, moi kich ban chay sau do se "tai hien" ra Connection
    refused thay vi bug that cua no.
    """
    if not sut_dir or not os.path.isdir(sut_dir):
        return False
    subprocess.run(["bash", "-c", "pkill -f '[n]ode serv'\''er.js' >/dev/null 2>&1 || true"])
    time.sleep(1)
    subprocess.run(["bash", "-c",
                    "cd %s && setsid --fork node server.js > /tmp/eshop_capture.log 2>&1 < /dev/null"
                    % sut_dir])
    for _ in range(30):
        if con_song(base):
            return True
        time.sleep(1)
    return False


def dot(obj, path):
    for k in path.split("."):
        if obj is None:
            return None
        obj = obj.get(k) if isinstance(obj, dict) else None
    return obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://localhost:3000")
    ap.add_argument("--out", default="bugs/evidence")
    ap.add_argument("--sut-dir", default="", help="thu muc backend cua SUT, de khoi dong lai khi no bi sap")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    tong = 0
    chi_muc = []
    for bug, (mo_ta, buoc) in sorted(kich_ban().items()):
        if not con_song(a.base):
            print("  [!] SUT dang khong phan hoi (kich ban truoc lam no sap) - khoi dong lai...")
            if not khoi_dong_lai(a.base, a.sut_dir):
                print("  [LOI] khong khoi dong lai duoc SUT. Dung lai.")
                break
        slug = bug.lower().replace("-", "")
        ctx = {"U": "api.%s.victim.%s@test.local" % (slug, SID),
               "A": "api.%s.attacker.%s@test.local" % (slug, SID)}
        ghi = ["# Bang chung tai hien bug %s" % bug, "",
               "**%s**" % mo_ta, "",
               "Thu tu %d buoc duoi day duoc chay tu dong bang" % len(buoc),
               "`agent-skill/eshop-api-23127060/scripts/capture_bug_evidence.py` tren",
               "`%s` luc %s." % (a.base, time.strftime("%Y-%m-%d %H:%M:%S %z")),
               "Buoc CUOI CUNG la buoc phoi bay bug; cac buoc truoc chi dung de chuan bi trang thai.", ""]
        for i, (m, p, b, tok, setv) in enumerate(buoc, 1):
            r = goi(a.base, m, p, b, tok, ctx)
            for ten, duong in setv.items():
                v = dot(r["json"], duong)
                if v is not None:
                    ctx[ten] = v
            nhan = "**BUOC %d/%d — PHOI BAY BUG**" % (i, len(buoc)) if i == len(buoc) else "Buoc %d/%d (chuan bi)" % (i, len(buoc))
            ghi += ["## %s" % nhan, "", "```bash", curl(a.base, r), "```", "",
                    "```http",
                    "HTTP/1.1 %s" % r["code"],
                    "Content-Type: %s" % (r["content_type"] or "(khong co)"),
                    "",
                    r["raw"][:1200] + ("\n... (da cat bot)" if len(r["raw"]) > 1200 else ""),
                    "```", ""]
        p = os.path.join(a.out, "%s.md" % bug)
        open(p, "w", encoding="utf-8").write("\n".join(ghi) + "\n")
        chi_muc.append((bug, mo_ta, len(buoc)))
        tong += 1
        print("  %-6s %d buoc -> %s" % (bug, len(buoc), p))

    idx = ["# Chi muc bang chung tai hien bug", "",
           "Sinh tu dong bang `capture_bug_evidence.py`. Moi file chua nguyen van cap",
           "request/response cua tung buoc.", "",
           "| Bug | Mo ta | So buoc | File |", "|---|---|---|---|"]
    for bug, mo_ta, n in chi_muc:
        idx.append("| **%s** | %s | %d | [`%s.md`](%s.md) |" % (bug, mo_ta, n, bug, bug))
    open(os.path.join(a.out, "README.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print("\nDa thu bang chung cho %d bug -> %s/" % (tong, a.out))


if __name__ == "__main__":
    main()
