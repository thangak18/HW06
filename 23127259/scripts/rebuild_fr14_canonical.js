#!/usr/bin/env node

const fs = require('fs');

const jsonPath = '23127259/testcases/fr14_canonical_cases.json';
const mapPath = '23127259/testcases/FR14_CANONICAL_PROVENANCE_MAP.md';
const rejected = new Set(['TC-FR14-034', 'TC-FR14-036', 'TC-FR14-H07']);
const cases = JSON.parse(fs.readFileSync(jsonPath, 'utf8')).filter((entry) => !rejected.has(entry.id));
const byId = new Map(cases.map((entry) => [entry.id, entry]));

function apply(ids, strength, oracle, refs) {
  for (const id of ids) {
    const entry = byId.get(id);
    if (!entry) throw new Error(`Missing canonical candidate ${id}`);
    entry.oracle_strength = strength;
    entry.semantic_oracle = oracle;
    if (refs) entry.source_refs = refs;
  }
}

apply(['TC-FR14-001'], 'PARTIAL-ORACLE', 'Successful public category-list observation; exact seeds/order/schema are not normative.', ['API-SPEC §3.4']);
apply(['TC-FR14-002', 'TC-FR14-003'], 'SPECIFICATION-BACKED', 'Admin create succeeds and the new unique-name category is API-visible via GET.', ['API-SPEC §3.4', 'SRS FR-12/FR-14']);
apply(['TC-FR14-004', 'TC-FR14-005'], 'SPECIFICATION-BACKED', 'Admin update succeeds and only the target category has the new API-visible name.', ['API-SPEC §3.4', 'SRS FR-12/FR-14']);
apply(['TC-FR14-006'], 'SPECIFICATION-BACKED', 'Admin delete succeeds and the isolated target is absent from the later list.', ['API-SPEC §3.4', 'SRS FR-12/FR-14']);
apply(['TC-FR14-007', 'TC-FR14-008', 'TC-FR14-009', 'TC-FR14-010', 'TC-FR14-011'], 'SPECIFICATION-BACKED', 'Invalid or missing JWT receives any 4xx/non-success and category state is not mutated.', ['SRS SEC-02', 'SRS FR-12']);
apply(['TC-FR14-012', 'TC-FR14-013', 'TC-FR14-014'], 'SPECIFICATION-BACKED', 'role=user category mutation receives any 4xx/non-success and no category state mutation.', ['SRS FR-12', 'SRS SEC-03']);
apply(['TC-FR14-015'], 'SPECIFICATION-BACKED', 'Authenticated User can read the public category list.', ['API-SPEC §3.4']);
apply(['TC-FR14-016', 'TC-FR14-017', 'TC-FR14-018', 'TC-FR14-019'], 'SPECIFICATION-BACKED', 'Mandatory non-empty name violation must not create an invalid API-visible category; exact error status is unspecified.', ['SRS FR-14']);
apply(['TC-FR14-020', 'TC-FR14-021', 'TC-FR14-022', 'TC-FR14-023'], 'EXPLORATORY', 'Observe unspecified name length/Unicode/duplicate/type behavior without a normative defect verdict.', ['API-SPEC §3.4']);
apply(['TC-FR14-024', 'TC-FR14-025', 'TC-FR14-037', 'TC-FR14-038'], 'PARTIAL-ORACLE', 'Any status is allowed, but the API must not falsely report successful modification/deletion of no existing entity.', ['API-SPEC §3.4', 'FR-14 CRUD semantics']);
apply(['TC-FR14-026', 'TC-FR14-027', 'TC-FR14-028'], 'EXPLORATORY', 'Observe unspecified zero/negative/non-numeric ID handling without exact status oracle.', ['API-SPEC §3.4']);
apply(['TC-FR14-029'], 'SPECIFICATION-BACKED', 'SQL-style input causes no query injection effect or category-table loss; black-box limitation recorded.', ['SRS SEC-05']);
apply(['TC-FR14-030'], 'EXPLORATORY', 'Record raw JSON persistence only; SEC-04 UI escaping cannot be adjudicated by this API response.', ['SRS SEC-04 (UI-scoped)']);
apply(['TC-FR14-031', 'TC-FR14-032'], 'PARTIAL-ORACLE', 'Observe that undocumented body fields do not override entity identity/authorization; SEC-07 is not claimed.', ['API-SPEC §3.4']);
apply(['TC-FR14-033'], 'EXPLORATORY', 'Observe object-type robustness without a NoSQL or exact-status oracle.', ['API-SPEC §3.4']);
apply(['TC-FR14-035'], 'SPECIFICATION-BACKED', 'Isolated create/read/update/read/delete/read lifecycle produces the expected API-visible states.', ['API-SPEC §3.4', 'SRS FR-14']);
apply(['TC-FR14-039', 'TC-FR14-040', 'TC-FR14-041', 'TC-FR14-042'], 'PARTIAL-ORACLE', 'Record observed response shape; only CRUD behavior and API-visible state are normative.', ['API-SPEC §3.4']);
apply(['TC-FR14-H01'], 'EXPLORATORY', 'Observe missing Content-Type behavior; HTTP 500 is robustness evidence, not a normative FR-14 bug.', ['GAP-H01']);
apply(['TC-FR14-H02'], 'PARTIAL-ORACLE', 'Zero-byte body does not establish a mandatory name; exact parser status is unspecified.', ['SRS FR-14', 'GAP-H02']);
apply(['TC-FR14-H03'], 'SPECIFICATION-BACKED', 'Undocumented PATCH receives non-success and does not change the isolated category.', ['API-SPEC §3.4', 'GAP-H03']);
apply(['TC-FR14-H04'], 'PARTIAL-ORACLE', 'Record JSON parseability and response MIME without treating header variation as a defect.', ['GAP-H04']);
apply(['TC-FR14-H05'], 'SPECIFICATION-BACKED', 'Missing update name must not erase/corrupt the isolated category name.', ['SRS FR-14', 'GAP-H05']);
apply(['TC-FR14-H06'], 'PARTIAL-ORACLE', 'Three rapid unique-name creates remain distinct and API-visible; monotonic IDs are observational.', ['SRS FR-14', 'GAP-H06']);

if (cases.length !== 46) throw new Error(`Expected 46 accepted cases, got ${cases.length}`);
fs.writeFileSync(jsonPath, `${JSON.stringify(cases, null, 2)}\n`);

const rows = cases.map((entry) => {
  const input = entry.input == null ? '' : JSON.stringify(entry.input).replaceAll('|', '\\|');
  return `| \`${entry.id}\` | ${entry.provenance} | ${entry.actor} | ${entry.method} | \`${entry.endpoint}\` | ${input} | ${entry.oracle_strength} | ${entry.semantic_oracle} |`;
});
const markdown = `# FR14 Canonical Provenance Map\n\n- Raw AI: 42\n- Rejected AI: TC-FR14-034, TC-FR14-036\n- Usable AI-derived: 40\n- Accepted Human: TC-FR14-H01..H06\n- Rejected Human candidate: TC-FR14-H07\n- Formal canonical total: 46\n\n| ID | Provenance | Actor | Method | Endpoint | Input | Oracle Strength | Corrected Semantic Oracle |\n|---|---|---|:---:|---|---|---|---|\n${rows.join('\n')}\n`;
fs.writeFileSync(mapPath, markdown);
