# DIAGRAM_BRIEF — Mo ta de SINH VIEN TU VE so do bo sinh test

> HW06 — SV **Ninh Van Khai — 23127060** | De bai muc 7 va muc 11

---

## ⚠ Quy tac bat buoc doc truoc

De bai **muc 11 (Anti-AI Cheat Constraints)** ghi ro:

> *"The AI test generator diagram, which must be self-drawn — designed by you, not generated
> directly by an AI."*

Vi vay:

- File nay **chi chua mo ta bang chu**. Trong ca thu muc `agent-skill/diagram/` **khong co**
  va **khong duoc co** bat ky file anh, file `.mmd`, khoi `mermaid`, `graphviz`, PlantUML hay
  ASCII-art nao do AI sinh ra. Neu co, do la vi pham muc 11 va bai bi tinh la gian lan.
- Sinh vien **tu ve** so do, bang cong cu tuy y (draw.io, Excalidraw, Figma, hoac ve tay roi
  chup anh — de bai chap nhan het, mien la **quyet dinh thiet ke la cua sinh vien**).
- Luu ket qua thanh `agent-skill/diagram/23127060_generator_diagram.png`.
- Nen luu them file nguon (`.drawio` / `.excalidraw`) canh file PNG: no chung minh so do do
  sinh vien dung tay dung nen, va sua lai duoc khi bao ve mieng.

Mo ta duoi day la **thong tin dau vao** de ve. Sinh vien doc va tu quyet dinh bo cuc, hinh
dang khoi, mau sac, cach dat mui ten. **Khong can ve giong het** — hieu kien truc roi ve theo
cach cua minh la dat yeu cau.

---

## 1. So do can tra loi duoc ba cau hoi

Truoc khi ve, ghi nho ba cau hoi ma nguoi cham se nhin so do de tim cau tra loi:

1. **Dau vao la gi, dau ra la gi?**
2. **Vi sao ket qua lap lai duoc?** (cung mot dau vao luon cho ra cung mot bo test)
3. **Con nguoi xen vao o dau?** (de bai coi trong diem nay: AI la tro ly co ky luat, khong
   phai hop den)

Neu so do ve xong ma khong tra loi duoc mot trong ba cau, thi con thieu.

---

## 2. Cac khoi can co

### Cot 1 — DAU VAO (ben trai)

| Khoi | Nhan goi y | Ghi chu |
|---|---|---|
| A1 | `eshop-sut/README.md` (SRS: FR-01..FR-24, SEC-01..07) | tai lieu van xuoi |
| A2 | `eshop-sut/api_specification.md` | hinh dang request/response |
| A3 | `eshop-sut/backend/server.js` | ma nguon — dung de doi chieu |

Ba khoi nay nen ve chung mot mau (mau "tai lieu"), va **ngoai duong vien** cua he thong —
chung la thu co san, khong phai thu minh xay.

### Khoi ban le — DICH SANG DANG MAY DOC DUOC

| Khoi | Nhan goi y |
|---|---|
| B | **Dich dac ta sang dang may doc duoc** → `spec/api-N.json` |

**Day la khoi quan trong nhat cua ca so do.** No nen duoc ve **to hon** cac khoi khac, va
phai the hien ro rang day la **cong doan co con nguoi tham gia** (xem muc 3).

Ly do: dac ta van xuoi khong noi ro dau la truc phan hoach. Cau *"Gia: bat buoc, phai la so
duong (> 0)"* chua ba thong tin an: ten tham so, kieu du lieu, va **mot bien tai 0**. Con
nguoi doc ra ngay; chuong trinh thi khong. Khoi B chinh la noi bien doi do xay ra.

Ben trong khoi B, ve bon o nho ung voi bon truc cua file JSON:

- `endpoints[].params[].partitions[]`
- `state_machine.transitions[]`
- `security[]`
- `schema_cases[]`

### Cot 2 — BON BO SINH (giua)

Bon khoi **song song**, moi khoi nhan dau vao tu dung mot truc tuong ung o khoi B:

| Khoi | Nhan | Ky thuat kiem thu | Ket qua bai nay |
|---|---|---|---|
| C1 | `SINH_DOMAIN` | Equivalence Partitioning, BVA, Decision Table | 128 case |
| C2 | `SINH_STATE` | State Transition Testing (0-switch) | 38 case |
| C3 | `SINH_SECURITY` | Anh xa SEC-01..SEC-07 | 41 case |
| C4 | `SINH_SCHEMA` | JSON Schema Validation | 18 case |

Ve **song song, khong noi tiep** — day la diem thiet ke co y: bon bo sinh doc lap nhau nen
chay duoc rieng tung cai (`--only DOM`, `--only STA`...). Do chinh la co so ky thuat de thoa
yeu cau *"drive it step by step, not with a single generic prompt"* cua de bai muc 6.

Nen ghi con so len tung khoi: no cho thay ngay do phu lech ve dau.

### Cot 3 — HAU XU LY (phai giua)

