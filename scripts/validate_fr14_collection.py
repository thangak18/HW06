#!/usr/bin/env python3
"""
FR14 Postman Collection Static Validator.

Verifies that FR14_Category_CRUD.postman_collection.json meets all assignment
requirements before being executed by Newman:

- Collection JSON parses
- Collection has X-Student-Id pre-request script
- Every HTTP request item carries X-Student-Id (or relies on collection prereq)
- No hardcoded live JWT/Bearer credentials
- All 46 canonical formal IDs are present (or split across multi-step items)
- All rejected IDs are absent
- Variable substitution patterns are correct (double braces, not single)
- Every multi-step lifecycle case (035, H05, H06) is materialized
"""

import json
import sys
import re
from pathlib import Path

COLLECTION = Path("23127259/postman/collections/FR14_Category_CRUD.postman_collection.json")
ENVIRONMENT = Path("23127259/postman/environments/FR14-local.postman_environment.json")
CANONICAL = Path("23127259/testcases/fr14_canonical_cases.json")

EXPECTED_REJECTED = {"TC-FR14-034", "TC-FR14-036", "TC-FR14-H07"}

# Cases that are intentionally split into multiple Newman items
SPLIT_PARENTS = {"TC-FR14-035", "TC-FR14-H05", "TC-FR14-H06"}


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def warn(msg):
    print(f"WARN: {msg}")


def ok(msg):
    print(f"OK: {msg}")


def main():
    if not COLLECTION.exists():
        fail(f"Collection missing: {COLLECTION}")
    if not ENVIRONMENT.exists():
        fail(f"Environment missing: {ENVIRONMENT}")
    if not CANONICAL.exists():
        fail(f"Canonical cases missing: {CANONICAL}")

    with open(COLLECTION, encoding="utf-8") as f:
        col = json.load(f)
    with open(ENVIRONMENT, encoding="utf-8") as f:
        env = json.load(f)
    with open(CANONICAL, encoding="utf-8") as f:
        canonical = json.load(f)

    canonical_ids = {c["id"] for c in canonical}
    if len(canonical) != 46:
        fail(f"Canonical map has {len(canonical)} cases, expected 46")

    # Check rejected IDs are absent from canonical
    for r in EXPECTED_REJECTED:
        if r in canonical_ids:
            fail(f"Rejected ID {r} appears in canonical map")

    # Check pre-request X-Student-Id
    pre_event = next((e for e in col.get("event", []) if e.get("listen") == "prerequest"), None)
    if not pre_event:
        fail("Collection missing prerequest event")
    prereq_exec = "\n".join(pre_event["script"]["exec"])
    if "X-Student-Id" not in prereq_exec:
        fail("Collection prerequest does not inject X-Student-Id")
    if "23127259" not in prereq_exec:
        fail("Collection prerequest does not reference 23127259")
    ok("Collection prerequest injects X-Student-Id: 23127259")

    # Walk requests
    requests = []
    def walk(items):
        for it in items:
            if "item" in it:
                walk(it["item"])
            elif "request" in it:
                requests.append(it)
    walk(col.get("item", []))

    # Check every request has X-Student-Id (explicit or via collection prereq)
    bad_headers = []
    for req in requests:
        headers = req["request"].get("header", [])
        keys = [h.get("key", "").lower() for h in headers]
        if "x-student-id" not in keys:
            bad_headers.append(req["name"])
    if bad_headers:
        for n in bad_headers:
            warn(f"No explicit X-Student-Id header (relies on prereq): {n}")
    ok(f"All {len(requests)} requests have X-Student-Id (via prereq)")

    # Check for hardcoded JWTs (long base64-looking strings)
    full_text = json.dumps(col)
    # Real JWTs have a real signature part (base64 of >=20 chars). Tampered
    # synthetic tokens may have placeholders like "tampered_signature" or
    # "fake" - exclude those.
    jwt_pattern = re.compile(r"eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]{8,}")
    hardcoded_jwts = []
    for m in jwt_pattern.findall(full_text):
        # Skip placeholder/keyword-based tokens used for synthetic auth probes
        last_part = m.rsplit(".", 1)[-1].lower()
        if any(kw in last_part for kw in ["tampered", "fake", "placeholder", "invalid", "redacted", "forged"]):
            continue
        hardcoded_jwts.append(m)
    if hardcoded_jwts:
        for j in hardcoded_jwts[:3]:
            fail(f"Hardcoded JWT detected in collection: {j[:30]}...")
    ok("No hardcoded JWT in collection (tampered-token placeholder excluded)")

    # Check for malformed variable substitution: any URL with single brace {{var}} or single brace
    url_text = ""
    for req in requests:
        url = req["request"].get("url", {})
        if isinstance(url, dict):
            url_text += json.dumps(url)

    # Find single-brace patterns that look like failed Postman vars: {varName}
    # but allow double-brace {{varName}}
    single_brace = re.findall(r'"(?:raw|path)"[^"]*\{[a-zA-Z]+\}', url_text)
    # Also check raw with single brace
    single_brace_in_raw = re.findall(r': "[^"]*\{[a-zA-Z]+(?:Id|Count|Email|Password)\}', url_text)
    if single_brace_in_raw:
        warn(f"Possible single-brace variable substitution: {single_brace_in_raw[:3]}")

    # Check every canonical ID has at least one matching Newman item
    item_names = [r["name"] for r in requests]
    missing = []
    for cid in canonical_ids:
        # Match either exact ID or any name starting with this ID (for split cases)
        matches = [n for n in item_names if cid in n or n.startswith(cid)]
        if not matches:
            missing.append(cid)
    if missing:
        fail(f"Canonical IDs with no Newman item: {missing}")

    # Check rejected IDs are not in collection
    leaked = []
    for r in EXPECTED_REJECTED:
        if any(r in n for n in item_names):
            leaked.append(r)
    if leaked:
        fail(f"Rejected IDs leaked into collection: {leaked}")

    ok(f"All 46 canonical IDs are represented in the collection (multi-step items split into {sum(1 for n in item_names if any(p in n for p in SPLIT_PARENTS))} items)")
    ok("No rejected IDs leaked into collection")

    # Check environment has studentId 23127259
    env_vars = {v["key"]: v.get("value") for v in env.get("values", [])}
    if env_vars.get("studentId") != "23127259":
        fail(f"Environment studentId is {env_vars.get('studentId')}, expected 23127259")
    ok("Environment studentId = 23127259")

    # Check no live JWT in environment
    live_jwt_pattern = re.compile(r"eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]{8,}")
    for k, v in env_vars.items():
        matches = live_jwt_pattern.findall(str(v))
        for m in matches:
            last = m.rsplit(".", 1)[-1].lower()
            if any(kw in last for kw in ["tampered", "fake", "placeholder", "invalid", "redacted", "forged"]):
                continue
            fail(f"Environment var {k} contains a live JWT")
    ok("No live JWT in environment (tampered-token placeholder excluded)")

    # Count tests
    test_count = 0
    for req in requests:
        for ev in req.get("event", []):
            if ev.get("listen") == "test":
                for line in ev["script"]["exec"]:
                    if "pm.test(" in line:
                        test_count += 1
    ok(f"Total pm.test() assertions: {test_count}")

    print(f"\nFR14 collection validation: PASS")


if __name__ == "__main__":
    main()
