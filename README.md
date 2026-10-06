# AI Data Governance Agent

AI-assisted analysis of data incidents focused on Data Quality, business impact,
governance, evidence traceability, and human oversight.

This repository is being developed as the individual Challenge project for the
Alura/ONE "Imersão de Agentes de IA para Negócios".

## Project Status

Current phase: Phase 0 — Planning and Bootstrap.

Official Challenge deadline: 2026-11-08.

Internal code freeze: 2026-11-06.

The agent implementation has not started yet.

## Problem

Data incidents are frequently investigated using fragmented technical evidence such as
pipeline reports, validation results, reconciliation differences, logs, Data Quality
checks, business rules, and governance policies.

This fragmentation can make incident triage slower and can lead to inconsistent
assessments of severity, business impact, root cause, and remediation priority.

The AI Data Governance Agent will assist data professionals by organizing evidence and
producing a structured and traceable incident assessment.

The system is advisory and does not replace accountable human decision-making for
critical situations.

## Main Objectives

The project demonstrates the intersection of:

- Data Engineering;
- Artificial Intelligence;
- Data Quality;
- Data Governance;
- DataOps;
- AI safety;
- human-in-the-loop decision-making.

## Planned Agent Tools

The initial MVP will contain four tools:

- quality_analyzer;
- business_impact_analyzer;
- policy_retriever;
- evidence_collector.

## Planned Structured Response

The agent response is expected to contain:

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

Final contracts will be defined before implementation.

## Human Oversight

Human review must be considered for situations including:

- critical or high-risk incidents;
- low confidence;
- insufficient evidence;
- conflicting evidence;
- material business impact;
- governance or regulatory concerns;
- destructive or irreversible recommended actions.

The agent will not automatically execute critical remediation actions.

## Evidence Principles

The solution must distinguish between:

- observed evidence;
- deterministic tool results;
- AI-generated hypotheses;
- recommendations.

Unsupported hypotheses must not be presented as verified facts.

When evidence is insufficient, the system must explicitly report that limitation.

## Technology Stack

Backend:

- Python 3.12;
- FastAPI;
- Pydantic;
- LangGraph.

Quality and testing:

- pytest;
- pytest-cov;
- Ruff;
- GitHub Actions.

AI provider strategy:

- FakeProvider for tests and CI;
- real LLM provider only for controlled tests and demonstrations.

Web interface:

- Node.js;
- Express;
- EJS;
- Vanilla JavaScript.

Streamlit remains a fallback option.

## Scope Constraints

Before Challenge delivery, the project intentionally avoids:

- Kubernetes;
- multi-agent architecture;
- mandatory cloud infrastructure;
- complex databases;
- Qdrant;
- Redis;
- Airflow in the Challenge runtime;
- Spark in the Challenge runtime;
- React;
- Next.js;
- autonomous critical remediation.

## Project Structure

The current project contains:

- docs/ — project documentation, contracts, ADRs, and evaluation definitions;
- src/ — Python application package;
- tests/ — automated tests;
- web/ — future Node.js demonstration interface;
- pyproject.toml — project dependencies and tool configuration.

## Local Development

Create the virtual environment:

    python3.12 -m venv .venv

Activate it:

    source .venv/bin/activate

Install the project:

    python -m pip install -e ".[dev]"

Validate dependencies:

    python -m pip check

Run lint:

    ruff check .

Validate formatting:

    ruff format --check .

Run tests:

    pytest

## Current Quality Gates

The project currently requires:

- pip check: PASS;
- Ruff lint: PASS;
- Ruff format: PASS;
- pytest: PASS.

## Evaluation

Initial planned metrics include:

- schema_valid_rate;
- severity_accuracy;
- evidence_traceability_rate;
- unsupported_rejection_rate;
- human_review_accuracy;
- tool_execution_success_rate;
- response_latency;
- test_pass_rate.

Detailed definitions will be maintained under docs/evaluation/.

## Reference Projects

The project may use patterns and scenarios from independent repositories including:

- aws-lakehouse-engineering-lab;
- databricks-lakehouse-data-engineering-lab;
- agente-ia-manuais-rh-rag;
- edudocs-ai-agent-oci;
- growth_equestre_hackathon_2026.

These repositories remain independent and will not be converted into this Challenge.

## Development Workflow

Development follows this sequence:

Plan -> acceptance criteria -> scoped task -> implementation -> pytest/Ruff -> review
-> commit -> next task.

Codex tasks will always be classified as:

- LIGHT;
- MEDIUM;
- HIGH.

LIGHT and MEDIUM tasks will be preferred whenever possible.

## Documentation

Core project documents:

- docs/PROJECT_CHARTER.md
- docs/ROADMAP.md
- docs/adrs/ADR-001-project-scope-and-stack.md

Additional contracts, evaluation definitions, and ADRs will be added incrementally.

## Delivery

Official Challenge delivery: 2026-11-08.

Internal code freeze: 2026-11-06.

The period after the internal freeze is reserved for validation, documentation review,
repository cleanup, demonstration preparation, and final submission.
