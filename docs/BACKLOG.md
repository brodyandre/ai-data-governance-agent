# AI Data Governance Agent — Development Backlog

## Purpose

This backlog defines the planned implementation sequence for the AI Data Governance Agent.

The backlog is designed to keep development incremental, testable, and aligned with the Challenge deadline.

Official delivery deadline: 2026-11-08.

Internal code freeze: 2026-11-06.

## Priority Levels

- P0 — required for the Challenge MVP;
- P1 — important for professional quality and demonstration;
- P2 — valuable improvement if time allows;
- P3 — post-Challenge or optional enhancement.

## Codex Complexity

Every implementation task must be classified before being sent to Codex.

Allowed classifications:

- LIGHT;
- MEDIUM;
- HIGH.

LIGHT and MEDIUM tasks should be preferred.

HIGH tasks should be decomposed whenever possible.

---

# Phase 0 — Planning and Bootstrap

## DG-001 — Repository bootstrap

Priority: P0

Codex: NOT REQUIRED

Status: DONE

Scope:

- create repository directory;
- initialize Git;
- create Python 3.12 virtual environment;
- configure src layout;
- configure pytest;
- configure Ruff;
- install project dependencies.

Acceptance criteria:

- Python 3.12 environment works;
- editable installation succeeds;
- `pip check` passes;
- Ruff passes;
- pytest passes.

---

## DG-002 — Project Charter

Priority: P0

Codex: NOT REQUIRED

Status: DONE

Scope:

Define:

- project problem;
- target users;
- project objectives;
- MVP;
- non-goals;
- human oversight;
- evidence principles;
- evaluation metrics.

Acceptance criteria:

- `docs/PROJECT_CHARTER.md` exists;
- scope is explicit;
- non-scope is explicit;
- MVP success criteria are documented.

---

## DG-003 — Project Roadmap

Priority: P0

Codex: NOT REQUIRED

Status: DONE

Acceptance criteria:

- implementation phases are documented;
- code freeze is documented;
- final delivery period is documented.

---

## DG-004 — Initial Architecture Decision

Priority: P0

Codex: NOT REQUIRED

Status: DONE

Deliverable:

`docs/adrs/ADR-001-project-scope-and-stack.md`

Acceptance criteria:

- primary stack is recorded;
- rejected complexity is documented;
- architectural rationale is explicit.

---

## DG-005 — Domain contracts

Priority: P0

Codex: NOT REQUIRED

Status: DONE

Deliverables:

- `docs/contracts/INCIDENT_INPUT.md`;
- `docs/contracts/AGENT_RESPONSE.md`;
- `docs/contracts/SEVERITY_AND_HUMAN_REVIEW.md`.

Acceptance criteria:

- conceptual input contract is defined;
- conceptual output contract is defined;
- severity levels are defined;
- human-review triggers are defined;
- evidence traceability principles are explicit.

---

## DG-006 — GitHub Actions bootstrap

Priority: P0

Codex classification: LIGHT

Status: TODO

Scope:

Create CI workflow for:

- Python 3.12;
- project installation;
- dependency validation;
- Ruff lint;
- Ruff formatting validation;
- pytest.

Acceptance criteria:

- workflow runs on push;
- workflow runs on pull request;
- CI requires no LLM credentials;
- CI passes on main.

---

## DG-007 — Initial repository publication

Priority: P0

Codex: NOT REQUIRED

Status: TODO

Scope:

- create GitHub repository;
- first commit;
- push main;
- verify CI;
- verify README rendering.

Acceptance criteria:

- repository is available on GitHub;
- working tree is clean;
- main branch is synchronized;
- CI passes.

---

# Phase 1 — Domain Models

## DG-101 — Severity and classification enums

Priority: P0

Codex classification: LIGHT

Status: TODO

Scope:

Implement normalized domain values for:

- severity;
- incident classification;
- evidence type;
- evidence reliability;
- business-impact status;
- action priority.

Acceptance criteria:

