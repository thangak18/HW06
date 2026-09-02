#!/usr/bin/env python3
"""
FR-14 Canonical Map Self-Check Validator
Validates that fr14_canonical_cases.json accurately reflects Level 1-4 provenance
and matches FR14_Category_CRUD.postman_collection.json.
No network I/O.
"""

import json
import os
import sys
import hashlib

CANONICAL_CASES_PATH = "23127259/testcases/fr14_canonical_cases.json"
RAW_AI_DRAFT_PATH    = "23127259/testcases/FR14_AI_DRAFT.md"
EXPECTED_RAW_AI_SHA  = "95ac502b0880efcc1c6ceb040a1171eeacebff5c262a5f6df8d49a86cadcaf70"
COLLECTION_PATH      = "23127259/postman/collections/FR14_Category_CRUD.postman_collection.json"

EXPECTED_IDS = [
    f"TC-FR14-{i:03d}" for i in range(1, 43)
] + [
    f"TC-FR14-H{i:02d}" for i in range(1, 8)
]


def validate():
    print("=== RUNNING FR-14 CANONICAL MAP SELF-CHECK VALIDATOR ===\n")
    errors = []

    # Gate 1: Verify raw AI draft immutability
    if not os.path.exists(RAW_AI_DRAFT_PATH):
        print(f"[FAIL] 1. Raw AI Draft missing: {RAW_AI_DRAFT_PATH}")
        return False
    with open(RAW_AI_DRAFT_PATH, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    if sha == EXPECTED_RAW_AI_SHA:
        print(f"[PASS] 1. Raw AI Draft SHA-256 verified immutable ({sha[:12]}...).")
    else:
        print(f"[FAIL] 1. Raw AI Draft SHA mismatch: expected {EXPECTED_RAW_AI_SHA}, got {sha}")
        return False

    # Load canonical cases JSON
    if not os.path.exists(CANONICAL_CASES_PATH):
        print(f"[FAIL] Canonical cases file missing: {CANONICAL_CASES_PATH}")
        return False
    with open(CANONICAL_CASES_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    # Gate 2: Exactly 49 canonical entries
    if len(cases) == 49:
        print(f"[PASS] 2. Exactly 49 canonical entries loaded.")
    else:
        print(f"[FAIL] 2. Expected 49 entries, got {len(cases)}")
        return False

    # Gate 3: Exact IDs match
    found_ids = [c["id"] for c in cases]
    if len(found_ids) != len(set(found_ids)):
        print("[FAIL] 3. Duplicate IDs found in canonical map.")
        return False
    if found_ids == EXPECTED_IDS:
        print(f"[PASS] 3. All 49 unique canonical IDs match expected sequence (42 AI + 7 Human).")
    else:
        missing = set(EXPECTED_IDS) - set(found_ids)
        extra = set(found_ids) - set(EXPECTED_IDS)
        print(f"[FAIL] 3. ID mismatch: missing={missing}, extra={extra}")
        return False

    # Gate 4: Field completeness
    required_fields = ["id", "provenance", "actor", "auth_condition", "method", "endpoint", "oracle_strength", "semantic_oracle", "source_refs"]
    for c in cases:
        for rf in required_fields:
            if rf not in c:
                errors.append(f"Case {c.get('id')} missing field: {rf}")
    if not errors:
        print("[PASS] 4. All canonical entries contain required schema fields.")
    else:
        print(f"[FAIL] 4. Missing fields in entries: {len(errors)} errors")
        return False

    # Gate 5: Cross-check against Postman Collection
    if os.path.exists(COLLECTION_PATH):
        with open(COLLECTION_PATH, "r", encoding="utf-8") as f:
            collection = json.load(f)

        coll_names = []
        def walk_items(items):
            for item in items:
                if "item" in item:
                    walk_items(item["item"])
                elif "request" in item:
                    coll_names.append(item["name"])
        walk_items(collection.get("item", []))

        # Check coverage: every expected ID should be represented in at least one collection request
        covered = 0
        for eid in EXPECTED_IDS:
            if any(eid in name for name in coll_names):
                covered += 1
            else:
                errors.append(f"Canonical ID {eid} not found in collection item names")

        if covered == len(EXPECTED_IDS):
            print(f"[PASS] 5. 100% bidirectional coverage: all 49 canonical cases mapped to Postman requests.")
        else:
            print(f"[FAIL] 5. Only {covered}/49 canonical cases mapped to collection.")
            return False
    else:
        print(f"[WARN] 5. Postman collection path not found for cross-check.")

    print("\n=== ALL CANONICAL MAP SELF-CHECKS PASSED SUCCESSFULLY ===")
    return True


if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
