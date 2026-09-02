# Chi muc bang chung tai hien bug

Sinh tu dong bang `capture_bug_evidence.py`. Moi file chua nguyen van cap
request/response cua tung buoc.

| Bug | Mo ta | So buoc | File |
|---|---|---|---|
| **A-01** | Response cua forgot-password tra thang ma OTP ra ngoai | 2 | [`A-01.md`](A-01.md) |
| **A-02** | OTP chi co 4 chu so trong khi SEC-07 doi toi thieu 6 | 2 | [`A-02.md`](A-02.md) |
| **A-03** | User enumeration: email khong ton tai tra 404, email ton tai tra 200 | 3 | [`A-03.md`](A-03.md) |
| **A-05** | reset-password khong kiem tra do manh mat khau | 4 | [`A-05.md`](A-05.md) |
| **A-07** | login tra ve nguyen ban ghi user gom ca password plaintext va reset_token | 3 | [`A-07.md`](A-07.md) |
| **A-08** | forgot-password bo qua bien err cua db.get nen loi CSDL bi bao thanh 404 | 1 | [`A-08.md`](A-08.md) |
| **A-09** | Bo dem dang nhap sai cong +2 moi lan nen khoa ngay o lan sai thu HAI | 4 | [`A-09.md`](A-09.md) |
| **B-01** | checkout tin tuyet doi total_amount tu client | 4 | [`B-01.md`](B-01.md) |
| **B-01b** | checkout chap nhan total_amount am | 3 | [`B-01b.md`](B-01b.md) |
| **B-02** | GET /api/orders/:id thieu xac thuc - IDOR doc don hang cua bat ky ai | 4 | [`B-02.md`](B-02.md) |
| **B-03** | PUT /api/admin/orders/:id/status khong kiem role - user thuong doi don nguoi khac | 6 | [`B-03.md`](B-03.md) |
| **B-05** | Cong thuc coupon percent sai: discount = total*(1-value) cho ra so AM | 1 | [`B-05.md`](B-05.md) |
| **B-06** | Nguong don toi thieu dung > thay vi >=: don bang dung min_order_amount bi tu choi | 2 | [`B-06.md`](B-06.md) |
| **B-07** | apply-coupon khong xac thuc; bo user_id di la bo qua toan bo kiem tra han muc | 1 | [`B-07.md`](B-07.md) |
| **B-08** | Kiem tra han su dung nam trong nhanh total > min nen thong bao loi sai nguyen nhan | 1 | [`B-08.md`](B-08.md) |
| **B-09** | PUT /api/orders/:id/cancel cho phep huy don dang shipping | 7 | [`B-09.md`](B-09.md) |
| **B-10** | admin/orders/:id/status cho phep canceled -> delivered | 6 | [`B-10.md`](B-10.md) |
| **B-11** | POST /api/coupon-usage ghi nhan luot dung cho coupon_id khong ton tai | 3 | [`B-11.md`](B-11.md) |
| **B-12** | checkout tao duoc don hang khi thieu han shipping_address | 4 | [`B-12.md`](B-12.md) |
| **B-14** | checkout tra 200 thay vi 201 Created cho thao tac tao tai nguyen | 3 | [`B-14.md`](B-14.md) |
| **C-01** | POST/PUT/DELETE /api/products hoan toan khong xac thuc | 3 | [`C-01.md`](C-01.md) |
| **C-02** | GET /api/products?search= noi chuoi SQL truc tiep - SQL Injection | 2 | [`C-02.md`](C-02.md) |
| **C-03** | Loi SQL tra ve HTML kem thong diep cua tang CSDL thay vi JSON | 1 | [`C-03.md`](C-03.md) |
| **C-04** | GET /api/products/:id voi id khong ton tai tra 200 {} thay vi 404 | 1 | [`C-04.md`](C-04.md) |
| **C-05** | price la number voi id le nhung la string voi id chan | 2 | [`C-05.md`](C-05.md) |
| **C-06** | POST /api/products khong validate gi: gia am, gia la chuoi, ten null deu duoc chap nhan | 2 | [`C-06.md`](C-06.md) |
| **C-07** | PUT /api/products/:id voi id khong ton tai van tra 200 Product updated | 1 | [`C-07.md`](C-07.md) |
| **C-08** | DELETE /api/products/:id voi id khong ton tai van tra 200 Product deleted | 1 | [`C-08.md`](C-08.md) |
| **C-09** | PUT khong ho tro cap nhat mot phan: truong khong gui bi ghi de thanh null | 3 | [`C-09.md`](C-09.md) |
| **C-10** | category_id khong duoc kiem khoa ngoai: tao duoc san pham thuoc danh muc khong ton tai | 2 | [`C-10.md`](C-10.md) |
| **C-11** | name va description khong duoc sanitize: payload script duoc luu nguyen van | 2 | [`C-11.md`](C-11.md) |
| **C-12** | POST /api/products tra 200 thay vi 201 Created | 1 | [`C-12.md`](C-12.md) |
| **C-13** | Mot san pham co price = null lam SAP HAN backend khi doc lai (tu choi dich vu) | 4 | [`C-13.md`](C-13.md) |
| **X-01** | PUT /api/users/me cho phep user thuong tu nang role len admin | 4 | [`X-01.md`](X-01.md) |
