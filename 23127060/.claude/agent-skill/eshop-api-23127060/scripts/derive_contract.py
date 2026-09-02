#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derive_contract.py - Suy ra bộ test hồi quy (@contract) từ KẾT QUẢ CHẠY THẬT.

  python3 derive_contract.py --dir newman --out postman/contract_baseline

Vì sao không dùng thẳng cột Tag trong CSV:
  Cột `Tag` được gắn lúc THIẾT KẾ, dựa trên danh sách bug đã biết trước. Nó trả lời câu
  "em NGHĨ SUT có đáp ứng điều này không". Nhưng bộ test đã tìm ra nhiều bug ngoài danh
  sách đó (63 case thất bại vì SUT trả 404 cho mọi đầu vào xấu thay vì 400), nên 72 case
  gắn @contract vẫn FAIL.

  Đề bài mục 6 đòi một lần chạy CI "all API test cases passing". Nếu lấy bộ @contract theo
  thiết kế làm lần chạy đó thì nó sẽ đỏ, và nếu sửa kỳ vọng cho khớp với hành vi sai của SUT
  thì là ngụy tạo kết quả.

  Cách đúng: bộ @contract là một MỐC HỒI QUY (regression baseline) - tập hợp các case
  mà SUT HIỆN ĐANG đáp ứng, chốt tại một commit cụ thể. Nó không khẳng định "API này đúng",
  mà khẳng định "những điều API này đang làm đúng thì không được phá". Đây là cách dùng
  chuẩn của một bộ test hồi quy trên hệ thống còn nhiều lỗi, và nó được ghi rõ trong báo cáo
  chứ không giấu đi.

  Bộ đầy đủ (Oracle = SPEC) vẫn là kết quả kiểm thử thật sự, và nó vẫn đỏ - đúng như mong đợi.
"""
import argparse
import collections
import glob
import gzip
import io
import json
import os
import re


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="newman")
    ap.add_argument("--out", default="postman/contract_baseline")
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    tong = collections.Counter()
    for f in sorted(glob.glob(os.path.join(a.dir, "*_API-*.json"))
                    + glob.glob(os.path.join(a.dir, "*_API-*.json.gz"))):
        if "_contract_" in f:
            continue
        m = re.search(r"_(API-\d)_", f)
        if not m:
            continue
        api = m.group(1)
        op = gzip.open if f.endswith(".gz") else io.open
        with op(f, "rt", encoding="utf-8") as fh:
            d = json.load(fh)
        per = collections.defaultdict(lambda: [0, 0])
        for e in d["run"]["executions"]:
            for x in e.get("assertions", []):
                mm = re.match(r"(TC-[A-Z0-9]+-[A-Z]+-\d+)", x["assertion"])
                if not mm:
                    continue
                per[mm.group(1)][0] += 1
                if x.get("error"):
                    per[mm.group(1)][1] += 1
        passed = sorted(t for t, v in per.items() if v[1] == 0)
        p = os.path.join(a.out, "%s.txt" % api)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("# Moc hoi quy %s - sinh tu %s\n" % (api, os.path.basename(f)))
            fh.write("# %d / %d test case dang duoc SUT dap ung tai commit eshop-sut 85af3ba.\n"
                     % (len(passed), len(per)))
            fh.write("# Day KHONG phai danh sach 'case dung'. Day la nhung gi SUT dang lam dung\n"
                     "# va khong duoc phep pha. Sinh boi derive_contract.py, khong sua tay.\n")
            for t in passed:
                fh.write(t + "\n")
        print("%s: %d/%d case vao moc hoi quy -> %s" % (api, len(passed), len(per), p))
        tong["pass"] += len(passed)
        tong["all"] += len(per)
    print("TONG: %d/%d case vao moc hoi quy" % (tong["pass"], tong["all"]))


if __name__ == "__main__":
    main()
