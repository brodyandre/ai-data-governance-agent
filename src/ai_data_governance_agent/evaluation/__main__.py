"""Run the deterministic evaluation suite from the command line."""

from ai_data_governance_agent.evaluation.metrics import (
    evaluate_dataset,
)


def main() -> None:
    """Execute the evaluation and print its JSON report."""
    report = evaluate_dataset()

    print(
        report.model_dump_json(
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
