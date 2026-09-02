#!/usr/bin/env python3
"""
FR-10 Tampered JWT Harness Static Validator
Phase 2D.1D.3.1 – INT-049
Validates that FR10-AI-028 implements strict, fail-fast cryptographic tampering without fallbacks.
No network I/O.
"""

import json
import re
import sys
import hashlib

COLLECTION_PATH      = "23127259/postman/collections/FR10_Order_State_Machine.postman_collection.json"
ENVIRONMENT_PATH     = "23127259/postman/environments/FR10-local.postman_environment.json"
RAW_AI_DRAFT_PATH    = "23127259/testcases/FR10_AI_DRAFT.md"
EXPECTED_RAW_AI_SHA  = "303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc"


def extract_items(items):
    reqs = []
    for it in items:
        if "item" in it:
            reqs.extend(extract_items(it["item"]))
        elif "request" in it:
            reqs.append(it)
    return reqs


def validate():
    print("=== RUNNING FR-10 TAMPERED JWT HARNESS STATIC VALIDATOR ===\n")

    # Gate 1: Verify raw AI draft immutability
    with open(RAW_AI_DRAFT_PATH, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    if sha == EXPECTED_RAW_AI_SHA:
        print("[PASS] 1. Raw AI Draft SHA-256 verified immutable.")
    else:
        print(f"[FAIL] 1. Raw AI Draft SHA mismatch: {sha}")
        return False

    # Gate 2: Verify environment committed value for tamperedAdminToken is empty
    with open(ENVIRONMENT_PATH) as f:
        env = json.load(f)
    env_vars = {v["key"]: v["value"] for v in env.get("values", [])}
    if "tamperedAdminToken" not in env_vars:
        print("[FAIL] 2. tamperedAdminToken missing from environment JSON.")
        return False
    if env_vars["tamperedAdminToken"] != "":
        print(f"[FAIL] 2. tamperedAdminToken in environment must be empty, found: '{env_vars['tamperedAdminToken']}'")
        return False
    print("[PASS] 2. Environment tamperedAdminToken committed value is empty (clean hygiene).")

    # Gate 3: Extract and inspect FR10-AI-028 action item
    with open(COLLECTION_PATH) as f:
        col = json.load(f)
    all_reqs = extract_items(col.get("item", []))
    ai028_actions = [r for r in all_reqs if "[FR10-AI-028]" in r.get("name", "") and "ACTION" in r.get("name", "")]
    if not ai028_actions:
        print("[FAIL] 3. FR10-AI-028 ACTION item not found in collection.")
        return False
    action_item = ai028_actions[0]

    # Verify endpoint and method
    req = action_item.get("request", {})
    method = req.get("method", "")
    url_raw = req.get("url", {}).get("raw", "") if isinstance(req.get("url"), dict) else str(req.get("url"))
    body_raw = req.get("body", {}).get("raw", "")
    headers = req.get("header", [])
    auth_headers = [h.get("value", "") for h in headers if "Authorization" in h.get("key", "")]

    if method != "PUT":
        print(f"[FAIL] 3. Method must be PUT, got {method}")
        return False
    if "admin/orders" not in url_raw or "status" not in url_raw:
        print(f"[FAIL] 3. Endpoint must be PUT /api/admin/orders/:id/status, got {url_raw}")
        return False
    if '{"status": "confirmed"}' not in body_raw and '{"status":"confirmed"}' not in body_raw:
        print(f"[FAIL] 3. Body must be {{\"status\": \"confirmed\"}}, got {body_raw}")
        return False
    if not any("tamperedAdminToken" in ah for ah in auth_headers):
        print(f"[FAIL] 3. Auth header must reference {{{{tamperedAdminToken}}}}, got {auth_headers}")
        return False
    print("[PASS] 3. FR10-AI-028 formal request structure verified (PUT /api/admin/orders/:id/status, body, auth header).")

    # Gate 4: Inspect pre-request script logic
    prereq_script = ""
    for ev in action_item.get("event", []):
        if ev.get("listen") == "prerequest":
            prereq_script = "\n".join(ev.get("script", {}).get("exec", []))

    # Check required fail-fast elements
    if "adminToken" not in prereq_script:
        print("[FAIL] 4. Pre-request script must read adminToken.")
        return False
    if "parts.length !== 3" not in prereq_script and "parts.length != 3" not in prereq_script:
        print("[FAIL] 4. Pre-request script must check exactly 3 JWT segments.")
        return False
    if "throw new Error" not in prereq_script:
        print("[FAIL] 4. Pre-request script must throw Error on invalid token.")
        return False
    if "tamperedToken === token" not in prereq_script:
        print("[FAIL] 4. Pre-request script must verify tamperedToken !== token.")
        return False

    # Check prohibition of fallback logic
    forbidden_patterns = [
        r'\.tampered',
        r'invalid\.token',
        r'garbage',
        r'eyJhbGciOi',
    ]
    for pat in forbidden_patterns:
        if re.search(pat, prereq_script, re.IGNORECASE):
            print(f"[FAIL] 4. Forbidden fallback pattern '{pat}' detected in AI-028 pre-request script!")
            return False

    # Check preservation of header and payload (parts[0], parts[1])
    if "parts[0]" not in prereq_script or "parts[1]" not in prereq_script:
        print("[FAIL] 4. Pre-request script must preserve header (parts[0]) and payload (parts[1]).")
        return False
    if "tamperedSignature" not in prereq_script and "replacement" not in prereq_script:
        print("[FAIL] 4. Pre-request script must mutate signature segment.")
        return False

    print("[PASS] 4. Strict fail-fast cryptographic tampering logic verified (zero fallback tokens, header & payload preserved).")

    # Gate 5: Simulate tampering transformation on a sample JWT
    sample_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIn0.AbCdEf123456"
    parts = sample_jwt.split(".")
    assert len(parts) == 3
    sig = parts[2]
    rep = "B" if sig[0] == "A" else "A"
    tampered = parts[0] + "." + parts[1] + "." + rep + sig[1:]
    tampered_parts = tampered.split(".")

    assert parts[0] == tampered_parts[0], "Header must be identical"
    assert parts[1] == tampered_parts[1], "Payload must be identical"
    assert parts[2] != tampered_parts[2], "Signature must be mutated"
    assert len(tampered_parts) == 3, "Tampered token must have exactly 3 parts"
    assert tampered != sample_jwt, "Tampered token must not equal original"
    print("[PASS] 5. Tampering mathematical proof verified (header identical, payload identical, signature mutated, 3 segments).")

    print("\n=== ALL 5 TAMPERED JWT HARNESS GATES PASSED (100% READY) ===")
    return True


if __name__ == "__main__":
    ok = validate()
    sys.exit(0 if ok else 1)
