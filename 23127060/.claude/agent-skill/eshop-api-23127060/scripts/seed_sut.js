#!/usr/bin/env node
/**
 * seed_sut.js - Dua SUT ve trang thai biet truoc de test API co the lap lai duoc.
 *
 *   node seed_sut.js reset  --db ../../../eshop-sut/backend/database.sqlite
 *   node seed_sut.js check  --db ../../../eshop-sut/backend/database.sqlite
 *
 * LUU Y QUAN TRONG:
 *   database.js cua SUT goi initDatabase() ngay khi require => MOI LAN restart
 *   backend la DB bi DROP + seed lai. Vi vay thu tu dung la:
 *     1) khoi dong backend
 *     2) chay seed_sut.js reset
 *     3) chay newman
 *   Neu restart backend giua chung thi phai seed lai.
 *
 * Script nay khong dung thu vien ngoai: no goi HTTP toi chinh SUT (khong dung sqlite3)
 * de tranh phu thuoc. Neu can thao tac truc tiep DB (vd gia lap token het han) thi
 * dung sqlite3 CLI - xem ham printSqlHints().
 */

const http = require("http");

const SID = "23127060";
const BASE = process.env.BASE_URL || "http://localhost:3000";

const USERS = [
  { email: `api.victim.${SID}@test.local`, password: "Api1234!", name: `Victim ${SID}` },
  { email: `api.attacker.${SID}@test.local`, password: "Api1234!", name: `Attacker ${SID}` },
];

function req(method, path, body, token) {
  return new Promise((resolve) => {
    const data = body ? JSON.stringify(body) : null;
    const u = new URL(BASE + path);
    const headers = {
      "Content-Type": "application/json",
      "X-Student-Id": SID,
    };
    if (data) headers["Content-Length"] = Buffer.byteLength(data);
    if (token) headers["Authorization"] = "Bearer " + token;

    const r = http.request(
      { hostname: u.hostname, port: u.port || 80, path: u.pathname + u.search, method, headers },
      (res) => {
        let buf = "";
        res.on("data", (c) => (buf += c));
        res.on("end", () => {
          let json = null;
          try { json = JSON.parse(buf); } catch (e) { json = null; }
          resolve({ status: res.statusCode, body: json, raw: buf });
        });
      }
    );
    r.on("error", (e) => resolve({ status: 0, body: null, raw: String(e) }));
    if (data) r.write(data);
    r.end();
  });
}

async function ping() {
  const r = await req("GET", "/api/products");
  if (r.status !== 200) {
    console.error(`[LOI] SUT khong phan hoi tai ${BASE} (status=${r.status}).`);
    console.error("      Chay: (cd <duong-dan>/eshop-sut/backend && nohup node server.js > /tmp/eshop.log 2>&1 &)");
    process.exit(1);
  }
  return r;
}

async function reset() {
  console.log(`[INFO] SUT = ${BASE}`);
  await ping();

  for (const u of USERS) {
    const r = await req("POST", "/api/register", {
      email: u.email, password: u.password, name: u.name,
    });
    if (r.status === 200 || r.status === 201) {
      console.log(`[OK ] tao user ${u.email}`);
    } else if (r.status === 400 || r.status === 409) {
      console.log(`[SKIP] user ${u.email} da ton tai`);
    } else {
      console.log(`[WARN] register ${u.email} -> ${r.status} ${r.raw.slice(0, 120)}`);
    }
  }

  for (const u of USERS) {
    const r = await req("POST", "/api/login", { email: u.email, password: u.password });
    if (r.status === 200 && r.body && r.body.token) {
      console.log(`[OK ] login ${u.email} -> userId=${r.body.user && r.body.user.id}`);
      if (r.body.user && r.body.user.password !== undefined) {
        console.log("       [BUG A-07] response login co chua truong 'password'!");
      }
    } else {
      console.log(`[WARN] login ${u.email} -> ${r.status}. Neu bi khoa, doi 180s hoac restart backend.`);
    }
  }

  const p1 = await req("GET", "/api/products/1");
  const p2 = await req("GET", "/api/products/2");
  console.log(`[INFO] product id=1 price type = ${p1.body ? typeof p1.body.price : "?"} (mong doi: number)`);
  console.log(`[INFO] product id=2 price type = ${p2.body ? typeof p2.body.price : "?"} (BUG C-05 neu la string)`);

  console.log("");
  console.log("[DONE] seed xong. Cac hang so dung trong test:");
  console.log(`  userEmail        = api.victim.${SID}@test.local`);
  console.log(`  attackerEmail    = api.attacker.${SID}@test.local`);
  console.log("  password         = Api1234!");
  console.log("  productIdOdd     = 1   (price la number)");
  console.log("  productIdEven    = 2   (price bi ep thanh string - bug C-05)");
  console.log("");
  printSqlHints();
}

async function check() {
  await ping();
  const checks = [
    ["GET /api/products", "GET", "/api/products", null],
    ["GET /api/products/999999 (mong doi 404, bug C-04 tra 200 {})", "GET", "/api/products/999999", null],
    ["GET /api/products?search=' (mong doi JSON 400, bug C-03 tra HTML)", "GET", "/api/products?search=%27", null],
  ];
  for (const [label, m, p, b] of checks) {
    const r = await req(m, p, b);
    const isHtml = r.raw.trim().startsWith("<");
    console.log(`[${String(r.status).padStart(3)}] ${label}${isHtml ? "  <-- TRA VE HTML" : ""}`);
  }
}

function printSqlHints() {
  console.log("[GOI Y] Cac thao tac phai lam truc tiep tren DB (dung sqlite3 CLI):");
  console.log("  # gia lap token reset het han");
  console.log("  sqlite3 database.sqlite \"UPDATE users SET reset_token='1234' WHERE email LIKE 'api.victim%';\"");
  console.log("  # gia lap tai khoan bi khoa");
  console.log("  sqlite3 database.sqlite \"UPDATE users SET login_attempts=5, locked_until=strftime('%s','now')*1000+180000 WHERE email LIKE 'api.victim%';\"");
  console.log("  # xem coupon da seed");
  console.log("  sqlite3 database.sqlite \"SELECT code, discount_type, discount_value, min_order_amount, expiry_date, is_active FROM coupons;\"");
  console.log("  # nang quyen admin cho 1 tai khoan test");
  console.log("  sqlite3 database.sqlite \"UPDATE users SET role='admin' WHERE email='admin@eshop.com';\"");
}

const cmd = process.argv[2] || "reset";
if (cmd === "reset") reset();
else if (cmd === "check") check();
else {
  console.log("Dung: node seed_sut.js [reset|check]");
  process.exit(1);
}
