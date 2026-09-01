# Agent Skill – Test Generator Pseudocode

- **Student:** Nguyễn Tấn Thắng (23127259)
- **Course:** HW06 – API Testing
- **Component:** Agent Skill AI Test Generator Engine (Phase 5 Specification)

---

## 1. Algorithmic Overview

The AI Test Generator Agent Skill consumes an API endpoint specification along with the authoritative security rules (**SEC-01** through **SEC-07**) and outputs structured, executable Postman test items.

```python
"""
Agent Skill: Automated API Test Generator
Input: API Specification Dict, Security Rule Set, State Transition Matrix
Output: Postman Collection Test Item Array
"""

def generate_api_test_suite(api_spec: dict, security_rules: list, state_matrix: dict) -> list:
    test_suite = []
    
    # 1. Parameter Extraction & Equivalence Partitioning
    parameters = extract_request_parameters(api_spec)
    ep_bva_cases = generate_domain_and_bva_partitions(parameters)
    test_suite.extend(ep_bva_cases)
    
    # 2. State Machine Transitions (Valid, Invalid, Terminal States)
    if state_matrix:
        state_cases = generate_state_machine_tests(state_matrix)
        test_suite.extend(state_cases)
        
    # 3. Security Rule Application (SEC-01..07)
    security_cases = apply_security_templates(api_spec, security_rules)
    test_suite.extend(security_cases)
    
    # 4. JSON Schema Validation Assertions
    schema_cases = generate_schema_assertions(api_spec.get("responses", {}))
    test_suite.extend(schema_cases)
    
    # 5. Negative & Malformed Request Scenarios
    negative_cases = generate_negative_payload_tests(api_spec)
    test_suite.extend(negative_cases)
    
    # 6. Deduplication & Unique Identifier Assignment
    final_cases = deduplicate_and_assign_ids(test_suite, prefix=api_spec.get("feature_id", "TC"))
    return final_cases
```
