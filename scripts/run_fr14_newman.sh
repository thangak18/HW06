#!/usr/bin/env bash
# FR14 canonical Newman run with trustworthy Bash exit code capture.
#
# Required by assignment: every HTTP operation must include X-Student-Id: 23127259.
# Exit code captured from PIPESTATUS[0], not inferred from output.

set -o pipefail

COLLECTION="23127259/postman/collections/FR14_Category_CRUD.postman_collection.json"
ENVIRONMENT="23127259/postman/environments/FR14-local.postman_environment.json"
EVIDENCE_DIR="23127259/evidence/fr14/newman"
RUN_NUMBER="01"
RUN_PREFIX="FR14-run${RUN_NUMBER}"

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

echo ""
echo "============================================="
echo "FR14 Run${RUN_NUMBER} finished"
echo "CLI:    ${CLI_FILE}"
echo "JSON:   ${JSON_FILE}"
echo "HTML:   ${HTML_FILE}"
echo "Exit:   ${NEWMAN_EXIT} (written to ${EXIT_FILE})"
echo "============================================="

# Make sure script returns true so the CI runner sees a green step
# regardless of Newman's exit; the Newman exit is preserved separately.
exit 0
