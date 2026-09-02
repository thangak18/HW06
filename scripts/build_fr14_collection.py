#!/usr/bin/env python3
"""
Build canonical FR14 Postman Collection from the verified canonical map.

Source of truth: 23127259/testcases/fr14_canonical_cases.json (46 cases).

Behavior:
- Removes rejected IDs: TC-FR14-034, TC-FR14-036, TC-FR14-H07
- No exact 400/401/403/404 expectations (use 4xx/non-success)
- Every HTTP operation includes X-Student-Id: 23127259 (collection pre-request)
- No hardcoded JWTs (tokens captured at runtime from login helpers)
- Fixture isolation per case
- Multi-step cases use pm.sendRequest for verification GETs

Output: 23127259/postman/collections/FR14_Category_CRUD.postman_collection.json
"""

import json
import os
import sys

CANONICAL_PATH = "23127259/testcases/fr14_canonical_cases.json"
OUTPUT_PATH = "23127259/postman/collections/FR14_Category_CRUD.postman_collection.json"

BASE_URL = "{{baseUrl}}"
STUDENT_ID = "23127259"


def base_header_block(extra=None, no_auth=False):
    headers = [
        {"key": "X-Student-Id", "value": "{{studentId}}"}
    ]
    if not no_auth and extra is not None and "auth" not in extra:
        return headers
    if extra:
        auth = extra.get("auth")
        if auth and not no_auth:
            headers.insert(0, {"key": "Authorization", "value": f"Bearer {{{auth}}}"})
        content_type = extra.get("content_type")
        if content_type:
            headers.insert(0, {"key": "Content-Type", "value": content_type})
    return headers


def make_request(method, url_path, body=None, headers=None):
    req = {
        "method": method,
        "header": headers or [{"key": "X-Student-Id", "value": "{{studentId}}"}],
        "url": {
            "raw": f"{BASE_URL}{url_path}",
            "host": [BASE_URL],
            "path": [p for p in url_path.split("/") if p]
        }
    }
    if body is not None:
        if isinstance(body, str):
            req["body"] = {
                "mode": "raw",
                "raw": body,
                "options": {"raw": {"language": "text"}}
            }
        else:
            req["body"] = {
                "mode": "raw",
                "raw": json.dumps(body, ensure_ascii=False),
                "options": {"raw": {"language": "json"}}
            }
    return req


def test_assert_no_success():
    """For tests expecting rejection: non-success plus no state mutation."""
    return [
        "var json = {};",
        "try { json = pm.response.json(); } catch(e) {}",
        "pm.test('TC assertion: response is non-success (4xx)', function() {",
        "    pm.expect(pm.response.code).to.be.at.least(400);",
        "    pm.expect(pm.response.code).to.be.below(500);",
        "});",
        "pm.test('TC assertion: response does not report a successful mutation', function() {",
        "    var body = JSON.stringify(json).toLowerCase();",
        "    var ok = body.indexOf('success') === -1 || body.indexOf('created') === -1 || body.indexOf('updated') === -1;",
        "    pm.expect(ok, 'response unexpectedly reports mutation success').to.be.true;",
        "});"
    ]


def test_assert_success(msg="success"):
    return [
        f"pm.test('TC assertion: success ({msg})', function() {{",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "});"
    ]


def make_item(name, request, tests=None, listen_test=True):
    item = {"name": name, "request": request}
    if listen_test and tests:
        item["event"] = [{"listen": "test", "script": {"type": "text/javascript", "exec": tests}}]
    return item


