# Utility Scripts

This directory contains shared utility scripts for local test execution, Newman report generation, and continuous integration helpers.

---

## Example Usage

### 1. Running Newman Locally for Student Workspace (e.g. 23127259)
```bash
# Run 23127259 Postman Collection
newman run 23127259/postman/collections/collection.json \
  -e 23127259/postman/environments/environment.json \
  -d 23127259/postman/data/testdata.json \
  -r cli,htmlextra \
  --reporter-htmlextra-export 23127259/newman/report.html
```

### 2. Prerequisites
- **Node.js**: v18+ or v20+
- **Newman CLI**: `npm install -g newman`
- **Newman HTML Extra Reporter**: `npm install -g newman-reporter-htmlextra`
