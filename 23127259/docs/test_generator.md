# AI-Driven API Test Generator – Pseudocode

> **Self-authored design artifact.** This document specifies the
> AI-driven test-generation pipeline used to produce the raw AI test drafts
> for FR-02, FR-10, and FR-14. The pseudocode is descriptive, not
> executable; it documents the intent and the inputs/outputs of each stage.

## 1. Goals

1. Generate ≥ 35 raw AI test cases per selected feature.
2. Cover Level-1 normative requirements first, then partial-oracle, then
   exploratory.
3. Use a deterministic prompt template so that each raw draft is
   reproducible from its prompt alone.
4. Enforce that every AI case is independently auditable by a Human.

## 2. Inputs

- `requirements[]` – List of normative requirements from `SRS.md` and
  `api_specification.md`.
- `security_map[]` – Mapping from requirement → security identifier
  (`SEC-02`, `SEC-03`, …).
- `feature_id` – One of `FR-02 | FR-10 | FR-14`.
- `endpoint_table[]` – From the API specification.

## 3. Stages

### Stage A – Requirement Compilation

```
INPUT: requirements[], security_map[], feature_id
OUTPUT: requirement_set[]

function compile_requirements(requirements, security_map, feature_id):
    return [
        req for req in requirements
        if req.feature == feature_id
    ]
```

### Stage B – Prompt Template Instantiation

```
INPUT: requirement_set[], endpoint_table[], feature_id
OUTPUT: prompt_text

PROMPT_TEMPLATE = """
You are a senior QA engineer.
Given the following requirements and endpoints for feature {feature_id},
generate {target_count} raw API test cases covering:
 - normative behaviour
 - error paths (4xx where Level-1 supports)
 - RBAC and authentication
 - boundary and validation
 - exploratory observations

Output each case with:
 - id (FEATURE-AI-NNN)
 - title
 - actor
 - method, endpoint, request body
 - expected status (cite Level-1 source if non-default)
 - source_refs

Do not fabricate exact status codes unless Level-1 documents them.
"""
```

### Stage C – Raw Draft Generation

```
INPUT: prompt_text
OUTPUT: raw_draft

function call_ai(prompt_text):
    response = llm.invoke(prompt=prompt_text)
    return response.text
```

### Stage D – Parse & Normalise

```
INPUT: raw_draft
OUTPUT: cases[]

function parse_cases(raw_draft):
    blocks = split_by_heading(raw_draft, "### TC-")
    return [
        {
            "id":          block.id,
            "title":       block.title,
            "actor":       block.actor,
            "method":      block.method,
            "endpoint":    block.endpoint,
            "body":        block.body,
            "expected":    block.expected,
            "source_refs": block.source_refs,
        }
        for block in blocks
    ]
```

### Stage E – Provenance Freeze

```
INPUT: cases[]
OUTPUT: canonical_raw_json, sha256

function freeze(cases, feature_id):
    payload = json.dumps(cases, sort_keys=True)
    sha256  = hashlib.sha256(payload.encode()).hexdigest()
    write_file(f"{feature_id}_AI_DRAFT.md", cases)
    write_file(f"{feature_id}_AI_DRAFT.sha256", sha256)
    return payload, sha256
```

### Stage F – Human Audit (downstream)

```
INPUT: cases[]
OUTPUT: audited_cases[] with status ∈ {VALID, INVALID, INCOMPLETE}

function human_audit(cases):
    for c in cases:
        c.status = classify(c)
        if c.status == INCOMPLETE:
            c.correction = human_correct(c)
    return cases
```

### Stage G – Gap Analysis & Human Extensions

```
INPUT: audited_cases[], requirement_set[]
OUTPUT: human_extensions[]

function gap_analysis(audited, requirements):
    covered_requirements = {req.id for req in audited}
    missing              = [r for r in requirements if r.id not in covered_requirements]
    return missing
```

### Stage H – Canonical Suite Reconstruction

```
INPUT: audited_cases[] + human_extensions[]
OUTPUT: canonical_cases[] (raw IDs preserved, INCOMPLETE replaced by correction)

function canonicalise(audited, human):
    keep  = [c for c in audited if c.status == VALID]
    fixed = [c for c in audited if c.status == INCOMPLETE]
    return dedupe_by_semantics(keep + fixed + human)
```

## 4. Validation Hooks

```
function validate_pipeline(feature_id):
    assert count(raw_draft) >= 35
    assert all(c.source_refs for c in audited)
    assert all(c.id.startswith(feature_id) for c in canonical)
    assert no_duplicate_ids(canonical)
    return True
```

## 5. Human-in-the-Loop Gates

1. **Stage F** cannot run without explicit Human sign-off per case.
2. **Stage G** additions must cite a specific uncovered requirement.
3. **Stage H** must produce a per-case audit trail in
   `*_EXECUTION_TRACEABILITY.md`.

## 6. Failure Modes

| Stage | Failure | Recovery |
|---|---|---|
| B | Prompt misfires | Re-issue with smaller `target_count`. |
| C | Provider unavailable | Use cached draft from `*.sha256` sibling. |
| D | Malformed draft | Re-prompt with stricter "Output Schema" prefix. |
| F | Human cannot classify | Mark INCOMPLETE and request correction. |
| H | Duplicate IDs | Re-number with explicit `-N` suffix. |

## 7. Outputs

- Per-feature raw draft Markdown file
- Per-feature SHA-256 sibling
- Canonical machine-readable JSON (`fr*_canonical_cases.json`)
- Per-feature Postman collection
- Per-feature Newman CLI/JSON/HTML artifacts
- Per-feature bug reports (`BUG-FR*-*.md`)

The pseudocode above is the authoritative design description of the
pipeline. The final visual diagram for the assignment is specified
separately in `AI_TEST_GENERATOR_DIAGRAM_SPEC.md`.