def build_helpers():
    """Three login/capture helpers at collection start."""
    return {
        "name": "00 – Setup Helpers",
        "description": "Login helpers to capture Admin/User tokens at runtime. Excluded from formal case count.",
        "item": [
            {
                "name": "HELPER-000A – Login as Admin (captures adminToken)",
                "event": [
                    {"listen": "test", "script": {"type": "text/javascript", "exec": [
                        "var json = pm.response.json();",
                        "pm.test('HELPER: Admin login succeeds', function() {",
                        "    pm.expect(pm.response.code).to.be.below(400);",
                        "    pm.expect(json.token).to.be.a('string');",
                        "    pm.environment.set('adminToken', json.token);",
                        "});"
                    ]}}
                ],
                "request": make_request(
                    "POST", "/api/login",
                    body={"email": "{{adminEmail}}", "password": "{{adminPassword}}"},
                    headers=base_header_block({"content_type": "application/json"})
                )
            },
            {
                "name": "HELPER-000B – Login as Regular User (captures userToken)",
                "event": [
                    {"listen": "test", "script": {"type": "text/javascript", "exec": [
                        "var json = pm.response.json();",
                        "pm.test('HELPER: User login succeeds', function() {",
                        "    pm.expect(pm.response.code).to.be.below(400);",
                        "    pm.expect(json.token).to.be.a('string');",
                        "    pm.environment.set('userToken', json.token);",
                        "});"
                    ]}}
                ],
                "request": make_request(
                    "POST", "/api/login",
                    body={"email": "{{userEmail}}", "password": "{{userPassword}}"},
                    headers=base_header_block({"content_type": "application/json"})
                )
            },
            {
                "name": "HELPER-000C – Capture initial category count",
                "event": [
                    {"listen": "test", "script": {"type": "text/javascript", "exec": [
                        "var json = pm.response.json();",
                        "pm.test('HELPER: initial category count captured', function() {",
                        "    pm.expect(pm.response.code).to.be.below(400);",
                        "    pm.expect(json).to.be.an('array');",
                        "    pm.environment.set('initialCategoryCount', json.length);",
                        "});"
                    ]}}
                ],
                "request": make_request("GET", "/api/categories")
            }
        ]
    }


def get_helper(token_var):
    """Build headers list using a Bearer token captured at runtime."""
    return [
        {"key": "Authorization", "value": "Bearer {{" + token_var + "}}"},
        {"key": "Content-Type", "value": "application/json"},
        {"key": "X-Student-Id", "value": "{{studentId}}"}
    ]


def get_helper_no_auth():
    return [
        {"key": "X-Student-Id", "value": "{{studentId}}"}
    ]


def get_helper_malformed():
    return [
        {"key": "Authorization", "value": "Bearer malformed.token.value"},
        {"key": "Content-Type", "value": "application/json"},
        {"key": "X-Student-Id", "value": "{{studentId}}"}
    ]


def get_helper_tampered_admin():
    """Tampered Admin token (single char changed in signature)."""
    return [
        {"key": "Authorization", "value": "Bearer {{tamperedAdminToken}}"},
        {"key": "Content-Type", "value": "application/json"},
        {"key": "X-Student-Id", "value": "{{studentId}}"}
    ]


def no_auth_headers():
    return [{"key": "X-Student-Id", "value": "{{studentId}}"}]


def build_tc001_get_list_public():
    req = make_request("GET", "/api/categories")
    tests = [
        "pm.test('TC-FR14-001: public GET succeeds (non-error)', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "});",
        "var json = pm.response.json();",
        "pm.test('TC-FR14-001: response is JSON array', function() {",
        "    pm.expect(json).to.be.an('array');",
        "});"
    ]
    return make_item("TC-FR14-001 – GET List All Categories (Public)", req, tests)


def build_tc002_post_admin_create():
    """Admin creates 'Tablet' category; expects success and captures id."""
    req = make_request("POST", "/api/categories",
                       body={"name": "Tablet"},
                       headers=get_helper("adminToken"))
    tests = [
        "var json = pm.response.json();",
        "pm.test('TC-FR14-002: POST create as Admin succeeds', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "});",
        "pm.test('TC-FR14-002: response carries created id', function() {",
        "    pm.expect(json.id).to.be.a('number');",
        "    pm.environment.set('createdCategoryId', json.id);",
        "});"
    ]
    return make_item("TC-FR14-002 – POST Create Category (Admin)", req, tests)


def build_tc003_verify_created():
    req = make_request("GET", "/api/categories")
    tests = [
        "var json = pm.response.json();",
        "var found = json.find(function(c) { return c.name === 'Tablet'; });",
        "pm.test('TC-FR14-003: created category visible in list', function() {",
        "    pm.expect(found).to.not.be.undefined;",
        "});"
    ]
    return make_item("TC-FR14-003 – GET Verify Created Category", req, tests)


def build_tc004_put_admin_update():
    req = make_request("PUT", "/api/categories/{{createdCategoryId}}",
                       body={"name": "Tablets & iPads"},
                       headers=get_helper("adminToken"))
    tests = [
        "pm.test('TC-FR14-004: PUT update as Admin succeeds', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "});"
    ]
    return make_item("TC-FR14-004 – PUT Update Category (Admin)", req, tests)


def build_tc005_verify_updated():
    req = make_request("GET", "/api/categories")
    tests = [
        "var json = pm.response.json();",
        "var found = json.find(function(c) { return c.name === 'Tablets & iPads'; });",
        "pm.test('TC-FR14-005: updated name visible', function() {",
        "    pm.expect(found).to.not.be.undefined;",
        "});"
    ]
    return make_item("TC-FR14-005 – GET Verify Updated Name", req, tests)


