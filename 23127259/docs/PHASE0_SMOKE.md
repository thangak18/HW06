# Phase 0 – SUT Smoke Check & Connectivity Log

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Execution Timestamp:** 2026-09-01T18:42:52+07:00
- **Target Host:** `http://localhost:3000`
- **Purpose:** Confirm that the local SUT backend is listening and responding to basic HTTP requests before initiating formal test design.

> [!NOTE]
> These smoke checks exist **solely to verify network connectivity and runtime readiness**. They do NOT constitute formal HW06 test case execution for FR-02, FR-10, or FR-14.

---

## 1. Smoke Check Execution Records

### Check 1: Public Categories Endpoint (`GET /api/categories`)
- **Endpoint:** `GET http://localhost:3000/api/categories`
- **Headers:** `Accept: application/json`
- **Response Status:** `HTTP 200 OK`
- **Response Body:**
  ```json
  [
    {"id": 1, "name": "Điện thoại"},
    {"id": 2, "name": "Laptop"},
    {"id": 3, "name": "Phụ kiện"}
  ]
  ```
- **Connectivity Status:** **SUCCESSFUL**

---

### Check 2: Public Products Endpoint (`GET /api/products`)
- **Endpoint:** `GET http://localhost:3000/api/products`
- **Headers:** `Accept: application/json`
- **Response Status:** `HTTP 200 OK`
- **Response Body Snippet:**
  ```json
  [
    {
      "id": 1,
      "name": "iPhone 15 Pro Max",
      "price": 30000000,
      "description": "Điện thoại cao cấp của Apple",
      "imageUrl": "https://placehold.co/300x300/png?text=iPhone+15",
      "category_id": 1
    }
  ]
  ```
- **Connectivity Status:** **SUCCESSFUL**

---

### Check 3: Authentication Smoke Check (`POST /api/login`)
- **Endpoint:** `POST http://localhost:3000/api/login`
- **Headers:** `Content-Type: application/json`
- **Request Body:** `{"email": "test@eshop.com", "password": "Test1234!"}` (Seeded test account per SRS)
- **Response Status:** `HTTP 200 OK`
- **Response Body Attributes:** Returns valid JWT `token`, `message: "Login successful"`, and `user` object.
- **Connectivity Status:** **SUCCESSFUL**

---

## 2. Summary
- All 3 baseline smoke checks returned `HTTP 200 OK`.
- SUT backend is healthy, responsive, and ready for Phase 1 automated testing.
