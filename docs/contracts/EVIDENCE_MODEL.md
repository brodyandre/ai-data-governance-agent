# Evidence Model Contract

## Purpose

This document defines the technical contract for the `Evidence` domain model used by the AI Data Governance Agent.

The implementation is tracked by backlog item:

`DG-102 — Evidence model`

The model will later be implemented with Pydantic 2.

This contract refines the conceptual evidence definition originally documented in:

`docs/contracts/INCIDENT_INPUT.md`

and depends on the enum definitions documented in:

`docs/contracts/DOMAIN_ENUMS.md`

---

## Objective

The Evidence model represents one traceable piece of technical, analytical, business, or governance information associated with an incident.

Examples include:

- Data Quality validation results;
- pipeline reports;
- reconciliation results;
- logs;
- business rules;
- governance policies;
- analyst observations;
- metrics;
- dataset samples.

Evidence is a core traceability primitive of the project.

Later components must be able to reference an evidence item through its stable `evidence_id`.

---

## Model Name

Python class:

`Evidence`

Planned implementation:

```text
src/
└── ai_data_governance_agent/
    └── domain/
        ├── __init__.py
        ├── enums.py
        └── evidence.py
```

Planned tests:

```text
tests/
└── domain/
    ├── test_enums.py
    └── test_evidence.py
```

---

## Fields

The Evidence model must support the following fields.

| Field | Type | Required |
| --- | --- | --- |
| `evidence_id` | string | yes |
| `evidence_type` | `EvidenceType` | yes |
| `source` | string | yes |
| `description` | string or null | no |
| `value` | JSON-compatible value or null | no |
| `collected_at` | datetime or null | no |
| `reliability` | `EvidenceReliability` or null | no |
| `metadata` | JSON-compatible object | no |

---

## evidence_id

Type:

`str`

Required:

Yes.

Purpose:

Provide a stable identifier that other domain objects can use to reference this evidence item.

Example:

```text
EV-001
```

Rules:

- must be present;
- must contain non-whitespace text;
- leading and trailing whitespace should be removed;
- identifiers are case-sensitive;
- identifiers must not be automatically rewritten;
- uniqueness is not enforced inside a single Evidence instance.

Examples of valid identifiers:

```text
EV-001
DQ-CHECK-17
PIPELINE-REPORT-2026-10-06
```

Examples of invalid identifiers:

```text
""
"   "
null
```

Duplicate evidence identifiers are not detected by the Evidence model itself.

Duplicate detection belongs to a collection-level or incident-level validation step.

This allows `DG-102` to remain focused on validating one evidence item.

---

## evidence_type

Type:

`EvidenceType`

Required:

Yes.

Purpose:

Identify the semantic type of the evidence.

Allowed serialized values are defined by:

`docs/contracts/DOMAIN_ENUMS.md`

Current values:

- `data_quality_check`;
- `pipeline_report`;
- `validation_result`;
- `reconciliation_result`;
- `log`;
- `business_rule`;
- `governance_policy`;
- `analyst_observation`;
- `metric`;
- `dataset_sample`.

Unsupported evidence types must be rejected.

The model must not silently convert unsupported values into another evidence type.

Examples:

```text
reconciliation_result
pipeline_report
metric
```

are valid.

Examples:

```text
reconciliation
report
DataQuality
unknown_type
```

are invalid.

---

## source

Type:

`str`

Required:

Yes.

Purpose:

Identify the system, process, document, report, user, component, or other origin that produced the evidence.

Examples:

```text
pipeline-report
great-expectations
sales-reconciliation-job
governance-policy-catalog
data-engineer-observation
```

Rules:

- must be present;
- must contain non-whitespace text;
- leading and trailing whitespace should be removed;
- the original semantic value must otherwise be preserved.

Examples of invalid source values:

```text
""
"   "
null
```

---

## description

Type:

`str | None`

Required:

No.

Purpose:

Provide a concise human-readable explanation of what the evidence represents.

Example:

```text
Raw and silver record counts differ.
```

When provided:

- leading and trailing whitespace should be removed;
- the resulting value must contain meaningful non-whitespace text.

An empty description should not be accepted as meaningful content.

The field may be omitted when the evidence value is self-explanatory or when the source does not provide a description.

---

## value

Type:

JSON-compatible value or `None`.

Required:

No.

Purpose:

Store the actual evidence payload or summarized evidence value.

The initial conceptual Incident Input contract described this concept as:

`value or content`

For the Challenge MVP, the canonical field name is:

`value`

A separate `content` field will not be introduced.

This avoids two fields representing the same concept.

The value may contain JSON-compatible data such as:

