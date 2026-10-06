# AI Data Governance Agent — Project Charter

## 1. Project Overview

The AI Data Governance Agent is the individual Challenge project for the Alura/ONE
"Imersão de Agentes de IA para Negócios".

Official delivery deadline: 2026-11-08.

Internal code freeze: 2026-11-06.

The project demonstrates the application of AI agents to Data Engineering, Data Quality,
Data Governance, business impact analysis, evidence traceability, and human oversight.

## 2. Problem Statement

Data incidents are often investigated through fragmented technical evidence such as
pipeline reports, validation outputs, logs, data quality checks, documentation, and
business rules.

This fragmentation can make incident triage slower and can produce inconsistent
assessments of:

- incident severity;
- affected datasets;
- business impact;
- possible root causes;
- relevant governance controls;
- recommended remediation actions.

The AI Data Governance Agent will assist analysts and data engineering teams by
organizing available evidence and producing a structured incident assessment.

The agent must not replace accountable human decision-making for critical incidents.

## 3. Primary User

The primary user is a data professional responsible for investigating or reviewing
data incidents, including roles such as:

- Data Engineer;
- Analytics Engineer;
- Data Quality Analyst;
- Data Governance Analyst;
- Data Platform Engineer.

## 4. Project Objective

Build an AI-assisted incident analysis workflow capable of:

1. receiving a structured data incident;
2. analyzing available data quality signals;
3. collecting and referencing supporting evidence;
4. assessing possible business impact;
5. retrieving applicable governance policies or controls;
6. generating root-cause hypotheses;
7. recommending remediation actions;
8. estimating confidence;
9. identifying when human review is required;
10. returning a structured and traceable response.

## 5. Positioning

The project is designed to reinforce professional positioning in:

- Data Engineering;
- AI applied to business;
- Data Quality;
- Data Governance;
- DataOps;
- AI safety and human oversight.

## 6. MVP Scope

The MVP must include:

- Python 3.12 backend;
- FastAPI API;
- Pydantic input and output contracts;
- LangGraph orchestration;
- deterministic or controlled tool execution;
- FakeProvider for tests and CI;
- optional real LLM provider for controlled demonstrations;
- four initial agent tools:
  - quality_analyzer;
  - business_impact_analyzer;
  - policy_retriever;
  - evidence_collector;
- structured incident response;
- evidence traceability;
- insufficient-evidence handling;
- human-review decision;
- automated tests;
- evaluation metrics;
- GitHub Actions CI;
- simple web demonstration interface using Node.js, Express, EJS, and vanilla JavaScript.

## 7. Out of Scope Before Challenge Delivery

The following are intentionally excluded from the pre-delivery scope unless a critical
requirement emerges:

- Kubernetes;
- multi-agent architecture;
- mandatory cloud deployment;
- complex relational or NoSQL databases;
- Qdrant;
- Redis;
- Airflow inside the Challenge runtime;
- Spark inside the Challenge runtime;
- React;
- Next.js;
- autonomous remediation of production systems;
- automatic execution of destructive actions;
- complex authentication or enterprise IAM;
- unnecessary infrastructure complexity.

## 8. Initial Agent Tools

### quality_analyzer

Purpose:

Analyze data quality evidence and identify signals such as invalid records,
missing relationships, validation failures, reconciliation differences, and other
quality problems.

### business_impact_analyzer

Purpose:

Translate technical findings into potential business consequences and affected
business processes.

### policy_retriever

Purpose:

Retrieve relevant governance rules, controls, or policies that apply to the incident.

### evidence_collector

Purpose:

Collect, normalize, and reference the evidence used by the agent so that conclusions
remain traceable.

## 9. Expected Structured Output

The target response contract should contain approximately:

- incident_id;
- classification;
- severity;
- executive_summary;
- evidence;
- business_impact;
- root_cause_hypotheses;
- recommended_actions;
- governance_controls;
- confidence;
- human_review_required.

The final schema will be defined separately in the project contracts.

## 10. Human Oversight

The agent is advisory.

Human review must be required when conditions such as the following are present:

- critical or high-risk incident;
- low confidence;
- insufficient evidence;
- conflicting evidence;
- potential regulatory or governance impact;
- destructive or irreversible recommended action;
- material business impact.

The agent must not automatically execute critical remediation actions.

## 11. Evidence and Grounding Principles

The system should distinguish among:

- observed evidence;
- deterministic tool results;
- model-generated hypotheses;
- recommendations.

The agent should not present unsupported hypotheses as verified facts.

When available evidence is insufficient, the system should explicitly communicate that
limitation rather than invent supporting information.

## 12. Reference Repositories

Existing repositories may provide patterns, examples, or test cases but will remain
independent projects.

### aws-lakehouse-engineering-lab

Primary source of Data Quality and incident scenarios, especially DE-101 and DE-102.

### databricks-lakehouse-data-engineering-lab

Reference for Data Engineering and lakehouse architecture patterns.

### agente-ia-manuais-rh-rag

Reference for FastAPI, guardrails, source traceability, and insufficient-evidence
responses.

### edudocs-ai-agent-oci

Reference for LangGraph, FakeProvider, automated evaluation, metrics, and safety.

### growth_equestre_hackathon_2026

Reference for Node.js, EJS, and demonstration-oriented user experience.

These repositories must not be transformed into the Challenge repository.

## 13. Evaluation Metrics

Initial evaluation metrics:

- schema_valid_rate;
- severity_accuracy;
- evidence_traceability_rate;
- unsupported_rejection_rate;
- human_review_accuracy;
- tool_execution_success_rate;
- response_latency;
- test_pass_rate.

Exact calculation rules and evaluation datasets will be defined in
`docs/evaluation/`.

## 14. Development Principles

Development should follow this loop:

1. plan the change;
2. define the acceptance criteria;
3. create a small implementation task;
4. implement;
5. run pytest;
6. run Ruff;
7. review the result;
8. commit;
9. proceed to the next task.

Codex tasks must be classified as:

- LIGHT;
- MEDIUM;
- HIGH.

Whenever possible, Codex work should remain LIGHT or MEDIUM with narrowly defined
scope.

## 15. Definition of MVP Success

The MVP will be considered successful when:

- a valid incident can be submitted to the system;
- the workflow invokes the required analysis tools;
- the result conforms to the response schema;
- supporting evidence is traceable;
- unsupported conclusions are rejected or qualified;
- critical situations trigger human review;
- deterministic test scenarios run without a real LLM;
- automated tests pass;
- Ruff passes;
- CI passes;
- at least one representative Data Quality incident can be demonstrated end to end;
- the project can be explained clearly as a business-oriented AI governance solution.

## 16. Delivery Principle

The Challenge will prioritize a reliable, explainable, testable, and demonstrable
system over architectural complexity.

Professional quality will be demonstrated through disciplined engineering decisions,
not through the number of technologies used.
