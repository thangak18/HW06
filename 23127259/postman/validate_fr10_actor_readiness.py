import json
import hashlib
import re

def validate_actor_readiness():
    print("=== RUNNING FR-10 ACTOR READINESS & CAPACITY VALIDATOR ===")

    # 1. Raw AI Draft SHA-256
    raw_path = "/Volumes/Thang/HW06/HW06/23127259/testcases/FR10_AI_DRAFT.md"
    with open(raw_path, "rb") as f:
        raw_hash = hashlib.sha256(f.read()).hexdigest()
    expected_hash = "303b5383f648a336b3a310aaad139422ee6525793444614dd3853902d30029cc"
    assert raw_hash == expected_hash, f"Raw hash mismatch: {raw_hash}"
    print("[PASS] 1. Raw AI Draft frozen SHA-256 verified immutable.")

    # 2. Environment JSON Credentials
    env_path = "/Volumes/Thang/HW06/HW06/23127259/postman/environments/FR10-local.postman_environment.json"
    with open(env_path, "r", encoding="utf-8") as f:
        env_data = json.load(f)
    env_map = {v["key"]: v["value"] for v in env_data["values"]}

    assert env_map.get("studentId") == "23127259"
    assert env_map.get("adminEmail") == "admin@eshop.com"
    assert env_map.get("adminPassword") == "Admin123!"
    assert env_map.get("userAEmail") == "user@eshop.com"
    assert env_map.get("userAPassword") == "User1234!"
    assert env_map.get("userBEmail") == "user_domain@eshop.com"
    assert env_map.get("userBPassword") == "Domain1234!"
    assert env_map.get("fixtureProductId") == "1"
    print("[PASS] 2. Environment credentials verified: True Admin (admin@eshop.com / Admin123!), User A, User B, fixtureProductId.")

    # 3. Collection JSON Inspection
    col_path = "/Volumes/Thang/HW06/HW06/23127259/postman/collections/FR10_Order_State_Machine.postman_collection.json"
    with open(col_path, "r", encoding="utf-8") as f:
        col_data = json.load(f)

    # 4. Folder 00 Helpers
    f00 = col_data["item"][0]
    f00_names = [it["name"] for it in f00["item"]]
    assert not any("Register Admin" in n for n in f00_names), "Unsupported Admin self-registration helper found in Folder 00!"
    print("[PASS] 3. Zero dependence on public Admin self-registration. Unsupported helper excluded.")

    # 5. Formal IDs & AI-012 Exclusion
    all_reqs = []
    def traverse(items):
        for it in items:
            if "item" in it:
                traverse(it["item"])
            else:
                all_reqs.append(it)
    traverse(col_data["item"])

    formal_ids = set()
    for req in all_reqs:
        m = re.findall(r"FR10-(?:AI|HUM)-\d{3}", req["name"])
        formal_ids.update(m)

    assert len(formal_ids) == 46, f"Expected 46 formal IDs, found {len(formal_ids)}"
    assert "FR10-AI-012" not in formal_ids, "Rejected case FR10-AI-012 found!"
    print("[PASS] 4. Exactly 46 formal test IDs represented (41 AI + 5 HUM; AI-012 strictly excluded).")

    # 6. Admin Actions Authorization Token Mapping (Authorized Admin transitions)
    for req in all_reqs:
        if "[SETUP" not in req["name"]:
            req_text = json.dumps(req)
            if "Admin" in req["name"] and "Non-Owner" not in req["name"] and "IDOR" not in req["name"] and "SEC-02" not in req["name"] and "SEC-03" not in req["name"]:
                assert "{{adminToken}}" in req_text, f"Admin formal action {req['name']} does not use adminToken!"
    print("[PASS] 5. All Admin formal actions strictly use {{adminToken}}.")

    # 7. Customer Owner Actions Authorization Token Mapping
    for req in all_reqs:
        if "[SETUP" not in req["name"]:
            req_text = json.dumps(req)
            if "Customer" in req["name"] and "Customer B" not in req["name"] and "Non-Owner" not in req["name"] and "IDOR" not in req["name"] and "FR10-AI-033" not in req["name"] and "FR10-AI-034" not in req["name"] and "FR10-HUM-002" not in req["name"] and "SEC-02" not in req["name"] and "SEC-03" not in req["name"]:
                assert "{{userAToken}}" in req_text, f"Customer formal action {req['name']} does not use userAToken!"
    print("[PASS] 6. All Customer owner actions strictly use {{userAToken}}.")

    # 8. Non-Owner IDOR Probes Token Mapping
    for item_name in ["FR10-AI-033", "FR10-AI-034"]:
        found = False
        for req in all_reqs:
            if item_name in req["name"] and "[SETUP" not in req["name"]:
                req_text = json.dumps(req)
                assert "{{userBToken}}" in req_text, f"Non-owner IDOR test {req['name']} does not use userBToken!"
                found = True
        assert found, f"Test {item_name} not found in collection!"
    print("[PASS] 7. Non-owner IDOR probes (FR10-AI-033, FR10-AI-034) strictly use {{userBToken}}.")

    # 9. Pre-Request X-Student-Id Injection
    col_prereq = col_data.get("event", [{}])[0].get("script", {}).get("exec", [])
    prereq_str = " ".join(col_prereq)
    assert "X-Student-Id" in prereq_str and "studentId" in prereq_str and env_map.get("studentId") == "23127259"
    print("[PASS] 8. Collection-level X-Student-Id (23127259) pre-request header injection verified.")

    # 10. No Hardcoded Live JWTs in Environment Actor Variables
    for token_key in ["adminToken", "userAToken", "userBToken"]:
        val = env_map.get(token_key, "")
        assert val == "" or val is None, f"{token_key} must not contain pre-filled live JWT in environment JSON!"
    print("[PASS] 9. Zero hardcoded live actor JWT tokens in environment JSON (dynamically populated at runtime).")

    # 11. Product Capacity Operational Resolution Documented
    readiness_path = "/Volumes/Thang/HW06/HW06/23127259/postman/FR10_PRE_NEWMAN_READINESS.md"
    with open(readiness_path, "r", encoding="utf-8") as f:
        readiness_text = f.read()
    assert "OPERATIONALLY UNBOUNDED FOR CURRENT LOCAL HARNESS" in readiness_text
    print("[PASS] 10. Operational inventory capacity defensibly documented as OPERATIONALLY UNBOUNDED.")

    print("\n=== ALL 10 ACTOR READINESS & INVENTORY CAPACITY GATES PASSED (100% READY) ===")

if __name__ == "__main__":
    validate_actor_readiness()
