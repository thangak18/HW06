#!/usr/bin/env python3
"""
FR-10 Semantic Traceability Static Validator
Phase 2D.1D.1 – INT-046
Validates the collection against a machine-readable frozen semantic mapping.
No network I/O.
"""

import json
import re
import sys
import hashlib

COLLECTION_PATH = "23127259/postman/collections/FR10_Order_State_Machine.postman_collection.json"
RAW_AI_PATH     = "23127259/testcases/FR10_AI_DRAFT.md"
EXPECTED_RAW_AI_SHA256 = "303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc"

# Frozen semantic mapping keyed by formal ID
# method: required HTTP method for action item
# path_must: substring that MUST appear in the action URL path
# path_not: substring that must NOT appear in the action URL path
# actor: environment variable name that must appear in auth headers for this action
# body_must_contain: exact string that must appear in action request body
# action_keyword: keyword to identify the action item (default: ACTION)
FROZEN_MAP = {
    # AI-001..008: Forward/cancellation cases
    "FR10-AI-001": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="confirmed"),
    "FR10-AI-002": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="shipping"),
    "FR10-AI-003": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="delivered"),
    "FR10-AI-004": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", action_keyword="STEP"),
    "FR10-AI-005": dict(method="PUT", path_must="cancel", path_not="admin", actor="userAToken"),
    "FR10-AI-006": dict(method="PUT", path_must="cancel", path_not="admin", actor="userAToken"),
    "FR10-AI-007": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="canceled"),
    "FR10-AI-008": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="canceled"),
    # AI-009..011, 013..015: Invalid skip/backward - action body is the FORBIDDEN target
    "FR10-AI-009": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="shipping"),
    "FR10-AI-010": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="delivered"),
    "FR10-AI-011": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="delivered"),
    "FR10-AI-013": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="pending"),
    "FR10-AI-014": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="confirmed"),
    "FR10-AI-015": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="pending"),
    # CRITICAL: AI-016 must use CANCEL endpoint by owner User
    "FR10-AI-016": dict(method="PUT", path_must="cancel", path_not="admin", actor="userAToken",
                        note="CRITICAL: Must be PUT /api/orders/:id/cancel by owner User, NOT admin/status"),
    # AI-017..023: Terminal/backward immutability - action body is the FORBIDDEN target
    # (body specifies what transition is being attempted, which should fail)
    "FR10-AI-017": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="pending"),
    "FR10-AI-018": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="confirmed"),
    "FR10-AI-019": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="shipping"),
    "FR10-AI-020": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="canceled"),
    "FR10-AI-021": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="pending"),
    "FR10-AI-022": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="confirmed"),
    "FR10-AI-023": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="shipping"),
    # CRITICAL: AI-024 Admin admin/status on canceled->delivered
    "FR10-AI-024": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="delivered",
                        note="CRITICAL: canceled->delivered via admin/status"),
    # SEC-02 authentication boundary cases
    "FR10-AI-025": dict(method="PUT", path="api/admin/orders", path_not="cancel", no_actor=True,
                        note="No Authorization header on admin/status"),
    "FR10-AI-026": dict(method="PUT", path="api/admin/orders", path_not="cancel", auth_fixed_contains="malformed",
                        note="Malformed bearer on admin/status"),
    "FR10-AI-027": dict(method="PUT", path="api/admin/orders", path_not="cancel",
                        note="Bad signature JWT on admin/status"),
    # CRITICAL: AI-028/029 must use CANCEL endpoint
    "FR10-AI-028": dict(method="PUT", path_must="cancel", path_not="admin", no_actor=True,
                        note="CRITICAL: No auth on PUT /api/orders/:id/cancel"),
    "FR10-AI-029": dict(method="PUT", path_must="cancel", path_not="admin", auth_fixed_contains="malformed",
                        note="CRITICAL: Malformed bearer on PUT /api/orders/:id/cancel"),
    # SEC-03 RBAC
    "FR10-AI-030": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="userAToken",
                        note="role=user token on admin/status"),
    # AI-031: Admin token on cancel endpoint (frozen spec: Admin on cancel)
    "FR10-AI-031": dict(method="PUT", path_must="cancel", path_not="admin", actor="adminToken",
                        note="Admin token on customer cancel endpoint"),
    # AI-032: Guest/Non-Admin on admin/status (any non-admin or guest token)
    "FR10-AI-032": dict(method="PUT", path="api/admin/orders", path_not="cancel",
                        note="Guest/non-admin token on admin/status"),
    # Ownership cases - CANCEL endpoint
    "FR10-AI-033": dict(method="PUT", path_must="cancel", path_not="admin", actor="userBToken",
                        note="User B on User A pending order cancel"),
    "FR10-AI-034": dict(method="PUT", path_must="cancel", path_not="admin", actor="userBToken",
                        note="User B on User A confirmed order cancel"),
    # Input domain - exact body values
    "FR10-AI-035": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="processing"),
    "FR10-AI-036": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_exact="{}"),
    "FR10-AI-037": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="null"),
    "FR10-AI-038": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="123"),
    # Edge cases
    "FR10-AI-039": dict(method="PUT", path_must="999999", actor="adminToken", note="Non-existent numeric ID"),
    "FR10-AI-040": dict(method="PUT", path_must="not-an-id", actor="adminToken", note="Malformed non-numeric ID"),
    "FR10-AI-041": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken", body_must_contain="confirmed"),
    "FR10-AI-042": dict(method="PUT", path="api/admin/orders", note="SEC-05 SQLi probe"),
    # Human cases
    "FR10-HUM-001": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken"),
    "FR10-HUM-002": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken"),
    # CRITICAL: HUM-003 key action is the CANCEL step (ACTION-3), not the setup admin transitions
    "FR10-HUM-003": dict(method="PUT", path_must="cancel", path_not="admin", actor="userAToken",
                         action_keyword="ACTION-3",
                         note="CRITICAL: Owner cancel during shipping via PUT /api/orders/:id/cancel"),
    "FR10-HUM-004": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken"),
    "FR10-HUM-005": dict(method="PUT", path="api/admin/orders", path_not="cancel", actor="adminToken"),
}

