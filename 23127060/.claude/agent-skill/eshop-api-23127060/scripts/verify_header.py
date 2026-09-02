#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_header.py - Chứng minh header X-Student-Id có mặt trên MỌI request đã gửi.

  python3 verify_header.py --dir newman --sid 23127060 --out ci/evidence/header_evidence.md

Đề bài mục 11 (chống gian lận) đòi bằng chứng cho header `X-Student-Id: {StudentID}`, và nói
rõ bằng chứng đó là ảnh chụp Postman Console. Ảnh chụp thì không kiểm chứng tự động được, và
một dòng console.log chỉ chứng minh script ĐÃ CHẠY chứ chưa chứng minh header ĐÃ ĐƯỢC GỬI.

Script này đọc thẳng phần `request.header` mà Newman ghi lại cho từng request thật sự rời
lên đường, nên nó trả lời đúng câu hỏi: có bao nhiêu request mang header, giá trị là gì, và
có request nào thiếu không. Ảnh chụp Console vẫn được nộp kèm, nhưng đây mới là bằng chứng
kiểm chứng lại được.
"""
import argparse
import collections
import glob
import gzip
import io
import json
import os


def load(path):
    op = gzip.open if path.endswith(".gz") else io.open
    with op(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="newman")
    ap.add_argument("--sid", default="23127060")
    ap.add_argument("--out", default="ci/evidence/header_evidence.md")
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.dir, "*.json")) + glob.glob(os.path.join(a.dir, "*.json.gz")))
    L = ["# Bang chung header `X-Student-Id: %s`" % a.sid, "",
         "> HW06 — SV **Ninh Van Khai — %s** | De bai muc 11 (chong gian lan)" % a.sid, "",
         "Sinh tu `agent-skill/eshop-api-23127060/scripts/verify_header.py`, doc thang phan",
         "`request.header` ma Newman ghi lai cho **tung request that su roi len duong**.", "",
         "| Bao cao Newman | Request da gui | Co header | Thieu header | Gia tri |",
         "|---|---|---|---|---|"]
    tong = collections.Counter()
    sai = []
    for f in files:
        d = load(f)
        co = thieu = 0
        vals = collections.Counter()
        for e in d["run"]["executions"]:
            hs = {h["key"].lower(): h["value"] for h in e["request"].get("header", [])}
            if "x-student-id" in hs:
                co += 1
                vals[hs["x-student-id"]] += 1
                if hs["x-student-id"] != a.sid:
                    sai.append((os.path.basename(f), e["item"]["name"], hs["x-student-id"]))
            else:
                thieu += 1
                sai.append((os.path.basename(f), e["item"]["name"], "(thieu)"))
        L.append("| `%s` | %d | %d | %d | %s |"
                 % (os.path.basename(f), co + thieu, co, thieu,
                    ", ".join("`%s` x%d" % (k, v) for k, v in vals.items()) or "—"))
        tong["co"] += co
        tong["thieu"] += thieu
    L.append("| **Tong** | **%d** | **%d** | **%d** | |"
             % (tong["co"] + tong["thieu"], tong["co"], tong["thieu"]))
    L += ["",
          "**Ket luan: %d/%d request mang header `X-Student-Id: %s`.**"
          % (tong["co"], tong["co"] + tong["thieu"], a.sid), ""]
    if sai:
        L += ["## Request co van de", "", "| Bao cao | Request | Gia tri |", "|---|---|---|"]
        for f, n, v in sai[:50]:
            L.append("| `%s` | %s | %s |" % (f, n[:60], v))
    else:
        L += ["Khong co request nao thieu header hoac mang gia tri khac.", ""]
    L += ["", "## Header duoc chen o dau", "",
          "Trong pre-request script cap **collection** (ap cho moi request, khong the quen):", "",
          "```javascript",
          'const STUDENT_ID = pm.environment.get("studentId") || "%s";' % a.sid,
          'pm.request.headers.upsert({ key: "X-Student-Id", value: STUDENT_ID });',
          'pm.request.headers.upsert({ key: "Accept", value: "application/json" });',
          "",
          "console.log(",
          '  "[HW06][" + STUDENT_ID + "] " +',
          '  pm.request.method + " " + pm.request.url.toString() +',
          '  " | X-Student-Id=" + STUDENT_ID +',
          '  " | " + new Date().toISOString()',
          ");",
          "```", "",
          "Dong `console.log` tren duoc Newman giu lai trong bao cao HTML nho co",
          "`--reporter-htmlextra-logs`, nen bao cao HTML vua la ket qua vua la bang chung."]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("Da ghi %s | %d/%d request co header dung"
          % (a.out, tong["co"], tong["co"] + tong["thieu"]))


if __name__ == "__main__":
    main()
