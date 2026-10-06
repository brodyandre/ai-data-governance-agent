"""Run the deterministic evaluation suite from the command line."""

import argparse
from pathlib import Path
from typing import Literal

from ai_data_governance_agent.evaluation.metrics import (
    evaluate_dataset,
)
from ai_data_governance_agent.evaluation.reporting import (
    render_markdown,
    render_summary,
)

type OutputFormat = Literal[
    "summary",
    "json",
    "markdown",
]


def main(
    argv: list[str] | None = None,
) -> None:
    """Execute the evaluation and render the requested report."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    report = evaluate_dataset()

    output = _render_output(
        report,
        output_format=args.format,
    )

    if args.output is None:
        print(output)
        return

    output_path = Path(args.output)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        output + "\n",
        encoding="utf-8",
    )

    print(f"Evaluation report written to {output_path}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=("Run deterministic evaluation for the AI Data Governance Agent.")
    )

    parser.add_argument(
        "--format",
        choices=(
            "summary",
            "json",
            "markdown",
        ),
        default="summary",
        help="Report output format.",
    )

    parser.add_argument(
        "--output",
        help=("Optional file path. When omitted, the report is printed to stdout."),
    )

    return parser


def _render_output(
    report,
    *,
    output_format: OutputFormat,
) -> str:
    if output_format == "json":
        return report.model_dump_json(
            indent=2,
        )

    if output_format == "markdown":
        return render_markdown(report)

    return render_summary(report)


if __name__ == "__main__":
    main()
