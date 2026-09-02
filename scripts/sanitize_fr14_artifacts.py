#!/usr/bin/env python3
"""
Sanitize FR14 Newman exports to remove resolved JWT/Bearer credentials.
Produces disclosure-controlled artifacts for grader navigation.

Source: 23127259/evidence/fr14/newman/FR14-run01.{json,html}
Output: 23127259/evidence/fr14/newman/FR14-run01-sanitized.{json,html}

This script never modifies the raw run01 files. The sanitized copies preserve
test names, methods, endpoints, statuses, assertion names, pass/fail counts,
timings, and error descriptions — but redact JWT/Bearer/Authorization values.
"""

import json
import re
import sys
from pathlib import Path

EVIDENCE_DIR = Path("23127259/evidence/fr14/newman")

# Patterns that indicate resolved credentials
JWT_PATTERN = re.compile(r"eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+")
BEARER_PATTERN = re.compile(r"Bearer\s+[A-Za-z0-9._\-]+")
AUTH_HEADER_PATTERN = re.compile(r'"Authorization"\s*:\s*"[^"]*"')


def redact_text(text):
    text = JWT_PATTERN.sub("[JWT_REDACTED]", text)
    text = BEARER_PATTERN.sub("Bearer [TOKEN_REDACTED]", text)
    return text


def sanitize_json(src, dst):
    """Sanitize a Newman JSON export, redacting resolved credentials."""
    with open(src, encoding="utf-8") as f:
        data = json.load(f)

    # Walk all string fields and redact; preserve structure
    def walk(obj):
        if isinstance(obj, dict):
            return {k: walk(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [walk(x) for x in obj]
        if isinstance(obj, str):
            return redact_text(obj)
        return obj

    sanitized = walk(data)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(sanitized, f, ensure_ascii=False, indent=2)


def sanitize_html(src, dst):
    text = src.read_text(encoding="utf-8", errors="replace")
    text = redact_text(text)
    # Also redact "Bearer [TOKEN_REDACTED]" within Authorization strings
    text = AUTH_HEADER_PATTERN.sub('"Authorization": "[REDACTED]"', text)
    dst.write_text(text, encoding="utf-8")


def verify_no_secrets(path):
    """Confirm no JWT/Bearer token remains in the sanitized output."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    jwt_count = len(JWT_PATTERN.findall(text))
    bearer_count = len(re.findall(r"Bearer\s+[A-Za-z0-9._\-]{20,}", text))
    return jwt_count, bearer_count


def main():
    src_json = EVIDENCE_DIR / "FR14-run01.json"
    src_html = EVIDENCE_DIR / "FR14-run01.html"
    dst_json = EVIDENCE_DIR / "FR14-run01-sanitized.json"
    dst_html = EVIDENCE_DIR / "FR14-run01-sanitized.html"

    if not src_json.exists() or not src_html.exists():
        print("Source artifacts missing; run canonical Newman first.")
        sys.exit(1)

    sanitize_json(src_json, dst_json)
    sanitize_html(src_html, dst_html)

    for path in [dst_json, dst_html]:
        jwt_count, bearer_count = verify_no_secrets(path)
        print(f"{path}: JWT={jwt_count}, Bearer={bearer_count}")


if __name__ == "__main__":
    main()