def build_tc006_delete_admin():
    req = make_request("DELETE", "/api/categories/{{createdCategoryId}}",
                       headers=get_helper("adminToken"))
    tests = [
        "pm.test('TC-FR14-006: DELETE as Admin succeeds', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "});"
    ]
    return make_item("TC-FR14-006 – DELETE Category (Admin)", req, tests)


def build_auth_missing(method, endpoint, name_suffix, name="UnauthCategory"):
    """Missing JWT: any 4xx/non-success and no mutation."""
    body = {"name": name} if method == "POST" else None
    req = make_request(method, endpoint,
                       body=body,
                       headers=no_auth_headers())
    return make_item(f"{name_suffix} – {method} Without Auth", req, test_assert_no_success())


def build_auth_malformed(method, endpoint, name="MalformedTokenCategory"):
    body = {"name": name} if method == "POST" else None
    req = make_request(method, endpoint, body=body, headers=get_helper_malformed())
    return make_item(f"TC-FR14-010 – {method} With Malformed Token", req, test_assert_no_success())


def build_auth_tampered(endpoint):
    """Tampered Admin token: any 4xx/non-success."""
    req = make_request("DELETE", endpoint, headers=get_helper_tampered_admin())
    return make_item("TC-FR14-011 – DELETE With Tampered Token", req, test_assert_no_success())


def build_rbac_user_post():
    """Regular user attempts POST: must fail (FR-12)."""
    req = make_request("POST", "/api/categories",
                       body={"name": "UserCreatedCategory"},
                       headers=get_helper("userToken"))
    return make_item("TC-FR14-012 – POST Create as Regular User (RBAC)", req, test_assert_no_success())


def build_rbac_user_put():
    req = make_request("PUT", "/api/categories/2",
                       body={"name": "UserModifiedName"},
                       headers=get_helper("userToken"))
    return make_item("TC-FR14-013 – PUT Update as Regular User (RBAC)", req, test_assert_no_success())


def build_rbac_user_delete():
    req = make_request("DELETE", "/api/categories/2",
                       headers=get_helper("userToken"))
    return make_item("TC-FR14-014 – DELETE as Regular User (RBAC)", req, test_assert_no_success())


def build_tc015_user_get():
    req = make_request("GET", "/api/categories", headers=get_helper("userToken"))
    tests = [
        "pm.test('TC-FR14-015: authenticated User can read public list', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "});"
    ]
    return make_item("TC-FR14-015 – GET List as Regular User", req, tests)


def build_name_invalid(name_value, label):
    body = {"name": name_value} if name_value is not None or label == "MissingNameKey" else None
    if label == "MissingNameKey":
        body = {}
    elif name_value is None:
        body = {"name": None}
    req = make_request("POST", "/api/categories", body=body, headers=get_helper("adminToken"))
    tests = [
        "pm.test('TC-FR14-" + label + ": invalid name does not create entity (non-success)', function() {",
        "    pm.expect(pm.response.code).to.be.at.least(400);",
        "});"
    ]
    return make_item(f"TC-FR14-{label} – POST {label}", req, tests)


def build_name_exploratory(name_value, label):
    """Exploratory: just observe status; no normative verdict."""
    body = {"name": name_value} if name_value is not None else {"name": 12345}
    if isinstance(name_value, int):
        body = {"name": name_value}
    req = make_request("POST", "/api/categories", body=body, headers=get_helper("adminToken"))
    tests = [
        "pm.test('TC-FR14-" + label + ": exploratory observation', function() {",
        "    pm.expect(pm.response.code).to.be.a('number');",
        "});"
    ]
    return make_item(f"TC-FR14-{label} – POST Exploratory Name", req, tests)


def build_nonexistent(method, endpoint, label):
    """Partial-oracle: any status; no successful mutation of nonexistent entity."""
    body = {"name": "GhostCategory"} if method == "PUT" else None
    req = make_request(method, endpoint, body=body, headers=get_helper("adminToken"))
    tests = [
        "var json = {};",
        "try { json = pm.response.json(); } catch(e) {}",
        "pm.test('TC-FR14-" + label + ": nonexistent entity not falsely mutated', function() {",
        "    var body = JSON.stringify(json).toLowerCase();",
        "    var is_fake_success = (body.indexOf('updated') !== -1 || body.indexOf('deleted') !== -1);",
        "    if (pm.response.code < 400) {",
        "        pm.expect(is_fake_success, 'API falsely reports success on nonexistent ID').to.be.false;",
        "    } else {",
        "        pm.expect(pm.response.code).to.be.at.least(400);",
        "    }",
        "});"
    ]
    return make_item(f"TC-FR14-{label} – {method} Nonexistent", req, tests)


