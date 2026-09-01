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
HEADER = """# AI_log — Nhat ky lam viec voi AI (HW06 API Testing, SV {sid})

Moi luot chat = 1 entry. Prompt goc va output day du luu trong `ai/interactions/`.
File nay la nguon duy nhat de sinh `ai/audit/AI_AUDIT_REPORT.md` (`ai_log.py build-audit`).

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
    L = [f"# AI Audit Report — HW06 API Testing (SV {a.sid} — Ninh Van Khai)", "",
         "> Phu luc bat buoc theo de bai muc 9.", "",
         "## Tuyen bo su dung AI", "",
         "**I use AI tools for the following tasks.**", "",
         "Toan bo qua trinh lam HW06 (sinh test case tu API spec, audit, mo rong, dung Postman",
         "collection, phan tich ket qua Newman, soan bao cao) deu co su tham gia cua cong cu AI.",
         "Moi luot tuong tac deu duoc ghi lai tu dong ngay tai thoi diem xay ra bang",
         "`agent-skill/eshop-api-23127060/scripts/ai_log.py`, khong viet lai tu tri nho.", "",
         "| Cong cu AI da dung | Vai tro |", "|---|---|"]
    for t in tools:
        L.append(f"| {t} | Sinh / bien doi tai lieu va test case, chay script, tong hop bao cao |")
    L += ["",
         "Cac ket qua so lieu (passed/failed) **khong** do AI uoc luong ma duoc tinh tu file",
         "`newman/*.json` that qua `scripts/summarize_newman.py`. So do bo sinh test do sinh vien",
         "**tu ve**, khong do AI sinh (de bai muc 11).", "",
         f"Sinh tu `ai/AI_log.md` luc {datetime.now(TZ).isoformat(timespec='seconds')} · tong {len(e)} luot tuong tac.",
         "", "## Phu luc A — Bang tuong tac AI", "",
         "| # | Thoi diem | Buoc | Tool | Noi dung | Prompt goc | Output | Human verified |",
         "|---|---|---|---|---|---|---|---|"]
    for x in e:
        L.append(f"| {x['id']} | {x['ts']} | {x['step']} | {x['tool']} | {x['title']} | "
                 f"{x['prompt']} | {x['output']} | {x['verified']} |")
    L += ["", "## Phu luc B — Chi tiet tung luot", ""]
    for x in e:
        L += [f"### #{x['id']} · {x['title']}", f"- Thoi diem: {x['ts']} · Buoc: {x['step']} · Tool: {x['tool']}",
              f"- Prompt: {x['prompt']}", f"- Output: {x['output']}",
              f"- Files: {x['files']}", f"- Human verified: {x['verified']}", ""]
    L += ["## Ghi chu", "",
          "- Toan bo prompt goc (nguyen van) va output nam trong `ai/interactions/`.",
          "- Cot `Human verified` = `yes` nghia la sinh vien da doc lai va chiu trach nhiem ve ket qua luot do.",
          "- So lieu passed/failed trong bao cao duoc tinh tu `newman/*.json` bang",
          "  `scripts/summarize_newman.py`, khong do AI uoc luong.",
          "- So do bo sinh test (`agent-skill/diagram/`) do sinh vien tu ve, khong do AI sinh."]
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
