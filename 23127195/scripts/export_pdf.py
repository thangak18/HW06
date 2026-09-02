#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_pdf.py — Xuat cac bao cao Markdown sang PDF

De bai (muc 14) yeu cau nop bao cao chinh va phan AI audit o CA HAI dinh dang
Markdown va PDF.

Cach lam: Markdown -> HTML (co CSS in an) -> PDF bang Chrome headless.
Khong phu thuoc LaTeX; font he thong ho tro tieng Viet.

Usage:
    python scripts/export_pdf.py
"""

import base64
import glob
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "pdf")

DOCS = [
    ("docs/00_MAIN_REPORT.md",   "00_MAIN_REPORT.pdf"),
    ("docs/01_API_SELECTION.md", "01_API_SELECTION.pdf"),
    ("docs/02_POSTMAN_FEATURES.md", "02_POSTMAN_FEATURES.pdf"),
    ("ai/AI_AUDIT_REPORT.md",    "AI_AUDIT_REPORT.pdf"),
    ("ai/AI_CRITIQUE.md",        "AI_CRITIQUE.pdf"),
    ("bugs/BUG_REPORTS.md",      "BUG_REPORTS.pdf"),
    ("ci/CI_CD_REPORT.md",       "CI_CD_REPORT.pdf"),
    ("agent-skill/DESIGN.md",    "AGENT_SKILL_DESIGN.pdf"),
    ("README.md",                "README.pdf"),
]

CSS = """
@page { size: A4; margin: 16mm 14mm; }
* { box-sizing: border-box; }
body {
    font-family: "Segoe UI", "Times New Roman", serif;
    font-size: 10.5pt; line-height: 1.55; color: #1a1a1a; margin: 0;
}
h1 { font-size: 19pt; border-bottom: 2px solid #1F4E78; padding-bottom: .25em;
     color: #1F4E78; margin-top: 0; }
h2 { font-size: 14pt; color: #1F4E78; margin-top: 1.4em;
     border-bottom: 1px solid #d0d7de; padding-bottom: .18em; page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #24292f; margin-top: 1.1em; page-break-after: avoid; }
h4 { font-size: 10.5pt; color: #444; page-break-after: avoid; }
p, li { orphans: 3; widows: 3; }
table { border-collapse: collapse; width: 100%; margin: .7em 0;
        font-size: 8.8pt; page-break-inside: avoid; }
th, td { border: 1px solid #d0d7de; padding: 4px 7px; text-align: left;
         vertical-align: top; word-break: break-word; }
th { background: #1F4E78; color: #fff; font-weight: 600; }
tr:nth-child(even) td { background: #f6f8fa; }
code { font-family: Consolas, "Courier New", monospace; font-size: 9pt;
       background: #f0f3f6; padding: 1px 4px; border-radius: 3px; }
pre { background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 5px;
      padding: 9px 11px; overflow-x: auto; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 8.5pt; line-height: 1.42; }
blockquote { border-left: 3px solid #1F4E78; margin: .7em 0; padding: .3em 0 .3em 12px;
             color: #444; background: #f6f8fa; }
a { color: #0969da; text-decoration: none; }
hr { border: none; border-top: 1px solid #d0d7de; margin: 1.3em 0; }
img { max-width: 100%; height: auto; display: block; margin: .8em auto;
      border: 1px solid #d0d7de; border-radius: 4px; page-break-inside: avoid; }
.footer { margin-top: 2.2em; padding-top: .6em; border-top: 1px solid #d0d7de;
          font-size: 8pt; color: #666; }
"""

HTML = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><title>{title}</title>
<style>{css}</style></head><body>
{body}
<div class="footer">HW06 - API Testing | Sinh vien 23127195 | Nguon: {src} |
Xuat tu Markdown bang scripts/export_pdf.py</div>
</body></html>"""


def embed_images(html, src_path):
    """Nhung anh cuc bo thanh data: URI.

    HTML tam duoc ghi o thu muc temp nen moi duong dan anh tuong doi trong
    Markdown se hong. Nhung thang vao file la cach chac chan nhat.
    """
    base = os.path.dirname(os.path.join(ROOT, src_path))
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".gif": "image/gif", ".svg": "image/svg+xml", ".webp": "image/webp"}

    def repl(m):
        pre, url, post = m.group(1), m.group(2), m.group(3)
        if re.match(r"^(https?:|data:)", url):
            return m.group(0)
        f = os.path.normpath(os.path.join(base, url.split("#")[0].split("?")[0]))
        ext = os.path.splitext(f)[1].lower()
        if not os.path.exists(f) or ext not in mime:
            print("[CANH BAO] khong nhung duoc anh: %s" % url, file=sys.stderr)
            return m.group(0)
        b64 = base64.b64encode(io.open(f, "rb").read()).decode("ascii")
        return '%sdata:%s;base64,%s%s' % (pre, mime[ext], b64, post)

    return re.sub(r'(<img[^>]*\ssrc=")([^"]+)(")', repl, html)


def find_chrome():
    for p in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]:
        if os.path.exists(p):
            return p
    for name in ("google-chrome", "chromium", "chromium-browser", "msedge"):
        p = shutil.which(name)
        if p:
            return p
    return None


def main():
    try:
        import markdown
    except ImportError:
        print("Can cai: pip install markdown", file=sys.stderr)
        return 1

    chrome = find_chrome()
    if not chrome:
        print("Khong tim thay Chrome/Edge de in PDF.", file=sys.stderr)
        return 1

    os.makedirs(OUT_DIR, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="hw06pdf-")
    ok = 0

    for src, out_name in DOCS:
        src_path = os.path.join(ROOT, src)
        if not os.path.exists(src_path):
            print("[BO QUA] %s (khong ton tai)" % src)
            continue

        text = io.open(src_path, encoding="utf-8").read()
        # Bo phan mo rong .md khoi lien ket noi bo cho gon khi in
        text = re.sub(r"\]\(([^)]+?)\.md(#[^)]*)?\)", r"](\1)", text)

        body = markdown.markdown(
            text, extensions=["tables", "fenced_code", "toc", "sane_lists", "nl2br"])
        body = embed_images(body, src)
        title = os.path.splitext(out_name)[0].replace("_", " ")
        html_path = os.path.join(tmp, out_name.replace(".pdf", ".html"))
        io.open(html_path, "w", encoding="utf-8").write(
            HTML.format(title=title, css=CSS, body=body, src=src))

        pdf_path = os.path.join(OUT_DIR, out_name)
        url = "file:///" + html_path.replace("\\", "/")
        cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
               "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
               "--virtual-time-budget=8000",
               "--print-to-pdf=" + pdf_path, url]
        subprocess.run(cmd, capture_output=True, timeout=120)

        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
            print("[OK] %-28s %6.1f KB" % (out_name, os.path.getsize(pdf_path) / 1024))
            ok += 1
        else:
            print("[LOI] %s — Chrome khong tao duoc PDF" % out_name, file=sys.stderr)

    shutil.rmtree(tmp, ignore_errors=True)
    print("\nDa xuat %d/%d file vao %s" % (ok, len(DOCS), OUT_DIR))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