- string;
- integer;
- floating-point number;
- boolean;
- list;
- object;
- null.

Examples:

```json
"orders RAW=400 SILVER=388"
```

```json
30
```

```json
0.075
```

```json
true
```

```json
{
  "raw_count": 400,
  "silver_count": 388,
  "difference": 12
}
```

```json
[
  "ORD-000038",
  "ORD-000144",
  "ORD-000148"
]
```

The Evidence model must not interpret or infer the semantic meaning of `value`.

Interpretation belongs to later deterministic tools or workflow logic.

---

## collected_at

Type:

`datetime | None`

Required:

No.

Purpose:

Represent when the evidence was collected or generated.

Example serialized value:

```text
2026-10-05T20:00:00Z
```

Pydantic may accept a valid ISO 8601 datetime string and parse it into a Python datetime.

Malformed datetime values must be rejected.

Examples of valid input:

```text
2026-10-05T20:00:00Z
2026-10-05T17:00:00-03:00
```

Example of invalid input:

```text
yesterday evening
```

DG-102 does not introduce additional timezone business rules.

Timezone-specific policies may be defined later if the project requires them.

---

## reliability

Type:

`EvidenceReliability | None`

Required:

No.

Purpose:

Represent the assessed reliability of the evidence source or observation.

Allowed values:

- `low`;
- `medium`;
- `high`.

These values are defined in:

`docs/contracts/DOMAIN_ENUMS.md`

No `unknown` reliability enum is defined.

When reliability has not been assessed, the field should remain absent or `None`.

This preserves the distinction between:

- an explicit reliability assessment;

and:

- no reliability assessment.

---

## metadata

Type:

JSON-compatible object.

Required:

No.

Default:

Empty object.

Purpose:

Store optional evidence-specific contextual attributes that do not justify dedicated top-level fields.

Examples:

```json
{
  "pipeline_run_id": "run-20261005-001",
  "dataset": "orders",
  "layer": "silver"
}
```

or:

```json
{
  "rule_id": "DQ-QUANTITY-001",
  "failed_records": 30
}
```

Metadata values must remain JSON-compatible.

The Evidence model should not attempt to interpret metadata semantics.

Mutable defaults must be created safely.

The implementation must not use a shared mutable dictionary instance between model objects.

---

## Minimum Valid Evidence

A structurally valid Evidence item requires only:

- `evidence_id`;
- `evidence_type`;
- `source`.

Example:

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "pipeline_report",
  "source": "sales-pipeline"
}
```

This is intentionally allowed.

The project accepts that evidence may be incomplete.

Insufficient informational content is different from an invalid schema.

Later analysis and governance logic may determine that the evidence is insufficient to support a conclusion.

DG-102 must not attempt to calculate evidence sufficiency.

---

## Complete Example

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "reconciliation_result",
  "source": "pipeline-report",
  "description": "Raw and silver record counts differ.",
  "value": {
    "raw_count": 400,
    "silver_count": 388,
    "difference": 12
  },
  "collected_at": "2026-10-05T20:00:00Z",
  "reliability": "high",
  "metadata": {
    "dataset": "orders",
    "layer": "silver"
  }
}
```

---

## Extra Fields

The Evidence model should reject undocumented top-level fields.

The planned Pydantic configuration should use strict schema behavior equivalent to:

```text
extra = "forbid"
```

For example, this should be rejected:

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric",
  "source": "monitoring",
  "unsupported_field": "value"
}
```

This behavior helps detect malformed or unsupported evidence structures early.

---

## String Normalization

For top-level textual fields:

- leading whitespace should be removed;
- trailing whitespace should be removed.

This applies to:

- `evidence_id`;
- `source`;
- `description`.

Example input:

```text
"  EV-001  "
```

should result in:

```text
"EV-001"
```

However, the system must not perform semantic rewriting.

For example:

```text
"ev-001"
```

must not automatically become:

```text
"EV-001"
```

---

## Enum Validation

The model must use the domain enums defined by DG-101.

Example:

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "reconciliation_result",
  "source": "pipeline-report",
  "reliability": "high"
}
```

must validate successfully.

This must fail:

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "RECONCILIATION_RESULT",
  "source": "pipeline-report"
}
```

Enum validation must remain case-sensitive.

---

## Serialization

The Evidence model must support deterministic serialization.

When serialized in JSON mode:

- enum members must use their string values;
- datetimes must use an ISO-compatible representation;
- dictionaries and lists must remain JSON structures;
- field names must remain stable.

Example conceptual result:

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "reconciliation_result",
  "source": "pipeline-report",
  "description": "Raw and silver record counts differ.",
  "value": "orders RAW=400 SILVER=388",
  "collected_at": "2026-10-05T20:00:00Z",
  "reliability": "high",
  "metadata": {}
}
```

