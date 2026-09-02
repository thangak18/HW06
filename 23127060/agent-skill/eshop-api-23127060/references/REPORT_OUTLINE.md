# REPORT_OUTLINE — Khung bao cao HW06 (SV 23127060)

Moi muc duoi day anh xa truc tiep vao 1 yeu cau cham diem cua de bai.
Khong duoc bo muc nao — "Missing any required document results in 0 points".

---

## Cay file bao cao

```
report/
├── MAIN_REPORT.md          <- ban chinh, gop tat ca (xuat PDF)
├── MAIN_REPORT.pdf
├── 00_environment.md
├── 01_api_selection.md
├── 02_generation.md
├── 03_audit.md
├── 04_extend.md
├── 05_postman_features.md
├── 06_execution.md
└── 07_test_generator_design.md
bugs/BUG_REPORT.md
ci/CI_CD_REPORT.md
ai/audit/AI_AUDIT_REPORT.md
ai/critique/AI_CRITIQUE.md
README.md
```

---

## MAIN_REPORT.md — khung chi tiet

### 1. Thong tin
Ho ten, MSSV, lop, link GitHub repo cong khai, link video (neu co), ngay nop,
tu danh gia diem.

### 2. Moi truong thuc nghiem
OS, Node, npm, Postman, Newman, base URL, cach chay SUT, commit hash cua SUT.

### 3. Lua chon 3 API (muc 5 de bai)

| API | Pool | FR | Endpoint | Ly do chon | Khong trung voi ai |
|---|---|---|---|---|---|
| API-1 | A | FR-03 | `POST /api/forgot-password`, `POST /api/reset-password` | luong 2 buoc, giau rui ro bao mat | 23127195 lam FR-05, 23127259 lam FR-02 |
| API-2 | B | FR-08 | `POST /api/checkout` (+FR-09, FR-10) | co state machine + tinh tien | ... |
| API-3 | C | FR-15 | `POST/PUT/DELETE /api/products` | CRUD day du + phan quyen | ... |

> Ghi ro: **Pool D (mobile) khong su dung trong HW06** theo muc 5 de bai.

### 4. Quy trinh sinh test case bang AI (muc 6.1)
**Bat buoc chung minh khong dung 1 prompt tong.** Trinh bay 4 vong:

| Vong | Muc tieu | Prompt (trich) | So case thu duoc | AI_log entry |
|---|---|---|---|---|
| 2a | domain partition | ... | 16 | #4 |
| 2b | state transition | ... | 9 | #5 |
| 2c | security SEC-01..07 | ... | 11 | #6 |
| 2d | schema validation | ... | 6 | #7 |

Kem bang do phu: moi tham so / moi chuyen trang thai / moi ma SEC deu co >=1 case.

### 5. Audit ket qua AI (muc 6.2)

| API | Tong AI | VALID | INVALID | INCOMPLETE | % VALID |
|---|---|---|---|---|---|
| API-1 | 36 | 22 | 5 | 9 | 61% |

Kem **>= 5 vi du chi tiet** dang: case goc -> nhan -> ly do -> ban da sua.

### 6. Test case tu bo sung (muc 6.3)

| TC_ID | Tieu de | Nhom | Tai sao AI bo sot |
|---|---|---|---|
| TC-C3-SEC-901 | DELETE san pham khong can token | SEC-03 | AI suy dien tu ten endpoint, khong doc code |

Toi thieu 5 case/API, tong >= 15.

### 7. Thuc thi (muc 6.4)

| API | Tong case | Passed | Failed | Fail do bug SUT | Thoi gian | Report |
|---|---|---|---|---|---|---|
| API-1 | 41 | 27 | 14 | 14 | 12.3s | `newman/23127060_API-1_*.html` |

- Anh chup Postman Console co `X-Student-Id: 23127060`.
- Giai thich ro: case FAIL nao la **expected failure** (phoi bay bug), case nao la loi that.

### 8. Postman features da dung (muc 6, bat buoc liet ke)
Bang checklist tu `report/05_postman_features.md`, kem screenshot cho feature GUI.

### 9. Bug report (muc 6.5)
Tom tat bang, chi tiet o `bugs/BUG_REPORT.md`, moi bug 1 link GitHub Issue + screenshot.

| ID | Tieu de | Muc | SEC | API | Issue |
|---|---|---|---|---|---|
| C-01 | Product CRUD khong yeu cau xac thuc | Critical | SEC-03 | API-3 | #12 |

### 10. CI/CD (muc 6)
Cau hinh pipeline, 2 run (1 pass / 1 fail), screenshot + link, 2 commit hash.

### 11. Thiet ke bo sinh test bang AI (muc 7 — 10 diem)
- **Diagram tu ve** (khong duoc AI sinh) — `agent-skill/diagram/23127060_generator_diagram.png`.
- **Pseudocode** — `agent-skill/pseudocode/generator.pseudo.md`.
- Ban hien thuc: `scripts/gen_testcases.py`, cach chay, vi du dau ra.
- Han che va huong mo rong.

### 12. Phu luc A — AI Audit Report (muc 9)
Cau mo dau bat buoc: **"I use AI tools for the following tasks"**, sau do bang
Tool / Date-time / Prompt / Output cho tung tuong tac.

### 13. Phu luc B — AI Critique (muc 10, 200-300 tu)
Tra loi du 3 cau: AI sai/thien lech/thieu o dau? Vi sao AI khong bat duoc?
Ban hoc duoc nguyen tac gi khi lam viec voi AI?

---

## README.md (bat buoc trong zip)

```markdown
# HW06 — API Testing — Ninh Van Khai — 23127060

## Test summary
| Chi so | Gia tri |
|---|---|
| So API | 3 |
| Test case AI sinh | |
| Test case tu them | |
| Tong test case | |
| Da thuc thi | |
| Passed | |
| Failed | |
| Failed do bug SUT (expected) | |
| So bug bao cao | |
| So GitHub Issue | |

## Bang tu danh gia
| No. | Tieu chi | Diem toi da | Tu cham |
|---|---|---|---|
| 1 | API 1 — full pipeline | 30 | |
| 2 | API 2 — full pipeline | 30 | |
| 3 | API 3 — full pipeline | 30 | |
| 4 | Agent Skills (AI-driven test generator) | 10 | |
| | **Tong** | **100** | |

## Link
- GitHub repo: 
- GitHub Issues: 
- Video demo generator (neu co): 

## Cach chay lai
...
```

Ten file nop: `23127060_HW06_AI_API_<3 chu so>.zip`

---

## Bang kiem truoc khi nop (chay `validate_submission.py`)

- [ ] MAIN_REPORT.md + .pdf
- [ ] Link GitHub repo cong khai
- [ ] 3 Postman collection .json
- [ ] Newman report .html (>=3)
- [ ] Danh sach Postman feature
- [ ] CI/CD report + 2 screenshot + 2 link run
- [ ] Excel test case + sheet summary
- [ ] Diagram (PNG/Mermaid) + pseudocode — diagram TU VE
- [ ] (tuy chon) OpenAPI .yaml — neu AI sinh thi phai audit
- [ ] Bug report + screenshot GitHub Issues
- [ ] AI_AUDIT_REPORT.md + .pdf
- [ ] AI_CRITIQUE.md + .pdf (200-300 tu)
- [ ] git commit log (.txt)
- [ ] README.md co bang tu danh gia + test summary
