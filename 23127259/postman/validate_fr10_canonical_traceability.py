#!/usr/bin/env python3
"""
FR-10 Canonical Traceability Static Validator
Phase 2D.1D.3.1 – INT-049
Validates the executable collection against the machine-readable CANONICAL mapping (fr10_canonical_cases.json).
Includes hardened static checks for FR10-AI-028 fail-fast cryptographic tampering.
No network I/O.
"""

import json
import re
import sys
import hashlib

CANONICAL_CASES_PATH = "23127259/testcases/fr10_canonical_cases.json"
COLLECTION_PATH      = "23127259/postman/collections/FR10_Order_State_Machine.postman_collection.json"
RAW_AI_DRAFT_PATH    = "23127259/testcases/FR10_AI_DRAFT.md"
EXPECTED_RAW_AI_SHA  = "303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc"


def extract_collection_items(items):
    results = []
    for item in items:
        if "item" in item:
            results.extend(extract_collection_items(item["item"]))
        else:
            case_id = None
            m = re.search(r'FR10-(AI|HUM)-(\d+)', item.get("name", ""))
            if m:
                case_id = f"FR10-{m.group(1)}-{m.group(2).zfill(3)}"
            if case_id:
                r = item.get("request", {})
                method = r.get("method", "?")
                url = r.get("url", {})
                if isinstance(url, dict):
                    path_parts = url.get("path", [])
                    path_str = "/".join(str(p) for p in path_parts).lower()
                else:
                    path_str = str(url).lower()

                body = ""
                b = r.get("body", {})
                if b and b.get("mode") == "raw":
                    body = b.get("raw", "")

                headers = r.get("header", [])
                auth_headers = [h.get("value", "") for h in headers if "Authorization" in h.get("key", "")]

                prereq_script = ""
                for ev in item.get("event", []):
                    if ev.get("listen") == "prerequest":
                        prereq_script = "\n".join(ev.get("script", {}).get("exec", []))

                results.append({
                    "name": item.get("name", ""),
                    "case_id": case_id,
                    "method": method,
                    "path_str": path_str,
                    "body": body,
                    "auth_headers": auth_headers,
                    "prereq_script": prereq_script,
                })
    return results


def validate():
    print("=== FR-10 CANONICAL TRACEABILITY STATIC VALIDATOR ===\n")

    # Gate 1: Verify raw AI draft immutability
    with open(RAW_AI_DRAFT_PATH, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    if sha == EXPECTED_RAW_AI_SHA:
        print("[PASS] 1. Level-2 Raw AI Draft hash verified immutable (SHA-256 match).")
    else:
        print(f"[FAIL] 1. Raw AI Draft SHA mismatch: {sha}")
        return False

    # Load canonical cases JSON
    with open(CANONICAL_CASES_PATH) as f:
        canonical_cases = json.load(f)

    if len(canonical_cases) == 46:
        print(f"[PASS] 2. Canonical cases definition loaded: exactly 46 executable cases (AI-012 excluded).")
    else:
        print(f"[FAIL] 2. Canonical cases count mismatch: expected 46, got {len(canonical_cases)}")
        return False

    # Load executable collection
    with open(COLLECTION_PATH) as f:
        col = json.load(f)

    items = extract_collection_items(col.get("item", []))

    # Index collection items by case_id
    item_map = {}
    for item in items:
        cid = item["case_id"]
        if cid:
            item_map.setdefault(cid, []).append(item)

    # Perform canonical comparison
    match_count = 0
    drift_count = 0
    drift_details = []

    print("\n--- Canonical Traceability Audit (Collection vs. Canonical JSON) ---")
    for c in canonical_cases:
        cid = c["id"]
        entries = item_map.get(cid, [])
        if not entries:
            drift_count += 1
            drift_details.append((cid, "Missing from collection", "No items found in Postman collection"))
            print(f"  [MISSING] {cid}: No items found in collection")
            continue

        # Find target action item
        action_items = [e for e in entries if "ACTION" in e["name"] or "STEP" in e["name"]]
        if not action_items:
            action_items = entries

        # For HUM-003, select the cancellation action (ACTION-3)
        if cid == "FR10-HUM-003":
            hum3_actions = [e for e in entries if "ACTION-3" in e["name"]]
            if hum3_actions:
                action_items = hum3_actions

        action_item = action_items[0]
        mismatches = []

        # Check HTTP method
        if action_item["method"].upper() != c["method"].upper():
            mismatches.append(f"Method: expected {c['method']}, got {action_item['method']}")

        # Check endpoint
        expected_endpoint = c["endpoint"].lower()
        if "cancel" in expected_endpoint and "cancel" not in action_item["path_str"]:
            mismatches.append(f"Endpoint: expected cancel route ({c['endpoint']}), got {action_item['path_str']}")
        if "admin" in expected_endpoint and "admin" not in action_item["path_str"]:
            mismatches.append(f"Endpoint: expected admin route ({c['endpoint']}), got {action_item['path_str']}")

        # Check actor token in auth headers
        actor = c["actor"].lower()
        auth_str = " ".join(action_item["auth_headers"]).lower()
        if "admin" in actor and "unauthenticated" not in actor and "tampered" not in actor:
            if "admintoken" not in auth_str and "bearer" not in auth_str:
                mismatches.append(f"Actor: expected Admin auth, got '{auth_str[:50]}'")
        elif "tampered" in actor:
            if "tamperedadmintoken" not in auth_str:
                mismatches.append(f"Actor: expected tamperedAdminToken, got '{auth_str[:50]}'")
        elif "user a" in actor or "customer" in actor:
            if "admintoken" in auth_str:
                mismatches.append(f"Actor: expected User/Customer token, but found Admin token '{auth_str[:50]}'")
        elif "user b" in actor:
            if "userbtoken" not in auth_str:
                mismatches.append(f"Actor: expected User B token, got '{auth_str[:50]}'")

        # Hardened checks for AI-028
        if cid == "FR10-AI-028":
            prereq = action_item.get("prereq_script", "")
            if "adminToken" not in prereq:
                mismatches.append("AI-028 pre-request script must derive from adminToken")
            if "parts.length !== 3" not in prereq and "parts.length != 3" not in prereq:
                mismatches.append("AI-028 pre-request script must require exactly 3 JWT segments")
            if "throw new Error" not in prereq:
                mismatches.append("AI-028 pre-request script must fail-fast with throw new Error")
            if re.search(r'\.tampered|invalid\.token|garbage|eyJhbGciOi', prereq, re.IGNORECASE):
                mismatches.append("AI-028 contains forbidden fallback or hardcoded token pattern")

        if mismatches:
            drift_count += 1
            drift_details.append((cid, c["semantic_oracle"], "; ".join(mismatches)))
            print(f"  [DRIFT]   {cid}:")
            for m in mismatches:
                print(f"    -> {m}")
        else:
            match_count += 1
            print(f"  [CANONICAL-MATCH] {cid}: OK")

    print("\n--- Canonical Traceability Summary ---")
    print(f"  Total Canonical Cases: {len(canonical_cases)}")
    print(f"  Exact Canonical Match: {match_count}")
    print(f"  Semantic Drift Count:  {drift_count}")

    if drift_count > 0:
        print(f"\n[FAIL] Collection contains {drift_count} semantic drift(s) against canonical provenance.")
        return False
    else:
        print("\n[PASS] All 46 collection items match canonical provenance (including hardened AI-028 fail-fast).")
        return True


if __name__ == "__main__":
    ok = validate()
    sys.exit(0 if ok else 1)
