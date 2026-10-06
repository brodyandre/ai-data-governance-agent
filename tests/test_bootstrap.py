"""Bootstrap tests for the AI Data Governance Agent project."""

from ai_data_governance_agent import __version__


def test_package_version_is_defined() -> None:
    """The project package must expose its expected initial version."""
    assert __version__ == "0.1.0"
