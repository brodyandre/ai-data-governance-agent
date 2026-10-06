# AI Data Governance Agent — Roadmap

## Delivery Dates

- Official Challenge deadline: 2026-11-08
- Internal code freeze: 2026-11-06

The internal freeze leaves time for final validation, documentation review, repository
cleanup, screenshots, presentation preparation, and submission.

---

## Phase 0 — Planning and Bootstrap

Goal:

Create a reproducible project foundation and freeze the initial product scope before
agent implementation.

Deliverables:

- repository structure;
- Python 3.12 virtual environment;
- pyproject.toml;
- pytest;
- Ruff;
- initial CI configuration;
- Project Charter;
- project roadmap;
- initial architecture decision records;
- initial README;
- backlog;
- initial contracts.

Status:

IN PROGRESS

---

## Phase 1 — Domain Contracts and Incident Model

Goal:

Define the domain before implementing orchestration.

Expected deliverables:

- IncidentInput model;
- Evidence model;
- severity model;
- classification model;
- BusinessImpact model;
- GovernanceControl model;
- RecommendedAction model;
- AgentResponse model;
- confidence representation;
- human-review rules;
- example incident fixtures;
- schema validation tests.

No real LLM integration is required in this phase.

---

## Phase 2 — Deterministic Analysis Tools

Goal:

Implement the first deterministic capabilities independently of LangGraph.

Initial tools:

- quality_analyzer;
- business_impact_analyzer;
- policy_retriever;
- evidence_collector.

Requirements:

- explicit inputs and outputs;
- unit tests;
- predictable failure behavior;
- evidence traceability;
- no dependency on a real LLM for CI.

---

## Phase 3 — Provider Abstraction

Goal:

Separate model-dependent behavior from business logic.

Expected deliverables:

- provider protocol or interface;
- FakeProvider;
- deterministic test behavior;
- controlled real-provider adapter;
- configuration through environment variables;
- safe handling of missing credentials.

CI must continue to run without external LLM credentials.

---

## Phase 4 — LangGraph Workflow

Goal:

Orchestrate incident analysis using LangGraph.

Expected high-level flow:

1. validate incident;
2. collect evidence;
3. analyze data quality;
4. analyze business impact;
5. retrieve governance controls;
6. produce or refine hypotheses;
7. generate recommendations;
8. calculate or assign confidence;
9. determine human-review requirement;
10. validate final response.

The first version must remain a single-agent workflow.

---

## Phase 5 — Guardrails and Governance

Goal:

Make the agent safer, traceable, and explicit about uncertainty.

Expected deliverables:

- insufficient-evidence behavior;
- unsupported-claim rejection;
- critical-decision human review;
- evidence references;
- confidence rules;
- structured failure responses;
- clear separation between facts and hypotheses.

---

## Phase 6 — FastAPI Application

Goal:

Expose the workflow through a stable HTTP contract.

Expected deliverables:

- health endpoint;
- incident-analysis endpoint;
- request validation;
- structured response;
- error handling;
- API tests;
- OpenAPI documentation.

---

## Phase 7 — Evaluation Framework

Goal:

Measure behavior objectively.

Initial metrics:

- schema_valid_rate;
- severity_accuracy;
- evidence_traceability_rate;
- unsupported_rejection_rate;
- human_review_accuracy;
- tool_execution_success_rate;
- response_latency;
- test_pass_rate.

Expected deliverables:

- evaluation fixtures;
- evaluation runner;
- expected outcomes;
- generated summary report.

---

## Phase 8 — Web Demonstration Interface

Goal:

Provide a professional demonstration experience without introducing unnecessary
frontend complexity.

Primary stack:

- Node.js;
- Express;
- EJS;
- vanilla JavaScript.

Expected capabilities:

- enter or load an incident;
- submit analysis;
- display severity and classification;
- display executive summary;
- show evidence;
- show business impact;
- show root-cause hypotheses;
- show recommended actions;
- show governance controls;
- show confidence;
- highlight human-review requirement.

Streamlit remains a fallback only.

---

## Phase 9 — Representative Incident Scenarios

Goal:

Demonstrate the agent with realistic Data Engineering incidents.

Initial sources:

- DE-101 patterns from aws-lakehouse-engineering-lab;
- DE-102 patterns from aws-lakehouse-engineering-lab;
- synthetic incidents specifically created for Challenge evaluation.

Existing repositories remain unchanged.

---

## Phase 10 — Final Hardening

Goal:

Prepare the repository for code freeze.

Activities:

- full pytest execution;
- Ruff validation;
- CI verification;
- dependency review;
- documentation review;
- removal of dead code;
- removal of temporary files;
- secret scanning review;
- reproducibility check;
- clean-environment installation test;
- final demonstration rehearsal.

Target completion:

2026-11-06.

---

## Phase 11 — Submission Preparation

Period:

2026-11-07 to 2026-11-08.

Activities:

- final README review;
- screenshots or demo evidence;
- presentation narrative;
- repository visibility validation;
- links validation;
- final Challenge submission.

No substantial feature development should occur during this phase.

---

## Scope Control Rule

A feature should enter the pre-delivery roadmap only if it materially improves at least
one of the following:

- Challenge requirements;
- demonstrability;
- reliability;
- governance;
- evidence traceability;
- evaluation quality;
- professional portfolio value.

Otherwise, it should be deferred.
