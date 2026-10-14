"""Keep pytest fixture outputs inside the resolved owning repository."""
import tempfile
from pathlib import Path

def pytest_configure(config) -> None:
    """Use a unique repository-local fixture root without deleting prior test data."""
    if config.option.basetemp is None:
        repository = Path(__file__).resolve().parents[1]
        parent = repository / "work" / "test-runs"
        parent.mkdir(parents=True, exist_ok=True)
        config.option.basetemp = tempfile.mkdtemp(prefix="pytest-", dir=parent)
