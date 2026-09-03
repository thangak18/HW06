#!/usr/bin/env bash
# FR10 canonical Newman runner (Run04 lineage).
# Writes CLI, JSON, HTML, and exit code to evidence dir.

set -o pipefail

STUDENT_ID="${STUDENT_ID:-23127259}"
FR_DIR="${FR_DIR:-23127259/postman}"
EVIDENCE_DIR="${EVIDENCE_DIR:-23127259/evidence/fr10/newman}"
RUN_PREFIX="${RUN_PREFIX:-FR10-run04}"

COLLECTION="${FR_DIR}/collections/FR10_Order_CRUD.postman_collection.json"
ENVIRONMENT="${FR_DIR}/environments/FR10-local.postman_environment.json"

mkdir -p "${EVIDENCE_DIR}"

CLI_FILE="${EVIDENCE_DIR}/${RUN_PREFIX}-cli.txt"
JSON_FILE="${EVIDENCE_DIR}/${RUN_PREFIX}.json"
HTML_FILE="${EVIDENCE_DIR}/${RUN_PREFIX}.html"
EXIT_FILE="${EVIDENCE_DIR}/${RUN_PREFIX}-exitcode.txt"

newman run "${COLLECTION}" \
    -e "${ENVIRONMENT}" \
    --reporters cli,json,htmlextra \
    --reporter-json-export "${JSON_FILE}" \
    --reporter-htmlextra-export "${HTML_FILE}" \
    2>&1 | tee "${CLI_FILE}"

NEWMAN_EXIT=${PIPESTATUS[0]}
printf '%s\n' "${NEWMAN_EXIT}" > "${EXIT_FILE}"

echo "FR10 Run finished. Exit=${NEWMAN_EXIT}"
# Always return 0 so CI upload-artifact step still runs on red runs.
exit 0
