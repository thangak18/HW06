#!/usr/bin/env python3
"""
FR-10 Canonical Map Self-Check Validator
Phase 2D.1D.3 – INT-048
Validates that fr10_canonical_cases.json accurately reflects Level 1-4 provenance.
No network I/O.
"""

import json
import sys
import hashlib

CANONICAL_CASES_PATH = "23127259/testcases/fr10_canonical_cases.json"
RAW_AI_DRAFT_PATH    = "23127259/testcases/FR10_AI_DRAFT.md"
EXPECTED_RAW_AI_SHA  = "303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc"

EXPECTED_IDS = [
    "FR10-AI-001", "FR10-AI-002", "FR10-AI-003", "FR10-AI-004", "FR10-AI-005",
    "FR10-AI-006", "FR10-AI-007", "FR10-AI-008", "FR10-AI-009", "FR10-AI-010",
    "FR10-AI-011", "FR10-AI-013", "FR10-AI-014", "FR10-AI-015", "FR10-AI-016",
    "FR10-AI-017", "FR10-AI-018", "FR10-AI-019", "FR10-AI-020", "FR10-AI-021",
    "FR10-AI-022", "FR10-AI-023", "FR10-AI-024", "FR10-AI-025", "FR10-AI-026",
    "FR10-AI-027", "FR10-AI-028", "FR10-AI-029", "FR10-AI-030", "FR10-AI-031",
    "FR10-AI-032", "FR10-AI-033", "FR10-AI-034", "FR10-AI-035", "FR10-AI-036",
    "FR10-AI-037", "FR10-AI-038", "FR10-AI-039", "FR10-AI-040", "FR10-AI-041",
    "FR10-AI-042",
    "FR10-HUM-001", "FR10-HUM-002", "FR10-HUM-003", "FR10-HUM-004", "FR10-HUM-005"
]


def validate():
    print("=== RUNNING FR-10 CANONICAL MAP SELF-CHECK VALIDATOR ===\n")

    # Gate 1: Verify raw AI draft immutability
    with open(RAW_AI_DRAFT_PATH, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    if sha == EXPECTED_RAW_AI_SHA:
        print("[PASS] 1. Raw AI Draft SHA-256 verified immutable.")
    else:
        print(f"[FAIL] 1. Raw AI Draft SHA mismatch: {sha}")
        return False

    # Load canonical cases JSON
    with open(CANONICAL_CASES_PATH) as f:
        cases = json.load(f)

    # Gate 2: Exactly 46 entries
    if len(cases) == 46:
        print(f"[PASS] 2. Exactly 46 canonical entries loaded.")
    else:
        print(f"[FAIL] 2. Expected 46 entries, got {len(cases)}")
        return False

    # Gate 3: Exact IDs and AI-012 absent
    found_ids = [c["id"] for c in cases]
    if "FR10-AI-012" in found_ids:
        print("[FAIL] 3. FR10-AI-012 must be absent from canonical executable map.")
        return False
    if len(found_ids) != len(set(found_ids)):
        print("[FAIL] 3. Duplicate IDs found in canonical map.")
        return False
    if found_ids == EXPECTED_IDS:
        print("[PASS] 3. Exactly 46 unique canonical IDs match expected sequence (AI-012 excluded).")
    else:
        print(f"[FAIL] 3. ID sequence mismatch.")
        return False

    case_dict = {c["id"]: c for c in cases}
    errors = []

    # Check AI-013..015 mappings
    c13 = case_dict["FR10-AI-013"]
    if c13["initial_state"] != "confirmed" or c13["input"] != {"status": "pending"}:
        errors.append(f"AI-013 must be confirmed->pending, got {c13['initial_state']}->{c13['input']}")

    c14 = case_dict["FR10-AI-014"]
    if c14["initial_state"] != "shipping" or c14["input"] != {"status": "confirmed"}:
        errors.append(f"AI-014 must be shipping->confirmed, got {c14['initial_state']}->{c14['input']}")

    c15 = case_dict["FR10-AI-015"]
    if c15["initial_state"] != "shipping" or c15["input"] != {"status": "pending"}:
        errors.append(f"AI-015 must be shipping->pending, got {c15['initial_state']}->{c15['input']}")

    # Check AI-028 (tampered JWT on admin status)
    c28 = case_dict["FR10-AI-028"]
    if "admin" not in c28["endpoint"].lower() or "tampered" not in c28["auth_condition"].lower():
        errors.append(f"AI-028 must be Tampered JWT on Admin status, got endpoint={c28['endpoint']}, auth={c28['auth_condition']}")

    # Check AI-029 (missing auth on customer cancel)
    c29 = case_dict["FR10-AI-029"]
    if "cancel" not in c29["endpoint"].lower() or "missing" not in c29["auth_condition"].lower():
        errors.append(f"AI-029 must be Missing Auth on Customer cancel, got endpoint={c29['endpoint']}, auth={c29['auth_condition']}")

    # Check AI-030..032 (all role=user on admin status endpoint)
    for cid in ["FR10-AI-030", "FR10-AI-031", "FR10-AI-032"]:
        c = case_dict[cid]
        if "admin" not in c["endpoint"].lower() or "user" not in c["actor"].lower():
            errors.append(f"{cid} must be Normal Customer role=user on Admin status endpoint, got actor={c['actor']}, endpoint={c['endpoint']}")

    # Check AI-033..034 (ownership cancellation)
    for cid in ["FR10-AI-033", "FR10-AI-034"]:
        c = case_dict[cid]
        if "cancel" not in c["endpoint"].lower() or "user b" not in c["actor"].lower():
            errors.append(f"{cid} must be User B on customer cancel route, got actor={c['actor']}, endpoint={c['endpoint']}")

    # Check AI-035..040 inputs
    if case_dict["FR10-AI-035"]["input"] != {"status": "processing"}:
        errors.append("AI-035 input must be {'status': 'processing'}")
    if case_dict["FR10-AI-036"]["input"] != {}:
        errors.append("AI-036 input must be {}")
    if case_dict["FR10-AI-037"]["input"] != {"status": None}:
        errors.append("AI-037 input must be {'status': None}")
    if case_dict["FR10-AI-038"]["input"] != {"status": 123}:
        errors.append("AI-038 input must be {'status': 123}")
    if "999999" not in case_dict["FR10-AI-039"]["endpoint"]:
        errors.append("AI-039 endpoint must contain 999999")
    if "not-an-id" not in case_dict["FR10-AI-040"]["endpoint"]:
        errors.append("AI-040 endpoint must contain not-an-id")

    # Check HUM-001..005
    if len([cid for cid in case_dict if cid.startswith("FR10-HUM-")]) != 5:
        errors.append("Must have exactly 5 FR10-HUM cases")

    if errors:
        print("\n[FAIL] 4. Semantic errors found in canonical map:")
        for e in errors:
            print(f"  -> {e}")
        return False

    print("[PASS] 4. All canonical case definitions verified against Level 1-4 provenance.")
    print("\n=== CANONICAL MAP SELF-CHECK: ALL PASS ===")
    return True


if __name__ == "__main__":
    ok = validate()
    sys.exit(0 if ok else 1)
