#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_bug_report.py - Sinh bugs/BUG_REPORT.md va bugs/ISSUE_TEMPLATES/*.md.

  python3 make_bug_report.py

Phan mo ta / muc do / de xuat sua duoc viet tay trong bang BUGS duoi day. Phan request va
response thi KHONG go tay: no duoc trich thang tu bugs/evidence/<ID>.md, tuc la tu lan chay
that cua capture_bug_evidence.py. Nho vay khong the co chuyen bao cao ghi mot dang response
ma he thong tra ve mot dang khac.
"""
import os
import re

SID = "23127060"

# (id, muc do, tieu de, API, tham chieu vi pham, anh huong, de xuat sua)
BUGS = [
# ---------------- API-1 ----------------
("A-01", "Critical", "`POST /api/forgot-password` tra thang ma OTP trong response body", "API-1",
 "SEC-07, FR-03",
 "Bat ky ai biet dia chi email cua nan nhan deu chiem duoc tai khoan trong hai request, khong "
 "can truy cap hop thu. Day la duong chiem tai khoan ngan nhat trong toan he thong: goi "
 "forgot-password de lay OTP, roi goi reset-password de dat mat khau moi.",
 "Bo `resetToken` khoi response. Gui OTP qua email. Trong moi truong demo, ghi ra log may chu "
 "chu khong tra ve cho client."),
("A-02", "High", "OTP chi co 4 chu so trong khi dac ta doi toi thieu 6", "API-1", "SEC-07, FR-03",
 "Khong gian ma chi 9000 gia tri (1000-9999). Khong co gioi han so lan thu nen do het toan bo "
 "khong gian la kha thi. Nghiem trong hon: voi 4 chu so, chi can khoang 100 nguoi cung dang cho "
 "reset la xac suat co hai nguoi trung ma vuot 40% (nghich ly ngay sinh) - khi do dieu kien "
 "`email AND reset_token` khong con bao ve duoc ai.",
 "`Math.floor(100000 + Math.random() * 900000)` cho 6 chu so, va tot hon la dung "
 "`crypto.randomInt` thay vi `Math.random` (khong an toan ve mat mat ma)."),
("A-03", "High", "User enumeration qua ma trang thai cua `forgot-password`", "API-1", "FR-03",
 "Email khong ton tai tra 404, email ton tai tra 200. Ke tan cong do duoc toan bo danh sach "
 "nguoi dung cua he thong chi bang cach thu lan luot cac dia chi email.",
 "Luon tra ve 200 voi cung mot thong diep chung chung, bat ke email co ton tai hay khong."),
("A-05", "High", "`reset-password` khong kiem tra do manh mat khau", "API-1", "FR-01, FR-03",
 "SRS doi mat khau toi thieu 8 ky tu, co chu hoa, chu thuong, chu so va ky tu dac biet. Thuc te "
 "chap nhan ca chuoi mot ky tu `\"1\"`. Nguoi dung di qua luong quen mat khau se dat duoc mot mat "
 "khau ma luong dang ky khong bao gio cho phep.",
 "Tach phep kiem do manh mat khau thanh mot ham dung chung, goi o ca `register` lan `reset-password`."),
("A-07", "Critical", "Mat khau luu plaintext va bi tra ve trong response cua `login` / `users/me`", "API-1", "SEC-01",
 "Cot `password` luu nguyen van. `SELECT *` roi `res.json(user)` dua ca `password` lan "
 "`reset_token` ra ngoai. Bat ky ai xem duoc mot response login (log, proxy, cache trinh duyet) "
 "deu co mat khau that. Vi nguoi dung thuong dung lai mat khau, thiet hai vuot ra ngoai he thong nay.",
 "Bam mat khau bang `bcrypt` khi ghi. Khi doc, chon dung cot can dung thay vi `SELECT *`, hoac "
 "loai bo `password` va `reset_token` truoc khi tra ve."),
("A-08", "Medium", "`forgot-password` bo qua bien loi cua `db.get` nen loi CSDL bi bao thanh 404", "API-1", "FR-03",
 "Callback nhan `(err, user)` nhung chi kiem `if (!user)`. Moi su co tang CSDL deu bien thanh "
 "\"User not found\", che mat su co that va lam nguoi dung tuong tai khoan cua ho khong ton tai.",
 "Kiem `if (err) return res.status(500).json({ error: 'Internal error' })` truoc khi kiem `!user`."),
("A-09", "High", "Bo dem dang nhap sai cong +2 moi lan nen tai khoan bi khoa o lan sai thu HAI", "API-1", "FR-02",
 "SRS quy dinh khoa tu lan sai thu ba va khoa 30 giay. Thuc te: `user.login_attempts + 2` nen "
 "dat nguong 3 ngay o lan sai thu hai, va thoi gian khoa la `180000` ms = 180 giay, gap sau lan "
 "quy dinh. Nguoi dung go nham mat khau hai lan bi khoa ba phut.",
 "Doi `+ 2` thanh `+ 1` va `180000` thanh `30000`."),
# ---------------- lien API ----------------
("X-01", "Critical", "`PUT /api/users/me` cho phep user thuong tu nang `role` len `admin`", "lien API",
 "SEC-06, FR-04, FR-12",
 "Endpoint nhan truong `role` tu body va ghi thang vao CSDL. Bat ky tai khoan nao cung tu tro "
 "thanh admin bang mot request. Ket hop voi viec cac API admin khac chi kiem su ton tai cua "
 "token, day la duong leo thang quyen tron ven.",
 "Bo `role` khoi danh sach truong duoc phep cap nhat. Chi cho phep dung ba truong `name`, "
 "`phone`, `shipping_address` nhu SRS FR-04 quy dinh."),
# ---------------- API-2 ----------------
("B-01", "Critical", "`checkout` tin tuyet doi `total_amount` do client gui", "API-2", "FR-08",
 "SRS FR-08 ghi ro: \"Backend phai tu tinh lai tong tien; khong chap nhan gia tri `total_amount` "
 "do client gui len\". Thuc te gia tri duoc ghi thang vao bang `orders`. Mua duoc dien thoai 30 "
 "trieu voi gia 1 dong. Day la lo hong gay thiet hai tai chinh truc tiep.",
 "Bo `total_amount` khoi body. Tinh lai tu gio hang phia may chu: doc `userCarts[userId]`, tra "
 "cuu gia tung san pham trong bang `products`, roi cong lai."),
("B-01b", "Critical", "`checkout` chap nhan `total_amount` am", "API-2", "FR-08",
 "Truong hop rieng cua B-01 nhung dang chu y rieng: don hang co tong tien am duoc tao thanh cong. "
 "Neu he thong co buoc hoan tien hoac tinh doanh thu, so am se lam sai toan bo so sach.",
 "Sau khi tu tinh lai tong tien phia may chu, them rang buoc `CHECK (total_amount > 0)` o tang CSDL."),
("B-02", "Critical", "`GET /api/orders/:id` thieu han xac thuc - IDOR", "API-2", "SEC-02",
 "Endpoint khong co middleware `authenticateToken`. Bat ky ai duyet lan luot id tu 1 deu doc "
 "duoc toan bo don hang cua moi nguoi dung: dia chi giao hang, tong tien, trang thai. Day la lo "
 "lot du lieu ca nhan tren dien rong.",
 "Them `authenticateToken` vao endpoint, va them dieu kien `AND user_id = ?` vao cau truy van "
 "de nguoi dung chi doc duoc don cua chinh minh."),
("B-03", "Critical", "`PUT /api/admin/orders/:id/status` khong kiem tra `role`", "API-2", "SEC-03, FR-12",
 "Endpoint co `authenticateToken` nhung khong he doc `req.user.role`. Bat ky nguoi dung dang "
 "nhap nao cung doi duoc trang thai don hang cua nguoi khac - vi du danh dau don cua nguoi khac "
 "la da giao de chan viec huy don.",
 "Them middleware kiem quyen: `if (req.user.role !== 'admin') return res.status(403).json(...)`. "
 "Ap cho toan bo nhom duong dan `/api/admin/*`."),
("B-05", "Critical", "Cong thuc giam gia `percent` sai dau, cho ra so tien giam AM", "API-2", "FR-09",
 "Code tinh `discount = Math.floor(total * (1 - discount_value))`. Voi `discount_value = 10` "
 "(nghia la 10%), cong thuc thanh `total * (1 - 10) = total * (-9)`. Voi don 500.000d, `discount_amount` "
 "la **-4.500.000** va `final_amount` thanh **5.000.000** - khach hang bi tinh gap muoi lan khi ap "
 "ma giam gia. SRS FR-09 ghi ro cong thuc dung la `total * discount_value / 100`.",
 "Sua thanh `Math.floor(total_amount * coupon.discount_value / 100)`."),
("B-06", "High", "Nguong don toi thieu dung `>` thay vi `>=`", "API-2", "FR-09",
 "SRS FR-09 dieu kien C3 ghi ro \"Tong don hang **>= (lon hon hoac bang)** `min_order_amount`\". "
 "Code viet `if (total_amount > coupon.min_order_amount)`. Don co gia tri bang dung nguong bi tu "
 "choi. Day la loi bien kinh dien, va no roi dung vao truong hop nguoi dung hay gap nhat: mua vua "
 "du nguong de duoc giam gia.",
 "Doi `>` thanh `>=`."),
("B-07", "Critical", "`apply-coupon` khong xac thuc; bo `user_id` la bo qua toan bo kiem tra han muc", "API-2",
 "SEC-02, FR-09",
 "Endpoint khong co `authenticateToken` va lay `user_id` tu body. Nghiem trong hon: phep kiem han "
 "muc nam trong nhanh `if (user_id)`, nen **khong gui** truong nay se di vao nhanh `else` va ap ma "
 "ma khong dem luot nao ca. Day la nghich ly \"bo bot du lieu de duoc nhieu quyen hon\": ma gioi han "
 "mot luot moi nguoi tro thanh dung duoc vo han.",
 "Them `authenticateToken` va lay `user_id` tu `req.user.id`, khong bao gio tu body. Bo hoan toan "
 "nhanh `else`."),
("B-08", "Medium", "Kiem tra han su dung nam ben trong nhanh nguong don nen thong bao loi sai nguyen nhan", "API-2",
 "FR-09",
 "Phep kiem `expired_at` duoc long ben trong `if (total_amount > min_order_amount)`. Mot ma da het "
 "han dung cho don nho hon nguong se bao \"chua du gia tri toi thieu\" thay vi \"ma da het han\". "
 "Nguoi dung se co mua them hang de dat nguong roi van bi tu choi.",
 "Tach nam dieu kien C1-C5 cua FR-09 thanh nam phep kiem doc lap, chay theo dung thu tu uu tien va "
 "moi phep kiem tra ve thong bao rieng."),
("B-09", "High", "`PUT /api/orders/:id/cancel` cho phep huy don dang giao (`shipping`)", "API-2", "FR-10",
 "SRS FR-10 ghi ro: \"Khi don hang da o trang thai `shipping`, User khong duoc phep tu huy - chi "
 "Admin moi co the thao tac\". Code chi chan `delivered` va `canceled`. Khach hang huy don khi hang "
 "dang tren duong giao, gay that thoat hang va chi phi van chuyen. Chinh comment trong ma nguon cung "
 "thua nhan dieu kien nay sai.",
 "Doi dieu kien thanh `if (order.status !== 'pending' && order.status !== 'confirmed')` dung nhu "
 "comment trong ma nguon da ghi."),
("B-10", "High", "`admin/orders/:id/status` cho phep chuyen `canceled` -> `delivered`", "API-2", "FR-10",
 "SRS FR-10 ghi ro `delivered` va `canceled` la **trang thai ket thuc**, khong duoc chuyen sang bat "
 "ky trang thai nao khac. Trong ma nguon co mot dong rieng biet `if (currentStatus === 'canceled' && "
 "status === 'delivered') isValidTransition = true` - mot don da huy co the bi danh dau la da giao.",
 "Xoa dong do. Tot hon: thay chuoi `if` bang mot bang chuyen trang thai khai bao duoc, de so do "
 "FR-10 va ma nguon doc ra cung mot thu."),
("B-11", "Medium", "`POST /api/coupon-usage` ghi nhan luot dung cho `coupon_id` khong ton tai", "API-2", "FR-09",
 "Khong kiem tra ma giam gia co ton tai khong, cung khong gan voi don hang nao. Ke tan cong tao "
 "duoc ban ghi rac, hoac chen luot dung gia cho tai khoan nguoi khac de ho khong dung duoc ma nua.",
 "Kiem `coupon_id` ton tai va gan ban ghi voi `order_id` that. Tot nhat la ghi nhan luot dung ngay "
 "trong giao dich thanh toan thay vi de client goi mot endpoint rieng."),
("B-12", "Medium", "`checkout` tao duoc don hang khi thieu han `shipping_address`", "API-2", "FR-08",
 "Khong co phep kiem nao. Don hang duoc tao voi dia chi giao hang `null`, khong the giao duoc va "
 "chi phat hien ra o khau van hanh.",
 "Kiem `shipping_address` bat buoc va khong rong truoc khi ghi; hoac lay dia chi mac dinh tu ho so "
 "nguoi dung khi client khong gui."),
("B-14", "Low", "`checkout` tra ve 200 thay vi 201 Created", "API-2", "FR-08",
 "Thao tac tao tai nguyen moi phai tra `201 Created`. Khong gay hai truc tiep nhung pha vo quy uoc "
 "REST va lam client kho phan biet \"da tao\" voi \"da co san\".",
 "`res.status(201).json({ ... })`."),
# ---------------- API-3 ----------------
("C-01", "Critical", "`POST` / `PUT` / `DELETE /api/products` hoan toan khong xac thuc", "API-3",
 "SEC-02, SEC-03, FR-12",
 "SRS FR-12 liet ke dich danh ba endpoint nay trong nhom bat buoc phai co token JWT hop le **va** "
 "`role = 'admin'`. Thuc te khong co middleware nao ca. Mot nguoi hoan toan khong dang nhap co the "
 "xoa sach toan bo catalog san pham, hoac sua gia moi mat hang ve 0. Day la bug nghiem trong nhat "
 "cua API-3.",
 "Them `authenticateToken` va middleware kiem `role === 'admin'` cho ca ba endpoint."),
("C-02", "Critical", "SQL Injection qua tham so `?search=`", "API-3", "SEC-05",
 "Cau truy van duoc noi chuoi truc tiep: ``WHERE name LIKE '%${searchQuery}%'``. Payload "
 "`%' OR '1'='1` tra ve toan bo bang. Nghiem trong hon, payload `UNION SELECT` doc duoc bang "
 "`users`: lan chay thu nghiem tra ve nguyen van `admin@eshop.com` kem mat khau `Admin123!` trong "
 "truong `price`. Ket hop voi A-07 (mat khau luu plaintext), mot request duy nhat lay duoc thong tin "
 "dang nhap cua quan tri vien.",
 "Dung tham so hoa: `db.all(\"SELECT * FROM products WHERE name LIKE ?\", ['%' + searchQuery + '%'], ...)`. "
 "Day dung la dieu SEC-05 yeu cau."),
("C-03", "High", "Loi SQL tra ve HTML kem thong diep cua tang CSDL", "API-3", "SEC-05",
 "Khi truy van loi, may chu tra `res.status(500).send('<h1>Database Error</h1><p>' + err.message + '</p>')` "
 "voi `Content-Type: text/html`. Hai hau qua: lo cau truc CSDL cho ke tan cong (giup tinh chinh payload "
 "SQLi), va pha vo hop dong JSON khien client goi `response.json()` bi nem loi.",
 "Tra ve `res.status(500).json({ error: 'Internal server error' })`. Ghi `err.message` vao log may chu, "
 "khong gui cho client."),
("C-04", "High", "`GET /api/products/:id` voi id khong ton tai tra `200 {}` thay vi `404`", "API-3", "FR-15",
 "Dong `if (!row) return res.status(200).json({})` tra ve thanh cong cho mot tai nguyen khong ton tai. "
 "Client khong phan biet duoc \"khong tim thay\" voi \"tim thay nhung rong\", va lop hien thi se ve ra "
 "mot san pham trong thay vi bao loi.",
 "`return res.status(404).json({ error: 'Product not found' })`."),
("C-05", "High", "`price` la so voi id le nhung la chuoi voi id chan", "API-3", "FR-15",
 "Dong `if (row.id % 2 === 0) row.price = row.price.toString()` doi kieu du lieu theo tinh chan le "
 "cua khoa chinh. Client cong tien se nhan `\"28000000\" + 1000` ra chuoi `\"280000001000\"`. Bug chi lo "
 "ra khi so sanh hai response voi nhau; test rieng tung response deu thay hop le.",
 "Xoa dong do. Them rang buoc kieu vao hop dong API va kiem bang JSON Schema trong bo test hoi quy."),
("C-06", "High", "`POST /api/products` khong validate bat ky truong nao", "API-3", "FR-15",
 "SRS FR-15 doi: ten bat buoc toi da 255 ky tu, gia bat buoc va phai duong, danh muc bat buoc chon tu "
 "danh sach co san. Thuc te tao duoc san pham voi `price: -100`, `price: \"abc\"`, `name: null`. Du lieu "
 "hong di vao CSDL va gay hau qua day chuyen - xem C-13.",
 "Them tang validate dau vao (vi du `express-validator` hoac mot ham kiem tay) truoc khi ghi."),
("C-07", "Medium", "`PUT /api/products/:id` voi id khong ton tai van tra `200 Product updated`", "API-3", "FR-15",
 "Callback khong doc `this.changes`, nen khong phan biet duoc \"da cap nhat 1 dong\" voi \"khong dong "
 "nao khop\". Client tuong da luu thanh cong trong khi khong co gi thay doi.",
 "`if (this.changes === 0) return res.status(404).json({ error: 'Product not found' })`."),
("C-08", "Medium", "`DELETE /api/products/:id` voi id khong ton tai van tra `200 Product deleted`", "API-3", "FR-15",
 "Cung nguyen nhan voi C-07.",
 "Kiem `this.changes` truoc khi tra ve thanh cong."),
("C-09", "Medium", "`PUT` khong ho tro cap nhat mot phan: truong khong gui bi ghi de thanh `null`", "API-3", "FR-15",
 "Cau `UPDATE products SET name=?, price=?, description=?, imageUrl=?, category_id=?` luon ghi ca nam "
 "cot. Gui mot body chi co `name` se xoa trang bon truong con lai. Lan chay thu nghiem cho ket qua "
 "`{\"price\": null, \"description\": null, \"imageUrl\": null, \"category_id\": null}`. Day la nguyen nhan "
 "truc tiep cua C-13.",
 "Dung cau `UPDATE` dong chi gom cac truong that su co mat trong body, hoac doi hoi PUT phai gui du "
 "va dung `PATCH` cho cap nhat mot phan."),
("C-10", "Medium", "`category_id` khong duoc kiem khoa ngoai", "API-3", "FR-15",
 "Tao duoc san pham voi `category_id = 9999` trong khi bang `categories` chi co id 1, 2, 3. San pham "
 "tro toi mot danh muc khong ton tai va se khong hien ra o bat ky bo loc theo danh muc nao.",
 "Kiem `category_id` ton tai truoc khi ghi, va khai bao `FOREIGN KEY (category_id) REFERENCES "
 "categories(id)` trong `database.js` kem `PRAGMA foreign_keys = ON`."),
("C-11", "Medium", "`name` va `description` khong duoc sanitize - nguon cua stored XSS", "API-3", "SEC-04",
 "Payload `<script>` va `<img src=x onerror=>` duoc luu nguyen van vao CSDL va tra ve nguyen van. "
 "SEC-04 doi du lieu nguoi dung nhap phai duoc escape khi hien thi. **Gioi han cua phep kiem nay:** o "
 "tang API chi chung minh duoc **nua nguon** - rang may chu luu payload tho. Viec no co thuc su chay "
 "tren trinh duyet hay khong con phu thuoc vao lop hien thi, phai kiem rieng o tang giao dien.",
 "Escape khi hien thi (khong dung `dangerouslySetInnerHTML`), va loc dau vao ngay o tang API nhu mot "
 "lop phong thu thu hai."),
("C-12", "Low", "`POST /api/products` tra ve 200 thay vi 201 Created", "API-3", "FR-15",
 "Cung loai voi B-14.",
 "`res.status(201).json({ ... })`."),
("C-13", "Critical", "Mot san pham co `price = null` lam SAP HAN backend khi doc lai (tu choi dich vu)", "API-3",
 "FR-15",
 "Day la bug nguy hiem nhat tim duoc, va no la **he qua day chuyen cua hai bug khac**. "
 "C-09 cho phep mot lenh `PUT` thieu truong ghi de `price` thanh `null`. Sau do, C-05 chay "
 "`row.price.toString()` tren gia tri `null` khi id la so chan. `TypeError` nem ra trong callback cua "
 "`sqlite3` khong duoc ai bat, Node thoat han, **toan bo API ngung phuc vu**. Trong lan chay thu "
 "nghiem, request tiep theo tra ve `Connection refused` va moi kich ban sau do khong chay duoc nua. "
 "Mot nguoi khong dang nhap co the ha guc toan bo he thong bang **hai** request (C-01 cho phep goi "
 "`PUT` ma khong can token). Khong bug nao trong ba bug thanh phan tu no gay sap; chi to hop cua "
 "chung moi gay.",
 "Sua ca ba: (1) C-01 them xac thuc; (2) C-09 chi cap nhat truong duoc gui; (3) C-05 xoa dong ep kieu. "
 "Ngoai ra bat buoc phai co `process.on('uncaughtException')` va mot tang xu ly loi cho moi callback "
 "cua tang CSDL, de mot ban ghi hong khong the ha duoc ca tien trinh."),
]

SEV_ICON = {"Critical": "🔴 Critical", "High": "🟠 High", "Medium": "🟡 Medium", "Low": "⚪ Low"}


def lay_buoc_cuoi(bug):
    """Trich curl + response cua buoc PHOI BAY BUG tu file bang chung."""
    p = "bugs/evidence/%s.md" % bug
    if not os.path.exists(p):
        return None, None
    t = open(p, encoding="utf-8").read()
    i = t.find("PHOI BAY BUG")
    if i < 0:
        return None, None
    khoi = re.findall(r"```(?:bash|http)\n(.*?)```", t[i:], re.S)
    return (khoi[0].strip() if khoi else None), (khoi[1].strip() if len(khoi) > 1 else None)


def main():
    os.makedirs("bugs/ISSUE_TEMPLATES", exist_ok=True)
    thu_tu = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    bugs = sorted(BUGS, key=lambda b: (thu_tu[b[1]], b[0]))

    L = ["# BUG REPORT — HW06 API Testing", "",
         "> SV **Ninh Van Khai — %s** | SUT: EShop @ `85af3ba` | De bai muc 6.5" % SID, "",
         "Moi bug trong tai lieu nay deu **tai hien duoc bang request that**. Phan `curl` va phan "
         "response o tung muc duoc trich thang tu `bugs/evidence/<ID>.md` — la ket qua cua mot lan "
         "chay that bang `scripts/capture_bug_evidence.py`, khong go tay.", "",
         "Chay lai toan bo bang chung:", "", "```bash",
         "python3 agent-skill/eshop-api-%s/scripts/capture_bug_evidence.py \\" % SID,
         "  --base http://localhost:3000 --out bugs/evidence \\",
         "  --sut-dir ../../../../eshop-sut/backend", "```", "",
         "---", "", "## 1. Bang tong hop", "",
         "| ID | Muc do | Tieu de | API | Vi pham | Bang chung | GitHub Issue |",
         "|---|---|---|---|---|---|---|"]
    dem = {}
    for bid, sev, tt, api, ref, _, _ in bugs:
        dem[sev] = dem.get(sev, 0) + 1
        L.append("| **%s** | %s | %s | %s | %s | [`%s.md`](evidence/%s.md) | `<dien link>` |"
                 % (bid, SEV_ICON[sev], tt, api, ref, bid, bid))
    L += ["", "**Tong %d bug:** %d Critical, %d High, %d Medium, %d Low."
          % (len(bugs), dem.get("Critical", 0), dem.get("High", 0),
             dem.get("Medium", 0), dem.get("Low", 0)), ""]

    theo_api = {}
    for b in bugs:
        theo_api[b[3]] = theo_api.get(b[3], 0) + 1
    L += ["| API | So bug |", "|---|---|"]
    for k in sorted(theo_api):
        L.append("| %s | %d |" % (k, theo_api[k]))
    L += ["", "De bai doi toi thieu 3 bug that cho moi API; ca ba deu vuot xa nguong nay.", "",
          "---", "", "## 2. Chi tiet tung bug", ""]

    for bid, sev, tt, api, ref, tac_dong, sua in bugs:
        c, r = lay_buoc_cuoi(bid)
        L += ["### %s — %s" % (bid, tt), "",
              "| | |", "|---|---|",
              "| **Muc do** | %s |" % SEV_ICON[sev],
              "| **API** | %s |" % api,
              "| **Vi pham** | %s |" % ref,
              "| **Bang chung day du** | [`bugs/evidence/%s.md`](evidence/%s.md) |" % (bid, bid),
              "", "**Anh huong:** %s" % tac_dong, ""]
        if c:
            L += ["**Buoc tai hien** (buoc cuoi cua kich ban; cac buoc chuan bi xem file bang chung):",
                  "", "```bash", c, "```", ""]
        if r:
            L += ["**Ket qua thuc te:**", "", "```http", r, "```", ""]
        L += ["**Ket qua mong doi:** theo `eshop-sut/README.md` (%s)." % ref, "",
              "**De xuat sua:** %s" % sua, "", "---", ""]

    L += ["## 3. Cong viec con lai cua sinh vien (HUMAN H3)", "",
          "De bai muc 6.5 doi moi bug phai duoc mo thanh mot GitHub Issue **kem anh chup man hinh**.",
          "Cac file trong `bugs/ISSUE_TEMPLATES/` da san sang de dan thang len GitHub:", "",
          "1. Mo `https://github.com/<tai-khoan>/<repo>/issues/new`.",
          "2. Dan noi dung `bugs/ISSUE_TEMPLATES/<ID>.md` (dong dau la tieu de Issue).",
          "3. Gan nhan theo muc do: `critical` / `high` / `medium` / `low`, kem nhan `api-1` / `api-2` / `api-3`.",
          "4. Chup man hinh Issue vua tao, luu vao `bugs/screenshots/<ID>.png`.",
          "5. Dien so hieu Issue vao cot **GitHub Issue** cua bang o muc 1.", "",
          "> Uu tien mo Issue cho %d bug Critical truoc neu khong du thoi gian lam het."
          % dem.get("Critical", 0), ""]

    open("bugs/BUG_REPORT.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

    for bid, sev, tt, api, ref, tac_dong, sua in bugs:
        c, r = lay_buoc_cuoi(bid)
        T = ["[%s][%s] %s" % (sev.upper(), bid, tt), "",
             "> Bao cao boi Ninh Van Khai — %s | HW06 API Testing" % SID,
             "> SUT: EShop, commit `85af3ba` | Moi truong: `http://localhost:3000`", "",
             "## Muc do", "", SEV_ICON[sev], "",
             "## Yeu cau bi vi pham", "", "`%s` — theo `eshop-sut/README.md`" % ref, "",
             "## Anh huong", "", tac_dong, ""]
        if c:
            T += ["## Buoc tai hien", "", "```bash", c, "```", ""]
        if r:
            T += ["## Ket qua thuc te", "", "```http", r, "```", ""]
        T += ["## Ket qua mong doi", "",
              "Theo `%s` trong dac ta cua he thong." % ref, "",
              "## De xuat sua", "", sua, "",
              "## Bang chung day du", "",
              "Toan bo chuoi request/response tai hien: `bugs/evidence/%s.md`" % bid, ""]
        open("bugs/ISSUE_TEMPLATES/%s.md" % bid, "w", encoding="utf-8").write("\n".join(T) + "\n")

    print("Da ghi bugs/BUG_REPORT.md (%d bug) va %d file trong bugs/ISSUE_TEMPLATES/"
          % (len(bugs), len(bugs)))


if __name__ == "__main__":
    main()
