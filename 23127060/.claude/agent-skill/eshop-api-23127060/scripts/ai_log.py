#!/usr/bin/env python3
"""ai_log.py — ghi nhat ky moi luot lam viec voi AI (bat buoc cho AI_Audit_Report).

  # them 1 entry (goi SAU MOI luot tra loi cua agent)
  python3 ai_log.py add --root . --tool "Claude Code (sonnet-4.5)" --step "STEP 3" \
      --title "Sinh 4 file jmx" --prompt "noi dung prompt goc" --output "tom tat output" \
      --files "testplans/23127060_Load_20260831.jmx" --human-verified pending

  # hoac tro toi file da luu san
  python3 ai_log.py add --root . --prompt-file ai/interactions/x_PROMPT.txt --output-file ai/interactions/x_OUTPUT.md ...

  python3 ai_log.py verify --root . --id 7 --status yes --note "da doi chieu jtl"
  python3 ai_log.py build-audit --root . --sid 23127060   # sinh ai/AI_AUDIT_REPORT.md tu AI_log.md
  python3 ai_log.py stats --root .
"""
import argparse, os, re, sys
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=7))
HEADER = """# AI_log — Nhật ký làm việc với AI (HW06 API Testing, SV {sid})

Mỗi lượt chat là một entry. Prompt gốc và output đầy đủ em lưu trong `ai/interactions/`.
File này là nguồn duy nhất để sinh ra `ai/audit/AI_AUDIT_REPORT.md` (`ai_log.py build-audit`).

"""


def slug(s, n=40):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", (s or "entry").lower()).strip("-")
    return (s[:n] or "entry")


def paths(root):
    ai = os.path.join(root, "ai")
    inter = os.path.join(ai, "interactions")
    os.makedirs(inter, exist_ok=True)
    return ai, inter, os.path.join(ai, "AI_log.md")


def next_id(log):
    if not os.path.exists(log):
        return 1
    ids = [int(m) for m in re.findall(r"^### #(\d+) ", open(log, encoding="utf-8").read(), re.M)]
    return (max(ids) + 1) if ids else 1


def cmd_add(a):
    ai, inter, log = paths(a.root)
    now = datetime.now(TZ)
    stamp = now.strftime("%Y%m%dT%H%M%S%z")
    n = next_id(log)
    sl = slug(a.title)

    prompt_path = a.prompt_file
    if not prompt_path:
        if not a.prompt:
            print("Can --prompt hoac --prompt-file", file=sys.stderr)
            sys.exit(2)
        prompt_path = os.path.join(inter, f"{stamp}_{sl}_PROMPT.txt")
        open(prompt_path, "w", encoding="utf-8").write(a.prompt.rstrip() + "\n")
    output_path = a.output_file
    if not output_path and a.output:
        output_path = os.path.join(inter, f"{stamp}_{sl}_OUTPUT.md")
        open(output_path, "w", encoding="utf-8").write(a.output.rstrip() + "\n")

    excerpt = ""
    try:
        lines = [l.strip() for l in open(prompt_path, encoding="utf-8").read().splitlines() if l.strip()]
        excerpt = " ".join(lines[:2])[:300]
    except Exception:
        pass

    if not os.path.exists(log):
        open(log, "w", encoding="utf-8").write(HEADER.format(sid=a.sid))
    rel = lambda p: os.path.relpath(p, a.root) if p else "-"
    entry = (f"### #{n} · {now.isoformat(timespec='seconds')} · {a.step or '-'} · {a.title}\n"
             f"- Tool: {a.tool}\n"
             f"- Prompt: `{rel(prompt_path)}`\n"
             + (f"  > {excerpt}\n" if excerpt else "")
             + f"- Output: `{rel(output_path)}`\n"
             f"- Files touched: {a.files or '-'}\n"
             f"- Human verified: {a.human_verified}\n\n")
    open(log, "a", encoding="utf-8").write(entry)
    print(f"AI_log: da ghi entry #{n} ({sl}) -> {rel(log)}")
    print(f"  prompt: {rel(prompt_path)}")
    if output_path:
        print(f"  output: {rel(output_path)}")


def cmd_verify(a):
    _, _, log = paths(a.root)
    txt = open(log, encoding="utf-8").read()
    pat = re.compile(rf"(### #{a.id} .*?- Human verified: )([^\n]*)", re.S)
    if not pat.search(txt):
        print(f"Khong thay entry #{a.id}", file=sys.stderr)
        sys.exit(1)
    new = f"{a.status} ({datetime.now(TZ).date()})" + (f" — {a.note}" if a.note else "")
    open(log, "w", encoding="utf-8").write(pat.sub(lambda m: m.group(1) + new, txt, count=1))
    print(f"entry #{a.id} -> Human verified: {new}")


