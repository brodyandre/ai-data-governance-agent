# Severity and Human Review Rules

## Purpose

This document defines the initial conceptual rules used to classify incident severity and determine when accountable human review is required.

These rules will later be converted into deterministic application logic and automated tests.

## Severity Levels

### LOW

Typical characteristics:

- limited technical impact;
- no known material business impact;
- no critical dataset affected;
- no governance or regulatory concern;
- straightforward remediation;
- high-quality supporting evidence.

A low-severity incident should normally be recoverable without urgent intervention.

### MEDIUM

Typical characteristics:

- measurable Data Quality degradation;
- limited downstream impact;
- recoverable pipeline or data issue;
- no evidence of major governance or regulatory exposure;
- affected users or processes remain operational;
- remediation is important but not urgent.

Medium severity indicates that the incident deserves attention but does not currently represent material operational risk.

### HIGH

Typical characteristics:

- material downstream impact;
- important analytical or operational dataset affected;
- significant record loss, corruption, or inconsistency;
- multiple consumers or systems affected;
- important business metrics may be incorrect;
- urgent remediation is required;
- evidence may be incomplete or conflicting.

A high-severity incident should normally receive human review.

### CRITICAL

Typical characteristics:

- severe business interruption;
- major data integrity failure;
- critical production process affected;
- regulatory, privacy, compliance, or governance exposure;
- irreversible or destructive consequence is possible;
- executive or operational decisions may rely on materially incorrect data;
- immediate human intervention is required.

Critical incidents always require human review.

## Severity Assessment Principles

Severity should not be determined from a single signal whenever multiple forms of evidence are available.

The assessment should consider:

- technical impact;
- business impact;
- number of affected datasets;
- number of affected consumers;
- duration;
- recoverability;
- integrity risk;
- governance risk;
- regulatory risk;
- evidence quality;
- uncertainty.

## Severity Escalation

The system should prefer the higher severity when reliable evidence indicates multiple severity levels.

Examples:

- technical impact is medium but material business impact is high -> severity may be high;
- technical impact is high and governance exposure is critical -> severity should be critical;
- evidence is insufficient to distinguish high from critical -> human review must be required.

## Human Review

`human_review_required` indicates whether an accountable person must review the incident assessment or recommended actions.

Human review is a governance control and must not depend solely on arbitrary LLM judgment.

## Mandatory Human Review Rules

`human_review_required` must be `true` when one or more of the following conditions apply:

- severity is critical;
- severity is high and business impact is material;
- confidence is below the accepted threshold;
- evidence is insufficient;
- evidence is conflicting;
- potential regulatory exposure exists;
- potential governance violation exists;
- potential privacy impact exists;
- recommended action is destructive;
- recommended action is irreversible;
- root cause remains highly uncertain;
- the system cannot determine a safe recommendation;
- a critical business process is affected.

## Initial Confidence Threshold

The initial planned confidence threshold is:

`confidence < 0.70`

When overall confidence is below this threshold, human review must be required.

This threshold is provisional and must be validated during the evaluation phase.

## Confidence Interpretation

Initial conceptual interpretation:

- 0.90 to 1.00: very high confidence;
- 0.80 to 0.89: high confidence;
- 0.70 to 0.79: moderate confidence;
- 0.50 to 0.69: low confidence;
- below 0.50: very low confidence.

Confidence is not a substitute for severity.

A critical incident with high confidence still requires human review.

## Insufficient Evidence

Evidence should be considered insufficient when the system cannot support an important conclusion with available sources.

Possible examples:

- no evidence is provided;
- evidence does not relate to the reported incident;
- required reconciliation information is missing;
- business impact cannot be assessed;
- root-cause hypotheses lack supporting evidence.

Insufficient evidence should normally result in:

- reduced confidence;
- qualified conclusions;
- requests or recommendations for additional investigation;
- human_review_required = true.

## Conflicting Evidence

Evidence is conflicting when reliable sources support incompatible conclusions.

The system must not silently choose one version without qualification.

When conflicting evidence materially affects the analysis:

- confidence should decrease;
- the conflict should be exposed in the response;
- human review should be required.

## Material Business Impact

Material business impact may include:

- inaccurate financial or revenue reporting;
- significant customer impact;
- operational interruption;
- incorrect executive reporting;
- regulatory reporting risk;
- material decision-making based on incorrect data;
- significant downstream analytical corruption.

The exact materiality criteria may evolve during evaluation.

## Governance Exposure

Potential governance exposure includes situations such as:

- violation of defined Data Quality controls;
- unauthorized data access;
- unapproved data transformation;
- policy non-compliance;
- lineage or traceability failure;
- sensitive data handling concerns;
- missing required approvals.

Potential governance exposure should increase the need for human oversight.

## Destructive or Irreversible Actions

The agent must never autonomously execute destructive or irreversible actions.

Examples include:

- deleting production data;
- overwriting production datasets;
- modifying access permissions;
- disabling governance controls;
- changing retention rules;
- bypassing approval processes;
- forcing production rollback;
- applying irreversible remediation.

The agent may recommend such actions, but accountable human approval is mandatory.

## Conservative Decision Principle

When the system is uncertain between requiring and not requiring human review, the preferred decision for the Challenge MVP is:

`human_review_required = true`

This conservative rule prioritizes safety, governance, and explainability.

## Deterministic Governance Principle

Where possible, human-review decisions should be made using explicit deterministic rules.

The LLM may provide supporting analysis, but critical governance decisions should remain auditable and reproducible.

## Example Decision Cases

### Case 1 — Low Severity

Conditions:

- low technical impact;
- no material business impact;
- confidence = 0.95;
- complete evidence;
- no governance exposure.

Expected:

`human_review_required = false`

### Case 2 — Low Confidence

Conditions:

- medium severity;
- confidence = 0.60;
- incomplete evidence.

Expected:

`human_review_required = true`

Reason:

Low confidence and insufficient evidence.

### Case 3 — High Business Impact

Conditions:

- high severity;
- material business impact;
- confidence = 0.88.

Expected:

`human_review_required = true`

Reason:

High severity with material business impact.

### Case 4 — Critical Incident

Conditions:

- critical severity;
- confidence = 0.97;
- strong evidence.

Expected:

`human_review_required = true`

Reason:

Critical incidents always require accountable human review.

### Case 5 — Destructive Recommendation

Conditions:

- medium severity;
- confidence = 0.92;
- recommendation involves deletion of production data.

Expected:

`human_review_required = true`

Reason:

Destructive or irreversible actions require human approval.
