import pytest

from hemera.exceptions import HemeraError
from hemera.types import HemeraHttpRequest, HemeraMetadata


def test_hemera_http_request_exceptions():
    """Test HemeraHttpRequest exceptions."""
    http_request = HemeraHttpRequest()

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request._get_property_value(source="header", keys=["invalid_key"])


def test_hemera_meta_data_exceptions():
    """Test HemeraMetadata exceptions."""
    hemera_meta_data = HemeraMetadata()

    with pytest.raises(HemeraError, match="Value not found in HemeraMetadata."):
        _ = hemera_meta_data.core
