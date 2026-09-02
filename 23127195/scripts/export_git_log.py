#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_git_log.py — Xuat git commit log ra dang text

De bai (muc 12) yeu cau: "Create a new Git commit for each step of the procedure"
va nop lich su commit duoi dang file text.

File sinh ra co ba phan:
  1. Ghi chu ve do min cua commit (giai thich vi sao gop/tach nhu vay)
  2. Bang doi chieu commit <-> buoc quy trinh
  3. Nhat ky day du (git log --stat)

Bang doi chieu lay tu STEPS ben duoi: khoa la tien to cua tieu de commit.
Them commit moi thi them mot dong vao STEPS, khong sua tay file ket qua.

Usage:
    python scripts/export_git_log.py
"""

import io
import os
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO = os.path.abspath(os.path.join(ROOT, ".."))
OUT = os.path.join(ROOT, "evidence", "git_commit_log.txt")
SEP = "=" * 100

# Chi lay commit dong toi thu muc cua sinh vien (hoac workflow CI cua minh)
PATHSPEC = ["23127195", ".github/workflows/newman-23127195.yml"]

# tien to tieu de commit -> mo ta buoc trong quy trinh cua de bai
STEPS = [
    ("refactor: update member",     "Chuan bi - tao workspace theo MSSV trong repo nhom"),
    ("chore(23127195): setup",      "Chuan bi - dung workspace, chon API lan 1"),
    ("chore(23127195): doi bo API", "Chuan bi - chot lai bo 3 API + ha tang sinh test"),
    ("feat(api1-fr04):",            "API-1 - Buoc 1 Generate + Buoc 2 Audit + Buoc 3 Extend"),
    ("feat(api2-fr09):",            "API-2 - Buoc 1 Generate + Buoc 2 Audit + Buoc 3 Extend"),
    ("feat(api3-fr16):",            "API-3 - Buoc 1 Generate + Buoc 2 Audit + Buoc 3 Extend"),
    ("build(postman):",             "Ca 3 API - bien dich test case sang Postman Collection"),
    ("test(all):",                  "Ca 3 API - Buoc 4 Execute (Newman) + xuat bang test case"),
    ("docs(bugs):",                 "Buoc 5 Report - bao cao loi + noi dung GitHub Issue"),
    ("feat(postman,ci):",           "Tich hop CI/CD - data-driven + cong chan hoi quy + GitHub Actions"),
    ("feat(ci):",                   "Tich hop CI/CD - workflow + cong chan hoi quy"),
    ("feat(agent-skill):",          "Agent Skill - thiet ke + pseudocode + cai dat tham chieu"),
    ("docs(ai):",                   "Ho so AI audit - khai bao, nhat ky tuong tac, phe binh"),
    ("docs(postman):",              "Tai lieu tinh nang Postman da dung"),
    ("docs(report):",               "Bao cao chinh + xuat PDF"),
    ("docs: bao cao chinh",         "Bao cao chinh, CI/CD report, Postman features, chi muc bang chung"),
    ("docs: kich ban video",        "Kich ban video demo, git commit log, bang phan cong nhom"),
    ("chore: chot ket qua",         "Chot ket qua lan chay cuoi, dong bo so lieu giua cac bao cao"),
    ("docs(pdf):",                  "Xuat 9 bao cao sang PDF (yeu cau muc 14)"),
    ("chore: bo __pycache__",       "Ve sinh repo - bo file rac khoi theo doi cua git"),
    ("docs(video):",                "Kich ban video, git commit log, bang phan cong nhom"),
    ("docs(diagram):",              "Huong dan ve so do (tu chua, khong kem ban ve)"),
    ("feat(diagram+issues):",       "So do tu ve + tao 24 GitHub Issue that"),
    ("chore(evidence):",            "Chi muc bang chung - script sinh git commit log"),
    ("docs(evidence):",             "Bang chung muc 11 - anh chup Postman Console + giai phong log khoi .gitignore"),
]

HEADER = """GIT COMMIT LOG - HW06 API Testing
Sinh vien : 23127195
Repository: https://github.com/thangak18/HW06
Xuat luc  : {now}

Theo muc 12 cua de bai: 'Create a new Git commit for each step of the procedure'.

GHI CHU VE DO MIN CUA COMMIT
----------------------------
De bai (muc 12) neu vi du: "generation, audit, extension, and execution for each API".
Trong bai nay, ba buoc Generate / Audit / Extend cua MOI API duoc gom vao MOT commit, vi ca ba
deu ghi vao cung mot file nguon test case (testcases/<api>_testcases.json) - nhan audit va co
nguon AI/HUMAN la CAC TRUONG NAM NGAY TRONG tung test case, khong phai ba file rieng biet:

    {{
      "id": "TC-A1-028",
      "source": "HUMAN",                              <- buoc 3 Extend
      "audit": {{ "label": "VALID", "reason": ... }},   <- buoc 2 Audit
      "expected_by_spec": ...,                        <- buoc 1 Generate
      ...
    }}

Tach lam ba commit se phai tao ra ba trang thai trung gian khong ung voi cach lam that, tuc la
nguy tao lich su. Thay vao do, thong diep commit cua tung API ghi ro ca ba buoc, va co the truy
nguoc bang cach loc theo truong `source` va `audit.label`.

Buoc 4 Execute duoc gom mot commit cho ca ba API vi ca ba chay trong cung mot lan
`bash scripts/run_newman.sh api1 api2 api3`.
"""


def git(*args):
    r = subprocess.run(["git"] + list(args), cwd=REPO,
                       capture_output=True)
    if r.returncode != 0:
        print(r.stderr.decode("utf-8", "replace"), file=sys.stderr)
        raise SystemExit("git %s that bai" % " ".join(args))
    return r.stdout.decode("utf-8", "replace")


def step_for(subject):
    for prefix, desc in STEPS:
        if subject.startswith(prefix):
            return desc
    return "(chua gan buoc - them vao STEPS trong scripts/export_git_log.py)"


def main():
    log = git("log", "--reverse", "--pretty=format:%H%x1f%ad%x1f%s", "--date=iso",
              "--", *PATHSPEC)
    rows = [l.split("\x1f") for l in log.splitlines() if l.strip()]

    parts = [HEADER.format(now=time.strftime("%Y-%m-%d %H:%M:%S")),
             SEP, "BANG DOI CHIEU COMMIT <-> BUOC QUY TRINH", SEP, ""]

    unmapped = 0
    for i, (sha, date, subject) in enumerate(rows, 1):
        desc = step_for(subject)
        if desc.startswith("(chua gan"):
            unmapped += 1
        parts += ["%2d. %s  %s" % (i, sha[:8], date[:19]),
                  "    Commit : %s" % subject,
                  "    Buoc   : %s" % desc, ""]

    parts += [SEP, "NHAT KY DAY DU (git log --stat)", SEP, "", ""]
    full = git("log", "--reverse", "--stat", "--stat-width=100",
               "--pretty=format:%n%n" + "-" * 70 +
               "%ncommit  %H%nAuthor  %an <%ae>%nDate    %ad%n%n%s%n",
               "--date=default", "--", *PATHSPEC)
    parts.append(full.strip("\n"))

    text = "\n".join(parts).rstrip() + "\n"
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)

    print("Da xuat %d commit vao %s" % (len(rows), os.path.relpath(OUT, ROOT)))
    if unmapped:
        print("CANH BAO: %d commit chua gan buoc quy trinh" % unmapped, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
