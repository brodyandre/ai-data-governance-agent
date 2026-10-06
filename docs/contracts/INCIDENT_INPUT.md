# Incident Input Contract

## Purpose

This document defines the conceptual input contract for incidents submitted to the AI Data Governance Agent.

This contract will later be implemented with Pydantic.

## Required Fields

### incident_id

Unique identifier for the incident.

Example:

`DE-101`

### title

Short human-readable description of the incident.

Example:

`Silver layer record divergence`

### description

Detailed description of the observed problem.

### source_system

System, pipeline, dataset, or platform where the incident originated.

### detected_at

Timestamp or date when the incident was detected.

### evidence

Collection of available technical or business evidence associated with the incident.

At least one evidence item should be provided whenever possible.

## Optional Fields

### affected_datasets

Datasets known or suspected to be affected.

### reported_by

Person, role, system, or automated process that reported the incident.

### business_context

Business process or analytical context related to the incident.

### expected_behavior

Expected data or pipeline behavior.

### observed_behavior

Behavior actually observed during the incident.

### initial_severity

Optional severity initially assigned by the source system or analyst.

### tags

Optional classification tags.

## Evidence Item

Each evidence item should conceptually contain:

- evidence_id;
- evidence_type;
- source;
- description;
- value or content;
- collected_at;
- reliability;
- metadata.

## Evidence Types

Initial evidence types may include:

- data_quality_check;
- pipeline_report;
- validation_result;
- reconciliation_result;
- log;
- business_rule;
- governance_policy;
- analyst_observation;
- metric;
- dataset_sample.

## Input Validation Principles

The final implementation should reject or flag:

- missing incident_id;
- missing title;
- missing description;
- malformed timestamps;
- invalid severity values;
- duplicated evidence identifiers;
- unsupported evidence structures.

## Insufficient Evidence

An incident may be accepted even when evidence is incomplete.

However, insufficient evidence must influence:

- confidence;
- recommendations;
- root-cause hypotheses;
- human_review_required.

The system must not fabricate missing evidence.

## Example

```json
{
  "incident_id": "DE-101",
  "title": "Silver layer record divergence",
  "description": "Record counts between raw and silver layers do not reconcile.",
  "source_system": "lakehouse-pipeline",
  "detected_at": "2026-10-05T20:00:00Z",
  "affected_datasets": [
    "orders",
    "order_items"
  ],
  "business_context": "Sales analytics pipeline",
  "expected_behavior": "Valid raw records should be represented in the silver layer.",
  "observed_behavior": "Some records were rejected during data quality validation.",
  "evidence": [
    {
      "evidence_id": "EV-001",
      "evidence_type": "reconciliation_result",
      "source": "pipeline-report",
      "description": "Raw and silver record counts differ.",
      "value": "orders RAW=400 SILVER=388",
      "reliability": "high"
    }
  ]
}
```