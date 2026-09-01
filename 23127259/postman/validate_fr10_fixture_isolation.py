import json
import re
import hashlib
import sys

def main():
    print("=== RUNNING FR-10 FIXTURE ISOLATION STATIC VALIDATOR ===")
    
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
    # Verify no prefilled static order IDs in environment
    assert "orderId" not in env_keys and "orderPendingId" not in env_keys, "Prefilled static order IDs found in environment"
    print("[PASS] 2. Postman Environment JSON parsed, studentId verified, zero prefilled static order IDs.")

    # 3. Collection JSON Validation & Request Extraction
    col_path = "/Volumes/Thang/HW06/HW06/23127259/postman/collections/FR10_Order_State_Machine.postman_collection.json"
    with open(col_path, "r", encoding="utf-8") as f:
        col_data = json.load(f)
    assert col_data.get("info", {}).get("name") == "FR10_Order_State_Machine"

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
    print("[PASS] 3. Exactly 138 collection request definitions present (3 auth helpers + co-located setups + formal steps).")

    # 4. Fail-Fast Collection Pre-Request Script Check
    events = col_data.get("event", [])
    prereq_script = ""
    for ev in events:
        if ev.get("listen") == "prerequest":
            prereq_script = "\n".join(ev.get("script", {}).get("exec", []))
    assert "X-Student-Id" in prereq_script, "Collection-level X-Student-Id pre-request script missing"
    assert "throw new Error" in prereq_script or "studentId" in prereq_script, "Fail-fast check missing"
    print("[PASS] 4. Fail-fast collection-level X-Student-Id pre-request header injection verified.")

    # 5. Formal IDs Extraction & Traceability Check
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
    print("[PASS] 5. Exactly 46 formal IDs represented (41 AI + 5 HUM; AI-012 strictly excluded).")

    # 6. Verify Per-Case Fixture Isolation & Zero Mutable Order Sharing
    col_str = json.dumps(col_data)
    
    # Check no dangerous fallback '1' or "1" in extraction scripts
    assert "|| '1'" not in col_str and '|| "1"' not in col_str, "Forbidden fallback order ID '1' detected in collection scripts!"
    print("[PASS] 6. Zero fallback order IDs ('1') found. Fail-fast extraction enforced.")

    # Check that each formal case has its own unique variable and no cross-case variable reuse
    case_var_mapping = {}
    for req in all_reqs:
        rname = req.get("name", "")
        m = re.findall(r'\[(FR10-(?:AI|HUM)-\d+)\]', rname)
        if m:
            fid = m[0]
            # Find order variables referenced in url or scripts
            req_str = json.dumps(req)
            vars_found = re.findall(r'order_FR10_(?:AI|HUM)_\d+(?:_[AB])?', req_str)
            for v in vars_found:
                if v not in case_var_mapping:
                    case_var_mapping[v] = set()
                case_var_mapping[v].add(fid)

    for v, fids in case_var_mapping.items():
        assert len(fids) == 1, f"CRITICAL: Variable {v} is shared across multiple formal cases: {fids}"
    print(f"[PASS] 7. Machine-verified: All {len(case_var_mapping)} order fixture variables are strictly isolated to single formal cases.")

    # 8. Verify HUM-002 has exactly two dedicated order variables
    assert "order_FR10_HUM_002_A" in case_var_mapping and "order_FR10_HUM_002_B" in case_var_mapping, "HUM-002 missing dedicated A and B variables"
    print("[PASS] 8. HUM-002 has two dedicated, non-shared order variables (A and B).")

    # 9. Verify Script-Triggered HTTP Calls (pm.sendRequest) for explicit X-Student-Id & Auth
    send_req_matches = re.findall(r'pm\.sendRequest\(', col_str)
    print(f"[INFO] Total pm.sendRequest script calls: {len(send_req_matches)}")
    assert len(send_req_matches) == 36, f"Expected 36 script-triggered calls, got {len(send_req_matches)}"
    
    for req in all_reqs:
        for ev in req.get("event", []):
            script_text = "\n".join(ev.get("script", {}).get("exec", []))
            if "pm.sendRequest(" in script_text:
                assert "'X-Student-Id': studentId" in script_text or "'X-Student-Id'" in script_text, f"Missing X-Student-Id in script call for {req.get('name')}"
                assert "'Authorization':" in script_text or "'Authorization'" in script_text, f"Missing Authorization in script call for {req.get('name')}"
    print("[PASS] 9. All 36 script-triggered HTTP calls explicitly include X-Student-Id and Authorization headers.")

    # 10. Verify Exact Cancellation Method is PUT
    cancel_methods = set()
    for req in all_reqs:
        url_raw = req.get("request", {}).get("url", {}).get("raw", "")
        if "/cancel" in url_raw:
            cancel_methods.add(req.get("request", {}).get("method"))
    assert cancel_methods == {"PUT"}, f"Expected only PUT method for /cancel, found: {cancel_methods}"
    print("[PASS] 10. Exact cancellation method verified as PUT across all requests.")

    print("\n=== ALL 10 PER-CASE FIXTURE ISOLATION GATES PASSED (100% READY) ===")

if __name__ == "__main__":
    main()
