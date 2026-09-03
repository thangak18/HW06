# Environment and Tooling Specifications

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Course:** HW06 – API Testing

---

## 1. Tooling & Runtime Environment Versions

| Component | Verified Version | Installation / Path | Verification Status |
|---|---|---|:---:|
| **Operating System** | macOS (Darwin arm64) | Host Machine | Verified |
| **Git CLI** | `git version 2.50.1 (Apple Git-155)` | `/usr/bin/git` | Verified |
| **Node.js** | `v25.2.1` | `/opt/homebrew/bin/node` | Verified |
| **npm** | `11.8.0` | `/opt/homebrew/bin/npm` | Verified |
| **Newman CLI** | `6.2.2` | `/opt/homebrew/bin/newman` | Verified |
| **Newman HTML Extra Reporter** | `newman-reporter-htmlextra` (latest) | Global npm package | Verified |
| **Postman Desktop Client** | `11.89.0` | Desktop Application | Verified |

---

## 2. System Under Test (SUT) Configuration

| Attribute | Configuration Detail |
|---|---|
| **SUT Repository** | [https://github.com/ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut) |
| **Local SUT Directory** | `../eshop-sut` (sibling directory outside HW06 repo) |
| **Backend Tech Stack** | Node.js, Express, SQLite3 (`sqlite3` module) |
| **Backend Entry Point** | `backend/server.js` |
| **Database File** | `backend/database.sqlite` (auto-seeded on server startup) |
| **Active Host / Port** | `http://localhost:3000` |
| **Startup Command** | `node backend/server.js` (from SUT root) |
| **Database Reset Behavior** | `initDatabase()` executes on every server restart, dropping and re-seeding all tables |
