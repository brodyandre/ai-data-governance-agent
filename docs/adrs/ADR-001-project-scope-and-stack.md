# ADR-001 — Project Scope and Technology Stack

## Status

Accepted

## Date

2026-10-05

## Context

The AI Data Governance Agent is being developed as an individual Challenge project for
the Alura/ONE "Imersão de Agentes de IA para Negócios".

The project has a fixed delivery deadline and must balance:

- business relevance;
- AI agent capabilities;
- Data Engineering relevance;
- governance and safety;
- demonstrability;
- automated testing;
- limited development time;
- limited Codex availability.

A broad technology stack could increase apparent sophistication but would also increase
implementation risk and reduce the time available for evaluation, documentation, and
demonstration quality.

## Decision

The project will use the following primary stack:

### Backend

- Python 3.12;
- FastAPI;
- Pydantic;
- LangGraph.

### Development Quality

- pytest;
- pytest-cov;
- Ruff;
- GitHub Actions.

### AI Provider Strategy

- FakeProvider for automated tests and CI;
- real LLM provider only for controlled testing and demonstrations.

### Web Interface

Primary approach:

- Node.js;
- Express;
- EJS;
- vanilla JavaScript.

Fallback:

- Streamlit.

### Initial Agent Tools

- quality_analyzer;
- business_impact_analyzer;
- policy_retriever;
- evidence_collector.

## Architectural Constraints

Before Challenge delivery, the project will intentionally avoid:

- Kubernetes;
- multi-agent architecture;
- mandatory cloud infrastructure;
- complex databases;
- Qdrant;
- Redis;
- Airflow in the runtime;
- Spark in the runtime;
- React;
- Next.js;
- autonomous critical remediation.

## Rationale

Python provides the strongest fit for the agent, evaluation, validation, and Data
Engineering components.

FastAPI provides a lightweight typed API layer and integrates naturally with Pydantic.

Pydantic provides explicit contracts and structured validation for inputs, tool outputs,
and final responses.

LangGraph provides explicit workflow orchestration while allowing the solution to remain
a single-agent architecture.

FakeProvider separates deterministic engineering tests from external model availability,
cost, credentials, latency, and nondeterminism.

Node.js with Express and EJS provides sufficient flexibility for a professional
demonstration interface without introducing the additional complexity of a SPA
framework.

## Consequences

Positive consequences:

- reduced delivery risk;
- simpler local development;
- deterministic CI;
- easier automated testing;
- explicit domain contracts;
- lower infrastructure cost;
- better explainability;
- easier demonstration;
- stronger alignment with Data Engineering and governance positioning.

Trade-offs:

- the project will not demonstrate distributed infrastructure;
- the project will not demonstrate a multi-agent architecture;
- the web interface will favor simplicity over frontend sophistication;
- production-grade enterprise scalability is outside the Challenge scope.

These trade-offs are accepted because they do not materially reduce the value of the
Challenge demonstration.

## Revisit Conditions

This decision should be revisited only if:

- the official Challenge requirements demand another technology;
- a selected component creates a blocking compatibility issue;
- a simpler option materially improves delivery reliability;
- a missing capability prevents a required demonstration.

Architectural expansion alone is not sufficient reason to revise this ADR.
