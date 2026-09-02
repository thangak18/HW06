#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""summarize_newman.py - Đọc newman/*.json và sinh bảng tổng hợp kết quả thực thi.

  python3 summarize_newman.py --dir newman --tc testcases --out report/06_execution.md

Mọi con số trong báo cáo chính đều phải đến từ đây, không được gõ tay. Script nối CSV test
case với báo cáo Newman qua mã TC_ID, nhờ vậy phân biệt được:
  - thất bại CÓ CHỦ ĐÍCH  : case gắn @bug, phơi bày một bug đã biết của SUT;
  - thất bại NGOÀI DỰ KIẾN: case gắn @contract nhưng vẫn đỏ -> hoặc là bug mới, hoặc là
                            kỳ vọng của chính test case sai. Phải rà soát từng cái.
"""
import argparse
import collections
import csv
import glob
import gzip
import io
import json
import os
import re


def load_meta(tcdir):
    meta = {}
    for f in sorted(glob.glob(os.path.join(tcdir, "API-*_final.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            meta[r["TC_ID"]] = r
    return meta


def load_json(path):
    """Bao cao JSON cua Newman rat lon (bao gom toan bo body request/response: 8-24 MB moi
    file). Chung duoc nen gzip de repo khong phinh ra, va moi cong cu doc duoc ca hai dang."""
    op = gzip.open if path.endswith(".gz") else io.open
    with op(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def read_run(path):
    d = load_json(path)
    run = d["run"]
    per = collections.OrderedDict()
    loi = []
    for e in run["executions"]:
        for a in e.get("assertions", []):
            nm = a["assertion"]
            m = re.match(r"(TC-[A-Z0-9]+-[A-Z]+-\d+)", nm)
            if not m:
                if a.get("error"):
                    loi.append((nm, a["error"]["message"]))
                continue
            tc = m.group(1)
            p = per.setdefault(tc, {"tong": 0, "fail": 0, "msg": []})
            p["tong"] += 1
            if a.get("error"):
                p["fail"] += 1
                p["msg"].append(a["error"]["message"].replace("\n", " ")[:120])
    return run, per, loi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="newman")
    ap.add_argument("--tc", default="testcases")
    ap.add_argument("--out", default="report/06_execution.md")
    a = ap.parse_args()
    meta = load_meta(a.tc)

    full, contract, dd = {}, {}, []
    for f in sorted(glob.glob(os.path.join(a.dir, "*.json"))
                    + glob.glob(os.path.join(a.dir, "*.json.gz"))):
        b = os.path.basename(f)
        m = re.search(r"_(API-\d)(_contract)?_", b)
        if m:
            (contract if m.group(2) else full)[m.group(1)] = f
        elif "_DD-" in b:
            dd.append(f)

    L = ["# STEP 6 — Thực thi bằng Postman + Newman", "",
         "> HW06 — API Testing | SV **Ninh Văn Khải — 23127060** | Đề bài mục 6.4", "",
         "Mọi con số trong tài liệu này được sinh từ `newman/*.json` bằng",
         "`agent-skill/eshop-api-23127060/scripts/summarize_newman.py`. Em không gõ tay con số nào.", "",
         "> Cột **Tiêu đề** trong mục 4 lấy nguyên văn từ `testcases/API-*_final.csv`, và cột",
         "> **Thông báo thất bại** là nguyên văn output của Newman — em giữ nguyên để làm bằng chứng.", ""]

    # ---------- 1. Bo day du ----------
    L += ["---", "", "## 1. Bộ test đầy đủ (Oracle = SPEC)", "",
          "Đây là kết quả kiểm thử thật sự: mọi kỳ vọng đều viết theo đặc tả, nên các case phơi bày",
          "bug của SUT **sẽ thất bại** — đó là mục đích của chúng.", "",
          "| API | Case | Case PASS | Case FAIL | Assertion | Assertion FAIL | Thời gian | Báo cáo HTML |",
          "|---|---|---|---|---|---|---|---|"]
    tong = collections.Counter()
    chi_tiet = {}
    for api in sorted(full):
        run, per, _ = read_run(full[api])
        st = run["stats"]; tm = run["timings"]
        p = sum(1 for v in per.values() if v["fail"] == 0)
        fl = len(per) - p
        html = os.path.basename(full[api]).replace(".json.gz", ".html").replace(".json", ".html")
        L.append("| %s | %d | %d | %d | %d | %d | %.1fs | `newman/%s` |"
                 % (api, len(per), p, fl, st["assertions"]["total"],
                    st["assertions"]["failed"], tm.get("completed", 0) / 1000.0 - tm.get("started", 0) / 1000.0
                    if tm.get("completed") else run.get("timings", {}).get("responseAverage", 0) / 1000.0, html))
        tong["case"] += len(per); tong["pass"] += p; tong["fail"] += fl
        tong["as"] += st["assertions"]["total"]; tong["asf"] += st["assertions"]["failed"]
        chi_tiet[api] = per
    L.append("| **Tổng** | **%d** | **%d** | **%d** | **%d** | **%d** | | |"
             % (tong["case"], tong["pass"], tong["fail"], tong["as"], tong["asf"]))
    L.append("")
    L.append("Tỷ lệ case PASS: **%.0f%%** (%d/%d). Tỷ lệ assertion PASS: **%.0f%%** (%d/%d)."
             % (100.0 * tong["pass"] / tong["case"], tong["pass"], tong["case"],
                100.0 * (tong["as"] - tong["asf"]) / tong["as"], tong["as"] - tong["asf"], tong["as"]))
    L.append("")

    # ---------- 2. Phan loai that bai ----------
    L += ["## 2. Phân loại case thất bại", "",
          "| API | FAIL tổng | Có chủ đích (`@bug`) | Ngoài dự kiến (`@contract`) |", "|---|---|---|---|"]
    ngoai = collections.defaultdict(list)
    for api in sorted(chi_tiet):
        c = collections.Counter()
        for tc, v in chi_tiet[api].items():
            if v["fail"] == 0:
                continue
            tag = meta.get(tc, {}).get("Tag", "?")
            c[tag] += 1
            if tag == "@contract":
                ngoai[api].append((tc, meta.get(tc, {}).get("Title", "")[:70], v["msg"][0] if v["msg"] else ""))
        L.append("| %s | %d | %d | %d |" % (api, sum(c.values()), c["@bug"], c["@contract"]))
    L.append("")

    # ---------- 3. Bug được phơi bày ----------
    L += ["## 3. Bug được phơi bày, theo mã bug", "",
          "| Mã bug | Số case thất bại phơi bày nó | API |", "|---|---|---|"]
    bug = collections.defaultdict(lambda: [0, set()])
    for api in sorted(chi_tiet):
        for tc, v in chi_tiet[api].items():
            if v["fail"] == 0:
                continue
            b = meta.get(tc, {}).get("Bug_Ref", "-")
            if b and b != "-":
                bug[b][0] += 1
                bug[b][1].add(api)
    for b in sorted(bug):
        L.append("| **%s** | %d | %s |" % (b, bug[b][0], ", ".join(sorted(bug[b][1]))))
    L.append("")

    # ---------- 4. That bai ngoai du kien ----------
    L += ["## 4. Thất bại ngoài dự kiến — em phải rà soát từng cái", "",
          "Đây là các case gắn `@contract` (nghĩa là lúc thiết kế em nghĩ SUT đáp ứng được) nhưng",
          "vẫn thất bại. Mỗi dòng ở đây hoặc là **một bug chưa có trong danh sách bug đã biết**,",
          "hoặc là **một kỳ vọng sai của chính test case**. Em không bỏ qua dòng nào.", ""]
    for api in sorted(ngoai):
        L += ["### %s — %d case" % (api, len(ngoai[api])), "",
              "| TC_ID | Tiêu đề | Thông báo thất bại đầu tiên |", "|---|---|---|"]
        for tc, ti, ms in sorted(ngoai[api]):
            L.append("| `%s` | %s | %s |" % (tc, ti.replace("|", "\\|"), ms.replace("|", "\\|")[:90]))
        L.append("")

    # ---------- 5. Moc hoi quy ----------
    if contract:
        L += ["## 5. Bộ hồi quy (`@contract`) — lần chạy all-pass cho CI", "",
              "Bộ này gồm các test case mà SUT **hiện đang đáp ứng**, được chốt từ kết quả chạy thật",
              "bằng `derive_contract.py`. Nó không khẳng định 'API này đúng', mà khẳng định 'những điều",
              "API này đang làm đúng thì không được phá'. Đây là lần chạy em dùng cho yêu cầu",
              "'all API test cases passing' của đề bài mục 6.", "",
              "| API | Case | Assertion | Assertion FAIL | Báo cáo HTML |", "|---|---|---|---|---|"]
        t2 = collections.Counter()
        for api in sorted(contract):
            run, per, _ = read_run(contract[api])
            st = run["stats"]
            L.append("| %s | %d | %d | **%d** | `newman/%s` |"
                     % (api, len(per), st["assertions"]["total"], st["assertions"]["failed"],
                        os.path.basename(contract[api]).replace(".json.gz", ".html").replace(".json", ".html")))
            t2["c"] += len(per); t2["a"] += st["assertions"]["total"]; t2["f"] += st["assertions"]["failed"]
        L.append("| **Tổng** | **%d** | **%d** | **%d** | |" % (t2["c"], t2["a"], t2["f"]))
        L.append("")

    # ---------- 6. Data-driven ----------
    if dd:
        L += ["## 6. Lần chạy data-driven (Postman Collection Runner / `newman -d`)", "",
              "| Bộ | Data file | Vòng lặp | Request | Assertion | Assertion FAIL |", "|---|---|---|---|---|---|"]
        NHAN = {"DD1": ("Brute force OTP", "brute_force_tokens.csv"),
                "DD2": ("Bảng chuyển trạng thái FR-10", "state_transitions.csv"),
                "DD3": ("Lạm dụng hạn mức coupon", "coupon_abuse.csv"),
                "DD4": ("Đầu vào không hợp lệ POST /api/products", "product_invalid.csv")}
        for f in sorted(dd):
            k = re.search(r"_DD-(DD\d)_", os.path.basename(f)).group(1)
            d = load_json(f)["run"]["stats"]
            ten, data = NHAN.get(k, (k, "?"))
            L.append("| %s %s | `postman/data/%s` | %d | %d | %d | %d |"
                     % (k, ten, data, d["iterations"]["total"], d["requests"]["total"],
                        d["assertions"]["total"], d["assertions"]["failed"]))
        L.append("")

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("Da ghi %s (%d dong)" % (a.out, len(L)))


if __name__ == "__main__":
    main()
