# VIDEO_SCRIPT — Kich ban quay demo bo sinh test (khoang 6 phut)

> HW06 — SV **Ninh Van Khai — 23127060** | De bai muc 7 (khuyen khich, khong bat buoc)
>
> *"You are encouraged to implement it as a reusable Agent Skill and submit a demonstration
> video (YouTube link) showing it generate tests for one API."*

Chon **API-3 (FR-15 — quan ly san pham)** de demo: no co tham so o ca ba vi tri (body, path,
query), va co bug SQL Injection de ket thuc video bang mot ket qua an tuong.

---

## Chuan bi truoc khi bam ghi

```bash
cd 23127060
# CSDL ve trang thai goc
pkill -f "[n]ode serv""er.js"; sleep 1
( cd ../../../../eshop-sut/backend && setsid --fork node server.js ) > /tmp/sut.log 2>&1 < /dev/null
curl -sf http://localhost:3000/api/products > /dev/null && echo "SUT san sang"
# don dep dau ra cu de quay cho sach
rm -f testcases/API-3_generated.csv
```

Mo san hai cua so: mot terminal (chu to, nen toi) va mot trinh soan thao mo `spec/api-3.json`.

---

## Phan 1 — Van de (0:00–0:45)

**Noi:**
> "Chao thay co. Em la Ninh Van Khai, MSSV 23127060. Em demo bo sinh test case API cho HW06.
>
> Cach lam hien nhien la bao AI 'doc dac ta nay va viet 35 test case'. Nhung cach do co ba van
> de: chay lai cho ra ket qua khac, khong do duoc do phu, va them mot API la lam lai tu dau.
>
> Thiet ke cua em tach lam hai lop: mot lop can doc hieu — do con nguoi va AI cung lam; va mot
> lop sinh — hoan toan tat dinh, cung dau vao luon cho cung dau ra."

**Man hinh:** mo so do tu ve `agent-skill/diagram/23127060_generator_diagram.png`, chi tay vao
khoi "dich sang JSON" va cum bon bo sinh.

## Phan 2 — Dau vao (0:45–2:00)

**Noi:**
> "Day la dac ta goc cua he thong. Cau nay noi: 'Gia: bat buoc, phai la so duong'. Con nguoi doc
> ra ngay ba dieu: co tham so ten price, kieu so, va co mot bien tai 0. Chuong trinh thi khong.
>
> Nen buoc dau tien la dich cau do sang dang may doc duoc."

**Man hinh:** mo `eshop-sut/README.md` phan FR-15, roi chuyen sang `spec/api-3.json`, cuon toi
tham so `price` va doc to bon phan hoach `valid` / `zero` / `negative` / `string`.

**Noi tiep:**
> "File spec co bon truc, ung voi bon ky thuat kiem thu ma de bai yeu cau: phan hoach mien,
> chuyen trang thai, bao mat SEC-01 den 07, va kiem tra schema."

## Phan 3 — Chay bo sinh (2:00–3:30)

**Noi:** "De bai cam dung mot prompt tong, nen em chay bon vong doc lap."

```bash
python3 agent-skill/eshop-api-23127060/scripts/gen_testcases.py \
  --spec spec/api-3.json --only DOM --out testcases/API-3_generated.csv
```
> "Vong mot: phan hoach mien. 51 test case. Dong 'Tham so CHUA phu DOM: (khong)' nghia la khong
> tham so nao bi bo sot."

```bash
... --only STA --append   # 9 case
... --only SEC --append   # 14 case
... --only SCH --append   # 6 case
```
> "Bon vong, 80 test case, vuot xa nguong 35 cua de bai."

**Man hinh:** mo CSV bang `column -s, -t | less -S` hoac Excel, chi vao cot `Oracle`, `SEC_Ref`,
`Tag`.
> "Moi case ghi ro oracle la dac ta hay la hanh vi thuc te, va tag @bug nghia la case nay se
> that bai — vi no phoi bay mot loi that cua he thong."

## Phan 4 — Bo sinh tu cham do phu (3:30–4:15)

```bash
python3 agent-skill/eshop-api-23127060/scripts/gen_testcases.py --spec spec/api-2.json --stats
```
> "Bo sinh khong chi in ra test case, no con tu cham do phu cua chinh minh. Dong cuoi: 'O bang
> chuyen trang thai da test: 20 / 25'. No chi thang ra con 5 o chua phu — va do la 5 o duong
> cheo, kieu chuyen mot trang thai ve chinh no. Em bo sung tay o buoc extend."

## Phan 5 — Chay that (4:15–5:30)

```bash
python3 agent-skill/eshop-api-23127060/scripts/build_collection.py \
  --csv testcases/API-3_final.csv --api API-3 \
  --out postman/collections/23127060_HW06_API-3.postman_collection.json

bash agent-skill/eshop-api-23127060/scripts/run_newman.sh API-3
```
> "86 test case, 405 assertion, 105 that bai. Nghe nhu bo test hong, nhung khong: he thong nay
> co 34 bug that va em co y viet ky vong theo dac ta chu khong theo hanh vi thuc te."

**Man hinh:** mo bao cao HTML, cuon toi mot test SQL Injection.
> "Day la ket qua an tuong nhat: mot cau UNION SELECT qua tham so search tra ve nguyen van
> email va mat khau cua tai khoan quan tri — `admin@eshop.com` va `Admin123!`."

## Phan 6 — Con nguoi o dau (5:30–6:00)

**Noi:**
> "Bo sinh khong thay the nguoi kiem thu. Sau khi no chay xong, em van phai lam ba viec: audit
> tung case — ket qua la 68 case sai va 74 case thieu, em da sua het; them 18 case ma bo sinh
> khong the nghi ra; va quyet dinh case nao la hop dong, case nao phoi bay bug.
>
> Dang chu y nhat: mot nua so case em phai tu them la nhung bug chi lo ra khi ket hop nhieu
> request. Do la gioi han cau truc cua thiet ke hien tai, va em da viet huong mo rong cho no
> trong bao cao. Em cam on thay co."

---

## Bang kiem sau khi quay

- [ ] Video < 8 phut, tieng noi ro
- [ ] Co canh **chay that** trong terminal (khong phai anh tinh)
- [ ] Co canh mo **so do tu ve**
- [ ] Co canh mo bao cao HTML cua Newman
- [ ] Up YouTube che do **unlisted**, dien link vao `README.md` va `report/MAIN_REPORT.md`
