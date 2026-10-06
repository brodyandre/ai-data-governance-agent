# Domain Enum Contract

## Purpose

This document defines the normalized enumerated values used by the AI Data Governance Agent domain models.

These values are intended to provide stable contracts across:

- Pydantic models;
- deterministic tools;
- LangGraph state;
- API requests and responses;
- evaluation fixtures;
- tests;
- the web demonstration interface.

The implementation is tracked by backlog item `DG-101`.

## General Rules

All domain enums defined by DG-101 must follow these rules:

- Python enum classes use PascalCase names;
- Python enum members use uppercase names;
- serialized values use lowercase `snake_case`;
- enum values are case-sensitive;
- aliases are not accepted;
- unsupported values must be rejected;
- automatic normalization of unsupported input is not allowed;
- serialized values must remain stable once exposed through the API.

The planned Python implementation should use `StrEnum`, available in Python 3.12.

Example:

```python
class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
```

The serialized representation of:

```python
Severity.HIGH
```

must be:

```json
"high"
```

---

## Severity

Python class:

`Severity`

Purpose:

Represent the normalized severity assigned to an incident.

Values:

| Python member | Serialized value |
| --- | --- |
| `LOW` | `low` |
| `MEDIUM` | `medium` |
| `HIGH` | `high` |
| `CRITICAL` | `critical` |

The semantic interpretation of severity is defined in:

`docs/contracts/SEVERITY_AND_HUMAN_REVIEW.md`

Severity ordering from lowest to highest is conceptually:

`low < medium < high < critical`

DG-101 does not need to implement comparison operators or automatic severity escalation.

Those behaviors should be implemented only when required by later domain rules.

---

## IncidentClassification

Python class:

`IncidentClassification`

Purpose:

Represent the primary classification assigned to an incident.

Values:

| Python member | Serialized value |
| --- | --- |
| `DATA_QUALITY` | `data_quality` |
| `SCHEMA` | `schema` |
| `INTEGRITY` | `integrity` |
| `RECONCILIATION` | `reconciliation` |
| `FRESHNESS` | `freshness` |
| `PIPELINE_FAILURE` | `pipeline_failure` |
| `GOVERNANCE` | `governance` |
| `UNKNOWN` | `unknown` |

`UNKNOWN` is a valid explicit domain value.

It should be used when available evidence does not support a more specific classification.

The implementation must not silently convert an unsupported classification into `UNKNOWN`.

For example:

```text
"security_problem"
```

must be rejected rather than automatically mapped to:

```text
"unknown"
```

---

## EvidenceType

Python class:

`EvidenceType`

Purpose:

Represent the type of evidence associated with an incident.

Values:

| Python member | Serialized value |
| --- | --- |
| `DATA_QUALITY_CHECK` | `data_quality_check` |
| `PIPELINE_REPORT` | `pipeline_report` |
| `VALIDATION_RESULT` | `validation_result` |
| `RECONCILIATION_RESULT` | `reconciliation_result` |
| `LOG` | `log` |
| `BUSINESS_RULE` | `business_rule` |
| `GOVERNANCE_POLICY` | `governance_policy` |
| `ANALYST_OBSERVATION` | `analyst_observation` |
| `METRIC` | `metric` |
| `DATASET_SAMPLE` | `dataset_sample` |

These values originate from the initial Incident Input contract.

Additional evidence types should not be introduced unless a concrete project requirement appears.

Unsupported evidence types must fail validation.

---

## EvidenceReliability

Python class:

`EvidenceReliability`

Purpose:

Represent the assessed reliability of an evidence item.

Values:

| Python member | Serialized value |
| --- | --- |
| `LOW` | `low` |
| `MEDIUM` | `medium` |
| `HIGH` | `high` |

The initial conceptual Incident Input contract mentions evidence reliability but does not define a complete value set.

For the Challenge MVP, the project standardizes reliability to:

`low`, `medium`, and `high`.

An `UNKNOWN` enum member is intentionally not included.

When reliability is not available, the future Evidence model may represent the field as absent or `None`.

This distinction prevents:

- missing reliability information;