- invalid enum values are rejected;
- unit tests cover valid and invalid values;
- Ruff and pytest pass.

---

## DG-102 — Evidence model

Priority: P0

Codex classification: LIGHT

Status: TODO

Scope:

Implement the Pydantic model for incident evidence.

Acceptance criteria:

- evidence_id is required;
- evidence_type is validated;
- source is required;
- duplicated evidence identifiers can later be detected at incident level;
- serialization works;
- tests pass.

---

## DG-103 — IncidentInput model

Priority: P0

Codex classification: MEDIUM

Status: TODO

Scope:

Convert `INCIDENT_INPUT.md` into Pydantic models.

Acceptance criteria:

- required fields are enforced;
- optional fields are supported;
- timestamps are validated;
- evidence is structured;
- malformed requests fail predictably;
- tests cover valid and invalid incidents.

---

## DG-104 — AgentResponse models

Priority: P0

Codex classification: MEDIUM

Status: TODO

Scope:

Implement structured models for:

- BusinessImpact;
- RootCauseHypothesis;
- RecommendedAction;
- GovernanceControl;
- AgentResponse.

Acceptance criteria:

- confidence is constrained to the accepted interval;
- severity is normalized;
- human_review_required is boolean;
- response serialization is deterministic;
- tests pass.

---

## DG-105 — Deterministic human-review rules

Priority: P0

Codex classification: MEDIUM

Status: TODO

Scope:

Implement rules defined in `SEVERITY_AND_HUMAN_REVIEW.md`.

Acceptance criteria:

- critical incidents always require review;
- confidence below 0.70 requires review;
- insufficient evidence requires review;
- conflicting evidence requires review;
- destructive actions require review;
- governance exposure requires review;
- rules are covered by unit tests.

---

# Phase 2 — Deterministic Tools

## DG-201 — evidence_collector

Priority: P0

Codex classification: MEDIUM

Status: TODO

Purpose:

Normalize and organize evidence provided with an incident.

Acceptance criteria:

- evidence identifiers remain traceable;
- duplicated identifiers are detected;
- unsupported evidence is handled explicitly;
- output is deterministic;
- unit tests pass.

---

## DG-202 — quality_analyzer

Priority: P0

Codex classification: MEDIUM

Status: TODO

Purpose:

Analyze deterministic Data Quality signals.

Initial supported patterns may include:

- invalid records;
- reconciliation differences;
- missing relationships;
- validation failures;
- record-count divergence.

Acceptance criteria:

- findings reference evidence;
- deterministic fixtures produce predictable output;
- unsupported conclusions are not generated;
- tests pass.

---

## DG-203 — business_impact_analyzer

Priority: P0

Codex classification: MEDIUM

Status: TODO

Purpose:

Map technical incident findings to possible business consequences.

Acceptance criteria:

- confirmed and potential impact are distinguished;
- supporting evidence is referenced;
- unknown impact remains representable;
- deterministic tests pass.

---

## DG-204 — policy_retriever

Priority: P0

Codex classification: MEDIUM

Status: TODO

Purpose:

Retrieve governance controls applicable to an incident.

Initial implementation should remain lightweight.

Acceptance criteria:

- policies are locally available;
- retrieval is deterministic for CI;
- retrieved controls contain source references;
- no vector database is required.

---

# Phase 3 — Provider Abstraction

## DG-301 — Provider interface

Priority: P0

Codex classification: LIGHT

Status: TODO

Scope:

Define a model-provider abstraction independent of any specific LLM vendor.

Acceptance criteria:

- application logic does not depend directly on a real provider;
- provider can return structured output;
- interface is documented.

---

## DG-302 — FakeProvider

Priority: P0

Codex classification: MEDIUM

Status: TODO

Purpose:

Provide deterministic model behavior for:

- unit tests;
- integration tests;
- CI;
- offline development.

Acceptance criteria:

- requires no credentials;
- requires no network;
- produces repeatable responses;
- supports error simulation;
- tests pass.