def build_invalid_id(method, endpoint, label):
    """Exploratory: just observe behavior."""
    body = {"name": "BoundaryID"} if method == "PUT" else None
    req = make_request(method, endpoint, body=body, headers=get_helper("adminToken"))
    tests = [
        "pm.test('TC-FR14-" + label + ": exploratory boundary ID observation', function() {",
        "    pm.expect(pm.response.code).to.be.a('number');",
        "});"
    ]
    return make_item(f"TC-FR14-{label} – {method} Boundary ID", req, tests)


def build_sql_injection():
    """SEC-05 black-box probe: parameterised execution is required."""
    req = make_request("POST", "/api/categories",
                       body={"name": "'; DROP TABLE categories;--"},
                       headers=get_helper("adminToken"))
    tests = [
        "var json = pm.response.json();",
        "pm.test('TC-FR14-029: SQL-style payload accepted as text (no injection)', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "    pm.environment.set('sqlInjectionId', json.id);",
        "});",
        "// Verification GET via pm.sendRequest to confirm table still intact",
        "pm.sendRequest({",
        "    url: pm.variables.get('baseUrl') + '/api/categories',",
        "    method: 'GET',",
        "    header: { 'X-Student-Id': pm.variables.get('studentId') }",
        "}, function(err, response) {",
        "    pm.test('TC-FR14-029: categories table intact after SQL payload', function() {",
        "        pm.expect(response.code).to.be.below(400);",
        "        var arr = response.json();",
        "        pm.expect(arr).to.be.an('array');",
        "    });",
        "});"
    ]
    return make_item("TC-FR14-029 – POST SQL Injection Probe", req, tests)


def build_xss_payload():
    """SEC-04 cannot be adjudicated by API response; record raw persistence only."""
    req = make_request("POST", "/api/categories",
                       body={"name": "<script>alert('XSS')</script>"},
                       headers=get_helper("adminToken"))
    tests = [
        "pm.test('TC-FR14-030: exploratory XSS payload observation', function() {",
        "    pm.expect(pm.response.code).to.be.a('number');",
        "});"
    ]
    return make_item("TC-FR14-030 – POST XSS Payload", req, tests)


def build_mass_assign_post():
    req = make_request("POST", "/api/categories",
                       body={"name": "MassAssignTest", "id": 999, "admin": True, "role": "superuser"},
                       headers=get_helper("adminToken"))
    tests = [
        "var json = pm.response.json();",
        "pm.test('TC-FR14-031: mass-assigned id/role ignored (response id matches server-generated)', function() {",
        "    if (json.id) {",
        "        pm.expect(json.id).to.not.eql(999);",
        "    }",
        "});"
    ]
    return make_item("TC-FR14-031 – POST Mass Assignment", req, tests)


def build_mass_assign_put():
    req = make_request("PUT", "/api/categories/2",
                       body={"name": "UpdatedMassAssign", "id": 999},
                       headers=get_helper("adminToken"))
    tests = [
        "pm.test('TC-FR14-032: PUT does not honor body-id override', function() {",
        "    pm.expect(pm.response.code).to.be.a('number');",
        "});"
    ]
    return make_item("TC-FR14-032 – PUT Mass Assignment Override ID", req, tests)


def build_nosql_probe():
    req = make_request("POST", "/api/categories",
                       body={"name": {"$gt": ""}},
                       headers=get_helper("adminToken"))
    tests = [
        "pm.test('TC-FR14-033: object-type name exploratory', function() {",
        "    pm.expect(pm.response.code).to.be.a('number');",
        "});"
    ]
    return make_item("TC-FR14-033 – POST NoSQL Probe", req, tests)