DG-102 does not require custom JSON encoders when standard Pydantic behavior already satisfies the contract.

---

## Duplicate Evidence IDs

DG-102 validates one Evidence object at a time.

Therefore, this task must not implement duplicate identifier detection.

For example, the following problem:

```text
Evidence A -> evidence_id = EV-001
Evidence B -> evidence_id = EV-001
```

requires access to a collection of Evidence objects.

That validation belongs to a later incident-level or evidence-collection step.

The Evidence model itself must not use global state or external registries to detect duplicates.

---

## Validation Failures

Representative invalid cases must include:

### Missing evidence_id

```json
{
  "evidence_type": "metric",
  "source": "monitoring"
}
```

### Empty evidence_id

```json
{
  "evidence_id": "   ",
  "evidence_type": "metric",
  "source": "monitoring"
}
```

### Invalid evidence_type

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "report",
  "source": "monitoring"
}
```

### Missing source

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric"
}
```

### Empty source

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric",
  "source": "   "
}
```

### Invalid reliability

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric",
  "source": "monitoring",
  "reliability": "trusted"
}
```

### Malformed collected_at

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric",
  "source": "monitoring",
  "collected_at": "yesterday"
}
```

### Unsupported extra field

```json
{
  "evidence_id": "EV-001",
  "evidence_type": "metric",
  "source": "monitoring",
  "confidence": 0.95
}
```

---

## Required Tests

DG-102 tests should verify at minimum:

1. minimal valid Evidence can be constructed;
2. complete valid Evidence can be constructed;
3. `evidence_id` is required;
4. empty or whitespace-only `evidence_id` is rejected;
5. `source` is required;
6. empty or whitespace-only `source` is rejected;
7. valid `EvidenceType` values are accepted;
8. invalid evidence types are rejected;
9. valid `EvidenceReliability` values are accepted;
10. invalid reliability values are rejected;
11. reliability may be omitted;
12. description may be omitted;
13. value may contain representative JSON-compatible data;
14. valid datetime strings are parsed;
15. malformed datetime strings are rejected;
16. metadata defaults safely to an empty dictionary;
17. mutable metadata is not shared between Evidence instances;
18. extra top-level fields are rejected;
19. serialization uses enum string values;
20. serialization produces predictable JSON-compatible output.

Tests must remain:

- deterministic;
- offline;
- independent of LLM credentials;
- independent of network access.

---

## Scope Boundaries

DG-102 must not implement:

- evidence collection across multiple items;
- duplicate evidence-ID detection;
- evidence sufficiency calculation;
- evidence conflict detection;
- evidence scoring;
- reliability inference;
- Data Quality analysis;
- business-impact analysis;
- IncidentInput;
- AgentResponse;
- human-review rules;
- FastAPI;
- LangGraph;
- LLM providers;
- external storage;
- database integration;
- vector search.

These capabilities belong to later backlog items.

---

## Dependencies

DG-102 implementation depends on DG-101 because Evidence uses:

- `EvidenceType`;
- `EvidenceReliability`.

Therefore, DG-102 implementation should begin only after the DG-101 enum implementation is available.

The documentation contract may be prepared before DG-101 implementation.

---

## Acceptance Criteria

DG-102 is complete when:

- the `Evidence` Pydantic model exists;
- `evidence_id` is required and validated;
- `evidence_type` uses `EvidenceType`;
- `source` is required and validated;
- optional evidence fields are supported;
- reliability uses `EvidenceReliability`;
- JSON-compatible evidence values are supported;
- datetime validation works;
- extra fields are rejected;
- serialization is predictable;
- duplicate-ID detection remains deferred;
- unit tests cover valid and invalid cases;
- existing tests continue to pass;
- `python -m pip check` passes;
- `ruff check .` passes;
- `ruff format --check .` passes;
- `pytest` passes.

---

## Deferred Responsibilities

The following responsibilities are intentionally deferred.

### DG-103 — IncidentInput

- collection of Evidence objects;
- incident-level validation;
- duplicate evidence identifier validation.

### DG-201 — evidence_collector

- evidence normalization across an incident;
- evidence organization;
- duplicate detection or reporting where appropriate;
- unsupported evidence handling;
- traceability processing.

### DG-501 to DG-503 — Guardrails

- unsupported conclusions;
- insufficient evidence behavior;
- traceability validation.

DG-102 must remain a small, deterministic domain-model task.
