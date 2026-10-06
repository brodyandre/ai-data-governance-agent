"""Tests for the deterministic evaluation dataset."""

from ai_data_governance_agent.evaluation import (
    load_evaluation_dataset,
)

EXPECTED_SCENARIO_IDS = {
    "de_101_raw_silver_divergence",
    "de_102_revenue_semantics",
    "insufficient_evidence",
    "conflicting_evidence",
    "low_severity_incident",
    "critical_incident",
    "unsupported_claim",
}


def scenario_by_id(scenario_id: str):
    """Return one evaluation scenario by identifier."""
    scenarios = {scenario.scenario_id: scenario for scenario in load_evaluation_dataset()}

    return scenarios[scenario_id]


def test_dataset_contains_all_required_initial_scenarios() -> None:
    scenarios = load_evaluation_dataset()

    assert len(scenarios) == 7

    assert {scenario.scenario_id for scenario in scenarios} == EXPECTED_SCENARIO_IDS


def test_scenario_and_incident_ids_are_unique() -> None:
    scenarios = load_evaluation_dataset()

    scenario_ids = [scenario.scenario_id for scenario in scenarios]
    incident_ids = [scenario.incident.incident_id for scenario in scenarios]

    assert len(scenario_ids) == len(set(scenario_ids))
    assert len(incident_ids) == len(set(incident_ids))


def test_expected_labels_match_provider_classification_and_severity() -> None:
    for scenario in load_evaluation_dataset():
        assert scenario.hypothesis_response.classification == scenario.expected.classification
        assert scenario.hypothesis_response.severity == scenario.expected.severity


def test_de_101_preserves_known_quality_divergence() -> None:
    scenario = scenario_by_id("de_101_raw_silver_divergence")

    evidence = {item.evidence_id: item for item in scenario.incident.evidence}

    assert evidence["EV-DE101-QUALITY"].value["invalid_rows"] == 30

    assert evidence["EV-DE101-RECON"].value["raw_count"] == 1000

    assert evidence["EV-DE101-RECON"].value["silver_count"] == 970


def test_de_102_preserves_semantic_uncertainty() -> None:
    scenario = scenario_by_id("de_102_revenue_semantics")

    evidence = {item.evidence_id: item for item in scenario.incident.evidence}

    metric = evidence["EV-DE102-METRIC"].value

    assert metric["analytics_revenue"] == 1416127.23
    assert metric["gold_revenue"] == 1416127.23
    assert metric["investigative_difference"] == 867804.01

    assert scenario.expected.classification == "governance"


def test_insufficient_evidence_scenario_contains_no_evidence() -> None:
    scenario = scenario_by_id("insufficient_evidence")

    assert scenario.incident.evidence == []
    assert scenario.recommendation_response is None
    assert scenario.expected.human_review_required is True


def test_conflicting_evidence_scenario_has_distinct_sources() -> None:
    scenario = scenario_by_id("conflicting_evidence")

    sources = {evidence.source for evidence in scenario.incident.evidence}

    assert sources == {
        "pipeline-report-a",
        "pipeline-report-b",
    }


def test_low_and_critical_scenarios_cover_severity_boundaries() -> None:
    low = scenario_by_id("low_severity_incident")
    critical = scenario_by_id("critical_incident")

    assert low.expected.severity == "low"
    assert low.expected.human_review_required is False

    assert critical.expected.severity == "critical"
    assert critical.expected.human_review_required is True


def test_unsupported_claim_scenario_requires_guardrail_rejection() -> None:
    scenario = scenario_by_id("unsupported_claim")

    hypothesis = scenario.hypothesis_response.root_cause_hypotheses[0]

    assert hypothesis.status == "probable"
    assert hypothesis.supporting_evidence == []

    assert scenario.expected.unsupported_claim_rejection_expected is True

    assert scenario.expected.final_hypothesis_statuses == ["suspected"]


def test_dataset_loader_returns_independent_objects() -> None:
    first = load_evaluation_dataset()
    second = load_evaluation_dataset()

    first[0].title = "Changed locally"

    assert first[0] is not second[0]
    assert second[0].title != "Changed locally"