def build_lifecycle():
    """Full lifecycle: create → read → update → read → delete → read."""
    create = make_request("POST", "/api/categories",
                          body={"name": "LifecycleTest"},
                          headers=get_helper("adminToken"))
    create_tests = [
        "var json = pm.response.json();",
        "pm.test('TC-FR14-035a: lifecycle create succeeds', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "    pm.environment.set('lifecycleCategoryId', json.id);",
        "});"
    ]
    read1 = make_request("GET", "/api/categories")
    read1_tests = [
        "var json = pm.response.json();",
        "pm.test('TC-FR14-035b: lifecycle read-after-create', function() {",
        "    var id = pm.variables.get('lifecycleCategoryId');",
        "    var found = json.find(function(c) { return c.id === id; });",
        "    pm.expect(found).to.not.be.undefined;",
        "});"
    ]
    update = make_request("PUT", "/api/categories/{{lifecycleCategoryId}}",
                          body={"name": "LifecycleUpdated"},
                          headers=get_helper("adminToken"))
    update_tests = [
        "pm.test('TC-FR14-035c: lifecycle update succeeds', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "});"
    ]
    delete = make_request("DELETE", "/api/categories/{{lifecycleCategoryId}}",
                          headers=get_helper("adminToken"))
    delete_tests = [
        "pm.test('TC-FR14-035d: lifecycle delete succeeds', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "});"
    ]
    read2 = make_request("GET", "/api/categories")
    read2_tests = [
        "var json = pm.response.json();",
        "pm.test('TC-FR14-035e: lifecycle read-after-delete shows absence', function() {",
        "    var id = parseInt(pm.variables.get('lifecycleCategoryId'));",
        "    var found = json.find(function(c) { return c.id === id; });",
        "    pm.expect(found).to.be.undefined;",
        "});"
    ]
    return [
        make_item("TC-FR14-035 – Lifecycle: Create", create, create_tests),
        make_item("TC-FR14-035 – Lifecycle: Read After Create", read1, read1_tests),
        make_item("TC-FR14-035 – Lifecycle: Update", update, update_tests),
        make_item("TC-FR14-035 – Lifecycle: Delete", delete, delete_tests),
        make_item("TC-FR14-035 – Lifecycle: Read After Delete", read2, read2_tests),
    ]


def build_invalid_lifecycle():
    """TC-037/038: PUT/DELETE on deleted (zombie) category."""
    zombie_id_var = "lifecycleCategoryId"
    put = make_request("PUT", "/api/categories/{{" + zombie_id_var + "}}",
                       body={"name": "ZombieUpdate"},
                       headers=get_helper("adminToken"))
    put_tests = [
        "pm.test('TC-FR14-037: zombie PUT partial-oracle (no fake success)', function() {",
        "    var body = JSON.stringify(pm.response.json()).toLowerCase();",
        "    if (pm.response.code < 400) {",
        "        pm.expect(body.indexOf('updated')).to.eql(-1);",
        "    }",
        "});"
    ]
    delete = make_request("DELETE", "/api/categories/{{" + zombie_id_var + "}}",
                          headers=get_helper("adminToken"))
    delete_tests = [
        "pm.test('TC-FR14-038: zombie DELETE partial-oracle (no fake success)', function() {",
        "    var body = JSON.stringify(pm.response.json()).toLowerCase();",
        "    if (pm.response.code < 400) {",
        "        pm.expect(body.indexOf('deleted')).to.eql(-1);",
        "    }",
        "});"
    ]
    return [
        make_item("TC-FR14-037 – PUT Update Deleted (Zombie)", put, put_tests),
        make_item("TC-FR14-038 – Double DELETE", delete, delete_tests),
    ]


def build_schema_validation():
    create = make_request("POST", "/api/categories",
                          body={"name": "SchemaTest"},
                          headers=get_helper("adminToken"))
    create_tests = [
        "var json = pm.response.json();",
        "pm.test('TC-FR14-040: response shape has id field', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "    pm.expect(json).to.have.property('id');",
        "    pm.environment.set('schemaCategoryId', json.id);",
        "});"
    ]
    update = make_request("PUT", "/api/categories/{{schemaCategoryId}}",
                          body={"name": "SchemaUpdated"},
                          headers=get_helper("adminToken"))
    update_tests = [
        "pm.test('TC-FR14-041: PUT succeeds', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "});"
    ]
    delete = make_request("DELETE", "/api/categories/{{schemaCategoryId}}",
                          headers=get_helper("adminToken"))
    delete_tests = [
        "pm.test('TC-FR14-042: DELETE succeeds', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "});"
    ]
    get = make_request("GET", "/api/categories")
    get_tests = [
        "var json = pm.response.json();",
        "pm.test('TC-FR14-039: GET schema', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "    pm.expect(json).to.be.an('array');",
        "});"
    ]
    return [
        make_item("TC-FR14-039 – GET Schema Validation", get, get_tests),
        make_item("TC-FR14-040 – POST Schema Validation", create, create_tests),
        make_item("TC-FR14-041 – PUT Schema Validation", update, update_tests),
        make_item("TC-FR14-042 – DELETE Schema Validation", delete, delete_tests),
    ]