from being confused with:

- an explicit reliability classification.

---

## BusinessImpactStatus

Python class:

`BusinessImpactStatus`

Purpose:

Distinguish whether business impact is confirmed, potential, or unknown.

Values:

| Python member | Serialized value |
| --- | --- |
| `CONFIRMED` | `confirmed` |
| `POTENTIAL` | `potential` |
| `UNKNOWN` | `unknown` |

Meaning:

### confirmed

Available evidence supports that the business consequence has occurred.

### potential

Available evidence supports a credible risk or possible consequence, but the consequence has not been confirmed.

### unknown

Available evidence is insufficient to determine business impact.

The implementation must preserve the distinction between these three states.

---

## ActionPriority

Python class:

`ActionPriority`

Purpose:

Represent the priority of an advisory recommended action.

Values:

| Python member | Serialized value |
| --- | --- |
| `LOW` | `low` |
| `MEDIUM` | `medium` |
| `HIGH` | `high` |
| `URGENT` | `urgent` |

Priority does not authorize execution.

A recommendation with priority `urgent` remains advisory and may still require accountable human approval.

---

## Validation Rules

Valid values must be accepted exactly as defined.

Examples of valid values:

```text
high
data_quality
reconciliation_result
potential
urgent
```

Examples of invalid values:

```text
HIGH
Data_Quality
data-quality
very_high
critical_incident
trusted
```

The system must reject invalid values rather than silently changing them.

For the Challenge MVP, no alias mapping is required.

Examples of unsupported aliases:

```text
med
sev1
dq
pipeline
reconcile
```

These values must not be automatically translated to valid enum values.

---

## Serialization Rules

Domain enum values must serialize using their defined string value.

Examples:

```json
{
  "severity": "high",
  "classification": "data_quality",
  "business_impact_status": "potential",
  "action_priority": "urgent"
}
```

API consumers must not receive Python enum member names such as:

```text
Severity.HIGH
IncidentClassification.DATA_QUALITY
ActionPriority.URGENT
```

---

## Implementation Location

Planned source structure:

```text
src/
└── ai_data_governance_agent/
    └── domain/
        ├── __init__.py
        └── enums.py
```

Planned test structure:

```text
tests/
└── domain/
    └── test_enums.py
```

DG-101 should not introduce:

- Pydantic IncidentInput models;
- Evidence models;
- AgentResponse models;
- human-review business rules;
- LangGraph;
- FastAPI;
- LLM providers;
- deterministic analysis tools.

Those capabilities belong to later backlog items.

---

## Required Tests

DG-101 tests should verify at minimum:

1. every documented enum member exists;
2. every member has the expected serialized string value;
3. valid string values can construct their enum;
4. unsupported values raise validation errors;
5. incorrect casing is rejected;
6. no undocumented aliases are accepted.

Representative valid tests should include:

```python
Severity("high") == Severity.HIGH
IncidentClassification("data_quality") == IncidentClassification.DATA_QUALITY
EvidenceType("reconciliation_result") == EvidenceType.RECONCILIATION_RESULT
EvidenceReliability("high") == EvidenceReliability.HIGH
BusinessImpactStatus("potential") == BusinessImpactStatus.POTENTIAL
ActionPriority("urgent") == ActionPriority.URGENT
```

Representative invalid inputs should include:

```text
HIGH
very_high
Data_Quality
data-quality
trusted
immediate
```

---

## Acceptance Criteria

DG-101 is complete when:

- all six required enums are implemented;
- values match this contract exactly;
- invalid values are rejected;
- valid values serialize predictably;
- unit tests cover valid and invalid cases;
- no unrelated domain models are introduced;
- `python -m pip check` passes;
- `ruff check .` passes;
- `ruff format --check .` passes;
- `pytest` passes.

---

## Deferred Domain Values

The Agent Response contract also introduces hypothesis statuses:

- suspected;
- probable;
- confirmed;
- rejected.

These values are intentionally deferred to `DG-104 — AgentResponse models`.

They are not part of DG-101.

This keeps the implementation aligned with the approved backlog and prevents unnecessary scope expansion.