| Khoi | Nhan | Ghi chu |
|---|---|---|
| D | `KHU_TRUNG` | Khoa gom 7 truong — xem muc 4, day la cho dang chu thich |
| E | `DANH_SO_LAI` | `TC-<prefix>-<NHOM>-<3 chu so>` |
| F | `KIEM_TRA_DO_PHU` | **cong tac chan** — xem muc 4 |

Khoi F nen ve khac hinh (vi du hinh thoi / hinh binh hanh) vi no la diem **quyet dinh**,
khong phai diem bien doi. Tu F ve **mot mui ten quay nguoc lai khoi B**, nhan
*"chua du do phu -> bo sung vao spec roi chay lai"*. Vong lap nay la thu the hien ro nhat
rang bo sinh co kiem soat chat luong, chu khong chi la mot may in test case.

### Cot 4 — DAU RA (ben phai)

| Khoi | Nhan |
|---|---|
| G | `testcases/API-N_generated.csv` (22 cot) |
| H | `build_collection.py` → Postman Collection v2.1 |
| I | `newman` → bao cao HTML/JSON |
| J | Bao cao + bug report |

---

## 3. Ba diem CON NGUOI xen vao — phan phai noi bat nhat

De bai coi trong dieu nay hon ca so luong test case. **Dung mau khac hoac vien dut** cho ba
diem nay, va **ghi chu thich ngay tren so do**:

| Diem | Vi tri tren so do | Con nguoi lam gi |
|---|---|---|
| **H1** | tai khoi **B** | Doc dac ta, quyet dinh dau la phan hoach, dau la bien, chuyen trang thai nao hop le. **Chat luong ca bo test nam o day.** |
| **H2** | sau khoi **G** | **AUDIT**: gan `VALID` / `INVALID` / `INCOMPLETE` cho tung case, ghi ly do, sua case sai. Ket qua bai nay: 83 VALID, 68 INVALID, 74 INCOMPLETE |
| **H3** | sau khoi **H2** | **EXTEND**: them case ma bo sinh khong the nghi ra. Ket qua bai nay: 18 case, moi case co cot `Why_AI_Missed` |

Ve H2 va H3 thanh mot khoi noi tiep giua G va H, **khong** duoc ve nhu mot nhanh phu — chung
nam tren duong di chinh cua du lieu.

---

## 4. Ba chu thich nen ghi thang len so do

Day la nhung dieu hoc duoc trong qua trinh lam. Ghi chung len so do lam cho no la **thiet ke
cua nguoi da chay that**, khong phai mot so do khoi chung chung.

**Chu thich 1 — canh khoi D (`KHU_TRUNG`):**
> Khoa khu trung phai gom ca `Category`, `Expected_Assertions` va `Preconditions`.
> Ban dau khoa chi co `(method, endpoint, body, status)` nen coi hai case la trung nhau khi
> chung gui cung mot request, bat ke chung khang dinh dieu gi. Ket qua: 34 test case bi nuot
> oan (191 thay vi 225), va do phu bang chuyen trang thai bi bao thieu (11/25 thay vi 20/25).

**Chu thich 2 — canh khoi C3 (`SINH_SECURITY`):**
> Ma SEC la nhan khong tu giai thich. Bang SEC-01..07 phai lay tu `README.md` muc 9, khong
> duoc dien tu tri nho ve OWASP. Lan dau lam theo tri nho: 39/41 test case bao mat bi gan sai ma.

**Chu thich 3 — canh cum C1..C4:**
> Bon bo sinh deu sinh ra test case **doc lap**, moi case mot request. Do la gioi han cau truc:
> 9/18 bug ma con nguoi phai tu bo sung chi lo ra khi noi **nhieu request** lai voi nhau.

---

## 5. Bo cuc goi y

Trai sang phai, bon cot:

```
[ TAI LIEU ] -> [ DICH SANG JSON ] -> [ 4 BO SINH ] -> [ HAU XU LY ] -> [ DAU RA ]
   A1 A2 A3            B                C1 C2 C3 C4      D  E  F        G H I J
                       ^                                    |
                       |                                    |
                       +----- chua du do phu, bo sung -------+
```

Con nguoi (H1, H2, H3) ve o **hang duoi**, moi diem co mot mui ten dut noi len khoi tuong ung.
Cach nay lam noi bat rang con nguoi cham vao quy trinh o ba cho khac nhau, chu khong phai chi
o cuoi.

---

## 6. Bang kiem truoc khi coi la ve xong

- [ ] Nhin so do doan duoc **dau vao** va **dau ra** ma khong can doc chu giai
- [ ] Bon bo sinh ve **song song**, khong ve noi tiep
- [ ] Co **mui ten phan hoi** tu `KIEM_TRA_DO_PHU` quay ve khoi dich spec
- [ ] Ba diem con nguoi H1/H2/H3 duoc lam noi bat va **nam tren duong di chinh**
- [ ] Co it nhat mot trong ba chu thich o muc 4
- [ ] Goc so do co ghi **ho ten + MSSV + ngay ve**
- [ ] Da luu `agent-skill/diagram/23127060_generator_diagram.png` (nen kem file nguon)
- [ ] **Khong co** file mermaid / graphviz / anh nao do AI sinh trong thu muc nay