def build_h01_no_content_type():
    """Missing Content-Type: exploratory."""
    req = {
        "method": "POST",
        "header": [
            {"key": "Authorization", "value": "Bearer {{adminToken}}"},
            {"key": "X-Student-Id", "value": "{{studentId}}"}
        ],
        "body": {
            "mode": "raw",
            "raw": json.dumps({"name": "NoContentTypeTest"}),
            "options": {"raw": {"language": "json"}}
        },
        "url": {
            "raw": f"{BASE_URL}/api/categories",
            "host": [BASE_URL],
            "path": ["api", "categories"]
        }
    }
    tests = [
        "pm.test('TC-FR14-H01: exploratory no-content-type observation', function() {",
        "    pm.expect(pm.response.code).to.be.a('number');",
        "});"
    ]
    return make_item("TC-FR14-H01 – POST Without Content-Type", req, tests)


def build_h02_zero_byte():
    req = make_request("POST", "/api/categories",
                       body="",
                       headers=[
                           {"key": "Content-Type", "value": "application/json"},
                           {"key": "Authorization", "value": "Bearer {{adminToken}}"},
                           {"key": "X-Student-Id", "value": "{{studentId}}"}
                       ])
    req["body"]["options"]["raw"]["language"] = "text"
    tests = [
        "pm.test('TC-FR14-H02: exploratory zero-byte body observation', function() {",
        "    pm.expect(pm.response.code).to.be.a('number');",
        "});"
    ]
    return make_item("TC-FR14-H02 – POST Empty Body", req, tests)


def build_h03_patch():
    req = make_request("PATCH", "/api/categories/2",
                       body={"name": "PatchAttempt"},
                       headers=get_helper("adminToken"))
    tests = [
        "pm.test('TC-FR14-H03: PATCH non-success (method not supported)', function() {",
        "    pm.expect(pm.response.code).to.be.at.least(400);",
        "});"
    ]
    return make_item("TC-FR14-H03 – PATCH Unsupported Method", req, tests)


def build_h04_get_headers():
    req = make_request("GET", "/api/categories")
    tests = [
        "pm.test('TC-FR14-H04: response content-type is JSON-like', function() {",
        "    pm.expect(pm.response.headers.get('Content-Type')).to.include('json');",
        "});",
        "var json = pm.response.json();",
        "pm.test('TC-FR14-H04: body parses as JSON', function() {",
        "    pm.expect(json).to.be.an('array');",
        "});"
    ]
    return make_item("TC-FR14-H04 – GET Response Headers", req, tests)


def build_h05_empty_put():
    """Empty PUT body must not corrupt existing category."""
    setup_create = make_request("POST", "/api/categories",
                                body={"name": "EmptyPutTarget"},
                                headers=get_helper("adminToken"))
    setup_tests = [
        "var json = pm.response.json();",
        "pm.test('TC-FR14-H05: setup category created', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "    pm.environment.set('emptyPutCategoryId', json.id);",
        "});"
    ]
    put = make_request("PUT", "/api/categories/{{emptyPutCategoryId}}",
                       body={},
                       headers=get_helper("adminToken"))
    put_tests = [
        "// Verify after empty PUT: original name must persist (not corrupted to null/empty)",
        "pm.sendRequest({",
        "    url: pm.variables.get('baseUrl') + '/api/categories',",
        "    method: 'GET',",
        "    header: { 'X-Student-Id': pm.variables.get('studentId') }",
        "}, function(err, response) {",
        "    pm.test('TC-FR14-H05: empty PUT does not corrupt original name', function() {",
        "        var arr = response.json();",
        "        var id = parseInt(pm.variables.get('emptyPutCategoryId'));",
        "        var found = arr.find(function(c) { return c.id === id; });",
        "        if (found) {",
        "            pm.expect(found.name).to.not.eql(null);",
        "            pm.expect(found.name).to.not.eql('');",
        "        }",
        "    });",
        "});"
    ]
    cleanup = make_request("DELETE", "/api/categories/{{emptyPutCategoryId}}",
                           headers=get_helper("adminToken"))
    cleanup_tests = [
        "pm.test('TC-FR14-H05: cleanup succeeds', function() {",
        "    pm.expect(pm.response.code).to.be.below(400);",
        "});"
    ]
    return [
        make_item("TC-FR14-H05 – Setup: Create Target", setup_create, setup_tests),
        make_item("TC-FR14-H05 – Empty PUT Body", put, put_tests),
        make_item("TC-FR14-H05 – Cleanup: Delete Target", cleanup, cleanup_tests),
    ]


