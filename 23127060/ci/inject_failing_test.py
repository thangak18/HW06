#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inject_failing_test.py - Làm sai ĐÚNG MỘT assertion để tạo lần chạy CI thất bại.

  python3 ci/inject_failing_test.py --apply     # lam sai 1 assertion
  python3 ci/inject_failing_test.py --revert    # tra lai nhu cu
  python3 ci/inject_failing_test.py --check     # xem dang o trang thai nao

Đề bài mục 6 đòi hai lần chạy pipeline: một lần tất cả test PASS, một lần có MỘT test FAIL.
Lần thứ hai phải là một thay đổi nhỏ, có chủ đích, trả lại được — không được phá bộ test.

Script sửa đúng một dòng trong collection hồi quy của API-1: đổi kỳ vọng mã trạng thái của
test case TC-A1-DOM-012 (`POST /api/reset-password` với dữ liệu hợp lệ) từ 200 thành 201.
Lý do chọn đúng case này:
  - Nó nằm trong bộ hồi quy, tức là bình thường chắc chắn PASS - nên khi pipeline đỏ thì lý do
    duy nhất là thay đổi vừa chèn vào.
  - Nó là case DOM đầu tiên của bộ hồi quy API-1 nên xuất hiện sớm trong log CI, dễ nhìn thấy.
  - Đổi 200 -> 201 là kiểu nhầm lẫn con người hay mắc thật (quy ước REST cho thao tác tạo mới),
    nên nó minh họa đúng loại lỗi mà pipeline sinh ra để bắt, thay vì một lỗi bịa đặt.
"""
import argparse
import json
import os
import sys

FILE = "postman/collections/23127060_HW06_API-1_contract.postman_collection.json"
TC = "TC-A1-DOM-012"
DUNG = "  pm.response.to.have.status(200);"
SAI = "  pm.response.to.have.status(201);  // [CI-DEMO] co y lam sai de pipeline that bai"


def duyet(col):
    for folder in col.get("item", []):
        for it in folder.get("item", []):
            if it["name"].startswith(TC):
                for ev in it.get("event", []):
                    if ev.get("listen") == "test":
                        return ev["script"]["exec"]
    return None


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--apply", action="store_true")
    g.add_argument("--revert", action="store_true")
    g.add_argument("--check", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(FILE):
        sys.exit("Khong thay %s. Chay tu thu muc 23127060/." % FILE)
    col = json.load(open(FILE, encoding="utf-8"))
    exec_ = duyet(col)
    if exec_ is None:
        sys.exit("Khong tim thay test case %s trong %s" % (TC, FILE))

    dang_sai = any(l.startswith(SAI.split("//")[0].rstrip()) for l in exec_)
    if a.check:
        print("%s: %s" % (TC, "DANG BI LAM SAI (pipeline se do)" if dang_sai
                          else "binh thuong (pipeline se xanh)"))
        return

    if a.apply:
        if dang_sai:
            print("Da o trang thai loi roi, khong lam gi.")
            return
        for i, l in enumerate(exec_):
            if l == DUNG:
                exec_[i] = SAI
                break
        else:
            sys.exit("Khong tim thay dong ky vong ma trang thai 200 de sua.")
        thong_diep = "DA LAM SAI 1 assertion cua %s (200 -> 201). Pipeline se that bai." % TC
    else:
        if not dang_sai:
            print("Dang binh thuong, khong co gi de tra lai.")
            return
        for i, l in enumerate(exec_):
            if l.startswith("  pm.response.to.have.status(201);"):
                exec_[i] = DUNG
                break
        thong_diep = "DA TRA LAI assertion cua %s ve 200. Pipeline se xanh tro lai." % TC

    json.dump(col, open(FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(thong_diep)
    print("File da sua: %s" % FILE)


if __name__ == "__main__":
    main()
