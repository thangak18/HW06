# Utility Scripts

This folder contains shared utility scripts for local execution, Newman report generation, and continuous integration helpers.

---

## Example Usage

### 1. Running Newman Locally for a Member Workspace
```bash
# Run Member 1 Postman Collection
newman run members/member-1/postman/collections/collection.json \
  -e members/member-1/postman/environments/environment.json \
  -d members/member-1/postman/data/testdata.json \
  -r cli,htmlextra \
  --reporter-htmlextra-export members/member-1/newman/report.html
```

### 2. Prerequisites
- **Node.js**: v18+ or v20+
- **Newman CLI**: `npm install -g newman`
- **Newman HTML Extra Reporter**: `npm install -g newman-reporter-htmlextra`