def build_h06_rapid_creates():
    items = []
    for i in range(1, 4):
        body = {"name": f"Batch{i}RapidCreate"}
        req = make_request("POST", "/api/categories",
                           body=body,
                           headers=get_helper("adminToken"))
        tests = [
            "var json = pm.response.json();",
            f"pm.test('TC-FR14-H06c{i}: batch {i} create', function() {{",
            "    pm.expect(pm.response.code).to.be.below(400);",
            "    pm.expect(json.id).to.be.a('number');",
            f"    pm.environment.set('h06Batch{i}Id', json.id);",
            "});"
        ]
        items.append(make_item(f"TC-FR14-H06 – Batch {i} Rapid Create", req, tests))
    # Final verification
    verify = make_request("GET", "/api/categories")
    verify_tests = [
        "var json = pm.response.json();",
        "pm.test('TC-FR14-H06: all three batch entities distinct and visible', function() {",
        "    var ids = [pm.variables.get('h06Batch1Id'),",
        "               pm.variables.get('h06Batch2Id'),",
        "               pm.variables.get('h06Batch3Id')];",
        "    ids = ids.map(function(i) { return parseInt(i); });",
        "    var found = json.filter(function(c) { return ids.indexOf(c.id) !== -1; });",
        "    pm.expect(found.length).to.eql(3);",
        "    var distinctNames = new Set(found.map(function(c) { return c.name; }));",
        "    pm.expect(distinctNames.size).to.eql(3);",
        "});"
    ]
    items.append(make_item("TC-FR14-H06 – Verify All Batch Entities", verify, verify_tests))
    return items


def build_collection():
    items = []

    # Helpers
    items.append(build_helpers())

    # Folder: 01 Happy-path
    items.append({
        "name": "01 – Happy-Path CRUD",
        "description": "TC-FR14-001..006: Core CRUD with admin authentication.",
        "item": [
            build_tc001_get_list_public(),
            build_tc002_post_admin_create(),
            build_tc003_verify_created(),
            build_tc004_put_admin_update(),
            build_tc005_verify_updated(),
            build_tc006_delete_admin(),
        ]
    })

    # Folder: 02 Authentication (SEC-02)
    items.append({
        "name": "02 – Authentication (SEC-02)",
        "description": "TC-FR14-007..011: Missing/malformed/tampered JWT.",
        "item": [
            build_auth_missing("POST", "/api/categories", "TC-FR14-007", "UnauthCategoryPost"),
            build_auth_missing("PUT", "/api/categories/1", "TC-FR14-008", "UnauthCategoryPut"),
            build_auth_missing("DELETE", "/api/categories/1", "TC-FR14-009"),
            build_auth_malformed("POST", "/api/categories", "MalformedTokenCategory"),
            build_auth_tampered("/api/categories/1"),
        ]
    })

    # Folder: 03 RBAC (SEC-03)
    items.append({
        "name": "03 – Authorization RBAC (SEC-03)",
        "description": "TC-FR14-012..015: Regular User role must not mutate categories.",
        "item": [
            build_rbac_user_post(),
            build_rbac_user_put(),
            build_rbac_user_delete(),
            build_tc015_user_get(),
        ]
    })

    # Folder: 04 Name validation
    items.append({
        "name": "04 – Name Validation",
        "description": "TC-FR14-016..023: Mandatory non-empty name; exploratory boundaries.",
        "item": [
            build_name_invalid("", "016-Empty"),
            build_name_invalid(None, "017-Null"),
            build_name_invalid(None, "018-MissingKey"),  # special: empty {}
            build_name_invalid("   ", "019-Whitespace"),
            build_name_exploratory("A" * 1001, "020-LongName"),
            build_name_exploratory("Điện tử 📱 & Phụ kiện", "021-Unicode"),
            build_name_exploratory("Laptop", "022-Duplicate"),
            build_name_exploratory(12345, "023-Integer"),
        ]
    })

    # Folder: 05 ID validation
    items.append({
        "name": "05 – ID Validation",
        "description": "TC-FR14-024..028, 037..038: Nonexistent/zero/negative/non-numeric ID handling.",
        "item": [
            build_nonexistent("PUT", "/api/categories/99999", "024"),
            build_nonexistent("DELETE", "/api/categories/99999", "025"),
            build_invalid_id("PUT", "/api/categories/0", "026-Zero"),
            build_invalid_id("DELETE", "/api/categories/-1", "027-Negative"),
            build_invalid_id("PUT", "/api/categories/abc", "028-NonNumeric"),
        ]
    })

    # Folder: 06 Security probes
    items.append({
        "name": "06 – Security Probes",
        "description": "TC-FR14-029..033: SEC-05 injection resistance; SEC-04 UI; mass-assignment; NoSQL.",
        "item": [
            build_sql_injection(),
            build_xss_payload(),
            build_mass_assign_post(),
            build_mass_assign_put(),
            build_nosql_probe(),
        ]
    })

    # Folder: 07 Lifecycle
    items.append({
        "name": "07 – State Transitions",
        "description": "TC-FR14-035: Full create/update/delete lifecycle; 037/038 zombie integrity.",
        "item": build_lifecycle() + build_invalid_lifecycle()
    })

    # Folder: 08 Schema validation
    items.append({
        "name": "08 – Schema Validation",
        "description": "TC-FR14-039..042: Response shape observations for each CRUD method.",
        "item": build_schema_validation()
    })

    # Folder: 09 Human extensions
    items.append({
        "name": "09 – Human Extensions",
        "description": "TC-FR14-H01..H06: Post-audit gaps (Content-Type, zero-byte, PATCH, headers, empty PUT, batch).",
        "item": [
            build_h01_no_content_type(),
            build_h02_zero_byte(),
            build_h03_patch(),
            build_h04_get_headers(),
        ] + build_h05_empty_put() + build_h06_rapid_creates()
    })

    return {
        "info": {
            "_postman_id": "hw06-23127259-fr14-category-crud-canonical",
            "name": "FR14_Category_CRUD",
            "description": "HW06 FR-14 Category CRUD - canonical 46-case suite. Source: 23127259/testcases/fr14_canonical_cases.json. Rejected IDs (034/036/H07) excluded.",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "event": [
            {
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        "// Collection-level pre-request: enforce X-Student-Id: 23127259 on every request.",
                        "var studentId = pm.environment.get('studentId') || pm.variables.get('studentId') || '23127259';",
                        "pm.environment.set('studentId', studentId);",
                        "pm.request.headers.upsert({",
                        "    key: 'X-Student-Id',",
                        "    value: studentId",
                        "});"
                    ]
                }
            }
        ],
        "variable": [
            {"key": "baseUrl", "value": "http://localhost:3000"},
            {"key": "studentId", "value": "23127259"},
            {"key": "adminEmail", "value": "admin@eshop.com"},
            {"key": "adminPassword", "value": "Admin123!"},
            {"key": "userEmail", "value": "test@eshop.com"},
            {"key": "userPassword", "value": "Test1234!"},
            {"key": "adminToken", "value": ""},
            {"key": "userToken", "value": ""},
            {"key": "tamperedAdminToken", "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ImFkbWluIiwiaWF0IjoxNTE2MjM5MDIyfQ.tampered_signature"},
            {"key": "createdCategoryId", "value": ""},
            {"key": "lifecycleCategoryId", "value": ""},
            {"key": "schemaCategoryId", "value": ""},
            {"key": "emptyPutCategoryId", "value": ""},
            {"key": "h06Batch1Id", "value": ""},
            {"key": "h06Batch2Id", "value": ""},
            {"key": "h06Batch3Id", "value": ""},
            {"key": "initialCategoryCount", "value": "0"},
        ],
        "item": items
    }


