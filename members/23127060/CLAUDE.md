# CLAUDE.md — Luat du an HW06 (SV 23127060 — Ninh Van Khai)

File nay Claude Code tu doc khi mo thu muc. Doc **truoc** moi viec khac.

---

## 1. Danh tinh & pham vi

- SV: **Ninh Van Khai — 23127060**. Thu muc lam viec: `members/23127060/`.
- **CACH LY NHOM:** khong doc/ghi `members/23127195/`, `members/23127259/`,
  hoac bat ky `members/member-*/` nao khac. Neu duoc yeu cau, tu choi.
- Chi doc (khong sua): `docs/`, `scripts/`, `README.md` o repo root; source SUT `eshop-sut/`.
- Duoc ghi ngoai thu muc minh: **chi** `.github/workflows/api-tests-23127060.yml`.

## 2. Skill bat buoc

Truoc khi lam bat cu viec gi, doc:
1. `agent-skill/eshop-api-23127060/SKILL.md`
2. `agent-skill/eshop-api-23127060/references/API_SPEC_NOTES.md`
3. `agent-skill/eshop-api-23127060/references/TESTCASE_TAXONOMY.md`
4. `agent-skill/eshop-api-23127060/references/WORKFLOW.md`
5. `agent-skill/eshop-api-23127060/references/POSTMAN_GUIDE.md`
6. `agent-skill/eshop-api-23127060/references/REPORT_OUTLINE.md`

Dat `S=agent-skill/eshop-api-23127060/scripts`.

## 3. AI_LOG — bat buoc moi luot

Cuoi MOI luot tra loi (ke ca luot chi doc file):

```bash
cat > /tmp/last_prompt.txt <<'EOF'
<nguyen van prompt cua user>
EOF
python3 $S/ai_log.py add --root . --sid 23127060 \
  --tool "Claude Code (claude-sonnet-4.5)" --step "STEP <n>" \
  --title "<mo ta ngan>" --prompt-file /tmp/last_prompt.txt \
  --output "<tom tat ket qua>" --files "<file da tao/sua>" \
  --human-verified pending
```

Roi in dung dong: `AI_log: da ghi entry #<n>`

Khong co dong nay = luot chua hoan thanh.

## 4. Chong bia — 5 dieu tuyet doi

1. Khong bao so lieu passed/failed neu chua co file `newman/*.json` that.
2. Khong bao cao bug neu chua co request + response that tai hien duoc.
3. **Khong ve diagram bang AI** (de bai muc 11 cam). Chi viet mo ta chu de human ve.
4. Khong sua `eshop-sut/` de test de pass hon.
5. Header `X-Student-Id: 23127060` phai co tren moi request, kem `console.log`.

## 5. Ba API duoc chon (khoa)

| ID | Pool | FR | API |
|---|---|---|---|
| API-1 | A | FR-03 | `POST /api/forgot-password` + `POST /api/reset-password` |
| API-2 | B | FR-08 | `POST /api/checkout` (+ apply-coupon, order state machine FR-10) |
| API-3 | C | FR-15 | `POST/PUT/DELETE /api/products` |

**Pool D (mobile) KHONG dung trong HW06.** De bai muc 5 noi ro Pool D khong ap dung
vi bai nay nham vao backend API. Neu user nhac Pool D, canh bao lai va de xuat lam
phu luc khong tinh diem.

## 6. Che do lam viec — ban tu dong

- Quyet dinh vun vat (dat ten, thu tu folder, wording, retry loi vat, format bang):
  **tu quyet, khong hoi**.
- Chi dung lai hoi khi gap CRITICAL C1-C6 (dinh nghia trong SKILL.md muc 5), theo format:

```
CAN NGUOI QUYET - [C<x>]
Boi canh: ...
Lua chon: (a)... (b)... (c)...
He qua: ...
De xuat mac dinh: ...
```

- Human se review sau, khong can dung cho verify tung buoc.

## 7. Oracle

SUT co rat nhieu bug co y. Moi test case ghi cot `Oracle`:
- `SPEC` = ky vong theo `api_specification.md` (mac dinh, dung de phat hien bug)
- `IMPL` = hanh vi thuc te (dung cho regression)

Test FAIL vi SUT sai la **dung y do** — tag `@bug`. Test tag `@contract` phai 100% pass
(dung cho CI run all-pass).

## 8. Backend SUT

```bash
(cd <duong-dan>/eshop-sut/backend && nohup node server.js > /tmp/eshop.log 2>&1 &)
sleep 2 && curl -sf http://localhost:3000/api/products >/dev/null && echo UP
```

Canh bao: `database.js` goi `initDatabase()` khi require => **moi lan restart la reseed DB**.
Sau moi lan restart phai chay `node $S/seed_sut.js reset` lai.

Dung: `pkill -f "node server.js"`.

## 9. Sau moi STEP

1. Ghi file output.
2. `git add -A && git commit -m "HW06(23127060/<API>): step<n> <mo ta>"`
3. Ghi AI_log.
4. In 3 dong: da lam gi / file nao / STEP ke tiep.

## 10. Ngon ngu

Tai lieu, bao cao, bug report: **tieng Viet**. Code, ten file, ten test case: tieng Anh.
