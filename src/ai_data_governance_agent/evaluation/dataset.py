"""Deterministic evaluation scenarios used by the project."""

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ai_data_governance_agent.domain.enums import (
    HypothesisStatus,
    IncidentClassification,
    Severity,
)
from ai_data_governance_agent.domain.incident import IncidentInput
from ai_data_governance_agent.workflow import (
    HypothesisGenerationResult,
    RecommendationGenerationResult,
)


class EvaluationExpectedOutcome(BaseModel):
    """Represent deterministic expectations for one evaluation scenario."""

    model_config = ConfigDict(extra="forbid")

    classification: IncidentClassification
    severity: Severity
    human_review_required: bool
    unsupported_claim_rejection_expected: bool = False
    final_hypothesis_statuses: list[HypothesisStatus] = Field(default_factory=list)


class EvaluationScenario(BaseModel):
    """Represent one reproducible evaluation case."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str
    title: str
    description: str
    source_reference: str | None = None
    incident: IncidentInput
    hypothesis_response: HypothesisGenerationResult
    recommendation_response: RecommendationGenerationResult | None
    expected: EvaluationExpectedOutcome
    tags: list[str] = Field(default_factory=list)

    @field_validator(
        "scenario_id",
        "title",
        "description",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        """Reject blank dataset metadata."""
        normalized = value.strip()

        if not normalized:
            raise ValueError("value must contain non-whitespace characters")

        return normalized


def _incident(
    *,
    incident_id: str,
    title: str,
    description: str,
    source_system: str,
    evidence: list[dict[str, object]],
    affected_datasets: list[str] | None = None,
    business_context: str | None = None,
    initial_severity: str | None = None,
    tags: list[str] | None = None,
) -> IncidentInput:
    """Build one validated incident fixture."""
    return IncidentInput.model_validate(
        {
            "incident_id": incident_id,
            "title": title,
            "description": description,
            "source_system": source_system,
            "detected_at": datetime(
                2026,
                10,
                6,
                12,
                0,
                tzinfo=UTC,
            ),
            "evidence": evidence,
            "affected_datasets": affected_datasets or [],
            "business_context": business_context,
            "initial_severity": initial_severity,
            "tags": tags or [],
        }
    )


def _hypothesis_response(
    *,
    classification: str,
    severity: str,
    executive_summary: str,
    confidence: float,
    hypotheses: list[dict[str, object]],
) -> HypothesisGenerationResult:
    """Build one validated deterministic provider response."""
    return HypothesisGenerationResult.model_validate(
        {
            "classification": classification,
            "severity": severity,
            "executive_summary": executive_summary,
            "confidence": confidence,
            "root_cause_hypotheses": hypotheses,
        }
    )


def _recommendation_response(
    recommendations: list[dict[str, object]],
) -> RecommendationGenerationResult:
    """Build one validated deterministic recommendation fixture."""
    return RecommendationGenerationResult.model_validate(
        {
            "recommended_actions": recommendations,
        }
    )


_DATASET: tuple[EvaluationScenario, ...] = (
    EvaluationScenario(
        scenario_id="de_101_raw_silver_divergence",
        title="DE-101 raw-to-silver data-quality divergence",
        description=(
            "Scenario inspired by the DE-101 investigation involving "
            "invalid items, missing relationships and record-count divergence."
        ),
        source_reference=("brodyandre/aws-lakehouse-engineering-lab:DE-101"),
        incident=_incident(
            incident_id="EVAL-DE-101",
            title="Raw-to-silver divergence in sales pipeline",
            description=(
                "Orders and order items show data-quality losses "
                "between raw, silver and gold processing stages."
            ),
            source_system="aws-lakehouse-engineering-lab",
            affected_datasets=[
                "orders",
                "order_items",
                "fct_sales",
            ],
            business_context=(
                "Sales analytics depend on records surviving quality and relationship validation."
            ),
            initial_severity="high",
            tags=[
                "de-101",
                "data-quality",
                "reconciliation",
            ],
            evidence=[
                {
                    "evidence_id": "EV-DE101-QUALITY",
                    "evidence_type": "data_quality_check",
                    "source": "bronze-to-silver-analysis",
                    "description": (
                        "Invalid quantities and missing relationships "
                        "were identified in order items."
                    ),
                    "value": {
                        "invalid_rows": 30,
                        "missing_relationships": 33,
                    },
                    "reliability": "high",
                },
                {
                    "evidence_id": "EV-DE101-RECON",
                    "evidence_type": "reconciliation_result",
                    "source": "pipeline-reconciliation",
                    "description": ("Order-item counts diverge between raw and silver."),
                    "value": {
                        "raw_count": 1000,
                        "silver_count": 970,
                    },
                    "reliability": "high",
                },
                {
                    "evidence_id": "EV-DE101-IMPACT",
                    "evidence_type": "analyst_observation",
                    "source": "incident-analysis",
                    "description": (
                        "The quality issue affects records used to construct the sales fact table."
                    ),
                    "value": {
                        "business_impact": {
                            "status": "confirmed",
                            "description": ("Sales fact-table completeness is affected."),
                            "affected_processes": ["sales analytics"],
                            "affected_consumers": ["analytics users"],
                            "materiality": "high",
                        }
                    },
                    "reliability": "high",
                },
            ],
        ),
        hypothesis_response=_hypothesis_response(
            classification="data_quality",
            severity="high",
            executive_summary=(
                "Data-quality validation is removing invalid "
                "and relationally inconsistent order-item records."
            ),
            confidence=0.92,
            hypotheses=[
                {
                    "description": (
                        "Invalid quantities and relationship failures "
                        "explain the observed raw-to-silver divergence."
                    ),
                    "supporting_evidence": [
                        "EV-DE101-QUALITY",
                        "EV-DE101-RECON",
                    ],
                    "confidence": 0.90,
                    "status": "probable",
                }
            ],
        ),
        recommendation_response=_recommendation_response(
            [
                {
                    "description": (
                        "Review rejected order items and reconcile "
                        "relationship and quantity validation failures."
                    ),
                    "priority": "high",
                    "rationale": ("The evidence identifies invalid rows and count divergence."),
                    "requires_human_approval": False,
                    "supporting_evidence": [
                        "EV-DE101-QUALITY",
                        "EV-DE101-RECON",
                    ],
                }
            ]
        ),
        expected=EvaluationExpectedOutcome(
            classification="data_quality",
            severity="high",
            human_review_required=True,
            final_hypothesis_statuses=["probable"],
        ),
        tags=[
            "de-101",
            "data-quality",
            "reconciliation",
        ],
    ),
    EvaluationScenario(
        scenario_id="de_102_revenue_semantics",
        title="DE-102 revenue semantic ambiguity",
        description=(
            "Scenario inspired by DE-102 where Gold and Analytics "
            "reconcile mathematically but the business definition "
            "of revenue eligibility is not explicit."
        ),
        source_reference=(
            "brodyandre/aws-lakehouse-engineering-lab:"
            "docs/incidents/de-102-analytics-revenue-status.md"
        ),
        incident=_incident(
            incident_id="EVAL-DE-102",
            title="Revenue metric has ambiguous status eligibility",
            description=(
                "Analytics includes all valid order statuses in revenue, "
                "while the business contract for recognized revenue "
                "has not been formally defined."
            ),
            source_system="aws-lakehouse-engineering-lab",
            affected_datasets=[
                "gold.fct_sales",
                "analytics.revenue_by_month",
            ],
            business_context=(
                "Financial reporting requires an explicit semantic "
                "definition of revenue eligibility."
            ),
            initial_severity="high",
            tags=[
                "de-102",
                "governance",
                "semantic-contract",
            ],
            evidence=[
                {
                    "evidence_id": "EV-DE102-METRIC",
                    "evidence_type": "metric",
                    "source": "de-102-investigation",
                    "description": (
                        "Gold and Analytics reconcile, but an investigative "
                        "paid-plus-shipped scenario produces a materially "
                        "different revenue value."
                    ),
                    "value": {
                        "analytics_revenue": 1416127.23,
                        "gold_revenue": 1416127.23,
                        "paid_shipped_revenue": 548323.22,
                        "investigative_difference": 867804.01,
                    },
                    "reliability": "high",
                },
                {
                    "evidence_id": "EV-DE102-RULE",
                    "evidence_type": "business_rule",
                    "source": "de-102-investigation",
                    "description": (
                        "No explicit business rule defines which "
                        "order statuses are eligible for revenue."
                    ),
                    "value": {
                        "business_impact": {
                            "status": "potential",
                            "description": (
                                "Financial metrics may be interpreted "
                                "inconsistently until revenue semantics "
                                "are formally defined."
                            ),
                            "affected_processes": ["financial analytics"],
                            "affected_consumers": ["business stakeholders"],
                            "materiality": "high",
                        }
                    },
                    "reliability": "high",
                },
            ],
        ),
        hypothesis_response=_hypothesis_response(
            classification="governance",
            severity="high",
            executive_summary=(
                "No technical reconciliation defect is established; "
                "the risk is an undefined semantic contract for revenue."
            ),
            confidence=0.88,
            hypotheses=[
                {
                    "description": (
                        "The incident is driven by an undefined "
                        "business definition of revenue eligibility."
                    ),
                    "supporting_evidence": [
                        "EV-DE102-METRIC",
                        "EV-DE102-RULE",
                    ],
                    "confidence": 0.87,
                    "status": "probable",
                }
            ],
        ),
        recommendation_response=_recommendation_response(
            [
                {
                    "description": (
                        "Obtain formal business approval for revenue "
                        "eligibility rules before changing Analytics SQL."
                    ),
                    "priority": "high",
                    "rationale": (
                        "The current implementation reconciles correctly, "
                        "but the semantic contract is undefined."
                    ),
                    "requires_human_approval": True,
                    "supporting_evidence": [
                        "EV-DE102-METRIC",
                        "EV-DE102-RULE",
                    ],
                }
            ]
        ),
        expected=EvaluationExpectedOutcome(
            classification="governance",
            severity="high",
            human_review_required=True,
            final_hypothesis_statuses=["probable"],
        ),
        tags=[
            "de-102",
            "governance",
            "semantic-contract",
        ],
    ),
    EvaluationScenario(
        scenario_id="insufficient_evidence",
        title="Incident with insufficient evidence",
        description=(
            "Valid incident input with no available evidence "
            "and an adversarial unsupported provider claim."
        ),
        incident=_incident(
            incident_id="EVAL-INSUFFICIENT",
            title="Incident without supporting evidence",
            description=("An anomaly was reported but no evidence has yet been collected."),
            source_system="orders-lakehouse",
            evidence=[],
            tags=["insufficient-evidence"],
        ),
        hypothesis_response=_hypothesis_response(
            classification="unknown",
            severity="medium",
            executive_summary=("The upstream process caused the incident."),
            confidence=0.95,
            hypotheses=[
                {
                    "description": ("The upstream process caused the incident."),
                    "supporting_evidence": ["EV-FAKE"],
                    "confidence": 0.95,
                    "status": "confirmed",
                }
            ],
        ),
        recommendation_response=None,
        expected=EvaluationExpectedOutcome(
            classification="unknown",
            severity="medium",
            human_review_required=True,
            unsupported_claim_rejection_expected=True,
            final_hypothesis_statuses=[],
        ),
        tags=[
            "insufficient-evidence",
            "guardrail",
        ],
    ),
    EvaluationScenario(
        scenario_id="conflicting_evidence",
        title="Incident with conflicting evidence",
        description=(
            "Two evidence sources report incompatible record counts, "
            "requiring conservative analysis."
        ),
        incident=_incident(
            incident_id="EVAL-CONFLICT",
            title="Conflicting reconciliation evidence",
            description=("Two validated reports disagree on the number of processed records."),
            source_system="customer-lakehouse",
            evidence=[
                {
                    "evidence_id": "EV-CONFLICT-A",
                    "evidence_type": "metric",
                    "source": "pipeline-report-a",
                    "description": ("First report indicates 970 processed records."),
                    "value": {"processed_records": 970},
                    "reliability": "medium",
                },
                {
                    "evidence_id": "EV-CONFLICT-B",
                    "evidence_type": "metric",
                    "source": "pipeline-report-b",
                    "description": ("Second report indicates 1000 processed records."),
                    "value": {"processed_records": 1000},
                    "reliability": "medium",
                },
            ],
            tags=["conflicting-evidence"],
        ),
        hypothesis_response=_hypothesis_response(
            classification="reconciliation",
            severity="medium",
            executive_summary=("Available reports conflict and require reconciliation."),
            confidence=0.60,
            hypotheses=[
                {
                    "description": (
                        "The reports may represent different pipeline execution boundaries."
                    ),
                    "supporting_evidence": [
                        "EV-CONFLICT-A",
                        "EV-CONFLICT-B",
                    ],
                    "confidence": 0.60,
                    "status": "probable",
                }
            ],
        ),
        recommendation_response=_recommendation_response(
            [
                {
                    "description": (
                        "Reconcile report scope and execution timestamps "
                        "before selecting a canonical record count."
                    ),
                    "priority": "medium",
                    "rationale": ("The available evidence contains incompatible counts."),
                    "requires_human_approval": False,
                    "supporting_evidence": [
                        "EV-CONFLICT-A",
                        "EV-CONFLICT-B",
                    ],
                }
            ]
        ),
        expected=EvaluationExpectedOutcome(
            classification="reconciliation",
            severity="medium",
            human_review_required=True,
            final_hypothesis_statuses=["probable"],
        ),
        tags=[
            "conflicting-evidence",
            "reconciliation",
        ],
    ),
    EvaluationScenario(
        scenario_id="low_severity_incident",
        title="Low-severity freshness incident",
        description=(
            "Small freshness delay with strong evidence and no identified material business impact."
        ),
        incident=_incident(
            incident_id="EVAL-LOW",
            title="Minor dataset freshness delay",
            description=(
                "A non-critical analytical dataset arrived five minutes later than expected."
            ),
            source_system="marketing-lakehouse",
            evidence=[
                {
                    "evidence_id": "EV-LOW-001",
                    "evidence_type": "metric",
                    "source": "freshness-monitor",
                    "description": ("Observed freshness delay is five minutes."),
                    "value": {"delay_minutes": 5},
                    "reliability": "high",
                }
            ],
            initial_severity="low",
            tags=[
                "low-severity",
                "freshness",
            ],
        ),
        hypothesis_response=_hypothesis_response(
            classification="freshness",
            severity="low",
            executive_summary=("A small freshness delay was detected without material impact."),
            confidence=0.93,
            hypotheses=[
                {
                    "description": ("A short scheduling delay caused the freshness deviation."),
                    "supporting_evidence": ["EV-LOW-001"],
                    "confidence": 0.90,
                    "status": "probable",
                }
            ],
        ),
        recommendation_response=_recommendation_response(
            [
                {
                    "description": ("Monitor the next scheduled execution."),
                    "priority": "low",
                    "rationale": ("The delay is small and supported by the freshness metric."),
                    "requires_human_approval": False,
                    "supporting_evidence": ["EV-LOW-001"],
                }
            ]
        ),
        expected=EvaluationExpectedOutcome(
            classification="freshness",
            severity="low",
            human_review_required=False,
            final_hypothesis_statuses=["probable"],
        ),
        tags=[
            "low-severity",
            "freshness",
        ],
    ),
    EvaluationScenario(
        scenario_id="critical_incident",
        title="Critical pipeline failure",
        description=("Critical pipeline failure affecting a business-critical data delivery."),
        incident=_incident(
            incident_id="EVAL-CRITICAL",
            title="Critical sales pipeline failure",
            description=(
                "The sales pipeline failed before publishing the required analytical dataset."
            ),
            source_system="sales-lakehouse",
            evidence=[
                {
                    "evidence_id": "EV-CRIT-001",
                    "evidence_type": "pipeline_report",
                    "source": "pipeline-orchestrator",
                    "description": ("Pipeline execution terminated with failed tasks."),
                    "value": {
                        "pipeline_status": "failed",
                        "failed_tasks": 4,
                    },
                    "reliability": "high",
                }
            ],
            initial_severity="critical",
            tags=[
                "critical",
                "pipeline-failure",
            ],
        ),
        hypothesis_response=_hypothesis_response(
            classification="pipeline_failure",
            severity="critical",
            executive_summary=(
                "The analytical delivery is blocked by a critical pipeline failure."
            ),
            confidence=0.95,
            hypotheses=[
                {
                    "description": (
                        "The failed orchestration tasks caused the analytical delivery failure."
                    ),
                    "supporting_evidence": ["EV-CRIT-001"],
                    "confidence": 0.94,
                    "status": "confirmed",
                }
            ],
        ),
        recommendation_response=_recommendation_response(
            [
                {
                    "description": (
                        "Investigate the failed tasks and prepare a controlled pipeline recovery."
                    ),
                    "priority": "urgent",
                    "rationale": ("The pipeline report confirms execution failure."),
                    "requires_human_approval": True,
                    "supporting_evidence": ["EV-CRIT-001"],
                }
            ]
        ),
        expected=EvaluationExpectedOutcome(
            classification="pipeline_failure",
            severity="critical",
            human_review_required=True,
            final_hypothesis_statuses=["confirmed"],
        ),
        tags=[
            "critical",
            "pipeline-failure",
        ],
    ),
    EvaluationScenario(
        scenario_id="unsupported_claim",
        title="Attempted unsupported root-cause claim",
        description=(
            "Provider attempts to promote a probable hypothesis "
            "without declaring supporting evidence."
        ),
        incident=_incident(
            incident_id="EVAL-UNSUPPORTED",
            title="Validation failures require investigation",
            description=(
                "Validation failures were detected, but the proposed "
                "root cause is not supported by the evidence."
            ),
            source_system="customer-lakehouse",
            evidence=[
                {
                    "evidence_id": "EV-UNSUP-001",
                    "evidence_type": "validation_result",
                    "source": "validation-report",
                    "description": ("Eight validation failures were detected."),
                    "value": {"validation_failures": 8},
                    "reliability": "high",
                }
            ],
            tags=[
                "unsupported-claim",
                "guardrail",
            ],
        ),
        hypothesis_response=_hypothesis_response(
            classification="data_quality",
            severity="medium",
            executive_summary=("Validation failures require root-cause investigation."),
            confidence=0.88,
            hypotheses=[
                {
                    "description": ("A deployment introduced the validation failures."),
                    "supporting_evidence": [],
                    "confidence": 0.86,
                    "status": "probable",
                }
            ],
        ),
        recommendation_response=_recommendation_response(
            [
                {
                    "description": (
                        "Inspect the failed validations before "
                        "attributing the incident to a deployment."
                    ),
                    "priority": "medium",
                    "rationale": (
                        "The available evidence confirms validation "
                        "failures but not their root cause."
                    ),
                    "requires_human_approval": False,
                    "supporting_evidence": ["EV-UNSUP-001"],
                }
            ]
        ),
        expected=EvaluationExpectedOutcome(
            classification="data_quality",
            severity="medium",
            human_review_required=False,
            unsupported_claim_rejection_expected=True,
            final_hypothesis_statuses=["suspected"],
        ),
        tags=[
            "unsupported-claim",
            "guardrail",
        ],
    ),
)


def load_evaluation_dataset() -> list[EvaluationScenario]:
    """Return independent copies of all deterministic evaluation scenarios."""
    return [scenario.model_copy(deep=True) for scenario in _DATASET]


__all__ = [
    "EvaluationExpectedOutcome",
    "EvaluationScenario",
    "load_evaluation_dataset",
]
