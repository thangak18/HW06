#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""md_to_pdf.py - Xuất các tài liệu Markdown bắt buộc sang PDF.

  python3 md_to_pdf.py                       # xuat 4 file bat buoc cua de bai
  python3 md_to_pdf.py --in a.md --out a.pdf # xuat mot file bat ky

Đề bài mục 14 đòi bản PDF cho: báo cáo chính, AI Audit Report và AI Critique
(script này xuất thêm cả bug report).

Dùng `markdown-pdf` (thuần Python, không cần pandoc / LaTeX / trình duyệt). Nếu gói PDF chưa
được cài, script báo rõ cách cài thay vì thất bại âm thầm.
"""
import argparse
import os
import re
import sys

CSS = """
body { font-family: "DejaVu Sans", "Noto Sans", Arial, sans-serif; font-size: 10.5pt;
       line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 19pt; border-bottom: 2px solid #1F4E78; padding-bottom: 5px; color: #1F4E78; }
h2 { font-size: 14pt; margin-top: 18px; color: #1F4E78; border-bottom: 1px solid #d0d7de;
     padding-bottom: 3px; }
h3 { font-size: 12pt; margin-top: 14px; color: #24292f; }
h4 { font-size: 11pt; margin-top: 12px; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 8.5pt; }
th, td { border: 1px solid #b8c0c8; padding: 4px 6px; text-align: left;
         vertical-align: top; word-break: break-word; }
th { background: #1F4E78; color: #fff; font-weight: bold; }
tr:nth-child(even) td { background: #f5f7f9; }
code { font-family: "DejaVu Sans Mono", "Courier New", monospace; font-size: 8.5pt;
       background: #f0f2f4; padding: 1px 3px; border-radius: 3px; }
pre { background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 4px; padding: 8px;
      font-size: 8pt; line-height: 1.35; white-space: pre-wrap; word-break: break-word; }
pre code { background: none; padding: 0; font-size: 8pt; }
blockquote { border-left: 3px solid #1F4E78; margin-left: 0; padding: 2px 0 2px 12px;
             color: #444; background: #f7f9fb; }
a { color: #0969da; text-decoration: none; }
hr { border: 0; border-top: 1px solid #d0d7de; margin: 16px 0; }
"""

MAC_DINH = [
    ("report/MAIN_REPORT.md", "report/MAIN_REPORT.pdf", "Bao cao chinh HW06 - 23127060"),
    ("ai/audit/AI_AUDIT_REPORT.md", "ai/audit/AI_AUDIT_REPORT.pdf", "AI Audit Report - 23127060"),
    ("ai/critique/AI_CRITIQUE.md", "ai/critique/AI_CRITIQUE.pdf", "AI Critique - 23127060"),
    ("bugs/BUG_REPORT.md", "bugs/BUG_REPORT.pdf", "Bug Report HW06 - 23127060"),
]


def don_lien_ket(md):
    """Bo cac lien ket khong dan toi dau duoc trong ban PDF.

    - `[chu](#neo)`: markdown-pdf dung PyMuPDF de dat neo, va no bao loi cung neu gap mot neo
      trong muc luc ma khong tim thay dich. Trong ban PDF thi muc luc do thua roi (PDF da co
      muc luc rieng do `toc_level` sinh ra), nen chuyen ve chu thuong.
    - `[chu](duong/dan.md)`: duong dan tuong doi trong repo, bam vao trong PDF khong ra gi.
      Doi thanh `chu (duong/dan.md)` de nguoi doc ban in van biet file nam o dau.
    """
    md = re.sub(r"\[([^\]]+)\]\(#[^)]*\)", r"\1", md)
    md = re.sub(r"\[([^\]]+)\]\((?!https?://)([^)]+\.(?:md|csv|json|xlsx|html|txt|ya?ml|py))\)",
                r"\1 (`\2`)", md)
    md = re.sub(r"\[([^\]]+)\]\((?!https?://)([^)]*/)\)", r"\1 (`\2`)", md)
    return md


def xuat(src, dst, tieu_de):
    from markdown_pdf import MarkdownPdf, Section
    if not os.path.exists(src):
        print("  [BO QUA] khong thay %s" % src)
        return False
    md = open(src, encoding="utf-8").read()
    md = don_lien_ket(md)
    pdf = MarkdownPdf(toc_level=2, optimize=True)
    pdf.add_section(Section(md, toc=True), user_css=CSS)
    pdf.meta["title"] = tieu_de
    pdf.meta["author"] = "Ninh Van Khai - 23127060"
    pdf.meta["subject"] = "HW06 - API Testing"
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    pdf.save(dst)
    kb = os.path.getsize(dst) / 1024.0
    print("  [OK] %-34s -> %-34s (%.0f KB)" % (src, dst, kb))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src")
    ap.add_argument("--out", dest="dst")
    ap.add_argument("--title", default="HW06 - 23127060")
    a = ap.parse_args()

    try:
        import markdown_pdf  # noqa: F401
    except ImportError:
        print("Chua co goi markdown-pdf. Chay:  pip install markdown-pdf", file=sys.stderr)
        sys.exit(1)

    if a.src:
        xuat(a.src, a.dst or os.path.splitext(a.src)[0] + ".pdf", a.title)
        return
    n = 0
    for src, dst, t in MAC_DINH:
        n += 1 if xuat(src, dst, t) else 0
    print("Da xuat %d file PDF." % n)


if __name__ == "__main__":
    main()