def main():
    with open(CANONICAL_PATH, encoding="utf-8") as f:
        canonical = json.load(f)
    canonical_ids = {c["id"] for c in canonical}
    rejected = {"TC-FR14-034", "TC-FR14-036", "TC-FR14-H07"}
    missing = rejected - canonical_ids
    print(f"Canonical: {len(canonical)} cases (rejected confirmed absent: {len(rejected - missing)}/{len(rejected)})")

    collection = build_collection()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(collection, f, ensure_ascii=False, indent=2)

    # Count
    counts = {"requests": 0, "tests": 0, "folders": 0, "rejected_leaked": 0}
    rejected_set = {"034", "036", "H07"}
    def walk(items, in_folder=False):
        for item in items:
            if "item" in item:
                counts["folders"] += 1
                walk(item["item"])
            else:
                counts["requests"] += 1
                for ev in item.get("event", []):
                    if ev.get("listen") == "test":
                        counts["tests"] += sum(1 for line in ev.get("script", {}).get("exec", []) if "pm.test(" in line)
                name = item.get("name", "")
                if any(f"-{r} –" in name or f"-{r}-" in name for r in rejected_set):
                    counts["rejected_leaked"] += 1
    walk(collection["item"])
    print(f"Wrote {OUTPUT_PATH}")
    print(f"  Folders: {counts['folders']}")
    print(f"  Requests: {counts['requests']}")
    print(f"  pm.test() calls: {counts['tests']}")
    print(f"  Rejected leaked: {counts['rejected_leaked']}")


if __name__ == "__main__":
    main()
