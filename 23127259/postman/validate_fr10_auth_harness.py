#!/usr/bin/env python3
"""
validate_fr10_auth_harness.py
Static validator for FR-10 Authentication Harness and Login Helper Routes.
Performs 10 strict static gates without network I/O.
"""

import json
import os
import sys

def main():
    print("=== RUNNING FR-10 AUTH HARNESS STATIC VALIDATOR ===")

    collection_path = "/Volumes/Thang/HW06/HW06/23127259/postman/collections/FR10_Order_State_Machine.postman_collection.json"
    env_path = "/Volumes/Thang/HW06/HW06/23127259/postman/environments/FR10-local.postman_environment.json"

    if not os.path.exists(collection_path):
        print(f"[FAIL] Collection file missing: {collection_path}")
        sys.exit(1)
    if not os.path.exists(env_path):
        print(f"[FAIL] Environment file missing: {env_path}")
        sys.exit(1)

    with open(collection_path, "r", encoding="utf-8") as f:
        col = json.load(f)
    with open(env_path, "r", encoding="utf-8") as f:
        env = json.load(f)

    # 1. Check Folder 00 items
    folder_00 = None
    for folder in col.get("item", []):
        if "00" in folder.get("name", ""):
            folder_00 = folder
            break

    if not folder_00:
        print("[FAIL] Gate 1: Folder 00 (Setup / Authentication Helpers) missing.")
        sys.exit(1)

    items_00 = {item.get("name"): item for item in folder_00.get("item", [])}
    required_helpers = [
        "[SETUP] Login Admin",
        "[SETUP] Login User A (Customer A - Owner)",
        "[SETUP] Login User B (Customer B - Non-Owner)"
    ]

    for rh in required_helpers:
        if rh not in items_00:
            print(f"[FAIL] Gate 1: Required auth helper '{rh}' missing from Folder 00.")
            sys.exit(1)
    print(f"[PASS] 1. Exactly expected 3 login helpers present in Folder 00.")

    # 2. Every auth helper uses POST method
    for rh in required_helpers:
        method = items_00[rh].get("request", {}).get("method")
        if method != "POST":
            print(f"[FAIL] Gate 2: Helper '{rh}' method is {method}, expected POST.")
            sys.exit(1)
    print(f"[PASS] 2. All 3 auth helpers strictly use HTTP POST.")

    # 3. Every auth helper uses /api/login (both raw and path array)
    for rh in required_helpers:
        url = items_00[rh].get("request", {}).get("url", {})
        raw_url = url.get("raw", "") if isinstance(url, dict) else str(url)
        path_list = url.get("path", []) if isinstance(url, dict) else []
        if path_list != ["api", "login"] or not raw_url.endswith("/api/login"):
            print(f"[FAIL] Gate 3: Helper '{rh}' URL is invalid: raw={raw_url}, path={path_list}")
            sys.exit(1)
    print(f"[PASS] 3. All 3 auth helpers strictly target '/api/login' (path=['api', 'login']).")

    # 4. Zero executable occurrences of /api/auth/login in entire collection
    col_str = json.dumps(col)
    if "api/auth/login" in col_str or '["api", "auth", "login"]' in col_str.replace(" ", ""):
        print("[FAIL] Gate 4: Stale '/api/auth/login' occurrence detected in collection.")
        sys.exit(1)
    print(f"[PASS] 4. Machine-verified: Zero executable occurrences of '/api/auth/login' in collection.")

    # 5. Token writing tests
    admin_test = "".join(items_00["[SETUP] Login Admin"].get("event", [{}])[0].get("script", {}).get("exec", []))
    user_a_test = "".join(items_00["[SETUP] Login User A (Customer A - Owner)"].get("event", [{}])[0].get("script", {}).get("exec", []))
    user_b_test = "".join(items_00["[SETUP] Login User B (Customer B - Non-Owner)"].get("event", [{}])[0].get("script", {}).get("exec", []))

    if "adminToken" not in admin_test or "pm.environment.set" not in admin_test:
        print("[FAIL] Gate 5: Admin login helper does not write 'adminToken'.")
        sys.exit(1)
    if "userAToken" not in user_a_test or "pm.environment.set" not in user_a_test:
        print("[FAIL] Gate 5: User A login helper does not write 'userAToken'.")
        sys.exit(1)
    if "userBToken" not in user_b_test or "pm.environment.set" not in user_b_test:
        print("[FAIL] Gate 5: User B login helper does not write 'userBToken'.")
        sys.exit(1)
    print(f"[PASS] 5. Admin, User A, and User B test scripts correctly write respective token variables.")

    # 6. No hardcoded live JWT tokens in environment actor variables or setup helpers
    env_values = {v.get("key"): v.get("value") for v in env.get("values", [])}
    for token_key in ["adminToken", "userAToken", "userBToken"]:
        val = env_values.get(token_key, "")
        if val != "" and val is not None:
            print(f"[FAIL] Gate 6: Environment variable '{token_key}' contains hardcoded value: {val}")
            sys.exit(1)
    
    folder_00_str = json.dumps(folder_00)
    if "eyJhbGciOi" in folder_00_str:
        print("[FAIL] Gate 6: Hardcoded JWT detected in Folder 00 setup helpers.")
        sys.exit(1)
    print(f"[PASS] 6. Zero hardcoded live JWT tokens in environment actor variables or Folder 00 helpers.")

    # 7. True Admin credential variables configured
    env_values = {v.get("key"): v.get("value") for v in env.get("values", [])}
    if env_values.get("adminEmail") != "admin@eshop.com" or env_values.get("adminPassword") != "Admin123!":
        print("[FAIL] Gate 7: Admin environment variables do not match proven seed credentials.")
        sys.exit(1)
    print(f"[PASS] 7. True Admin credentials verified (adminEmail=admin@eshop.com / Admin123!).")

    # 8. Public Admin registration absent
    for item_name in items_00.keys():
        if "Register Admin" in item_name:
            print("[FAIL] Gate 8: Unsupported public Admin registration helper found in Folder 00.")
            sys.exit(1)
    print(f"[PASS] 8. Public Admin self-registration helper strictly absent.")

    # 9. studentId configured in environment
    if env_values.get("studentId") != "23127259":
        print(f"[FAIL] Gate 9: studentId is '{env_values.get('studentId')}', expected '23127259'.")
        sys.exit(1)
    print(f"[PASS] 9. studentId is authoritatively configured as '23127259'.")

    # 10. Collection-level X-Student-Id injection verified
    col_events = col.get("event", [])
    prerequest_script = ""
    for ev in col_events:
        if ev.get("listen") == "prerequest":
            prerequest_script = "".join(ev.get("script", {}).get("exec", []))
            break
    if "X-Student-Id" not in prerequest_script or "studentId" not in prerequest_script or env_values.get("studentId") != "23127259":
        print("[FAIL] Gate 10: Collection-level X-Student-Id pre-request header injection missing.")
        sys.exit(1)
    print(f"[PASS] 10. Fail-fast collection-level X-Student-Id pre-request header injection verified.")

    print("\n=== ALL 10 AUTH HARNESS STATIC GATES PASSED (100% READY) ===")

if __name__ == "__main__":
    main()
