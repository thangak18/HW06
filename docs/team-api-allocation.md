# Team API Allocation Matrix

This document tracks the API feature assignments for each member of the team to ensure zero duplicate feature selections across the group.

---

## 1. Team Allocation Table

| Member | Student Name | Student ID | GitHub Handle | Pool A Feature (Auth / Prod) | Pool B Feature (Cart / Order) | Pool C Feature (Admin) | Workspace Folder |
|---|---|---|---|---|---|---|---|
| **Member 1** | TODO | TODO | TODO | TODO | TODO | TODO | `members/member-1` |
| **Member 2** | TODO | TODO | TODO | TODO | TODO | TODO | `members/member-2` |
| **Member 3** | TODO | TODO | TODO | TODO | TODO | TODO | `members/member-3` |

---

## 2. Selection Rules & Feature Directory

Each member **must pick exactly one feature from each of the three pools**:

### Available Features in Pool A (Authentication & Catalog)
- `FR-01`: Account registration (`POST /api/auth/register`)
- `FR-02`: Login and account lockout (`POST /api/auth/login`)
- `FR-03`: Forgot / reset password (`POST /api/auth/forgot-password`, `POST /api/auth/reset-password`)
- `FR-04`: Personal profile management (`GET /api/user/profile`, `PUT /api/user/profile`, `PUT /api/user/change-password`)
- `FR-05`: Product listing & search (`GET /api/products`, `GET /api/products/search`)
- `FR-06`: Product detail view (`GET /api/products/:id`)

### Available Features in Pool B (Shopping Cart & Order)
- `FR-07`: Shopping cart (`GET/POST/PUT/DELETE /api/cart`)
- `FR-08`: Checkout (`POST /api/checkout`, `POST /api/checkout/calculate`)
- `FR-09`: Discount coupons (`POST /api/coupons/apply`, `GET /api/coupons/validate`)
- `FR-10`: Order state machine (`GET/POST /api/orders/:id/status`, `POST /api/orders/:id/cancel`)
- `FR-11`: Order history view (user) (`GET /api/orders`, `GET /api/orders/:id`)

### Available Features in Pool C (Web Admin & Governance)
- `FR-12`: Access control (`/api/admin/*` RBAC checks)
- `FR-13`: Dashboard metrics (`GET /api/admin/dashboard/*`)
- `FR-14`: Category management CRUD (`/api/admin/categories`)
- `FR-15`: Product management CRUD (`/api/admin/products`)
- `FR-16`: Product CSV import (`POST /api/admin/products/import-csv`)
- `FR-17`: Coupon management CRUD (`/api/admin/coupons`)
- `FR-18`: Admin order management (`/api/admin/orders`)
- `FR-19`: Admin user management (`/api/admin/users`)

---

## 3. Duplication Guard

> **Rule:** No two team members should test the exact same 3-API tuple. It is strongly recommended that each member selects distinct individual features within each pool to maximize learning diversity and eliminate cross-member submission overlap.
