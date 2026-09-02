#!/usr/bin/env python3
"""
FR-10 Canonical Traceability Static Validator
Phase 2D.1D.2 – INT-047
Validates the executable collection against the machine-readable CANONICAL mapping (fr10_canonical_cases.json).
Does NOT use FR10_FINAL_EXECUTABLE_SUITE.md as its oracle authority.
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

                results.append({
                    "name": item.get("name", ""),
                    "case_id": case_id,
                    "method": method,
                    "path_str": path_str,
                    "body": body,
                    "auth_headers": auth_headers,
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
        if "admin" in actor and "unauthenticated" not in actor:
            if "admintoken" not in auth_str and "bearer" not in auth_str:
                mismatches.append(f"Actor: expected Admin auth, got '{auth_str[:50]}'")
        elif "user a" in actor or "customer" in actor:
            if "admintoken" in auth_str:
                mismatches.append(f"Actor: expected User/Customer token, but found Admin token '{auth_str[:50]}'")
        elif "user b" in actor:
            if "userbtoken" not in auth_str:
                mismatches.append(f"Actor: expected User B token, got '{auth_str[:50]}'")

        # Check specific drifted cases from provenance analysis
        if cid == "FR10-AI-028" and "admin" not in action_item["path_str"]:
            mismatches.append("Canonical AI-028 requires Tampered JWT on Admin Status (PUT /api/admin/orders/:id/status), collection implements Customer Cancel")
        if cid == "FR10-AI-029" and "malformed" in auth_str:
            mismatches.append("Canonical AI-029 requires Missing Auth on Customer Cancel, collection implements Malformed Bearer")
        if cid == "FR10-AI-031" and "cancel" in action_item["path_str"]:
            mismatches.append("Canonical AI-031 requires User A on Admin Status Cancel (PUT /api/admin/orders/:id/status), collection implements Admin on Customer Cancel")
        if cid == "FR10-AI-032" and "guesttoken" in auth_str:
            mismatches.append("Canonical AI-032 requires User A (role=user) on Admin Status Shipping, collection implements Guest token")

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
        print(f"\n[DRIFT DETECTED] Collection contains {drift_count} semantic drift(s) against canonical provenance.")
        print("Affected Drift Cases:")
        for d in drift_details:
            print(f"  - {d[0]}: {d[2]}")
        print("\nNext Phase Required: PHASE 2D.1D.3 – Collection Semantic Repair for Run 03.")
        return False
    else:
        print("\n[PASS] All collection items match canonical provenance.")
        return True


if __name__ == "__main__":
    ok = validate()
    # Exit with code 0 to allow audit reporting without script failure abort
    sys.exit(0 if ok else 2)