---

## DG-303 — Controlled real LLM provider

Priority: P1

Codex classification: MEDIUM

Status: TODO

Acceptance criteria:

- configuration uses environment variables;
- missing credentials fail safely;
- no secrets are committed;
- real provider is optional;
- CI remains independent of it.

---

# Phase 4 — Agent Workflow

## DG-401 — LangGraph state

Priority: P0

Codex classification: MEDIUM

Status: TODO

Scope:

Define workflow state based on approved domain contracts.

Acceptance criteria:

- incident state is explicit;
- evidence state is explicit;
- tool results are explicit;
- errors can be represented;
- final response can be constructed from state.

---

## DG-402 — LangGraph nodes

Priority: P0

Codex classification: MEDIUM

Status: TODO

Initial nodes:

- validate incident;
- collect evidence;
- analyze quality;
- analyze business impact;
- retrieve policies;
- generate hypotheses;
- generate recommendations;
- determine human review;
- construct final response.

Acceptance criteria:

- node responsibilities remain narrow;
- nodes are independently testable where practical;
- failures are represented predictably.

---

## DG-403 — LangGraph orchestration

Priority: P0

Codex classification: MEDIUM

Status: TODO

Acceptance criteria:

- single-agent graph compiles;
- deterministic FakeProvider execution succeeds;
- tools execute in expected sequence;
- final AgentResponse is valid;
- integration tests pass.

---

# Phase 5 — Guardrails

## DG-501 — Unsupported claim guardrail

Priority: P0

Codex classification: MEDIUM

Status: TODO

Acceptance criteria:

- unsupported conclusions are rejected or qualified;
- hypotheses cannot silently become confirmed facts;
- tests contain unsupported-evidence scenarios.

---

## DG-502 — Insufficient evidence behavior

Priority: P0

Codex classification: MEDIUM

Status: TODO

Acceptance criteria:

- low-evidence incidents are accepted when structurally valid;
- confidence is reduced;
- missing evidence is communicated;
- human review is triggered when required;
- fabricated evidence is prohibited.

---

## DG-503 — Evidence traceability validation

Priority: P0

Codex classification: MEDIUM

Status: TODO

Acceptance criteria:

- important conclusions can reference evidence IDs;
- invalid evidence references are detected;
- traceability can be measured.

---

# Phase 6 — FastAPI

## DG-601 — FastAPI application bootstrap

Priority: P0

Codex classification: LIGHT

Status: TODO

Acceptance criteria:

- application starts;
- `/health` responds successfully;
- API configuration is minimal;
- test client validates health endpoint.

---

## DG-602 — Incident analysis endpoint

Priority: P0

Codex classification: MEDIUM

Status: TODO

Expected endpoint:

`POST /api/v1/incidents/analyze`

Acceptance criteria:

- accepts IncidentInput;
- invokes agent workflow;
- returns AgentResponse;
- invalid requests return appropriate status;
- API tests pass.

---

## DG-603 — API error handling

Priority: P1

Codex classification: MEDIUM

Status: TODO

Acceptance criteria:

- validation errors are structured;
- internal failures do not expose sensitive details;
- provider failures are handled safely;
- error tests pass.

---

# Phase 7 — Evaluation

## DG-701 — Evaluation dataset

Priority: P0

Codex classification: MEDIUM

Status: TODO

Initial scenarios:

- DE-101-inspired incident;
- DE-102-inspired incident;
- insufficient-evidence incident;
- conflicting-evidence incident;
- low-severity incident;
- critical incident;
- unsupported-claim scenario.

Existing source repositories must remain unchanged.

---

## DG-702 — Evaluation metrics

Priority: P0

Codex classification: MEDIUM

Status: TODO

Metrics:

- schema_valid_rate;
- severity_accuracy;
- evidence_traceability_rate;
- unsupported_rejection_rate;
- human_review_accuracy;
- tool_execution_success_rate;
- response_latency;
- test_pass_rate.

Acceptance criteria:

- metric definitions are explicit;
- each metric is reproducible;
- deterministic evaluation works with FakeProvider.

---

## DG-703 — Evaluation report

Priority: P1

Codex classification: MEDIUM

Status: TODO

Acceptance criteria:

- evaluation command generates summary output;
- metrics are understandable;
- results can be used in README or Challenge presentation.

---

# Phase 8 — Web Interface

## DG-801 — Node.js application bootstrap

Priority: P1

Codex classification: LIGHT

Status: TODO

Stack:

- Node.js;
- Express;
- EJS;
- Vanilla JavaScript.

Acceptance criteria:

- application starts locally;
- configuration is simple;
- no React or Next.js is introduced.

---

## DG-802 — Incident input screen

Priority: P1

Codex classification: MEDIUM

Status: TODO

Acceptance criteria:

- user can enter or load an incident;
- interface validates essential fields;
- sample incident can be loaded easily.

---

## DG-803 — Analysis result screen

Priority: P1

Codex classification: MEDIUM

Status: TODO

Display:

- classification;
- severity;
- executive summary;
- evidence;
- business impact;
- hypotheses;
- actions;
- governance controls;
- confidence;
- human-review requirement.

---

## DG-804 — Demonstration polish

Priority: P2

Codex classification: LIGHT

Status: TODO

Scope:

- visual hierarchy;
- severity indication;
- human-review warning;
- readable evidence cards;
- loading state;
- error state.

---

# Phase 9 — Challenge Demonstration

## DG-901 — DE-101 scenario

Priority: P0

Codex classification: MEDIUM

Status: TODO

Purpose:

Create a representative incident based on Data Quality patterns previously investigated in the `aws-lakehouse-engineering-lab`.

Existing repository must remain unchanged.

---

## DG-902 — DE-102 scenario

Priority: P1

Codex classification: MEDIUM

Status: TODO

Purpose:

Create a second representative incident scenario to demonstrate generalization.

---

## DG-903 — Demo narrative

Priority: P0

Codex: NOT REQUIRED

Status: TODO

Narrative should explain:

1. business problem;
2. incident submitted;
3. evidence collected;
4. tools used;
5. AI reasoning boundaries;
6. governance controls;
7. human review;
8. measurable evaluation results;
9. business value.

---

# Phase 10 — Hardening

## DG-1001 — Full quality gate

Priority: P0

Codex classification: LIGHT

Status: TODO

Required checks:

- pip check;
- Ruff lint;
- Ruff formatting;
- full pytest;
- CI;
- clean environment installation.

---

## DG-1002 — Security and secret review

Priority: P0

Codex classification: LIGHT

Status: TODO

Acceptance criteria:

- no API keys committed;
- `.env` ignored;
- example environment documented safely;
- provider credentials optional.

---

## DG-1003 — Documentation review

Priority: P0

Codex classification: LIGHT

Status: TODO

Acceptance criteria:

- README reflects implemented architecture;
- setup instructions work from a clean environment;
- diagrams match implementation;
- evaluation results are current;
- known limitations are documented.

---

## DG-1004 — Code freeze

Priority: P0

Codex: NOT REQUIRED

Target:

2026-11-06

After code freeze:

- no unnecessary features;
- only blocking fixes;
- final validation;
- demonstration rehearsal;
- submission preparation.

---

# Deferred / Post-Challenge

The following items should remain deferred unless Challenge requirements change:

- Kubernetes;
- multi-agent architecture;
- Redis;
- Qdrant;
- Airflow runtime integration;
- Spark runtime integration;
- React;
- Next.js;
- complex authentication;
- enterprise IAM;
- mandatory cloud deployment;
- autonomous remediation;
- production scalability work.

## Backlog Rule

A new item should be added to the pre-delivery backlog only when it materially improves:

- Challenge compliance;
- reliability;
- explainability;
- governance;
- evidence traceability;
- evaluation;
- demonstration quality;
- professional portfolio value.

Otherwise, it should be deferred.