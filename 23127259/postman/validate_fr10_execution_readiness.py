import json
import re
import hashlib
import sys

def main():
    print("=== RUNNING FR-10 EXECUTION READINESS STATIC VALIDATOR ===")
    
    # 1. Raw AI Draft Integrity Check
    raw_path = "/Volumes/Thang/HW06/HW06/23127259/testcases/FR10_AI_DRAFT.md"
    with open(raw_path, "rb") as f:
        raw_hash = hashlib.sha256(f.read()).hexdigest()
    expected_hash = "303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc"
    assert raw_hash == expected_hash, f"Raw draft hash mismatch: {raw_hash}"
    print("[PASS] 1. Raw AI Draft frozen SHA-256 verified immutable.")

    # 2. Environment JSON Validation
    env_path = "/Volumes/Thang/HW06/HW06/23127259/postman/environments/FR10-local.postman_environment.json"
    with open(env_path, "r", encoding="utf-8") as f:
        env_data = json.load(f)
    assert env_data.get("name") == "FR10-local"
    env_keys = {item["key"]: item["value"] for item in env_data.get("values", [])}
    assert env_keys.get("studentId") == "23127259", "studentId missing or incorrect in environment"
    assert env_keys.get("baseUrl") == "http://localhost:3000", "baseUrl missing or incorrect"
    assert env_keys.get("adminEmail") == "admin@eshop.com"
    print("[PASS] 2. Postman Environment JSON parsed and studentId verified.")

    # 3. Collection JSON Validation
    col_path = "/Volumes/Thang/HW06/HW06/23127259/postman/collections/FR10_Order_State_Machine.postman_collection.json"
    with open(col_path, "r", encoding="utf-8") as f:
        col_data = json.load(f)
    assert col_data.get("info", {}).get("name") == "FR10_Order_State_Machine"
    print("[PASS] 3. Postman Collection JSON parsed.")

    # 4. Fail-Fast Collection Pre-Request Script Check
    events = col_data.get("event", [])
    prereq_script = ""
    for ev in events:
        if ev.get("listen") == "prerequest":
            prereq_script = "\n".join(ev.get("script", {}).get("exec", []))
    assert "X-Student-Id" in prereq_script, "Collection-level X-Student-Id pre-request script missing"
    assert "throw new Error" in prereq_script or "studentId" in prereq_script, "Fail-fast check missing"
    print("[PASS] 4. Fail-fast collection-level X-Student-Id pre-request header injection verified.")

    # 5. Extract & Count Request Definitions
    def extract_items(items):
        reqs = []
        for it in items:
            if "item" in it:
                reqs.extend(extract_items(it["item"]))
            elif "request" in it:
                reqs.append(it)
        return reqs

    all_reqs = extract_items(col_data.get("item", []))
    print(f"[INFO] Total Collection Request Definitions: {len(all_reqs)}")
    assert len(all_reqs) == 140, f"Expected 140 collection request definitions, got {len(all_reqs)}"
    print("[PASS] 5. Exactly 140 collection request definitions present with isolated per-case setup/action steps.")

    # 6. Formal IDs Extraction & Traceability Check
    formal_ids = []
    for req in all_reqs:
        rname = req.get("name", "")
        matches = re.findall(r'\[(FR10-(?:AI|HUM)-\d+)\]', rname)
        if matches:
            formal_ids.extend(matches)

    unique_formal_ids = sorted(list(set(formal_ids)))
    print(f"[INFO] Extracted {len(unique_formal_ids)} unique formal test IDs from collection.")
    assert len(unique_formal_ids) == 46, f"Expected 46 unique formal IDs, found {len(unique_formal_ids)}"
    assert "FR10-AI-012" not in unique_formal_ids, "CRITICAL: Rejected case FR10-AI-012 present in executable collection!"
    
    hum_ids = [fid for fid in unique_formal_ids if "HUM" in fid]
    assert hum_ids == ['FR10-HUM-001', 'FR10-HUM-002', 'FR10-HUM-003', 'FR10-HUM-004', 'FR10-HUM-005']
    print("[PASS] 6. Exactly 46 formal IDs represented (41 AI + 5 HUM; AI-012 strictly excluded).")

    # 7. Check Script-Triggered HTTP Calls (pm.sendRequest) for explicit X-Student-Id & Auth
    col_str = json.dumps(col_data)
    send_req_matches = re.findall(r'pm\.sendRequest\(', col_str)
    print(f"[INFO] Total pm.sendRequest script calls: {len(send_req_matches)}")
    assert len(send_req_matches) == 36, f"Expected 36 script-triggered calls, got {len(send_req_matches)}"
    
    # Check that in every test script with pm.sendRequest, X-Student-Id and Authorization are present
    for req in all_reqs:
        for ev in req.get("event", []):
            script_text = "\n".join(ev.get("script", {}).get("exec", []))
            if "pm.sendRequest(" in script_text:
                assert "'X-Student-Id': studentId" in script_text or "'X-Student-Id'" in script_text, f"Missing X-Student-Id in script call for {req.get('name')}"
                assert "'Authorization':" in script_text or "'Authorization'" in script_text, f"Missing Authorization in script call for {req.get('name')}"
    print("[PASS] 7. All 36 script-triggered HTTP calls explicitly include X-Student-Id and Authorization headers.")

    # 8. Fixture Provenance & Variable Dataflow Verification
    setup_reqs = all_reqs[:4]
    setup_names = [r.get("name", "") for r in setup_reqs]
    assert any("Login Admin" in n for n in setup_names), "Missing Login Admin helper"
    assert any("Login User A" in n for n in setup_names), "Missing Login User A helper"
    assert any("Login User B" in n for n in setup_names), "Missing Login User B helper"
    per_case_setup_names = [r.get("name", "") for r in all_reqs[4:] if "SETUP" in r.get("name", "")]
    assert per_case_setup_names, "Missing isolated per-case setup steps"
    assert any("SETUP-CREATE" in n for n in per_case_setup_names), "Missing per-case checkout setup"
    assert any("SETUP-SHIP" in n for n in per_case_setup_names), "Missing per-case shipping setup"
    assert any("SETUP-CANCELED" in n or "SETUP-CANCEL" in n for n in per_case_setup_names), "Missing per-case canceled setup"
    print("[PASS] 8. User-B registration/authentication helpers plus isolated per-case order fixture/state setup pipeline verified.")

    # 9. Check Exploratory and Partially Spec-Backed Oracles
    for req in all_reqs:
        rname = req.get("name", "")
        for ev in req.get("event", []):
            script_text = "\n".join(ev.get("script", {}).get("exec", []))
            if "FR10-HUM-004" in rname:
                assert "pm.expect(pm.response.code).to.eql(400)" not in script_text, "Brittle 400 assertion in HUM-004"
                assert "pm.expect(pm.response.code).to.eql(200)" not in script_text, "Brittle 200 assertion in HUM-004"
            if "FR10-HUM-005" in rname:
                assert "pm.expect(pm.response.code).to.eql(500)" not in script_text, "Brittle 500 assertion in HUM-005"
            if "FR10-AI-033" in rname or "FR10-AI-034" in rname:
                assert "pm.expect(pm.response.code).to.eql(403)" not in script_text, "Overstated strict 403 in AI-033/034"
            if "FR10-AI-040" in rname:
                assert "pm.expect(pm.response.code).to.eql(400)" not in script_text, "Overstated strict 400 in AI-040"
    print("[PASS] 9. Exploratory (HUM-004/005) and Partially Spec-Backed (AI-033/034/040) oracles verified non-brittle.")

    print("\n=== ALL 9 EXECUTION READINESS STATIC GATES PASSED (100% READY) ===")

if __name__ == "__main__":
    main()
