#!/usr/bin/env bash

set -o pipefail

run_label="${1:-local-smoke}"
evidence_dir="23127259/ci/evidence/${run_label}"
collection="23127259/postman/collections/HW06_CI_Passing_Smoke.postman_collection.json"
base_url="${BASE_URL:-http://localhost:3010}"
student_id="${STUDENT_ID:-23127259}"
deliberate_red="${DELIBERATE_RED:-0}"
if [[ -n "${NEWMAN_BIN:-}" ]]; then
  newman_cmd=("${NEWMAN_BIN}")
else
  newman_cmd=(npx newman)
fi

mkdir -p "${evidence_dir}"
cli_file="${evidence_dir}/ci-smoke-cli.log"
junit_file="${evidence_dir}/ci-smoke-junit.xml"
exit_file="${evidence_dir}/ci-smoke-exit.txt"

set +e
"${newman_cmd[@]}" run "${collection}" \
  --env-var "baseUrl=${base_url}" \
  --env-var "studentId=${student_id}" \
  --env-var "deliberateRed=${deliberate_red}" \
  --reporters cli,junit \
  --reporter-junit-export "${junit_file}" \
  2>&1 | tee "${cli_file}"
newman_exit=${PIPESTATUS[0]}
set -e

printf '%s\n' "${newman_exit}" > "${exit_file}"

if [[ "${deliberate_red}" == "1" ]]; then
  if [[ "${newman_exit}" -eq 0 ]]; then
    echo "ERROR: deliberate-red run unexpectedly passed"
    exit 2
  fi
  if ! grep -Eq 'failures="1"' "${junit_file}"; then
    echo "ERROR: deliberate-red JUnit does not show exactly one failure"
    exit 3
  fi
  if ! grep -q 'DELIBERATE_RED' "${junit_file}"; then
    echo "ERROR: the sole failure is not the deliberate-red assertion"
    exit 4
  fi
  echo "Verified exactly one intended DELIBERATE_RED assertion failure."
  exit "${newman_exit}"
fi

if [[ "${newman_exit}" -ne 0 ]]; then
  echo "ERROR: passing smoke suite had a Newman failure"
  exit "${newman_exit}"
fi

if ! grep -Eq 'failures="0"' "${junit_file}"; then
  echo "ERROR: passing smoke JUnit does not report zero failures"
  exit 5
fi

echo "Verified all FR02/FR10/FR14 CI smoke assertions passed."
