import pytest
from toml import load

from hemera.exceptions import HemeraError
from hemera.metadata import get_software_versions


def test_get_software_versions():
    """Test get_software_versions."""

    pyproject = load("pyproject.toml")

    assert get_software_versions("hemera") == {
        "hemera": pyproject["tool"]["poetry"]["version"]
    }

    with pytest.raises(HemeraError, match="Software versions not found."):
        _ = get_software_versions("nonexistent")