def parse_entries(log):
    txt = open(log, encoding="utf-8").read()
    out = []
    for block in re.split(r"\n(?=### #)", txt):
        m = re.match(r"### #(\d+) · ([^·]+) · ([^·]*) · (.+)", block.strip())
        if not m:
            continue
        g = lambda k, d="-": (re.search(rf"- {k}: (.+)", block) or [None, d])[1].strip()
        out.append({"id": m.group(1), "ts": m.group(2).strip(), "step": m.group(3).strip(),
                    "title": m.group(4).strip(), "tool": g("Tool"), "prompt": g("Prompt"),
                    "output": g("Output"), "files": g("Files touched"), "verified": g("Human verified")})
    return out


def cmd_build_audit(a):
    ai, _, log = paths(a.root)
    if not os.path.exists(log):
        print("Chua co ai/AI_log.md", file=sys.stderr)
        sys.exit(1)
    e = parse_entries(log)
    tools = sorted({x["tool"] for x in e})
    L = [f"# AI Audit Report — HW06 API Testing (SV {a.sid} — Ninh Văn Khải)", "",
         "> Phụ lục bắt buộc theo đề bài mục 9.", "",
         "## Tuyên bố sử dụng AI", "",
         "**I use AI tools for the following tasks.**", "",
         "Toàn bộ quá trình em làm HW06 (sinh test case từ API spec, audit, mở rộng, dựng Postman",
         "collection, phân tích kết quả Newman, soạn báo cáo) đều có sự tham gia của công cụ AI.",
         "Mỗi lượt tương tác đều được ghi lại tự động ngay tại thời điểm nó xảy ra bằng",
         "`agent-skill/eshop-api-23127060/scripts/ai_log.py`, em không viết lại từ trí nhớ.", "",
         "| Công cụ AI đã dùng | Vai trò |", "|---|---|"]
    for t in tools:
        L.append(f"| {t} | Sinh / biến đổi tài liệu và test case, chạy script, tổng hợp báo cáo |")
    L += ["",
         "Các kết quả số liệu (passed/failed) **không** do AI ước lượng, mà được tính từ file",
         "`newman/*.json` thật qua `scripts/summarize_newman.py`. Sơ đồ bộ sinh test là do em",
         "**tự vẽ**, không do AI sinh (đề bài mục 11).", "",
         f"Sinh từ `ai/AI_log.md` lúc {datetime.now(TZ).isoformat(timespec='seconds')} · tổng {len(e)} lượt tương tác.",
         "", "## Phụ lục A — Bảng tương tác AI", "",
         "| # | Thời điểm | Bước | Tool | Nội dung | Prompt gốc | Output | Human verified |",
         "|---|---|---|---|---|---|---|---|"]
    for x in e:
        L.append(f"| {x['id']} | {x['ts']} | {x['step']} | {x['tool']} | {x['title']} | "
                 f"{x['prompt']} | {x['output']} | {x['verified']} |")
    L += ["", "## Phụ lục B — Chi tiết từng lượt", ""]
    for x in e:
        L += [f"### #{x['id']} · {x['title']}", f"- Thời điểm: {x['ts']} · Bước: {x['step']} · Tool: {x['tool']}",
              f"- Prompt: {x['prompt']}", f"- Output: {x['output']}",
              f"- Files: {x['files']}", f"- Human verified: {x['verified']}", ""]
    L += ["## Ghi chú", "",
          "- Toàn bộ prompt gốc (nguyên văn) và output nằm trong `ai/interactions/`.",
          "- Cột `Human verified` = `yes` nghĩa là em đã đọc lại và chịu trách nhiệm về kết quả lượt đó.",
          "- Số liệu passed/failed trong báo cáo được tính từ `newman/*.json` bằng",
          "  `scripts/summarize_newman.py`, không do AI ước lượng.",
          "- Sơ đồ bộ sinh test (`agent-skill/diagram/`) là do em tự vẽ, không do AI sinh."]
    outdir = os.path.join(ai, "audit")
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "AI_AUDIT_REPORT.md")
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote", p, f"({len(e)} entries)")


def cmd_stats(a):
    _, _, log = paths(a.root)
    if not os.path.exists(log):
        print("0 entry")
        return
    e = parse_entries(log)
    pend = [x["id"] for x in e if x["verified"].startswith("pending")]
    print(f"tong entry: {len(e)} · pending human verify: {len(pend)}" + (f" (#{', #'.join(pend)})" if pend else ""))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    common = lambda p: (p.add_argument("--root", default="."), p.add_argument("--sid", default="23127060"))

    p = sub.add_parser("add"); common(p)
    p.add_argument("--tool", default="Claude Code")
    p.add_argument("--step", default="")
    p.add_argument("--title", required=True)
    p.add_argument("--prompt")
    p.add_argument("--prompt-file")
    p.add_argument("--output")
    p.add_argument("--output-file")
    p.add_argument("--files")
    p.add_argument("--human-verified", default="pending", choices=["pending", "yes", "rejected"])
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("verify"); common(p)
    p.add_argument("--id", required=True)
    p.add_argument("--status", default="yes", choices=["yes", "rejected", "pending"])
    p.add_argument("--note")
    p.set_defaults(fn=cmd_verify)

    p = sub.add_parser("build-audit"); common(p); p.set_defaults(fn=cmd_build_audit)
    p = sub.add_parser("stats"); common(p); p.set_defaults(fn=cmd_stats)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
