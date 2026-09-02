#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inject_failing_test.py - Lam sai DUNG MOT assertion de tao lan chay CI that bai.

  python3 ci/inject_failing_test.py --apply     # lam sai 1 assertion
  python3 ci/inject_failing_test.py --revert    # tra lai nhu cu
  python3 ci/inject_failing_test.py --check     # xem dang o trang thai nao

De bai muc 6 doi hai lan chay pipeline: mot lan tat ca test PASS, mot lan co MOT test FAIL.
Lan thu hai phai la mot thay doi nho, co chu dich, tra lai duoc — khong duoc pha bo test.

Script sua dung mot dong trong collection hoi quy cua API-1: doi ky vong ma trang thai cua
test case TC-A1-DOM-012 (`POST /api/reset-password` voi du lieu hop le) tu 200 thanh 201.
Ly do chon dung case nay:
  - No nam trong bo hoi quy, tuc la binh thuong chac chan PASS - nen khi pipeline do thi ly do
    duy nhat la thay doi vua chen vao.
  - No la case DOM dau tien cua bo hoi quy API-1 nen xuat hien som trong log CI, de nhin thay.
  - Doi 200 -> 201 la kieu nham lan con nguoi hay mac that (quy uoc REST cho thao tac tao moi),
    nen no minh hoa dung loai loi ma pipeline sinh ra de bat, thay vi mot loi bia dat.
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
