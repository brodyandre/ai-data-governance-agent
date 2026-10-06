# Agent Response Contract

## Purpose

This document defines the conceptual structured response produced by the AI Data Governance Agent.

The final implementation will use Pydantic to enforce this contract.

## Fields

### incident_id

Identifier of the analyzed incident.

The value must correspond to the incident received in the input contract.

### classification

Primary classification assigned to the incident.

Initial values may include:

- data_quality;
- schema;
- integrity;
- reconciliation;
- freshness;
- pipeline_failure;
- governance;
- unknown.

The classification must be based on available evidence.

### severity

Normalized severity assigned by the analysis.

Initial values:

- low;
- medium;
- high;
- critical.

Severity rules are defined separately in `SEVERITY_AND_HUMAN_REVIEW.md`.

### executive_summary

Concise explanation of the incident.

The summary should communicate:

- what happened;
- why it matters;
- the current level of risk;
- whether human review is required.

### evidence

Evidence used to support the analysis.

Every important conclusion should be traceable to one or more evidence items whenever possible.

Evidence references should use the same identifiers defined in the incident input.

### business_impact

Structured description of confirmed or potential business consequences.

The business impact should distinguish among:

- confirmed impact;
- potential impact;
- unknown impact.

Suggested conceptual fields:

- status;
- description;
- affected_processes;
- affected_consumers;
- materiality;
- supporting_evidence.

### root_cause_hypotheses

Possible explanations for the incident.

Each hypothesis should conceptually contain:

- description;
- supporting_evidence;
- confidence;
- status.

Initial hypothesis statuses may include:

- suspected;
- probable;
- confirmed;
- rejected.

A hypothesis must not be represented as confirmed unless supporting evidence justifies that status.

### recommended_actions

Recommended next steps.

Each action should conceptually contain:

- description;
- priority;
- rationale;
- requires_human_approval;
- supporting_evidence.

Initial priorities may include:

- low;
- medium;
- high;
- urgent.

Recommendations must remain advisory.

### governance_controls

Relevant governance rules, controls, or policies associated with the incident.

Each control should conceptually contain:

- control_id;
- title;
- description;
- source;
- relevance;
- supporting_evidence.

### confidence

Confidence in the overall assessment.

The initial implementation is expected to use a numeric value between:

`0.0` and `1.0`

where:

- `0.0` represents no meaningful confidence;
- `1.0` represents maximum confidence supported by the available evidence.

Confidence must reflect evidence quality and uncertainty.

### human_review_required

Boolean indicating whether accountable human review is required.

Possible values:

- true;
- false.

The decision must follow explicit governance rules rather than arbitrary model behavior.

### human_review_reasons

List of reasons explaining why human review was required.

Examples:

- high severity;
- critical severity;
- insufficient evidence;
- conflicting evidence;
- low confidence;
- possible governance exposure;
- material business impact;
- destructive recommendation.

## Response Principles

A valid response must:

- conform to the defined schema;
- preserve the original incident_id;
- distinguish facts from hypotheses;
- reference supporting evidence;
- expose uncertainty;
- avoid unsupported claims;
- explicitly identify insufficient evidence;
- indicate human review when appropriate.

## Evidence Traceability

Important conclusions should reference the evidence that supports them.

The response should make it possible to answer:

- What evidence supports this conclusion?
- Which source produced the evidence?
- Is the conclusion observed, derived, or hypothetical?

A conclusion without sufficient support must be qualified or rejected.

## Insufficient Evidence Behavior

When evidence is insufficient, the response must not fabricate information.

The agent should instead:

- reduce confidence;
- identify missing information;
- qualify root-cause hypotheses;
- avoid unsupported conclusions;
- recommend additional investigation;
- require human review when appropriate.

## Human Oversight

The response is advisory.

The agent must not imply that a recommendation has already been executed.

Critical or irreversible actions require accountable human approval.

## Example

```json
{
  "incident_id": "DE-101",
  "classification": "data_quality",
  "severity": "high",
  "executive_summary": "Data Quality validation removed records from the silver layer and may affect downstream sales analytics.",
  "evidence": [
    {
      "evidence_id": "EV-001",
      "source": "pipeline-report"
    }
  ],
  "business_impact": {
    "status": "potential",
    "description": "Downstream sales metrics may be incomplete.",
    "affected_processes": [
      "sales analytics"
    ],
    "materiality": "medium",
    "supporting_evidence": [
      "EV-001"
    ]
  },
  "root_cause_hypotheses": [
    {
      "description": "Invalid item quantities caused records to fail validation.",
      "supporting_evidence": [
        "EV-001"
      ],
      "confidence": 0.95,
      "status": "probable"
    }
  ],
  "recommended_actions": [
    {
      "description": "Review rejected records and validate upstream quantity rules.",
      "priority": "high",
      "rationale": "Rejected records may be causing incomplete downstream analytics.",
      "requires_human_approval": false,
      "supporting_evidence": [
        "EV-001"
      ]
    }
  ],
  "governance_controls": [],
  "confidence": 0.90,
  "human_review_required": true,
  "human_review_reasons": [
    "high severity",
    "potential material business impact"
  ]
}
```