EXCLUDED_IDS = {"FR10-AI-012"}


def extract_items(items):
    results = []
    for item in items:
        if "item" in item:
            results.extend(extract_items(item["item"]))
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
                auth_header_vals = [h.get("value", "") for h in headers if "Authorization" in h.get("key", "")]

                results.append({
                    "name": item.get("name", ""),
                    "case_id": case_id,
                    "method": method,
                    "path_str": path_str,
                    "body": body,
                    "auth_headers": auth_header_vals,
                })
    return results


def validate():
    print("=== FR-10 SEMANTIC TRACEABILITY STATIC VALIDATOR ===\n")

    # Gate 1: Raw AI draft immutability
    with open(RAW_AI_PATH, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    if sha == EXPECTED_RAW_AI_SHA256:
        print("[PASS] 1. Raw AI Draft frozen SHA-256 verified immutable.")
    else:
        print(f"[FAIL] 1. Raw AI Draft SHA mismatch: {sha}")

    # Load collection
    with open(COLLECTION_PATH) as f:
        col = json.load(f)

    items = extract_items(col.get("item", []))

    # Build per-case item lists (all items, not just ACTION)
    item_map = {}
    for item in items:
        cid = item["case_id"]
        if cid:
            item_map.setdefault(cid, []).append(item)

    # Verify all 46 formal IDs have at least one item
    expected_ids = set(FROZEN_MAP.keys())
    found_ids = set(item_map.keys())
    missing = expected_ids - found_ids
    extra = found_ids - expected_ids - EXCLUDED_IDS
    if not missing and not extra:
        print(f"[PASS] 2. All 46 formal IDs present (AI-012 excluded).")
    else:
        if missing: print(f"[FAIL] 2. Missing IDs: {missing}")
        if extra:   print(f"[WARN] 2. Extra IDs: {extra}")

    # Per-case semantic checks
    drift_count = 0
    pass_count = 0
    total = 0

    print("\n--- Per-Case Semantic Checks ---")
    for cid in sorted(FROZEN_MAP.keys()):
        rules = FROZEN_MAP[cid]
        entries = item_map.get(cid, [])

        # Find the target action item by keyword
        kw = rules.get("action_keyword", "ACTION")
        target_items = [e for e in entries if kw in e["name"]]
        if not target_items:
            # Fall back to any item with ACTION substring
            target_items = [e for e in entries if "ACTION" in e["name"] or "STEP" in e["name"]]

        if not target_items:
            print(f"  [FAIL] {cid}: No action item found (keyword='{kw}')")
            drift_count += 1
            continue

        item = target_items[0]
        errors = []

        # Method check
        if rules.get("method") and item["method"].upper() != rules["method"].upper():
            errors.append(f"method={item['method']} (expected {rules['method']})")

        # path_must
        if "path_must" in rules:
            if rules["path_must"].lower() not in item["path_str"]:
                errors.append(f"path must contain '{rules['path_must']}' (got '{item['path_str']}')")

        # path_not
        if "path_not" in rules:
            if rules["path_not"].lower() in item["path_str"]:
                errors.append(f"path must NOT contain '{rules['path_not']}' (got '{item['path_str']}')")

        # path contains
        if "path" in rules:
            if rules["path"].lower() not in item["path_str"]:
                errors.append(f"path must contain '{rules['path']}' (got '{item['path_str']}')")

        # Actor check
        if "actor" in rules and not rules.get("no_actor"):
            actor = rules["actor"]
            auth_str = " ".join(item["auth_headers"])
            if actor.lower() not in auth_str.lower() and f"{{{{{actor}}}}}" not in auth_str:
                errors.append(f"actor '{actor}' not in auth headers (got: {auth_str[:80]})")

        # No actor check (must have absent or empty auth)
        if rules.get("no_actor"):
            auth_str = " ".join(item["auth_headers"])
            # Allow for explicit no-auth entries; just note if there IS an auth
            if "Bearer {{" in auth_str and "malformed" not in auth_str.lower() and "invalid" not in auth_str.lower():
                errors.append(f"Expected no/absent auth but found: {auth_str[:80]}")

        # Auth fixed value (e.g. malformed)
        if "auth_fixed_contains" in rules:
            auth_str = " ".join(item["auth_headers"])
            if rules["auth_fixed_contains"].lower() not in auth_str.lower():
                errors.append(f"Expected auth to contain '{rules['auth_fixed_contains']}' (got: {auth_str[:80]})")

        # Body must contain
        if "body_must_contain" in rules:
            bval = rules["body_must_contain"]
            if bval not in item["body"]:
                errors.append(f"body must contain '{bval}' (got '{item['body'][:80]}')")

        # Body exact
        if "body_exact" in rules:
            if item["body"].strip() != rules["body_exact"].strip():
                errors.append(f"body must be '{rules['body_exact']}' (got '{item['body'][:60]}')")

        total += 1
        if errors:
            drift_count += 1
            note_str = f" [{rules.get('note','')}]" if rules.get("note") else ""
            print(f"  [DRIFT] {cid}{note_str}:")
            for e in errors:
                print(f"    -> {e}")
        else:
            pass_count += 1
            if rules.get("note"):
                print(f"  [PASS]  {cid}: OK [{rules['note']}]")

    print(f"\n--- Semantic Traceability Summary ---")
    print(f"  Total:    {total}")
    print(f"  PASS:     {pass_count}")
    print(f"  DRIFT:    {drift_count}")

    if drift_count == 0:
        print(f"\n=== ALL {total} SEMANTIC GATES PASS – 0 DRIFT ===")
    else:
        print(f"\n=== {drift_count} SEMANTIC DRIFT(S) DETECTED ===")
    return drift_count == 0


if __name__ == "__main__":
    ok = validate()
    sys.exit(0 if ok else 1)
